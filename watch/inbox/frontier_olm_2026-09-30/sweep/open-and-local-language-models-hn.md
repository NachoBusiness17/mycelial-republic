# SWEEP: open-and-local-language-models via HN - 2026-09-30

source-fetched: 2026-09-30 · area: open-and-local-language-models via hn · agent: sweep gopher (hn lane)

## Door status

HN Algolia door LIVE all session, no 403, no degradation, no fallback used. Queries fired (all 2026-09-30, window `numericFilters=created_at_i>1788134400` = 2026-08-31T00:00Z where dated):

| query | endpoint | nbHits |
|---|---|---|
| "local llm" (quoted) | search_by_date | 24 |
| "local llm" (quoted) | search (relevance) | 540 |
| "open weights" | search_by_date | 17 |
| ollama | search_by_date | 82 |
| qwen | search_by_date | 235 |
| gemma | search_by_date | 135 |
| GLM-5.3 (unquoted, all types) | search_by_date | 434 |
| z.ai | search_by_date | 8 |
| deepseek | search_by_date | 120 |
| "on-device" model | search_by_date | 14 |
| featherless | search_by_date | 2 |
| "free tier" llm | search_by_date | 5 |
| "lightning.ai" | search_by_date | 0 |
| "glm-5" | search_by_date | 434 (comment hits) |
| clippy local llm | search | 3 |
| "GLM-5.3-FlashX" | search | 1 |

Door-fidelity note on `lens/doors.md:29`: the 2,916 nbHits figure is the UNQUOTED `local llm` relevance query and my own fetch of the Clippy story confirms it exactly: "Show HN: Clippy - 90s UI for local LLMs", 1122 points, 275 comments, objectID 43905942. My quoted-phrase variant reads 540 - both numbers are real, they are different query shapes, not a door contradiction.

## Pass 1 (broad sweep, 2026-08-31..2026-09-30)

60+ candidate stories considered across the 16 queries above. Strongest by points: Ollaya 613 (49848269, 09-25), Desert Ant Labs 490 (49624823, 09-09), "Why your local LLM feels dumber than it is" 511 (49402232, 08-22 - outside window), "Ask HN: Can we please limit the AI news flood?" 868 (49657850, meta), open letter to Dario 308 (49676085), DeepSeek Elastic Compute 322 (49859112), GLM infra 411 (49737922), Cactus Needle 3 236 (49748553), JevBench 153 (49800574), prompt lookup drafting 89 (49859982), OpenAI Codex agents $78k rogue 82 (49861047), Sunk Cost 47/99c (49706656), AI-rete-RAG 44 (49803683), Open Weights Are Good 41 (49769183), InstinctFlash 27 (49802789), whichllm 283 (48146369, May), plus since-09-28 releases: Strata Qwen3.8-Flash-Next 125B-on-8GB (49879253, 09-28), "GLM 5.3 flash on AMD GPUs 670 tok/s" (49905366, 09-30), Ollama Jev support x2 (49906337 + 49908997, 09-30), CAISI GLM-5.3 assessment (49905262, 09-30), 640tok/s Gemma 4 megakernel (49897153, 09-29), Qwen3.5-4B fine-tune (49897103, 09-29), ThinkingCap-Qwen3.8-27B (49857003, 09-26), StepFun Step 5 (49796998, 09-22, open weights promised Oct 15), SoTA Feed (49794230, 09-21), Vyne 205MB decision model (49773767, 09-20), GLM-5.3-FlashX docs (49757191, 09-18), Mozilla local-server benchmark (49742415, 09-17), ROCmFix/InferBench AMD (49770070, 09-19), Cactus Needle 3 (09-18), OpenCode $60 DeepSeek v4.1 Flash permanent (49846863, 09-25), Z.ai ZCode repo-upload saga (49810164 / 49807362 / 49782006 / 49757971), "Is z.ai shipping a different ZCode client than the source?" (49850328, 09-25).

## Pass 2 (deep reads, end to end, this session)

9 pages read end to end: Cactus Needle 3 full 93-comment thread · Desert Ant Labs 104-comment thread · Ollaya 145-comment thread · Sunk Cost 99-comment thread · GLM infra 285-comment thread · duane.sh Qwen3.5-4B article · prompt-lookup-drafting thread · Clippy 275-comment thread · Ollama Jev blog post. Plus verification fetches: featherless.ai homepage, docs.z.ai GLM-5.3-Flash/FlashX page, sota.borgcloud.ai.

## Dedup ledger (what was EXCLUDED as already held - re-banking is waste)

- **Cactus Needle 3** - FULLY held by `watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-hn.md` (same Scaevolus 230-case bench: FunctionGemma 90.9%/85.2% vs Needle 3 32.2%/20.4%, vendor BFCL/Mobile Actions numbers, thread teardown). FunctionGemma paper itself in catalog (`de0d63306435`, `watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.25373.txt`).
- **Ollaya story** - passing mention in 09-28 inference-efficiency sweep ("Ollaya 49848269 at 613 pts, a different project"). My marginal add: the thread's classifier demystification and the Ollama 09-30 landing (below).
- **GLM-5.3-FlashX** - heavily held: `tools/flashx_probe.py`, `watch/inbox/FLASHX_PROBE_20260927.md` (glm-5.3-flashx vs glm-5.3-flash on the fleet OpenRouter lane), `memory/continuity/seat_memory_20260927/glm-flashx-not-on-plan-20260927.md`. Banked below only as vendor-docs confirmation.
- **GLM infra story itself** - held at `memory/continuity/seat_memory_20260927/fleet-knowledge-graph-20260917.md` ("GLM Built Its Own Inference Infrastructure ... 3x throughput"). Banked below: the comment-layer economics only.
- **SoTA Feed / StepFun Step 5 / 640tok/s Gemma 4 megakernel** - today's sibling `open-and-local-language-models-arxiv.md` already pooled/adjudicated all three ("hold: throughput ceiling signal").
- **Clippy thread** - today's sibling `open-and-local-language-models-x.md` already DEEP-READ item 43905942. My independent Algolia fetch re-confirms 1122 pts.
- **Mozilla local-server benchmark** - held in `watch/inbox/frontier_olm_20260928/sweep/` (inference-efficiency-x, quantization-compression-hn).
- **DeepSeek v4.1 Flash OpenCode $60-permanent (09-25)** - 09-28 register already holds DeepSeek V4.1 Flash items per today's x-sibling dedup baseline.
- **Strata (Qwen3.8-Flash-Next runner, 49879253)** - the "strata" hit in today's agent-memory-continuity-hn is a DIFFERENT Strata (memory layer, 49807583); the runner repo is new but 4 pts / 0 comments, self-reported, held to note level.

## Findings by research question

### RQ1 - open-weight janitor/scut contenders since 09-28

The paradigm shifted under our feet this week: **typed decision models landed natively in Ollama 0.35** (2026-09-30, `/v1/systemone` endpoint) with three models: **nimble 9B** (Bespoke Labs), **tev1 4B** and **tev1:0.8B** (Together AI, experimental). Vendor claims 91 ms per decision on an M5 Max, ~4-token outputs, one call answering all named questions - verbatim: "Send text as state with a set of named questions, and a model running on your machine answers them all in one request." This is a drop-in shape for `gemma:2b` scut work (triage/routing/moderation), and the Ollaya thread's demystification is the guard rail: per hbrn, "'Decision model' is just marketing jargon. decision model = classifier... system one model = small non-reasoning LLM... It's sad to see how gullible engineers are today." The Ollaya author conceded their 421M ModernBERT Laya is "well below Jev on harder queries"; Kev/decider (Qwen-based, 0.8B-35B) approach Jev quality.

The strongest direct janitor-slot evidence is **not** a release but a recipe: duane.sh fine-tuned **Qwen3.5-4B** (SFT LoRA r32 on ~25k Opus-written contexts, then DPO 12k on-policy pairs, then GRPO RL; $7 on one H100, 1.6 h) to replace the retired Gemini 2.5 Flash-Lite; serves on one RTX 4090 at ~1.3 s/excerpt, $76/M excerpts (71% below the old model, 92% below its successor), usefulness 4.19 vs 4.20 teacher. Verbatim: "It makes fewer mistakes than Gemini 2.5 Flash-Lite at 71% less cost." 9B student cost 3x with no usefulness gain - 4B is the size that paid.

Threshold cross-check from the Sunk Cost thread: 7-9B class is "fine for automation/tool-calling"; the 27-35B MoE band (Qwen3.8 27B, Qwen3.6:35b-a3b) is the practical chat-class sweet spot at 50-57 tok/s on a used 3090; consensus "never pays off at current prices" because providers are dumping compute.

Self-reported claims the funded tier must verify before any lane promotion (laws.md:23 sensing-never-verification): nimble's 91 ms/decision and its 13-dataset/3,880-decision accuracy (vendor, no scores listed in the post); Strata's "Qwen3.8-Flash-Next (125B MoE) on a 8GB+ Nvidia GPU" (4 pts, 0 comments, repo-only); "GLM 5.3 flash on AMD GPUs 670 tok/s" (tweet, 2 pts); ThinkingCap-Qwen3.8-27B "less thinking, similar accuracy" (3 pts). Note Cactus-Needle-style tiny-model claims already got torn down once this window (see dedup ledger).

### RQ2 - Lightning lane / dropped GLM-5.3-Flash rung / Featherless gap

- lightning.ai: **zero stories** in the 30-day window (nbHits 0) - no provider-side replacement signal on HN; the lane is dead quiet, matching `lens/burns.md:59` ("Lightning lane closed FULLY DEAD").
- GLM-5.3-Flash: **not dead at the vendor**. The docs page (fetched today) shows Flash on the GLM Coding Plan with "3x the available quota compared with GLM-5.3" and off-peak calls at 50% points; FlashX (320B/18B MoE, 1M context, 200 tok/s) is "not yet available on the plan." The rung was dropped in OUR lanes, not by z.ai - confirms and extends the estate's 09-27 OpenRouter probe. The 411-pt GLM infra thread adds the access economics: Lite $18 / Pro $80 / Max $168 coding plans, users report 5.3 quotas "exhaust absurdly fast" for heavy agentic coding, and alexjplant recommends "GLM-5.3 Flash via OpenRouter as cheap," noting recurring free "stealth" models likely GLM-family. Hard-local angle from the same thread: argodrive streams full GLM-5.3 (744B MoE, 4-bit experts, 434 GB) off NVMe on a 128 GB M5 Max at 2 tok/s per drive, 4.2 tok/s striped - and Schlagbohrer laments the 35B-200B open-weights gap on 128 GB consumer boxes, filled per Catloafdev by Qwen3.8 Flash Next and DeepSeek V4 Flash (2-bit hybrid).
- Featherless: **no published explanation found** for the 22,059-vs-28.6k counter gap (`lens/burns.md:57-59`). The homepage fetched today now claims "Browse 40,000+ models" / "Test any of 40,000+ models effortlessly." - the counter has moved past both held numbers, making the old gap moot. Constraint worth law-noting: the $25 Chat tier is "interactive human use only," explicitly not for "app/API traffic, automation, or benchmarking" - the developer tier ($50 credits/mo, 256K context, rollover) is the only compliant lane for fleet use. HN in-window Featherless signal is thin (2 hits; "Simple-jev by featherless AI" product page, 09-22).

### RQ3 - what the local-LLM wave says about capability/UX thresholds

Clippy door independently re-verified (1122 pts / 275 c, id 43905942; the sibling x-lane deep-read it today; I read it end to end for the threshold layer). Recurring adoptability thresholds from that thread: ease of setup is decisive (node-llama-cpp "by far the easiest way"; repeated Ollama-integration requests so users don't duplicate local runtimes), GUI familiarity beats terminals ("quake-terminal" friction), hardware guidance must precede model load (LM Studio load crashed a machine), small frictions (hotkeys, model file locations) are churn drivers, and binary trust/signing matters ("signed, reproducible builds"). Capability thresholds from the wave: the estate's `gemma4` worker family got independent (non-vendor) behavioral evidence - arXiv 2609.30716, already adjudicated by today's arxiv sibling - and the decision-model wave sets a new scut bar: typed answers with calibrated probabilities in one ~91 ms call instead of autoregressive chat tokens. The Sunk Cost economics say the local tier's honest justification is privacy/autonomy ("It pays off instantly, because OpenAI/Anthropic can no longer see what I'm doing"), never cost.

### RQ4 - repeatable arXiv-door harvest for frontier_thinking, and state/arxiv staleness

The shelf is 11 files (`lens/corpus.md:23`, verified). Repeatable harvest options measured today:
1. **arXiv export API door** (`lens/doors.md:14-18`, verified live 09-30 by the probe: Atom XML, `sortBy=submittedDate`, first entry one day old) - the sanctioned repeatable door; today's arxiv sibling ran it at scale (110 entries pooled, 35 adjudicated). This is what should feed frontier_thinking continuously.
2. **SoTA Feed** (sota.borgcloud.ai, HN 49794230) - has RSS + Atom + lite feeds, ~130 releases, tracks DeepSeek/Qwen/NVIDIA/Z.ai/Moonshot/Xiaomi/MiniMax/Meta/Google/OpenAI. BUT the footer snapshot reads 2026-06-10 - the feed itself looks ~3.5 months stale, and today's sibling already pooled "14 SoTA Feed September rows" from it. Use as secondary, verify freshness each run.
3. **HN Algolia per-model queries** (this sweep's method) - the model-name query set (qwen/gemma/glm/deepseek/featherless) is itself a repeatable door recipe; nbHits per query recorded above as the baseline.

state/arxiv staleness (my counts, run today): **3,776 rows across 26 date dirs, 2026-09-05 through 2026-09-30** - matches `lens/corpus.md:23` exactly. Rows are raw header+abstract txt, untagged by area (sample: `state/arxiv/2026-09-05/2609.03324v1.txt`, DE-Venus RLVR). Per-day sampled: 09-05:101, 09-06:148, 09-07:253, 09-08:1, 09-09:242, 09-10:230, 09-12:1, 09-15:1, 09-19:1, 09-30:234. For THIS area, the pre-09-18 bulk-dump rows (975+ in 09-05..09-10 alone) predate the decision-model wave breaking on HN (JevBench 09-22, Ollaya 09-25, Ollama support 09-30) and carry no area routing - they are the stale-past-usefulness candidates. The prune/re-tag call belongs to the corpus owner; today's arxiv sibling already adjudicated 35 rows explicitly, so coordinate before deleting anything.

## Verification owed (funded tier, per laws.md:23)

1. nimble/tev1 typed-decision accuracy + 91 ms claim - run the estate's own eval on the Windows host before any scut-lane promotion.
2. duane.sh Qwen3.5-4B numbers - single-author blog, Opus-judged; medium confidence; replicate cheaply on our own 4090-class hardware if the recipe is adopted.
3. Strata's 125B-MoE-on-8GB claim - 4 pts, repo-only, unverified.
4. "GLM 5.3 flash on AMD GPUs 670 tok/s" - tweet, unverified.

## Method notes (honest limits)

- Overlap greps: `catalog/catalog.jsonl` grepped for every candidate term (full); `memory/` was grepped full-tree for 9 terms before the scan was stopped for runtime (memory corpus zone is 355k+ rows); remaining terms ran against a scoped set (memory/rib, memory/press, memory/improve, memory/research_packs, memory/research_polished, memory/attention.md, memory/live_from_grok.md, both frontier_olm sweep trees). Corpus-zone matches seen before the kill were generic-text noise (Cactus in game-design/gutenberg files) except where noted.
- The 434-hit "glm-5" query returns mostly comment rows on the Anthropic "GLM-5.3 and the spread of advanced cyber capabilities" story (heavy thread 09-29/30, plus NIST CAISI assessment story 49905262) - security-policy signal, adjacent to but outside this area's lane; not deep-read.
