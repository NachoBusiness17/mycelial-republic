# f-19: dashboard/ census - every file, every surface, every orphan

2026-09-28, Mag Resource Harness @ HEAD 69a3c8614 (branch mag/run-beta1-factory-build-audi-20260806T231709Z), working-tree reads (16 files dirty under dashboard/ per git status; file lists byte-checked against HEAD: tracked html 171 == disk html 171, zero untracked, zero missing).

## Method (commands actually run)

- `find dashboard -type f` full walk; per-extension histogram; per-dir html counts.
- Read in full: `dashboard/server.py` (1,144 lines), `dashboard/rest.py` route tables (ROUTES + LEGACY, lines 5330-5544), `dashboard/lan_start.cmd`, heads of `mud_relay.py` / `lan_proxy.py`, `nav.js` (119 lines), `index.html` (287 lines), `home.html` (head), `decks.html` (deck wiring), `museum`/`games`/`night` index pages, all 4 redirect stubs, `dashboard_plugin.py` view_contract block.
- `watch/inbox/burn_reset_20260927/flash50/_f19_census_scan.py` (venv python): walked dashboard/ (591 files) + a repo reference corpus of 66,667 files (repo minus the archival trees named in "Scope caveats"), extracted every html/js/css `<title>`, outbound edges (script src / link href / a href / img src / fetch / location), and one substring pass for all 195 basenames. 2,299 corpus files matched at least one name.
- `_f19_recheck.py`: re-verified every v1 hit with boundary-corrected regexes `(?<![\w.-])NAME(?![\w.-])` (fixes: "board.js" matched inside "ractor_board.jsonl", "index.html" matched inside "index.html.bak-nav", "feed.html" inside "whale_feed.html", route string "/game.html" crediting game.html for a wave.html route). The 6 same-named `index.html` files are keyed on their `<dir>/index.html` path instead.
- Classification tiers: SERVER (named route target in server.py), INDEX (dir index.html served by safe_file's is_dir branch), PAGE (referenced by a live dashboard/static file: no .bak, not museum/, no noise paths), CODE (referenced only from python/tools/docs/state/queue), ORPHAN (zero live references of any kind).
- Second pass `git grep -l -F <name> -- .` over ALL tracked files for each orphan and code-only candidate (covers memory/biography, corpus/library, catalog, attic tars - trees the corpus walk excluded).
- Manual load checks: `grep -rn "oracle_dice" dashboard/ --include=*.html --include=*.js`, `grep src="app.js"` / windows.js / visual.js / board.js over live html, `grep -o "decks/[a-z0-9]*\.html" decks.html`, `grep -n "decks" decks.html`, `grep -n tapestry app.js`.

## Inventory

- Files under dashboard/: 597 total; 593 excluding __pycache__ (4 pyc); 461 also excluding the 132 static/.mimosa hook artifacts; 589 in the scanner walk (593 minus the 4 .vercel files; root .mimosa lives outside dashboard/).
- Total bytes: 4,356,720,726 (4.36 GB), of which dashboard/data/ holds 4.25 GB in 3 files: ESTATE_INDEX.jsonl 1,291,745,128 B; ractor_board.jsonl 713,252,012 B; ractor_board.jsonl.runaway-evidence-20260903 2,241,937,839 B.
- HTML/JS/CSS subject set: 195 files = 171 html + 20 js + 4 css, 6,431,375 B total. All 171 html are git-tracked; the tracked and on-disk lists are identical.
- Backup corpus inside the web root: 59 files named *.bak* or *.retired (13 nav.js variants; single .bak-nav pages for agents/aos/arrakis/aos/cast/cast-voice/chan/control/feed/fleet/health/index.clear-ui/index/lattice/museum/seat/sovereign_shell/table/tavern_brawl/tesuji_map/wave/wearable/viz_lattice_test plus .bak-surface seconds for control/ractor/index; 5 maze_arena baks; 3 shadow_walk baks; 3 salon_lightmap baks; 2 room_game copies; 2 rest.py baks at dashboard/ root; 2 verkle_birth.json pre_* baks; verkle_pyramid_seed.json.bak; overseer.json.bak; skifree.html.bak; room_game.html.retired). Plus dashboard/static/_frag_extract.tmp and lan_proxy.log/.pid.
- Generator scripts live in the web root and are themselves served by /static/*: _build_cli_desk.py, _build_estate_walk.py, _build_keeper_voice.py, _build_scout_deck.py, _build_shadow_walk.py, _restore_cli_desk.py, _rtfm_graph_build.py, _rtfm_graph_data.py, _rtfm_graph_verify.py.
- Deploy twin: dashboard/vercel.json points all routes at server.py (@vercel/python); .vercel/project.json = project "dashboard" (prj_L3O70daOMroyaKTaJRWdx9cr5A4F); a full deploy twin lives at repo root dashboard-deploy/ (567 static files) and is excluded from live-reference counting (it is a copy, not a consumer). mag/hermes_warm_boot.py:71 cites the deployed game URL https://vercel-deploy-7jx41m3r3-mag-d961.vercel.app/public/soul_frontier.html.

## Server layer (who serves what)

- Entrypoints: `main.py:2345` (dashboard command) and `main.py:5404` (UI/tls variant) both call `dashboard.server.run`; `dashboard/lan_proxy.py` + `lan_start.cmd` forward 192.168.86.35:8765 -> 127.0.0.1:8765 and :8001 (MCP).
- Explicit HTML routes in server.py do_GET (server.py:580-643), 9 distinct targets from 21 paths:
  - `/`, `/index.html` -> static/index.html (server.py:592)
  - `/chan`, `/chan.html`, `/keep`, `/keep.html`, `/b`, `/b.html` -> static/chan.html (server.py:580)
  - `/wave`, `/wave.html`, `/desk`, `/desk.html` -> static/wave.html (server.py:586)
  - `/table`, `/table.html`, `/play`, `/play.html`, `/game`, `/game.html` -> static/wave.html (server.py:604; comment: "Text adventure. /table is /wave - not the ASCII board" - so game.html and table.html are NOT routed despite their names)
  - `/voice`, `/voice.html`, `/cast-voice.html` -> static/cast-voice.html (server.py:611)
  - `/shell`, `/shell.html` -> static/sovereign_shell.html (server.py:597)
  - `/seat`, `/seat.html` -> static/seat.html (server.py:618)
  - `/fleet`, `/fleet.html` -> static/fleet.html (server.py:625)
  - `/health`, `/health.html`, `/loop-health` -> static/health.html (server.py:632)
  - `/aos`, `/aos.html` -> static/aos.html (server.py:639)
- Generic static door: `/static/*` -> safe_file() serves ANY file under dashboard/static/ (server.py:645-655, 437-463): traversal-guarded only; serves .py generators, .bak pages, .md, .json, media. Directory URLs resolve to the dir's index.html (server.py:457-458) - that routes /static/, /static/art/, /static/games/, /static/night/, /static/frontdoor/, /static/salons/astra/ to their index pages (museum/ has none and 404s on the bare dir).
- Data door: `/data/` serves exactly two allow-listed files, ractor_board.jsonl + ESTATE_INDEX.jsonl (server.py:540-557).
- rest.py dispatch (ROUTES+LEGACY) serves JSON only; exactly one payload names a static page: `"page": "/static/lattice.html"` (rest.py:4295, the conspiracy-lattice door). rest.py has NO `/api/v1/surfaces/liveness` route - the liveness organ index.html polls (index.html:95, 123-125) 404s and the page falls back to its embedded LIVENESS_MAP.
- LAW-060 fleetbar injected into every served html server-side unless `?embed=1` (server.py:27-47, 653-654); nav.js is the fleetnav bar, single source of nav links (nav.js:1, restored 2026-09-28 per FW-45 note at nav.js:2-8).
- mud_relay.py: standalone LAN process on :8766 (presence relay + /mud/ws push), imported by nothing; consumed by static/games/mud.html:456-457 (RELAY const, /mud/seen, /mud/others, /mud/ws) and probed by deck.html:715 (`:8766/mud/state`).

## Classification of the 195 html/js/css files

Tally: SERVER 9 (136,134 B) | INDEX 5 (11,567 B) | PAGE 172 (6,208,171 B) | CODE 4 (54,721 B) | ORPHAN 5 (20,782 B). Per-dir html counts: static root 112, decks/ 8, doctrine/ 5, games/ 10 (+soul_frontier/ 1), museum/ 6, night/ 22, vislab/ 4, art/ 1, frontdoor/ 1, salons/astra/ 1.

Per-file table (class | title | wired by, first referrers):

| static/agents.html | 16345 | PAGE | Agents - sub-agent fleet | app.js, estate_walk.html, AGENT_PLATFORM_REPOS_INDEX.md, CONVO.md |
| static/airflow_home.html | 18986 | PAGE | AIRFLOW HOME - the house is the prompt | nav.js, catalog.html, gaming_corpus_briefs.jsonl |
| static/aos.html | 7542 | SERVER | AOS · Bones - Live | server.py route, index.html, nav.js, build_vislab_catalog.py, gaming_corpus_briefs.jsonl |
| static/app.js | 351247 | PAGE | (no title) | _build_cli_desk.py, _restore_cli_desk.py, AGENT_UI_STEAL.md, DASHBOARD_PLUGIN_SURFACE.md |
| static/arena_operator_field.html | 498 | PAGE | moved | deck.html, gamebuild.html, CONVO.md, CONVO.md.bak-gpl |
| static/arrakis.html | 459 | PAGE | moved | deck.html, index.html, arena_bench.py, CONVO.md |
| static/art/index.html | 1748 | INDEX | Quest Art - the Forge's wall | health.json |
| static/bad_apple_field.html | 281186 | PAGE | BAD APPLE FIELD - the room that remembers plays the video · B5 | nav.js, read_receipts.json, build_vislab_catalog.py, gaming_corpus_briefs.jsonl |
| static/board.js | 13843 | PAGE | (no title) | _restore_cli_desk.py, app.js, room_state.py, room_state.py.bak-lightmapv2-20260906 |
| static/burn_board.html | 7428 | PAGE | Burn Board | index.html, nav.js, burn_steer.py, CONVO.md |
| static/calabi_yau.html | 5868 | PAGE | CALABI-YAU QUINTIC - shadow-fields | index.html, nav.js, build_vislab_catalog.py |
| static/cast-voice.html | 48625 | SERVER | Mag Voice | server.py route, estate_walk.html, index.html, voice-vad-end-of-turn-2026-08-07.md, cast_server.py |
| static/cast.html | 2184 | PAGE | Mag Cast | nav.js, operator_board.html, cast_server.py, gaming_corpus_briefs.jsonl |
| static/chain_check.html | 30811 | PAGE | MAG · Chain Check - verkle knot link verifier v1 | _rtfm_graph_data.py, falsifiers.html, RTFM_20260904.md, gaming_corpus_briefs.jsonl |
| static/chain_witness.html | 9657 | PAGE | THRESHOLD - the cold-start witness door | index.html, verkle_construction.html, witness_snapshot.py, CONVO.md |
| static/chan.html | 12719 | SERVER | /keep/ - Anonymous Science | server.py route, index.html, read_receipts.json, gaming_corpus_briefs.jsonl, test_chan.py |
| static/chaos_refract.html | 3126 | PAGE | REFRACT - emergent, unexplained | index.html, catalog.html |
| static/claim_check.html | 14106 | PAGE | MAG · Claim Check - launch-law card verifier v1 | _rtfm_graph_data.py, falsifiers.html, OPERATOR_GATES_SCHEMA.md, RTFM_20260904.md |
| static/clear-boot.js | 3542 | ORPHAN | (no title) |  |
| static/clear.css | 10319 | ORPHAN | (no title) |  |
| static/cli.css | 159715 | PAGE | (no title) | _build_cli_desk.py, _restore_cli_desk.py, cloud-09eadb5328.json, peer-56b8cc3c06.json |
| static/conservation_room.html | 24318 | PAGE | THE SOWING ROOM - a fable of the conservation clause | index.html, live_feed.json, CONVO.md, CONVO.md.bak-gpl |
| static/control.html | 3508 | PAGE | Direct Mag | home.html, nav.js, cast_server.py, CONVO.md |
| static/daytool.html | 8228 | PAGE | DAY TOOL | DAY_WORK_DIGEST.md, day_work_digest.txt, CONVO.md, CONVO.md.bak-gpl |
| static/decisions.html | 1088 | PAGE | DECISIONS | home.html, index.html, decision_hook.py, CONVO.md |
| static/deck.html | 38671 | PAGE | COMMAND DECK - local_sovereign_agent | index.html, catalog.html, build_deck.py, tide_dashboard.py |
| static/decks.html | 10724 | PAGE | DECKS - the pro surface | deck.html, cacheecon.html, MCLUHAN.md, MCLUHAN_rashomon_20260904.md |
| static/decks/cacheecon.html | 47721 | PAGE | DECK - Cache Econ | read_receipts.json, health.json, gaming_corpus_briefs.jsonl |
| static/decks/gamebuild.html | 198664 | PAGE | DECK - Game Build | health.json, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/decks/glmwatch.html | 93892 | PAGE | DECK - GLM Watch | health.json, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/decks/legions.html | 72578 | PAGE | DECK - Legions | health.json, gaming_corpus_briefs.jsonl |
| static/decks/mag.html | 568671 | PAGE | DECK - Mag | shadow_walk_content.json, health.json, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/decks/mesh3d.html | 64335 | PAGE | DECK - Mesh 3D | shadow_walk_content.json, health.json, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/decks/personal.html | 21092 | PAGE | DECK - Personal | read_receipts.json, health.json, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/decks/rocinante.html | 94685 | PAGE | DECK - Rocinante | health.json, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/doctrine/AUTONOMY_WHEEL.html | 4088 | PAGE | AUTONOMY_WHEEL_20260904.md - fleet doctrine | scout_deck.html, health.json, gaming_corpus_briefs.jsonl |
| static/doctrine/BURST_DOCTRINE.html | 5570 | PAGE | BURST_DOCTRINE_20260903.md - fleet doctrine | read_receipts.json, scout_deck.html, gaming_corpus_briefs.jsonl |
| static/doctrine/SWARM_SCALE_PLAN.html | 5251 | PAGE | SWARM_SCALE_PLAN_20260904.md - fleet doctrine | read_receipts.json, scout_deck.html, gaming_corpus_briefs.jsonl |
| static/doctrine/TRI_PARTY.html | 6365 | PAGE | TRI_PARTY_ARCHITECTURE_20260904.md - fleet doctrine | read_receipts.json, scout_deck.html, gaming_corpus_briefs.jsonl |
| static/doctrine/X_SCOUT_DOCTRINE.html | 4861 | PAGE | X_SCOUT_DOCTRINE_20260904.md - fleet doctrine | scout_deck.html, health.json, gaming_corpus_briefs.jsonl |
| static/doorbench.html | 23011 | PAGE | DOORBENCH - cache-invalidation falsifier | live_feed.json, nav.js, CONVO.md, gaming_corpus_briefs.jsonl |
| static/drift_board.html | 4067 | CODE | Teleo Drift Board | DRIFT_BOARD_SPEC.md, drift_dashboard.py |
| static/dungeon.html | 8439 | PAGE | THE DUNGEON - invariants as lighting | gamebuild.html, mag.html, arena_bench.py |
| static/emergence_test_visualization.html | 7391 | PAGE | Neural Emergence Test - Fixed Wiring vs Trainable Heads | index.html, catalog.html, gaming_corpus_briefs.jsonl |
| static/eraser_maze.html | 25407 | PAGE | ERASER MAZE - seeing collapses the light (PURPLE HARVEST B2) | index.html, nav.js |
| static/erosion_field.html | 17260 | PAGE | EROSION FIELD - B1 v1 | gamebuild.html, mag.html, gaming_corpus_briefs.jsonl |
| static/estate_walk.html | 599197 | PAGE | ESTATE WALK | _build_estate_walk.py, deck.html, build_deck.py, gaming_corpus_briefs.jsonl |
| static/fable_room.html | 10836 | PAGE | THE FABLE ROOM - room #0 · the union of story and record | index.html, nav.js, worldline_dungeon.py, CONVO.md |
| static/falsifiers.html | 4862 | PAGE | MAG · Falsifiers - paste-checkable invariants index v1 | _rtfm_graph_data.py, chain_check.html, RTFM_20260904.md, gaming_corpus_briefs.jsonl |
| static/feed.html | 4681 | PAGE | Mycelial Republic · Feed | nav.js, operator_board.html, cast_server.py, gaming_corpus_briefs.jsonl |
| static/feed_badge.js | 3621 | PAGE | (no title) | chain_witness.html, decisions.html |
| static/field_quills.html | 7231 | PAGE | QUILL FIELD - instanced EM quills over the B1 operator field | nav.js, operator_board.html, gaming_corpus_briefs.jsonl |
| static/fleet.html | 9569 | SERVER | HYPERVISOR · fleet cool/heat + real bills | server.py route, home.html, index.html |
| static/fleet_symbols.html | 16820 | PAGE | FLEET SYMBOLS - the operator algebra | nav.js, operator_board.html, LIGHT_OPERATOR_FOUNDATION_20260904.md, room_state.py |
| static/frontdoor/index.html | 3308 | INDEX | the republic - front door |  |
| static/game.html | 29768 | PAGE | The Necromancer's Swarm - a game of k3s, dragons, and invariants | index.html, nav.js, saelis_room.py, salon_50.py |
| static/game_verkle_knots.js | 67478 | PAGE | (no title) | game.html, verkle_knot_wave.html, _gen_game_verkle.py |
| static/games/arena_operator_field.html | 13823 | PAGE | OPERATOR FIELD · B1a - lights are vector operators, the marble has momentum | arena_operator_field.html, deck.html, CONVO.md, CONVO.md.bak-gpl |
| static/games/arrakis.html | 17501 | PAGE | ARRAKIS v2 - RIDE THE MAKER | arrakis.html, deck.html, arena_bench.py, CONVO.md |
| static/games/frontier_souls.html | 95076 | PAGE | FRONTIER SOULS | deck.html, index.html, build_deck.py, probe_snake.js |
| static/games/index.html | 860 | INDEX | Games |  |
| static/games/maze_arena.html | 51645 | PAGE | GRAY SWAN ARENA · MAG WING - lightmap GPS vs dumb models | deck.html, gamebuild.html, shadertoy_rule_lattice.md, maze_real.py |
| static/games/mud.html | 125486 | PAGE | MUD | deck.html, index.html, mud_to_wow_full_ask.json, CONVO.md |
| static/games/oracle_dice.js | 2633 | ORPHAN | (no title) |  |
| static/games/ruins_go.html | 12998 | PAGE | RUINS GO | index.html, oracle_dice.js, build_knowledge_graph.py, gaming_corpus_briefs.jsonl |
| static/games/ruins_go_engine.js | 17196 | PAGE | (no title) | ruins_go.html |
| static/games/skifree.html | 16200 | PAGE | SKIFREE | index.html, gaming_corpus_briefs.jsonl |
| static/games/soul_frontier/soul_frontier.html | 44212 | CODE | Soul Frontier - Death Must Die × Dark Souls | hermes_warm_boot.py, gaming_corpus_briefs.jsonl |
| static/games/swarm.html | 79502 | PAGE | PRIVLIDGE - a disco science skate | deck.html, index.html, CONVO.md, todo.md |
| static/games/toy.html | 14229 | PAGE | THE TOY - the i-frame roll | deck.html, index.html, game_ramp.py, build_deck.py |
| static/grab_write.html | 4728 | PAGE | The Tesuji - Grab &amp; Write | index.html, nav.js, gaming_corpus_briefs.jsonl |
| static/hardware_primer.html | 9545 | PAGE | THE HARDWARE PRIMER - Room 1: The Darlington Pair | nav.js, catalog.html, gaming_corpus_briefs.jsonl |
| static/health.html | 10278 | SERVER | LOOP HEALTH · real-time what works / what doesn't | server.py route, home.html, index.html |
| static/home.html | 17261 | PAGE | Home &mdash; the six destinations | grounding_wave.md, nav.js, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/hum.html | 10503 | PAGE | THE HUM - organ board | index.html, catalog.html, gaming_corpus_briefs.jsonl, record_briefs.jsonl |
| static/incident_dungeon.html | 25142 | PAGE | INCIDENT DUNGEON - the maze-arena incident, walkable | nav.js, catalog.html, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/index.html | 16693 | SERVER | FLEET CONSOLE - everything, one place | server.py route, _build_cli_desk.py, _restore_cli_desk.py, canon_world_games_cache_farming_2.txt, art_forge.py |
| static/intel.html | 3371 | PAGE | Tonight in your fleet | nav.js, read_receipts.json, fleet_intel.py, render_brief.py |
| static/keeper_voice.html | 10515 | PAGE | THE KEEPER'S VOICE | home.html, keeper_voice_harness.js, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/keeper_voice_harness.js | 2042 | ORPHAN | (no title) |  |
| static/kv_os.html | 5487 | PAGE | KV OS - kernel status | hum.html, index.html, gaming_corpus_briefs.jsonl |
| static/labs_map.html | 958 | PAGE | COMPETITOR MAP | nav.js, read_receipts.json, gaming_corpus_briefs.jsonl |
| static/lanes.html | 3298 | PAGE | LANES - manager board | daytool.html, home.html, lite_guard.py, CONVO.md |
| static/lattice.html | 5183 | PAGE | MAG · Conspiracy lattice | nav.js, operator_board.html, DOCTRINE_MAP.md, gaming_corpus_briefs.jsonl |
| static/lattice_check.html | 8700 | PAGE | MAG · Lattice Check - Legendre three-square invariant v1 | _rtfm_graph_data.py, falsifiers.html, RTFM_20260904.md, gaming_corpus_briefs.jsonl |
| static/lattice_data.js | 6617 | PAGE | (no title) | viz_lattice_test.html, CONVO.md, lattice_render.py |
| static/light_maze.html | 9551 | PAGE | LIGHT MAZE - what you see is what you know | nav.js, catalog.html, gaming_corpus_briefs.jsonl |
| static/links.html | 6380 | PAGE | MAG · Links Library | nav.js, todo.md |
| static/live.html | 3752 | PAGE | Fleet Live - every window, verbose | grounding_wave.md, home.html, room_state.py, room_state.py.bak-lightmapv2-20260906 |
| static/live_feed.html | 4082 | PAGE | THE FL33T - Live Feed | home.html, index.html, gaming_corpus_briefs.jsonl |
| static/maze.html | 10144 | PAGE | THE MAZE ENTRANCE | grounding_wave.md, index.html, gaming_corpus_briefs.jsonl |
| static/maze_arena.html | 468 | PAGE | moved | deck.html, gamebuild.html, shadertoy_rule_lattice.md, maze_real.py |
| static/memory_graph_data.js | 319191 | PAGE | (no title) | memory_map.html, _gen_memory_map.py |
| static/memory_map.html | 5889 | PAGE | The Memory Map - categorized relational graph of the Republic | index.html, nav.js, hero_simulation.json, hero_simulation.json.bak-rehome-20260907 |
| static/mesh_gallery.html | 67937 | PAGE | MAG · Mesh Gallery - dungeon content pipeline v1 | mag.html, mesh3d.html, MESH_PIPELINE_20260903.md, fleet_intel.py |
| static/model_map.html | 6633 | PAGE | Model Disk Map - the fleet's brain shelf | index.html, catalog.html, gaming_corpus_briefs.jsonl |
| static/module_map.html | 6477 | PAGE | The Module Map - every mag module surfaced with its real purpose | index.html, nav.js |
| static/module_map_data.js | 196252 | PAGE | (no title) | module_map.html, salon_50.py, _gen_module_map.py |
| static/mud.html | 447 | PAGE | moved | deck.html, index.html, mud_to_wow_full_ask.json, CONVO.md |
| static/museum.html | 2264 | PAGE | MAG · The Museum | nav.js, chord_v4.html, JUNG.md, FREUD_desire_20260905.md |
| static/museum/_rtfm_graph_shell.html | 11497 | PAGE | MAG · RTFM Graph - the fleet's manuals, browsable | _rtfm_graph_build.py, nav.js, gaming_corpus_briefs.jsonl |
| static/museum/estate_walk.lod.html | 683614 | PAGE | ESTATE INDEX - zone LOD | _build_estate_walk.py, deck.html, build_deck.py, gaming_corpus_briefs.jsonl |
| static/museum/index.clear-ui.html | 18989 | PAGE | Mag - Local office | _restore_cli_desk.py, nav.js, gaming_corpus_briefs.jsonl |
| static/museum/index_old_mag_board.html | 101830 | PAGE | MAG · マグ · 勾玉 | read_receipts.json, health.json, gaming_corpus_briefs.jsonl, test_desk_baseline_probe.py |
| static/museum/scan_me.html | 488 | CODE | Scan me | gaming_corpus_briefs.jsonl |
| static/museum/viz_horse_lane2_carcass.html | 3956 | PAGE | Spore Form - the horse (attempt 2) | catalog.html, catalog.json, gaming_corpus_briefs.jsonl |
| static/nav.js | 5900 | PAGE | (no title) | agents.html, aos.html, decision_hook.py, fleet_intel.py |
| static/night/chord_v4.html | 4309 | PAGE | MAG CHORD v4 - adopted as ExperienceCandidate | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/design_theory.html | 4398 | PAGE | Design Theory - one organism, many senses | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/game_codex.html | 4530 | PAGE | The Game Codex - dragons are assumptions | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/game_lattice.html | 4697 | PAGE | The Game Mechanics Lattice - 7 engines x 47 rooms | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/hermes_dossier_v1.html | 7394 | PAGE | Hermes Dossier V1 - the fold of the wings | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/hermes_steal_v0.html | 5999 | PAGE | The Hermes Steal - dossier v0 | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/index.html | 3060 | INDEX | THE NIGHT BOOK - 09-02/03 | health.json |
| static/night/light_codec.html | 3104 | PAGE | The Light Codec - content-borne steering | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/light_loop.html | 3325 | PAGE | Light-in-the-Loop - dungeons as DFA | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/maze_enhancement.html | 4155 | PAGE | The Enhancement Map - corpus to game systems | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/maze_synthesis.html | 5835 | PAGE | The Prompt Maze Synthesis - the inversion | index.html, health.json, salon_50.py, gaming_corpus_briefs.jsonl |
| static/night/morning_state.html | 4687 | PAGE | Morning State - the whole night in one file | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/orphan_register.html | 5213 | PAGE | The Orphan Register - v4 first live run | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/primer_wired.html | 4215 | PAGE | Salon: Primer Wired - the tale-re-encoder | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/sherpa_spec.html | 3700 | PAGE | The Sherpa Spec - councils, footholds, Mickeys | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/stockfish.html | 3350 | PAGE | The Stockfish Doctrine - evaluation vs decision | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/surface_atlas.html | 4877 | PAGE | The Surface Atlas - 20 surfaces mapped | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/systems_gap_map.html | 6934 | PAGE | SYSTEMS ↔ SALON GAP MAP - the thesis v3 | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/the_session_self_steal.html | 5898 | PAGE | The Session Self-Steal - 12 laws with scars | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/time_machinery.html | 3870 | PAGE | The Time Machinery Map - 30 organs | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/titor_stack.html | 4845 | PAGE | The Titor Stack - verkle in old rib tech | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/night/trade_sheet.html | 7378 | PAGE | The Trade Sheet - every tangent traded | index.html, health.json, gaming_corpus_briefs.jsonl |
| static/ontology_dashboard.html | 3430 | PAGE | Ontology Compiler Dashboard - Phase 1 | index.html, catalog.html, ONTOLOGY_COMPILER_PHASE1.md, gaming_corpus_briefs.jsonl |
| static/operator_board.html | 15376 | PAGE | THE OPERATOR'S BOARD | nav.js, read_receipts.json, violation_baseline.json, gaming_corpus_briefs.jsonl |
| static/persistent_world.html | 8373 | PAGE | THE PERSISTENT WORLD - glyph edition v0 · an interface to the hive | index.html, catalog.html, CONVO.md, gaming_corpus_briefs.jsonl |
| static/phase_particles.html | 12684 | PAGE | PHASE PARTICLES - liquid → gas → plasma (room R1) | nav.js, catalog.html, gaming_corpus_briefs.jsonl |
| static/phonesalon.html | 4096 | PAGE | PHONESALON - the android free-lane deck | nav.js, operator_board.html, CONVO.md, CONVO.md.bak-gpl |
| static/pipeline.html | 13144 | PAGE | PIPELINE - the shader cartridges | deck.html, index.html, CONVO.md, build_deck.py |
| static/pong.html | 3209 | PAGE | PONG - the classics ladder, rung 1 | index.html, catalog.html |
| static/ractor.html | 4649 | PAGE | MAG · The Ractor Board | index.html, nav.js, CONVO.md, CONVO.md.bak-gpl |
| static/reply_console.html | 20104 | PAGE | REPLY OVERDRIVE - 36 doors (fl33t) | catalog.html, catalog.json, gaming_corpus_briefs.jsonl |
| static/rib_toy.html | 9923 | PAGE | THE RIB TOY - a shadertoy for steering packets | nav.js, read_receipts.json, gaming_corpus_briefs.jsonl |
| static/room_lightmap.html | 4766 | PAGE | MAG · The Room - 2026-09-02 rendered as a dungeon | gamebuild.html, mag.html, ONTOLOGY_COMPILER_PHASE1.md, shadertoy_rule_lattice.md |
| static/rtfm_graph.html | 46308 | PAGE | MAG · RTFM Graph - the fleet's manuals, browsable | _rtfm_graph_build.py, _rtfm_graph_verify.py, gaming_corpus_briefs.jsonl |
| static/salon_lightmap.html | 28370 | PAGE | Salon Lightmap v2 - the room that remembers | index.html, live_feed.json, _astra_triangulation.md |
| static/salons/astra/index.html | 2591 | INDEX | ASTRA SALON - research steal, live | health.json |
| static/scout_deck.html | 13264 | PAGE | MAG // SCOUT DECK | _build_scout_deck.py, nav.js, gaming_corpus_briefs.jsonl |
| static/seat.html | 5023 | SERVER | SEAT · ghost surface | server.py route, index.html, nav.js, gaming_corpus_briefs.jsonl |
| static/seat.js | 11821 | PAGE | (no title) | seat.html |
| static/self_hologram.html | 5147 | PAGE | SELF HOLOGRAM - the seat's self-model trajectory | index.html, nav.js, self_hologram.py, CONVO.md |
| static/shadow_walk.html | 112293 | PAGE | SHADOW WALK - voxel roguelite · vision-gated · JIT · v2 THE RUN | _build_shadow_walk.py, grounding_wave.md, swarm_quests.py, volume_fidelity.py |
| static/shadowbonk.html | 13502 | PAGE | SHADOWBONK - tony mczoom vs the shadow volume | index.html, catalog.html, CONVO.md |
| static/shell.css | 2334 | PAGE | (no title) | sovereign_shell.html, SOVEREIGN_STACK.md |
| static/shell.js | 3676 | PAGE | (no title) | sovereign_shell.html, SOVEREIGN_STACK.md, cloud-925cb9b3ae.json |
| static/smith_chart.html | 14759 | PAGE | SMITH CHART - the fold law | gamebuild.html, nav.js, gaming_corpus_briefs.jsonl |
| static/sovereign_shell.html | 2073 | SERVER | Mag Sovereign Shell | server.py route, index.html, nav.js, SOVEREIGN_STACK.md, gaming_corpus_briefs.jsonl |
| static/spectral_maze.html | 42708 | PAGE | SPECTRAL MAZE - three bands, one flood (PURPLE HARVEST B7) | home.html, nav.js, gaming_corpus_briefs.jsonl, hero_simulation.json |
| static/spend.html | 12255 | PAGE | SPEND - one wall | nav.js, operator_board.html, gaming_corpus_briefs.jsonl |
| static/steal_tools.html | 4513 | PAGE | The Armory - 116 steal tools | index.html, nav.js, gaming_corpus_briefs.jsonl |
| static/steal_tools_data.js | 56897 | PAGE | (no title) | steal_tools.html, salon_50.py |
| static/steer_field.html | 7012 | PAGE | STEER FIELD - the film | nav.js, systems_gap_map.html, shadertoy_rule_lattice.md, gaming_corpus_briefs.jsonl |
| static/style.css | 37776 | PAGE | (no title) | _build_cli_desk.py, _restore_cli_desk.py, git_tree.json, _fix_appjs_load.py |
| static/swarm.html | 80408 | PAGE | PRIVLIDGE - a disco science skate | deck.html, index.html, CONVO.md, todo.md |
| static/table.html | 26172 | PAGE | Mag Table - the lantern | estate_walk.html, index.html, TABLE_DOGFOOD.md, 20260816-022647-harness.json |
| static/tapestry.js | 29053 | PAGE | (no title) | app.js, estate_walk.html, TAPESTRY_VERKLE_VISUAL.md, tapestry_visual.py |
| static/tavern_brawl.html | 20049 | PAGE | THE KABUKI TAVERN - brawl of the ractors | grounding_wave.md, index.html, CONVO.md, record_briefs.jsonl |
| static/tavern_test.html | 3027 | PAGE | tavern cartridge test | index.html, catalog.html, CONVO.md, gaming_corpus_briefs.jsonl |
| static/tesuji_map.html | 15677 | PAGE | TESUJI FIELD MAP · GLM-5.3-flash behavior surface | grounding_wave.md, home.html, INDEX.md, worldline_dungeon.py |
| static/the_fence.html | 4953 | PAGE | The Fence | index.html, catalog.html, gaming_corpus_briefs.jsonl |
| static/the_index.html | 6841 | PAGE | THE INDEX - estate map (open-rib spine v0) | index.html, verkle_construction.html, CONVO.md, gaming_corpus_briefs.jsonl |
| static/the_radar.html | 8842 | PAGE | FLEET RADAR - the watch, visualized | index.html, catalog.html, CONVO.md |
| static/the_rings.html | 4750 | PAGE | THE RINGS - one per day (2026-08-25 →) | index.html, catalog.html, CONVO.md |
| static/tide.html | 6727 | PAGE | TIDE - nightly compaction | deck.html, build_deck.py, tide_dashboard.py |
| static/universe_within.html | 8576 | PAGE | THE UNIVERSE WITHIN - the network, with music, in a dark room | index.html, catalog.html, CONVO.md |
| static/verkle_construction.html | 15727 | PAGE | THE BIRTH CANVAS - the verkle through its construction | index.html, catalog.html, CONVO.md |
| static/verkle_knot_wave.html | 7032 | PAGE | The Verkle Knot - standing wave | index.html, nav.js |
| static/verkle_pyramid.html | 8414 | PAGE | VERKLE PYRAMID - the chain as a place (zone two) | index.html, verkle_construction.html, CONVO.md |
| static/vislab/belt_trick.html | 40557 | PAGE | THE BELT TRICK DOMAIN LATTICE - 720° true close · Lipschitz-bounded march | catalog.html, catalog.json, build_vislab_catalog.py, gaming_corpus_briefs.jsonl |
| static/vislab/catalog.html | 96030 | PAGE | VISLAB CATALOG - everything built, one surface | deck.html, health.json, build_deck.py, build_vislab_catalog.py |
| static/vislab/isfahan_lattice.html | 5954 | CODE | ISFAHAN LATTICE - light through the law (12 seeds) | gaming_corpus_briefs.jsonl |
| static/vislab/play.html | 9246 | PAGE | GAME PLAYER - every module dungeon, one interface | deck.html, catalog.html, build_deck.py, build_vislab_catalog.py |
| static/visual.js | 29384 | PAGE | (no title) | _restore_cli_desk.py, surface_atlas.html, DASHBOARD_ICONS_WINDOW_DEEP_DIVE_20260811.md, _fix_appjs_load.py |
| static/viz_3d_verkle.html | 8568 | PAGE | Verkle Chain - 3D | index.html, nav.js |
| static/viz_gallery.html | 4379 | PAGE | Viz Lab - the Republic's visualizations | index.html, nav.js, INDEX.md, CONVO.md |
| static/viz_horse_run.html | 9376 | PAGE | Spore Form - the horse (reinterpreted) | index.html, catalog.html, INDEX.md, fire_horse.py |
| static/viz_lattice_test.html | 17026 | PAGE | Viz Lab - the constitution as a lattice | index.html, lattice_data.js, lattice_render.py, gaming_corpus_briefs.jsonl |
| static/viz_spore_fish.html | 1572 | PAGE | Spore Form - the fish (attempt 1) | index.html, nav.js, fire_horse.py, gaming_corpus_briefs.jsonl |
| static/wave.html | 23612 | SERVER | Mag - standing wave | server.py route, index.html, nav.js, 20260816-022647-harness.json, gaming_corpus_briefs.jsonl |
| static/wave_gpu.js | 2246 | ORPHAN | (no title) |  |
| static/wave_scene.js | 3340 | PAGE | (no title) | wave.html, 20260816-022647-harness.json |
| static/wearable.html | 6334 | PAGE | Swarm HUD - Wearable | nav.js, operator_board.html, cast_server.py, novelty_lens.py |
| static/whale_console.html | 20535 | PAGE | WHALE CONSOLE - almanac · doors · council (fl33t) | catalog.html, catalog.json, gaming_corpus_briefs.jsonl |
| static/whale_feed.html | 4080 | PAGE | WHALE PATROL - live feed (fl33t) | catalog.html, catalog.json, gaming_corpus_briefs.jsonl |
| static/windows.js | 6451 | PAGE | (no title) | _build_cli_desk.py, _restore_cli_desk.py, DASHBOARD_ICONS_WINDOW_DEEP_DIVE_20260811.md, _fix_appjs_load.py |
| static/wipeout_lightmaze.html | 11862 | PAGE | WIPEOUT // LIGHT MAZE - the song is the level | index.html, catalog.html, INDEX.md, CONVO.md |
| static/wipeout_sunset.html | 15360 | PAGE | WIPEOUT v3 - synthwave sunset · the music moves the mountains | index.html, catalog.html, INDEX.md, CONVO.md |
| static/wipeout_v2.html | 12034 | PAGE | WIPEOUT v2 - raymarched · the song sets the speed | index.html, catalog.html, INDEX.md, CONVO.md |
| static/worldline_dungeon.html | 14699 | PAGE | THE WORLDLINE DUNGEON - a telling rendered from the board | index.html, catalog.html, worldline_dungeon.py, CONVO.md |

### Reading the table

- SERVER = named route target. INDEX = dir index.html (art, games, night, salons/astra wired from nav.js lines 62/15/32/65; frontdoor/index.html has NO referrer anywhere - served only if typed). PAGE = some live static file names it. CODE = only python/tools/docs/state name it. ORPHAN = nothing live names it at all.
- Dynamic wiring (invisible to static grep, verified by reading the code):
  - decks.html:97 builds `window.location.href='/static/decks/'+d.id+'.html'` at runtime from a snapshot JSON: all 8 decks/*.html are live-wired dynamically; static grep finds only snapshot mentions (read_receipts.json, vislab/health.json).
  - index.html:160-164 auto-tiles EVERY top-level dashboard/static/*.html via /api/workspace/tree - while the console lives, nothing at static top level is unreachable; orphanhood here means unreferenced, not unreachable.
  - app.js:4559 dynamically imports `/static/tapestry.js?v=days-v5`.
- Referrer-name caution: read_receipts.json, vislab/catalog.json, vislab/health.json, model_census.json etc. are data snapshots that mention most surfaces; auto-inventories (catalog/catalog.jsonl, catalog/tags.jsonl, dashboard/data/ESTATE_INDEX.jsonl, memory/trajectory/steps.jsonl, receipt_fts.sqlite) name EVERY dashboard file by construction (git grep for clear.css hits catalog.jsonl + ESTATE_INDEX.jsonl though nothing loads it). A name inside those is not wiring.

## The 5 orphans (zero live references, git-grep second pass over all tracked files)

1. `static/wave_gpu.js` (2,246 B) - TRUE ORPHAN. Zero mentions in any html/js/css in the repo outside itself. Its header says the ?gpu query flag should swap wave.html to a Three.js readout, but no page loads it (wave.html does not reference it). Survives only in memory/agent_sessions snapshots, memory/portable_bags/travel_kit manifest, auto-inventories, and attic/matthew_export tar archives.
2. `static/games/oracle_dice.js` (2,633 B) - ORPHAN with a false self-description. Header comment claims "Used by: mud.html, ruins_go.html, frontier_souls.html, any game that needs rolls" (oracle_dice.js:2-3). `grep -rn oracle_dice dashboard/ --include=*.html --include=*.js` matches ONLY the file itself: none of the three claimed games loads it. Documented intent (memory/continuity/seat_memory_20260927/oracle-dice-shared-module.md, watch/inbox/BUILD_ORDER_LIVING_MUD_20260922.md) never wired.
3. `static/clear.css` (10,319 B) + 4. `static/clear-boot.js` (3,542 B) - ORPHANED PAIR. Loaded only by static/museum/index.clear-ui.html, a page in the retired museum/ archive dir (the live twin index.clear-ui.html at static root is itself a .bak-nav). The Clear UI was the old desk; _restore_cli_desk.py can swap it back over index.html.
5. `static/keeper_voice_harness.js` (2,042 B) - ORPHAN as a web asset. No page loads it; it is a node-side verifier for keeper_voice.html (extracts page JS between //<<JS and //JS>>, syntax-checks, emits state/shadow_work/keeper_lines.json - keeper_voice_harness.js:1-5), run by hand per watch/inbox/KEEPER_VOICE_20260907.md. Not an orphan as a tool; orphan as static content (and it sits in the served web root).

## The 4 CODE-tier pages (wired, but no page links them)

1. `static/drift_board.html` (4,067 B) - written by tools/drift_dashboard.py:49 (OUT_HTML = dashboard/static/drift_board.html); owned by docs/DRIFT_BOARD_SPEC.md; read by tools/visor.py. Generator output, reachable only by URL.
2. `static/games/soul_frontier/soul_frontier.html` (44,212 B) - live game cited by mag/hermes_warm_boot.py:71 via its deployed Vercel URL; generated/checked by tools/build_adam_soul.py + build_adam_soul_full.py; not linked from games/index.html (which lists 9 other games).
3. `static/museum/scan_me.html` (488 B) - archive member (museum/ is retired per index.html liveness map); mentions only in state/fuel gaming briefs + training events.
4. `static/vislab/isfahan_lattice.html` (5,954 B) - sibling belt_trick.html and play.html are linked from vislab/catalog.html, isfahan is NOT (catalog is generated by scripts/build_vislab_catalog.py); documented in memory/continuity/seat_memory_20260927/isfahan-lattice-beyond-dots.md.

## The dormant CLI-desk bundle (PAGE-tier by refs, zero live loaders)

`app.js` (351,247 B) + `cli.css` (159,715 B) + `windows.js` + `visual.js` + `board.js` + `tapestry.js` are the old Mag CLI desk front-end. No live html loads any of them (`grep src="app.js"|"windows.js"|"visual.js"` over live html: zero hits; board.js appears in app.js only as a fallback comment at app.js:7987). They reference each other (app.js imports tapestry.js), the night book's surface_atlas.html documents them as surfaces, static/_build_cli_desk.py + _restore_cli_desk.py can rebuild/restore the desk, and mag/dashboard_plugin.py:39 declares app.js in its view_contract (a manifest, not a loader). Verdict: dormant bundle, one dynamic-import hop from retirement, restorable by design.

## Findings

- F1 OPEN STATIC ROOT: /static/* serves every file under dashboard/static/ including 9 generator .py scripts, 59 .bak copies, room_state/overseer/model_census JSON, read_receipts.json, and the trails/lanes/tide data. Server is loopback/LAN by default (lan_proxy forwards LAN), but the surface exposes working source and internal data to anything on the LAN segment.
- F2 MISLEADING ROUTE NAMES: /game and /table serve wave.html, not game.html / table.html (server.py:604). The two real pages are /static/-only.
- F3 THE CONSOLE'S LIVENESS ORGAN DOES NOT EXIST: index.html fetches /api/v1/surfaces/liveness (index.html:95); rest.py ROUTES+LEGACY contain no such route; the fetch 404s on every load and the embedded LIVENESS_MAP (index.html:97-112, derived 2026-09-22) silently stands in.
- F4 5 orphans (above), incl. one module whose header comment falsely claims 3 consumer pages (oracle_dice.js).
- F5 The biggest byte weights in the web root are data, not code: grounding_wave.md 124,491 B, museum/estate_walk.lod.html 683,614 B, estate_walk.html 599,197 B, index_data/orphan_ledger.json 4,047,714 B, topic_index.json 3,627,383 B - all served whole by /static/* with no range support in safe_file (read_bytes then write, server.py:645-655).
- F6 Dead weight in the served tree: 59 .bak*/.retired copies + rest.py.bak-docfix/.bak_p0 + _frag_extract.tmp + 2.24 GB runaway-evidence jsonl. The .bak-nav family was the 2026-09-05/06/07 nav-wave habit; none are referenced by live code (only by each other and snapshots).
- F7 Deploy twin drift risk: dashboard-deploy/ carries a full static copy (incl. its own .mimosa hook-state); deck.html:479 itself records a past incident of site/dist/games/mud.html going byte-stale vs canonical. Two live copies of the whole static tree exist under one repo.
- F8 museum/ = retired archive (per index.html:119 liveness rule "museum/* retired (stale)"), yet museum.html is a live nav.js surface reading /static/museum.jsonl, and night/ (22 pages) is a live doc book from nav.js:32.
- F9 The only rest.py -> static-page wire is lattice.html via rest.py:4295; nav.js carries 95 links including 6 URL forms that hit server.py routes (/chan, /, /static/games/ x2).
- F10 Every number above traces to a command in Method; the per-file verdicts live in _f19_final.json (195 records with cls, title, size, out-edges, referrer lists).

## Scope caveats (what was NOT searched)

- Reference corpus excluded (read-verified counts from the per-top-dir probe): root .mimosa/ 3,121,985 files, .venv 52,198, memory/biography_backup 139,290, memory/runs 51,126, memory/biography 46,065, memory/agent_state 39,811, memory/corpus 22,422, memory/ghost 20,235, corpus/library 43,217, corpus/oral_history 15,749, mine/raw 100,983, agents/ pytest-tmp trees, watch/.mimosa 1,564, dashboard/data. Corpus walked: 66,667 files.
- The gap is closed for the 9 decision files (5 orphans + 4 code-only) by `git grep -F <name>` over ALL tracked files, which covers tracked archival trees; within those the only hits were auto-inventories, tar/zip backups, and the receipts already cited. Root .mimosa/ and mine/raw are untracked (git check-ignore: .mimosa/ ignored via .gitignore:190) and were not searched - a hook-artifact mention there would not be wiring.
- Frontend references inside git history (deleted files) are out of scope; working tree + HEAD index only.
- The two PRIVLIDGE twins differ (static/swarm.html 80,408 B vs static/games/swarm.html 79,502 B, cmp DIFFER): both live, both referenced (games/ by the arcade index, top-level by deck.html + todo.md + playtest_swarm.js); which is canonical is not decidable from references alone.

## Artifacts (this dir)

- f-19.md (this file) + dashboard-census.md (byte-identical mirror)
- _f19_census_scan.py - inventory + titles + edges + ref scan (corpus walk + substring pass)
- _f19_recheck.py - boundary-corrected re-verification + tier classification
- _f19_census_raw.json - raw scan output (inventory 591, by_ext, per-file titles/out-edges/refs)
- _f19_final.json - 195 classified records (cls, title, size, out, referrer lists)
