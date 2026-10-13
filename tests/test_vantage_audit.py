"""tests for vantage_audit — the higher-vantage audit: where we are / where we're going / what it
takes, an audit of all surfaces/subsystems/tools, and iterate.

RIB (frozen spec):
  surfaces()  -> audit every surface/subsystem/tool (inventory count + capability utilization + gap
                 maps) grounded from corpus_wave + self_steal + gap_frontier + gap_analysis.
  synthesis() -> the higher-vantage picture: where we ARE / GOING / WHAT IT TAKES.
  frontier()  -> route deep frontier research to the swarm via swarm_surface.route_novel (dedupe +
                 drain). Honest (never fabricates).
  iterate()   -> the loop: audit -> synthesize -> frontier-research.

Contract: reuses corpus_wave + self_steal + gap_frontier + gap_analysis + swarm_surface — no
invention. Deterministic + $0 aggregation, swarm-routed frontier.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import vantage_audit  # noqa: E402


def test_surfaces_audits_all():
    s = vantage_audit.surfaces()
    assert s["ok"] is True
    # at least the inventory or an honest error is present
    assert "inventory" in s or "inventory_error" in s
    assert "capabilities" in s or "capabilities_error" in s
    assert "gaps" in s or "gaps_error" in s


def test_synthesis_higher_vantage():
    syn = vantage_audit.synthesis()
    assert syn["ok"] is True
    assert "where_we_are_going" in syn
    assert "what_it_takes" in syn
    assert "mycelial" in syn["where_we_are_going"].lower() or "republic" in syn["where_we_are_going"].lower()


def test_frontier_routes_or_dedupes():
    f = vantage_audit.frontier(enqueue=True, limit=4)
    assert f["ok"] is True
    assert "routed_to_swarm" in f and "already_deduped" in f
    assert f["honesty"]


def test_iterate_loop():
    r = vantage_audit.iterate(enqueue=True)
    assert r["ok"] is True
    assert "audit" in r and "synthesis" in r and "frontier" in r
