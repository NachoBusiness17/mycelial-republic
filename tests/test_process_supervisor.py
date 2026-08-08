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
    r = ps.reap()
    assert "autorun" in r["crashed"]
    st = ps.status()
    autorun = next(l for l in st["loops"] if l["name"] == "autorun")
    assert autorun["status"] == "crashed"


def test_unknown_loop():
    r = ps.start_loop("nope")
    assert r["ok"] is False
    assert "known" in r
