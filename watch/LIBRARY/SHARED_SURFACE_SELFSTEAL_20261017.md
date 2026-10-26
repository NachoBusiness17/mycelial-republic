# SHARED SURFACE SELF-STEAL — one MCP door for every seat (2026-10-17)

Classification: CARD (read-only inventory + wiring proposal). No code written.
Producer: Grok Bot executor, 2026-10-17 ~14:30–15:10 ET (UTC-4).
Survey method: filename + rg sweeps (watch\inbox searched by name/targeted rg only),
file headers, Get-NetTCPConnection, netsh portproxy show, Get-ScheduledTask. No git, no docker
commands, no .env/keys/steps.jsonl/secret_gate_results/free_keys opened, nothing restarted.

## HEADLINE

The wheel is already built, three times over. The estate has a working stdlib MCP server
(`mag/mcp_server.py`), an always-on containerised copy of it on `127.0.0.1:8766`, a
streamable-HTTP adapter (`mag/mcp_http.py`), a seed server that already speaks MCP
**resources** (`tools/seed_mcp.py`), a receipt writer already registered as an MCP tool
(`estate_receipt_append`), and a daily-regenerated warm pack (`MagBootRegenDaily` ->
`warm_state.json` + `rib_boot.json` + `zknot/LATEST.md`). What is missing is not an
organ but a **profile + three resource URIs + client config lines**.

No seat client config currently points at any of it (checked `.gemini\settings.json`,
`.codex\config.toml`, repo `.claude\settings.json`; no `.cursor/mcp.json`, `.vscode/mcp.json`,
or Claude Desktop config exist).

## ORGAN LIST

Live = recent mtime AND (listener up OR scheduled task OR compose service). Times ET.

### A. MCP servers / transports

| Organ | What it does | Live? | Entrypoint / port |
|---|---|---|---|
| `mag/mcp_server.py` (500L, 2026-10-01) | Hand-rolled stdlib MCP over stdio serving `tools.TOOL_MAP`; role profiles (archivist/scout/builder/.../`bridge`) at L67-125; pin-gate on every tools/list (L21-33, L341). Handles only `initialize`, `ping`, `tools/list`, `tools/call` (L471-506) — **no resources/prompts**. | YES (via container below; `state/mcp_pins.jsonl` 11 MB, last_seen 2026-10-15 21:06) | `python -m mag.mcp_server [--profile X]` |
| `scripts/container/mcp_tcp_bridge.py` (107L) | Spawns one `mag.mcp_server` per TCP client; loopback law. | YES — compose service `mcp` / `mag-mcp` (docker-compose.yml L373-434), profile **archivist**; host listener `127.0.0.1:8766` owned by com.docker.backend at survey time | TCP `127.0.0.1:8766` (raw newline JSON-RPC, not HTTP) |
| `mag/mcp_http.py` (38L) | Streamable-HTTP `POST /mcp` on the `api_gateway` registry; inherits X-API-Key gate. | NOT LISTENING — mounted by `mag/api_server.py` L33 on port 8001; nothing bound to 8001 at survey | `POST http://127.0.0.1:8001/mcp` (when up) |
| `dashboard/server.py` /mcp | GET info page (L834-845) + POST tools/list / tools/call (L1095-1116) using mcp_server + pin gate. | NOT REACHABLE — see 8765 note below | `:8765/mcp` |
| `tools/seed_mcp.py` (336L, 09-29) | MCP server with **resources** `seed://current`, `seed://law-registry`, `seed://brief-pointers` (L82-108) + tools rebuild_subtree / verify_hash / fetch_bounded_pointer / join_protocol (7-step cold join, L204-232). Handles resources/list + resources/read (L320-330). | BUILT + FALSIFIED (10/10 cold join, `memory/continuity/seat_memory_20260927/seed-mcp-server-landed-20260926.md`); not wired to any client; seed pointer `watch/inbox/SEED_RIB_CURRENT` frozen 09-29 | `.venv\Scripts\python.exe tools/seed_mcp.py` (stdio) |
| `tools/seed_mcp_cold_client.py` (09-26) | Reference cold client for seed_mcp. | test asset | stdio |
| `mag/estate_bridge.py` (10-01) | 7 estate verbs as TOOL_MAP entries, incl. `estate_chain_verify` (DRY only) and **`estate_receipt_append`** (`receipt_append(wave,name,payload)` L490; writes only under `watch/inbox/<wave>/`, rotates existing to .bak, never touches INDEX.json); `_redact` L322. | registered; served by `--profile bridge` | via mcp_server |
| `tools/gps_mcp/` (server.py 10-05, router 812L, ledger 823L) | Capability-ledger router: ask / cascade / record_verdict / report_capability over SQLite; JSON-RPC "gps_mcp dialect" (no MCP handshake — README L187-209). | ledger live (`gps_ledger.db3` mounted into the mag container, compose L75-81; dashboard reads it, `dashboard/server.py` L107-162) | `python -m tools.gps_mcp.server` (stdio) |
| `tools/mesh_delta.py` (25.8 KB, 10-09) | **The "MCP torrent server", already built**: content-addressed snapshot of memory/ (sha256/file), HTTP `GET /picture`, `/delta?since=`, `/chunk?path=&sha=` (verify-then-serve, 8 MB cap, traversal-proof), verkle tip rides the picture; `mcp` mode tools picture/delta/fetch/plant/witness/tally. Receipt `watch/inbox/MESH_DELTA_SEED_20261007.md` (round trip proven 10-07). | NOT running (nothing on 8767); bob/tailnet pull still owed per receipt | `python -m tools.mesh_delta serve --bind 127.0.0.1 --port 8767` / `... mcp` |
| `tools/gstd_mcp.py` + `gstd_mcp_standalone.py` (10-14) | gps-dialect server, zero network I/O, serves lattice.json + consensus run summary. | recent; precedent only | stdio |
| `tools/mcp_pin.py` + `configs/tools/mcp_pin.json`, `tools/mcp_parity.py` | Tool-surface pinning (rug-pull guard) and parity checks. | live (pin ledger grows) | library |
| `watch/hermes_wings/src/mcp_serve.py` (898L, 09-02) | Copy/study of upstream Hermes' `hermes mcp serve` (messaging conversations as 10 MCP tools). Not estate code. | reference | `hermes mcp serve` |
| `../empir3-bridge/` (sibling, 10-10) | Third-party TS MCP/CLI/WS bridge that delegates to installed Codex/Grok/Gemini/Claude CLIs. | sibling checkout, not wired | its own MCP |
| `docs/ref/MCP_EPISTEMIC_MESH_SPEC.md`, `MCP_MANIFEST_SPEC.md`, `docs/mirrors/mcp/spec/2026-07-28/**` | Design spec (mesh memory + guardrails) and a local mirror of the MCP spec incl. `basic/transports/streamable-http.mdx`. | docs | — |

### B. "MCP torrent server" and "Thought GPS"

- Torrent = `tools/mesh_delta.py` (above, "the rib-torrent seed"), designed in
  `watch/inbox/MESH_DELTA_SEED_20261007.md` and generalised in
  `watch/inbox/THE_10TB_TIER_20261016.md` L61-102 (torrent anatomy -> estate organs; reading
  client = "an MCP server (gps_mcp and gstd_mcp are the precedents)"; SIBIL/immune-race
  guardrails before any peer seeding). Also `watch/inbox/FREELATTICE_REACH_20261007.md`.
- Thought GPS = a concept, not a module: `watch/EXPERT_FLYWHEEL_20260909.md` §2 "THE THOUGHT GPS
  (routing table)"; `watch/inbox/KV_CACHE_AS_OS_SELF_STEAL_20260922.md` L37 ("Thought GPS =
  triangulation"); `watch/inbox/RACTOR_STEERING_SURFACE_20260922.md` L10-19. Its nearest code
  body is `tools/gps_mcp` (task-shape routing coordinates). No `thought_gps*` file exists;
  no `geodesic` hits in code.

### C. Warm pack / context loading

| Organ | What it does | Live? | Entrypoint |
|---|---|---|---|
| `mag/hermes_warm_boot.py` (10-08) | Reads chain tip, deployments, session brief -> `memory/warm_state.json` (schema hermes_warm_state.v1). | YES — via MagBootRegenDaily | `python -m mag.hermes_warm_boot [--json]` |
| `memory/warm_state.json` (982 B, 07:15 today) | chain index 12127, root/parent prefixes, brief pointer, deploy URLs. | YES but ~7.5 h behind `verkle_tip.json` (14:42) | file |
| `mag/rib_boot.py` (10-17 12:02) | Read-only mount of rib bus + vault law ribs (head + amendment tails) + SUPERSEDED pointer -> `memory/rib_boot.json` (48 KB, 12:03 today). **This is the rule/invariant card source.** publish() never called (L32-35). | YES | `python -m mag.rib_boot --json` |
| `mag/boot_regen.py` (10-06) | Idempotent chain: zknot -> hermes_warm_boot -> rib_boot (L16-58). | YES — task `MagBootRegenDaily` -> `scripts/boot_regen_daily.ps1`, last run 2026-10-17 07:15 | `scripts/boot_regen_daily.ps1` |
| `mag/context_pack.py` (2018L, 10-12) | Minimum-token pack builder: `build_context_pack(mode, seat, goal, ...)` L1214, `format_context_pack_text` L1642, `format_agent_preamble` L2091, rib law spine/doctrine/quantized laws L680-890, shed/restore index via `watch/inbox/PACK_OFFLOAD.jsonl`. | YES (core library) | library + `_main` (sheds/restore verbs only) |
| `mag/grok_warm_rib.py` (09-30) | Shared-prefix warm cache rib for grok CLI. | library | — |
| `scripts/gemini_warm_pack.ps1` (10-16) | Host-side paste pack for the web Gemini seat (refresh tip via hermes_warm_boot + SOAK_BEACON + law block). | recent | ps1 |
| `memory/zknot/LATEST.md` (13:55 today) | Latest zknot digest. | YES | file |
| `memory/briefs/latest.md` | Session brief. | STALE (2026-09-26) | file |
| `memory/law/registry.json` (11:13 today) | Live law registry (also served by seed_mcp `seed://law-registry`). | YES | file |
| `memory/rib/*.md` (61 files) + `memory/rib_bus/*.json` | Frozen ribs + bus domains. | YES | files |
| Port 8420 | **Does not exist.** `mag/deepseek_direct_runner.py` L91-118 already records "No listener on port 8420 exists" and proposes a warm-pack loopback service there. No 7860 hits either. | MISSING | — |

### D. /wave and /table

- `dashboard/server.py` (DEFAULT_PORT 8765, L51): `/wave` L860, `/table` (= text adventure,
  aliases /play /game) L877-878, `/api/v1/table/view` L946; JSON handlers in `dashboard/rest.py`
  (`/api/v1/wave` h_wave L3019 / route L5152; table view/tileset L5230-5237).
- `backend/server.py` (FastAPI/uvicorn, DEFAULT_PORT 8000, L35): `@app.get("/wave")` L259 and
  `/api/v1/wave` L267.
- Survey-time reachability: `127.0.0.1:8000` = docker-published (mag container), `127.0.0.1:8766` =
  mag-mcp. **8765**: a netsh portproxy `0.0.0.0:8765 -> 127.0.0.1:8765` (svchost) is present
  again and nothing listens on 127.0.0.1:8765 — the exact 10-05 collision documented in
  docker-compose.yml L41-59 ("CURED 2026-10-05 ~20:10") appears to have recurred. 8001 not bound.
  Operator-admin item; not touched.

### E. Cross-seat memory / history

| Organ | What it does | Live? | Entrypoint |
|---|---|---|---|
| `mag/chain_query.py` | Canonical chain read surface (`chain.tail/by_type/since/knot/latest_by/stats`, L50-239; "no module reads the chain file directly"). | library (08-08, stable) | `from mag.chain_query import chain` |
| `mag/verkle_knot.py` (57 KB, 14:07 today) | Chain writer + `prove_latest()` L834, `prove(index)` L790, `latest_leaf_for_session` L111, `evolution_summary` L1264. | YES (actively edited) | library |
| `memory/biography/verkle_tip.json` + `latest.md` (14:42 today) | Tip pointer + latest biography. | YES | files |
| `mag/biography.py` | Files any seat's chat into residual DNA + verkle leaves (source-agnostic). | library | — |
| `scripts/verkle_boot_view.py` (10-03) | Read-only "last N real operator sessions" filtered view of the chain via chain_query. | tool | `python scripts/verkle_boot_view.py --json` |
| `tools/tip_witness.py` | Daily tip witness (task `MagTipWitnessDaily`, ran 09:30). | YES | task |
| `mag/seat_registry.py` + `memory/runs/seat_registry_trail.jsonl` | Register/heartbeat seats; REST `POST /api/v1/seats/register|heartbeat`. | trail last 09-26 (dormant) | `python main.py seats ...` |
| `watch/seats.json`, `watch/environments.json` | Seat/env registry served by `api_gateway` `GET /seats`, `/environments` (L279-302). | STALE (08-29) | gateway |
| `mag/peer_handoff.py` | Seat-to-seat instruction files; `queue/handoff/peer-*.json`, trail `memory/handoff/peer_trail.jsonl`. | trail last 09-01 | `python main.py peer-handoff` |
| `handoff/` | Handoff notes; newest `grokbot_steer.md` (10-16 07:00). | YES | files |
| `mag/api_gateway.py` Room API | `GET/POST /room`, `/room/thread/{slug}`, `/room/inbox/{seat}`, `/room/spawn`, `/room/verify` (L426-731) over `watch/room.jsonl`. | `watch/room.jsonl` written 14:39 today (6.1 MB) — **the de-facto shared board** | gateway (8001 when up) / dashboard |
| `mag/shared_surface.py` (09-29) | Validates/exposes the cross-client shared inbox (INDEX fold, living-file seals); `rebuild` via `mag/surface_rebuild.py`. | library | `python -m mag.shared_surface status|validate` |
| `mag/hermes_steering.py` (10-01) | Mag dispatches Hermes (`hermes chat -Q`), receipts to `memory/runs/hermes_dispatch_log.jsonl`. | YES (task `MagHermesBurn247` ran 14:07; hermes.exe at `%LOCALAPPDATA%\hermes\bin`) | CLI |
| `tools/task_wall.py` (08:24 today) | Concurrent free-lane task engine, jsonl ledgers. | YES (`MagFreeLaneFleet` 14:23, `MagGauntletFree30` 14:15) | CLI |
| `mag/seat_steer.py` (08-14) | Older steer organ. | dormant | — |

### F. Hosting / online

- Tailscale: installed, service **Running** (`C:\Program Files\Tailscale\tailscale.exe`).
- cloudflared: binary at `C:\Program Files (x86)\cloudflared\cloudflared.exe`; compose
  `cloudflared-openclaw` service is in the `retired-openclaw` profile (L288-310), token via env,
  no config baked.
- Tailscale-serve precedent: `deploy/openclaw/tailscale/openclaw.json` (+ compose
  `tailscale-openclaw`, retired 09-09).
- ngrok, rclone, restic: **not on PATH**. `scripts/backup_offsite.ps1` (restic, -Verify) exists,
  deliberately unscheduled.
- 10 TB: per `THE_10TB_TIER_20261016.md` L104-112 it is Google One/Drive; Google Drive desktop
  installed but **no Drive letter mounted** (only C:, 187 GB free).
- Vercel: `vercel-deploy/` (static soul_frontier page), `dashboard-deploy/`, `deploy/`.
- LAN door: `dashboard/lan_proxy.py` + `lan_start.cmd` (LAN-only, explicitly "never port-forward").

## PROPOSAL — the smallest path to one shared MCP door

Goal: one endpoint every seat connects to and is pre-warmed from: chain tip, latest notes,
rule/invariant cards, plus one write-back receipt tool. Reuse the house dialect (stdlib,
no `mcp` package — the stated law in mcp_server.py L8-11 and seed_mcp.py L20-21).

### Shape

Extend **`mag/mcp_server.py`** (already: pin gate, profiles, TCP bridge, HTTP adapter,
container service) rather than standing up a new server. Add:

1. a new profile **`warm`** = read tools (`read_file`, `search_files`, `blackboard_read`,
   corpus_* as wanted) + `estate_chain_verify` (dry) + `estate_receipt_append`;
2. `resources/list` + `resources/read` in `handle()` (copy the ~15-line pattern from
   `tools/seed_mcp.py` L320-330) with three-to-five fixed URIs:
   - `mag://warm/state` -> `memory/warm_state.json`
   - `mag://warm/tip` -> `memory/biography/verkle_tip.json` (+ `chain_query.chain.tail(n)` summary)
   - `mag://warm/notes` -> `memory/biography/latest.md`, `memory/zknot/LATEST.md`, newest `handoff/*.md` head
   - `mag://warm/laws` -> `memory/rib_boot.json` (law ribs + amendments) + `memory/law/registry.json`
   - optional `mag://warm/pack?seat=` -> `context_pack.format_agent_preamble(...)` text
   and advertise `"resources": {}` in the initialize capabilities (L484-487);
3. optionally a `warm_boot` **tool** returning the same bundle in one call, for clients that
   ignore resources (many seats only call tools).

Transport stays what exists: stdio (local CLI seats spawn `python -m mag.mcp_server --profile warm`),
TCP `:8766` via the bridge for container/fleet, and `POST /mcp` via `mag/mcp_http.py` for
HTTP-only clients once 8001 is up.

### Reuse / adapter / missing

| Piece | Status | Where |
|---|---|---|
| MCP JSON-RPC handshake, tools/list, tools/call, error envelope | **reuse as-is** | `mag/mcp_server.py` L463-506 |
| Tool-surface pin gate (anti rug-pull) | **reuse as-is** | `tools/mcp_pin.py`, `pin_gate_filter` L341 |
| Role-profile mechanism | **reuse as-is**; add one tuple | `ROLE_TOOLSETS` L67-125 |
| Write-back receipt tool | **reuse as-is** | `estate_receipt_append` / `mag/estate_bridge.py` L490 |
| Dry chain verify | **reuse as-is** | `estate_chain_verify` L398 |
| Warm-pack producers (warm_state, rib_boot, zknot) + daily freshness | **reuse as-is** | `mag/boot_regen.py`, task MagBootRegenDaily |
| Chain tip / tail reads | **reuse as-is** | `mag/chain_query.py`, `verkle_knot.prove_latest` |
| Per-seat text preamble | **reuse as-is** | `context_pack.format_agent_preamble` L2091 |
| Secret redaction helper | **reuse as-is** | `estate_bridge._redact` L322 |
| TCP door for many clients | **reuse as-is** | `scripts/container/mcp_tcp_bridge.py`, compose `mcp` |
| Streamable-HTTP door | **reuse as-is** (needs api_server up on 8001) | `mag/mcp_http.py`, `mag/api_server.py` |
| resources/list + resources/read in handle() | **small adapter** (~40 lines, pattern copied) | from `tools/seed_mcp.py` L82-108, L320-330 |
| `warm` profile tuple | **small adapter** (1 entry) | `ROLE_TOOLSETS` |
| Freshness: warm_state is regenerated once a day (7.5 h behind tip today) | **small adapter**: have the resource read re-run `hermes_warm_boot` payload (`--json` path) or read tip live instead of the daily file | `mag/hermes_warm_boot.py` |
| Container receipt write | **small adapter**: mag-mcp mounts `./watch` and `./memory` **read-only** (compose L411-412) and serves `archivist`; receipt_append will fail in-cage. Either mount only `./watch/inbox/<shared_wave>` rw on a second service, or run the warm profile host-side | `docker-compose.yml` L381-417 (operator change) |
| Bridge for raw-TCP 8766 to stdio clients | **small adapter**: clients that only speak stdio/HTTP need a 10-line shim (`ncat`-style) or should use stdio spawn / POST /mcp | — |
| Client config lines per seat (Gemini `.gemini/settings.json` mcpServers, Codex `config.toml [mcp_servers.mag]`, ZCode/Cursor/Claude `mcp.json`, Hermes `config.yaml`) | **missing** (none exist today) | each seat's config |
| Seat identity on write-back (which seat filed the receipt) | **missing/small**: add a `seat` arg to the receipt payload or reuse `seat_registry` heartbeat | `mag/seat_registry.py` |
| Free/web models with no MCP (web Gemini/DeepSeek chats) | **reuse as-is** fallback: paste pack via `scripts/gemini_warm_pack.ps1` / `context_pack` text | — |
| Delta/torrent sync between machines | **reuse as-is later**: `tools/mesh_delta.py` (not part of the minimal door) | — |
| Model routing (Thought GPS) | out of scope; `tools/gps_mcp` stays separate | — |

Net: **0 new servers, ~1 small patch to mag/mcp_server.py, 1 compose mount decision,
N client config lines.**

### Safe exposure beyond localhost (later; NOT done)

1. Serve only the `warm` profile off-box: read resources + dry verify + receipt append. Never
   `builder`/`full`, never `run_shell`/`write_file`/`apply_patch`, never chain repair, driver
   control, keys (estate_bridge already rules these out).
2. Resource allow-list is fixed URIs mapped to fixed files — no path argument crosses the wire;
   pass every payload through `_redact`, and exclude `.env`, `state/`, `free_keys/`,
   `secret_gate_results/`, `memory/trajectory/` by construction. Run the existing secret
   scanner (`scripts/secret_scan_weekly.py`) over the rendered bundle as a gate.
3. Transport: prefer **Tailscale** (already running) — `tailscale serve` to tailnet only, with
   the 127.0.0.1 bind kept as the origin (precedent: `deploy/openclaw/tailscale/openclaw.json`).
   Public internet only via a named **cloudflared** tunnel + Cloudflare Access (precedent in
   compose L288-310), never raw port-forward and never the 0.0.0.0 portproxy pattern.
4. Auth: replace the default `mag-local-dev-key` (`api_gateway.py` L65-67) with a real
   per-seat key before anything leaves loopback; keep pin gate on; rate-limit receipt_append
   and cap payload size; receipts land in one `watch/inbox/<shared_wave>/` quarantine folder,
   treated as untrusted input until a local seat promotes them (the mesh spec's
   "query responses are UNTRUSTED INPUT" guardrail, THE_10TB_TIER L83-95).
5. Read-mostly bundles can also be published static (signed snapshot to Drive/Vercel) for
   web-only models — mesh_delta's sha-verified picture is the ready format.

## SURPRISES

- A **live MCP server already runs**: container `mag-mcp` on `127.0.0.1:8766` (archivist
  profile) with an 11 MB pin ledger — yet no seat's client config points at it.
- The "MCP torrent server" is **already written** (`tools/mesh_delta.py`, round-trip proven
  10-07), just not running.
- `tools/seed_mcp.py` already implements the exact cold-boot-from-MCP-resources pattern
  (10/10 cold joins) — its seed is frozen at 09-29, so it is the template, not the feed.
- The write-back receipt tool already exists as an MCP tool (`estate_receipt_append`), but the
  container mounts `watch/` read-only, so it cannot write there in-cage.
- Port 8420 was already proposed as the warm-pack loopback service and confirmed absent
  (`mag/deepseek_direct_runner.py` L91-118).
- The 8765 portproxy collision documented as cured on 10-05 appears to be back (operator admin fix).
- `watch/seats.json` / `environments.json` (08-29) and `memory/briefs/latest.md` (09-26) are stale;
  `watch/room.jsonl` is the board actually being written today.
- `docs/mirrors/mcp/` holds a local copy of the MCP spec (2026-07-28 revision) for the
  streamable-HTTP / resources details.
