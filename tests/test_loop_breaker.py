"""Tests for mag/loop_breaker — crash-respawn LOOP vs genuine strain discrimination.

Hermetic: monkeypatches _enum() so no real processes are touched.
"""
from __future__ import annotations

from mag import loop_breaker as lb


def _proc(pid, sig, age, ppid=1, cmd=""):
    return {"pid": pid, "ppid": ppid, "cmd": cmd or ("python -c " + sig), "sig": sig, "age_s": age}


def test_no_procs_is_none(monkeypatch) -> None:
    monkeypatch.setattr(lb, "_enum", lambda: [])
    assert lb.detect()["verdict"] == "none"


def test_few_healthy_is_strain(monkeypatch) -> None:
    # 2 distinct cmdlines, old -> genuine work, never touched
    monkeypatch.setattr(lb, "_enum", lambda: [
        _proc(1, "autorun", 5000), _proc(2, "dashboard", 5000)])
    d = lb.detect()
    assert d["verdict"] in ("strain", "none")
    assert d["verdict"] != "crash_loop"


def test_respawn_storm_is_crash_loop(monkeypatch) -> None:
    # 6 processes with the SAME cmdline, most short-lived -> broken-process loop
    monkeypatch.setattr(lb, "_enum", lambda: [
        _proc(i, "main.py dashboard", 3) for i in range(6)])
    d = lb.detect()
    assert d["verdict"] == "crash_loop"
    assert d["loop"]["count"] >= lb.LOOP_CONCURRENCY


def test_duplicate_long_lived_autorun_is_crash_loop(monkeypatch) -> None:
    # The 2026-08-09 window-storm: 5 autorun_loop brains ALL LONG-LIVED (old, not short-lived)
    # running natively, each spawning sub-agents into desktop windows. A healthy single-brain
    # system has EXACTLY ONE autorun_loop, so ghost must break this even though none are young.
    sig = "from mag.governor_autorun import autorun_loop; autorun_loop(5.0)"
    monkeypatch.setattr(lb, "_enum", lambda: [
        _proc(i, sig, 9000, cmd="python -c " + sig) for i in range(5)])
    d = lb.detect()
    assert d["verdict"] == "crash_loop"
    assert d["loop"]["count"] >= lb.LOOP_CONCURRENCY


def test_duplicate_long_lived_ghost_cycle_is_crash_loop(monkeypatch) -> None:
    # Two+ ghost cycle loops (should be exactly one) must also be flagged.
    sig = "from mag.ghost import cycle"
    monkeypatch.setattr(lb, "_enum", lambda: [
        _proc(i, sig, 9000, cmd="python -c " + sig) for i in range(4)])
    assert lb.detect()["verdict"] == "crash_loop"


def test_runaway_spawner_cascade_is_crash_loop(monkeypatch) -> None:
    # 8 framework children under ONE parent = runaway-spawner cascade (the 2026-08-09
    # case: a respawner parent spawning duplicate daemons/loops). Ghost must break it,
    # and break_loop should target the PARENT tree.
    # Distinct cmdlines under ONE parent (the real cascade: ghost-daemon + cycle + autorun
    # all under a single respawner) — this is the by_ppid path, not the duplicate-cmdline path.
    monkeypatch.setattr(lb, "_enum", lambda: [
        _proc(i, f"mag.ghost --daemon child{i}", 5000, ppid=99) for i in range(8)])
    d = lb.detect()
    assert d["verdict"] == "crash_loop"
    assert d["loop"].get("kind") == "spawner_cascade"
    assert d["loop"].get("ppid") == 99


def test_break_loop_noop_when_none(monkeypatch) -> None:
    monkeypatch.setattr(lb, "_enum", lambda: [])
    r = lb.break_loop(dry=False)
    assert r["action"] == "none"
    assert r["ok"] is True


def test_break_loop_dry_does_not_kill(monkeypatch) -> None:
    monkeypatch.setattr(lb, "_enum", lambda: [
        _proc(i, "main.py dashboard", 3) for i in range(6)])
    r = lb.break_loop(dry=True)
    assert r["action"] == "break_loop"
    assert r["dry"] is True
    assert all(k.get("dry") for k in r["killed"])
