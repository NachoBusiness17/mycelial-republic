# API endpoint map: dashboard/rest.py + dashboard/server.py

Item s2-18, banked 2026-09-28. Census of every HTTP surface in the two dashboard
server files: route, method, handler, auth requirement, response shape.

Instruments (all run this session):

- AST parse of `dashboard/rest.py` ROUTES + LEGACY tables (`_s218_extract.py`,
  stdlib `ast`, no regex on source): 347 ROUTES rows (rest.py:5079-5432) +
  64 LEGACY rows (rest.py:5435-5500) = 411 rows, 323 distinct paths, 234 distinct
  named handlers + 3 lambdas.
- Live cross-check: the running operator desk on 127.0.0.1:8765 (PID 14308, started
  2026-09-25 23:47:33 EDT per `wmic process where processid=14308 get creationdate`)
  self-reports `GET /api/v1/endpoints` count=411 - exactly the file's row count.
  Agreement explained: both files are clean vs HEAD (`git status --porcelain` empty),
  the only commits since process start that touched them (5dff72ac3 Q-042 13:10 EDT,
  +18/-9 inside h_seat_steer only; d90bc8607 Q-028 15:09 EDT, +12 = the new
  /api/v1/links/tail door in server.py) change no route rows, so the in-process
  module and the file carry the same table.
- Live GET probes with curl against 8765 for response-shape evidence (read-only; no
  mutating POST was fired).

## 1. Dispatch architecture

- Entry: `dashboard/server.py` `Handler(BaseHTTPRequestHandler)` (server.py:466),
  `ThreadingHTTPServer` on 127.0.0.1:8765 by default (server.py:49, run() :1107),
  optional TLS wrapper `_TLSServer` (server.py:1051).
- server.py `do_GET` (:494) first serves a set of fixed routes inline (cost, tails,
  pages, files, SSE), then hands anything under `/api/` to `dashboard.rest.dispatch`
  (server.py:701-715). `do_POST` (:814) same shape (:896-902); `do_PATCH` (:1025)
  dispatches only; `do_OPTIONS` (:1041) answers 204 CORS preflight.
- `dispatch(method, path, body, query)` (rest.py:5520-5544) walks ROUTES+LEGACY
  compiled once at import (rest.py:5514-5517); `{name}` segments compile to
  `([^/]+)` (rest.py:5503-5511). Path params overwrite same-named query params
  (rest.py:5537-5539). Handler exception -> 500 `{"ok": false, "error": str(e)[:400]}`
  (rest.py:5540-5543). No route -> server.py generic 404 `{"error": "not found",
  "path": ...}` (server.py:799 GET, :924 POST).
- Envelopes: `_ok(data, status=200, schema=...)` -> `{ok: true, schema?, ...data}`
  (rest.py:25-32); `_err(code, message, **extra)` -> `{ok: false, error: ...}` with
  real HTTP codes (rest.py:35-39). Usage across rest.py: 13 `_ok(` sites, 78 `_err(`
  sites (grep counts).
- Deadline wrapper `_dl` (rest.py:5004-5024) hard-caps 4 hot handlers (loop_health,
  overview, providers, quota, rest.py:5027-5030) at 5.0s (rest.py:4999), returning
  503 `{ok:false, stale:true, error:"timeout", last_known}` on overrun; success payloads
  are cached in `_STALE_CACHE`.
- Shadowing: GET /api/v1/table/view and GET /api/table/view are served by the
  server.py inline branch (server.py:672-698, subprocess + memory/working/table_view.json
  cache) before dispatch ever sees them, so the GET rows at rest.py:5221/5223 are
  unreachable from HTTP; their POST rows (:5222/:5224) do reach h_table_view. GET
  /api/catch-up is special-cased into a POST dispatch call (server.py:706-709).
  GET /api/sessions legacy responses are re-shaped to `{sessions:[...]}` for old UI
  (server.py:713-714).

## 2. Auth requirement: NONE at the HTTP layer

Findings, each from code read this session or a command run this session:

- No authentication check exists anywhere in either file. The only request header
  either file reads is Content-Length (server.py:802, for body framing).
  `grep -n "self.headers" dashboard/server.py` -> line 802 only;
  `grep -n "headers.get|Authorization|cookie|Cookie" dashboard/rest.py` -> line 140
  (`r.headers.get_content_charset()` on an outbound web fetch, not inbound auth).
- server.py:824 carries the comment "Auth: same X-API-Key gate as the rest of the API
  (loopback-only by default)" above POST /mcp - the gate it names does not exist in
  the code path. POST /mcp (server.py:825-839) executes arbitrary registered MCP
  tools (`tools/call`) with no credential check. Stale/wrong comment.
- The real perimeter is the bind address: `bind_host()` (config.py:153-160) returns
  127.0.0.1 on bare metal (container override via MAG_BIND_HOST). Live netstat:
  8765, 8766, 8001 all LISTENING on 127.0.0.1 only (PID 14308). Anything on the
  host - every local process, any malicious local actor - can call every endpoint,
  including POST /api/v1/power/stop (kill switch, rest.py:5322) and POST /mcp
  tools/call, with no credential.
- CORS is wide open by design: OPTIONS answers `Access-Control-Allow-Origin: *`,
  methods GET/POST/PATCH/OPTIONS (server.py:1041-1048, live-verified below).
  Browsers on other origins can GET the API (responses carry no auth dependency);
  the SSE streams add `Access-Control-Allow-Origin: *` explicitly (server.py:936, :967).
- The only X-API-Key in the estate is on a different process: the LAN proxy
  `dashboard/lan_proxy.py` (:8, :33, :53) fronts the mag MCP gateway on 8001 and
  relies on that gateway's key check; the dashboard on 8765 has no equivalent.

## 3. server.py fixed routes (outside the rest.py dispatch table)

Every row read from server.py this session. Auth column is NONE for all rows
(section 2); repeated here once, not per row.

| Method | Route | Handler (server.py line) | Response shape |
|---|---|---|---|
| GET | /api/v1/cost | inline :502-512, fed by daemon thread `_cost_refresher` :1075-1104 | 200 cost_surface.v1 payload `{schema, truth, enforcer, overlay}`; 202 while warming `{schema, warming:true, warming_since, error}` |
| GET | /api/v1/ractor/tail | inline :517-523 via `_tail_jsonl` :75-99 | `{rows:[...], truncated:bool, bytes_read:int}` from dashboard/data/ractor_board.jsonl, ?limit= 1..2000 default 500 |
| GET | /api/v1/links/tail | inline :529-535 (landed today, d90bc8607 FW-45) | same tail shape over watch/inbox/LINKS.jsonl, ?limit= 1..2000 default 200; NOTE: 404 on the running 8765 (section 8) |
| GET | /data/{name} | inline :540-557 | raw bytes of allowlisted `{ractor_board.jsonl, ESTATE_INDEX.jsonl}` only, else 404 `{error}` |
| GET | /mcp | inline :561-577 | `{ok, endpoint:"MCP over HTTP", method:"POST only", usage, tools:[names], count}`; live count 34 (section 8); 500 `{ok:false,error}` on import failure |
| GET | /chan /keep /b (+.html) | inline :580-584 | static/chan.html bytes, text/html + fleetbar |
| GET | /wave /desk (+.html) | inline :586-590 | static/wave.html bytes |
| GET | / /index.html | inline :592-595 | static/index.html bytes |
| GET | /shell (+.html) | inline :597-601 | static/sovereign_shell.html bytes |
| GET | /table /play /game (+.html) | inline :604-608 | static/wave.html bytes (aliases) |
| GET | /voice (+.html), /cast-voice.html | inline :611-615 | static/cast-voice.html bytes |
| GET | /seat (+.html) | inline :618-622 | static/seat.html bytes |
| GET | /fleet (+.html) | inline :625-629 | static/fleet.html bytes |
| GET | /health /health.html /loop-health | inline :632-636 | static/health.html bytes (page, not the JSON /api/v1/health) |
| GET | /aos (+.html) | inline :639-643 | static/aos.html bytes |
| GET | /static/* | inline :645-655 via `safe_file` :437-463 | file bytes by mimetype; HTML gets fleetbar injected unless ?embed=1 (:653-654); 404 `{error}` |
| GET | /files/* | inline :657-665 via `safe_file` (maps to memory/, blocks `..` traversal :439-455) | file bytes; PDF gets `Content-Disposition: inline` (:490); 404 `{error, path}` |
| GET | /api/v1/stream | `_stream_fleet` :926-949 | SSE text/event-stream, `data: {"type":"fleet","tasks":[...]}` every 2s from mag.orchestrator.list_tasks_live(limit=50) |
| GET | /api/v1/table/view, /api/table/view | inline :672-698 | table view dict via 4s subprocess `mag.table_view_cache` + 8s-fresh cache file; fallback `{ok:true, title, grid_text, error}` |
| GET | /api/dossier/latest | inline :718-720 | latest.dossier.json contents or `{error:"no latest dossier"}` |
| GET | /api/knot/latest | inline :722-724 | latest.knot.json contents or `{error:"no latest knot"}` |
| GET | /api/multi-smoke/latest | inline :726-732 | models.multi_smoke.last_smoke() or `{ok:false, error}` |
| GET | /api/usage-report | inline :734-769 | `{ok, local:{calls,tokens}, remote:{calls,tokens}, grok_tui, probe, note}` summed from logs/provider_usage.jsonl |
| GET | /api/probe-status | inline :771-781 | logs/probe_status_latest.json contents or `{ok:false, error}` |
| GET | /api/aos/chat | inline :785-797 | JSON from 8s subprocess `mag.aos_live_view --json`; 200 `{ok:false, error}` on failure |
| GET | /api/catch-up | inline :706-709 | re-dispatched as POST /api/v1/catch-up (deprecated GET form) |
| POST | /mcp | inline :825-839 | tools/list -> `{tools:[manifest]}`; tools/call -> tool result dict; unknown method 400; exception 500 |
| POST | /api/v1/agent/stream | `_stream_agent` :951-1023 | SSE events: `{type:"delta",text}`, `{type:"tool",name,args}`, `{type:"done",answer,tools,provider,model,session_id,tip,n_messages}`, `{type:"error",error}`; missing goal -> error event |
| POST | /api/v1/agent/steer | inline :844-856 | 200 `{ok:true, queued, cmd}` via mag.agent_cli.push_steer; 400 no cmd; 500 on exception |
| POST | /api/aos/send | inline :860-894 | JSON from 30s subprocess `mag.aos_live_view --send-file`; author forced to bone|operator; 400 no text |
| POST | /api/probe-status | inline :904-922 | runs scripts/probe_status_cache.py (180s timeout, CREATE_NO_WINDOW at :917) then returns logs/probe_status_latest.json |

Spawn-flag observation (win32): only the probe-status POST passes
`creationflags=CREATE_NO_WINDOW` (server.py:917); the three `subprocess.check_output`
sites (server.py:685, :790, :878) pass none and can flash console windows on win32.
rest.py's single spawn `_headless_run` (rest.py:365-376) carries
`CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` (rest.py:357-361).

## 4. rest.py ROUTES table (347 rows, v1 + shared legacy-dup paths)

Verbatim from the AST extraction. Shape column = static dict keys visible at the
handler's first `return <status>, {dict}` (or `_ok(data={...})`) position, extracted
by AST; "dynamic" = the handler builds its dict at runtime (99 handlers have no
static dict literal at any return position and no delegation; their shapes are
runtime data, not fabricated here). Auth = NONE for all rows (section 2).
Path params: `{id}` style. Statuses = every literal status the handler can return.

Group census (first path segment after /api/v1/):

- index: 27
- voice: 26
- agents: 17
- table: 8
- game: 7
- diary: 7
- ghost: 6
- ideas: 6
- skill-ledger: 5
- chan: 4
- rightsize: 4
- memory: 4
- sessions: 4
- agent: 4
- seats: 4
- power: 4
- governance: 4
- overseer: 4
- ecosystem: 3
- viewports: 3
- providers: 3
- blast: 3
- coordination: 3
- drainer: 3
- workspace: 3
- partner: 2
- fleet: 2
- tapestry: 2
- test-run: 2
- swarm: 2
- system-map: 2
- brain: 2
- feature-lab: 2
- arena: 2
- routing-network: 2
- local-scheduler: 2
- unsloth: 2
- refine: 2
- story: 2
- costs: 2
- brief: 2
- visual: 2
- desk-dialogue: 2
- agent-desk: 2
- tangent: 2
- fork: 2
- lifecycle: 2
- temperature-stacks: 2
- improve: 2
- token-chain: 2
- operator-inbox: 2
- route: 2
- decide: 2
- verkle-knots: 2
- coding-session: 2
- factory-machine: 2
- framework: 2
- janitor: 2
- orphan: 2
- failure: 2
- warnings: 2
- supervisor: 2
- handoff: 2
- aos-grok: 2
- research-lens: 2
- cheap-swarm: 2
- mycelium: 2
- republic-os: 2
- comms-trail: 2
- grok-mirror: 2
- legacy: 2
- law: 2
- steer: 2
- run: 2
- spec-gate: 2
- seat: 2
- elevate: 2
- cleanup: 2
- docker: 2
- embassy: 2
- live-feed: 2
- behavior: 2
- schemas: 1
- endpoints: 1
- pile: 1
- loop: 1
- operator-os: 1
- org-review: 1
- lattice-lab: 1
- health: 1
- web: 1
- doctor: 1
- tokens: 1
- sovereign: 1
- solved: 1
- afk: 1
- sentinel: 1
- mag-os: 1
- os: 1
- kpi: 1
- registry: 1
- board: 1
- chain: 1
- wave: 1
- desk: 1
- ingest: 1
- overview: 1
- hood: 1
- nervous: 1
- stack: 1
- repo-readiness: 1
- local-pulse: 1
- display: 1
- grove: 1
- lattice-history: 1
- home: 1
- summary: 1
- attention-ranked: 1
- attention-feedback: 1
- models: 1
- quota: 1
- router-status: 1
- status: 1
- usage: 1
- economy: 1
- compute-schedule: 1
- flow: 1
- catch-up: 1
- desk-orchestrate: 1
- ask: 1
- dispatch: 1
- context-pack: 1
- session: 1
- tangents: 1
- export: 1
- multi-smoke: 1
- probe-lanes: 1
- chronicle: 1
- seat-feed: 1
- coordinate: 1
- autorun: 1
- handoff-inbox: 1
- graph: 1
- surface-audit: 1
- grok-batch: 1
- extension: 1
- autopilot: 1
- orchestrator: 1
- thrash: 1

### ROUTES (rest.py:5079-5432)

| # | Method | Route | Handler (rest.py line) | Statuses | Response shape (static keys) |
|---|---|---|---|---|---|
| 1 | GET | `/api/v1/chan/catalog` | h_chan_catalog :4924 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 2 | GET | `/api/v1/chan/thread/{slug}` | h_chan_thread :4931 | 200,400 | ok, error |
| 3 | POST | `/api/v1/chan/post` | h_chan_post :4940 |  | dynamic (dict built at runtime, no static literal at return) |
| 4 | POST | `/api/v1/chan/wake` | h_chan_wake :4952 | 200,400 | ok, error |
| 5 | GET | `/api/v1/partner/puppet` | h_partner_puppet :4962 | 200,500 | ok, type, title, status, detail |
| 6 | POST | `/api/v1/partner/puppet` | h_partner_puppet_post :4972 | 200,422,500 | ok, type, title, status, detail |
| 7 | GET | `/api/v1/ecosystem` | h_ecosystem :260 | 200,500 | ok, error |
| 8 | GET | `/api/v1/ecosystem/rib` | h_ecosystem_rib :271 | 200,500 | ok, error |
| 9 | GET | `/api/v1/ecosystem/scan` | h_ecosystem_scan :281 | 200,500 | ok, error |
| 10 | GET | `/api/v1/schemas` | h_schemas :250 | 200,500 | ok, error |
| 11 | GET | `/api/v1/endpoints` | h_endpoints :4892 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 12 | GET | `/api/endpoints` | h_endpoints :4892 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 13 | GET | `/api/v1/rightsize` | h_rightsize :4825 | 200,500 | ok, registry |
| 14 | GET | `/api/v1/rightsize/endpoints` | h_rightsize_endpoints :4835 | 200,500 | ok, count, items |
| 15 | POST | `/api/v1/rightsize/audit` | h_rightsize_audit :4846 | 200,500 | ok, **rightsize_all.audit() |
| 16 | POST | `/api/v1/rightsize/apply` | h_rightsize_apply :4856 | 200,500 | ok, **rightsize_all.apply(dry=dry) |
| 17 | GET | `/api/v1/skill-ledger` | h_skill_ledger :4780 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 18 | GET | `/api/skill-ledger` | h_skill_ledger :4780 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 19 | POST | `/api/v1/skill-ledger/record` | h_skill_ledger_record :4786 | 200 | ok, recorded, progress |
| 20 | POST | `/api/skill-ledger/record` | h_skill_ledger_record :4786 | 200 | ok, recorded, progress |
| 21 | POST | `/api/v1/skill-ledger/labeled-row` | h_skill_ledger_labeled_row :4804 | 200 | ok, recorded, progress |
| 22 | POST | `/api/skill-ledger/labeled-row` | h_skill_ledger_labeled_row :4804 | 200 | ok, recorded, progress |
| 23 | GET | `/api/v1/pile` | h_pile :4819 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 24 | GET | `/api/pile` | h_pile :4819 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 25 | GET | `/api/v1/fleet/triad` | h_fleet_triad :167 | 200 | ok, triad |
| 26 | GET | `/api/v1/fleet/hypervisor` | h_fleet_hypervisor :176 | 200,500 | ok, ts, mermaid, seats, n_seats, n_available, accounts, active_lanes (+2 more) |
| 27 | GET | `/api/v1/loop/health` | _dl_loop_health |  | dynamic (dict built at runtime, no static literal at return) |
| 28 | GET | `/api/v1` | h_api_index :4663 | 200 | ok, name, version, product, primary, resources, conventions |
| 29 | GET | `/api/v1/` | h_api_index :4663 | 200 | ok, name, version, product, primary, resources, conventions |
| 30 | GET | `/api/v1/operator-os` | h_operator_os :4236 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 31 | GET | `/api/v1/org-review` | h_operator_os :4236 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 32 | GET | `/api/v1/tapestry` | h_tapestry :4242 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 33 | POST | `/api/v1/tapestry/rebuild` | h_post_tapestry :4251 |  | dynamic (dict built at runtime, no static literal at return) |
| 34 | GET | `/api/v1/lattice-lab` | h_lattice_lab :4255 | 200 | ok, instrument, role, mag_home, open_url, open_demo_url, start, preset (+6 more) |
| 35 | GET | `/api/v1/health` | h_health :105 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 36 | GET | `/api/v1/web/fetch` | h_web_fetch :123 | 200,400,502 | ok, error |
| 37 | GET | `/api/v1/doctor` | h_health :105 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 38 | GET | `/api/v1/test-run` | h_test_run :151 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 39 | POST | `/api/v1/test-run` | h_test_run :151 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 40 | GET | `/api/v1/tokens/saved` | h_tokens_saved :200 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 41 | GET | `/api/v1/game/score` | h_game_score :208 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 42 | GET | `/api/v1/ghost/control` | h_ghost_control :218 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 43 | GET | `/api/v1/sovereign` | h_sovereign :227 | 200,500 | ok, error |
| 44 | GET | `/api/v1/solved` | h_solved :239 | 200,500 | ok, error |
| 45 | POST | `/api/v1/ghost/talk` | h_ghost_talk :293 | 200,400,500 | ok, error |
| 46 | GET | `/api/v1/memory/search` | h_memory_search :335 | 200,400 | ok, error |
| 47 | GET | `/api/v1/memory/recent` | h_memory_recent :345 | 200 | ok, items |
| 48 | GET | `/api/v1/memory/{key}` | h_memory_get :309 | 200,400,404 | ok, memory |
| 49 | POST | `/api/v1/memory` | h_memory_put :321 | 200,400,500 | ok, error |
| 50 | POST | `/api/v1/swarm/ramp` | h_swarm_ramp :379 | 200 | delegates: _headless_run |
| 51 | POST | `/api/v1/swarm/test` | h_swarm_test :389 | 200 | delegates: _headless_run |
| 52 | POST | `/api/v1/afk/run` | h_afk_run :397 | 200 | delegates: _headless_run |
| 53 | POST | `/api/v1/sentinel` | h_sentinel :403 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 54 | GET | `/api/v1/mag-os` | h_mag_os :855 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 55 | GET | `/api/v1/os` | h_mag_os :855 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 56 | GET | `/api/v1/kpi` | h_kpi :2955 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 57 | GET | `/api/v1/registry` | h_registry :2961 | 200 | ok, count, sessions |
| 58 | GET | `/api/v1/sessions` | h_sessions :2968 | 200 | ok, count, sessions |
| 59 | GET | `/api/v1/sessions/{id}` | h_session :2975 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 60 | GET | `/api/v1/sessions/{id}/residual` | h_session_residual :2983 | 200,404 | ok, session_id, residual |
| 61 | GET | `/api/v1/sessions/{id}/visual` | h_visual :3690 | 200,404 | ok, error, session_id |
| 62 | GET | `/api/v1/board` | h_board :2993 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 63 | GET | `/api/v1/chain` | h_chain :2999 | 200 | ok, tip, chain, evolution, timeline |
| 64 | GET | `/api/v1/wave` | h_wave :3009 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 65 | GET | `/api/v1/desk` | h_wave :3009 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 66 | GET | `/api/v1/ingest` | h_ingest :3016 | 200 | ok, catalog, registry_tail |
| 67 | GET | `/api/v1/overview` | _dl_overview |  | dynamic (dict built at runtime, no static literal at return) |
| 68 | GET | `/api/v1/hood` | h_hood :3028 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 69 | GET | `/api/v1/nervous` | h_nervous :3035 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 70 | GET | `/api/nervous` | h_nervous :3035 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 71 | GET | `/api/v1/system-map` | h_system_map :3041 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 72 | POST | `/api/v1/system-map` | h_system_map :3041 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 73 | GET | `/api/v1/brain` | h_brain :3497 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 74 | POST | `/api/v1/brain` | h_brain :3497 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 75 | GET | `/api/brain` | h_brain :3497 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 76 | POST | `/api/brain` | h_brain :3497 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 77 | GET | `/api/v1/stack` | h_stack :3065 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 78 | GET | `/api/stack` | h_stack :3065 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 79 | GET | `/api/v1/repo-readiness` | h_repo_readiness :3079 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 80 | GET | `/api/v1/feature-lab` | h_feature_lab :3086 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 81 | POST | `/api/v1/feature-lab` | h_feature_lab :3086 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 82 | GET | `/api/v1/local-pulse` | h_local_pulse :3113 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 83 | GET | `/api/local-pulse` | h_local_pulse :3113 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 84 | GET | `/api/v1/arena` | h_agent_arena :3120 | 200,<dyn> | ok, **league_snapshot(game=_p.get('g |
| 85 | POST | `/api/v1/arena` | h_agent_arena :3120 | 200,<dyn> | ok, **league_snapshot(game=_p.get('g |
| 86 | GET | `/api/arena` | h_agent_arena :3120 | 200,<dyn> | ok, **league_snapshot(game=_p.get('g |
| 87 | POST | `/api/arena` | h_agent_arena :3120 | 200,<dyn> | ok, **league_snapshot(game=_p.get('g |
| 88 | GET | `/api/v1/routing-network` | h_routing_network :3149 | 200,<dyn> | ok, peers |
| 89 | POST | `/api/v1/routing-network` | h_routing_network :3149 | 200,<dyn> | ok, peers |
| 90 | GET | `/api/v1/local-scheduler` | h_local_scheduler :3096 | 200,400 | ok, error |
| 91 | POST | `/api/v1/local-scheduler` | h_local_scheduler :3096 | 200,400 | ok, error |
| 92 | GET | `/api/local-scheduler` | h_local_scheduler :3096 | 200,400 | ok, error |
| 93 | POST | `/api/local-scheduler` | h_local_scheduler :3096 | 200,400 | ok, error |
| 94 | GET | `/api/v1/unsloth` | h_unsloth :3463 | 200,400,<dyn> | ok, error |
| 95 | POST | `/api/v1/unsloth` | h_unsloth :3463 | 200,400,<dyn> | ok, error |
| 96 | GET | `/api/unsloth` | h_unsloth :3463 | 200,400,<dyn> | ok, error |
| 97 | POST | `/api/unsloth` | h_unsloth :3463 | 200,400,<dyn> | ok, error |
| 98 | POST | `/api/v1/voice/scratch` | h_voice_scratch :3232 | 200,400,500 | ok, error, speak_text |
| 99 | POST | `/api/voice/scratch` | h_voice_scratch :3232 | 200,400,500 | ok, error, speak_text |
| 100 | POST | `/api/v1/voice/turn` | h_voice_turn :3249 | 500,<dyn> | ok, error |
| 101 | POST | `/api/voice/turn` | h_voice_turn :3249 | 500,<dyn> | ok, error |
| 102 | GET | `/api/v1/voice/shadow` | h_voice_shadow :3260 | 500,<dyn> | ok, error |
| 103 | POST | `/api/v1/voice/shadow` | h_voice_shadow :3260 | 500,<dyn> | ok, error |
| 104 | GET | `/api/voice/shadow` | h_voice_shadow :3260 | 500,<dyn> | ok, error |
| 105 | POST | `/api/voice/shadow` | h_voice_shadow :3260 | 500,<dyn> | ok, error |
| 106 | GET | `/api/v1/voice/task` | h_voice_task :3271 | 500,<dyn> | ok, error |
| 107 | POST | `/api/v1/voice/task` | h_voice_task :3271 | 500,<dyn> | ok, error |
| 108 | GET | `/api/voice/task` | h_voice_task :3271 | 500,<dyn> | ok, error |
| 109 | POST | `/api/voice/task` | h_voice_task :3271 | 500,<dyn> | ok, error |
| 110 | GET | `/api/v1/voice/stt` | h_voice_stt :3286 | 200,500,<dyn> | ok, error, text |
| 111 | POST | `/api/v1/voice/stt` | h_voice_stt :3286 | 200,500,<dyn> | ok, error, text |
| 112 | GET | `/api/voice/stt` | h_voice_stt :3286 | 200,500,<dyn> | ok, error, text |
| 113 | POST | `/api/voice/stt` | h_voice_stt :3286 | 200,500,<dyn> | ok, error, text |
| 114 | GET | `/api/v1/voice/canvas` | h_voice_canvas :3310 | 500,<dyn> | ok, error |
| 115 | POST | `/api/v1/voice/canvas` | h_voice_canvas :3310 | 500,<dyn> | ok, error |
| 116 | GET | `/api/voice/canvas` | h_voice_canvas :3310 | 500,<dyn> | ok, error |
| 117 | POST | `/api/voice/canvas` | h_voice_canvas :3310 | 500,<dyn> | ok, error |
| 118 | GET | `/api/v1/voice/dig` | h_voice_canvas :3310 | 500,<dyn> | ok, error |
| 119 | POST | `/api/v1/voice/dig` | h_voice_canvas :3310 | 500,<dyn> | ok, error |
| 120 | GET | `/api/v1/diary/seal` | h_diary_seal :3327 | 500,<dyn> | ok, error |
| 121 | POST | `/api/v1/diary/seal` | h_diary_seal :3327 | 500,<dyn> | ok, error |
| 122 | GET | `/api/v1/diary/nodes` | h_diary_seal :3327 | 500,<dyn> | ok, error |
| 123 | POST | `/api/v1/diary/nodes` | h_diary_seal :3327 | 500,<dyn> | ok, error |
| 124 | GET | `/api/diary/seal` | h_diary_seal :3327 | 500,<dyn> | ok, error |
| 125 | POST | `/api/diary/seal` | h_diary_seal :3327 | 500,<dyn> | ok, error |
| 126 | GET | `/api/v1/voice/handoff` | h_voice_handoff :3344 | 500,<dyn> | ok, error |
| 127 | POST | `/api/v1/voice/handoff` | h_voice_handoff :3344 | 500,<dyn> | ok, error |
| 128 | GET | `/api/voice/handoff` | h_voice_handoff :3344 | 500,<dyn> | ok, error |
| 129 | POST | `/api/voice/handoff` | h_voice_handoff :3344 | 500,<dyn> | ok, error |
| 130 | GET | `/api/v1/refine` | h_refine_chain :3360 | 500,<dyn> | ok, error |
| 131 | POST | `/api/v1/refine` | h_refine_chain :3360 | 500,<dyn> | ok, error |
| 132 | GET | `/api/refine` | h_refine_chain :3360 | 500,<dyn> | ok, error |
| 133 | POST | `/api/refine` | h_refine_chain :3360 | 500,<dyn> | ok, error |
| 134 | GET | `/api/v1/game` | h_game :3374 | 500,<dyn> | ok, error |
| 135 | POST | `/api/v1/game` | h_game :3374 | 500,<dyn> | ok, error |
| 136 | GET | `/api/game` | h_game :3374 | 500,<dyn> | ok, error |
| 137 | POST | `/api/game` | h_game :3374 | 500,<dyn> | ok, error |
| 138 | GET | `/api/v1/game/frontier` | h_frontier_game :3425 | 200,500 | ok, error |
| 139 | POST | `/api/v1/game/frontier` | h_frontier_game :3425 | 200,500 | ok, error |
| 140 | GET | `/api/game/frontier` | h_frontier_game :3425 | 200,500 | ok, error |
| 141 | POST | `/api/game/frontier` | h_frontier_game :3425 | 200,500 | ok, error |
| 142 | GET | `/api/v1/table/view` | h_table_view :3392 | 200,500 | ok, error |
| 143 | POST | `/api/v1/table/view` | h_table_view :3392 | 200,500 | ok, error |
| 144 | GET | `/api/table/view` | h_table_view :3392 | 200,500 | ok, error |
| 145 | POST | `/api/table/view` | h_table_view :3392 | 200,500 | ok, error |
| 146 | GET | `/api/v1/table/tileset` | h_table_tileset :3450 | 200,500 | ok, error |
| 147 | POST | `/api/v1/table/tileset` | h_table_tileset :3450 | 200,500 | ok, error |
| 148 | GET | `/api/table/tileset` | h_table_tileset :3450 | 200,500 | ok, error |
| 149 | POST | `/api/table/tileset` | h_table_tileset :3450 | 200,500 | ok, error |
| 150 | GET | `/api/v1/display` | h_display :3053 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 151 | GET | `/api/display` | h_display :3053 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 152 | GET | `/api/v1/grove` | h_grove :3510 | 200 | ok, schema, nodes, count, build |
| 153 | GET | `/api/grove` | h_grove :3510 | 200 | ok, schema, nodes, count, build |
| 154 | GET | `/api/v1/lattice-history` | h_lattice_history :3531 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 155 | GET | `/api/lattice-history` | h_lattice_history :3531 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 156 | GET | `/api/v1/viewports` | h_viewports :3538 |  | dynamic (dict built at runtime, no static literal at return) |
| 157 | GET | `/api/v1/viewports/{id}` | h_viewport_one :3546 |  | dynamic (dict built at runtime, no static literal at return) |
| 158 | POST | `/api/v1/viewports/sync` | h_viewports_sync :3557 |  | dynamic (dict built at runtime, no static literal at return) |
| 159 | GET | `/api/v1/home` | h_home_summary :983 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 160 | GET | `/api/v1/summary` | h_home_summary :983 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 161 | GET | `/api/v1/attention-ranked` | h_attention_ranked :862 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 162 | POST | `/api/v1/attention-feedback` | h_attention_feedback :869 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 163 | GET | `/api/v1/ideas` | h_ideas :1355 |  | dynamic (dict built at runtime, no static literal at return) |
| 164 | POST | `/api/v1/ideas` | h_ideas_create :1417 |  | dynamic (dict built at runtime, no static literal at return) |
| 165 | GET | `/api/v1/ideas/{id}/pack` | h_idea_pack :1400 |  | dynamic (dict built at runtime, no static literal at return) |
| 166 | GET | `/api/v1/ideas/{id}` | h_idea_one :1372 |  | dynamic (dict built at runtime, no static literal at return) |
| 167 | PATCH | `/api/v1/ideas/{id}` | h_idea_patch :1443 |  | dynamic (dict built at runtime, no static literal at return) |
| 168 | POST | `/api/v1/ideas/seed` | h_ideas_seed :1473 |  | dynamic (dict built at runtime, no static literal at return) |
| 169 | GET | `/api/v1/models` | h_models :3565 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 170 | GET | `/api/v1/providers` | _dl_providers |  | dynamic (dict built at runtime, no static literal at return) |
| 171 | GET | `/api/v1/quota` | _dl_quota |  | dynamic (dict built at runtime, no static literal at return) |
| 172 | GET | `/api/v1/providers/local-only` | h_local_only_get :3583 |  | dynamic (dict built at runtime, no static literal at return) |
| 173 | POST | `/api/v1/providers/local-only` | h_local_only_post :3593 |  | dynamic (dict built at runtime, no static literal at return) |
| 174 | GET | `/api/v1/router-status` | h_router_status :1537 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 175 | GET | `/api/v1/status` | h_router_status :1537 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 176 | GET | `/api/v1/diary` | h_diary :1487 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 177 | GET | `/api/v1/story` | h_story :1499 | 200,500 | ok, error, schema |
| 178 | GET | `/api/v1/story/file` | h_story_file :1509 | 200,400,403,404,415,500 | ok, path, bytes, text |
| 179 | GET | `/api/v1/usage` | h_usage :3649 | 200 | ok, today, grok_escalations_today, grok_budget_max, tail, lanes |
| 180 | GET | `/api/v1/economy` | h_economy :3611 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 181 | GET | `/api/v1/costs` | h_costs :3624 | 200,500 | ok, schema, error |
| 182 | POST | `/api/v1/costs/vast/sync` | h_vast_cost_sync :3634 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 183 | GET | `/api/v1/compute-schedule` | h_compute_schedule :3642 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 184 | GET | `/api/v1/flow` | h_idea_flow :3670 | 200,500 | ok, error |
| 185 | GET | `/api/v1/brief` | h_brief_latest :3679 | 200 | ok, text, dir |
| 186 | GET | `/api/v1/visual/latest` | lambda -> h_visual(id=latest) |  | dynamic (dict built at runtime, no static literal at return) |
| 187 | POST | `/api/v1/catch-up` | h_post_catch_up :3706 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 188 | POST | `/api/v1/desk-orchestrate` | h_desk_orchestrate :3748 | 200,400 | ok, error |
| 189 | POST | `/api/v1/desk-dialogue` | h_desk_dialogue :3768 | 200 | ok, cursor, manual, user_model, trust, desk_api, local_model, local_role (+4 more) |
| 190 | GET | `/api/v1/desk-dialogue` | h_desk_dialogue :3768 | 200 | ok, cursor, manual, user_model, trust, desk_api, local_model, local_role (+4 more) |
| 191 | GET | `/api/v1/agent-desk` | h_agent_desk :3712 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 192 | POST | `/api/v1/agent-desk` | h_agent_desk :3712 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 193 | POST | `/api/v1/ask` | h_post_ask :3877 | 200,400 | ok, error |
| 194 | POST | `/api/v1/dispatch` | h_post_dispatch :3908 | 200,400,500 | ok, error |
| 195 | POST | `/api/v1/agent` | h_post_agent :3942 | 200,400,500 | ok, error |
| 196 | POST | `/api/agent` | h_post_agent :3942 | 200,400,500 | ok, error |
| 197 | GET | `/api/v1/agent/live` | h_agent_live :3934 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 198 | POST | `/api/v1/agent/upload` | h_post_agent_upload :3973 | 200,400 | ok, error |
| 199 | POST | `/api/agent/upload` | h_post_agent_upload :3973 | 200,400 | ok, error |
| 200 | GET | `/api/v1/context-pack` | h_context_pack :4039 | 200,500 | ok, text, paste, chars, path, tip |
| 201 | GET | `/api/context-pack` | h_context_pack :4039 | 200,500 | ok, text, paste, chars, path, tip |
| 202 | GET | `/api/v1/session/freeze` | h_session_freeze :4081 | 200,500 | ok, error |
| 203 | GET | `/api/v1/tangents` | h_tangents :4097 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 204 | POST | `/api/v1/tangent` | h_post_tangent :4148 | 200,400 | ok, error |
| 205 | POST | `/api/v1/tangent/process` | h_post_tangent_process :4176 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 206 | POST | `/api/v1/fork/detect` | h_fork_detect :4103 | 200,400 | ok, error |
| 207 | POST | `/api/v1/fork/confirm` | h_fork_confirm :4116 | 400,<dyn> | ok, error |
| 208 | POST | `/api/v1/brief` | h_post_brief :4185 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 209 | POST | `/api/v1/visual` | h_post_visual :4194 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 210 | POST | `/api/v1/export` | h_post_export :4202 | 400,<dyn> | ok, error |
| 211 | POST | `/api/v1/multi-smoke` | h_post_multi_smoke :4223 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 212 | POST | `/api/v1/probe-lanes` | h_post_probe_lanes :4229 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 213 | GET | `/api/v1/blast` | h_blast :4299 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 214 | POST | `/api/v1/blast` | h_post_blast :4305 | 200,400 | ok, error |
| 215 | POST | `/api/v1/blast/promote` | h_post_blast_promote :4349 | 200,400 | ok, error |
| 216 | GET | `/api/v1/agents` | h_agents :4364 | 200 | ok, tasks, count, scope, archived_hidden, layman |
| 217 | POST | `/api/v1/agents` | h_agents_spawn :4398 | 200,400,500 | ok, error |
| 218 | POST | `/api/v1/agents/fan` | h_agents_fan :4420 | 400,500,<dyn> | ok, error |
| 219 | GET | `/api/v1/agents/pipes` | h_agents_pipes :4589 | 200 | ok, pipes |
| 220 | GET | `/api/v1/agents/pipes/{id}` | h_agents_pipe_one :4595 | 200,404 | ok, pipe |
| 221 | POST | `/api/v1/agents/pipes/{id}/collect` | h_agents_pipe_collect :4605 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 222 | POST | `/api/v1/agents/pipes/{id}/kill` | h_agents_pipe_kill :4621 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 223 | POST | `/api/v1/agents/pipes/{id}/cmd` | h_agents_pipe_cmd :4629 | 400,404,<dyn> | ok, error |
| 224 | POST | `/api/v1/agents/reap` | h_agents_reap :4473 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 225 | POST | `/api/v1/agents/heal` | h_agents_heal :4479 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 226 | GET | `/api/v1/agents/{id}` | h_agent_one :4445 | 200,404 | ok, task |
| 227 | GET | `/api/v1/agents/{id}/state-snapshot` | h_agent_state_snapshot :4507 | 200 | ok, schema, data |
| 228 | GET | `/api/v1/agents/{id}/log` | h_agent_log :4462 | 200 | ok, log |
| 229 | POST | `/api/v1/agents/{id}/kill` | h_agent_kill :4455 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 230 | POST | `/api/v1/agents/{id}/cmd` | h_agent_cmd :4486 | 200,400 | ok, error |
| 231 | POST | `/api/v1/agents/{id}/steer` | h_agent_steer_post :4530 | 200 | ok, schema, data |
| 232 | GET | `/api/v1/agents/{id}/steer/{steer_id}/status` | h_agent_steer_status :4564 | 200 | ok, schema, data |
| 233 | GET | `/api/v1/chronicle` | h_chronicle :414 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 234 | GET | `/api/v1/seats` | h_seats :421 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 235 | POST | `/api/v1/seats/register` | h_seats_register :431 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 236 | POST | `/api/v1/seats/heartbeat` | h_seats_heartbeat :457 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 237 | POST | `/api/v1/seats/unregister` | h_seats_unregister :474 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 238 | GET | `/api/v1/power` | h_power :487 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 239 | POST | `/api/v1/power/stop` | h_power_stop :493 | 200 | ok, action, hint |
| 240 | POST | `/api/v1/power/start` | h_power_start :511 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 241 | GET | `/api/v1/lifecycle` | h_lifecycle :519 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 242 | POST | `/api/v1/lifecycle/reconcile` | h_lifecycle_reconcile :526 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 243 | GET | `/api/v1/power/lifecycle` | h_lifecycle :519 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 244 | GET | `/api/v1/temperature-stacks` | h_temperature_stacks :535 | 200 | ok, stack, sampling, timeout_s |
| 245 | POST | `/api/v1/temperature-stacks` | h_temperature_stacks :535 | 200 | ok, stack, sampling, timeout_s |
| 246 | POST | `/api/v1/improve/cloud` | h_improve_cloud :579 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 247 | POST | `/api/v1/improve/cycle` | h_improve_cycle :603 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 248 | GET | `/api/v1/token-chain` | h_token_chain :619 | 200,<dyn> | ok, latest, hint |
| 249 | POST | `/api/v1/token-chain` | h_token_chain :619 | 200,<dyn> | ok, latest, hint |
| 250 | GET | `/api/v1/governance` | h_governance :645 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 251 | POST | `/api/v1/governance` | h_post_governance :651 | 200 | ok, **broadcast_steer(cmd) |
| 252 | POST | `/api/v1/governance/auto-steer/add` | h_governance_auto_steer_add :678 | 200 | ok, schema, data |
| 253 | GET | `/api/v1/governance/steering-log` | h_governance_steering_log :712 | 200 | ok, schema, data |
| 254 | GET | `/api/v1/overseer/manifest` | h_overseer_manifest :771 | 200 | ok, schema, data |
| 255 | GET | `/api/v1/overseer/events` | h_overseer_events :723 | 200 | ok, schema, data |
| 256 | GET | `/api/v1/overseer/session` | h_overseer_session :754 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 257 | POST | `/api/v1/overseer/session` | h_overseer_session :754 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 258 | GET | `/api/v1/operator-inbox` | h_operator_inbox :841 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 259 | POST | `/api/v1/operator-inbox` | h_operator_inbox :841 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 260 | GET | `/api/v1/seat-feed` | h_seat_feed :1789 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 261 | GET | `/api/v1/coordination` | h_coordination :1799 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 262 | POST | `/api/v1/coordination` | h_coordination_post :1812 | 200 | ok, activity |
| 263 | POST | `/api/v1/coordination/gather` | h_coordination_gather :1830 | 200 | ok, schema, data |
| 264 | POST | `/api/v1/coordinate` | h_coordinate :1951 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 265 | POST | `/api/v1/route` | h_route :1862 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 266 | GET | `/api/v1/route` | h_route :1862 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 267 | POST | `/api/v1/decide` | h_decide :1937 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 268 | GET | `/api/v1/decide` | h_decide :1937 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 269 | GET | `/api/v1/verkle-knots/{id}` | h_verkle_knot :1907 | 200,404,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 270 | POST | `/api/v1/verkle-knots/{id}` | h_verkle_knot :1907 | 200,404,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 271 | GET | `/api/v1/autorun` | h_autorun :1978 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 272 | GET | `/api/autorun` | h_autorun :1978 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 273 | GET | `/api/v1/handoff-inbox` | h_handoff_inbox :1985 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 274 | GET | `/api/handoff-inbox` | h_handoff_inbox :1985 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 275 | GET | `/api/v1/coding-session` | h_coding_session_get :2030 |  | dynamic (dict built at runtime, no static literal at return) |
| 276 | POST | `/api/v1/coding-session` | h_coding_session :1993 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 277 | GET | `/api/v1/factory-machine` | h_factory_machine_get :2063 |  | dynamic (dict built at runtime, no static literal at return) |
| 278 | POST | `/api/v1/factory-machine` | h_factory_machine :2034 | 200,<dyn> | dynamic (dict built at runtime, no static literal at return) |
| 279 | GET | `/api/v1/drainer` | h_drainer_status :2067 | 200 | ok, **st |
| 280 | POST | `/api/v1/drainer` | h_drainer_toggle :2766 | 200 | ok, drainer, hint |
| 281 | GET | `/api/v1/drainer/stats` | h_drainer_stats :2082 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 282 | GET | `/api/v1/graph/ops` | h_ops_graph :2089 | 200,500 | ok, error |
| 283 | GET | `/api/v1/framework/map` | h_framework_map :2099 | 200,500 | ok, error |
| 284 | GET | `/api/v1/framework/reports` | h_framework_reports :2109 | 200,500 | ok, reports |
| 285 | GET | `/api/v1/surface-audit` | h_surface_audit :2123 | 200,500 | ok, error |
| 286 | GET | `/api/v1/janitor` | h_janitor :2133 | 200,500 | ok, report |
| 287 | POST | `/api/v1/janitor` | h_janitor :2133 | 200,500 | ok, report |
| 288 | GET | `/api/v1/orphan` | h_orphan :2151 | 200,500 | ok, schema, open, n_open |
| 289 | POST | `/api/v1/orphan` | h_orphan :2151 | 200,500 | ok, schema, open, n_open |
| 290 | GET | `/api/v1/failure` | h_failure :2175 | 200,500 | ok, schema, logged |
| 291 | POST | `/api/v1/failure` | h_failure :2175 | 200,500 | ok, schema, logged |
| 292 | GET | `/api/v1/warnings` | h_warnings :2211 | 200,500 | ok, error |
| 293 | POST | `/api/v1/warnings` | h_warnings :2211 | 200,500 | ok, error |
| 294 | GET | `/api/v1/supervisor` | h_supervisor :2229 | 200,500 | ok, error |
| 295 | POST | `/api/v1/supervisor` | h_supervisor :2229 | 200,500 | ok, error |
| 296 | POST | `/api/v1/handoff/deep` | h_handoff_deep :2283 | 200,500 | ok, error |
| 297 | GET | `/api/v1/grok-batch` | h_grok_batch :2304 | 200 | ok, schema, buffers, results, path |
| 298 | GET | `/api/v1/aos-grok` | h_aos_grok :2321 | 200,500 | ok, error |
| 299 | POST | `/api/v1/aos-grok` | h_aos_grok :2321 | 200,500 | ok, error |
| 300 | GET | `/api/v1/research-lens` | h_research_lens :2342 | 200,500 | ok, error |
| 301 | POST | `/api/v1/research-lens` | h_research_lens :2342 | 200,500 | ok, error |
| 302 | GET | `/api/v1/cheap-swarm` | h_cheap_swarm :2376 | 200,500 | ok, error |
| 303 | POST | `/api/v1/cheap-swarm` | h_cheap_swarm :2376 | 200,500 | ok, error |
| 304 | GET | `/api/v1/mycelium` | h_mycelium :2401 | 200,500 | ok, error |
| 305 | POST | `/api/v1/mycelium` | h_mycelium :2401 | 200,500 | ok, error |
| 306 | GET | `/api/v1/republic-os` | h_republic_os :2430 | 200,500 | ok, error |
| 307 | POST | `/api/v1/republic-os` | h_republic_os :2430 | 200,500 | ok, error |
| 308 | GET | `/api/v1/comms-trail` | h_comms_trail :2458 | 200,500 | ok, error |
| 309 | POST | `/api/v1/comms-trail` | h_comms_trail :2458 | 200,500 | ok, error |
| 310 | GET | `/api/v1/grok-mirror` | h_grok_mirror :2477 | 200,500 | ok, error |
| 311 | POST | `/api/v1/grok-mirror` | h_grok_mirror :2477 | 200,500 | ok, error |
| 312 | GET | `/api/v1/ghost` | h_ghost :2503 | 200,500 | ok, summary |
| 313 | POST | `/api/v1/ghost` | h_ghost :2503 | 200,500 | ok, summary |
| 314 | GET | `/api/v1/ghost/summon` | h_ghost_summon :2558 | 200,500 | ok, error |
| 315 | POST | `/api/v1/ghost/summon` | h_ghost_summon :2558 | 200,500 | ok, error |
| 316 | GET | `/api/v1/legacy` | h_legacy_audit :2572 | 200,500 | ok, error |
| 317 | POST | `/api/v1/legacy` | h_legacy_audit :2572 | 200,500 | ok, error |
| 318 | GET | `/api/v1/law` | h_law :2525 | 200,500 | ok, error |
| 319 | POST | `/api/v1/law` | h_law :2525 | 200,500 | ok, error |
| 320 | GET | `/api/v1/steer` | h_steer :2541 | 200,500 | ok, error |
| 321 | POST | `/api/v1/steer` | h_steer :2541 | 200,500 | ok, error |
| 322 | GET | `/api/v1/run` | h_run :2590 | 200,500 | ok, error |
| 323 | POST | `/api/v1/run` | h_run :2590 | 200,500 | ok, error |
| 324 | GET | `/api/v1/spec-gate` | h_spec_gate :2610 | 200,500 | ok, error |
| 325 | POST | `/api/v1/spec-gate` | h_spec_gate :2610 | 200,500 | ok, error |
| 326 | POST | `/api/v1/extension/deploy` | h_extension_deploy :2627 | 200,500 | ok, error |
| 327 | POST | `/api/v1/seat/steer` | h_seat_steer :2637 | 200,400,500 | ok, error |
| 328 | GET | `/api/v1/elevate` | h_elevate :2694 | 200,500 | ok, error |
| 329 | POST | `/api/v1/elevate` | h_elevate :2694 | 200,500 | ok, error |
| 330 | GET | `/api/v1/cleanup` | h_cleanup :2677 | 200,500 | ok, error |
| 331 | POST | `/api/v1/cleanup` | h_cleanup :2677 | 200,500 | ok, error |
| 332 | GET | `/api/v1/docker` | h_docker :2264 | 200,500 | ok, error |
| 333 | POST | `/api/v1/docker` | h_docker :2264 | 200,500 | ok, error |
| 334 | GET | `/api/v1/embassy/publish` | h_embassy_publish :2715 | 500 | ok, error |
| 335 | POST | `/api/v1/embassy/publish` | h_embassy_publish :2715 | 500 | ok, error |
| 336 | GET | `/api/v1/live-feed` | h_live_feed :2734 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 337 | POST | `/api/v1/live-feed` | h_live_feed :2734 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 338 | GET | `/api/v1/workspace/tree` | h_workspace_tree :2778 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 339 | GET | `/api/v1/workspace/file` | h_workspace_file_get :2789 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 340 | POST | `/api/v1/workspace/file` | h_workspace_file_post :2799 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 341 | POST | `/api/v1/autopilot` | h_autopilot :2810 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 342 | POST | `/api/v1/orchestrator/queue` | h_orchestrator_queue_post :2823 | 200 | ok, **rec |
| 343 | POST | `/api/v1/handoff/request` | h_handoff_request_post :2844 | 200 | ok, schema, id, file, note |
| 344 | GET | `/api/v1/behavior/vscode` | h_vscode_feed :2886 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 345 | POST | `/api/v1/behavior/vscode` | h_vscode_feed :2886 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 346 | GET | `/api/v1/thrash` | h_thrash :5058 |  | dynamic (dict built at runtime, no static literal at return) |
| 347 | POST | `/api/v1/seat/task` | h_seat_task :2906 | <dyn> | dynamic (dict built at runtime, no static literal at return) |

## 5. rest.py LEGACY alias table (64 rows, rest.py:5435-5500)

All legacy bare `/api/*` aliases point at the same handlers as v1 (rest.py:5435
comment). Two rows are inline lambdas: /api/visual/latest -> h_visual(id=latest)
(:5466) and /api/timeline -> direct `_read_jsonl(knot_timeline.jsonl)` returning
`{rows:[...]}` (:5468).

| # | Method | Route | Handler (rest.py line) | Statuses | Response shape (static keys) |
|---|---|---|---|---|---|
| 1 | GET | `/api/operator-os` | h_operator_os :4236 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 2 | GET | `/api/org-review` | h_operator_os :4236 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 3 | GET | `/api/thrash` | h_thrash :5058 |  | dynamic (dict built at runtime, no static literal at return) |
| 4 | GET | `/api/health` | h_health :105 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 5 | GET | `/api/doctor` | h_health :105 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 6 | GET | `/api/mag-os` | h_mag_os :855 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 7 | GET | `/api/os` | h_mag_os :855 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 8 | GET | `/api/sessions` | h_sessions :2968 | 200 | ok, count, sessions |
| 9 | GET | `/api/session/{id}` | h_session :2975 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 10 | GET | `/api/board` | h_board :2993 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 11 | GET | `/api/verkle` | h_chain :2999 | 200 | ok, tip, chain, evolution, timeline |
| 12 | GET | `/api/ingest` | h_ingest :3016 | 200 | ok, catalog, registry_tail |
| 13 | GET | `/api/overview` | _dl_overview |  | dynamic (dict built at runtime, no static literal at return) |
| 14 | GET | `/api/hood` | h_hood :3028 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 15 | GET | `/api/home` | h_home_summary :983 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 16 | GET | `/api/diary` | h_diary :1487 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 17 | GET | `/api/story` | h_story :1499 | 200,500 | ok, error, schema |
| 18 | GET | `/api/summary` | h_home_summary :983 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 19 | GET | `/api/models` | h_models :3565 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 20 | GET | `/api/providers` | _dl_providers |  | dynamic (dict built at runtime, no static literal at return) |
| 21 | GET | `/api/quota` | _dl_quota |  | dynamic (dict built at runtime, no static literal at return) |
| 22 | GET | `/api/status` | h_status :5033 | 200 | ok, schema, service, time, checks, dark |
| 23 | GET | `/api/loop-health` | _dl_loop_health |  | dynamic (dict built at runtime, no static literal at return) |
| 24 | GET | `/api/usage` | h_usage :3649 | 200 | ok, today, grok_escalations_today, grok_budget_max, tail, lanes |
| 25 | GET | `/api/economy` | h_economy :3611 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 26 | GET | `/api/costs` | h_costs :3624 | 200,500 | ok, schema, error |
| 27 | POST | `/api/costs/vast/sync` | h_vast_cost_sync :3634 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 28 | GET | `/api/compute-schedule` | h_compute_schedule :3642 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 29 | GET | `/api/idea-flow` | h_idea_flow :3670 | 200,500 | ok, error |
| 30 | GET | `/api/brief/latest` | h_brief_latest :3679 | 200 | ok, text, dir |
| 31 | GET | `/api/visual/latest` | lambda -> h_visual(id=latest) |  | dynamic (dict built at runtime, no static literal at return) |
| 32 | GET | `/api/visual/{id}` | h_visual :3690 | 200,404 | ok, error, session_id |
| 33 | GET | `/api/timeline` | lambda -> _read_jsonl timeline |  | dynamic (dict built at runtime, no static literal at return) |
| 34 | POST | `/api/catch-up` | h_post_catch_up :3706 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 35 | POST | `/api/ask` | h_post_ask :3877 | 200,400 | ok, error |
| 36 | POST | `/api/dispatch` | h_post_dispatch :3908 | 200,400,500 | ok, error |
| 37 | GET | `/api/tangents` | h_tangents :4097 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 38 | POST | `/api/tangent` | h_post_tangent :4148 | 200,400 | ok, error |
| 39 | POST | `/api/tangent/process` | h_post_tangent_process :4176 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 40 | POST | `/api/fork/detect` | h_fork_detect :4103 | 200,400 | ok, error |
| 41 | POST | `/api/fork/confirm` | h_fork_confirm :4116 | 400,<dyn> | ok, error |
| 42 | POST | `/api/brief` | h_post_brief :4185 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 43 | POST | `/api/visual/rebuild` | h_post_visual :4194 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 44 | POST | `/api/export` | h_post_export :4202 | 400,<dyn> | ok, error |
| 45 | POST | `/api/multi-smoke` | h_post_multi_smoke :4223 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 46 | POST | `/api/probe-lanes` | h_post_probe_lanes :4229 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 47 | GET | `/api/blast` | h_blast :4299 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 48 | POST | `/api/blast` | h_post_blast :4305 | 200,400 | ok, error |
| 49 | POST | `/api/blast/promote` | h_post_blast_promote :4349 | 200,400 | ok, error |
| 50 | GET | `/api/chronicle` | h_chronicle :414 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 51 | GET | `/api/seats` | h_seats :421 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 52 | GET | `/api/governance` | h_governance :645 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 53 | POST | `/api/governance` | h_post_governance :651 | 200 | ok, **broadcast_steer(cmd) |
| 54 | GET | `/api/operator-inbox` | h_operator_inbox :841 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 55 | POST | `/api/operator-inbox` | h_operator_inbox :841 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 56 | GET | `/api/seat-feed` | h_seat_feed :1789 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 57 | GET | `/api/drainer` | h_drainer_status :2067 | 200 | ok, **st |
| 58 | POST | `/api/drainer` | h_drainer_toggle :2766 | 200 | ok, drainer, hint |
| 59 | GET | `/api/workspace/tree` | h_workspace_tree :2778 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 60 | GET | `/api/workspace/file` | h_workspace_file_get :2789 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 61 | POST | `/api/workspace/file` | h_workspace_file_post :2799 | <dyn> | dynamic (dict built at runtime, no static literal at return) |
| 62 | POST | `/api/autopilot` | h_autopilot :2810 | 200 | dynamic (dict built at runtime, no static literal at return) |
| 63 | POST | `/api/orchestrator/queue` | h_orchestrator_queue_post :2823 | 200 | ok, **rec |
| 64 | POST | `/api/seat/task` | h_seat_task :2906 | <dyn> | dynamic (dict built at runtime, no static literal at return) |

## 6. Shape-coverage census (rows, not handlers)

- Rows with static keys at first return: 231
- Rows whose only static trace is delegation to another handler: 3
- Rows fully dynamic at return: 177
- Self-description: the repo ships its own per-endpoint one-liner index:
  `GET /api/v1/endpoints` (h_endpoints rest.py:4892-4921, schema endpoints.v1) derives
  `{method, path, summary(docstring first line), group, version}` per row at request
  time, and `GET /api/v1` (h_api_index rest.py:4663-4776) hand-lists ~100 primary
  resources with descriptions. Both live-verified below. This census treats those
  summaries as the repo's claims; the key lists above are this session's own AST
  reads.
- The one PATCH in the estate: PATCH /api/v1/ideas/{id} -> h_idea_patch (rest.py:5248,
  handler :1443); server.py do_PATCH :1025-1039 is its only entry.

## 7. Live probe log (curl against 127.0.0.1:8765, 2026-09-28 ~23:29 UTC)

Read-only GETs + OPTIONS only; no state-changing POST was executed.

| Probe | Command | Result |
|---|---|---|
| health | `curl -s /api/v1/health` | 200 `{ok, status:"up", ts, integral:{heartbeat,pid_alive,port_8765,board_api,port_8000,backend_api,up}, recording:{...}, lanes:{L0_ollama(ok, 16 models), L1_openrouter, L2_grok}, gaps[], reconnect{...}, hallucination_guard{...}}` |
| endpoints | `curl -s /api/v1/endpoints` | 200 `{ok, schema:"endpoints.v1", count:411, items:[411 x {method,path,summary,group,version}]}` - count matches AST exactly |
| endpoints paging | `curl -s -i '/api/v1/endpoints?limit=2'` | 200 + `next: /api/v1/endpoints?cursor=2`; headers show `Server: MagDashboard/1.0 Python/3.12.14`, `Cache-Control: no-store`, no auth scheme, no WWW-Authenticate |
| OPTIONS | `curl -i -X OPTIONS /api/v1/health` | 204 with `Access-Control-Allow-Origin: *`, methods GET/POST/PATCH/OPTIONS |
| unknown route | `curl /api/v1/zzz-no-such-route` | 404; body shape `{error:"not found", path}` (server.py:799) |
| mcp info | `curl /mcp` | 200 `{ok, endpoint, method:"POST only", usage, tools:[...], count:34}` - the server.py:821 comment says "17 tools", live manifest has 34 (stale comment) |
| chan catalog | `curl /api/v1/chan/catalog` | 200 `{ok, schema:"chan.v1", board:"keep", count:18, threads:[...]}` |
| ractor tail | `curl '/api/v1/ractor/tail?limit=1'` | 200 `{rows:[...], truncated, bytes_read}` |
| links tail | `curl '/api/v1/links/tail?limit=1'` | **404 `{error:"not found", path:"/api/v1/links/tail"}`** - DRIFT: HEAD server.py:529-535 defines it; the running process started 09-25, FW-45 (d90bc8607) landed 09-28 15:09 EDT and Q-028's own receipt notes it was live-verified on a throwaway :18799 server with "operator :8765 untouched". This probe confirms the operator desk still lacks the door. |
| ideas | `curl /api/v1/ideas` | 200 `{ok, schema:"idea_graph.v0", n_nodes:43, n_edges:34, by_type{...}, by_status{...}, paths{...}}` |
| pile | `curl /api/v1/pile` | 200 `{ok, schema:"state_snapshot.v1", pile:144, classified:144, unclassified:0, by_kind{...}, by_outcome{...}}` |
| cost | `curl /api/v1/cost` | 200 `{schema:"cost_surface.v1", truth:{...cost_truth.v1...}, enforcer, overlay}` |
| v1 index | `curl /api/v1` | 200 `{ok, name, version, product, primary{...}, resources{...}, conventions{...}}` |
| overview deadline | `curl -w %{http_code},%{time_total} /api/overview` | **503 in 5.32s** - the `_dl` 5s deadline (rest.py:5004-5024) firing as designed; body `{ok:false, stale:true, error:"timeout", last_known:null}` shape |
| sessions (slow) | `curl /api/v1/sessions` at 20s, 90s, then `-w` at 30s | **no response, curl exit 28 (timeout), 0 bytes all three**. Handler h_sessions (rest.py:2968-2972) imports server.list_sessions() (server.py:115-288: registry scan + BIO globs + per-session find_derived). Live 8765 has never answered this inside 30s today. |
| agents (slow) | `curl /api/v1/agents` at 15s, 30s | **no response, curl exit 28, 0 bytes both**. h_agents (rest.py:4364) same class of live scan. |

## 8. Method and table census (cross-footed)

- All rows: 239 GET + 171 POST + 1 PATCH = 411
- ROUTES: 197 GET + 149 POST + 1 PATCH = 347
- LEGACY: 42 GET + 22 POST = 64
- Distinct paths (ROUTES + LEGACY union): 323 (264 in ROUTES incl /api/v1/ideas/{id}/pack, 59 legacy-only; zero path overlap between tables - verified by set intersection)
- Distinct named handlers: 234 (+3 lambdas); one handler can serve many routes
  (e.g. h_diary_seal serves 6 rows, h_game 4, h_brain 4)
- Cross-foot 1: AST row count 411 == live `/api/v1/endpoints` count 411
- Cross-foot 2: AST distinct paths 323 == regex pass 322 + the 1 row (rest.py:5246)
  the regex dropped (trailing comment `# before {id}`)

## 9. OWED / not run

- Response shapes for the 99 dynamic handlers are reported as "dynamic": extracting
  them would require executing each handler against live state; not done. No shape
  in this file is invented.
- No mutating POST was live-fired (power/stop, agents spawn, MCP tools/call etc.):
  their server-side behavior is cited from code lines only.
- The two hanging GETs (sessions, agents) were not diagnosed to root cause; three
  and two timeout probes respectively are the recorded evidence.
- The operator desk (PID 14308) predates today's FW-45 server.py; restarting it is
  an operator call, not taken by this census.

## Files

- This map banked byte-identical as `watch/inbox/burn_reset_20260927/flash50/api-endpoint-map.md`
  and `watch/inbox/burn_reset_20260927/flash50/s2-18.md`.
- Scratch (repo root, deletable): `_s218_extract.py`, `_s218_routes.json`,
  `_s218_build.py`, `_s218_endpoints_live.json`.
