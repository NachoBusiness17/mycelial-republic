"""Pins for tools/seed_paired_uplift.py, the law-D TARA gate (B2-155).

Falsifier surface from B2-58 receipt F2: amendment D was untestable until a
paired scorer existed. These tests pin the executor so a refactor cannot
silently weaken the auto-revert arm (e.g. adopt on aggregate delta alone, or
adopt ties).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.seed_paired_uplift import _demo, _folds, flag_only_compare, gate

SEEDS = [f"s{i}" for i in range(1, 13)]


def _flat(v):
    return {s: v for s in SEEDS}


def test_folds_deterministic_and_cover_all():
    a = _folds(12, 5)
    b = _folds(12, 5)
    assert a == b  # fixed partition, no run-to-run drift
    flat = [i for fold in a for i in fold]
    assert sorted(flat) == list(range(12))
    assert len(a) == 5
    # small-set answer: k = min(5, n)
    assert len(_folds(3)) == 3
    assert len(_folds(2)) == 2


def test_single_fold_confined_gain_is_refused():
    """The B2-200 refusal shape: aggregate +3.0, but the gain lives in one fold.

    A single-delta gate (the pre-B2-200 law D) would adopt +3.0; the fold
    check must refuse it and leave the seed standing.
    """
    d = _demo()
    c = d["candidates"]["single_fold_gain"]
    assert c["aggregate_delta"] > 0
    assert c["aggregate_ok"] is True
    assert c["heldout_delta_sum"] == 0.0
    assert c["verdict"] == "REVERT"
    assert c["standing"] == "p0"  # auto-revert arm: the seed stays


def test_two_fold_recurring_gain_is_adopted():
    d = _demo()
    c = d["candidates"]["two_fold_gain"]
    assert c["aggregate_delta"] > 0
    assert c["heldout_delta_sum"] > 0
    assert c["verdict"] == "ADOPT"
    assert c["standing"] == "two_fold_gain"


def test_broad_gain_is_adopted_and_regressor_refused():
    d = _demo()
    assert d["candidates"]["broad_gain"]["verdict"] == "ADOPT"
    r = d["candidates"]["pure_regressor"]
    assert r["aggregate_ok"] is False
    assert r["verdict"] == "REVERT"
    assert r["standing"] == "p0"


def test_tie_never_adopts():
    scores = {"p0": _flat(0.5), "same": _flat(0.5)}
    out = gate("p0", SEEDS, scores)
    assert out["candidates"]["same"]["verdict"] == "REVERT"


def test_gate_beats_flag_only_on_seed_paired_regressions():
    """F2 metric: the gate must not adopt what flag-only adopts blind."""
    d = _demo()
    cmp = flag_only_compare("p0", SEEDS, _demo_scores(), d)
    assert cmp["gate_beats_flag_only"] is True
    assert cmp["gate_mean_seed_regressions"] == 0.0
    assert cmp["flag_only_mean_seed_regressions"] > 0.0


def _demo_scores():
    seeds = SEEDS
    seed_scores = _flat(0.5)
    from tools.seed_paired_uplift import FOLDS

    fold_seeds = _folds(12, min(FOLDS, 12))
    fold0 = [seeds[i] for i in fold_seeds[0]]
    fold1 = [seeds[i] for i in fold_seeds[1]]

    confined = dict(seed_scores)
    for s in fold0:
        confined[s] = 1.5
    twofold = dict(seed_scores)
    for s in fold0 + fold1:
        twofold[s] = 1.0
    broad = dict(seed_scores)
    for s in seeds:
        broad[s] = 0.58
    regressor = dict(seed_scores)
    for s in seeds:
        regressor[s] = 0.4
    return {
        "p0": seed_scores,
        "single_fold_gain": confined,
        "two_fold_gain": twofold,
        "broad_gain": broad,
        "pure_regressor": regressor,
    }
