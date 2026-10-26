# TOOL PRICING RIGHTSIZE — 2026-09-13 (paste wave: metered tool sheet + usage CSV through 09-13)

Sources: operator-pasted tool pricing sheet (Browser Use, FAL queue, Krea direct, Modal, Firecrawl, OpenAI audio) + Downloads/usage-day-summary-a537a9b9-2026-09-14.csv (coverage 09-07→09-13). Prices = operator surface = Supported. Behavior claims = Unproven until receipt.

## 1. THE INVOICE (from the CSV, Python-parsed)

- Lifetime spend: **$32.11** against the 09-07 **$220.00** top-up → **~$187.89 headroom** (arithmetic on the CSV, not a balance-API read).
- **09-13 alone = $26.49** — 82% of all spend ever, one night, ~4,849 paid requests (~$0.0067/req blended).
- Day trail: 09-07 $0.12 · 09-08 $4.13 · 09-10 $0.00 · 09-12 $1.37 · 09-13 $26.49.

### 09-13 per-request league (paid lanes)
| model | req | $ | $/req |
|---|---|---|---|
| amazon/nova-pro-v1 | 59 | 1.71 | 0.0290 |
| moonshotai/kimi-k2 | 77 | 2.21 | 0.0287 |
| **anthropic/claude-sonnet-4** | **273** | **7.77** | **0.0285** |
| minimax-m2 | 128 | 1.55 | 0.0121 |
| claude-haiku-4.5 | 142 | 1.63 | 0.0115 |
| gpt-5-mini | 350 | 1.74 | 0.0050 |
| z-ai/glm-4.5-air | **1,571** | 4.38 | 0.0028 |
| mistral-small | 929 | 1.88 | 0.0020 |
| openai/gpt-oss-120b | 655 | 0.81 | 0.0012 |
| google/gemma-3-27b | 74 | 0.09 | 0.0012 |
| **ling-3.0-flash-sante:free** | **647** | **0.00** | free (22.0M tok in, 19.1M cache-read) |

- **The 3¢ cluster (sonnet + kimi + nova) ate $11.69 = 44% of the night for 409 of 4,849 requests (8%).**
- Sonnet alone = $7.77 = 29% of the night. Confirms the hermes-mirror verdict in PRODUCTION traffic: 24x the paid floor ($0.0012). Not a benchmark artifact — a billing pattern.
- Heroes hold: glm-4.5-air (workhorse), ling free (biggest token volume at $0), gpt-oss/gemma (paid floor).
- All-time per-request record: **gpt-6-astra $0.3714/req** (09-08, 10 req) — 300x the floor; that arm was the frontier probe and it stays retired.

## 2. THE TOOL SHEET = THE MODEL MIRROR AGAIN (penny tier vs premium tier)

**Stills:** krea-v2 via fal **$0.0011** · Z Image Turbo $0.0053 · pixverse $0.0053 · ideogram-v4-instant $0.0053 · qwen-image-3 $0.0105 · seedream-v5-lite $0.0368 · nano-banana-pro $0.1575 · **gpt-image-2 $1.05 · mai-image-2.5-pro $1.575** — a 1,400x spread. Law: penny tier does bulk (game art, riddle renders, drafts); $1+ tier = judgment-only (mint, Head Museum jars, tapestry visual spec).
**Video:** LTX-2.3 **$0.0017** · seedance-2.0-mini $0.0074 · grok-imagine $0.0105 · seedance-2.0 $0.0147 · minimax-h3 $0.0525 · flux-3 $0.0893 · **veo3.1 $0.42 · kling-v3-4k $0.441** — 250x spread; the top tier is wow-surface-only.
**Audio:** Whisper **$0.0063/min** (bulk transcribe — the ghost_cold_boot door at scale) · tts-1 $0.000015/char (~66K chars/$1) · gpt-4o transcribe out $10.50/1M tok (premium only).
**Infra:** Modal **$0.0495/CPU-hr**, $0.0084/GiB-hr (burst-runner substrate — nanobot/Rocinante split: local wins sustained at $0 marginal, Modal takes burst) · Firecrawl **$0.0005/credit** (bulk scrape / cite_gate fetch-door candidate) · Browser Use **$0.0011/min** (time is free; **bandwidth is the tax — $4.20/GB ≈ 3,800 session-minutes**, so text-crawls are free and media-heavy pages are the cost center).

## 3. TWO ANOMALIES (receipt-test before doctrine)

1. **nano-banana-2-lite.EDIT = $0.00** — while lite t2i is $1.05 and full nano-banana-2 is $0.084. The table inverts its own names. If the free edit is real, it's a free-lane image-EDIT organ. Price Supported (operator sheet); behavior Unproven.
2. **Same-family surface gap: krea-2-large = $0.06/generation direct vs $0.0011/billable-unit via fal — 55x.** Trust the sheet not the brand — but billable-unit semantics are Unproven (may not be 1:1 with generations). Receipt test decides.

## 4. LAW (extends the lane law to tools)

Check the usage CSV before firing paid tool lanes — **the tools have sonnets of their own.** Penny tier for bulk generation; premium tier only when a human eyeball judges the output; free lane first, always.

**Next (GO-gated, sub-penny):** fire the two receipt probes — one nano-banana-2-lite.edit + one fal-krea generation, combined cost ≤ $0.01 — read the bytes, file the row, promote or kill the anomaly.
