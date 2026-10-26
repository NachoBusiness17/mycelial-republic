"""refold_gate end-to-end run tests (Mickey17 W3, 2026-09-29).

The disease this pins: tools/refold_gate.py _run called itself recursively
(the name had been rebound away from subprocess.run), so the first spawn --
the B2-343 restore-guard audit -- died with RecursionError and the gate
fail-closed every run with a traceback instead of a REFOLD-GATE verdict.
The gate_canary refold_gate family proved it BLIND at HEAD on 2026-09-29.
Same bug class the secret-gate fix took (tools/secret_gate_scan.py _run,
2026-09-28 drift-patrol receipt); mirrored into refold_gate this date.

The regression shape is NOT a unit call into a helper -- it RUNS the gate
as a subprocess on a self-contained fixture tree (stub restore-guard, stub
queue-dupes census, stub fold host, one stub pin test), so the spawn path
that used to recurse is exercised for real and the exit contract is pinned:
0 + "REFOLD-GATE: ok" on the green fixture, 2 + "cannot verify" on a tree
missing its pins/host, and never a traceback in either.

Node guard: the gate exits 2 at its node check BEFORE its first spawn, so
without node on PATH the recursion path is never reached and a pass would
be vacuous -- the test skips instead (node is a test dependency per the
refold_gate brief; its absence must be named, never silently green).

Receipt: watch/inbox/mates_leave_protocol/W3B_REFOLD_FIX.md.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / "tools" / "refold_gate.py"

# HEADLESS law (spawn_sites_no_window, ratcheted by tests/test_headless_law.py):
# every subprocess spawn carries CREATE_NO_WINDOW on win32 so no console window
# pops on the operator's desktop. 0 on platforms without the flag.
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

RESTORE_GUARD_STUB = '''#!/usr/bin/env python3
# fixture stub: the refold gate's B2-343 arm must exit 0 and leave one line
# (the gate reads the last stdout line as its guard_ok token).
import sys
print("RESTORE-GUARD: ok (fixture stub, 0 records)")
sys.exit(0)
'''

QUEUE_DUPES_STUB = '''#!/usr/bin/env python3
# fixture stub: the gate's B2-486 arm must exit 0 and speak the ok prefix.
import sys
print("QUEUE-DUPES: ok (fixture stub, 0 rows)")
sys.exit(0)
'''

PIN_STUB = '''def test_fixture_pin_passes():
    assert True
'''


def _build_fixture(root: Path) -> Path:
    """Self-contained tree the gate can run against: its own copy of the
    gate under test, stub arms, stub host, one stub pin."""
    (root / "tools").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "tests").mkdir()
    shutil.copyfile(GATE, root / "tools" / "refold_gate.py")
    (root / "tools" / "restore_guard.py").write_text(RESTORE_GUARD_STUB,
                                                     encoding="utf-8")
    (root / "tools" / "queue_dupes_check.py").write_text(QUEUE_DUPES_STUB,
                                                         encoding="utf-8")
    (root / "scripts" / "index_fold_host.mjs").write_text(
        "// fixture stub host (not executed: the stub pins never spawn node)\n",
        encoding="utf-8")
    (root / "tests" / "test_index_fold_host.py").write_text(PIN_STUB,
                                                            encoding="utf-8")
    return root


def _run_gate(root: Path, timeout: int = 240) -> tuple[int, str]:
    p = subprocess.run(
        [sys.executable, str(root / "tools" / "refold_gate.py"),
         "--root", str(root)],
        capture_output=True, text=True, errors="replace", timeout=timeout,
        creationflags=HEADLESS,
    )
    return p.returncode, (p.stdout or "") + (p.stderr or "")


@pytest.mark.skipif(shutil.which("node") is None,
                    reason="refold gate exits 2 at its node check before the "
                           "first spawn, so without node the recursion path "
                           "is never reached and a pass would be vacuous")
def test_gate_runs_green_on_fixture_tree(tmp_path):
    root = _build_fixture(tmp_path / "fixroot")
    rc, out = _run_gate(root)
    # No recursion: the pre-fix tree died here with RecursionError and a
    # traceback instead of a verdict.
    assert "RecursionError" not in out
    assert "Traceback (most recent call last)" not in out
    # Exit contract: green fixture -> 0 with the ok verdict, the stub pin
    # count, and both stub arms' tokens in the tail.
    assert rc == 0, out
    assert "REFOLD-GATE: ok" in out
    assert "1 passed" in out
    assert "RESTORE-GUARD: ok" in out
    assert "QUEUE-DUPES: ok" in out


def test_gate_missing_pins_is_cannot_verify(tmp_path):
    # Empty tree (no tests/test_index_fold_host.py, no
    # scripts/index_fold_host.mjs): exit 2 "cannot verify", never a
    # traceback. Reaches the verdict before node is even consulted.
    root = tmp_path / "emptyroot"
    root.mkdir()
    (root / "tools").mkdir()
    shutil.copyfile(GATE, root / "tools" / "refold_gate.py")
    rc, out = _run_gate(root)
    assert rc == 2, out
    assert "cannot verify" in out
    assert "Traceback (most recent call last)" not in out
