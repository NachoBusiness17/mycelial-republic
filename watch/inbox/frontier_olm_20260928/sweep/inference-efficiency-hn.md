# sweep: inference-efficiency via HN (frontier_olm 2026-09-28)

source-fetched: 2026-09-28 (run executed 2026-09-29 UTC window; stamp per ask)
Lane: frontier_olm 2026-09-28 sweep seat (inference-efficiency). Door: Hacker News via hn.algolia.com API + news.ycombinator.com item pages.

## Door health

- Algolia API worked on all 11 queries (search_by_date, tags=story). No 403s.
- `numericFilters=created_at>2026-08-30` returned nbHits 0 on both attempts (once url-encoded as %3E), while the same query without the filter returned hits. Cause unverified; recency therefore came from search_by_date's own date-descending sort plus manual window filtering. Fallback per recipe (relevance endpoint) attempted once with the filter and degraded the same way; no fabricated success claimed.
- news.ycombinator.com item pages fetched clean (no 403, no redirect wall).
- One local hazard: `memory/runs/quote_audit_wide_20260925/inbox_concat.txt` (37,863,872 bytes) and `memory/thinking/app_reasoning.jsonl` (22,188,172 bytes) made a naive full-string grep hang; the overlap scan was redone as a line-streaming scan (see overlap ledger).

## Pass 1: candidate pool (in-window stories considered, created 2026-08-30 onward)

37 distinct candidates across 11 Algolia queries (speculative decoding, llama.cpp performance, ollama, vLLM, quantization LLM, LLM energy power consumption, consensus decoding, Windows LLM inference, power profiling GPU, FlashAttention kernel, tokens per second, energy per token inference, MoE offload VRAM). Headline candidates: 49859982 Faster prompt lookup drafting in llama.cpp (09-26, 85 pts / 12 comments); 49596054 Speculative Decoding in vLLM on AMD GPUs (09-07, 145 / 53); 49524447 Slotstream 104GB Qwen on 48GB Mac (09-01, 240 / 118); 49882781 MicroLLM Lab (09-28, 243 / 85); 49823348 Mercury 2.5 at 770 tok/s (09-23, 151 / 92); 49727511 Swift-Qwen3.8-27B (09-16, 33 / 17); 49876817 2.2x tok/s Intel Arc (09-28); 49845314 multiGPU MoE llama.cpp fork (09-25); 49884625 ESP32S3 BitNet cluster (09-28, 98 / 19); 49529209 MoE expert offload on 2-core Celeron (09-01); 49557885 Distributed PyTorch Profiling (09-03); 49851266 Speculative Reward Hacking (09-25); 49626887 You Could Have Come Up with Speculative Decoding (09-09); 49599031 Spec Decoding: How It Evolved (09-07); 49582850 Lossless Spec Decoding survey (09-06); 49543221 NVIDIA co-design spec decode (09-02); 49500821 Reward Guided Speculative Decoding / GSI (08-30); 49510441 Slotstream 4-bit first post (08-31); 49523381 GPT-OSS un-break (09-01); 49674280 Gemma 4 on Windows XP (09-12); 49878572 Jeva.cpp (09-28); 49882129 Nibia Fabric (09-28); 49889751 token-speed hosting (09-29); 49882932 Why we removed Ollama from Return (09-28); 49889447 ContextMemory (09-29); 49767564 CUA-S1 (09-19); 49497451 300M training in 1.5GB (08-30); 49462561 LPDDR5-PIM 650 tok/s (08-27, out by 3 days); 49264007 DFlash tok/s (08-11, out); 49378710 DGX Spark spec-decode bench (08-20, out); 49396806 SlimSpec (08-22, out); 49417257 LLM Quantization Part 3 (08-24, out); 49099601 AI content footprint (07-29, out); 47960034 Token Thermodynamics (04-30, out); 47426564 WattSeal power monitor (03-18, out); 47691182 OS megakernel tok/watt (04-08, out).

Out-of-window note: the energy/cool-heat tooling candidates that exist on HN (WattSeal PC power monitor 47426564, Token Thermodynamics 47960034, kilowatt-hour LLM billing 48684027, luce-megakernel tok/watt 47691182) are all March-June 2026, outside the 30-day window; none banked.

## Pass 2: deep reads (8 pages fetched and read end to end)

1. https://jadidbourbaki.github.io/blog/prompt-lookup-llama-cpp/ (+ thread https://news.ycombinator.com/item?id=49859982)
2. https://vllm.ai/blog/2026-08-23-speculative-decoding-amd-gpus (+ thread https://news.ycombinator.com/item?id=49596054)
3. https://grigio.org/how-i-got-2-2x-more-tokens-per-second-from-llama-cpp-on-intel-arc/
4. https://arxiv.org/abs/2506.04118 (GSI, reward-tilted speculative sampling; the HN listing titled it Reward Guided Speculative Decoding)
5. https://news.ycombinator.com/item?id=49524447 (Slotstream thread; repo github.com/carloslfu/slotstream not separately fetched)
6. https://news.ycombinator.com/item?id=49823348 (Mercury 2.5 thread; artificialanalysis.ai page itself not fetched)
7. https://news.ycombinator.com/item?id=49727511 (Swift-Qwen3.8-27B thread)
8. https://zhenyu.github.io/2026/09/02/why-a-gpu-profiling-capture-turned-into-a-distributed-systems-problem/

## Findings per research question

### RQ1. Speculative / consensus decoding for small local models; does anything answer rib Q1 (consensus-decode redesign)?

- llama.cpp-side, directly adoptable: prompt lookup drafting (n-gram draft, no draft model) got a 42x drafting-path speedup and 2.6x memory cut in a fork, purely by fixing data structures: inner maps were being copied every drafting step, unordered_map replaced by ankerl::unordered_dense::segmented_map, inner map by sorted vector with branchless binary search, static cache by Lemire's constmap on binary fuse filters ("position in the high 40 bits, count in the low 24 bits"), plus a threshold precheck ("up to 4.2x faster with a static cache"). Acceptance rates unchanged; load "6.32x to 16.12x faster, from 3.76 s to 0.23 s". Caveats the author states: benchmarks replay text through llama-lookup-stats rather than a real model, thresholds still hard-coded at b11182, dynamic cache outer map not yet constmap. The estate's janitors (gemma:2b, gemma4) run llama.cpp, so this fork is a drop-in candidate for the local tier.
- Method vocabulary current as of 2026-09: vLLM on AMD ships five draft families, "Current vLLM supports mtp, eagle3, dflash, and dspark as method values", with measured 1.9x-2.9x throughput on 26-35B MoE targets at proposal length N=7, and honest failures (Qwen3-8B EAGLE-3 hit 0.44x on MATH500 at N=1, i.e. worse than baseline). For 2B-8B targets the paper's own small-model rows are the caution: spec decode gains shrink and can invert as the target gets smaller and decode gets cheaper.
- Closest published shape to rib Q1 (lens laws.md:68: "a decode mapping to the ACTUAL task output space (numbers/text) is named 'a real redesign, not a patch'"): arxiv 2506.04118 (GSI) replaces exact distributional match with a reward-tilted acceptance target, provably approximating the reward-tilted policy and beating soft best-of-n "while reducing end-to-end latency by up to 28%". This is decode whose acceptance criterion lives in the task-output/reward space, not the story-space the estate's riddler surrogate used (RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:25, :40-43). It is adjacent, not identical: GSI is single-target-plus-reward speculative sampling, not multi-model flock consensus, and the abstract does not give RSD's (Liao et al. 2025) accept mechanics. Verdict: Q1 stays open; GSI names the design shape (verify against the task's own output-space objective, accept approximation) and is the first concrete prior art the estate has for it.
- Anti-pattern worth a rib: "Speculative Reward Hacking in Coding Agents" (49851266, 09-25) - reward-guided decoding is exactly the surface where draft and verifier collude; not deep-read, candidate only.

### RQ2. Best tok/s serving stack on Windows for 2B-8B

- No clean 2B-8B Windows benchmark surfaced in-window on this door. Closest replicable evidence:
- Intel Arc integrated GPU on a Windows-class laptop (Core Ultra X7 358H + Arc B390, 30 GiB unified): llama.cpp 0.5.0-dev Vulkan build (-DGGML_VULKAN=ON -DGGML_NATIVE=ON), Qwen3.6-35B MoE Q4_K_M, three changes took live server completions "from 15-17 t/s to 33-36 t/s", 38.7 t/s with n-gram speculation at draft n=2: (1) CPU_MOE 1 -> 0 ("The real cost is 55% of your decode throughput" - the old README claimed 10%), (2) batch/ubatch 512 -> 2048, (3) spec-draft-n-max 5 -> 2 ("n=2 is the sweet spot", +32%; n=5 failed allocating a 236 MB buffer). Threads 2-16, CPU governor, and KV quant type moved <=1%; --no-kv-offload was catastrophic (2.85 t/s). The flag recipe is directly replicable on the estate's Windows box for the janitor 2B-8B lanes even though the tested model is bigger than 8B.
- The same HN day carried "2.2x more tokens per second from llama.cpp on Intel Arc" at only 4 points / 0 comments; the sibling lane's Panther Lake backend benchmark (grigio.org, Vulkan vs SYCL vs OpenVINO vs CPU) is already held at memory/runs/gapwave/hn_x_fanout/local_serving.md - this new post is the follow-up and is new to the estate.
- vLLM local mode: absent from the in-window conversation for small models; the only vLLM performance thread is the AMD one above (server-grade MI300X/MI355X). Ollama shows up in-window only as product churn ("Why we removed Ollama from Return", 49882932; Ollaya 49848269 at 613 pts, a different project), not as tok/s evidence. Honest verdict: HN does not answer RQ2 for 2B-8B on Windows this month; the replicable experiment is the Arc flag recipe plus the prompt-lookup fork, run on our own hardware and measured with our own llama-bench.

### RQ3. Profiling methods attributing GPU/RAM/process cost to agent lanes on Windows (rib Q9)

- In-window HN has no Windows-native process/GPU attribution method. The one substantive profiling item is K8s/Linux: Meta-style MAIProf decomposition with torch.profiler + Kineto capture, dynolog node daemon, HTA analysis; per-rank, per-GPU, per-attempt attribution via identity-bound, checksummed trace manifests; the engineering lesson is dispatch semantics ("sending a request does not mean Kineto actually accepted it, and a file appearing on disk does not mean it is complete") and per-(job, attempt) coordinators with verify-then-publish receipts. Maps to Q9's shape (attribution = process-tree + job-object identity + receipts) but is not a Windows answer; nothing closes Q9, and the rib's own record stands: the CIM-tree plan is recorded as advice, not adoption (RIB_RUNAWAY_PYTHON_20260810.md:51-61; GROK_ADVICE_RUNAWAY_PYTHON_20260810.md:5-21; lens laws.md:76).
- Windows-relevant nugget from the AMD thread (not Windows itself): pyrolistical's bandwidth arithmetic sanity-check of claimed tok/s ("a ~33 tok/s memory-bandwidth ceiling on a single R9700 unless tensor-parallel MTP is involved") is exactly the kind of ceiling check the estate should run against any per-lane GPU attribution claim.

### RQ4. Activity/energy profiling, cool vs heat per lane, no kernel drivers (rib Q7)

- Nothing bankable in-window. All HN energy-profiling items found are outside the 30-day window: WattSeal PC power monitor (47426564, 2026-03-18), Token Thermodynamics notebook (47960034, 2026-04-30), kilowatt-hour LLM billing (48684027, 2026-06-26), luce-megakernel tok/watt (47691182, 2026-04-08), AI content footprint ranges (49099601, 2026-07-29). None read end to end, none banked as items.
- Honest verdict: this door did not produce a driverless per-process energy tool this month. The cool/heat map (RIB_FREE_USAGE_POLICY_20260823.md:30-37) remains fed only by the estate's own observed cool/heat signals; if the operator wants an HN answer the search needs to leave this door (AnandTech-style reviews, uProf/VTune release notes, GitHub).

### RQ5. 2026 kernel or quantization wins vs the 109.4M tok/h fan-out envelope

- Local-side wins are real and stack: prompt-lookup drafting path 42x (above), Swift-Qwen3.8-27B post-training cutting reasoning tokens ~40-60% at 1.95x speed with <1pp accuracy loss on most in-house tests (GPQA-Diamond 88.4 -> 88.3 with 58% fewer tokens; honest regression disclosed: AIME 2026 98.7 -> 94.0 from a token-penalizer bug), MoE expert streaming to SSD at 12 tok/s for a 104GB 4-bit model on a 48GB Mac with the model's MTP head adding "86% acceptance and about 1.24x faster decoding", ESP32S3 1.58-bit BitNet at 98 points (not deep-read), Mercury 2.5 diffusion LLM at 770 tok/s hosted with the thread's consensus that it is "stupid and it's fast" (below-average intelligence rank).
- None of these touch the fan-out envelope's binding constraint. The estate's 109.4M tok/h was measured on the z.ai account dispatch shape (width 10, maxAttempts 11, rolling-throughput cap), and every win above changes LOCAL tokens-per-joule or tokens-per-second, not provider rolling throughput. HN this window gives no counter-evidence that provider-side caps loosened; the Mercury thread even documents provider-side waitlists and silicon-etched speed ceilings as the frontier there. Verdict: dispatch shape remains the binding constraint for fan-out; kernel/quant wins change the local tier's economics, which per the driving ladder is the sensing tier, not the funded workhorse tier (RIB_DRIVING_LADDER_20260928.md:7-12).
- Cross-check worth keeping: the thread rebuttal to Ray-tracing-style vendor numbers - Roark66 in the AMD thread warns Intel's 1400 tok/s Arc claim "relied on 200 users sharing one prompt"; the estate should hold its own receipts to the same standard.

## Overlap ledger (greps run this ask)

Commands run via .venv/Scripts/python.exe: (1) a 22-pattern count scan of catalog/catalog.jsonl + memory walk (os.walk over memory/, extensions md/json/jsonl/txt); (2) line-streaming scans of the two oversized memory files after the naive full-string scan hung; (3) a sibling-sweep cross-scan of watch/inbox/frontier_olm_20260928/sweep/*.md.

- catalog/catalog.jsonl: 0 hits for every candidate title/phrase (prompt.lookup, prompt-lookup-llama, Speculative Decoding in vLLM, vllm.ai/blog/2026-08-23, 2.2x more tokens, Intel Arc, Mercury 2.5, 770 tokens, Swift-Qwen3.8, ukisai, slotstream, MAIProf, Holistic Trace Analysis, dynolog, Celeron, ESP32S3, jadidbourbaki, grigio.org, artificialanalysis.ai/models/mercury, Radeon AI Pro R9700).
- memory/: 'speculative decoding' concept is held 45 places (frontier scout row f-012 "Speculative Decoding - 2-3x inference speedup" at memory/frontier/scout_findings.jsonl; the translation dict "speculative decoding = deliberate-ask" at memory/continuity/seat_memory_20260927/llm-internals-syllabus-arc.md) but none of the specific 2026 posts were held.
- Already-held by a sibling: Swift-Qwen3.8-27B is banked twice in memory/runs/gapwave/hn_x_fanout/local_serving.md and skill_quantization.md, and listed in the sibling sweep quantization-compression-hn.md; EXCLUDED from my items per the no-rebanking rule.
- Partial: grigio.org held for the older Panther Lake post (gapwave local_serving.md); the 09-28 Arc post is new.
- steps.jsonl hits for almost every pattern are this session's own trajectory echo (session ids sess_dwf-...-actor_3_30, ts 2026-09-29) - self-echo, not holdings.
- slotstream appears only inside subagent session transcripts (memory/thinking/app_reasoning.jsonl, sess_subagent_*/sess_6d6cbd91 rows) - not a banked holding, so banked here.
- Mercury 2.5: one line-match inside an archivist harvest digest (memory/runs/quote_audit_wide_20260925/inbox_concat.txt, 37.8MB) whose visible fragment is a 2026-09-01 harvest header; no Mercury holding identified.

## Honesty block

- Read end to end (8): listed above. Everything else in pass 1 is a candidate from API listings only, not banked.
- Not fetched: github.com/carloslfu/slotstream repo, artificialanalysis.ai/models/mercury-2-5, any Microsoft/NVIDIA docs, the DGX Spark benchmark, SlimSpec, and the reward-hacking post (candidate only). Their numbers above come only from the pages listed as read.
- Not run: any estate gate, test, or benchmark; no local llama-bench replication of the Arc recipe (that would need the estate GPU box and is the natural next experiment).
- Quotes are relayed through the WebFetch reader (small model extracts verbatim spans); where a quote contained a unicode multiply sign it was transliterated to plain x and marked in the item note. Item confidence is set accordingly (0.85-0.9), not 1.0.
- em/en dash scan: run on this file before landing; see receipt line in the run result.
