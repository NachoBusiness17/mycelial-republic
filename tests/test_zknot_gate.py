"""Tests for the zknot S1 no-silent-truncation gate (ouroboros R4-L1, 2026-10-05).

The measured disease (SYNTHESIS move 3): the [:3] rewrite of LATEST.md
dropped qualifying sessions without naming them - 2026-10-05 row read
qualifying 18, LATEST carrying 3 cards, zero omission tokens. These pins
hold the cure: build_latest NAMES every cut session, and s1_gate fails
closed (main returns 2, previous LATEST kept) when a rewrite truncates
unnamed.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import zknot  # noqa: E402


def _sess(n: int, tc_ms: int, title: str) -> dict:
    return {"id": f"sess_{n:08d}abcdef", "title": title, "tc": tc_ms,
            "tu": tc_ms + 3600_000, "task_type": "default", "dir": ""}


def _cards(real: list[dict]) -> dict[str, str]:
    return {s["id"]: f"# card {s['title']}\n- body" for s in real}


def test_build_latest_names_every_cut_session():
    real = [_sess(i, 1_800_000_000_000 + i * 86_400_000, f"title {i}") for i in range(5)]
    latest, dropped = zknot.build_latest(real, _cards(real), "METER x", "2026-10-05 21:00")
    assert dropped == 2
    assert zknot.s1_gate(dropped, latest) is False, "named truncation must not fail the gate"
    assert zknot.OMIT_MARK in latest
    for s in real[3:]:
        assert zknot._short_sid(s["id"]) in latest, f"cut session {s['id']} must be named"
    for line in zknot.name_omitted(real[3:]):
        assert line in latest


def test_build_latest_no_omission_block_when_nothing_cut():
    real = [_sess(i, 1_800_000_000_000 + i * 86_400_000, f"title {i}") for i in range(3)]
    latest, dropped = zknot.build_latest(real, _cards(real), "METER x", "2026-10-05 21:00")
    assert dropped == 0
    assert zknot.OMIT_MARK not in latest
    assert zknot.s1_gate(dropped, latest) is False


def test_name_omitted_caps_at_ten_and_counts_the_rest():
    real = [_sess(i, 1_800_000_000_000 + i * 86_400_000, f"title {i}") for i in range(12)]
    lines = zknot.name_omitted(real)
    assert lines and zknot.OMIT_MARK in lines[0] and "12" in lines[0]
    named = [ln for ln in lines if ln.startswith("  - 2")]
    assert len(named) == 10, "cap is 10 names"
    assert any("+2 more" in ln for ln in lines), "the uncapped remainder is counted, not hidden"


def test_s1_gate_fails_closed_on_unnamed_truncation():
    assert zknot.s1_gate(2, "# zknot LATEST\n(no omission block)") is True, (
        "dropped sessions without the omission mark must fail closed")
    assert zknot.s1_gate(2, f"# recap\n- ... 2 {zknot.OMIT_MARK}:") is False
    assert zknot.s1_gate(0, "# zknot LATEST\n(no omission block)") is False, (
        "zero dropped sessions can never fail the gate")


def test_omission_names_survive_redaction():
    real = [_sess(0, 1_800_000_000_000, "sk-AgAmPlEsEcReTkEy123456 should not leak")]
    lines = zknot.name_omitted(real)
    joined = "\n".join(lines)
    assert "sk-AgAmPlEsEcReTkEy123456" not in joined, "the omission block rides the redact law"
