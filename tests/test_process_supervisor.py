"""Tests for the process supervisor (mag.process_supervisor)."""
import json
from pathlib import Path

import pytest

import mag.process_supervisor as ps


@pytest.fixture(autouse=True)
def _isolate_state(tmp_path, monkeypatch):
    """Point the supervisor at a temp state/log so tests don't touch real state."""
    monkeypatch.setattr(ps, "STATE_PATH", tmp_path / "state.json")
    monkeypatch.setattr(ps, "LOG_PATH", tmp_path / "supervisor.jsonl")
    return tmp_path


def test_status_initial(_isolate_state):
    st = ps.status()
    assert st["ok"] is True
    names = {l["name"] for l in st["loops"]}
    assert {"autorun", "ghost"} <= names
    assert st["running"] == []


def test_start_loop_monkeypatched_spawn(_isolate_state, monkeypatch):
    monkeypatch.setattr(ps, "_spawn", lambda name: {"pid": 4242, "started_at": "t", "cmd": "x"})
    monkeypatch.setattr(ps, "_pid_alive", lambda pid: True)
    r = ps.start_loop("autorun")
    assert r["ok"] is True and r["started"] is True and r["pid"] == 4242
    # already running now
    r2 = ps.start_loop("autorun")
    assert r2["already_running"] is True
    assert r2["pid"] == 4242


def test_stop_loop_removes_state(_isolate_state, monkeypatch):
    monkeypatch.setattr(ps, "_spawn", lambda name: {"pid": 7, "started_at": "t", "cmd": "x"})
    monkeypatch.setattr(ps, "_pid_alive", lambda pid: True)
    killed = []
    monkeypatch.setattr(ps, "_kill_tree", lambda pid: killed.append(pid))
    ps.start_loop("ghost")
    r = ps.stop_loop("ghost")
    assert r["ok"] is True and r["stopped"] is True
    assert killed == [7]
    # state cleared
    assert json.loads(ps.STATE_PATH.read_text(encoding="utf-8")) == {}


def test_reap_marks_crashed(_isolate_state, monkeypatch):
    monkeypatch.setattr(ps, "_spawn", lambda name: {"pid": 99, "started_at": "t", "cmd": "x"})
    # First start reports alive, then pid becomes dead
    alive = {"v": True}
    monkeypatch.setattr(ps, "_pid_alive", lambda pid: alive["v"])
    ps.start_loop("autorun")
    alive["v"] = False
    # auto_restart=False isolates the crash-marking (default auto_restart respawns
    # the loop, so status would be 'running' again — the respawn is a separate concern).
    r = ps.reap(auto_restart=False)
    assert "autorun" in r["crashed"]
    st = ps.status()
    autorun = next(l for l in st["loops"] if l["name"] == "autorun")
    assert autorun["status"] == "crashed"


class _FakeTime:
    def __init__(self, start: float = 1000.0):
        self.now = start

    def time(self) -> float:
        return self.now


def test_reap_crash_loop_backoff_no_storm(_isolate_state, monkeypatch):
    # A default loop that dies instantly must NOT be respawned every instant
    # (the 2026-08-09 window-storm source) — crashLoopBackOff throttles it.
    ft = _FakeTime(1000.0)
    monkeypatch.setattr(ps, "time", ft)
    monkeypatch.setattr(ps, "_pid_alive", lambda pid: False)  # always looks dead
    monkeypatch.setattr(ps, "_spawn", lambda name: {"pid": 100, "started_at": "t", "cmd": "x"})
    ps.start_loop("autorun")
    restarted = 0
    for _ in range(10):
        restarted += len(ps.reap()["auto_restarted"])
    # first crash sets a backoff; nothing respawns within the same instant
    assert restarted == 0
    st = ps.status()
    autorun = next(l for l in st["loops"] if l["name"] == "autorun")
    assert autorun["status"] == "crashed"
    # advance past the max backoff -> it retries (self-healing preserved)
    ft.now += ps.BACKOFF_MAX_S + 1
    r = ps.reap()
    assert "autorun" in r["auto_restarted"]


def test_backoff_seconds_exponential_capped():
    # pure helper: 0 with no recent crashes; exponential; capped at MAX
    now = 1000.0
    assert ps._backoff_seconds([], now) == 0.0
    assert ps._backoff_seconds([now], now) == ps.BACKOFF_BASE_S
    assert ps._backoff_seconds([now - 1, now], now) == ps.BACKOFF_BASE_S * 2
    many = [now - i for i in range(20)]
    assert ps._backoff_seconds(many, now) == ps.BACKOFF_MAX_S


def test_unknown_loop():
    r = ps.start_loop("nope")
    assert r["ok"] is False
    assert "known" in r
