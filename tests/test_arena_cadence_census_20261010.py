"""Arena cadence census tests (GAP_REGISTER 2026-10-10 R2 fill).

The R2 law under test: a cadence receipt carries FAILED fires as rows,
never a bare cycle count. The census reads the harness's own
tasks-index.sqlite automation_runs table read-only; these tests pin the
rendering contract on a synthetic sqlite (no harness state needed):

- one FAIL row per non-succeeded fire, with fire time and run id
- counts + span + automation_row LIVE/DELETED on the census line
- HONEST-GAP fail-open when the index is absent or unreadable
- the zero-failure branch says FAIL (none), it does not go silent
"""
from __future__ import annotations

import sqlite3

import tools.arena_feed as af


def _make_index(tmp_path, fires, live=False):
    """A tasks-index.sqlite stand-in: automations + automation_runs with the
    same column shapes the real index carries (ms-epoch scheduled_at)."""
    db = tmp_path / "tasks-index.sqlite"
    con = sqlite3.connect(db)
    con.execute("create table automations (automation_id TEXT PRIMARY KEY)")
    con.execute(
        "create table automation_runs (run_id TEXT PRIMARY KEY, "
        "automation_id TEXT, scheduled_at INTEGER, outcome TEXT, error TEXT)")
    if live:
        con.execute("insert into automations values (?)", (af.ARENA_AUTOMATION_ID,))
    base = 1791032400000  # 2026-10-03T13:00:00Z in ms epoch
    for i, outcome in enumerate(fires):
        con.execute(
            "insert into automation_runs values (?, ?, ?, ?, ?)",
            (f"run-{i}", af.ARENA_AUTOMATION_ID, base + i * 3600000,
             outcome, None))
    con.commit()
    con.close()
    return db


def test_failed_fires_render_as_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(af, "TASKS_INDEX", _make_index(
        tmp_path, ["failed", "succeeded", "succeeded"]))
    lines = af.cadence_census()
    assert lines[0].startswith("ARENA CADENCE AS-OF ")
    assert "fires=3" in lines[1]
    assert "succeeded=2 failed=1" in lines[1]
    assert "span=2026-10-03T13:00:00Z..2026-10-03T15:00:00Z" in lines[1]
    assert "automation_row=DELETED" in lines[1]  # no automations row minted
    assert len(lines) == 3  # header + census + exactly one FAIL row
    fail = lines[2]
    assert fail.startswith("FAIL sched=2026-10-03T13:00:00Z outcome=failed")
    assert "run=run-0" in fail
    assert "err=None" in fail


def test_live_automation_and_zero_failures_say_so(tmp_path, monkeypatch):
    monkeypatch.setattr(af, "TASKS_INDEX", _make_index(
        tmp_path, ["succeeded", "succeeded"], live=True))
    lines = af.cadence_census()
    assert "succeeded=2 failed=0" in lines[1]
    assert "automation_row=LIVE" in lines[1]
    assert lines[2] == "FAIL (none): zero failed fires at this read"


def test_absent_index_fail_open_honest_gap(tmp_path, monkeypatch):
    monkeypatch.setattr(
        af, "TASKS_INDEX", tmp_path / "not-there.sqlite")
    lines = af.cadence_census()
    assert len(lines) == 1
    assert lines[0].startswith("ARENA CADENCE: HONEST-GAP - ")
