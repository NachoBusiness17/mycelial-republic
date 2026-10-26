"""latch tests - the memory element (mariner cycle 5, 2026-10-12).

The cycle-4 receipt's self-chosen NEXT THREAD, landed: kind "latch" is a
pool-level gate whose sill field is its LEVEL (clamped >= 1). The gate
verdict reads the POOL (standing volume plus this tick's deferred
inflow), not the inlets; a below-level latch KEEPS its pool across dry
ticks and NEVER STARVED-spills (the sill drains on the first dry tick;
these tests carry the contrast). A charged latch discharges on a dry
tick: the only gate whose verdict can pass with zero inlets. Each test
is one law: charge-and-regulate, dry-tick discharge, the sill contrast,
the rotor divider, the integrator chain, roundtrip + graded-law parity,
the level clamp, determinism. Spec: mag/water_graph.py module docstring,
LATCH block; receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261012_mariner.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def test_latch_charges_then_opens_and_regulates():
    """Charge-and-regulate (probe P1, traced): cap-1 feed at 1/tick into a
    level-3 latch with a cap-1 outflow. Ticks 1-2 pool 1, 2 ("holds pool N
    below level 3; pooling."). Tick 3 the pool reaches 3: "Latch tank opens
    (pool 3 >= level 3)." and the outflow drains 1 (pool 2). Ticks 3-6 are
    the steady state: one unit through per tick (throughput caps at the
    outflow cap; the excess is stored, never spilled). Tick 7 the feed is
    dry: pool 2 < 3: the latch goes SILENT and keeps its 2 (the hysteresis
    floor of level-1) through tick 10. End: src 0, tank 2, sink 4,
    conserved 6, zero STARVED lines anywhere."""
    g = WaterGraph()
    g.add_node("src", elev=9, volume=6)
    g.add_node("tank", elev=5, kind="latch", sill=3)
    g.add_node("sink", elev=1)
    g.add_pipe("in", "src", "tank", cap=1)
    g.add_pipe("out", "tank", "sink", cap=1)
    ev1 = g.tick()
    assert g.volume("tank") == 1 and g.volume("sink") == 0
    assert any(e.startswith("Latch tank holds pool 1 below level 3") for e in ev1), ev1
    ev2 = g.tick()
    assert g.volume("tank") == 2
    assert any(e.startswith("Latch tank holds pool 2 below level 3") for e in ev2), ev2
    ev3 = g.tick()
    assert ev3 == ["in: 1 src->tank.", "Latch tank opens (pool 3 >= level 3).",
                   "out: 1 tank->sink."], ev3
    assert g.volume("tank") == 2 and g.volume("sink") == 1
    for _ in range(3):  # ticks 4-6: regulate at cap-1 per tick
        assert g.tick() == ["in: 1 src->tank.", "Latch tank opens (pool 3 >= level 3).",
                            "out: 1 tank->sink."]
    assert g.volume("src") == 0 and g.volume("sink") == 4
    for _ in range(4):  # ticks 7-10: below level, dry: silent, pool kept
        assert g.tick() == []
    assert g.volume("tank") == 2, "the level-1 floor is held, not spilled"
    assert _total(g) == 6
    spec = g.to_spec()
    assert "STARVED" not in json.dumps(spec), "no starve line ever fired"


def test_latch_discharges_on_a_dry_tick():
    """Deliver-on-gate, keep-on-dry. Three cap-1 feeds land 3 units in one
    tick: "opens (pool 3 >= level 2)" and the cap-1 outflow drains 1,
    leaving pool 2. Tick 2 is DRY (every feed empty, zero deferred inlets)
    and the verdict STILL passes on the standing pool: "Latch tank opens
    (pool 2 >= level 2)." and o drains 1: the only gate whose verdict can
    pass with zero inlets. The floor 1 stays below level 2 in silence
    forever after. End: tank 1, sink 2, feeds 0, conserved 3."""
    g = WaterGraph()
    g.add_node("f0", elev=9, volume=1)
    g.add_node("f1", elev=9, volume=1)
    g.add_node("f2", elev=9, volume=1)
    g.add_node("tank", elev=5, kind="latch", sill=2)
    g.add_node("sink", elev=1)
    g.add_pipe("i0", "f0", "tank", cap=1)
    g.add_pipe("i1", "f1", "tank", cap=1)
    g.add_pipe("i2", "f2", "tank", cap=1)
    g.add_pipe("o", "tank", "sink", cap=1)
    ev1 = g.tick()
    assert ev1 == ["i0: 1 f0->tank.", "i1: 1 f1->tank.", "i2: 1 f2->tank.",
                   "Latch tank opens (pool 3 >= level 2).",
                   "o: 1 tank->sink."], ev1
    assert g.volume("tank") == 2 and g.volume("sink") == 1
    ev2 = g.tick()  # DRY tick: the charged latch fires on its pool alone
    assert ev2 == ["Latch tank opens (pool 2 >= level 2).",
                   "o: 1 tank->sink."], ev2
    assert g.volume("tank") == 1 and g.volume("sink") == 2
    for _ in range(3):
        assert g.tick() == [], "pool 1 < level 2 on a dry tick: silent keep"
    assert g.volume("tank") == 1
    assert _total(g) == 3


def test_latch_is_the_sill_contrast_never_spills():
    """THE contrast pin (cycle-4 finding 6's board, both kinds). Same
    shape: two cap-1 inlets pass the gate in one tick, the cap-1 outflow
    drains 1, ONE unit stands at the junction, then every tick is dry.
    The sill STARVED-spills its standing 1 to the first waste on the dry
    tick (waste 1); the latch KEEPS it silently (waste 0, tank 1 forever).
    No STARVED line in the latch board's whole run."""
    def board(kind: str) -> WaterGraph:
        g = WaterGraph()
        g.add_node("f0", elev=9, volume=1)
        g.add_node("f1", elev=9, volume=1)
        g.add_node("j", elev=5, kind=kind, sill=2)
        g.add_node("sink", elev=1)
        g.add_node("waste", elev=0, kind="waste")
        g.add_pipe("i0", "f0", "j", cap=1)
        g.add_pipe("i1", "f1", "j", cap=1)
        g.add_pipe("o", "j", "sink", cap=1)
        return g
    sill_g = board("sill")
    sill_g.tick()
    ev2 = sill_g.tick()
    assert any("STARVED" in e for e in ev2), ev2
    assert sill_g.volume("waste") == 1 and sill_g.volume("j") == 0
    latch_g = board("latch")
    ev1 = latch_g.tick()
    assert ev1 == ["i0: 1 f0->j.", "i1: 1 f1->j.",
                   "Latch j opens (pool 2 >= level 2).",
                   "o: 1 j->sink."], ev1
    for _ in range(4):
        assert latch_g.tick() == [], "the latch keeps its pool in silence"
    assert latch_g.volume("j") == 1 and latch_g.volume("waste") == 0
    assert latch_g.volume("sink") == 1
    assert _total(latch_g) == 2


def test_rotor_feeding_a_latch_is_a_divider():
    """Rotor + latch = the divider (probe P2, traced): a k=3 vortex
    round-robins v0(s0), v1(s1), v2(tank level 2, cap-1 outflow o). The
    vortex's delivery is COMMITTED (phase 5, after this tick's verdicts),
    so the tank pools 1 on t3 and 2 on t6. Tick 7's verdict passes on the
    POOL with zero inflow: "Latch tank opens (pool 2 >= level 2)." and o
    drains 1 (out 1) BEFORE the vortex emits v0 that tick (the phase law:
    verdicts, gated outflow, rotor). The out rhythm is one unit per three
    feed units after the charge. End: s0 3, s1 3, out 1, tank 2, rot 0,
    conserved 9."""
    g = WaterGraph()
    g.add_node("swirl", elev=9, kind="vortex", volume=9)
    g.add_node("s0", elev=1)
    g.add_node("s1", elev=1)
    g.add_node("tank", elev=5, kind="latch", sill=2)
    g.add_node("out", elev=1)
    g.add_pipe("v0", "swirl", "s0", cap=1)
    g.add_pipe("v1", "swirl", "s1", cap=1)
    g.add_pipe("v2", "swirl", "tank", cap=1)
    g.add_pipe("o", "tank", "out", cap=1)
    marks = []
    for _ in range(9):
        for e in g.tick():
            if e.startswith("o:") or e.startswith("v") or "Latch" in e:
                marks.append((g.tick_count, e))
    assert marks == [
        (1, "v0: 1 swirl->s0."), (2, "v1: 1 swirl->s1."),
        (3, "v2: 1 swirl->tank."),
        (4, "v0: 1 swirl->s0."), (5, "v1: 1 swirl->s1."),
        (6, "v2: 1 swirl->tank."),
        (7, "Latch tank opens (pool 2 >= level 2)."),
        (7, "o: 1 tank->out."), (7, "v0: 1 swirl->s0."),
        (8, "v1: 1 swirl->s1."),
        (9, "v2: 1 swirl->tank."),
    ], marks
    assert g.volume("s0") == 3 and g.volume("s1") == 3
    assert g.volume("out") == 1 and g.volume("tank") == 2
    assert g.nodes["swirl"].rot == 0, "9 deliveries: 9 % 3"
    assert _total(g) == 9


def test_latch_chain_is_a_pipeline_of_integrators():
    """Two latches in series (probe P5, traced): src (4 units, cap-1) ->
    A (level 2) -> B (level 2) -> sink, all cap-1. A's outflow lands in B
    COMMITTED (a gate's outflow is a plain _move: B's gate never sees it
    as a deferred inlet; the vortex-into-xor shape). Traced: t1 A holds 1;
    t2 A opens (2 >= 2), ab 1 (B 1); t3 A opens again (B 2); t4's verdicts
    announce A then B (insertion order) BEFORE any outflow moves: "Latch B
    opens (pool 2 >= level 2)." fires on B's standing pool, then ab lands
    (B 3) and bo drains B to 2 (sink 1); t5 B opens on its pool (sink 2);
    t6-8: dry, A keeps 1, B keeps 1, silent. The chain delivered 2 of 4;
    each stage stores a floor of 1: state carried between reads."""
    g = WaterGraph()
    g.add_node("src", elev=9, volume=4)
    g.add_node("A", elev=7, kind="latch", sill=2)
    g.add_node("B", elev=5, kind="latch", sill=2)
    g.add_node("sink", elev=1)
    g.add_pipe("ia", "src", "A", cap=1)
    g.add_pipe("ab", "A", "B", cap=1)
    g.add_pipe("bo", "B", "sink", cap=1)
    ev1 = g.tick()
    assert ev1 == ["Latch A holds pool 1 below level 2; pooling."], ev1
    ev2 = g.tick()
    assert ev2 == ["ia: 1 src->A.", "Latch A opens (pool 2 >= level 2).",
                   "ab: 1 A->B."], ev2
    assert g.volume("A") == 1 and g.volume("B") == 1
    ev3 = g.tick()
    assert ev3 == ev2, "same trace again: A refills as it drains, B pools 2"
    assert g.volume("B") == 2
    ev4 = g.tick()
    assert ev4 == ["ia: 1 src->A.", "Latch A opens (pool 2 >= level 2).",
                   "Latch B opens (pool 2 >= level 2).",
                   "ab: 1 A->B.", "bo: 1 B->sink."], ev4
    assert g.volume("A") == 1 and g.volume("B") == 2 and g.volume("sink") == 1
    ev5 = g.tick()
    assert ev5 == ["Latch B opens (pool 2 >= level 2).",
                   "bo: 1 B->sink."], ev5
    for _ in range(3):
        assert g.tick() == [], "dry chain below level: silent keep"
    assert g.volume("src") == 0 and g.volume("A") == 1 and g.volume("B") == 1
    assert g.volume("sink") == 2 and _total(g) == 4
def test_latch_roundtrip_and_graded_law():
    """One law, two engines + the wire: (a) to_spec/from_spec carries kind
    "latch", the level in sill, and the pooled volume; second roundtrip is
    byte-exact; (b) under the graded head law (HydrologyGraph inherits
    tick(); only _available/_move are overridden) the latch charges and
    opens with the same trace: cap-1 feed at dHead 1030*8 >> 8 = 32 is
    cap-bound at 1, so t1 pools 1 ("holds pool 1 below level 2"), t2 opens
    (pool 2 >= level 2) and drains 1, t3 is silent. End: src 0, tank 1,
    sink 1, conserved 2 on both engines."""
    from mag.water_graph import from_spec
    g = WaterGraph()
    g.add_node("src", elev=9, volume=2)
    g.add_node("tank", elev=5, kind="latch", sill=2)
    g.add_node("sink", elev=1)
    g.add_pipe("in", "src", "tank", cap=1)
    g.add_pipe("out", "tank", "sink", cap=1)
    g.tick()
    g.tick()
    assert g.volume("tank") == 1 and g.volume("sink") == 1
    spec = g.to_spec()
    assert spec["nodes"]["tank"] == {"elev": 5, "kind": "latch",
                                     "volume": 1, "steam": 0, "rot": 0,
                                     "sill": 2}
    g2 = from_spec(spec)
    assert g2.nodes["tank"].kind == "latch" and g2.nodes["tank"].sill == 2
    assert g2.to_spec() == spec, "second roundtrip byte-exact"
    from mag.hydrology import HydrologyGraph
    h = HydrologyGraph()
    h.add_node("src", elev=9, volume=2)
    h.add_node("tank", elev=5, kind="latch", sill=2)
    h.add_node("sink", elev=1)
    h.add_pipe("in", "src", "tank", cap=1)
    h.add_pipe("out", "tank", "sink", cap=1)
    ev1 = h.tick()
    assert any(e.startswith("Latch tank holds pool 1 below level 2") for e in ev1), ev1
    ev2 = h.tick()
    assert "Latch tank opens (pool 2 >= level 2)." in ev2, ev2
    assert h.volume("tank") == 1 and h.volume("sink") == 1
    assert h.tick() == []
    assert _total(h) == 2


def test_latch_level_clamps_and_a_blocked_outflow_announces_per_tick():
    """The clamp + the announcement grammar (probe P0): a latch with sill 0
    evaluates at level 1 (clamped like a sill threshold) and NAMES the
    effective level in its events. Its outflow runs uphill (never moves:
    check-valve law), so the charged latch announces "Latch tank opens
    (pool 2 >= level 1)." EVERY tick with zero movement: the gate verdict
    is a per-tick statement (the sill's grammar), and the water leaves or
    does not under the ordinary laws. End: tank 2, drywell 0, conserved 2.
    An event claiming movement never fires; the announce claims only the
    verdict, which is true."""
    g = WaterGraph()
    g.add_node("src", elev=9, volume=2)
    g.add_node("tank", elev=5, kind="latch", sill=0)
    g.add_node("drywell", elev=9)
    g.add_pipe("in", "src", "tank", cap=1)
    g.add_pipe("out", "tank", "drywell", cap=1)
    ev1 = g.tick()
    assert "Latch tank opens (pool 1 >= level 1)." in ev1, ev1
    ev2 = g.tick()
    assert "Latch tank opens (pool 2 >= level 1)." in ev2, ev2
    ev3 = g.tick()
    assert ev3 == ["Latch tank opens (pool 2 >= level 1)."], ev3
    assert g.volume("tank") == 2 and g.volume("drywell") == 0
    assert _total(g) == 2


def test_latch_is_deterministic():
    """Same board, same ticks: byte-identical state, zero RNG."""
    def run() -> str:
        g = WaterGraph()
        g.add_node("src", elev=9, volume=6)
        g.add_node("tank", elev=5, kind="latch", sill=3)
        g.add_node("sink", elev=1)
        g.add_pipe("in", "src", "tank", cap=1)
        g.add_pipe("out", "tank", "sink", cap=1)
        for _ in range(10):
            g.tick()
        return json.dumps(g.to_spec(), sort_keys=True)
    assert run() == run()
