# WF - WATER WAVE SYNTHESIS (lane 6/6, 2026-09-30)

## The answer
water_graph.py is a logic circuit in a wetsuit. Its own docstring says so: built to generalize "the family's real laws" - check valves, XOR/sill gates, siphon crests - legality, not fluids. Evidence: head is a boolean (`src.elev > dst.elev`), flow is integer `min(cap, volume)`, nodes have volume but no shape (no depth, no pressure, no momentum, no surface), steam teleports to the highest cold node. Each tick renders a verdict on *who delivered*, never *how fluid moves*. It is verdict physics, not fluid physics - deliberately, because "no floats, no RNG" is what lets server/world.py promise byte-identical hash-chained logs.

## The ladder
1. **Graded head + node geometry** (cross-section -> depth; head = elev+depth; flow prop. to dHead in fixed-point). Unlocks pools that visibly fill, equalize, backwater; meter: mm of depth.
2. **Field layer** (heightfield sheet-flow to lowest neighbors). Water finds its own paths - no hand-placed pipes; meter: wetted cells.
3. **Particles** (droplets with position+velocity riding the field). Splash, spray, drifting steam, carried tokens; meter: particles/tick at 60 FPS.
4. **Erosion/sediment** (capacity by velocity; carve and deposit). The mountain remembers - channels, deltas, shifting courses; meter: rock units moved.
5. **Full hydraulics** (momentum, surge, emergent siphons, water hammer). Burst dams as puzzles - a true hydraulic analog computer; meter: Bernoulli residual per tick.

## The first build
Rung 1 in water_graph.py: replace the boolean head test in _available/_move with fixed-point dHead over node cross-sections (~20 lines, no floats - determinism law intact), plus depth-tint in the Godot view. Every later rung hangs off a continuous head; this is the hinge, most water-feel per line.

## The name
**mag/hydrology.py - "The Watershed."** water_graph stays the verdict layer; the Watershed owns the water.

## WC companion (river-bend steal, filed here because siblings' dir arrived late)
sael.net/river-bend implements the Ikeda-Parker-Sawai bend-migration model: near-bank velocity from curvature, bank erosion by excess shear (1.35 m/s threshold), point-bar deposition, helical flow, oxbow cutoffs, scroll bars that revegetate. Alive-ness = time-layers (the river writes its own history). Estate version: add `silt` as a second integer per node; erosion = volume-transfer above a sill-style threshold (move 1 silt + 1 elev-unit to the lowest neighbor); deposition below it; meanders emerge as the flow-path re-solves. Mountain payoff: rivers that carve the board as you play - every session leaves oxbow scars the next inherits.
