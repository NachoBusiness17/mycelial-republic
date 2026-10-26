# FRONTIER SWEEP - inference-efficiency via X (adhoc seat)

source-fetched: adhoc - swept 2026-10-11 - door: WebSearch site:x.com + fxtwitter resolve (`https://api.fxtwitter.com/<user>/status/<id>`)

## Door status (read this first)

- 15 distinct search queries fired. The `site:x.com` door is degraded for most technical phrasings (vLLM, SGLang, Liger, llama.cpp, single-GPU 8B, FTS5: all returned zero or noise; two queries 429'd with code 1302 and were retried inside the search tool). The one cluster that resolved cleanly is the DeepSeek peak/off-peak repricing wave - real posts with status IDs, cross-consistent across six independent accounts.
- Strict 30-day window came up empty on X. The richest posts are dated 2026-06-30 through 2026-09-05 (5-15 weeks old). An October-specific query (`site:x.com API price drop October 2026 inference`) returned nothing. I bank them because no later repricing surfaced anywhere in the sweep, so this is still the live board as far as this door can see - but the vintage is stated, not hidden.
- All 8 banked items were resolved end-to-end through the fxtwitter JSON door and read by this seat. Quotes below are verbatim fragments from those fetches.

## Pass 1 - candidate pool (~31 items considered)

X posts (10): B.AI discount card, Artificial Analysis V4 Pro 0813, AI Battle docs-live, Pandaily price-raise report, Ollama off-peak token rates, TechBuzzChina V4-official analysis, Intellectual Insights billing clock, Irushi +355% breakdown, Chetaslua V4 Flash benchmark claim, Essays Hub lineup note (this last one low-signal, dropped).

Web candidates surfaced but NOT banked (not X, not deep-read here): vllm.ai v0.6.0 perf blog (2024, stale), vLLM GitHub issues/discussions on tok/s semantics, Google Cloud vLLM tuning guide (Aug 2025), Modal vLLM throughput docs, Liger-Kernel issue #1119 (Qwen 3.5 dense support ask, Mar 2026 - signals Liger lag on newest dense archs), Liger arXiv paper, Ternary Bonsai 1.7B/4B/8B llama.cpp support discussion, featherless.ai pricing guide ("time-based pricing is still rare in the industry"), Gemini 3 Flash pricing pages ($0.50/$3 per M, ~218 tok/s per Artificial Analysis via search snippet - snippet-grade, not fetched), The Verge Batch-API-50% (Apr 2024, stale), thejessezhang token-price-fall post (unresolved).

## Pass 2 - deep reads (8 resolved via fxtwitter, read in full)

### 1. Ollama introduces off-peak hour token rates - @ollama, 2026-09-05
https://x.com/ollama/status/2096374001119744190
"Introducing off-peak hour token rates" - half price outside 12:00-18:00 UTC weekdays, all-day weekends, for DeepSeek-V4-Flash and Pro, "hosted in the US & Europe with ZDR and fast performance"; more models coming. Engagement: ~104.6K views, 967 likes. Estate hook: the estate's own janitor-stack vendor now runs a time-metered cloud; peak window 12:00-18:00 UTC means the estate's overnight (US-East) hours are all off-peak - the sherpa cheap-first baseline and the offpeak queue (LAW-11 routing) gain a half-price DeepSeek lane with zero new vendor. Note Ollama's peak window (12:00-18:00 UTC) does NOT match DeepSeek first-party peak windows (01:00-04:00 + 06:00-10:00 UTC) - resellers set their own clocks, so the routing rib should carry per-vendor windows, not one global one.

### 2. Artificial Analysis - DeepSeek V4 Pro 0813 measurement card - @ArtificialAnlys, 2026-08-15
https://x.com/ArtificialAnlys/status/2088440350734201149
"DeepSeek's first-party API will charge $1.32 / 1M input tokens and $3.96 / 1M output tokens"; "Off-peak pricing is discounted by 50%." Intelligence Index 53 (+8 over April V4 Pro, +1 over V4 Flash 0731); blended price +264% (~3.6x); cached input $0.044/1M (~97% discount, 12x higher than before); Cost per Task $0.25 (5x the old $0.05, ~20% under GLM-5.2's $0.32); 128M output tokens on the index run (~30% fewer than April); GDPval-AA v2 Elo 1590 (+284); 1.6T total / 49B active, 1M context, MIT license. No latency figures in the post. Estate hook: this is the today's-board anchor for RQ1 - the exact numbers the shoulders-era measurements must be re-based to. CAREFUL: the estate already holds a NEWER AA post (2026-09-10, status 2098148674203488422, `watch/inbox/frontier_olm_20260928/sweep/_raw/`) saying V4.1 Flash (552B, 8B active in / 16B active out, encoder-decoder) overtakes V4 Pro 0813 at index 40 - the index was evidently rescaled between Aug and Sep snapshots; do not mix 53 and 40 in one arithmetic.

### 3. The billing clock explainer - @Intellectualins (Sahil Khanna), 2026-08-14
https://x.com/Intellectualins/status/2088203990823813580
"DeepSeek's V4 API bill will now depend on the clock." Time-based pricing from 16:00 UTC Aug 16, 2026 (midnight Aug 17 Beijing). Peak windows 01:00-04:00 and 06:00-10:00 UTC, peak = 2x off-peak. V4 Pro output $0.87 -> $1.98 off-peak / $3.96 peak; cache-hit input $0.003625 -> $0.022 / $0.044 (+507% / +1114%). Advice verbatim: "keep urgent traffic real-time, shift batch workloads to off-peak hours"; closing line "tokens x model x time of day." Estate hook: the UTC windows cross-check exactly against B.AI's SGT windows (09:00-12:00 + 14:00-18:00 SGT = UTC+8) and TechBuzzChina's Beijing framing - three independent sources, one clock. The estate's burn drivers log timestamps in UTC; the peak-avoidance predicate is a two-interval UTC check.

### 4. B.AI reseller stack: 50-75% off official, plus free flash tier - @BAI_AGI, 2026-09-03
https://x.com/BAI_AGI/status/2095443150076784898
"DeepSeek-V4-Flash and Vision-Exp Discount Live" - extra 50% off official peak rates during peak; 75% off official peak rates during off-peak; and GLM-5.3-Flash, Qwen3.8-Flash, Hy3, MiMo V2.5 stay free. Estate hook: a free flash lane spanning GLM-5.3-Flash and Qwen3.8-Flash is exactly the SENSING-tier class the driving ladder wants before any paid judgment climb - candidate for the free-tier rotation alongside gemini/groq/z.ai.

### 5. The price-rise anatomy - @Im_IrushiK, 2026-08-13
https://x.com/Im_IrushiK/status/2087868854919975295
"DeepSeek just MASSIVELY increased its API pricing." V4-Pro cache hits up to +1114%, cache misses up to +203%, output up to +355%; "peak rates cost 2x off-peak"; "Cheap inference has been one of DeepSeek's biggest advantages." Estate hook: the cache-hit line is the one that touches the estate's conditions-suspect economics - cache pricing moved 12x, so any shoulders-era measurement that leaned on cache hits without measuring them is now structurally wrong, independent of the thinking-ON default question.

### 6. TechBuzzChina: the demand-shifting read - @TechBuzzChina, 2026-06-30
https://x.com/TechBuzzChina/status/2071745549917688075
V4 official mid-July 2026; peak doubling 9AM-12PM + 2PM-6PM (Beijing); "off-peak pricing stays the same"; rationale "more reasonable resource allocation and service stability improvement" - read as demand-shifting under infra strain, not a revenue play; follows a May move that cut V4-Pro 75% permanently. Estate hook: the strategy frame for why off-peak discounts exist at all - they are load-shaping instruments, which is precisely what a scheduler can arbitrage.

### 7. Cheap tier beats premium preview - @chetaslua, 2026-07-31
https://x.com/chetaslua/status/2083070808512135336
"far exceeding the benchmark of v4 pro preview" (V4 Flash update); "During peak hours, prices will be 2x the regular prices, applicable to all billing items." Scores live in the attached image (not OCR'd here - claim is directional). Estate hook: RQ2 datapoint on the cheap-matches-premium arc, consistent with the estate's own 14/17 mesh finding and with AA's V4.1-Flash-overtakes-Pro receipt already in corpus.

### 8. Docs-page pointer - @AiBattle_, 2026-08-13
https://x.com/AiBattle_/status/2087862699568791875
"New DeepSeek peak / off-peak pricing is live on the docs page. The new pricing will take effect on August 16" - primary-source pointer for the re-measure; the docs page itself was not fetched this sweep (OWED).

## Overlap results (grep against holdings, run this seat)

- `catalog/catalog.jsonl`: zero hits for post IDs 2096374001119744190 / 2088440350734201149, zero "ollama/status" URLs, zero "peak/off-peak pricing" phrase. 15 "off-peak" hits exist but are zcode-cli source files plus the estate's own internal "RECEIPT: DeepSeek off-peak scheduling + 120x-to-30x cache-ratio correction (2026-09-25)" - our scheduling receipt, not these posts.
- Same-account different-post overlap: AA status 2098148674203488422 (V4.1 Flash, Sep 10) already banked at `watch/inbox/frontier_olm_20260928/sweep/_raw/` and re-confirmed 2026-10-06 - my AA item is the Aug 15 V4 Pro 0813 card, different post, different numbers; flagged so nobody arithmetic-mixes the two index snapshots.
- Domain overlap: catalog holds "DeepSeek V4 Flash across 14 providers: cost, speed and caching" (inference.academy, intake 2026-10-04, `watch/inbox/frontier_olm_2026-10-04/sweep/_ihn_page_49602817_14providers.txt`) - provider-board article; my items are the first-party repricing clock plus reseller moves; complementary, not duplicate.
- `memory/press/PRESS_DIGEST.md`, `memory/frontier/HELP_WANTED.md`, `memory/frontier/allowance.jsonl`, `memory/warm_state.json`: no off-peak / Ollama / V4.1 Flash hits.

## Research-question coverage (honest)

- RQ1 (off-peak price/latency board): SERVED for DeepSeek-family + resellers (items 1-8; latency numbers absent from all fetched posts - OWED; search-snippet-grade Gemini 3 Flash ~218 tok/s at $0.50/$3 was NOT fetched and is not banked as an item). The unmeasured-thinking-ON concern is compounded, not resolved: cache-hit pricing moved 12x, so the shoulders-era baseline needs a full re-measure, not a multiplier patch.
- RQ2 (cheap-local vs premium, where the gap re-opens): PARTIAL. One directional X datapoint (item 7) plus the estate's own V4.1 Flash receipt. No 2026 benchmark evidence on long-context / tool-use / multilingual gap surfaced through this door - the X index does not serve those queries. OWED to a different door (benchmark-report sweep).
- RQ3 (vLLM/SGLang/Triton/Liger wins for single-GPU 1-8B on Windows): NOT SERVED by this door. Zero relevant X posts surfaced. Only adjacent signal: Liger-Kernel issue #1119 shows Qwen 3.5 dense support still an open ask (Mar 2026), and a Ternary Bonsai 1.7B/4B/8B llama.cpp support discussion exists - both GitHub, both unfetched. The inference-opt shelf prioritization needs its own sweep (GitHub/blog door, not X).
- RQ4 (Leviathan vs FTS5 at estate scale): NOT SERVED and not an X question. The night-cools card's measured numbers are an estate-internal artifact (grokbot 8/8 find, commit b928a2240); no public source re-states them. Re-measuring belongs to a local bench run, not a frontier sweep.

## Actions for the ribs (if the switchboard takes them)

1. `memory/rib/RIB_DRIVING_LADDER_20260928.md` addendum candidate: per-vendor off-peak windows (DeepSeek first-party 01:00-04:00 + 06:00-10:00 UTC vs Ollama cloud 12:00-18:00 UTC peak) - a single global "offpeak" predicate is now provably wrong across vendors.
2. Free-lane rotation candidate: B.AI free flash tier (GLM-5.3-Flash, Qwen3.8-Flash, Hy3, MiMo V2.5) for SENSING work.
3. `tools/hermes_burn.py` carrier: re-base the DeepSeek cost lines to $1.32/$3.96 with 0.5x off-peak and $0.044 cached input before the next projection run, or the projection inherits the 12x cache error.
