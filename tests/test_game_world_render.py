"""tests for game_world_render — STONE 3, the intent-gated world render. Deterministic + $0.

RIB (frozen spec):
  reveal(player, direction) -> a building appears where you steer (content-addressed + committed).
  render(region)            -> base ASCII field with revealed buildings placed.
  walk(player, direction)   -> reveal then render.
  status()                  -> the surface's contract.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_world_render as gwr  # noqa: E402


def test_status_contract():
    s = gwr.status()
    assert s["ok"] is True and "reveal" in s["contract"]


def test_reveal_intent_gated_and_deterministic():
    a = gwr.reveal(player="you", direction="north")
    b = gwr.reveal(player="you", direction="north")
    assert a["ok"] is True and a["building"]
    # same steer -> same building + same cell (persistent fidelity)
    assert a["x"] == b["x"] and a["y"] == b["y"] and a["building"] == b["building"]
    # different steer -> (almost certainly) different cell
    c = gwr.reveal(player="you", direction="east")
    assert (c["x"], c["y"]) != (a["x"], a["y"])


def test_render_places_building_in_ascii():
    reveal = gwr.reveal(player="tester", direction="south")
    r = gwr.render()
    assert r["ok"] is True and r["grid"] == [gwr.GRID_W, gwr.GRID_H]
    assert r["buildings_revealed"] >= 1
    # the building glyph is actually in the grid
    assert any(reveal["glyph"] in row for row in r["ascii"].splitlines())


def test_walk_reveal_then_render():
    w = gwr.walk(player="walker", direction="west")
    assert w["ok"] is True
    assert w["reveal"]["ok"] is True and w["render"]["ok"] is True
