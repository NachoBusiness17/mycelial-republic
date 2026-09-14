# LANE A — STATIC CLASSIFICATION RUN (the backbone)
Date: 2026-09-10 · Scope: `dashboard/static` (structure + content only, no rendering tests)

## THE POINT
`dashboard/static` is the fleet's public surface: ~100 live HTML pages plus ~60 data/media/code assets, where the same EIGHT ideas get rebuilt over and over (verkle-as-place, corpus-as-walkable-room, the live fleet watch, vision-gated mazes/shadow fields, the one console, the music-driven level, paste-checkable verifiers, the seat's self-model) — the duplication IS the emphasis record. Version fragments are everywhere and load-bearing history: nav.js has 14 versions, maze_arena 6, shadow_walk/salon_lightmap 4 each, ~30 pages carry `.bak-nav` siblings from the 09-06/07 nav rewires. The rebuild should sort by family (console / office / rooms / games / fields / verkle / maps / decks / books / data / media), collapse versions into one archive layer, and move multi-hundred-MB payloads (ractor_board 713MB + 2.2GB runaway evidence, ESTATE_INDEX 420MB) out of the web root.

## CLASSIFICATION TABLE
Family codes: **GAME** · **VIZ** · **DASH** (dashboard surface) · **DECK** · **FEED** (data feed) · **TOOL** · **EXP** (experiment) · **BOOK** (record/doctrine) · **CHROME** · **ART** · **CLUTTER**

### Top-level HTML — operator/dash surfaces
| item | family | claims to be | versions/siblings | dup group | subcontent deps |
|---|---|---|---|---|---|
| index.html | DASH | FLEET CONSOLE — everything, one place | .bak-nav (101KB old monolith!), .bak-worldline-20260907 | THE ONE CONSOLE | nav.js |
| home.html | DASH | Home — the six destinations | — | THE ONE CONSOLE | nav.js, media/ (bad_apple ref) |
| index.clear-ui.html | DASH | Mag — Local office (Magatama lineage) | .bak-nav | THE ONE CONSOLE | nav.js, clear.css, clear-boot.js, app.js (351KB), board.js, windows.js, visual.js |
| live.html | DASH | Fleet Live — every window, verbose | — | LIVE WATCH | live_feed.json, overseer.json, grounding_wave.md |
| live_feed.html | DASH | THE FL33T — Live Feed | — | LIVE WATCH | data/canon.json, data/meter.json, data/oracle.json, data/whale_feed.json, data/x_timeline.json |
| fleet.html | DASH | HYPERVISOR · fleet cool/heat + real bills | .bak-nav | LIVE WATCH | /api/v1/fleet/hypervisor, mermaid CDN |
| health.html | DASH | LOOP HEALTH · what works/what doesn't | .bak-nav | LIVE WATCH | /api/v1/loop/health |
| the_radar.html | DASH/VIZ | FLEET RADAR — the watch, visualized | — | LIVE WATCH | /api/v1/fleet/hypervisor |
| feed.html | DASH | Mycelial Republic · Feed | .bak-nav | LIVE WATCH | /api/v1/feed |
| intel.html | DASH | Tonight in your fleet | — | LIVE WATCH | intel.json (no static ref found — probable orphan/dynamic) |
| lanes.html | DASH | LANES — manager board | — | SEAT SELF-MODEL (adjacent) | /static/lanes/*.md (8 lane briefs) |
| decisions.html | DASH | DECISIONS | — | — | decisions.json |
| spend.html | DASH | SPEND — one wall | — | LIVE WATCH (bills) | /api/v1/cost |
| agents.html | DASH | Agents — sub-agent fleet | .bak-nav | LIVE WATCH | /api/v1/stream |
| burn_board.html (+burn_board.png) | DASH | Burn Board | — | LIVE WATCH | (png twin) |
| operator_board.html | DASH | THE OPERATOR'S BOARD | — | THE ONE CONSOLE | — |
| daytool.html | TOOL | DAY TOOL | — | VERIFIERS (adjacent) | day_work_digest.txt, lattices/ |
| ractor.html | DASH | MAG · The Ractor Board | .bak-nav, .bak-surface | LIVE WATCH | /api/v1/ractor/tail, ractor_board.jsonl (**713MB**; + 2.2GB .runaway-evidence sibling) |
| whale_console.html | DASH | WHALE CONSOLE — almanac · doors · council (fl33t) | — | LIVE WATCH | — |
| whale_feed.html | FEED | WHALE PATROL — live feed (fl33t) | — | LIVE WATCH | data/whale_feed.json |
| reply_console.html | DASH | REPLY OVERDRIVE — 36 doors (fl33t) | — | LIVE WATCH | — |
| the_index.html | DASH/FEED | THE INDEX — estate map (open-rib spine v0) | — | CORPUS GRAPHS | index_data/ESTATE_INDEX.jsonl (**420MB**), last_run.json, rollup.json |
| ontology_dashboard.html | DASH | Ontology Compiler Dashboard — Phase 1 | — | CORPUS GRAPHS | /memory/runs/harness/events.jsonl |
| tesuji_map.html | DASH/VIZ | TESUJI FIELD MAP · GLM-5.3-flash behavior surface | .bak-paths-20260907 | SEAT SELF-MODEL | tesuji_map.json, trajectory_paths.json |
| chain_witness.html | DASH/BOOK | THRESHOLD — the cold-start witness door | — | VERKLE AS PLACE | witness_snapshot.json |
| doorbench.html | TOOL/EXP | DOORBENCH — cache-invalidation falsifier | nav.js.bak-doorbench sibling | VERIFIERS | — |
| phonesalon.html (+phonesalon/) | DECK/EXP | PHONESALON — the android free-lane deck | runs/ (5 runs + md) | DECKS | phonesalon_*.png ×7, runs/*.png+.md |
| labs_map.html (+labs_map.png) | VIZ | COMPETITOR MAP | — | — | labs_map.png |

### Top-level HTML — office/voice/communication surfaces
| item | family | claims to be | versions/siblings | dup group | subcontent deps |
|---|---|---|---|---|---|
| wave.html | DASH/VOICE | Mag — standing wave | .bak-nav | VOICE LOOP | wave_scene.js, wave_gpu.js, /api/v1/wave, voice/turn, voice/stt, game |
| table.html | DASH/VOICE | Mag Table — the lantern | .bak-nav | VOICE LOOP | /api/v1/game, voice/turn |
| cast-voice.html | VOICE | Mag Voice | .bak-nav | VOICE LOOP | /api/v1/voice/* (turn, stt, canvas, shadow, handoff, refine), diary/seal |
| cast.html | DASH | Mag Cast (display) | .bak-nav | VOICE LOOP | /api/v1/display |
| wearable.html | VOICE | Swarm HUD — Wearable | .bak-nav | VOICE LOOP | wearable/command, voice/stt |
| keeper_voice.html | TOOL | THE KEEPER'S VOICE (narration) | keeper_voice_harness.js verifier | VERIFIERS + VOICE | keeper_voice_data.json |
| aos.html | DASH | AOS · Bones — Live | .bak-nav | THE ONE CONSOLE | /api/aos/chat, /api/aos/send |
| chan.html | DASH | /keep/ — Anonymous Science | .bak-nav | THE ONE CONSOLE | /api/v1/chan/* (catalog, post, thread, wake) |
| control.html | DASH | Direct Mag | .bak-nav, .bak-surface | THE ONE CONSOLE | nav.js |
| seat.html | DASH | SEAT · ghost surface | .bak-nav | SEAT SELF-MODEL | seat.js |
| sovereign_shell.html | TOOL | Mag Sovereign Shell — Tier 4 chrome MVP | .bak-nav | THE ONE CONSOLE | monaco CDN, shell.js, shell.css |
| steal_tools.html | TOOL | The Armory — 116 steal tools | — | SEAT SELF-MODEL | steal_tools_data.js (auto-gen) |
| grab_write.html | TOOL/GAME | The Tesuji — Grab & Write | — | VERIFIERS (tesuji) | — |

### Top-level HTML — games & walkable rooms
| item | family | claims to be | versions/siblings | dup group | subcontent deps |
|---|---|---|---|---|---|
| game.html | GAME | The Necromancer's Swarm — k3s, dragons, invariants | — | VERKLE AS PLACE (data) | game_verkle_knots.js, 127.0.0.1:8799 saelis API |
| shadow_walk.html | GAME | SHADOW WALK — voxel roguelite · vision-gated · JIT · v2 THE RUN | .bak-runner-20260906, .bak-w5, .bak-warden (**4**) | VISION MAZE | shadow_walk_content.json; generated by _build_shadow_walk.py |
| maze_arena.html | GAME/EXP | GRAY SWAN ARENA · MAG WING — lightmap GPS vs dumb models | .bak-b1, .bak-m2, .bak-maze, .bak-merge, .bak-simfix (**6**) | VISION MAZE (flagship) | grounding_wave.md |
| arrakis.html | GAME | ARRAKIS — the Dune wing · play = dogfood | .bak-fix-20260906 | VISION MAZE | — |
| dungeon.html | GAME/VIZ | THE DUNGEON — invariants as lighting | — | CORPUS AS ROOM | — |
| incident_dungeon.html | GAME/BOOK | INCIDENT DUNGEON — the maze-arena incident, walkable | — | CORPUS AS ROOM | — |
| worldline_dungeon.html | GAME/BOOK | THE WORLDLINE DUNGEON — a telling from the board | — | CORPUS AS ROOM + VERKLE | — |
| conservation_room.html | BOOK/GAME | THE SOWING ROOM — fable of the conservation clause | — | CORPUS AS ROOM | — |
| fable_room.html | BOOK/GAME | THE FABLE ROOM — room #0 · story ∪ record | — | CORPUS AS ROOM | — |
| eraser_maze.html | EXP/GAME | ERASER MAZE — seeing collapses the light (PURPLE HARVEST B2) | — | VISION MAZE | — |
| light_maze.html | EXP/GAME | LIGHT MAZE — what you see is what you know | — | VISION MAZE | — |
| spectral_maze.html | EXP/GAME | SPECTRAL MAZE — three bands, one flood (PURPLE HARVEST B7) | — | VISION MAZE | — |
| pong.html | GAME | PONG — the classics ladder, rung 1 | — | — | — |
| tavern_brawl.html | GAME | THE KABUKI TAVERN — brawl of the ractors | .bak-truthcourt-20260908 | — | — |
| tavern_test.html | EXP | tavern cartridge test | — | MUSIC LEVEL | shaders/library/tavern.glsl |
| shadowbonk.html | GAME | SHADOWBONK — tony mczoom vs the shadow volume | — | VISION MAZE | sb_enemies.json, sb_upgrades_a.json, sb_upgrades_b.json |
| wipeout_v2.html | GAME/VIZ | WIPEOUT v2 — raymarched · the song sets the speed | family: v2 → sunset(v3) → lightmaze + wipeout_raymarch.glsl | MUSIC LEVEL | suno/*.mp3 |
| wipeout_sunset.html | GAME/VIZ | WIPEOUT v3 — synthwave sunset | (see family) | MUSIC LEVEL | suno/*.mp3 |
| wipeout_lightmaze.html | GAME/VIZ | WIPEOUT // LIGHT MAZE — the song is the level | (see family) | MUSIC LEVEL | suno/*.mp3 |
| hardware_primer.html | BOOK/GAME | THE HARDWARE PRIMER — Room 1: The Darlington Pair | — | CORPUS AS ROOM | — |
| arena_operator_field.html | EXP | OPERATOR FIELD · B1a — lights are vector operators | — | SHADOW FIELDS | — |
| bad_apple_field.html | EXP | BAD APPLE FIELD — the room plays the video · B5 (281KB) | — | SHADOW FIELDS | media/ (video/audio refs), .glb |
| airflow_home.html | VIZ/BOOK | AIRFLOW HOME — the house is the prompt | — | CORPUS AS ROOM | — |

### Top-level HTML — shadow fields & visualizations
| item | family | claims to be | versions/siblings | dup group | subcontent deps |
|---|---|---|---|---|---|
| salon_lightmap.html | VIZ | Salon Lightmap v2 — the room that remembers | .bak-embedfix-20260907, .bak-lightmapv2-20260906, .bak-v2 (**4**) | CORPUS AS ROOM + SHADOW | room_state.json (+.prev.json) |
| room_lightmap.html | VIZ | MAG · The Room — 2026-09-02 rendered as a dungeon | — | CORPUS AS ROOM | room_state.json |
| erosion_field.html | EXP | EROSION FIELD — B1 v1 | — | SHADOW FIELDS | — |
| field_quills.html | EXP | QUILL FIELD — instanced EM quills over B1 | — | SHADOW FIELDS | — |
| phase_particles.html | EXP | PHASE PARTICLES — liquid→gas→plasma (room R1) | — | SHADOW FIELDS | — |
| steer_field.html | EXP | STEER FIELD — the film | — | SHADOW FIELDS | — |
| chaos_refract.html | EXP | REFRACT — emergent, unexplained | — | SHADOW FIELDS | — |
| calabi_yau.html | EXP/VIZ | CALABI-YAU QUINTIC — shadow-fields | — | SHADOW FIELDS | — |
| rib_toy.html | EXP/TOOL | THE RIB TOY — a shadertoy for steering packets | — | SHADOW FIELDS | — |
| pipeline.html | TOOL | PIPELINE — the shader cartridges | — | MUSIC LEVEL (cartridges) | shaders/library/manifest.json + 8 .glsl |
| mesh_gallery.html | VIZ | MAG · Mesh Gallery — dungeon content pipeline v1 | — | CORPUS AS ROOM | kimodo_walk_wave.glb, kimodo_walk_wave_strip.glb |
| smith_chart.html | VIZ/BOOK | SMITH CHART — the fold law | — | — | — |
| the_rings.html | VIZ | THE RINGS — one per day (2026-08-25→) | — | LIVE WATCH (adjacent) | — |
| self_hologram.html | VIZ | SELF HOLOGRAM — the seat's self-model trajectory | — | SEAT SELF-MODEL | self_hologram_data.json |
| fleet_symbols.html | VIZ | FLEET SYMBOLS — the operator algebra | — | — | — |
| verkle_knot_wave.html | VIZ | The Verkle Knot — standing wave | — | VERKLE AS PLACE | game_verkle_knots.js |
| verkle_pyramid.html | VIZ | VERKLE PYRAMID — the chain as a place (zone two) | — | VERKLE AS PLACE | verkle_pyramid_seed.json |
| verkle_construction.html | VIZ | THE BIRTH CANVAS — verkle through its construction | — | VERKLE AS PLACE | index_data/verkle_birth.json (+2 .bak generations) |
| viz_3d_verkle.html | VIZ | Verkle Chain — 3D | — | VERKLE AS PLACE | game_verkle_knots.js, local-pulse API |
| viz_horse_run.html | VIZ | Spore Form — the horse (attempt 2) | pair with viz_spore_fish | — | — |
| viz_spore_fish.html | VIZ | Spore Form — the fish (attempt 1) | pair with viz_horse_run | — | — |
| viz_gallery.html | VIZ | Viz Lab — the Republic's visualizations | — | launcher | — |
| universe_within.html | VIZ/ART | THE UNIVERSE WITHIN — the network, with music, in a dark room | — | MUSIC LEVEL | suno/ |

### Maps, tools, checkers
| item | family | claims to be | versions/siblings | dup group | subcontent deps |
|---|---|---|---|---|---|
| memory_map.html | VIZ | The Memory Map — relational graph of the Republic | — | CORPUS GRAPHS | memory_graph_data.js (auto-gen from knowledge_graph.json) |
| module_map.html | VIZ | The Module Map — every mag module, real purpose | — | CORPUS GRAPHS | module_map_data.js (auto-gen from docstrings) |
| rtfm_graph.html | VIZ | MAG · RTFM Graph — the fleet's manuals, browsable | + _rtfm_graph_shell.html generator | CORPUS GRAPHS | built by _rtfm_graph_data.py/_build/_verify |
| museum.html | VIZ/BOOK | MAG · The Museum | .bak-nav; museum/index_old_mag_board.html (retired board) | CORPUS GRAPHS | museum.jsonl |
| chain_check.html | TOOL | Chain Check — verkle knot link verifier v1 | — | VERIFIERS + VERKLE | — |
| claim_check.html | TOOL | Claim Check — launch-law card verifier v1 | — | VERIFIERS | — |
| lattice_check.html | TOOL | Lattice Check — Legendre three-square invariant v1 | — | VERIFIERS | — |
| falsifiers.html | TOOL | Falsifiers — paste-checkable invariants index v1 | — | VERIFIERS | — |
| lattice.html | TOOL/VIZ | MAG · Conspiracy lattice | .bak-nav | VERIFIERS | /api/v1/lattice-lab, :8743 health |

### Decks
| item | family | claims to be | notes | dup group | deps |
|---|---|---|---|---|---|
| decks.html | DECK | DECKS — the pro surface (launcher) | live cost/stream | DECKS | /api/v1/cost, stream |
| scout_deck.html | DECK | MAG // SCOUT DECK | generated by _build_scout_deck.py | DECKS | — |
| decks/cacheecon.html | DECK | "DECK — Legions" template (7 cards) | title clones legions.html | DECKS | — |
| decks/gamebuild.html | DECK | template (25 cards) | largest deck | DECKS | .glb refs |
| decks/glmwatch.html | DECK | template (10 cards) | | DECKS | — |
| decks/legions.html | DECK | template — the original | | DECKS | — |
| decks/mag.html | DECK | template | 575KB | DECKS | .glb refs |
| decks/mesh3d.html | DECK | template (11 cards) | | DECKS | .glb refs |
| decks/personal.html | DECK | template (5 cards) | | DECKS | — |
| decks/rocinante.html | DECK | template (13 cards) | | DECKS | .glb refs |

All 8 deck pages share ONE "DECK — Legions" template with an "INVARIANT HUNT" strip; only card counts/topics differ.

### Books / records
| item | family | claims to be | notes |
|---|---|---|---|
| night/*.html ×21 | BOOK | THE NIGHT BOOK — the 09-02/03 climb (index.html + 20 chapters: chord_v4, design_theory, game_codex, game_lattice, hermes_dossier_v1, hermes_steal_v0, light_codec, light_loop, maze_enhancement, maze_synthesis, morning_state, orphan_register, primer_wired, sherpa_spec, stockfish, surface_atlas, systems_gap_map, the_session_self_steal, time_machinery, titor_stack, trade_sheet) | morning_state refs museum.jsonl; several ref grounding/arena themes. Version pairs: hermes_steal_v0→hermes_dossier_v1 |
| doctrine/*.html ×5 | BOOK | Fleet doctrine renders (AUTONOMY_WHEEL, BURST_DOCTRINE, SWARM_SCALE_PLAN, TRI_PARTY, X_SCOUT_DOCTRINE — each titled "…md — fleet doctrine") | static renders of watch/ cards |
| lanes/*.md ×8 | BOOK | lane briefs (android_surface, bard_ledger, builder, day_work, economist, elder, research) | consumed by lanes.html; trails/*.jsonl are their log twins (no static consumer found) |
| salons/astra/* | BOOK | ASTRA SALON — research steal (BRIEF, FOLD, PRIMER, post_ASTRA, index.html) | self-contained salon |
| grounding_wave.md | FEED/BOOK | GROUND ledger narrative (56KB) | ref'd by live.html + maze_arena.html |
| day_work_digest.txt / DAY_WORK_DIGEST.md | FEED | the day's work digest (twins) | consumed by daytool.html |
| HUMAN_BRIEF_20260906.md | BOOK | human brief | — |

### Shared code (chrome)
| item | family | versions/siblings | role |
|---|---|---|---|
| nav.js | CHROME | current + **13 .bak** (b2-eraser, b5, b7-spectral, batch5, batch5-s2, doorbench, fixall, hologram, nav-decks-daytool, nav-wiring, rehome, surface, w5) — most-versioned file in the tree | single source of nav truth |
| app.js (351KB) | CHROME | — | Magatama office harness (clear-ui) |
| board.js / windows.js / visual.js | CHROME | — | office kanban / tab shell / chamber map |
| seat.js / shell.js / clear-boot.js | CHROME | — | seat surface / Tier-4 shell / clear-ui boot |
| tapestry.js / wave_gpu.js / wave_scene.js | CHROME | — | 3D residual graph / wave renderers |
| keeper_voice_harness.js | TOOL | — | node verifier for keeper_voice.html |
| game_verkle_knots.js (67KB) | FEED | — | AUTO-GEN real chain data — shared by game.html + 3 verkle viz |
| memory_graph_data.js (319KB) / module_map_data.js (196KB) / steal_tools_data.js (57KB) / tapestry data | FEED | — | auto-generated corpus data ("Real bytes, not invented") |
| style.css / clear.css / cli.css (160KB) / shell.css | CHROME | — | per-shell styles |
| manifest.webmanifest | CHROME | — | PWA |
| _build_cli_desk.py / _build_keeper_voice.py / _build_scout_deck.py / _build_shadow_walk.py / _restore_cli_desk.py / _rtfm_graph_{build,data,verify}.py / _rtfm_graph_shell.html | TOOL | — | PAGE GENERATORS — several pages are build products, sources live here |

### Data feeds (loose)
| item | family | consumer | note |
|---|---|---|---|
| ractor_board.jsonl (**713MB**) + .runaway-evidence-20260903 (**2.2GB**) | FEED | ractor.html | evidence file must leave web root |
| index_data/ESTATE_INDEX.jsonl (**420MB**), orphan_ledger.json (4MB), rollup.json, last_run.json | FEED | the_index.html | index should stream, not sit static |
| index_data/verkle_birth.json + .pre_dedupe.bak + .pre_theme_lexicon.bak | FEED | verkle_construction.html | versioned data |
| live_feed.json (145KB), overseer.json, room_state.json + .prev.json, witness_snapshot.json (502KB), museum.jsonl, decisions.json, tesuji_map.json, trajectory_paths.json, keeper_voice_data.json, self_hologram_data.json, shadow_walk_content.json, verkle_pyramid_seed.json, sb_*.json ×3, data/* ×5 (canon, meter 214KB, oracle, whale_feed, x_timeline) | FEED | (see table rows) | live pages |
| **ORPHANS — no static consumer found:** shadow_quests.json (378KB), echo_net.json (181KB), x_radar.json, cite_edges.json, intel.json, read_receipts.json, topic_index.json (3.6MB), trails/*.jsonl ×13, lattices/*.json ×6 (daytool refs the dir only) | FEED | none found | verify against runtime API before deleting; likely stale or API-fed |
| grounding_wave.md, museum.jsonl, DAY_WORK_DIGEST twins | FEED | live/museum/daytool | — |

### Media / art
| group | items | notes |
|---|---|---|
| art/ | quest-art PNGs (astra_dragon, blind_gate, cold_forge, ledger_panel + _v2, prose_furnace, puzzle_001/002 ~1.5MB each) + index.html + forge_log.json | the Forge's wall; ledger_panel has a v2 sibling |
| media/ | grok_is_so_cool.jpg, shape_of_ideas ×2 (v2 + wave), the_lost_civilization.jpg, hi_ghost_sancho mp3, magatama edition mp3+cover+visualizer, radial_lightmap_rib_render.webm, light_finds_center_circle.webm | magatama lineage assets |
| suno/ | 5 mp3 (aerodynamic, dance, flat_beat, genesis…) | fuel for wipeout_* + universe_within + pipeline |
| sound/ | tortoise_crab_canon: mp3 + wav + **_v2.mp3** | versioned music |
| phonesalon/ | 7 screenshots + runs/ (3 runs: png+md) | experiment record |
| loose | kimodo_walk_wave.glb + _strip.glb (mesh twins), philbrick_1964.png (616KB), story-parker-arc.png, swarm_board.png, burn_board.png, labs_map.png, mag-icon.png, tiles/df_curses_local.png | burn_board/swarm_board png twins of html boards |

### Clutter (not content)
- `.mimosa/` hook-state dirs ×5 scattered through the tree (root, art/, shaders/library/) — security-scan tool residue, exclude from IA.
- `__pycache__/` — build residue.

## DUPLICATION-EMPHASIS — the load-bearing organs (what the fleet kept rebuilding)
1. **VERKLE CHAIN AS A PLACE** — 9+ surfaces: chain_check, chain_witness (THRESHOLD), verkle_knot_wave, verkle_pyramid, verkle_construction (BIRTH CANVAS), viz_3d_verkle, worldline_dungeon, night/titor_stack, + shared game_verkle_knots.js data + verkle_birth.json (3 generations). The single most emphasized idea in the tree.
2. **VISION-GATED MAZE / SHADOW FIELD** — ~14: maze_arena (6 versions, flagship), shadow_walk (4), eraser/light/spectral mazes (PURPLE HARVEST B2/B7), arrakis, shadowbonk, arena_operator_field (B1a), erosion_field (B1), field_quills, phase_particles, steer_field, chaos_refract, calabi_yau, bad_apple_field (B5), rib_toy. The shadertoy-steal + purple-harvest waves made this the biggest volume.
3. **CORPUS AS WALKABLE ROOM/DUNGEON** — ~11: room_lightmap, salon_lightmap (4 versions), dungeon, incident_dungeon, worldline_dungeon, conservation_room, fable_room, hardware_primer ("Room 1"), airflow_home ("the house is the prompt"), mesh_gallery (pipeline), night/light_loop ("dungeons as DFA").
4. **LIVE FLEET WATCH** — ~11: live, live_feed (THE FL33T), fleet (HYPERVISOR), health, the_radar, feed, intel, whale_feed, whale_console, reply_console, agents + burn_board. "Am I up, what's it cost" asked ten ways.
5. **THE ONE CONSOLE** — 7 shells: index (FLEET CONSOLE), index.clear-ui (Local office), home (six destinations), sovereign_shell (Tier 4), control (Direct Mag), aos, chan + board/windows/app.js. index.html.bak-nav (101KB) shows an earlier monolith attempt. nav.js: 14 versions.
6. **MUSIC DRIVES THE LEVEL** — 6: wipeout_v2 → wipeout_sunset (v3) → wipeout_lightmaze, tavern_test, pipeline (shader cartridges), universe_within — the wipeout lineage the lane brief predicted (~6 fragments incl. wipeout_raymarch.glsl).
7. **PASTE-CHECKABLE VERIFIERS** — 6: chain_check, claim_check, lattice_check, falsifiers, doorbench, keeper_voice_harness (+ grab_write). The cite-gate culture rendered as browser tools.
8. **THE SEAT'S SELF-MODEL** — 7: self_hologram, seat.html, module_map, memory_map, rtfm_graph, steal_tools (Armory), tesuji_map (+ museum as archive).
9. **VOICE LOOP** — 6: wave, cast-voice, cast, wearable, table, keeper_voice.
10. **CORPUS GRAPHS** — 5: memory_map, module_map, rtfm_graph, ontology_dashboard, the_index (+ topic_index.json data).
11. **DECKS** — 8 template clones + launcher + scout_deck + phonesalon: one "DECK — Legions" template stamped 8 times for X-scouting.

## NESTED-IA PROPOSAL (skeleton for a sorted /static/)
```
/static/
├── index.html          front door (one hub; kill the 4-shell sprawl into tabs)
├── console/            ops dashboards: live, live_feed, fleet, health, the_radar, intel,
│                       lanes, decisions, spend, feed, agents, burn_board, operator_board,
│                       ractor, whale_console, whale_feed, reply_console, daytool,
│                       ontology_dashboard, the_index, tesuji_map, doorbench
├── office/             shells+chrome: clear-ui, sovereign_shell, control, seat, aos, chan,
│                       cast, cast-voice, wave, table, wearable (+app/board/windows/seat/
│                       shell/clear-boot js, cli/clear/shell css)
├── rooms/              walkable corpus: room_lightmap, salon_lightmap, dungeon,
│                       incident_dungeon, worldline_dungeon, conservation_room, fable_room,
│                       hardware_primer, airflow_home, universe_within, mesh_gallery
├── games/              game, shadow_walk, maze_arena, arrakis, wipeout_* (3), tavern_brawl
│                       (+tavern_test), shadowbonk, pong, eraser_maze, light_maze,
│                       spectral_maze, grab_write, smith_chart
├── fields/             shadow-field experiments: arena_operator_field, bad_apple_field,
│                       calabi_yau, chaos_refract, erosion_field, field_quills,
│                       phase_particles, steer_field, rib_toy, pipeline (+shaders/)
├── verkle/             chain surfaces: chain_check, chain_witness, verkle_knot_wave,
│                       verkle_pyramid, verkle_construction, viz_3d_verkle
├── maps/               corpus graphs + viz: memory_map, module_map, rtfm_graph,
│                       fleet_symbols, viz_gallery, viz_horse_run, viz_spore_fish,
│                       self_hologram, the_rings, labs_map
├── decks/              (exists) decks.html, decks/, scout_deck, phonesalon
├── books/              night/, doctrine/, salons/, lanes/ (md), HUMAN_BRIEF,
│                       grounding_wave.md, DAY_WORK_DIGEST
├── checkers/           chain_check, claim_check, lattice_check, falsifiers,
│                       keeper_voice (harness)   [or fold into console/]
├── archive/            museum.html + museum/, attic/, ALL *.bak-* (~45 files),
│                       room_game lineage, verkle_birth baks
├── data/               every *.json/*.jsonl feed + index_data/ + lattices/ + trails/
│                       + generated *_data.js  (ESTATE_INDEX + ractor_board STREAMED,
│                       runaway-evidence evicted from web root entirely)
├── media/              art/, sound/, suno/, media/, tiles/, loose pngs/glbs
└── lib/                nav.js, style.css, manifest.webmanifest
```
Bound notes for the rebuild lanes: several pages are BUILD PRODUCTS (_build_*.py generate shadow_walk, scout_deck, cli_desk, rtfm, keeper_voice) — keep generators beside their outputs or the rebuild regresses them; the 8 orphan data files need a runtime-API check before any deletion decision (tri-state: Unproven orphans, not garbage).
