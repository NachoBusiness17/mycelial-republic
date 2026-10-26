"""ldt_train — Z13: the LDT v0 baseline control (no lattice), pure numpy.

Mickey17 W3K lane (2026-09-29), Z12 manifest edge #1: "LDT TRAINING RUN on
W3k's 18k rows". This tool is the v0 FLOOR of that arc — the baseline the
later lattice-projection run must beat. What it deliberately is NOT:

  - No lattice projection, no typed binding, no atom-position structure.
    The whole point of v0 is to measure how far a FLAT bag-of-tokens view
    of the render gets: the state is an unordered multiset of token atoms
    (so "tgt:pool is dry" — a two-atom binding — is only learnable through
    hidden-layer feature interactions, not by construction).
  - No torch. Mission law for this lane is pure numpy (verified first:
    `pip show torch` reports 2.13.0 PRESENT in the venv; the lane card
    still says numpy-only, and numpy-only keeps the run byte-deterministic
    with zero CUDA variance). Softmax MLP + Adam, ~60k params.

Features (from tools/legality_dataset.py's flat token render):
  [STATE vector]   log1p token COUNTS over the train-split state-token
                   vocabulary (n:/k:/z:/v:/s:/sill:/p:/A>B/c:/sip:/o:/
                   cr:/pr: atoms), train-fit only, unseen atoms dropped.
  [ACTION onehot]  verb:V onehot ++ tgt:T onehot over the train-split
                   action vocabularies.
  -> 5-way label   illegal_unknown_verb / illegal_unknown_target /
                   illegal_dry_pool / legal_no_gain / legal_gain.

Abstain head (the Z12 card's "soundness by architecture", v0 form): max
softmax prob < --threshold (0.7) => ABSTAIN. On the answered (non-abstain)
set, soundness := correct / (correct + wrong), coverage := answered / N.

CLI: train on logs/legality_ds (18k/2k, dataset is byte-deterministic),
print per-class recall + abstain-adjusted soundness, save weights +
featurizer + config to models/legality_v0.npz. Determinism law: one
np.random.default_rng(seed) stream, no wall clock in outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Manifest label_set order (tools/legality_dataset.py) — fixed on purpose.
LABELS = ["illegal_unknown_verb", "illegal_unknown_target",
          "illegal_dry_pool", "legal_no_gain", "legal_gain"]
LABEL_TO_IDX = {lab: i for i, lab in enumerate(LABELS)}

MARKERS = {"[STATE]", "[ACTION]", "[LABEL]"}


# ------------------------------------------------------------- featurize ----
def split_tokens(tokens: list[str]) -> tuple[list[str], str | None, str | None]:
    """Render tokens -> (state atoms, verb token, tgt token). The label
    token and structural markers are dropped: they are targets, not inputs."""
    state: list[str] = []
    verb = tgt = None
    for tok in tokens:
        if tok in MARKERS:
            continue
        if tok.startswith("verb:"):
            verb = tok
        elif tok.startswith("tgt:"):
            tgt = tok
        elif tok in LABELS:
            continue
        else:
            state.append(tok)
    return state, verb, tgt


class Featurizer:
    """Bag-of-atoms encoder fitted on the TRAIN split only (no val leakage:
    val atoms outside the train vocab are silently dropped — that drop IS
    the honest flat-render baseline, an unseen atom is indistinguishable
    from an absent one)."""

    def __init__(self) -> None:
        self.state_vocab: list[str] = []
        self.verb_vocab: list[str] = []
        self.tgt_vocab: list[str] = []
        self._sidx: dict[str, int] = {}
        self._vidx: dict[str, int] = {}
        self._tidx: dict[str, int] = {}

    def fit(self, rows: list[dict]) -> "Featurizer":
        s_set: set[str] = set()
        v_set: set[str] = set()
        t_set: set[str] = set()
        for r in rows:
            state, verb, tgt = split_tokens(r["tokens"])
            s_set.update(state)
            if verb:
                v_set.add(verb)
            if tgt:
                t_set.add(tgt)
        # sorted => deterministic vocab regardless of row order
        self.state_vocab = sorted(s_set)
        self.verb_vocab = sorted(v_set)
        self.tgt_vocab = sorted(t_set)
        self._sidx = {t: i for i, t in enumerate(self.state_vocab)}
        self._vidx = {t: i for i, t in enumerate(self.verb_vocab)}
        self._tidx = {t: i for i, t in enumerate(self.tgt_vocab)}
        return self

    @property
    def dim(self) -> int:
        return len(self.state_vocab) + len(self.verb_vocab) + len(self.tgt_vocab)

    def transform(self, rows: list[dict]) -> np.ndarray:
        ds, dv, dt = (len(self.state_vocab), len(self.verb_vocab),
                      len(self.tgt_vocab))
        X = np.zeros((len(rows), ds + dv + dt), dtype=np.float32)
        for i, r in enumerate(rows):
            state, verb, tgt = split_tokens(r["tokens"])
            for tok in state:
                j = self._sidx.get(tok)
                if j is not None:
                    X[i, j] += 1.0
            if verb is not None and verb in self._vidx:
                X[i, ds + self._vidx[verb]] = 1.0
            if tgt is not None and tgt in self._tidx:
                X[i, ds + dv + self._tidx[tgt]] = 1.0
        # log1p compresses count range (0..~12) while keeping sparsity at 0
        X[:, :ds] = np.log1p(X[:, :ds])
        return X

    def vocab_arrays(self) -> dict[str, np.ndarray]:
        return {"state_vocab": np.array(self.state_vocab, dtype=object),
                "verb_vocab": np.array(self.verb_vocab, dtype=object),
                "tgt_vocab": np.array(self.tgt_vocab, dtype=object)}


def rows_xy(rows: list[dict], fe: Featurizer) -> tuple[np.ndarray, np.ndarray]:
    X = fe.transform(rows)
    y = np.array([LABEL_TO_IDX[r["label"]] for r in rows], dtype=np.int64)
    return X, y


# ------------------------------------------------------------------ model ----
def init_params(dim: int, hidden: list[int], n_classes: int, seed: int,
                ) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    dims = [dim, *hidden, n_classes]
    params: dict[str, np.ndarray] = {}
    for li in range(len(dims) - 1):
        fan_in, fan_out = dims[li], dims[li + 1]
        params[f"W{li}"] = (rng.standard_normal((fan_in, fan_out))
                            * np.sqrt(2.0 / fan_in)).astype(np.float32)
        params[f"b{li}"] = np.zeros(fan_out, dtype=np.float32)
    return params


def forward(params: dict[str, np.ndarray], X: np.ndarray,
            ) -> tuple[np.ndarray, list[np.ndarray]]:
    """Returns (softmax probs, activations per layer for backprop)."""
    acts = [X]
    n_layers = sum(1 for k in params if k.startswith("W"))
    for li in range(n_layers):
        z = acts[-1] @ params[f"W{li}"] + params[f"b{li}"]
        if li < n_layers - 1:
            z = np.maximum(z, 0.0)          # ReLU on hidden layers
        acts.append(z)
    logits = acts[-1]
    logits = logits - logits.max(axis=1, keepdims=True)
    probs = np.exp(logits)
    probs /= probs.sum(axis=1, keepdims=True)
    return probs, acts


def _adam_state(params: dict[str, np.ndarray]) -> dict[str, dict]:
    return {k: {"m": np.zeros_like(v), "v": np.zeros_like(v), "t": 0}
            for k, v in params.items()}


def train_model(X: np.ndarray, y: np.ndarray, hidden: list[int],
                epochs: int, lr: float, batch: int, seed: int,
                l2: float = 1e-4, log_every: int = 0,
                ) -> tuple[dict[str, np.ndarray], list[float]]:
    """Minibatch Adam on multinomial cross-entropy. Deterministic given
    seed (single rng drives init AND shuffling)."""
    n, dim = X.shape
    params = init_params(dim, hidden, len(LABELS), seed)
    opt = _adam_state(params)
    rng = np.random.default_rng(seed + 1)
    Y = np.eye(len(LABELS), dtype=np.float32)[y]
    n_layers = sum(1 for k in params if k.startswith("W"))
    losses: list[float] = []

    for epoch in range(epochs):
        order = rng.permutation(n)
        epoch_loss = 0.0
        n_batches = 0
        for start in range(0, n, batch):
            idx = order[start:start + batch]
            xb, yb = X[idx], Y[idx]
            probs, acts = forward(params, xb)
            eps = 1e-9
            epoch_loss += float(-np.mean(np.log(probs[np.arange(len(idx)), y[idx]] + eps)))
            n_batches += 1
            # backward: dlogits = (P - Y) / B, through ReLU layers
            grads: dict[str, np.ndarray] = {}
            delta = (probs - yb) / len(idx)
            for li in range(n_layers - 1, -1, -1):
                grads[f"W{li}"] = acts[li].T @ delta + l2 * params[f"W{li}"]
                grads[f"b{li}"] = delta.sum(axis=0)
                if li > 0:
                    delta = (delta @ params[f"W{li}"].T) * (acts[li] > 0)
            # Adam step
            for k, g in grads.items():
                st = opt[k]
                st["t"] += 1
                st["m"] = 0.9 * st["m"] + 0.1 * g
                st["v"] = 0.999 * st["v"] + 0.001 * (g * g)
                m_hat = st["m"] / (1 - 0.9 ** st["t"])
                v_hat = st["v"] / (1 - 0.999 ** st["t"])
                params[k] -= lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        losses.append(epoch_loss / max(n_batches, 1))
        if log_every and (epoch + 1) % log_every == 0:
            print(f"epoch {epoch + 1}/{epochs} loss={losses[-1]:.4f}")
    return params, losses


def subset_rows(rows: list[dict], fraction: float, seed: int = 13) -> list[dict]:
    """AH8 data-scaling axis (2026-09-30): deterministic subsample of the
    train split. One `np.random.default_rng(seed)` permutation, first
    round(fraction*n) rows, returned in original file order. fraction=1.0
    returns a copy unchanged (so the 100% arm is byte-identical to Z13's
    full-data recipe and must reproduce its frozen numbers). PARITY LAW:
    every arm of an experiment must eat the SAME subset — call this once
    per fraction and pass the result around, never re-roll per arm."""
    if not 0.0 < fraction <= 1.0:
        raise ValueError(f"fraction must be in (0, 1], got {fraction!r}")
    if fraction == 1.0:
        return list(rows)
    n = len(rows)
    k = max(1, int(round(fraction * n)))
    order = sorted(np.random.default_rng(seed).permutation(n)[:k])
    return [rows[i] for i in order]


def train_model_gated(X: np.ndarray, y_elem: np.ndarray, n_out: int,
                      gate: np.ndarray, hidden: list[int], epochs: int,
                      lr: float, batch: int, seed: int, l2: float = 1e-4,
                      log_every: int = 0,
                      ) -> tuple[dict[str, np.ndarray], list[float]]:
    """AH8 v1 generalization of train_model: cross-entropy to a TARGET
    ELEMENT under a per-row boolean output GATE (the differentiable mask).
    The lattice (tools/ldt_lattice.py) supplies the gate; this function
    stays lattice-agnostic — it only knows "output elements may be
    structurally impossible for a given row, and their gradients must be
    exactly zero there".

    Math: gating the softmax and renormalizing within the gate gives
    p_j = g_j*exp(z_j)/sum_k g_k*exp(z_k), so gated-OUT elements carry
    p_j = 0 and dL/dz_j = p_j - 1[j==t] = 0 — the gate is self-enforcing;
    the explicit `* gate` on the delta is belt-and-braces (and pins the
    law for the reader). Training therefore optimizes exactly the
    renormalized-within-mask quantity that renorm-mode inference reads:
    the deployment metric IS the training objective (that alignment is
    AE2's whole steal).

    train_model above stays UNTOUCHED on purpose: it is the frozen v0
    control whose byte-behavior Z13's receipt pins (0.8545 val / 0.8830
    soundness); this is its generalization, not a refactor of it. Same
    rng discipline (init stream `seed`, shuffle stream `seed+1`), same
    Adam constants, same l2 — so a gate of all-ones with n_out=5 and
    y_elem=y reproduces train_model's training dynamics exactly."""
    n, dim = X.shape
    if gate.shape != (n, n_out):
        raise ValueError(f"gate shape {gate.shape} != {(n, n_out)}")
    params = init_params(dim, hidden, n_out, seed)
    opt = _adam_state(params)
    rng = np.random.default_rng(seed + 1)
    T = np.eye(n_out, dtype=np.float32)[y_elem]
    G = gate.astype(np.float32)
    n_layers = sum(1 for k in params if k.startswith("W"))
    losses: list[float] = []
    last = n_layers - 1

    for epoch in range(epochs):
        order = rng.permutation(n)
        epoch_loss = 0.0
        n_batches = 0
        for start in range(0, n, batch):
            idx = order[start:start + batch]
            xb, tb, gb = X[idx], T[idx], G[idx]
            probs, acts = forward(params, xb)
            probs = renormalize_gated(probs, gb)
            eps = 1e-9
            epoch_loss += float(-np.mean(np.log(
                probs[np.arange(len(idx)), y_elem[idx]] + eps)))
            n_batches += 1
            # backward: gated-out columns carry p_j=0 and target 0, so
            # delta is exactly 0 there — gradients never leave the mask
            delta = ((probs - tb) * gb) / len(idx)
            grads: dict[str, np.ndarray] = {}
            for li in range(n_layers - 1, -1, -1):
                grads[f"W{li}"] = acts[li].T @ delta + l2 * params[f"W{li}"]
                grads[f"b{li}"] = delta.sum(axis=0)
                if li > 0:
                    delta = (delta @ params[f"W{li}"].T) * (acts[li] > 0)
            for k, g in grads.items():
                st = opt[k]
                st["t"] += 1
                st["m"] = 0.9 * st["m"] + 0.1 * g
                st["v"] = 0.999 * st["v"] + 0.001 * (g * g)
                m_hat = st["m"] / (1 - 0.9 ** st["t"])
                v_hat = st["v"] / (1 - 0.999 ** st["t"])
                params[k] -= lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        losses.append(epoch_loss / max(n_batches, 1))
        if log_every and (epoch + 1) % log_every == 0:
            print(f"epoch {epoch + 1}/{epochs} loss={losses[-1]:.4f}")
    return params, losses


def renormalize_gated(probs: np.ndarray, gate: np.ndarray) -> np.ndarray:
    """Softmax mass renormalized inside the gate: p_j * g_j / sum_k(p_k*g_k).
    THE one renorm op shared by v1 training and v1 inference (lattice_
    gate -> renormalize_gated is the whole learned-concept-layer pipeline;
    keeping it here means the trainer and the evaluator cannot drift)."""
    masked = probs * gate
    return masked / np.maximum(masked.sum(axis=1, keepdims=True), 1e-12)


# ------------------------------------------------------------------ eval ----
def evaluate(params: dict[str, np.ndarray], X: np.ndarray, y: np.ndarray,
             threshold: float = 0.7) -> dict:
    """Accuracy per class + abstain-adjusted soundness.

    soundness := correct / (correct + wrong) over non-abstained rows
    (max prob >= threshold); coverage := non-abstained / N. A row below
    threshold is an ABSTAIN — never counted as wrong."""
    probs, _ = forward(params, X)
    pred = probs.argmax(axis=1)
    pmax = probs.max(axis=1)
    correct = pred == y

    per_class = {}
    for c, name in enumerate(LABELS):
        mask = y == c
        supp = int(mask.sum())
        per_class[name] = {
            "support": supp,
            "recall": float(correct[mask].mean()) if supp else float("nan"),
            "answered_frac": float((pmax[mask] >= threshold).mean()) if supp else float("nan"),
        }

    answered = pmax >= threshold
    n_ans = int(answered.sum())
    n_corr = int((correct & answered).sum())
    return {
        "n": len(y),
        "accuracy": float(correct.mean()),
        "per_class": per_class,
        "threshold": threshold,
        "coverage": n_ans / len(y) if len(y) else 0.0,
        "answered": n_ans,
        "answered_correct": n_corr,
        "answered_wrong": n_ans - n_corr,
        "soundness": (n_corr / n_ans) if n_ans else float("nan"),
        "abstained_correct_rate": (float(correct[~answered].mean())
                                   if (~answered).any() else float("nan")),
    }


# ------------------------------------------------------------------ disk ----
def save_npz(path: Path, params: dict[str, np.ndarray], fe: Featurizer,
             config: dict, labels: list[str] | None = None) -> None:
    """labels defaults to the 5-way LABELS; AH8's v1 32-element head passes
    its own element names so a reloaded head is self-describing."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {**params, **fe.vocab_arrays(),
               "labels": np.array(labels if labels is not None else LABELS,
                                  dtype=object),
               "config_json": np.array(json.dumps(config, sort_keys=True))}
    np.savez_compressed(path, **payload)


def load_npz(path: Path) -> tuple[dict[str, np.ndarray], Featurizer, dict]:
    data = np.load(path, allow_pickle=True)
    fe = Featurizer()
    fe.state_vocab = [str(t) for t in data["state_vocab"]]
    fe.verb_vocab = [str(t) for t in data["verb_vocab"]]
    fe.tgt_vocab = [str(t) for t in data["tgt_vocab"]]
    fe._sidx = {t: i for i, t in enumerate(fe.state_vocab)}
    fe._vidx = {t: i for i, t in enumerate(fe.verb_vocab)}
    fe._tidx = {t: i for i, t in enumerate(fe.tgt_vocab)}
    params = {k: data[k] for k in data.files if k[0] in "Wb" and len(k) == 2}
    return params, fe, json.loads(str(data["config_json"]))


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


# ------------------------------------------------------------------- cli ----
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path, default=ROOT / "logs" / "legality_ds")
    ap.add_argument("--out", type=Path, default=ROOT / "models" / "legality_v0.npz")
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--hidden", default="128,64")
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--l2", type=float, default=1e-4)
    args = ap.parse_args(argv)

    hidden = [int(h) for h in args.hidden.split(",")]
    train_rows = load_jsonl(args.data / "train.jsonl")
    val_rows = load_jsonl(args.data / "val.jsonl")
    train_sha = hashlib.sha256((args.data / "train.jsonl").read_bytes()).hexdigest()

    fe = Featurizer().fit(train_rows)
    Xtr, ytr = rows_xy(train_rows, fe)
    Xva, yva = rows_xy(val_rows, fe)
    print(f"train={Xtr.shape} val={Xva.shape} "
          f"(state|verb|tgt = {len(fe.state_vocab)}|{len(fe.verb_vocab)}|{len(fe.tgt_vocab)})")

    params, losses = train_model(Xtr, ytr, hidden, args.epochs, args.lr,
                                 args.batch, args.seed, l2=args.l2,
                                 log_every=10)
    metrics = evaluate(params, Xva, yva, threshold=args.threshold)
    tr_metrics = evaluate(params, Xtr, ytr, threshold=args.threshold)

    print(f"\nval accuracy: {metrics['accuracy']:.4f} "
          f"(train {tr_metrics['accuracy']:.4f}, final loss {losses[-1]:.4f})")
    for name in LABELS:
        pc = metrics["per_class"][name]
        print(f"  {name:24s} support={pc['support']:5d} "
              f"recall={pc['recall']:.4f} answered={pc['answered_frac']:.3f}")
    print(f"abstain@p>={args.threshold}: coverage={metrics['coverage']:.4f} "
          f"answered={metrics['answered']} "
          f"(correct {metrics['answered_correct']} / wrong {metrics['answered_wrong']})")
    print(f"soundness = {metrics['soundness']:.4f}   "
          f"accuracy-if-abstained-were-right-guess={metrics['abstained_correct_rate']:.4f}")

    config = {"schema": "ldt_v0.npz", "train_sha256": train_sha,
              "n_train": len(train_rows), "n_val": len(val_rows),
              "hidden": hidden, "epochs": args.epochs, "lr": args.lr,
              "batch": args.batch, "seed": args.seed, "l2": args.l2,
              "threshold": args.threshold, "feature_dim": fe.dim,
              "state_transform": "log1p_counts", "labels": LABELS,
              "val_metrics": {k: v for k, v in metrics.items()
                              if k != "per_class"}}
    save_npz(args.out, params, fe, config)
    print(f"\nsaved: {args.out} "
          f"({sum(v.size for v in params.values())} weight elements)")
    print(json.dumps({"val": {k: round(v, 4) if isinstance(v, float) else v
                              for k, v in metrics.items() if k != "per_class"}},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
