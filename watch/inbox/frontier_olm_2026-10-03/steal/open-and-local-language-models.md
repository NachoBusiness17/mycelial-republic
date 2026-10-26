# STEAL CARD: open-and-local-language-models (round 2)

**Frontier sweep:** olm 2026-10-03. Round 1 verdict: HOLD, one surgical fix round; fixes A through D are applied here.
**Provenance upgrade:** the two provider-doc mechanism legs were re-fetched live by the steering seat (round 1 critique) and are promoted from ask-provided to steer-verified; the Groq page was additionally re-fetched by this seat on 2026-10-03 (probe step 0, below).
**Laws held:** no fabrication (OWED section), no em-dashes, citations as path:line or URL.

## The steal (the mechanism)

1. **Groq** (steer-verified; re-fetched by this seat 2026-10-03): caps are org-level and per-model across RPM, RPD, TPM, TPD (some orgs split ITPM/OTPM). Verbatim from https://console.groq.com/docs/rate-limits : "You can hit any limit type depending on which threshold you reach first." and "retry-after is only set if you hit the rate limit and status code 429 is returned. The other headers are always included." and "Cached tokens do not count towards your rate limits."
2. **Gemini** (steer-verified): caps span RPM plus input TPM plus RPD, apply per project not per key, RPD resets at midnight Pacific, and the page states "Specified rate limits are not guaranteed and actual capacity may vary." with per-model numbers withdrawn into AI Studio (https://ai.google.dev/gemini-api/docs/rate-limits).

**Overlap claim, CORRECTED (fix A).** Round 1 overstated: it called these the first provider-doc mechanism bytes the estate holds. The estate already held provider cap bytes:
- The Groq free-plan cap table since 2026-09-25: 30 RPM / 1K RPD / 8K TPM / 200K TPD on openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.8-27b, plus the cached-token and org-level clauses verbatim (watch/inbox/BURN_free-resource-landscape_20260925.md:7, spelled out at :14).
- Developer-plan numbers, 250k TPM / 1k RPM for openai/gpt-oss-120b, with groq.com/docs URLs (memory/research_packs/20260828_seat_underpinning/REPORT.md:89,91).
- Discrepancy noted honestly: the 2026-09-25 receipt labeled the 30/1K/8K/200K rows "free-plan"; this seat's 2026-10-03 fetch renders the identical rows under "the base limits for the Developer plan". The numbers are the banked prior either way; the tier label is unstable between fetches.
**Genuinely new** (this seat's greps, tracked non-attic, 0 hits): the first-threshold-wins sentence and the retry-after-only-on-429 condition. Adjacent prior art named: docs/REBUILD_SPEC_TOKEN_RENDER_MANAGER.md:49 (planned cap detection via retry-after headers, different organ) and memory/research_polished/kv_cache_compaction.md:15 (429-shape discrimination: Retry-After above 10s = pool, below 5s = key cap).

**RQ2 consequence (unchanged):** the stealth grid row reading 459 rows, zero 429s, 69h+ sustained forced mining, marked CONTRADICTION OPEN against memory/rib/RIB_FREE_USAGE_POLICY_20260823.md:3-5 (watch/inbox/frontier_olm_2026-10-03/lens/laws.md:69), is consistent with both "cool lanes work" AND "caps exist", because width alone cannot cross a tank the dispatch shape never approaches and the docs guarantee nothing. The lens's own order stands: resolve with instruments, not by silently editing either rib (same line).

## The five finds, mapped onto estate organs

### 1. Groq first-threshold-wins caps (find 1) -> water graph + sovereign mirror + stealth driver

- **Organs:** the water graph is the right shape: tanks with integer volume, one-way pipes with integer capacity, overflow to waste (mag/water_graph.py:5-14). The sovereign mirror's stealth_driver census already tracks the hosts (configs/mirrors.json, ts 2026-10-03T13:13:48.510975+00:00: groq "unreachable" stable, llm7 68 models stable, openrouter 466 stable).
- **Live-shape fact this card adds:** groq was DROPPED from the stealth driver allowlist on 2026-09-29 because its /models endpoint 403'd every cycle (tools/stealth_driver.py:55,94); the live free families are OpenRouter x2 keys, Hermes/Nous x2 keys, LLM7 anonymous, round-robin with per-lane minimums (tools/stealth_driver.py:169-170).
- **Port move with hook point (fix C):** extend mag/inference_budget.py, the per-fire harness-table organ whose header declares it the single source carriers import for per-animal recipes, the empty classifier, and the one sanctioned reaction (mag/inference_budget.py:1-11), with a per-provider tank table and tick() accounting; first import at the stealth driver's per-lane dispatch path (lane construction _work_lanes() at tools/stealth_driver.py:275, payload build work_payload() at :245; the funded Hermes leg _dispatch_hermes() at :375-407 is the paid seat and outside the free-lane tank concern). This closes one of the seven named bypasses (stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire, ds_workhorse; watch/inbox/frontier_olm_2026-10-03/lens/laws.md:74) instead of building the tank next to a bypass the ribs already flagged.

### 2. Gemini capacity is provider-discretionary (find 2) -> routing grid + percolator posture

- Cells fill only from estate instruments with a receipt file, never from vendor claims; UNMEASURED is a legal default (memory/rib/RIB_MODEL_GARDEN_ROUTING.md:47-53); rows expire at 30 days or on a family event (:54-57), both via watch/inbox/frontier_olm_2026-10-03/lens/laws.md:27,29.
- **Port move:** no doc-derived number ever fills a Gemini free-lane cell (the provider withdrew the numbers and disclaims guarantees); a live measurement receipt must name the moment including the Pacific-day boundary because the RPD reset lands there.

### 3. StepFun Step 5 Preview, open weights 2026-10-15 (find 3) -> quantizer watch

- Overlap evidence is now this seat's own: catalog holds only stepfun__step-3.7-flash run artifacts (catalog/catalog.jsonl:310529 and siblings) and no Step 5; the model itself is new to the estate.
- **Cut (fix D1):** round 1's secondary steal, banking the fxtwitter resolution door, is dropped; this run's lens already holds it OPEN with the exact recipe (watch/inbox/frontier_olm_2026-10-03/lens/doors.md:54,62-64).
- **Port move:** a dated watch, not a build. Prior arithmetic: 600B total params at 4-bit is on the order of 300GB of weights; 27B active improves compute cost, not the weight footprint; a 1M context window adds its own KV burden. Action: on 2026-10-15 re-run the footprint arithmetic against the actual shipped sizes and configs before any quant card is drafted. Weight-quant surface is the MLX/exo card fleet (catalog/catalog.jsonl:350927-350935); mag/auto_quantize.py:1-26 is the separate analytics-resolution organ.

### 4. Ajax: abliterated Qwen3.5-9B (find 4) -> POINTER-GRADE register entry (fix D2)

- Line 1: the Qwen3.5-9B family is already held estate-side; corpus/library/kev/PLAN_Qwen35.md:3 records the plan completed 2026-09-20 with Kev-0.8B/4B/9B shipped the same day (also catalog/catalog.jsonl:27783).
- Line 2: the tool name Heretic (open-source abliteration) is genuinely new to the estate; if an uncensored Kev variant is ever wanted, Heretic is the named prior art to evaluate on estate-TRAINED bases, human-gated; the base license string is OWED (the article states none; the find's Tongyi-Qianwen note is a GitHub snippet, not a model-card read).
- No mechanism claim beyond the register pointer. The article's home-PC claim adds no capability news given Kev-9B already shipped.

### 5. Tokenomics 2610.00954 (find 5) -> gopher fleet + percolator; NOT a first discovery

- **Overlap CORRECTED:** the find scoped its overlap grep to the quantization sibling sweep only. This same run's inference-efficiency sweep already deep-read the paper (full HTML text fetched; watch/inbox/frontier_olm_2026-10-03/sweep/inference-efficiency-arxiv.md:7) and banked the analysis that its metric suite is what the lens's five costed-but-unbuilt instruments want (:23). The name-drop predates this card (watch/inbox/frontier_olm_2026-10-03/lens/burns.md:186).
- **Steal that remains is the estate mapping:** ensemble with an SLM judge reached 97.34% IFEval strict prompt accuracy, +5.81pp over gpt-5.4, bought with extra test-time tokens and orchestration. This supports the flock shape and does NOT support solo sub-8B judgment, so the tier ladder stands (memory/rib/RIB_DRIVING_LADDER_20260928.md:20-23), and it agrees with the estate's own consensus-illusion instrument: high flock-consensus strength did not predict correctness on grounded tasks (memory/rib/RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:21-25,35-43).
- **Port move:** draft a percolator invariant candidate (record shape: text, count, first_seen, decay_as_of; memory/percolator/invariants.json), human-gated: "SLM ensembles buy instruction-following fidelity with an explicit judge and extra tokens; they do not certify judgment." If tested, test on estate evals (evals/v4/transfer-v4), not the paper's bench.

## The probe (fix B: it can now compute its own number)

**Step 0, before the window: bank the chosen host's cap table with URL + moment.**
- Groq: this seat re-fetched https://console.groq.com/docs/rate-limits on 2026-10-03. The page renders only "the base limits for the Developer plan"; the Free Plan Limits tab's numbers did not render (third failure: find 1, steering critique, this fetch). Rendered base rows: openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.8-27b all at 30 RPM / 1K RPD / 8K TPM / 200K TPD, matching the banked 2026-09-25 receipt. The receipt itself documents the table moving (14.4K RPD became 1K RPD; watch/inbox/BURN_free-resource-landscape_20260925.md:8), so step 0 is mandatory re-verification, never a one-time read.
- Host choice: NOT groq. It is dropped from the stealth allowlist (403s every cycle, tools/stealth_driver.py:55,94); re-admission is its own task. Primary probe host: openrouter (keys present at tools/stealth_driver.py:283-284; 466 models stable in the mirror census), fallback llm7. For openrouter and llm7 the estate holds NO fetched cap table (none found in this seat's greps), so those hosts run the instrument-only scope by default.

**24h window:** log per-dispatch request count and token count (cached tokens logged separately) for ONE model on the chosen host, per tank.

**Margin, precise:** margin = (cap - measured rate) / cap, headroom as a fraction of the cap, computed per tank from the logged window.

- **Doc-cap scope** (groq, only if re-admitted): prediction under first-threshold-wins: minimum tank margin stays above 0.5 (at least 2x headroom) with zero 429s, and any 429 coincides with a tank whose margin first crosses 0.
- **Instrument-only scope** (openrouter/llm7, no doc caps needed): set self-imposed tank thresholds (the banked Groq 30/1K/8K/200K shape as template), log every crossing. Falsifier: a 429 arriving while every logged tank rate is below half its threshold, or zero 429s while a tank runs above its threshold for a full window; either kills tank-observability and resolves RQ2 the other way.
- Either outcome lands as an instrument receipt for the CONTRADICTION OPEN row (watch/inbox/frontier_olm_2026-10-03/lens/laws.md:69), with instrument, moment, and assumptions named per the one-bug law (memory/rib/RIB_DRIVING_LADDER_20260928.md:53-72). Zero new spend; the accounting is passive over traffic the lanes already send, so the fan-out width law is untouched.

## OWED (claimed by nobody)

- Groq Free Plan Limits tab numbers: failed to render in all three fetch attempts (find 1, steering critique, this seat 2026-10-03).
- Gemini per-model numbers: withdrawn to AI Studio; not fetched.
- OpenRouter and llm7 cap tables: none fetched, none found in estate greps this session.
- Step 5 weights: unreleased as of the find's date; specs are tweet-level via the resolution door.
- Ajax base license string: article silent; model card not read.
- Largest estate host memory: no hardware census run.
- 2610.00954 full text: not read by THIS seat (deep-read banked by the sibling sweep, cited above).

## Checks run this session (exact commands)

- `git grep -n "groq.com/docs\|console.groq.com" -- "*.md" "*.jsonl" "*.json" "*.py"` : hits in seed/ACCOUNTS.md, tools/build_adam*.py, tools/seed_v2.py, watch/inbox/BURN_free-resource-landscape_20260925.md:7,23 (+_b variant), memory/research_packs/20260828_seat_underpinning/REPORT.md:89; none in doctrine dirs (memory/rib, docs/).
- `git grep -n -i "retry-after" -- "*.md" "*.py"` : adjacent organs only (ZCODE steal maps; docs/REBUILD_SPEC_TOKEN_RENDER_MANAGER.md:49; memory/research_polished/kv_cache_compaction.md:15; others unrelated).
- `git grep -n -i "threshold you reach\|hit any limit"` : 0 hits.
- `git grep -n "2610.00954"` : 0 tracked hits (name-drop lives in untracked lens files); untracked-scope grep found watch/inbox/frontier_olm_2026-10-03/lens/burns.md:186 plus the sibling sweep deep-read (:7,:23) and this card itself.
- `git grep -n -i "stepfun" catalog/catalog.jsonl` : only step-3.7-flash run artifacts.
- WebFetch of https://console.groq.com/docs/rate-limits on 2026-10-03 (step 0; output quoted above).
- citation_lint and byte counts on this card: results reported in the submission (commands below in Grounding run log).

## Grounding (read this session)

- memory/rib/RIB_FREE_USAGE_POLICY_20260823.md:3-5 (throttling law), 14-22 (decision rule), 39-42 (standing gate).
- watch/inbox/frontier_olm_2026-10-03/lens/laws.md:69 (RQ2 CONTRADICTION OPEN), 74 (seven fire surfaces bypassing the budget organ), 12 (one-bug law), 23-24 (cheap-first; sensing never substitutes for judgment), 27 (instruments-only routing), 29 (verdict expiry), 40 (consensus illusion).
- mag/water_graph.py:5-14 (tank/pipe/overflow engine).
- configs/mirrors.json (stealth_driver host census, ts 2026-10-03T13:13:48.510975+00:00: groq unreachable stable, llm7 68, openrouter 466, churn false).
- watch/inbox/BURN_free-resource-landscape_20260925.md:7 (free-plan table plus cached-token and org-level clauses), 8 (14.4K RPD became 1K), 14 (corrected denominator), 15 (frozen-prefix caching steal), 23 (receipt URL).
- memory/research_packs/20260828_seat_underpinning/REPORT.md:89 (groq docs URLs), 91 (Developer-plan 250k TPM / 1k RPM), 99 (groq lane dark at the time).
- tools/stealth_driver.py:55 (groq dropped v2), 94 (groq removed, 403 every cycle), 97-98 (openrouter and llm7 host URLs), 169-170 (three free families, round-robin, per-lane minimums), 245 (work_payload), 275 (_work_lanes), 283-284 (openrouter keys), 375-407 (_dispatch_hermes, the funded leg).
- mag/inference_budget.py:1-11 (the per-fire harness-table organ, single source carriers import).
- memory/rib/RIB_MODEL_GARDEN_ROUTING.md:47-53 (instruments-only cells), 54-57 (30-day expiry).
- memory/rib/RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:21-25 (consensus strength did not predict correctness), 35-43 (flock valid for open-ended sampling, not verifiable answers).
- memory/rib/RIB_DRIVING_LADDER_20260928.md:20-23 (sensing feeds judgment, never substitutes), 53-72 (one-bug law conditions).
- docs/REBUILD_SPEC_TOKEN_RENDER_MANAGER.md:49 (adjacent prior art: cap detection via retry-after headers).
- memory/research_polished/kv_cache_compaction.md:15 (adjacent prior art: 429-shape discrimination).
- watch/inbox/frontier_olm_2026-10-03/lens/doors.md:54 (fxtwitter OPEN), 62-64 (recipe and notes).
- watch/inbox/frontier_olm_2026-10-03/lens/burns.md:186 (bare 2610.00954 name-drop).
- watch/inbox/frontier_olm_2026-10-03/sweep/inference-efficiency-arxiv.md:7 (full HTML text fetched), 23 (metric-suite analysis).
- corpus/library/kev/PLAN_Qwen35.md:3 (completed 2026-09-20, Kev-0.8B/4B/9B shipped), 5 (original proposal line).
- catalog/catalog.jsonl:27783 (Kev Qwen3.5 plan entry), catalog/catalog.jsonl:310529 (stepfun step-3.7-flash artifact), catalog/catalog.jsonl:350927-350935 (mlx-community Qwen3.5 quant cards).
- memory/percolator/invariants.json (invariant record shape: text, count, first_seen, decay_as_of).
- mag/auto_quantize.py:1-26 (analytics-resolution quantizer, distinct organ from weight quants).
- AGENTS.md (DRIVING LADDER, fan-out width law, gopher fan-out dogfood line).

Finds 1 through 5 are ask-provided confirmed finds cited to their URLs in place; legs 1 and 2 carry the steering seat's live re-verification from the round 1 critique.
