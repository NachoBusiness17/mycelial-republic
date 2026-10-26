"""tests/test_lane_budget.py - W3 mechanism 1: pre-bound metered lane budgets.

Covers the three contract cases from the W3 lane ask (2026-09-29):
1. exhaustion raises AND the death receipt row lands in deaths.jsonl first;
2. a resumed lane inherits the REMAINING budget from its checkpoint;
3. no budget = unmetered, explicitly (UNMETERED / all-None caps never halt).

Instrument: pytest on tests/test_lane_budget.py only.
"""
from __future__ import annotations

import json

import pytest

from tools.lane_budget import UNMETERED, Budget, BudgetExhausted


def _rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


# --- 1. exhaustion raises + receipt written ----------------------------------


def test_actions_exhaustion_raises_and_writes_death_receipt(tmp_path):
    deaths = tmp_path / "deaths.jsonl"
    budget = Budget(
        "steal-mine-7",
        max_actions=2,
        deaths_path=deaths,
        checkpoint_path=tmp_path / "ckpt.json",
    )
    budget.spend()
    budget.spend()  # reaching the cap exactly is still legal
    with pytest.raises(BudgetExhausted) as excinfo:
        budget.spend()  # the fatal third action

    assert excinfo.value.reason == "actions"
    assert excinfo.value.budget_name == "steal-mine-7"

    rows = _rows(deaths)
    assert len(rows) == 1, "one corpse, one epitaph"
    row = rows[0]
    assert set(row) == {"lane", "reason", "spent", "ts"}, "receipt contract shape"
    assert row["lane"] == "steal-mine-7"
    assert row["reason"] == "actions"
    assert row["spent"]["actions"] == 3, "fatal spend is spent, not rolled back"
    assert row["ts"]


def test_re_spending_a_dead_budget_writes_no_second_receipt(tmp_path):
    deaths = tmp_path / "deaths.jsonl"
    budget = Budget("zombie", max_actions=1, deaths_path=deaths)
    budget.spend()
    with pytest.raises(BudgetExhausted):
        budget.spend()
    with pytest.raises(BudgetExhausted):
        budget.spend()  # re-raise, no new epitaph
    assert len(_rows(deaths)) == 1


def test_reported_seconds_dimension_halts(tmp_path):
    deaths = tmp_path / "deaths.jsonl"
    budget = Budget(
        "night-burn", max_seconds=0.2, deaths_path=deaths
    )
    with pytest.raises(BudgetExhausted) as excinfo:
        budget.spend(seconds=0.5)  # child-lane reported time past the cap
    assert excinfo.value.reason == "seconds"
    assert _rows(deaths)[0]["reason"] == "seconds"


def test_wall_clock_halts_without_caller_reporting(tmp_path, monkeypatch):
    """S22 auto-stop: elapsed time trips the cap with seconds=0 reported."""
    import tools.lane_budget as lb

    clock = iter([100.0, 105.0])
    monkeypatch.setattr(lb.time, "monotonic", lambda: next(clock))
    budget = Budget("wall-clocked", max_seconds=4.0, deaths_path=tmp_path / "d.jsonl")
    with pytest.raises(BudgetExhausted) as excinfo:
        budget.spend()  # 5s of wall elapsed, nothing reported
    assert excinfo.value.reason == "seconds"


def test_usd_dimension_halts(tmp_path):
    deaths = tmp_path / "deaths.jsonl"
    budget = Budget(
        "pilot", max_usd_estimate=0.5, deaths_path=deaths
    )
    with pytest.raises(BudgetExhausted) as excinfo:
        budget.spend(usd=0.75)
    assert excinfo.value.reason == "usd_estimate"
    assert _rows(deaths)[0]["spent"]["usd_estimate"] == 0.75


def test_death_receipt_written_before_the_raise(tmp_path):
    """The receipt must already be on disk inside the except block."""
    deaths = tmp_path / "deaths.jsonl"
    budget = Budget("ordering", max_actions=1, deaths_path=deaths)
    caught = False
    try:
        budget.spend()
        budget.spend()
    except BudgetExhausted:
        caught = True
        assert deaths.exists() and len(_rows(deaths)) == 1
    assert caught


# --- 2. resume inherits remaining ---------------------------------------------


def test_context_manager_writes_checkpoint_and_resume_inherits(tmp_path):
    deaths = tmp_path / "deaths.jsonl"
    ckpt = tmp_path / "ckpt.json"

    with Budget(
        "multi-cycle", max_actions=3, deaths_path=deaths, checkpoint_path=ckpt
    ) as first:
        first.spend()
        first.spend()  # 2 of 3 spent; clean exit banks the remainder

    assert ckpt.exists()
    state = json.loads(ckpt.read_text(encoding="utf-8"))
    assert state["schema"] == "lane_budget.v1"
    assert state["caps"]["max_actions"] == 3
    assert state["spent"]["actions"] == 2

    with Budget.resume(ckpt, deaths_path=deaths) as resumed:
        assert resumed.remaining()["actions"] == 1
        resumed.spend()  # the inherited third action is legal
        with pytest.raises(BudgetExhausted):
            resumed.spend()  # the fourth trips the SAME pre-bound cap
        assert resumed._dead
    rows = _rows(deaths)
    assert len(rows) == 1 and rows[0]["lane"] == "multi-cycle"
    assert rows[0]["spent"]["actions"] == 4


def test_resume_cannot_launder_a_dead_budget(tmp_path):
    ckpt = tmp_path / "ckpt.json"
    with Budget("dead-walk", max_actions=1, checkpoint_path=ckpt) as b:
        try:
            b.spend()
            b.spend()
        except BudgetExhausted:
            pass  # exhaustion inside the with: exit still checkpoints (dead=True)
    revived = Budget.resume(ckpt)
    assert revived._dead
    with pytest.raises(BudgetExhausted):
        revived.spend()


def test_resume_rejects_foreign_schema(tmp_path):
    ckpt = tmp_path / "ckpt.json"
    ckpt.write_text(json.dumps({"schema": "other.v9"}), encoding="utf-8")
    with pytest.raises(ValueError):
        Budget.resume(ckpt)


# --- 3. no budget = unmetered (explicit) ---------------------------------------


def test_unmetered_never_halts_and_writes_nothing(tmp_path):
    UNMETERED.spend(n=10**9, seconds=10**9, usd=10**9)
    with UNMETERED as u:  # same context-manager surface as Budget
        u.spend(5, seconds=5.0, usd=5.0)
    assert UNMETERED.remaining() == {
        "actions": None,
        "seconds": None,
        "usd_estimate": None,
    }
    assert UNMETERED.checkpoint() is None


def test_all_none_caps_is_an_explicit_meter_that_never_halts(tmp_path):
    """A Budget with no caps still meters (spent() counts) but cannot halt."""
    budget = Budget(
        "sensing-only",
        deaths_path=tmp_path / "deaths.jsonl",
        checkpoint_path=tmp_path / "ckpt.json",
    )
    totals = budget.spend(n=10_000, usd=999.0)
    assert totals["actions"] == 10_000
    assert not (tmp_path / "deaths.jsonl").exists()


def test_unmetered_is_a_singleton_token_in_code():
    from tools.lane_budget import UNMETERED as again

    assert again is UNMETERED
    assert UNMETERED.name == "UNMETERED"
