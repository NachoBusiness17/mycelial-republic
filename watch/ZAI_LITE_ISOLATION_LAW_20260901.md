# Z.AI LITE ISOLATION LAW — 2026-09-01 (operator-authored, 06:28Z + 06:42Z docs digest)

Source: operator RTFM digest of official docs (docs.z.ai/devpack/overview, api-code,
quick-start). This file is the cage-side enforcement of that digest. Law, not advice.

## The 7 points, operationalized on this cage

1. **Coding endpoint only.** z.ai coding-plan keys touch `api.z.ai/api/coding/paas/v4`
   (or anthropic-protocol `/api/anthropic`) — never general `paas/v4` (that's PAYG,
   different keys, different billing).
2. **One concurrency slot by default.** z.ai lens lanes run SEQUENTIALLY in salons —
   never in a parallel family batch. The 05:55Z salon's simultaneous
   lessig/ellul/bernays spawn set violated this; bernays' FailoverError x2 was the
   1302/1313-class consequence, not provider flakiness.
3. **No automatic fallback into Lite.** If a z.ai lane fails, fail over to DeepSeek
   (funded) or another family — never retry-loop the Lite slot.
4. **No swarm fan-out through Lite.** Parallel spawn batches route to DeepSeek paid /
   other families. Lite carries at most ONE active lane; salon design puts z.ai last
   or sequential.
5. **Heavy/high/max work → funded lanes.** DeepSeek v4-pro (T2 judge/synthesis,
   $24.13 invoiced) + the two PAYG accounts (fostertron $9.99, nacho $25 —
   operator-attested 06:28Z) once their standard keys are wired. GLM-5.3 non-flash
   (Max tier) stays parked till the 09-08 weekly reset regardless.
6. **Per-request telemetry row (every z.ai call):** {ts, key_fp, model, credits_est,
   cached_in, out_toks, http_code, biz_code, reset_hint} → /board/meter_readings.jsonl.
   This is M0's row schema — adopted now, not when the cron exists.
7. **Dashboard = exact limits.** The authenticated rate-limit dashboard
   (z.ai/manage-apikey/rate-limits) is truth for account-specific numbers; my endpoint
   probes give pool state, not exact concurrency ceilings. Never guess limits from
   model docs when the dashboard can answer.

## Credit-weight facts that change salon design (from the digest)
- Formula: (in×m + cached×m + out×m)/10,000 — GLM-5.3: 6.9/1.7/24; flash: 2.3/0.56/8.
- Repeated context is cheap (cached 1.7 vs 6.9) — frozen-prefix cache-mining law confirmed
  by pricing, not just measurement.
- Long parallel agents drain Lite fast → Lite is for single-lane, sequential, flash-class
  work. That is its identity on this cage.
- Peak 14:00–18:00 SGT (= CST offset; identical wall clock to our BJ windows). Off-peak
  = 50% credits. Weekends off-peak.

## Accounts map (attested by operator 06:28Z)
| Account | Cash | Type | Wired? |
|---|---|---|---|
| nacho | $25.00 | z.ai PAYG (standard key needed) | NO — coding keys can't touch PAYG |
| fostertron | $9.99 | z.ai PAYG (standard key needed) | NO — unused lane, the parallel-models launcher |
| deepseek (nacho) | $24.13 invoiced 06:09Z | API PAYG | YES — funded, in rotation |

## Enforcement hook
These 7 points are the FIRST REAL ROWS of the temporal-authority gate table
(see SALON_RIGHT_TIME_SYNTHESIS_20260901.md): scope=zai-lite, action=deny on parallel
fan-out; scope=heavy-work, route=funded-lane; telemetry row schema = the meter contract.
Operator law predates the organ — the organ formalizes what this file already commands.


## AMENDMENT (06:56Z, config audit + operator digest 06:45Z)
- RETRACTION: the 08-29 belief "coding-plan keys structurally refuse paas/v4" was tool-context-specific (opencode UA guard), not universal — OpenClaw calls to paas/v4 with coding keys SUCCEED and bill an unknown (likely cash) pool. Rule 1 was being violated by 4 of 5 providers in live config. Audit: only zai-2 on coding endpoint; zai/zai-lite/glm53-api/zai-pro on paas/v4.
- Enforcement: fix staged as /board/inbox/PROVIDER_ENDPOINT_PATCH_20260901.json (protected paths — operator applies). zai-lite + glm53-api → coding endpoint immediately; zai + zai-pro become PAYG arms when standard keys land (ZAI_PAYG_NACHO_KEY / ZAI_PAYG_FOSTERTRON_KEY).
- REASONING-TIER ROUTING LAW (operator 06:45Z): flash low = routine; flash high = important implementation/debugging; flash max = bounded long-horizon jobs only. Thinking is FORCED on flash (default max if omitted) — cost control = pass explicit low/high.
- METER LAW M-L1 (operator 06:45Z): NEVER infer account balance from a successful API call. A 200 proves service, not solvency. Balances come from balance endpoints, quota endpoints, or the dashboard — labeled by grade.
- UNKNOWN list honored (no fixed RPM/TPM for Lite, no exact concurrency, tool-call credit accounting unclear, no independent benchmarks) — dashboard + biz error codes are the source of truth.
