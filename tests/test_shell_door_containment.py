"""Shell door containment tests (port-order lane P4, 2026-10-07).

The exploit class is the estate's own measured one: the 2026-10-07 steal round
(watch/inbox/frontier_olm_2026-10-07/steal/shell_escape_probe_runner.py) fired
run_python with a snippet using only open() and a literal absolute path; the old
door (five-pattern substring ban + tempdir cwd) returned ok=True, exit 0 and the
marker landed OUTSIDE the tempdir (banked marker: shell_escape_probe.txt, 98
bytes: "marker: shell door wrote outside its tempdir cwd with full user
privileges, 2026-10-07 steal round"). Every test here is the standing falsifier:
the shell must FAIL to write outside its declared root, loud (exit nonzero +
violation row), and a clean in-sandbox run must keep passing.
"""
from __future__ import annotations

import pathlib
import sys
import tempfile

import pytest

from config import ROOT
from tools.code_execution import (
    _RUN_ROOT_NAME,
    _VIOLATION_LOG,
    banned_pattern_lint,
    run_python,
    static_path_gate,
)

pytestmark = pytest.mark.skipif(sys.platform != "win32",
                                reason="win32 job-object shell door")


def _run_root() -> pathlib.Path:
    return pathlib.Path(tempfile.gettempdir()) / _RUN_ROOT_NAME


def _gate_root() -> str:
    return str(_run_root())


def _newest_canary_snippet() -> str:
    # Computed path (no literal absolute): exactly the class the L1 static gate
    # cannot see and the L4 canary + audit walk exist for.
    return (
        "import tempfile, pathlib\n"
        f'root = pathlib.Path(tempfile.gettempdir()) / "{_RUN_ROOT_NAME}"\n'
        'c = max(root.glob("*.canary"), key=lambda p: p.stat().st_mtime)\n'
        'c.write_bytes(b"tampered")\n'
    )


def test_original_exploit_marker_fails_loud():
    """The steal round's exact attack shape, retargeted inside the repo: a
    literal absolute marker path OUTSIDE the run root must be refused pre-exec,
    exit 125, with a violation row, and the marker must never land."""
    marker = ROOT / "watch" / "inbox" / "port_wave_20261007" / "p4_probe_should_never_land.txt"
    code = (
        f"p = r'{marker.as_posix()}'\n"
        "open(p, 'w').write('marker: shell door wrote outside its tempdir cwd "
        "with full user privileges, 2026-10-07 steal round')\n"
        "print('wrote bytes:', len(open(p).read()))\n"
    )
    # Old-code reproduction, conceptually banked: the snippet contains none of
    # the old door's five banned substrings, so its ONLY gate (the substring
    # ban) was structurally blind to it; the steal measured ok=True, exit 0 and
    # the marker on disk (shell_escape_probe_runner.py evidence).
    for banned in banned_pattern_lint(code):
        raise AssertionError(f"exploit fixture tripped the old lint ({banned}); fixture is wrong")
    if marker.exists():
        marker.unlink()

    result = run_python(code, timeout=30)

    assert result["ok"] is False
    assert result["exit_code"] == 125
    assert result["violation"]["kind"] == "static_path_gate"
    assert "containment violation" in result["error"]
    assert not marker.exists(), "the exploit marker landed; containment failed"


def test_canary_detects_sibling_tamper():
    """A computed-path write to the canary beside the run (sibling of the
    tempdir) is invisible to the static gate and caught by the post-exec
    canary hash check: loud 125, canary_tamper."""
    result = run_python(_newest_canary_snippet(), timeout=30)
    assert result["ok"] is False
    assert result["exit_code"] == 125
    assert result["violation"]["kind"] == "canary_tamper"


def test_audit_flags_sibling_pollution():
    """The gate instruction's standing form: write a marker to a SIBLING of the
    tempdir. Computed path, lands in the owned run root top level, flagged by
    the audit walk: loud 125, run_root_pollution, and the sweep removes it."""
    marker_name = "escape_marker_p4.txt"
    code = (
        "import tempfile, pathlib\n"
        f'root = pathlib.Path(tempfile.gettempdir()) / "{_RUN_ROOT_NAME}"\n'
        f'(root / "{marker_name}").write_text("escaped")\n'
    )
    result = run_python(code, timeout=30)
    assert result["ok"] is False
    assert result["exit_code"] == 125
    assert result["violation"]["kind"] == "run_root_pollution"
    assert marker_name in result["violation"]["detail"]
    assert not (_run_root() / marker_name).exists(), "sweep left the escape marker"


def test_clean_in_sandbox_run_passes():
    """No containment regression: reads via the preamble ROOT helper, writes
    and reads inside the run dir, prints output; all clean."""
    code = (
        "open('out.txt', 'w').write('hi from inside')\n"
        "print(open('out.txt').read())\n"
        "print(P('no_such_file'))\n"
    )
    result = run_python(code, timeout=30)
    assert result["ok"] is True, result
    assert result["exit_code"] == 0
    assert "hi from inside" in result["output"]
    assert "violation" not in result


def test_relative_literal_write_not_flagged():
    """A relative literal write path resolves against the child's cwd (the run
    dir) at runtime: the static gate must not false-positive on it."""
    assert static_path_gate("open('relative.txt', 'w').write('x')", _gate_root()) == []
    result = run_python("from pathlib import Path\n"
                        "Path('rel.txt').write_text('x')\n"
                        "print(Path('rel.txt').read_text())", timeout=30)
    assert result["ok"] is True, result


def test_static_gate_normalizes_literal_paths():
    """Unit layer: join folds, expandvars and read-only opens are classified."""
    flagged = "import os\np = os.path.join(r'C:/_p4_unit', 'bad.txt')\nopen(p, 'w')"
    assert len(static_path_gate(flagged, _gate_root())) == 1
    assert static_path_gate("open(r'C:/Windows/win.ini')", _gate_root()) == []  # read-only default
    assert static_path_gate("open('relative.txt', 'w')", _gate_root()) == []
    assert len(static_path_gate(
        "from pathlib import Path\nPath(r'C:/elsewhere/x.txt').write_text('y')",
        _gate_root())) == 1


def test_temp_prefix_but_outside_run_root_trips():
    """The declared writable root is the owned run root, not the whole OS temp
    prefix: a marker dropped as a sibling OF the run root is still an escape
    (this is the exact live attack run at the gate, 2026-10-08)."""
    marker = pathlib.Path(tempfile.gettempdir()) / "p4_gate_attack_marker.txt"
    if marker.exists():
        marker.unlink()
    code = (
        f"p = r'{marker.as_posix()}'\n"
        "open(p, 'w').write('marker beside the run root')\n"
    )
    result = run_python(code, timeout=30)
    assert result["ok"] is False
    assert result["exit_code"] == 125
    assert result["violation"]["kind"] == "static_path_gate"
    assert not marker.exists()


def test_job_memory_cap_kills_allocation():
    """Job Object layer: the child's process memory cap turns a fat allocation
    into a MemoryError (loud child failure, no escape, no violation row: the
    cap did its job)."""
    monkey = pytest.MonkeyPatch()
    monkey.setenv("MAG_EXEC_MEM_CAP_MB", "96")
    try:
        result = run_python("b = bytearray(512 * 1024 * 1024)\nprint(len(b))",
                            timeout=60)
    finally:
        monkey.undo()
    assert result["ok"] is False
    assert result["exit_code"] != 0
    assert "MemoryError" in result.get("output", "")
    assert "violation" not in result


def test_timeout_still_returns_124():
    """Historical contract: timeout is 124, and the job terminate path does not
    hang the door."""
    result = run_python("import time\ntime.sleep(60)", timeout=2)
    assert result["ok"] is False
    assert result["exit_code"] == 124


def test_banned_patterns_are_secondary_lint():
    """The old five-pattern ban is demoted to a cheap lint layer (exit 126) and
    says so; containment no longer rides on it."""
    code = "import subprocess\nsubprocess.run(['cmd'])\n"
    assert banned_pattern_lint(code) == ["subprocess"]
    result = run_python(code, timeout=30)
    assert result["ok"] is False
    assert result["exit_code"] == 126
    assert "secondary lint" in result["error"]


def test_ctypes_job_fallback_end_to_end(monkeypatch):
    """Without pywin32 the ctypes job factory must carry the whole loop: clean
    run passes with the fallback factory in place."""
    monkeypatch.setitem(sys.modules, "win32job", None)  # forces ImportError -> ctypes
    result = run_python("print('ctypes job path')", timeout=30)
    assert result["ok"] is True, result
    assert "ctypes job path" in result["output"]


def test_violation_rows_banked_to_ledger():
    """Loud means banked: every containment hit appends a row to the violation
    log, so a patrol can read the door's refusals."""
    _ = run_python(_newest_canary_snippet(), timeout=30)
    assert _VIOLATION_LOG.exists()
    rows = [line for line in _VIOLATION_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows, "violation log empty after a triggered containment hit"
    assert '"kind": "canary_tamper"' in rows[-1]
