# GSTD FLEET LANE SPEC (the 8th lane, the one that PAYS)

Landed: 2026-10-07, run `gstd-mycelial-kickoff-20261007`, lane g3-fleet-lane-spec.
Owns: P3 FLEET LANE of `docs/ref/GSTD_DOGFOOD_PLAN.md`. Skeleton module:
`tools/gstd_fleet_provider.py`. The wire (the patch into
`tools/free_lane_fleet.py`) is OUT OF SCOPE until wallet paste; see section 7.

## 1. What this lane is

The gstd mesh (Cloudflare Worker platform + three nodes: desktop FULL node,
bob node-lite, pixel node-lite in Termux) becomes the fleet's 8th provider
lane. Unlike the 7 free surfaces in `tools/free_lane_fleet.py` it PAYS: task
executions settle GSTD credits to our per-device wallets. The driving-ladder
law still binds: outputs bank as findings, never as done/trusted work, and
judgment climbs to the funded tier. The lane pays us to sense.

## 2. The wallet gate (fail-closed, the hard gate)

P0 INPUTS OWED (plan): one wallet PER DEVICE (operator ruling request). The
gate reads three `.env` keys, strip()ed at load (CR law,
`watch/inbox/CSV_VERDICT_20261004.md`):

- `GSTD_WALLET_DESKTOP`
- `GSTD_WALLET_BOB`
- `GSTD_WALLET_PIXEL`

Law: absent `.env`, missing key, empty value, and whitespace-only value all
read as absent. With zero wallets present, EVERY live verb
(`submit_task`, `poll_task`, `cycle_gstd`) returns a
`WALLET GATE BLOCKED` verdict before any byte leaves the box, and
`--cycle` exits 3. Nothing in this module has an env-var or flag bypass; the
only way the gate opens is a wallet actually present in `.env`.

## 3. The submit / poll / bank pattern

Platform base is a module constant, `https://platform.gstdtoken.com` (the
P3 MCP door domain; `mag/gstd_probe.py` probes health on
`app.gstdtoken.com` and stays read-only). No env override of the base: the
SSRF law (`tools/free_lane_fleet.py` Mimosa finding 2026-10-05) requires
byte-matched fixed literals, so changing the base is a code edit at wire time,
never a config flip.

1. SUBMIT: `POST {platform}/api/v1/tasks/submit`. Body:
   `{"id": "gstd-<work_id>", "kind": <task_shape>, "prompt": ..., "device_hint": ...}`.
   `work_id` reuses the fleet's ids (`queue:<id>`, `probe-<hash>`,
   `corridor:<area>`). `task_shape` is one of `probe | corridor | queue`.
   Wallet rides the `Authorization: Bearer` header (wallet-present gate
   guarantees a token exists).
2. POLL: `GET {platform}/api/v1/tasks/<task_id>`, 10s sleep x 30 tries (5 min
   window; the mesh's own node cadence is 5s poll, our lane is patient
   upstream). The variable `<task_id>` segment is the ONLY non-literal in any
   URL this module opens and must match `^[A-Za-z0-9_:-]{1,80}$` before the
   URL is joined. The opener refuses redirects (`_NoRedirect`).
3. BANK (two row classes):
   - Fleet finding row: through `tools/free_lane_fleet.bank`
     (`provider: "gstd-mesh:<node_device>"`), scrubbed, into the shared
     `memory/runs/free_lane_fleet/ledger.jsonl` so the fleet liveness check
     and the census patrol see mesh work in one place.
   - GPS mesh row (`gps_mesh_row.v1`, section 5): appended to
     `memory/runs/gstd_fleet_lane/mesh_ledger.jsonl`, completions ONLY.
     Blocked / failed / poll-expired cycles bank a plain cycle row there
     instead (a cycle row never carries a gps_mesh_row.v1 schema tag).

Retry law carried: retry never. One submit, one poll window, failures bank.
Resubmission and settlement disputes are a human gate, not a loop.

## 4. Laws carried from the free lane (non-negotiable)

- Keys strip()ed at load (CR law, CSV_VERDICT_20261004.md).
- Every banked string passes `_scrub` (KEY_SCRUB_20261004.md trail-leak class).
- SSRF guard: `urlopen` sees only the fixed platform literals plus the
  regex-gated poll segment, through a redirect-refusing opener.
- One-shot fires, failures bank; dead-node skip rides the free lane health
  table, not a local retry counter.

## 5. GPS ledger row shape (the contract)

Keyed `(node_device, task_shape, evidence_hash)`, schema `gps_mesh_row.v1`:

```json
{
  "schema": "gps_mesh_row.v1",
  "node_device": "desktop|bob|pixel",
  "task_shape": "probe|corridor|queue",
  "evidence_hash": "<sha256 hex of the completion bytes, 64 chars, REQUIRED>",
  "key": ["<node_device>", "<task_shape>", "<evidence_hash>"],
  "work_id": "probe-<hash>",
  "task_id": "<platform task id>",
  "provider": "gstd-mesh:<node_device>",
  "ok": true,
  "chars": 276,
  "model": "<ollama model the node reports>",
  "latency_ms": 0,
  "ts": "2026-10-07T12:00:00Z",
  "detail": "<scrubbed completion tail, 1200 max>"
}
```

- `evidence_hash` is the sha256 of the completion TEXT bytes, computed at poll
  time (the falsifier in section 9 exists because of this clause). Empty
  evidence NEVER banks: the builder raises. That is the Q28 gate
  (`tools/gps_mcp/ledger.py`: evidence never stored on trust; dedupe on the
  triple through the partial UNIQUE index `ux_verdict_log_evidence_triple`).
- Mapping onto the GPS ledger: `node_device -> model_id` as
  `gstd-mesh:<device>`, `task_shape` unchanged, `evidence_hash` unchanged.
  Per-device wallets (P0 ruling) are what make this real per-node CAPABILITY
  data instead of one pooled lane. `to_verdict_log_args()` is the wire
  adapter into `GpsLedger.record_verdict(model_id, task_shape, verdict,
  evidence_hash, evidence_source="gstd mesh task <id>")`; the triple dedupe
  makes a re-poll of the same completion a no-op in the GPS ledger.

## 6. Honest scope of the skeleton (what it does NOT do)

- No live submits: the gate is closed until P0 wallets paste.
- No settlement or balance accounting: the settlement RFC is staged upstream;
  the skeleton banks observations only, computes nothing owed.
- No quorum attestations (P4 gated in the plan).
- No port of gstdbot code: LICENSE is NOASSERTION (plan standing note); the
  module speaks HTTP to the platform only.
- API body/response field names are parsed defensively (`task_id` /
  `status` / `result` fallbacks); exact shapes verify at wire time against a
  live platform, before the first real submit.

## 7. Wire plan (fires on wallet paste, one sitting)

1. Operator pastes per-device wallets into `.env` (P0).
2. Desktop FULL node up: `docker compose up gstd-node` with the estate Ollama
   wired (P1); verify on the platform `/api/v1/nodes` list.
3. `.venv\Scripts\python.exe -m tools.gstd_fleet_provider --status` reads
   `WALLET GATE: OPEN`.
4. `.venv\Scripts\python.exe -m tools.gstd_fleet_provider --cycle` fires the
   first gated cycle (queue items first, then probes, then corridors,
   round-robin over wallet-carrying devices).
5. The free lane wire: add to `tools/free_lane_fleet.py` PROVIDERS:
   `{"id": "gstd-mesh", "kind": "gstd", "url": SUBMIT_URL, "key_env":
   "GSTD_WALLET_DESKTOP", "model": "mesh:auto"}` and a `gstd` branch in
   `fire()` that delegates to `gstd_fleet_provider.submit_task` +
   `poll_task`; `_ALLOWED_URLS` grows by the SUBMIT_URL literal only. This
   patch is the step that lands on wallet paste, not before.
6. First completion banks finding row + gps row; extend the drift patrol to
   `/api/v1/nodes` liveness per P3 RECEIPTS.

## 8. Falsifier

A wallet-pasted week where `memory/runs/gstd_fleet_lane/mesh_ledger.jsonl`
grew but no GPS capability row moved (`gstd-mesh:<device>` x task_shape
pass-rates flat in `gps_ledger.db3`) means the lane burns without paying
data. Fix the evidence capture first: `evidence_hash` must be computed at
poll time from completion bytes, never reconstructed at bank time.

## 9. Tests

`tests/test_gstd_fleet_provider.py`: gate fail-closed, gate opens on one
wallet, no network behind a closed gate, task-id allowlist regex before URL
join, foreign-URL refusal, full-key + non-empty-evidence requirements, scrub
carries into banked rows, verdict-log adapter preserves the key triple, fixed
literals only. Run: `.venv\Scripts\python.exe -m pytest -q tests/test_gstd_fleet_provider.py`.
