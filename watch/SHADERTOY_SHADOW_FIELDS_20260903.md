# SHADOW FIELDS — the 1D radial lightmap, stolen whole (2026-09-03, zcode seat)

*Layer 9 of the Shadertoy lineage. Trigger: operator handed us two URLs in one breath —
Flyguy's XsK3RR (the tornado) and mattdesl's "2D Pixel Perfect Shadows" wiki — and asked
for a proper research thread: capabilities, why it works, how we use it. Deep self-steal +
salon. This file is the fold; the salon runs on it
(memory/runs/salons/shadow_fields_20260903/).*

## PROVENANCE (tri-state, per law)

- **mattdesl lwjgl-basics wiki, "2D Pixel Perfect Shadows": SUPPORTED.** Fetched raw
  2026-09-03 (`raw.githubusercontent.com/wiki/mattdesl/lwjgl-basics/2D-Pixel-Perfect-Shadows.md`,
  13,837 bytes, quotes below are verbatim). Technique lineage it self-declares: Catalin
  Zima 2010 (shader-based dynamic 2D shadows, XNA) → java-gaming Starbound thread 2013 →
  this wiki (LibGDX/GLSL, ~2013). Source demo: gist.github.com/mattdesl/5286905.
- **Flyguy XsK3RR "1D Radial Lightmap Test" (Shadertoy, 2016): SUPPORTED-by-descent,
  source-text UNPROVEN.** shadertoy.com 403s fetches (wall pre-documented 2026-08-11 and
  2026-08-24). Identity grounded in: our layer-8 steal (watch/SELF_STEAL_SHADERTOY_RIB_20260903.md),
  operator live-screen confirmation 09-03, and now — the decisive bit — the wiki below,
  which is the same engine documented at its origin. CC BY-NC-SA, credit Flyguy 2016.
- **The finding that started this thread: THE TORNADO SHADER IS A SHADOW ALGORITHM.**
  XsK3RR and the wiki are the same engine family (1D radial shadow map). When the operator
  fed video into the tornado's channels, a shadow engine ate live flesh. We were looking at
  the ancestor's documentation without knowing it. Provenance loop closed: 2010 Zima → 2013
  wiki → 2016 Flyguy → 2026-08-24 our deep steal (layers 2-7) → 2026-09-03 layer 8
  (video = live flesh) → today layer 9 (the shadow math itself).
- **PROVENANCE AUDIT 09-04 (intake seat, watch/INTAKE_MATTPERFECT_SHADOWS_20260903.md):
  PASSED.** Re-fetch byte-identical (13,837 bytes, HTTP 200); every verbatim quote on this
  shelf checks against source with zero fabrication; all four laws' mechanisms present in
  the page text (two remain our honest abstractions, not quotes). HYGIENE FINDINGS:
  (1) the wiki page and repo carry **no license** — default copyright — so B1' must
  REIMPLEMENT from the description, never paste GLSL bodies; (2) the page contains
  **no penumbra quads** — softness is a distance-scaled angular gaussian (correct the
  vocabulary wherever "penumbra quad" appears in our derivations). Credit: mattdesl.

## THE TECHNIQUE — three passes, exactly as written

1. **Occlusion map** (FBO, lightSize×lightSize, light at center): render the scene;
   `alpha > 0.75` = shadow caster. **Per-PIXEL casters** — any sprite, any silhouette,
   no convex decomposition, no edge extraction.
2. **1D shadow map** (lightSize×1 texture): one shader pass builds a lookup where the
   x-axis is angle θ (360° = lightSize rays, 256 default = 1.4° angular resolution) and the
   value is **minimum normalized distance to the first opaque pixel along that ray** — d(θ),
   the radial horizon. Rect-to-polar in the sampler; a per-column loop keeps the min.
3. **Light render** (per fragment, polar coords (θ, r)): `lit = step(r, d(θ))` — one
   dependent texture read + compare. Softness: 9-tap gaussian over NEIGHBORING ANGLES with
   width scaled by `smoothstep(0., 1., r)` — penumbra widens with distance from the light.
   Radial falloff `smoothstep(1., 0., r)`; lights composite additively. Author's measured
   budget: **~20 lights fill-bound on a 2013 GeForce 9400**.

## WHY IT WORKS — four load-bearing facts

1. **VISIBILITY FACTORIZATION.** A point light's visibility field is a function of angle
   alone: d(θ). The whole 2D shadow state of a point collapses from O(W×H) to O(N_rays).
   This is 3D shadow mapping with one dimension amputated — depth-from-light becomes
   distance-per-angle. A point SENSOR's knowledge of a field IS its radial horizon function.
2. **FIRST-HIT DOMINANCE.** Occlusion along a ray is monotone — only the nearest caster
   matters. So the accumulation is a min() reduction, which is commutative and order-free.
   Order-free reduction = embarrassingly parallel = why it maps to GPU at all. (The wiki's
   loop-min and the java-gaming blending-mode version are the same reduction, two engines.)
3. **ONE DEPENDENT READ PER FRAGMENT.** All lighting is `step(r, d(θ))`. The scene's
   shadow complexity is pre-baked into 256 bytes of texture; the per-pixel cost is constant.
4. **ARTIFACT-INTO-FEATURE.** Finite ray count means angular uncertainty σ ≈ 1/N; a
   shadow edge blurs by ≈ r·σ, growing linearly with distance. The wiki *multiplies the
   gaussian width by smoothstep(0,1,r)* — it converts sampling aliasing into a
   physically-plausible penumbra. Measurement noise spent as gradient, not hidden as error.
   (2013 graphics independently discovered our honest-meter doctrine.)

## CAPABILITIES — three engines of one invariant

| | **Ray-field** (wiki, XsK3RR) | **Geometry wedges** (Starbound extrusion) | **Grid flood** (our maze_arena BFS) |
|---|---|---|---|
| Casters | per-pixel sprites (alpha) | polygon edges | grid cells |
| Edges | soft, distance-scaled penumbra free | hard exact; softness costs extra wedges | hard cell edges |
| Cost | fill-bound (~20 lights/2013 GPU) | vertex-bound, cheap fill | CPU, O(cells×lights) |
| Precision | 1.4° angular + dependent reads | exact | cell size |
| Agent-readable | needs GPU→CPU readback | no (pixels only) | **YES — the field IS data** |

mattdesl's own honesty (verbatim): *"this is generally less performant than geometry
shadows (which are not per-pixel)."* You trade fill-rate for per-pixel casters and free
penumbra. Our maze_arena BFS is the third engine: coarse, CPU, but the only one the agents
can read directly without a render pipeline. **Engine choice is a cost model, not a truth —
all three compute the same invariant: visibility.**

Honest limitations: first-hit only (no translucency, no colored shadows), all-or-nothing
alpha casters, dependent texture reads are cache-hostile, θ-wrap seam at the map's edge
(repeat wrap hides it), casters self-shade, rect-to-polar distortion at grazing angles,
one light per pass (multi-light wants an atlas — the wiki's optimization list says exactly
this: pack 4 shadow maps into RGBA, cones are cheaper than 360°, disc meshes cut fill).

## HOW WE USE IT — six builds, anchored to existing invariants (FOOTHOLD LAW)

1. **SWARM GPS — the queued research project gets its GPU recipe.** The 1D map IS the
   sensor: agent at p casts K rays, reads d(θ), steers away from small numbers. Two
   implementations: render + readback (the render is the GPS), or CPU K-ray against the
   same occluder polygons. The falsifier stands from layer 8: same swarm, same maze,
   lightmap GPS on/off, measure steps.
2. **THE ROOM gets honest occlusion.** room_lightmap.html's failure-class occluder pillars
   + engine lights through this pipeline = shadows that are *correct*. Wavelength = channel
   (per-band, per the hyperspectral salon). A light that cannot reach behind a pillar
   SHOWS the blind spot instead of approximating it away.
3. **PER-LANE BLIND-SPOT RENDERING (new, Unproven — design).** Each model/lane = a light
   at a position; each lane's walled sources and context limits = its occluder set; render
   each lane's shadow map → THE ROOM shows WHERE EACH SEAT IS BLIND. Dispatch becomes
   visibility routing: send the task to the lane whose light reaches it. ask_router as a
   shadow computation. Falsifier: render three lanes' fields over one room; the rendered
   blind regions must match known lane failures (no-vision lane blind to images, walled
   lane blind to its wall) — disagreement kills the design.
4. **SALON VERDICT FIELD (new, Unproven — design).** N blind posts = N lights; failure
   classes = occluders. A claim DISCOVERED = lit by ≥1 witness (union of visibility
   polygons). A claim SURVIVING = lit by ALL witnesses (intersection). The salon's
   epistemology renders as a lightmap — and the gate's "keep only what survives" is a
   set operation on shadows. Build: salon_lightmap.html on the board.
5. **OCCLUSION AS ACCESS CONTROL (metaphor with teeth).** Loopback-only = walls; doors =
   light cones; a surface's visibility polygon = who can read it. A secret behind an
   occluder is invisible to lanes without line-of-sight. Renderable security model — the
   fair-use firewall drawn as physics.
6. **BAY WEATHER (the tornado, upgraded).** XsK3RR proved the channels accept reality
   (video → tornado). Feed OUR channels — queue density, event.v1 stream, bay congestion —
   into the lightmap's iChannel0 → the fleet's own weather rendered on the board.
   Exhibit-009 candidate.

## BUILD ORDER (falsifiable, cheapest-first)

- **B1** maze_arena GPU field: port the 3-pass pipeline to WebGL in maze_arena.html;
  falsifier = walker steps, BFS field vs ray-field, same maze.
- **B2** salon_lightmap.html: render the last salon's 7 posts as 7 lights, failure classes
  as occluders; PASS if the rendered union/intersection matches the fold verdict.
- **B3** per-lane blind-spot map (design-falsified per #3 above).
- **B4** bay weather channel (exhibit-009).

## LAWS EXTRACTED (the fold)

- **VISIBILITY FACTORIZATION:** a point sensor's knowledge of a field is its radial
  horizon function d(θ); sensing is 1D per point. (Supported: wiki + lineage.)
- **MIN-REDUCTION:** first-hit dominance makes occlusion order-free → parallel. Any
  "who blocks whom" computation in the fleet is a min-reduction, not a search.
  (Technique Supported; fleet application Unproven.)
- **ARTIFACT-INTO-FEATURE:** where sampling is finite, spend the error as gradient, not
  as noise. (Supported: penumbra construction; resonates with honest-meter doctrine.)
- **THREE ENGINES ONE FIELD:** ray-field, wedge, flood compute one invariant — visibility.
  Engine choice = cost model. (Supported.)

## ANCESTRY

- 2026-08-11 flocking-corpus + flock_shader steals (layers 0-1)
- 2026-08-24 DEEP_STEAL_SHADERTOY_HORSE_20260824.md (layers 2-7)
- 2026-09-03 SELF_STEAL_SHADERTOY_RIB (layer 8: video = live flesh; pass graph = dataflow)
- 2026-09-03 this file (layer 9: the shadow math, the wiki, the fleet mapping)
- Salon verdict: memory/runs/salons/shadow_fields_20260903/

## SALON ADDENDUM (fold verdict, 5/7 posts, deepseek judge 15s — read the artifact)

The salon attacked this thread's build order and the fold stands as follows:

- **KILLED on paper:** per-lane blind-spot rendering (category error — lanes are mobile,
  contextual agents, not point lights; a static shadow map renders a static blind spot),
  and salon-verdict-field as a *computation* (claim survival is a logical AND across
  witnesses, not a geometric set operation on lightmaps — "aware of" ≠ "agreeing with").
  Access control stays what it said it was: board language, metaphor, explicitly labeled.
- **First runtime wall everywhere:** GPU→CPU readback latency for swarm control loops
  (consensus S1/S2/S3); θ-wrap seam for any rendered 360° scene; data-to-alpha mapping
  for bay weather (queue density isn't binary like `alpha > 0.75`).
- **REVISED BUILD ORDER (supersedes B1-B4 above):** B1' = CPU K-ray sensor on the EXISTING
  maze_arena walker — run the GPS falsifier (same maze, field on/off, measure steps) with
  zero GPU work. Only if the field earns its steps does the WebGL 3-pass port (old B1) run.
  B2' = THE ROOM occlusion with ground-truth raycast comparison. Weather last, behind the
  alpha-mapping problem.
- **Standing gap (fold, collision #3):** every build is a design until one artifact runs
  the actual pipeline on real fleet data. Lineage confidence is not evidence.
