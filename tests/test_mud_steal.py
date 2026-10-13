"""tests for mud_steal — deep research + steal on the MUD (Multi-User Dungeon), the direct ancestor
of the republic-game.

RIB (frozen spec):
  route_research() -> route the MUD lineage deep-research to the swarm (dedupe + drain). Honest.
  self_map()       -> map each MUD mechanism (persistent world, mudlib, online creation, no-resets,
                      MUSH) onto our existing modules.
  learn()          -> fold the root (MUD is the direct ancestor, turned real).

Contract: reuse swarm_surface + tesuji_shell; the MUD's mechanisms map 1:1 onto our machinery.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import mud_steal  # noqa: E402


def test_research_threads_cover_mud_lineage():
    assert len(mud_steal.RESEARCH_THREADS) >= 3
    joined = " ".join(mud_steal.RESEARCH_THREADS).lower()
    for kw in ("mud", "persistent", "sovereignty"):
        assert kw in joined


def test_route_routes_or_dedupes():
    r = mud_steal.route_research(enqueue=True, limit=3)
    assert r["ok"] is True
    assert "routed_to_swarm" in r and "already_deduped" in r
    assert r["honesty"]


def test_self_map_covers_deep_mechanisms():
    m = mud_steal.self_map()
    assert m["ok"] is True
    assert len(m["map"]) >= 5
    joined = " ".join(x["ours"] for x in m["map"])
    assert "game_world" in joined or "swarm" in joined  # the persistent-world mechanism is ours
    assert "republic_wave" in joined or "contribute" in joined  # online-creation is ours


def test_learn_folds_root():
    l = mud_steal.learn()
    assert l["ok"] is True
    assert "lesson_folded" in l
