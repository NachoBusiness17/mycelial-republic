<!--
prior_art: docs/ref/SOVEREIGN_DATA_PLANE_DECOUPLING.md, tools/mag_relay/mag_relay.py -- the decoupling spec names the data plane this relay implements; mag_relay.py is the carrier the doc documents
-->

# mag-relay (2026-10-25)

Stateless signed JSON-RPC relay between Mag mesh nodes. One file: `mag_relay.py`. Python stdlib only; uses `cryptography` when present (Bob, PC) and a vendored pure-Python RFC 8032 Ed25519 otherwise (Termux phones). Interop checked both ways.

## Self-steal sources
- PC repo `mag/mcp_http.py` (2026-10-17): stateless POST /mcp, one JSON-RPC per request, 202 for notifications.
- PC repo `mag/seat_handshake.py` (2026-10-17): domain-tagged Ed25519 canonical string, public-key allowlist, skew window, replay cache, bare reject with no detail.
- PC repo `scripts/verify_knot_v2.py` (2026-10-17): pure-Python Ed25519 sign/verify.
- PC repo `mag/seed_seal.py` (2026-10-02), `scripts/seat_keygen.py` (2026-10-17): keygen prints public key only.
- Bob `hermes_fleet/fleet.py`, `devices.json` (2026-10-25): ssh lane table, hermes invocation, node IPs.

## Wire format
POST http://<tailscale-ip>:8765/mcp, JSON-RPC 2.0, `tools/call`, `params.arguments.mag_relay` = envelope:
`{from, to, ts, nonce, head, tool, args, sig}`. Signed bytes = `mag-relay.v1\n` + canonical JSON of
`{from,to,ts,nonce,head,tool,payload_sha=sha256(canonical args)}`.

## Checks (server, in order), any failure = generic `-32001 rejected` + reject line in ledger
unknown sender, wrong recipient, Tailscale whois (CLI present: source IP pinned AND whois ComputedName == peer ts_host; Termux: pinned source IP only), skew > 120 s, tool not in global allowlist or per-peer `allow`, tool name mismatch, replay (nonce persisted in ledger, survives restart), Ed25519 signature.

## Tools (allowlist)
read_chain_head, append_record, submit_task (queue; `run:true` invokes local `hermes chat -q` synchronously), get_result, describe_image (local ollama vision model via MAG_RELAY_VISION_MODEL; errors cleanly if absent).

## Ledgers
- Node-local: `~/.mag_relay/relay_ledger_<node>.jsonl`, each line `{seq, prev, t, kind, ..., hash=sha256(canonical line)}`; kinds call/result/record/reject.
- Receipts: server signs `{node, from, nonce, tool, call_hash, result_hash, result_sha, ledger_head, seq, ts}`; caller verifies and appends to `receipts_<node>.jsonl`.
- Bob merge: `mag_relay.py merge --out merged_relay_ledger.jsonl receipts...` folds only verified receipts, dedupes by (node, call_hash), hash-linked, append-only, idempotent.
- The Mag verkle chain file, tip and ACL are never opened.

## Keys
`keygen --node N` creates `~/.mag_relay/N.seed` (32 bytes, O_EXCL, 0600 on Termux; Windows inherits user-profile ACL) and prints only the public key. Only public keys go into `peers.json`.

## Vision / direction path (design)
Non-vision Hermes (phones: hermes-nous / hermes-default lanes) -> relay `describe_image` -> node holding a vision model -> text back + signed receipt.
Models seen 2026-10-25:
- PC (ollama): qwen2.5vl:3b (VISION), qwen2.5:7b, qwen2.5:7b-instruct-q8_0, qwen2.5-coder:7b, deepseek-r1:14b, deepseek-r1:1.5b, gemma2:2b, gemma:2b, athena-class, Ternary-Bonsai-2-27B. => PC is the vision node (MAG_RELAY_VISION_MODEL=qwen2.5vl:3b).
- Pixel (ollama, server not running): qwen2.5, qwen2.5:3b-instruct (no vision).
- T90, Moto: no local ollama models; hermes CLI only.
- Bob: switchboard, no models (3.4 GB RAM).
`ask_frontier`: NOT implemented. Would route to a node whose hermes lane already has a frontier provider configured; no paid keys added. Pending owner decision on which lane counts as frontier.

## Run (foreground only, no autostart)
`MAG_RELAY_HOME=~/.mag_relay python mag_relay.py serve --node t90 --bind 100.72.38.3`
`python mag_relay.py call --node bob --to t90 --url http://100.72.38.3:8765/mcp --tool read_chain_head --args "{}"`

## Auto-router (2026-10-25, 11:40-12:00 EDT)
Files: `router/router.py`, `router/routing_rules.json` (deployed on Bob at `C:\Users\etfag\mag_relay\router\`). Rules are data; edit the JSON, not code.
- New allowlisted relay tool `health`: free_mb, battery, charging, running jobs, ollama models, vision model, hermes primary/fallback config, and key env NAMES only (never values).
- `submit_task run:true` now uses `hermes chat --query-file` (no quoting issues), optional `provider`/`model` from an allowlist, and returns `provenance` parsed from the hermes `agent.log` lines written during the run: every endpoint attempted (provider, base_url host, model), fallback events, 404/429 errors, final model.
- Router flow: classify (tokens, vision, browser, gpu, frontier, latency) -> health from each eligible node over the signed relay -> gates (retired/never_route, Pixel paid-backup gate, RAM, battery <30% unless charging, one job at a time) -> pick -> dispatch (`submit_task run:true` + `get_result`, or `describe_image` on PC) -> stamped reply `[routed node=.. provider=.. host=.. model=.. | FALLBACK HAPPENED: chain | cause]`.
- Browser jobs: PC only, never Bob; if PC is down the job is queued in `router/queue/` and the reply says so.
- No spend: hermes jobs pinned to `nous-nacho` + `poolside/laguna-s-2.1:free` (`hermes_pin`). Node config fallbacks to paid deepseek can still fire if the free model fails; that is stamped.
- Every decision is appended to Bob's relay ledger (`state/relay_ledger_bob.jsonl`, kind `route`, outcomes dispatch/done/queued), hash-linked.
- PC relay port is 8766 (8765 on PC is held by a Windows svchost). Kill switch: `STOP` file in each node's `~/.mag_relay/` and in `router/`; `router/stop_router.ps1` sets all of them.
- ZAI lane: wired in rules (`lanes.zai`, provider `zai`, base `https://api.z.ai/api/coding/paas/v4`); activates per phone only when health shows one of ZAI_API_KEY/GLM_API_KEY/Z_AI_API_KEY/ZHIPUAI_API_KEY. None present on any node today.
- mag-openclaw: status retired (rules and hermes_fleet/devices.json).
