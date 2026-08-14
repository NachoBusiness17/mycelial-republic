"""Tests for mag/source_trace — ghost 'sense runaway python TO SOURCE'.

Hermetic: monkeypatches _enum() so no real processes are touched.
"""
from __future__ import annotations

from mag import source_trace as st


def _proc(pid, ppid, cmd):
    return {"pid": pid, "ppid": ppid, "name": "python.exe", "cmd": cmd, "env": {}}


def test_no_procs_is_clean(monkeypatch) -> None:
    monkeypatch.setattr(st, "_enum", lambda: [])
    assert st.sense()["verdict"] == "clean"


def test_healthy_stack_is_clean(monkeypatch) -> None:
    # one of each singleton slot -> clean
    monkeypatch.setattr(st, "_enum", lambda: [
        _proc(1, 0, "mag_launch.py"),
        _proc(2, 1, "main.py lab --no-dashboard"),
        _proc(3, 1, "synthesis_agent.py"),
        _proc(4, 1, "-m mag.ghost --daemon --port 9000"),
    ])
    d = st.sense()
    assert d["verdict"] == "clean"


def test_duplicate_singleton_is_runaway_with_source(monkeypatch) -> None:
    # 2 lab slots under the same mag_launch root -> runaway, traced to source
    monkeypatch.setattr(st, "_enum", lambda: [
        _proc(100, 0, "mag_launch.py"),          # root
        _proc(101, 100, "main.py lab --no-dashboard"),   # uv child
        _proc(102, 100, "main.py lab --no-dashboard"),   # duplicate lab
    ])
    d = st.sense()
    assert d["verdict"] == "runaway"
    dup = d["duplicates"][0]
    assert dup["slot"] == "lab"
    assert dup["count"] == 2
    assert dup["source"]["root_pid"] == 100
    assert "mag_launch" in dup["source"]["root_cmd"]


def test_trace_source_walks_to_root(monkeypatch) -> None:
    procs = [
        _proc(1, 0, "boot_mag.cmd"),
        _proc(2, 1, "main.py power start --browser"),
        _proc(3, 2, "mag_launch.py"),
        _proc(4, 3, "-m mag.ghost --daemon --port 9000"),
        _proc(5, 4, "from mag.governor_autorun import autorun_loop; autorun_loop(5.0)"),
    ]
    chain = st.trace_source(5, procs)
    assert chain[-1]["pid"] == 1
    assert chain[0]["slot"] == "drainer"
    assert any(c["boot"] for c in chain)


def test_break_source_dry_does_not_kill() -> None:
    r = st.break_source(123, dry=True)
    assert r["dry"] is True
    assert r["action"] == "break_source"


def test_dedupe_uv_pairs_collapses_shim_child() -> None:
    # one logical lab process = venv shim + its uv-cpython child (same cmd tail)
    procs = [
        _proc(1, 0, "mag_launch.py"),
        _proc(2, 1, "C:\\...\\.venv\\Scripts\\python.exe main.py lab --no-dashboard"),
        _proc(3, 2, "C:\\...\\AppData\\Roaming\\uv\\python\\python.exe main.py lab --no-dashboard"),
    ]
    dedup = st.dedupe_uv_pairs(procs)
    pids = {p["pid"] for p in dedup}
    assert pids == {1, 2}  # uv child (3) dropped; shim (2) kept

def test_dedupe_survives_quote_mismatch() -> None:
    # REGRESSION (2026-08-10): shim cmd is UNQUOTED, uv child QUOTED. Invariant must
    # strip quotes/collapse whitespace or the pair is never collapsed and every healthy
    # slot reads as a 2x duplicate.
    procs = [
        _proc(1, 0, "mag_launch.py"),
        _proc(2, 1, "C:\\\\...\\\\.venv\\\\Scripts\\\\python.exe -m backend.server --host 127.0.0.1"),
        _proc(3, 2, '"C:\\\\...\\\\AppData\\\\Roaming\\\\uv\\\\python\\\\python.exe" -m backend.server --host 127.0.0.1'),
    ]
    dedup = st.dedupe_uv_pairs(procs)
    pids = {p["pid"] for p in dedup}
    assert pids == {1, 2}  # quoted uv child (3) still collapsed


def test_multi_boot_counts_supervisors_not_per_proc_roots(monkeypatch) -> None:
    # one healthy stack: all slots under ONE mag_launch, each with a uv twin.
    # Must be clean (multi_boot False) even though each shim's parent is a boot shell.
    procs = [_proc(1, 0, "mag_launch.py")]
    slots = [
        "main.py lab --no-dashboard",
        "synthesis_agent.py",
        "-m mag.ghost --daemon --port 9000",
        "main.py dashboard --host 127.0.0.1",
    ]
    for i, cmd in enumerate(slots):
        shim = 100 + i * 2
        procs.append(_proc(shim, 1, "C:\\\\...\\\\.venv\\\\Scripts\\\\python.exe " + cmd))
        procs.append(_proc(shim + 1, shim, "C:\\\\...\\\\AppData\\\\Roaming\\\\uv\\\\python\\\\python.exe " + cmd))
    monkeypatch.setattr(st, "_enum", lambda: procs)
    d = st.sense()
    assert d["verdict"] == "clean"
    assert d["multi_boot"] is False

def test_healthy_stack_with_uv_pairs_is_clean(monkeypatch) -> None:
    # one of each singleton slot, each with its venv/uv pair, ALL under ONE shared
    # boot root (mag_launch) -> clean, not runaway/multi_boot
    procs = [_proc(1, 0, "mag_launch.py")]  # single shared root
    slots = [
        "main.py lab --no-dashboard",
        "synthesis_agent.py",
        "-m mag.ghost --daemon --port 9000",
        "main.py dashboard --host 127.0.0.1",
    ]
    for i, cmd in enumerate(slots):
        shim = 100 + i * 2
        procs.append(_proc(shim, 1, "C:\\...\\.venv\\Scripts\\python.exe " + cmd))
        procs.append(_proc(shim + 1, shim, "C:\\...\\AppData\\Roaming\\uv\\python\\python.exe " + cmd))
    monkeypatch.setattr(st, "_enum", lambda: procs)
    d = st.sense()
    assert d["verdict"] == "clean"
