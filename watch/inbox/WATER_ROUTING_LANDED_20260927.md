# WATER ROUTING LANDED — the physics build — 2026-09-27

Operator question that ordered this: "why doesn't our water routing work, is
that a sacred cow, I really think it's useful using the physics instead of
fighting them." Answered in-thread: not a sacred cow — under-built (the
entire routing graph was VALVE_AT = two valves on one fixed line). This
window lands the physics.

## What landed

1. **mag/water_graph.py** — the flow-graph engine (generalizes
   hydro_xor_sim's real laws to an arbitrary graph):
   - Nodes: integer elevation + volume; kinds plain | xor | sill | cold |
     waste. Pipes: one-way check valves (never uphill, by construction),
     integer capacity, optional SIPHON with crest volume (primes at crest,
     breaks when the intake dries — hydro_xor_sim semantics, integerized).
   - Junctions as gates: XOR delivers only on exactly-one inlet (both →
     overflow to waste — the hydraulic XOR); SILL delivers at threshold
     (hydraulic AND); plain/cold/waste as expected.
   - Steam as a second routing medium: `boil()` lifts volume to steam; it
     ignores pipes entirely and condenses at the highest `cold` node.
   - Deterministic: insertion-ordered pipes, integer volumes, no floats,
     no RNG; three-phase tick (condense → plain/deferred inflows → gate
     evaluation + gated outflow). Spec roundtrip via to_spec/from_spec.
   - First cut had a real design bug the tests caught: gated-junction
     OUTFLOW ran in the same pass as its inflows, so the XOR delivered on
     both-inlet ticks. Restructured to deferred inflows + gate evaluation
     + gated outflow. (Also fixed two test bugs of mine: a pipe addressed
     as a node, and a mis-seeded XOR case.)

2. **tests/test_water_graph.py (7)**: gravity-only-when-open, never-uphill,
   siphon prime/break, hydraulic XOR pass/overflow, steam-to-highest-cold,
   byte-determinism, spec roundtrip. **Water family 14/14** with the legacy
   water_computer suite (its 3-tank mode untouched — the regression suite
   for the old path). RATCHET PASS.

3. **The granted shape_map family extension LANDED** (from the attic
   census): FAMILY_CLAIMS in mag/shape_map.py — verkle_chain claims the
   archived knot family (4 rules: relocated knots/, by-session pointers,
   chain+tip snapshots). The Mimosa hook-state blob and ghost leak-report
   stream stay deliberately UNCLAIMED per the operator's fork. shape()
   re-verified live (8,040 chain leaves, fresh root).

## The demo (hydraulic logic, run live)

SOURCE feeds two routes to OUT: an XOR junction (two feeders) and a SILL
junction (two inlets = hydraulic AND). Three ticks: the AND route delivered
2/tick; the XOR route refused both-inlet ticks and overflowed — the physics
IS the logic gate. Close one XOR feeder and it passes. Water is now a wire.

## Owed (small, named)

- Campaign integration: water_computer can seed a graph spec and delegate
  gravity_tick; verbs exist (open/close by pipe name). Not wired into the
  campaign JSON yet — next window or on play demand.
- Steam nodes need a campaign surface (boil verb already exists in the
  module layer for the legacy path).
