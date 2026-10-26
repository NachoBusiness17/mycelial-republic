"""winding clock tests - the crown as a winded delay line, the band,
and the balloon (mariner cycle 11, 2026-10-17).

THE WINDING CLOCK, the cycle-10 receipt's self-chosen NEXT THREAD,
landed with ZERO engine bytes: every pin here composes kinds the
engine already has. Laws: (1) STORE-THEN-COUNT: one batch lift of N
into the sky, serve never started, and the governor wheel opens
EXACTLY N times before the park (the sky holds a number); (2) the
CLOCK CANNOT READ THE SHOVEL: a batch wind and a stream wind drive
byte-identical clock runs; (3) THE BAND: the sense leg's cap sets
where the surplus waits, never the wheel's rate (the ramp, the crown
hostage, and under wind THE BALLOON: the buffer lives inside the
latch pool); (4) THE WORLD-VERB WIND: staged world boils wind the
Mountain's win meter zero-latency, one merged rain line per beat,
winner on the crossing beat. Spec: mag/water_graph.py module
docstring, THE WINDING CLOCK block; receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261017_mariner.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _wheel_board(b: int, sill: int, cl_cap: int = 1) -> WaterGraph:
    """The governor wheel: waste basin of b units, cold crown, latch L,
    a sense leg cl (crown->L) at the given cap and a cap-1 return leg
    ol (L->waste)."""
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=b)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=sill)
    g.add_pipe("cl", "crown", "L", cap=cl_cap)
    g.add_pipe("ol", "L", "waste", cap=1)
    return g


OPEN1 = ["cl: 1 crown->L.", "Latch L opens (pool 1 >= level 1).",
         "ol: 1 to waste at waste."]


def test_the_sky_holds_a_number():
    """STORE-THEN-COUNT (probe round 1, traced for N 0, 1, 3, 5): one
    batch lift of N at the basin, serve never started. Tick 1 carries
    the merged condense +N plus the first wheel turn, ticks 2..N the
    bare three-line wheel, tick N+1 silent: the wheel opens EXACTLY N
    times, then parks at the birth state (waste B, crown 0, L 0).
    N=0 is the null wind: every tick silent from t1. The count is in
    the water, not the acts: mass B conserved at every tick."""
    for n, b in ((0, 8), (1, 8), (3, 8), (5, 8)):
        g = _wheel_board(b, sill=1)
        assert g.boil("waste", n) == n
        opens = 0
        for t in range(1, n + 3):
            evs = g.tick()
            opens += sum(1 for e in evs if e.startswith("Latch"))
            if t == 1 and n > 0:
                assert evs == [f"Steam condenses at crown (+{n})."] + OPEN1, (n, t, evs)
            elif 2 <= t <= n:
                assert evs == OPEN1, (n, t, evs)
            else:
                assert evs == [], (n, t, evs)
            assert _total(g) == b, (n, t)
        assert opens == n, (n, opens)
        assert g.volume("waste") == b and g.volume("crown") == 0
        assert g.volume("L") == 0


def test_the_clock_cannot_read_the_shovel():
    """The winding equivalence (probe round 1, traced): a batch wind of
    5 (one boil act) and a stream wind of 5 (five acts of 1, all
    before any tick) drive BYTE-IDENTICAL clock runs: every event list
    equal across eight ticks, same opens (5), same park. The shovel-
    economy law's whole-run form: the physics sees steam totals, never
    act counts, so no board can read how many shovels wound it."""
    traces = []
    for mode in ("batch", "stream"):
        g = _wheel_board(8, sill=1)
        if mode == "batch":
            g.boil("waste", 5)
        else:
            for _ in range(5):
                g.boil("waste", 1)
        trace = []
        for t in range(1, 9):
            evs = g.tick()
            trace.append(evs)
            assert _total(g) == 8, (mode, t)
        traces.append(trace)
        opens = sum(1 for evs in trace for e in evs if e.startswith("Latch"))
        assert opens == 5, (mode, opens)
        assert g.volume("waste") == 8 and g.volume("crown") == 0
        assert g.volume("L") == 0
    assert traces[0] == traces[1]


def test_the_band_unparks_the_crown_on_the_ramp():
    """THE BAND, steady serve (probe round 2, traced): cap-2 sense leg
    under a sill-2 latch vs the cap-1 control, B=4, prime 2, one
    shovel per open t1-t4. Steady shape identical from t2 (the same
    four-line wheel), but the RAMP differs: the wide leg carries the
    whole prime through on t1 (cl: 2, the latch opens on the FIRST
    tick, no HOLD line); the narrow leg can only move 1, so t1 is a
    HOLD and the ramp unit parks at the crown FOREVER (crown 1 at
    every tick t1-t5, a hostage the steady state never redeems; it
    spends only at t6, after the serve dies). The sump rides one
    lower on the narrow board: [1, 2] vs [2, 3]. The leg's cap sets
    where the surplus waits, never the wheel's rate."""
    wide = _wheel_board(4, sill=2, cl_cap=2)
    wide.boil("waste", 2)
    t1 = wide.tick()
    assert t1 == ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
                  "Latch L opens (pool 2 >= level 2).",
                  "ol: 1 to waste at waste."], t1
    assert wide.volume("waste") == 3 and wide.volume("crown") == 0
    assert wide.volume("L") == 1
    wide.boil("waste", 1)  # the t1 serve
    steady = ["Steam condenses at crown (+1).", "cl: 1 crown->L.",
              "Latch L opens (pool 2 >= level 2).", "ol: 1 to waste at waste."]
    for t in range(2, 9):
        evs = wide.tick()
        if 2 <= t <= 5:
            assert evs == steady, (t, evs)
            assert wide.volume("waste") == 3 and wide.volume("crown") == 0
        else:
            assert evs == [], (t, evs)
        assert _total(wide) == 4, t
        if t <= 4 and wide.volume("waste") > 0:
            wide.boil("waste", 1)
    assert wide.volume("waste") == 3 and wide.volume("L") == 1

    narrow = _wheel_board(4, sill=2, cl_cap=1)
    narrow.boil("waste", 2)
    t1 = narrow.tick()
    assert t1 == ["Steam condenses at crown (+2).",
                  "Latch L holds pool 1 below level 2; pooling."], t1
    assert narrow.volume("waste") == 2 and narrow.volume("crown") == 1
    assert narrow.volume("L") == 1
    narrow.boil("waste", 1)  # the t1 serve
    for t in range(2, 9):
        evs = narrow.tick()
        if 2 <= t <= 5:
            assert evs == steady, (t, evs)
            # the hostage: the ramp unit never leaves the crown while served
            assert narrow.volume("crown") == 1, (t, narrow.volume("crown"))
            assert narrow.volume("waste") == 2
        elif t == 6:
            # serve dead: the crown spends its hostage, no condense line
            assert evs == ["cl: 1 crown->L.",
                           "Latch L opens (pool 2 >= level 2).",
                           "ol: 1 to waste at waste."], (t, evs)
            assert narrow.volume("crown") == 0 and narrow.volume("waste") == 3
        else:
            assert evs == [], (t, evs)
        assert _total(narrow) == 4, t
        if t <= 4 and narrow.volume("waste") > 0:
            narrow.boil("waste", 1)
    assert narrow.volume("waste") == 3 and narrow.volume("L") == 1
    assert narrow.volume("crown") == 0


def test_the_balloon_holds_the_wind_inside_the_latch():
    """THE BALLOON (probe round 1, traced): the wide leg under a wind.
    B=6, sill 2, cl cap 2, prime 2, three batch-2 shovels (t1-t3).
    The leg carries the whole 2/tick wind, the crown NEVER parks
    (crown 0 at every tick), and the surplus accumulates INSIDE the
    latch: the pool balloons 1->2->3->4->5 while served (opens read
    pool 2..5), then with the sky dry the charged latch keeps opening
    on dry ticks and drains 4->1 through ol: the open run is UNBROKEN
    t1-t7 (no silent gap between serve-death and sky-spend), then
    silent, asleep at the sill-1 floor. 8 units wound, 7 opens, the
    8th unit sleeps in the pool: never opened, never lost. Control
    half: the cap-1 sill-1 board spends the same 8 units as 8 opens
    from crown stock (1->4) and parks at the birth state: the floor
    is the difference. Mass 6 conserved at every tick, both boards."""
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=6)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=2)
    g.add_pipe("cl", "crown", "L", cap=2)
    g.add_pipe("ol", "L", "waste", cap=1)
    g.boil("waste", 2)
    wants = {
        1: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 2 >= level 2).", "ol: 1 to waste at waste."],
        2: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 3 >= level 2).", "ol: 1 to waste at waste."],
        3: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 4 >= level 2).", "ol: 1 to waste at waste."],
        4: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 5 >= level 2).", "ol: 1 to waste at waste."],
        5: ["Latch L opens (pool 4 >= level 2).", "ol: 1 to waste at waste."],
        6: ["Latch L opens (pool 3 >= level 2).", "ol: 1 to waste at waste."],
        7: ["Latch L opens (pool 2 >= level 2).", "ol: 1 to waste at waste."],
        8: [], 9: [],
    }
    pools = {1: 1, 2: 2, 3: 3, 4: 4, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1}
    for t in range(1, 10):
        evs = g.tick()
        assert evs == wants[t], (t, evs)
        assert g.volume("crown") == 0, (t, g.volume("crown"))
        assert g.volume("L") == pools[t], (t, g.volume("L"))
        assert _total(g) == 6, t
        if t <= 3:
            take = 2 if g.volume("waste") >= 2 else g.volume("waste")
            assert take == 2, (t, take)
            g.boil("waste", 2)
    assert g.volume("waste") == 5 and g.volume("L") == 1
    opens = sum(1 for evs in wants.values() for e in evs if e.startswith("Latch"))
    assert opens == 7

    ctl = _wheel_board(6, sill=1)
    ctl.boil("waste", 2)
    ctl_opens = 0
    for t in range(1, 10):
        evs = ctl.tick()
        ctl_opens += sum(1 for e in evs if e.startswith("Latch"))
        assert _total(ctl) == 6, t
        if t <= 3:
            take = 2 if ctl.volume("waste") >= 2 else ctl.volume("waste")
            assert take == 2, (t, take)
            ctl.boil("waste", take)
        if 1 <= t <= 4:
            assert evs == ["Steam condenses at crown (+2)."] + OPEN1, (t, evs)
            assert ctl.volume("crown") == t, (t, ctl.volume("crown"))
        elif 5 <= t <= 8:
            assert evs == OPEN1, (t, evs)
        else:
            assert evs == [], (t, evs)
    assert ctl_opens == 8
    assert ctl.volume("waste") == 6 and ctl.volume("crown") == 0
    assert ctl.volume("L") == 0


def test_the_world_verb_wind_counts_to_the_win():
    """THE WORLD-VERB WIND (probe round 2, traced through
    MountainWorld.tick): the world verb layer winds the win meter
    zero-latency. Two same-beat staged pairs at the spring: each tick
    row carries two boil lines in arrival order and ONE merged rain
    line (+2) from the same beat, the crown reads 2 then 4, and the
    winner flips true on the crossing beat. The mountain's own
    gravity lines ride alongside every beat (p_drain, p_spring, the
    xor pass, p_out), and the board conserves 8 at every tick: the
    wind spends nothing, it only lifts."""
    from server.world import MountainWorld

    w = MountainWorld()
    w.register_session("s1", "mariner")
    for beat in range(2):
        for _ in range(2):
            ack = w.stage("s1", "boil", "spring")
            assert ack["op"] == "ack" and ack["applies_at_tick"] == beat + 1, ack
        t = w.tick()
        boils = [e for e in t["events"]
                 if e == "mariner boils 1 at spring; it rises."]
        rains = [e for e in t["events"] if e.startswith("Steam condenses")]
        assert boils == ["mariner boils 1 at spring; it rises."] * 2, t
        assert rains == ["Steam condenses at crown (+2)."], t
        assert t["nodes"]["crown"] == 2 * (beat + 1), t
        assert t["winner"] is (beat == 1), t
        assert "p_drain: 1 to waste at waste." in t["events"], t
        assert "Junction gate1 passes (p_spring sole inlet)." in t["events"], t
        assert sum(t["nodes"].values()) == 8, t
