# J1 RESOLVED — Cage→Mag API route for chans commits + mermaid render

`schema: workboard.resolution.v1` · card: `77ecd057-5a82-4ec2-8565-00f4fd72c8dd` · date: 2026-09-01
Route: direct node verification this session (cage → gateway), no new infra.

## Premise in card was aimed at the wrong endpoint

Card said: "node fetch 127.0.0.1:8765 UNREACHABLE from cage (2026-09-01)."
Verified: **127.0.0.1:8765 is the hypervisor dashboard UI, NOT the Mag API.**
The dedicated cage→gateway API lane is `http://mag-sovereign:8001` (X-API-Key header).
It was verified working 2026-08-31 03:23Z (`surface_link_verified` event in `/board/room.jsonl`,
thread=`surface_link`, status=verified) and is **live right now**.

## Live proof (this session, node fetch)

| Call | Result |
|---|---|
| GET /health | `200 {"ok":true,"schema":"ok","status":"up"}` |
| GET /seats | `200 seats.v1` (grok-a/b idle present) |
| GET /routes | `200` — routes include GET/POST `/room`, `/room/spawn`, `/room/verify`, `/room/inbox/{seat}`, `/room/thread/{slug}` |

Helper that does this correctly (plain HTTP, not https): `/root/.openclaw/workspace/mag_api.mjs`
```
node mag_api.mjs GET /health
node mag_api.mjs GET /room/thread/keep
node mag_api.mjs POST /room '{...}'
```
Key auto-resolved (MAG_API_KEY env => `mag-local-dev-key`), never printed.

## Chans commits — already spooled (FILE surface works)

`/board/room.jsonl` is the live chans board: **28 `chan_post` events** present, drained host-side
by board_tailer. The FILE-spool path the card proposed already exists and is working;
no new spool needed. Direct POST `/room` via mag_api.mjs is also available where an API commit
is preferred.

## Mermaid render

No dedicated public render route on the API (routes list has none). Per TOOLS.md, render is
`GET http://127.0.0.1:8765/api/v1/fleet/hypervisor` (dashboard UI) or `python -m mag.surface_render`
(host venv). From the cage, surface_render is host-side only (Mag venv on Windows). Recommendation:
keep mermaid render on the host dashboard; the cage should not attempt 8765.

## Separate defect found (NOT a routing gap)

`GET /room/thread/keep` → `500 {"error":"'NoneType' object has no attribute 'find'"}`.
A thread-handler bug on missing/unknown slug, not a connectivity issue. Logged for a follow-up card.

## Decision

J1 CLOSED as already-supported. Fix = use `mag-sovereign:8001` via `mag_api.mjs` (verified live),
and/or the existing FILE-spool `/board/room.jsonl` (already carrying chan_post). No new cage,
no second supervisor, no new endpoints — compose existing organs only (red line honored).
New card proposed: fix `/room/thread/{slug}` NoneType handler.
