# U8 UNION TECH INTEL — stealth/union-alpha technical/concurrency reconnaissance

- **Wave-lane:** U8 · **Seat:** technical/concurrency intel on `stealth/union-alpha` (OpenRouter)
- **Opened:** 2026-09-16 (UTC timestamps appended as work lands)
- **Method:** public OpenRouter API record + measured probes via repo key (`mag.flight_recorder.load_env`; key never printed) + WebSearch/WebFetch for third-party reports
- **Constraints honored:** no git, no paid APIs, `.venv\Scripts\python.exe` only, receipt-first + append-as-you-go

## Log

### Step 1 — API record (https://openrouter.ai/api/v1/models, fetched 2026-09-16)

`stealth/union-alpha` — **"Union Alpha"** (stealth model, provider slug `Stealth`, tag `stealth`, single endpoint).

| Field | Verified value |
|---|---|
| Created | **2026-09-16 14:42 UTC — brand new (today)** |
| Context window | **262,144 tok (256K)** |
| Max completion tokens | **131,072 (128K)** · max_prompt_tokens: null (uncapped) |
| Modality | **text+image → text** (vision-capable) |
| Tokenizer | `"Other"` — undisclosed |
| Pricing (now) | **$0 prompt / $0 completion** — free window ACTIVE (discount 0) |
| Pricing after free window | **NOT published.** No future pricing anywhere in the record; `expiration_date` is a placeholder (2098-12-31). Expect a nonzero prompt/completion price to appear on the same endpoint slug when the window ends — lanes must re-read `/models` before assuming $0 |
| Moderated | false |
| Caching | `supports_implicit_caching: false` — no implicit prompt cache, full re-bill on paid |
| Provider stats | uptime 30m ≈ 99.97%, 1d ≈ 99.98%; latency/throughput: null (OpenRouter hasn't measured yet) |
| Supported params | `max_tokens, response_format, temperature, tool_choice, tools, top_p` |
| tool_choice detail | supports `auto` only (no `none`/`required`/named-function) |
| per_request_limits | null (no documented per-key cap) |

### Step 2 — Rate-limit discovery (measured probes, 2026-09-16 ~15:20–16:00 UTC)

**OpenRouter returns NO `X-RateLimit-*` headers on this endpoint.** Full header inventory captured: only standard CF/Server headers + `X-Generation-Id` + `Server-Timing`. There is nothing to read — limit discovery had to be behavioral (burst until 429).

Burst ladder (all via one repo key, tiny prompts, `max_tokens=16`):

| Wave | Result | Wall | Latency spread |
|---|---|---|---|
| 6 concurrent | **6/6 HTTP 200** | 50.3s | 13.7–17.1s (solo-speed) |
| 12 concurrent | **12/12 HTTP 200** | 62.0s | 17.2–17.6s (**zero** degradation) |
| 24 concurrent | **24/24 HTTP 200** | 182.8s | 11.2–120.2s (tail queuing, **no 429**) |

- **Zero 429s across 53 total requests in the session.** Peak instantaneous rate: 24 requests fired in ~1s — all accepted.
- At 24 concurrent the wall shows provider-side queueing (some requests 120s), i.e. the visible limit is **latency, not rejection**.
- Key record (`GET /api/v1/key`): `is_free_tier: false`, no spend limit; `free_model_daily_requests` counter 88/1000 today — union-alpha is **not `:free`-suffixed**, so the 20 RPM / 50–1000-per-day free-model platform gates should not bind it (docs confirm those apply to IDs ending `:free`).
- Consequence for wave code: **no headers to budget from** — must handle 429 via `Retry-After` + exponential backoff and treat it as exceptional, not routine.
- OpenRouter docs: extra accounts/keys do NOT help ("we govern capacity globally"); negative balance 402s even free models.

### Step 3 — Latency / throughput (measured)

| Probe | Wall | Completion tokens | Effective tok/s |
|---|---|---|---|
| P1–P4 tiny factual | 14.6–17.2s | 5–26 | 0.3–1.5 |
| B1 JSON (25 tok out) | 45.1s | 25 | 0.55 |
| B2 long prose (220 tok out) | 58.8s | 220 | **3.7** |
| B4 5K-in, 59 tok out | 19.1s | 59 | 3.1 |
| Raw-SSE count-to-30 | 47.4s | ~60 | 1.3 |

- Latency is **reasoning-overhead dominated**: ~11–17s floor for trivial calls, 45–60s when the model deliberates (structured output, long prose). Prompt size barely matters (5.3K-token prompt answered in 19s).
- **Streaming is fake**: the provider holds the SSE connection open with `: OPENROUTER PROCESSING` keepalive comments for the whole generation, then dumps the complete text in 1–3 final chunk events. No TTFT benefit, no incremental output, no reasoning tokens streamed. **Wave lanes should call non-streaming with client timeout ≥180s.**
- vs U2's tape (88–170s for ~2K chars ≈ 500 tok → 3–6 tok/s): Union Alpha is **comparable-to-faster** (~1.5–4 tok/s effective, up to 120s worst-case tail under 24× load), with 256K context and $0 pricing.

### Step 4 — Capability probes

| Probe | Verdict |
|---|---|
| **Structured JSON instruction** | **PASS.** Returned exactly `{"name":"union-test","primes":[2,3,5,7,11],"ok":true}` — no markdown fence, no commentary. `response_format` and `tools` are advertised; tool_choice supports `auto` only |
| **Refusal behavior** | **No hard refusal.** On the Apollo-staged rhetoric probe it added a one-line classroom framing ("…the Apollo 11 landing was real:") then fully complied with the persuasive paragraph. Benign boundary-pushing sails through; expect disclaimers, not blocks |
| **5K-token input** | **PASS at 5,271 prompt tokens.** Perfect 4/4 retrieval (exact codes, masses, counts) in 19.1s, finish=stop, no truncation. 256K context claim credible; long-paste lanes are safe |
| Errors/reliability | 53/53 calls 200, `finish=stop` except deliberate `length` on B2; uptime 99.97% (30m) per OpenRouter |

### Step 5 — Third-party reports (community intel)

- **Identity: unconfirmed.** OpenRouter announced via X handle **@unionalphaai**; r/MistralAI guesses Mistral ("the Alpha in the European Union") — unverified. **Distinct from `stealth/ox-alpha`** (the GLM-5.3-lineage/OpenCode-linked model); do not conflate the Ox Alpha census claims with this model. A GitHub codex-router project explicitly separates them.
- **Free window:** free at launch, described as limited-time; `~2 billion tokens processed on day zero` (daily.dev). No published post-window pricing — must re-check `/models` when the window closes.
- **Rate limits:** no public concurrency numbers from anyone. Provider-rep "near unlimited usage" quotes circulating belong to **Ox Alpha's** OpenCode channel, not verified for Union Alpha. Community throughput numbers: none found.
- Reception on r/opencodeCLI: "not bad, but I don't get the hype for agentic coding" — mixed on agentic quality, no one reports walls.
- Also mirrored as "Union Alpha Free" on OpenCode Zen (zero-retention provider claim).

---

## MODEL SPEC CARD — stealth/union-alpha (verified 2026-09-16)

| Spec | Value | Source |
|---|---|---|
| Context window | 262,144 (256K) | API record |
| Max completion | 131,072 (128K) | API record |
| Pricing NOW | **$0 prompt / $0 completion** (free window ACTIVE) | API record |
| Pricing AFTER window | **Unpublished** — re-read `/models` before assuming $0 | API record gap |
| Modality | text+image → text, tokenizer undisclosed (`Other`) | API record |
| Moderation | none (`is_moderated: false`); implicit caching OFF | API record |
| Params | `max_tokens, response_format, temperature, tool_choice(auto only), tools, top_p` | API record |
| Rate-limit headers | **NONE returned** — budget blind, backoff-driven | measured |
| Streaming | **Non-incremental** (keepalive-then-dump) | measured |
| Reliability | 99.97% uptime (30m) | OpenRouter |

## MEASURED BUDGET FOR OUR WAVES (this week)

- **Requests:** ≥24 in one minute verified clean (24/24 × 200). Session total 53 requests, zero 429s. Hard RPM ceiling not found ≤24/min.
- **Throughput:** ~1.5–4 effective tok/s per request (reasoning overhead dominates); ~11–17s floor per call, 45–60s for deliberation-heavy outputs, 5K-token ingest +19s.
- **Recommended max concurrency for wave lanes this week: 12** — zero latency degradation at 12× (solo speed maintained), huge safety margin under the first observed queuing (24×→120s tails). Lanes that tolerate slow tails may push to 16–24; treat 429 as exceptional with backoff, set client timeout **≥180s**, call **non-streaming**, and re-check pricing on `/models` daily while the free window lasts.

**Evidence scripts kept alongside this receipt:** `u8_probe.py` (burst + header capture), `u8_probe2.py` (stream/JSON/refusal/5K probes). Key loaded from `mag.flight_recorder.load_env`, never printed, never logged.

## Sources

- [OpenRouter model record](https://openrouter.ai/api/v1/models) / [endpoints record](https://openrouter.ai/api/v1/models/stealth/union-alpha/endpoints) (fetched 2026-09-16)
- [Union Alpha page](https://openrouter.ai/stealth/union-alpha) · [OpenRouter rate-limit docs](https://openrouter.ai/docs/api_reference/limits)
- [r/singularity thread](https://www.reddit.com/r/singularity/comments/1wi03f6/new_stealth_model_union_alpha/) · [Stealth census (Ox Alpha, distinct model)](https://www.digitalapplied.com/blog/openrouter-stealth-model-census-who-they-turned-out-to-be)

---
