# INTAKE CARD — THREE.JS SHADERTOY MANUAL (item 7, 2026-09-03)

## ITEM
Operator pasted: https://threejs.org/manual/#en/shadertoy
The vendor manual for porting Shadertoy shaders into Three.js — receipted from
raw source (hash-routed page fetched via raw.githubusercontent master):
fullscreen quad = `PlaneGeometry(2,2)` + `OrthographicCamera(-1,1,1,-1)` +
`ShaderMaterial`; uniforms `iTime` / `iResolution` / `iChannel0` fed from JS
(`Clock` ms→s, `TextureLoader` + NearestFilter + RepeatWrapping); `mainImage()`
wrapped and called from `main()`. Two modes: **fullscreen** (per-pixel) and
**procedural texture** (per-surface via `vUv` varying — their demo: three rotating
cubes carrying the shader on their faces). Honest vendor warnings: heavy
per-pixel shaders can hit ~5 fps; Shadertoy globals are site conventions, not
GLSL; example shaders (iq, Daedelus) are CC BY-NC-SA.

## SCORE — F:4 P:5 C:4 W:4 N:3 = 20/25 → **BUILD NOW**

## WHY IT SCORES
This is the vendor recipe for **B1 maze_arena GPU field** — the build already
named "Next" in the shadow fields arc (AGENTS.md pointer + memory). The manual is
the consult-first pass, already written by the vendor. The per-surface `vUv`
variant is the second key: it is how THE ROOM's walls/occluders could CARRY the
shadow field (the mattdesl radial lightmap computed on geometry) — the Light
Codec's film becomes the actual framebuffer, and Britney content-borne steering
becomes literal: FIELD.json → uniform array → pixels.

## DESIGN (named now so the build is one session)
- **B1a (recommended first): raw WebGL2 fullscreen quad in maze_arena.html.**
  The manual's technique ports 1:1 to raw WebGL — no three.js dependency. Keeps
  the STATIC RENDER LAW (zero-fetch, renders in any browser). ~100 lines + our
  own GLSL.
- **B1b: three.js per-surface procedural textures** — only when THE ROOM grows
  real 3D occluder geometry; vendored three.js at that point, not CDN.
- **The honest hard part:** walkers are JS and read the CPU field. Don't do
  per-frame readback. Do DUAL DERIVATION: GLSL renders the field from FIELD.json
  uniforms; JS BFS keeps navigating from the same FIELD.json; add a **divergence
  receipt** — sample N points per frame, GPU vs CPU must match within epsilon.
  One source, two renderers: the standing wave (det spine + stoch flesh) applied
  to our own renderer stack. One-builds-one-verifies, inside one file.
- **License hygiene:** steal the technique, write our own GLSL (the field is
  ours anyway); iq/Daedelus example code is CC BY-NC-SA — never vendored.

## DOGFOOD RECEIPTS
1. **INVARIANT PASS**: extends the Britney doctrine — steering packets now write
   the film itself; reinforces STATIC RENDER LAW (the reason B1a stays raw);
   the divergence receipt is the full-chord law applied to renderers (assert
   every leg or say "partial").
2. **STOCKFISH PASS**: opcode = BUILD, shadow-fields B1; lane = THIS seat (the
   driver is on campaign legs; no dependency between lanes).
3. **ROOM TEST**: the room's walls carry the light as procedural texture — the
   map presents the solved problem IN LIGHT.

## FALSIFIER (pre-registered)
maze_arena.html renders the light field via GPU shader from FIELD.json uniforms;
N-point GPU-vs-CPU divergence < epsilon; walkers still reach the cheese at steps
≤ CPU baseline; receipt filed to the intake thread. Fail either check → the GPU
field is a costume → demote to CALIBRATE.

## VERDICT
**BUILD** B1a tonight in this lane on operator GO (one word). B1b queued behind
real 3D geometry in THE ROOM.
