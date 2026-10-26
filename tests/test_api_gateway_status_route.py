"""t39 (2026-09-25): GET /status surfaces the scheduled-task probe.

Dispatch-level tests against the gateway registry, no HTTP server. The
doctor probe is mocked at mag.doctor.check_scheduled_tasks (the route
lazy-imports it at call time), so no schtasks subprocess runs here and a
not-Ready state is reproducible on any machine. Non-Windows behavior
(null payload, no doctor call) is covered too: negatives are first-class.
"""
from __future__ import annotations

from mag import api_gateway as gw

HDR = {"X-API-Key": "mag-local-dev-key"}


def test_status_carries_scheduled_task_and_clean_warning(monkeypatch):
    hits = []

    def fake_check(*a, **k):
        hits.append(1)
        return {"check": "scheduled_tasks", "ok": True,
                "statuses": {"MagImproveDaily": "Ready"}, "issues": []}

    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", fake_check)
    s, payload = gw.dispatch("GET", "/status", headers=HDR)
    assert s == 200
    assert hits, "route must call the doctor probe via its lazy import"
    assert payload["scheduled_task"]["ok"] is True
    assert payload["scheduled_task"]["statuses"]["MagImproveDaily"] == "Ready"
    assert payload["warning"] is None


def test_status_not_ready_flips_warning(monkeypatch):
    def fake_check(*a, **k):
        return {"check": "scheduled_tasks", "ok": False,
                "statuses": {"MagImproveDaily": "Disabled"},
                "issues": ["SCHEDULED TASK DISABLED: 'MagImproveDaily' is Disabled, "
                           "its job silently stopped"]}

    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", fake_check)
    s, payload = gw.dispatch("GET", "/status", headers=HDR)
    assert s == 200
    assert payload["scheduled_task"]["ok"] is False
    assert payload["warning"], "not-Ready must flip the warning flag"
    assert "DISABLED" in payload["warning"]


def test_status_non_windows_returns_null_without_doctor_call(monkeypatch):
    hits = []

    def fake_check(*a, **k):
        hits.append(1)
        return {"check": "scheduled_tasks", "ok": True, "statuses": {},
                "issues": []}

    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", fake_check)
    monkeypatch.setattr("os.name", "posix")
    s, payload = gw.dispatch("GET", "/status", headers=HDR)
    assert s == 200
    assert payload["scheduled_task"] is None, "non-Windows must be null cleanly"
    assert payload["warning"] is None
    assert not hits, "non-Windows must not touch the doctor probe"
