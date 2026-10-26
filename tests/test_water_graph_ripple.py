"""ripple counter + difference detector tests - compositions over the
rotor and gate kinds (mariner cycle 6, 2026-10-13).

The cycle-5 receipt's self-chosen NEXT THREAD, landed with ZERO engine
bytes: every pin here composes kinds the engine already has. Three laws:
(1) a chain of k=2 vortices is a binary ripple counter whose rotors read
the tick count in binary and whose digit sinks hold the divided streams,
the count surviving a dry gap byte-exactly; (2) a rotor feeding a gate
directly can never pass that gate's verdict (committed landings never
join the deferred-inlet verdict) and the plain pulse tank is the
rotor-to-gate adapter; (3) two tanked wheels into one xor into one latch
make a difference detector: the latch's pool accumulates exactly the
ticks where exactly one wheel delivered. Spec: mag/water_graph.py module
docstring, RIPPLE COUNTER + DIFFERENCE DETECTOR block; receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261013_mariner.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _counter_board() -> WaterGraph:
    g = WaterGraph()
    g.add_node("src", elev=9, volume=13)
    g.add_node("V0", elev=8, kind="vortex")
    g.add_node("d0", elev=1)
    g.add_node("V1", elev=7, kind="vortex")
    g.add_node("d1", elev=1)
    g.add_node("V2", elev=6, kind="vortex")
    g.add_node("d2", elev=1)
    g.add_node("V3", elev=5, kind="vortex")
    g.add_node("d3", elev=1)
    g.add_node("tail", elev=1)
    g.add_pipe("in", "src", "V0", cap=1)
    g.add_pipe("a0", "V0", "d0", cap=1)
    g.add_pipe("b0", "V0", "V1", cap=1)
    g.add_pipe("a1", "V1", "d1", cap=1)
    g.add_pipe("b1", "V1", "V2", cap=1)
    g.add_pipe("a2", "V2", "d2", cap=1)
    g.add_pipe("b2", "V2", "V3", cap=1)
    g.add_pipe("a3", "V3", "d3", cap=1)
    g.add_pipe("b3", "V3", "tail", cap=1)
    return g


def test_ripple_chain_of_k2_rotors_reads_its_count_in_binary():
    """Four k=2 vortices, each stage's first outlet a digit sink and its
    second outlet the next stage, fed 1/tick from a 13-unit source
    (probe P1, traced). The marks ARE binary counting: a0 passes on the
    odd ticks, and every tick whose new count ends in trailing ones
    hands the carry up (t2: b0,a1; t4: b0,b1,a2; t8: the full four-stage
    cascade b0,b1,b2,a3 on 7+1=8; t12: b0,b1,a2 on 11+1=12). After 13
    ticks the rotors read rot 1,1,0,1 = 1101 = 13 (rot_i = bit i of the
    tick count) and the digit sinks hold the divided streams:
    d0 7 (every odd tick), d1 3 (t2,6,10), d2 2 (t4,12), d3 1 (t8).
    Conserved 13, every rotor pool empty: the graph is a counter whose
    register is the rotor positions."""
    g = _counter_board()
    marks = []
    for _ in range(13):
        for e in g.tick():
            if not e.startswith("in:"):
                marks.append((g.tick_count, e))
    assert marks == [
        (1, "a0: 1 V0->d0."),
        (2, "b0: 1 V0->V1."), (2, "a1: 1 V1->d1."),
        (3, "a0: 1 V0->d0."),
        (4, "b0: 1 V0->V1."), (4, "b1: 1 V1->V2."), (4, "a2: 1 V2->d2."),
        (5, "a0: 1 V0->d0."),
        (6, "b0: 1 V0->V1."), (6, "a1: 1 V1->d1."),
        (7, "a0: 1 V0->d0."),
        (8, "b0: 1 V0->V1."), (8, "b1: 1 V1->V2."),
        (8, "b2: 1 V2->V3."), (8, "a3: 1 V3->d3."),
        (9, "a0: 1 V0->d0."),
        (10, "b0: 1 V0->V1."), (10, "a1: 1 V1->d1."),
        (11, "a0: 1 V0->d0."),
        (12, "b0: 1 V0->V1."), (12, "b1: 1 V1->V2."), (12, "a2: 1 V2->d2."),
        (13, "a0: 1 V0->d0."),
    ], marks
    assert g.volume("d0") == 7 and g.volume("d1") == 3
    assert g.volume("d2") == 2 and g.volume("d3") == 1
    assert g.volume("tail") == 0 and g.volume("src") == 0
    for name in ("V0", "V1", "V2", "V3"):
        assert g.volume(name) == 0, "no rotor holds stock after its tick"
    assert [g.nodes[n].rot for n in ("V0", "V1", "V2", "V3")] == [1, 0, 1, 1]
    assert _total(g) == 13


def test_the_counter_remembers_across_a_dry_gap():
    """The count is pure state (probe P2, traced): board A runs 13 ticks
    straight. Board B runs 7 ticks, has its feed closed for 5 ticks
    (every gap tick emits zero events: no rotor holds stock, so nothing
    moves), then reopens for 6 more. Same 13 fed units, and B's end
    state is BYTE-IDENTICAL to A's: nodes and pipes dicts equal, rotors
    and sinks exactly where the unbroken run left them. The counter is
    a function of the pulse COUNT, not the pulse timing: a register,
    not a leak."""
    a = _counter_board()
    for _ in range(13):
        a.tick()
    b = _counter_board()
    for _ in range(7):
        b.tick()
    b.close("in")
    for _ in range(5):
        assert b.tick() == [], "a gap tick moved water"
    b.open("in")
    for _ in range(6):
        b.tick()
    sa, sb = a.to_spec(), b.to_spec()
    assert sa["nodes"] == sb["nodes"]
    assert sa["pipes"] == sb["pipes"]
    assert sb["nodes"]["V3"]["rot"] == 1, "1101 keeps its high bit"


def test_rotor_into_a_gate_starves_without_a_pulse_tank():
    """The committed-landing interface law, pinned as the negative
    (probe P4, traced): two k=2 vortex wheels demux straight into one
    xor (VA's xa on odd ticks, VB's xb on even ticks). A vortex outlet
    is a COMMITTED _move in the rotor phase, after the verdict, so the
    xor's verdict never counts it: ins is empty every tick. Each landed
    unit pools, and the next inlet-free tick STARVED-spills it to the
    waste. Traced 6 ticks: five 1-unit STARVED spills (t2-t6), one unit
    stranded in X at close, the latch L at 0 with zero events, and not
    one "Junction X passes" line in the whole run. End: sinkA 3,
    sinkB 3, w 5, X 1, conserved 12. The detector sketch in cycle 5's
    NEXT THREAD died here, and the death is the finding: gates read
    deferred inlets only; rotor water needs an adapter."""
    g = WaterGraph()
    g.add_node("srcA", elev=9, volume=6)
    g.add_node("srcB", elev=9, volume=6)
    g.add_node("VA", elev=8, kind="vortex")
    g.add_node("VB", elev=8, kind="vortex")
    g.add_node("sinkA", elev=1)
    g.add_node("sinkB", elev=1)
    g.add_node("X", elev=5, kind="xor")
    g.add_node("w", elev=0, kind="waste")
    g.add_node("L", elev=3, kind="latch", sill=1)
    g.add_node("drywell", elev=9)
    g.add_pipe("ia", "srcA", "VA", cap=1)
    g.add_pipe("xa", "VA", "X", cap=1)
    g.add_pipe("sa", "VA", "sinkA", cap=1)
    g.add_pipe("ib", "srcB", "VB", cap=1)
    g.add_pipe("sb", "VB", "sinkB", cap=1)
    g.add_pipe("xb", "VB", "X", cap=1)
    g.add_pipe("ox", "X", "L", cap=1)
    g.add_pipe("ol", "L", "drywell", cap=1)
    starves = 0
    for _ in range(6):
        for e in g.tick():
            assert "passes" not in e, "a rotor-fed xor can never pass"
            assert "Latch" not in e, "the latch never charges"
            if "STARVED" in e:
                starves += 1
    assert starves == 5, starves
    assert g.volume("X") == 1 and g.volume("w") == 5
    assert g.volume("L") == 0 and g.volume("drywell") == 0
    assert g.volume("sinkA") == 3 and g.volume("sinkB") == 3
    assert _total(g) == 12


def test_pulse_tank_adapter_lets_two_wheels_drive_one_xor():
    """The adapter, pinned positive (probe, traced): the same two wheels
    and xor, but each wheel's gate-facing outlet now lands in a one-unit
    PLAIN pulse tank (tankA elev 7, tankB elev 7) that drains through an
    ordinary pipe into X. A plain-source delivery into a gated junction
    IS a deferred inlet, so the verdict finally sees the trains, one
    tick late and one unit wide. Anti-phase wheels (VB's sink outlet
    first): exactly one inlet reaches X every tick from t2 on, so X
    passes every tick and its ox charges the level-1 latch. Traced
    exactly through t4, then marked to t6. End: L 5 (one more unit in
    flight in tankB: a clock comparison never closes without a settling
    tick), sinks 3+3, w 0, X 0, conserved 12. The xor is reachable from
    the rotor world through two plain nodes; the latch pool is the
    accumulated disagreement of the two clocks."""
    g = WaterGraph()
    g.add_node("srcA", elev=9, volume=6)
    g.add_node("srcB", elev=9, volume=6)
    g.add_node("VA", elev=8, kind="vortex")
    g.add_node("VB", elev=8, kind="vortex")
    g.add_node("tankA", elev=7)
    g.add_node("tankB", elev=7)
    g.add_node("sinkA", elev=1)
    g.add_node("sinkB", elev=1)
    g.add_node("X", elev=5, kind="xor")
    g.add_node("w", elev=0, kind="waste")
    g.add_node("L", elev=3, kind="latch", sill=1)
    g.add_node("drywell", elev=9)
    g.add_pipe("ia", "srcA", "VA", cap=1)
    g.add_pipe("xa", "VA", "tankA", cap=1)
    g.add_pipe("sa", "VA", "sinkA", cap=1)
    g.add_pipe("ib", "srcB", "VB", cap=1)
    g.add_pipe("sb", "VB", "sinkB", cap=1)
    g.add_pipe("xb", "VB", "tankB", cap=1)
    g.add_pipe("ta", "tankA", "X", cap=1)
    g.add_pipe("tb", "tankB", "X", cap=1)
    g.add_pipe("ox", "X", "L", cap=1)
    g.add_pipe("ol", "L", "drywell", cap=1)
    ev1 = g.tick()
    assert ev1 == ["ia: 1 srcA->VA.", "ib: 1 srcB->VB.",
                   "xa: 1 VA->tankA.", "sb: 1 VB->sinkB."], ev1
    ev2 = g.tick()
    assert ev2 == ["ia: 1 srcA->VA.", "ib: 1 srcB->VB.",
                   "ta: 1 tankA->X.", "Junction X passes (ta sole inlet).",
                   "ox: 1 X->L.", "sa: 1 VA->sinkA.",
                   "xb: 1 VB->tankB."], ev2
    assert g.volume("L") == 1 and g.volume("X") == 0
    ev3 = g.tick()
    assert ev3 == ["ia: 1 srcA->VA.", "ib: 1 srcB->VB.",
                   "tb: 1 tankB->X.", "Junction X passes (tb sole inlet).",
                   "Latch L opens (pool 1 >= level 1).",
                   "ox: 1 X->L.", "xa: 1 VA->tankA.",
                   "sb: 1 VB->sinkB."], ev3
    assert g.volume("L") == 2
    ev4 = g.tick()
    assert ev4 == ["ia: 1 srcA->VA.", "ib: 1 srcB->VB.",
                   "ta: 1 tankA->X.", "Junction X passes (ta sole inlet).",
                   "Latch L opens (pool 2 >= level 1).",
                   "ox: 1 X->L.", "sa: 1 VA->sinkA.",
                   "xb: 1 VB->tankB."], ev4
    passes = 0
    for _ in range(2):  # ticks 5-6: the alternation holds
        for e in g.tick():
            if "passes" in e:
                passes += 1
    assert passes == 2
    assert g.volume("L") == 5, "pool = the exactly-one ticks so far"
    assert g.volume("tankB") == 1, "t6's wheel unit is in flight"
    assert g.volume("tankA") == 0 and g.volume("X") == 0
    assert g.volume("w") == 0 and g.volume("drywell") == 0
    assert g.volume("sinkA") == 3 and g.volume("sinkB") == 3
    assert _total(g) == 12


def test_difference_detector_accumulates_drift_not_coincidence():
    """Drift board (probe P5 re-traced through the adapter): wheel A
    k=2 (xa to tankA on odd ticks), wheel B k=3 (xb to tankB every
    third tick, sb1/sb2 sinks elsewhere), both tanks into X, X's ox
    into the level-1 latch L whose ol runs uphill to a drywell (the
    honest blocked-outflow grammar: the per-tick opens announce, zero
    movement). In 12 ticks the trains coincide twice (t2 and t8: both
    tanks deliver: X holds 2, the next dry verdict STARVED-spills the
    pair to w), disagree six times (t4,5,6,10,11,12: X passes one unit
    into L), and share four neither-ticks (t1,3,7,9: silence, zero
    bytes moved). The latch's pool ends at 6: exactly the disagreement
    count; the waste reads 4: exactly the coincidence volume. The
    announces on L name pools 1,2,3,3,3,3,4,5 on t5-t12 (the pool at
    each verdict; ol never moves uphill). End: sinkA 6, sb1 4, sb2 4,
    L 6, w 4, X 0, conserved 24: a relation between two signals,
    accumulated in water."""
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
    g.add_pipe("ta", "tankA", "X", cap=1)
    g.add_pipe("tb", "tankB", "X", cap=1)
    g.add_pipe("ox", "X", "L", cap=1)
    g.add_pipe("ol", "L", "drywell", cap=1)
    hold, starve, pass_, latch_open = 0, 0, 0, []
    for _ in range(12):
        for e in g.tick():
            if "holds 2 below gate" in e:
                hold += 1
            elif "STARVED" in e:
                starve += 1
            elif "passes" in e:
                pass_ += 1
            elif e.startswith("Latch L opens"):
                latch_open.append(e)
    assert hold == 2 and starve == 2 and pass_ == 6, (hold, starve, pass_)
    assert latch_open == [
        "Latch L opens (pool 1 >= level 1).",
        "Latch L opens (pool 2 >= level 1).",
        "Latch L opens (pool 3 >= level 1).",
        "Latch L opens (pool 3 >= level 1).",
        "Latch L opens (pool 3 >= level 1).",
        "Latch L opens (pool 3 >= level 1).",
        "Latch L opens (pool 4 >= level 1).",
        "Latch L opens (pool 5 >= level 1).",
    ], latch_open
    assert g.volume("L") == 6 and g.volume("w") == 4
    assert g.volume("X") == 0 and g.volume("drywell") == 0
    assert g.volume("sinkA") == 6 and g.volume("sb1") == 4
    assert g.volume("sb2") == 4 and g.volume("tankA") == 0
    assert g.volume("tankB") == 0
    assert _total(g) == 24


def test_phase_locked_wheels_agree_in_silence():
    """The agreement pin: the drift board's wheels both set to k=2 with
    xb first (phase-locked: both tanks fill on odd ticks, both deliver
    on even). Every delivery tick is a coincidence: X sees two inlets
    and holds the pair; every odd tick STARVED-spills the pooled pair
    to w. X never passes, so ox never moves and the latch NEVER fires:
    zero Latch lines in the run. Agreement is silence at the detector;
    the coincidence volume reads at the waste instead. Traced 12 ticks:
    six holds, five 2-unit STARVED spills, one pair stranded mid-rhythm
    in X at close. End: sinkA 6, sinkB 6, w 10, X 2, L 0, conserved
    24. Read against the drift pin (pool 6): the SAME parts distinguish
    locked clocks from drifting clocks by where the water lands."""
    g = WaterGraph()
    g.add_node("srcA", elev=9, volume=12)
    g.add_node("srcB", elev=9, volume=12)
    g.add_node("VA", elev=8, kind="vortex")
    g.add_node("VB", elev=8, kind="vortex")
    g.add_node("tankA", elev=7)
    g.add_node("tankB", elev=7)
    g.add_node("sinkA", elev=1)
    g.add_node("sinkB", elev=1)
    g.add_node("X", elev=5, kind="xor")
    g.add_node("w", elev=0, kind="waste")
    g.add_node("L", elev=3, kind="latch", sill=1)
    g.add_node("drywell", elev=9)
    g.add_pipe("ia", "srcA", "VA", cap=1)
    g.add_pipe("xa", "VA", "tankA", cap=1)
    g.add_pipe("sa", "VA", "sinkA", cap=1)
    g.add_pipe("ib", "srcB", "VB", cap=1)
    g.add_pipe("xb", "VB", "tankB", cap=1)
    g.add_pipe("sb", "VB", "sinkB", cap=1)
    g.add_pipe("ta", "tankA", "X", cap=1)
    g.add_pipe("tb", "tankB", "X", cap=1)
    g.add_pipe("ox", "X", "L", cap=1)
    g.add_pipe("ol", "L", "drywell", cap=1)
    hold, starve = 0, 0
    for _ in range(12):
        for e in g.tick():
            assert "passes" not in e and "Latch" not in e, e
            if "holds 2 below gate" in e:
                hold += 1
            elif "STARVED" in e:
                starve += 1
    assert hold == 6 and starve == 5, (hold, starve)
    assert g.volume("w") == 10 and g.volume("X") == 2
    assert g.volume("L") == 0 and g.volume("drywell") == 0
    assert g.volume("sinkA") == 6 and g.volume("sinkB") == 6
    assert g.volume("tankA") == 0 and g.volume("tankB") == 0
    assert _total(g) == 24
