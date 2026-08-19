# Handoff — /table fix (for ChatGPT / next agent). Read this FIRST.

Goal: get http://127.0.0.1:8765/table (the D&D text-adventure page) working and STABLE.
Please read this before touching anything — it is the grounded truth so you don't re-break it.

## Symptom (what "broken" looked like)
- Page at /table served wave.html which rendered, but /static/wave_scene.js (3KB) and
  /api/v1/wave both returned ERR_EMPTY_RESPONSE, and the boot fetch threw 'Failed to fetch'.
- Root cause of the ERR_EMPTY_RESPONSE: the DESK PROCESS ballooned to 4-5GB (a memory leak) and
  wedged the single-process server, so even tiny requests timed out against the 20s handler timeout.

## Root cause (verified)
- NOT file sizes (all tiny), NOT routing, NOT the ~1.6s snapshot.
- The desk process leaked to ~5GB. Operator's hint: "my text adventure tried to mount a 5gb world" /
  "the renderer crashed the page rendering ~5gb." The world itself is TINY (world_state.json = 0.2MB,
  40x16 ASCII grid). The 5GB was the render/cache layer holding large objects.

## Fix ALREADY APPLIED + VERIFIED (on disk, mag/renderman.py)
- The render caches (TextureCache max 1000, GeometryCache max 500) were bounded in COUNT but
  unbounded in per-entry SIZE -> could hold 5GB of large parsed/geometry objects.
- Added `MAX_CACHE_VALUE_BYTES = 2 * 1024 * 1024` (2MiB) + `_approx_size()` guard: `put()` and
  `put_structured()` SKIP any value over 2MiB. VERIFIED: reload clean; big value skipped (cache
  size stays 1 after big+small); TextureCache.get(big) = None.
- IMPORTANT: this fix is on disk but NOT live until the server/desk process is RESTARTED.

## Current state
- The desk was restarted (by the desk agent); the view API answered ~60ms (Keep Gatehouse,
  doors south/north/down) at that time. State may have changed since — verify live.

## What to check / avoid
- RESTART the desk/server so the renderman.py fix loads. Don't hand-edit the running process.
- There is a disk cache: dashboard/server.py line ~506 writes memory/working/table_view.json —
  check it isn't stale/huge.
- There are ~10 leftover python processes (governor_auto, ghost --daemon, multiple ipykernel
  kernels) starving the box — that contributes to wedging. Safe to reap stale notebook kernels.
- Coordinate: do NOT make conflicting edits to server.py /table routing or the wave page that
  overlap with the render-cache fix. One clean state, then verify by loading the page.

## Standing context
- This is the Mycelial Republic sovereign agent (local_sovereign_agent). The D&D game is the real
  game (game_campaign / game_world), NOT the necromancer clicker (game.html).
- DeepSeek default for narration (mag/game_passage.py, game_narrate.py rewired), deterministic
  route is the $0 instant fallback.
