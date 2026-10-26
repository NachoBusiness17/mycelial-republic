# Sweep: quantization-compression via arxiv (frontier_olm 2026-10-07)

source-fetched: 2026-10-07

- Lane: frontier_olm 2026-10-07, sweep seat (quantization + compression, arxiv door)
- Doors used: export.arxiv.org Atom API, 5 targeted queries, all rendered clean, zero 403s (cs.CL+quantization 40 results; "KV cache"+compression 25; "mixed-precision quantization" cs.LG 25; GGUF/llama.cpp/Vulkan 25; quantization+CPU/on-device/edge cs.CL 25). Plus arxiv.org/abs pages (16 fetched and read this sitting) and arxiv.org/html full text (6 fetched and read end to end). No door degraded; no fallback needed; WebSearch not needed.
- Window: last 30 days = 2026-09-07 through 2026-10-07. Pass 1 considered ~140 feed entries, >=35 in-window shortlisted. Pass 2 deep-read 16 abs pages + 6 full texts.

## The dedup boundary (read this before mining this area again)

This estate has already mined this area HARD on prior days. Before banking anything I grepped every candidate ID and title phrase against watch/inbox/** (all sweeps, steals, DIGESTs, registers) and catalog/catalog.jsonl. Already held, do NOT re-mine:

- 2609.32042 PolAgentBench (8-bit to 2-bit agentic cliff, full text held at frontier_olm_20260928/sweep/_raw/full_2609.32042.txt; its numbers: 11B 0.716 to 0.045, 7B 0.463 to 0.149 between 3 and 2 bits, McNemar p<0.001)
- 2609.26693 serving-stack confounds (mined 10-01: Ollama tools= static flag, per-seed vs pooled 55-point gap)
- 2610.04403 GGUF rare-word audit (mined 10-06: Q4_K_M clean >=1B, sub-2B Q2_K loses 20-67% definitions, perplexity blind to it)
- 2609.35465 Tetra leech-lattice 2.7 bpw (mined 5 different days: +23.6 MMLU over llama.cpp IQ2_XXS at 4B, L40S GPU)
- 2609.33923 RAM spectrally-flat probe (mined 09-30: beats vendor IQ3_M mix at matched bytes, no code)
- 2609.36032 TORQUE (mined in 7 files across 5 days)
- 2609.37988 KV-Kaizen, 2610.03027 TaSQ, 2610.02462 Scaling-Down Laws, 2610.06251 HQQ shared-stopping, 2610.06174 Anosognosia, 2609.36760 QuantMLA, 2609.38169 STEPQuant, 2609.39329 PatchKV, 2609.36322 phase sensitivity, 2609.26333 disaggregated prefill/decode quant, 2609.14864 GGUF-metadata throughput, 2609.30692 LUMO RPi5, 2610.06286 DeferKV, 2610.06479 behavior-preserving eviction: all previously banked.
- Day-6 lens banked (lens/burns.md:112-113 of this run's lens): BreadthKV 2610.05685, BARQ 2610.04490.

What follows is ONLY what is genuinely new: seven items with zero curated hits anywhere in the estate (verified by grep this sitting; five exist only as raw feed-stage abstract fetches under state/arxiv/<date>/, two are absent from the estate entirely).

## Banked items (7, strongest first)

### 1. Quantization Effects on Tool-Failure Recovery Vary Across Prompts and Evaluation Designs
arXiv 2610.07781, https://arxiv.org/abs/2610.07781, submitted 2026-10-06. Yuhe Hu, single author. NeurIPS 2026 Workshop on Small Language Models for Agentic Systems (SLM-Agents), 7 pages. Read end to end (abs + full HTML).
- THE direct published analog of our owed qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B (lens/burns.md:97-98, 218-219): Llama-3.1-8B-Instruct AND Qwen2.5-7B-Instruct served via llama.cpp at GGUF Q8_0 vs Q4_K_M (plus Q3_K_M/Q6_K/Q5_K_M/Q2_K ladder in appendix), 20 deterministic tool-use tasks x 5 prompts, tool-FAILURE-recovery scored.
- Quote: "The 8-bit-4-bit recovery comparison changes direction across prompts and evaluation targets."
- Qwen2.5-7B matched-task 8-bit minus 4-bit across the 5 prompts: +8.3, -3.3, -10.0, -50.0, +35.0 points; only P3 [-65.0,-35.0] and P4 [+20.0,+50.0] CIs exclude zero, favoring OPPOSITE precisions. Screened rates P3: 43.3% (Q8) vs 90.9% (Q4). Strict output parsing flips Llama P4 full-pipeline from +28.3 to -15.0 "while leaving Qwen essentially unchanged."
- Steal for the owed A/B design: matched tasks (per-prompt clean intersections), full-pipeline success for deployment verdicts, test the deployed prompt, state+log the scoring policy, tasks as the unit of uncertainty. A naive single-prompt A/B at 7B can manufacture either verdict.

### 2. Align, Then Correct: Training-Free Two-Stage Low-Rank Compensation for Extremely Quantized Large Language Models
arXiv 2610.08164, https://arxiv.org/abs/2610.08164, submitted 2026-10-06. Song, Lee, Lee, Choi. 17 pages. Read end to end (abs + full HTML).
- Protected-spine-adjacent (RQ2): fixes LQEC-style rank-r adapters beside frozen quantized weights. Stage 1 Fisher-weighted ASYMMETRIC alignment (symmetric calibration makes the target inherently high-rank); stage 2 rank-constrained natural-gradient step absorbing the first-order signal everyone else drops. Closed-form, zero training.
- Quote: "it recovers 51% and 84% of the gap to FP16, versus 31% and 63% for the strongest baseline"
- Numbers (2-bit QuIP#): Qwen3-8B WikiText-2 12.43 -> 10.26 (FP16 9.73); Qwen3-4B 21.11 -> 13.22, beating FP16's 13.64. 3-bit Qwen3-8B WT2 8.54, CSQA 69.11; 4-bit 8.22 / 69.41. Stage 2 uses only 8K calibration tokens. Overhead: rank-64 adapter per linear, 264-349 MB per set on 8B. No code release.

### 3. AlignQuant: Tile-Aligned Mixed-Precision Quantization for Efficient LLM Generation
arXiv 2610.07457, https://arxiv.org/abs/2610.07457, submitted 2026-10-05. Zhang et al. (UHD/UMD-line). Abs read. Open code: github.com/HanzhiZhang-Ulrica/AlignQuant.
- RQ2 best-practice shape: precision allocated per 2D weight TILE (the GPU storage/compute unit), not per channel or per layer; phase-normalized sensitivity (prefill vs decode scored jointly, loss-gradient weighted); one stored representation per tile, phase-specialized kernels expand low-bit to INT8 for compute.
- Quote: "local precision choices can conflict with regular GPU storage and computation units"
- Four LLMs 3B-14B, up to 2.50x generation speedup over BF16, contexts to 64K, three GPUs. The estate tie: RIB_GPU_LADDER's FP8/MoE gate waits on real demand; this is the per-tile allocation grammar that hardware-native low-bit serving wants. Caveat: GPU kernels (not CPU/Vulkan).

### 4. Monte Carlo Estimation for KV Cache Eviction (LORE-KV)
arXiv 2610.07643, https://arxiv.org/abs/2610.07643, submitted 2026-10-06. Bilal et al. Abs read.
- RQ4, the retained-token axis BreadthKV cares about: asks "which memory will matter while answering?" not "which mattered while reading?" Training-free: samples short autoregressive continuations from the frozen model, scores prompt tokens by projected leave-one-out attention-output deletion cost across sampled futures.
- Quote: "a single response-side continuation recovers about 89% of the gain over the prompt-window control"
- At budget B=128: LongBench avg Qwen2.5-14B 45.49 -> 48.24; 16K RULER Mistral-7B 45.20 -> 51.05. Cost: 1.46-2.77x another method's per-sample wall-clock as one-time compression overhead. Gains shrink at larger budgets; task-level regressions coexist.

### 5. Mask-Guided KV Cache Eviction in Block Diffusion Language Models (MaskAhead / Q-MaskAhead)
arXiv 2610.06996, https://arxiv.org/abs/2610.06996, submitted 2026-10-04. Molodtsov, Beznosikov et al. Abs read.
- RQ4: training-free selection AND eviction from one mask-query ranking; the quantized variant Q-MaskAhead computes selection and attention "directly from low-bit KV."
- Quote: "probes of upcoming masked blocks guide eviction"
- Long-prompt QA: 9.5x KV memory cut at 1.2-point mean F1 drop; Q-MaskAhead 20.1x at 2.3-point drop. Batch-32 profile: 1.23x end-to-end, 1.68x decode. Block-diffusion LMs only (Fast-dLLM-v2, DreamReasoner, LLaDA2.0-mini).

### 6. Lost in the bf16 Cast: Exporting Ternary Language Models Can Revert Most Low-Learning-Rate Code Changes
arXiv 2610.07853, https://arxiv.org/abs/2610.07853, submitted 2026-10-06. Sahai, Raj, Srivastava. 14 pages. Abs read.
- Integrity rider for ANY quant-ladder measurement (RQ3 methodology): the export path itself can silently destroy a model. Shipped ternary checkpoints' fp32 latents disagree with deployed codes on 0.83-1.77% of codes; bf16 rounding lands exactly on quantization thresholds where "ties-to-even maps to zero"; documented export drops GSM8K greedy strict 58.79% -> 0.78% (Falcon-E-1B-Base) and 36.13% -> 0.39% (BitCPM-0.5B); a bf16 save/reload cuts BitNet 2B-4T by 27.54 points.
- Estate tie: the dead-instrument warning class (lens/burns.md:113 benchmark_bridge fallback always True). Verdict for us: when the day-6 0.6B ladder (bf16 0.757 / Q8_0 0.750 / Q4_K_M 0.703) or the owed 7B A/B runs, hash the exact artifact and pin the conversion toolchain, or the ladder measures the exporter, not the quant.

### 7. SoloQ: Calibration-Free Quantization for Diffusion Language Models
arXiv 2610.07121, https://arxiv.org/abs/2610.07121, submitted 2026-10-05. Lee et al. (Panda lab). Abs read.
- RQ4 adjacent: calibration-free W/A quant for diffusion LMs (rotated normalized basis, distribution-matched codebooks or hardware-native NVFP4); commit-time KV-cache quantization compresses persistent block states "without perturbing the actively denoised block."
- Peak memory up to 2.61x lower, end-to-end up to 2.24x faster, accuracy retained at 4-bit, beats calibration-based baselines on knowledge/reasoning. Relevant only if the estate ever serves a dLLM; banked as the KV-quant frontier datum for the diffusion family.

## Answers to the research questions

RQ1 (7B task-graded Q4_K_M vs Q8_0 deltas): there is NO stable published single number, and 2610.07781 is the proof: at 7-8B on tool-failure recovery the sign itself flips with prompt, task screening, scoring policy, and executor parsing (-50.0 to +35.0 on matched tasks for Qwen2.5-7B). Combined with pre-held ACBench (4-bit costs 1-3% protocol shape but 10-15% end-to-end app accuracy) and PolAgentBench (cliff between 3 and 2 bits, task-graded), the literature's message to the owed A/B is: multi-prompt, matched-task, full-pipeline, parsing policy pinned, per-task uncertainty. Typical DEFENSIBLE 4-bit-vs-8-bit cost at 7B on agentic work: single digits to low tens of points, design-dependent, not a constant.

RQ2 (protected-spine / mixed precision best practice): the late-2026 grammar is budget-targeted allocation at ever finer granularity with the execution unit respected: per-tile (AlignQuant, open code), per-coordinate pre/post rotation (TORQUE, held), data-free probe knapsack (RAM, held; models on HF, no code), closed-form adapter compensation (Align-Then-Correct, no code), trellis codebooks (Tetra, held, open code). VeriLoop's protected-spine IQ1_M-beats-uniform-IQ2_S sits squarely in this consensus: protection budgets beat uniform at extreme bits. Open implementations that ship: AlignQuant and Tetra (GitHub); RAM ships pre-quantized HF artifacts only; Align-Then-Correct ships none.

RQ3 (sub-1B ladder cliff + IQ placement): the estate's day-6 cliff (0.757 -> 0.750 -> 0.703) matches published shape: sub-1B/sub-2B GGUF artifacts lose 8-19% at Q4 variants and 20-67% at Q2_K on rare-word definitions (2610.04403, held) while >=1B Q4_K_M stays clean; agentic cliffs land between 3 and 2 bits at 7-11B (PolAgentBench, held). IQ quants: Tetra (held) puts llama.cpp IQ2_XXS 23.6 MMLU points below a 2.7-bpw trellis codebook at 4B, i.e., IQ-style codebooks at ~2.5 bits are NOT the quality frontier at small scale; quality at extreme compression now lives in lattice/trellis codebooks plus per-row retraining, with IQ as the speed king (312.9 tok/s in llama.cpp). New rider: 2610.07853 shows ladder measurements can be corrupted by the export cast itself.

RQ4 (KV frontier + retained-token optimizers): the window's KV quant frontier runs to 1-bit VQ with reshaped target spaces (TaSQ, held), function-aligned dual-path MLA INT4/INT2 (QuantMLA, held), learned per-layer depth/precision/rank selectors (KV-Kaizen, 32x cache on 14B, held), and commit-time quantization for dLLMs (SoloQ, new). Methods that optimize what token count buys, BreadthKV-style: LORE-KV (new) improves the eviction SIDE by estimating future utility from sampled continuations; MaskAhead (new) pushes eviction+low-bit KV to 20.1x on dLLMs. BreadthKV's explicit precision-for-count trade remains the framing paper; nothing new in-window supersedes it, the field is adding better utility estimators instead.

RQ5 (CPU/Vulkan-backend quant, 2B-9B): HONEST GAP. Nothing in this window measures quantization quality or throughput on a Vulkan backend specifically. New items are CUDA (AlignQuant 3 GPUs; Tetra one L40S). The estate-held CPU/llama.cpp-side items are all prior mining: GGUF-metadata throughput prediction across three systems (2609.14864), disaggregated prefill/decode quant with llama.cpp offloading 1.78x TTFT at 8K (2609.26333), LUMO RPi5 4-bit GGUF (2609.30692). OWED, not found: a Vulkan-vs-CPU quant backend bench for 2B-9B. Our own 72.97 tok/s Vulkan vs 6.0 CPU (12x, tier-2 unconfirmed, lens/burns.md:135-136) remains estate-measured, not literature-corroborated.

## Near hits, not banked (feed gist level or out of scope)
- 2610.07767 TRACE: FP4 quantization-aware RL for MoE rollouts, 5.4x rollout speedup. Training-side; estate is inference-side. Unmined if a later lane wants it.
- 2610.05977 StagQ, 2610.06026 differentiable bit-widths, 2610.00983 reconstruction-loss-scale: pre-mined or register-held.
- 2609.05881 Broken on Arrival (quantcheck, silently defective registry artifacts): dated 2026-09-05, 2 days outside window, and prior lanes touched registry-integrity ground; noted for the artifact-hashing law in item 6.

## Honesty block
- Read depth: items 1 and 2 read end to end (abs + arxiv.org/html full text). Items 3-7 read at abs-page level only (fetched and read this sitting; numbers above are from the abstract pages; per-section verification like table-level numbers was not done for them).
- Quotes are verbatim fragments as rendered by my fetches of the pages above; quote 5 and 6 and 7 are short fragments because the pages' fetch summaries capped verbatim reproduction.
- Overlap greps ran against catalog/catalog.jsonl and watch/inbox/** and memory/ via ripgrep-style grep this sitting; memory/ full recursive grep was slow and partially backgrounded, so memory-side coverage relied on the catalog (which indexes watch/inbox and state/arxiv) plus targeted greps of memory/lens and memory/rib paths named in the ask. residual risk: an un-indexed memory note mentioning a title informally.
- The Vulkan/CPU gap is stated as a gap, not filled.
- No fallback door was needed; no door 403'd.
