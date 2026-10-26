"""vortex tests - the rotor primitive (mariner cycle 3, 2026-10-10).

The skyrmion steal (PRX 16, 031078: vortices trap and rotate floating
bodies) landed as node kind "vortex": a metering wheel over its live
outflow pipes. Each test is one law of the rotor: alternating demux,
park on a blocked outlet, mod-k counting, committed landing at a gated
junction, roundtrip (rot AND steam), graded-law parity, determinism.
Spec: mag/water_graph.py module docstring, VORTEX block; receipt
watch/inbox/mates_leave_protocol/receipts/receipt_20261010_mariner.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402


def _demux_board(volume: int, k: int = 2) -> WaterGraph:
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=volume)
    names = ["a", "b", "c"][:k]
    for i, name in enumerate(names):
        g.add_node(name, elev=1)
        g.add_pipe(f"v{i}", "swirl", name, cap=1)
    return g


def test_vortex_alternates_two_outlets_and_conserves():
    """k=2 demux: 6 units leave one cap-1 unit per tick, alternating;
    3/3 split, hub dry, register back where it started, economy exact."""
    g = _demux_board(6, k=2)
    total0 = sum(n.volume + n.steam for n in g.nodes.values())
    for _ in range(6):
        g.tick()
    assert g.volume("a") == 3 and g.volume("b") == 3
    assert g.volume("swirl") == 0, "the hub drains one unit per tick"
    assert g.nodes["swirl"].rot == 0, "6 deliveries advance rot 6 times: (0+6) % 2"
    assert sum(n.volume + n.steam for n in g.nodes.values()) == total0


def test_vortex_parks_on_blocked_outlet():
    """Metering law: rot advances ONLY on delivery. Outlet b runs uphill
    (check valve), so after the first turn the rotor parks on b forever
    and every remaining unit waits at the hub... no: waits go through a
    only when rot points at a. Pinned: one delivery, then the wheel
    stops on the blocked channel and the hub keeps the rest."""
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=6)
    g.add_node("low", elev=1)
    g.add_node("high", elev=9)          # uphill from the hub: never flows
    g.add_pipe("va", "swirl", "low", cap=1)
    g.add_pipe("vb", "swirl", "high", cap=1)
    for _ in range(5):
        g.tick()
    assert g.volume("low") == 1, "tick 1 delivered through va, rot then parked on vb"
    assert g.volume("high") == 0, "check-valve law: the vortex cannot lift"
    assert g.volume("swirl") == 5, "the parked wheel leaves the pool at the hub"
    assert g.nodes["swirl"].rot == 1


def test_vortex_is_a_mod_k_counter():
    """k=3: the delivery sequence is the rotation register read aloud.
    5 units: a, b, c, a, b. Counts 2/2/1, rot ends at 5 % 3 = 2."""
    g = _demux_board(5, k=3)
    seq = []
    for _ in range(5):
        seq.extend(e for e in g.tick() if e.startswith("v") and "swirl->" in e)
    assert [e.split(":")[0] for e in seq] == ["v0", "v1", "v2", "v0", "v1"]
    assert g.volume("a") == 2 and g.volume("b") == 2 and g.volume("c") == 1
    assert g.nodes["swirl"].rot == 2


def test_vortex_into_a_gate_lands_committed_then_starves():
    """Gate interaction: a vortex's outflow rides the gated-outflow slot,
    so it lands at the junction COMMITTED (the same shape as gate-to-gate
    outflow today) and the junction's own gate never sees it: with no
    deferred inlet the xor's outflow never opens and the standing
    STARVATION law spills the pool to the first waste on the next dry
    tick. Pinned so nobody calls the starve a bug later."""
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=2)
    g.add_node("jx", elev=3, kind="xor")
    g.add_node("pool", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("vj", "swirl", "jx", cap=1)
    g.add_pipe("jo", "jx", "pool", cap=1)
    for _ in range(3):
        g.tick()
    assert g.volume("jx") == 0 and g.volume("pool") == 0
    assert g.volume("waste") == 2, "the committed pool starved out to waste"
    assert g.nodes["swirl"].rot == 0, "2 deliveries on k=1: (0+2) % 1"


def test_roundtrip_carries_rot_and_steam():
    """The vortex law's roundtrip half AND the cycle-1 steam fix in one
    pin: to_spec/from_spec must carry node rot AND node steam (from_spec
    dropped steam to 0 on every roundtrip before the cycle-3 fix; the
    LW5 drop family, third member). Second roundtrip must be exact.
    k=2 so the register actually moves: one delivery parks rot at 1."""
    from mag.water_graph import from_spec
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=4)
    g.add_node("low", elev=1)
    g.add_node("side", elev=1)
    g.add_pipe("va", "swirl", "low", cap=1)
    g.add_pipe("vb", "swirl", "side", cap=1)
    g.tick()                              # one delivery through va: rot 1, swirl 3
    g.boil("swirl", 2)                    # swirl: volume 1, steam 2 (parks: no cold node)
    spec = g.to_spec()
    # LATCH roundtrip law (2026-10-12, cycle 5): sill joined the node dict
    # the same additive way (steam, then rot, now sill): the latch LEVEL is
    # runtime-essential gate state and to_spec must carry it.
    assert spec["nodes"]["swirl"] == {"elev": 5, "kind": "vortex",
                                      "sill": 0, "volume": 1, "steam": 2,
                                      "rot": 1}
    g2 = from_spec(spec)
    assert g2.nodes["swirl"].steam == 2, "roundtrip must not drop steam"
    assert g2.nodes["swirl"].rot == 1, "roundtrip must not drop rot"
    assert g2.to_spec() == spec, "second roundtrip must be byte-exact"


def test_vortex_under_the_graded_head_law():
    """HydrologyGraph inherits tick(); the rotor must turn identically
    under the graded law (one law, two head laws), and the hydrology
    roundtrip must carry rot AND steam (the node-side AF2 family fix)."""
    from mag.hydrology import HydrologyGraph, from_spec as hydro_from_spec
    g = HydrologyGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=6)
    g.add_node("a", elev=1)
    g.add_node("b", elev=1)
    g.add_pipe("v0", "swirl", "a", cap=1)
    g.add_pipe("v1", "swirl", "b", cap=1)
    for _ in range(6):
        g.tick()
    assert g.volume("a") == 3 and g.volume("b") == 3
    assert g.nodes["swirl"].rot == 0
    g.boil("a", 2)                        # a: volume 1, steam 2 (parks: no cold node)
    spec = g.to_spec()
    g2 = hydro_from_spec(spec)
    assert g2.nodes["a"].steam == 2 and g2.nodes["swirl"].rot == 0
    assert g2.to_spec() == spec


def test_vortex_is_deterministic():
    """Same board, same ticks: byte-identical state, zero RNG."""
    def run():
        g = _demux_board(6, k=2)
        for _ in range(6):
            g.tick()
        return g.to_spec()
    assert json.dumps(run(), sort_keys=True) == json.dumps(run(), sort_keys=True)


# ---- cycle 4 (2026-10-11): the clock law, the burst remap, the brakes ------
# Probes behind every pin here: receipt_20261011_mariner.md (JOURNEY turns
# 4-6). The cycle-3 docstring's self-clock guess was falsified by probe and
# the docstring now states the DAG law; these tests are its executable half.


def _clock_board(volume: int) -> WaterGraph:
    """v1 (k=2: outlet 0 fd -> waste, outlet 1 ff -> v2's hub) half-feeds the
    k=3 wheel v2 (outlets g_x/g_y/g_z). All legs descend: 9 > 7 > 5, waste 1.
    Pipe insertion order fd, ff, g_x, g_y, g_z: vortex emission phases run
    in first-vortex-pipe insertion order (v1 before v2), so on a feeding
    tick the hub is filled BEFORE the downstream wheel reads it."""
    g = WaterGraph()
    g.add_node("v1", elev=9, kind="vortex", volume=volume)
    g.add_node("v2", elev=7, kind="vortex")
    g.add_node("drain", elev=1, kind="waste")
    g.add_pipe("fd", "v1", "drain", cap=1)
    g.add_pipe("ff", "v1", "v2", cap=1)
    for nm in ("x", "y", "z"):
        g.add_node(nm, elev=5)
        g.add_pipe(f"g_{nm}", "v2", nm, cap=1)
    return g


def test_half_fed_ladder_is_a_run_down_clock_of_period_k1_times_k2():
    """THE CLOCK LAW (cycle 4): v1 k=2 feeds the k2=3 wheel on every second
    tick (odd ticks drain, even ticks feed), so v2 emits x,y,z cycling on
    EVEN ticks: the (tick, outlet) pattern repeats with period k1*k2 = 6.
    12 units run two full laps. Traced: ticks 1..12; v1 emits fd on odd
    ticks (6 to waste) and ff on even ticks (6 through v2: x,y,z,x,y,z);
    rot1 = 12 mod 2 = 0, rot2 = 6 mod 3 = 0; conserved 12."""
    g = _clock_board(12)
    total0 = sum(n.volume + n.steam for n in g.nodes.values())
    marks = []
    for _ in range(12):
        for e in g.tick():
            if e.startswith("g_") and "v2->" in e:
                marks.append((g.tick_count, e.split(":")[0]))
    assert marks == [(2, "g_x"), (4, "g_y"), (6, "g_z"),
                     (8, "g_x"), (10, "g_y"), (12, "g_z")], marks
    assert g.volume("drain") == 6
    assert g.volume("x") == 2 and g.volume("y") == 2 and g.volume("z") == 2
    assert g.volume("v1") == 0 and g.volume("v2") == 0, "the clock ran down dry"
    assert g.nodes["v1"].rot == 0 and g.nodes["v2"].rot == 0
    assert sum(n.volume + n.steam for n in g.nodes.values()) == total0 == 12


def test_continuously_fed_wheel_collapses_to_its_own_period():
    """The clock's period is set by FEED CADENCE times the wheel: v1 k=2
    with BOTH outlets piped downhill into v2's hub (via the m0/m1 tanks)
    feeds the k2=3 wheel every tick, so f0,f1,f2 fire on CONSECUTIVE ticks:
    the period collapses from k1*k2 to k2. Traced: 6 units, ticks 2..7 read
    f0,f1,f2,f0,f1,f2; sinks 2/2/2; both rotors end at 0 (6 mod 2, 6 mod 3)."""
    g = WaterGraph()
    g.add_node("v1", elev=9, kind="vortex", volume=6)
    g.add_node("v2", elev=7, kind="vortex")
    for i in (0, 1):
        g.add_node(f"m{i}", elev=8)
        g.add_pipe(f"e{i}", "v1", f"m{i}", cap=1)
        g.add_pipe(f"j{i}", f"m{i}", "v2", cap=1)
    for i in (0, 1, 2):
        g.add_node(f"s{i}", elev=5)
        g.add_pipe(f"f{i}", "v2", f"s{i}", cap=1)
    marks = []
    for _ in range(7):
        for e in g.tick():
            if e.startswith("f") and "v2->" in e:
                marks.append((g.tick_count, e.split(":")[0]))
    assert marks == [(2, "f0"), (3, "f1"), (4, "f2"),
                     (5, "f0"), (6, "f1"), (7, "f2")], marks
    assert g.volume("s0") == 2 and g.volume("s1") == 2 and g.volume("s2") == 2
    assert g.nodes["v1"].rot == 0 and g.nodes["v2"].rot == 0


def test_outlet_fracture_turns_the_wheel_then_remaps_the_phase():
    """Burst-on-its-tick, pinned small: vb is stress-seeded AT its djb2
    threshold, so its first full-bore turn bursts it. Tick 1: va delivers,
    rot 1. Tick 2: vb's turn runs full bore, stress crosses, vb FRACTURES,
    the unit sprays to a (lowest node that is not dst b) and the wheel
    STILL TURNS (the water left the hub): rot wraps (1+1) % 2 = 0.
    Tick 3: the live-outlet list rebuilds with k=1; the stored rot 1 reads
    1 % 1 = 0, so the survivor va emits and the phase has REMAPPED.
    Roundtrip: fractured + stress + rot all carry; the post-roundtrip tick
    emits the survivor again (swirl 2 - 1 = 1, a 2 + 1 = 3)."""
    from mag.water_graph import fracture_threshold, from_spec
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=4)
    g.add_node("a", elev=1)
    g.add_node("b", elev=1)
    g.add_pipe("va", "swirl", "a", cap=1)
    g.add_pipe("vb", "swirl", "b", cap=1,
               stress=fracture_threshold("vb"))
    ev1 = g.tick()
    assert g.volume("a") == 1 and g.nodes["swirl"].rot == 1, ev1
    ev2 = g.tick()
    assert any("vb FRACTURES" in e and "spray to a" in e for e in ev2), ev2
    assert g.volume("swirl") == 2 and g.volume("a") == 2 and g.volume("b") == 0
    assert g.nodes["swirl"].rot == 0, "the burst tick still turned the wheel"
    ev3 = g.tick()
    assert any(e.startswith("va:") and "swirl->a" in e for e in ev3), ev3
    assert g.volume("swirl") == 1 and g.volume("a") == 3
    assert g.nodes["swirl"].rot == 0, "(0+1) % 1: the wheel reads the survivor"
    spec = g.to_spec()
    assert spec["pipes"]["vb"]["fractured"] is True
    assert spec["pipes"]["vb"]["stress"] == fracture_threshold("vb") + 1
    g2 = from_spec(spec)
    assert g2.pipes["vb"].fractured and g2.nodes["swirl"].rot == 0
    g2.tick()
    assert g2.volume("swirl") == 0 and g2.volume("a") == 4, "survivor still emits"


def test_siphon_outlet_makes_a_crest_gated_rotor():
    """Outlet 0 is a siphon (crest 3, cap 2), outlet 1 a plain cap-1 pipe.
    Below crest the wheel PARKS on the siphon channel (a siphon primes only
    at volume >= crest under positive head); at hub >= 3 it primes and
    delivers min(cap, volume) = 2; while primed the wheel alternates
    siphon/plain; when the feed runs dry the primed siphon BREAKS (intake
    dry) and the wheel parks for good. A hysteresis rotor: crest-gated
    start, break-stop. Traced off the cycle-4 probe (10-unit feed, 1/tick):
    parks ticks 1-2 at 1, 2; primes tick 3 (3 >= 3): low +2; alternates
    ticks 4-10; tick 11 the feed is dry, the hub is dry, the siphon breaks;
    end: low 6, high 4, swirl 0, rot 0, conserved 10."""
    g = WaterGraph()
    g.add_node("feed", elev=9, volume=10)
    g.add_node("swirl", elev=5, kind="vortex")
    g.add_node("low", elev=1)
    g.add_node("high", elev=1)
    g.add_pipe("in", "feed", "swirl", cap=1)
    g.add_pipe("vs", "swirl", "low", cap=2, siphon=True, crest=3)
    g.add_pipe("vo", "swirl", "high", cap=1)
    break_seen = False
    for _ in range(12):
        for e in g.tick():
            if "vs breaks (intake dry)" in e:
                break_seen = True
    assert break_seen, "the primed siphon must break on the dry hub"
    assert g.volume("low") == 6 and g.volume("high") == 4
    assert g.volume("swirl") == 0 and g.volume("feed") == 0
    assert g.nodes["swirl"].rot == 0, "parked on the siphon channel at the end"
    assert g.pipes["vs"].primed is False


def test_direct_self_loop_is_a_brake_not_a_clock():
    """The cycle-3 docstring guessed a feedback pipe makes a self-clocking
    source; the cycle-4 probes falsified it and the docstring now states
    the DAG law. This pin is the falsifier, kept: a self-loop outlet's dst
    IS the hub, equal elevation is no head (check-valve law), so the loop
    channel never flows and the wheel parks on it at rot 0 forever; the
    live outlet never fires. 6 ticks, zero movement, events empty,
    conserved 4."""
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=4)
    g.add_node("sink", elev=1)
    g.add_pipe("loop", "swirl", "swirl", cap=1)
    g.add_pipe("out", "swirl", "sink", cap=1)
    for _ in range(6):
        ev = g.tick()
        assert ev == [], "a parked wheel must emit nothing"
    assert g.nodes["swirl"].rot == 0, "parks on the dead loop channel"
    assert g.volume("swirl") == 4 and g.volume("sink") == 0


def test_all_outlets_burst_freezes_the_hub_with_its_pool():
    """The k=0 endgame: both outlets stress-seeded at threshold; each bursts
    on its first turn (the burst tick still turned the wheel: rot 1 then
    (1+1) % 1 = 0). After that the vortex has NO live outlet: the rotor
    loop skips it entirely (a rot % 0 evaluation seat that the grouping
    loop makes unreachable), the pool freezes at the hub, no crash, no
    events, conserved 6 = 4 + 1 + 1."""
    from mag.water_graph import fracture_threshold
    g = WaterGraph()
    g.add_node("swirl", elev=5, kind="vortex", volume=6)
    g.add_node("a", elev=1)
    g.add_node("b", elev=1)
    g.add_pipe("va", "swirl", "a", cap=1, stress=fracture_threshold("va"))
    g.add_pipe("vb", "swirl", "b", cap=1, stress=fracture_threshold("vb"))
    ev1 = g.tick()   # va bursts on its first turn; spray to b (elev 1, not dst)
    assert any("va FRACTURES" in e and "spray to b" in e for e in ev1), ev1
    assert g.nodes["swirl"].rot == 1
    ev2 = g.tick()   # vb (now k=1) bursts on its first turn; spray to a
    assert any("vb FRACTURES" in e and "spray to a" in e for e in ev2), ev2
    assert g.nodes["swirl"].rot == 0
    for _ in range(4):
        assert g.tick() == [], "a frozen hub must be silent"
    assert g.volume("swirl") == 4 and g.volume("a") == 1 and g.volume("b") == 1
    assert g.pipes["va"].fractured and g.pipes["vb"].fractured
