# DEEP STEAL — Shadertoy: the horse rendered at 60fps (2026-08-24)

**Date:** 2026-08-24
**Commitment:** `deep-steal-shadertoy-horse-001`
**Method:** steal the INVARIANT, not the GLSL. Extends the 2026-08-11 flocking-corpus + flock_shader
steals (do NOT re-steal those — this is the NEXT layer, through today's lens).
**Sources actually opened this turn:**
- https://en.wikipedia.org/wiki/Shadertoy — 52k+ public contributions (mid-2021), Íñigo Quílez +
  Pol Jeremias, launched Feb 2013, WebGL/GLSL, demoscene roots (18 authors from the demoscene
  donated the first content), live editor with immediate visual feedback, floating-point
  multi-pass rendering + history (FBO ping-pong), media inputs (mic, webcam, keyboard, mouse,
  VR, soundcloud, video, textures), annual competitions, referenced in academic papers.
- https://www.shadertoy.com/ + /about — HTTP 403 (site blocks fetches; same as 2026-08-11 —
  provenance honest: knowledge-grounded, not live-scraped).

## What the deep steal is (one sentence)

Shadertoy is the Rocinante image running at 60fps: a FROZEN deterministic program (the shader —
the bones) executed in lockstep across a million coordinates (pixels — seats that receive
coordinates, not payloads), on a shared clock (iTime — the cadence) with a feedback buffer
(iChannel ping-pong — the verkle flywheel), where the only thing worth spending on is the seams.

## The seven deep principles (the layer past 2026-08-11)

1. **THE SHADER IS MAG'S BPE.** A shader receives `uv` (a coordinate) and returns `rgb` (a color).
   It never receives "the scene" — just coordinates + uniforms. That is the own-tokenizer
   invariant verbatim: seats receive coordinates, not payloads. The shader is a frozen function
   over the field; the RIB/STEER block is a shader over the agent field. Same shape, same law.

2. **THE PROGRAM IS THE BONES; THE RENDER IS THE LIFE.** The GLSL is byte-fixed per frame
   (deterministic). The "life" — flocks, metaballs, fractals — emerges from running that SAME
   rule across a parallel field with shared state. Deterministic doesn't stop the running; it is
   what makes the running possible. Identical to SkelMo's skeleton-injected-at-every-step and
   our FROZEN_PREFIX-at-every-call. The horse, all three ways.

3. **iTime IS THE CADENCE; PING-PONG IS THE FLYWHEEL.** iTime = one shared clock for the whole
   field (no per-pixel clocks — cadence is global). iChannel0 feeds frame t's output into frame
   t+1's input (FBO ping-pong) — state persists, the flock "lives." That is the verkle flywheel /
   meta_percolate feed-back: the renderer eats its own output. We already named this in
   flock_shader; the deep part is that the CLOCK is shared and the FEEDBACK is structural.

4. **THE SEAMS ARE WHERE THE MONEY IS.** A shader is ~free per pixel; the interesting structure
   lives at divergence — edges, creases, shadows, where neighboring pixels disagree. Emergence
   LIVES at the seams; the seams are where you escalate. This is flock_shader.seams() +
   fold_gaps (frontier only at divergences) and today's organism-loops steal (escalate at the
   judgment boundary). Shadertoy makes the doctrine visible: spend nothing on the flat field,
   everything on the seams.

5. **LIVE EDIT, IMMEDIATE FEEDBACK = THE STATELESS TIGHT LOOP.** Shadertoy's killer UX is
   stateless iteration: edit → see → edit at 60fps. No memory, no persistence, no ceremony —
   the tightest cadence the medium allows. That is rightsize-don't-pattern-match made literal:
   stateless means no reason to idle; the loop is as tight as the feedback loop allows. Our 120s
   loop and Shadertoy's 16ms loop are the SAME law at different scales.

6. **THE CORPUS IS RULE-STRUCTURE, NOT CODE.** 52k shaders = 52k answers to "what law makes local
   rules become global life?" We do NOT need the GLSL; we need the RULE STRUCTURES people
   discovered: sep/align/coh regimes, curl noise flow fields, ray-marched distance fields
   (iterative field queries), multi-pass accumulation. The 2026-08-11 steal said "port a few
   shaders as emergence tests"; the deep version: mine the RULE LATTICE — which local rules, at
   which parameters, produce which global behavior — as a $0 curriculum for tuning our own fields.

7. **THE RENDERER IS THE OBSERVER.** Every frame is a complete observation of the whole field for
   ~nothing. A million pixels rendered = a million data points gathered as a byproduct. Ghost
   already renders; the deep point: rendering is not display, it is MEASUREMENT. The horse sees
   its own bones every frame and corrects at the seams.

## Self-steal (already built — this deep steal confirms, does not rebuild)

- flock_shader.v1 (agent=pixel, field=texture, swarm=GPU, ghost=renderer) — the language exists.
- seams() + fold_gaps + rightsize_spend — the seam-economy exists and is RIB-verified.
- illuminate/shadow (evidence lighting) — grounded synthesis via evidence falloff exists.
- percolator + meta_percolate feed-back — the ping-pong flywheel exists in memory-space.
- FROZEN_PREFIX / work_contract.BRIEF at every call — the frozen program exists.
- escalate_cached — the seam escalation exists, cache-aware.
- cadence_learn — the shared clock with learned cadence exists.

## External-steal (the NEW atoms)

TAKE 1 — **the field-clock discipline**: one shared clock (iTime) for the whole field, and the
render loop is the heartbeat. Audit our loops: do they share ONE clock (cadence_learn) or does
each loop keep its own? Shared clock = coherence; per-loop clocks = drift. This is the flock
"lives" condition made structural.

TAKE 2 — **render-as-measurement**: every render pass is already a full-field observation. Make
the renderer's output a first-class sensor feed (not just display): the difference between
consecutive frames IS the field's motion, measured for free. Ghost can read frame deltas as
emergence telemetry ($0).

TAKE 3 — **the rule-lattice curriculum**: build a small $0 index of shader rule-structures
(sep/align/coh, curl, ray-march, ping-pong accumulation) → which global behavior each produces →
our fields' tuning knobs. Not GLSL; the INVARIANT of each technique. Reuse flock_field + our
existing flocking tests; do not build a new engine.

REFUSE:
- Porting GLSL, a WebGL stack, a GPU render farm, or the site's JS/PHP. We do not need their
  bytes; we need their laws.
- Scraping the 52k corpus wholesale (403 anyway, and it is rule-structure we want, not code).
- Per-frame LLM calls (their shaders are $0; ours must stay token-bound — LLM only at seams).

## Plain English

A demoscene kid in 2013 put a pure function in front of a GPU and let a million coordinates run
it in lockstep on a shared clock, feeding the output back into the next frame. The "art" is what
the function BECOMES when the field runs it together — greater than the sum of its pixels. That
is the horse: the bones are the shader, the running is the render, and the whole site is proof
that the deterministic frame is what lets the life emerge instead of collapsing.

## Rope

Frozen program + shared clock + ping-pong feedback + spend only at the seams + renderer-as-
observer. We hold the program, the seams, the escalation, the cadence. The two open atoms: a
single shared field-clock across our loops, and render-delta-as-telemetry.

## Ordered adaptations (cheapest first)

1. Fold this deep steal (memory) — deterministic + $0. Confirms flock_shader + organism loops +
   tokenizer + SkelMo as ONE law.
2. Audit loop clocks: do our cadences share one source (cadence_learn) or drift per-loop? Fix
   toward one shared clock. Deterministic, $0, read-only audit first.
3. Render-as-measurement: expose consecutive-frame delta from ghost's renderer as emergence
   telemetry. Reuse what exists.
4. Rule-lattice curriculum: index the handful of shader rule-structures we already reference
   (flocking, curl, ray-march) → their emergent behavior → our tuning knobs. Small, $0.
5. No GLSL, no WebGL, no GPU farm, no corpus scrape, no per-frame LLM.
