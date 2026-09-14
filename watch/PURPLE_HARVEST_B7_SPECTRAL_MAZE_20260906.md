# PURPLE HARVEST B7 — SPECTRAL MAZE receipt (2026-09-06)

Builder: zcode seat (B7 lane) · design spec: `watch/SELF_STEAL_LIGHT_MAZE_SPECTRAL_20260906.md`
(band-ladder audit → formula→mechanic map → B7 launch) · siblings B1-B6 are separate
builders and separate files (no clobber).

## Shipped

- **Surface:** `dashboard/static/spectral_maze.html` (NEW, 832 lines, single file, house
  conventions: dark field, errbanner fixture on `window.onerror` + `unhandledrejection`,
  nav.js include, marker-delimited pure-math core at lines 32-666
  (`/*__SPECTRAL_CORE_BEGIN__…END__*/`), offscreen ImageData rendering with smoothing
  off, rAF loop, keyboard controls, debug/falsifier strip, R = new maze).
- **Nav wiring:** `dashboard/static/nav.js` LINKS entry
  `["/static/spectral_maze.html", "Spectral Maze"]` (line 65, after Eraser Maze).
  Backup at `nav.js.bak-b7-spectral-20260906`. `node --check` clean.
- **Harness:** `watch/PURPLE_HARVEST_B7_harness_20260906.mjs` — slices the marker core,
  evals it in Node (the tested code IS the shipped code), drives all six falsifiers with
  INDEPENDENT re-implementations of the reference solver, descent path, Fermat
  prediction, and Snell scan; then boots the FULL page script under a DOM stub and drives
  the real game loop (B5 pattern). `ALL FALSIFIERS PASS`, stable across repeated runs.
- **Receipt:** this file.

## What was built (file:line, spectral_maze.html)

- **Three real bands:** R 680nm / G 532nm / B 450nm (`LAMBDA_NM`, k_R < k_G < k_B via
  `KWAVE`). One independent field per band: `T[b]` (Float64 arrival time) + `A[b]`
  (Float32 carried amplitude), same grid (81×49 game; makeField:49-79).
- **Per-band refractive zones:** `N_TAB` = vacuum 1.00, glass [1.44,1.53,1.62], water
  [1.331,1.333,1.340], crystal [1.30,1.45,1.66] (dispersing prism zones), plus a 2.00
  test slab for the Snell bench. Cost per cell = n(zone,band) — see the convention note
  below. Solver: `solveBand` (line 99), one binary-heap Dijkstra per band, preallocated
  (no build-time allocations; heap-cap tripwire exposed and asserted clean).
- **Open-field propagation is a first-order Godunov eikonal update** (line 150):
  `T = min(a,b)+s` one-sided, `(a+b+sqrt(2s²−(a−b)²))/2` diagonal branch, on the 4-axis
  stencil — i.e. a Dijkstra-swept FMM. Structure edges (mirror relay, guide
  entry/exit/leak) stay explicit additive edges on the 8-neighborhood.
- **Mirror walls:** wall tiles with `kind=MIRROR` + axis (`maxis`). When relaxed from
  open cell u, mirror v relays the flood to its 8-neighbors on the SAME SIDE as u only
  (sign test against the mirror axis), band-independent ×0.90 gain (line 156-178).
- **TIR waveguides:** wall-cell polylines (`addGuide`, line 87). Guide edges exist only
  along the polyline; ends accept/emit light from adjacent open cells (coupling 0.95);
  per-tile loss 0.995; at a kink tile the band-dependent leak fraction
  `leakFrac = 1−(θ_c/θ)²` (θ_c = π−2·asin(n_clad/n_core[b])) is applied: carried amp ×
  (1−leak), leak amp booked to `leakSum` (post-pass, lines 200-208).
- **Sensors + win:** `placeSensors` (line 394) ranks open cells near guide ends and
  leak bends by their strongest band's amplitude; lit threshold 0.35; win = step on a
  lit sensor (checked per frame). Generation retries up to 40 worlds, keeping the best.
- **Filter:** TAB/E cycles ALL → RED 680 → GREEN 532 → BLUE 450; masked channels render
  at 12%. Composite: `P = A/(1+0.08T)²` per band → RGB channels (compositeInto, 233).
- **Zones/mirrors/guides generation:** braided maze (house pattern from eraser_maze B2,
  credited), 3 dispersing blobs, 5 axis-aligned mirror runs, up to 4 kinked guide
  polylines (axis + period-3 stair runs, kinks 26.6°-90°) with straight-guide fallback
  (genWorld, line 263).

## The discrete rules, stated plainly (grid approximations)

1. **Mirror i=r is a same-side relay, not angular reflection.** A mirror tile returns
   the flood to every open neighbor on the incident side (including retro and
   wall-parallel hops) — a superset of the specular direction. The falsifier therefore
   tests the law that actually matters: the relay rule is exactly symmetric under
   reflection about the mirror line, so the flood past a mirror equals the mirrored
   flood of the mirrored source. Measured: **max |ΔT| = 0.0** (bit-identical), and the
   far side stays dark.
2. **TIR bends are judged over a 6-tile window per side.** The bend angle at a guide
   tile is the angle between (tile − tile[−6]) and (tile[+6] − tile). A 6-window spans
   exactly two periods of a period-3 stair run, so the fine angles (26.57°, 63.43°)
   measure wobble-free; axis runs measure exactly. Interior tiles read partial bends;
   the junction tile reads the full kink.
3. **TIR leak is a smoothed Fresnel-style rule, not binary.** Real TIR is a step at the
   critical angle; the game grades it: leak = max(0, 1−(θ_c/θ)²), so bends slightly past
   a band's critical angle leak a little and steep kinks leak more, in band order. This
   is what makes one kink a demultiplexer.
4. **Cost convention CORRECTED from the card.** The B7 card wrote "cost = 1/n per cell".
   That inverts the physics: with 1/n, glass is faster than vacuum and the emergent law
   would be sin i/n₁ = sin r/n₂. Eikonal travel time is ∫n ds, so the shipped cost is
   n per cell (vacuum 1). This is the version the falsifier n₁sin i = n₂sin r checks.
   The card's own falsifier wins over the card's formula.
5. **Amplitude bookkeeping is max-at-equal-time.** Where several least-time paths tie,
   the cell keeps the max arriving amplitude — approximate (±few % on leak fractions),
   documented where it matters (F7(3) numbers).

## The deep find, verified: Fermat-in-the-cost-field — with two catches

The card's claim "Snell emerges from the flood, do not code Snell separately" is TRUE,
but only after two fixes the build surfaced:

- **Graph-path metrics cannot show Snell at shallow angles.** With 8- (or any fixed-
  neighborhood) graph Dijkstra, the distance metric is piecewise-linear in the crossing
  height, so the least-time crossing always snaps to a metric sector edge or to
  bang-bang (all vertical travel migrates into the cheaper medium). Measured before the
  fix: incidence angle 0.0° for every target — the ray hugged the boundary. Grid
  refinement does NOT cure this (sector angles don't change with h). The cure is the
  Godunov update, whose diagonal branch interpolates between neighbors: all-angle
  characteristics, and Snell becomes measurable.
- **Small-angle refraction is genuinely unresolvable at h=1 — say so.** For the first
  Snell world (n=1.5 slab, incidence 9-22°), the continuous Fermat gain over the
  bang-bang path was ~0.3-0.5 time units while the scheme's own error over 50 cells is
  ~1.0: the field cannot and did not resolve it (measured, not assumed). The shipped
  Snell bench therefore works in the resolvable regime: n=2.0 slab, legs 62,
  incidence ~21/24/26°, where the Fermat gain (8-16) dwarfs the scheme error (~2.5).
  Honest limit: at small angles the honest answer is "the flood does not resolve Snell
  here" — a labeled failure we chose to design around rather than hide.

## Falsifiers — PASS (measured, Node 22 harness on shipped code)

| # | Falsifier | Result | Numbers |
|---|---|---|---|
| F7(1) | Monochrome regression | **PASS** | shipped flood vs independent Godunov reference: maxDiff **0.0** (bit-identical); band-equality in a dispersion-free world: **0.0** |
| F7(2) | Snell check | **PASS** | measured r vs continuous Fermat: err **1.07° / 6.66° / 3.71°** at incidence ~21/24/26° (3/3 within 8° grid tolerance); n₁sin i − n₂sin r = 0.065 at the best ray |
| F7(3) | TIR + dispersion-split criticals | **PASS** | shallow 26.6° kink: leak R/G/B = **0.000/0.000/0.000**, carried 0.707 each; sharp 90° kink: leak **0.923/0.902/0.739** (all bands leak, ordered R>G>B); demux 63.4° kink: leak **0.844/0.329/0.000**, carried 0.048/0.444/0.707 (red drops, blue holds) |
| F7(4) | Mirror symmetry | **PASS** | mirror-world vs mirrored twin-world: max |ΔT| **0.0**; far side dark (no leakage) |
| F7(5) | Perf | **PASS** | 3-band build = **1.63ms**, single band **0.53ms**, ratio **3.09×** (floor is exactly 3× = three solves; gate ≤3.5 guards superlinear blowup — none); render hot path median **0.085ms**, p95 0.154ms (budget 8ms) |
| F7(6) | Per-band visibility strip | **PASS** | demux corridor output shares: leak port **0.719/0.281/0.000** (red-dominant), carry port **0.040/0.370/0.590** (red-free) |

Plus: page-strip self-test (`runFalsifiers`) passes all six on-page (6 PASS / 0 FAIL);
full-page boot under DOM stub: no throws, falsifier strip populated, ≥1 lit sensor at
boot, deterministic rebuild (byte-identical T/A), Tab/E filter cycling, movement gating,
R reseed, lit-sensor win fires and dark-sensor win correctly blocked, no heap-cap trip.

## What was verified vs not (honest tape)

- **VERIFIED (Node 22, exact shipped code):** all of the above. The harness's reference
  solver, descent, ternary-search Fermat prediction, and boundary scan are independent
  re-implementations, and the core's own scan agrees with the harness scan to 0.0000
  median difference. Game-logic layer exercised through the real loop (frames, keys,
  win conditions, rebuild determinism).
- **NOT VERIFIED (no browser on this seat):** pixels, 60fps under real compositor load,
  keyboard feel, the visual read of color fringing at glass edges. Error-banner fixture
  is in place per house convention; every frame()-reachable code path ran in the stub
  except canvas draw calls (stubbed no-ops) — logic verified, pixels not.
- **Known honest limits (measured, not hidden):** the wavefront-normal scan across the
  boundary shows a systematic |n₁sin i − n₂sin r| median of 0.148 — the first-order
  scheme's near-interface gradient bias; the descent-vs-Fermat table is the falsifier,
  the scan is printed as a diagnostic on-page. Small-angle refraction (few degrees) is
  unresolvable at h=1 in ANY fixed-graph flood — the bench geometry avoids that regime
  by design. The prism-ridge corridor (deviation of a point-source beam) was abandoned:
  least-time paths hug the slow medium's edge, so "beams" don't cast like ray diagrams;
  the demux corridor replaced it.

## Files

- `dashboard/static/spectral_maze.html` (new, 832 lines, single file)
- `dashboard/static/nav.js` (one LINKS line; backup `nav.js.bak-b7-spectral-20260906`)
- `watch/PURPLE_HARVEST_B7_harness_20260906.mjs` (falsifier harness)
- `watch/PURPLE_HARVEST_B7_SPECTRAL_MAZE_20260906.md` (this receipt)

Console access: `window.__SPECTRAL_CORE` (field core + probes) and
`window.__SPECTRAL_GAME` (buildWorld / cycleFilter / state) for on-surface poking.

*Lineage: the band-ladder audit said we were band-zero — one scalar with wave
decoration, a light maze a month before it earned the word. B7 ships the band axis:
three wavelengths, three floods, one grid; glass that bends blue more than red; a
single kink that sorts red from blue. And the oldest formula in the sheet was already
in the walls — Fermat was here first. He just needed the price to change.*

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran the shipped harness fresh: EXIT=0, 30 PASS / 0 FAIL, every number
reproducing — monochrome regression 0.0, Snell errors 1.07°/6.66°/3.71° (3/3 in
tolerance), TIR leak ordered R>G>B with the 63.4° demux kink dropping red (0.844)
while holding blue (0.000), mirror symmetry 0.0, 3-band build 2.97× (floor 3×,
no blowup), render 0.12ms median, full-page stub boot driving filter cycling,
movement gating, reseed determinism, and both win conditions. Nav wired at
nav.js:65, backup present. **The card's "cost = 1/n" was inverted — the builder
caught the seat's spec error with the seat's own falsifier** (eikonal time is
∫n ds; shipped cost = n), and the graph-metric Snell limitation (bang-bang rays
at shallow angles) was fixed at the solver level (Godunov diagonal branch) with
the small-angle regime labeled unresolvable rather than hidden. Second time today
the falsifier has caught the analyst. VERDICT: PASS. Pixels remain the family's
one open eye.
