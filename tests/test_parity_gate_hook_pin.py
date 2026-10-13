"""D2 pin: the rule_parity pre-push block, from real hook bytes.

Sibling of the B2-451 pin (tests/test_scenarios_gate_hook_pin.py) for the
rule-parity gate block in githooks/pre-push (D2, 2026-09-30, spec
watch/inbox/last_mile_20260930/D2_PARITY_GATE.md). Laws pinned here:

  - TRIGGER LAW: the block fires when EITHER parity twin changes
    (mag/water_graph.py, roblox_to_godot/systems/water_graph.gd) and skips
    otherwise, decided by the real tools/prepush_paths_changed.py in a real
    temp git repo - not by re-implementing the decision;
  - FIRST-LINE CONTRACT: a green run opens "PARITY: ok" (lowercase ok, the
    B2-338 cry-wolf law), a divergent run "PARITY: FAIL"; the hook's case
    arm matches the ok prefix only, so both a FAIL and a traceback fall to
    the block arm (fail-closed);
  - ENFORCING: the block exits 1 on anything but the ok arm, and exits 1 on
    a cannot-verify trigger decision (prepush_paths_changed exit 2).

The brief's falsifier, pinned: point the trigger at only one twin (or swap
the ok token's case) and these tests go red.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "githooks" / "pre-push"
TOOL = ROOT / "tools" / "rule_parity.py"
HELPER = ROOT / "tools" / "prepush_paths_changed.py"
TWIN_PY = "mag/water_graph.py"
TWIN_GD = "roblox_to_godot/systems/water_graph.gd"
BLOCK_MARK = 'PUSH-GATE: rule_parity quick (conditional, enforcing)'

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def _hook_text() -> str:
    return HOOK.read_text(encoding="utf-8")


def _block_text() -> str:
    text = _hook_text()
    assert BLOCK_MARK in text, "rule_parity block missing from githooks/pre-push"
    return text.split(BLOCK_MARK)[1].split("# secret gate")[0]


def _ok_pattern(block: str) -> str:
    m = re.search(r'^\s*"?(PARITY: ok)"?\*\)', block, re.M)
    assert m, 'ok arm not found in the rule_parity block (expected "PARITY: ok"*))'
    return f'"{m.group(1)}"*'


def _replay(pattern: str, first_line: str) -> str:
    """Evaluate the hook's real case-arm pattern with real sh, as the hook does."""
    replay = 'case "$1" in ' + pattern + ') echo OK_ARM ;; *) echo BLOCK_ARM ;; esac'
    out = subprocess.run(["sh", "-c", replay, "sh", first_line],
                         capture_output=True, text=True, timeout=60,
                         creationflags=HEADLESS)
    return out.stdout.strip()


# ------------------------------------------------------ hook shape laws ----

def test_hook_block_names_both_twins_as_the_trigger():
    block = _block_text()
    assert f"PARITY_PY_TWIN={TWIN_PY}" in block, "py twin pathspec missing"
    assert f"PARITY_GD_TWIN={TWIN_GD}" in block, "gd twin pathspec missing"
    assert 'prepush_paths_changed.py' in block, "trigger must use the B2-272 helper"
    assert '-- "$PARITY_PY_TWIN" "$PARITY_GD_TWIN"' in block, \
        "helper call must pass exactly the two twins (the trigger law)"


def test_hook_block_is_enforcing_fail_closed():
    block = _block_text()
    assert block.count("exit 1") >= 2, \
        "the block must block on parity red AND on a cannot-verify trigger"
    assert '"PARITY: ok"*' in block, "lowercase-ok case arm missing"
    assert "PARITY: OK" not in block.replace("PARITY: ok", ""), \
        "an uppercase OK token crept into the block"
    assert "rule_parity skipped, twins unchanged" in _hook_text(), \
        "unchanged-arm skip line missing"


def test_hook_passes_quick_and_source_prepush():
    block = _block_text()
    assert "all --quick --source prepush" in block, \
        "the gate payload must be the quick profile tagged source=prepush"


# ------------------------------------------------- trigger decision law ----

@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_trigger_fires_on_either_twin_and_skips_otherwise(tmp_path: Path):
    """The real helper, in a real repo, with the hook's real twin pathspecs:
    dirty twin -> exit 1 (gate fires), untracked twin -> exit 1, clean or
    unrelated-only changes -> exit 0 (gate skips)."""
    def git(*a: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *a], cwd=tmp_path, capture_output=True,
                              text=True, timeout=60, creationflags=HEADLESS)

    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    py_twin = tmp_path / TWIN_PY
    py_twin.parent.mkdir(parents=True)
    py_twin.write_text("v1\n", encoding="utf-8")
    other = tmp_path / "README.md"
    other.write_text("r1\n", encoding="utf-8")
    git("add", TWIN_PY, "README.md")
    git("commit", "-q", "-m", "base")

    def changed() -> int:
        return subprocess.run(
            [sys.executable, str(HELPER), "--refs", "", "--", TWIN_PY, TWIN_GD],
            cwd=tmp_path, capture_output=True, text=True, timeout=60,
            creationflags=HEADLESS).returncode

    # gd twin present but UNCOMMITTED: the untracked arm must fire
    gd_twin = tmp_path / TWIN_GD
    gd_twin.parent.mkdir(parents=True)
    gd_twin.write_text("v1\n", encoding="utf-8")
    assert changed() == 1, "untracked gd twin must fire the gate"
    git("add", TWIN_GD)
    git("commit", "-q", "-m", "gd twin")
    assert changed() == 0, "clean tree must skip the gate"

    # unrelated change only: skip (the gate's scope is the twins ONLY)
    other.write_text("r2\n", encoding="utf-8")
    assert changed() == 0, "unrelated file changes must not fire the gate"

    # either twin dirty: fire
    gd_twin.write_text("v2\n", encoding="utf-8")
    assert changed() == 1, "dirty gd twin must fire the gate"
    git("checkout", "-q", "--", TWIN_GD)
    py_twin.write_text("v2\n", encoding="utf-8")
    assert changed() == 1, "dirty py twin must fire the gate"


# --------------------------------------------- first-line contract law ----

@pytest.mark.skipif(not (ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe").exists(),
                    reason="godot binary not present")
def test_gate_payload_first_line_and_latest_json(tmp_path: Path):
    """Run the gate's exact payload at throwaway out-dir. Pinned: the first
    stdout line carries the PARITY contract and agrees with the process exit
    code AND with latest.json (the honest-orbit law - the standing artifact
    can never disagree with the run that wrote it); the ok line matches the
    hook's real case pattern, a FAIL line falls to the block arm."""
    import json
    import time
    t0 = time.monotonic()
    proc = subprocess.run(
        [sys.executable, str(TOOL), "all", "--quick", "--source", "prepush",
         "--out-dir", str(tmp_path)],
        capture_output=True, text=True, timeout=300, creationflags=HEADLESS)
    wall = time.monotonic() - t0
    first = proc.stdout.splitlines()[0] if proc.stdout else ""

    assert first.startswith(("PARITY: ok", "PARITY: FAIL", "PARITY: ERROR")), first
    pattern = _ok_pattern(_block_text())
    if first.startswith("PARITY: ok"):
        assert proc.returncode == 0
        assert _replay(pattern, first) == "OK_ARM"
    else:
        assert proc.returncode in (1, 2), \
            "FAIL/ERROR first line with a zero exit code is a lying contract"
        assert _replay(pattern, first) == "BLOCK_ARM", \
            "red output must fall through the ok arm (the hook would exit 1)"

    latest = json.loads((tmp_path / "latest.json").read_text(encoding="utf-8"))
    assert latest["mode"] == "quick" and latest["source"] == "prepush"
    assert latest["exit_code"] == proc.returncode
    assert latest["parity"] is (proc.returncode == 0)
    assert set(latest["twins"]) == {"py", "gd"}
    assert latest["twins"]["py"]["path"] == TWIN_PY
    assert latest["twins"]["gd"]["path"] == TWIN_GD
    for t in latest["twins"].values():
        assert re.fullmatch(r"[0-9a-f]{12}", t["sha256_12"]), t

    # the quick budget law (mission contract: 20 sequences, <60s)
    assert wall < 60.0, f"quick payload took {wall:.1f}s (budget 60s)"


def test_case_flip_is_caught():
    """The B2-338 falsifier: an uppercased ok token in the hook must stop
    matching the real green first line, so this pin goes red with it."""
    block = _block_text()
    first = "PARITY: ok mode=quick rows_py=1220"
    assert _replay(_ok_pattern(block), first) == "OK_ARM"
    assert _replay('"PARITY: OK"*', first) == "BLOCK_ARM", \
        "a case-flipped pattern still matched; the pin can no longer catch the cry-wolf shape"
