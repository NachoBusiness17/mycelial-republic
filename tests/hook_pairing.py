"""Shared pre-push prefix-pairing helper (B2-363).

Factors the B2-338 sh-replay pattern (tests/test_census_drift_patrol.py) so
EVERY githooks/pre-push ok case-arm is pinned to its emitter by one mechanism:
the arm PATTERN is read from the real hook bytes at test time and evaluated by
real sh against a captured output sample (exactly what the hook does with
`out=$(... 2>&1)`). Not named test_* so pytest does not collect this module.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "githooks" / "pre-push"

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

# every ok-shape case-arm consumer in githooks/pre-push and the tool whose
# first output line must carry the arm's literal (census is pinned live by
# B2-338's own band; it is listed here so "every consumer" stays enumerated)
CONSUMERS = {
    "FRESHNESS-GATE: ok": "tools/freshness_gate.py",
    "CENSUS-PATROL: ok": "tools/census_drift_patrol.py",
    "REFOLD-GATE: ok": "tools/refold_gate.py",
    "RESULT: PASS": "scripts/the50_t21_q_caption_ledger_verify.py",
    "SCENARIOS ok": "tools/workflow_gate.py",
}


def hook_arm_pattern(literal: str) -> str:
    """Extract the quoted case-arm pattern for `literal` from the real
    githooks/pre-push bytes (e.g. '"FRESHNESS-GATE: ok"*'). Fails when the
    arm is missing or duplicated: a second arm for the same literal means the
    pairing under test is ambiguous."""
    text = HOOK.read_text(encoding="utf-8")
    arms = re.findall(r'(\*?"(?:%s)"\*)\)' % re.escape(literal), text)
    assert len(arms) == 1, f"expected exactly one pre-push case arm for {literal!r}, found {len(arms)}"
    return arms[0]


def sh_arm_decision(pattern: str, sample: str) -> str:
    """Evaluate real sh case-matching of `sample` (the tool's captured first
    output line) against the hook's arm pattern; returns OK_ARM or WARN_ARM
    exactly as the hook's arms would route it."""
    replay = 'case "$1" in ' + pattern + ') echo OK_ARM ;; *) echo WARN_ARM ;; esac'
    r = subprocess.run(["sh", "-c", replay, "sh", sample],
                       capture_output=True, text=True, timeout=60,
                       creationflags=HEADLESS)
    return (r.stdout or "").strip()


def source_ok_literal(rel_path: str, literal: str) -> str:
    """Assert the emitter's source bytes still contain the ok literal (static
    pairing half for emitters whose green run is expensive). Returns the
    matched literal so the test can replay it through sh."""
    src = (ROOT / rel_path).read_text(encoding="utf-8")
    assert literal in src, f"{rel_path} no longer prints {literal!r}: the hook pairing is broken"
    return literal
