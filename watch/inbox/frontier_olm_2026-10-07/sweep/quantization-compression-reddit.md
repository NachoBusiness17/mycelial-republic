# Sweep: quantization-compression via reddit - 2026-10-07

source-fetched: 2026-10-07. Ask: five research questions feeding the owed qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B (watch/inbox/frontier_olm_2026-10-07/lens/burns.md:95-98, owed at :216-225) and RIB_GPU_LADDER_20261001.md (lens/burns.md:134-136).

## Door status (all attempted this sitting)

- `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` (WebFetch): returned Reddit page shell + "Log in to use old Reddit" - login-walled, no posts. webReader on same URL: same wall.
- `www.reddit.com/r/LocalLLaMA/top.json` (WebFetch): HTTP 403 Blocked.
- `www.reddit.com/.../top.rss` (webReader): HTTP 429.
- `www.reddit.com` post permalink HTML (webReader): "Reddit - Please wait for verification" bot interstitial.
- pullpush.io submission search: two spaced attempts, both HTTP 429.
- redlib mirrors: catsarch 429, perennialte 403, rl.bloat.cat ECONNRESET.
- WORKING DOORS: `arctic-shift.photon-reddit.com/api/posts/ids?ids=` and `/api/comments/search?link_id=` (open Reddit archive; posts/search works newest-first only, no score sort, `title`/`after` params 422) + WebSearch `site:reddit.com` (the recipe's sanctioned fallback).
- This replicates the estate's own record: "every Reddit JSON door" listed dead at lens/burns.md:211-212.

## Instruments

Pass 1: 5 WebSearch queries (Q4_K_M/Q8_0 benchmarks; KV cache quant; Vulkan llama.cpp; Unsloth dynamic/imatrix; r/ollama+r/LocalLLM) -> 40 candidate threads. Dates/scores verified per-ID via arctic-shift posts/ids. Strict last-30-days window (2026-09-08..10-07): no quant thread surfaced through any live door (search engines index nothing that fresh; archive newest-feed shows only low-score same-day posts). Freshest strong cluster is Aug 2026. Recorded as fact, not filled.

Pass 2: 9 threads read end-to-end (post body + comment tree via arctic-shift), plus the linked llama.cpp PR 21038 read directly on GitHub. 7 banked as new; 2 excluded as known work (below).

## Banked items (new to the estate)

### 1. Qwen 3.6 27B BF16 vs Q4_K_M vs Q8_0 GGUF evaluation (1sxzqry)
https://www.reddit.com/r/LocalLLaMA/comments/1sxzqry/qwen_36_27b_bf16_vs_q4_k_m_vs_q8_0_gguf_evaluation/ - gvij, 2026-04-28, 695 pts, 152 comments, r/LocalLLaMA.
Task-graded (not perplexity) three-way ladder on llama-cpp-python, n_ctx 32768: HumanEval/HellaSwag/BFCL averages - BF16 69.78% (15.5 tok/s, 54 GB), Q4_K_M 66.54% (22.5 tok/s, 28 GB), Q8_0 66.15% (18.0 tok/s, 42 GB). Author: "Q4_K_M looks like the best practical variant here"; Q8_0 "a bit underwhelming in this run". Per-task shape: BFCL (function-calling, agentic) essentially flat across quants (63.25/63.00/63.00); HumanEval most sensitive (-5.5 pts at Q4_K_M).
Comment-tree value for the owed 7B A/B: ikkiho - at N=100, Wilson 95% CIs are roughly +/-7-10pp, so the Q8<Q4 inversion sits inside noise; run 3-5 seeds. suicidaleggroll: "That just means it's a sampling error, and OP didn't perform enough iterations." Shoddy-Tutor9563: single-run results "are not trustworthy". ClearApartment2627: benchmarks use ~4k contexts; "Aggressive quants (<q6)... fall apart in real life" at 30k+. dionysio211: Q8 losing 3.7 pts vs BF16 is notable for something "close to lossless".
Q1 answer: published task-graded deltas at the ~27B scale cluster at roughly -3 to -5 points avg from BF16 at both Q4_K_M and Q8_0, with the Q4-vs-Q8 ordering itself unstable under single-run N - the estate's A/B must be multi-seed or it measures noise.

### 2. Introducing Qwen3.8-27B Dynamic v3 Unsloth GGUFs (1vsr67c)
https://www.reddit.com/r/LocalLLaMA/comments/1vsr67c/introducing_qwen3827b_dynamic_v3_unsloth_ggufs/ - danielhanchen (Unsloth), 2026-08-16, 1,581 pts, 239 comments.
The strongest open per-layer protection scheme shipping now: Dynamic v3.0 claims "10% higher accuracy for the same size"; 1-bit quants "retain 77% accuracy" running on 8 GB RAM; pure PTQ (no QAT), imatrix file public. Artifacts: https://unsloth.ai/docs/basics/dynamic-3.0-ggufs and https://huggingface.co/unsloth/Qwen3.8-27B-GGUF.
Community verification is mixed: jonaddb's independent A/B found UD-Q4_K_XL indistinguishable from a competitor AD-Q4_K_M ("perplexity gap well inside the error bars", kept the ~765 MiB smaller one). TastyStatistician: IQ3_XXS at 40K context "thought for 8 minutes then filled the context without completing the task". BirdForsaken6616: 32-token KLD windows may not generalize to long agentic runs - the short-window-metric critique that mirrors our task-graded law. Sizing caveat (NovaXeros/rekh127): file sizes partly reflect MTP-head removal, "IQ2_S is the first one with ut removed".
Q2 answer: Unsloth Dynamic v3 (open, ships GGUFs + public imatrix) is late-2026 default practice for per-layer protection; independent parity reports at Q4 and failure reports at IQ3/40K.

### 3. Are q4 quants suddenly OK now? (1vsmrwn)
https://www.reddit.com/r/LocalLLM/comments/1vsmrwn/are_q4_quants_suddenly_ok_now/ - bigb159, 2026-08-15, 117 pts, 121 comments, r/LocalLLM.
OP: past Qwen q4 gave "too many loops and inaccurate results in my agentic usage"; in comments, "I think it's an agentic thinking problem" - the model loops, over-verifying via tool calls for 20 minutes; looping appears mainly at long context, fine under 8k; turning thinking off helps.
altz3r0 (production): Q6 vs near-BF16 showed 12% divergence in subtitle translation and shipped production-fixable code where the aggressive quant didn't. feverdoingwork: months of production INT4 AWQ on Qwen 27B; with 3.8 "I think using any q4 should be fine". Any_Meringue_7765 (counter): Q4 burned 4 hours and 4x 256k context on a dark-mode toggle and broke it. Adventurous-Paper566: llama.cpp added TurboQuant-inspired rotation; Q4_K_XL UD3 solid but "Q6 reste significativement meilleur". TimAndTimi: commercial APIs already serve 4-bit.
Q1 answer: agentic degradation at Q4 is real, context-length-linked (loops >8k), model-generation-linked (Qwen 3.8 more tolerant than 3.6), and visible in production traces - not in short-window perplexity.

### 4. Qwen3.5-35B-A3B quantization quality + speed (1rei65v)
https://www.reddit.com/r/LocalLLaMA/comments/1rei65v/qwen3535ba3b_quantization_quality_speed/ - gaztrab, 2026-02-26, 130 pts, 69 comments.
Counter-evidence on mixed precision: on this MoE, "UD-Q4_K_XL is significantly worse than standard Q4_K_M on this model" - PPL 7.1702 (+9.7%) vs Q4_K_M 6.6688 (+2.1%) vs Q8_0 6.5342. So Unsloth Dynamic is not universally above plain K-quants; MoE calibration is a failure mode. Same post: q8_0 KV cache called "a free lunch" (+12-38% throughput); --n-cpu-moe 24 tuning reached ~70 tok/s at 14.9 GB VRAM on RTX 5080 + Ryzen 9 9950X (hybrid CPU-offload evidence, though CUDA-side).
Q2 answer: per-layer protection schemes must be re-validated per model family; MoE + imatrix miscalibration can invert the Dynamic-vs-plain ordering.

### 5. I'm still surprised on how good the kv quantization has become (1u6bwz0)
https://www.reddit.com/r/LocalLLaMA/comments/1u6bwz0/im_still_surprised_on_how_good_the_kv/ - DeepBlue96, 2026-06-15, 64 pts, 39 comments.
OP: "kv at q4_0 (even the drafter is q4_0 kv) and still manages to find the info accurately in a 100k context".
Comment-tree mechanisms: Lirezh - llama.cpp PR #21038 added Walsh-Hadamard rotation before attention so quantization superblocks protect values as designed; it "is auto-disabled on non 64 dimension divisible k and v heads" and "fails silently" (a real serving pitfall for our CPU/Vulkan estate). Anbeeld (24 pts): "Qwen passes needle in a haystack with basically any sane KV cache quantization" but q4_0 can still break tool calls or degrade over long context - retrieval tests under-measure agentic damage. dunnolawl: Harry Potter long-context tests are contaminated ("they could probably regurgitate most of that without the text being in the context"). My_Unbiased_Opinion (counter-report): Qwen3.6 27B IQ4_XS + Q4 KV at 262K context on a single 3090, "zero failed tool calls" with MTP. Fragrant_Scale6456: --cache-ram 32768 checkpoint retention cut cache-invalidation wall time from 13% to 2% at 192K.
Q4 answer: the rotation-era llama.cpp KV stack (banked via 1s720r8/PR 21038) is what public reports now measure against; the open frontier is task-graded KV testing (tool calls, structured output) - needle tests pass under everything.

### 6. Made a quantization-aware trained (QAT) Qwen3.8 27b 2-bit gguf quant (1vvls0u)
https://www.reddit.com/r/LocalLLM/comments/1vvls0u/made_a_quantizationaware_trained_qat_qwen38_27b_2/ - Chance_Ease_9413, 2026-08-19, 112 pts, 37 comments, r/LocalLLM.
"Outperforms Unsloth 2 bit quants at reasoning and code at smaller file size. Unlike most other community quants that are PTQ, this one is QAT." Open artifact: https://huggingface.co/sdkyuan/qwen3.8-27B-qat-q2_0-gguf.
overand (22 pts, top skepticism): "How exactly is it 'quantization-aware training' if you didn't train the model?" - the QAT label is doing heavy lifting. Healthy-Nebula-3603: classic degradation benchmarks obsolete, run "swe-pro multi-step tests" instead. OP cites ParetoQ ("model dist changes a lot at 1-2 bit"), plans q1_0 next.
Q2/Q3 answer: at extreme compression (1-2 bit), community practice is drifting from pure post-hoc mixed precision toward QAT-style or hybrid schemes; verification is contested.

### 7. When should you choose F16 over Q8_0 quantization? (1q0ci23)
https://www.reddit.com/r/LocalLLaMA/comments/1q0ci23/when_should_you_choose_f16_over_q8_0_quantization/ - dtdisapointingresult, 2025-12-31, 19 pts, 63 comments. Older than the window; banked because its comment tree is the densest public taxonomy of what to protect.
OP: "We've all read about how Q8_0 is 'virtually indistinguishable' from F16 when doing inference."
From the raw comment JSON (read in full): GoodTip7897 - "Even q8_0 kv causes drifts over long contexts or reasoning chains" (and: new linear-attention models may make KV quant obsolete). TSG-AYAN - "Context should be kept at FP16, I have noticed heavy degradation at even Q8. Quanting only V cache seems to help a little". CheatCodesOfLife - "q4_k with fp16 embedding/out sounds better than pure q8" (embedding/output protection at low bits). bigjeff5 - I-quants "at 4 bits (average) maintain up to 80%+ of the performance of bf16". daHaus - "programming and arithmetic are extra sensitive to quantization due to the tokenizer". MelodicRecognition7 - keep mmproj (multimodal projector) FP16.
Q2/Q4 answer: folk best-practice protection list = KV/context at FP16-or-high, V-before-K if forced, embeddings/output layer, mmproj; task-sensitivity ordering (arithmetic/code > chat).

## Confirmed known work - read but NOT banked (re-banking = waste)

- KVarN (Huawei, 1twptw2, 2026-06-05, 415 pts): already in catalog 18 rows (kvarn_comments.json 23,784 B, kvarn_pullpush.json, receipts, find_kvarn.ps1) plus the paper PDF at memory/runs/gathering_expedition/p2_2606.03458.pdf. My read confirmed repo github.com/huawei-csl/KVarN, arXiv 2606.03458, Apache 2.0, vLLM single-flag, 3-5x context claims.
- KV rotation / q8-KV-degrades-AIME25 (1s720r8, 2026-03-30, 233 pts): already banked (reddit_json_1s720r8.json 189,908 B + arctic_refetch_1s720r8.json, 2026-10-02). PR 21038 table re-confirmed: AIME25 gpt-oss-20b F16 37.9%, Q8_0 31.7%->37.1% rotated, Q4_0 2.0%->21.7%.
- VeriLoop (2 catalog rows), BreadthKV (1), TurboQuant (15): all present.

## Per-question verdicts

- Q1 (7B-scale task-graded deltas): public analogs report ~-3 to -5 pt average drops from BF16 at both Q4_K_M and Q8_0 on mixed suites, BFCL/function-calling nearly flat, code most sensitive, and single-run Q4-vs-Q8 orderings unstable (CI +/-7-10pp at N=100). Direct input to the owed A/B design: multi-seed, task-graded, report CIs.
- Q2 (protected spine / mixed precision): late-2026 practice = Unsloth Dynamic v3 (open GGUFs + public imatrix, ~10% same-size claim) with per-model re-validation (MoE inversion case banked), folk protection of embeddings/output/mmproj, and a drift toward QAT-style schemes at 1-2 bit (open HF artifact, contested).
- Q3 (sub-1B ladder replication): NOT ANSWERED from reddit this pass. No public sub-1B quant ladder surfaced through live doors (closest banked signal remains PR 21038's Qwen3 0.6B q5_1 PPL 61.7->14.15 under KV rotation, already estate-known). OWED: a dedicated arXiv/HN search for sub-1B ladders.
- Q4 (KV frontier): rotation-era llama.cpp KV quant is the measured baseline (banked); fresh reddit signal says retrieval passes at q4_0 KV/100k but tool-calls/structured-output are the fragile surface; silent auto-disable on non-64-divisible head dims is the serving pitfall to check on our qwen2.5:7b before any KV-quant step.
- Q5 (CPU/Vulkan quant methods): THIN on reddit this pass. Vulkan candidates found were perf-wiring, not quant-method comparisons (1sb5jmv ARM-32 Vulkan bug 2026-04-01; 1suqqng iGPU-primary 2026-04-24; 1ooyr6r Vulkan-RPC 2025-11-05). The canonical measured surface is the llama.cpp GitHub Vulkan benchmark discussion #10879 (found via search, not read this pass). OWED: mine #10879 directly for 2B-9B Q4/Q8 tok/s on our hardware class.

Overlap instrument note: catalog greps ran with LC_ALL=C grep -i over catalog/catalog.jsonl (341,492,470 bytes, mtime 2026-10-07 03:37); memory/ greps were single-walk grep -r -l -i -E alternations; the 2026-10-07 lens (lens/burns.md:85-233) supplied the do-not-remine list. Disclosure: memory/trajectory/steps.jsonl (live seat-trajectory log, 68 MB) shows a sibling seat's sweep_qc bash loops fetched several of the same thread IDs (1sxzqry, 1vsmrwn, 1vsr67c, 1vvls0u, 1q0ci23 fragments) minutes before my reads, plus sibling-only candidates I did NOT read or bank (1tgk9y6 "quantizing_mtp_k...", 1t53dhp, and a "Qwen3.5-4B GGUF quants comparison (KLD vs speed) - Lunar Lake" thread, score 133). Catalog has zero rows for all 7 banked IDs, so nothing banked duplicates; the sibling's findings, wherever they landed, are not in this sweep dir's reddit lane.
