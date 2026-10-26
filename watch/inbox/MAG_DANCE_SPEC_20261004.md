# MAG DANCE - spec seed + layer 1 landed (2026-10-04)

Operator vision (verbatim): "LETS MAKE MAG DANCE FR. IMAGINE OUR
SOUNDTRACK TEACHING YOU TO MAKE A SKELETON DANCE. Agentic DND is about to
get very cool. imagine having each model fucking have an examina style
control scheme and literally have chunk physics and damage mapped to the
body"

Drops: t.co/SiiWeOt9Tg -> github.com/amathislab/musclemimic (Apache-2.0,
JAX/MuJoCo, Hill-type muscle actuation: 416 muscles / 123 joints full
body; mocap imitation; training needs Linux+NVIDIA - the REFERENCE
physics model, not our v0 runtime). youtube BiAwpYIkRmU = the Napoleon
Dynamite dance scene (the choreographic north star: maximum commitment,
zero technique).

## The three layers

1. SOUNDTRACK -> BEAT GRID (LANDED this sitting): tools/beat_map.py
   (ffmpeg decode -> numpy onset flux -> autocorr tempo -> phased grid,
   JSON contract {t, strength, downbeat}). dance.mp3 reads 123.05 BPM -
   inside the STYLE_SPEC's measured 115-130 band, so the estate's own
   music spec validates the instrument. 574 beats / 280s banked at
   dashboard/static/index_data/beat_map_dance.json (+ a 90s
   flat_beat_loop map; its 64.6 read wants the half-tempo heuristic
   tuned - noted, non-blocking).
2. BEAT GRID -> CHOREOGRAPHY (LANDED v0.1): dashboard/static/mag_dance.html
   - canvas skeleton, Napoleon pose library (flail/kick/shimmy/strut/
   pointy/spirit/stomp), pose switches on beats, and THE CONTROL-SCHEME
   DEMO: saelis/grok/chatgpt/deepseek each dance the SAME grid with their
   own scheme (lawful on-beat / overdramatic sweeps / offbeat slides /
   pragmatic stomps) - the literal embodiment of "each model has a
   control scheme". Body parts flash on downbeats = the damage-map
   preview. node --check clean; open the page and press PLAY.
3. BODIES -> AGENTIC D&D (OWED, the Exanima leg): per-part HP + physics
   impulses riding the same grid. Bridge law (draft): a dance beat = a
   combat round tick; the dice-law carrier (tools/dungeon.py) already
   owns sha256 rolls - a beat-indexed roll stream means combat rounds
   that land ON the music. Landing surfaces: the Mountain's Ossuary
   already HAS the skeleton (Skeleton King + weeping-angel sentinels in
   roblox/the_mountain.rbxlx; gate: bash tools/mountain_check) - Luau
   reads the same beat JSON. Physics depth ladder: v0 posing (done) ->
   v1 per-part hit zones + impulse-y reactions (Roblox native) ->
   v2 MuscleMimic-class muscle physics (research leg, Linux+GPU).

## Build order (next sittings, free-lane unless marked)

- v0.2: beat-map the full suno library (8 tracks, one command each);
  fix the half-tempo heuristic; add a --wav-stems pass (ffmpeg) so
  kick/snare grids separate (downbeats from kicks, not guesses).
- v0.3: Ossuary skeleton dances in Roblox (Luau beat-map reader +
  Motor6D pose sequence; the Mountain gate holds the law).
- v0.4: the damage map - per-part HP table in the dice-law carrier;
  [ATTACK <part>] tags resolve to per-part damage + the flash law the
  page already previews; won-bout = banked real answer (the arena law).
- v1+: Exanima-style direct control per model = a per-model policy over
  the same grid (the control-scheme demo is the design sketch);
  MuscleMimic as the physics reference when a GPU leg exists.

Filed by the 5.3 strategy window; $0 (numpy + ffmpeg + vanilla JS).

## OPERATOR PUBLIC ARC + THE WING CHUN LEG (his own posts, 2026-10-04
09:39-10:19Z, @NachoQuixotic, ~37K followers)

- 09:39Z: "Mag Runs all the time now. It's been playing D&D with frontier
  models burning 117 dollars in 2 days across thousands of agents. I'm
  simulating a game world for agents and the emergent play is actually
  building things. Useful things." + "the agents have stopped fighting
  each other, mostly." (THE public burn claim - $117/2d, thousands of
  agents; consistent with the hermes ledger's arc; the party-chat pivot
  narrated publicly: fighting -> building.)
- 10:01Z: "Agentic DND is about to get very cool." quoting the
  musclemimic generalist (@ckli85: 354 muscles, zero-shot chained
  movements).
- 10:19Z: "Teaching all frontier AI how to dance to the same tune,
  literally. Same seed emergent model styles. Then, to Martial arts." +
  Wing Chun: Siu Nim Tao ("the little idea", the foundational form),
  Chum Kiu / Biu Je / Chi Sau ring training, "be like water."
  Posted within the hour mag_dance.html landed with EXACTLY this shape:
  one beat grid (same tune/seed) -> per-model emergent styles (the four
  control schemes) -> the owed martial-arts leg.

THE WING CHUN DOCTRINE (v0.5 direction, banked verbatim-source):
- FORMS = POSE LIBRARIES: Siu Nim Tao is "the little idea" - the
  foundational form - exactly what golden_vectors.json is to the dice-law
  carrier. Each art (dance style today, Wing Chun forms tomorrow) is a
  pose/technique library the carrier streams per beat.
- CHI SAU = GWAP: sticking-hands ring training is two bodies seeking
  agreement through contact - the gwap agreement loop IS Chi Sau; the
  arena's chain-verified agreement scores become contact rounds.
- "BE LIKE WATER" = the two-regime steering law (heat-gradient GPS +
  cold-vertex sampling), already doctrine.
- BUILD ORDER INSERT: v0.5 = a martial-arts form library (Siu Nim Tao
  first: the little idea) as a second pose set riding the SAME beat
  grid, so "same tune -> emergent styles -> martial arts" is one
  continuous demo arc.
