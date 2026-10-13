"""B2-427 (2026-09-26): pin the append-only line contract of REGISTRY.jsonl.

All seven workflow_gate scenario cards cite registry rows by fixed line
number as history, but validate_card keys identity on (ts, digest) only, so
a compaction pass that sorted or deduped the registry would silently move
every card's cited line while the gate stayed green. This probe fails on ANY
rewrite of the recorded prefix: every baseline line must still sit at its
original ordinal with the same bytes (pure appends pass by construction),
and every card's cited ordinal must still carry the exact row the card
cites. Baseline: configs/workflow_registry_baseline.json (append a fresh
baseline in the same landing as any registry migration, never in place).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "memory" / "workflows" / "REGISTRY.jsonl"
BASELINE = ROOT / "configs" / "workflow_registry_baseline.json"

pytestmark = pytest.mark.skipif(
    not REGISTRY.exists() or not BASELINE.exists(),
    reason="registry or baseline missing",
)


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def test_registry_prefix_is_unchanged():
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    live = REGISTRY.read_text(encoding="utf-8").splitlines()
    # the registry may only GROW: never shrink, never rewrite its head
    assert len(live) >= base["lines"], (
        f"registry shrank: {base['lines']} baseline lines -> {len(live)}; "
        "a compaction/rewrite moved every card's cited line")
    for i, want in enumerate(base["line_sha256"]):
        got = _sha(live[i])
        assert got == want, (
            f"registry line {i + 1} was rewritten, reordered or deduped "
            f"(baseline sha {want[:12]}, live {got[:12]}): the append-only "
            f"line contract is broken and every card citation is stale")


def test_card_citations_still_resolve_to_the_same_rows():
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    live = REGISTRY.read_text(encoding="utf-8").splitlines()
    for cite in base["card_citations"]:
        ln = cite["line"]
        assert ln <= len(live), f"{cite['card']} cites line {ln}, registry shrank to {len(live)}"
        assert _sha(live[ln - 1]) == cite["sha256"], (
            f"{cite['card']} cites line {ln} but the row at that ordinal "
            f"changed: the registry was rewritten under the cards")
