# D22 — PROVIDER PROBE 2026-09-16

- **Lane:** D22 (ops: providers re-probe — feeds the wave's rotation)
- **Operator:** wave agent, free-tier only, $0 budget
- **Wave-lane law:** receipt first, append as you go, no git.
- **Baseline (salon lane tonight):** alive = groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, zai-air, or-nemotron, or-ling3; dead = groq-qwen, mistral-small (429), or-glm52 (502), zai-47 (PAID WALL — do not retry).

## Method

- Registry: `mag/research_fanout.py` `LANES` (12 lanes; groq ×3, cerebras ×2, mistral ×2, z.ai ×2, openrouter ×3). Probe method: module's own `probe_lanes()` — one minimal call per lane, prompt "Reply with exactly: READY", 45 s timeout, `max_tokens` 2600 (reasoning models burn the budget in a reasoning channel first), failures preserved as rows. **No code edited** — imported the module, runtime-filtered the in-memory lane list.
- Excluded by mission order: `zai-47` (PAID WALL — do not retry). Not probed, not retried.
- Keys read from `.env` (names verified present, values never printed): GROQ_API_KEY, CEREBAS_API_KEY, Mistral_API_KEY, ZAI_API_KEY, OPENROUTER_API_KEY. (`CEREBAS_API_KEY` is the real env name — registry matches, not a typo.)
- Pass 1: `probe_lanes()` → alive/dead + latency + error class.
- Pass 2: per-provider free `GET /models` (un-metered) to read rate-limit headers → quota-headroom signals; plus ONE classified retry per dead lane to capture 429 body / retry-after (rate-limit class only).
- Interpreter: `.venv\Scripts\python.exe` per AGENTS.md. All calls free-tier, $0.

## Probe log — pass 1 (probe_lanes, UTC 2026-09-16)

ALIVE (8): groq-qwen 435 ms · groq-oss 708 ms · groq-oss20 446 ms · cerebras-oss 389 ms · cerebras-qwen 859 ms · mistral-min8 6758 ms · or-nemotron 45152 ms · or-ling3 1033 ms — all sampled "READY".
DEAD (3): mistral-small HTTP 429 (389 ms) · zai-air HTTP 429 (1058 ms) · or-glm52 HTTP 429 (587 ms).
SKIPPED (1): zai-47 — paid wall, not probed per order.

Drift vs salon baseline (same night):
- `groq-qwen` salon DEAD → **ALIVE** (435 ms). Recovered.
- `zai-air` salon ALIVE → **HTTP 429**. Newly rate-limited.
- `or-glm52` salon 502 → **HTTP 429**. Failure mode changed: upstream gateway error → rate limit.
- `mistral-small` still 429. Consistent.

## Probe log — pass 2 (gen-2, UTC 2026-09-16 18:07)

Gen-1 died mid-pass-2; gen-2 completed it. Scope: (a) fresh re-verify of all 8 lanes gen-1 logged
ALIVE at 17:46 UTC (lanes drift within the hour — one did), (b) classified retry of the 3 dead
lanes capturing 429 body + rate-limit headers, (c) un-metered `GET /models` per provider, (d) one
extra or-glm52 retry after its `Retry-After: 5` elapsed. Prompt kept identical to gen-1
(`Reply with exactly: READY`) for comparability; timeout 60 s. **17 calls total** (≤ 20 cap),
all free-tier, $0. Raw tape (append-as-you-go, crash-safe for gen-3):
`receipts/D22_probe_pass2.jsonl` · script: `../D22_probe_pass2.py` (imports the module registry,
no repo code edited).

### Fresh re-verify of gen-1's ALIVE-8 (18:07 UTC, 18 min after pass 1)

| lane | latency | verdict |
|---|---|---|
| groq-oss20 | 693 ms | ALIVE |
| cerebras-oss | 726 ms | ALIVE |
| cerebras-qwen | 737 ms | ALIVE |
| groq-oss | 738 ms | ALIVE |
| mistral-min8 | 934 ms | ALIVE (warm; pass-1's 6.7 s was cold start) |
| or-ling3 | 1322 ms | ALIVE |
| or-nemotron | 37444 ms | ALIVE but SLOW (37 s for READY, reasoning burn) |
| groq-qwen | 429 @ 591 ms | **FLIPPED** — but the body says gated, not dead (below) |

### Classified 429s — four different failure classes

- **groq-qwen** — `429 Request too large ... output tokens per minute (OTPM): Limit 1000,
  Requested 1201 ... reduce max_tokens`. Org bucket itself is full (limit-requests 1000 /
  limit-tokens 8000, remaining 1000/8000). **Not dead: GATED.** Lane works with
  `max_tokens <= ~800`. Gen-1's identical probe passed at 17:46 — the output-token estimator
  drifts, so this lane 429s intermittently at high max_tokens.
- **mistral-small** — `429 code 1300 rate_limited`, headers `x-ratelimit-limit-req-minute: 0`,
  `remaining: 0`. **Quota-zeroed**: 0 req/min budgeted for this model — will not come back on
  retry. ministral-8b on the same key is unaffected (188/min).
- **zai-air** — `429 code 1113 "Insufficient balance or no resource package"` — **the same paid
  wall as zai-47**. `GET /models` still lists glm-4.5-air, so the wall is billing, not model
  availability. The z.ai key is paywalled model-wide → **both zai lanes: never call for $0 work.**
- **or-glm52** (probed ×2, second time after `Retry-After: 5` elapsed) — still 429:
  `limit_source: upstream_provider_shared_pool`, `provider_error_code: overloaded`. **Upstream
  shared-pool saturation, not our quota.** The 5 s Retry-After is optimistic; opportunistic only.

### Quota-headroom signals (response headers + GET /models)

| provider | limits seen | headroom NOW |
|---|---|---|
| cerebras (qwen-3.8-27b) | 450 req/min, 27k/hr, 648k/day · 150k tok/min | untouched (449/450 req-min · 215.997M/216M tok-day remaining) → **biggest budget in the fleet** |
| cerebras (gpt-oss-120b) | **5 req/min**, 150/hr, 2400/day · 30k tok/min | tight per-minute (4/5 remaining) → sparse, high-value calls only |
| mistral (ministral-8b) | 188 req/min · 625k tok/min | untouched (187/188 remaining) |
| groq (org bucket, shared by all 3 groq lanes) | 1000 req/min · **8000 tok/min**, reset ~1m26s | bucket full but refills fast; oss/oss20 completions are tiny → capacity ≈ 50+ short calls/min; qwen's OTPM 1000 sub-gate is the trap |
| openrouter :free | no rate headers on success | only visible via 429 bodies (glm52 upstream pool); ling3/nemotron answered clean |
| z.ai | n/a | paid wall (1113) |

`GET /models`: groq 13 (incl. `groq/compound`, `groq/compound-mini` — unprobed candidate lanes),
cerebras 2 (only the two we use), mistral 46 (incl. `labs-leanstral-1-5` — unprobed candidate),
openrouter 444, zai 10.

## ROTATION TABLE — the deliverable (probed UTC 2026-09-16 18:07)

| lane | model | status | latency | rate-limit class | recommended wave use |
|---|---|---|---|---|---|
| cerebras-qwen | qwen-3.8-27b | ALIVE | 737 ms | 450 RPM / 648k RPD · 150k TPM — huge | **PRIMARY workhorse** — backbone of any wide fan-out |
| mistral-min8 | ministral-8b-latest | ALIVE | 934 ms | 188 RPM · 625k TPM — large | **SECONDARY workhorse** — high-rate lane |
| groq-oss | openai/gpt-oss-120b | ALIVE | 738 ms | org 8k TPM shared bucket | ESCALATOR, short outputs; shares bucket with oss20 + qwen |
| groq-oss20 | openai/gpt-oss-20b | ALIVE | 693 ms | same 8k TPM org bucket | FAST short-output lane; watch combined groq burn |
| groq-qwen | qwen/qwen3.8-27b | ALIVE-GATED | — | model OTPM sub-limit 1000 → **max_tokens ≤ ~800** | SHORT answers only; set max_tokens=800 or it intermittently 429s |
| or-ling3 | ling-3.0-flash-sante:free | ALIVE | 1322 ms | OpenRouter free pool (no headers) | OVERFLOW / tertiary |
| or-nemotron | nemotron-3.5-lightning:free | ALIVE-SLOW | 37444 ms | heavy reasoning burn (171 tok for READY) | BACKGROUND batch only, timeout ≥ 90 s, never interactive |
| or-glm52 | glm-5.2:free | FLAKY | 429 @ 351 ms | upstream shared pool overloaded (not our quota) | OPPORTUNISTIC: 1–2 retries @ 5 s; never plan around it |
| mistral-small | mistral-small-latest | DEAD | — | limit-req-minute **0** (code 1300) | DROP from rotation; min8 covers mistral |
| zai-air | glm-4.5-air | DEAD (paid wall) | — | code 1113 insufficient balance | NEVER call — key paywalled model-wide |
| zai-47 | glm-4.7 | DEAD (paid wall) | — | code 1113 | NEVER call (standing order) |

**Net for the wave's next generation:** 6 clean lanes + 1 gated + 1 flaky. Rotation order:
cerebras-qwen → mistral-min8 → groq-oss20/oss (short outputs) → or-ling3 (overflow) →
or-nemotron (background). Drop zai entirely, drop mistral-small. Rule of thumb: cerebras-qwen
alone can absorb a 50-wide battery (450 calls/min, 150k tok/min); groq is the fragile one
(shared 8k TPM + qwen's OTPM 1000 gate); keep `max_tokens` small on groq lanes.

*Probe tally (gen-2): 17 calls — 12 metered chat probes, 5 un-metered GETs. $0. Receipt closed by
gen-2 2026-09-16 ~18:12 UTC.*

