"""tests for physics_steal — deep steal on the action/roguelike/physics lineage: XCOM2-live strategy,
destructible + watermelon-soft physics, intelligent swarm enemies (Gunfire Reborn), roguelikes/lites,
and Palworld cohabitation.

RIB (frozen spec):
  route_research() -> route the deep research to the swarm via swarm_surface.route_novel (dedupe +
                      drain). Honest.
  self_map()       -> map each style target (XCOM live, destructible physics, watermelon soft,
                      intelligent swarm, roguelike perm-history, Palworld) onto our existing modules.
  learn()          -> fold the action-layer intent.

Contract: reuse swarm_surface + tesuji_shell; the swarm is the intelligent enemy, the world is
destructible verkle state, perm-death is permanent history.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import physics_steal  # noqa: E402


def test_research_threads_cover_style_targets():
    assert len(physics_steal.RESEARCH_THREADS) >= 4
    joined = " ".join(physics_steal.RESEARCH_THREADS).lower()
    for kw in ("xcom", "watermelon", "swarm", "roguelike", "palworld"):
        assert kw in joined


def test_route_routes_or_dedupes():
    r = physics_steal.route_research(enqueue=True, limit=4)
    assert r["ok"] is True
    assert "routed_to_swarm" in r and "already_deduped" in r
    assert r["honesty"]


def test_self_map_covers_style_targets():
    m = physics_steal.self_map()
    assert m["ok"] is True
    assert len(m["map"]) >= 5
    joined = " ".join(x["ours"] for x in m["map"])
    assert "swarm" in joined or "game_world" in joined  # the intelligent-enemy mechanism is ours


def test_learn_folds_intent():
    l = physics_steal.learn()
    assert l["ok"] is True
    assert "lesson_folded" in l
