# MAZE ARENA B1 — shadow-field pass landed (2026-09-06, worker maze, group 2 width 8)

Built: the B1 build from watch/SHADERTOY_SHADOW_FIELDS_20260903.md — the 3-pass GPU
ray-field ported into dashboard/static/maze_arena.html, self-contained, no build step,
no external assets, $0. Backup: maze_arena.html.bak-maze-20260906.

## What changed in the file
- New WebGL module (~90 lines, additive): offscreen 480x270 GL canvas + three shader
  programs (occlusion / 1D shadow map / light render), two FBOs (256x256 occlusion,
  256x1 shadow map), wall occluder quads precomputed from the existing SDF wall list.
- frame() composites per FIELD mode: BOTH (default — BFS grid flood dimmed to 35%,
  GPU ray-field composited 'lighter' on top), RAY (bg fill + ray-field + wall outlines),
  BFS (original render, untouched). New FIELD button cycles BOTH/RAY/BFS.
- drawWalls(): faint cyan wall outlines (needed in RAY mode since the BFS layer is hidden;
  kept in all modes for crispness).
- GLSL REIMPLEMENTED from the card's description, never pasted (provenance-audit hygiene:
  the wiki carries no license, default copyright). Graceful degradation: no WebGL ->
  FIELD button hides, arena runs BFS-only.

## Algorithm mapping (the card's three passes -> this file)
1. OCCLUSION MAP 256x256, light at center: the 10 SDF walls rasterized as white quads
   (alpha 1 > 0.75 caster threshold), light-centered, LIGHT_R=190px maps to the map edge.
2. 1D SHADOW MAP 256x1: per column theta, march 256 samples outward through the occlusion
   texture, d(theta) = min normalized distance to first caster — the order-free
   min-reduction (VISIBILITY FACTORIZATION + MIN-REDUCTION laws, engine 1: ray-field).
3. LIGHT RENDER: r = dist/lightR, d(theta) via one dependent texture read (LINEAR-filtered,
   fract() hides the theta-wrap seam), lit = step(r, d(theta)), radial falloff
   smoothstep(1,0,r), and the 9-tap gaussian over neighboring angles with width
   (2pi/256)*6*smoothstep(0,1,r) — ARTIFACT-INTO-FEATURE: penumbra widens with distance.
   Light = CHEESE (amber core -> cyan #7cf5ff mid-field; amber #e8c96a cheese dot kept).

## Eyeball-verify
Open http://127.0.0.1:8765/maze_arena.html (dashboard already serves static/ — nothing
started). Default BOTH: BFS flood glows dim, cheese ray-field adds hard shadow wedges
behind walls with soft distance-widened penumbra. Click FIELD -> RAY: pure 1D radial
shadow map, walls as black occlusion wedges. Click -> BFS: the original pre-B1 render.
Falsifier surface for the card's B1 test (BFS field vs ray-field, same maze) is now
renderable side by side in BOTH mode.

## Nav
NONE NEEDED — nav.js line 55 already carries ["/static/maze_arena.html", "Maze Arena"].
Wiring worker: do not touch this file's entry.

## Limits + next
Render-only by design: walkers still read the CPU BFS field (the salon addendum's B1'
position — the ray-field earns the GPS falsifier before it steers agents). Known honest
limits inherited from the card: first-hit only, casters self-shade, rect-to-polar
distortion at grazing angles. Next step if wanted: K-ray CPU sensor on walkers reading the
same occluder set -> steps-on/steps-off measurement.
