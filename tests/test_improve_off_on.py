"""t73 (2026-09-25): the deliberate-off flow actually writes the marker.

t47 built the intentional-disable marker (logs/magimprove_intentional.flag,
read by mag/doctor.py) but no in-repo code path wrote it. This pins the t73
executor in mag/lifecycle.py:

  - improve_off writes the marker (cited in the result) then disables
  - improve_on re-registers then clears the marker, only on success
  - marker write failure aborts WITHOUT disabling (fail closed, negative)
  - task command failure keeps the marker (doctor still sees intentional)

The flag path is redirected to a tmp dir and the schtasks/powershell runner
is always mocked: the live MagImproveDaily task is never touched from a test.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import lifecycle  # noqa: E402


def _tmp_flag(monkeypatch, tmp_path: Path) -> Path:
    flag = tmp_path / "logs" / "magimprove_intentional.flag"
    monkeypatch.setattr(lifecycle, "IMPROVE_INTENTIONAL_FLAG", flag)
    return flag


def _mock_run(ok=True, calls=None):
    def _run(cmd):
        if calls is not None:
            calls.append(cmd)
        return {"ok": ok, "returncode": 0 if ok else 1, "cmd": " ".join(cmd),
                "stdout": "", "stderr": "" if ok else "mock failure"}
    return _run


def test_improve_off_writes_marker_then_disables(monkeypatch, tmp_path):
    flag = _tmp_flag(monkeypatch, tmp_path)
    calls: list[list[str]] = []
    r = lifecycle.improve_off(reason="t73 test", _run=_mock_run(ok=True, calls=calls))
    assert r["ok"] is True
    # the marker write is cited in the result and on disk
    assert r["marker"]["ok"] is True
    assert Path(r["marker"]["path"]).name == "magimprove_intentional.flag"
    payload = json.loads(flag.read_text(encoding="utf-8"))
    assert payload["reason"] == "t73 test"
    assert payload["by"] == "mag.lifecycle.mark_improve_intentional"
    # the disable went through the injectable runner, not the live scheduler
    assert calls == [["schtasks", "/Change", "/TN", "MagImproveDaily", "/Disable"]]
    # the reader the doctor uses sees the marker
    assert lifecycle.improve_intentional() == payload


def test_improve_on_clears_marker_after_success(monkeypatch, tmp_path):
    flag = _tmp_flag(monkeypatch, tmp_path)
    flag.parent.mkdir(parents=True, exist_ok=True)
    flag.write_text('{"ts": "x", "reason": "old", "by": "t73"}', encoding="utf-8")
    calls: list[list[str]] = []
    r = lifecycle.improve_on(_run=_mock_run(ok=True, calls=calls))
    assert r["ok"] is True
    assert r["marker_cleared"]["removed"] is True
    assert not flag.exists()
    assert lifecycle.improve_intentional() is None
    assert calls and "register_improve_task.ps1" in calls[0][-1]


def test_marker_write_failure_aborts_without_disabling(monkeypatch, tmp_path):
    # negative first-class: a failed marker write must NOT create a
    # silent-disabled state (fail closed).
    _tmp_flag(monkeypatch, tmp_path / "no" / "write" / "here")
    monkeypatch.setattr(lifecycle, "mark_improve_intentional",
                        lambda reason="": {"ok": False, "path": "x", "error": "boom"})
    calls: list[list[str]] = []
    r = lifecycle.improve_off(_run=_mock_run(ok=True, calls=calls))
    assert r["ok"] is False
    assert r["task"] is None
    assert calls == []  # the disable was never attempted
    assert "NOT disabled" in r["error"]


def test_task_failure_keeps_marker(monkeypatch, tmp_path):
    # negative first-class: failed re-register leaves the marker so the
    # doctor probe still reads the Disabled state as intentional.
    flag = _tmp_flag(monkeypatch, tmp_path)
    flag.parent.mkdir(parents=True, exist_ok=True)
    flag.write_text('{"ts": "x", "reason": "old", "by": "t73"}', encoding="utf-8")
    r = lifecycle.improve_on(_run=_mock_run(ok=False))
    assert r["ok"] is False
    assert r["marker_cleared"] is False
    assert flag.exists()  # marker kept


def test_clear_is_idempotent(monkeypatch, tmp_path):
    flag = _tmp_flag(monkeypatch, tmp_path)
    r = lifecycle.clear_improve_intentional()
    assert r["ok"] is True
    assert r["removed"] is False
    assert not flag.exists()


def test_waste_action_improve_prescribes_t73_executor():
    # t77: the lifecycle UI's waste remediation must name the landed t73
    # executor commands exactly (flags per main.py argparse: improve-off takes
    # --reason, improve-on takes none), not the old prose.
    action = lifecycle._waste_action("improve")
    assert 'python main.py improve-off --reason "..."' in action
    assert "python main.py improve-on" in action
    # negative first-class: the old prose prescription is gone.
    assert "stop improve jobs" not in action
    # other pieces keep their actions untouched.
    assert lifecycle._waste_action("engine") == "unset MAG_ENGINE_CMD"
