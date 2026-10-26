# AC13 — verdicts panel gps rows live (two ledger instances → one)

Date: 2026-09-30 (filed 2026-09-29 local) · last_mile_20260930 lane · owner: AC13 seat
Working-tree change: `docker-compose.yml` (+1 volume). **No commit** (lane rule).

## Verdict

FIXED AND VERIFIED LIVE. The panel's empty gps rows were not a missing feed — the
X11 demo (and Z1's weld) wrote the correct production ledger all along. The live
dashboard is the `mag-sovereign` **container** (W10's finding), and the container
read a `/app/tools/gps_mcp/gps_ledger.db3` that **did not exist in the container**
(the image never carried `tools/gps_mcp`; no compose mount covered it). Missing
file → `_verdicts_gps_rows` returns `[]` → "gps rows empty - ledger has no data yet".
One bind mount now shares the host ledger into the container; the panel serves rows.

## Answers to the four checks

1. **What the dashboard reads:** `dashboard/server.py:107` `GPS_LEDGER_DB = ROOT /
   "tools" / "gps_mcp" / "gps_ledger.db3"`, queried read-only (`mode=ro`) in
   `_verdicts_gps_rows` (server.py:112-131). In the live container ROOT = `/app`,
   so the read target was `/app/tools/gps_mcp/gps_ledger.db3`.
2. **What the X11 demo wrote:** `server/verdict_feed.py:88`
   `PRODUCTION_GPS_DB = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"` — on the
   **host**, where the demo ran. Host file held the proof before any fix:
   capability row `mountain-world-v0 / world-tick, pass_rate 1.0, sample_size 4,
   updated_at 2026-09-30T03:20:55+00:00` (mtime 23:20 EDT Sep 29; 10 verdict_log
   rows total; repo-wide find: this is the only `gps_ledger*.db3`).
3. **Same path, different instances:** container path was absent
   (`docker exec mag-sovereign ls /app/tools/gps_mcp/` → No such file or
   directory; compose mounts memory/watch/logs/state/queue/jobs/configs/mag/
   dashboard/models/tests/main.py/mag_launch.py — no `./tools`, no `./server`).
   Chose "point them at the same file" over "run the feed against the dashboard's
   file": a container-local feed would fork a second divergent truth table, and
   re-running the demo against the host ledger would append 4 more verdict rows
   for zero information. The durable alignment is the mount.
4. **Fix + verification:**
   - `docker-compose.yml` mag service volumes: added
     `- ./tools/gps_mcp:/app/tools/gps_mcp` (dir mount, not file mount — file
     binds on Docker Desktop break if sqlite ever recreates the file; same
     overlay pattern as `./mag`, `./dashboard`).
   - `docker compose up -d mag` → Recreated + Started (seconds downtime, same
     class as W10's accepted restart; no rebuild).
   - After: `curl 127.0.0.1:8765/api/v1/verdicts` → 200 with **gps rows
     non-empty**: `mountain-world-v0 / world-tick / 1.0 / n=4` and
     `z-ai/glm-5.3-prime / night-judgment / 0.833… / n=6`. gwap (3 files) and
     mountain organs unchanged.
   - One ledger, byte-proven: md5 `10ea07c33e3377c114fc3fd91ce14471` identical
     for host `tools/gps_mcp/gps_ledger.db3` and container
     `/app/tools/gps_mcp/gps_ledger.db3`. No WAL/-shm sidecars present.
   - Panel page: `/static/verdicts.html` → HTTP 200.

## Z1 weld (server loop feed call) — verified wired

`server/server.py:38` imports `PRODUCTION_GPS_DB, VerdictFeed`; `_serve` (lines
451-459) constructs `VerdictFeed(world, PRODUCTION_GPS_DB, store=<log dir>/gwap)`;
`pump_once` calls `self.verdict_feed.feed_tick()` after each world tick (lines
109-116), fail-open by design ("the world outranks the meter"). The world server
runs host-side, so production ticks land in the host ledger — which the panel now
reads through the mount. No weld change needed.

## Notes for the operator

- `mag-sovereign` showed `(unhealthy)` before AND after (pre-existing per W10);
  the healthcheck story is untouched by this fix.
- The compose edit is uncommitted in the working tree (lane rule: no commit).
  If it ever lands, the receipt line above is the receipt comment.
- Next world-server ticks (Z1 weld) will grow `mountain-world-v0` sample_size in
  the same shared file; the panel reflects them on next poll with no restart.
