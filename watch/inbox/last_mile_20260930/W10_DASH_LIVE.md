# W10 — verdicts panel served live

Date: 2026-09-29 (local) / filed from last_mile_20260930 lane · owner: W10 seat

## Verdict

SERVED LIVE. The verdicts panel (`dashboard/static/verdicts.html` + `/api/v1/verdicts`)
was confirmed absent from the running dashboard (404), root-caused, and brought live by
restarting the container. No rebuild needed.

## Evidence chain

1. **Before:** `curl 127.0.0.1:8765/api/v1/verdicts` → 404
   `{"error": "not found", "path": "/api/v1/verdicts"}` (catch-all at server.py:881 of the
   OLD in-memory code).
2. **Who owns 8765:** PID on the port is `com.docker.backend` (Docker proxy) → the
   dashboard is the **`mag-sovereign` container** (e26f592620cd, image `mag-sovereign:local`),
   up 15h at check time (started ~05:30, before the verdicts code landed Sep 29 20:24).
   The operator's `mag.cmd dashboard` (host `main.py`) was NOT the live surface — nothing
   host-side listens on 8765.
3. **Why restart sufficed:** `docker-compose.yml` mounts `./dashboard:/app/dashboard` (rw
   bind). New `server.py` (route at lines 616-617) was already inside the container FS;
   only the long-lived python process predated it. `restart: unless-stopped` policy.
4. **Action taken:** `docker restart mag-sovereign` (gentle, seconds downtime; no restart
   script exists — checked `scripts/`; this IS the exact restart command for future use).
5. **After (verified by curl):**
   - `/api/v1/verdicts` → **200**, `{"schema": "verdicts.v1", organs: {gps: rows [] (ledger
     empty — data state, not a defect), gwap: 3 files listed, mountain: ...}}`
   - `/static/verdicts.html` → **200**
   - live `/static/nav.js` contains the `["/static/verdicts.html", "Verdicts"]` entry
     (source nav.js:44; nav is client-side injected, so this is the render path).
   - Container post-restart: Up, health `starting` → expected to settle.

## STEER.md live state

`.venv/Scripts/python.exe tools/steer_read.py all` → ok. Operative row (scope `all`):
`st_20260930_seed_1` — **"keep rolling 24 wide; proven seats only; dogfood gps"**,
ts 2026-09-30T00:00:00Z, via `hand-edit` (operator-sourced, `proposal: false`). The
compute-ladder steer IS operative. Note: 1 malformed row skipped at line 7 (missing
`mate`/`steer`) — reader warned and exited 1 per spec; last VALID row governed.

## Notes for the operator

- The pre-restart `(unhealthy)` flag on mag-sovereign predates this work; healthcheck
  restarts fresh — watch whether it settles healthy.
- gps organ returns empty rows until `tools/gps_mcp/gps_ledger.db3` capability rows exist.
- If the panel 404s again after a future code landing: `docker restart mag-sovereign`
  (code is bind-mounted; rebuild only needed for dependency/image changes).
