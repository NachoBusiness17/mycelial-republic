"""t33 (2026-09-25): improve --status must announce a not-Ready scheduled task.

t20's doctor probe (mag/doctor.check_scheduled_tasks) only ran when someone
asked doctor. lifecycle.py already prescribes the t73 executor
("python main.py improve-off --reason ... / improve-on"; prose aligned
by t77, hint by t81) as a remediation, so disablement is a known state;
the seat surface has to say so.
These tests pin the wiring in mag/improve.py:

  - status_summary embeds the scheduled_task check (reused via import)
  - ONE WARNING line on stderr when the task is not Ready
  - no WARNING when Ready or when the check skips (non-Windows)
  - the schtasks output is mocked; no subprocess runs in these tests
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import improve  # noqa: E402

_ISSUE_DISABLED = (
    "SCHEDULED TASK DISABLED: 'MagImproveDaily' is Disabled, its job silently "
    "stopped. Re-enable (elevated): schtasks /Change /TN MagImproveDaily /ENABLE"
)


def test_status_summary_embeds_scheduled_task_ok(monkeypatch, capsys):
    stub = {"check": "scheduled_tasks", "ok": True,
            "statuses": {"MagImproveDaily": "Ready"}, "issues": []}
    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", lambda *a, **k: stub)
    res = improve.status_summary()
    assert res["scheduled_task"]["ok"] is True
    assert res["scheduled_task"]["statuses"] == {"MagImproveDaily": "Ready"}
    assert "WARNING" not in capsys.readouterr().err


def test_disabled_task_prints_one_warning_line(monkeypatch, capsys):
    stub = {"check": "scheduled_tasks", "ok": False,
            "statuses": {"MagImproveDaily": "Disabled"},
            "issues": [_ISSUE_DISABLED]}
    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", lambda *a, **k: stub)
    res = improve.status_summary()
    err = capsys.readouterr().err
    assert res["scheduled_task"]["ok"] is False
    assert "WARNING" in err
    assert "MagImproveDaily" in err
    assert len([ln for ln in err.splitlines() if "WARNING" in ln]) == 1


def test_skipped_platform_prints_no_warning(monkeypatch, capsys):
    stub = {"check": "scheduled_tasks", "ok": True, "statuses": {},
            "issues": [],
            "note": "skipped: schtasks is Windows-only (platform=posix)"}
    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", lambda *a, **k: stub)
    res = improve.status_summary()
    assert res["scheduled_task"]["ok"] is True
    assert "WARNING" not in capsys.readouterr().err


def test_seat_surface_routes_through_doctor(monkeypatch):
    # The import path must be mag.doctor.check_scheduled_tasks itself:
    # reuse, not a duplicated schtasks call.
    calls = []

    def fake(*a, **k):
        calls.append((a, k))
        return {"check": "scheduled_tasks", "ok": True,
                "statuses": {}, "issues": []}

    monkeypatch.setattr("mag.doctor.check_scheduled_tasks", fake)
    improve.status_summary()
    assert calls, "status_summary never reached mag.doctor.check_scheduled_tasks"
    # The probe's tracked task set is doctor's own; the seat adds no task list.
    from mag import doctor  # noqa: E402
    assert "MagImproveDaily" in doctor.SCHEDULED_TASKS
