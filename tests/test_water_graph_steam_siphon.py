"""steam + siphon corner pins - the weather medium and the dry-spell
hysteresis (mariner cycle 7, 2026-10-13).

Two corners the persona named and no test had forced: (1) the steam lift
is a second routing medium that crosses a CLOSED valve without opening
it: boil at a sealed source, condense at the cold crown, drain on: the
sealed pipe never moves and never leaks. (2) the siphon break lives in
the _move path only, so a siphon feeding a GATED junction is probed
through _available, which delivers 0 on a dry intake but never breaks
the prime: the gate-side siphon holds its crest across dry spells and
delivers a below-crest refill when water returns, while the same siphon
into a plain dst breaks on the first dry tick and refuses the refill.
The dry-spell hysteresis belongs to the dst kind, not the pipe. Spec:
mag/water_graph.py module docstring, Pipes + Steam bullets; receipt
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


def test_steam_bypasses_a_closed_valve():
    """The weather route (probe S1, traced): src holds 3 units and its
    only pipe out is CLOSED (p_closed, never opened). boil(src, 3)
    empties the tank into steam; t1 condenses all 3 at the cold crown
    (elev 8, above the sealed pipe's whole world) and cs starts
    draining 1/tick to sink2 (t1-t3). The sealed pipe carries zero
    bytes forever: sink stays 0, no event ever names p_closed, and the
    valve is still shut at close (open() law untouched). End: src 0/0,
    sink 0, crown 0, sink2 3, conserved 3. The water escaped as
    weather: the lift ignores pipes entirely; a closed valve seals its
    pipe, not the sky."""
    g = WaterGraph()
    g.add_node("src", elev=5, volume=3)
    g.add_node("sink", elev=1)
    g.add_node("crown", elev=8, kind="cold")
    g.add_node("sink2", elev=2)
    g.add_pipe("p_closed", "src", "sink", cap=1, open_=False)
    g.add_pipe("cs", "crown", "sink2", cap=1)
    assert g.boil("src", 3) == 3
    assert g.volume("src") == 0 and g.nodes["src"].steam == 3
    ev1 = g.tick()
    assert ev1 == ["Steam condenses at crown (+3).",
                   "cs: 1 crown->sink2."], ev1
    ev2 = g.tick()
    assert ev2 == ["cs: 1 crown->sink2."], ev2
    ev3 = g.tick()
    assert ev3 == ["cs: 1 crown->sink2."], ev3
    assert g.tick() == []
    assert g.volume("sink") == 0, "the sealed pipe never carried a unit"
    assert g.volume("sink2") == 3 and g.volume("crown") == 0
    assert g.nodes["src"].volume == 0 and g.nodes["src"].steam == 0
    assert g.pipes["p_closed"].open is False
    assert _total(g) == 3


def test_siphon_prime_survives_a_dry_spell_only_at_a_gate():
    """The dry-spell hysteresis, both kinds on one storm (probes S2+S3,
    traced). Gate side: a crest-3 cap-1 siphon feeds a level-2 latch
    (its outflow o drains to a sink). t1 primes at crest and the first
    charge pools ("holds pool 1 below level 2"); t2-t6 run at 1/tick
    (opens, drains, steady). t7 the intake runs dry: SILENCE, no break
    line, primed still True: _available delivers 0 on a dry intake and
    never breaks the prime (the break lives in _move). t8 a BELOW-CREST
    refill (1 unit at a crest-3 gate) is delivered anyway and the latch
    opens again: the crest is paid once per prime, not per unit. Plain
    side: the SAME siphon into a plain tank charges t1-t6, then t7
    emits "Siphon sp2 breaks (intake dry)." and primed goes False, so
    t8's identical refill is refused in silence. End: gate side src 0,
    L 1, sink 6, primed True, conserved 7; plain side P 6, primed
    False. Same pipe laws, same storm: whether the prime survives the
    dry spell is the dst kind's decision."""
    g = WaterGraph()
    g.add_node("src", elev=9, volume=6)
    g.add_node("L", elev=5, kind="latch", sill=2)
    g.add_node("sink", elev=1)
    g.add_pipe("sp", "src", "L", cap=1, siphon=True, crest=3)
    g.add_pipe("o", "L", "sink", cap=1)
    ev1 = g.tick()
    assert ev1 == ["Siphon sp primes at crest (3).",
                   "Latch L holds pool 1 below level 2; pooling."], ev1
    for _ in range(5):  # ticks 2-6: steady 1/tick through the gate
        assert g.tick() == ["sp: 1 src->L.",
                            "Latch L opens (pool 2 >= level 2).",
                            "o: 1 L->sink."]
    assert g.tick() == [], "dry intake at a gated dst: silent, prime held"
    assert g.pipes["sp"].primed is True
    assert g.volume("src") == 0 and g.volume("L") == 1
    assert g.volume("sink") == 5
    g.nodes["src"].volume = 1  # below-crest refill (crest 3)
    ev8 = g.tick()
    assert ev8 == ["sp: 1 src->L.",
                   "Latch L opens (pool 2 >= level 2).",
                   "o: 1 L->sink."], ev8
    assert g.volume("src") == 0 and g.volume("L") == 1
    assert g.volume("sink") == 6
    assert g.pipes["sp"].primed is True
    assert _total(g) == 7

    k = WaterGraph()
    k.add_node("src", elev=9, volume=6)
    k.add_node("P", elev=5)
    k.add_pipe("sp2", "src", "P", cap=1, siphon=True, crest=3)
    ev1 = k.tick()
    assert ev1 == ["Siphon sp2 primes at crest (3).",
                   "sp2: 1 src->P."], ev1
    for _ in range(5):  # ticks 2-6: same charge rhythm, plain dst
        assert k.tick() == ["sp2: 1 src->P."]
    ev7 = k.tick()
    assert ev7 == ["Siphon sp2 breaks (intake dry)."], ev7
    assert k.pipes["sp2"].primed is False
    k.nodes["src"].volume = 1  # the identical below-crest refill
    assert k.tick() == [], "unprimed, 1 < crest 3: the refill is refused"
    assert k.volume("P") == 6 and k.volume("src") == 1
    assert _total(k) == 7, "the refused refill stands at the intake"
