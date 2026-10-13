"""The autonomy switch is durable, atomic, and visible to shared gates."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from mag import operator_mode as om


def test_pause_resume_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(om, "STATE_PATH", tmp_path / "state" / "operator_mode.json")
    monkeypatch.setattr(om, "TRAIL_PATH", tmp_path / "state" / "operator_mode.jsonl")

    assert om.pause_reason() is None
    paused = om.set_paused(reason="overnight hold", requested_by="test")
    assert paused["mode"] == "paused"
    assert om.is_paused()
    assert "overnight hold" in (om.pause_reason() or "")
    assert len((tmp_path / "state" / "operator_mode.jsonl").read_text().splitlines()) == 1

    resumed = om.resume(requested_by="test")
    assert resumed["effective_mode"] == "running"
    assert not om.is_paused()
    assert len((tmp_path / "state" / "operator_mode.jsonl").read_text().splitlines()) == 2


def test_expired_pause_is_not_effective(tmp_path, monkeypatch):
    monkeypatch.setattr(om, "STATE_PATH", tmp_path / "operator_mode.json")
    monkeypatch.setattr(om, "TRAIL_PATH", tmp_path / "operator_mode.jsonl")
    past = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat().replace("+00:00", "Z")
    om.set_paused(reason="expired", until=past)
    state = om.read()
    assert state["mode"] == "paused"
    assert state["effective_mode"] == "running"
    assert not om.is_paused()


def test_invalid_control_file_holds_autonomy(tmp_path, monkeypatch):
    path = tmp_path / "operator_mode.json"
    monkeypatch.setattr(om, "STATE_PATH", path)
    path.write_text(json.dumps({"schema": "wrong", "mode": "running"}), encoding="utf-8")
    assert om.is_paused()
    assert "invalid" in (om.pause_reason() or "")
