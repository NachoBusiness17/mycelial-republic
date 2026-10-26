# BOT1 — Fleet Console API Survey (KV OS steal lane)

Surveyed 2026-09-10T12:29Z. Read-only GETs to 127.0.0.1:8765 only. Bounded sweep, nothing fixed, nothing spawned.

## THE POINT

The FLEET CONSOLE at /static/ is a single 13.8 KB HTML file whose JavaScript calls exactly four API endpoints: /api/health, /api/v1/fleet/hypervisor, /api/workspace/tree, /api/workspace/file — search is done client-side over the tree slices, there is no search endpoint. All four work and answer fresh (server-side ts 2026-09-10T12:29Z, seconds old); health honestly self-reports the body as degraded (heartbeat stale since 09-08). The whole pattern — health doc, hypervisor seats/bills, tree listing, file text reader — is a read-only file membrane served by stdlib Python http.server, and that membrane is the skeleton of a KV OS control plane: steal the shapes, add mtime/size, and add the one missing organ (server-side search).

## Endpoint table

| Endpoint | Works/broken | Freshness | Steal-into-KV-OS note |
|---|---|---|---|
| GET /api/health | works (valid JSON) | fresh — ts 2026-09-10T12:29:21Z, computed live per call. Content reports `ok:false, status:degraded` (mag heartbeat stale 210,047s since 09-08T02:08, `alive:false`) — endpoint fresh, body degraded, honestly labeled | THE health shape: {ok, status, ts, integral{heartbeat,pid,port checks}, recording, lanes{}, missing_while_down[], gaps[{when_down,on_restart}], reconnect{commands, law}, hallucination_guard}. A cache OS should steal the composed-diagnosis pattern: not just ping, but gaps + reconnect playbook + "trust file ages, not model claims" guard |
| GET /api/v1/fleet/hypervisor | works | fresh — ts 2026-09-10T12:29:23Z | Fleet view: `seats[] {seat, available, available_n, checks_n, ratio}` (7 seats, 5/7), `bills{deepseek_spend: $63.72, balance: 11.81}`, `active free lanes: 18`, plus a pre-rendered `mermaid` flowchart string. KV OS: seat/ratio/bills shape is exactly the cache-tenant + spend view; server-side mermaid string is a cheap UI trick worth keeping |
| GET /api/workspace/tree?path=X&depth=N | works | live directory read; entries carry NO mtime/size | Minimal listing shape: {ok, root, entries:[{name, path, type: dir\|file}]}. KV OS cache-listing primitive — steal as-is but ADD mtime+size. Two defects: entries silently capped (mag and watch both returned exactly 400 — watch has 1,000+ files, so truncation is invisible; add `total` field), and root path= lists odd parent junk (`%SystemDrive%`, `ProgramData`) — scope the root |
| GET /api/workspace/file?path=X | works | returns file text; no mtime/size metadata in response | Reader shape: {ok, path, text}; clean error shape {ok:false, error:"not found", path}. Client caps render at 200k chars. This is the KV OS cache-line viewer. NOTE: a POST sibling handler exists (h_workspace_file_post, rest.py:5329/5397) — the write door lives on the same route; a KV OS should split read and write onto separate ports. Not touched this survey (GET-only bounds) |
| GET /api/board | works | live lanes + local model map (gemma:2b, qwen-desk) | Lane/model registry — KV OS wants this as its cache-tier table |
| GET /api/usage | works | fresh — tail rows ts 2026-09-10T11:12Z, per-lane today counts (L1:490, L0:10) | Per-lane counters + escalation budget — the KV OS quota meter |
| GET /api/home | works | live, schema "mag_home_summary.v2" | Headline + zeitgeist summary card — steal the versioned-schema habit |
| GET /api/overview | BROKEN (timeout >8s, 0 bytes) | n/a | Heavy aggregate; KV OS: keep single-purpose fast endpoints, not god-endpoints |
| GET /api/quota | BROKEN (timeout >8s, 0 bytes) | n/a | Same lesson — usage endpoint already carries the live numbers |
| GET /api/providers | BROKEN (timeout >8s, 0 bytes) | n/a | Probe lanes synchronously, presumably; KV OS should cache probe results instead |

Console-called endpoints = first four rows; the rest are the same server's wider surface sampled once each (used by other /static pages — dashboard/static pages reference ~40+ /api/* routes total; not exhaustively surveyed, out of bounds).

MISSING ORGAN: no /api/search. The console fakes search by loading tree slices and filtering in the browser. A cache OS needs a server-side find (path/name/content grep over the cache) — that is the one endpoint the console proves by absence.

## Serving-process identity

- Host-side listener on 127.0.0.1:8765 is com.docker.backend.exe (PID 17192) — Docker Desktop port-forward. The actual server runs inside the mag-sovereign container.
- Server = Python 3.12 stdlib `ThreadingHTTPServer` + `BaseHTTPRequestHandler` (dashboard/server.py:14,1015,1091), Server header `MagDashboard/1.0` set at dashboard/server.py:466.
- API routes live in `dashboard/rest.py` route table: GET /api/v1/fleet/hypervisor (h_fleet_hypervisor, rest.py:5011), GET /api/workspace/tree and /api/v1/workspace/tree (h_workspace_tree, rest.py:5327,5395), GET /api/workspace/file and /api/v1/workspace/file (h_workspace_file_get, rest.py:5328,5396; POST sibling at :5329,5397 — not touched), GET /api/health (h_health, rest.py:5342). server.py:666 dispatches via `dashboard.rest.dispatch`.
- Absolute paths: C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\server.py and C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\rest.py; console HTML served from C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\static\.

## KV OS verdict

Steal whole: health shape (composed diagnosis + gaps + reconnect), hypervisor shape (seats/ratio/bills/mermaid), tree/file membrane (the KV namespace listing + value reader), usage counters. Fix while stealing: add mtime/size to tree+file, add `total` to capped listings, split the POST write door onto its own route/port, kill god-endpoints (overview/quota/providers time out), and build the missing /api/search. Every console payload is plain JSON with a server-side ts — freshness discipline already correct.
