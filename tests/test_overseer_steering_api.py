from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def steer_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import mag.pigeonhole as ph

    mail_root = tmp_path / "mail"
    steering_log = tmp_path / "logs" / "steering_events.jsonl"
    monkeypatch.setattr(ph, "MAIL_ROOT", mail_root)
    monkeypatch.setattr(ph, "STEERING_LOG", steering_log)
    return {"mail_root": mail_root, "steering_log": steering_log}


def test_agent_steer_accept_and_status(monkeypatch: pytest.MonkeyPatch, steer_env):
    import mag.pigeonhole as ph
    from dashboard import rest

    monkeypatch.setattr(
        "mag.orchestrator.task_status",
        lambda tid: {"task_id": tid, "status": "running", "phase": "model"} if tid == "t1" else None,
    )

    code, body = rest.h_agent_steer_post(
        {"id": "t1"},
        {"context": "focus on contract tests", "source_tier": "E1", "reason": "test"},
    )
    assert code == 200
    assert body.get("ok") is True
    sid = body["data"]["steer_id"]

    code2, body2 = rest.h_agent_steer_status({"id": "t1", "steer_id": sid}, None)
    assert code2 == 200
    assert body2["data"]["status"] in ("accepted", "received")

    ph.ack_steer("t1", sid, status="applied", phase="model")
    code3, body3 = rest.h_agent_steer_status({"id": "t1", "steer_id": sid}, None)
    assert code3 == 200
    assert body3["data"]["status"] == "applied"
    assert body3["data"]["phase_at_apply"] == "model"


def test_agent_state_snapshot(monkeypatch: pytest.MonkeyPatch):
    from dashboard import rest

    monkeypatch.setattr(
        "mag.orchestrator.task_status",
        lambda tid: {
            "task_id": tid,
            "goal": "build api",
            "phase": "tool",
            "alive": True,
            "detail": "running",
            "status": "running",
        }
        if tid == "t2"
        else None,
    )

    code, body = rest.h_agent_state_snapshot({"id": "t2"}, None)
    assert code == 200
    assert body.get("schema") == "overseer.state_snapshot.v1"
    assert body["data"]["task_id"] == "t2"
    assert body["data"]["phase"] == "tool"


def test_coordination_gather(monkeypatch: pytest.MonkeyPatch):
    from dashboard import rest

    def fake_status(tid: str):
        if tid == "missing":
            return None
        return {
            "task_id": tid,
            "goal": f"goal {tid}",
            "phase": "model",
            "alive": True,
            "status": "running",
            "detail": "ok",
        }

    monkeypatch.setattr("mag.orchestrator.task_status", fake_status)

    code, body = rest.h_coordination_gather({}, {"task_ids": ["a1", "missing"]})
    assert code == 200
    assert body.get("schema") == "overseer.gather_response.v1"
    snaps = body["data"]["snapshots"]
    assert len(snaps) == 2
    assert snaps[0]["ok"] is True
    assert snaps[1]["ok"] is False


def test_governance_steering_log(monkeypatch: pytest.MonkeyPatch, steer_env):
    import mag.pigeonhole as ph
    from dashboard import rest

    sid = ph.post_steer("t3", "collect status", reason="audit", source_tier="E0")
    ph.ack_steer("t3", sid, status="applied", phase="model")

    code, body = rest.h_governance_steering_log({"limit": "10"}, None)
    assert code == 200
    assert body.get("schema") == "overseer.steering_log.v1"
    events = body["data"]["events"]
    assert events
    assert any(e.get("steer_id") == sid for e in events)


def test_governance_auto_steer_add(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from dashboard import rest

    monkeypatch.setattr(rest, "ROOT", tmp_path)
    code, body = rest.h_governance_auto_steer_add(
        {},
        {"trigger": "stalled", "threshold": 60, "action": "nudge", "chain_scope": "global"},
    )
    assert code == 200
    assert body.get("ok") is True
    rec = body["data"]
    assert rec["trigger"] == "stalled"
    p = tmp_path / "memory" / "governance" / "auto_steer_policies.json"
    assert p.is_file()


def test_overseer_manifest_and_events(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, steer_env):
    from dashboard import rest
    from mag import memory_events as me
    import mag.pigeonhole as ph

    events = tmp_path / "logs" / "memory_events.jsonl"
    checkpoints = tmp_path / "logs" / "memory_checkpoint_index.json"
    monkeypatch.setattr(me, "EVENTS_PATH", events)
    monkeypatch.setattr(me, "CHECKPOINT_INDEX", checkpoints)

    me.emit_route_decision(goal="doctor health", lane="local", reason="heuristic:local_ops", clerk_model="m:clerk", fallback_count=0)
    sid = ph.post_steer("t-manifest", "focus api", reason="test", source_tier="E1")
    assert sid

    code, body = rest.h_overseer_manifest({"limit": "100"}, None)
    assert code == 200
    assert body.get("schema") == "overseer.manifest.v1"
    tabs = body["data"]["tabs"]
    assert any(t.get("id") == "route" and t.get("count", 0) >= 1 for t in tabs)
    assert any(t.get("id") == "steer" and t.get("count", 0) >= 1 for t in tabs)
    assert body["data"]["invocation"]["id"] == "strike_the_chord"

    code2, body2 = rest.h_overseer_events({"tab": "route", "limit": "20"}, None)
    assert code2 == 200
    assert body2.get("schema") == "overseer.events.v1"
    assert all(str(e.get("event_kind") or "").startswith("route.") for e in body2["data"]["events"])


def test_overseer_events_bad_tab():
    from dashboard import rest

    code, body = rest.h_overseer_events({"tab": "nope"}, None)
    assert code == 400
    assert body.get("ok") is False
