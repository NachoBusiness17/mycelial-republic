# FLY1 EXTRACTION SPEC — maze_arena without a GUI (2026-09-11, night watch lane)

*Follows FLY1_IMPL_RECON_20260911.md (which named the two plug points) and
FLY1_QUEUED_20260911.md. This is the headless half of F-FLY1: get the simulation
interface out of maze_arena.html so a connectome — or any brain — can drive it
from a terminal. Everything below was read first-hand from
`dashboard/static/maze_arena.html` (644 lines, the 09-06-fixed M2 build).
Read-only lane; this file is the one output.*

## 1. HOW THE ARENA ACTUALLY WORKS (verified, line-referenced)

**One file, three layers:**

- **ENGINE (lines 33-303) — pure JS, zero DOM. This is what we extract.**
  `sdf()` (60), walls (35-46), `ROUND_CFG` (49-53), `buildField()` BFS lightmap
  (85-130), `refillFieldDirty()` (135-173), `Agent` class (179-237), seeding and
  round logic (239-303).
- **RENDER (304-555)** — canvas, WebGL ray-field, compass strip, HUD. The WebGL
  shadow-field is RENDER-ONLY: GPS agents read the BFS lightmap `LM` and nothing
  else; the ray-field never feeds back into the sim. Headless skips all of it.
- **PLAYER LAYER (578-643)** — the white lantern (keydown), law shards, and the
  red assumption (dragon). The dragon's state logic is tangled inside the
  `frame` render wrapper (612-626) — extraction must lift it into the tick.

**What drives a frame:** `requestAnimationFrame(frame)` (534). One frame =
`tick++; roundTick(); for(const a of agents) a.step(); render` (495-533).
No fixed timestep — all round timers are "ticks @60fps". Headless replaces
rAF with a plain `for` loop: one iteration = one tick. Same semantics.

**State that exists:**
- `walls` — 10 axis-aligned boxes `[cx,cy,halfw,halfh]` in maze-space
  (x∈[0,2], y∈[0,2.7]). `WALLS_BASE` = invariants; `WALL_ALTS` indices
  {1,2,4,5} slide in round 2 every 210 ticks.
- `LM` — Float32Array 240x135. BFS distance-from-cheese; lit = `<1e8`,
  unlit sentinel `1e9`. Full rebuild ~17 ms; R2 refills a dirty radius (30 cells).
- `CHEESE {x:1.2, y:1.35, R:0.06}` — the goal. Reached when
  `hypot(dx,dy) < R` (235). R3: the beacon walks `BEACON_PATH` (54) and the
  field rebuilds every 12 cells of beacon travel.
- `agents[]` — gps (8-dir gradient walk), dumb (random bounce), ms (MODEL SEAT).
  Spawn at (0.15, 1.35). `a.deaths` counts BLOCKED moves, not real deaths —
  naming trap, do not read it as damage.
- `player {x:0.12, y:1.35}` — keydown-driven, step 0.016, axis-separated
  collision (592-606). In the headless harness the BRAIN takes the player role.
- `dragon {x:1.9, y:2.2, awake:false, speed:0.006}` — see section 4.
- Round timers: R1 900 ticks, R2 1500, R3 1500 → one episode = 900-1500 ticks.

**What the SDF and lightmap ARE:**
- `sdf(x,y)` = signed distance to the nearest wall (union of 10 boxes) and the
  bounded outer walls (x∈[0.05,1.95], y∈[0.05,2.65]); negative inside a wall.
  A move passes if `sdf(nx,ny) >= 0.012` — this one constant is the collision law.
- lightmap `LM` = BFS flood from the cheese's grid cell through non-wall cells.
  It is a deterministic distance field — the arena's "GPS". `etaOdd` (handed
  curl) is an optional perturbation; `eta=0` is the classic flood, bit-for-bit.
  Headless v1 pins `etaOdd=0` (classic), keeps the code for later experiments.

**THE PORTING TRAP (top bug risk):** world y is squashed — grid mapping is
`gx=floor(x/2*240)`, `gy=floor(y/2.7*135)`, and every move multiplies the y
component by `2.7/2`. Compass angles are SCREEN-space; in maze-space they are
anisotropic. Observations and actions must live in the same squashed geometry
(present goal vectors as `[dx, dy*2/2.7]`) or the brain steers crooked.
This exact /2.7 transform was the arena's original birth defect — do not
re-introduce it in the harness.

**Determinism:** `Math.random()` appears at exactly 2 sites — agent heading
init (182) and dumb-bounce turn (232). GPS and ms agents are fully
deterministic. Extraction swaps in a seeded PRNG (mulberry32) passed into the
engine so every episode reproduces bit-for-bit from `{seed, round, moves}`.

## 2. THE HEADLESS LOOP (the interface spec)

```
seed --> state --> step --> observations --> action in {0..7} --> repeat
```

Per tick, in order (mirrors frame() exactly):
1. `roundTick()` — round timers, R2 wall moves, R3 beacon walk (+field rebuilds).
2. dragon update (lifted out of the render wrapper into the tick).
3. driven agent takes ONE action.
4. all other agents step (optional; omit for single-agent episodes).
5. emit observation row for the driven agent.

**Observation block (the brain's senses):**

```
obs = {
  t, round, roundT,
  player_pos:   [x, y],                    // maze-space
  clear:        sdf(player),               // signed clearance, negative = in wall
  walls_nearby: [d0..d7],                  // sdf() clearance at each compass
                                           // candidate next-step (8 probes at
                                           // the exact step the action would take)
  goal_vector:  [dx, dy_sq],               // to cheese, y pre-squashed (see trap)
  goal_dist:    hypot,
  goal_bearing: theta_radians,             // atan2 in squashed space
  lightmap_sample: [lm_own, lm_N, lm_NE, lm_E, lm_SE, lm_S, lm_SW, lm_W, lm_NW],
                                           // 3x3 grid neighborhood, raw BFS
                                           // distance; -1 if unlit (1e9)
  dragon: {awake, dist},                   // aversive sense
  pulse:  0 | 1,                           // aversive pulse fired THIS tick
  done:   false | "escaped" | "caught" | "timeout"
}
```

Unlit cells read -1, not 1e9 — a raw sentinel would poison any neural read.
The 3x3 lightmap sample + goal vector + 8 wall probes is the full sensory
contract; it is strictly more informative than doomfly's retinal encoding and
downsamples cleanly if a 4,146-channel shape is ever wanted (recon section 3).

**Action space:** integer 0..7, compass dir, `theta = i*PI/4` (0=E, CCW),
fixed step 0.012, y-squash applied by the engine. Semantics identical to the
MODEL SEAT ints (216-227): a blocked move (sdf < 0.012) = agent stays put,
`deaths++`. `[x,y]` waypoints stay supported as the optional second action
form (approached at GPS step length) so MODEL SEAT move-lists replay unchanged.

**Termination:** reach cheese (escaped), dragon contact (caught, section 4),
or round duration (timeout). One episode = one seeded run, 900-1500 ticks.

## 3. EPISODE FILE FORMAT (one JSONL file per episode)

Path: `memory/runs/fly1/episodes/<date>_<arm>_<cond>_<NNNN>.jsonl`
(arm ∈ {mcns, substrate-b, gps, dumb}; cond ∈ {no-attractor, attractor,
shuffled}). Three row types, one object per line:

```
{"type":"meta","ep":"20260911_mcns_attractor_0001","seed":8675309,"round":2,
 "engine":"maze_core@<sha>","eta":0,"agent":"mcns","attractor":"planted@0.7,0.9",
 "falsifier_pred":"registered prediction string, written BEFORE the run"}
{"type":"step","t":0,  "obs":{...}, "action":3, "deaths":0}
{"type":"step","t":1,  "obs":{...}, "action":3, "deaths":0}
...
{"type":"end","t":1471,"result":"escaped","steps":1471,"esc_t":1471,
 "deaths":12,"path_hash":"a1b2c3","ladder":{"ms":{"done":1,"total":1,"first":1471}}}
```

Rules: meta row first (prediction included — the falsifier law requires the
prediction registered before results exist), exactly one step row per tick,
end row last. Flat, greppable, replayable: meta + the action column alone
replays the whole episode in the browser via MODEL SEAT.

## 4. THE RED ASSUMPTION — aversive channel, documented exactly (predator pass)

Source: lines 591, 612-626. Current behavior, verified:

- **Spawn:** (1.9, 2.2), `awake:false`.
- **Trigger:** `distP = hypot(dragon.x - player.x, dragon.y - player.y)`;
  when `distP < 0.5` → `awake = true`. One-way latch — it never sleeps again.
- **Pursuit:** each tick, moves toward the player at `speed=0.006` in x and
  `0.006*0.4` in y (the y damping mirrors the world squash). Straight-line,
  NO sdf check — the assumption walks through walls (fitting; keep verbatim
  in v1 for source fidelity, note as a v2 fix candidate).
- **It hunts the PLAYER only** — gps/dumb/ms agents are invisible to it.
  In the headless harness the driven brain takes the player role, so the
  predator hunts the brain. That mapping is the design, not an accident.
- **Tri-state honesty on "damage":** the recon says "predator proximity =
  our PPL101-equivalent pulse". Precise finding: maze_arena has the TRIGGER
  (proximity → wake → pursuit pressure) but NO damage semantics — no health,
  no collision consequence, no death. The PPL101 damage-pulse analog must be
  ADDED at the harness layer. This is an addition, documented, not a claim
  the arena already had it.
- **Pulse definition (the harness adds exactly two rules):**
  1. `pulse=1` fires on any tick with `dragon.dist < 0.35` — the continuous
     aversive channel (doomfly's 200 ms PPL101 pulse; here one pulse per
     near-tick, visible in the obs stream).
  2. `dragon.dist < 0.08` → terminal `result:"caught"` — gives the pressure
     a consequence. 0.08 is the law-shard pickup radius (604), reused so
     attract and harm share one distance grammar.
- Both thresholds live in the harness config, not the engine — the engine
  stays a verbatim lift and the PPL101 mapping stays adjustable per arm.

## 5. PLUG POINTS (as the recon named them)

**Plug point 1 — MODEL SEAT door (built, zero engine changes, demo-grade).**
`msLoad()` (564) + Agent 'ms' (211-227): paste
`{"round":2,"moves":[3,3,4,0,[0.31,1.02]]}` — ints 0..7 compass, [x,y]
waypoints. The connectome drives the arena by emitting move-lists; episodes
replay in-browser and are scored on the ladder next to GPS/DUMB. For a LIVE
brain this door is browser-rate and batch-shaped (paste a list). It is the
demo surface and the parity-check oracle, not the stats surface.

**Plug point 2 — headless harness (new build, stats-grade). Three files:**

1. `dashboard/static/maze_core.js` — VERBATIM lift of lines 33-303 plus the
   dragon logic lifted out of the render wrapper (617-622) into a `dragonTick()`.
   Changes allowed, all mechanical: swap `Math.random` for an injected seeded
   PRNG; stub `flash()` and `drawLM()`; export {sdf, walls, LM, buildField,
   refillFieldDirty, Agent, ROUND_CFG, seed/run, roundTick, dragonTick, CHEESE}.
   No DOM, no WebGL, no `document`. UMD wrapper so both the browser page and
   Node can load the same bytes — one engine, two homes (the one-builds-
   one-verifies law applied to the arena itself).
2. `mag/sim/maze_headless.js` (Node) — the loop of section 2: seed → meta row →
   tick → obs → read action → JSONL. Action sources, in order of build:
   (a) `--moves file.jsonl` replay of a MODEL SEAT list (works day one,
   parity-checkable against the browser);
   (b) `--bridge` stdio line protocol — harness writes one JSON obs line,
   brain process replies one JSON action line, tick-locked. This is the door
   the Python doomfly loop (Python 3.11 + C++ kernel) drives: it stays in
   Python, the arena stays JS, the bridge is 40 lines on each side.
3. `mag/sim/fly1_run.py` — experiment runner on the Python side: loads the
   connectome substrate, spawns the Node bridge, executes the arm × condition
   grid (no-attractor / attractor / shuffled / dumb-floor), writes episodes,
   computes escape-rate deltas.

The attractor plant (the falsifier's ONE moved object) is a harness-level
edit to `CHEESE`/`BEACON_PATH` before episode start — one config line, never
an engine edit, so arms differ only in the registered variable.

**Parity gate before any stats run:** same seed + same move-list through
(a) browser MODEL SEAT and (b) headless replay → per-tick positions must
match to float tolerance. This catches every porting bug including the
y-squash trap. The error-banner fixture (line 16) stays on the page for the
new brain agent.

## 6. EFFORT ESTIMATE (one lane, $0 model tokens)

| Piece | File | Hours |
|---|---|---|
| Engine lift + stubs + seeded PRNG + exports + smoke | maze_core.js | 2-3 |
| Dragon lift + pulse rules (harness layer) | maze_core.js / runner | 1 |
| Headless loop + obs encoder + JSONL writer | maze_headless.js | 2-3 |
| stdio bridge (JS side + Python side) | maze_headless.js / fly1_run.py | 1-2 |
| Parity run vs browser MODEL SEAT + fix pass | — | 1-2 |
| **Total** | **3 new files, 1 extracted** | **7-11 h** |

No GPU. Engine is 240x135 BFS + 10-box SDF — thousands of episodes/hour on
one core headless. The mag container (Linux, Node available) is the natural
home; Windows host works too since the engine is plain JS. Premium tokens
touch only the falsifier verdicts, per the routing law.

**Gates before build (inherited from the recon, restated):** doomfly kernel
timestep read at clone time; MCNS download (Google sign-in, human step);
Citation Guidelines fetch before any redistribution; substrate-B GGUF export
from the cage. None of these block the EXTRACTION — the harness is brain-
agnostic and the dumb-bounce walker + seeded move-lists exercise it fully.

## VERDICT

The arena was built extractable: the engine is already DOM-free, the action
contract already exists (MODEL SEAT ints 0..7), and the only predators in the
code are documented. Two loaders (engine core + bridge) and one harness. The
falsifier still needs zero edits — it needs episodes.
