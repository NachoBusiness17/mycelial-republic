"""tests for gygax_steal — full deep research on the underpinnings back to Gygax, routed to the
swarm, with the self-steal map of mechanisms we already hold.

RIB (frozen spec):
  route_research() -> route the Gygax/OSR/roguelike/DF/generative lineage deep-research to the swarm
                      via swarm_surface.route_novel (dedupe + drain). Honest.
  self_map()       -> map each Gygax mechanism onto our existing modules (the steal lands on our
                      machinery, not new skin).
  learn()          -> fold the origin (Dwarf Fortress for agent swarms + player collabs) as a tesuji.

Contract: reuse swarm_surface + tesuji_shell; the thesis is the deep origin of the republic-game.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import gygax_steal  # noqa: E402


def test_research_threads_cover_lineage():
    assert len(gygax_steal.RESEARCH_THREADS) >= 4
    joined = " ".join(gygax_steal.RESEARCH_THREADS).lower()
    for kw in ("gygax", "dwarf fortress", "roguelike", "emergent"):
        assert kw in joined


def test_route_routes_or_dedupes():
    r = gygax_steal.route_research(enqueue=True, limit=4)
    assert r["ok"] is True
    assert "routed_to_swarm" in r and "already_deduped" in r
    assert r["honesty"]


def test_self_map_lands_on_our_modules():
    m = gygax_steal.self_map()
    assert m["ok"] is True
    assert len(m["map"]) >= 4
    joined = " ".join(x["ours"] for x in m["map"])
    assert "game_dm_voice" in joined or "game_portal" in joined  # the DM mechanism is ours


def test_learn_folds_origin():
    l = gygax_steal.learn()
    assert l["ok"] is True
    assert "lesson_folded" in l
