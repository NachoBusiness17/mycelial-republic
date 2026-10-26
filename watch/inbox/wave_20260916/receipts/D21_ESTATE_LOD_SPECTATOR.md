# D21 — ESTATE_INDEX LOD + relay spectator (FIFTY-WIDE estate bundle)

- **Wave:** 20260916, lane D21 (Mickey17 gen-2; gen-1 died to a rate limit)
- **Status:** DONE — all three steps landed, tests green
- **Repo:** C:\Users\foste\Documents\projects\local_sovereign_agent
- **Constraints honored:** receipt-first, no git, no paid APIs, repo venv interpreter only, Write/Edit for source

## Plan
1. ESTATE_INDEX LOD — zone-level level-of-detail for estate walk builder; keep self-contained HTML law; emit `.lod.html` alongside if regen of the 585KB original is risky.
2. Relay spectator — read-only GET endpoint on dashboard relay (:8766) returning current lantern-state JSON; stdlib-only; 6s expiry intact; POST untouched; compile check.
3. Tests: builder syntax check, relay compile check, file size sanity.

## Log
- Receipt filed (this file). Read builder + relay.
- Builder: added `compute_lod_zones()` (4×4 spatial grid over estate bounds; per-zone node/corridor/star counts, dominant-type histogram, 6 sample titles) + `LOD_TEMPLATE` + `build(lod_only=)` + `--lod-only` flag. Ran in LOD-only mode: **main estate_walk.html NOT regenerated** (per mission's risk clause) — the .lod.html was emitted alongside.
- Relay: added `GET /mud/state` spectator endpoint + `SEEN_TOTAL` counter; POST path and `/mud/others`/`/mud/ping` untouched.

## What changed
1. `dashboard/static/_build_estate_walk.py` (23,359 → 35,295 bytes)
   - `OUT_LOD` = `dashboard/static/estate_walk.lod.html`; `ZONE_GRID = 4`.
   - `compute_lod_zones(nodes, edges, stars)`: deterministic spatial zoning; zone summaries ride along on the main payload as `data["lod"]` (main template ignores it) so a future full regen carries the index for free.
   - `LOD_TEMPLATE`: second **self-contained HTML** ("ESTATE INDEX"). Startup parses zone summaries only; the full estate payload sits in an inert `<script type="application/json" id="full">` block (JSON-parsed only when a zone is opened or "expand: full estate" is clicked; `</` escaped as `<\/` in the embed). Overview → click zone → zone detail (internal corridors + in-zone nodes/stars) → full estate; ESC/← back; pan/zoom + hover tooltips; click-vs-drag guard.
   - `build(lod_only=False)`; `--lod-only` writes only the .lod.html. Build ran **lod-only** this lane — the builder's internal read-only `git log` executed as part of its normal data pull; no direct git commands by the lane.
2. `dashboard/mud_relay.py` (6,113 bytes)
   - `GET /mud/state` → `{"ok":true,"now":...,"expire":6.0,"players":[fresh lanterns with age s],"stale":N,"seen_total":N}`. Read-only (no mutation, no sweep), stdlib-only, 6s expiry governs the `players` list; expired ids counted as `stale` until the existing 24s sweep.
   - `SEEN_TOTAL` incremented under LOCK in POST (existing behavior otherwise byte-identical).
   - Docstring API table updated.

## Sizes
- `dashboard/static/estate_walk.html` — **599,197 bytes, UNTOUCHED** (mtime 2026-09-14 19:05:33 preserved).
- `dashboard/static/estate_walk.lod.html` — **683,614 bytes (667 KB)**, new.
  - Honest note: it is *larger* than the main walk because the payload grew with Sep 14→16 commits/trails (now 201 commits vs the old build's 144-era) and the .lod.html embeds the full payload as inert JSON — the LOD win is **startup cost** (parse 16 zone summaries ≈ KBs instead of JSON-parsing 233 nodes/111 corridors/1200 stars on load), not download bytes.
- `dashboard/mud_relay.py` 6,113 bytes · `_build_estate_walk.py` 35,295 bytes.
- Receipt: this file.

## Test outputs
- `py_compile` via `compileall -q dashboard` (repo venv): **COMPILE_OK**.
- Build (lod-only): `estate_walk.lod.html: 667 KB | zones 16 (grid 4x4) detail-inert-until-open | window 2026-08-04..2026-09-16`.
- Payload/LOD reconciliation (JSON-parsed both embedded blocks): `FULL_BLOCK_OK nodes=233 edges=111 stars=1200 commits=201 lanes=6 lod_key=True` · `LOD_BLOCK_OK zones=16 node_sum=233 star_sum=1200 internal_edge_sum=102` — **zone sums match the payload exactly** (233/111/1200 = mission census).
- Relay live smoke (scratch port 18799, repo venv, stdlib urllib):
  - `SEEN1/SEEN2 {ok:true}` — POST unchanged.
  - `STATE_FRESH ok=True expire=6.0 n_players=2 seen_total=2 ages=[0.0, 0.0]`.
  - After 6.5s: `STATE_EXPIRED n_players=0 stale=2 seen_total=2` — **6s expiry honored**.
  - `OTHERS_REGRESSION {"ok": true, "others": []}` (expired correctly filtered) · `PING_AFTER {'ok': True, 'players': 0}`.

## Next stone
- Wire `data["lod"]` into the main walk's HUD (zone thumbnails / jump-to-zone) on its next full regen, and regenerate estate_walk.html then (deliberately skipped tonight to leave the 585KB artifact untouched).
- Optional .lod.html shrink: drop lane `events` details from the inert block (lantern replay is the main walk's job; the index needs structure only) — would cut a few hundred KB.
- Relay v2 (authoritative server-side sim) remains the mud_relay's own next stone; a spectator page could poll `/mud/state` and render embers on the estate canvas.
- Note: a prior gen-1 draft at this receipt path, if any, was overwritten when this lane filed its receipt-first stub (mission designated this path; no git history consulted per lane law).
