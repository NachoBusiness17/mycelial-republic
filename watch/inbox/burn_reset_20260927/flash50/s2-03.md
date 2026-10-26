# Luau census: roblox/src/ (item s2-03, 2026-09-28)

Census of every Luau file under `roblox/src/` in the Mag Resource Harness repo
(`C:/Users/foste/Documents/projects/local_sovereign_agent`). Every number below
comes from a command run in this session on 2026-09-28; per-file purposes come
from reading each file's header comment block in this session.

## Headline numbers

| Metric | Value | Instrument (exact command) |
|---|---|---|
| Luau file count | 51 | `find roblox/src -type f -name "*.luau" \| wc -l` |
| Total lines | 10,038 | `find roblox/src -name "*.luau" -print0 \| xargs -0 wc -l` |
| Total bytes | 456,309 | same instrument, `wc -c` |
| Non-Luau files under src/ | 4 | `find roblox/src -type f ! -name "*.luau"` (all `src/server/.mimosa/` hook-state JSON, see below) |
| Files opening `--!strict` | 51 / 51 | `grep -l -- "--!strict" ... \| wc -l` |
| Commits touching roblox/src | 26 (2026-09-24 `5e291421a` first, 2026-09-28 `0f75d80c8` latest) | `git log --oneline -- roblox/src/ \| wc -l` |
| In-tree spec/test files | 0 | `find roblox -name "*.spec.luau" -o -name "*.test.luau"` (only false hit: `SpectralMazeZone.luau`, a zone named Spectral) |
| pytest tests/ references to roblox or luau | 0 | `grep -ril "roblox" tests/` and `grep -rli "luau" tests/` both empty |

Per directory (from the per-file `wc -l` listing):

| Directory | Files | Lines |
|---|---|---|
| src/client/ | 4 | 1,054 |
| src/server/ (top level) | 18 | 3,723 |
| src/server/zones_extra/ | 11 | 2,337 |
| src/shared/ | 18 | 2,924 |
| TOTAL | 51 | 10,038 |

## Tests: the honest answer is zero

- No `*.spec.luau` or `*.test.luau` exists anywhere under `roblox/`.
- The repo's pytest suite (`tests/`) contains zero references to `roblox` or
  `luau` (both greps empty this session).
- No test runner config (TestEZ/TestBootstrap/wally/aftman/selene/stylua)
  exists; `roblox/` holds only `default.project.json`, `sourcemap.json`,
  `the_mountain.rbxlx`, `docs/`, `prompts/`, `README.md`.
- Closest thing to tests: two banked standalone `luau.exe` executable checks
  (below), which are runtime-style module checks, not a test suite.

## Runtime verification: three instruments, keep them separate

1. **Static gate, covers all 51:** `tools/mountain_check` = structural lint
   (`tools/luau_lint.py`, advisory) -> rojo sourcemap -> `luau-lsp analyze`
   with Roblox globalTypes defs over `src/shared src/server
   src/server/zones_extra src/client` (i.e. every one of the 51) -> rojo place
   build. This is static analysis plus a build, NOT runtime. This census did
   NOT re-run the gate: it writes `sourcemap.json` + `the_mountain.rbxlx` into
   the shared working tree, which is clean and shared with parallel lanes.
   Last receipted gate evidence: Q-032/Q-042/Q-043 commits (GATE PASS, 0 parse
   failures, rbxlx rebuilt).
2. **Engine-free Luau runtime checks, covers exactly 2 files.** Both banked
   under `watch/inbox/burn_reset_20260927/queue/`, both re-run by this census
   under `tools/bin/luau/luau.exe` (they embed the real module source with a
   Vector3 stub because the CLI sandbox cannot `require`):
   - `shared/Flock.luau`: `Q_032_flock_check.luau` re-run this session ->
     `Q_032_flock_check: 37 passed, 0 failed`, exit 0. Embedded source verified
     byte-identical to current disk bytes: sha256 prefix `959a7179823dbd0f` on
     both sides (matches the sha in commit `0f75d80c8`).
   - `shared/SectionStream.luau`: `Q_043_sectionstream_check.luau` re-run this
     session -> 12 individual PASS lines + `ALL CHECKS PASS`, exit 0.
   - No other Luau file has any executable check artifact.
3. **In-Studio / live-server runtime: zero files.** No Studio playtest has
   been receipted for any of the 51. Evidence read this session: Q-042 receipt
   "no Studio playtest run (owed, like Q-037)"; Q-040 commit "live touch
   playtest owed"; Q-043 receipt honest-limits section "No in-Studio or
   live-server runtime test exists in this session"; lane-close commit
   `372f176bd` still names "Studio playtest per roblox/docs/PLAYTEST.md before
   Sep 29 soft launch" as an open operator gate. `docs/PLAYTEST.md` is the
   20-minute manual script, written but not yet receipted as executed. The one
   live smoke on record (commit `5e291421a`, "LIVE smoke test passed, Elder
   replied in persona") exercised the Python side `tools/roblox_npc_gateway.py`
   over HTTP, not any Luau file.

So the runtime-verification verdict per file: **2 of 51 have executed checks
(Flock, SectionStream), 51 of 51 have only the static gate, 0 of 51 have an
in-engine playtest receipt.**

## Wiring (require graph)

From `grep -rhoE "require\(...\)" roblox/src` and a full walk of
`roblox/sourcemap.json` (run this session):

- Entry points that run as scripts (required-by-0 by design): `init.server.luau`
  (Script under ServerScriptService), `init.client.luau` and the three named
  client LocalScripts (`CathedralMapHud`, `LeaderstatsHud`, `PetOrb`) under
  StarterPlayerScripts. All four client files are mapped in
  `default.project.json` / present in `sourcemap.json`.
- All 18 shared modules are required at least once. Most-required (number of
  distinct requiring files, measured): SeedRng 10, Trove 6, Config 6, Lore 4,
  Worldgen 3, SectionStream 2, ArtifactLore 2, all others 1. `Temptation` and
  `ProceduralBody` are consumed only by `MudBasecamp`
  (`roblox/src/server/MudBasecamp.luau:163`, `:203`, `:216`).
- All 17 top-level server modules plus all 11 zones_extra modules are required
  from `init.server.luau` or their siblings (one require site each observed in
  the tally, the wave wiring per commit `d63a05cdf`).
- **Incidental census finding:** the 4 transient `.mimosa` hook-state JSON
  files under `src/server/.mimosa/` are swept into the Rojo build as
  ModuleScripts (4 entries in `sourcemap.json`, children of
  ServerScriptService). They are not Luau and not game code; the tree currently
  ships them into `the_mountain.rbxlx`.

## Per-file table (51 rows)

Purpose is condensed from each file's own header comment, read this session.
Tests column: none, for every file (see Tests section). Runtime column:
`luau.exe` check name where one exists, else `gate only` (mountain_check static
gate), else `gate only (entry script)`.

### src/client/ (4 files, 1,054 lines)

| File | Lines | Purpose | Tests | Runtime verification |
|---|---|---|---|---|
| client/init.client.luau | 414 | The one client script: input keys in, remotes out, feel out; portal pads tint by server Gate attributes, sphere corner chip, chat log, dash FOV kick, touch buttons (Q-040) | none | gate only (entry script) |
| client/CathedralMapHud.client.luau | 265 | Walker-view overlay rendering THE CATHEDRAL eigen-map from shared/CathedralMap, single authorship of all numbers | none | gate only (entry script) |
| client/PetOrb.client.luau | 262 | Rebirth pet orb LocalScript (Q-042): hatches off the server PetOrb attribute, shoulder follower, gem-collect burst inside the mirrored 12-stud radius | none | gate only (entry script); receipt names Studio playtest owed |
| client/LeaderstatsHud.client.luau | 113 | Always-on scorecard page (Q-041) mirroring the server's four leaderstats IntValues via Changed signals, read-only, no polling | none | gate only (entry script) |

### src/server/ top level (18 files, 3,723 lines)

| File | Lines | Purpose | Tests | Runtime verification |
|---|---|---|---|---|
| server/OssuaryZone.luau | 618 | THE OSSUARY Halloween dungeon: 3-floor seeded backtracker maze, weeping-angel sentinels, bone levers, boulders, Candy Bones economy; floors 2-3 streamed via SectionStream | none | gate only |
| server/MudBasecamp.luau | 465 | Basecamp: the Roshomon MUD as a place (rooms = fleet systems, survey/claim, Vellum's hall, counting circle, garden, terror loop); consumes Temptation + ProceduralBody + Soul | none | gate only |
| server/SwarmZone.luau | 379 | Bullet-hell port of swarm.html: 122bpm pulse, horde + pellets + depth gates, gems as spore fish riding shared/Flock, pheromone horde steering | none | gate only (its Flock dependency has the executable check) |
| server/LedgerExchange.luau | 314 | Steal-a economy cloned 1:1: artifact conveyor, VM slots, steal with carry penalty, counting-circle locks, rebirth, dwarven artifact lore, DF value law | none | gate only |
| server/init.server.luau | 271 | Server entry: builds every zone fault-isolated, dual-ring 18 portals, leaderstats signal bindings, pcall tick hooks | none | gate only (entry script) |
| server/ArrakisZone.luau | 245 | Riding sim port of arrakis.html: speed is score, spice chains, crest launches, thumper redirects, gate banking, Maker telegraph | none | gate only |
| server/HeadMuseum.luau | 222 | Museum of the fleet's minds: one pedestal per persona, heads speak via NpcGateway, Trove-scoped flush loop, souls ride visits | none | gate only |
| server/LightMazeZone.luau | 216 | Flicker Tower (Tower of Hell format): no checkpoints, 8:00 rounds, seeded sections, wisp bullies, Trove-scoped wisp loop | none | gate only |
| server/CathedralPlate.luau | 177 | THE CATHEDRAL made walkable: beacons at CathedralMap eigen centroids, water_first chain over saddle legs, DARK anchor isolated | none | gate only |
| server/TheAnswerBoss.luau | 154 | Summit boss: 5 phases, 15-degree tell, Calabi-Yau deflection, Wing Chun redirect; Trove-scoped fight thread | none | gate only |
| server/ZoneGate.luau | 140 | Sphere-alliance zone access/buffs (WORLDGEN_MINE law 4): owns no zone list, joins come from init's strict-required region field | none | gate only |
| server/SkiZone.luau | 107 | Downhill port of skifree.html: speed ramp, score/frame, trees, crash -> yeti chase | none | gate only |
| server/ShadowLedger.luau | 92 | "The room that remembers": DataStore ledger of observed choices keyed by k-space address, readable by The Watchful Eye pass | none | gate only |
| server/PlayerFeel.luau | 82 | Movement polish layer: sprint, Q dash (server-authoritative, stamps DashAt), double jump with idempotent airJumps | none | gate only |
| server/NpcGateway.luau | 66 | Bridge from NPC heads to the fleet brain via tools/roblox_npc_gateway.py over the free stealth lanes; honest canned fallback when the bus is dark | none | gate only (Python side has the live smoke, not this module) |
| server/AbilitySlots.luau | 65 | Four abilities on Z/X/C/V with server-validated cooldowns as player attributes zones read; carrying disables slots | none | gate only |
| server/Monetization.luau | 59 | MarketplaceService wiring per the monetization plan; id=0 means disabled until Studio SKUs filled | none | gate only |
| server/RuinsGoZone.luau | 51 | Grid puzzle climb: capture tiles/chains by walking; Extra Life rescue product | none | gate only |

(18 file rows; the zones_extra modules are in their own table below.)

### src/server/zones_extra/ (11 files, 2,337 lines)

All 11 are ported estate web games wired by the wave (commit `d63a05cdf`); all
`gate only`, none with tests, none with executable checks or playtest receipts.

| File | Lines | Purpose |
|---|---|---|
| zones_extra/GalleryZone.luau | 266 | The Estate Gallery made physical: Isfahan Lattice Voronoi glass port, Spore Fish (numbers marked CLAIMED, no render source found) |
| zones_extra/RiddleMazeZone.luau | 257 | THE ERASER MAZE (no riddles despite the name): two-layer quantum field maze, unitary phase eraser, delayed-choice PRISM win; ~1,400-part grid streamed in 8x8 chunks |
| zones_extra/FrontierSoulsZone.luau | 239 | Souls-like rim: DEATH boss three phases (hunt-lunge, scythe sweep, dagger fans, shadow steps), MARROW loadout, soul timer |
| zones_extra/ErosionFieldZone.luau | 221 | Erosion sim (runevision technique credit): talus-limited slide, ping-pong erode passes, 7 engines, 6 marbles, paint raise/carve |
| zones_extra/MazeArenaZone.luau | 219 | THE STACKED ARENA: four rounds around the cheese-light (race, moving walls, walking beacon, dwell scoring), six LAW_SHARDS |
| zones_extra/ToyBoxZone.luau | 212 | THE TOY: read -> roll -> punish melee grammar, exact dodge/swing constants, riposte window, single rng draw |
| zones_extra/SpectralMazeZone.luau | 205 | THE MAZE ENTRANCE: seven spoken-riddle gates (lowercase substring match verbatim), threshold keeps your name, clearing files W2-stones to ShadowLedger |
| zones_extra/IncidentDungeonZone.luau | 204 | The 2026-09-06 incident as a dungeon: four rooms = four birth defects, buggy line inscriptions, THE RUN restates the classes |
| zones_extra/SteerFieldZone.luau | 194 | THE FILM: summed radial falloff field, six gradient-climbing sagents sampling 8 directions per 66ms step, lamp writing |
| zones_extra/HardwarePrimerZone.luau | 192 | Electronics dungeon room 1: predict-before-measure beta/hand circuit constants, log-brightness law, verdict tolerance; earns credibility, not revenue |
| zones_extra/LightmapRoomsZone.luau | 128 | THE ROOM (2026-09-02) as a dungeon: radial lightmap, exact engine-light orbit constants, failure-class pillars, center-ring fold |

### src/shared/ (18 files, 2,924 lines)

| File | Lines | Purpose | Tests | Runtime verification |
|---|---|---|---|---|
| shared/CathedralMap.luau | 347 | Eigen-map single authorship: region positions byte-copied from the curvature scan JSON, one convention across data, minimap and plate | none | gate only |
| shared/SphereKinship.luau | 325 | GENERATED (tools/gen_df_luau_data.py): sphere kinship graph -> zone alliances from df_spheres.json, never hand-authored | none | gate only |
| shared/ProceduralBody.luau | 314 | DF build_body_from_rcp fold: weighted 235-profile pick, 1-in-20 leg flip, must_have parts, wisp body assembly | none | gate only |
| shared/Flock.luau | 304 | Boids engine ported from swarm.html (Q-032): flee/tire/rest, school, pheromone trail; pure module, no Instances | none | **luau.exe: Q_032_flock_check 37/37 PASS, re-run by this census, embedded source byte-identical to disk (sha 959a7179823dbd0f)** |
| shared/RcpData.luau | 297 | GENERATED: 235 weighted RCP profiles for ProceduralBody | none | gate only |
| shared/Worldgen.luau | 259 | DF world-history laws: ages driven by megabeast kills with ordinals, forgotten-name compounds, sourced spheres | none | gate only |
| shared/ArtifactLore.luau | 187 | Dwarven artifact naming + strange-mood histories from the raws mine, POS-legal compounds | none | gate only |
| shared/Trove.luau | 122 | RbxUtil-shape scoped cleanup + Loop extension; six hand-rolled task.spawn loops converted to ownership (Q-043) | none | gate only |
| shared/Lore.luau | 126 | MUD rooms translated from mag/game_mud.py: rooms as fleet systems with frontier questions | none | gate only |
| shared/SectionStream.luau | 103 | Streamed-sections pattern (Doors ep.1): one-shot build closures, radius + budget polls, ordered mode byte-identical to eager | none | **luau.exe: Q_043_sectionstream_check 12/12 PASS, re-run by this census** |
| shared/DfGoods.luau | 96 | GENERATED: DF tradegoods/material value tables for DfValue | none | gate only |
| shared/Soul.luau | 91 | DF unit_soul fold: emotions as timestamped ledger rows, stress cutoff ladder, needs pin, static traits | none | gate only |
| shared/DfValue.luau | 89 | DF item-value law: value = BASE x MATERIAL x QUALITY_MULT + QUALITY_BONUS, artifact x20 +300 | none | gate only |
| shared/Config.luau | 78 | The Mountain constants: swarm 122bpm engine, arrakis laws, monetization SKUs (id=0 disabled until filled) | none | gate only |
| shared/Temptation.luau | 65 | DF villain law on Vellum's grant: temptation vs personality/values, ethic weighing, ongoing corruption | none | gate only |
| shared/KSpace.luau | 50 | Knowledge-space addresses (knowledge/practice/depth axes) for the room that remembers | none | gate only |
| shared/SeedRng.luau | 40 | xorshift32 replay-safe RNG: same seed, same mountain, bit-exact; Python mulberry32 seeds map 1:1 | none | gate only |
| shared/RegionSpheres.luau | 31 | GENERATED: generator_region_spheres verbatim from df_spheres.json for ZoneGate joins | none | gate only |

## Honest limits of this census

- `tools/mountain_check` was NOT re-run here (it writes sourcemap + place into
  the shared clean tree). Its coverage claim (all 51 analyzed) comes from
  reading the gate script `tools/mountain_check` in this session, not from a
  fresh run.
- In-Studio playtests: none exist on record; the "runtime verification" column
  for 49 of 51 files therefore reads `gate only`, and for 0 files can an
  in-engine receipt be claimed.
- The Q-043 executable check embeds its SectionStream copy inline (no
  BEGIN/END markers to diff mechanically); its header matches the disk file's
  header and its 12 checks pass on re-run, but a byte-level embedded-vs-disk
  diff was only performed for the Q-032 Flock check.
- Purposes for zone files are header-condensed; game-logic bodies were not
  line-audited line by line (that is a review, not a census).

## Instruments run this session (summary)

1. `find roblox/src -type f -name "*.luau"` (51 files, full list captured)
2. `find roblox/src -name "*.luau" -print0 | xargs -0 wc -l` / `wc -c` (10,038 / 456,309)
3. `find roblox -name "*.spec.luau" -o -name "*.test.luau"` (0 real hits)
4. `grep -ril "roblox" tests/` and `grep -rli "luau" tests/` (both empty)
5. Header read (`head -14 | grep "^--"`) of all 51 files
6. `cat tools/mountain_check` (gate anatomy read)
7. `git log` over roblox/src (26 commits, first/latest identified; luau.exe
   check and playtest-owed claims extracted from commit bodies)
8. `tools/bin/luau/luau.exe Q_032_flock_check.luau` -> 37 passed, 0 failed, exit 0
9. `tools/bin/luau/luau.exe Q_043_sectionstream_check.luau` -> 12 PASS, exit 0
10. Embedded-vs-disk sha256 comparison for Q_032 (identical, 959a7179823dbd0f)
11. Require-graph greps + full `sourcemap.json` walk (wiring table above)
12. `grep -l -- "--!strict"` over all 51 (51/51)
13. Receipts read: `watch/inbox/burn_reset_20260927/queue/Q-032.md`,
    `Q-043.md`, `Q-042.md`; `roblox/docs/PLAYTEST.md`; `roblox/README.md`
