# SHADER PIPELINE — research card + the interchange contract (2026-09-08)

**Operator directive:** "gather all the orphans and figure out how to do all of these
more easily and interchangeably. Self steal and then do a research project." + (on the
license fuss): "steal ideas are fucking ideas. if someone says don't do this, build it
your fucking self based off their shit and the math they used."

---

## 1. THE RESEARCH INPUT — @dzhng's Fly Escape Room (Sep 8, 17:11Z)

"Introducing Fly Escape Room — the world's first game with NPCs powered by a real
fruit fly brain, all 166k neurons. Leave food and other objects for the flies, run
the simulation, watch what happens. Goal is to get all flies to escape. Built w/
GPT-6 Astra over a 3 day loop."

**The steal (ideas are free; the math is public):**
- NPC brains = REAL neural substrate (the fly connectome), not scripted AI
- Player shapes the ENVIRONMENT (food, objects); behavior is emergent
- Win condition = all agents escape; the simulation runs itself
- Built by one human + Astra in a 3-day loop — our exact cadence

**OUR VERSION (already half-built, better substrate):** our fly brain is the ACTUAL
quantized behavior volume of a real model — 9,305 thinking-parts of 5.3-flash,
byte-verified down to the GGUF specimen (sha 5ee4f07c). The shadow walk IS the escape
room: the volume is the world, the walkers are the flies, and the player plants
attractors/repellents instead of puppeting anyone. "Plant not command" (bernaise,
the fleet's oldest steering doctrine) = this game's control scheme. F-FLY1 falsifier:
a player must change the escape rate by moving ONE object, blind to doctrine.

## 2. SELF-STEAL — what the orphans share (the 90% we keep rewriting)

Every visual room built tonight re-implements the same 90%: fullscreen quad, context,
resize, uniform plumbing, audio FFT texture, error trap, pause-on-hidden. The ONLY
per-room delta: the fragment shader + 2-3 extra uniforms. Seven rooms = seven copies
of identical scaffolding. That is the orphan disease.

**THE CONTRACT (Shadertoy-compatible, on purpose):** any cartridge is a GLSL fragment
defining `void mainImage(out vec4, in vec2)` — verbatim Shadertoy grammar, so the
entire public shadertoy corpus is our content library by convention. The runner injects:
`iTime, iResolution, iMouse, iChannel0 (live music FFT), uBPM, uEnergy, uBass, uDay`
(fleet day count), `uSeed` (song/chain hash). CHAIN ROLE: a cartridge marked "post"
receives the previous pass's output in iChannel0 — CRT on top of anything.

## 3. THE LAWS (license gate — the operator's amendment)

"Steal ideas are fucking ideas" — ideas, mechanisms, and MATH are free; artifacts and
explicit prohibitions are not. The gate is now mechanical:
- license MIT / CC-BY / CC-BY-NC-SA → INGEST (attributed, non-commercial fleet use)
- license forbids host/copy/train (e.g. iquilezles voxellines) → LOOK-ONLY: no code
  stored, technique re-derivable from the public article, manifest marks it
- unstated → shadertoy default CC BY-NC-SA, attributed, non-commercial
Self-steal discipline (steal-the-contract-not-the-code) is the same law pointed inward.

## 4. THE INTERCHANGEABLE CORE (built tonight)

- `dashboard/static/shaders/manifest.json` — the cartridge registry (id, title, author,
  license, role, source)
- `dashboard/static/shaders/library/*.glsl` — verbatim GLSL, one file per cartridge
- `dashboard/static/pipeline.html` — THE RUNNER: any cartridge + any track + CRT post
  toggle + audio FFT bus. ?cartridge=&post=&audio= for deep links.
- Cartridges ingested tonight: rings (fleet chronometer), crt_beam (post, MIT),
  disco_maze (Noztol), warp_speed (Hoskins CC BY-NC-SA), drive_home (BigWings CC BY-NC-SA),
  sunset (fleet, from synthwave lineage), fractal_cartoon (Kali — nyan iChannel1 asset
  pending), laser_tone (michael0884 fork post-pass)

## FALSIFIERS
- F-P1: a NEW shadertoy shader runs in the runner with ZERO code changes (paste .glsl
  into library/, add manifest row, done) — timed, must be <2 minutes.
- F-P2: any SCENE cartridge + CRT post composes with correct audio reactivity.
- F-P3: the fly-escape room changes escape rate when one attractor moves (measured,
  blind player).

## LINEAGE (the pipeline's own receipt)
Tonight's chain: the dream → shadow walk → the wipeout family → the pyramid → the
rings → the radar → the universe within → THIS contract. Every room an orphan; the
pipeline adopts them all. The next hundred rooms are data, not code.
