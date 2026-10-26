"""Seed-paired uplift harness with the TARA gate (law D executor).

B2-155 (2026-09-26). Makes roblox/prompts/README.md amendment D testable
instead of spec-only (B2-58 receipt F2 called D untestable until a paired
scorer exists; no harness had landed, so this is it).

What it does:
  - consumes per-seed PAIRED scores for the seed prompt and every candidate
    (law C: same fixed seed set, one score per seed per prompt; this module
    is arithmetic only, it never generates);
  - applies the law-D gate verbatim: adopt a candidate iff its seed-paired
    mean beats the seed's AND the gain holds across folds, where folds are
    k = min(5, n_seeds) fixed partitions; on each fold the best candidate is
    re-picked on the other folds, scored on the held-out fold, and the
    held-out sums must beat the seed's;
  - on refuse, the seed stays standing (the TARA accept-or-revert arm:
    "adopts the repair iff s(x_hat)>s(x0) and otherwise reverts");
  - compares the gate against flag-only adoption (adopt whatever carries the
    uplift flag) on seed-paired regression rate, which is the F2 falsifier
    metric: if the gate cannot beat flag-only there, the auto-revert clause
    is vacuous.

Fold mechanics mirror the vendored dspy ReAnchor calibrate the law names
(watch/inbox/burn_wave_20260926/B2_59_dspy_reanchor_calibrate.py:50,214-252):
k = min(5, n), fixed deterministic shuffle, strictly-better pick, held-out
sum, restore on refuse.

Usage:
  python tools/seed_paired_uplift.py --scores scores.json
  python tools/seed_paired_uplift.py --demo      # built-in replay, no input

scores.json shape:
  {
    "seed_prompt": "p0",
    "seeds": ["s1", "s2", ...],
    "scores": {"p0": {"s1": 0.5, ...}, "candidateA": {"s1": 0.5, ...}}
  }
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

FOLDS = 5


def _folds(n: int, k: int = FOLDS) -> list[list[int]]:
    """Fixed deterministic partition of range(n) into min(k, n) folds (calibrate.py:214).

    k = min(FOLDS, n) is the law's own small-set answer, so the function
    clamps internally and never emits empty folds.
    """
    k = min(k, n)
    idx = list(range(n))
    random.Random(0).shuffle(idx)
    return [idx[i::k] for i in range(k)]


def _total(scores: dict[str, float], seeds: list[str]) -> float:
    return sum(float(scores[s]) for s in seeds)


def gate(
    seed_prompt: str,
    seeds: list[str],
    scores: dict[str, dict[str, float]],
) -> dict:
    """Apply the law-D TARA gate. Returns per-candidate verdicts + summary."""
    seed_scores = scores[seed_prompt]
    seed_total = _total(seed_scores, seeds)
    n = len(seeds)
    k = min(FOLDS, n)
    folds = _folds(n, k)
    fold_seeds = [[seeds[i] for i in fold] for fold in folds]

    results = {}
    for cand, cscores in scores.items():
        if cand == seed_prompt:
            continue
        cand_total = _total(cscores, seeds)
        aggregate_ok = cand_total > seed_total  # strictly better, no tie adopt

        # The gate is PER-CANDIDATE accept-or-revert against the seed (TARA:
        # "adopts the repair iff s(x_hat)>s(x0) and otherwise reverts"), so
        # each fold re-picks between THIS candidate and the seed on the
        # training folds, then scores that pick on the held-out fold. B2-155
        # replay fix: a shared best-pick across candidates lets a confined
        # candidate hitchhike on another candidate's held-out gains, which
        # would adopt exactly the shape law D exists to refuse.
        heldout_delta = 0.0
        picks = []
        for f in range(k):
            train = [s for j, fs in enumerate(fold_seeds) if j != f for s in fs]
            held = fold_seeds[f]
            if _total(cscores, train) > _total(seed_scores, train):
                d = _total(cscores, held) - _total(seed_scores, held)
                picks.append({"fold": f, "pick": cand, "heldout_delta": round(d, 6)})
                heldout_delta += d
            else:
                picks.append({"fold": f, "pick": "seed", "heldout_delta": 0.0})
        folds_ok = heldout_delta > 0  # strictly better on held-out sum
        adopt = bool(aggregate_ok and folds_ok)
        results[cand] = {
            "aggregate_delta": round(cand_total - seed_total, 6),
            "aggregate_ok": aggregate_ok,
            "heldout_delta_sum": round(heldout_delta, 6),
            "folds_ok": folds_ok,
            "folds": k,
            "picks": picks,
            "verdict": "ADOPT" if adopt else "REVERT",
            "standing": cand if adopt else seed_prompt,
        }
    return {
        "seed_prompt": seed_prompt,
        "n_seeds": n,
        "k_folds": k,
        "seed_total": round(seed_total, 6),
        "candidates": results,
    }


def flag_only_compare(
    seed_prompt: str,
    seeds: list[str],
    scores: dict[str, dict[str, float]],
    gated: dict,
) -> dict:
    """F2 metric: seed-paired regression rate, gate vs flag-only adoption.

    A regression = a seed whose score DROPPED under the adopted prompt.
    Flag-only adopts every candidate that carries the flag (here: every
    candidate at all); the gate adopts only its ADOPT verdicts.
    """
    seed_scores = scores[seed_prompt]
    per_seed_regress = lambda prompt: sum(
        1 for s in seeds if float(scores[prompt][s]) < float(seed_scores[s])
    )
    flagged = list(k for k in scores if k != seed_prompt)
    flag_reg = sum(per_seed_regress(c) for c in flagged) / max(1, len(flagged))
    adopted = [c for c, r in gated["candidates"].items() if r["verdict"] == "ADOPT"]
    gate_reg = sum(per_seed_regress(c) for c in adopted) / max(1, len(adopted)) if adopted else 0.0
    return {
        "flag_only_candidates": len(flagged),
        "flag_only_mean_seed_regressions": round(flag_reg, 6),
        "gate_adopted": len(adopted),
        "gate_mean_seed_regressions": round(gate_reg, 6),
        "gate_beats_flag_only": gate_reg < flag_reg,
    }


def _demo() -> dict:
    """Confined-gain replay plus controls, n=12.

    The confined candidate's gain sits on exactly the seeds of ONE fold of
    the fixed partition (the B2-200 refusal shape); the two-fold candidate's
    gain sits on two folds, so it legitimately recurs and is adopted; the
    broad candidate gains everywhere; the regressor loses everywhere and
    shows what flag-only adopts that the gate refuses.
    """
    seeds = [f"s{i}" for i in range(1, 13)]
    seed_scores = {s: 0.5 for s in seeds}
    fold_seeds = _folds(12, min(FOLDS, 12))
    fold0 = [seeds[i] for i in fold_seeds[0]]
    fold1 = [seeds[i] for i in fold_seeds[1]]

    confined = dict(seed_scores)
    for s in fold0:
        confined[s] = 1.5  # aggregate gain, but all of it lives in fold 0

    twofold = dict(seed_scores)
    for s in fold0 + fold1:
        twofold[s] = 1.0  # gain recurs across two folds

    broad = dict(seed_scores)
    for s in seeds:
        broad[s] = 0.58  # small everywhere-gain

    regressor = dict(seed_scores)
    for s in seeds:
        regressor[s] = 0.4  # loses everywhere; flag-only would still adopt

    scores = {
        "p0": seed_scores,
        "single_fold_gain": confined,
        "two_fold_gain": twofold,
        "broad_gain": broad,
        "pure_regressor": regressor,
    }
    gated = gate("p0", seeds, scores)
    gated["fold0_seeds"] = fold0
    gated["fold1_seeds"] = fold1
    gated["f2_compare"] = flag_only_compare("p0", seeds, scores, gated)
    return gated


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--scores", type=Path, help="JSON file with paired per-seed scores")
    src.add_argument("--demo", action="store_true", help="run the built-in replay")
    args = ap.parse_args(argv)
    if args.demo:
        out = _demo()
    else:
        data = json.loads(args.scores.read_text(encoding="utf-8"))
        out = gate(data["seed_prompt"], data["seeds"], data["scores"])
        out["f2_compare"] = flag_only_compare(
            data["seed_prompt"], data["seeds"], data["scores"], out
        )
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
