"""t20 (2026-09-25): silent disablement of scheduled tasks must surface in doctor.

Before this probe, a disabled or deleted MagImproveDaily task kept the daily
improve job silently undone and no doctor check said a word. These tests pin
the probe in mag/doctor.py:

  - LIST output parsing (real schtasks /FO LIST shape)
  - Ready/Running pass, Disabled/MISSING/unqueryable are flagged
  - non-Windows platforms skip cleanly
  - the check is wired into examine() (the doctor output path)
  - one live probe on Windows (shape only; machine state is not asserted)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import doctor  # noqa: E402

_LIST_READY = """\

Folder: \\
HostName:      DESKTOP-XYZ
TaskName:      \\MagImproveDaily
Next Run Time: 2026-09-26 08:00:00
Status:        Ready
Logon Mode:    Interactive only

"""


def test_parse_list_extracts_status():
    assert doctor._parse_schtask_list(_LIST_READY) == "Ready"


def test_parse_list_missing_status_returns_unknown():
    assert doctor._parse_schtask_list("no status line here") == "?"


def test_ready_task_passes():
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "Ready")
    assert r["check"] == "scheduled_tasks"
    assert r["ok"] is True
    assert r["issues"] == []
    assert r["statuses"] == {"MagImproveDaily": "Ready"}


def test_running_task_passes():
    # Running implies registered + enabled; flagging it would false-alarm mid-run.
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "Running")
    assert r["ok"] is True


def test_disabled_task_is_flagged():
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "Disabled")
    assert r["ok"] is False
    assert any("MagImproveDaily" in i and "DISABLED" in i for i in r["issues"])
    assert any("python main.py improve-on" in i for i in r["issues"])  # t82: t73 executor first
    assert any("/ENABLE" in i for i in r["issues"])  # elevated fallback kept


def test_disabled_remediation_never_skips_marker_clearing():
    # t82 negative: any issue string naming the raw /ENABLE fallback must
    # prescribe `python main.py improve-on` (t73 executor, which clears the
    # intentional marker on success) BEFORE it, so the doctor never points
    # an operator at a remediation that leaves the marker stale.
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "Disabled")
    assert r["ok"] is False
    for i in r["issues"]:
        if "/ENABLE" in i:
            assert "improve-on" in i
            assert i.index("improve-on") < i.index("/ENABLE")


def test_missing_task_is_flagged():
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "MISSING")
    assert r["ok"] is False
    assert any("MagImproveDaily" in i and "not registered" in i for i in r["issues"])


def test_unqueryable_task_is_flagged():
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "?")
    assert r["ok"] is False
    assert any("UNQUERYABLE" in i for i in r["issues"])


def test_odd_status_is_flagged_not_ready():
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "Queued")
    assert r["ok"] is False
    assert any("NOT READY" in i and "Queued" in i for i in r["issues"])


def test_non_windows_platform_skips():
    r = doctor.check_scheduled_tasks(_platform="posix")
    assert r["ok"] is True
    assert "skipped" in r.get("note", "")


def test_wired_into_examine(monkeypatch):
    stub = {"check": "scheduled_tasks", "ok": True, "statuses": {}, "issues": []}
    monkeypatch.setattr(doctor, "check_scheduled_tasks", lambda *a, **k: stub)
    report = doctor.examine()
    names = [c["check"] for c in report.checks]
    assert "scheduled_tasks" in names


def test_live_probe_on_windows():
    if os.name != "nt":
        return
    # Live probe asserts the report SHAPE only; whether MagImproveDaily is
    # currently Ready is machine state, not a property of the probe.
    r = doctor.check_scheduled_tasks()
    assert "statuses" in r
    assert "MagImproveDaily" in r["statuses"]
    assert isinstance(r["ok"], bool)


# --- t47 (2026-09-25): intentional-vs-silent disablement ---------------------
# A Disabled task with lifecycle's intentional-disable marker
# (logs/magimprove_intentional.flag) is a declared state, not an alarm;
# a MISSING task still alarms even with the marker (disable is not delete).

_MARKER = {"ts": "2026-09-25T00:00:00+00:00", "reason": "test", "by": "t47"}


def test_disabled_with_intentional_marker_passes():
    r = doctor.check_scheduled_tasks(
        _status_fn=lambda t: "Disabled", _intentional_fn=lambda: _MARKER)
    assert r["ok"] is True
    assert r["issues"] == []
    assert r["intentional"] == {"MagImproveDaily": _MARKER}


def test_disabled_without_marker_still_flags():
    r = doctor.check_scheduled_tasks(
        _status_fn=lambda t: "Disabled", _intentional_fn=lambda: None)
    assert r["ok"] is False
    assert any("DISABLED" in i for i in r["issues"])


def test_missing_with_marker_still_flags():
    r = doctor.check_scheduled_tasks(
        _status_fn=lambda t: "MISSING", _intentional_fn=lambda: _MARKER)
    assert r["ok"] is False
    assert any("not registered" in i for i in r["issues"])
    assert r["intentional"] == {}


def test_default_intentional_reader_is_lifecycle():
    # The default reader is mag.lifecycle.improve_intentional (lazy import);
    # it must be readable and return the marker dict or None, never raise.
    from mag import lifecycle
    r = doctor.check_scheduled_tasks(_status_fn=lambda t: "Ready")
    assert isinstance(r["intentional"], dict)
    assert callable(lifecycle.improve_intentional)
    assert lifecycle.improve_intentional_flag_path().name == "magimprove_intentional.flag"
