# BOT2 — Visual Deck Survey (fleet dashboard, door 127.0.0.1:8765/static/)

2026-09-10. Read-only GETs only. 131 HTML pages under `dashboard/static/`, ALL serve 200 through the door — zero BROKEN-PAGE. Health is a feed question, not a page question.

## THE POINT

The dashboard is 131 HTML pages and every one serves 200 through the 8765 door — nothing is a broken page; health is entirely a question of whether the JSON under the page is live, fresh, or frozen. Only the `/api/v1/fleet/hypervisor` API is genuinely live (ts 2026-09-10T12:29Z, polled by fleet.html / the_radar.html / index.html); most file feeds serve but are frozen 3-4 days (overseer.json 09-07 and still lists pre-rebuild mag-openclaw; live_feed/meter/decisions/room_state 09-06; verkle_pyramid_seed pinned at tip 5346 / 7,377 leaves while the chain has moved past it). For KV-OS the steals are already built — verkle_construction renders tree growth over time, chain_witness shows root-hash + leaf-count integrity, tesuji/cacheecon show verdict grids and econ cards, and live.html's overseer strip is the per-process census pattern — so a KV OS dashboard is an assembly job, not a build from zero.

## Per-page table (scoped pages; mtime = file date, today = 09-10)

| page | mtime | verdict | feed | steal-into-KV-OS |
|---|---|---|---|---|
| index.html (FLEET CONSOLE) | 09-09 | WORKS | /api/health + /api/v1/fleet/hypervisor + /api/workspace/tree — LIVE | console shell: nav + live hypervisor tile |
| fleet.html (HYPERVISOR) | 09-02 | WORKS | /api/v1/fleet/hypervisor — LIVE (only live API found) | cool/heat + real bills = KV cost/tier panel |
| the_radar.html | 09-08 | WORKS | /api/v1/fleet/hypervisor, setInterval poll — LIVE | watch radar, direct steal |
| live.html | 09-06 | STALE-FEED | overseer.json frozen 09-07T06:16Z, census pre-dates 09-08 rebuild | per-process census strip = page-table-per-process pattern |
| live_feed.html | 09-06 | STALE-FEED | live_feed.json + data/meter.json frozen 09-06 | trajectory excerpt stream with redaction note |
| verkle_construction.html (BIRTH CANVAS) | 09-09 | WORKS | index_data/verkle_birth.json (from verkle_chain.jsonl) | tree-growth-over-time = page allocation timeline / knot lattice |
| chain_witness.html (THRESHOLD) | 09-08 | WORKS | witness_snapshot.json 09-09: published_root + 7,377 rows | integrity strip: root hash + leaf count = KV crash-consistency proof |
| tesuji_map.html | 09-07 | WORKS | /static/tesuji_map.json fresh 09-09 | probe grid (SUPPORTED/DISPUTED per cell) = KV hit/miss verdict matrix |
| the_index.html (ESTATE MAP) | 09-09 | WORKS (heavy) | index_data/rollup.json + last_run.json (09-09) + ESTATE_INDEX.jsonl 402MB | storage census: per-tree files/bytes = slab usage; lazy-load the 402MB file |
| pipeline.html | 09-08 | WORKS | shaders/library/manifest.json (09-08) | cartridge contract = JIT tier-loader manifest pattern |
| tavern_test.html | 09-08 | WORKS | shaders/library/tavern.glsl | single-cartridge test harness |
| shadowbonk.html | 09-08 | BROKEN-FEED (partial) | sb_enemies/sb_upgrades json OK; ../state/shadow_work/projection_3d.json 404 via door | occlusion/volume viz; fix the out-of-root path |
| burn_board.html | 09-10 | WORKS (self-contained) | none | quota burn-down board — reuse for lane quota gauge |
| verkle_pyramid.html | 09-08 | STALE-FEED | verkle_pyramid_seed.json: tip_ts 09-06T23:08Z, 7,377 leaves (chain moved past) | chain-as-place zone render |
| decisions.html | 09-06 | STALE-FEED | decisions.json built 09-06T23:09Z | decision ledger with open-count |
| keeper_voice.html | 09-07 | STALE-FEED | keeper_voice_data.json generated 09-07 | world-state narration feed pattern |
| decks/cacheecon.html | 09-04 | WORKS / deck stale | self-contained 7 cards; INVARIANT HUNT live-arm widget; /api/status ref = 404 if ever fetched | CACHE-ECON warning cards + refeed gauge = hit-rate/tier-flow panel (bind mag/refeed_guard.py B1 94%) |
| decks/rocinante.html | 09-04 | WORKS / deck stale | 13 substrate cards; openclaw_traj.json ref | substrate readiness = hardware-tier deck (ROCINANTE DOCK/PREP) |
| decks/mesh3d.html | 09-04 | WORKS / deck stale | watch/steer_field/FIELD.json + eyes receipt + shader API | 3D mesh topology canvas with field overlays |
| decks/mag.html | 09-04 | WORKS / deck stale | 81 cards, mixed refs (events.json, field_smith.json) | master deck; card schema (id/verdict/evidence) is the KV annotation unit |
| decks/glmwatch.html | 09-04 | WORKS / deck stale | 10 cards, CACHE ECONOMICS WARNING content | model-lane watch deck |
| decks/legions.html, personal.html, gamebuild.html | 09-04 | WORKS / deck stale | self-contained (12/5/25 cards) | lane roster / operator / build-arc decks |
| home.html | 09-07 | WORKS | static landing | six-destination entry |
| all other ~105 pages (agents, aos, doctrine/*, night/* 18, art, mazes x6, wipeout x3, viz_*, rtfm_graph, shadow_walk, salon_lightmap, ...) | 09-02→09-09 | 200 OK, self-contained or archival | mostly none / local json | content archive, not dashboard chrome |

Feed probes (15 total): 200-live = hypervisor API; 200-fresh = tesuji_map.json (09-09), witness_snapshot.json (09-09), verkle_birth.json (operator-dated 09-11), rollup/last_run (09-09); 200-frozen = overseer (09-07), live_feed + meter + decisions + room_state (09-06), keeper_voice_data (09-07), verkle_pyramid_seed (tip 09-06); 404 = /api/status, state/shadow_work/projection_3d.json (out of static root).

Known defect to fix when stealing: all 8 decks share the title "DECK — Legions" — the deck generator never templatized `<title>` or the h1.

## Top-3 steal priorities for KV-OS

1. **live.html overseer strip + /api/v1/fleet/hypervisor** — the only live feed; the census-strip pattern (one row per process, status + uptime) is exactly the KV OS process table; point it at a fresh overseer writer and it is done.
2. **verkle_construction.html + chain_witness.html** — tree-growth-over-time plus root-hash/leaf-count integrity strip; the verkle chain is already a page tree, so these two render the KV OS memory map and its crash-consistency proof as-is.
3. **decks/cacheecon.html card format + tesuji verdict grid** — cache-econ warning cards bound to mag/refeed_guard.py (94% refeed) become hit-rate and tier-flow gauges; the tesuji SUPPORTED/DISPUTED cell grid becomes the per-tier probe/verdict matrix.
