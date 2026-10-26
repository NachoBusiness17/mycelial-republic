# Sweep: quantization-compression via Hacker News - 2026-10-07

source-fetched: 2026-10-07. Door: HN Algolia API (search_by_date + search, tags=story,
numericFilters=created_at_i>1788739200 = 2026-09-07, 30-day window), then per-item page fetches;
HN comment threads via news.ycombinator.com/item?id=...; one fallback door (webReader MCP) used
where WebFetch timed out. All quotes below are from pages I fetched this sitting.

## Doors and degradation

- hn.algolia.com API: worked. Queries run: quantization, quantized, GGUF, "KV cache", llama.cpp,
  Vulkan, "mixed precision", 1-bit, "KV quantization", quantization benchmark (relevance),
  ternary LLM. Three complex boolean queries (IQ2/Q4_K_M/AWQ combined, MoE quantization,
  quantization LLM relevance) TIMED OUT at 60s and were not retried verbatim - plain-term doors
  returned plenty, so coverage held.
- news.ycombinator.com item fetch: worked for thread 49611128; TIMED OUT twice for 49926773
  (Janus Vulkan GGUF runner, 106 pts) and once for the AMD Quark blog via WebFetch.
- Fallback door used as the recipe allows: webReader MCP fetched the AMD Quark post successfully;
  the Janus thread fetch returned only a truncated table header, so Janus is NOT banked (OWED, below).

## Pass 1 - candidates considered (35 on-topic, 30-day window)

Strong: 49611128 Quesma Qwen3.8-27B quant benchmark (286 pts); 49732931 Breaking the 1.58-bit
Barrier for Ternary LLMs (245 pts, arXiv 2609.16338); 49735410 DeepSeek-v4.1-Flash KV cache
compression (131 pts, zartbot); 49926773 Janus Vulkan GGUF (106 pts); 49643543 LRU harder to
beat than KV-cache papers (108 pts); 49869861 Quantized Reasoning Models Think They Need to
Think Longer (arXiv 2606.00206); 49727511 Swift-Qwen3.8-27B (33 pts). Mid: 49770070 ROCmFix/
InferBench Vulkan vs HIP; 49703818 GSQ-RCO Flash-Next GGUF; 49676635 bartowski per-tensor
layout maps; 49726446 grigio Panther Lake Vulkan/SYCL/OpenVINO/CPU; 49876817 2.2x llama.cpp
Intel Arc; 49847732 VeriLoop E2 BF16-to-IQ1_M; 49975499 AMD Quark Strix Halo; 49822130
Lifeboat no-quant; 49823211 quant-delta-predictor; 49743523 4-bit rotational quantization
(vector-DB, off-area); 49945575 KV cache memory wall; 49893944 Fathom per-query read depth;
49639110/49639339 DSv4.1-Flash tech report; 49812339 Transformers runs llama.cpp quants;
49813964/49774861 Bonsai ternary GGUFs; 49942092/49934323 llama.cpp Decision Models;
49734038 Quantifying Context Rot; 49758259 vLLM prefix cache agents; 49701675 KV efficiency
agentic; 49796779 what are KV caches; 49980637 Hopf spherical quantization; 49801526 Internet
for KV cache; 49911995 Magnitude; misc GGUF-runner items. 11 pages were then read end to end.

## Pass 2 - answers to the five research questions

### RQ1. Task-graded (not perplexity) quant deltas at 7B-scale class

Two in-window task-graded studies, both stronger than perplexity folklore:

- Quesma, Qwen3.8-27B GGUF ladder (BF16/Q8_0/Q4_K_M/UD-Q2_K_XL/UD-IQ1_S/M) on GPQA Diamond,
  IFBench, and Terminal-Bench 2.1 (agentic, 89 tasks, llama.cpp, F16 KV): Q8_0 and Q4_K_M
  "essentially indistinguishable from BF16"; Q4_K_M matches BF16 on Terminal-Bench; 2-bit shows
  "a noticeable fall"; 1-bit lands "around random chance on GPQA Diamond". Verdict sentence:
  "quantization damage is nonlinear: first there is no measurable change, then a small decline,
  and finally a collapse." The 2-bit model also writes ~25% more tokens on the same solved tasks.
- AMD Quark on Strix Halo, Qwen3.6-35B-A3B W4A16 (RTN, INT4/UInt4, group 32/128, GS32 exported
  to GGUF Q4_0/Q4_1 for llama.cpp): task-graded lm-eval table, deltas vs BF16 of -0.4 pt (BBH),
  -1.4 pt (MMLU-Pro), -2.0 pt (GSM8K), -2.5 pt (GPQA) for the llama.cpp INT4-GS32 config; IFEval
  noisy enough to sometimes sit above baseline. Honest caveat in the post: "The results do not
  indicate a single quantization configuration that is uniformly best across all tasks."

Estate tie-in: the owed qwen2.5:7b Q4_K_M vs q8_0 A/B (lens/burns.md:216-225 owed list) should
EXPECT a 0-3 pt task gap at Q4_K_M vs Q8_0 from published shapes, not a proportional-to-bits gap.
Also relevant: arXiv 2606.00206 (5 models, 1.5B-32B, 3 PTQ methods) finds quant damage shows up
as behavior, not just score: "in up to 52% of the quantized models' failures, models reach the
right answer in intermediate reasoning steps but do not output it", with a training-free logit
penalty on overthinking markers cutting CoT length 12-23% at preserved accuracy. The Quesma
1-bit result ("longer reasoning makes it worse") is the same phenomenon at the cliff edge.

### RQ2. Protected-spine / mixed precision, late-2026 best practice, open implementations

- bartowski's per-tensor layout maps (HF blog, llama.cpp ecosystem, open): learned per-tensor
  sensitivity via degrade-one runs (one tensor at q2_k, rest q8_0, KLD vs bf16 on wikitext),
  then a solver picks per-tensor quants under a size budget. Findings: "token_embd dominates
  the sensitivity scale" (8-16x the worst weight tensor, mostly recoverable at q4_k); depth is
  a U-shape (early+late layers need bits); "Per bit, small attention projections are the most
  sensitive"; ffn_gate "basically never worth any extra bits"; K-quants should not be crushed
  level-to-level while IQ quants can be crushed granularly to fund bumps; a canary KLD-per-bit
  check falls back to the old heuristic if a map regresses. This is the open llama.cpp-native
  implementation of exactly the protected-spine idea behind the estate's VeriLoop IQ1_M row.
- The Quesma HN thread adds the A/B design caveat the estate's owed test needs: wgd: "they
  tested Q4_K_M which should be just the standard K-quant without any imatrix calibration" - the
  smaller UD quants ARE mixed-precision, so "4-bit isn't actually a 'true' 4-bit here"
  (kouteiheika). For our A/B: name imatrix/UD status in the receipt or the comparison is
  apples-to-oranges.
- Already held by the estate (do not re-mine): GSQ-RCO (ISTA-DASLab; DASLab repos IST-DASLab/GSQ
  + RCO; arXiv 2604.18556 + 2605.00649) - deep-banked 2026-09-28 at
  watch/inbox/frontier_olm_20260928/sweep/inference-efficiency-reddit.md:61 with richer numbers
  than any in-window rerun (3.50 bpw matches BF16 on every benchmark; 2.40 bpw averages ABOVE
  BF16, 78.00 vs 76.94; 1.89 bpw pruned-expert Coder build keeps 91.3% SWE-bench Verified).
  My re-read of the pfeifferj Flash-Next GGUF card this sitting only corroborates: RCO search
  under exact size budget, embeddings + vision projector protected, non-expert matrices Q8_0.

### RQ3. Day-6 cliff shape (bf16 0.757 -> Q8_0 0.750 -> Q4_K_M 0.703, 0.6B decision model)

- The shape replicates in-window at 27B: Quesma's ladder is flat (BF16/Q8_0/Q4_K_M) then bends
  (2-bit) then collapses (1-bit). The estate's -0.7% (bf16->Q8_0) then -6.7% (Q4_K_M) cliff on
  a 0.6B decision model is STEEPER at Q4_K_M than the 27B published shape (where Q4_K_M ~ 0
  delta), consistent with small models having less redundancy - but note Quesma tests 27B, and
  no in-window published sub-1B WEIGHT-quant task-graded ladder was found. That absence is
  itself the finding: the estate's day-6 ladder is publishable-grade evidence if run cleanly.
- IQ quants on the curve: bartowski explains the mechanism - IQ formats exist to be crushable,
  letting the solver fund bumps for sensitive tensors; below ~3 bits dense models tie the old
  heuristic, above ~Q5 differences are noise. The estate's cliff sits right at the Q4 boundary
  where published work says the flat region ends for small models.
- Decision models in llama.cpp (ggml-org HF blog, NEW this sweep): the model class the estate's
  day-6 cliff was measured on now has first-class llama.cpp support - /v1/systemone endpoint,
  Julia-1 144M / Laya 421M / Kev-4B / lev 4B / OpenJev 27B / Clef 27B, GGUF quants shipped
  ("llama serve -hf ggml-org/Kev-4B-GGUF:Q8_0"), median answer 3-43 ms. Julia-1 (144M) and
  Laya (421M) bracket our 0.6B decision model: the ladder A/B can run on the actual class.

### RQ4. KV compression frontier under local long-context serving

- Held + corroborated this sitting: zartbot's DeepSeek-v4.1-Flash writeup (131 pts) - 890
  B/token via cross-layer KV sharing (only 4 full-KV source layers [2,8,14,20]), 2:1 encoder
  position merge, FP4 E2M1 with E4M3 per-16-channel scales; and the protected-spine-on-the-KV-
  side detail: "the KV cache of sliding window attention SWA is sensitive to quantization, FP8
  precision is retained". Estate already holds this content (memory/runs/gapwave/kvmem_digest.md:66
  carries the 890 B/token fact; context_economics_1m.md:21 cites the zartbot analysis).
- Held: arXiv 2609.04098 (3 catalog rows) - FP8 KV on Qwen3.8-27B "essentially free on tasks",
  ship calibrated per-layer scales, ~1.8-1.9x KV capacity; the Quesma thread independently
  surfaced it (skolos). NVFP4 weights+KV anecdotes in the same thread (RTX 5090, 264k cache).
- BreadthKV-style buy-count-before-fidelity (arXiv 2610.05685) and BARQ (2610.04490) are banked
  per the ask; in-window HN adds no new retained-token-count-optimizing method beyond what the
  estate holds - the LRU-vs-KV-papers thread (108 pts, 58 comments, gauravapiscean/agentic-kv-cache)
  argues simple LRU eviction stays competitive for agentic KV, worth a follow-up read (OWED).

### RQ5. Quantization on CPU/Vulkan (not CUDA), 2B-9B class

- Held + corroborated: grigio Panther Lake benchmark (memory/runs/gapwave/hn_x_fanout/
  local_serving.md:50-51, marked NEITHER/Intel-only) - Vulkan beats SYCL by ~3% pp / ~7% tg,
  6.1x pp and 1.7x tg over CPU on a 35B MoE Q4_K_M; OpenVINO fails on hybrid MoE/Mamba2/MTP;
  f16 KV would OOM so q4_0 KV + flash-attn was used. The estate's 12x Vulkan-vs-CPU decode
  claim (72.97 vs 6.0 t/s, lens/burns.md:135-136) is the same direction; published tg ratios
  run smaller than pp ratios, so our 12x decode figure stays tier-2-unconfirmed as filed.
- Quesma thread, civvv (AMD RX 9070 XT): ROCm build "kept crashing with 0xC0000005", the
  Windows Vulkan llama.cpp build "worked reliably" at Q3_K_XL, 64k context, ~32 t/s - Vulkan
  as the reliability answer on consumer AMD, matching the estate's serving reality.
- AMD Quark (NEW): local on-device BF16->W4A16 quantization of a 35B MoE on Strix Halo
  (128GB unified), exporting GS32 GGUF for llama.cpp - a non-CUDA quant toolchain end to end
  (~70GB -> ~21GB, quant 0.8-1.5 min, export ~22 min, 95GB peak GTT).
- Honest gap: NO in-window published study measures quant FORMATS against each other on
  CPU/Vulkan backends specifically for 2B-9B. Backend-vs-backend is published (Vulkan/SYCL/
  OpenVINO/CPU); quant-vs-quant is published on CUDA; the intersection is empty in this window.
  The estate's own A/B on its Vulkan box would be net-new public-grade evidence.

## Banked items (all fetched and read this sitting; overlap greps run against
catalog/catalog.jsonl (581,477 rows) and memory/)

1. Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses -
   https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/ (HN 49611128, 286 pts)
   Quote: "quantization damage is nonlinear: first there is no measurable change, then a small
   decline, and finally a collapse"
   Overlap: catalog 0; exists only as unconfirmed percolator candidate row
   (memory/percolator/candidates.jsonl, canonical 14053729808aeaa3). This bank adds the full
   task-graded deltas + thread analysis.

2. HN thread 49611128 on the above - https://news.ycombinator.com/item?id=49611128
   Quote (skolos): "There was a study specifically related to Qwen3.8 27B that showed that kv
   cache quantization has almost no impact"
   Overlap: catalog 0, memory 0. Thread carries: imatrix/UD caveat on Q4_K_M comparisons,
   NVFP4 weights+KV field reports, GSQ-RCO and Bonsai-1bit pointers, AMD-Vulkan reliability
   anecdote, KLD-vs-task methodology debate.

3. Per-tensor layout maps for GGUF quantization (bartowski) -
   https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization
   Quote: "Per bit, small attention projections are the most sensitive."
   Overlap: catalog has only an unrelated bartowski-ministral-2410 model card; this method post
   is new. THE open protected-spine implementation for the llama.cpp side of the estate.

4. Quantized Reasoning Models Think They Need to Think Longer, but They Do Not -
   https://arxiv.org/abs/2606.00206 (HN 49869861)
   Quote: "in up to 52% of the quantized models' failures, models reach the right answer in
   intermediate reasoning steps but do not output it"
   Overlap: catalog 0, memory 0. Directly upgrades the estate's quant A/B protocol: grade
   reasoning-length inflation alongside task score; logit-penalty fix is training-free.

5. Local Quantization and Multi-Backend Deployment with AMD Quark on Strix Halo -
   https://rocm.blogs.amd.com/artificial-intelligence/quark-strix-halo/README.html (HN 49975499)
   Quote: "The results do not indicate a single quantization configuration that is uniformly
   best across all tasks."
   Overlap: "Strix Halo"/"amd quark" => catalog 0, memory 0. On-device non-CUDA quant toolchain
   with a task-graded W4A16 table exportable to GGUF.

6. New in Llama.cpp: Decision Models (ggml-org) -
   https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp (HN 49934323/49942092)
   Quote: "A model that answers by scoring the options you give it, instead of generating text."
   Overlap: catalog's only ggml-org row is a llama.cpp CONTRIBUTING blob; memory 0 for this
   post. Feeds the estate's pending decision-model confirmation (DIGEST.md:71-81): named
   endpoint /v1/systemone, 144M-27B lineup with Q8_0 GGUFs, 3-43 ms answers.

## OWED / not done (never asserted as done)

- Janus (Vulkan GGUF runner, HN 49926773, 106 pts): HN thread fetch timed out twice via
  WebFetch and returned only a truncated table via the fallback door - NOT banked, NOT read.
- The LRU-vs-KV-papers thread (49643543) and Fathom (arXiv 2609.17652) were candidate-level
  only, not deep-read this sweep.
- No sub-1B weight-quant task-graded ladder and no quant-format-vs-quant-format CPU/Vulkan
  study found in the 30-day window (stated as absence, not as nonexistence).

Corroborated-but-held (no re-banking): GSQ-RCO (20260928 sweep :61), zartbot DSv4.1-Flash
(kvmem_digest.md:66, context_economics_1m.md:21; catalog V4.1-Flash x22), arXiv 2609.04098
(catalog x3), BITCOS/2609.16338 (catalog x6), VeriLoop ladder (catalog veriloop_iq1m_ladder.html),
BreadthKV (catalog x1), BARQ (banked per ask), grigio Panther Lake (local_serving.md:50-51).
