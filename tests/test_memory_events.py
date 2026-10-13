from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def memory_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import mag.memory_events as me

    events = tmp_path / "logs" / "memory_events.jsonl"
    checkpoints = tmp_path / "logs" / "memory_checkpoint_index.json"
    monkeypatch.setattr(me, "EVENTS_PATH", events)
    monkeypatch.setattr(me, "CHECKPOINT_INDEX", checkpoints)
    return {"events": events, "checkpoints": checkpoints}


def test_emit_event_schema(memory_env):
    import mag.memory_events as me

    out = me.emit_event(
        event_kind="route.decision",
        seat="router",
        session_id="s1",
        tier="T2",
        payload={"lane": "local"},
    )
    assert out["ok"] is True
    row = json.loads(memory_env["events"].read_text(encoding="utf-8").splitlines()[0])
    assert row["schema"] == me.SCHEMA
    assert row["event_kind"] == "route.decision"
    assert row["seat"] == "router"
    assert row["session_id"] == "s1"
    assert row["tier"] == "T2"
    assert row["scope_hash"]


def test_checkpoint_summary_dedupes_by_state_hash(memory_env):
    import mag.memory_events as me

    first = me.emit_checkpoint_summary(
        seat="agent",
        session_id="s1",
        tier="T2",
        summary_kind="round_end",
        summary={"phase": "tool", "step": 3},
    )
    second = me.emit_checkpoint_summary(
        seat="agent",
        session_id="s1",
        tier="T2",
        summary_kind="round_end",
        summary={"phase": "tool", "step": 3},
    )
    assert first["ok"] is True
    assert second.get("skipped") is True
    lines = memory_env["events"].read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_route_goal_emits_memory_event(memory_env, monkeypatch: pytest.MonkeyPatch):
    import mag.route as route

    monkeypatch.setattr("mag.route.model_for", lambda role: f"m:{role}")
    out = route.route_goal("doctor health status")
    assert out["ok"] is True
    rows = [json.loads(line) for line in memory_env["events"].read_text(encoding="utf-8").splitlines()]
    assert any(r.get("event_kind") == "route.decision" for r in rows)


def test_steer_event_emits_memory_event(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import mag.memory_events as me
    import mag.pigeonhole as ph

    mail_root = tmp_path / "mail"
    steering_log = tmp_path / "logs" / "steering_events.jsonl"
    events = tmp_path / "logs" / "memory_events.jsonl"
    checkpoints = tmp_path / "logs" / "memory_checkpoint_index.json"

    monkeypatch.setattr(ph, "MAIL_ROOT", mail_root)
    monkeypatch.setattr(ph, "STEERING_LOG", steering_log)
    monkeypatch.setattr(me, "EVENTS_PATH", events)
    monkeypatch.setattr(me, "CHECKPOINT_INDEX", checkpoints)

    sid = ph.post_steer("t-memory", "focus on tests", reason="pytest", source_tier="E1")
    assert sid.startswith("sid-")
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    assert any(r.get("event_kind") == "steer.accepted" for r in rows)
