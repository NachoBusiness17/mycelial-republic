"""Pre-push prefix pairing pins (B2-363, 2026-09-26).

The 2026-09-25 crying-wolf disease (census green runs taking the WARN arm
because the emitter printed uppercase OK) is cured for the census channel by
B2-338's sh replay. B2-363 extends the pairing pin to EVERY pre-push ok
case-arm so a case drift on any other channel goes red in tests instead of
re-training operators to dismiss WARNs:

- freshness: LIVE both-directions band (a green receipt run and a stale run,
  captured output replayed through real sh against the hook's own arm bytes);
- census: live band already owned by tests/test_census_drift_patrol.py
  (B2-338); this file only asserts the arm still exists exactly once;
- refold / caption / scenarios: static pairing half (emitter source must
  still print the ok literal) PLUS the same sh replay of the literal through
  the hook arm, including a case-mutated sample that must fall to WARN_ARM
  (the falsifier: a mutated ok token case that no test catches).

Owning brief: QUEUE.md B2-363. Falsifier: mutate an emitter's ok token case
and no gate test goes red -> this file is the test that goes red.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

# plain (non-package) layout: pytest puts tests/ itself on sys.path, so the
# shared helper imports by module name (the census tests import tools.* the
# same way, from the repo root pytest also inserts)
import hook_pairing as hp
from hook_pairing import CONSUMERS, hook_arm_pattern, sh_arm_decision, source_ok_literal

ROOT = Path(__file__).resolve().parents[1]
FRESHNESS = ROOT / "tools" / "freshness_gate.py"

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

pytestmark = pytest.mark.skipif(shutil.which("sh") is None, reason="sh not on PATH")


def test_every_pre_push_ok_consumer_is_enumerated():
    # the registry must cover every ok-shape case arm actually present in the
    # hook bytes: a new arm without a pin here is an unpinned pairing
    text = (ROOT / "githooks" / "pre-push").read_text(encoding="utf-8")
    arms = set(text.split("case")[0]) and set()
    import re
    arms = set(re.findall(r'\n\s*(\*?"[A-Z][A-Za-z: -]*?(?: ok|: ok|: PASS)"?\*)\)', text))
    for arm in arms:
        literal = arm.lstrip("*").rstrip("*").strip('"')
        assert literal in CONSUMERS, f"unpinned pre-push ok arm: {literal!r}"
    for literal in CONSUMERS:
        hook_arm_pattern(literal)  # exactly-once check per consumer


def test_freshness_green_run_takes_ok_arm_live(tmp_path):
    receipt = tmp_path / "fresh.md"
    receipt.write_text(f"source-fetched: {date.today().isoformat()}\nclaim here\n", encoding="utf-8")
    out = subprocess.run([sys.executable, str(FRESHNESS), str(receipt)],
                         capture_output=True, text=True, timeout=120,
                         creationflags=HEADLESS)
    assert out.returncode == 0, out.stdout + out.stderr
    first = out.stdout.splitlines()[0]
    assert first.startswith("FRESHNESS-GATE: ok"), repr(first)
    assert sh_arm_decision(hook_arm_pattern("FRESHNESS-GATE: ok"), first) == "OK_ARM"


def test_freshness_stale_run_takes_warn_arm_live(tmp_path):
    receipt = tmp_path / "stale.md"
    receipt.write_text("source-fetched: 2026-09-01\nclaim here\n", encoding="utf-8")
    out = subprocess.run([sys.executable, str(FRESHNESS), str(receipt)],
                         capture_output=True, text=True, timeout=120,
                         creationflags=HEADLESS)
    assert out.returncode != 0
    first = out.stdout.splitlines()[0]
    assert first.startswith("FRESHNESS-GATE: FAIL"), repr(first)
    assert sh_arm_decision(hook_arm_pattern("FRESHNESS-GATE: ok"), first) == "WARN_ARM"


def test_freshness_case_mutated_ok_token_falls_to_warn_arm():
    # the brief's falsifier, both directions: an emitter that drifts to
    # uppercase OK must take the WARN arm (crying wolf), not the ok arm
    pattern = hook_arm_pattern("FRESHNESS-GATE: ok")
    assert sh_arm_decision(pattern, "FRESHNESS-GATE: OK receipt (fresh)") == "WARN_ARM"


def test_refold_literal_pairs_with_hook_arm():
    pattern = hook_arm_pattern("REFOLD-GATE: ok")
    literal = source_ok_literal("tools/refold_gate.py", "REFOLD-GATE: ok")
    sample = 'REFOLD-GATE: ok (pins ran against host: 12 passed; guard ok)'
    assert sh_arm_decision(pattern, sample) == "OK_ARM"
    assert sh_arm_decision(pattern, "REFOLD-GATE: OK (pins ran)") == "WARN_ARM"


def test_caption_pass_literal_pairs_with_hook_arm():
    pattern = hook_arm_pattern("RESULT: PASS")
    literal = source_ok_literal("scripts/the50_t21_q_caption_ledger_verify.py", "RESULT: {'PASS' if ok else 'FAIL'}")
    assert literal  # source still builds the PASS/FAIL line
    assert sh_arm_decision(pattern, "RESULT: PASS - 51 rows, all checks green") == "OK_ARM"
    assert sh_arm_decision(pattern, "RESULT: PASSX - rows") == "OK_ARM"  # leading-glob arm is a prefix arm
    assert sh_arm_decision(pattern, "RESULT: Fail - rows") == "WARN_ARM"


def test_scenarios_ok_literal_pairs_with_hook_arm():
    pattern = hook_arm_pattern("SCENARIOS ok")
    source_ok_literal("tools/workflow_gate.py", "SCENARIOS ok")
    assert sh_arm_decision(pattern, "SCENARIOS ok   pass_control: all seven gates clean") == "OK_ARM"
    assert sh_arm_decision(pattern, "SCENARIOS OK   pass_control") == "WARN_ARM"
