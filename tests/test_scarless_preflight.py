"""Scarless-preflight tests (Mickey17 W2, 2026-09-29).

Ledger return 25 named the heredity: 69% of registered ratchet debt is
except-pass, and the improvement is that endemic rules move to PREflight for
files born after a cutoff, so the next clone cannot inherit the scar. These
tests pin the three laws of that rule against the REAL frozen contract
(configs/constitutional_rails.json), not a synthetic copy:

1. Grandfathered: a file whose git first-commit is on/before the cutoff
   keeps its scars (the write passes).
2. Birth: a file with no git history (untracked, being born now) carrying
   a bare `except Exception: pass` or `except: pass` is BLOCKED at preflight.
3. Health: a new file with real handling (log + return, re-raise, typed
   non-pass body) passes untouched.

The git age probe (rails._git_first_commit) is monkeypatched per test; the
probe contract it must honor is: ISO date string, '' = untracked,
'?' = git probe failed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import rails  # noqa: E402

SCAR = "try:\n    boil()\nexcept Exception:\n    pass\n"
BARE_SCAR = "try:\n    boil()\nexcept:\n    pass\n"
HANDLED = (
    "try:\n    boil()\n"
    'except Exception as e:\n    logger.warning("boil failed: %s", e)\n'
    "    return None\n"
)


def _rule() -> dict:
    for rule in rails.load_rails().get("write_file_content", []):
        if rule.get("git_first_commit_after"):
            return rule
    return {}


def test_rule_is_in_the_frozen_contract():
    """The scar law lives in configs/constitutional_rails.json, not in code."""
    rule = _rule()
    assert rule.get("id") == "no_new_except_pass"
    assert rule.get("git_first_commit_after") == "2026-09-29"
    assert rule.get("severity") == "block"
    # The regex must compile (a broken regex would silently skip the rail).
    re.compile(rule["regex"])


def test_grandfathered_old_file_keeps_its_scars(monkeypatch):
    """Law 1: first-commit 2026-09-28 (before cutoff) -> scar write passes."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "2026-09-28")
    ok, msg = rails.check_content("mag/old_timer.py", SCAR)
    assert ok is True
    assert msg == ""


def test_grandfather_boundary_is_inclusive(monkeypatch):
    """Born ON the wave date = existing estate -> grandfathered."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "2026-09-29")
    ok, _ = rails.check_content("mag/wave_day_file.py", SCAR)
    assert ok is True


def test_file_born_after_cutoff_is_blocked(monkeypatch):
    """First-commit 2026-10-01 (after cutoff) -> the scar is blocked."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "2026-10-01")
    ok, msg = rails.check_content("mag/next_clone.py", SCAR)
    assert ok is False
    assert "no_new_except_pass" in msg


def test_new_untracked_file_with_except_pass_is_blocked(monkeypatch):
    """Law 2: no git history (being born now) -> blocked, rail named."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "")
    ok, msg = rails.check_content("mag/brand_new.py", SCAR)
    assert ok is False
    assert "no_new_except_pass" in msg


def test_new_untracked_file_with_bare_except_pass_is_blocked(monkeypatch):
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "")
    ok, msg = rails.check_content("mag/brand_new.py", BARE_SCAR)
    assert ok is False
    assert "no_new_except_pass" in msg


def test_new_file_with_proper_handling_passes(monkeypatch):
    """Law 3: real handling (log + return) is not a scar, write passes."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "")
    ok, msg = rails.check_content("mag/brand_new.py", HANDLED)
    assert ok is True
    assert msg == ""


def test_git_probe_failure_fails_open(monkeypatch):
    """Engine law: git unknowable ('?') -> rule skipped, never a wrong block;
    the pre-push ratchet stays the backstop for undatable files."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "?")
    ok, _ = rails.check_content("mag/anywhere.py", SCAR)
    assert ok is True


def test_existing_rules_unaffected_by_extension(monkeypatch):
    """The date gate wraps only cutoff-bearing rules: the secret rail still
    fires for a grandfathered path (regression guard on the additive claim)."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "2020-01-01")
    leak = 'API_KEY = "sk-abcdefghij0123456789"'
    ok, msg = rails.check_content("mag/old_timer.py", leak)
    assert ok is False
    assert "no_live_secret_values" in msg


def test_check_write_file_routes_through_content_rails(monkeypatch):
    """The exact preflight door agent_cli:717 uses blocks the new-born scar."""
    monkeypatch.setattr(rails, "_git_first_commit", lambda p: "")
    ok, msg = rails.check_write_file("mag/brand_new.py", SCAR)
    assert ok is False
    assert "no_new_except_pass" in msg
