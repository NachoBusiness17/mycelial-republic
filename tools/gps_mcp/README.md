# gps-mcp v0: the capability-ledger router facade

One intelligent layer between all callers and all model endpoints. It
routes on MEASURED pass-rate from a SQLite capability ledger, not on
marketing labels, and every routing decision lands in an append-only
JSONL receipt. Built from the spec in
`watch/inbox/game_platform_basecamp_20260929/OPUS_ASK_DRAFT_20260929.md`
(BUILD section, as amended by the inverted-frontier verdict: the
plumbing is commodity, build it locally).

Ships in TEST-DOUBLE mode: every provider in `config.json` is answered
by an in-process fake with deterministic canned answers, so the whole
system runs offline for $0. Flip `"test_double": false` per provider to
go live.

## Layout

| File | What it is |
|---|---|
| `ledger.py` | SQLite capability ledger: schema, `record_verdict` (incremental running mean + the positive floor), `momentum` (streaks, badges, window delta), `report_capability`, verdict audit log |
| `router.py` | `ask()` and `cascade()` routing rules + the JSONL receipt log |
| `providers.py` | One JSON/YAML config for all endpoints, test double, OpenAI-compatible real calls |
| `server.py` | stdlib JSON-RPC 2.0 stdin/stdout loop exposing the tools |
| `seed_fixtures.py` | Seeds 6 synthetic models x 5 task shapes with varied plausible rates |
| `config.json` | The shipped test-double config (also the default the server loads) |
| `config.gstd.json` | The LIVE gstd surface (2026-10-09): the 6 doubles plus 14 real `gstd`-tier garden models served by the desktop gstd node's gateway, `test_double: false`; load with `GPS_MCP_CONFIG=tools/gps_mcp/config.gstd.json`. Receipt: `watch/inbox/gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md` |
| `test_gps_mcp.py` | The test suite |

## Run it

All commands from the repo root with the repo venv (never bare
`python`, which is Hermes on this host):

```text
# 1. seed a ledger (idempotent; 30 fixture rows)
.venv/Scripts/python.exe -m tools.gps_mcp.seed_fixtures
#    or point somewhere else:
.venv/Scripts/python.exe -m tools.gps_mcp.seed_fixtures --db /tmp/led.db3

# 2. run the server (line-delimited JSON-RPC on stdin/stdout)
.venv/Scripts/python.exe -m tools.gps_mcp.server

# 3. talk to it, one JSON-RPC object per line:
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ask","arguments":{"task_shape":"design_judgment","payload":{"q":"sound?"},"constraints":{"max_cost_usd":0.5}}}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"cascade","arguments":{"task_shape":"summarize","payload":"tldr","constraints":{"min_confidence":0.8}}}}
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"record_verdict","arguments":{"model_id":"frontier-opus","task_shape":"design_judgment","verdict":true,"evidence_hash":"sha256:..."}}}
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"report_capability","arguments":{"model_id":"frontier-opus","task_shape":"design_judgment"}}}
```

Paths are env-overridable: `GPS_MCP_CONFIG`, `GPS_MCP_LEDGER`,
`GPS_MCP_RECEIPTS` (defaults sit next to `server.py`).

Run the tests:

```text
.venv/Scripts/python.exe -m pytest tools/gps_mcp/test_gps_mcp.py -q
```

## The tools

- `ask(task_shape, payload, constraints?)`: single routing decision.
  Constraints: `max_cost_usd`, `max_latency_ms`, `min_confidence`,
  `pass_rate_threshold` (default 0.85). Routing priority: (a) hard
  constraints filter; (b) measured pass-rate from the ledger; (c) cost
  (cheapest qualifying wins); (d) the endpoint's own calibrated
  confidence, recorded on the receipt. A task shape with no ledger
  history routes to the designated mid tier with `exploration: true`.
- `cascade(task_shape, payload, constraints?)`: cheapest qualifying
  tier first; when the endpoint's returned confidence is below
  `min_confidence` (default 0.8) it escalates one tier and re-asks
  with the prior answer attached as context; max three tiers; returns
  the full trace (tiers tried, why, what each cost).
- `report_capability(model_id, task_shape)`: the ledger row
  (pass-rate, sample size, last-measured, cost) or `measured: false`.
  The row also carries a `momentum` sub-dict whenever the pair has
  recorded verdicts: `badge` (RISING / STEADY / DECLINING),
  `streak_badge` (STREAK-n once the current pass streak reaches 3),
  current and best pass streaks, window rates, and the improvement
  delta (see "The positive arm" below).
- `record_verdict(model_id, task_shape, verdict, evidence_hash?,
  evidence_path? | evidence_bytes?, evidence_source?)`: ground truth in,
  running-mean pass-rate update out. Every verdict is appended to a
  `verdict_log` audit table with its evidence hash, and the hash is
  never stored on trust (evidence-resolution gate, Q28 2026-10-01, the
  citation-resolution-gate-at-landing law of
  `watch/inbox/ractor50/accuracy.md` applied to hashes): pass the cited
  bytes (`evidence_path` file, or `evidence_bytes` inline -- retained on
  the row, capped at 64 KiB) and the sha256 is recomputed at append.
  Agreement stores `evidence_resolved: 1`; a claim with no bytes (or a
  hash the bytes contradict) lands `evidence_resolved: 0` --
  UNVERIFIED-class, legal but self-attested, and counted unresolved by
  the audit. `python -m tools.gps_mcp.ledger audit <db>` re-walks
  `verdict_log`, rehashes every resolvable citation (file sources
  re-read, retained blobs re-hashed), and prints agreed / mismatch /
  unresolved; exit 1 only when a hash contradicts its bytes. Rows fed
  before the gate (no source, no bytes) read unresolved: that is the
  honest reading of a self-attestation. A fail landing while the pair
  holds a RISING momentum window is floored: it logs, it does not
  punish (see below).

## The positive arm (LM7)

The meter does not only fail cold. Per (model, task_shape) the ledger
derives momentum from the last 30 recorded verdicts, split oldest half
vs newest half:

- `improvement_delta` = newest-half rate minus oldest-half rate;
  RISING when delta > 0.05, DECLINING when delta < -0.05, else STEADY.
- Streaks: current trailing pass streak and best pass streak ever;
  STREAK-n badge from 3 onward.
- Ranking tiebreak: at similar pass_rate (both qualify, cost tied),
  RISING outranks STEADY/no-history, which outranks DECLINING. The AC10
  lane-chooser law inverted toward momentum. Candidates with no verdict
  history are neutral, so cost-first routing is unchanged wherever the
  positive arm has no evidence.
- The floor: while a pair is RISING, a FAIL verdict never demotes
  `pass_rate` below the window-start rate. The threshold is named
  honestly: floor = window-start rate. The fail still lands in
  `verdict_log` (errors during improvement log, they do not punish),
  the clamp is surfaced on the result (`floor_applied`, `floor_rate`),
  and the clamp is `min(floor, pre-fail rate)` so a fail can never
  RAISE the meter either: recording failures is never a way to gain
  standing. When the window stops rising, the protection lapses with
  it.

Operator law this implements: positive reinforcement is the only
effective steering; negative pressure causes panic-errors (2026-09-30,
receipt `watch/inbox/last_mile_20260930/LM7_POSITIVE_GPS.md`).

## Receipts

Every decision (ask, each cascade attempt, even a no-route outcome)
appends one row to `receipts.jsonl`:

```json
{"ts": "...", "task_shape": "...", "chosen": "flash-mid-1",
 "considered": [{...per-candidate stats...}], "reasons": ["..."],
 "cost_usd": 0.004, "confidence": 0.92, "exploration": false}
```

Cascade rows add `trace_id` + `cascade_step`. The file is append-only;
a decision we cannot audit did not happen.

## Config and real endpoints

One file declares every endpoint, cheapest tier first:

```json
{
  "tier_order": ["local", "mid", "frontier"],
  "exploration_model": "flash-mid-1",
  "providers": [
    {"model_id": "flash-mid-1", "base_url": "http://localhost:4000/v1",
     "model": "vendor/flash-cheap", "tier": "mid",
     "cost_usd_per_call": 0.004, "latency_ms": 800,
     "test_double": false, "api_key_env": "LITELLM_KEY"}
  ]
}
```

- `latency_ms` is a declared estimate used by the `max_latency_ms`
  constraint filter (and reported by test doubles; it is not slept).
- Point at real fleets by swapping `base_url`:
  - LiteLLM proxy: `http://localhost:4000/v1`, `model` as `provider/model`.
  - Ollama: `http://localhost:11434/v1`, `model` as the local tag.
  - Any OpenAI-compatible gateway: same shape; `api_key_env` names the
    env var holding the bearer token (never inline the key).
- Confidence convention: real endpoints that emit a calibrated
    probability should put it in the response field `confidence`
    (top level or inside `choices[0]`); endpoints that do not leave
    confidence null and rule (d) simply does not trigger.

## Reading the ledger

```text
.venv/Scripts/python.exe -c "import sqlite3; c=sqlite3.connect('tools/gps_mcp/gps_ledger.db3');
[print(r) for r in c.execute('SELECT * FROM capability ORDER BY task_shape, pass_rate DESC')]"
```

Schema: `capability(model_id, task_shape, pass_rate, sample_size,
cost_usd_per_call, last_measured, updated_at, PRIMARY KEY(model_id,
task_shape))` plus the `verdict_log` audit table. Cost in the ledger is
the last measured cost (fixtures mirror the config price); routing
constraint checks use the live config price.

## Mapping to real MCP

v0 speaks plain JSON-RPC 2.0 over stdio. The tool surface is already
MCP-shaped, so wiring a real MCP server later is mechanical:

| MCP call | v0 request |
|---|---|
| `initialize` | `{"method": "initialize"}` |
| `tools/list` | `{"method": "tools/list"}` |
| `tools/call` with `name` + `arguments` | `{"method": "tools/call", "params": {"name": ..., "arguments": ...}}` |

Results already come back MCP-style:
`{"content": [{"type": "text", "text": "<json>"}], "isError": false}`.
What is missing is only the MCP handshake/protocolVersion negotiation
and framing; swap the loop in `server.py.main()` for an MCP SDK
stdio transport and keep `process_request` as the dispatcher.

## What v0 deliberately does not do

- No auth, no multi-tenancy, no rate limiting, no retry/storm
  protection: one trusted caller, one process.
- No streaming: every tool call returns one JSON blob.
- No real MCP protocol handshake (JSON-RPC stdio only; mapping above).
- The real-endpoint HTTP path (`test_double: false`) is written but
  never exercised against a live server; all tests run against the
  test double. Untested access is not access: smoke it before trusting
  it.
- Test-double latency is declared, not slept: constraint filtering
  works, wall-clock behavior does not.
- No automatic cost updates in the ledger from live billing; ledger
  cost is seeded or operator-written.
- No concurrency control: the sqlite connection is shared and the
  server is single-threaded by design.
- Routing is greedy threshold + cost, not bandit/adaptive: it does not
  explore deliberately beyond the no-history rule, and it does not
  decay stale measurements.

## IF WE GROW THIS (ranked, highest leverage first)

1. Verification-gate contract: bind `record_verdict` to machine-checkable
   evidence (hash the graded artifact, chain verdicts) so ledger
   pass-rates cannot be inflated by a lying caller; trust is the core
   product, routing is commodity.
2. Adaptive routing over the ledger (UCB/Thompson with time decay) to
   replace the greedy threshold and handle drift without operator
   re-seeding.
3. Real MCP transport + LiteLLM/KServe adapters so gps-mcp drops into
   the existing fleet as a plain sidecar, no client changes.
