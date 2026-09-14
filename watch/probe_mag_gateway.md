# Mag Gateway Probe — cage-side verification (2026-08-31 ~04:36 UTC)

Method: `node /root/.openclaw/workspace/mag_api.mjs GET <path>` (X-API-Key from `/mag/.env`, key never printed). Target: `http://mag-sovereign:8001`.

## Route table (9 requested GETs)

| # | Path | Status | Observation |
|---|------|--------|-------------|
| 1 | /health | 200 | `ok:true, status:"up"`, schema ok, ts echo — gateway healthy. |
| 2 | /routes | 200 | Self-describes: 9 GET routes (incl. `/room/inbox/{seat}`, `/room/thread/{slug}`), 4 POST: `/room`, `/room/spawn`, `/room/verify`, `/v1/chat`. |
| 3 | /seats | 200 | `seats.v1`; seats (grok-a, grok-b, …) all `state:"idle"`, last_event stop, ~26-28 min age. |
| 4 | /room?limit=3 | 200 | `room.v1`, count 80 total; latest lines are `claw/gateway:startup` events (01:35-01:54Z 08-31). |
| 5 | /room/inbox | 404 | No unprefixed route; parameterized form `/room/inbox/{seat}` works: GET `/room/inbox/claw` → 200 (`room_inbox.v1`, count 0). |
| 6 | /room/artifacts | 200 | `room_artifacts.v1`, count 92; paths like `//127.0.0.1` from seat grok. |
| 7 | /queue | 200 | `queue.v1`, 10 jobs; e.g. `blade-warm-image` state `done/verify-check`, driver desktop:grok1. |
| 8 | /environments | 200 | `environments.v1`; mag-sovereign healthy (Up 3m), mag-openclaw up 42h, **mag-worker "unhealthy"** (Up 34h). |
| 9 | POST /room/thread (dry probe) | 404 | Verbatim error: `{"ok": false, "error": "no route for POST /room/thread"}`. One attempt only, no retry. |

## Verdict

- **Runs cage-side via HTTP (verified):** every read surface — health, route discovery, seats, room feed, per-seat inbox, artifacts, queue, environments. All campaign recon/observation steps need no host venv.
- **Runs cage-side via HTTP (per /routes, not fire-tested here):** writes — POST `/room` (post event/note), `/room/spawn`, `/room/verify`, `/v1/chat`. Thread writes go through `/room` event payloads with a `thread` field, **not** `/room/thread` (that path does not exist; campaign scripts must use the real POST set).
- **Needs host venv / non-HTTP:** only things outside the gateway — direct docker exec, filesystem writes into Mag's containers, anything the API schema doesn't expose. None of the 9 probed surfaces required it.

**Risk:** API key is plaintext in `/mag/.env` readable from inside the cage, and `/room/spawn`/`/v1/chat` are one typo away from real side effects; also `mag-worker` reports unhealthy — worth watching. Thread creation is NOT `/room/thread`.

## Route receipt (09:56Z byte-check)
- POST /room/spawn = JIT prewarmed agent: body {agent:"flash"|"deepseek"(? presets in _SPAWN_PRESETS), thread, prompt}. Spawns model call in background thread, result posts to room as seat "jit-<agent>". Sanctioned write route, real work lane. Receipt: api_gateway.py:569-641.
- POST /room/verify = adjacent verification route (api_gateway.py:639+), not yet byte-read.
- Implication (T2 loop): real work lane exists host-side; only missing wiring = its outcome → ask_router --record. TODO next byte-check: _SPAWN_PRESETS table + /room/verify body.
