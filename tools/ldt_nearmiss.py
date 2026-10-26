"""ldt_nearmiss — IMP9: N4's near-miss adversarial split, raw vs projected.

Mickey17 W3K lane (2026-09-30), N4's OOD split (c) realized on the estate's
water graph: "near-miss adversarial: legal action on a graph, plus the same
graph with one edge retyped so the action becomes illegal (forces symbolic,
not pattern, matching)."

DOMAIN MAPPING (honest — N4's generic edge types do not exist here):
MountainWorld.validate consults ONLY the verb table, the target's EXISTENCE,
and (boil/tag) the target's VOLUME — no pipe-field retype can flip legality,
so the minimal retypes that flip legal_gain -> illegal_* are exactly three,
and they are the whole generator:

  dry_pool             verb=boil on a wet target that gains: the target's
                       volume atom retyped k -> 0. One render atom flips; the
                       binding (verb:boil, tgt:T, volume(T)=0) is what a
                       symbolic matcher makes and a bag of atoms cannot.
  unknown_target_node  the target NODE renamed T -> T_twin. The action still
                       names T; n:T vanishes from the render (the featurizer
                       drops the OOV T_twin atom) — the twin's flat view is
                       the original's view MINUS the hole where T stood.
  unknown_target_pipe  verb=valve: the target PIPE renamed P -> P_twin — the
                       literal "one edge retyped" of N4's design.

VERIFICATION LAW: every pair is verified with Y10's propagator before it is
kept — original verdict legal_gain, twin verdict the family's illegal_*; a
pair that does not flip exactly is discarded, never kept on trust.
tests/test_ldt_nearmiss.py pins engine agreement (label_sample) on both
sides plus render-diff minimality, so the generator cannot drift from the
engine it is adversarial FOR.

EXPERIMENT: train the Z13 v0 shape on the standard split (frozen recipe
seed 13, 40 epochs, 128,64, tau 0.7; parity check vs models/legality_v0.
npz's 0.8545/0.8830), then evaluate THE SAME WEIGHTS two ways on the
near-miss set: RAW vs PROJECTED (V7's post-hoc lattice projection, strict
and renorm — the projection is the only delta). Metrics: forced-argmax
accuracy on orig/twin rows, BOTH-correct pairs, distinguished pairs,
twin_fooled, tau-answered soundness/coverage on evaluate_lattice.

THE HONEST BAR: renorm on a singleton feasible set is a PROOF, not a
measurement — conf renormalizes to exactly 1.0, the pin — so renorm twin
accuracy 1.0 is soundness-by-construction demonstrated, not an empirical
score. The MEASURED quantities are the raw arm (how badly pattern matching
is fooled) and strict's coverage cost. The originals' tier is crown physics
(F = {legal_gain, legal_no_gain}): the lattice cannot help there by design.

Determinism law: one random.Random stream per artifact, no wall clock in
any output. $0, stdlib + numpy.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.ldt_lattice import (evaluate_lattice, feasible_mask,  # noqa: E402
                               feasible_set)
from tools.ldt_train import (LABELS, LABEL_TO_IDX, Featurizer,  # noqa: E402
                             evaluate as raw_evaluate, forward, load_jsonl,
                             load_npz, rows_xy, train_model)
from tools.legality_dataset import make_graph_spec, render_tokens  # noqa: E402
from tools.legality_propagator import propagate  # noqa: E402

FAMILIES = ("dry_pool", "unknown_target_node", "unknown_target_pipe")
TWIN_SUFFIX = "_twin"
GAIN = "legal_gain"


# ----------------------------------------------------------- twin builders ----
def _drain(spec: dict[str, Any], target: str) -> dict[str, Any]:
    """dry_pool twin: the target's volume atom retyped k -> 0."""
    out = copy.deepcopy(spec)
    out["nodes"][target]["volume"] = 0
    return out


def _rename_node(spec: dict[str, Any], target: str) -> dict[str, Any]:
    """unknown_target_node twin: node T -> T_twin, insertion order kept
    (the propagator's first-max/first-min tie rules read dict order)."""
    out = copy.deepcopy(spec)
    out["nodes"] = {(k + TWIN_SUFFIX if k == target else k): copy.deepcopy(v)
                    for k, v in spec["nodes"].items()}
    out["pipes"] = {}
    for pname, pp in spec["pipes"].items():
        pp2 = copy.deepcopy(pp)
        pp2["src"] += TWIN_SUFFIX if pp2["src"] == target else ""
        pp2["dst"] += TWIN_SUFFIX if pp2["dst"] == target else ""
        out["pipes"][pname] = pp2
    return out


def _rename_pipe(spec: dict[str, Any], target: str) -> dict[str, Any]:
    """unknown_target_pipe twin: the edge P -> P_twin, order kept."""
    out = copy.deepcopy(spec)
    out["pipes"] = {(k + TWIN_SUFFIX if k == target else k): copy.deepcopy(v)
                    for k, v in spec["pipes"].items()}
    return out


def build_twin(spec: dict[str, Any], target: str,
               family: str) -> tuple[dict[str, Any], str]:
    """The family's single retype -> (twin spec, the label it must produce)."""
    if family == "dry_pool":
        return _drain(spec, target), "illegal_dry_pool"
    if family == "unknown_target_node":
        return _rename_node(spec, target), "illegal_unknown_target"
    if family == "unknown_target_pipe":
        return _rename_pipe(spec, target), "illegal_unknown_target"
    raise ValueError(f"unknown family {family!r}")


def twin_edit_desc(family: str, target: str) -> str:
    if family == "dry_pool":
        return f"nodes[{target}].volume -> 0"
    if family == "unknown_target_node":
        return f"node {target} -> {target}{TWIN_SUFFIX}"
    return f"pipe {target} -> {target}{TWIN_SUFFIX}"


# ------------------------------------------------------------- the sampler ----
def _propose(rng: random.Random, spec: dict[str, Any],
             family: str) -> tuple[str, str] | None:
    """A legal-candidate action for the family's verb class (rejection
    sampling: the propagator has the final word on legal_gain)."""
    if family == "dry_pool":
        wet = [n for n, d in spec["nodes"].items() if d["volume"] > 0]
        return ("boil", rng.choice(wet)) if wet else None
    if family == "unknown_target_node":
        verb = rng.choices(("boil", "join", "tag"), weights=(6, 2, 2))[0]
        cand = [n for n, d in spec["nodes"].items()
                if verb == "join" or d["volume"] > 0]
        return (verb, rng.choice(cand)) if cand else None
    pipes = list(spec["pipes"])
    return ("valve", rng.choice(pipes)) if pipes else None


def make_pair(rng: random.Random, family: str) -> dict[str, Any] | None:
    """One verified near-miss pair, or None (not a gain board / did not
    flip exactly — discarded, never kept on trust)."""
    spec = make_graph_spec(rng)
    act = _propose(rng, spec, family)
    if act is None:
        return None
    verb, target = act
    if propagate(spec, verb, target)["label"] != GAIN:
        return None
    twin_spec, want = build_twin(spec, target, family)
    if propagate(twin_spec, verb, target)["label"] != want:
        return None
    return {
        "family": family, "verb": verb, "target": target,
        "edit": twin_edit_desc(family, target),
        "orig": {"graph": spec, "verb": verb, "target": target, "label": GAIN,
                 "tokens": render_tokens(spec, verb, target, GAIN)},
        "twin": {"graph": twin_spec, "verb": verb, "target": target,
                 "label": want,
                 "tokens": render_tokens(twin_spec, verb, target, want)},
    }


def generate_pairs(per_family: int, seed: int,
                   max_tries_per_family: int = 80000) -> list[dict[str, Any]]:
    """The near-miss set: per_family verified pairs per family, one rng
    stream, families filled in FAMILIES order (deterministic)."""
    rng = random.Random(seed)
    pairs: list[dict[str, Any]] = []
    for fam in FAMILIES:
        got = tries = 0
        while got < per_family and tries < max_tries_per_family:
            tries += 1
            if (p := make_pair(rng, fam)) is not None:
                p["id"] = f"nm-{len(pairs):06d}"
                pairs.append(p)
                got += 1
    return pairs


def write_pairs(pairs: list[dict[str, Any]], out_dir: Path,
                seed: int) -> dict[str, Any]:
    """Durable artifact: canonical JSONL + manifest (sha256 per file)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "nearmiss.jsonl"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for p in pairs:
            fh.write(json.dumps(p, sort_keys=True,
                                separators=(",", ":")) + "\n")
    dist: dict[str, int] = {}
    for p in pairs:
        dist[p["family"]] = dist.get(p["family"], 0) + 1
    manifest = {
        "schema": "nearmiss.v1", "seed": seed, "pairs": len(pairs),
        "families": dist,
        "pair_contract": "orig legal_gain / twin the family's illegal_*, "
                         "both propagator-verified",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "path": str(path),
    }
    (out_dir / "MANIFEST.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8")
    return manifest


# ---------------------------------------------------------------- metrics ----
def _arm(name: str, probs: np.ndarray, feas: list[frozenset[str]],
         y: np.ndarray, is_twin: np.ndarray, family: np.ndarray,
         tau: float, mode: str) -> dict[str, Any]:
    """One evaluation arm (mode raw -> plain argmax; strict/renorm -> the
    V7 projection). Row-level forced accuracy, tau-answered soundness/
    coverage on the shared evaluate_lattice contract, pair metrics."""
    if mode == "raw":
        pred, answered = probs.argmax(axis=1), probs.max(axis=1) >= tau
    else:
        lat = evaluate_lattice(probs, feas, y, tau, mode=mode)
        mask = feasible_mask(feas)
        neg = np.where(mask, probs, -np.inf)
        pred = neg.argmax(axis=1)
        conf = neg.max(axis=1).astype(np.float64)
        if mode == "renorm":
            mass = (probs * mask).sum(axis=1)
            conf = np.where(mass > 0, conf / np.maximum(mass, 1e-12), 0.0)
        answered = conf >= tau

    correct = pred == y

    def _slice(twin: bool, fam: str | None = None) -> np.ndarray:
        m = is_twin == twin
        return m & (family == fam) if fam is not None else m

    def _rows(m: np.ndarray, scope: str) -> dict[str, Any]:
        n = int(m.sum())
        n_ans = int((answered & m).sum())
        n_corr = int((correct & answered & m).sum())
        return {
            "n": n,
            "forced_acc": float(correct[m].mean()) if n else float("nan"),
            "fooled_into_gain": (int(((pred == LABEL_TO_IDX[GAIN]) & m).sum())
                                 if scope == "twin" else 0),
            "coverage": n_ans / n if n else 0.0,
            "answered": n_ans, "answered_correct": n_corr,
            "answered_wrong": n_ans - n_corr,
            "soundness": (n_corr / n_ans) if n_ans else float("nan"),
        }

    out: dict[str, Any] = {"arm": name, "mode": mode, "n": int(len(y)),
                           "tau": tau, "by_family": {}}
    for scope, twin in (("all", None), ("orig", False), ("twin", True)):
        m = np.ones(len(y), dtype=bool) if twin is None else _slice(twin)
        out[scope] = _rows(m, scope)
    for fam in sorted(set(family.tolist())):
        mo, mt = _slice(False, fam), _slice(True, fam)
        out["by_family"][fam] = {
            "orig_forced_acc": float(correct[mo].mean()),
            "twin_forced_acc": float(correct[mt].mean()),
            **_pair_metrics(pred, correct, mo, mt),
        }
    out["pairs"] = _pair_metrics(pred, correct, ~is_twin, is_twin)
    if mode != "raw":
        out["tripwires"] = {k: lat[k] for k in ("answered_infeasible",
                                                "answered_not_raw")}
    return out


def _pair_metrics(pred: np.ndarray, correct: np.ndarray, m_o: np.ndarray,
                  m_t: np.ndarray) -> dict[str, Any]:
    """Both-correct / distinguished over pairs (m_o and m_t select the
    originals and twins in the same pair order)."""
    n = int(m_o.sum())
    if n == 0 or int(m_t.sum()) != n:
        return {"pairs": n, "both_correct": 0, "distinguished": 0}
    return {
        "pairs": n,
        "both_correct": int((correct[m_o] & correct[m_t]).sum()),
        "distinguished": int((pred[m_o] != pred[m_t]).sum()),
    }


# -------------------------------------------------------------------- run ----
def run_experiment(args: argparse.Namespace) -> int:
    t0 = time.perf_counter()
    tau = args.threshold
    hidden = [int(h) for h in args.hidden.split(",")]

    # 1. standard-split training, frozen Z13 recipe + parity check
    train_rows = load_jsonl(args.data / "train.jsonl")
    val_rows = load_jsonl(args.data / "val.jsonl")
    fe = Featurizer().fit(train_rows)
    Xtr, ytr = rows_xy(train_rows, fe)
    Xva, yva = rows_xy(val_rows, fe)
    params, _ = train_model(Xtr, ytr, hidden, args.epochs, args.lr, args.batch,
                            args.seed, l2=args.l2)
    val_raw = raw_evaluate(params, Xva, yva, threshold=tau)

    frozen: dict[str, Any] = {}
    if args.model.exists():
        _, _, cfg = load_npz(args.model)
        frozen = cfg.get("val_metrics", {})
    parity = "n/a (no frozen model)"
    if frozen and "soundness" in frozen:
        ds = abs(val_raw["soundness"] - frozen["soundness"])
        da = abs(val_raw["accuracy"] - frozen["accuracy"])
        parity = "yes" if (ds < 1e-9 and da < 1e-9) else \
            f"NO (dS={ds:.6f} dA={da:.6f})"

    # 2. the near-miss set (fresh boards, never a training row)
    pairs = generate_pairs(args.pairs_per_family, args.nm_seed)
    if not pairs:
        print("ERROR: no near-miss pairs generated")
        return 1
    if args.out:
        manifest = write_pairs(pairs, args.out, args.nm_seed)
        print(f"near-miss set: {manifest['pairs']} pairs "
              f"{manifest['families']} -> {manifest['path']} "
              f"(sha256 {manifest['sha256'][:12]}…)")
    # interleave: row 2i is a pair's original, row 2i+1 its twin
    rows = [r for p in pairs for r in (p["orig"], p["twin"])]
    Xnm = fe.transform(rows)
    ynm = np.array([LABEL_TO_IDX[r["label"]] for r in rows], dtype=np.int64)
    feas = [feasible_set(r["graph"], r["verb"], r["target"]) for r in rows]
    is_twin = np.array([i % 2 == 1 for i in range(len(rows))], dtype=bool)
    family = np.array([p["family"] for p in pairs for _ in range(2)])

    # truth-feasibility law on the adversarial set (must hold by construction)
    truth_out = sum(1 for i, r in enumerate(rows) if r["label"] not in feas[i])
    print(f"\ntrain={len(train_rows)} (frozen recipe seed={args.seed}) "
          f"val n={len(val_rows)}: acc={val_raw['accuracy']:.4f} "
          f"soundness={val_raw['soundness']:.4f} "
          f"(frozen Z13 parity: {parity})")
    print(f"near-miss rows={len(rows)} pairs={len(pairs)}; "
          f"labels outside their feasible set: {truth_out} (must be 0)")

    probs, _ = forward(params, Xnm)
    arms = {name: _arm(name, probs, feas, ynm, is_twin, family, tau, name)
            for name in ("raw", "strict", "renorm")}

    print(f"\n{'arm':>7} {'twin acc':>9} {'fooled':>7} {'twin snd':>9} "
          f"{'twin cov':>9} {'orig acc':>9} {'both-corr':>10} {'disting':>8}")
    for name, a in arms.items():
        tw, og, pr = a["twin"], a["orig"], a["pairs"]
        snd = f"{tw['soundness']:.4f}" if tw["answered"] else "n/a"
        print(f"{name:>7} {tw['forced_acc']:>9.4f} {tw['fooled_into_gain']:>7d} "
              f"{snd:>9} {tw['coverage']:>9.4f} {og['forced_acc']:>9.4f} "
              f"{pr['both_correct']:>4d}/{pr['pairs']:<5d} "
              f"{pr['distinguished']:>4d}/{pr['pairs']:<4d}")
        for fam, d in a["by_family"].items():
            print(f"  [{fam:>19}] orig={d['orig_forced_acc']:.4f} "
                  f"twin={d['twin_forced_acc']:.4f} "
                  f"both={d['both_correct']}/{d['pairs']}")

    # the machine-named verdict the receipt cannot soften
    raw_twin = arms["raw"]["twin"]["forced_acc"]
    cured = (arms["renorm"]["twin"]["forced_acc"] == 1.0
             and arms["strict"]["twin"]["forced_acc"] >= raw_twin
             and arms["renorm"]["tripwires"]["answered_infeasible"] == 0)
    verdict = ("PROJECTION CURES THE NEAR-MISS (renorm twin acc 1.0 by "
               "construction; strict >= raw)" if cured else
               "PROJECTION DOES NOT FULLY CURE — honest failure, see numbers")
    print(f"\nVERDICT: {verdict}")
    print(f"wall: {time.perf_counter() - t0:.1f}s (budget {args.budget}s)")
    print(json.dumps({
        "threshold": tau, "n_pairs": len(pairs), "parity": parity,
        "val_raw": {k: v for k, v in val_raw.items() if k != "per_class"},
        "arms": arms, "verdict": verdict,
    }, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path, default=ROOT / "logs" / "legality_ds")
    ap.add_argument("--model", type=Path,
                    default=ROOT / "models" / "legality_v0.npz")
    ap.add_argument("--out", type=Path, default=ROOT / "logs" / "nearmiss_ds")
    ap.add_argument("--pairs-per-family", type=int, default=200)
    ap.add_argument("--nm-seed", type=int, default=4242)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--hidden", default="128,64")
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--l2", type=float, default=1e-4)
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--budget", type=int, default=600)
    return run_experiment(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
