"""B2-451 pin: the workflow_gate_scenarios pre-push block, from real hook bytes.

Sibling of the B2-338 census pin (tests/test_census_drift_patrol.py) for the
B2-164 scenario-suite gate block in githooks/pre-push. The block's first-line
contract: a green run_scenarios prints a per-card "SCENARIOS ok ..." row first
so the hook's case arm matches the lowercase-ok prefix; red runs open with
"SCENARIOS FAIL"; errors (including the no-cards guard) with "SCENARIOS
ERROR"; the case arm exits 1 on anything else; the unchanged arm skips.

The brief's falsifier, pinned as a test: change "SCENARIOS ok" to
"SCENARIOS OK" in the hook block and zero tests go red. test_case_flip_is_caught
reads the pattern from the real hook bytes, flips the case, and requires the
green first line to STOP matching - so a case regression in the hook lands
loudly here.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "githooks" / "pre-push"
TOOL = ROOT / "tools" / "workflow_gate.py"
CARDS = ROOT / "configs" / "workflow_gate_scenarios"
OK_LINE_RE = re.compile(r'^(\s*)("(?:SCENARIOS ok)"\*)\)\s*$', re.M)

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def _hook_text() -> str:
    return HOOK.read_text(encoding="utf-8")


def _ok_pattern() -> str:
    """The ok-arm pattern, read from the real hook bytes (the B2-338 pattern)."""
    m = OK_LINE_RE.search(_hook_text())
    assert m, 'scenarios ok arm not found in githooks/pre-push bytes (expected a line like "SCENARIOS ok"*))'
    return m.group(2)


def _run_scenarios(card_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "check", "--scenarios", str(card_dir)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120,
        creationflags=HEADLESS,
    )


def _replay(pattern: str, first_line: str) -> str:
    """Evaluate the hook's real case-arm pattern with real sh, as the hook does."""
    replay = 'case "$1" in ' + pattern + ') echo OK_ARM ;; *) echo BLOCK_ARM ;; esac'
    out = subprocess.run(["sh", "-c", replay, "sh", first_line],
                         capture_output=True, text=True, timeout=60,
                         creationflags=HEADLESS)
    return out.stdout.strip()


def test_hook_block_shape_from_real_bytes():
    text = _hook_text()
    assert '"SCENARIOS ok"*' in text, "lowercase-ok case arm missing from the hook"
    assert "SCENARIOS ok" in text and "SCENARIOS OK" not in text.replace("SCENARIOS ok", ""), \
        "an uppercase OK token crept into the block"
    # enforcing arm: red output falls through to *) and exits 1
    block = text.split('echo "PUSH-GATE: workflow_gate_scenarios (conditional, enforcing)"')[1]
    block = block.split('\nelse\n')[0]
    assert 'exit 1' in block, "the scenarios block lost its enforcing exit 1"
    assert '"SCENARIOS ok"*)' in block, "ok arm not in the enforcing block"
    assert "workflow_gate_scenarios skipped, gate script unchanged" in text, \
        "unchanged-arm skip line missing"


def test_green_run_matches_the_real_hook_pattern():
    proc = _run_scenarios(CARDS)
    first = proc.stdout.splitlines()[0] if proc.stdout else ""
    assert first.startswith("SCENARIOS ok"), f"green run no longer opens lowercase-ok: {first!r}"
    assert _replay(_ok_pattern(), first) == "OK_ARM"


@pytest.mark.skipif(shutil.which("sh") is None, reason="sh not on PATH")
def test_error_run_falls_to_the_block_arm(tmp_path):
    bad = tmp_path / "cards"
    bad.mkdir()
    (bad / "broken.card.json").write_text("{not json", encoding="utf-8")
    proc = _run_scenarios(bad)
    first = proc.stdout.splitlines()[0] if proc.stdout else ""
    assert first.startswith(("SCENARIOS FAIL", "SCENARIOS ERROR")), first
    assert _replay(_ok_pattern(), first) == "BLOCK_ARM", \
        "red/error output must fall through the ok arm (the hook would exit 1)"


def test_case_flip_is_caught():
    """The brief's exact falsifier: uppercase OK in the hook must fail this pin."""
    first = _run_scenarios(CARDS).stdout.splitlines()[0]
    flipped = _ok_pattern().replace("SCENARIOS ok", "SCENARIOS OK")
    assert _replay(flipped, first) == "BLOCK_ARM", (
        "a case-flipped pattern still matched; the pin can no longer catch "
        "the B2-338 cry-wolf shape")
