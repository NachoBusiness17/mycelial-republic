"""tests for the referent-age guard in tools/drift_pairs_stamp.py (B2-66, 2026-09-26).

Spec under test (module docstring, "REFERENT-AGE GUARD"):
  - referent_age_days = the referent layer's calendar days of observed
    life at stamp time, (run_date - first referent ts date).days + 1
    (inclusive, the B2-05 counting); None when the referent has no
    dated rows;
  - REFERENT_MATURE_DAYS = 7: ALIGNED stands only for a referent at
    least 7 days old; younger stamps FRAGILE-ALIGNED;
  - only ALIGNED downgrades; every other verdict passes through at any
    age, and the input verdict dict is never mutated;
  - stamp() rows carry referent_first_date / referent_last_date /
    referent_age_days / verdict_guard, and the ledger stays idempotent
    per ISO week under the guard;
  - the W39 boundary case: a 2-day-old referent downgrades (the B2-05
    receipt named exactly this fragile).

All tests run against a throwaway ledger and synthetic pair builders;
the durable memory/runs surface is never written.
test_pair_t6_exposes_referent_bounds reads the real
memory/burns/LEDGER.jsonl (append-only, small) and skips if missing.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tools.drift_pairs_stamp as dps


# ------------------------------------------------------------------ units

def test_age_counts_first_day_as_day_1():
    # burn ledger: first row 2026-09-25, W39 stamp 2026-09-26 = day 2
    assert dps._referent_age_days(date(2026, 9, 25), date(2026, 9, 26)) == 2


def test_age_none_without_dated_rows():
    assert dps._referent_age_days(None, date(2026, 9, 26)) is None


def test_threshold_is_the_pre_registered_seven():
    assert dps.REFERENT_MATURE_DAYS == 7


def _aligned_verdict():
    # constant deltas would be DEGENERATE (zero delta variance); this pair
    # has variance in both delta series and corr +1.0
    return dps.drift_check([0, 2, 1, 4, 3, 6], [0, 2, 1, 4, 3, 6], label="t")


def test_boundary_age_two_downgrades_aligned():
    # the B2-05 W39 T6 case: ALIGNED corr 0.6387 on a 2-day-old referent
    v = _aligned_verdict()
    assert v["verdict"] == "ALIGNED"
    g = dps._apply_aging_guard(v, 2)
    assert g["verdict"] == "FRAGILE-ALIGNED"
    assert g["corr_dm_dr"] == v["corr_dm_dr"]
    assert g["ok"] is True


def test_mature_aligned_stands():
    v = _aligned_verdict()
    assert dps._apply_aging_guard(v, 7)["verdict"] == "ALIGNED"
    assert dps._apply_aging_guard(v, 1244)["verdict"] == "ALIGNED"


def test_unknown_age_is_not_mature():
    v = _aligned_verdict()
    assert dps._apply_aging_guard(v, None)["verdict"] == "FRAGILE-ALIGNED"


def test_guard_never_mutates_input():
    v = _aligned_verdict()
    before = dict(v)
    dps._apply_aging_guard(v, 2)
    assert v == before


@pytest.mark.parametrize("state", ["DRIFTING", "INVERTED", "VACUOUS",
                                   "DEGENERATE", "INSUFFICIENT"])
def test_only_aligned_downgrades(state):
    v = {"ok": True, "verdict": state}
    assert dps._apply_aging_guard(v, 1)["verdict"] == state
    assert dps._apply_aging_guard(v, None)["verdict"] == state


def test_error_verdict_passes_through():
    v = {"ok": False, "error": "series must be same length, >= 2 points"}
    assert dps._apply_aging_guard(v, 1) is v


# ------------------------------------------------------------------ stamp()

def _built(metric, referent, first, last):
    span = [date(2026, 10, i) for i in range(1, 7)]
    return {"metric": metric, "referent": referent, "span": span,
            "sources": {}, "referent_first": first, "referent_last": last}


@pytest.fixture()
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(dps, "LEDGER", tmp_path / "stamps.jsonl")
    monkeypatch.setattr(dps, "RECEIPT", tmp_path / "receipt.json")
    return tmp_path


def _wire(monkeypatch):
    pairs = {
        # ALIGNED series whose referent layer is 3 days old at the stamp:
        # the downgrade path
        "TX": {"pair": "young_aligned", "teleo": "t",
               "build": lambda: _built([0, 2, 1, 4, 3, 6], [0, 2, 1, 4, 3, 6],
                                       date(2026, 10, 5), date(2026, 10, 6))},
        # DRIFTING series (corr -0.0891) on a 68-day-old referent: passes
        # through at any age
        "TY": {"pair": "old_drifting", "teleo": "t",
               "build": lambda: _built([0, 2, 1, 4, 3, 6], [0, 0, 0, 0, 1, 2],
                                       date(2026, 8, 1), date(2026, 10, 6))},
    }
    monkeypatch.setattr(dps, "PAIRS", pairs)


def test_stamp_rows_carry_age_and_guard(isolated, monkeypatch):
    _wire(monkeypatch)
    out = dps.stamp(today=date(2026, 10, 7))
    assert out["added"] == 2
    rows = [json.loads(l) for l in
            isolated.joinpath("stamps.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    by = {r["pair_id"]: r for r in rows}
    tx = by["TX"]
    assert tx["verdict"]["verdict"] == "FRAGILE-ALIGNED"
    assert tx["verdict"]["ok"] is True and "corr_dm_dr" in tx["verdict"]
    assert tx["referent_first_date"] == "2026-10-05"
    assert tx["referent_last_date"] == "2026-10-06"
    assert tx["referent_age_days"] == 3
    g = tx["verdict_guard"]
    assert g["threshold_days"] == 7
    assert g["original_verdict"] == "ALIGNED"
    assert g["downgraded"] is True
    ty = by["TY"]
    assert ty["verdict"]["verdict"] == "DRIFTING"
    assert ty["verdict_guard"]["downgraded"] is False
    assert ty["verdict_guard"]["original_verdict"] == "DRIFTING"
    assert ty["referent_age_days"] == 68
    assert ty["referent_first_date"] == "2026-08-01"


def test_stamp_idempotent_under_guard(isolated, monkeypatch):
    _wire(monkeypatch)
    dps.stamp(today=date(2026, 10, 7))
    first = isolated.joinpath("stamps.jsonl").read_text(encoding="utf-8")
    out2 = dps.stamp(today=date(2026, 10, 7))
    assert out2["added"] == 0 and out2["skipped"] == 2
    assert isolated.joinpath("stamps.jsonl").read_text(encoding="utf-8") == first


def test_receipt_lists_referent_age(isolated, monkeypatch):
    _wire(monkeypatch)
    dps.stamp(today=date(2026, 10, 7))
    receipt = json.loads(isolated.joinpath("receipt.json").read_text(encoding="utf-8"))
    ages = {e["pair_id"]: e["referent_age_days"]
            for e in receipt["week_stamps_in_ledger"]}
    assert ages == {"TX": 3, "TY": 68}


# ------------------------------------------------------------- live bytes

def test_pair_t6_exposes_referent_bounds_from_ledger_bytes():
    if not dps.BURNS.exists():
        pytest.skip("memory/burns/LEDGER.jsonl missing")
    built = dps.pair_t6()
    rows = [json.loads(l) for l in
            dps.BURNS.read_text(encoding="utf-8", errors="replace").splitlines()
            if l.strip()]
    dates = sorted({d for d in (dps._utc_date(r.get("ts")) for r in rows) if d})
    assert dates, "ledger has dated rows"
    assert built["referent_first"] == dates[0]
    assert built["referent_last"] == dates[-1]
