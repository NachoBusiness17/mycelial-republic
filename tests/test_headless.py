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
