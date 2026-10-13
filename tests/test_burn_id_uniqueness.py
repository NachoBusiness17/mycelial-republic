"""Burn-ledger ask-id uniqueness (2026-10-03 process-improve wave 1).

The disease: dungeon and tavern minted bank ids from the TURN NUMBER alone
(DND0_beat7_dm, TAVERN_r3_JUDGE), so every session after the first re-rows
the same (id, turn) key in memory/runs/hermes_burn/usage.jsonl and trips the
instance_guard doubled-key re-fire alarm — 217 false re-fire rows plus an
800-line attention.md flood on arena day 2026-10-03. The cure: ids embed the
per-session tag. Receipt: watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import dungeon, tavern  # noqa: E402
from tools.hermes_burn import PRICING  # noqa: E402


def _fake_call(model, messages, max_tokens, key):
    return {"choices": [{"message": {"content": "a beat"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5}}


def _bank_capture(bucket):
    def _bank(row):
        bucket.append(row)
    return _bank


def test_dungeon_ids_unique_across_sessions(tmp_path, monkeypatch):
    monkeypatch.setattr(dungeon, "PLAY_DIR", tmp_path)
    monkeypatch.setattr(dungeon, "_hermes_key", lambda: "k")
    monkeypatch.setattr(dungeon, "_call", _fake_call)
    ids = []
    monkeypatch.setattr(dungeon, "_bank", _bank_capture(ids))
    # stamps are second-resolution: force different now() per construction so
    # two sessions in one test tick can't share a stamp (live sessions are
    # minutes apart; the collision that mattered live was same NAME, not time)
    from datetime import datetime, timezone

    class FakeDT(datetime):
        _t = 0

        @classmethod
        def now(cls, tz=None):
            cls._t += 1
            return datetime(2026, 10, 3, 22, 0, cls._t, tzinfo=timezone.utc)
    monkeypatch.setattr(dungeon, "datetime", FakeDT)
    stamps = []
    for _ in range(2):
        g = dungeon.Dungeon(tip="t", dry=False, budget=1.0)
        stamps.append(g.tag)
        g.turn = 7
        g._dm("test beat")
    assert stamps[0] != stamps[1]  # per-session tags differ
    assert len(ids) == 2
    assert ids[0]["id"] == f"{stamps[0]}_beat7_dm"
    assert ids[1]["id"] == f"{stamps[1]}_beat7_dm"
    # the property that failed live: same beat number, different session,
    # different ledger key (no doubled-key false alarm)
    assert ids[0]["id"] != ids[1]["id"]


def test_tavern_ids_carry_the_run(tmp_path, monkeypatch):
    monkeypatch.setattr(tavern, "PLAY_DIR", tmp_path)
    monkeypatch.setattr(tavern, "_call", _fake_call)
    ids = []
    monkeypatch.setattr(tavern, "_bank", _bank_capture(ids))
    scenario = {"title": "test tavern", "room": "r", "objects": ["mug"],
                "personas": [{"name": "greta", "model": next(iter(PRICING)),
                              "register": "gruff", "want": "quiet",
                              "secret": "past", "tell": "sniff"}]}
    run = tavern.Run(scenario, rounds=2, budget_usd=1.0, dry=False,
                     judge_model=None, chain_tip="t")
    run.key = "k"
    assert run.run.startswith("TAVERN_")  # the docstring law, now in code
    run.bar_round(3)  # round 3 of a DIFFERENT run must not collide with another run's r3
    assert ids, "bar_round must bank at least one row"
    assert all(r["id"].startswith(run.run + "_r3_") for r in ids)
