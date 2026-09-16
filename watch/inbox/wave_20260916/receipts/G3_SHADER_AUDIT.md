# G3_SHADER_AUDIT — receipt (wave 20260916)

- **Lane:** G3 · operator order: audit our shaders
- **Scope:** every GLSL/WebGL shader in the estate (`dashboard/static/` — games, vislab, estate_walk, `shaders/library/`; worktree `sovereign-mirror-scaffold` for belt-trick; `watch/*.glsl` custody copies)
- **Mode:** audit only — fix nothing. No git, no paid APIs.
- **Date:** 2026-09-16
- **Status:** COMPLETE

## Sweep log

- [x] Located shader-marker files via grep across `dashboard/static/` (+ games/, vislab, attic, shaders/)
- [x] Inventory every shader (file, line range, type, what it renders) — 24 shader sites, 30 programs
- [x] Syntax sanity per shader (braces, varying/in-out pairing vertex↔fragment)
- [x] Uniform liveness (JS-side getUniformLocation cross-check → dead-uniform list)
- [x] Version mismatch risks (GLSL ES 1.00 vs 3.00 idioms)
- [x] Precision qualifiers (mobile-safety)
- [x] Performance smells (division in loops, non-constant loop bounds, texture fetch in branches)
- [x] Belt-trick lattice shader (720/spinor/belt): verdict below — it is not GLSL and the constants are not documented
- [x] WebGL-unavailable degradation check in games (IAB finding explained)
- [x] Final tables

---

## 1. Shader inventory

### 1a. Library cartridges — `dashboard/static/shaders/library/` (loaded by `pipeline.html` runner, WebGL2, wrapper injects `#version 300 es` + `precision highp float;`)

| # | File (lines) | Type | Renders | Verdict |
|---|---|---|---|---|
| 1 | `crt_beam.glsl` (1–81) | fragment (post) | CRT beam-raster BFI pass over iChannel0; needs iFrame | OK under ES3 wrapper. `texture(s,uv,bias)` is ES3-only. Stale comment claims iTimeDelta needed — code uses only iFrame. |
| 2 | `disco_maze.glsl` (1–113) | fragment (scene) | Wolfenstein DDA raycaster through disco maze, auto-races | ES1-safe, constant 64-step loop. Clean. Compiles under both eras. |
| 3 | `laser_tone.glsl` (1–26) | fragment (post) | Tonemap of previous pass (XYZ→sRGB, tanh grade) | ES3-only (`texture()` + `tanh`). Divides by `acc.w` — NaN if accumulator w=0. |
| 4 | `rings_cartridge.glsl` (1–51) | fragment (scene) | Fleet smoke rings, one per day since 2026-08-25 | **BROKEN: references `uDays`, wrapper declares `uDay` → compile error ('uDays' undeclared).** See §3. |
| 5 | `tavern.glsl` (1–109) | fragment (scene) | Hearth + five ractor flames, round-robin speech | Clean. ES1-safe. Constant loops (5, 16). First fleet-original cartridge. |
| 6 | `warp_speed.glsl` (1–18) | fragment (scene) | Hoskins starfield warp | ES3-only (`tanh`). 100×10 nested loops w/ division — heaviest simple shader in estate. |
| 7 | `wipeout_raymarch.glsl` (1–137) | fragment (scene) | Raymarched bpm-clock racer (track, gates, grid towers) | ES3-only (uint bit ops, floatBitsToUint). **uBPM/uSeed never set by runner (§2). Grid-traversal bug line 33 (§3).** |

### 1b. Deployed games — `dashboard/static/games/` (top-level `swarm.html`/`maze_arena.html`/`arena_operator_field.html` are byte-identical duplicates, md5-verified)

| # | File (lines) | Type | Renders | Verdict |
|---|---|---|---|---|
| 8 | `games/swarm.html` FS_SRC (322–449) + VS (457) | fragment+vertex | Raymarched wipeout terrain + slit sun behind 2D swarm game | ES1, `precision highp` present, all 6 used uniforms set. **iChannel0 declared + 1×1 texture bound but never sampled → dead.** 300-step march + 4-tap gradient — heaviest game shader. Graceful: try/catch → GLOK=false, game runs 2D. |
| 9 | `games/maze_arena.html` VS+FS_OCC+FS_SHADOW+FS_LIGHT (443–466) | 1 VS + 3 fragment | 3-pass 1D shadow field: occlusion → 256-ray march → polar 9-tap penumbra + 110° gaze sector | ES1, highp/mediump all declared, `RC=256` documented inline (line 430). All 6 uniforms fetched. Gaussian weight sum 4.898 correct. **Graceful: catch → `fieldMode='bfs'` CPU fallback.** `preserveDrawingBuffer:true` here (the one canvas dumps can read). |
| 10 | `games/arena_operator_field.html` VS+FS_REAL (65–89) | fragment+vertex | Scalar-field spectator view: tilt plane + Gaussian lights + vortex ring + SDF walls; R-channel readback divergence receipt | ES1, mediump, all 5 uniforms wired. **NO WebGL guard/catch — null context crashes the page.** JS `sh()` missing braces: returns failed shader anyway (line 90–91). readPixels receipt is same-task (works, fragile). |

### 1c. Visual surfaces (top-level `dashboard/static/`)

| # | File (lines) | Type | Renders | Verdict |
|---|---|---|---|---|
| 11 | `the_rings.html` FS (32–88) | fragment | Standalone THE RINGS (uDays declared correctly here) | WebGL1 ES1, highp. No gl guard. |
| 12 | `wipeout_v2.html` FS (63–225) | fragment | ES3 rewrite of the racer (uSeed in noise, vec3 iResolution) | `#version 300 es` + highp in-source; all 6 uniforms fetched. Same grid bug line 103. No gl guard. |
| 13 | `wipeout_sunset.html` FS (65–224) | fragment | ES1 ancestor of the racer | iChannel0 declared, never sampled → dead. No gl guard. |
| 14 | `calabi_yau.html` FS (27–74) | fragment | Calabi-Yau quintic (Nishitsuji technique), mouse-orbited | WebGL2 ES3, highp, iMouse vec4 set via uniform4f. Custody copy `watch/CALABIYAU_SOURCE_20260904.glsl`. N=5,G=20 → 10k inner ops/px. No gl guard. |
| 15 | `chaos_refract.html` FS (30–51) | fragment | Chromatic refraction field | WebGL1, highp, iResolution/iTime wired. No gl guard. |
| 16 | `field_quills.html` VS+FS (32–~78) | fragment+vertex | Field-line quills (charges + vortex), ES3 | Clean hygiene: `#version` line 1, highp, constant loop bound documented in comment (line 31). All uniforms wired. |
| 17 | `doorbench.html` VERT_SRC+FRAG_SRC (68–~150) | fragment+vertex | Verkle door benchmark: sampler3D raymarch of 64³ field, 110 steps | WebGL2 ES3, `precision highp sampler3D` declared (rare + correct). All 7 uniforms fetched. **Graceful: `fatal('WEBGL2 UNAVAILABLE…')` + throw.** |
| 18 | `mesh_gallery.html` 2 programs (595–617, 982–985) | 2×(VS+FS) | Mesh viewer (normal/tint/unlit) + points/lines overlay | WebGL1, mediump, all uniforms fetched both programs (636, 1008). |
| 19 | `universe_within.html` FS (53–147) | fragment | "Universe within" — samples FFT texture2D(iChannel0) live | iChannel0 LIVE here (line 134). uBoost wired. No gl guard. |
| 20 | `shadow_walk.html` CY_GLSL sky (588–632) + paste-runner (634–653) | fragment ×2 | Calabi-Yau sky behind voxel game + **arbitrary pasted-mainImage ingestion door** (localStorage, compile-error surfaced to operator) | WebGL2 ES3. skyInit throws are caught at all 3 call sites → sky silently skipped, game survives. Graceful. |
| 21 | `verkle_pyramid.html` FS (~43) | fragment | Verkle pyramid knot field (uKnots/uTip) | WebGL1, highp, all wired. No gl guard. |
| 22 | `the_radar.html` FS (~41) | fragment | Radar sweep with uBlips | WebGL1, highp, all wired. No gl guard. |
| 23 | `phase_particles.html` 2 GPGPU compute + points VS/FS (~85–180) | 2 compute fragments + VS + FS | Phase-of-matter particle instrument (solid/liquid/gas/plasma) via GPUComputationRenderer | ES1-style source wrapped by three.js. Float-texture/NearestFilter pitfall documented inline (lines 79–81) — exemplary. All uniforms set via material.uniforms. CPU readback per frame (line 210) — instrument cost. |
| 24 | `tavern_test.html` (whole file) | harness | One-shot compile+40-frame test of tavern.glsl under the exact runner wrapper | Correct approach — **extend to all 7 cartridges; it would have caught the rings break.** |

### 1d. Custody / reference (not shipped, correctly quarantined)

- `watch/CALABIYAU_SOURCE_20260904.glsl` (45 lines) — byte-preserved custody copy of the calabi shader.
- `watch/dune_fiction_baselunaire_source.glsl` (54 lines) — baselunaire reference receipt, header states "never shipped", steal-inventory documented. License-clean posture.

### 1e. Not shaders (verified negatives)

- `estate_walk.html` / `estate_walk.lod.html` — zero shader content (canvas/LOD DOM walk).
- `games/arrakis.html`, `games/frontier_souls.html`, `games/mud.html`, `games/toy.html` — canvas-2D only; immune to WebGL issues.
- `wave_gpu.js` — three.js stock materials readout, opt-in `?gpu`, no custom GLSL. `wave_scene.js` — none.
- `decks/legions|mesh3d|gamebuild|mag.html`, `module_map_data.js`, `vislab/*` — prose/JSON mentions only (grep false positives).
- `memory/corpus/shadertoy21k/` — 21k scraped Shadertoy fragments: reference corpus, NOT estate-authored; out of audit scope (license posture is the question it raises, not correctness).

---

## 2. Dead-uniform list

| Location | Uniform | Status |
|---|---|---|
| pipeline.html line 133 | `uBPM`, `uSeed`, `iFrame` | **Declared in WRAP_TOP but never in the scene fetch list → wipeout_raymarch runs with uBPM=0, uSeed=0 → bpm=0 → speed=0 → the racer never moves, world static.** (Post pass fetches iFrame; scene does not.) |
| pipeline.html line 199 | `CARBPM` | **Undeclared JS identifier — ReferenceError every playing frame → rAF chain breaks → scene frozen after frame 1. This is the pipeline's current live state.** |
| games/swarm.html + wipeout_sunset.html | `iChannel0` | Declared + 1×1 black texture bound (lines 465–466 / equivalent), never sampled. Dead sampler + dead bind. |
| pipeline WRAP_TOP (all cartridges) | `iMouse` | Declared for every program; used by none of the 7 cartridges (compiler strips; harmless). `uDay` used only by (broken) rings; `uBass`/`uEnergy` used only by tavern + wipeout. |
| crt_beam.glsl line 3 comment | `iTimeDelta` | Comment says "Needs iFrame, iTimeDelta"; wrapper doesn't declare iTimeDelta and code never uses it. Stale doc, no bug. |

All other surfaces: every declared uniform has a matching `getUniformLocation` + setter (verified per file in §1). No orphan setters found.

## 3. Pair-mismatch list

| Pair | Mismatch | Effect |
|---|---|---|
| `pipeline.html` WRAP_TOP line 72 (`uniform float uDay`) ↔ `shaders/library/rings_cartridge.glsl` line 32 (`uDays`) | **Name mismatch, case-sensitive GLSL** | The Rings cartridge FAILS TO COMPILE under the runner: `'udays' : undeclared identifier`. Standalone `the_rings.html` declares its own `uDays` and works — the cartridge port is the broken link. |
| wipeout_raymarch.glsl line 33 + wipeout_v2.html line 103 | `min(src.x,min(src.z,src.z))` — `src.y` almost certainly intended | Grid-crossing on Y never advances `grid.d` — duplicated bug in both copies. Not a crash; traversal robustness smell. |
| maze_arena VS writes `vUv` ↔ FS_OCC ignores it | none | Legal (unused varying at link is fine) — listed only to record it was checked. |
| swarm VS (no varyings) ↔ FS (no varyings) | none | Legal. |

## 4. Version-mismatch risks (ES 1.00 vs 3.00)

- Runner (`pipeline.html`) is WebGL2/ES3-only and injects `#version 300 es` + `precision highp float;` — so **all 7 cartridges compile-era-safe today except rings (name bug, §3)**.
- ES3-only constructs inside cartridges: `crt_beam` (3-arg texture bias), `laser_tone` (`texture()`, `tanh`), `warp_speed` (`tanh`), `wipeout_raymarch` (uint bit-ops, `floatBitsToUint`). These can never be dropped into a WebGL1 wrapper without rewrite — the manifest should record the era per cartridge.
- ES1-only idioms in games/surfaces (swarm, maze_arena, arena_operator_field, the_rings, wipeout_sunset, mesh_gallery, universe_within, verkle_pyramid, the_radar, chaos_refract): `gl_FragColor`/`attribute`/`varying`/`texture2D` — fine on WebGL1 contexts they request; porting any to WebGL2 requires conversion.
- swarm.html user-defines `float round(float)` — `round` is a built-in in ES 3.00; rename before any future port.
- shadow_walk paste-runner compiles arbitrary operator-pasted mainImage under ES3 — the ingestion door is era-3 only by construction (correct and intentional).

## 5. Precision qualifiers (mobile-safety)

- Embedded shaders: **every one declares precision** (highp for all marchers; mediump in arena_operator_field + mesh_gallery FS). Good.
- Library cartridges: none declare precision — they depend on the runner's `precision highp float;`. Present (WRAP_TOP line 70), so safe, but the manifest contract should say so explicitly.
- doorbench declares `precision highp sampler3D;` — the only sampler-precision declaration in the estate; exemplary.
- Note: arena_operator_field does Gaussian exp/division in mediump — acceptable on desktop, marginal on mobile GPUs; it's a desktop spectator surface today.

## 6. Performance smells

- **swarm.html backdrop**: 300-step march × (trinoise 3× hash + edgeMin) + 4-tap gradient per pixel, fullscreen, every frame, behind gameplay — the estate's most expensive game shader. Constant bounds (good). `dx=da.x/db.y` → 0-div on lattice lines (inf/NaN risk via mix).
- **warp_speed**: 100×10 = 1000 inner iterations/pixel with `/dot(p,p)` division in loop — known-heavy classic; fine as a showpiece, never as ambient.
- **calabi_yau**: G=20 × N=5 → 20·20·5·5 = 10,000 cpow/exp ops per pixel. Bounded but the heaviest math on the estate. Fine at 131-line scale; do not scale G.
- **wipeout family (library + v2)**: 200-step march + 4-SDF normal; **undamped displacement wobble** `cross(sin(hp*7.),cos(hp.yzx*5.))*mix(.01,.1,tp.z/2.)` breaks the field's Lipsitz bound → overstep artifacts; `tp.z/2.` division per SDF eval; globals everywhere (ro/rt/rd/rp/rs/x/y/z/o).
- **maze_arena**: FS_SHADOW does 256 texture fetches/pixel but on a 256×1 viewport (by design — documented); FS_LIGHT 9-tap. Correct and cheap in practice.
- **crt_beam**: 3 texture fetches inside per-channel branch loop — mild.
- Non-constant loop bounds: **none anywhere** — every loop in the estate has a compile-time bound. (This is the single best hygiene stat in the codebase.)
- Texture fetch in branches: only crt_beam + maze_arena dOf — both acceptable.

## 7. Belt-trick lattice shader (720/spinor/belt) — operator's own math

**Verdict: the belt-trick lattice artifact is NOT a GLSL shader, and its math constants are not documented anywhere a shader lives.**

- Trail: `memory/diary_latest.md` line 113 — session `019f7582-b985-7270-85c2-aed0b524bd89`, 2026-07-18, "Dirac Belt Trick with Domain Repetition for Lattice Representation" → biography dossier/visual_pack → paths_touched point to worktree `projects/worktrees/sovereign-mirror-scaffold`.
- The artifact: `worktrees/sovereign-mirror-scaffold/src/sovereign_mirror/dashboard/static/platform/scenes/belt_domain.js` (140 lines) — a **Three.js scene**: 3×3 domain tiles, spinning cube (the belt-trick object), ring of frame anchors, transport-colored ribbons, holonomy badge; spin speed reacts to live field twist; odd holonomy = red + faster + bigger ribbon kink. **Zero custom GLSL** — stock MeshStandardMaterial/TubeGeometry only. There is no constant table and no march in it to verify.
- No other belt/spinor/720 GLSL exists anywhere in `dashboard/static/`, `vislab/`, `memory/artifacts/` (console_render shows only), or the worktree platform scenes. `memory/artifacts/` contains only console-render show JSONs — no shader sources.
- The Lipschitz doctrine lives only as prose: `dashboard/static/lanes/elder.md` lines 70–74 ("sparse-grid distance field, Lipschitz-bound dirty radius … SDF marching with Lipschitz continuity gives provable invalidation radii for free") and scattered memory/runs notes. **No shader file carries a Lipschitz-bounded march constant or a comment deriving one.** The actual marchers (wipeout family, swarm, doorbench) state steps/epsilon inline with no bound derivation — and wipeout's displacement wobble actively violates a Lipschitz assumption (§6).
- gen-2 recommendation: either (a) port belt_domain.js to a real GLSL belt-trick cartridge with the constant tables + holonomy math in a header comment (where the operator's math would finally live next to its shader), or (b) pin a doc-comment at the top of belt_domain.js stating the math (frames/transports/odd-holonomy semantics, twist-speed constants 0.45/0.55/0.9·twist, kink amplitudes 0.55/0.12) so the artifact is self-describing. Today none of those numbers are written down anywhere the code lives.

## 8. WebGL-unavailable degradation (games) + the IAB black-canvas finding

| Game | WebGL missing behavior |
|---|---|
| games/swarm.html | **GRACEFUL** — glInit try/catch → GLOK=false; glDraw early-returns; 2D game fully playable, backdrop simply absent. |
| games/maze_arena.html | **GRACEFUL (best in estate)** — catch → `fieldMode='bfs'`, CPU ray-field fallback, GL canvas hidden, warn logged. |
| games/arena_operator_field.html | **NOT GRACEFUL** — no guard, no catch; null context throws at createShader → whole script dies. Same fix pattern as maze_arena should be copied. |
| pipeline.html / tavern_test.html | GRACEFUL — explicit "webgl2 required" / FAIL message. |
| doorbench.html | GRACEFUL — `fatal('WEBGL2 UNAVAILABLE…')` DOM message + throw. |
| shadow_walk.html | GRACEFUL — skyInit throws caught at every call site → sky skipped, voxel game survives. |
| the_rings, wipeout_sunset, wipeout_v2, calabi_yau, chaos_refract, universe_within, verkle_pyramid, the_radar, phase_particles | NOT guarded — null context throws in fit()/first frame. Visual surfaces, not games; low blast radius, one shared guard would fix all. |
| arrakis, mud, frontier_souls, toy, estate_walk | 2D-only — immune. |

**IAB finding explained:** swarm's GL canvas is in-DOM but created with `{antialias:false}` only — **no `preserveDrawingBuffer`**, so any post-compositing canvas dump (screenshot/toDataURL) reads black even when rendering fine. maze_arena's GL canvas is `preserveDrawingBuffer:true` but offscreen (createElement, never appended) — dumps can't see it at all. So "WebGL reads black in canvas dumps" is a capture-mechanics artifact, not a rendering bug: gameplay does not depend on dumps. Fix option for observability: `preserveDrawingBuffer:true` on swarm's canvas, or dump via a readPixels-inside-frame path.

## 9. Load-bearing vs cosmetic

- **LOAD-BEARING FOR GAMEPLAY:** maze_arena shadow-field (visibility + gaze mechanic; gameplay survives via BFS fallback — the only shader whose loss is fully absorbed), arena_operator_field GPU field (is the spectator's field view AND its own divergence-receipt instrument; loss = surface death, no fallback).
- **INSTRUMENT (not gameplay):** doorbench (verkle door benchmark data), phase_particles (phase instrument), arena's checkDiv receipt.
- **COSMETIC (ambience/backdrop):** all 7 library cartridges + pipeline runner, swarm backdrop (gameplay is 2D), the_rings, wipeout_sunset/v2, calabi_yau, chaos_refract, field_quills, mesh_gallery, universe_within, verkle_pyramid, the_radar, shadow_walk skies.
- **Fun fact for gen-2:** the only shader whose failure changes game rules is maze_arena's — and it is the only one with a full CPU fallback. The pattern is proven; copy it to arena_operator_field.

## 10. Ranked fixes for gen-2 (audit-only; nothing changed)

1. **pipeline.html:199 — define `CARBPM`** (`let CARBPM=125;` or wire the BPM detector). Currently a ReferenceError kills the rAF chain: every scene cartridge freezes after frame 1. BLOCKER, one line.
2. **rings_cartridge.glsl:32 — `uDays` → `uDay`** (or add `uniform float uDays` alias to WRAP_TOP + fetch list). The Rings cartridge cannot compile today. Extend tavern_test.html to run all 7 cartridges so this class of break is caught by harness, not by eye.
3. **pipeline.html:133 — add `uBPM`, `uSeed`, `iFrame` to the scene uniform fetch list** — even after fix 1, wipeout_raymarch's world is static (uBPM=0 ⇒ speed=0) and uSeed stays 0.
4. **wipeout_raymarch.glsl:33 + wipeout_v2.html:103 — `min(src.z,src.z)` → `min(src.y,src.z)`** (grid Y-crossing ignored; duplicated bug).
5. **games/arena_operator_field.html — wrap GL init in try/catch with a 2D fallback** (copy maze_arena's `fieldMode` pattern). Only unguarded game surface.
6. **swarm.html + wipeout_sunset.html — drop the dead `iChannel0` declaration + 1×1 texture bind**, or actually sample the FFT (universe_within shows the intended pattern).
7. **swarm.html — `preserveDrawingBuffer:true` (or in-frame readback)** if canvas dumps should show the backdrop (IAB observability).
8. **Shared `if(!gl)` guard + DOM message** for the_rings, wipeout_sunset/v2, calabi_yau, chaos_refract, universe_within, verkle_pyramid, the_radar.
9. **Document march constants at shader tops** (steps, epsilon, displacement amplitude ⇒ Lipschitz note) for wipeout family + swarm; belt-trick: see §7 — create the GLSL belt cartridge or pin the math doc-comment on belt_domain.js. The operator's Lipschitz doctrine (elder.md) currently has no shader-side anchor.
10. **pipeline.html — delete the first duplicate `usePost` (lines 139–149)**; second definition (173–183) wins by hoisting; first is dead code. Also clear `U` on cartridge switch (stale per-program locations are silently ignored but it's a trap).
11. **Manifest: record GLSL era per cartridge** (ES3-only: crt_beam, laser_tone, warp_speed, wipeout_raymarch; dual-safe: disco_maze, tavern) so nobody drops an ES3 cartridge into a WebGL1 wrapper later.

## Receipt close

- Shader sites inventoried: 24 (30 programs incl. 3 maze_arena passes, 2 phase compute, mesh_gallery ×2, shadow_walk ×2, custody ×2).
- Compile-blocked today: 1 (rings cartridge, name mismatch). Runtime-blocked today: pipeline scene playback (CARBPM). Everything else compiles and runs by static analysis.
- Dead uniforms: 5 entries (§2). Pair mismatches: 1 real + 1 latent bug + 2 legal (§3).
- Nothing was modified. `watch/inbox/wave_20260916/receipts/G3_SHADER_AUDIT.md` is the sole artifact written.
