# LANE C — THE WIPEOUT CASE STUDY (the exemplar of broken)

Static rebuild lane, 2026-09-10. Operator's charge: "it displays weird and there's like
6 versions all have pieces but none of them sync."

## THE POINT

Wipeout is four builds of one idea ("the song is the level") that share zero code: the
same 30-line BPM autocorrelator is pasted verbatim in two files, the flagship shader
exists twice and the copies have already drifted apart, and the three pages disagree on
seed math, clock anchor, canvas tech, and even what a "race" is. No single page is
broken alone — the family is broken because there is no shared state object and no
canonical uniform set to snap to, so every new build re-solved the same five problems
differently. The rebuild method this case study defines: compute ONE state object per
song, bind ONE uniform set, share ONE shell (menu/audio/HUD), and treat renderers as
swappable shaders registered against it.

## FRAGMENT INVENTORY

| # | Fragment | Piece it implements | mtime | Lines | Tech | Shared state? |
|---|----------|--------------------|-------|-------|------|---------------|
| 1 | `dashboard/static/shaders/library/wipeout_raymarch.glsl` | Full raymarched world: track SDF, path camera, lighting. Takes uBPM/uEnergy/uBass/uSeed. No ship, no HUD, no game. | 09-08 20:17 | 137 | GLSL, Shadertoy-style `mainImage` | Declared in `shaders/library/manifest.json` (`id: wipeout_raymarch`) but **included by no page** — v2 carries a drifted inline copy |
| 2 | `dashboard/static/wipeout_v2.html` | Raymarch world + BPM detection + HUD (bpm/speed/dist) + track menu. Passive camera flight — no ship, no collision. | 09-08 18:39 | 293 | WebGL2 / GLSL ES3, `gl_VertexID` triangle | Standalone. Seed = `(filename.length*7919)%1000/100`. Clock = `performance.now()` |
| 3 | `dashboard/static/wipeout_sunset.html` (titles itself **v3**) | Synthwave terrain fed live by FFT texture + JS terrain-mirror collision + hull/wipes HUD + grade screen | 09-08 18:49 | 360 | **WebGL1** / GLSL ES1, attribute-buffer triangle, `iChannel0` = 128x1 LUMINANCE freq texture | Standalone. No BPM measured. `iResolution` is vec2. Clock = `performance.now()` |
| 4 | `dashboard/static/wipeout_lightmaze.html` | The actual game logic: waveform → beat grid → level events (wall/block/gate/boost), 2D ship, combo/hull, fake-tunnel neon render | 09-08 18:27 | 240 | **Canvas2D** — no WebGL at all | Standalone. Seed = FNV-1a(name)+round(duration) via mulberry32. Own `songT` clock |

Supporting refs: `shaders/library/manifest.json:53` (library entry), `index.html:177-182`
(three separate page rows). Family history per `watch/ORPHAN_SWEEP_20260909.md` item 9:
"**Wipeout v2 collision events** — 'v3 = SDF collision events' was the named next;
sunset-v3 shipped instead, collision v3 didn't." `watch/GAME_SUBSYSTEM_AUDIT_20260909.md`
names the family "v1/v2/v3" — a v1 existed and is gone from disk.

**The "~6 versions" reconciles as:** 4 on-disk fragments + the deleted v1 + the
duplicated shader (library copy + v2's inline copy) = ~6 artifacts, each holding
pieces, none sharing a line.

## SYNC-FAILURE DIAGNOSIS

1. **No state contract.** Every page re-implements song analysis its own way. The
   autocorrelation BPM detector is duplicated *verbatim* (v2 lines 236-244 == lightmaze
   lines 87-93) yet consumed differently: v2 makes it the world clock, lightmaze makes
   it a beat grid, sunset never measures at all.
2. **Incompatible seed math** for the same stated design goal ("same song = same world"):
   v2 hashes the *filename length*; lightmaze uses FNV-1a(name)+duration; sunset uses
   none (live FFT is the terrain); the library shader takes uSeed with no specified
   derivation. Same song = three different worlds, by accident.
3. **Incompatible shader interfaces.** v2: WebGL2, `#version 300 es`, vec3 iResolution,
   uBPM/uEnergy/uBass/uSeed. Sunset: WebGL1, vec2 iResolution, iTimeDelta, iChannel0
   sampler, uSteer/uSpeed/uCrashFlash. The only uniform they share is iTime. Nothing can
   feed both without a bridge.
4. **Three render bootstraps:** gl_VertexID fullscreen triangle (WebGL2), attribute
   buffer (WebGL1), Canvas2D. Three fit()/resize/DPR policies, three HUD DOM trees with
   near-identical CSS pasted three times.
5. **Clock drift by construction.** All pages anchor the world clock to
   `performance.now()` at click, never to the audio clock — any decode stall desyncs
   world from song, and each page desyncs differently.
6. **The library broke its own promise — the drift is already measurable.** The manifest
   declares wipeout_raymarch as a reusable scene, but its only consumer (v2) embeds a
   hand-copied version that has diverged: v2's `dosub()` hashes `gsub.cell+uSeed`
   (line 94); the library copy hashes `gsub.cell` only. Library preview and v2 page
   render *different worlds for the same seed*. Copy-paste is the sync killer; this one
   diff is the whole case in miniature.
7. **No shared game model.** v2 is a passive camera (no ship), sunset has hull/wipes via
   a JS mirror of the shader terrain, lightmaze has hull/combo via a serialized event
   list. The named next build — SDF collision events on the raymarched track — never
   landed. That is the family's missing organ.

## SYNC SPEC

### A. One state object — `WIPEOUT_STATE`
Computed ONCE per song load by one shared module (`dashboard/static/js/wipeout_state.js`),
cached per file. Merges lightmaze's level gen with v2's analysis:

```json
{
  "song":   { "name": "genesis", "file": "suno/genesis.mp3", "duration_s": 294.0 },
  "seed":   1837462219,
  "bpm":    126.3,
  "beat_s": 0.475,
  "level":  [ { "t": 12.4, "type": "wall", "x": 0.31, "w": 0.72 },
              { "t": 13.1, "type": "gate", "x": -0.2, "w": 0.5 },
              { "t": 14.9, "type": "boost", "x": 0.6, "w": null } ]
}
```
- `seed` = FNV-1a(name) ^ round(duration_s*1000) — **lightmaze's strSeed wins**.
- `bpm`/`beat_s` from the shared autocorrelator (already identical in two files — dedupe).
- `level` = lightmaze's `genLevel()` output, the only serialized level format that exists.

### B. One canonical uniform set
Every renderer binds all of these; defaults 0/unbound when unused:

| Uniform | Type | Semantics |
|---|---|---|
| `uTime` | float | seconds, **anchored to `AudioContext.currentTime - songStart`**, never performance.now |
| `uResolution` | vec3 | (w, h, 1.0) |
| `uSeed` | float | seed/1000 |
| `uBPM` | float | measured tempo |
| `uEnergy` | float | smoothed full-spectrum RMS x3 (v2 semantics become canon) |
| `uBass` | float | smoothed low-8-bin average |
| `uSteer` | float | -1..1 |
| `uCrashFlash` | float | 0..1 |
| `iChannel0` | sampler2D | 128x1 live FFT texture (sunset's feed promoted to canon) |

### C. One shell
Track menu, audio decode, HUD DOM, end screen, fit()/resize live once
(`dashboard/static/js/racer_shell.js`). A renderer is
`{ name, gl: 'webgl2'|'webgl'|'2d', frag, needs: [uniforms] }` registered against the
shell. v2's raymarcher and an ES3-ported sunset terrain both register; lightmaze's 2D
renderer registers as `'2d'`.

### D. One clock
Audio clock feeds `uTime`, the HUD, and the level-event pointer (lightmaze's `songT`) —
one value, everywhere.

## KEEP / RETIRE

**KEEP**
- lightmaze `genLevel()` + `strSeed`/mulberry32 — becomes the level format and seed law.
- the `analyze()` autocorrelator — keep ONCE, in the shared module (currently pasted twice).
- v2's ES3 raymarcher — the flagship world. Re-home it so `shaders/library/wipeout_raymarch.glsl`
  is the single source: promote v2's uSeed-in-grid-hash fix back into the library file,
  and have the page fetch/include the library text instead of embedding a copy.
- sunset's iChannel0 FFT-texture feed and its JS-terrain-mirror collision pattern — the
  bridge that gives any shader world honest math collisions.

**RETIRE**
- all three inline copies of menu/CSS/HUD/end-screen markup — one shell.
- v2's filename-length seed (renaming a song must not change the world).
- sunset's WebGL1/ES1 shader path and attribute-buffer bootstrap — port the terrain to
  ES3 under the shared runner (plain GLSL, cheap port).
- v2's passive-camera "race" frame — no ship, no crash. Either adopt lightmaze's
  hull/combo events on the raymarched track (that IS the never-built collision v3) or
  reclassify it a music visualizer, not a racer.
- performance.now()-anchored world clocks (all three pages).

**TARGET:** one `wipeout.html` + `racer_shell.js` + `wipeout_state.js` + the shader
library as single shader source. `index.html` rows collapse 3 → 1.

## THE TEMPLATE (method for every fragmented family)

1. Find fragments by name AND by content (grep, not just filename — the drift hides in copies).
2. Table them: piece, mtime, lines, tech, standalone?
3. Name the diverged twins — same artifact in two places, diff them. The drift is the
   proof no contract exists (here: one `+uSeed`).
4. Pick the winning impl per concern (level gen, seed, analysis, collision) — never
   invent a fifth variant.
5. Write the one state object + one uniform set + one clock.
6. Keep/retire list, and name the family's missing organ (wipeout's was collision v3).
