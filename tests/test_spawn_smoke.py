"""Smoke test for the orchestrator spawn path (mag.orchestrator.spawn_task).

The operator's recurring ask: "smoke test spawn." This exercises the REAL
spawn_task() entry point hermetically — no LLM, no network, no real child
process. We isolate TASK_DIR/LOG_DIR/TRAIL to temp dirs and monkeypatch
subprocess.Popen so the spawn path runs end-to-end (guards -> command build ->
task record -> persistence -> trail) without launching a sub-agent.

Covers the deterministic guards that gate every spawn:
  - empty goal refused
  - factory (frozen-build) gate refusal
  - same-goal dedupe while a task is running
  - real spawn: valid task record, correct command, status=running, persisted
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import uuid
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mag import orchestrator as orc


class _FakeProc:
    """Minimal stand-in for subprocess.Popen result used by _spawn_cmd."""

    def __init__(self, pid: int = 4242):
        self.pid = pid

    def poll(self) -> None:
        return None


def _isolate(monkeypatch) -> Path:
    """Point orchestrator state dirs at a temp tree; fake Popen."""
    tmp = Path(tempfile.mkdtemp())
    monkeypatch.setattr(orc, "TASK_DIR", tmp / "tasks")
    monkeypatch.setattr(orc, "LOG_DIR", tmp / "logs")
    monkeypatch.setattr(orc, "TRAIL", tmp / "trail.jsonl")
    monkeypatch.setattr(orc, "QUEUE_DIR", tmp / "queue")
    # Fake the child process so no real sub-agent / network is touched.
    monkeypatch.setattr(orc.subprocess, "Popen", lambda *a, **k: _FakeProc())
    return tmp


def test_spawn_empty_goal_refused(monkeypatch) -> None:
    _isolate(monkeypatch)
    r = orc.spawn_task("   ")
    assert r.get("ok") is False
    assert "empty goal" in r.get("error", "")
    print("PASS test_spawn_empty_goal_refused")


def test_spawn_factory_gate_refuses(monkeypatch) -> None:
    """A goal that trips the frozen-build gate must not spawn."""
    _isolate(monkeypatch)
    # Force the factory gate to reject by requiring a build that isn't frozen.
    r = orc.spawn_task("some goal", require_build="definitely-not-frozen-build")
    assert r.get("ok") is False
    assert r.get("factory_gate") is not None
    assert r.get("factory_gate", {}).get("ok") is False
    print("PASS test_spawn_factory_gate_refuses")


def test_spawn_dedupes_same_running_goal(monkeypatch) -> None:
    """Second spawn of the same goal while one is running is refused."""
    _isolate(monkeypatch)
    goal = "[smoke] dedupe spawn " + uuid.uuid4().hex[:6]
    r1 = orc.spawn_task(goal, provider="ollama")
    assert r1.get("ok") is True, f"first spawn failed: {r1}"
    tid1 = r1["task_id"]
    # Second spawn of the identical goal -> refused, points at existing task.
    r2 = orc.spawn_task(goal, provider="ollama")
    assert r2.get("ok") is False
    assert "duplicate" in str(r2.get("error", "")).lower()
    assert r2.get("existing") == tid1
    print("PASS test_spawn_dedupes_same_running_goal")


def test_spawn_real_path_builds_valid_task(monkeypatch) -> None:
    """Real spawn_task path: valid record, correct cmd, running, persisted."""
    tmp = _isolate(monkeypatch)
    goal = "[smoke] real spawn path " + uuid.uuid4().hex[:6]
    r = orc.spawn_task(goal, provider="ollama", tag="smoke")
    assert r.get("ok") is True, f"spawn failed: {r}"
    tid = r["task_id"]
    assert tid.startswith("t")
    assert r.get("status") == "running"
    assert r.get("goal") == goal
    assert r.get("tag") == "smoke"
    # Command must target main.py agent --query with the goal + provider.
    cmd = r.get("cmd") or []
    assert any("main.py" in c for c in cmd)
    assert "--query" in cmd
    assert cmd[cmd.index("--query") + 1] == goal
    assert "--provider" in cmd
    assert cmd[cmd.index("--provider") + 1] == "ollama"
    # Record persisted to the isolated TASK_DIR.
    saved = orc._load(tid)
    assert saved is not None
    assert saved["status"] == "running"
    assert saved["task_id"] == tid
    # Spawn trail written.
    trail = (tmp / "trail.jsonl").read_text(encoding="utf-8")
    assert "spawn" in trail and tid in trail
    print("PASS test_spawn_real_path_builds_valid_task")
