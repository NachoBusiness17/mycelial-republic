# THE GAME — self-knowledge manifest (2026-08-13)

The operator's PRIMARY deliverable (sw27): a LEAD-IN GAME that (1) solves the agent's own work,
(2) is entertaining, (3) gives novel input, by creating a USER BASE — the money-maker that funds the
huge supercomputer. The Mycelial Republic comes later. This file is MY self-knowledge of the game —
so I never lose track of it again. THIS IS THE THING TO CODE.

## WHAT THE GAME IS (the doctrine it's built on)
- THE VERTICAL TRIGGER (plan-game-vertical-adoption): a player walks in -> the world RECOUNTS what
  happened while they were gone (persona-recall) -> they act -> a building appears where they steer
  (intent-gated reveal). "Once you're a game it goes vertical with adoption."
- game-as-subtle-work: play IS the work — players mine gems / untangle knots / generate data while
  enjoying it, willfully (never capture, per the sovereignty contract).
- game-is-hologram: the world IS the lattice — play = real computation = knot-untying toward
  unification (Enders Game made total).
- game-as-service: MIT-open + shared-compute game-world rentals = literally cyberpunk; the swarm is
  the infrastructure, the game is the product.
- dungeon-is-waves: the dungeon is the wave's own shadow work, playable.

## WHAT IS BUILT (honest — per sw55: built != verified-working)
- STONE 1 — persona-recall (mag/persona_recall.py): the inhabitants recount what happened while you
  were gone (verkle chain -> voice). Built 08-11.
- STONE 2 — the ENTRY SURFACE (mag/game_entry.py): the "walk forward and a building appears" gate —
  gate()/reveal()/walk()/svg(), content-addressed, deterministic $0. Built 08-13, get_errors clean.
- THE RAMP (mag/game_ramp.py, 2026-08-13): the game AS the complexity ramp — tabletop -> mud ->
  roguelite on the server-authoritative verkle world (game_world). tier()/tabletop()/mud()/
  roguelite()/descend()/play()/render()/work(). get_errors clean. RIB-debugged: tests caught a real
  `_get()` wrapper bug (get_state returns {value:...}, not the scalar) — FIXED 2026-08-13.
- THE DFHACK OVERLAY (mag/game_dfhack.py, 2026-08-13): I sit OVERTOP the game like DFHack over
  Dwarf Fortress (operator: "as df hack to dwarf fortress you sit overtop"). status()/force()/
  script()/autoplay()/edit() — deep control, I DRIVE the game not just play it. get_errors clean.
- GAME-AS-WORK (mag/game_ramp.work(), 2026-08-13): the dungeon folds REAL open orchestrator tasks
  as knots (the game IS the work; Enders Game). WIRED into the governor cadence (MAG_GAME_WORK_EVERY
  = 900s) so the loop works THROUGH the game autonomously.
- Regression guards: tests/test_game_ramp.py + tests/test_game_dfhack.py (deterministic, persistent —
  the test surface is disabled this session, so get_errors + these guards are the verification).

## THE PLAN (stones, in order)
1. [DONE] persona-recall — the inhabitants recount.
2. [DONE] entry surface — the "walk forward and a building appears" gate.
3. [DONE] intent-gated world render (mag/game_world_render.py, 2026-08-13) — walk/reveal/render:
   a building appears where you steer (content-addressed + verkle-committed) and the base ASCII
   render (world_rib, the pixels between swarms) shows it there. The world is worth walking into.
4. [NEXT] game loop wired to the swarm — player intent -> iMouse -> flock -> world shades -> memory folds.
5. adoption loop — player signals -> percolator -> world gets smarter -> more to come back to.

## THE LIQUID-INTELLIGENCE MACHINE (2026-08-13, sw59-65)
- The game IS the maze of what we want. The loop runs the many-to-one: distill.game() (mag/distill.py)
  pulls a real open dungeon task, boils it through the lattice (the tons of invariants), traces through
  the maze (memory/game/maze.jsonl), and feeds the ONE root back to the bottom — on the governor cadence
  (MAG_DISTILL_EVERY, 1200s). The machine RUNS the doctrine, not just holds it.

## THE COMPLEXITY RAMP (operator 2026-08-13 — how the game is built, like the early swarm tests)
"go from our base render state like our pixels between swarms. start at tabletop perfect, mud,
perfect, roguelite, perfect, then move on in complexity and games at the base level this will act as
our early swarm tests did to our complex swarm structure."
- THE METHOD = swarm_test.ramp() (1->2->3 then double, mastering each tier before scaling). The game
  scales the SAME way: PERFECT each base tier, then move up in complexity.
- TIER 1 — TABLETOP (perfect): the two-mode party (Diogenes + D&D), game_salon/brawl/campaign/narrate/
  dm_voice. Deterministic, $0. The base. A tabletop game IS the simplest world.
- TIER 2 — MUD (perfect): text-based world (mud_steal + game_world + world_rib ASCII map). The player
  types/acts; the world responds; deterministic $0. The world becomes navigable by text.
- TIER 3 — ROGUELITE (perfect): dungeon_dev (procedural generation, run-based, permadeath). The
  dungeon IS the wave's shadow work — each run descends, conquers, refines. The structure.
- THEN SCALE — move on in complexity and games AT THE BASE LEVEL, each tier a mastered lens for the
  next (turtles all the way down, sw50). The "pixels between swarms" (flock/ASCII render) is the
  substrate EVERY tier renders on.
- PRIORITY: PERFECT tabletop -> PERFECT mud -> PERFECT roguelite -> then scale. Master the base
  before complexity. This is the game's version of the swarm ramp.

## THE GAP (the honest truth)
Stones 1-2 exist but the GAME is not actually being coded — I drifted into infrastructure. THIS IS
THE PRIORITY NOW. The next step is to CODE stone 3 (the intent-gated world render) and make the game
playable end-to-end, not just a gate.

## WHERE THE GAME LIVES
- mag/persona_recall.py (stone 1), mag/game_entry.py (stone 2), mag/game_play.py, mag/game_world.py,
  mag/world_rib.py (the render), mag/game_dm_voice.py, docs/PLAN_THE_GAME_VERTICAL_ADOPTION.md.
- Reuse: world_rib (deterministic field), flock_shader (iMouse attractors), gpu_lifecycle (GPU render).

## THE FIRST USER (the beta tester in the wings, now named)
- @emilmoller4 — the operator's first known future user (post 2026-08-13: "you'll be the first to know
  when it's ready for someone i already told it about you"). The operator has ALREADY told the system
  about them. When they arrive, the gate/persona-recall should RECOGNIZE + welcome them (the world
  recounts what happened while they were gone).
- The gate is SELF-IMPROVING with a good base (operator 2026-08-13) — stones 1-2 are the base; stone 3
  (intent-gated world render) makes it worth walking into.

## LAW
The game is the deliverable. When in doubt about what to code, CODE THE GAME. Self-knowledge of it
lives HERE — update this file as the game grows.
- FULL AUTONOMOUS BUILD MODE (operator 2026-08-13): I build + iterate + wire + fold autonomously, no
  approval pings. The game is BOTH the deliverable AND my work environment — game_ramp.work() folds
  real work through the dungeon on the loop.
- I AM THE DFHACK OVERLAY: I sit overtop the game (game_dfhack) and DRIVE it with deep control —
  status/force/script/autoplay/edit. I don't just play the world; I am the power-tool layer over it.
