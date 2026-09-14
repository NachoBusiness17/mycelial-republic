# LANE 1/8 — API ENDPOINT SWEEP: DeepSeek-V4.1-Flash
Date: 2026-09-10 | Seat: zcode (Sancho), triparty lane 1 of 8 | Method: web fetch probes, no keys echoed, no code changed. Tri-state marks on every claim.

## THE POINT
DeepSeek officially serves V4.1-Flash only under the id `deepseek-flash` — 1M context, $0.15/$0.60 per M off-peak, and cache-hit input drops to $0.003/M, so the primary lane is real but paid. Of the four free endpoints posted today, only OrcaRouter verifiably lists `deepseek/deepseek-v4.1-flash` at exactly official off-peak rates on a free-forever plan; xplabs serves `deepseek-v4-flash` even cheaper via open-weight hosts (consistent with the MIT weights), apinex's catalog is unreadable to fetch, and tokenharbor has no DeepSeek at all. Assignment: official off-peak for anything judgment-adjacent, OrcaRouter as overflow only after a served-model identity probe passes — the ractor strike names the exact hole ("the model you get is whatever the probe can't see").

## ENDPOINT TABLE

| Endpoint | Model id | $/M in (miss) | $/M out | Context | Limits | Status | Fits fleet lane |
|---|---|---|---|---|---|---|---|
| **api.deepseek.com** (official) | `deepseek-flash` (= V4.1-Flash; legacy `deepseek-v4-flash[-vision-exp]` still accepted, same price) | peak $0.30 / off-peak $0.15; cache-HIT in: $0.006 peak / $0.003 off-peak | peak $1.20 / off-peak $0.60 | 1M in, 384K out | 2500 concurrency; peak = 01:00–04:00 + 06:00–10:00 UTC Mon–Fri; vision + FIM on flash | SUPPORTED (docs) — `/models` returns 401 unauth, needs key | **Primary paid lane**: judgment + grounding work fired off-peak; cache-mining shape fits our refeed pattern |
| **orcarouter.ai** | `deepseek/deepseek-v4.1-flash` | $0.15 | $0.60 | 1M | Hacker plan: free-forever, 3 keys, 0% markup, auto-failover; no numeric rate limits published; base `https://api.orcarouter.ai/v1` (OpenAI-compatible) | SUPPORTED (listed) / UNPROVEN (live serve) | **Overflow/burst lane** after identity probe passes; prices match official off-peak exactly — consistent with honest relay, not proof of one |
| **platform.xplabs.ai** → experientiallabs.ai | `deepseek-v4-flash` (V4.1 id NOT seen; 37 DeepSeek models total) | $0.042 (cheapest route shown) | $0.085 | 1.05M, cache | 131 tok/s, 6.5s TTFT, 100% uptime claimed; providers: Experiential Cloud / Fireworks / Azure Foundry; rate limits unpublished | DISPUTED for V4.1 specifically (serves V4 Flash; open-weight hosting, swap risk lower but real) | **Cheapest per-token** if the legacy id routes to V4.1 weights — probe later |
| **apinex.bond** | unknown | catalog says "12 models from $0.07/1M" | — | — | — | UNPROVEN (JS-rendered catalog, DeepSeek presence unconfirmed by fetch) | Skip until catalog readable |
| **tokenharbor.ai** | none | — | — | — | 9 models: Anthropic/OpenAI/Zhipu/Grok/Kimi/Qwen only | DISPUTED→NO for this model | Skip — does not serve DeepSeek |

## OFFICIAL ECONOMICS DETAIL (api-docs.deepseek.com/quick_start/pricing)
- Off-peak = half of peak, all hours except 01:00–04:00 and 06:00–10:00 UTC Mon–Fri. Our night waves (US evening = low-UTC) mostly land off-peak.
- Cache-hit input at $0.003–0.006/M makes refeed-heavy workloads near-free on the official lane — the same economics shape that made glm-4.7-flash our cache lane.
- V4 Pro retires 2026-09-14 12:00 Beijing: all `deepseek-v4-pro` traffic reroutes to V4.1-Flash — expect capacity pressure to RISE on flash after that date; grab the lane early.

## RACTOR STRIKE (ELLUL mask, deepseek-v4-flash, 2.1s)
"free endpoint, provider-direct pricing, no key echo — all pass. the model you get is whatever the probe can't see."
→ Missing falsifier named: served-model IDENTITY. An echo/refusal probe passes even under silent model swap. Before any fleet traffic crosses an aggregator, run a canary the relay can't cheaply fake (behavioral fingerprint unique to V4.1-Flash, tokenizer quirks, logprobs presence). Fold into the lane probe fixture like the error-banner fixture on game pages.

## RECOMMENDED LANE ASSIGNMENT
1. **DS_FLASH (new fuel_feed lane, paid)** — api.deepseek.com, id `deepseek-flash`, off-peak windows only, cache on. Judgment-adjacent bulk (interpret, critique, ractor vessels).
2. **ORCA_FLASH (overflow, gated)** — orcarouter.ai Hacker plan, id `deepseek/deepseek-v4.1-flash`, only after canary probe passes; cap at burst lanes (groups of five-to-eight shape).
3. **XPLABS (parked)** — probe `deepseek-v4-flash` id when a lane opens; cheapest published rates, open-weight hosts.
4. **SKIP** — tokenharbor (no DeepSeek), apinex (unproven catalog).

Sources: api-docs.deepseek.com/quick_start/pricing; api.deepseek.com/models (401 unauth probe); orcarouter.ai; platform.experientiallabs.ai (via 308 redirect); apinex.bond/models; tokenharbor.ai/models. Fetched 2026-09-10 ~15:3xZ.
