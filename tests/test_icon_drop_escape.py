"""B2-413 (2026-09-26): pytest pins for the icon_drop escaping helpers.

Cause: the three helpers (_ps_quote, _cmd_echo_safe, _cmd_single_line) and
the drop_shortcut quote round-trip were probe-verified only
(watch/inbox/burn_wave_20260926/B2_377_unescape_probe.py), so a refactor back
to raw interpolation would re-open the silent-drop class with no gate. Pins
follow the B2-353 shell-pin pattern; the WScript.Shell round-trip pin runs a
real powershell only when one exists (CI-less hosts skip, never fail).
"""
from __future__ import annotations

import shutil
import sys

import pytest

import mag.icon_drop as icon_drop


# ---------------------------------------------------------------- helpers


def test_ps_quote_doubles_embedded_single_quotes():
    assert icon_drop._ps_quote("it's") == "'it''s'"
    assert icon_drop._ps_quote("a''b") == "'a''''b'"
    assert icon_drop._ps_quote("plain") == "'plain'"
    assert icon_drop._ps_quote("O'Brien's") == "'O''Brien''s'"


def test_cmd_echo_safe_escapes_metacharacters_and_percent():
    out = icon_drop._cmd_echo_safe("a & b | c < d > e ^ f")
    for ch in ("&", "|", "<", ">", "^"):
        assert f"^{ch}" in out
    assert icon_drop._cmd_echo_safe("100% done") == "100%% done"
    assert "^&" in icon_drop._cmd_echo_safe("&")


def test_cmd_echo_safe_collapses_crlf():
    for bad in ("one\r\ntwo", "one\ntwo", "one\rtwo"):
        out = icon_drop._cmd_echo_safe(bad)
        assert "\r" not in out and "\n" not in out  # no injected batch line
        assert "one" in out and "two" in out


def test_cmd_single_line_collapses_crlf_and_keeps_percent_live():
    out = icon_drop._cmd_single_line("notepad %USERPROFILE%\\.env\r\nsecond line")
    assert "\r" not in out and "\n" not in out  # single batch line, no injection
    assert "notepad %USERPROFILE%\\.env" in out and "second line" in out
    # % must stay live (batch expands at click time): no doubling here
    assert "%%" not in out


# ------------------------------------------------- drop_shortcut assembly


def test_drop_shortcut_quote_carrying_fields_round_trip(tmp_path, monkeypatch):
    """The B2-354 silent-drop class, pinned end to end.

    A target_path/args/desc full of single quotes must land status dropped
    with the .lnk on disk and fields read back equal through WScript.Shell.
    Runs a real powershell (skipped on hosts without one); the real Desktop
    and ledgers stay untouched via the same sandbox pattern as
    tests/test_icon_drop_fold.py.
    """
    ps_exe = shutil.which("powershell") or shutil.which("powershell.exe") or (
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        if sys.platform == "win32" else None
    )
    if not ps_exe:
        pytest.skip("no powershell on this host")
    weird_dir = tmp_path / "o'brien's dir"
    weird_dir.mkdir(parents=True)
    target = weird_dir / "tar'get.txt"
    target.write_text("x", encoding="utf-8")
    args_val = "-a 'quoted arg' -b"
    desc_val = "it's a 'test' desc"
    monkeypatch.setattr(icon_drop, "LEDGER", tmp_path / "icons" / "ledger.jsonl")
    desktop = tmp_path / "desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(icon_drop, "desktop_folder", lambda: desktop)
    import mag.skill_ledger as sl
    import mag.training_events as te
    monkeypatch.setattr(sl, "DECISIONS_PATH", tmp_path / "skill_decisions.jsonl")
    monkeypatch.setattr(te, "EVENTS_PATH", tmp_path / "training_events.jsonl")
    row = icon_drop.drop_shortcut("b2'413 pin", str(target), args_val, desc=desc_val)
    assert row["status"] == "dropped", row
    lnk = row["path"]
    ps = (
        "$s=(New-Object -ComObject WScript.Shell).CreateShortcut"
        f"({icon_drop._ps_quote(lnk)});"
        "$s.TargetPath + '|' + $s.Arguments + '|' + $s.Description"
    )
    import subprocess
    got = subprocess.run(
        [ps_exe, "-NoProfile", "-Command", ps],
        capture_output=True, text=True, timeout=60,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0,
    )
    assert got.returncode == 0, got.stderr
    t, a, d = got.stdout.strip().split("|", 2)
    assert t == str(target)
    assert a == args_val
    assert d == desc_val
