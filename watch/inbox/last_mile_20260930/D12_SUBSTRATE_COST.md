# D12_SUBSTRATE_COST — standing infrastructure cost vs value (2026-09-30)

Fence owner: D12 seat. Instruments named per census-denominator law: `docker ps -a` + `docker stats --no-stream` + `docker top` at ~19:05 EDT; `Get-Process`/`Get-CimInstance` at ~18:55 EDT; live CPU deltas sampled over 6.0s wall at ~19:07 EDT; `Get-ScheduledTask`+`Get-ScheduledTaskInfo` at ~18:56 EDT; container logs counted via `docker logs ... --since 24h`. Host: 32 GB RAM. All CPU% figures are one-moment samples; CPU-s figures are process-lifetime accumulations.

## 1) Enumeration (what is standing right now)

| # | unit | cost (measured) | produced, last 24h (bytes) |
|---|---|---|---|
| 1 | ZCode seat fleet, 21 proc | 4,500 MB RAM; funded tier (subscription, $0 metered — COST_TRUTH §1) | 150+ receipts in `watch/inbox/last_mile_20260930/` alone (AA→B18, IMP, LM, V, W waves), all file-dated 09-30 |
| 2 | Hermes stack (gateway 89 MB + serve 205 MB + desktop renderer 403 MB), ~5.2 CPU-h lifetime | ~700 MB RAM | dispatch ACTIVE today: CYCLE_BRIEF rows `2026-09-30T22:09:31Z` + `22:46:30Z` hermes-executed; `logs/mates/dispatcher_20260930.log` |
| 3 | ollama serve (host eye) | 37 MB, `ollama ps` = EMPTY (no model resident, no VRAM held) | janitor tier on demand; 0 calls observed in this window |
| 4 | stealth_driver + fanout (free lanes) | ~0 local CPU; free-lane quota only | 20 files banked 24h in `watch/inbox/burn_reset_20260927/work/` (kabbalah-epistemics, nelson-shuffle × openrouter1-3 + hermes-verify); loop confirmed live (proc start 19:05 EDT, 300s cycle, no `.off` flag) |
| 5 | mag-sovereign (restarted 18:49:58 EDT today) | **1.47 GB RAM, 135% CPU sustained**; 8 children (`docker top` avg since start): drainer 45%, synthesis 25%, ghost 21%, lab 19%, dashboard 15% | drainer = 38,893 `[swarm-grok-watch] WATCHING (2/12 fail)` spam lines in 5.6 MB `logs/drainer_sv.log`, zero drained work visible; dashboard served only its own healthcheck (`GET /` every 15s ≈ 5,760 self-probes/day; api_gateway log = 15 requests total); synthesis output = `48h_synth/` (09-29/30, real) |
| 6 | mag-redis | 13.6 MB, 0.55% CPU | dependency enabler for #5/#8 |
| 7 | mag-mcp (archivist bridge) | 38.6 MB, 0.00% CPU | **2,854 sessions/24h ≈ the container's OWN healthcheck cadence** (30s interval → 2,880/day theoretical; ≈26 non-self sessions max). Self-probe churn spawns an mcp_server subprocess per probe |
| 8 | mag-worker (drain beat) | 30.3 MB, beats every ~75s since 08-27 | 10,418 beats lifetime: **9 items EVER drained** (20,759 `done:0` result lines vs 9 `done:1`). 0 today |
| 9 | run_armC.py zombie (PID 42364, `memory/runs/interference_replication_20260925/`) | **72.4 CPU-h lifetime, 0.71 core burning RIGHT NOW** (4.27 CPU-s / 6.0s wall) | newest output file 09-27 05:44; run log = 40 bytes (`budget=200 [1/30] solved=True`). ZERO bytes in 3+ days |
| 10 | loving_driscoll container | `Created`, never started (playwright image, created 18:47 EDT) | nothing; dead weight |
| 11 | Scheduled task fleet: MagCensusPatrol, MagCorpusRescan, MagFtsIndex, MagImprove, MagGapSentinel, MagGateCanary, MagEndpointNews, MagVision, MagQCaption, MagSecretScan, EstateWalk, mag-docker-watchdog | seconds of CPU each, daily | rescan +15,207 corpus rows today; census patrol exit=1 (flagged drift = job working); FTS fresh 0.5s; improve wrote `memory/improve/latest.md` today 14:22; canary snapshotted 41,588 paths. **Flagged: MagXRadarDaily exit 2 (cannot-verify incident per B2-246 law); MagLeaveProtocolDaily result 0xFFFFFFFF (never completes)** |
| 12 | OUT OF BOUNDARY (fle_u1 project, same machine): `inspect.exe eval` PID 556 **78.8 CPU-h lifetime, 0.93 core live**; cluster-factorio_0-1 19.7% CPU / 202 MB, up 28h | ~1.1 cores + 326 MB standing | not Mag's ledger — operator decision |

Standing Mag-attributable RAM ≈ 7.1 GB / 32 GB; standing Mag CPU ≈ 2.1 cores (sovereign 1.35 + armC 0.71 + scraps) + seats on demand.

## 2) Classification

**LOAD-BEARING (5):** ZCode seats · Hermes stack · daily-task fleet + docker-watchdog · ollama (dormant-cheap, $0 when idle) · stealth fleet — CONDITIONAL, see §4.

**DISPLAY (3):** mag-sovereign (dashboard/ghost/lab serve self-probes and on-demand eyes; the drainer child is spam, not display — that part is waste) · mag-mcp (transport on demand; 99% of its traffic is its own healthcheck) · mag-redis (pooled dependency, near-free).

**IDLE (3 + 2 out-of-boundary):** mag-worker (0.09% useful beats) · run_armC zombie (the single biggest Mag-attributable waste: 72 CPU-h for a 40-byte log) · loving_driscoll (never-started container). Out of boundary: fle_u1 eval + factorio (1.1 cores).

## 3) Minimization plan (drop / pool / keep)

1. **Kill run_armC NOW** (`taskkill /PID 42364`): saves 0.71 core; IMP8 already holds the replication receipt this run was feeding. Re-launch only as a bounded scheduled run when a consumer exists.
2. **mag-worker → on-demand:** `docker compose stop worker`; if its queue is the same queue the sovereign drainer watches, the beat is redundant — fold into a 10-min scheduled drain or delete the service after 7 empty days.
3. **mag-mcp:** healthcheck 30s→120s (self-probe 2,854→~700/day), or have the bridge spawn mcp_server only after a first MCP handshake byte, not on TCP accept.
4. **mag-sovereign:** split dashboard/ghost/lab behind a `--profile ui` (on-demand); keep backend/api/lanes always-on. Cap the drainer's grok-watch at exponential backoff (38,893 identical lines is log-spam cost, not sensing).
5. `docker rm loving_driscoll`.
6. EstateWalkDaily → weekly unless a consumer opens `estate_walk.html` this week (1.8 MB display artifact, detail-inert-until-open).
7. Fix or remove MagLeaveProtocolDaily (0xFFFFFFFF); MagXRadarDaily exit 2 is an OPEN incident under the B2-246 law — inspect `logs/x_radar_backfill/`, do not ignore.
8. Opencode daemons: **NONE running** (verified 0 matching processes; the mission's "8 daemons" premise is stale). 4 node procs / 79 MB are harness-owned. No pooling action available.
9. fle_u1 pair (1.1 cores): operator call, outside this repo — reported, not acted on.

## 4) The honest stealth-fleet answer

The fleet is cheap and producing (20 files/24h at $0), so it is NOT the waste. The missing organ is the READER: SNOWBALL_PLAN C3 already names it — "B13's manual triage becomes a cycle_brief stage... the stealth fleet stops being write-only" — and today's CYCLE_BRIEF line 30 still carries "run the full B13 method on today's tail" as an unexecuted TODO. So: fleet = load-bearing sensing surface held back by an unbuilt triage stage; land C3 (top-5 actionable findings/day into the cycle brief, rib-contradictions to attention.md) before adding any new sensing. Verdict stands until triage runs for 3 consecutive days.

## 5) Verdict line

5 load-bearing / 3 display / 3 idle (+2 out-of-boundary). Biggest waste: run_armC zombie — 72.4 CPU-h, live 0.71 core, zero output since 09-27. Second: mag-sovereign's drainer spam loop. The fleet's problem is the missing triage organ, not the fleet.
