"""cockpit tests -- the next-action ladder and the glance contract.

The cockpit's worth is that it never guesses: a red signal must map to the one
command that unsticks it, and a clean estate must say "clear" rather than invent
work. These tests pin that ladder plus the TTL cache that keeps a glance <1s.
"""
from __future__ import annotations

import json
from pathlib import Path

import tools.cockpit as cp


def _s(name, status, detail="", **extra):
    return {"name": name, "status": status, "detail": detail, **extra}


def _base():
    return {n: _s(n, "ok", "fine") for n in
            ("git", "sweeper", "chain", "fossil", "percolator",
             "falsifier", "smoke", "tasks")}


def test_clean_estate_says_clear():
    nxt = cp.next_action(_base())
    assert nxt["id"] == "clear"


def test_stale_lock_wins_over_everything():
    sig = _base()
    sig["git"] = _s("git", "red", "index.lock 14m old with no commit for 40m")
    sig["falsifier"] = _s("falsifier", "red", "1 FAIL")
    assert cp.next_action(sig)["id"] == "clear-stale-lock"


def test_dirty_stall_maps_to_unstick_sweeper():
    sig = _base()
    sig["git"] = _s("git", "red", "3051 files uncommitted, no commit for 45m (sweeper stalled)")
    assert cp.next_action(sig)["id"] == "unstick-sweeper"


def test_falsified_invariant_ranks_above_smoke():
    sig = _base()
    sig["falsifier"] = _s("falsifier", "red", "1 FAIL")
    sig["smoke"] = _s("smoke", "red", "FAIL")
    assert cp.next_action(sig)["id"] == "falsified-invariant"


def test_i5_is_a_named_wave_not_a_red():
    sig = _base()
    sig["percolator"] = _s("percolator", "warn", "5/6 gates; failing I5",
                           failed=["I5"], stats={"explore_live": 10, "explore_rows": 20})
    assert cp.next_action(sig)["id"] == "i5-leaf-gate"


def test_live_backlog_without_i5_failure_points_at_consumer():
    sig = _base()
    sig["percolator"] = _s("percolator", "ok", "6/6",
                           failed=[], stats={"explore_live": 1517, "explore_rows": 3478})
    assert cp.next_action(sig)["id"] == "explore-consumer"


def test_html_embeds_the_state():
    html = cp.render_html({"ts": "t", "status": "ok",
                           "next": {"id": "clear", "why": "none", "do": "nothing"},
                           "signals": {"git": _s("git", "ok", "0 dirty")}})
    assert "0 dirty" in html and "clear" in html and "__DATA__" not in html


def test_cache_serves_second_call_without_rerunning(tmp_path, monkeypatch):
    monkeypatch.setattr(cp, "CACHE", tmp_path / "cache.json")
    monkeypatch.setattr(cp, "_REFRESH", False)
    calls = {"n": 0}

    def slow():
        calls["n"] += 1
        return _s("slow", "ok", f"call {calls['n']}")

    first = cp.cached("slow", slow)
    second = cp.cached("slow", slow)
    assert calls["n"] == 1
    assert first["measured_ago_s"] == 0 and second["measured_ago_s"] >= 0
    monkeypatch.setattr(cp, "_REFRESH", True)
    cp.cached("slow", slow)
    assert calls["n"] == 2
