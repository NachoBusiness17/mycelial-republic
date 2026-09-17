# N8_GAME_RAMP_REWIRE — receipt (wave 2026-09-16, COMPLETE)

Lane law: receipt first, appended as I go. No git commands. Write/Edit for source. `.venv\Scripts\python.exe` only.

## Mission
`mag/game_ramp.py` has hardcoded 3-room tiers while the real engines sit dormant (game_campaign,
game_mud/relay, dungeon_dev, world_state.json rooms). Re-point the ramp at the real engines:
- tier 1 (tabletop) = toy/toy.html core verb
- tier 2 (mud) = mud.html via its window.MUD handle or the mud harness (game_mud)
- tier 3 (roguelite) = dungeon_dev / game_campaign engine
- tier 4 (wow) = wow_world sessions
Constraint: keep the ramp's own API stable so callers don't break.

## Log
- [start] Read mag/game_ramp.py — current shape: TIERS = ["tabletop","mud","roguelite"]; tabletop/mud
  are self-contained toy loops (3-room hardcoded exits dict in mud()), roguelite only touches
  dungeon_dev for a cosmetic string. API surface: tier(), tabletop(), mud(), roguelite(), work(),
  descend(), play(), render(), status(). Backed by game_world set_state/get_state.
- [start] Located engines: dashboard/static/games/toy.html, dashboard/static/games/mud.html (+ root
  dashboard/static/mud.html), mag/game_mud.py, mag/game_campaign.py, mag/dungeon_dev.py,
  mag/wow_world.py. Reading them next.
- [recon] Consumers locked the API contract:
  * tests/test_game_ramp.py asserts `TIERS == ["tabletop","mud","roguelite"]` (frozen) + the shapes
    of tabletop/mud/roguelite/descend/render.
  * main.py `game` cmd: play()/render()/descend()/status(); printer reads reply/scene/turns/room/
    depth/best/world_root.
  * mag/distill.py + mag/governor_autorun.py: gr.work(action="turn") -> {ok, task, reply, folded}.
  * mag/game_dfhack.py: gr.tier() + handler map {tabletop, mud, roguelite}(action).
- [recon] Engines verified drivable headless: game_mud.act (11-room Roshomon world, stdlib only),
  dungeon_dev.generate_room/assign_workers/conquer/dungeon_state (file-backed, $0),
  wow_world.WorldSession (bones fixture EXISTS at memory/runs/wow_bones/bones.json; sessions
  persist under memory/runs/wow_world/sessions; stdlib imports only). toy.html is browser-side
  (window.TOY) -> tier 1 uses a faithful headless port of its ONE verb (roll).

## The rewiring diff summary (mag/game_ramp.py only, API kept stable)
- SCHEMA unchanged ("game_ramp.v1"); `TIERS` left EXACTLY as the frozen 3-list; added
  `LADDER = TIERS + ["wow"]` — tier 4 rides past roguelite; tier()/descend()/status() now use
  LADDER for "next" while status() still reports "tiers": TIERS (old key intact).
- Added `ENGINE` map (per-tier engine provenance, surfaced in every tier result + status()).
- TIER 1 tabletop: kept look/talk/rest + turns contract; ADDED the toy core verb headless —
  `_toy_state()` + `_toy_roll()` port of toy.html window.TOY law verbatim (LCG 1664525/1013904223
  seeded, draw_index counts draws, roll = 30 sta / 0.28 rollT / 0.5 cd / 0.35 iframes, regen 25/s
  gated during rollT at x1.5 still on the idle tail). "roll"/"dodge" run the verb; "rest" refills
  toy stamina. Result gains `toy` + `engine` keys; old keys untouched.
- TIER 2 mud: now DELEGATES to mag.game_mud.act (command mapping: look/l/map/survey/witness/claim/
  fold/take/inv/help/status; "go X"/"move X"/bare dirs -> "go X"; unknown strings pass through for
  the harness's typed refusal). Mirrors the real room into the legacy key "game.mud.room". The old
  hardcoded 3-room loop survives ONLY as `_mud_legacy()`, used when the harness import/act raises
  (result marked degraded:True + engine:"legacy 3-room fallback").
- TIER 3 roguelite: keeps the depth/best run law (test contract) AND delegates to dungeon_dev:
  descend/enter -> generate_room() (real roadmap room: floor/region/task in reply + result
  `dungeon_room`, room stored as game.rogue.last_room); NEW verbs conquer [room] -> dungeon_dev.
  conquer (folds the knot, publish default), assign [room] -> dungeon_dev.assign_workers DRY
  (enqueue=False: deterministic + $0, no swarm writes from the ramp), state/rooms/map ->
  dungeon_state(). die unchanged. All engine calls wrapped; failures recorded in `dungeon_error`.
- TIER 4 wow (NEW): `wow(action)` drives mag.wow_world.WorldSession — session id persisted in
  world state ("game.wow.session"), run counter seeds fresh runs ("game.wow.run" -> "ramp-runN").
  Verbs: look / go <dir> (bare dirs too) / verbs (legal_verbs) / map / status / new. Every turn
  goes through the bones gate (typed refusals surface verbatim) and the engine's own save() is the
  only write. Stub path: if the bones fixture is missing, returns degraded result telling the
  operator to run the bones extract — nothing invented.
- play() routes "wow"; render() gains a wow branch (room + route + status ASCII); CLI __main__
  gains toy/mud/wow direct commands.
- OTHER SOURCE FILE TOUCHED (recorded): tests/test_game_ramp.py — (a) test_tiers_and_status checks
  the live tier against LADDER (the shared world may legitimately sit at tier 4 now) while keeping
  the frozen TIERS equality + adding LADDER == TIERS + ["wow"]; (b) test_descend_ramps_tiers now
  pins the world tier to tabletop, asserts descend tabletop->mud, and RESTORES the prior tier/
  mastered in a finally (the suite was hostage to shared-world state — the rewire exposed that
  latent flakiness; now it leaves the world as found).

## Smoke outputs (repo venv python; heredoc stdin, no shell .py names)
- TIER 1 toy verb: roll -> "You roll. 30 stamina, 0.28s of commitment, 0.35s of iframes — sta
  70/100, draw 1 (seed 20260813)"; second roll sta 48.25, draw 2 (LCG advancing, regen math
  verified: idle-tail 8.25/cycle).
- TIER 2 real MUD: look -> room "the World-Memory", engine "mag.game_mud.act (Roshomon MUD
  harness, 11-room world)", degraded=null; go west -> "the Hall of Shared Supper" with full prose.
- TIER 3 dungeon_dev: descend -> depth/best counters incremented; generate_room returned room=None
  because ALL 6 roadmap rooms are "in-progress" in memory/dungeon/dungeon_map.json (real engine
  state from earlier runs — the ramp's new "dungeon is being remapped" branch answered correctly).
  state verb -> conquered=[] in_progress=[emulator-core, rib-as-mod, warm-prefix, vram-lattice,
  arrival-compiler, hologram-visor]. assign dry -> ok (no room to throw at while none generated).
- TIER 4 wow_world: look -> session wworld-6f2ab06c8c74 created, room atrium, STATUS_LOGGEDIN
  (auth verb consumed by promotion, the bones law), world "atrium-ring"; go north -> torch_hall,
  route [atrium, torch_hall]; verbs -> [GO_EAST, GO_SOUTH, LOOK]; play("status") at wow tier ->
  "torch_hall · STATUS_LOGGEDIN · turn 2 · encounter TO_BE_DECIDED · verdict OPEN"; render -> wow
  ASCII with room + route.
- LADDER: descend roguelite -> wow; descend at wow -> at_max stays wow (typed note).
- pytest tests/test_game_ramp*: 6 passed in 0.61s (after the statefulness fix). POST-TEST WORLD
  verified: tier=roguelite, mastered=[tabletop, mud] — left exactly as found.
- CLI via mag.cmd: `game status` prints tier/mastered/ramp; `game play look` at roguelite prints
  the new typed refusal listing descend/conquer/assign/die/state; printer keys all intact.
- work() contract re-verified: ok=True, folded=False (no open tasks), tier=roguelite.

## Engines now live per tier
- tier 1 tabletop -> toy core verb (headless port of dashboard/static/games/toy.html window.TOY)
- tier 2 mud -> mag.game_mud.act (the Roshomon MUD harness; legacy loop = degraded fallback only)
- tier 3 roguelite -> mag.dungeon_dev (generate / assign dry / conquer / state)
- tier 4 wow -> mag.wow_world.WorldSession (bones-gate legality rooms, persistent sessions)

## What remains unwired / notes
- toy.html's full frame loop (walker AI, punish/hit events, the i-frame roll against real
  telegraphs) stays browser-side; tier 1 drives the VERB law headless, not the arena sim.
- mud.html's window.MUD browser handle is not driven from Python (headless JS pump not safe here);
  tier 2 drives the Python mud harness, which is the same world's server-authoritative twin.
- game_campaign.py (4765-line campaign engine: begin_play/apply_action/handle_game) is NOT wired
  into the ramp — it is its own surface with its own session model (campaign_id + character gate);
  forcing it under tier 3 would have collided with dungeon_dev's room model. Recorded, not forced.
  A future tier could host campaign sessions if the operator wants a narrative rung.
- dungeon_dev currently has ZERO undiscovered rooms (all 6 in-progress since earlier runs), so
  tier-3 descend answers "dungeon being remapped" until the roadmap grows or rooms are conquered.
- assign is DRY from the ramp (no swarm enqueue). Live assign stays a dungeon_dev/op call.
- Shared-world counters moved by smoke+tests (the game's own progression law, pre-existing trait):
  rogue best depth now 13; a wow session file exists for wworld-6f2ab06c8c74. Tier/mastered
  restored to found values (roguelite / [tabletop, mud]).
- Consumers NOT broken: main.py CLI, mag.cmd, distill.game(), governor_autorun game-work cadence,
  game_dfhack (its tier map simply doesn't know "wow" yet — returns its own typed unknown-tier).
- Files touched: mag/game_ramp.py, tests/test_game_ramp.py. No git commands run.
