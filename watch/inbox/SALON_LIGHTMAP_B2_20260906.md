# SALON_LIGHTMAP B2 — the mattdesl 1D radial lightmap, made real (2026-09-06, worker lightmap)

**File:** `dashboard/static/salon_lightmap.html` — one self-contained page, zero external
assets, zero build step, $0. Canvas 2D reimplementation of the wiki's GLSL from the
description (source carries no license → no shader bodies pasted, per the 09-04 audit law).

**Eyeball-verify:** <http://127.0.0.1:8765/static/salon_lightmap.html> — NOTE: the
root-less URL (`/salon_lightmap.html`) 404s on the current server; the canonical serving
path is `/static/…` (same as every nav.js link). Drag/click the scene to move the light,
wheel changes radius, hover to probe any ray against its horizon.

## The algorithm in 5 lines (as rendered on the page)

1. **OCCLUSION** — casters = any pixel alpha>0.75, baked to a mask: per-pixel casters, no edge extraction.
2. **1D MAP** — cast N=256 rays from the light; d(θ) = min normalized distance to first caster. The entire 2D shadow state collapses to 256 texels.
3. **RENDER** — per pixel, polar (θ,r): `lit = step(r, d(θ))` — one lookup, constant cost.
4. **PENUMBRA** — 9-tap gaussian over NEIGHBORING ANGLES, width × smoothstep(0,1,r): finite-ray aliasing spent as gradient, not hidden as error (artifact-into-feature).
5. **FALL OFF + ADD** — radial smoothstep(1,0,r); lights composite additively.

## Provenance

`watch/SHADERTOY_SHADOW_FIELDS_20260903.md` (layer 9): Catalin Zima 2010 → mattdesl
lwjgl-basics wiki "2D Pixel Perfect Shadows" 2013 (raw 13,837 bytes, audit PASS 09-04,
watch/INTAKE_MATTPERFECT_SHADOWS_20260903.md) → Flyguy XsK3RR Shadertoy 2016 → our deep
steal 2026-08-24. This build is original B2 (pre-revision): the steal made visible.

## The visible steal element

The **raw 1D gradient strip** sits beside the lit scene: 256 texels wide, x-axis = θ
(0°→360°), brightness = d(θ), amber texels where a ray hits a caster, white column marks
the probe ray. Hover the scene and you watch the pixel's lit/shadow verdict fall straight
out of one texel on the strip — the factorization (2D state → 256 numbers → one dependent
read) demonstrated in one look. Occluders carry the salon failure-class names as
explicitly-labeled metaphor (walled source / context wall / no-vision lane / stale cache) —
a wall is a wall, not a computation, per the salon fold.

## NAV ENTRY NEEDED (wiring worker owns nav.js — not edited here)

In `dashboard/static/nav.js` LINKS, add beside the Maze Arena line (line 55), to keep the
shadow-fields family together:

    ["/static/salon_lightmap.html", "Salon Lightmap"],

## Falsifier / honest limits

Every surface samples the same field, so casters self-shade (the wiki's known limitation —
visible on the far sides of blocks). CPU ray-march is 256×R steps ≈ 60k per light move,
rAF-throttled; light buffer renders at half res and upscales (soft look, cheap fill). One
light, first-hit only, no translucency — faithful to the technique's own budget.
