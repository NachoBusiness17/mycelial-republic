"""tests for oracle — the Chainlink-style primitive for INTERNAL COHERENCE OF THE OUTSIDE WORLD.
Deterministic $0 coordinator.

RIB (frozen spec):
  fetch_sources(topic) -> multi-source fetch via OUR OWN surface; honest per-source ok flags.
  verify(sources)      -> cross-source agreement; verified=True only if >=2 sources agree on a
      non-trivial core; else honest partial (need >=2 agreeing sources).
  anchor(claim, prov)  -> content-addressed (leaf_hash) append to the anchored ledger + provenance.
  oracle(topic)        -> fetch -> verify -> anchor; only anchors when VERIFIED (or force_anchor,
      flagged). query(topic) -> the indexed map.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import oracle  # noqa: E402


def test_verify_cross_source_agreement():
    # agreeing sources -> verified with a consensus core
    v = oracle.verify([
        {"ok": True, "text": "the swarm must evolve with the chain and the wave together"},
        {"ok": True, "text": "the chain evolves with the swarm toward the wave"},
    ])
    assert v["ok"] is True
    assert "consensus" in v


def test_verify_needs_two_agreeing():
    # fewer than 2 ok sources -> honest unverified (never fabricates agreement)
    v = oracle.verify([{"ok": False, "error": "down"}, {"ok": True, "text": "only one"}])
    assert v["verified"] is False


def test_anchor_content_addressed():
    a = oracle.anchor("the outside world is coherent", provenance=["src1", "src2"], topic="test")
    assert a["ok"] is True and a["anchored"] is True
    assert a["leaf_hash"] and len(a["leaf_hash"]) == 16
    assert a["provenance"] == ["src1", "src2"]


def test_oracle_never_fabricates_when_unverified():
    # with no reachable sources, oracle does NOT anchor (honest)
    r = oracle.oracle("unreachable topic", urls=["http://127.0.0.1:1/nope"])
    assert r["ok"] is True
    assert r["anchor"]["anchored"] is False  # not verified -> not anchored


def test_query_shape():
    q = oracle.query("anything")
    assert q["ok"] is True
    assert "hits" in q and "n_hits" in q
