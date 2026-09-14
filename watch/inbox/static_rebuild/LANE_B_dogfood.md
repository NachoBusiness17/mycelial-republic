# LANE B/6 — STATIC DOGFOOD RUN (2026-09-10)

Scope: all 137 .html in dashboard/static. Method: local parse scan (tail inspection — every file ends with a proper `</body></html>`, zero truncation), full grep of fetch/JSON/API targets, disk existence check on every referenced feed, live curl probes against 127.0.0.1:8765 (plus side ports 8743/8799).

## THE POINT

All 137 pages parse and none are truncated — 112 render clean — but the operator's instinct is directionally right: the operations cockpit is down while the art wing works. Thirteen pages fetch dead feeds (8 API endpoints return 404, 5 more accept the connection and hang forever without answering) and twelve more are frozen in time (overseer.json stopped 09-07 02:16, museum.jsonl 09-02, and ractor_board.jsonl is a 713 MB fossil from 09-03 that ractor.html still pulls whole into the browser). The broken pages are exactly the ones you'd steer by — home, agents, feed, health, cast, control, wearable — the fleet's instruments, not its paintings.

## Counts

| Verdict | Count |
|---|---|
| WORKS | 112 |
| BROKEN-FEED | 13 |
| STALE | 12 |
| BROKEN-PAGE | 0 |

Known anchors confirmed: `/api/v1/fleet/hypervisor` 200 (fleet.html + the_radar.html live); overseer.json mtime 2026-09-07 02:16 (frozen); `/api/status` 404; shadowbonk's `../state/shadow_work/projection_3d.json` 404 (file exists at repo-root `state/shadow_work/`, but the relative path from /static/ resolves into dashboard/state/ which does not exist).

## API surface status (probed 2026-09-10)

- 200: fleet/hypervisor, cost, chan/catalog, voice/shadow, ractor/tail, api/home, api/health, lattice-lab, local-pulse, table/view, workspace/tree, wave, stream (SSE, stays open — normal), files/working/decks_snapshot.json; POST voice/turn + chan/post exist (400 on empty body); diary/seal 200; refine 200.
- 404 (dead): api/status, v1/feed, v1/wearable/surface, v1/wearable/command, v1/remote/status, v1/remote/intent, v1/chan/wake, aos/send, aos/chat, /memory/* mounts (events.jsonl, astra_world), /static/lanes/ (dir itself; the .md files inside serve fine).
- HANG (accepted, never responds — worst class): v1/status, v1/quota, v1/agents, v1/loop/health, v1/display.
- Dead side ports: 8743 (sovereign shell), 8799 (saelis).
- Static feeds present but frozen: overseer.json 09-07, live_feed.json 09-06, room_state.json 09-06, decisions.json 09-06, museum.jsonl 09-02, ractor_board.jsonl 713 MB @ 09-03, keeper_voice_data.json 09-07, self_hologram_data.json 09-06, shadow_walk_content.json 09-06.
- Missing on disk (referenced, never existed here): field_smith.json, law_registry.json, law_lattice.json, invariants.json, field.json, dashboard/state/shadow_work/* (wrong relative base).
- Live feeds: index_data/* (ESTATE_INDEX.jsonl 420 MB, rollup, last_run — 09-10), tesuji_map.json 09-09, witness_snapshot.json 09-08, verkle_pyramid_seed.json 09-08, whale_feed.json 09-08, lanes/*.md 09-10.

## Verdict table (page | mtime | verdict | missing feed)

### BROKEN-FEED (13)

| page | mtime | verdict | missing feed |
|---|---|---|---|
| home.html | 09-07 | BROKEN-FEED | /api/v1/status (hang); overseer.json frozen 09-07 |
| agents.html | 09-02 | BROKEN-FEED | /api/v1/agents + /api/v1/quota (hang); pipes/ same family |
| feed.html | 09-02 | BROKEN-FEED | /api/v1/feed (404) |
| health.html | 09-02 | BROKEN-FEED | /api/v1/loop/health (hang) |
| cast.html | 09-02 | BROKEN-FEED | /api/v1/display (hang) |
| control.html | 09-06 | BROKEN-FEED | /api/v1/remote/status + remote/intent (404) |
| wearable.html | 09-02 | BROKEN-FEED | /api/v1/wearable/surface + wearable/command (404) |
| aos.html | 09-02 | BROKEN-FEED | /api/aos/send + /api/aos/chat (404) — page fully dead |
| game.html | 09-04 | BROKEN-FEED | 127.0.0.1:8799/api/saelis (port dead) |
| daytool.html | 09-05 | BROKEN-FEED | law_lattice.json + law_registry.json + field.json (not on disk) |
| ontology_dashboard.html | 09-08 | BROKEN-FEED | /memory/runs/harness/events.jsonl (404 — /memory not routed) |
| salons/astra/index.html | 09-05 | BROKEN-FEED | ../../../memory/runs/astra_world/research/ (resolves to unrouted /memory; graceful "pending" fallback) |
| shadowbonk.html | 09-08 | BROKEN-FEED | ../state/shadow_work/projection_3d.json (404; known anchor) |

### STALE (12)

| page | mtime | verdict | frozen feed |
|---|---|---|---|
| live.html | 09-06 | STALE | overseer.json frozen 09-07 02:16; live_feed.json 09-06 |
| ractor.html | 09-06 | STALE | ractor_board.jsonl 713 MB frozen 09-03, fetched whole into browser (tab-killer; tail API is live) |
| museum.html | 09-02 | STALE | museum.jsonl 09-02 |
| museum/index_old_mag_board.html | 09-06 | STALE | superseded by name (_old_) |
| index.clear-ui.html | 09-02 | STALE | superseded by index.html 09-09 |
| _rtfm_graph_shell.html | 09-04 | STALE | shell variant of rtfm_graph.html |
| keeper_voice.html | 09-07 | STALE | keeper_voice_data.json 09-07 (chunk_manifest/world.json strings are attribution labels, not fetches) |
| salon_lightmap.html | 09-07 | STALE | room_state.json 09-06 |
| self_hologram.html | 09-06 | STALE | self_hologram_data.json 09-06 |
| shadow_walk.html | 09-06 | STALE | shadow_walk_content.json 09-06 (content json exists; chunk_manifest ref is a label) |
| decisions.html | 09-06 | STALE | decisions.json 09-06 (snapshot board) |
| sovereign_shell.html | 09-02 | STALE | launcher points at 8743 — port dead |

### WORKS (112)

| page | mtime | verdict | missing feed |
|---|---|---|---|
| fleet.html | 09-02 | WORKS | — (hypervisor 200) |
| the_radar.html | 09-08 | WORKS | — (hypervisor 200) |
| chan.html | 09-02 | WORKS | — (catalog 200, post live; chan/wake 404, minor) |
| wave.html | 09-02 | WORKS | — (wave/stt/turn/game live) |
| table.html | 09-02 | WORKS | — (game/table-view/voice live) |
| lattice.html | 09-02 | WORKS | — (lattice-lab 200; 8743 probe dead, minor) |
| seat.html | 09-02 | WORKS | — |
| spend.html | 09-03 | WORKS | — (cost 200) |
| decks.html | 09-05 | WORKS | — (cost 200 + SSE stream live) |
| cast-voice.html | 09-05 | WORKS | — (voice/shadow, refine, diary/seal 200) |
| tesuji_map.html | 09-07 | WORKS | — (tesuji_map.json 09-09) |
| the_index.html | 09-09 | WORKS | — (index_data fresh 09-10) |
| verkle_construction.html | 09-09 | WORKS | — (verkle_birth 09-09) |
| index.html | 09-09 | WORKS | — (workspace/tree 200) |
| verkle_pyramid.html | 09-08 | WORKS | — (seed 09-08) |
| chain_witness.html | 09-08 | WORKS | — (witness_snapshot 09-08) |
| whale_feed.html | 09-07 | WORKS | — (whale_feed.json 09-08) |
| pipeline.html | 09-08 | WORKS | — (shaders manifest 09-08) |
| viz_3d_verkle.html | 09-04 | WORKS | — (local-pulse 200) |
| rtfm_graph.html | 09-04 | WORKS | — |
| lanes.html | 09-04 | WORKS | — (fetches /static/lanes/<slug>.md — files fresh 09-10) |
| tavern_test.html | 09-08 | WORKS | — (tavern.glsl present) |
| tavern_brawl.html | 09-08 | WORKS | — |
| live_feed.html | 09-06 | WORKS | — (self-refresh viewer) |
| burn_board.html | 09-10 | WORKS | — |
| viz_horse_run.html | 09-10 | WORKS | — |
| viz_gallery.html | 09-10 | WORKS | — |
| bad_apple_field.html | 09-06 | WORKS | — (self-contained; chunk_manifest ref is a label) |
| maze_arena.html | 09-06 | WORKS | — |
| decks/cacheecon.html | 09-04 | WORKS | — (self-contained deck) |
| decks/gamebuild.html | 09-04 | WORKS | — |
| decks/glmwatch.html | 09-04 | WORKS | — |
| decks/legions.html | 09-04 | WORKS | — (field_smith/events refs are prose, not fetches) |
| decks/mag.html | 09-04 | WORKS | — |
| decks/mesh3d.html | 09-04 | WORKS | — |
| decks/personal.html | 09-04 | WORKS | — |
| decks/rocinante.html | 09-04 | WORKS | — |
| night/index.html | 09-03 | WORKS | — |
| night/light_codec.html | 09-03 | WORKS | — |
| night/light_loop.html | 09-03 | WORKS | — |
| night/stockfish.html | 09-03 | WORKS | — |
| night/sherpa_spec.html | 09-03 | WORKS | — |
| night/time_machinery.html | 09-03 | WORKS | — |
| night/maze_enhancement.html | 09-03 | WORKS | — |
| night/primer_wired.html | 09-03 | WORKS | — |
| night/chord_v4.html | 09-03 | WORKS | — |
| night/design_theory.html | 09-03 | WORKS | — |
| night/game_codex.html | 09-03 | WORKS | — |
| night/morning_state.html | 09-03 | WORKS | — |
| night/game_lattice.html | 09-03 | WORKS | — |
| night/titor_stack.html | 09-03 | WORKS | — |
| night/surface_atlas.html | 09-03 | WORKS | — |
| night/orphan_register.html | 09-03 | WORKS | — |
| night/maze_synthesis.html | 09-03 | WORKS | — |
| night/the_session_self_steal.html | 09-03 | WORKS | — |
| night/hermes_steal_v0.html | 09-03 | WORKS | — |
| night/trade_sheet.html | 09-03 | WORKS | — |
| night/hermes_dossier_v1.html | 09-03 | WORKS | — |
| night/systems_gap_map.html | 09-03 | WORKS | — |
| doctrine/AUTONOMY_WHEEL.html | 09-03 | WORKS | — |
| doctrine/BURST_DOCTRINE.html | 09-03 | WORKS | — |
| doctrine/SWARM_SCALE_PLAN.html | 09-03 | WORKS | — |
| doctrine/TRI_PARTY.html | 09-03 | WORKS | — |
| doctrine/X_SCOUT_DOCTRINE.html | 09-03 | WORKS | — |
| rib_toy.html | 09-03 | WORKS | — |
| steer_field.html | 09-03 | WORKS | — |
| dungeon.html | 09-03 | WORKS | — |
| arena_operator_field.html | 09-03 | WORKS | — |
| erosion_field.html | 09-03 | WORKS | — |
| smith_chart.html | 09-03 | WORKS | — |
| scout_deck.html | 09-03 | WORKS | — |
| mesh_gallery.html | 09-03 | WORKS | — |
| art/index.html | 09-04 | WORKS | — |
| lattice_check.html | 09-04 | WORKS | — (self-tests on load) |
| claim_check.html | 09-04 | WORKS | — |
| chain_check.html | 09-04 | WORKS | — |
| falsifiers.html | 09-04 | WORKS | — |
| phonesalon.html | 09-04 | WORKS | — |
| labs_map.html | 09-04 | WORKS | — |
| calabi_yau.html | 09-04 | WORKS | — |
| field_quills.html | 09-04 | WORKS | — |
| fleet_symbols.html | 09-04 | WORKS | — |
| memory_map.html | 09-04 | WORKS | — |
| module_map.html | 09-04 | WORKS | — |
| verkle_knot_wave.html | 09-04 | WORKS | — |
| steal_tools.html | 09-04 | WORKS | — |
| grab_write.html | 09-04 | WORKS | — |
| viz_spore_fish.html | 09-04 | WORKS | — |
| operator_board.html | 09-05 | WORKS | — |
| arrakis.html | 09-05 | WORKS | — |
| doorbench.html | 09-05 | WORKS | — |
| conservation_room.html | 09-06 | WORKS | — |
| eraser_maze.html | 09-06 | WORKS | — |
| spectral_maze.html | 09-06 | WORKS | — |
| fable_room.html | 09-06 | WORKS | — |
| intel.html | 09-06 | WORKS | — |
| incident_dungeon.html | 09-07 | WORKS | — |
| worldline_dungeon.html | 09-07 | WORKS | — |
| airflow_home.html | 09-07 | WORKS | — |
| phase_particles.html | 09-07 | WORKS | — |
| light_maze.html | 09-07 | WORKS | — |
| hardware_primer.html | 09-07 | WORKS | — |
| reply_console.html | 09-07 | WORKS | — |
| whale_console.html | 09-07 | WORKS | — |
| pong.html | 09-07 | WORKS | — |
| wipeout_lightmaze.html | 09-08 | WORKS | — |
| wipeout_v2.html | 09-08 | WORKS | — |
| wipeout_sunset.html | 09-08 | WORKS | — |
| the_rings.html | 09-08 | WORKS | — |
| chaos_refract.html | 09-08 | WORKS | — |
| universe_within.html | 09-08 | WORKS | — |

## 5 worst offenders

1. **home.html** — the front door. `/api/v1/status` hangs ~6.5 s every load, then the panel falls back; overseer strip reads frozen 09-07 data. First impression of the whole dashboard is a stall.
2. **agents.html** — the swarm console. `/api/v1/agents` and `/api/v1/quota` accept connections and never answer — the browser just spins. SSE stream is the only live part.
3. **health.html** — the health page is blind: its single feed `/api/v1/loop/health` is in the hang class. The watchman cannot see.
4. **feed.html** — named after an endpoint that no longer exists; `/api/v1/feed` is a flat 404.
5. **aos.html** — both of its endpoints (`/api/aos/send`, `/api/aos/chat`) are 404; the page is 100% dead weight.

Dishonorable mentions: **ractor.html** fetches the 713 MB ractor_board.jsonl (frozen 09-03) whole into the tab — works, but kills the browser; **daytool.html** has three buttons (law lattice / law registry / steer field) wired to files that were never written to disk; **wearable.html** and **control.html** each lost their entire endpoint family to 404s; side services on 8743 (shell) and 8799 (saelis) are down, quietly dead-ending lattice.html's shell probe and game.html entirely.

## Rebuild targets (for the static_rebuild lane)

Priority order implied by the evidence: (1) the five hanging endpoints (status/quota/agents/loop-health/display) — one server-side fix likely revives five pages; (2) repoint or resurrect the eight 404 endpoints; (3) regenerate the six missing JSONs (law_lattice, law_registry, field, field_smith, invariants, projection_3d path fix); (4) re-arm the frozen feed writers (overseer, live_feed, room_state, museum, decisions); (5) stream or slice ractor_board.jsonl instead of serving 713 MB raw.
