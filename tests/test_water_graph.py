"""water_graph tests — routing as physics (operator order 2026-09-27).

Each test is a physics law: gravity-only flow, no backflow, siphon
prime-and-break, hydraulic XOR, steam condenses at the highest cold node,
determinism. The win honesty lives in water_computer; this file pins the
engine the router delegates to.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph, fracture_threshold  # noqa: E402


def _graph() -> WaterGraph:
    g = WaterGraph()
    g.add_node("source", elev=5, volume=6)
    g.add_node("work", elev=3)
    g.add_node("out", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    return g


def test_gravity_flows_only_when_open():
    g = _graph()
    g.add_pipe("a", "source", "work", cap=2)
    g.close("a")
    g.tick()
    assert g.volume("work") == 0, "closed valve must move nothing"
    g.open("a")
    g.tick()
    assert g.volume("work") == 2, "open pipe flows up to capacity"


def test_no_uphill_flow_ever():
    g = _graph()
    g.add_node("high", elev=9)
    g.add_pipe("up", "out", "high", cap=3)  # dst higher than src
    g.tick()
    assert g.volume("high") == 0, "check-valve law: nothing flows uphill"


def test_siphon_primes_at_crest_and_breaks_dry():
    g = _graph()
    g.add_node("barrel", elev=4, volume=1)      # below crest
    g.add_node("cistern", elev=0)
    g.add_pipe("sip", "barrel", "cistern", cap=2, siphon=True, crest=2)
    g.tick()
    assert g.volume("cistern") == 0, "unprimed siphon must not flow"
    barrel = g.nodes["barrel"]
    barrel.volume = 3                            # now above crest
    g.tick()
    assert g.volume("cistern") == 2, "primed siphon flows its capacity"
    assert g.pipes["sip"].primed is True
    barrel.volume = 0                            # intake breaks
    g.tick()
    assert g.pipes["sip"].primed is False, "siphon breaks when intake dries"


def test_hydraulic_xor_passes_one_inlet_overflows_two():
    g = WaterGraph()
    g.add_node("a", elev=5, volume=2)
    g.add_node("b", elev=5, volume=2)
    g.add_node("jx", elev=2, kind="xor")
    g.add_node("down", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("pa", "a", "jx", cap=2)
    g.add_pipe("pb", "b", "jx", cap=2)
    g.add_pipe("pj", "jx", "down", cap=4)
    g.close("pb")
    g.tick()
    assert g.volume("down") == 2, "single inlet passes the XOR junction"
    # both inlets now -> junction overflows, nothing new reaches down
    g.nodes["a"].volume = 2
    g.open("pb")
    g.tick()
    assert g.volume("down") == 2, "XOR: both inlets -> overflow, no delivery"


def test_steam_condenses_at_highest_cold_node():
    g = WaterGraph()
    g.add_node("kettle", elev=1, volume=3)
    g.add_node("low_cold", elev=4, kind="cold")
    g.add_node("high_cold", elev=7, kind="cold")
    g.boil("kettle", 3)
    assert g.volume("kettle") == 0 and g.nodes["kettle"].steam == 3
    g.tick()
    assert g.volume("high_cold") == 3, "steam rises past the low cold to the highest"
    assert g.nodes["kettle"].steam == 0


def test_deterministic_same_ticks_same_state():
    import json

    def run():
        g = _graph()
        g.add_pipe("a", "source", "work", cap=2)
        g.add_pipe("b", "work", "out", cap=1)
        for _ in range(5):
            g.tick()
        return g.to_spec()
    assert json.dumps(run(), sort_keys=True) == json.dumps(run(), sort_keys=True), (
        "same inputs must produce byte-identical states")


def test_roundtrip_spec():
    from mag.water_graph import from_spec
    g = _graph()
    g.add_pipe("a", "source", "work", cap=2, siphon=False)
    g.tick()
    spec = g.to_spec()
    g2 = from_spec(spec)
    assert g2.to_spec() == spec, "spec roundtrip must be exact"


def test_spec_roundtrip_preserves_siphon_primed_state():
    """LW5 from_spec fix, pinned: to_spec emits `primed` but from_spec never
    passed it to add_pipe — a primed siphon silently reverted to unprimed on
    every spec roundtrip (estate_water_graph_tick included)."""
    from mag.water_graph import from_spec
    g = _graph()
    g.add_node("barrel", elev=4, volume=3)
    g.add_node("cistern", elev=0)
    g.add_pipe("sip", "barrel", "cistern", cap=2, siphon=True, crest=2)
    g.tick()                                    # primes at crest (3 >= 2), flows
    assert g.pipes["sip"].primed is True
    spec = g.to_spec()
    g2 = from_spec(spec)
    assert g2.pipes["sip"].primed is True, "roundtrip must not drop primed state"
    assert g2.to_spec() == spec, "primed must survive a second roundtrip too"


# ---- LW5 negative-volume law (2026-09-29): deferred inflow reserves at probe


def test_shared_source_gated_inflows_never_go_negative():
    """LW5 deferred-inflow double-count, minimal repro: two pipes from ONE
    source into gated junctions each probed the FULL source volume
    (_available is a no-commit probe), then the gate phase decremented src
    once per deferred entry — 3 units spent twice, tank at -3. The deferred
    flow must leave the source at probe time so sibling pipes cannot
    re-spend it."""
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=3)
    g.add_node("j1", elev=2, kind="xor")
    g.add_node("j2", elev=2, kind="xor")
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("p1", "tank", "j1", cap=3)
    g.add_pipe("p2", "tank", "j2", cap=3)
    g.tick()
    assert g.volume("tank") == 0, "units leave the source ONCE, not once per pipe"
    assert all(n.volume >= 0 for n in g.nodes.values()), "no node may go negative"
    assert g.volume("j1") == 3, "first pipe in insertion order carries the water"


def test_deferred_then_plain_from_same_source_never_negative():
    """Same double-count via a plain pipe: the deferred probe (insertion
    order first) saw the full volume, the plain _move drained what was left,
    then the gate commit decremented the deferred flow again -> -5."""
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=5)
    g.add_node("jx", elev=2, kind="xor")
    g.add_node("pool", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("pa", "tank", "jx", cap=5)       # deferred first by insertion order
    g.add_pipe("pb", "tank", "pool", cap=5)     # plain move, same tick
    g.tick()
    assert g.volume("tank") == 0, "the deferred reservation drains the tank once"
    assert all(n.volume >= 0 for n in g.nodes.values()), "no node may go negative"
    assert g.volume("jx") == 5 and g.volume("pool") == 0, (
        "insertion order decides which pipe spends the shared volume")


def test_no_negative_volume_across_seeded_random_graphs():
    """The LW5 law as a property: 1000 seeded random graphs (mixed kinds,
    siphons, closed valves, colliding sources), 1-6 ticks each — negative
    volume NEVER occurs, and the V5 economy law holds (tick conserves
    volume+steam; waste is a basin, never a void)."""
    import random
    for seed in range(1000):
        rng = random.Random(seed)
        g = WaterGraph()
        names = [f"n{i}" for i in range(rng.randint(3, 8))]
        for n in names:
            g.add_node(n, elev=rng.randint(0, 9),
                       kind=rng.choice(["plain", "plain", "xor", "sill",
                                        "cold", "waste"]),
                       sill=rng.randint(1, 3), volume=rng.randint(0, 6))
        for i in range(rng.randint(2, 10)):
            a, b = rng.sample(names, 2)
            g.add_pipe(f"p{i}", a, b, cap=rng.randint(1, 4),
                       siphon=rng.random() < 0.3, crest=rng.randint(1, 4),
                       open_=rng.random() < 0.8)
        total0 = sum(n.volume + n.steam for n in g.nodes.values())
        for _ in range(rng.randint(1, 6)):
            g.tick()
        for n in g.nodes.values():
            assert n.volume >= 0, f"seed {seed}: {n.name} volume went negative"
            assert n.steam >= 0, f"seed {seed}: {n.name} steam went negative"
        total1 = sum(n.volume + n.steam for n in g.nodes.values())
        assert total0 == total1, f"seed {seed}: economy lost {total0 - total1} units"


# ---- AC2 pipe-fracture law (2026-09-30): full-bore stress -> burst -> spray
# spec: watch/inbox/last_mile_20260930/AD1_FRACTURE.md (the AC2 mission text;
# AC2_DESIGN.md was never on disk this session).


def test_stress_accumulates_only_at_full_bore():
    """flow == cap loads the pipe; partial flow loads nothing."""
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=10)
    g.add_node("pool", elev=2)
    g.add_node("sump", elev=0)
    g.add_pipe("p_main", "tank", "pool", cap=3)
    g.tick()                                   # flow 3 == cap
    assert g.pipes["p_main"].stress == 3
    g.nodes["tank"].volume = 2
    g.tick()                                   # flow 2 < cap
    assert g.pipes["p_main"].stress == 3, "partial flow must not stress"
    assert not g.pipes["p_main"].fractured


def test_fracture_fires_exactly_at_threshold():
    """cap 1, fresh pipe: one stress per tick; the burst lands the tick
    stress EXCEEDS the threshold, with the exact event grammar and the
    final tick's unit sprayed to the lowest-elev node other than dst."""
    t = fracture_threshold("burst")
    assert 200 <= t <= 400
    g = WaterGraph()
    g.add_node("tank", elev=9, volume=10_000)
    g.add_node("pool", elev=5)
    g.add_node("sump", elev=0)
    g.add_pipe("burst", "tank", "pool", cap=1)
    fired: list[str] = []
    for _ in range(t + 1):
        fired = [e for e in g.tick() if "FRACTURES" in e]
        if fired:
            break
    assert fired == [f"Pipe burst FRACTURES (stress {t + 1}): spray to sump."]
    assert g.pipes["burst"].fractured and not g.pipes["burst"].open
    assert g.pipes["burst"].stress == t + 1
    assert g.volume("pool") == t, "t pre-burst ticks delivered; the burst tick did not"


def test_fracture_threshold_is_deterministic_per_pipe():
    """200 + hash(name) % 201 (B1 2026-09-30): stable across calls, in the
    [200, 400] VOLUME band (cumulative throughput — a cap-1 pipe bursts in
    200-400 ticks of sustained full bore), and names spread (zero RNG —
    same name, same threshold, every call)."""
    assert fracture_threshold("alpha") == fracture_threshold("alpha")
    assert all(200 <= fracture_threshold(f"pipe_{i}") <= 400 for i in range(64))
    assert len({fracture_threshold(f"pipe_{i}") for i in range(8)}) > 1


def test_fracture_conserves_volume_and_valve_cannot_reopen():
    """One-shot burst (cap = threshold + 1 fractures on tick 1): dst gets
    nothing, the spray lands at the lowest-elev node, the economy is
    conserved, and g.open() refuses the reopen forever."""
    cap = fracture_threshold("one_shot") + 1
    g = WaterGraph()
    g.add_node("tank", elev=9, volume=cap + 7)
    g.add_node("pool", elev=5)
    g.add_node("sump", elev=0)
    g.add_pipe("one_shot", "tank", "pool", cap=cap)
    total0 = sum(n.volume + n.steam for n in g.nodes.values())
    events = g.tick()
    assert g.pipes["one_shot"].fractured
    assert g.volume("pool") == 0, "burst tick sprays; dst receives nothing"
    assert g.volume("sump") == cap, "the spray volume lands somewhere"
    assert any("FRACTURES" in e for e in events)
    assert sum(n.volume + n.steam for n in g.nodes.values()) == total0
    g.nodes["tank"].volume = 5
    g.open("one_shot")                         # valve verb path: refused
    g.tick()
    assert not g.pipes["one_shot"].open
    assert g.volume("pool") == 0 and g.volume("sump") == cap


def test_spec_roundtrip_preserves_stress_and_fractured():
    """to_spec/from_spec must carry the AC2 fields — a burst pipe survives
    the estate roundtrip closed, and partial stress survives with it."""
    from mag.water_graph import from_spec
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=9)
    g.add_node("pool", elev=2)
    g.add_node("sump", elev=0)
    g.add_pipe("carry", "tank", "pool", cap=2)
    g.tick()
    g.tick()
    assert g.pipes["carry"].stress == 4        # 2 full-bore ticks
    g2 = from_spec(g.to_spec())
    assert g2.pipes["carry"].stress == 4
    assert g2.pipes["carry"].fractured == g.pipes["carry"].fractured is False
    burst = WaterGraph()
    burst.add_node("tank", elev=9, volume=999)
    burst.add_node("pool", elev=5)
    burst.add_node("sump", elev=0)
    burst.add_pipe("one_shot", "tank", "pool", cap=fracture_threshold("one_shot") + 1)
    burst.tick()
    assert burst.pipes["one_shot"].fractured
    b2 = from_spec(burst.to_spec())
    assert b2.pipes["one_shot"].fractured and not b2.pipes["one_shot"].open


# ---- B1 FRACTURE-REACH (2026-09-30, watch/inbox/last_mile_20260930/
# B1_FRACTURE_REACH.md): cumulative-VOLUME law (stress += flow at full
# bore, threshold 200 + hash%201 = [200, 400] volume units) AND the gated-
# inlet seam fix — full-bore flow INTO a gated junction stresses the pipe
# at probe time, so the default Mountain's main artery can burst.


def test_gated_inlet_stresses_at_full_bore():
    """B1 seam fix: a pipe feeding a gated junction at flow == cap loads
    stress at PROBE time (the water left the source through the pipe
    section). The AC2 cut loaded pipes only in _move, so gated inlets never
    stressed — the default Mountain's p_spring could NEVER fracture."""
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=5)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("pool", elev=0)
    g.add_pipe("p_gate", "tank", "gate", cap=2)
    g.add_pipe("p_out", "gate", "pool", cap=2)
    g.tick()                                   # probe 2 == cap into the xor
    assert g.pipes["p_gate"].stress == 2, "gated inlet full bore must stress"
    g.nodes["tank"].volume = 1                 # partial flow loads nothing
    g.tick()
    assert g.pipes["p_gate"].stress == 2


def test_gated_inlet_bursts_at_probe_and_sprays():
    """A pre-stressed gated inlet bursts ON the probe; the gate never sees
    THAT tick's inlet (sole-inlet xor keeps its earlier pooled water), the
    flow sprays to the lowest node other than the junction, and the burst
    pipe stays closed."""
    from mag.water_graph import fracture_threshold as ft
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=9)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("sump", elev=0)
    g.add_pipe("p_gate", "tank", "gate", cap=3)
    # stress exactly one full-bore tick below the burst: threshold t,
    # stress t-3; next probe adds 3 -> t (== t does NOT burst; strict >).
    g.pipes["p_gate"].stress = ft("p_gate") - 3
    g.tick()
    assert not g.pipes["p_gate"].fractured
    assert g.pipes["p_gate"].stress == ft("p_gate")
    assert g.volume("gate") == 3                # tick 1 delivered through the gate
    g.nodes["tank"].volume = 9
    events = g.tick()
    assert g.pipes["p_gate"].fractured and not g.pipes["p_gate"].open
    assert (f"Pipe p_gate FRACTURES (stress {ft('p_gate') + 3}): "
            f"spray to sump.") in events
    assert g.volume("gate") == 3, "burst tick's flow never reaches the gate"
    assert g.volume("sump") == 3 and g.volume("tank") == 6  # conserved (fed 9+3)


def test_default_mountain_sustained_full_bore_fractures_in_window():
    """The B1 reach law's acceptance: the DEFAULT Mountain board (game.gd
    POOL_LAYOUT / server.world.build_mountain_graph shape, all pipes cap 1)
    under sustained full-bore — a fed source refills the inlet each tick
    (the AJ4 playtest instrument) — fractures EVERY pipe within 200-400
    ticks, deterministically (identical rerun)."""
    def board():
        g = WaterGraph()
        g.add_node("spring", 10, "plain", 0, 6)
        g.add_node("terrace", 6)
        g.add_node("gate1", 5, "xor")
        g.add_node("hollow", 3, "plain", 0, 2)
        g.add_node("waste", 0, "waste")
        g.add_node("crown", 14, "cold")
        g.add_pipe("p_spring", "spring", "gate1", 1)
        g.add_pipe("p_terrace", "terrace", "gate1", 1)
        g.add_pipe("p_out", "gate1", "hollow", 1)
        g.add_pipe("p_drain", "hollow", "waste", 1)
        g.add_pipe("p_bypass", "spring", "terrace", 1, True, 2, False)
        return g

    for target, feed, open_bypass in [("p_spring", "spring", False),
                                      ("p_terrace", "terrace", False),
                                      ("p_out", "spring", False),
                                      ("p_drain", "hollow", False),
                                      ("p_bypass", "spring", True)]:
        bursts = []
        for _ in range(2):                      # determinism: identical rerun
            g = board()
            if open_bypass:
                g.open("p_bypass")              # player valve verb (starts shut)
            burst_at = None
            for tick in range(1, 2001):
                g.nodes[feed].volume = 10       # sustained full-bore source
                if any(target in e and "FRACTURES" in e for e in g.tick()):
                    burst_at = tick
                    break
            bursts.append(burst_at)
        assert bursts[0] == bursts[1] is not None, target
        assert 200 <= bursts[0] <= 400, f"{target}: {bursts[0]} outside window"
