# FX3_SHADER_FIXES — receipt (wave 20260916)

- **Lane:** FX3 · gen-2 fixes from `G3_SHADER_AUDIT.md` (same wave, same dir)
- **Scope:** blocking pair + cheap wins only. Belt-trick doctrine items (audit §7, fix #9) explicitly OUT of scope — design task, not a patch.
- **Mode:** patch. No git. Write/Edit for source. node --check for JS syntax.
- **Date:** 2026-09-16
- **Status:** IN PROGRESS

## Fix list (from audit §10)

1. [ ] `dashboard/static/shaders/pipeline.html:199` — undeclared `CARBPM` (ReferenceError kills rAF chain) — BLOCKER
2. [ ] `dashboard/static/shaders/library/rings_cartridge.glsl:32` — `uDays` vs wrapper's `uDay` (compile-blocked cartridge)
3. [ ] `dashboard/static/shaders/pipeline.html:133` — add missing scene uniform fetches `uBPM`, `uSeed`, `iFrame`
4. [ ] wipeout family `min(src.x,min(src.z,src.z))` → `src.y` — both audited copies
5. [ ] `games/arena_operator_field.html` — null-WebGL guard (graceful message + 2D fallback note, maze_arena pattern)

## Log (appended as work proceeds)

- 2026-09-16 — receipt opened before first edit (wave-lane law). G3 audit read.
- Fix 1 DONE — `pipeline.html`: `let CARBPM=125;` declared at playback state (after `let audio=…`); `useCartridge` now honors an optional manifest `bpm` field (`if(typeof car.bpm==='number')CARBPM=car.bpm;`). Manifest has no `bpm` field today, so 125 (the `||125` fallback value already in the code) is the intended constant; the config-field hook makes it overridable per cartridge.
- Fix 3 DONE — `pipeline.html:135` scene fetch list now `['iResolution','iTime','iMouse','iChannel0','uBass','uEnergy','uDay','uBPM','uSeed','iFrame']`. The per-frame setters (uBPM/uSeed/iFrame) already existed and were writing to undefined locations; they are now live.
- Fix 2 DONE — runner's fetch convention is `uDay` (fetch list + `gl.uniform1f(U.uDay,DAY)`), so the CARTRIDGE was fixed: `rings_cartridge.glsl:32` `uDays`→`uDay`, comment line 3 updated. Also aligned the stale `manifest.json` prose that recorded the wrong name (contract line + rings entry `uniforms`/`note`) — that prose is how this bug was born. `the_rings.html`'s own `uDays` is self-contained and correct; untouched.
- Fix 4 DONE — audit locates the typo in the wipeout pair, NOT swarm: `shaders/library/wipeout_raymarch.glsl:33` and `wipeout_v2.html:103`. Mission's parenthetical said "games/swarm" — grep proves `swarm.html` never contained the pattern; the two audited copies are the ones fixed: `min(src.x,min(src.z,src.z))` → `min(src.x,min(src.y,src.z))`. (`grid.d` is the 3D DDA step distance — `glen+=grid.d` — so y-crossing belongs in the min.)
- Fix 5 DONE — `games/arena_operator_field.html` + top-level twin (md5-verified identical before AND after edit, `4e79fbe1…`): maze_arena-pattern guard. GL init wrapped in `try{ if(!gl)throw new Error('no webgl'); … }catch(e){…}` — on failure: `glOK=false`, GPU canvas hidden, `console.warn`, and a visible DOM note ("WEBGL UNAVAILABLE — GPU field view disabled; agents navigate the CPU field in 2D fallback. GPU/CPU divergence receipt: N/A."). `drawGL()`/`checkDiv()` early-return on `!glOK` so the rAF loop, agents, and 2D overlay keep running; stats line shows `GPU/CPU Δ N/A — 2D CPU fallback` instead of a bogus FAIL. Included the audit's flagged `sh()` missing-braces bug (§1b #10): compile failure now THROWS (maze_arena's `sh` semantics) so a broken shader lands in the fallback instead of silently rendering nothing.

## Per-fix diff summary

| Fix | File | Delta | Detail |
|---|---|---|---|
| 1 | `dashboard/static/shaders/pipeline.html` | +2 lines | line 106 `let CARBPM=125;` (declared — ReferenceError gone); line 134 `if(typeof car.bpm==='number')CARBPM=car.bpm;` in `useCartridge` (config-field hook; manifest has no `bpm` entries today) |
| 2 | `dashboard/static/shaders/library/rings_cartridge.glsl` | 1:1 ×2 | line 32 `uDays`→`uDay`; line 3 comment updated to name `uDay`/WRAP_TOP |
| 2b | `dashboard/static/shaders/library/manifest.json` | 1:1 ×2 | stale prose aligned: contract line now lists `uDay` (+`uBass`/`uBPM`/`uSeed`/`iFrame`); rings entry `uniforms:["uDay"]`, note `uDay auto-injected` |
| 3 | `dashboard/static/shaders/pipeline.html` | 1:1 | line 135 scene fetch list now `['iResolution','iTime','iMouse','iChannel0','uBass','uEnergy','uDay','uBPM','uSeed','iFrame']` — the three existing per-frame setters (lines 197/199/200-ish) were writing to undefined locations, now live |
| 4 | `dashboard/static/shaders/library/wipeout_raymarch.glsl` | 1:1 | line 33 `min(src.x,min(src.z,src.z))` → `min(src.x,min(src.y,src.z))` |
| 4 | `dashboard/static/wipeout_v2.html` | 1:1 | line 103 same fix (whitespace style of that copy preserved) |
| 5 | `dashboard/static/games/arena_operator_field.html` | +21 lines | guard try/catch + glOK gates (drawGL/checkDiv) + DOM fallback note + N/A stats branch + `sh()` throw |
| 5 | `dashboard/static/arena_operator_field.html` | +21 lines | byte-identical twin, synced via `cp` after edit (md5 `4e79fbe1b49590d95b57091a4b6961fb` both) |

Not touched (out of scope): belt-trick doctrine items (audit §7/fix #9), dead `iChannel0` in swarm/wipeout_sunset (fix #6), `preserveDrawingBuffer` (fix #7), shared `!gl` guards for visual surfaces (fix #8), duplicate `usePost` (fix #10), era manifest fields (fix #11), hardcoded `$('day').textContent='14'` (pre-existing oddity, noted only).

## Changed files (wc -l after; "added" = net new lines from this wave)

| File | wc -l now | added |
|---|---|---|
| `dashboard/static/shaders/pipeline.html` | 264 | +2 |
| `dashboard/static/shaders/library/rings_cartridge.glsl` | 50 | 0 (1:1) |
| `dashboard/static/shaders/library/manifest.json` | 107 | 0 (1:1) |
| `dashboard/static/shaders/library/wipeout_raymarch.glsl` | 137 | 0 (1:1) |
| `dashboard/static/wipeout_v2.html` | 293 | 0 (1:1) |
| `dashboard/static/games/arena_operator_field.html` | 245 | +21 |
| `dashboard/static/arena_operator_field.html` | 245 | +21 (twin) |

## Syntax-check outputs (node v22.23.1, `node --check` on extracted `<script>` bodies, temps under %TEMP%)

```text
PASS  pipeline.html <script>[0] (211 lines)
PASS  wipeout_v2.html <script>[0] (245 lines)
PASS  games/arena_operator_field.html <script>[0] (220 lines)
PASS  arena_operator_field.html <script>[0] (220 lines)
PASS  shaders/library/manifest.json parses (10 cartridges, duplicate ids: 0)
EXIT=0
```

GLSL sanity (edited cartridges): brace-balance=0, never negative — `rings_cartridge.glsl`, `wipeout_raymarch.glsl`.

Grep verification:
- `min(src.z,src.z)` — 0 hits estate-wide (was 2).
- `CARBPM` — exactly 3 hits, all pipeline.html (decl line 106 / set line 134 / use line 201). No bare identifier remains.
- `uDays` — remaining hits ONLY in `the_rings.html` (declares + fetches its own `uDays`, self-contained and correct per audit §3; not a mismatch). Zero in `shaders/library/`.

## Which pipeline scenes animate past frame 1 now

ALL of them. The `CARBPM` ReferenceError fired inside `loop()` on every playing frame and killed the rAF chain for every cartridge after frame 1 — it was cartridge-independent. With it fixed:

- **disco_maze, warp_speed, tavern** — animate (they only ever needed the already-wired uniforms).
- **The Rings (rings)** — now also COMPILES (uDay fix) and animates; day count flows from the runner's `DAY`.
- **Wipeout Raymarch (wipeout_raymarch)** — compiles, animates, and actually MOVES now: `uBPM` (125 via CARBPM), `uSeed` (5346.0), `iFrame` reach the program via the extended fetch list; previously its world was static (uBPM=0 ⇒ speed=0) even with a working loop.
- Post chain (crt_beam, laser_tone) unaffected — post fetch list already had `iFrame`.

## Receipt close

- Fixes applied: 5/5 (+1 audit-adjacent inclusion: arena `sh()` throw, logged above). Blocking pair cleared: CARBPM rAF-killer + rings compile failure.
- Files changed: 7 (6 unique sources + 1 md5 twin). No git commands used. No belt-trick doctrine items touched.
- Verification: 5/5 syntax/parse PASS, greps clean, GLSL brace-balanced.
- Residual for a later lane: wipeout's undamped displacement wobble (audit §6), QUEUED manifest entries lacking `file` fields render as clickable-but-dead deck cards (pre-existing, observed while in the file), `$('day')` hardcoded '14' vs computed `DAY`.
