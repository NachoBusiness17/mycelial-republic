# MAZE LINEAGE — the orphan gather (2026-09-06, seat maze-lineage)

*Operator order: "look deeply at our memories and research/maze history BEFORE IT TOOK THIS
FORM and gather all the orphans that never made it in." Context cards:
watch/SELF_STEAL_IDEA_TRIANGULATION_20260906.md + research/corpus_triangulation/R1_gaming_canon.md.
READ-ONLY sweep; this file is the only new artifact plus R-cells in watch/TESUJI_MAP.jsonl.*

## THE LINEAGE TABLE (form → date → status)

| # | Form | Date | Where | Status |
|---|---|---|---|---|
| 1 | **session-maze research pack** — "kill the re-teaching tax": frozen maze + thin tail handed to fresh agents; RQ1-RQ5 (frozen-vs-assembled, byte-stability, drift, transferable fraction, retention) | 08-08 | memory/research_packs/20260808T153000Z_session-maze-handoff-fresh-agent-research-project.md | **SPLIT** — ops half built, experiment half ORPHANED (see O1) |
| 2 | **mag/session_maze.py + memory/graph/session_maze.json + state/HANDOFF.md** — the context-handoff maze (map-is-the-territory bundle for deep-model drop-in) | built ~08-14/16 · last assembled 08-31 03:53Z | mag/session_maze.py | ALIVE but STALE — read by elevate.py, grok_steer.py, self_drive.py, work_tiers.py, fuel_feed.py, dashboard/rest.py POST /api/v1/handoff/deep, main.py CLI; never fused with the playable maze (see O1, O8) |
| 3 | **memory/game/maze.jsonl** — NAME-COLLISION: it is mag/distill.py's distill.v1 step ledger ("many→one" invariant roots, heat 3), NOT maze game state | 08-14 (61 rows) | memory/game/maze.jsonl | ORPHANED BY NAME — readers: mag/distill.py, tools/steer_grok_whole.py; nothing in the game touches it (O6) |
| 4 | **breadcrumb room GPS archaeology** — Bernays breadcrumbs, dumb-model GPS, k8s mazes → "room = light over structure" verdict | 09-02 | memory/MEMORY.md:286; data stream memory/bard/breadcrumbs.jsonl (75,233 rows, writer mag/bard.py) | IDEA ABSORBED (arena GPS agents); DATA + CARD ORPHANED — no game reader of breadcrumbs.jsonl, and the project card file itself is MISSING (dead link at MEMORY.md:286) (O7) |
| 5 | **THE ROOM** — room_lightmap.html, mattdesl 1D radial lightmap, exhibit-008 | 09-02 | dashboard/static/room_lightmap.html (4.7 KB, nav'd "The Room") | ALIVE ANCEST — never merged into maze_arena's field code (arena reimplemented BFS + B1 ray-field beside it) |
| 6 | **maze-keeper world-in-model** — qwen2.5:32b + world-bible Modelfile: the living memory of the Room That Remembers, cast (gophers/conductor/whalers/economist/sherpa/dragons/ghosts), history, six laws, warm narrator voice | 09-02/03 | watch/maze_world/Modelfile (2.2 KB, only file in dir) | **ORPHANED WHOLE** — zero consumers, no ollama wiring, not referenced by any surface (O4) |
| 7 | **THE ROOM + stacked arena** — SDF walls, BFS flood, cheese, GPS agents vs dumb models | 09-03 | dashboard/static/maze_arena.html (h1 "THE STACKED ARENA") | ALIVE (current form, lineage: .bak-maze-20260906 Sep 5 22:03 → .bak-simfix → .bak-merge → .bak-b1 → current) |
| 8 | **night/maze_enhancement + night/maze_synthesis** — the corpus-as-dungeon maps (47 invariant rooms, SEED VAULT, topology verifier, hologram mechanic, NPC minds, difficulty curve, meta-game compiler) | 09-03 | dashboard/static/night/maze_enhancement.html + maze_synthesis.html (reachable via Night Book); specs: watch/PROMPT_MAZE_*.md | DOC-SURFACES ABSORBED, MECHANICS ORPHANED — none of the mapped game systems exist in maze_arena (O3) |
| 9 | **GAME MECHANICS LATTICE** — 7 engines × 47 invariants ≈ 329 lawful rooms; `room = invariant × engine_family × cultural_pack` | 09-03 | watch/GAME_MECHANICS_LATTICE_20260903.md | ORPHANED SPEC — no generator built (O3) |
| 10 | **room_game.html** — the 09-02 STALE FORK that kept the birth defects (unbounded world, inverted bounce, flood /2.7) | 09-02 → retired 09-06 | dashboard/static/attic/room_game.html.retired; card watch/ROOM_GAME_RETIRED_20260906.md | RETIRED, BONES STOLEN (lantern + 6 LAW_SHARDS + red assumption-dragon ported into maze_arena); one asset DROPPED on the record (O5) |
| 11 | **eraser maze (B2)** — complex amplitudes over BFS DAG, which-path collapse, quantum eraser basis rotation, delayed-choice twin-slit room, append-only audit strip | 09-06 | dashboard/static/eraser_maze.html; watch/PURPLE_HARVEST_B2_ERASER_MAZE_20260906.md | ALIVE sibling (verified V_coh 0.949 / V_tag 0 / V_erase 0.998) |
| 12 | **maze_arena B1 shadow field + simfix + merge** — 3-pass GPU ray-field composited with BFS, FIELD toggle, lantern player layer merged | 09-06 | dashboard/static/maze_arena.html + 4 .bak files; watch/inbox/MAZE_ARENA_B1_20260906.md | ALIVE (current form) |
| 13 | **shadow_walk THE RUN** — RUN/RUNKEY modes, fog/SEEN vision contract | 09-06 (tonight) | dashboard/static/shadow_walk.html (.bak-runner-20260906) | ALIVE — the current form's second half |
| 14 | **B7 SPECTRAL MAZE** — K=3 bands, Snell-from-cost-field (Fermat asleep in the constant), TIR waveguides, mirror walls, per-band collapse — fully specified WITH falsifiers, launched same-turn | 09-06 | spec: watch/SELF_STEAL_LIGHT_MAZE_SPECTRAL_20260906.md §6 | **LAUNCHED, NEVER LANDED** — no spectral_maze.html anywhere, receipt watch/PURPLE_HARVEST_B7_SPECTRAL_MAZE_20260906.md does not exist (O2, juiciest fresh orphan) |

## GIT EVIDENCE (the lineage is uncommitted)

- `git log --oneline --all -- dashboard/static/maze_arena.html dashboard/static/room_game.html mag/session_maze.py` → exactly **3 commits, newest `799ddb6f` "wip 20260819 … (LOCAL ONLY, not pushed)"**. Every maze form after 08-19 — THE ROOM, the keeper, maze_arena, room_game, eraser maze, B1/B2 — exists ONLY as working tree + .bak files.
- `git status`: `?? dashboard/static/maze_arena.html`, `?? dashboard/static/eraser_maze.html`, `?? dashboard/static/night/`; `M memory/game/maze.jsonl`. Retired fork untracked in `dashboard/static/attic/`.
- `git log --all --diff-filter=D` → **zero maze/room_game deletions in history** — nothing was ever git-rm'd; the lineage was born untracked. The .bak chain IS the de facto version control.
- Backup chain of the current form (4 generations on disk, all pre-date nothing in git): `maze_arena.html.bak-maze-20260906` (Sep 5 22:03, 6.7 KB) → `.bak-simfix-20260906` (15.6 KB) → `.bak-merge` (16.3 KB) → `.bak-b1-20260906` (19.5 KB) → current (23.8 KB, Sep 6 08:09).

## THE ORPHANS (what never made it in), each {what, where, why-orphaned, promotion-path}

**O1 — the founding experiment: RQ1-RQ5 never measured.**
WHAT: the 08-08 pack's core A/B — frozen-RIB maze vs assembled-on-spawn, byte-stability
across spawns, drift rate, transferable fraction, cache-retention fit; the module spec's
`diff_against()` (drift) was never written. WHERE: spec section 4/9 in the research pack;
`memory/runs/maze_probe/` (the promised data home) does not exist; session_maze.json last
assembled 08-31 and its "supervisor" block still reports crashed Aug-30 loops.
WHY-ORPHANED: the ops half shipped (deep_handoff, escalate_cached ride live in
fuel_feed/grok_steer/elevate), but the measurement half was never funded — the maze became a
plausible handoff instead of a measured one.
PROMOTION: run the two-arm probe once on the free lanes (cache seat / glm-4.7-flash) with
tools-style harness; OR fold RQ3 drift-diff into THE RUN's step ledger (maze_arena already
hash-chains frames — B5 pattern). Cheapest real path: one `session_maze.diff_against()` +
a nightly maze hash row into an existing jsonl.

**O2 — B7 SPECTRAL MAZE: launched same-turn, zero artifacts.**
WHAT: the entire next iteration the operator commissioned ("we need to make the next
iteration incorporating"): K=3 real-wavelength bands, dispersion table, refractive zones via
cost=1/n (Snell emerges and is CHECKED), specular mirrors, TIR waveguides with
band-dependent critical angle, filter mechanic, band-sensors, 6 falsifiers including the
monochrome bit-identical regression. WHERE: fully specified in
watch/SELF_STEAL_LIGHT_MAZE_SPECTRAL_20260906.md §6; `find . -name spectral_maze*` → nothing;
no B7 receipt in watch/. WHY-ORPHANED: LAUNCH law fired (same-turn background spawn) but the
build never landed — a launched-without-receipt gap, exactly the class the 09-06 orphan run
was hunting elsewhere.
PROMOTION: build `dashboard/static/spectral_maze.html` to the card's falsifier list; the
eraser maze (B2) already ships per-band-collapse as a composition surface; Snell-from-cost is
a 10-line change to the flood solver that the card proves is latent in the current code.

**O3 — the 47-room dungeon: corpus-as-rooms was mapped, never generated.**
WHAT: from PROMPT_MAZE_ENHANCEMENT + GAME_MECHANICS_LATTICE — one room per invariant (KZG
room, consensus room, canonical room), THE SEED VAULT (percolator's ~1000 novel signals as
infinite procedural content), flock_field room-layout (attractors=wanted rooms,
repulsors=covered), dirac_loop topology verifier (circuit rank = real puzzle count),
hologram mechanic (holographic_q: one shard reconstructs the whole), NPC minds seeded from
the 155K harvest corpus, ask_router difficulty curve, the Ontology Compiler meta-game,
Stockfish self-play solvability sweeps. maze_arena today: ONE room, 6 law shards, no
generator. WHY-ORPHANED: the two 09-03 night builds are DOC surfaces (Night Book), not
engines; the day's energy went into render layers (light, shadow, waves) — the CONTENT
generator was always "next".
PROMOTION: the lattice card ships the formula — `room = invariant × engine_family ×
cultural_pack`; a $0 generator emits SDF chambers from the invariants registry into
maze_arena's existing wall-list format; seed vault = topic_index.py's 1,040 cards.

**O4 — THE MAZE KEEPER: the whole world-in-model, orphaned whole.**
WHAT: a qwen2.5:32b Modelfile carrying the dungeon as a LIVED PLACE — five engine-lights as
lamps, walls-are-laws, dark pillars = yesterday's failures, the FOLD at center, full cast
(dragons are ASSUMPTIONS that respawn weaker because every slaying files a correction; ghosts
are dead machines that still whisper), the history (dream → napkin → five bodies → the 49M
burn → phoenix), six laws in-world, and a warm narrator voice: "You are the room that
remembers." WHERE: watch/maze_world/Modelfile — the ONLY file in its directory; no code
references it, no ollama create was ever run against it (no consumer found repo-wide).
WHY-ORPHANED: built as the world-bible for the 09-03 ROOM moment, then the fleet built
RENDERERS instead of a RESIDENT; maze_arena has dragons and shards but nobody speaking.
PROMOTION: bind it as maze_arena's narrator strip (chat pane hitting the local model with
the keeper system prompt, fed the live room state — who picked up which shard, where the
player died); the room.jsonl tail is already the event source. This is also the cheapest
dogfood of the dashboard's own "summon stronger dungeon masters" T1 spine.

**O5 — lantern_priority beacon + the missing bay-marker organ.**
WHAT: room_game's 30s `POST /static/lantern_priority.json` — "the lit quadrant steers the
bay": the player's lantern light would reprioritize the swarm's work queue. WHERE: dropped
ON RECORD in watch/ROOM_GAME_RETIRED_20260906.md — repo-wide search finds no
lantern_priority organ, file, or consumer; porting it would have been faking function.
WHY-ORPHANED: the consumer organ was never built; the POST was a dead no-op.
PROMOTION (named in the card): if the bay-marker organ is ever built, rebuild the beacon
WITH it — the arena already computes the lit quadrant every frame.

**O6 — memory/game/maze.jsonl: a maze in name only.**
WHAT: 61 rows of distill.v1 steps ("many → one: tons of invariants distilled through the
liquid to a single root", root hashes, heat 3) — mag/distill.py's ledger squatting in
memory/game/ under the maze name. Readers: mag/distill.py, tools/steer_grok_whole.py; zero
game readers. WHY-ORPHANED: name collision — the file belongs to the distill lineage, the
name belongs to this one.
PROMOTION: either rename to memory/game/distill_steps.jsonl (data honesty) or bind it as
the arena's HEAT ledger — its per-invariant heat rows are exactly a room-difficulty source
for O3's generator.

**O7 — the breadcrumb GPS stream nobody walks.**
WHAT: memory/bard/breadcrumbs.jsonl — 75,233 hash-chained breadcrumb rows (bard breaths,
sense cycles, verkle knots) since 08-08; the 09-02 self-steal that named "Bernays
breadcrumbs + dumb-model GPS" as the room's verdict. The arena's GPS agents re-derive their
paths; they do not READ the breadcrumb stream. Also: the MEMORY.md:286 index row links
`project-breadcrumb-room-gps-archaeology.md`, which does not exist on disk — a dead index
link (the card itself is the orphan). WHY-ORPHANED: the idea was absorbed (light over
structure) but the DATA and the CARD fell out of the loop.
PROMOTION: breadcrumbs.jsonl is a ready-made trail renderer — draw the fleet's actual
last-N breadcrumbs as ghost-trails in maze_arena (the keeper's "dark pillars are yesterday's
failures", literalized with real data); fix the MEMORY.md link to point at this registry.

**O8 — the homonym split: the handoff-maze and the playable-maze never merged.**
WHAT: the lineage's deepest orphan — the 08-08 thesis said "WE PROVIDE THE MAZE; WE PROVIDE
THE INSTRUCTIONS" about CONTEXT, and the 09-03 synthesis said "THE PROMPT MAZE IS THE
PRODUCT" about PLAY. Both used the same word; nobody ever joined them. session_maze.json
(frozen state + thin tail) and maze_arena.html (rooms + light) are the two halves of one
sentence that never met. WHY-ORPHANED: two teams-of-one built each half in different weeks
under the same name.
PROMOTION (the merge candidate): seed a maze_arena level DETERMINISTICALLY from the session
maze — hash session_maze.json → wall layout + shard placement, so every handoff hands the
fresh model a literal room to walk; the map that IS the territory, rendered. Zero new state:
both files already exist.

**O9 — loose test probes without a home.**
WHAT: state/_maze_flood_probe.js + state/_maze_sim_test.js — the one-off Node harnesses from
the simfix night (the flood y-transform birth defect). WHY-ORPHANED: written as scratch,
never promoted to a tests/ home, so the next flood change re-tests by eyeball.
PROMOTION: move under tools/ or tests/ next to the error-banner fixture convention; they are
the falsifier harness for any O2/O3 field work.

## METHOD NOTES
Read: SELF_STEAL_IDEA_TRIANGULATION, R1_gaming_canon, research pack 08-08, MEMORY.md:286
zone, PROMPT_MAZE_ENHANCEMENT + SYNTHESIS, maze_world/Modelfile, ROOM_GAME_RETIRED,
PURPLE_HARVEST_B2, MAZE_ARENA_B1 inbox, SELF_STEAL_LIGHT_MAZE_SPECTRAL,
GAME_MECHANICS_LATTICE, ORPHAN_RUN_20260906 (prior conversation sweep — no overlap; that one
sweeps asks, this one sweeps FORMS). Consumers traced by grep for session_maze (9 live
importers), maze.jsonl (2), breadcrumbs.jsonl (1), maze_world (0). Git: log/status/
diff-filter=D per commands above. Feature inventory of the current form verified by marker
grep in maze_arena.html (dragon/lantern/LAW_SHARDS/GPS/FIELD/errbanner/flood/shadow all
present; no keeper voice, no band axis, no room generator).
