"""reading glass tests - the dropper gauge, the park's forgetfulness,
and the balloon's ceiling (mariner cycle 12, 2026-10-18).

THE READING GLASS, the cycle-11 receipt's self-chosen NEXT THREAD,
landed with ZERO engine bytes: every pin here composes kinds the
engine already has. Laws: (1) THE DROPPER GAUGE: a cap-1 tap leg
from a ballooned pool into a reader latch (sill 1) with a counter
sink; the tap clamps the balloon into a wire when open from birth,
and after a stored wind it reads the store minus the floor; (2) THE
2-TICK LATENCY: a gate's outflow into a gate is a committed landing,
so the reader's verdict never sees same-tick inflow: one tick per
gate hop, and the reader outlives the wind by one tick; (3) THE PARK
FORGETS THE STORAGE SITE: the cap-1 hostage board and the cap-2
balloon board end identical with the same open count while their
accrual tables are disjoint (cycle 9's windowed law, fed); (4) THE
CEILING IS THE BALLOON'S ONLY PORT: a latch pool at VOLUME_SAT
absorbs with the named amount and drains straight back down; (5)
THE READ IS A DRAIN: uphill and equal taps move zero forever.
Spec: mag/water_graph.py module docstring, THE READING GLASS block;
receipt watch/inbox/mates_leave_protocol/receipts/
receipt_20261018_mariner.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import VOLUME_SAT, WaterGraph  # noqa: E402


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _gauge_board(b: int, sill: int, cl_cap: int, tap_open: bool,
                 ol_open: bool = True) -> WaterGraph:
    """The governor wheel plus a gauge: waste basin of b, cold crown,
    balloon latch L, reader latch R (sill 1), counter sink; legs cl
    (crown->L), ol (L->waste drain), tap (L->R), ro (R->sink)."""
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=b)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=sill)
    g.add_node("R", elev=2, kind="latch", sill=1)
    g.add_node("sink", elev=1)
    g.add_pipe("cl", "crown", "L", cap=cl_cap)
    g.add_pipe("ol", "L", "waste", cap=1, open_=ol_open)
    g.add_pipe("tap", "L", "R", cap=1, open_=tap_open)
    g.add_pipe("ro", "R", "sink", cap=1)
    return g


def test_the_live_wire_clamps_the_balloon():
    """THE GAUGE CLAMPS THE BALLOON (probe A1, traced): tap open from
    birth, drain open, cycle-11 balloon wind (B=6, sill 2, cap-2 leg,
    prime 2, three 2-shovels). The integrator becomes a pass-through
    wire: the pool rides [2 at verdict, 0 after outflow] on every
    served tick, the crown never parks, and the tap passes exactly
    1/tick (the wind's balance over the cap-1 drain). The reader R
    lags one tick (its verdict never sees same-tick inflow): t1's tap
    unit sleeps in R, the sink counts 1/tick from t2, and on t5, the
    first silent tick, R drains its afterbeat (sink 4). End: waste 2,
    sink 4, L 0, R 0: 8 wound units split 4 drain / 4 tap, mass 6
    conserved at every tick."""
    g = _gauge_board(6, sill=2, cl_cap=2, tap_open=True)
    g.boil("waste", 2)
    served = ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
              "Latch L opens (pool 2 >= level 2)."]
    for t in range(1, 8):
        evs = g.tick()
        if t == 1:
            assert evs == served + ["ol: 1 to waste at waste.",
                                    "tap: 1 L->R."], (t, evs)
            assert g.volume("waste") == 5 and g.volume("L") == 0
            assert g.volume("R") == 1 and g.volume("sink") == 0
        elif t <= 4:
            assert evs == served + ["Latch R opens (pool 1 >= level 1).",
                                    "ol: 1 to waste at waste.",
                                    "tap: 1 L->R.", "ro: 1 R->sink."], (t, evs)
            assert g.volume("sink") == t - 1, (t, g.volume("sink"))
        elif t == 5:
            assert evs == ["Latch R opens (pool 1 >= level 1).",
                           "ro: 1 R->sink."], (t, evs)
            assert g.volume("sink") == 4
        else:
            assert evs == [], (t, evs)
        assert _total(g) == 6, t
        assert g.volume("crown") == 0, t
        if t <= 3:
            assert g.boil("waste", min(2, g.volume("waste"))) == 2, t
    assert g.volume("waste") == 2 and g.volume("L") == 0
    assert g.volume("R") == 0 and g.volume("sink") == 4


def test_the_pure_gauge_reads_wind_minus_floor():
    """THE PURE GAUGE (probe A2, traced): same wind but the drain ol
    is shut from birth. The store pools net +1/tick (2 in through cl,
    1 out through the live tap), the reader relays 1/tick one tick
    behind, and when the sky dies the charged balloon keeps feeding
    the tap on dry ticks (opens read pool 3 then 2) until the sill-2
    floor sleeps: L parks at 1, the sink ends at 5 of the 6 wound
    units (wind minus the floor). Mass 6 conserved at every tick."""
    g = _gauge_board(6, sill=2, cl_cap=2, tap_open=True, ol_open=False)
    g.boil("waste", 2)
    wants = {
        1: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 2 >= level 2).", "tap: 1 L->R."],
        2: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 3 >= level 2).",
            "Latch R opens (pool 1 >= level 1).", "tap: 1 L->R.",
            "ro: 1 R->sink."],
        3: ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
            "Latch L opens (pool 4 >= level 2).",
            "Latch R opens (pool 1 >= level 1).", "tap: 1 L->R.",
            "ro: 1 R->sink."],
        4: ["Latch L opens (pool 3 >= level 2).",
            "Latch R opens (pool 1 >= level 1).", "tap: 1 L->R.",
            "ro: 1 R->sink."],
        5: ["Latch L opens (pool 2 >= level 2).",
            "Latch R opens (pool 1 >= level 1).", "tap: 1 L->R.",
            "ro: 1 R->sink."],
        6: ["Latch R opens (pool 1 >= level 1).", "ro: 1 R->sink."],
        7: [], 8: [], 9: [],
    }
    pools = {1: 1, 2: 2, 3: 3, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}
    sinks = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 5, 8: 5, 9: 5}
    for t in range(1, 10):
        evs = g.tick()
        assert evs == wants[t], (t, evs)
        assert g.volume("L") == pools[t], (t, g.volume("L"))
        assert g.volume("sink") == sinks[t], (t, g.volume("sink"))
        assert _total(g) == 6, t
        if t <= 3:
            take = min(2, g.volume("waste"))
            assert g.boil("waste", take) == take, t
    assert g.volume("waste") == 0 and g.volume("L") == 1
    assert g.volume("sink") == 5


def test_the_stored_read_and_its_floor():
    """THE STORED READ (probes B and B2, traced): wind 6 into a pure
    store (both ol and tap shut: L opens t1-t4, the t4 open the
    memory law's dry-tick discharge with no outflow to move), park at
    pool 6, then open the tap. The tap emits 1/tick while the pool
    stays at or above level 2 (t5-t9, five units), R relays each unit
    one tick behind (first ro at t6), the sink ends at 5, and the
    floor sleeps forever: a stored 6 reads as 5 at sill 2. Second
    half: the same wind into a sill-1 balloon reads the FULL 6 (opens
    t5-t10, pool to 0, sink 6): the resolution is the balloon's own
    sill, never the tap's. Mass 6 conserved throughout, both boards."""
    g = _gauge_board(6, sill=2, cl_cap=2, tap_open=False, ol_open=False)
    g.boil("waste", 2)
    for t in range(1, 5):
        evs = g.tick()
        if t <= 3:
            assert evs == [f"Steam condenses at crown (+2).",
                           f"cl: 2 crown->L.",
                           f"Latch L opens (pool {2 * t} >= level 2)."], (t, evs)
            take = min(2, g.volume("waste"))
            assert g.boil("waste", take) == take, t
        else:
            assert evs == ["Latch L opens (pool 6 >= level 2)."], (t, evs)
        assert _total(g) == 6, t
    assert g.volume("L") == 6
    g.open("tap")
    for t in range(5, 11):
        evs = g.tick()
        if t == 5:
            assert evs == ["Latch L opens (pool 6 >= level 2).",
                           "tap: 1 L->R."], (t, evs)
        elif t <= 9:
            assert evs == [f"Latch L opens (pool {11 - t} >= level 2).",
                           "Latch R opens (pool 1 >= level 1).",
                           "tap: 1 L->R.", "ro: 1 R->sink."], (t, evs)
            assert g.volume("sink") == t - 5, (t, g.volume("sink"))
        else:
            assert evs == ["Latch R opens (pool 1 >= level 1).",
                           "ro: 1 R->sink."], (t, evs)
            assert g.volume("sink") == 5
        assert _total(g) == 6, t
    for t in range(11, 15):
        assert g.tick() == [], t
    assert g.volume("L") == 1 and g.volume("sink") == 5

    full = _gauge_board(6, sill=1, cl_cap=2, tap_open=False, ol_open=False)
    full.boil("waste", 2)
    for t in range(1, 5):
        full.tick()
        if t <= 3:
            take = min(2, full.volume("waste"))
            assert full.boil("waste", take) == take, t
    assert full.volume("L") == 6
    full.open("tap")
    sink_total = 0
    for t in range(5, 13):
        evs = full.tick()
        sink_total += sum(1 for e in evs if e.startswith("ro:"))
        assert _total(full) == 6, t
        if 5 <= t <= 10:
            assert evs[0] == f"Latch L opens (pool {11 - t} >= level 1).", (t, evs)
        elif t == 11:
            assert evs == ["Latch R opens (pool 1 >= level 1).",
                           "ro: 1 R->sink."], (t, evs)
        else:
            assert evs == [], (t, evs)
    assert full.volume("L") == 0 and full.volume("sink") == 6
    assert sink_total == 6


def test_the_park_forgets_the_storage_site():
    """THE PARK FORGETS THE STORAGE SITE (probes C1 and C2, traced):
    B=8, sill 2, prime 2, three 2-shovels; the cap-1 leg parks the
    ramp unit at the crown (the cycle-11 hostage), the cap-2 leg
    balloons the pool. End states IDENTICAL (waste 7, crown 0, pool
    1), open counts IDENTICAL (7: the narrow board's t1 HOLD line is
    not an open), yet the accrual tables are disjoint: crown stock
    1,2,3,4,3,2,1,0 vs 0 forever, pool flat 1 vs 1,2,3,4,3,2,1,
    waste tables differ t1-t7. The storage site (sky vs pool) is
    unreadable at the park and readable only mid-window; the wide
    board also parks one tick sooner (silent from t8 vs t9). Mass 8
    conserved at every tick, both boards."""
    def board(cl_cap: int) -> WaterGraph:
        g = WaterGraph()
        g.add_node("waste", elev=0, kind="waste", volume=8)
        g.add_node("crown", elev=10, kind="cold")
        g.add_node("L", elev=4, kind="latch", sill=2)
        g.add_pipe("cl", "crown", "L", cap=cl_cap)
        g.add_pipe("ol", "L", "waste", cap=1)
        return g

    narrow = board(1)
    narrow.boil("waste", 2)
    wide = board(2)
    wide.boil("waste", 2)
    n_pool, n_crown, n_waste, n_opens = [], [], [], 0
    w_pool, w_crown, w_waste, w_opens = [], [], [], 0
    n_first, w_first = None, None
    for t in range(1, 10):
        ne = narrow.tick()
        we = wide.tick()
        n_opens += sum(1 for e in ne if e.startswith("Latch L opens"))
        w_opens += sum(1 for e in we if e.startswith("Latch L opens"))
        n_pool.append(narrow.volume("L"))
        n_crown.append(narrow.volume("crown"))
        n_waste.append(narrow.volume("waste"))
        w_pool.append(wide.volume("L"))
        w_crown.append(wide.volume("crown"))
        w_waste.append(wide.volume("waste"))
        if n_first is None and ne:
            n_first = ne
        if w_first is None and we:
            w_first = we
        assert _total(narrow) == 8 and _total(wide) == 8, t
        if t <= 3:
            assert narrow.boil("waste", min(2, narrow.volume("waste"))) == 2, t
            assert wide.boil("waste", min(2, wide.volume("waste"))) == 2, t
    assert n_first == ["Steam condenses at crown (+2).",
                       "Latch L holds pool 1 below level 2; pooling."], n_first
    assert w_first == ["Steam condenses at crown (+2).", "cl: 2 crown->L.",
                       "Latch L opens (pool 2 >= level 2).",
                       "ol: 1 to waste at waste."], w_first
    assert (narrow.volume("waste"), narrow.volume("crown"),
            narrow.volume("L")) == (7, 0, 1)
    assert (wide.volume("waste"), wide.volume("crown"),
            wide.volume("L")) == (7, 0, 1)
    assert n_opens == 7 and w_opens == 7
    assert n_pool == [1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert w_pool == [1, 2, 3, 4, 3, 2, 1, 1, 1]
    assert n_crown == [1, 2, 3, 4, 3, 2, 1, 0, 0]
    assert w_crown == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert n_waste == [6, 5, 4, 3, 4, 5, 6, 7, 7]
    assert w_waste == [7, 6, 5, 4, 5, 6, 7, 7, 7]
    assert n_pool != w_pool and n_crown != w_crown and n_waste != w_waste


def test_the_ceiling_is_the_balloons_only_port():
    """THE CEILING IS THE BALLOON'S ONLY PORT (probes D1 and D2,
    traced): a latch pool grown to VOLUME_SAT minus 1 absorbs the
    next 2-unit inflow at the ceiling: the SATURATES line names
    exactly 1 absorbed at 9223372036586340, the verdict still passes
    (the open line carries the 16-digit pool), and the cap-1 drain
    plus the cap-1 tap pull 2/tick off the ceiling while R relays one
    tick behind. Mass loss across the window is exactly the named
    absorbed unit: a clamp, not a freeze. Second half: the same
    ceiling under a bare cap-1 drain reads the pool straight down
    (SAT, SAT-1, SAT-2): no stuck state, no wrap."""
    g = WaterGraph()
    g.add_node("feeder", elev=9, volume=2)
    g.add_node("L", elev=4, kind="latch", sill=2, volume=VOLUME_SAT - 1)
    g.add_node("R", elev=2, kind="latch", sill=1)
    g.add_node("sink", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("fd", "feeder", "L", cap=2)
    g.add_pipe("ol", "L", "waste", cap=1)
    g.add_pipe("tap", "L", "R", cap=1)
    g.add_pipe("ro", "R", "sink", cap=1)
    before = _total(g)
    t1 = g.tick()
    assert t1 == [f"Node L SATURATES: 1 absorbed at the volume ceiling "
                  f"{VOLUME_SAT} (int64 depth domain, R8).",
                  "fd: 2 feeder->L.",
                  f"Latch L opens (pool {VOLUME_SAT} >= level 2).",
                  "ol: 1 to waste at waste.", "tap: 1 L->R."], t1
    assert g.volume("L") == VOLUME_SAT - 2
    assert g.volume("R") == 1 and g.volume("sink") == 0
    assert _total(g) == VOLUME_SAT
    t2 = g.tick()
    assert t2 == [f"Latch L opens (pool {VOLUME_SAT - 2} >= level 2).",
                  "Latch R opens (pool 1 >= level 1).",
                  "ol: 1 to waste at waste.", "tap: 1 L->R.",
                  "ro: 1 R->sink."], t2
    assert g.volume("sink") == 1
    assert _total(g) == VOLUME_SAT
    assert before - _total(g) == 1
    for t in range(3, 6):
        evs = g.tick()
        assert evs == [f"Latch L opens (pool {g.volume('L') + 2} >= level 2).",
                       "Latch R opens (pool 1 >= level 1).",
                       "ol: 1 to waste at waste.", "tap: 1 L->R.",
                       "ro: 1 R->sink."], (t, evs)
        assert _total(g) == VOLUME_SAT, t
    assert g.volume("L") == VOLUME_SAT - 10

    bare = WaterGraph()
    bare.add_node("L", elev=4, kind="latch", sill=2, volume=VOLUME_SAT)
    bare.add_node("waste", elev=0, kind="waste")
    bare.add_pipe("ol", "L", "waste", cap=1)
    for t, drop in ((1, 0), (2, 1)):
        evs = bare.tick()
        assert evs == [f"Latch L opens (pool {VOLUME_SAT - drop} >= level 2).",
                       "ol: 1 to waste at waste."], (t, evs)
        assert _total(bare) == VOLUME_SAT, t
    assert bare.volume("L") == VOLUME_SAT - 2


def test_the_read_is_a_drain():
    """THE READ IS A DRAIN (probe E, traced): uphill and
    equal-elevation taps move zero forever (no events name them), the
    downhill tap moves 1/tick while the verdict passes: every moving
    tap needs head (src.elev strictly above dst.elev), so NO
    non-destructive read exists in the engine; the head law is the
    privacy law, and a tap always consumes its specimen down toward
    the floor."""
    g = WaterGraph()
    g.add_node("pool", elev=4, kind="latch", sill=2, volume=6)
    g.add_node("high", elev=9)
    g.add_node("equal", elev=4)
    g.add_node("low", elev=1)
    g.add_pipe("up", "pool", "high", cap=1)
    g.add_pipe("eq", "pool", "equal", cap=1)
    g.add_pipe("dn", "pool", "low", cap=1)
    t1 = g.tick()
    assert t1 == ["Latch pool opens (pool 6 >= level 2).",
                  "dn: 1 pool->low."], t1
    assert g.volume("pool") == 5 and g.volume("high") == 0
    assert g.volume("equal") == 0 and g.volume("low") == 1
    assert _total(g) == 6
    t2 = g.tick()
    assert t2 == ["Latch pool opens (pool 5 >= level 2).",
                  "dn: 1 pool->low."], t2
    assert g.volume("pool") == 4 and g.volume("high") == 0
    assert g.volume("equal") == 0 and g.volume("low") == 2
    assert _total(g) == 6
