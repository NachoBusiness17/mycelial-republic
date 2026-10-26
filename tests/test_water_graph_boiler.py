"""boiler's toll tests - the steam lift's cost, the state-gated sky,
and the forgetful drift mass (mariner cycle 9, 2026-10-15).

THE BOILER'S TOLL, the cycle-7 receipt's self-chosen NEXT THREAD, landed
with ZERO engine bytes: every pin here composes kinds the engine already
has. The steam lift is the engine's only uphill route (the DAG law) and
it is actuated, never autonomous: these pins price the shovel. Laws: (1)
on a cap-1 descent a batch lift and a stream lift complete on the same
tick, so the actuation count is the whole cost and the cold crown is a
free buffer; (2) every cloud condenses at the one highest cold node, so
a lower cold crown is shadowed while any higher exists; (3) boiling the
top cold node itself is a dead lift whose only trace is an event line;
(4) a rotor-charged latch gates the operator's shovel: state, not
physics, throttles the weather, and the verdict lags the pool by one
tick (rotor landings commit after the verdict phase); (5) the world verb
layer has zero lift latency: a staged boil rains the same tick; (6) a
plain two-hop leg flips a train's phase by pipe insertion order (+0
chained vs +1 delayed) while the drift mass stays invariant: the offset
is readable only in the accrual, never in the completed total. Spec:
mag/water_graph.py module docstring, THE BOILER'S TOLL block; receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261015_mariner.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402
from server.world import MountainWorld  # noqa: E402


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _lift_board() -> WaterGraph:
    """The two-basin lift: basin, cold crown, receiver (cap-1 descent)."""
    g = WaterGraph()
    g.add_node("basin", elev=0, volume=4)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("rcv", elev=5)
    g.add_pipe("cr", "crown", "rcv", cap=1)
    return g


def test_batch_lift_beats_stream_on_shovel_economy():
    """The shovel economy (probes A1+A2, traced): board A lifts 4 units
    with ONE actuation (boil(basin, 4)); board B lifts the same 4 with
    FOUR acts of 1. The rain lands at t1 on both boards (all 4 at once
    vs 1 per tick) and the crown's cap-1 drain finishes on the SAME
    tick 4: the completion time is set by the descent's outflow, never
    by the shovel. The actuation count is the whole cost: 1 vs 4. The
    crown held the whole batch for three ticks without spilling: a
    cold node is a plain accumulator, a free buffer. End on both:
    basin 0/0 steam, crown 0, rcv 4, conserved 4."""
    a = _lift_board()
    assert a.boil("basin", 4) == 4
    assert a.volume("basin") == 0 and a.nodes["basin"].steam == 4
    assert a.tick() == ["Steam condenses at crown (+4).", "cr: 1 crown->rcv."]
    for _ in range(3):
        assert a.tick() == ["cr: 1 crown->rcv."]
    assert a.tick() == []
    assert a.volume("rcv") == 4 and a.volume("crown") == 0
    assert _total(a) == 4

    b = _lift_board()
    acts = 0
    for i in range(4):
        b.boil("basin", 1)
        acts += 1
        assert b.tick() == ["Steam condenses at crown (+1).", "cr: 1 crown->rcv."]
    assert acts == 4
    assert b.tick() == []
    assert b.volume("rcv") == 4 and b.volume("crown") == 0
    assert _total(b) == 4


def test_the_sky_is_one_bus_to_the_highest_crown():
    """The one-bus sky (probe A3, traced): two basins under two cold
    crowns, lo at elevation 8 and hi at 10, each with a cap-1 drain.
    boil(b1, 2) then boil(b2, 1): EVERY unit condenses at hi; lo never
    receives a drop while a higher crown exists (it stays 0 through
    the whole run and rcvLo stays 0). The sky is a single bus to max-
    elevation cold: route lifts by crown elevation, never by basin
    proximity. End: rcvHi 3, everything else 0, conserved 3."""
    g = WaterGraph()
    g.add_node("b1", elev=0, volume=2)
    g.add_node("b2", elev=0, volume=1)
    g.add_node("lo", elev=8, kind="cold")
    g.add_node("hi", elev=10, kind="cold")
    g.add_node("rcvLo", elev=5)
    g.add_node("rcvHi", elev=5)
    g.add_pipe("cl", "lo", "rcvLo", cap=1)
    g.add_pipe("ch", "hi", "rcvHi", cap=1)
    g.boil("b1", 2)
    assert g.tick() == ["Steam condenses at hi (+2).", "ch: 1 hi->rcvHi."]
    g.boil("b2", 1)
    assert g.tick() == ["Steam condenses at hi (+1).", "ch: 1 hi->rcvHi."]
    assert g.tick() == ["ch: 1 hi->rcvHi."]
    assert g.tick() == []
    assert g.volume("hi") == 0 and g.volume("rcvHi") == 3
    assert g.volume("lo") == 0 and g.volume("rcvLo") == 0
    assert g.volume("b1") == 0 and g.volume("b2") == 0
    assert g.nodes["b1"].steam == 0 and g.nodes["b2"].steam == 0
    assert _total(g) == 3


def test_boil_at_the_top_crown_is_a_dead_lift():
    """The dead lift (probe A4, traced): a cold crown at elevation 10
    already holds 1 unit and drains cap-1 to a receiver. boil(crown, 1)
    lifts that unit to steam; at t1 it condenses back into the SAME
    node before the pipes move, and the drain carries it out exactly
    as if nothing had been boiled: end volumes byte-match a no-boil
    control (crown 0, rcv 1 on both), and the actuation's only trace
    is the extra "Steam condenses at crown (+1)." line. One wasted
    shovel, zero water moved: never boil the top crown."""
    g = WaterGraph()
    g.add_node("crown", elev=10, kind="cold", volume=1)
    g.add_node("rcv", elev=5)
    g.add_pipe("cr", "crown", "rcv", cap=1)
    g.boil("crown", 1)
    assert g.tick() == ["Steam condenses at crown (+1).", "cr: 1 crown->rcv."]
    assert g.tick() == []
    k = WaterGraph()
    k.add_node("crown", elev=10, kind="cold", volume=1)
    k.add_node("rcv", elev=5)
    k.add_pipe("cr", "crown", "rcv", cap=1)
    assert k.tick() == ["cr: 1 crown->rcv."]
    assert k.tick() == []
    assert g.nodes["crown"].volume == k.nodes["crown"].volume == 0
    assert g.volume("rcv") == k.volume("rcv") == 1
    assert _total(g) == 1 and _total(k) == 1


def test_the_latch_gates_the_weather():
    """The gated boiler, flagship (probe B1, traced): a k=2 rotor (its
    first outlet a digit sink, its second a drip into the level-2
    latch L) feeds verdicts to an operator loop that reads each tick's
    events and shovels ONE unit from the boiler basin between ticks,
    only on a "Latch L opens" line. The verdict LAGS the pool: the b
    drip lands at t4 (committed, after t4's verdict phase), so the
    pool reads 2 for the first time at t5's verdict: the first open is
    t5, not t4. Shovel 1 after t5 rains at t6; the second drip recharges
    the pool at t6 (landing after t6's verdict), t7 opens on a DRY tick
    (the only gate that can), shovel 2 rains at t8. Then the feed is
    dead, the rotor parks, the latch sits at pool 1 in silence, and
    the shovel never fires again: the state, not the physics, gated
    the weather. Exact lists t1-t8; shovels == opens == delivered ==
    2; end: digit 3, L 1, lsnk 2, boiler 1, rcv 2, conserved 9."""
    g = WaterGraph()
    g.add_node("feed", elev=9, volume=6)
    g.add_node("R", elev=8, kind="vortex")
    g.add_node("digit", elev=1)
    g.add_node("L", elev=5, kind="latch", sill=2)
    g.add_node("lsnk", elev=1)
    g.add_node("boiler", elev=0, volume=3)
    g.add_node("crown", elev=12, kind="cold")
    g.add_node("rcv", elev=5)
    g.add_pipe("in", "feed", "R", cap=1)
    g.add_pipe("a", "R", "digit", cap=1)
    g.add_pipe("b", "R", "L", cap=1)
    g.add_pipe("ol", "L", "lsnk", cap=1)
    g.add_pipe("cr", "crown", "rcv", cap=1)
    shovels, opens = 0, 0
    expected = [
        ["in: 1 feed->R.", "a: 1 R->digit."],
        ["in: 1 feed->R.", "b: 1 R->L."],
        ["in: 1 feed->R.", "a: 1 R->digit."],
        ["in: 1 feed->R.", "b: 1 R->L."],
        ["in: 1 feed->R.", "Latch L opens (pool 2 >= level 2).",
         "ol: 1 L->lsnk.", "a: 1 R->digit."],
        ["Steam condenses at crown (+1).", "in: 1 feed->R.",
         "cr: 1 crown->rcv.", "b: 1 R->L."],
        ["Latch L opens (pool 2 >= level 2).", "ol: 1 L->lsnk."],
        ["Steam condenses at crown (+1).", "cr: 1 crown->rcv."],
    ]
    for want in expected:
        evs = g.tick()
        assert evs == want, evs
        for e in evs:
            if e.startswith("Latch L opens"):
                opens += 1
        if opens > shovels and g.volume("boiler") > 0:
            g.boil("boiler", 1)  # the operator's shovel, between ticks
            shovels += 1
    assert g.tick() == [], "the silent tail: dead feed, parked rotor, pool 1"
    assert shovels == 2 and opens == 2 and g.volume("rcv") == 2
    assert g.volume("digit") == 3 and g.volume("L") == 1
    assert g.volume("lsnk") == 2 and g.volume("boiler") == 1
    assert g.volume("feed") == 0 and g.volume("crown") == 0
    assert _total(g) == 9


def test_world_stage_boil_rains_the_same_tick():
    """The world verb layer has ZERO lift latency (probe B2, traced on
    the Mountain board): a staged boil applies at tick start, BEFORE
    condense, so tick 1's own event row carries both the boil line and
    the rain line ("mariner boils 1 at spring; it rises." + "Steam
    condenses at crown (+1).") and the crown reads 1 at the same tick.
    Two more boils staged in one beat apply in arrival order and MERGE
    in the origin node: tick 2 carries two boil lines and ONE rain line
    (+2), crown 3. The engine-level between-ticks boil costs one tick
    of latency; the world verb costs none: the shovel is inside the
    beat."""
    w = MountainWorld()
    w.register_session("s1", "mariner")
    ack = w.stage("s1", "boil", "spring")
    assert ack["op"] == "ack" and ack["applies_at_tick"] == 1
    t1 = w.tick()
    assert t1["events"][0] == "mariner boils 1 at spring; it rises."
    assert "Steam condenses at crown (+1)." in t1["events"]
    assert t1["nodes"]["crown"] == 1
    assert w.stage("s1", "boil", "spring")["op"] == "ack"
    assert w.stage("s1", "boil", "spring")["op"] == "ack"
    t2 = w.tick()
    boils = [e for e in t2["events"] if e == "mariner boils 1 at spring; it rises."]
    rains = [e for e in t2["events"] if e.startswith("Steam condenses")]
    assert boils == ["mariner boils 1 at spring; it rises."] * 2
    assert rains == ["Steam condenses at crown (+2)."]
    assert t2["nodes"]["crown"] == 3
    assert t2["winner"] is False


def _detector_board(mode: str) -> WaterGraph:
    """The drift board (k=2 vs k=3 wheels, pulse tanks, one xor, one
    level-1 latch with a head-blocked outflow). mode: 'chain0' adds a
    second B tank with the INLET hop (tb) created before the OUTLET hop
    (tb2): the leg chains same-tick, +0. 'lagB' creates tb2 FIRST: the
    leg delays B by one tick. 'lagA' delays A the same way. Both legs
    always reach X."""
    g = WaterGraph()
    g.add_node("srcA", elev=9, volume=12)
    g.add_node("srcB", elev=9, volume=12)
    g.add_node("VA", elev=8, kind="vortex")
    g.add_node("VB", elev=8, kind="vortex")
    g.add_node("tankA", elev=7)
    g.add_node("tankB", elev=7)
    g.add_node("sinkA", elev=1)
    g.add_node("sb1", elev=1)
    g.add_node("sb2", elev=1)
    g.add_node("X", elev=5, kind="xor")
    g.add_node("w", elev=0, kind="waste")
    g.add_node("L", elev=3, kind="latch", sill=1)
    g.add_node("drywell", elev=9)
    g.add_pipe("ia", "srcA", "VA", cap=1)
    g.add_pipe("xa", "VA", "tankA", cap=1)
    g.add_pipe("sa", "VA", "sinkA", cap=1)
    g.add_pipe("ib", "srcB", "VB", cap=1)
    g.add_pipe("xb", "VB", "tankB", cap=1)
    g.add_pipe("sb1", "VB", "sb1", cap=1)
    g.add_pipe("sb2", "VB", "sb2", cap=1)
    if mode == "lagB":
        g.add_node("tankB2", elev=6)
        g.add_pipe("tb2", "tankB2", "X", cap=1)
        g.add_pipe("tb", "tankB", "tankB2", cap=1)
        g.add_pipe("ta", "tankA", "X", cap=1)
    elif mode == "lagA":
        g.add_node("tankA2", elev=6)
        g.add_pipe("ta2", "tankA2", "X", cap=1)
        g.add_pipe("ta", "tankA", "tankA2", cap=1)
        g.add_pipe("tb", "tankB", "X", cap=1)
    elif mode == "chain0":
        g.add_node("tankB2", elev=6)
        g.add_pipe("tb", "tankB", "tankB2", cap=1)
        g.add_pipe("tb2", "tankB2", "X", cap=1)
        g.add_pipe("ta", "tankA", "X", cap=1)
    else:
        g.add_pipe("ta", "tankA", "X", cap=1)
        g.add_pipe("tb", "tankB", "X", cap=1)
    g.add_pipe("ox", "X", "L", cap=1)
    g.add_pipe("ol", "L", "drywell", cap=1)
    return g


def _run13(g: WaterGraph):
    verdicts, pools = [], []
    for _ in range(13):
        for e in g.tick():
            if "holds 2 below gate" in e:
                verdicts.append("hold")
            elif "STARVED" in e:
                verdicts.append("starve")
            elif "passes" in e:
                verdicts.append(e.split("(")[1].split()[0])  # the inlet pipe
        pools.append(g.volume("L"))
    return verdicts, pools


def test_pipe_order_flips_the_phase_without_changing_the_board():
    """The pipe-order phase flip (probe round 2, traced): chain0 (tb
    before tb2) and the zero-lag board have the SAME topology except
    one idle tank hop, and their drift signatures are byte-identical
    (the leg chains same-tick, +0): same verdict sequence, same pool
    table. lagB (tb2 created BEFORE tb) is the same board one dict
    order apart, and B's whole signature moves: passes at t5,t11 ->
    t3,t9, holds at t2,t8 -> t6,t12, first pool increment one tick
    earlier. The insertion order of plain pipes is clock wiring."""
    base_v, base_p = _run13(_detector_board("base"))
    c0_v, c0_p = _run13(_detector_board("chain0"))
    assert base_v == ["hold", "starve", "ta", "tb", "ta", "hold", "starve",
                      "ta", "tb", "ta"]
    # same TIMING, but each pass line names the leg's own outlet hop:
    # chain0's B side passes through tb2, so the raw names differ where
    # the ticks they fire on do not.
    c0_norm = [v.replace("tb2", "tb") for v in c0_v]
    assert c0_norm == base_v
    assert base_p == c0_p == [0, 0, 0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 6]
    lagb_v, lagb_p = _run13(_detector_board("lagB"))
    assert lagb_v == ["ta", "tb2", "ta", "hold", "starve", "ta", "tb2", "ta",
                      "hold", "starve"]
    assert lagb_p == [0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 6, 6, 6]


def test_the_drift_mass_forgets_the_offset_but_the_accrual_remembers_it():
    """The forgetful mass (probe round 2, traced): zero-lag, +0-chained,
    B-lagged (+1) and A-lagged (+1) boards all end the 13-tick window
    at the SAME totals - pool 6, waste 4, xor 0, conserved 24 - while
    their accrual tables differ tick by tick and only converge at the
    close: [0,0,0,1,...] zero-lag, [0,1,2,3,...] B-lagged, [0,1,2,2,...]
    A-lagged. The hold ticks name the offset (t2,t8 zero-lag; t6,t12
    B-lagged; t5,t11 A-lagged): which train lags is readable MID-WINDOW
    and only mid-window. Signed detection in this engine is a windowed
    read, never a completed total."""
    ends = []
    for mode, want_pool in (("base", [0, 0, 0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 6]),
                            ("chain0", [0, 0, 0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 6]),
                            ("lagB", [0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 6, 6, 6]),
                            ("lagA", [0, 1, 2, 2, 2, 2, 3, 4, 5, 5, 5, 5, 6])):
        g = _detector_board(mode)
        verdicts, pools = _run13(g)
        assert pools == want_pool, (mode, pools)
        assert g.volume("L") == 6 and g.volume("w") == 4
        assert g.volume("X") == 0 and g.volume("drywell") == 0
        assert g.volume("sinkA") == 6 and g.volume("sb1") == 4
        assert g.volume("sb2") == 4
        assert _total(g) == 24
        ends.append((mode, verdicts.count("hold")))
    assert ends == [("base", 2), ("chain0", 2), ("lagB", 2), ("lagA", 2)]
    g = _detector_board("lagA")
    verdicts, pools = _run13(g)
    assert pools == [0, 1, 2, 2, 2, 2, 3, 4, 5, 5, 5, 5, 6]
    assert verdicts == ["tb", "ta2", "hold", "starve", "ta2", "tb", "ta2",
                        "hold", "starve", "ta2"]
