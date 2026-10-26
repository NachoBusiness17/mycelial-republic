"""B2-382 pins: the B2-85 mag-side powershell resolutions in the enumeration
branches stay resolved (never a bare "powershell" literal again).

Disease (sig run_shell:e566037def80, 7,964 failure_kb rows): scrubbed-PATH
launch contexts raised FileNotFoundError on subprocess ["powershell"]. The
B2-85 fix resolves shutil.which("powershell") -> which("powershell.exe") ->
the System32 full path before spawn, in every module that enumerates
processes: mag/legacy_audit.py _enum_procs, mag/platform_kill.py
_enum_host_pids, mag/loop_breaker.py _enum (flow-probe-verified by
B2_85_flow_probe, but until these pins NO pytest failed on a revert).

Pattern per the B2-353 shell pin: shutil.which monkeypatched to None so the
System32 arm is the only one that can answer, spawn argv spied and canned so
the run is deterministic, and the parse asserted clean (zero error rows).

Falsifier contract: revert any of the three branches to the bare
["powershell"] literal and its pin fails on argv[0] not being the absolute
System32 path; the clean-path pin fails if the psutil branch starts spawning.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SYSTEM32_PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

win32_only = pytest.mark.skipif(
    sys.platform != "win32", reason="B2-85 disease is the win32 spawn branch"
)

CANNED_PS_OUTPUT = json.dumps([
    {"ProcessId": 4242, "ParentProcessId": 100, "Name": "python.exe",
     "CommandLine": "python -m mag.orchestrator"},
])


def _force_psutil_importerror(monkeypatch):
    # a None entry in sys.modules makes `import psutil` raise ImportError,
    # which is exactly the branch these modules' PowerShell fallback serves
    monkeypatch.setitem(sys.modules, "psutil", None)


def _spy_ps_run(monkeypatch, mod, calls, stdout=CANNED_PS_OUTPUT):
    """Replace subprocess.run with a spy that records argv and returns a
    canned CompletedProcess-shaped object (no real spawn: deterministic).
    The modules import subprocess LOCALLY inside the fallback branch, so the
    patch must land on the shared stdlib module (monkeypatch restores it)."""
    del mod  # the local import rebinds from sys.modules; patch globally

    def fake_run(argv, *a, **k):
        calls.append(list(argv))
        return type("R", (), {"returncode": 0, "stdout": stdout, "stderr": ""})()

    monkeypatch.setattr("subprocess.run", fake_run)


@win32_only
def test_legacy_audit_enum_procs_takes_system32_arm(monkeypatch):
    import mag.legacy_audit as mod

    _force_psutil_importerror(monkeypatch)
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
    calls: list = []
    _spy_ps_run(monkeypatch, mod, calls)

    out = mod._enum_procs()

    assert len(calls) == 1, "expected exactly one PowerShell spawn"
    assert calls[0][0] == SYSTEM32_PS, "argv[0] must be the absolute System32 path"
    assert "-NoProfile" in calls[0]
    assert out and out[0]["pid"] == 4242, "canned row parsed (zero error rows)"
    assert all("error" not in r for r in out)


@win32_only
def test_platform_kill_enum_host_pids_takes_system32_arm(monkeypatch):
    import mag.platform_kill as mod

    _force_psutil_importerror(monkeypatch)
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
    calls: list = []
    _spy_ps_run(monkeypatch, mod, calls,
                stdout=json.dumps([{"ProcessId": 4242, "Name": "python.exe",
                                    "CommandLine": "python main.py orchestrator drain"}]))

    out = mod._enum_host_pids()

    assert len(calls) == 1
    assert calls[0][0] == SYSTEM32_PS
    assert out and out[0]["pid"] == 4242


@win32_only
def test_loop_breaker_enum_takes_system32_arm(monkeypatch):
    import mag.loop_breaker as mod

    _force_psutil_importerror(monkeypatch)
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
    calls: list = []
    _spy_ps_run(monkeypatch, mod, calls,
                stdout=json.dumps([{"ProcessId": 4242,
                                    "CommandLine": "python main.py orchestrator drain"}]))

    out = mod._enum()

    assert len(calls) == 1
    assert calls[0][0] == SYSTEM32_PS
    assert out and out[0]["pid"] == 4242


def test_legacy_audit_clean_path_never_spawns(monkeypatch):
    """Clean-path pin (one site, per the brief): with psutil importable, the
    enumerator reads processes directly and must not spawn PowerShell."""
    import mag.legacy_audit as mod

    calls: list = []
    _spy_ps_run(monkeypatch, mod, calls)

    out = mod._enum_procs()

    assert calls == [], "clean (psutil) path must not spawn any subprocess"
    assert isinstance(out, list)
