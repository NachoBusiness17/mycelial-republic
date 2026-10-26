## Files read

- `dashboard/static/universe_within.html` — **the real source**. The cited path `dashboard/static/games/universe_within.html` does not exist (verified via glob).
- `site/dist/games/universe_within.html` — deployed mirror (grep-verified: same anchors at L30–33, L47–48, L140–141, L162, L192–194).
- `dashboard/static/games/swarm.html` L64–69 — the repo's own audio "deploy law" precedent.
- Asset globs: `dashboard/static/suno/` (all 4 tracks present) vs `site/dist/suno/` (only `jsr_loop`, `hemisync`, `gift_track`, `flat_beat_loop` — **none of this game's 4 tracks**).
- Wiring: `dashboard/static/index.html` L104/L221, `site/build.py` L32.

---

## Findings

### Presentation
1. **CRITICAL — canvas never sized (L24, L47–48).** `fit()` is defined and bound to `resize`, but **never called**. `<canvas id="c">` has no width/height attrs → drawing buffer stays at the HTML default **300×150**, and `gl.viewport` is never set. `tick()` feeds `iResolution = cv.width, cv.height` (L189) = (300,150). So at the exact moment the menu hides and the reveal happens (L180–181), the whole network renders at 300×150, CSS-upscaled to fullscreen: mushy lines, blobby sparkles, 2:1 internal aspect stretched onto a 16:9 monitor. It only looks right if the player happens to resize the window.
2. `#ui` background `#000f0` (L10) is an invalid 5-digit hex → declaration dropped → menu bg is transparent (masked only because body/canvas are black). Wants `#000f00`.
3. `fit()` ignores `devicePixelRatio` — after the fix, retina displays still render at half-native res.
4. `.home`/`#cap` color `#334` on black (L19–20) ≈ 2:1 contrast; intentional dark-room vibe, flagging only.
5. Track cards are fixed `width:420px` (L13) with `overflow:hidden` on body (L8) → horizontal clipping below ~460px viewports; no touch affordance.

### Pacing
1. **Shadertoy export fade left in (L140–141).** `tt=mod(iTime,230.)`, `col*=S(0.,20.,tt)*S(224.,200.,tt)` → **20-second fade-in from pure black after the click** (music already started at L182 — the player gets ~15s of black screen with audio), then fade-out at 200→224s and **full blackout 224→230s, repeating every 3:50** while the track loops forever (L176 `loop=true`). The dark room dies mid-session on a timer unrelated to the music. Also `smoothstep(224., 200., …)` has `edge0 > edge1` → undefined per GLSL spec (works by accident on most drivers).
2. Dead branch L197 (`…>songDur && !srcNode.loop`) can never fire — harmless, but shows the visual cycle was never tied to audio.

### Interactivity
1. **Menu bricks on any failure (L162–167).** Handlers are nulled *before* `await fetch`/`decodeAudioData`, with no try/catch → one 404 or decode error leaves `#status` stuck at "decoding …", no retry, error only surfaces in `document.title` (L49).
2. **Deployed copy is 100% broken by that combo.** `site/dist/games/universe_within.html` fetches `suno/<track>` relative to `/games/` → `/games/suno/…` 404s; and `site/dist/suno/` doesn't even ship these 4 tracks. `swarm.html` L64–69 documents the fix this file lacks (`AUDIO_BASES=['../suno/','suno/']`).
3. **One-shot session:** after first click there is no track switch, pause, mute, ESC→menu, keyboard, or pointer input (no `iMouse`). Only exit is reload/close.
4. **The headline promise is unwired (L29, L36 vs L134, L192, L194).** "the glow drinks the bass" reads a *single* texel at `x=.15` → bin ≈19 ≈ **3.3 kHz hi-mid** (fftSize 256 → ~172 Hz/bin), not bass; `uBoost` — the boost hook in the shader — is hardcoded `0` every frame (L194); and L192 `for(i…128) freqData[i*2]=freqData[i*2]` is a self-assign no-op that reads out of bounds (index up to 254 on a 128-length array). Leftover dead wiring: kick drums don't pump anything.
5. Good: `AudioContext` created inside the click gesture (L165) — autoplay-safe; dashboard copy's 4 tracks all resolve.

---

## THE ONE PATCH — size the buffer before first frame

**Rank rationale:** every other defect is viewed *through* a 300×150 stretched rende