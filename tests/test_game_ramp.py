"""tests for game_ramp — the GAME built as the complexity ramp: tabletop -> mud -> roguelite.
Deterministic + $0, on the shared verkle world (the authority). THE DELIVERABLE.

RIB (frozen spec):
  tier()      -> current tier + mastered, persisted in the world.
  tabletop(a) -> the simplest world (scene + DM voice + actions). Always ok.
  mud(a)      -> navigable text world (rooms + exits on the world_rib map).
  roguelite(a)-> run-based dungeon (descend levels, permadeath, best depth).
  descend()   -> master the current tier + progress to the next (the ramp).
  play(a)     -> route to the current tier; a turn is a world change.
  render()    -> the base ASCII render.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_ramp as gr  # noqa: E402


def test_tiers_and_status():
    st = gr.status()
    assert st["ok"] is True
    assert st["tier"] in gr.TIERS
    assert gr.TIERS == ["tabletop", "mud", "roguelite"]


def test_tabletop_always_ok_and_persists():
    r = gr.tabletop("look")
    assert r["ok"] is True and r["tier"] == "tabletop"
    assert r["reply"] and r["turns"] >= 1


def test_mud_navigable_world():
    r = gr.mud("look")
    assert r["ok"] is True and r["tier"] == "mud"
    assert "room" in r and r["reply"]


def test_roguelite_run_descends_and_permadeath():
    r = gr.roguelite("descend")
    assert r["ok"] is True and r["tier"] == "roguelite"
    assert r["depth"] >= 1 and r["best"] >= 1
    d = gr.roguelite("die")
    assert d["reply"] and d["depth"] == 0


def test_descend_ramps_tiers():
    # master tabletop -> descend to mud (the ramp)
    from mag import game_ramp as _gr
    r = _gr.descend()
    assert r["ok"] is True
    assert r["tier"] in _gr.TIERS
    assert "tabletop" in r["mastered"]


def test_render_base_pixels():
    r = gr.render()
    assert r["ok"] is True
    assert "ascii" in r
