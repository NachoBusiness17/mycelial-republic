# GSTD DESKTOP BUILD-OUT - tunnel, wire, NAAS call, smoke - 2026-10-09

Operator order: "build out the gstd shit on the desktop and make everything
work and test it a bit." Carried by the GSTD BUILD-OUT lane. Code read before
every change (byte-first law). No wallet bytes touched.

## 1. Registration surface read (what the node registers as)

- `src/core/platform-link.ts`: `register()` POSTs `public_url` to
  `platform.../api/v1/nodes/register`; value = `/tmp/gstd_tunnel_url.txt`
  (read fresh, INSIDE the container) with fallback `process.env.GSTD_PUBLIC_URL`.
  `sendHeartbeat()` re-reads the same and sends `node_url` only when truthy.
  File beats env. The file is re-read every cycle, so a docker exec write of
  /tmp/gstd_tunnel_url.txt refreshes the URL with NO container restart.
- `src/index.ts:513` : `GSTD_PUBLIC_URL` also derives the P2P `wsAnnounceHost`
  (wss rides the same tunnel, no extra port). Confirmed live in logs:
  "P2P Peer Manager started. Public URL: https://procurement-...trycloudflare.com".
- Does the platform route TASKS to the full node gateway? YES:
  `src/gateway/server.ts:4568` exposes `POST /api/v1/tasks/push` (M4
  push-primary; the platform pushes a task, node runs it on Ollama, POSTs
  result to `/api/v1/tasks/complete`). Fallback poll loop lives in
  platform-link.ts (`/api/v1/tasks/poll`, 30s). The Pi census evidence (only
  task-earner on the platform runs a trycloudflare node_url) matches: the
  public URL is what makes push routing possible.
- Platform truth before this window: gstd-desktop registered with
  `node_url: ""` (empty), 15 capabilities, tasks_completed 0.

## 2. Tunnel (cloudflared quick tunnel)

- cloudflared was ALREADY INSTALLED: `C:\Program Files (x86)\cloudflared\
  cloudflared.exe`, version 2026.8.2. No winget, no download needed.
- Started quick tunnel as a background host process:
  `cloudflared tunnel --url http://localhost:8080 --no-autoupdate`,
  log `logs/gstd_quicktunnel.log` (repo logs dir).
- URL captured from log: `https://procurement-unto-porcelain-baghdad.trycloudflare.com`
- Verified from outside: `curl` tunnel `/health` -> `{"status":"ok",
  "version":"3.5.0",...,"swarm":{"peers":0,"models":10}}`.
- NOTE: trycloudflare quick-tunnel URLs are EPHEMERAL. If cloudflared dies or
  the host reboots, a NEW URL is minted and the pinned one goes stale.
  Persistence = named tunnel (needs a Cloudflare account decision) or a
  compose sidecar mirroring `reference/gstdcoin/gstdbot/tunnel.sh`. Operator
  call, deliberately not improvised here.

## 3. Wire (GSTD_PUBLIC_URL into the override)

- Appended `GSTD_PUBLIC_URL=https://procurement-unto-porcelain-baghdad.trycloudflare.com`
  to `reference/gstdcoin/gstdbot/docker-compose.override.yml` (with a comment
  naming the ephemeral nature and the no-restart refresh lever). Wallet env
  and wallet bind-mount untouched.
- `docker compose up -d --force-recreate` in the gstdbot dir: Recreated,
  Started, healthy within ~30s. Boot log: "Platform Link: node registered
  (gstd-desktop)".
- Also wrote the same URL into the container file (code reads it FIRST):
  `docker exec gstd-node sh -c 'echo -n <url> > /tmp/gstd_tunnel_url.txt'`.
- Verified on the platform API: gstd-desktop `node_url` now
  `https://procurement-unto-porcelain-baghdad.trycloudflare.com`
  (was empty this morning). Registration public_url carried it on boot.
- Observation vs the P1 receipt: this build's PlatformLink heartbeat interval
  logs as 600s ("heartbeat every 600s"), UptimeDaemon also 600s
  (HEARTBEAT_INTERVAL_MS = 10 min, KV write budget). The "60s heartbeats"
  phrasing in the P1 receipt does not match this build's logs.

## 4. NAAS decision: OFF (not enabled)

- Code read: `GSTD_NAAS_ENABLED=true` (src/index.ts:377) starts
  `NaaSManager` (src/naas/orchestrator.ts), which is Multi-Chain RPC
  Node-as-a-Service: detects hardware, launches BLOCKCHAIN chain-node docker
  containers (2 CPU / 4GB each) via docker-in-container, starts an RPC proxy
  on :9000, starts a revenue flywheel, and registers the node as a NaaS
  PROVIDER using the wallet address as the Bearer api key.
- It is NOT the task/inference serving lane. The inference lane (gateway
  /v1/* routes, swarm task loop, /api/v1/tasks/push) and the uptime rewards
  (UptimeDaemon, src/naas/uptime_daemon.ts) run WITHOUT any NAAS env;
  UptimeDaemon starts unconditionally in node mode (index.ts:638).
- Why OFF: it changes the risk and payout shape (provider registration keyed
  to the payout wallet, chain containers, a second revenue flywheel) and its
  container-launch leg cannot work inside our node container anyway (no
  docker socket; `docker info` fails, roles get skipped with a warn). Mission
  rule: ambiguous or payout/risk-changing -> leave off and file. FILED.
- Operator question parked: if multi-chain RPC earning is ever wanted, it
  needs its own cage (docker socket mount or sidecar), its own review, and a
  separate payout-risk ruling. Not this window.

## 5. Smoke test (test it a bit): PASS, three round trips

Auth note: the gateway's /v1 inference routes have NO auth gate (rate limit
120 req/min per IP; pinAuth on /health refers to dashboard session routes
/api/auth/*). No pin needed for inference. Rate limiter verified live (429s
observed, see finding below).

a) Direct Ollama passthrough from INSIDE the container (clean rate bucket):
POST /v1/ollama/completions {"model":"gemma:2b","messages":[{"role":"user",
"content":"Reply with exactly: GSTD node alive"}],"max_tokens":12}
-> 200 {"model":"gemma:2b","content":"GSTD node alive","usage":
{"prompt_tokens":30,"completion_tokens":5,"total_tokens":35}}
Total 5.82s (first hit includes gemma:2b load; only qwen2.5:7b is pre-warmed).

b) Same endpoint THROUGH THE TUNNEL (outside-in proof), first attempt after
the storm eased:
-> 200 {"model":"gemma:2b","content":"Sure. The tunnel path is alive and
active. It'","finish_reason":"length"} with 14 cached_tokens (keep_alive
working). Total 0.54s.

c) GSTD router path through the tunnel: POST /v1/chat/completions
{"model":"gemma:2b","messages":[{"role":"user","content":"Say: router ok"}],
"max_tokens":10} -> 200 {"model":"gemma:2b","content":"Router OK","_gstd":
{"tier":"gstd","sovereignty":true,"latency_ms":4895}}. Total 5.31s.

Verdict: the garden (Ollama on the host) serves THROUGH the node gateway,
locally and through the public tunnel, on both the passthrough and the
sovereign-router shapes.

## 6. Longrunner law rows

`configs/longrunner_policy.json`:
- Tier A_caged_by_default: added gstd-node row (compose service; memory cap
  Memory=536870912 VERIFIED by docker inspect; docker compose only control
  surface; alerts-never-kills posture spelled in the row).
- Added dated amendment object `gstd_tunnel_amendment` (2026-10-09): the
  bare-host quick-tunnel cloudflared is a this-sitting exception, not in
  watch_process_names so the patrol never kills it; persistent form is an
  operator call; stale-URL refresh lever documented.
- JSON re-validated after edit (parses, 8 A rows).

## 7. Findings, failures, untested surfaces (honest)

- RATE-BUCKET COLLAPSE BEHIND THE TUNNEL (finding, not fixed): within 26s of
  the URL going public, the gateway rate limiter logged "Rate limited:
  172.20.0.1 (124 req/min)". 172.20.0.1 is the docker bridge gateway: ALL
  host-originated traffic INCLUDING every cloudflared-forwarded external
  request lands in ONE per-IP bucket (the gateway reads socket IP, no proxy
  header trust), and unattributed external traffic (platform probes or
  trycloudflare scanners; I did not verify which) ate the 120/min budget.
  Effects: two of my probes 429ed (one localhost /health, one tunnel POST)
  before succeeding on retry. Not papered over with a code change: trusting
  CF headers is an upstream-code decision. If task starvation is ever
  observed, that is the first place to look.
- Heartbeat cadence is 600s in this build, not 60s (see section 3).
- UNTESTED SURFACES (named, not claimed):
  - A real platform-dispatched TASK through /api/v1/tasks/push (platform's
    routing choice; push lane verified by code read + registration, not by a
    live task; tasks_completed still 0 at receipt time).
  - Dashboard pin auth (/api/auth/setup, session flow) - never exercised.
  - /api/v1/free-api/* key issuance - never exercised.
  - P2P mesh dial-in over wss through the tunnel (peers still 0).
  - Fastify engine on internal 8081 - untouched.
  - NAAS - deliberately off (section 4).
  - Named tunnel / tunnel persistence - operator call (section 2).
- Tunnel process is a background host process from this sitting; if it dies,
  node_url goes stale until refreshed (docker exec write of
  /tmp/gstd_tunnel_url.txt is the no-restart lever; override edit + recreate
  is the durable one).

## Files touched

- reference/gstdcoin/gstdbot/docker-compose.override.yml (GSTD_PUBLIC_URL + comment)
- configs/longrunner_policy.json (A row + gstd_tunnel_amendment)
- watch/inbox/gstd_desktop_buildout_20260109.md (this receipt)
- logs/gstd_quicktunnel.log (tunnel log, new)

Context receipts: watch/inbox/gstd_p1_fired_20260109.md,
watch/inbox/GSTD_WALLET_DOOR_20261007.md.
