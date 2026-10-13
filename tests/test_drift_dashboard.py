"""Tests for tools/drift_dashboard.py pure functions (B2-64, spec DRIFT_BOARD_SPEC.md)."""
from datetime import date

from tools.drift_dashboard import current, drifting_days, history_cell, load_stamps


def _v2(pid, week, verdict, corr=0.0, stamped="2026-09-19T16:50:05Z"):
    return {
        "schema": "teleo_drift_stamp.v2", "week_key": week, "pair_id": pid,
        "stamped_at": stamped,
        "verdict": {"ok": True, "verdict": verdict, "corr_dm_dr": corr},
        "_gen": "v2",
    }


def _v1(label="teleological drift pair T1", verdict="DRIFTING"):
    return {"ok": True, "tool": "drift_check", "label": label,
            "verdict": verdict, "_gen": "v1"}


def test_load_stamps_derives_v1_pair_id(tmp_path, monkeypatch):
    import json

    import tools.drift_dashboard as dd
    ledger = tmp_path / "stamps.jsonl"
    ledger.write_text(
        json.dumps({"ok": True, "tool": "drift_check",
                    "label": "teleological drift pair T3", "verdict": "DRIFTING"}) + "\n" +
        json.dumps({"schema": "teleo_drift_stamp.v2", "week_key": "2026-W39",
                    "pair_id": "T3", "stamped_at": "2026-09-25T00:00:00Z",
                    "verdict": {"ok": True, "verdict": "ALIGNED"}}) + "\n",
        encoding="utf-8")
    monkeypatch.setattr(dd, "LEDGER", ledger)
    rows = dd.load_stamps()
    assert [r["pair_id"] for r in rows] == ["T3", "T3"]
    assert [r["_gen"] for r in rows] == ["v1", "v2"]


def test_history_marks_v1_undated_and_current_week():
    rows = [_v1(), _v2("T1", "2026-W38", "DRIFTING"), _v2("T1", "2026-W39", "ALIGNED")]
    cell = history_cell(rows)
    assert cell == "v1(undated) 2026-W38=DRIFTING 2026-W39=ALIGNED*"


def test_current_picks_latest_stamp_at():
    rows = [_v2("T1", "2026-W38", "DRIFTING", corr=0.4, stamped="2026-09-19T00:00:00Z"),
            _v2("T1", "2026-W39", "ALIGNED", corr=0.9, stamped="2026-09-25T00:00:00Z")]
    assert current(rows)["verdict"]["corr_dm_dr"] == 0.9


def test_drifting_days_trailing_run_only():
    today = date(2026, 9, 26)
    aligned_then_drift = [
        _v2("T1", "2026-W37", "ALIGNED", stamped="2026-09-10T00:00:00Z"),
        _v2("T1", "2026-W38", "DRIFTING", stamped="2026-09-19T00:00:00Z"),
        _v2("T1", "2026-W39", "DRIFTING", stamped="2026-09-25T00:00:00Z"),
    ]
    days, start = drifting_days(aligned_then_drift, today)
    assert (days, start) == (7, "2026-09-19")

    drift_then_aligned = [
        _v2("T2", "2026-W38", "DRIFTING", stamped="2026-09-19T00:00:00Z"),
        _v2("T2", "2026-W39", "ALIGNED", stamped="2026-09-25T00:00:00Z"),
    ]
    assert drifting_days(drift_then_aligned, today) == (0, "")


def test_drifting_days_ignores_v1_rows_in_math():
    today = date(2026, 9, 26)
    rows = [_v1(verdict="DRIFTING"),
            _v2("T1", "2026-W39", "DRIFTING", stamped="2026-09-25T00:00:00Z")]
    days, start = drifting_days(rows, today)
    # v1 is undated and must never be counted: streak starts at the v2 stamp
    assert (days, start) == (1, "2026-09-25")


# ---- B2-226: a W40 FRAGILE-ALIGNED stamp row through the board functions ----
# Spec: docs/DRIFT_BOARD_SPEC.md section 3 (FRAGILE-ALIGNED renders as
# ALIGNED's provisional form: amber-green, never the unknown-gray fallback,
# and it counts as ALIGNED for DRIFTING-day streak semantics: it breaks a
# DRIFTING streak, it never extends one). Producer: tools/drift_pairs_stamp.py
# _apply_aging_guard (the tests there pin the downgrade itself; these pin the
# board side so the B2-218 vocabulary-sweep falsifier is decidable).

from tools.drift_dashboard import _verdict_color  # noqa: E402


def test_fragile_aligned_history_cell_and_amber_green_color():
    rows = [
        _v2("T1", "2026-W39", "DRIFTING", stamped="2026-09-25T00:00:00Z"),
        _v2("T1", "2026-W40", "FRAGILE-ALIGNED", stamped="2026-09-28T00:00:00Z"),
    ]
    cell = history_cell(rows)
    assert "2026-W40=FRAGILE-ALIGNED*" in cell
    # amber-green (provisional ALIGNED), never the default-gray fallback and
    # never the VACUOUS/INSUFFICIENT gray
    assert _verdict_color("FRAGILE-ALIGNED") == "#b9e77a"
    assert _verdict_color("FRAGILE-ALIGNED") != "#ddd"
    assert _verdict_color("FRAGILE-ALIGNED") not in (
        _verdict_color("VACUOUS"), _verdict_color("INSUFFICIENT"))


def test_fragile_aligned_breaks_a_drifting_streak():
    today = date(2026, 9, 28)
    rows = [
        _v2("T1", "2026-W38", "DRIFTING", stamped="2026-09-19T00:00:00Z"),
        _v2("T1", "2026-W39", "DRIFTING", stamped="2026-09-25T00:00:00Z"),
        _v2("T1", "2026-W40", "FRAGILE-ALIGNED", stamped="2026-09-28T00:00:00Z"),
    ]
    # the newest stamp is FRAGILE-ALIGNED: the trailing DRIFTING run is empty
    assert drifting_days(rows, today) == (0, "")


def test_fragile_aligned_never_extends_a_streak():
    today = date(2026, 9, 29)
    rows = [
        _v2("T1", "2026-W39", "FRAGILE-ALIGNED", stamped="2026-09-25T00:00:00Z"),
        _v2("T1", "2026-W40", "DRIFTING", stamped="2026-09-28T00:00:00Z"),
    ]
    # a fragile week between DRIFTING weeks must not glue the runs together:
    # the streak starts at the W40 stamp only, not back through W39
    assert drifting_days(rows, today) == (1, "2026-09-28")
