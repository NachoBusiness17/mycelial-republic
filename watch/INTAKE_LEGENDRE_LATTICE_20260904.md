# INTAKE CARD — @mathemetica lattice distances / √7 impossibility (2026-09-04)

**Paste**: https://x.com/mathemetica/status/2095814176837161388
**Score**: 15/25 — **BUILD WINDOWED** (small, rides existing surfaces)
**Math verified by hand before filing**: distance on the 3D integer lattice is
√(x²+y²+z²); Legendre's three-square theorem says n is a sum of three squares
iff n is NOT of the form 4^a(8b+7). 7 = 4⁰(8·0+7) → excluded → √7 impossible;
14 = 1+4+9 → √14 lives. Tweet's math is correct.

## Why it matters here (math-viz genre rule: wireable + consumer)
- **Wireable**: it's a DISTANCE-METRIC INVARIANT for every lattice space we
  run — maze_arena cells, voxel/mesh-baker grids, B1 field samples on integer
  coords. On-grid straight-line distances can ONLY be √(non-4^a(8b+7)).
  √7, √15, √23, √28, √31, √39… never appear between lattice points. That's
  a falsifier-class constraint: if a rendered "on-grid" distance measures √7,
  the grid is broken (or the space isn't Z³).
- **Consumers** (all existing organs, no new substrate):
  1. B1/maze_arena: gate/cheese placement law — cursed distances as a
     teaching beat ("some doors can never be exactly 7 steps away").
  2. mesh-baker: free sanity assertion — lattice-distance validator on
     parsed GLB voxel coords (one function, zero deps).
  3. dungeon: the amnesiac wizard's number-magic — numbers that refuse to
     live in three perpendicular directions is a ready-made room.

## Axes
FIT 4 (bolts onto arena/mesh-baker/dungeon directly) · PULL 2 (B1 v1 skin
catalog, teaching shelf) · COST 5 ($0, hand-verified) · WINDOW 2 (nothing
starved; one-function consumers when B1 v1 opens) · NOVELTY 3 (three-square
family absent from corpus; the 2D version — two squares — not filed either).

## Routing
1. **BUILD WINDOWED**: `lattice_distance_validator` — one function + one
   assertion in mesh-baker's parser test set; rides the next mesh-baker
   session. Dungeon gate-placement note parked with the teaching panels.
2. **REMEMBER**: sum-of-squares impossibility families (three squares:
   4^a(8b+7); two squares: primes 3 mod 4) = the shelf's "impossible
   distances" pair. Fist-and-Latimer for gate magic.

Tri-state: theorem Supported (hand-verified + classical); tweet framing
correct; build value Unproven until the validator asserts on a real GLB.
