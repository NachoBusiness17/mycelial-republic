"""Tests for mag.invariant — the stable-prefix / cache-hit invariant.

Proves the session prefix is byte-identical across different asks (cache-safe),
pins via spec_gate + verkle, and check() reports stability (and drift).
Deterministic, no LLM, no network.
"""
from __future__ import annotations

import hashlib

from mag import invariant


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_stable_prefix_is_byte_identical_across_asks():
    a = invariant.stable_prefix("coding-agent")
    b = invariant.stable_prefix("coding-agent")
    assert a == b
    assert _sha(a) == _sha(b)
    assert a  # non-empty


def test_stable_prefix_excludes_volatile_learned_tail():
    # stable_prefix must NOT contain the volatile learned/case-law or the delim.
    assert invariant.DELIM not in invariant.stable_prefix("coding-agent")
    # it does include the seed + formatting
    assert "Session seed" in invariant.stable_prefix("coding-agent")


def test_preamble_separates_stable_and_tail():
    p = invariant.preamble("fix a typo", "coding-agent", with_model=False)
    assert p["delim"] in p["text"]
    # stable prefix identical to standalone stable_prefix (the invariant)
    assert p["prefix"] == invariant.stable_prefix("coding-agent")
    assert p["prefix_len"] > 0


def test_preamble_prefix_stable_across_asks():
    a = invariant.preamble("fix a typo", "coding-agent", with_model=False)
    b = invariant.preamble("design the protocol", "coding-agent", with_model=False)
    assert a["prefix"] == b["prefix"]
    assert _sha(a["prefix"]) == _sha(b["prefix"])


def test_freeze_then_check_is_stable():
    r = invariant.freeze("test-state", label="test")
    assert r["ok"] is True
    c = invariant.check("test-state")
    assert c["ok"] is True
    assert c["stable"] is True
    assert c["prefix_stable"] is True


def test_check_unpinned_reports_needs_freeze():
    c = invariant.check("no-such-state-xyz")
    assert c["ok"] is False
    assert c["stable"] is False
    assert "freeze" in c.get("error", "")


def test_drift_is_detected_by_sha_change():
    # Pin one sha, then mutate the pinned record to simulate drift -> unstable.
    st = "drift-test-state"
    invariant.freeze(st)
    state = invariant._load_state()
    state["pins"][st]["sha"] = "0" * 64  # simulate the world changed
    invariant._save_state(state)
    c = invariant.check(st)
    assert c["prefix_stable"] is False
    assert "RE-FREEZE" in c.get("action", "")
