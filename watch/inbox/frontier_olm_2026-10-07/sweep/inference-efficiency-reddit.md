# Frontier sweep: inference-efficiency via reddit - 2026-10-07

source-fetched: 2026-10-07 · seat: sweep-inference-efficiency-reddit · doors: recipe doors DEGRADED, fallback used (recorded below) · 8 items banked, all read end-to-end by this seat

## Door status (honest record)

- `old.reddit.com/r/*/top.json?t=month` - DEGRADED: r/MachineLearning + r/LocalLLM + r/ollama timed out (60s); r/LocalLLaMA returned a JS "Welcome to Reddit" landing shell with zero post data.
- `www.reddit.com/r/LocalLLaMA/top.json` - HTTP 403 Blocked (network security).
- `old.reddit.com` thread pages - login wall; verified with curl -L: final URL `old.reddit.com/login/?reason=lor2&dest=...` (code 200 on the login page, thread never served).
- `www.reddit.com` thread pages - "Please wait for verification" wall (both WebFetch and the webReader MCP path).
- `r.jina.ai` proxy of reddit - "You've been blocked by network security" + 403.
- Wayback Machine - PARTIAL: post bodies sometimes captured (e.g. the NVFP8 thread), comments never captured in the snapshots tried; one capture was just the verification wall.
- redlib mirrors: `redlib.catsarch.com` 429, `rl.bloat.cat` ECONNRESET, `redlib.perennialte.ch` 403, `redart.com` empty. `safereddit.com` WORKS as a full mirror (post + full comments + dates + scores). All 8 deep reads below were fetched through `safereddit.com` thread URLs; canonical reddit permalinks are listed as the durable reference.
- Fallback discovery: WebSearch `site:reddit.com` per the recipe (worked intermittently; the search backend itself hit 1302 rate limits between queries - queries were spaced, not skipped).
- NOTE for the next seat (stolen from the 2026-10-01 sweep's receipt, `watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-reddit.md:3`): the public arctic-shift archive API (`arctic-shift.photon-reddit.com/api/posts/ids` + `/api/comments/search`) served that sweep full post bodies and comment trees byte-level - a second real door when safereddit eventually walls too.

## Method

- Pass 1 (broad): 35+ unique candidate threads collected across the five RQs via six WebSearch queries (FP8/llama.cpp; routing/cascade; reasoning-budget steering; MoE CPU tok/s; batch/offpeak pricing; r/ollama + r/MachineLearning). The r/ollama and r/MachineLearning doors yielded only pre-window threads (2023-2025 and Feb 2026 respectively) - no in-window items from either, recorded as a gap, not papered over.
- Pass 2 (deep): 8 threads fetched and read end-to-end via the safereddit mirror (OP + comments). One high-value candidate (r/LocalLLaMA "DeepSeek V4 being 17x cheaper...", 1t4s6g2) was UNREADABLE - three fetch attempts tripped a content filter (1301) regardless of prompt phrasing; it is NOT banked and stands OWED.
- Overlap: per-item greps of `catalog/catalog.jsonl` + `memory/` (results inline per item; memory single-pass grep ran to completion, see addendum).

## Items (strongest first)

### 1. Qwen3.8-27B - one week later: the r/LocalLLaMA + r/LocalLLM verdict
- url: https://www.reddit.com/r/LocalLLM/comments/1vvu1uj/qwen3827b_one_week_later_the_rlocalllama/ (read via safereddit.com same path)
- date: 2026-08-23 · RQ2 (reasoning-channel budget steering) + RQ4
- Verbatim: "low is the rational preset. xhigh is for leaderboard screenshots." (@superalesha's 67h/4,800-task run, quoted in-thread)
- Findings: llama.cpp web-UI "reasoning selector" is a hard token cap that truncates mid-thought - NOT Qwen's native effort levels (low/medium/xhigh, each trained into the model at RL time); the fix is `--reasoning-effort medium` or `chat_template_kwargs`. Measured: low matched xhigh at 89.3% with 1/7.5th the tokens; xhigh burns 6-11x more tokens for marginal gains (718s vs 112s wall for +1.5 visual points) but wins pass/fail tasks 9/12 vs 6-7/12; reasoning fully off costs 8-12 points. THE ESTATE-DOCTRINE HIT: the stock chat template's xhigh can "burn-20k-tokens-then-return-empty" - a literal measured empty-content failure from reasoning overruns, fixed by the froggeric community template. This is the exact EMPTY_REASONING terminal-never-refire failure mode (lens/laws.md:34-36) measured in the wild, plus the steering-vs-capping distinction our refire policy needs.
- Overlap: catalog grep "Qwen3.8" = 3 lines, all adjacent not duplicate (internal plan corpus/library/kev/PLAN_27b.md, a 2026-09-20 splash digest, Qwen3.8-Omni arxiv paper). PRIOR-SWEEP CROSS-CHECK: the 2026-10-01 inference-efficiency sweep banked the PRIMARY effort thread 1vpuh7m (measured low/medium/xhigh: 4,418 vs 39,398 reasoning tokens, 111.6s vs 717.8s) and pulled @superalesha's quant-at-xhigh results on the X side - so the effort-economics numbers are PRE-BANKED from primary sources. This megathread itself was DROPPED by that sweep's kv-cache sibling as out-of-window (named by ID in `kv-cache-context-engineering-reddit.md:17`, never read). NEW here: the hard-cap-vs-native-effort PSA, the burn-20k-then-empty failure + froggeric template fix, reasoning-off costs 8-12 points, pass/fail 9/12 vs 6-7/12.

### 2. Llama.cpp now with a true reasoning budget!
- url: https://www.reddit.com/r/LocalLLaMA/comments/1rr6wqb/llamacpp_now_with_a_true_reasoning_budget/ (read via safereddit)
- date: 2026-03-11 · RQ2 (mechanism)
- Verbatim: "when the given number of reasoning tokens is reached, we force terminating the reasoning." (u/ilintar, patch author)
- Findings: `--reasoning-budget N` implemented in the sampler (count tokens during reasoning, force-terminate at limit; -1 unlimited, 0 disables); `--reasoning-budget-message` injects a transition string right before the cutoff - without it quality craters; API field `thinking_budget_tokens` (naming mismatch, unification promised). Measured: Qwen3 9B HumanEval 94% full / 88% non-reasoning / 78% hard cutoff / 89% with the transition message at budget 1000 - a 16-point quality recovery from a one-line injected message. Qwen3.5-35B car-wash test: unlimited passes but thinks 83s; budget 1000 + message passes in 18s. Failure modes: Qwen3.5-27B resumes thinking OUTSIDE the tags after the forced `</think>` (~40k more tokens); newline needed at end of the transition message; u/coder543's proposed soft ramp (gradually boosting the end-of-think logit bias) still unimplemented upstream at that date. Qwen3's own paper (arXiv 2505.09388) ships the canonical stop string.
- Overlap: greps "reasoning-budget"/"reasoning_budget" catalog=0; memory holds the CONCEPT in run digests (memory/runs/compaction_eval/steps_frozen_20260920.jsonl, memory/runs/mickey17/MASTER_INDEX_20260920.md, memory/runs/salons/) and the 2026-10-01 sweep dir has zero hits on "true reasoning budget" - the specific mechanism thread and its HumanEval deltas are not held. New.

### 3. NInfer vs llama.cpp vs vLLM: quality + speed comparison
- url: https://www.reddit.com/r/LocalLLaMA/comments/1w821fg/ninfer_vs_llamacpp_vs_vllm_quality_speed/ (read via safereddit)
- date: 2026-09-05 · RQ4 (FP8/quant status in the llama.cpp lineage; throughput at quality parity)
- Verbatim: "Blindly adopting a new engine just for speed without verifying all other performance metrics is dumb." (OP, defending the methodology)
- Findings: RTX 5090 32GB eGPU + Ryzen 7840HS, Qwen3.8-27B. NInfer (NVFP4 + FP8 KV + MTP3 speculative at 76% acceptance, 2 lanes) vs llama.cpp (Q5_K_M + q8_0 KV): decode 158 vs 114 tok/s @1K (1.4x), 202 vs 72 @128K (2.8x); prefill 7,265 vs 1,545 tok/s @1K (4.7x); TTFT 138ms vs 670ms. Quality statistically indistinguishable (relevance 86/84/86%, reasoning 100/100/98%, p=0.69 on transcript QA). The speed delta is entirely MTP3 speculative decoding (vLLM ~70 tok/s without it). Comment pushback: mismatched KV dtypes (q8_0 vs FP8) weakens the comparison; a vLLM+DFlash2 patch exists; u/jonas-reddit reports SGLang DFlash2 50-60 to 90-100+ t/s in agentic work. FP8 status answer for RQ4: FP8 lives in the NVFP4/FP8-KV engine tier (NInfer/vLLM/SGLang); llama.cpp proper stays GGUF quants (Q5/Q8 KV) - consistent with the "Why no NVFP8 or MXFP8?" thread (1qsi8n2, Jan 2026, read via wayback OP-only, not banked as separate item).
- Overlap: grep "NInfer" catalog=0 (the prior sweep's "openInference tracing substring" note notwithstanding, current catalog grep is clean). PRIOR-SWEEP CROSS-CHECK: the 2026-10-01 sweep banked a DIFFERENT NInfer thread (1wcv38q, 3090 mini-benchmark: TG 170.7 vs 148.6 t/s on Qwen3.6-35B-A3B, llama.cpp still winning TG on dense 27B) - so the ENGINE is known. NEW here: the quality-parity table (statistically indistinguishable), FP8-KV/NVFP4 quant status, MTP3 76% acceptance attribution, and the llama.cpp-stays-GGUF lineage point. This thread (1w821fg) itself: not previously banked.

### 4. I don't believe in model routing anymore
- url: https://www.reddit.com/r/LLMDevs/comments/1vbqshh/i_dont_believe_in_model_routing_anymore/ (read via safereddit)
- date: 2026-07-31 · RQ1 (cost-per-blind-point routing priors)
- Verbatim: "for most of use cases, sticking to a single model is the best thing you can do." (OP u/nuno6Varnish)
- Findings: 4 months running a smart (prompt-inferred) router across 7,000 cloud users, then shut down. Four reasons: complexity can't be inferred from the prompt alone; caching cuts cost more than routing does; routers break behavior consistency; unpredictability has a cost. Hidden costs named: "Engineering, evals, maintenance, dealing with quality loss." Pushback in-thread is the useful part for us: rule-based routing by context/subagent works (small Qwen 27B for small bugs, Kimi/DeepSeek for 7+ file changes); route per-context not per-turn or you blast context into 10 different caches; adjusting EFFORT levels beats rerouting; cheaper models burn more tokens per task plus human review time, so per-token price is misleading. Estate fit: the published prior for our blind-point grid (lens/laws.md:104) - prompt-inferred complexity routing is the weak cell class; routing by question-class (which already dominates our variance, 36.3% vs 3.6%, lens/laws.md:47) and effort-steering are the survivors. No dollar figures - field report, not benchmark.
- Overlap: greps "model routing anymore" catalog=0, prior sweep dir=0; memory hits self-echo only (addendum). The prior sweep's Q3 routing evidence came from two OTHER threads (Chimera 1ulose2, router-burn 1wq9ipm) - this teardown is complementary, not duplicate. New.

### 5. PSA: No peak pricing during the weekend (DeepSeek)
- url: https://www.reddit.com/r/DeepSeek/comments/1vvcne3/psa_no_peak_pricing_during_the_weekend/ (read via safereddit)
- date: 2026-08-22 (effective 2026-08-23) · RQ5 (batch/offpeak economics for ds_workhorse)
- Verbatim: "I don't even need super low prices every day, would be nice if they looked at their api usage graphs and picked say 2 hours" (u/MikeX7s)
- Findings: the encodable rule - weekends (Sat/Sun Beijing time) are off-peak ALL DAY; weekday peak windows are 01:00-04:00 and 06:00-10:00 UTC; off-peak rates are half of peak. Community: planning usage around windows is the practical exploit; sentiment that dynamic pricing is a developer headache; speculation the weekend change signals falling demand. Related threads found but NOT deep-read (search-snippet level only, not banked): r/DeepSeek 1uio6yf/1uio0qn "V4 official launch + peak/off-peak pricing" (peak hours roughly double standard rates), r/vibecoding 1vo273x (V4 pricing change starting Aug 16).
- Overlap: greps "no peak pricing"/"peak pricing" catalog=0; memory hits were self-echo only (see addendum). The 2026-10-01 sweep covered DeepSeek input-CACHING economics (50x via API platform), not time-of-day pricing. New - and this resolves part of the owed DeepSeek invoice-strength discount check (lens/burns.md:222-223): the discount exists as time-of-day pricing, not an invoice line.
- CAVEAT for the lane runner: encode the windows, but verify current numbers against DeepSeek's pricing page before wiring money logic - a PSA thread is evidence, not a price sheet.

### 6. Trying to tame Qwen 3.8 27B pathological over-reasoning
- url: https://www.reddit.com/r/LocalLLaMA/comments/1w9zrpg/trying_to_tame_qwen_38_27b_pathological/ (read via safereddit)
- date: 2026-09-07 · RQ2
- Verbatim: "You are FAR better off just using the preset thinking levels the model was trained with instead of trying to change innate behavior" (u/tomz17, top comment)
- Findings: a failure catalog for over-reasoning (flip-flop "Actually.../Wait.../Hmm...", re-deriving established facts, 20k+ token deliberations on trivial problems, refusing user-stated facts, meta-reasoning instead of acting, loops until context exhaustion). Fixes ranked by thread consensus: native reasoning_effort levels > reasoning budget caps > fixed/sharp chat templates (froggeric Qwen-Fixed-Chat-Templates) > compaction hygiene > anti-overthinking finetunes (one claims 4x speed from lower overthinking, quality unverified). OP's own 550-token/11-rule system doc admitted to decay over a ~150k session. Estate fit: independent confirmation of items 1+2's doctrine - steer with trained-in effort levels, don't surgery the prompt; our EMPTY_REASONING refire policy should re-ask at lower effort, not just re-roll.
- Overlap: grep "over-reasoning" catalog=0; memory hits self-echo only; prior sweep dir grep "pathological"=0. New.

### 7. Software FP8 for GPUs without hardware support - 3x on memory-bound ops
- url: https://www.reddit.com/r/LocalLLaMA/comments/1q0x8ci/software_fp8_for_gpus_without_hardware_support_3x/ (read via safereddit)
- date: 2026-01-01 · RQ4 (FP8 status in the llama.cpp/Ollama lineage)
- Verbatim: "OP's kernels can directly replace fp8 matmul and that's what we need for the next step" (u/woct0rdho, Triton fp8-to-fp16 patch author)
- Findings: "Feather" (github.com/SuriyaaMM/feather) packs FP8 into FP32 via bitwise ops + Triton kernels, upcasting to FP16/FP32 in registers - claimed 3x on memory-bound GEMV/FlashAttention for RTX 20/30 (no advantage on 40-series; author walked back "any GPU"). Mechanism confirmed by commenters: half the bytes cross VRAM, math still on 16-bit ALUs. THE NEGATIVE FINDING THAT MATTERS TO US: entirely CUDA/Triton/PyTorch - Vulkan is never covered; and it is incompatible with SageAttention (no benefit if you already quantize attention to int8). For the estate's Vulkan rung (lens/burns.md:135-136): no software-FP8 path exists in this lineage as of this thread; FP8 remains CUDA-side, and the llama.cpp/Ollama line stays on Q8_0-class integer quants. This GATES the FP8 adoption question the lens asks: on Vulkan the late-2026 answer is still "not available; Q8_0 remains the ceiling."
- Overlap: greps "Software FP8" catalog=0, prior sweep dir=0; "Feather" catalog=1 line but it is the boids paper "Boids of a Feather Flock Together" (state/arxiv/2026-09-30/2609.37885v1.txt) and the 248 memory hits on "Feather" resolve to the Featherless PROVIDER (memory/burns/LEDGER.jsonl "Featherless /v1/models") plus unrelated text - not this FP8 project. New.

### 8. Steering vectors to limit thinking budgets?
- url: https://www.reddit.com/r/LocalLLaMA/comments/1wkif87/steering_vectors_to_limit_thinking_budgets/ (read via safereddit)
- date: ~2026-09-19 (mirror shows "18 days ago" from fetch day 2026-10-07) · RQ2
- Verbatim: "a vector can correspond to many different things" (u/Nakidnakid, on why steering vectors are risky for this)
- Findings: technique map for gradual thinking-termination, no measurements (question thread): steering vectors (cautioned - multi-behavior side effects), marker-token LoRA/finetunes (Swift-Qwen3.8-27B-GGUF penalizes reasoning-marker tokens), logit bias on `</think>`, strix-llama.cpp fork's multi-point reasoning budget, and plain `chat_template_kwargs: {"reasoning_effort": "low"}`. Estate fit: names the exact knobs a budget-steering rib could rank; the strix fork's multi-point budget is the soft-ramp idea u/coder543 proposed in item 2, now existing in the wild.
- Overlap: grep "steering vectors" catalog=0; memory holds the CONCEPT in run digests (memory/runs/ds_batches/*, memory/runs/gapwave/) but the prior sweep dir has zero hits on the phrase and this thread is unheld. New.

## Cross-cutting answer to the five RQs

- RQ1 (routing priors): the only late-2026 published field measurement found says prompt-inferred smart routing LOST to single-model + caching at 7,000-user scale (item 4); survivors are rule-based routing by question/context class and effort steering. No public benchmark with per-cell cost/quality dollar figures surfaced in-window - the estate measuring its own grid (lens/laws.md:104) remains the only path; OWED.
- RQ2 (reasoning steering): the strongest single find of the sweep - the ecosystem converged on trained-in effort levels (Qwen) + sampler-enforced budgets with transition messages (llama.cpp), and there IS a measured empty-content failure ("burn-20k-tokens-then-return-empty") with a template-level fix (items 1, 2, 6, 8). Hard caps truncate mid-thought and cost 8-16 quality points; transition messages recover most of it.
- RQ3 (multi-tier dispatch): nothing measured in-window beyond item 4's comment-tier evidence (cheaper models burn more tokens + review time; effort-adjust beats rerouting). Draft-verify/speculative-decoding savings ARE measured at engine level (item 3, MTP3 76% acceptance). Deeper multi-tier dispatch benchmarks: OWED.
- RQ4 (local throughput + FP8): item 3 gives the measured 2026-09 engine ladder on consumer hardware (llama.cpp 72-114 tok/s decode on a 5090 for 27B-class, 2-2.8x more with NVFP4+MTP engines at quality parity). MoE-vs-dense CPU/Vulkan numbers specifically: nothing in-window on reddit (search returned 2023-2025 and non-reddit sources only) - OWED; item 7 closes the FP8 half: no Vulkan FP8 path, CUDA/Triton only.
- RQ5 (batch/offpeak): item 5 encodes the DeepSeek time-of-day rule (weekends all off-peak; weekday peaks 01:00-04:00 + 06:00-10:00 UTC; off-peak = 50%). OpenAI/Anthropic/Gemini flat 50% batch APIs surfaced at search-snippet level only (r/OpenAI 1ijzuag, r/ClaudeAI 1fz86om, r/Bard 1ltx8mm) - older threads, not deep-read, not banked.

## OWED (never fabricated)

- The r/LocalLLaMA "DeepSeek V4 being 17x cheaper" thread (1t4s6g2): content-filter-walled on three attempts, unread.
- In-window r/ollama and r/MachineLearning threads: none existed in search results for these topics; both doors recorded empty for the window.
- Any per-cell cost/quality routing benchmark with dollar figures (RQ1's ideal): not found in-window.
- MoE vs dense 7B-class CPU/Vulkan throughput measurements (RQ4's ideal): not found on reddit in-window; candidate non-reddit sources (tiffena.me CPU benchmark, epoch.ai MoE analysis) noted but outside this sweep's reddit mandate.
- Verbatim quotes above are from the safereddit mirror renders; mirror text could differ from live reddit in minor ways.

## Overlap addendum (verified, run - not assumed)

memory/ is 585,384 files (find | wc -l), so the overlap check ran in three stages: per-phrase catalog greps (instant), a single-pass memory grep for all 11 phrases (completed), and targeted drill-downs into every hit that could mean a re-bank.

- SELF-ECHO RESOLVED: the phrases that counted 6-8 in memory ("burn-20k" 8, "model routing anymore" 8, "no peak pricing" 7, "over-reasoning" 6, "Software FP8" 7 in memory/trajectory/steps.jsonl) are THIS SWEEP'S OWN grep commands being trajectory-logged as they ran - they did not exist in memory/ before this seat. Not holdings.
- REAL PRE-EXISTING CONCEPT HOLDINGS (not threads): "Qwen3.8" x892 (the estate's own Qwen3.8 work incl. corpus/library/kev/PLAN_27b.md), "Feather" x248 (resolves to the Featherless provider, memory/burns/LEDGER.jsonl "Featherless /v1/models ... 22,032 models", plus unrelated text), "steering vectors" x80 and "reasoning-budget" x40+7 (run digests and ds-batch items: memory/runs/compaction_eval/, memory/runs/mickey17/MASTER_INDEX_20260920.md, memory/runs/ds_batches/). Concepts known, specific threads unheld.
- NInfer: 3 holder files (memory/runs/ds_batches/gapfold_items.jsonl, memory/runs/mickey17_v2/.../a01-olm-day2.json, memory/trajectory/steps.jsonl) - all point at the 2026-10-01 sweep's own activity; that sweep banked thread 1wcv38q, NOT this sweep's 1w821fg.
- PRIOR-SWEEP CROSS-CHECK (the decisive one): `watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-reddit.md` banked 10 threads for this SAME area; ID-and-phrase greps of that whole directory against all 8 of my items show two touchpoints only - 1vvu1uj was named-and-DROPPED as out-of-window by the kv-cache sibling (`kv-cache-context-engineering-reddit.md:17`), and 1w821fg's ID match was a false positive inside an unrelated tweet JSON. Zero of the 8 items below are re-banks; two carry partial-credit notes inline (items 1 and 3) where the prior sweep holds the primary numbers from other sources.
