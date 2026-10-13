"""Pin the B2-85 run_shell powershell resolution (tools/shell.py).

Disease (sig run_shell:e566037def80, 7,964 failure_kb rows since 2026-09-19):
the win32 branch executed subprocess.run(["powershell", ...]) directly, so in
launch contexts with a scrubbed PATH (headless daemons, spawned seats) the OS
raised FileNotFoundError("[Errno 2] No such file or directory: 'powershell'")
and the error string was returned, then logged, per call. The B2-85 root fix
(tools/shell.py, receipt watch/inbox/burn_wave_20260926/B2_85_powershell_fix_20260926.md)
resolves the executable before spawn: shutil.which("powershell"), then
shutil.which("powershell.exe"), then the System32 full-path fallback.

These pins make the bare-literal revert fail even on a host whose PATH
resolves powershell: the resolution path is simulated by patching
tools.shell.shutil.which to return None and emptying PATH for the spawn, the
exact launch-context condition the production failure class came from.

Falsifier contract (B2-353): revert tools/shell.py to the bare
["powershell"] literal and every behavioral pin here must fail (the source
pin fails too, naming the literal).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tools.shell as shell_mod

SYSTEM32_PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

win32_only = pytest.mark.skipif(
    sys.platform != "win32", reason="B2-85 disease is the win32 branch of run_shell"
)


def _spy_run(calls):
    real_run = shell_mod.subprocess.run

    def spy(argv, *a, **k):
        calls.append(list(argv))
        return real_run(argv, *a, **k)

    return spy


@win32_only
def test_run_shell_executes_allowlisted_command_when_which_returns_none(monkeypatch):
    """The scrubbed-PATH disease case: both which lookups miss, the System32
    fallback path is taken, and the allowlisted command still executes."""
    if not Path(SYSTEM32_PS).exists():
        pytest.skip("System32 WindowsPowerShell not present on this host")
    asked = []
    monkeypatch.setattr(
        shell_mod.shutil,
        "which",
        lambda name: asked.append(name) and None,
    )
    monkeypatch.setenv("PATH", "")
    calls: list = []
    monkeypatch.setattr(shell_mod.subprocess, "run", _spy_run(calls))

    r = shell_mod.run_shell("echo b2-353-pin-marker")

    # the command actually executed, no FileNotFoundError mentioning powershell
    assert r["ok"] is True, r
    assert r["exit_code"] == 0, r
    assert "b2-353-pin-marker" in r.get("output", ""), r
    assert "powershell" not in (r.get("error") or ""), r
    # resolution order pinned: which("powershell") then which("powershell.exe")
    assert asked == ["powershell", "powershell.exe"], asked
    # System32 fallback path taken: argv[0] is the full absolute powershell.exe
    assert calls, "subprocess.run was never called"
    assert calls[0][0].lower() == SYSTEM32_PS.lower(), calls[0]


@win32_only
def test_run_shell_uses_which_result_verbatim_when_lookup_hits(monkeypatch):
    """The normal-launch case: the first which hit feeds argv[0] unchanged."""
    if not Path(SYSTEM32_PS).exists():
        pytest.skip("System32 WindowsPowerShell not present on this host")
    asked = []
    monkeypatch.setattr(
        shell_mod.shutil,
        "which",
        lambda name: asked.append(name) or SYSTEM32_PS,
    )
    calls: list = []
    monkeypatch.setattr(shell_mod.subprocess, "run", _spy_run(calls))

    r = shell_mod.run_shell("echo b2-353-which-hit")

    assert r["ok"] is True, r
    assert r["exit_code"] == 0, r
    assert "b2-353-which-hit" in r.get("output", ""), r
    assert asked == ["powershell"], asked
    assert calls and calls[0][0] == SYSTEM32_PS, calls[0]


def test_no_bare_powershell_argv_literal_in_shell_source():
    """Source-level pin: the bare argv literal must not re-land anywhere in
    tools/shell.py, not even as powershell.exe (the B2-85 falsifier's exact
    revert shape is subprocess.run(["powershell", "-NoProfile", ...]))."""
    src = (ROOT / "tools" / "shell.py").read_text(encoding="utf-8")
    assert '["powershell' not in src, "bare powershell argv literal re-landed in tools/shell.py"
    assert "shutil.which" in src, "which-based resolution removed from tools/shell.py"
    assert "System32" in src, "System32 fallback removed from tools/shell.py"
