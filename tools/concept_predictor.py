"""concept_predictor — AF1 (2026-09-30) + AH16 grouped-split redesign.

AF1 built the estate's first next-CONCEPT predictor (AE6's implied build:
the Z13 ldt_train.py numpy-MLP shape on memory/percolator/explore.jsonl
instead of token renders) and banked a named data fact: all 119
recurring-canonical occurrences sit strictly in the train era, the
chronological tail is pure behavioral novelty, so the canonical head
scored 0 in-vocab holdout rows = UNSCORABLE (a data fact, not a model
failure). AH16 redesigns the split so the canonical question is
answerable without abandoning the honest forecast game: every head now
reports TWO splits.

GROUPED (AH16)  hold out a seeded random 15% of RECURRING groups of the
                window's KEY (the conditioning event: canonical groups
                for the canonical head, lane groups for the lane head),
                each held group's key-windows across its full timeline.
                Key-side by design: grouping by TARGET canonical would
                move every window whose truth is a held-out canon out of
                training, and a class with zero training rows is
                unnameable by construction (0.000 for both predictors, a
                protocol ceiling, not a measurement). Key-side grouping
                keeps every recurring canon a trained, nameable class on
                both sides — the 73/119 rec->rec chain keeps its edges in
                train — while the unseen-canon pressure moves to the
                conditioning side. The featurizer fits only on events
                covered by train windows (context + target, no peeking).
CHRONO (AF1)    the time tail (last 15%), labeled novelty-forecast: the
                honest answer may remain 0 there.

DATA      (ts, source, domain, canonical, lane) events ordered by ts.
FEATURES  one-hot (source_norm | domain | canonical | lane) for each of the
          last K=8 events ++ 3h hour bucket of the newest event. All vocabs
          are fit on the TRAIN side only; unseen values drop to the 'other'
          bucket (cold-start honesty, same law as ldt_train's featurizer).
TARGETS   (1) next canonical: the exact-canonical target is UUID-guessing
          over the full stream (2026-09-30 data: 1,826 uniques / 1,916
          rows, only 29 recur), so the candidate vocab is the train-side
          recurring canonicals (>= 2 train targets). (2) next lane, over
          the lane-bearing subsequence (the AC10 lane-chooser game).
          Both heads, both splits use ONE scoring protocol: every holdout
          window scores; a truth outside the train-fit vocab is a miss for
          every predictor (MLP y = -1, baseline candidates exclude it);
          n_in_vocab reports how many rows were winnable at all.
BASELINE  frequency predictor: most-common next item given current item
          (bigram counts, deterministic (-count, name) ranking, unigram
          backoff + padding). The MLP must BEAT it on the scored holdout
          or the AE6 falsifier fires; losing to baseline is a valid result.
MODEL     ldt_train.py's exact numpy MLP pattern (ReLU MLP + stable softmax +
          minibatch Adam + l2, one rng stream for init AND shuffling, no
          torch, no deps beyond numpy). Each cell = one independent model.

PARITY    For each cell the baseline and the MLP see identical training
          windows, choose among the identical candidate vocab, and are
          scored on the identical holdout rows.

CLI       Trains both heads x both splits, prints the per-cell blocks + the
          4-cell table + one JSON verdict line, saves weights to
          models/concept_predictor.npz (schema concept_predictor_v1).
          Exit 0 whatever the verdict: a fired falsifier is a result, not
          an error. Runtime budget 300s (AH16 mission cap).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HOUR_BUCKETS = 8  # 24h / 3h buckets


# ------------------------------------------------------------------- data ----
def normalize_source(raw: str | None) -> str:
    """Collapse the high-cardinality source field (fuel:<hash>, ox:t0042,
    OX_RESIDENT_..., moderation:...) into a small set of stream classes."""
    s = (raw or "").strip()
    if not s:
        return "unknown"
    if s.startswith("fuel:"):
        return "fuel"
    low = s.lower()
    if low.startswith("ox:"):
        return "ox"
    if low.startswith("ox_resident"):
        return "ox_resident"
    if low.startswith("moderation:"):
        return "moderation"
    return s


def hour_bucket(ts: str) -> int:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.hour * HOUR_BUCKETS // 24


def load_events(path: Path) -> list[dict]:
    """jsonl -> event dicts sorted by ts. Rows without ts+canonical are
    dropped (a row with no canonical carries no concept to predict)."""
    events: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            ts, canon = r.get("ts"), r.get("canonical")
            if not ts or not canon:
                continue
            events.append({
                "ts": ts,
                "source": normalize_source(r.get("source")),
                "domain": r.get("domain") or "unknown",
                "canonical": canon,
                "lane": (r.get("lane") or "").strip(),
                "hour": hour_bucket(ts),
            })
    events.sort(key=lambda e: e["ts"])  # stable; file is already ts-ordered
    return events


def lane_bearing(events: list[dict]) -> list[dict]:
    """The lane subsequence: rows the percolator actually routed to a lane."""
    return [e for e in events if e["lane"] not in ("", "none")]


def make_windows(events: list[dict], k: int) -> list[tuple[list[dict], dict]]:
    """(context, target) for every target index j >= k. Context is strictly
    before the target (no peeking). Window i corresponds to j = k + i."""
    return [(events[j - k:j], events[j]) for j in range(k, len(events))]


# --------------------------------------------------------------- features ----
class SequenceFeaturizer:
    """One-hot encoder for K-event context windows, fit on TRAIN events only.
    Layout per event slot (oldest -> newest): source | domain | canonical |
    lane one-hots; then the 3h hour bucket of the newest event."""

    def __init__(self, src_top: int = 24, canon_top: int = 64) -> None:
        self.src_top = src_top
        self.canon_top = canon_top
        self.src_vocab: list[str] = []
        self.domain_vocab: list[str] = []
        self.canon_vocab: list[str] = []
        self.lane_vocab: list[str] = []

    def _top(self, counts: Counter, cap: int) -> list[str]:
        ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return [t for t, _ in ranked[:cap]]

    def fit(self, train_events: list[dict]) -> "SequenceFeaturizer":
        src = Counter(e["source"] for e in train_events)
        dom = Counter(e["domain"] for e in train_events)
        can = Counter(e["canonical"] for e in train_events)
        lan = Counter(e["lane"] or "nolane" for e in train_events)
        self.src_vocab = self._top(src, self.src_top) + ["other"]
        self.domain_vocab = self._top(dom, 10**9) + ["other"]
        self.canon_vocab = self._top(can, self.canon_top) + ["other"]
        self.lane_vocab = self._top(lan, 10**9) + ["other"]
        return self

    @property
    def slot(self) -> int:
        return (len(self.src_vocab) + len(self.domain_vocab)
                + len(self.canon_vocab) + len(self.lane_vocab))

    def transform(self, windows: list[tuple[list[dict], dict]], k: int) -> np.ndarray:
        """Output width = k * slot + HOUR_BUCKETS (slot = the four one-hot
        blocks per event). k is passed here, not at fit, so one featurizer
        can serve any window size over its fitted vocabs."""
        sD, dD = 0, len(self.src_vocab)
        cD = dD + len(self.domain_vocab)
        lD = cD + len(self.canon_vocab)
        slot = lD + len(self.lane_vocab)
        X = np.zeros((len(windows), k * slot + HOUR_BUCKETS), dtype=np.float32)
        sidx = {t: i for i, t in enumerate(self.src_vocab)}
        didx = {t: i for i, t in enumerate(self.domain_vocab)}
        cidx = {t: i for i, t in enumerate(self.canon_vocab)}
        lidx = {t: i for i, t in enumerate(self.lane_vocab)}
        for i, (ctx, _tgt) in enumerate(windows):
            for pos, ev in enumerate(ctx):  # pos 0 = oldest
                base = pos * slot
                X[i, base + sidx.get(ev["source"], sidx["other"])] = 1.0
                # domain block starts at dD, NOT sD: the first cut used sD
                # (=0, the source block start), silently overwriting every
                # source one-hot with the domain one-hot. Caught by the
                # tests' 4-per-event one-hot count invariant (13 != 17 lit
                # columns per window) before any result was banked.
                X[i, base + dD + didx.get(ev["domain"], didx["other"])] = 1.0
                X[i, base + cD + cidx.get(ev["canonical"], cidx["other"])] = 1.0
                X[i, base + lD + lidx.get(ev["lane"] or "nolane",
                                           lidx["other"])] = 1.0
            X[i, k * slot + ctx[-1]["hour"]] = 1.0
        return X

    def vocab_arrays(self) -> dict[str, np.ndarray]:
        return {"src_vocab": np.array(self.src_vocab, dtype=object),
                "domain_vocab": np.array(self.domain_vocab, dtype=object),
                "canon_feat_vocab": np.array(self.canon_vocab, dtype=object),
                "lane_feat_vocab": np.array(self.lane_vocab, dtype=object)}


# --------------------------------------------------------------- baseline ----
class FrequencyPredictor:
    """The mission baseline: most-common next item given current item.
    Bigram counts ranked by (-count, name); unseen key falls back to the
    unigram ranking; top-k is padded from the unigram ranking without
    duplicates. Candidate filtering keeps the baseline choosing among the
    same vocab the MLP's softmax spans (parity law)."""

    def __init__(self) -> None:
        self.bigram: dict[str, Counter] = {}
        self.unigram: Counter = Counter()

    def fit(self, pairs: list[tuple[str, str]]) -> "FrequencyPredictor":
        for key, tgt in pairs:
            self.bigram.setdefault(key, Counter())[tgt] += 1
            self.unigram[tgt] += 1
        return self

    def _rank(self, items: list[tuple[str, int]],
              seen: set[str]) -> list[str]:
        items.sort(key=lambda x: (-x[1], x[0]))
        return [t for t, _ in items if t not in seen]

    def topk(self, key: str, k: int,
             candidates: set[str] | None = None) -> list[str]:
        seen: set[str] = set()
        ranked: list[str] = []
        cnt = self.bigram.get(key)
        if cnt:
            ranked += self._rank([(t, c) for t, c in cnt.items()
                                  if candidates is None or t in candidates],
                                 seen)
            seen.update(ranked)
        uni = self._rank([(t, c) for t, c in self.unigram.items()
                          if candidates is None or t in candidates], seen)
        ranked += uni
        return ranked[:k]

    def accuracy(self, pairs: list[tuple[str, str]], k: int,
                 candidates: set[str] | None = None) -> float:
        if not pairs:
            return float("nan")
        hits = sum(1 for key, truth in pairs
                   if truth in self.topk(key, k, candidates))
        return hits / len(pairs)

    def unigram_accuracy(self, pairs: list[tuple[str, str]], k: int,
                         candidates: set[str] | None = None) -> float:
        if not pairs:
            return float("nan")
        top = self.topk("", k, candidates)  # unseen key => pure unigram rank
        return sum(1 for _k, truth in pairs if truth in top) / len(pairs)


# ------------------------------------------------------------------ model ----
# ldt_train.py's numpy MLP, generalized over n_classes (LABELS was the only
# hard-coded part there). Same init, same stable softmax, same Adam.
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


def train_mlp(X: np.ndarray, y: np.ndarray, n_classes: int,
              hidden: list[int], epochs: int, lr: float, batch: int, seed: int,
              l2: float = 1e-4, log_every: int = 0,
              ) -> tuple[dict[str, np.ndarray], list[float]]:
    """Minibatch Adam on multinomial cross-entropy. Deterministic given
    seed (one rng drives init AND shuffling)."""
    n, dim = X.shape
    params = init_params(dim, hidden, n_classes, seed)
    opt = _adam_state(params)
    rng = np.random.default_rng(seed + 1)
    Y = np.eye(n_classes, dtype=np.float32)[y]
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
            epoch_loss += float(-np.mean(np.log(
                probs[np.arange(len(idx)), y[idx]] + eps)))
            n_batches += 1
            grads: dict[str, np.ndarray] = {}
            delta = (probs - yb) / len(idx)
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


def mlp_topk_accuracy(params: dict[str, np.ndarray], X: np.ndarray,
                      y: np.ndarray, k: int) -> float:
    """y == -1 marks an OOV truth: it can never be hit (class ids are >= 0),
    so an OOV row scores wrong for the MLP exactly as it does for the
    baseline whose candidates exclude it."""
    if len(X) == 0:
        return float("nan")
    probs, _ = forward(params, X)
    top = np.argsort(-probs, axis=1)[:, :k]
    return float(np.mean(np.any(top == y[:, None], axis=1)))


# ------------------------------------------------------------- orchestration --
def chrono_train_mask(events: list[dict], windows: int, k: int,
                      holdout: float) -> tuple[list[bool], dict]:
    """AF1's split, unchanged (regression law: same seed must reproduce the
    AF1 numbers modulo live data appends): train = windows whose TARGET
    event index k+i falls before the event-index cut."""
    cut = int(len(events) * (1 - holdout))
    mask = [(k + i) < cut for i in range(windows)]
    return mask, {"split": "chrono", "cut_event_index": cut, "held_groups": []}


def grouped_train_mask(windows: list[tuple[list[dict], dict]], field: str,
                       holdout: float, seed: int, group_min: int,
                       held_override: set[str] | None,
                       ) -> tuple[list[bool], dict]:
    """AH16's split: hold out a seeded random 15% (rounded, >=1) of the
    RECURRING key-groups — keys occurring >= group_min times among window
    keys — and move EVERY window keyed by a held group to the holdout,
    across its full timeline (indices are scattered, not a tail). Key-side
    by design (module docstring): target-side grouping would strip every
    training row of a held canon, making it unnameable by construction."""
    keys = [ctx[-1][field] for ctx, _tgt in windows]
    counts = Counter(keys)
    recurring = sorted(kk for kk, c in counts.items() if c >= group_min)
    if held_override is not None:
        unknown = held_override - set(recurring)
        if unknown:  # fail loud: a pinned rerun naming a non-recurring or
            # misspelled group must not silently hold nothing (empty
            # holdout reads as UNSCORABLE, a fabricated non-result).
            raise ValueError(f"held_override names non-recurring groups "
                             f"for field {field!r}: {sorted(unknown)}")
        held = set(held_override)
    else:
        n_held = max(1, round(len(recurring) * holdout)) if recurring else 0
        rng = np.random.default_rng(seed)
        pick = (rng.choice(len(recurring), size=n_held, replace=False)
                if n_held else [])
        held = {recurring[j] for j in pick}
    mask = [kk not in held for kk in keys]
    meta = {"split": "grouped", "held_groups": sorted(held),
            "n_recurring_groups": len(recurring)}
    return mask, meta


def fit_event_mask(n_events: int, train_idx: list[int], k: int) -> np.ndarray:
    """Events a train window actually sees: window i (target event k+i)
    covers event indices i .. k+i inclusive (its k context events + its
    target). The featurizer may fit ONLY on covered events — for the chrono
    split this reduces exactly to events[:cut] (AF1's fit, verbatim)."""
    covered = np.zeros(n_events, dtype=bool)
    for i in train_idx:
        covered[i:k + i + 1] = True
    return covered


def _verdict(m1: float, b1: float, n_scored: int,
             n_in_vocab: int) -> str:
    if n_scored == 0:
        return "UNSCORABLE: empty holdout"
    if n_in_vocab == 0:
        return ("UNSCORABLE: no in-vocab truths in holdout "
                "(falsifier stands, no evidence either way)")
    if not (m1 == m1 and b1 == b1):  # NaN guard
        return "UNSCORABLE: NaN metric"
    if m1 > b1:
        return "MLP BEATS baseline"
    if m1 < b1:
        return "FALSIFIER FIRES: MLP loses to baseline"
    return "TIE"


def run_cell(label: str, events: list[dict], field: str,
             min_count: int | None, split: str, args,
             held_override: set[str] | None = None) -> dict:
    """Train + score one head on ONE split (a table cell). min_count sets
    the recurring-vocab policy: None (lane) = every train truth is a
    candidate; >=2 (canonical) = only recurring canonicals are candidates.
    The featurizer fits ONLY on events covered by train windows (context +
    target, no peeking); for the chrono split that coverage is exactly
    events[:cut], preserving AF1's fit verbatim."""
    k = args.k
    windows = make_windows(events, k)
    if split == "chrono":
        mask, meta = chrono_train_mask(events, len(windows), k, args.holdout)
    elif split == "grouped":
        mask, meta = grouped_train_mask(windows, field, args.holdout,
                                        args.seed, args.group_min_count,
                                        held_override)
    else:
        raise ValueError(f"unknown split {split!r}")
    train_idx = [i for i, m in enumerate(mask) if m]
    scored_rows = [i for i, m in enumerate(mask) if not m]

    # fit-events law: only events a train window actually sees (its context
    # or its target). Window i covers event indices i .. k+i inclusive.
    covered = fit_event_mask(len(events), train_idx, k)
    fit_events = [e for e, c in zip(events, covered) if c]

    fe = SequenceFeaturizer(args.src_top, args.canon_feat_top).fit(fit_events)
    X = fe.transform(windows, k)
    truths = [tgt[field] for _ctx, tgt in windows]
    keys = [ctx[-1][field] for ctx, _tgt in windows]

    train_counts = Counter(truths[i] for i in train_idx)
    vocab = sorted((t for t, c in train_counts.items()
                    if c >= (min_count or 1)),
                   key=lambda t: (-train_counts[t], t))
    y_idx = {t: i for i, t in enumerate(vocab)}
    cands = set(vocab)

    train_rows = [i for i in train_idx if truths[i] in cands]
    # Unified scoring protocol (fixed in AF1 after the first run scored
    # 0/287: all 29 recurring canonicals' 119 occurrences sit strictly in
    # the train era, so an in-vocab-only chronological holdout scored
    # NOTHING). Both splits score every holdout window; an OOV truth is a
    # miss for every predictor (the MLP's y is -1, the baseline's
    # candidates exclude it), and n_in_vocab reports winnable rows.
    n_in_vocab = sum(1 for i in scored_rows if truths[i] in cands)

    if not train_rows:
        verdict = "UNSCORABLE: no trainable rows"
        return {"label": label, **meta, "n_events": len(events),
                "n_train_windows": 0, "n_holdout_windows": len(scored_rows),
                "n_scored": len(scored_rows), "n_in_vocab": n_in_vocab,
                "vocab": vocab, "uni_top1": float("nan"),
                "uni_top3": float("nan"), "base_top1": float("nan"),
                "base_top3": float("nan"), "mlp_top1": float("nan"),
                "mlp_top3": float("nan"), "mlp_train_top1": float("nan"),
                "first_loss": float("nan"), "last_loss": float("nan"),
                "verdict": verdict, "_params": {}, "_fe": fe}

    Xtr = X[train_rows]
    ytr = np.array([y_idx[truths[i]] for i in train_rows], dtype=np.int64)
    pairs_tr = [(keys[i], truths[i]) for i in train_rows]
    pairs_ho = [(keys[i], truths[i]) for i in scored_rows]
    yho = np.array([y_idx.get(truths[i], -1) for i in scored_rows],
                   dtype=np.int64)

    base = FrequencyPredictor().fit(pairs_tr)
    hidden = [int(h) for h in args.hidden.split(",")]
    params, losses = train_mlp(Xtr, ytr, len(vocab), hidden, args.epochs,
                               args.lr, args.batch, args.seed, l2=args.l2)

    m1 = mlp_topk_accuracy(params, X[scored_rows], yho, 1)
    m3 = mlp_topk_accuracy(params, X[scored_rows], yho, 3)
    b1 = base.accuracy(pairs_ho, 1, cands)
    b3 = base.accuracy(pairs_ho, 3, cands)
    u1 = base.unigram_accuracy(pairs_ho, 1, cands)
    u3 = base.unigram_accuracy(pairs_ho, 3, cands)

    return {
        "label": label, **meta, "n_events": len(events),
        "n_train_windows": len(train_rows),
        "n_holdout_windows": len(scored_rows),
        "n_scored": len(scored_rows), "n_in_vocab": n_in_vocab,
        "vocab": vocab,
        "uni_top1": u1, "uni_top3": u3, "base_top1": b1, "base_top3": b3,
        "mlp_top1": m1, "mlp_top3": m3,
        "mlp_train_top1": mlp_topk_accuracy(params, Xtr, ytr, 1),
        "first_loss": losses[0], "last_loss": losses[-1],
        "verdict": _verdict(m1, b1, len(scored_rows), n_in_vocab),
        "_params": params, "_fe": fe,
    }


def save_npz(path: Path, results: list[dict], config: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, np.ndarray] = {}
    for res in results:
        head = res["label"].replace("-", "_")
        for k, v in res["_params"].items():
            payload[f"{head}_{k}"] = v
        payload[f"{head}_target_vocab"] = np.array(res["vocab"],
                                                   dtype=object)
        for name, arr in res["_fe"].vocab_arrays().items():
            payload[f"{head}_{name}"] = arr
    payload["config_json"] = np.array(json.dumps(config, sort_keys=True))
    np.savez_compressed(path, **payload)


def _fmt(x: float) -> str:
    return "  nan " if x != x else f"{x:.3f}"


# ------------------------------------------------------------------- cli ----
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path,
                    default=ROOT / "memory" / "percolator" / "explore.jsonl")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "models" / "concept_predictor.npz")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--holdout", type=float, default=0.15)
    ap.add_argument("--epochs", type=int, default=80)
    ap.add_argument("--hidden", default="128,64")
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--l2", type=float, default=1e-4)
    ap.add_argument("--canon-min-count", type=int, default=2)
    ap.add_argument("--group-min-count", type=int, default=2,
                    help="a window KEY is a recurring group at >= this many "
                         "occurrences among keys (grouped split)")
    ap.add_argument("--canon-feat-top", type=int, default=64)
    ap.add_argument("--src-top", type=int, default=24)
    args = ap.parse_args(argv)

    t0 = time.perf_counter()
    data_sha = hashlib.sha256(args.data.read_bytes()).hexdigest()
    events = load_events(args.data)
    lane_events = lane_bearing(events)
    print(f"data: {args.data} sha256={data_sha[:12]} "
          f"rows={len(events)} lane_bearing={len(lane_events)} "
          f"(unique canonicals={len(set(e['canonical'] for e in events))})")

    cells = [  # the AH16 4-cell table: 2 heads x 2 splits
        ("next-canonical", events, "canonical", args.canon_min_count,
         "grouped"),
        ("next-canonical", events, "canonical", args.canon_min_count,
         "chrono"),
        ("next-lane", lane_events, "lane", None, "grouped"),
        ("next-lane", lane_events, "lane", None, "chrono"),
    ]
    results = [run_cell(f"{head}-{sp}", ev, field, mc, sp, args)
               for head, ev, field, mc, sp in cells]

    print()
    for r in results:
        held = (f"  held_groups={r['held_groups']}"
                if r.get("held_groups") else "")
        print(f"target={r['label']}  split={r['split']}  "
              f"vocab={len(r['vocab'])}  "
              f"train_windows={r['n_train_windows']}{held}")
        print(f"  scored={r['n_scored']} (in-vocab truths: "
              f"{r['n_in_vocab']})")
        print(f"  predictor   top1     top3")
        print(f"  unigram    {_fmt(r['uni_top1'])}   {_fmt(r['uni_top3'])}")
        print(f"  baseline   {_fmt(r['base_top1'])}   {_fmt(r['base_top3'])}")
        print(f"  mlp        {_fmt(r['mlp_top1'])}   {_fmt(r['mlp_top3'])}"
              f"   (train@1 {_fmt(r['mlp_train_top1'])}, "
              f"loss {_fmt(r['first_loss'])}->{_fmt(r['last_loss'])})")
        d1 = r["mlp_top1"] - r["base_top1"]
        d3 = r["mlp_top3"] - r["base_top3"]
        print(f"  verdict: {r['verdict']} "
              f"(top1 {d1:+.3f}, top3 {d3:+.3f})\n")

    split_tag = {"grouped": "grouped (AH16)",
                 "chrono": "chrono (novelty-forecast)"}
    print("4-cell table (holdout top-1 / top-3):")
    print("| head           | split                      | n (in-vocab) "
          "| baseline     | MLP          | verdict |")
    print("|----------------|-----------------------------|--------------"
          "|--------------|--------------|---------|")
    for r in results:
        head = r["label"].rsplit("-", 1)[0]
        print(f"| {head:<14} | {split_tag[r['split']]:<26} | "
              f"{r['n_scored']:>3} ({r['n_in_vocab']:>3})    | "
              f"{_fmt(r['base_top1'])} / {_fmt(r['base_top3'])} | "
              f"{_fmt(r['mlp_top1'])} / {_fmt(r['mlp_top3'])} | "
              f"{r['verdict']} |")

    gc = next(r for r in results if r["label"] == "next-canonical-grouped")
    if "BEATS" in gc["verdict"]:
        signal = ("PRESENT: MLP beats the frequency baseline on the grouped "
                  "canonical split")
    elif "FALSIFIER" in gc["verdict"]:
        signal = ("ABSENT: baseline >= MLP on the grouped canonical split "
                  "(falsifier fired)")
    else:
        signal = f"NO EVIDENCE: grouped canonical cell {gc['verdict']}"
    print(f"canonical signal under recurrence representation: {signal}\n")

    elapsed = time.perf_counter() - t0
    config = {"schema": "concept_predictor_v1", "data_sha256": data_sha,
              "n_events": len(events), "k": args.k,
              "holdout": args.holdout, "epochs": args.epochs,
              "hidden": args.hidden, "lr": args.lr, "batch": args.batch,
              "seed": args.seed, "l2": args.l2,
              "canon_min_count": args.canon_min_count,
              "group_min_count": args.group_min_count,
              "elapsed_s": round(elapsed, 2),
              "canonical_signal": signal,
              "cells": {r["label"]: {k: v for k, v in r.items()
                                     if not k.startswith("_")}
                        for r in results}}
    save_npz(args.out, results, config)
    print(json.dumps({r["label"]: {"base_top1": round(r["base_top1"], 4)
                                   if r["base_top1"] == r["base_top1"]
                                   else None,
                                   "mlp_top1": round(r["mlp_top1"], 4)
                                   if r["mlp_top1"] == r["mlp_top1"]
                                   else None,
                                   "n_scored": r["n_scored"],
                                   "n_in_vocab": r["n_in_vocab"],
                                   "verdict": r["verdict"]}
                      for r in results} | {"elapsed_s": round(elapsed, 2),
                                           "canonical_signal": signal},
                     sort_keys=True))
    print(f"saved: {args.out} ({elapsed:.1f}s total, "
          f"budget 300s: {'OK' if elapsed < 300 else 'OVER'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
