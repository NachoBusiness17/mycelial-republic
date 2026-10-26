"""Tests for the process supervisor (mag.process_supervisor)."""
import json
from pathlib import Path

import pytest

import mag.process_supervisor as ps


@pytest.fixture(autouse=True)
def _isolate_state(tmp_path, monkeypatch):
    """Point the supervisor at a temp state/log so tests don't touch real state.

    Also isolates the Docker-only marker (the real repo carries one) and the
    host-runtime override so policy-gate tests stay hermetic.
    """
    monkeypatch.setattr(ps, "STATE_PATH", tmp_path / "state.json")
    monkeypatch.setattr(ps, "LOG_PATH", tmp_path / "supervisor.jsonl")
    monkeypatch.setattr(ps, "DOCKER_ONLY_MARKER", tmp_path / "DOCKER_ONLY")
    monkeypatch.delenv("MAG_ALLOW_HOST_RUNTIME", raising=False)
    # These tests exercise THIS supervisor's own spawn/reap logic, which only runs
    # when it is the controller. mag_launch being live (normal fleet operation) used
    # to flip _container_mode() and silently turn these into no-op failures.
    monkeypatch.setattr(ps, "_container_mode", lambda: False)
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


def test_reap_policy_blocked_no_restart(_isolate_state, monkeypatch):
    # 2026-09-19 autopsy: the Docker-only drainer self-blocks on the host, and the
    # supervisor used to respawn it forever as a false crash-loop. With the marker
    # present, a dead drainer must become blocked_by_policy, never respawn.
    (_isolate_state / "DOCKER_ONLY").write_text("docker owns the drainer\n", encoding="utf-8")
    spawns = []
    monkeypatch.setattr(ps, "_spawn", lambda name: spawns.append(name) or {"pid": 1, "started_at": "t", "cmd": "x"})
    monkeypatch.setattr(ps, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(ps, "time", _FakeTime(1000.0))
    ps._save_state({"autorun": {
        "status": "crashed", "pid": 37172, "started_at_ts": 900.0,
        "crash_times": [999.0], "next_retry_at": 900.0, "cmd": "governor_autorun"}})
    for _ in range(5):
        ps.reap()
    assert spawns == []  # never respawned under the marker
    state = json.loads(ps.STATE_PATH.read_text(encoding="utf-8"))
    assert state["autorun"]["status"] == "blocked_by_policy"
    assert "next_retry_at" not in state["autorun"]
    st = ps.status()
    autorun = next(l for l in st["loops"] if l["name"] == "autorun")
    assert autorun["status"] == "blocked_by_policy"


def test_reap_policy_unblocks_when_marker_lifts(_isolate_state, monkeypatch):
    # The gate must lift: marker removed -> the drainer is restartable again.
    marker = _isolate_state / "DOCKER_ONLY"
    marker.write_text("x", encoding="utf-8")
    monkeypatch.setattr(ps, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(ps, "time", _FakeTime(1000.0))
    ps._save_state({"autorun": {
        "status": "blocked_by_policy", "pid": 37172, "started_at_ts": 900.0,
        "crash_times": [999.0], "cmd": "governor_autorun"}})
    ps.reap()
    state = json.loads(ps.STATE_PATH.read_text(encoding="utf-8"))
    assert state["autorun"]["status"] == "blocked_by_policy"  # still gated
    marker.unlink()
    monkeypatch.setattr(ps, "_spawn", lambda name: {"pid": 424242, "started_at": "t", "cmd": "x"})
    r = ps.reap()
    assert "autorun" in r["auto_restarted"]
    state = json.loads(ps.STATE_PATH.read_text(encoding="utf-8"))
    assert state["autorun"]["status"] == "running"


def test_policy_blocked_override_env(_isolate_state, monkeypatch):
    # MAG_ALLOW_HOST_RUNTIME=1 lifts the gate even with the marker present.
    (_isolate_state / "DOCKER_ONLY").write_text("x", encoding="utf-8")
    monkeypatch.setenv("MAG_ALLOW_HOST_RUNTIME", "1")
    assert ps._policy_blocked("autorun") is False
    monkeypatch.delenv("MAG_ALLOW_HOST_RUNTIME")
    assert ps._policy_blocked("autorun") is True
    assert ps._policy_blocked("ghost") is False  # gate is drainer-scoped


def test_policy_gate_matches_child_predicate(_isolate_state, monkeypatch):
    # B2-51 2026-09-26: the gate and the drainer child must evaluate the SAME
    # policy (mag.runtime_policy.host_runtime_blocked). The pre-2026-09-26
    # copies drifted: the children gated on os.name == "nt", the gate did not.
    import mag.runtime_policy as rp

    marker = _isolate_state / "DOCKER_ONLY"
    monkeypatch.setattr(rp, "DOCKER_ONLY_MARKER", marker)
    monkeypatch.setattr(ps, "DOCKER_ONLY_MARKER", marker)
    marker.write_text("x", encoding="utf-8")
    child = rp.host_runtime_blocked()
    assert ps._policy_blocked("autorun") == child  # one policy, two callers
    marker.unlink()
    assert ps._policy_blocked("autorun") is False
    assert ps._policy_blocked("autorun") == rp.host_runtime_blocked()
