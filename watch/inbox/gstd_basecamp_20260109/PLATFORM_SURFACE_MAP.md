# GSTD PLATFORM SURFACE MAP - every skin, and where we came from - 2026-10-09

SURFACE lane (operator: "touch every part of it and see where you came
from"). Read-only GET probes, 28 endpoints: 12 platform, 1 tunnel, 15
gateway. All moments UTC (docker/host clock); probe window bounded by the
data itself: the /api/v1/nodes fetch carried last_seen 04:35:24Z, final
probe 04:47Z. No POSTs, no auth poked, no writes anywhere.

## 1. Platform API (platform.gstdtoken.com) - the world's skin

- GET /api/v1/nodes -> 200, shape {"nodes":[{...}],"count":5}
- GET /api/v1/health -> 200, {"status":"ok","service":"gstd-platform"}
- GET /api/v1/tasks/poll -> 200, {"task":null} - GET answers; our node
  POSTs this same path in its 30s fallback poll loop (platform-link.ts)
- GET /api/v1/tasks -> 404 {"error":"not found"}
- GET /api/v1/stats -> 404
- GET /api/v1/leaderboard -> 404 (the roster IS the leaderboard, see 5)
- GET /api/v1/nodes/gstd-desktop -> 404, no per-node lookup route
- GET /api/v1/wallet/<our-addr> -> 404, no wallet lookup route
- GET /api/v1/nodes/register -> 404 on GET (POST-only, platform-link.ts)
- GET /api/v1/tasks/complete -> 404 on GET (POST-only, result lane)
- GET / and /nodes -> 404 JSON: NO web frontend exists, API-only host

Public truth: two live GET data routes (nodes, health) plus the poll.
Everything else on the platform is POST ingestion from nodes.

## 2. Our public record, verbatim (GET /api/v1/nodes, at/after 04:35:24Z)

- node_id: "gstd-desktop", name: "gstd-desktop", version: "3.5.0"
- wallet_address: UQAcDahtjR7... (truncated; 48 chars on the wire)
- node_url: https://procurement-unto-porcelain-baghdad.trycloudflare.com
- capabilities (15): qwen2.5:7b-instruct-q8_0, gemma2:2b-instruct-q5_K_M,
  gemma:2b, Ternary-Bonsai-2-27B, athena-class, qwen2.5:7b,
  deepseek-r1:1.5b, qwen2.5vl:3b, qwen2.5-coder:7b, qwen-desk,
  qwen2.5:3b-instruct, gemma4-desk, gemma4, gemma4-hermes,
  nomic-embed-text (full tags on the wire, shortened here)
- tasks_completed: 9, gstd_earned: 0.091556
- last_seen: 1791520524 = 2026-10-09T04:35:24Z
- registered_at: 1791518610 = 2026-10-09T04:03:30Z
- reputation_score: 59, avg_response_ms: 1698, early_adopter: 1
- Roster peers (same fetch): GSTD Bootstrap Pi (288 tasks, 51.4376 GSTD,
  registered 2026-08-28T20:52:36Z), LAPTOP-UTO92FB9-node (4.7346 GSTD),
  "unknown" (no wallet), localhost-node (0.3444 GSTD). Count 5.

## 3. Origin trace

- The network's memory of our arrival: registered_at 2026-10-09T04:03:30Z
  (/api/v1/nodes). This PREDATES the current container start
  (started_at 2026-10-09T04:15:13.376Z, GET :8080/api/node/status) by 12
  minutes: the registration survived a container restart, and the
  platform's counters (9 tasks, 0.0916 GSTD) outlive every reboot.
- Current container's first registration line (docker logs gstd-node,
  log starts 04:15:14Z, this restart's boot):
  "2026-10-09T04:15:20.810961054Z  Platform Link: node registered
  (gstd-desktop)" (emoji prefix omitted, verbatim otherwise)
- Heartbeat cadence in-log: "heartbeat every 600s ->
  https://platform.gstdtoken.com" (04:15:20.810998956Z)
- Tunnel still standing: GET procurement-...-baghdad.trycloudflare.com/health -> 200 in 0.28s

## 4. Our gateway (localhost:8080) - the body's own skin

- Route table (grep src/gateway/server.ts): 151 registrations,
  81 GET + 68 POST + 2 DELETE. Families: /v1/* inference (models, chat
  completions, ollama passthrough, sovereignty, skills, swarm/status),
  /api/node/* telemetry GETs vs control POSTs (control, restart, stop,
  update), /api/auth/* pin sessions, /api/v1/tasks/push POST (line 4568,
  the platform push lane) + /complete, /api/storage/* IPFS pins,
  /api/apps/* store, /api/validators/*, /api/ssl/*, /api/dns/*,
  /api/system/* (reinstall/reset: POST, never poked), /api/oracle/*.
- GET probes, 13 x 200: /health (swarm peers 0 models 10), /v1/models,
  /v1/sovereignty (index 100, 11 requests: cache 3 swarm 8),
  /v1/skills (0), /v1/swarm/status (heartbeat 600s, rank field),
  /api/peers (same 15 capabilities), /api/node/status (ip 172.20.0.2),
  /api/swarm/models, /api/node/earnings (local zeros, reset on restart),
  /api/node/platform (registered true, lastHeartbeat 04:45:21Z,
  failCount 0), /api/node/tasks (0/0/0), /api/node/rating (score 58/100,
  tier silver, multiplier 1.5, models 48/48, activity 10/32, uptime
  0.5h -> 0/20), /api/node/usage/recent (empty)
- 429 x 2: /api/fees, /api/node/overview -> "Too many requests" at
  ~04:44Z - the standing rate-bucket collapse (all traffic shares the
  172.20.0.1 bridge bucket, 120/min); 10 gentle GETs shared it with
  tunnel traffic. Probed-not-poked stands.
- No .ws() routes in server.ts (P2P wss rides index.ts announce). No
  8081 listener in src or netstat, only 8080 - the buildout receipt's
  "Fastify engine on internal 8081" matches no code in this tree.
- Discrepancy banked: /health says swarm.models 10 vs 15 capabilities on
  both /api/peers and the platform record (different counters, unnamed).

## 5. What the body can feel (daily chartable)

- platform /api/v1/nodes: gstd_earned, tasks_completed,
  reputation_score, avg_response_ms, last_seen - for us AND all peers;
  one fetch is the whole leaderboard
- gateway /api/node/rating: score/tier/multiplier + breakdown; the
  uptime component (0/20) grows with node age, the honest aging curve
- gateway /api/node/platform: heartbeat freshness + failCount
- docker logs: task completions stream (9 tasks 04:17-04:40Z, all
  gemma:2b, 9-248 chars) and uptime rewards (+0.000083 GSTD per 600s)
- Truth split: local counters reset on restart, the platform is the durable ledger; chart from /api/v1/nodes, alert from logs.
