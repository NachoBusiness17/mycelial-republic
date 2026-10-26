"""Tests for mag/headless — the canonical single-interpreter spawner LAW.

LAW (2026-08-10): the canonical interpreter MUST bypass the venv shim
(`.venv/Scripts/python.exe` re-execs into the base interpreter as a CHILD, doubling
every spawn and causing the host reap/seat-exit=-1 mismatch). It must resolve to the
REAL interpreter (pyvenv.cfg 'home') with PYTHONPATH to the venv site-packages.
"""
from __future__ import annotations

from pathlib import Path

from mag import headless as h


def test_canonical_python_bypasses_venv_shim() -> None:
    # The canonical PYTHON must NOT be the venv shim (that's the doubling root).
    p = Path(h.PYTHON)
    assert p.name in ("python.exe", "pythonw.exe")
    assert r"\Scripts\python" not in str(p), f"PYTHON must bypass the venv shim: {h.PYTHON}"


def test_spawn_env_has_pythonpath_to_venv_sitepackages() -> None:
    env = h._spawn_env()
    pp = env.get("PYTHONPATH", "")
    assert pp, "PYTHONPATH must be set so the real interpreter resolves mag/deps"
    assert ".venv" in pp and "site-packages" in pp


def test_resolved_real_interpreter_runs() -> None:
    import subprocess
    r = subprocess.run(
        [h.PYTHON, "-c", "import sys, mag, config; from fastapi import FastAPI; print('OK')"],
        capture_output=True, text=True, timeout=90,
        env=h._spawn_env(),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) if __import__("os").name == "nt" else 0,
    )
    assert r.returncode == 0, r.stderr[-400:]
    assert "OK" in r.stdout


def test_popen_wrapper_is_class_and_installer_safe_under_pytest() -> None:
    """REGRESSION (wave5 suite-burn, 2026-09-29): the conftest/headless collision.

    tests/conftest.py used to replace subprocess.Popen with a plain FUNCTION
    wrapper; mag/headless.py:24 then captured that function as _REAL_Popen at
    first import under pytest, and install_no_window_defaults' `class
    _Popen(_REAL_Popen)` (mag/headless.py:72) raised
    "TypeError: function() argument 'code' must be code, not str" for every
    runtime caller. f-15 + s2-19 full-suite runs 2026-09-28: casualties
    tests/test_swarm_quota_gate.py x2 (via mag/swarm_worker.py:380/:553) and
    tests/test_write_strip.py x1 (via main.py:39). Conftest now delegates to
    the canonical installer. Two invariants keep this collision class dead:

    1. the ambient subprocess.Popen under pytest is a CLASS, because
       mag.headless (here) and asyncio's windows plumbing both subclass it;
    2. install_no_window_defaults() is safe to call at runtime under pytest -
       the entry points do exactly that (mag/swarm_worker.py:380/:553,
       main.py:39) and must never crash because some wrapper captured earlier
       is not subclassable.
    """
    import asyncio
    import subprocess

    assert isinstance(subprocess.Popen, type), (
        "subprocess.Popen must be a class under pytest, not a function wrapper: "
        "subclassing it (mag/headless.py:72, asyncio windows plumbing) raises "
        f"TypeError on a function; got {subprocess.Popen!r}")

    # the exact crash shape that killed the 2026-09-28 suite runs, proven dead:
    class _Probe(subprocess.Popen):  # must not raise
        pass

    # and the runtime installer entry point stays safe (idempotent under pytest)
    h.install_no_window_defaults()
    assert getattr(subprocess, "_mag_nowin", False) is True, (
        "install_no_window_defaults must hold the installed marker under pytest")
    # the 2026-08-11 ghost-daemon crash shape: importing asyncio's subprocess
    # plumbing under the installed wrapper must stay clean
    import asyncio.subprocess  # noqa: F401
