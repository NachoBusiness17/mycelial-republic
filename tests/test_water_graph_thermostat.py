"""thermostat tests - the closed weather loop, the governor wheel,
and the recirculation lap (mariner cycle 10, 2026-10-16).

THE THERMOSTAT, the cycle-9 receipt's self-chosen NEXT THREAD, landed
with ZERO engine bytes: every pin here composes kinds the engine
already has. The loop is drain -> waste -> boil -> crown -> receiver
-> drain and its only input is the operator's shovel. Laws: (1) a
governor starts only on an unconditioned PRIME (the latch cannot open
before the first lift); (2) the SERVE law: one shovel per open line
holds the sump at a level, spends acts not water, and parks one
momentum tick after the last shovel at the birth state; (3) the
SETPOINT law: the sill is the dial and the parked latch sleeps
charged, so a half prime restarts the wheel mid-phase; (4) the wheel
rate is the SENSE LEG's cap: over-shoveling pools the surplus at the
crown and the sky spends itself last after the shovel dies; (5) rain
charges a latch through a crown drain (the cycle-7 residual g,
closed); (6) the recirculation lap is PIPE ORDER: one tick (+0 chain)
or two ticks (+1 rest), one act per lap either way. Spec:
mag/water_graph.py module docstring, THE THERMOSTAT block; receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261016_mariner.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _wheel_board(b: int, sill: int) -> WaterGraph:
    """The governor wheel: waste basin of b units, cold crown, latch L,
    a cap-1 sense leg cl (crown->L) and a cap-1 return leg ol (L->waste)."""
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=b)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=sill)
    g.add_pipe("cl", "crown", "L", cap=1)
    g.add_pipe("ol", "L", "waste", cap=1)
    return g


SERVE = ["Steam condenses at crown (+1).", "cl: 1 crown->L.",
         "Latch L opens (pool 1 >= level 1).", "ol: 1 to waste at waste."]


def test_a_governor_starts_only_on_an_unconditioned_prime():
    """The prime law (probe round 1 dead end, pinned): a serve loop that
    waits for a "Latch L opens" line BEFORE the first shovel never
    starts: the latch has no inflow until something lifts, so ticks 1-3
    are three empty lists. The first UNCONDITIONED act (the prime) is
    the ignition: tick 4 runs the full four-line wheel on the primed
    steam. Board: waste 3, sill 1."""
    g = _wheel_board(3, sill=1)
    for _ in range(3):
        assert g.tick() == [], "no prime, no open, no wheel"
    assert g.volume("L") == 0 and g.volume("crown") == 0
    assert _total(g) == 3
    g.boil("waste", 1)
    assert g.tick() == SERVE
    assert g.volume("L") == 0 and g.volume("crown") == 0
    assert g.volume("waste") == 3  # primed 1 out, return leg paid 1 back
    assert _total(g) == 3


def test_the_serve_law_holds_the_sump_and_parks_at_the_birth_state():
    """The serve law + the momentum tick + the birth-state park (probe
    W1, traced): prime 1, then serve one shovel per open for ticks 1-5.
    Every served tick is the same four-line list, the sump rides [2, 3]
    (state after each tick+shovel: waste 2, steam 1), and the total
    never leaves 3: the steady state HOLDS A LEVEL and spends acts,
    not water. Serve window closes after t5: t6 still turns the wheel
    (the t5 shovel's steam is in flight: the MOMENTUM tick) and leaves
    the sump at 3; t7-t8 are silent. Parked state waste 3, crown 0,
    L 0: byte-equal to the birth state. Acts == opens == turns == 6
    (prime + 5 served, t1-t6 opens)."""
    g = _wheel_board(3, sill=1)
    g.boil("waste", 1)  # the prime
    acts, opens = 1, 0
    for t in range(1, 9):
        evs = g.tick()
        served = ""
        if t <= 5:
            assert evs == SERVE, (t, evs)
            opens += 1
            if g.volume("waste") > 0:
                g.boil("waste", 1)
                acts += 1
                served = " SHOVEL"
        elif t == 6:
            assert evs == SERVE, (t, evs)  # the momentum tick
            opens += 1
        else:
            assert evs == [], (t, evs)  # the silent park
        assert _total(g) == 3, (t, served)
        if t <= 5:
            assert g.volume("waste") == 2 and g.nodes["waste"].steam == 1
    assert g.volume("waste") == 3 and g.nodes["waste"].steam == 0
    assert g.volume("crown") == 0 and g.volume("L") == 0
    assert acts == 6 and opens == 6


def test_the_sill_sets_the_draw_and_the_park_sleeps_charged():
    """The setpoint law (probe S2, traced): B=3, sill 2, prime 2. The
    wheel starts one tick later than sill 1 (the latch fills to the
    sill first: t1 is condense +2 then a HOLD at pool 1 while the
    crown keeps the second unit), and the sump now rides [1, 2]
    instead of [2, 3]: the sill is the dial, each notch drinks the
    sump one unit lower. Stop serving after t5: t6 is the momentum
    tick, t7-t8 silent, and the park SLEEPS CHARGED (waste 2, crown 0,
    L 1: pool sill-1, the memory law at rest). A HALF prime (the
    missing residual, 1 unit) restarts the wheel at full period on
    the very next tick (t9: condense, cl, OPEN at pool 2, ol): the
    residual is the phase. Total 3 at every tick."""
    g = _wheel_board(3, sill=2)
    g.boil("waste", 2)  # prime == the sill
    for t in range(1, 9):
        evs = g.tick()
        if t == 1:
            assert evs == ["Steam condenses at crown (+2).",
                           "Latch L holds pool 1 below level 2; pooling."], evs
            assert g.volume("crown") == 1 and g.volume("L") == 1
            continue
        if 2 <= t <= 6:
            want = ["cl: 1 crown->L.", "Latch L opens (pool 2 >= level 2).",
                    "ol: 1 to waste at waste."]
            if t >= 3:
                want.insert(0, "Steam condenses at crown (+1).")
            assert evs == want, (t, evs)
            if t <= 5 and g.volume("waste") > 0:
                g.boil("waste", 1)
            assert _total(g) == 3
            if 3 <= t <= 5:
                assert g.volume("waste") == 1 and g.nodes["waste"].steam == 1
        else:
            assert evs == [], (t, evs)
    assert g.volume("waste") == 2 and g.volume("L") == 1
    assert g.volume("crown") == 0
    # the half prime: the parked latch is one unit below its level
    g.boil("waste", 1)
    evs = g.tick()
    assert evs == ["Steam condenses at crown (+1).", "cl: 1 crown->L.",
                   "Latch L opens (pool 2 >= level 2).",
                   "ol: 1 to waste at waste."], evs
    g.boil("waste", 1)  # serve it: the wheel is back at full period
    evs = g.tick()
    assert evs == ["Steam condenses at crown (+1).", "cl: 1 crown->L.",
                   "Latch L opens (pool 2 >= level 2).",
                   "ol: 1 to waste at waste."], evs
    g.boil("waste", 1)  # serve this open too, then read the steady state
    assert g.volume("waste") == 1 and g.nodes["waste"].steam == 1
    assert _total(g) == 3


def test_the_wheel_rate_is_the_sense_leg_and_the_sky_spends_itself_last():
    """The sense-leg law (probe W2, traced): B=5, sill 1, prime 2, then
    over-shovel TWO units per open for six ticks. The wheel NEVER
    speeds up: every served tick still carries exactly one cl unit
    (cap 1) and one open, so the surplus pools at the cold crown
    (crown 1->2->3->4 over t1-t4, the free buffer) while the sump
    drains 3->2->1->0. At sump 0 the serve degrades to one shovel and
    the circuit converges to the honest wheel (t5-t6: shovel 1 ==
    return 1, sump riding 0/1: pure recirculation through an empty
    sump). Serve window closes after t6: t7 is the last condense tick,
    then t8-t11 the wheel turns FOUR more times on the crown's stored
    four units with zero condense lines (the sky spends itself last,
    one momentum tick per stored unit), t12-t13 are silent, and the
    final state is the birth state (waste 5, crown 0, L 0): the
    over-shoveled board loses nothing. Total 5 at every tick."""
    g = _wheel_board(5, sill=1)
    g.boil("waste", 2)  # prime
    open1 = ["cl: 1 crown->L.", "Latch L opens (pool 1 >= level 1).",
             "ol: 1 to waste at waste."]
    # condense counts: the prime's 2, then the serves' 2 per tick while
    # the batch shovel holds (t2-t4), then 1 per tick once the sump
    # degrades the serve (t5-t7), then the sky is dry (t8 on)
    serve2 = ["Steam condenses at crown (+2)."] + open1
    serve1 = ["Steam condenses at crown (+1)."] + open1
    wants = {
        1: serve2, 2: serve2, 3: serve2, 4: serve2, 5: serve1, 6: serve1,
        7: serve1, 8: open1, 9: open1, 10: open1, 11: open1, 12: [], 13: [],
    }
    crowns = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4,
              8: 3, 9: 2, 10: 1, 11: 0, 12: 0, 13: 0}
    # post-tick, pre-serve sump levels (the probe's printed states are
    # post-serve: subtract each tick's shovel to compare)
    wastes = {1: 4, 2: 3, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1,
              8: 2, 9: 3, 10: 4, 11: 5, 12: 5, 13: 5}
    for t in range(1, 14):
        evs = g.tick()
        assert evs == wants[t], (t, evs)
        assert g.volume("crown") == crowns[t], (t, g.volume("crown"))
        assert g.volume("waste") == wastes[t], (t, g.volume("waste"))
        assert _total(g) == 5, t
        if t <= 6:
            take = 2 if g.volume("waste") >= 2 else g.volume("waste")
            if take:
                g.boil("waste", take)
    assert g.volume("waste") == 5 and g.volume("crown") == 0
    assert g.volume("L") == 0


def test_rain_charges_the_latch_through_a_crown_drain():
    """Rain as a latch input: the cycle-7 residual g, CLOSED (probe B,
    traced). A cold crown sits ABOVE a level-2 latch; one batch lift of
    3 at the basin. t1: all 3 condense at the crown (the latch is not
    cold: the sky never lands in it directly), the crown's drain probes
    the gate deferred and the latch HOLDS pool 1 (the held inlet gets
    no provenance line: the cycle-3 residual, still open). t2 and t3:
    one drain unit each, the latch opens at pool 2 and discharges 1 to
    the sink each time. t4-t5: silent; the latch keeps its residual 1
    (the level-minus-1 hysteresis floor; a latch never STARVED-spills).
    End: basin 0, crown 0, L 1, lsnk 2, conserved 3."""
    g = WaterGraph()
    g.add_node("basin", elev=0, volume=3)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=2)
    g.add_node("lsnk", elev=1)
    g.add_pipe("cd", "crown", "L", cap=1)
    g.add_pipe("ol", "L", "lsnk", cap=1)
    assert g.boil("basin", 3) == 3
    assert g.tick() == ["Steam condenses at crown (+3).",
                        "Latch L holds pool 1 below level 2; pooling."]
    assert g.volume("crown") == 2 and g.volume("L") == 1
    assert g.nodes["basin"].steam == 0 and g.volume("lsnk") == 0
    open3 = ["cd: 1 crown->L.", "Latch L opens (pool 2 >= level 2).",
             "ol: 1 L->lsnk."]
    assert g.tick() == open3
    assert g.tick() == open3
    assert g.tick() == [] and g.tick() == []
    assert g.volume("basin") == 0 and g.volume("crown") == 0
    assert g.volume("L") == 1 and g.volume("lsnk") == 2
    assert _total(g) == 3


def test_the_recirculation_lap_is_pipe_order():
    """The lap is pipe order (probes R + R3, traced). Board: receiver
    rcv (elev 5), cold crown (elev 10), waste; legs cd (crown->rcv)
    and dr (rcv->waste). +0 BOARD (cd created first): after the seeded
    rider's drain tick, each lap is ONE tick: condense, cd lands the
    rider, dr chains it straight to waste the same tick. One act +
    one tick per lap for three laps, waste constant 1, conserved 1 at
    every boundary. +1 BOARD (dr created first, same topology one
    dict order apart): the rider RESTS at rcv for a tick (the drain
    already ran when the rain landed), so a lap is TWO ticks and the
    waste oscillates 1/0. Same act per lap, same conservation: the
    lap cadence is clock wiring, not physics."""
    g = WaterGraph()
    g.add_node("rcv", elev=5, volume=1)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("cd", "crown", "rcv", cap=1)
    g.add_pipe("dr", "rcv", "waste", cap=1)
    assert g.tick() == ["dr: 1 to waste at waste."]
    lap = ["Steam condenses at crown (+1).", "cd: 1 crown->rcv.",
           "dr: 1 to waste at waste."]
    for _ in range(3):
        g.boil("waste", 1)
        assert g.tick() == lap
        assert g.volume("rcv") == 0 and g.volume("crown") == 0
        assert g.volume("waste") == 1
        assert _total(g) == 1
    h = WaterGraph()
    h.add_node("rcv", elev=5, volume=1)
    h.add_node("crown", elev=10, kind="cold")
    h.add_node("waste", elev=0, kind="waste")
    h.add_pipe("dr", "rcv", "waste", cap=1)
    h.add_pipe("cd", "crown", "rcv", cap=1)
    assert h.tick() == ["dr: 1 to waste at waste."]
    for _ in range(2):
        h.boil("waste", 1)
        assert h.tick() == ["Steam condenses at crown (+1).",
                            "cd: 1 crown->rcv."]
        assert h.volume("rcv") == 1 and h.volume("waste") == 0
        assert h.tick() == ["dr: 1 to waste at waste."]
        assert h.volume("rcv") == 0 and h.volume("waste") == 1
        assert _total(h) == 1
