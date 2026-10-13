"""tests for game_dfhack — the OVERLAY that sits over the game like DFHack over Dwarf Fortress.
I drive the game; I don't just play it. Deterministic + $0.

RIB (frozen spec):
  status()   -> the overlay's deep view (tier + world knots).
  force(tier, action) -> drive any tier directly regardless of current tier.
  script(steps)       -> run a scripted sequence of turns.
  autoplay(n)         -> the world self-plays, folding real work through the dungeon.
  edit(key, value)    -> modify the world state directly.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_dfhack as gd  # noqa: E402


def test_status_deep_view():
    s = gd.status()
    assert s["ok"] is True
    assert "tier" in s and "world_knots" in s
    assert "overlay" in s["role"]


def test_force_any_tier():
    r = gd.force("tabletop", "look")
    assert r["ok"] is True
    assert r["tier"] == "tabletop"
    # unknown tier honest
    assert gd.force("nope", "look")["ok"] is False


def test_script_runs_sequence():
    r = gd.script([("tabletop", "look"), ("mud", "look"), ("roguelite", "descend")])
    assert r["ok"] is True and r["n_steps"] == 3
    assert len(r["results"]) == 3


def test_autoplay_self_plays():
    r = gd.autoplay(2)
    assert r["ok"] is True
    assert r["n"] == 2
    assert len(r["turns"]) == 2


def test_edit_world():
    r = gd.edit("game.dfhack.test", {"v": 1})
    assert r["ok"] is True and r["set"] is True
