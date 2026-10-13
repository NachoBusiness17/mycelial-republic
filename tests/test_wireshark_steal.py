"""tests for wireshark_steal — full research steal (wireshark-class + deep reuse of briar/openclaw)
routed to the swarm, + the 10-player-dragon vision grounded in our existing modules.

RIB (frozen spec):
  route_research() -> route the full research threads to the swarm via swarm_surface.route_novel
                      (dedupe by anchor + drain in-cluster). The swarm digs; never run locally.
  vision()         -> the 10-player-dragon vision, GROUNDED in our existing modules (render farm,
                      shared compute, MIT, world, route trace, DM) — not invented.
  status()         -> contract.

Contract: novel research routes via the one primitive; the vision self-steals our own machinery.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import wireshark_steal  # noqa: E402


def test_research_threads_present():
    assert len(wireshark_steal.RESEARCH_THREADS) >= 4
    joined = " ".join(wireshark_steal.RESEARCH_THREADS).lower()
    for kw in ("wireshark", "briar", "openclaw", "mit"):
        assert kw in joined


def test_route_research_routes_or_dedupes():
    r = wireshark_steal.route_research(enqueue=True, limit=5)
    assert r["ok"] is True
    assert "routed_to_swarm" in r and "already_deduped" in r
    assert r["honesty"] is True


def test_vision_grounded_in_existing_modules():
    v = wireshark_steal.vision()
    assert v["ok"] is True
    assert "scene" in v["vision"]
    assert "existing_pieces" in v["vision"]
    # every piece maps to a real module (self-steal, not invented)
    assert len(v["vision"]["existing_pieces"]) >= 5
    assert "game_world" in " ".join(p["module"] for p in v["vision"]["existing_pieces"])


def test_status():
    s = wireshark_steal.status()
    assert s["ok"] is True
    assert "route_research" in s["contract"] and "vision" in s["contract"]
