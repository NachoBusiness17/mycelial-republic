"""Starvation law tests — the sensor the spec lacked (operator 2026-09-28).

"this whole starve out thing is bullshit and our water computer spec should
have picked it up": a gated junction that eats water while looking like a
gate is silent starvation. These pin (1) pooling — under-gate inflow HOLDS
and can still reach the gate later; (2) the STARVED event — pooled water
spilled with no new inflow is NAMED; (3) the healthy path unchanged.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402


def _net():
    g = WaterGraph()
    g.add_node("src", elev=6, volume=8)
    g.add_node("mid", elev=5, volume=8)
    g.add_node("jx", elev=3, kind="sill", sill=2)
    g.add_node("out", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("a", "src", "jx", cap=4)
    g.add_pipe("b", "mid", "jx", cap=4)
    g.add_pipe("j", "jx", "out", cap=8)
    return g


def test_starved_junction_pools_instead_of_eating():
    g = _net()
    g.close("b")                      # starve the second inlet
    evs = g.tick()
    joined = " | ".join(evs)
    assert "holds 4 below gate" in joined, joined
    assert g.volume("jx") == 4, "the single inlet's water must POOL, not vanish"
    assert "STARVED" not in joined, "pooling with live inflow is not starvation"


def test_starved_event_fires_when_pooled_water_dies():
    g = _net()
    g.close("b")
    g.tick()                          # pools 4
    g.nodes["src"].volume = 0         # now NO inflow at all
    evs = g.tick()
    joined = " | ".join(evs)
    assert "STARVED" in joined and "4 pooled units" in joined, joined
    assert g.volume("jx") == 0, "dead pooled water is spilled, but NAMED"
    # V5 economy law (2026-09-29): the spill ROUTES to the waste basin —
    # the old law zeroed it into the void; slow starters lost the economy.
    assert g.volume("waste") == 4, "STARVED spill must be HELD at waste, not deleted"
    assert "boil waste to recover" in joined, joined


# ---- V5 economy law (2026-09-29): waste is a basin, never a void ----------


def test_piped_to_waste_is_held_not_deleted():
    g = WaterGraph()
    g.add_node("tank", elev=2, volume=3)
    g.add_node("pit", elev=0, kind="waste")
    g.add_pipe("drain", "tank", "pit", cap=2)
    evs = g.tick()
    assert g.volume("pit") == 2, "units piped to waste must accumulate there"
    assert g.volume("tank") == 1
    assert any("to waste at pit" in e for e in evs), evs


def test_boil_from_waste_condenses_at_crown():
    """The recovery loop: STARVED units are boiled back out of waste as
    steam (pipes ignored) and condense at the highest cold node. The
    8-unit economy is conserved end to end."""
    g = _net()
    g.add_node("crown", elev=9, kind="cold")
    g.close("b")
    g.tick()                          # pools 4 at jx
    g.nodes["src"].volume = 0
    g.tick()                          # STARVED: 4 spill to waste
    assert g.volume("waste") == 4
    lifted = g.boil("waste", 4)       # player action near the waste pool
    assert lifted == 4
    assert g.volume("waste") == 0 and g.nodes["waste"].steam == 4
    evs = g.tick()
    assert g.volume("crown") == 4, "steam from waste must condense at the crown"
    assert any("Steam condenses" in e for e in evs), evs


def test_starved_economy_conserves_total_units():
    """Z14's hidden flaw, pinned: nothing the STARVED path does may change
    the total water in the network (here 16 = 8 + 8). No hand-edits — src
    drains naturally through two pooling ticks, then starves."""
    g = _net()
    g.add_node("crown", elev=9, kind="cold")
    total0 = sum(n.volume + n.steam for n in g.nodes.values())
    g.close("b")
    g.tick()                          # pools 4
    g.tick()                          # pools 4 more; src now dry
    g.tick()                          # STARVED: 8 spill to waste
    assert g.volume("waste") == 8
    g.boil("waste", 3)
    g.tick()                          # steam condenses at crown
    total1 = sum(n.volume + n.steam for n in g.nodes.values())
    assert total0 == total1 == 16, "economy must conserve through starve + boil"


def test_starved_without_waste_node_holds_at_junction():
    g = _net()
    del g.nodes["waste"]              # a spec with no basin
    g.close("b")
    g.tick()                          # pools 4
    g.nodes["src"].volume = 0
    evs = g.tick()
    joined = " | ".join(evs)
    assert "STARVED" in joined and "4 pooled units" in joined, joined
    assert g.volume("jx") == 4, "no waste node: conserve by HOLDING, never delete"


def test_pool_can_still_reach_the_gate():
    g = _net()
    g.close("b")
    g.tick()                          # pools 4 from src
    g.open("b")                       # second inlet returns
    evs = g.tick()
    joined = " | ".join(evs)
    assert "sill reached" in joined, joined
    assert g.volume("out") == 8, "pooled + new inflow reaches the gate together"


def test_healthy_both_inlet_path_unchanged():
    g = _net()
    evs = g.tick()
    assert g.volume("out") == 8
    assert "sill reached (2 inlets)" in " | ".join(evs)
