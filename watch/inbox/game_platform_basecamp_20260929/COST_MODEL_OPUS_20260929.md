# COST MODEL: CLAUDE OPUS 5.5 DELIBERATE ASK (2026-09-29)

Lane: research + arithmetic, cost model for the Opus 5.5 deliberate ask (OPUS_ASK_DRAFT_20260929.md, Amendment 1 inverted shape, Amendment 2 three-layer data-tuned shape). Question: what does it COST to have Opus answer (A), read our whole system and write an improved version (B), read blind multiple times (C); how do we make it cheaper; how do other people do it. Prices verified against platform.claude.com docs on 2026-09-29 (web lane, URLs in Sources). Arithmetic executed, not hand-waved (verification script inline in session; every number below recomputed twice). House style: zero em-dashes, enforced.

## 1. VERIFIED PRICE TABLE (Opus 5.5, per million tokens)

| Line | Price | Multiplier | Verified |
|---|---|---|---|
| Input | $4.00 | 1x | docs + Finout |
| Output | $20.00 | 5x input | docs + Finout |
| Cache write, 5-min TTL | $5.00 | 1.25x input | prompt-caching docs |
| Cache write, 1-hour TTL | $8.00 | 2x input | prompt-caching docs |
| Cache read (hit or refresh) | $0.20 | 0.05x input | prompt-caching docs |
| Batch API | 50% off ALL usage | 0.5x everything | batch-processing docs |
| Long context >200k input | output billed 1.5x | $30/M output | context-windows docs |

Corrections to the operator's brief, byte-trust law applied:

- Cache read $0.20/M was RIGHT, but the parenthetical "5x cheaper than input" was WRONG: $0.20/$4.00 = 0.05x = 20x cheaper. Opus 5.5 gets a special discount: standard cache read is 0.1x on other Claude models; Opus 5.5 is 0.05x.
- Cache write 1.25x for 5-min TTL confirmed; the 1-hour TTL option exists at 2x.
- Batch discount confirmed at 50% on all usage, stacks with prompt caching (Respán and AI Moda guides below).
- New fact the brief lacked: output above 200k input is billed at 1.5x ($30/M). No tier below crosses 200k input; keep it that way.

Mechanics that shape the arithmetic (all from the prompt-caching docs):

- 5-min TTL refreshes FREE on every cache hit; the clock starts at request start, and GENERATION TIME COUNTS AGAINST IT.
- Minimum cacheable prefix on Opus 5.5: 512 tokens (trivially met).
- Max 4 cache_control breakpoints.
- Cache-breakers: content changed above a breakpoint, switching models mid-conversation, CHANGING EFFORT LEVELS, compaction. Lesson for us: freeze effort=xhigh across every pass or the cache dies.
- Implicit/auto caching exists; a lone one-shot may get auto-written at 1.25x with no read to amortize it (pennies at our sizes, noted per tier).

## 2. BYTE-GROUNDING THE BASKET (trust bytes, not reports)

Measured on disk 2026-09-29 (tokens estimated at bytes/4, markdown):

| Doc | Bytes | Est. tokens | Operator budget |
|---|---|---|---|
| AGENTS.md | 17,170 | ~4.3k | ~8k (over) |
| docs/ref/GAME_PLATFORM_BASECAMP.md | 12,291 | ~3.1k | ~8k (over) |
| LANES_20260929.md + lane files (six-lane digests) | ~54k combined | ~12k to 14k | ~12k (match) |
| corpus/steal/ZCODE_REPO_STEAL_MAP_20260924.md | 143,074 | ~36k RAW | ~3k (12x over if raw) |
| tools/gps_mcp/README.md + spec (GPS_MCP_V0) | ~14.8k | ~3.7k | ~6k (over) |
| gwap receipt (BEACON_GWAP_72STEP_20260922.md) | 4,018 | ~1k | ~2k (over) |
| BASELINE_SPEC.md + BASELINE_QUALITY.md | 21,375 | ~5.3k | ~7k (over) |
| The ask itself (Amendment 1+2 shape, XML framed) | | ~4 to 5k | ~4k (match) |

Verdict: the operator's ~46k basket is REALISTIC but only if the steal map goes in as a ~3k DIGEST. Raw, it alone is ~36k and pushes the basket to ~79k. Every other line was budgeted high; measured total with steal-map digest: ~40 to 46k + ask ~5k = 45 to 51k. Arithmetic below uses 50k input (46k basket + 4k ask) as the Tier B midpoint, consistent with the operator's stated budget.

## 3. ASSUMPTIONS (stated, so the math is auditable)

1. Output verbosity at xhigh effort: 2 to 3x a normal answer. Tier A output 10 to 15k (mid 12.5k); Tier B/C output 30 to 40k (mid 35k).
2. Amendment 1 inverted ask = single API call, no tool loop (tests-first spec + critique, one response). The historical build-ask would loop; loop multipliers noted where relevant.
3. GLM-5.3-class mid tier priced at $0.3/M input, $1.2/M output (market rate). Via prepaid Nous credits the marginal CASH cost is $0; both shown.
4. Token estimates are bytes/4 heuristic on markdown; treat totals as +-20%.
5. One USD display cent rounding; script recomputed every line.

## 4. TIER A: THE ASK AS DESIGNED (in ~11k, out 10 to 15k)

Naive (single call, no cache):

- Input: 11,000 x $4/M = $0.044
- Output mid: 12,500 x $20/M = $0.250
- TOTAL: $0.29 (range $0.24 at 10k out, $0.34 at 15k out)

With batch (50% off, 24h async, fits a deliberate ask fine):

- TOTAL: $0.15 (range $0.12 to $0.17)

With prompt caching: NO SAVING. A one-shot has no prior cache to read. Marking the prefix cache_control pays 1.25x on write ($0.055 input line) with zero reads back: caching a lone single-shot is a small LOSS. Caching is a multi-read instrument (law derived in Tier B).

Cascade (GLM drafts, Opus judges/revises):

- GLM draft: 11k in x $0.3/M + 15k out x $1.2/M = $0.021 (or $0 cash via Nous)
- Opus judge: (11k ask + 15k draft) x $4/M + 4k revision x $20/M = $0.104 + $0.080 = $0.184
- TOTAL: $0.21 (30% under naive), $0.11 with batch on the Opus leg
- Verdict on shape: at this size the cascade saves dimes and adds a handoff risk (the estate's own SuperScout finding: the handoff, not the routing, carries the result). Do NOT cascade Tier A. Fire it straight, optionally batched.

## 5. TIER B: THE SYSTEM-READ (in ~50k, out 30 to 40k)

Naive:

- Input: 50,000 x $4/M = $0.200
- Output mid: 35,000 x $20/M = $0.700
- TOTAL: $0.90 (range $0.78 to $1.00)

With batch: TOTAL $0.45 (range $0.39 to $0.50).

With prompt caching, honest single-use math (the pre-warm trap):

- Cache write once (5m): 50k x $5/M = $0.250, then output $0.700 = $0.95. WORSE than naive.
- Pre-warm call (write, max_tokens ~16, negligible output) then the ask reads 50k x $0.20/M = $0.010 + output $0.700: two-call total $0.96. Still worse.
- 1h TTL pre-warm: $0.40 write + $0.01 read + $0.70 output = $1.11 single use. Worst.
- BREAK-EVEN LAW (exact): with 5m TTL, cost of N prefix reads = 1.25P + (N-1) x 0.05P vs naive N x P; cached wins when N >= 2. With 1h TTL: 2.0P + (N-1) x 0.05P wins when N >= 3. A cache is a subscription, not a discount: it pays only across multiple asks inside the TTL window.

So Tier B cheap, real: $0.90 naive, $0.45 batched. Cache only enters if Tier B becomes 2+ asks within an hour (it then saves ~$0.19 per extra read vs naive, or ~$0.09 batched).

## 6. TIER C: BLIND RE-READS x3 (Tier B three passes)

Model: 3 passes x (50k in, 35k out each; later passes re-read the same frozen prefix and write a fresh "even better version"; ask stays inside the stable prefix).

Naive: 3 x $0.90 = $2.70.

With 5m cache, optimistic (all hits): pass 1 writes 50k x $5/M = $0.250; passes 2 to 3 read 50k x $0.20/M = $0.010 each; outputs 3 x $0.700 = $2.100. TOTAL $2.37 (12% under naive).

TTL CAVEAT THAT BITES US: a 35k-token xhigh generation streams at roughly 50 to 100 tok/s = 6 to 12 minutes, and generation time counts against the 5-minute TTL. Pass 2 fired after a long pass-1 generation can MISS the cache and re-write at $5/M. The 5m number above is the optimistic bound.

With 1h cache (generation-safe): write $0.400 + 2 reads $0.020 + outputs $2.100 = TOTAL $2.52. Only 7% under naive.

With batch (no cache): $1.35. With 1h cache + batch (50% applies to all usage, stacking documented): $1.26. This is the best MECHANICAL price for Tier C: $1.26.

THE DOMINANT FACT: output is 78% of Tier C's naive cost ($2.10 of $2.70). Input cheapening (caching) moves 12 cents on the dollar; output cheapening moves dollars. No cache scheme fixes Tier C; only making Opus write less (or not write at all on some passes) does.

Cascade Tier C (GLM drafts all 3 passes, Opus judges each):

- GLM: 3 x (50k x $0.3/M + 35k x $1.2/M) = 3 x $0.057 = $0.171 (or $0 cash via Nous)
- Opus judge per pass: (50k prefix + 35k draft) x $4/M + 8k verdict x $20/M = $0.340 + $0.160 = $0.500; x3 = $1.500
- TOTAL: $1.67 cash; $0.92 with batch on the Opus legs
- Frontier OUTPUT tokens: 105k naive down to 24k = 77% cut; frontier dollars $2.70 down to $1.50 = 44% cut (72% with batch). Frontier input tokens go UP (drafts attached); the cascade's saving is entirely in output tokens, which is where the money is.
- Alt split (Opus does pass 1 full, GLM does passes 2 to 3, Opus delta-judges): $1.63 total. Same ballpark; pick by judgment need, not price.

## 7. DELIVERABLE 2: THE CHEAPENING STEAL (web, cited)

### 7.1 Anthropic prompt caching, official practice

- TTLs: 5-minute (default, 1.25x write) and 1-hour (2x write). Reads 0.1x standard, 0.05x on Opus 5.5. Break-even: 5m pays from the 2nd read, 1h from the 3rd (my arithmetic above; consistent with TensorMesh's published break-even analysis).
- Byte-stable prefix is the law: the cookbook moved a timestamp out of the system prompt and cut cost 44%; stable-first ordering (manual before per-claim data) cut 54%; explicit system breakpoint on an eval halved per-task cost ($0.0500 to $0.0223 on Sonnet medium).
- Cache-breakers named by Anthropic: dynamic content above breakpoints, model switches, EFFORT CHANGES, compaction. Our rib must freeze the census bullet and every date-stamped line OUT of the cached prefix, or each edit re-pays the write.
- Context caching on AWS bedrock page confirms the intended use: tools, system prompts, message history pinned at prefix.
- Announcement-level claim: up to 90% cost reduction, 85% TTFT latency cut.

### 7.2 Batch API reality

- 50% off all usage, async, results within up to 24h, single-shot only (no tool loops inside a batch entry; restructure: inline everything, attach terminal tools, cap max_tokens). Stacks with prompt caching (Respán, AI Moda, LibreChat report up to 90% combined). For a deliberate ask with a 24h fuse this is a free halving; for anything agentic it is unavailable.

### 7.3 Draft-cheap, judge-frontier in the wild

- FrugalGPT (Stanford): the canonical cascade; up to 98% cost reduction matching GPT-4 on benchmark tasks, or +4% accuracy at same cost.
- RouteLLM (LMSYS): GPT-4-level quality at ~85% lower cost via learned routing.
- Anthropic's own cookbook operationalizes it two ways: (a) "advisor tool": Haiku drives, Opus on call, ~$0.10 to $0.13 per task vs $0.29 Opus-high baseline, best "with a cheap signal to gate the consult on"; (b) decomposed routing: Haiku gatherers + Sonnet decider ~90% under baseline (9/10, with the failure mode named: the cheap tier flattened an exclusion the frontier caught; that is what the frontier judge pass is for).
- Anthropic's own ordering doctrine: model selection is the LAST lever ("easiest to pull but directly constrains the intelligence"), after caching, input management, loop efficiency, output management. And their economics line the estate already holds: upgrading the model beat doubling the token budget.
- Productized shape: OpusPlan (Opus plans, cheap tier executes), already banked in DELEGATION_RESEARCH_20260929.md.

### 7.4 Eval-gated escalation (cheap first, frontier when the trajectory says so)

- SWE-Router (arXiv:2607.00053, Son et al. 2026): uses PARTIAL AGENT TRAJECTORIES to decide whether to escalate a turn to the stronger model; "greatly improves the cost efficiency of SWE tasks while maintaining the majority of the performances of the stronger model" on SWE-bench.
- SuperScout (arXiv:2608.04804, estate-held): the handoff rather than the routing decision carries the result. Direct caveat on all cascade plans above: invest in the handoff artifact, not the router.
- TwinRouterBench (community): 75/100 resolved for $25.66 vs 74/100 all-Opus for $54.73 = 53.1% cut at parity. Real published numbers, same shape as our cascade.
- Related: R2-Router lineage at 4 to 5x lower cost than prior routers; MTRouter (2026) adds history-aware cost-aware routing.

### 7.5 Pre-warm the context (session priming, cached system prompts at scale)

- The pattern is exactly Anthropic's cached-system-prompt architecture: pin tools + system prompt + stable history at the prefix, mark breakpoints (max 4), keep effort and model constant, and let every request ride $0.20/M reads. The cookbook's "byte-stable prefix" (44% saving demo) and "stable-first ordering" (54%) are the two build rules.
- 1h TTL exists precisely for scheduled re-use windows (their docs frame it for batch/scheduled jobs): a deliberate-ask firing window of an hour amortizes the 2x write from the 3rd read.
- Anthropic checklist item #1 is our "test runs on cheaper models first": "get it working on a capable model, build an eval, and measure a baseline" BEFORE spending frontier tokens; their own demos measured cost per task, not per token, because "a model with a higher sticker price can be the cheaper option if it finishes the job in fewer turns."

### 7.6 Whole-codebase reads priced efficiently (precedent)

- Gemini 1M-window whole-repo passes: $1.25/M input under 200k, $2.50/M above 200k (long-context surcharge), implicit+explicit caching at $0.375/M write and $0.125/M read. A FULL 1M-token repo pass is ~$2.50 input alone, and every uncached request re-pays it; context caching is the only way iterative repo work stays sane. A 500k read on Gemini is $1.25 input vs $2.00 on Opus 5.5, and Opus adds the 1.5x output surcharge above 200k ($30/M) that Gemini does not.
- Claude Code repo-context: the repo prompt (CLAUDE.md + tools + file state) sits at the byte-stable prefix, so subagent forks and follow-up turns ride cache reads; heavy users report ~$25/day (HN datapoint) precisely because repeat reads price at cache rate. No official "whole-repo pricing" exists on any platform; the affordable pattern everywhere is: cache the stable prefix, pay full price only for the first read and for new tokens.
- Precedent conclusion for the estate: whole-system reads are done either on Gemini 1M windows (cheaper raw input, no output surcharge) or on Claude with the corpus pinned as a cached prefix. First reads are never cheap anywhere; REPEAT reads are 20x off on Opus 5.5, the best read rate of any current Claude model.

## 8. TOP 3 CHEAPENERS BY SAVINGS (ranked, dollars, on Tier C = the expensive tier)

1. OUTPUT-TOKEN CASCADE (draft GLM, judge Opus): saves $1.03 to $1.78 of $2.70 (44% plain, up to 66% with batch on the Opus legs; 77% of frontier output tokens eliminated). Biggest mover because output is 78 to 85% of every tier's cost. FrugalGPT/RouteLLM/advisor-tool precedent.
2. BATCH API 50%: saves 50% of EVERYTHING with zero engineering, whenever a 24h fuse and a single-shot (non-agentic) shape are acceptable: $2.70 to $1.35, $0.90 to $0.45, $0.29 to $0.15. Stacks with caching. The only reason not to: you lose the interactive loop and same-day iteration.
3. PROMPT CACHING (the pre-warmed RIB): on multi-ask or multi-pass shapes, repeat input drops from $4.00/M to $0.20/M (20x). On Tier C saves $0.18 to $0.33 of $2.70 (7 to 12%) because input is the small share; on a FUTURE lane of many frontier asks over one rib, it is the difference between paying $4 per ask for context and $0.10 (the 46k rib re-read costs $0.0092). Rule: it is a subscription (pays from the 2nd read at 5m TTL, 3rd at 1h), worthless on single shots, and dies on any prefix edit, model switch, or effort change.

Runner-up: effort discipline. Effort xhigh is why output is 2 to 3x verbose; Anthropic's own per-task table shows Opus high ~ $0.15 vs medium ~ $0.137 (small) BUT the estate's differentiation brief measured 7 index points of quality between them; the verdict below keeps xhigh on the ONE judgment shot and nowhere else. Also: keep every pass under 200k input or output reprices to $30/M.

## 9. VERDICT: THE FIRING PLAN

FIRE TIER A, AMENDMENT 1 SHAPE (inverted ask), BATCHED IF THE 24H FUSE IS TOLERABLE.

- Cost: $0.29 straight, $0.15 batched. Budget cap to name before firing: $0.50 (covers a 2x verbosity surprise).
- No cascade at this size (saves dimes, adds handoff risk).
- No pre-warm at this size (single shot; cache would LOSE $0.05 to $0.21).
- Do run the ask shape itself past GLM-5.3 first (Nous credits, $0 cash): one cheap dry pass catches ambiguity, missing context, and output-contract holes BEFORE the one funded shot. This is Anthropic checklist item #1 verbatim, and it is free on our ladder.
- Judge the return with the estate's gates (tests-first acceptance, baseline section 10 diff contract), never prose.

IF THE OPERATOR WANTS THE SYSTEM-READ (Tier B): fire it ONCE, batched: $0.45. Do NOT buy Tier C blind x3 at $2.70; if multi-pass is wanted, the honest menu is: mechanical 1h-cache + batch $1.26, or cascade (GLM drafts 3, Opus judges 3) $1.67 plain / $0.92 with Opus legs batched. The blind-re-read fantasy costs 3 to 9 Tier A shots; the cascade version costs about 3 to 6 and leaves a judged artifact per pass.

STANDING LAW FROM THIS MODEL: output tokens are 78 to 85% of every tier. Cheapening input (caching) is a rounding error until ask volume is high; cheapening OUTPUT (cascade, tighter output contracts, effort discipline) is where every real dollar is. Any future "make Opus cheaper" idea that does not reduce Opus OUTPUT tokens is cosmetic.

## 10. PRE-WARMED RIB DESIGN (RIB_FRONTIER_ASK_20260929)

Purpose: every future frontier ask re-rides one frozen, byte-stable, pre-cached system prefix, so context costs $0.20/M instead of $4.00/M from ask #2 onward. Lands in memory/rib/ per rib law (boot-order: load ribs, load state, then act).

Cache prefix layout (4 breakpoints max, stable-first, per Anthropic cookbook ordering):

1. BREAKPOINT 1, rib core (byte-frozen, versioned, hash in the rib): AGENTS.md TRIMMED (volatile lines stripped: census bullet, dispatch-log dates, anything with a date that moves; a frozen "as of 2026-09-29" fork) + GAME_PLATFORM_BASECAMP.md + six-lane digests + steal-map DIGEST (3k, NOT the 143KB raw) + gps-mcp README/spec + gwap receipt + BASELINE_SPEC + BASELINE_QUALITY. Target ~46k tokens, hash-pinned (sha256 recorded in the rib so a changed file is a visible cache-break, not a silent re-write).
2. BREAKPOINT 2: tool schemas (frozen; tool definitions are cache-prime real estate per AWS/docs guidance).
3. BREAKPOINT 3: the per-ask brief (ask + output contract; changes every ask, sits late so earlier tiers stay cached).
4. BREAKPOINT 4: scratch (amendments, mid-session material).

Firing protocol for any deliberate ask window:

1. Queue 2+ frontier asks (break-even law) OR one multi-pass ask; below that, cache is a loss, fire uncached.
2. Warm-up call: write the rib prefix with cache_control (1h TTL, $8/M = $0.40 on the 50k rib), max_tokens minimal.
3. Fire asks within the hour; each re-reads the rib at $0.20/M ($0.0092 per 46k re-read). Effort pinned xhigh for every call (effort change = cache death). Model pinned (model switch = cache death).
4. Receipt: log tokens in/read, tokens write, hit/miss, and dollars per ask in the rib's ledger line; a miss on pass 2+ is an incident to explain (TTL expiry vs prefix drift), same law as the FTS gate.
5. Rib refresh is a deliberate act: edit the rib file, re-hash, re-warm once; never let a date or index pointer live inside the prefix.

Cost of the standing rib, amortized: first ask in a window pays $0.40 warm-up + its own tokens; asks 2+ pay $0.0092 for the whole estate context. After ~10 asks in a window the rib has cost $0.40 + 9 x $0.0092 = $0.48 total for context that would cost $4.14 uncached: 88% off the context line, forever, and the rib doubles as the estate's canonical frozen context pack (the same bytes feed Hermes Nous asks and any future frontier).

## 11. SOURCES (retrieved 2026-09-29)

- Prompt caching (official): https://platform.claude.com/docs/en/build-with-claude/prompt-caching (multipliers, 512-token minimum on Opus 5.5, TTL refresh rules, 4 breakpoints, per-model price table incl. Opus 5.5 $4/$5/$8/$0.20/$20)
- Batch processing (official): https://platform.claude.com/docs/en/build-with-claude/batch-processing (50% all usage, 24h, caching supported)
- Cost optimization cookbook: https://platform.claude.com/cookbook/cost-optimization-cost-optimization (checklist order, 32/44/54% caching demos, advisor tool, decomposed routing ~90%, batch triage demo, model/effort per-task table)
- Effort guidance: https://platform.claude.com/docs/en/build-with-claude/effort (effort constant preserves cache)
- Models overview (pricing incl. batch + cache rates): https://platform.claude.com/docs/en/models/overview
- Long-context output surcharge (1.5x above 200k): https://platform.claude.com/docs/en/build-with-claude/context-windows
- Opus 5.5 price confirmation: https://www.finout.io (Claude Opus 5.5 $4/$20, 20% cut from Opus 5)
- Prompt caching breakdowns: https://www.tensormesh.ai/learn/anthropic-prompt-caching-pricing and https://technspire.com/sv/blog/anthropic-prompt-caching-pricing-mechanisms (break-even math)
- Batch + caching stacking: https://www.respan.ai/articles/anthropic-message-batches-api and https://www.ai.moda/en/blog/anthropics-batches-with-caching and https://github.com/danny-avila/LibreChat/discussions/5034
- FrugalGPT: https://arxiv.org/abs/2305.05176 (98% max cost cut at GPT-4 parity)
- RouteLLM: https://arxiv.org/abs/2406.18665 (~85% cheaper at GPT-4 quality)
- SWE-Router: https://arxiv.org/abs/2607.00053 (trajectory-gated escalation, cost efficiency at majority of strong-model performance)
- TwinRouterBench datapoint: 75/100 for $25.66 vs 74/100 all-Opus $54.73 (53.1% cut), https://github.com (community router bench)
- Gemini pricing (1M window, long-context surcharge, caching): https://ai.google.dev/gemini-api/docs/pricing and https://openrouter.ai and https://llm-stats.com
- Claude Code repo caching practice + $25/day heavy-use datapoint: https://news.ycombinator.com (Feb 2025 Claude Code thread)
- Estate-held: SuperScout arXiv:2608.04804 (handoff > routing), OpusPlan economics, DELEGATION_RESEARCH_20260929.md, CLAUDE_DIFFERENTIATION_20260929.md (xhigh +7 index points, multi-turn -39%)

## 12. RECEIPT

- Arithmetic verified by script (Mag venv python), two passes, all lines in sections 4 to 6 and 8 to 10 recomputed; no hand-copied totals.
- Prices byte-verified against platform.claude.com docs on 2026-09-29; the operator's $0.20/M cache-read figure confirmed, its "5x cheaper" gloss corrected to 20x (0.05x).
- Basket byte-measured on disk 2026-09-29; steal map flagged 12x over budget if raw (digest mandatory).
- Headline numbers: TIER A $0.29 ($0.15 batched); TIER B $0.90 ($0.45 batched); TIER C $2.70 naive, $1.26 best mechanical (1h cache + batch), $1.67 cascade ($0.92 with Opus legs batched). Recommendation: fire Tier A (Amendment 1 shape) at a $0.50 cap, batched if 24h fuse tolerable; GLM dry-run first at $0; build RIB_FRONTIER_ASK_20260929 for every multi-ask window thereafter.
