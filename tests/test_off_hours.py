from __future__ import annotations

from datetime import datetime, timezone

from mag import off_hours


def _config(tmp_path):
    path = tmp_path / "off_hours.yaml"
    path.write_text(
        """
schema: off_hours.v1
timezone: UTC
default_policy: defer_heavy
windows:
  - id: overnight
    days: [sun, mon, tue, wed, thu, fri, sat]
    start: '22:00'
    end: '07:00'
immediate_keywords: [fleet, repair, gateway, queue, liveness]
overnight_keywords: [coding, game, gaming, shader]
overnight_lane:
  id: overnight-5.3-max
  provider: z_ai
  model: glm-5.3
""",
        encoding="utf-8",
    )
    return path


def test_fleet_operation_bypasses_implicit_heavy_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(off_hours, "CONFIG", _config(tmp_path))
    monkeypatch.setattr(off_hours, "_tz", lambda _config: ("UTC", timezone.utc))
    decision = off_hours.classify(goal="repair the fleet gateway queue after a crash")
    assert decision["work_class"] == "fleet_operation"
    assert decision["schedule_policy"] == "anytime"

    noon = datetime(2026, 8, 30, 12, tzinfo=timezone.utc)
    result = off_hours.eligibility({"goal": "repair the fleet gateway full codebase"}, now=noon)
    assert result["eligible"] is True
    assert result["reason"] == "anytime"


def test_coding_uses_overnight_lane_only_when_window_is_open(tmp_path, monkeypatch):
    monkeypatch.setattr(off_hours, "CONFIG", _config(tmp_path))
    monkeypatch.setattr(off_hours, "_tz", lambda _config: ("UTC", timezone.utc))
    task = {"goal": "coding build for the game shader", "provider": "deepseek", "model": "deepseek-chat"}
    classified = off_hours.decorate(dict(task))
    assert classified["work_class"] == "gaming"
    assert classified["heavy"] is True
    assert classified["schedule_policy"] == "off_hours"

    noon = datetime(2026, 8, 30, 12, tzinfo=timezone.utc)
    late = datetime(2026, 8, 30, 23, tzinfo=timezone.utc)
    assert off_hours.eligibility(task, now=noon)["eligible"] is False
    routed = off_hours.dispatch_spec(task, now=late)
    assert routed["rerouted"] is True
    assert routed["provider"] == "z_ai"
    assert routed["model"] == "glm-5.3"
    assert routed["lane_id"] == "overnight-5.3-max"


def test_force_is_an_explicit_immediate_escape_hatch(tmp_path, monkeypatch):
    monkeypatch.setattr(off_hours, "CONFIG", _config(tmp_path))
    monkeypatch.setattr(off_hours, "_tz", lambda _config: ("UTC", timezone.utc))
    task = {"goal": "coding build", "provider": "deepseek", "model": "deepseek-chat"}
    noon = datetime(2026, 8, 30, 12, tzinfo=timezone.utc)
    result = off_hours.eligibility(task, now=noon, force=True)
    assert result["eligible"] is True
    routed = off_hours.dispatch_spec(task, now=noon, force=True)
    assert routed["rerouted"] is False
    assert routed["provider"] == "deepseek"
