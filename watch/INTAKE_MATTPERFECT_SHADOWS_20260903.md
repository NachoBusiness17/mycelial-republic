# INTAKE CARD — MATTPERFECT SHADOWS (2026-09-03) — PRIMARY-SOURCE PROVENANCE VERIFIED, ONE NEW HYGIENE FIND

## ITEM
https://github.com/mattdesl/lwjgl-basics/wiki/2D-Pixel-Perfect-Shadows — mattdesl's
wiki page on 2D pixel-perfect shadow rendering. Intake brief flagged it as "likely a
PRIMARY-SOURCE receipt, not a new discovery" — the shadow-fields arc
(watch/SHADERTOY_SHADOW_FIELDS_20260903.md) already claims it as the stolen ancestor.

## RECEIPTS (fetched 2026-09-03, independent re-fetch by intake seat)

- **Fetch**: raw door worked exactly as briefed —
  `raw.githubusercontent.com/wiki/mattdesl/lwjgl-basics/2D-Pixel-Perfect-Shadows.md`,
  HTTP 200, **13,837 bytes — byte-identical to the shelf's recorded receipt.**
  (First curl attempt returned a hijacked/proxied page — an Agent.so Framer site,
  975KB of Framer HTML from a GitHub URL; clean retry succeeded. Sandbox network
  flakiness, worth remembering, not a wall.)
- **Lineage self-declared on page**: "My technique is inspired by Catalin Zima's
  [dynamic lighting](catalinzima.com/2010/07/my-technique-for-the-shader-based-dynamic-2d-shadows/),
  although the process discussed in this article is rather different and requires far
  fewer passes." + java-gaming Starbound thread link + demo at
  gist.github.com/mattdesl/5286905. Matches shelf PROVENANCE bullet verbatim.
- **The 1D map, verbatim**: "The texture is very small (256x1 pixels)" ... "Each pixel
  in the resulting 1D shadow map describes the *minimum distance to the first occluder
  for that ray's angle*." — this IS d(θ), the radial horizon, taught explicitly.
- **Min-reduction, verbatim**: "We take the *minimum* distance so that we 'stop casting
  the ray' after hitting the first occluder (so to speak)." + `distance = min(distance, dst);`
  + the author's own note: "we could probably use 'break' or 'return' here."
- **Light render, verbatim**: `return step(r, texture2D(u_texture, coord).r);` —
  `step(r, d(θ))` exactly. Softness: "we multiply the blur amount by our distance from
  center ... this leads to more blurriness as the shadow 'fades away'" —
  `float blur = (1./resolution.x) * smoothstep(0., 1., r);`, 9-tap gaussian over
  neighboring angles, falloff `sum * smoothstep(1.0, 0.0, r)`.
- **Budget, verbatim**: "On my Mac OSX 10.6.6 (GeForce 9400), I can add about 20 lights
  before fill-rate becomes a bottleneck." Honesty: "this is generally less performant
  than geometry shadows (which are not per-pixel)." Wrap seam handled by
  `TextureWrap.Repeat`. Optimizations list matches shelf: 4 maps in RGBA channels,
  cones cheaper than 360°, disc meshes cut fill.
- **LICENSE (the new finding)**: the page carries no license statement, and GitHub's
  license API returns 404 for mattdesl/lwjgl-basics — **no license file in the repo**.
  Default copyright applies. Hygiene rule: attribute mattdesl, short quotes fine,
  **never republish the two GLSL shader bodies wholesale — re-implement from the
  technique description.** This lands exactly on B1', the next build, where the
  temptation to paste the gaussian shader verbatim is highest.
- **PENUMBRA QUADS: ABSENT.** The intake brief expected "penumbra quads" on this page —
  there are none. Softness here is the distance-scaled angular gaussian, not quad
  geometry; penumbra-quad construction belongs to a different technique family
  (geometry extrusion). The shelf never claimed penumbra quads, so nothing filed is
  contradicted — the brief's model was the only thing wrong.

## SCORE — F:5 P:2 C:5 W:4 N:1 = **17/25 → BUILD WINDOWED** (ride with B1')

- **FIT 5** — it is the ground truth under the live arc: anchors all exist and compose
  (dashboard/static/arena_operator_field.html, dashboard/static/room_lightmap.html,
  watch/steer_field/FIELD.json, dashboard/static/maze_arena.html B1' target).
- **PULL 2** — pulls nothing new; all momentum was captured at first steal. Only pull
  is de-risking B1' (recipe now verified against source).
- **COST 5** — the fix is a two-line append, minutes.
- **WINDOW 4** — tied to B1' timing: the license constraint must exist BEFORE anyone
  ports the WebGL shader.
- **NOVELTY 1** — primary-source re-find, honestly scored. Repetition as emphasis.
  The value is verification, not discovery — see READ.

## READ

This is provenance closure, not a find — and it closes clean. The independent re-fetch
is byte-identical to what the shelf recorded, every verbatim quote in
SHADERTOY_SHADOW_FIELDS_20260903.md checks against the source with zero fabrication,
and all four extracted laws have their mechanisms physically present in the page text.
The one genuinely new output is the license finding (no license on page or repo →
default copyright → B1' must re-implement, never paste), plus the negative result that
the page contains no penumbra-quad construction — the brief's vocabulary, not the
page's. Provenance-closing has its own value: the shelf's PROVENANCE section now moves
from self-reported to independently witnessed.

## DOGFOOD

1. **INVARIANT PASS (verbatim-check of the visibility-factorization claim)**: the page
   teaches the MECHANISM exactly — x-axis = theta, value = minimum distance to first
   occluder per angle, per-fragment `step(r, d(θ))` — but never states the LAW as a
   principle. "A point sensor's knowledge of a field is its radial horizon function"
   is the seat's generalization, not a quote; the shelf correctly files it as
   abstraction over technique. Min-reduction: taught explicitly (quoted above).
   Artifact-into-feature: taught as intent but framed aesthetically ("more blurriness
   as the shadow 'fades away'") — the doctrine reading (spend error as gradient) is
   ours, and the page's own words support it. Three-engines-one-field: the page
   supplies two of three engines (blending-mode alternative linked; geometry-shadow
   contrast stated); the unification is the fleet's. Verdict: four for four grounded,
   zero fabricated quotes, two of four honestly fleet-level abstractions.
2. **STOCKFISH PASS**: opcode confirmed as provenance-citation on the shadow-fields
   shelf — with one correction: the shelf ALREADY carries the primary citation
   (PROVENANCE bullet 1, URL + byte count). The honest opcode is therefore
   "verify existing citation + append license note," not "add citation." Verified and
   routed below.

## TRI-STATE

- **SUPPORTED** — this page is the primary ancestor of the four extracted laws:
  byte-identical fetch, all mechanisms present in text, lineage self-declared
  (Zima 2010 → java-gaming Starbound thread → this wiki → gist demo).
- **SUPPORTED** — shelf receipts (13,837 bytes, raw URL, verbatim quotes):
  independently reproduced this intake.
- **DISPROVEN** — "the page teaches penumbra quads": no penumbra-quad construction
  exists on the page; softness is distance-scaled angular gaussian. (Intake brief's
  model only; the shelf never claimed it.)
- **DISPUTED → settled as constraint** — "wiki content is reusable": no license on
  page or repo (GitHub license API 404) → default copyright. Attribute, quote short,
  re-implement; no wholesale GLSL reuse.
- **UNPROVEN (out of scope)** — the Flyguy CC BY-NC-SA attribution in the shelf
  (Shadertoy 403 wall stands; not re-verified here).

## VERDICT

**17/25 BUILD WINDOWED — citation-hygiene fix, rides with B1'.** No new build
warranted; the page's build-relevant content was fully absorbed at first steal.

## ROUTE

1. **Exact shelf file**: `watch/SHADERTOY_SHADOW_FIELDS_20260903.md` — already cites
   the primary source correctly (PROVENANCE bullet 1). Append two lines to that
   section: (a) license note — page and repo carry no license (GitHub API 404);
   default copyright; attribute mattdesl, short quotes only, **B1' WebGL port
   re-implements the shaders from the technique description, never pastes the GLSL
   bodies**; (b) optional one-line credit to "nego" (LibGDX forums) for the
   fewer-passes reduction, per the page's own acknowledgment.
2. **B1' implementer constraint**: the license rule above binds the CPU K-ray sensor
   and any later WebGL port.
3. This card filed. Done.
