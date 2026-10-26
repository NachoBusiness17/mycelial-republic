# DD GAMES AUDIT - gala lane dd-games-audit (division B), 2026-10-03

The owed waltz: read all 4 DD game JSONs and the 3 dungeon HTML pages in full; verdict per artifact on what it is, whether it is playable, what it teaches, and the gap to a playable D&D module; cross-ref the game-dig saved workflows. Receipt is the finish line.

Read in full this session: `dashboard/static/games/dd_dragon-hoard.json`, `dd_gelatinous-cube.json`, `dd_mimic-plate.json`, `dd_riddle-door.json`, `dashboard/static/dungeon.html` (155 lines), `dashboard/static/incident_dungeon.html` (427 lines), `dashboard/static/worldline_dungeon.html` (89 lines). Supporting surfaces read to ground the verdicts: `dashboard/static/games/ruins_go_engine.js` (417 lines, the consumer), `dashboard/static/games/ruins_go.html` (233 lines), `dashboard/static/games/oracle_dice.js` (88 lines), `dashboard/static/games/ruins_go_pack.json` (33 levels), `dashboard/static/games/index.html`, `watch/inbox/replay_deepseek_thinking/DND_module.md`.

## 1. The four DD encounter JSONs

Provenance: commit `3862c1c8a`, message (paraphrased, dashes normalized): D&D encounters land via groq gpt-oss-120b fast lane; Cube Corridor 7 moves + Mimic Plate 5 moves, gate ALL PASS; pack at 31 levels; 2 more D&D briefs pending (riddle door, dragon hoard). All four are level defs for the Ruins Go engine: tile legend `ruins_go_engine.js:17-18` ('p' plate, 'k' crank, 'b' bridge, 'x' collapse, 's' spear, 'E' exit), spawn from the `player` field (`ruins_go_engine.js:229`), win on 'E' (`ruins_go_engine.js:326`), gems optional (L10, `ruins_go_engine.js:15`). The `p` tile is a pressure plate, not the player; the `player` field is authoritative (so the apparent player-vs-p mismatch is not a bug; verified against the engine).

Playability measured with the engine's own `step()` under Node (BFS over hashed states, full script in checks file):

| file | id inside | in pack? | engine win | signature tiles (k/p/b/s/x) on win path |
|---|---|---|---|---|
| dd_dragon-hoard.json | DD-hoard "Greedy Collapse" | NO | 2 moves (D,D) | NONE |
| dd_gelatinous-cube.json | DD-gelatinous-cube "Cube Corridor" | YES, idx 29, byte-identical | 7 moves (U,U,U,U,R,R,R) | NONE |
| dd_mimic-plate.json | DD-mimic-plate "Mimic Plate" | YES, idx 30, byte-identical | 5 moves (U,U,R,R,U) | NONE |
| dd_riddle-door.json | DD-spear-parity "Spear Parity" | NO | 8 moves (D,D,D,D,R,R,R,R) | NONE |

- The two pack entries match the commit's claimed move counts exactly (7 and 5): the solvability half of "gate ALL PASS" reproduces.
- Pack fold verified by python equality (`cube pack==standalone: True`, `mimic pack==standalone: True`); corroborated by the prior census `watch/inbox/burn_reset_20260927/flash50/games-census.md:100-102`.
- `dd_riddle-door.json` filename does not match content (id is "DD-spear-parity"); same defect flagged at `games-census.md:94` on 2026-09-27, still unfixed today.
- Playable in browser: only the 2 folded levels, via `ruins_go.html:65-67` (fetches `ruins_go_pack.json` and appends). `dd_dragon-hoard.json` and `dd_riddle-door.json` are loaded by nothing: grep across dashboard/, mag/, tools/, memory/, queue/, watch/, state/ finds them only in census receipts and a knowledge-graph listing.
- Design finding (the headline): every level is winnable while ignoring its named mechanic. Cube's hint says "push block down" but the level defines no blocks; its plate/bridge cube corridor is bypassed by the west column. Mimic's inscription says "the treasure is load-bearing" but the win path takes the east perimeter and never enters the treasure room. Spear Parity's spears are never crossed, so the parity mechanic is never exercised. Hoard's crank/bridge/collapse/gems are all skipped by a 2-move walk. "Gate ALL PASS" was a solvability gate; no gate requires the signature mechanic to be load-bearing.

What they teach: the encounter-frame (id/name/chapter/ins/hint/rows/player/gems) is a good level contract, and inscriptions-as-teaching works; but dispatched encounters need a design gate that walks the intended mechanic, or the D&D flavor is wallpaper.

## 2. The three dungeon HTML pages

### dungeon.html: "invariants as lighting" (playable: yes)
6 rooms, each an estate invariant as its lighting, receipt text embedded in the room def (`dungeon.html:30-47`: I1 static-prefix immutability, I2 variable-last ordering, I3 the LLM never solves, I6 falsifiability discipline, P0 append-only or claimed, P1 measured or estimated). RGB channel lenses (`:19-20`); traps blaze only under their channel's light (metamerism as mechanic, `:73-75`, `:102-108`); CPU ray-rect occlusion (`:54-61`); click-adjacency stepping with rendered trail and steps/falls counters. Reachable: linked at `dashboard/static/index.html:236` ("The Game") and `dashboard/static/operator_board.html:132`. Dogfooded: `mag/arena_bench.py` parses ROOMS as ground truth (`mag/arena_bench.py:67,117,159,184`), so the page is a graded surface, not a toy. Teaches: which representation you inspect is the survival skill; estate law is dungeon content; the exit is "the angle where light passes".

### incident_dungeon.html: the 09-06 maze-arena incident, walkable (playable: yes)
4 rooms = 4 real birth defects, inscriptions are the buggy lines (`:60-69`), diagnosis panels are quizzes read from the inscription (`:102-140`), the seal defect is rendered as geometry overflowing the world (`:365-379`). Curator mode (C key) shows the real diff hunks with the post-fix receipt line (`:170-195`). The falsifier gate: finishing requires restating the 4 defect classes (`:154-165`), then the exit teleports to the fixed `maze_arena.html` (`:163`, `:331`). Error banner wired (`:29`). Reachable: `dashboard/static/nav.js:81`. Teaches: teaching = the game (its own thesis, `:158`); the endgame is a restatement, not a door; "bogus fields look alive" kept DISPUTED-AND-KEPT (`:160`).

### worldline_dungeon.html: the telling, rendered from the board (playable: no, by design)
Not interactive: a dungeon-master telling generated by `mag/worldline_dungeon.py` (`OUT` at `mag/worldline_dungeon.py:36`) from real artifacts, with a PROOF table mapping every story element to a receipt (`:71-73`) and live spans weighed at render. The "walk" is your own context window; the last door is row 320 of the tesuji wall, unwritten at render time (`:67`). Drift measured today against the board (the page's own law: "if a number in this dungeon disagrees with the board, the board wins", `:56`): page says the wall holds 319 stones and the door stands OPEN; `wc -l watch/TESUJI_MAP.jsonl` reads 336 rows today, so the wall has passed 320 since the 09-07 render (what row 320 contains is not verifiable from counts alone). Page says the tape is 85 rows / 37 sessions; `wc -l memory/runs/trajectory/steps.jsonl` reads 102 rows. The page itself instructs "Next session, re-run the teller" (`:85`); that re-render is owed since 09-07.

## 3. What the arc teaches about game design

1. Mechanics-as-representation (dungeon.html): information gating (which channel you inspect) beats difficulty gating (hp/speed).
2. Falsifier-as-endgame (incident_dungeon): the win condition is a restatement the player produces, which is also the proof they learned.
3. Live data as level content (worldline): the level IS the ledger, staleness is designed to be visible, and the board outranks the tale.
4. Determinism as design: engine hash includes tick parity (`ruins_go_engine.js:408`), oracle dice are seeded mulberry32 (`oracle_dice.js:6-13`), the D&D module's dice law is sha256 (`DND_module.md` section 2). Replays are receipts.
5. Solver-as-ability: the Rogue class ships the page's own BFS solver as a first-move hint (`ruins_go.html:74,92-111`), the Bard sees spear parity (`:76,159`). The validator became a character class.
6. Inscriptions carry the teaching everywhere: level `ins` fields, room plaques, corridor timeline.

## 4. The gap between what exists and a playable D&D module

- Combat does not exist. `rollStatBlock` output is display-only flavor: `ruins_go.html:176-185` builds a message line from it and never assigns it to game state; hp is never consumed; snakes kill on touch (`ruins_go_engine.js:308`).
- The trait layer is inert and, if ever wired, crashes. `loadLevel` never sets `st.sb` (proven: `st.sb === undefined` after loadLevel). The vision branch in `step()` (`ruins_go_engine.js:344-357`) reads `def.player` at `:348-349`, but `def` exists only as `loadLevel`'s parameter (`:222`) and is not in `step`'s scope. Proven both ways under Node: with no `def` binding anywhere, a wired vision trait throws `ReferenceError: def is not defined`; with `globalThis.def` set, the branch silently reads the global. The berserk branch reads `st.sb` the same way (`:380`).
- The dice module is fully built and unused. `oracle_dice.js` implements d4 through d100, check/advantage/disadvantage, oracle yesNo, pick, seeded log (`:15-87`); its header claims "Used by: mud.html, ruins_go.html, frontier_souls.html" and grep finds zero `OracleDice` references in all three. Dead module with a stale header (corroborating `games-census.md:141`).
- 2 of 4 encounters are orphaned files (dragon-hoard, riddle-door), and one carries a wrong filename.
- The real module exists on paper only: `watch/inbox/replay_deepseek_thinking/DND_module.md` (DICE-LAW DUNGEON v1) has scenes, monsters with HP/AC/attacks/quirks, a sha256 dice law, and honest UNVERIFIED markers on its worked examples. No digital surface implements it; the 4 DD JSONs are its ghost, minus the dice.
- What a playable D&D module needs that is missing here: a persistent party, a combat loop that consumes hp/ac, dice inside the decision loop (OracleDice is ready, unwired), a DM narration seat (Hermes is the natural DM per AGENTS.md, dormant but dispatch-capable), encounters whose named mechanic is load-bearing, and the orphaned levels folded or deleted.

## 5. Cross-ref: the game-dig saved workflows

Saved and listed this session: game-dig-coop-social, game-dig-creature-farming, game-dig-horror-maze, game-dig-liveops-seasonal, game-dig-roguelike-runs, plus game-mechanics-deep-dig. Their receipts (`watch/inbox/GAMEDIG_*_20260926.md`, `GAMEDIG_MASTER_ATLAS_20260927.md`) mine EXTERNAL games (Valheim/DST, Palworld/Stardew, Doors/Lethal, GAGA/Adopt Me, Balatro/Hades) for the wheel spec; the master atlas contains zero references to ruins_go, DD-, or dungeon (grep hits only an unrelated Tinkertown line at `:29`). The method those digs standardize (one digger per brief, clone/reskin/skip verdict, evidence quotes, abuse vectors) has never been pointed at the estate's own game arc. Self-dig gap: the DD encounters would fail their own dig method's implied "mechanic load-bearing" bar, and nobody ran it.

## 6. Checks run (raw output saved to watch/inbox/gala_20260925/dd-selfsteal/lanes/dd-games-audit.check.txt)

1. Engine BFS on all 4 DD levels via `node -e` requiring `ruins_go_engine.js`: wins in 2/7/5/8 moves, signature tiles NONE on all win paths, cube=7 and mimic=5 reproducing commit 3862c1c8a.
2. Pack fold equality via `.venv/Scripts/python.exe` (cube/mimic True, pack census 33 levels, chapters histogram).
3. Player-vs-p legend resolution: parse of all 4 files + engine legend at `ruins_go_engine.js:17-18` and `:229`.
4. `st.sb` inertness + vision-branch crash: Node experiments A (ReferenceError) and B (global def read).
5. oracle_dice consumers: `grep -c OracleDice` = 0 in mud.html, ruins_go.html, frontier_souls.html.
6. Linkage: dungeon.html at `dashboard/static/index.html:236` + `operator_board.html:132`; worldline at `index.html:234`; incident at `nav.js:81`; arcade index `games/index.html` links none of the three.
7. Worldline drift: `wc -l watch/TESUJI_MAP.jsonl` = 336, `wc -l memory/runs/trajectory/steps.jsonl` = 102 vs page claims 319-stone OPEN door and 85 rows.
8. Byte-checked finish line: this receipt file's `wc -c`/`wc -l` recorded in the check file.

No code under mag/ or tools/ was touched by this lane (only watch/inbox/ receipts written), so the violation ratchet is not applicable and was not run.

## 7. Decision ledger

Closes: the owed DD games audit (division B lane). Changes the next DD build decision: "gate ALL PASS" (solvability) is measured insufficient as the encounter bar; the named one-sittings are (a) a design gate that requires the signature mechanic to be load-bearing on a winning path, (b) wire `st.sb` + fix the `def` scoping in the vision branch before any trait goes live, (c) fold-or-delete the 2 orphaned DD files and fix the dd_riddle-door filename, (d) re-run the worldline teller (owed since 09-07), (e) wire or shelve oracle_dice.js. First three are one-sittings; (d) is a command; (e) is an operator call.
