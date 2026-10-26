# MCP BRIDGE: estate tools for Z.ai agents (design, 2026-09-28)

Item mcp-bridge, flash50 lane. Every claim below cites a file I read or a
command I ran this session, or is marked OWED. No em-dashes, no en-dashes.

## 0. Headline

The estate does NOT need a new bridge protocol. It already owns a working MCP
server (`mag/mcp_server.py`, stdio JSON-RPC 2.0, proven live this session) and
an MCP HTTP adapter (`mag/mcp_http.py`, `POST /mcp` on the API gateway at
127.0.0.1:8001). What is missing is: (1) the five named tools are NOT in
`tools.TOOL_MAP` (live manifest = 34 tools, none of the five), (2) the gateway
auth is one shared key with a weak default, (3) there is no per-seat rate
limiting on the MCP surface. The bridge is therefore an EXTENSION of three
existing organs, not a from-scratch build:

- registry: `tools.TOOL_MAP` (tools/__init__.py:4) + profiles in
  `mag/mcp_server.py:47` (ROLE_TOOLSETS)
- transport: `mag/mcp_server.py` (stdio) + `mag/mcp_http.py` (HTTP)
- authority: `mag/effect_broker.py` execute() receipt chain (effect_broker.py:369)

The Z.ai side needs no estate code at all in the primary shape: a Z.ai
coding-plan seat (exactly the seat writing this sentence, which already has
external MCP servers mounted as `mcp__*` tools in its tool list: Mapbox,
web-reader) mounts the estate's MCP server via its client config and calls the
tools natively.

## 1. The two ends

Estate end (MCP server): the repo, Windows host, loopback-bound.
Z.ai end (MCP client): two real shapes.

- Shape A (PRIMARY, zero new perimeter): a Z.ai coding-plan seat running on a
  machine with repo access (this very session is one; its harness mounts MCP
  servers and exposes them as tools, observed directly in this session's
  available-tool list). It speaks stdio to `python -m mag.mcp_server` or HTTP
  to `http://127.0.0.1:8001/mcp`. Evidence the client half works: this
  session's tool list carries `mcp__plugin_mapbox_*` and `mcp__web_reader__*`
  tools, i.e. the z.ai coding-plan harness is already a working MCP client.
- Shape B (operator GO required, opens the perimeter): a Z.ai-hosted cloud
  agent with no repo access needs a reachable URL. Design: cloudflared named
  tunnel in front of the gateway, per-seat bridge tokens, `?key=` bypass
  disabled. lan_proxy.py:32-35 states today's law (LAN-only, never internet,
  "never port-forward 8765/8001"), so Shape B flips a standing security
  posture and is gated on an explicit operator decision. A tunnel command was
  NOT run this session (OWED until operator GO).

## 2. What exists today (read, and run live)

| Surface | File | Proof |
|---|---|---|
| stdio MCP server, hand-rolled JSON-RPC 2.0, stdlib-only | mag/mcp_server.py:9-11, 366-380 | live handshake this session |
| protocol version | mcp_server.py:40 `PROTOCOL_VERSION = "2025-06-18"` | echoed back in live initialize |
| profiles = capability projections, "not permission sets" | mcp_server.py:44-47, 47-92 | read |
| effect-class metadata per tool (read/mutating/model) | mcp_server.py:107-118, _tool_meta 121-157 | visible in live tools/list `_meta` |
| quantized cartridges (content-addressed, cacheable) | mcp_server.py:245-306 | read |
| MCP over HTTP, stateless streamable, batch, 202 on notifications | mag/mcp_http.py:1-11, 32-44 | read |
| FastAPI host of the gateway on 127.0.0.1:8001 | mag/api_server.py:14, 19, 39 | read |
| X-API-Key gate, constant-time compare, `MAG_API_KEY` env | mag/api_gateway.py:61-94, 163-164 | read; live 401 path in dispatch |
| effect broker: authority + budget + receipt chain | mag/effect_broker.py:1-11, 205-219, 369-434 | read |
| cross-process in-flight lease gate (stale-steal 120s) | mag/concurrency_gate.py:1-18, 61-63, 89-107 | read |
| LAN forwarder 8001 with security caveat | dashboard/lan_proxy.py:8, 30-35, 53 | read |
| SSRF fence pattern (allowlist + public-IP resolve + no redirects) | tools/stealth_driver.py:73-111, 495-513; mag/auth_switchboard.py:56-67 | read |
| shared-surface authority law: "A proposal or model message cannot authorize an effect" | watch/inbox/SHARED_SURFACE_CONTRACT.json laws[] | read |

Live probes run this session (all commands executed here):

1. stdio handshake: `printf '{"jsonrpc":"2.0","id":1,"method":"initialize",...}' ... | ./.venv/Scripts/python.exe -m mag.mcp_server`
   returned `{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"serverInfo":{"name":"mag-tool-map","version":"1.0.0"}}`.
2. `tools/list` over the same pipe: 34 tools, and a name scan for the five
   bridge targets returned `[]` (none registered).
3. `tools/call` end-to-end (`corpus_stats`): full round trip returned
   `{"ok": true, "total_rows": 581477, ...}`. The dispatch path
   (mcp_server.call_tool -> TOOL_MAP) works today.
4. Five-tool import check (venv python): all five import clean with their
   entry points present: water_graph (WaterGraph.tick, from_spec), dirac_loop
   (scan, rank, spectrum, fundamental_cycles, bank), chain_repair (repair,
   find_bad_tail_index), thought_quantizer (compile_packs, check, classify),
   stealth_driver (one_cycle, t_chain, TOPICS, _work_lanes).
5. Z.ai-side rate-limit contact: a WebSearch call made through this session's
   Z.ai hosted web-search MCP returned `MCP error -429 {"error":{"code":"1302",
   "message":"Rate limit reached for requests"}}` three times in a row.
   First-hand confirmation that 1302 concurrency limits bite Z.ai-hosted MCP
   tools too (matches docs/ref/ZAI_API_EXPERT_REFERENCE.md:81).

## 3. Tool surface: the five estate tools as MCP tools

Naming: `estate_` prefix, one tool per verb, never a generic "run tool" proxy.
Registration goes into `tools.TOOL_MAP` as static entries (the ephemeral
overlay at tools/__init__.py:52-62 exists but static registration is the
honest shape for standing organs; the overlay refuses to shadow static tools,
tools/__init__.py:67-73).

### 3.1 estate_water_graph_tick (read_or_deterministic_compute)

- Wraps: `mag/water_graph.py` WaterGraph.tick() (water_graph.py:108-196).
- Why this tool is the bridge's showcase: the module is ALREADY stateless by
  design. Graph state serializes to a spec dict (`to_spec`, water_graph.py:248-259,
  schema `water_graph.v1`) and rebuilds (`from_spec`, water_graph.py:262-274).
  No server-side session store needed; the caller holds the state, the server
  holds the physics. This is the correct MCP shape for any deterministic tool.
- Input: `spec` (object, water_graph.v1), `ticks` (int, default 1, cap 1000).
- Output: new spec + the tick's event lines (the STARVED sensor line at
  water_graph.py:185 is the interesting output for an external agent).
- Determinism: integer volumes, insertion-ordered, no RNG (docstring
  water_graph.py:24). Same spec in, same spec out, any number of calls.
- Cost: $0, milliseconds. Rate class: widest.

### 3.2 estate_dirac_scan / estate_dirac_rank / estate_dirac_spectrum (read)

- Wrap: `mag/dirac_loop.py` scan() :295-312, rank() :257-269, spectrum()
  :272-292. Input: `scope` enum operational|knowledge|all (validated at
  dirac_loop.py:66-69). These read the organ/knowledge graphs and return the
  loop census (beta1, closed_solved, open_gaps). $0, read-only.
- Timeout: 60s (graph build can walk the estate; scan truncates lists to 8 at
  dirac_loop.py:309-310, so response size is bounded).

### 3.3 estate_dirac_bank (mutating, broker-gated)

- Wraps: `bank(edge, receipt, seat)` dirac_loop.py:231-254. Appends one row to
  `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` (BANKED_FILE, dirac_loop.py:228).
- Class: mutating_or_executing. This is the tesuji act (verify-without-replay
  closes a loop in the estate's lattice), so an external agent's bank call must
  ride an effect-broker authority envelope (section 5) and lands a broker
  receipt next to the row. The `receipt` argument is REQUIRED non-empty: the
  no-receipt bank is exactly the fabrication smell the estate forbids.

### 3.4 estate_chain_verify (read) / estate_chain_repair (mutating, operator tier)

- Wrap: `tools/chain_repair.py` repair(dry=True/False) (chain_repair.py:49-90).
  `--dry` is verify-only (the same read-only call stealth_driver already runs
  every cycle at stealth_driver.py:564-569). Real repair rewrites a row of the
  verkle chain file under verkle_lock and refreshes the tip
  (chain_repair.py:54-87). Blast radius: the estate's integrity spine.
- Decision: chain_repair(real) is NOT exposed to external agents in v1. It
  stays a seat-internal + operator verb. The MCP tool `estate_chain_verify`
  runs dry-mode only and returns the CHAIN-REPAIR verdict line. If a cloud
  agent ever needs repair, the correct pattern is: it files a finding, a
  funded seat executes the repair. Exit contract preserved: 0 ok / 1 still
  broken / 2 unexpected shape (chain_repair.py:19-20).

### 3.5 estate_thought_check (read) / estate_thought_compile (mutating, scoped)

- Wrap: `tools/thought_quantizer.py` check(max_age_hours) :200-217 (pure
  staleness read, exit 0/1/2) and compile_packs() :121-197 (writes
  `memory/corpus/quantized_thought/instructions_{frontier,flash,local}.jsonl`
  + compile_report.json, OUT_DIR at thought_quantizer.py:37).
- compile writes only inside its own OUT_DIR (paths come from CLI defaults;
  the MCP adapter pins --in/--out to the repo defaults and does NOT accept
  caller-supplied out paths, which keeps an external caller from aiming the
  writer elsewhere). Class: mutating, but the allowlist is one directory, so
  broker-gated with a canned authority, not operator-tier.

### 3.6 estate_driver_status (read only)

- stealth_driver is a 24/7 loop process, not a request/response tool. Expose
  exactly one read tool: tail of `state/fuel/stealth_driver.jsonl` heartbeat
  (HEARTBEAT, stealth_driver.py:64) + `_off()` flag state (stealth_driver.py:65,
  516-517) + lane state `state/fuel/stealth_work_state.json`.
- NEVER exposed: the stop/start control words (OFF_FLAG create/delete,
  stealth_driver.py:26-29), `once` cycle trigger, and anything touching
  `_work_lanes()` (:205-251) or `_sdd_key()` (:192-202). Two hard reasons:
  (a) the lanes carry live provider keys, including the funded Nous key read
  from the hermes .env, and keys never cross the bridge; (b) control of the
  driver is the operator's single word by design (boot-lane law), and the
  shared-surface contract forbids a model message from authorizing an effect.

### 3.7 Effect-class summary

| tool | class | authority path | timeout |
|---|---|---|---|
| estate_water_graph_tick | read/deterministic | read guard | 10s |
| estate_dirac_scan/rank/spectrum | read | read guard | 60s |
| estate_dirac_bank | mutating | broker authority envelope required | 60s |
| estate_chain_verify | read (dry only) | read guard | 180s (matches stealth_driver t_chain timeout, stealth_driver.py:565) |
| estate_thought_check | read | read guard | 15s |
| estate_thought_compile | mutating, OUT_DIR-pinned | broker, canned authority | 120s |
| estate_driver_status | read | read guard | 10s |

These classes reuse `_tool_meta`'s five honest fields (effect_class, risk,
authority, cost_kind, exhaustion; mcp_server.py:121-157) so every manifest row
tells the caller who authorizes what BEFORE the call.

## 4. Protocol

### 4.1 Wire (unchanged from what exists)

MCP = JSON-RPC 2.0. Handshake: `initialize` -> `notifications/initialized` ->
`tools/list` / `tools/call`; unknown method -> -32601; parse error -> -32700;
notifications (no id) get no reply on stdio (mcp_server.py:342-380) and 202
empty-body on HTTP (mcp_http.py:22-29, 40-43). Protocol version string
"2025-06-18" (mcp_server.py:40). HTTP transport is stateless streamable: one
JSON-RPC message per POST, batch arrays supported (mcp_http.py:9-11, 39-43).

Client config, Shape A (coding-plan seat, stdio):

```json
{ "mcpServers": { "mag-estate": {
    "command": "C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe",
    "args": ["-m", "mag.mcp_server", "--profile", "bridge"] } } }
```

Client config, Shape A over loopback HTTP (shares one gateway process):
url `http://127.0.0.1:8001/mcp`, header `X-API-Key: <token>`.

### 4.2 Server additions (small, named)

1. `ROLE_TOOLSETS["bridge"]` in mcp_server.py:47: exactly the eight estate
   tools of section 3, nothing else. A profile is a projection, not a
   permission set (mcp_server.py:44-46), so the bridge profile is about
   context economy and surface honesty; authority stays with the broker.
2. Static registration of the eight tools in tools/__init__.py TOOL_MAP with
   `_normalize_args` alias entries where models tend to blob arguments
   (pattern: _ARG_ALIASES, tools/__init__.py:117-130).
3. The manifest `_meta.mag` rows carry the section 3.7 effect classes, so
   Z.ai-side agents can pre-flight authority without a round trip.
4. Quantized cartridges already exist for cache-stable manifest shipping
   (mcp_server.py:245-277); the bridge profile gets one automatically.

### 4.3 Response contract (honesty on the wire)

Every tool result is JSON text carrying the estate's claim grammar: a result
is `{"ok": true, ...}` only for work actually executed in the estate process;
anything sensed-but-unverified returns the `sensed` wording (the driving-ladder
law: free/external outputs are findings, never done; AGENTS.md DRIVING LADDER;
code-as-law precedent at stealth_driver.py:486-492 flips free-lane work to
done only after funded-tier verification). Tools that cannot verify return
`{"ok": false, "owed": "..."}` rather than a plausible guess. No fabrication
and no em-dash laws ride in each tool description so the law travels with the
schema into the client's context.

## 5. Auth model

### 5.1 Three rings (existing law, extended)

Ring 0, stdio/loopback, today: spawn-is-trust. The stdio server grants nothing
the local process does not already have (mcp_server.py:13-19). No token.
Ring 1, LAN HTTP, today: gateway `X-API-Key` (api_gateway.py:61-94), one
shared key, constant-time compare (:70-77), 401 on miss (:163-164), LAN-only
via lan_proxy (lan_proxy.py:30-35). The default key literal
`mag-local-dev-key` (api_gateway.py:67) is acceptable ONLY because the bind is
loopback; any Shape B work begins by removing that fallback for the /mcp
route.
Ring 2, internet (Shape B, operator GO gated): tunnel + per-seat tokens.

### 5.2 Per-seat bridge tokens (the new part, R3)

- Token: `MAG_BRIDGE_TOKEN_<SEAT>` env entries; value 32+ bytes of
  os.urandom, hex or base64url. Shape obeys the house secret grammar
  (uppercase ENV-ASSIGN name, tools/secret_gate_rules.py:62 rule and :139
  never-block list) and clears the 4.3-bit entropy floor
  (secret_gate_rules.py:122) by construction.
- Check: extend `check_api_key` with a token-table lookup
  (`state/bridge_seats.jsonl`: seat, token_sha256, profile, expires_ts,
  budget_per_day). Compare by sha256 + constant-time equality; log
  fingerprints only, never values (auth_switchboard.py:17 law; fp() pattern
  auth_switchboard.py:78-79).
- The `?key=` query convenience (api_gateway.py:86-91) is DISABLED for the
  bridge profile and any tunnel: URLs leak into logs and browser history.
- Rotation: snapshot-style vault per auth_switchboard's grammar
  (state/auth_switchboard/<ts>_<name>/, auth_switchboard.py:12-13); `use`
  stays operator-typed-GO (never-edit-own-credentials law,
  auth_switchboard.py:17-19).
- What never crosses: provider keys. The bridge serves estate COMPUTE; the
  caller's Z.ai credentials stay on the caller. Conversely the estate's
  OpenRouter/Nous/Groq keys (stealth_driver lanes, stealth_driver.py:205-251)
  are unreachable through any of the eight tools by construction.

### 5.3 Authority for mutating calls

`tools/call` on a mutating tool requires `params.authority` to be a broker
authority envelope: `{status: "AUTHORIZED", granted_capabilities: [...],
event_id, budget, ttl_seconds}` (shape from effect_broker.execute's gate,
effect_broker.py:205-219, and the self-test fixtures at :511-518). The call
path for mutating tools becomes: gateway auth (token) -> broker
`execute(effect, params, authority)` -> receipt committed to
`memory/runs/effect_broker/` (:26, :184-198). The broker is the single
side-effect door (its module law, effect_broker.py:1-11) and it is what makes
the shared-surface rule enforceable in code: an external agent's PROMPT can
propose a bank; only an authority object issued through the switchboard
executes it. Missing/expired authority returns a JSON-RPC tool error with the
broker's reason string, not a crash.

## 6. Rate limiting

Three layers, all from parts the estate already runs.

### 6.1 Estate-side in-flight caps (concurrency_gate leases)

`mag/concurrency_gate.py` is a cross-process lease-file semaphore built
exactly for this (its own docstring: z.ai limits are CONCURRENCY, not RPM;
lease slots with LEASE_SECS=120 stale-steal so a crashed caller cannot
deadlock the lane, concurrency_gate.py:1-18, 61-63). The bridge adds lanes:

| lane name | in-flight | covers |
|---|---|---|
| mcp-bridge.read | 4 | tick, dirac reads, chain verify, thought check, driver status |
| mcp-bridge.mutate | 1 | dirac bank, thought compile |
| mcp-bridge.heavy | 1 | dirac scan over scope=all |

Rationale: mutating verbs are append/rewrite on single files; one in-flight is
the honest cap (chain_repair itself takes verkle_lock, chain_repair.py:54).
Read caps exist to keep one cloud agent from pinning the box. Acquisition
failure surfaces as JSON-RPC error `-32000` with `retry_after_ms` derived from
POLL_SECS and queue depth, so a well-behaved Z.ai client can back off without
burning attempts.

### 6.2 Per-seat budgets (policy_engine through the broker)

Every mutating call already passes `pe.check_budget(authority, effect,
decrement=True)` (effect_broker.py:391-402). Bridge seats get a daily budget
in the seat registry (5.2); exhaustion is a clean refused call with the
receipt's `budget_remaining: 0`, never a soft degradation. This is the
existing "budget existed only in prose otherwise" fix (effect_broker.py:387-390)
applied to external callers.

### 6.3 Z.ai-side backoff (caller law, already measured)

The bridge client on the Z.ai seat obeys the fleet's receipted backoff:
429 with body codes 1305/1302/"overloaded" -> retry same request at 15s then
30s, 2 attempts max, bounded worst case +45s, every failed attempt recorded
(docs/ref/ZAI_API_EXPERT_REFERENCE.md:96-107, measured by B2-04). Concurrency
context from the operator-pasted z.ai table: GLM-5.3-Flash 50, GLM-5.3 15,
GLM-4.7-Flash 1 in-flight (ZAI reference, ADDENDUM 2). This session's own
1302 wall on Z.ai's hosted web-search MCP (probe 5, section 2) is the live
reminder that the CALLER's lane, not the bridge, is usually the first
bottleneck. Harness-level law also applies on coding-plan seats: workflow
children maxAttempts 0, keep max_concurrency at 3 or less for workflow shapes,
Task agents ride the main retry path (AGENTS.md fan-out width law).

### 6.4 What the bridge does NOT rate-limit

Read-only deterministic compute with bounded outputs (water tick, thought
check) is cheap enough to leave under the shared read lane only; adding
per-tool quotas there would be theater. If metering is ever owed, the broker
receipt stream is the meter (every call is already receipted; count receipts).

## 7. Failure posture

- Tool exceptions are reported at the tool boundary, never crash the server
  (mcp_server.call_tool already catches and wraps, mcp_server.py:322-326).
- Subprocess spawns (chain verify, quantizer compile) carry
  `creationflags=CREATE_NO_WINDOW` on win32 (house law; precedent
  stealth_driver.py:530-534).
- Timeouts in section 3.7 are resource fences for remote callers, not design
  patches; a timeout firing repeatedly is a defect to fix at the source
  (build-discipline law: no timeouts papering over sync problems, AGENTS.md).
- The gateway never returns stack traces (envelope, api_gateway.py:50-54,
  177-179).
- Degradation: if TOOL_MAP import fails the server still answers initialize
  and tools/list fails closed with a JSON-RPC error, so a client sees an
  honest empty-not-broken surface.

## 8. Rollout

- R1 (no auth change, $0): register the eight tools + bridge profile +
  alias entries + unit tests (tick determinism, scan shape, verify exit
  codes, compile OUT_DIR pin). Proven low-risk: this session's probes show
  the dispatch path works the moment a tool name exists in TOOL_MAP.
- R2: scenario cards for the workflow gate (configs/workflow_gate_scenarios
  pattern) covering: unauthorized call, expired authority, budget exhaustion,
  lease timeout, sensed-vs-done grammar in results.
- R3: per-seat token table + check_api_key extension + `?key=` off for
  bridge routes + rotation vault.
- R4: broker wiring for the two mutating tools (canned authority for
  thought compile; switchboard-issued authority for dirac bank).
- R5 (operator GO): Shape B tunnel, Ring 2. Never precedes R3.

## 9. Falsifiers / OWED

- OWED: no Z.ai-hosted cloud-agent MCP client doc was verified this session;
  the web search for it was itself rate-limited by Z.ai 1302 (probe 5). Shape
  B client compatibility is UNVERIFIED until a cloud agent is pointed at a
  tunnel in a drill. Shape A needs no such doc (first-hand: this seat mounts
  MCP servers).
- OWED: tunnel not run, no internet-facing test performed (operator GO gate).
- OWED: R1-R4 are unimplemented design; only the probes in section 2 were
  executed here.
- Falsifier for the whole design: if `python -m mag.mcp_server --profile
  bridge` does not answer initialize + tools/list with the eight tools after
  R1 lands, or if a mutating call without authority is not refused by the
  broker, this doc is wrong and must be amended, not argued around.
- Not a claim: nothing here asserts Z.ai product UIs (chat.z.ai etc.) can
  connect to arbitrary remote MCP servers; only the coding-plan seat client
  shape is evidenced.

## 10. Appendix: receipt index

Files read this session: mag/water_graph.py (274 lines), mag/dirac_loop.py
(348), tools/chain_repair.py (101), tools/thought_quantizer.py (247),
tools/stealth_driver.py (879), mag/mcp_server.py (410), mag/mcp_http.py (44),
mag/api_gateway.py (portions), mag/effect_broker.py (607),
mag/auth_switchboard.py (292), mag/concurrency_gate.py (155),
tools/__init__.py (portions), mag/desk_tools.py (header),
dashboard/lan_proxy.py (header), watch/inbox/SHARED_SURFACE_CONTRACT.json,
docs/ref/ZAI_API_EXPERT_REFERENCE.md (sections 2, 5, 5.1, ADDENDUM 2),
tools/secret_gate_rules.py (rule indexes).
Commands run this session: git ls-files/grep sweeps; venv import check of all
five tools (output in section 2.4); stdio MCP handshake, tools/list (34 tools,
bridge targets absent), tools/call corpus_stats (581477 rows); WebSearch probe
(1302 x3).
Banked: watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md and
flash50/mcp-bridge-design.md (byte-identical copies, per the ask naming both
paths).
