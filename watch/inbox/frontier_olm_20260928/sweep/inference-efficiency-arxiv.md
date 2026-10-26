# sweep: inference-efficiency via arXiv (frontier_olm 20260928)

source-fetched: 2026-09-28

Lane: inference-efficiency via arXiv. All items below were fetched and read by this seat this
session (abs pages plus full HTML where arXiv rendered it). Pass 1 considered 109 feed entries
across 7 arXiv API queries (speculative decoding 25, consensus decoding 5, llama.cpp 20,
energy+LLM inference 20, GPU profiling+inference 6, quantization+decode throughput 18,
serving+benchmark+llama 15; 2608.25053 appeared twice, so ~108 unique candidates) from the
last 30 days. Pass 2 deep-read 8 end to end. Overlap grep ran against
`catalog/catalog.jsonl` and `memory/` (memory grep covered all 14 title/phrase probes; the
two generic phrases were cut mid-scan after per-phrase results landed, stopped task
exec_f19a3bd5; per-phrase output captured above the cut).

## Answers to the five questions (summary)

1. Consensus decode: YES, a published design now decodes consensus in the actual task output
   space (2607.23394, token-level next-token distribution aggregation). See item 4.
2. Windows serving stack: no paper benchmarks llama.cpp vs Ollama vs vLLM tok/s ON Windows
   head to head; the closest are a GGUF-metadata throughput model fitted on a Windows RTX
   5080 host (2609.14864, decode ~56-446 tok/s, prefill ~17,800 tok/s) and a serving-stack
   confound study (2609.26693). Replication on our hosts is the move, not import.
3. Windows process attribution: NOTHING on arXiv in the window answers per-lane GPU/RAM/
   process attribution on Windows. Closest is Hydra's phase-attributed telemetry on Jetson
   (Linux). Web-search leads (ETW DxgKrnl provider, uberAgent, CHAOS ETW power models) are
   search-sourced only, not read, NOT banked. Rib Q9 (lens laws.md:76) stays open; OWED.
4. Cool/heat map: two driverless instruments banked: NVML cumulative energy counter
   (nvmlDeviceGetTotalEnergyConsumption, mJ, userspace, ships with the NVIDIA driver,
   2608.28044) and ADB current/voltage sampling P=I*V on Android (2609.01798). Neither needs
   an extra kernel driver. Both decompose energy by phase and work type, which is the seed
   of a per-lane cool/heat map.
5. Kernel/quant wins vs dispatch shape: in-window wins (DQ: llama.cpp TTFT 1.78x at 8K ctx,
   decode LUT2 3.82-4.15x vs BF16 on Qwen3 0.6B-8B; FlashAttention-2 cutting token energy up
   to 51.9%) change LOCAL janitor-lane economics only. Nothing in the window touches the
   account-side rolling throughput cap that binds the measured 109.4M tok/h fan-out envelope
   (AGENTS.md fan-out law). Dispatch shape stays the binding constraint for fan-out; quant
   wins matter for the ollama lanes.

## The 8 banked items (strongest first)

### 1. Measuring the Serving Stack Instead of the Model: Hidden Confounds in Local Tool-Use Evaluation
- arXiv 2609.26693, 2026-09-22, REALM @ EMNLP 2026. https://arxiv.org/abs/2609.26693 (full HTML read)
- The estate hazard: Ollama v0.30.8 rejects `tools=` requests with HTTP 400 "does not support
  tools" for Phi-3-mini, Gemma-3-4B, Gemma-3-270m; the models NEVER RUN, yet naive analysis
  reports 0% tool fidelity. Our janitor fleet is gemma:2b / gemma4 on Ollama: any tool-calling
  ask routed through Ollama's default surface can be a pre-inference rejection, not a model
  failure. llama.cpp llama-server with --jinja serves the SAME GGUF weights fine (HTTP 200).
- vLLM needs --enable-auto-tool-choice + --tool-call-parser or it 400s; SGLang accepts but
  returns the call as text without --tool-call-parser. Constrained decoding caused 600-900
  turn non-termination loops (Qwen-0.5B hit 869 turns). Pooled vs per-seed fidelity gaps up
  to ~55 points. Checklist: pin stack version, log transport/serving failures as distinct
  outcomes never as model non-calls, report per-seed rates with intervals.
- Quote: "The same GGUF weights that Ollama rejects with HTTP 400 run when served by llama.cpp"
- Overlap: already in catalog (abstract .txt, zone lsa, age 3 days) and
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json. This deep read adds the per-stack
  rejection matrix, fidelity numbers, and the checklist beyond the abstract.

### 2. GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems
- arXiv 2609.14864, 2026-09-14, to ICASSP 2027. https://arxiv.org/abs/2609.14864 (full HTML read)
- One host IS Windows: NVIDIA RTX 5080, Windows-AMD64, CUDA (the other two are M4 Max,
  Darwin-arm64, Metal). 23 GGUF files, low-bit ladders incl Qwen3.8-27B (IQ2_XXS..Q6_K),
  SmolLM3-3B, Qwen3.5-4B/9B, gpt-oss-20b/120b, MoE rows. Decode on the RTX 5080 ~56-446
  tok/s, prefill ~17,800 tok/s.
- Roofline-shaped predictor reads ONLY GGUF metadata (file size, tensor shapes, active
  parameter counts with expert k/E fields, KV head dims, sliding window, recurrent-state
  fields): decode MAPE 13.1% / 14.4% / 36.1% per host held-out, 11.6% / 16.8% / 36.0%
  leave-one-host-out. Active-weight accounting cuts naive errors from ~50% to those numbers.
  Fitted efficiency factors are host-specific and do NOT transfer verbatim.
- Steal: fit eta(h,q) on our own hosts from a handful of runs, then predict any new GGUF's
  janitor tok/s before loading it.
- Quote: "GGUF structure helps on all three systems, but fitted efficiencies are not universal."
- Overlap: NOT in catalog, NOT in ARXIV_REGISTER; memory/ hits were only
  memory/trajectory/steps.jsonl (directory-listing artifact per the ladder-02 audit). New.

### 3. Characterization of Request and Token Energy Costs for LLM Inference Workloads on GPU Platforms
- arXiv 2608.28044, 2026-08-28, IISWC 2026, CMU ECE. https://arxiv.org/abs/2608.28044 (full HTML read)
- The driverless-tool answer for the cool/heat question: energy from the NVML cumulative
  counter `nvmlDeviceGetTotalEnergyConsumption` (mJ), differenced across inference windows;
  `nvmlDeviceGetPowerUsage` at ~50 ms only as a smoothed diagnostic. NVML is a userspace API
  shipped with the stock NVIDIA driver: no extra kernel driver. Per-kernel attribution via
  isolated replay (TaxBreak-style, 500 ms windows, <=5% variation gate).
- Decomposition E_request = E_fixed + N * E_step with E_fixed = E_prefill + E_decode,fixed.
  Numbers: Llama-3.2-1B on H200 (B=16, C=4K): token energy falls 7.46 -> 0.72 J/token as N
  goes 10 -> 512 while total window energy RISES 1.19 -> 5.93 kJ. Floor share median 51.6%,
  up to 79.1% at low load. B=4 captures ~80% of the B=16 batching energy gain. H200 = 0.61-0.84x
  H100 token energy for dense models. FlashAttention-2 cuts token energy up to 51.9%.
- Steal: the fixed-vs-step split IS a cool/heat coordinate: fixed floor cost per lane request
  vs marginal per-token heat. Instruments: H100/H200 only; consumer-GPU transfer unverified.
- Quote: "energy-aware serving should jointly optimize both request energy and token energy,
  rather than only reducing per-token energy cost."
- Overlap: NOT in catalog, NOT in register. New.

### 4. Inference-Time Consensus for Mitigating Hidden Behaviors from LLM Fine-Tuning
- arXiv 2607.23394, 2026-07-25 (12 days older than the 30-day preference window; it is the
  direct hit on rib Q1 so banked with the date stated). https://arxiv.org/abs/2607.23394 (full HTML read)
- Rib Q1 (lens laws.md:68) asks for a consensus decode that maps to the ACTUAL task output
  space (numbers/text), not a surrogate; the flock failed 3/3 at strength 0.60-0.67
  (RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:14-25). This paper IS that mapping:
  one rank-8 LoRA reference per source on Qwen3-8B / Qwen2.5-7B, then decode-time next-token
  distribution aggregation with four variants: token-wise minimum pi_min (any source can veto
  a token), base-relative pi_delta (agree-rise keeps smallest lift, disagree reverts to base),
  quorum Phi_q, and semantic smoothing over short rollouts. Results: prefix-poisoning
  suppression with 0/128 cost leakage while keeping 117-121/128 joke benefits; smoothed
  minimum 109/128 markers with 1/128 prefixes.
- Costs and limits, stated by the authors: one forward pass PER reference model PER token
  (semantic-smoothing pilot: 33 h 16 min on two A100 80GB); "consensus measures support, not
  correctness"; one actor posing as multiple sources can manufacture agreement. So the design
  exists but is expensive and does not by itself make consensus correct; our quality-of-
  consensus-vs-strong-remote measurement (RIB_MINDSWEAVE_EVAL.md:34-43) remains ours to run.
- Quote: "we fine-tune a separate reference model on each source's dataset and aggregate their
  next-token distributions at decoding time."
- Overlap: NOT in catalog, NOT in register; memory/ hit only steps.jsonl artifact. New. Note:
  BlockBatch (2605.29233, multi-scale consensus decoding for diffusion LMs, 1.33x over
  Fast-dllm) is the efficiency-flavored cousin, seen in feed only, not deep-read, not banked.

### 5. Disaggregated Quantization: Specializing LLM Prefill and Decode
- arXiv 2609.26333, 2026-09-22, NVIDIA & ISTA. https://arxiv.org/abs/2609.26333 (full HTML read)
- The biggest in-window kernel/quant win for our size class: prefill is compute-bound (wants
  NVFP4), decode is memory-bound (wants 2-3 bit LUT weight-only); specialize per phase via
  QADD distillation. In a custom llama.cpp fork, offloaded disaggregated prefill gives TTFT
  1.78x over weight-only IQ1_S at 8K ctx (12.27 s -> 6.90 s); on vLLM batch-1 decode, LUT2 is
  3.82x / 4.15x BF16 on Qwen3 0.6B-8B / Gemma3 1B-12B. 1-bit prefiller on Qwen3.8-27B buys
  +32.5 MMLU-Pro (29.04 -> 61.54) without touching the decode checkpoint.
- Caveats: custom forks (llama.cpp fork + vLLM/NIXL), measured on DGX Spark GB10, not stock
  Windows builds; adoption cost is real. This is the item that changes LOCAL tok/s economics;
  it does not touch the account-side fan-out cap.
- Quote: "We propose 'disaggregated quantization' (DQ), which specializes computation formats,
  weights and storage placement to both of these phases."
- Overlap: catalog.jsonl already holds the abstract; NOT in ARXIV_REGISTER. Deep read adds
  the TTFT/decode numbers and the fork caveat.

### 6. How Do Prompt Variations Affect Energy Consumption in On-Device LLMs?
- arXiv 2609.01798, 2026-09-01, EMNLP 2026. https://arxiv.org/abs/2609.01798 (full HTML read)
- Driverless energy instrument #2: ADB current/voltage sampling, P(t)=I(t)*V(t), integrated
  over prefill/decode windows (MLC-LLM + LM-Meter), Pixel 8 Pro / Pixel 7. Models: Gemma-2-2B,
  Llama-3.2-1B, Qwen-2.5-0.5B/1.5B, SmolLM2-360M.
- The cool/heat seed: prompt cognitive load (heat of the WORK) moves per-token energy
  (extraneous load 1.29x decode energy on Qwen-2.5-1.5B; prefill 3-6x decode per token on
  most models, Gemma-2-2B inverted) while phrasing moves token COUNTS (~1.0x per token).
  No per-process attribution; device-level only, so it maps work type to energy, not lane
  to energy.
- Quote: "We find that cognitive load primarily affects the energy cost per token, while
  phrasing pattern affects energy largely through token usage."
- Overlap: NOT in catalog, NOT in register. New.

### 7. Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels
- arXiv 2608.25053, 2026-08-25, IISWC 2026. https://arxiv.org/abs/2608.25053 (full HTML read)
- 107,110 per-prompt records, 286 CSVs, phase-attributed telemetry (349-419 columns), open on
  Zenodo (DOI 10.5281/zenodo.21844843) and github.com/amirtaherin/hydra. Three Jetson
  generations (Xavier/Orin/Thor), HF vs llama.cpp backends, GGUF Q8_0/Q6_K/Q4_K_M, 13 LLMs
  1.24-8.54B. Instruments: tegrastats + NVML (userspace), CUDA sync barriers.
- Findings that transfer: backend structure changes WHERE latency lives (HF ITL 63.5 ms vs
  33.0 ms raw generation on Thor, CPU orchestration; llama.cpp ITL nearly matches generation);
  power is non-monotonic under quantization (Q6_K often draws MORE watts than Q8_0 or Q4_K_M);
  Thor draws more watts but fewer joules per token than Orin.
- Not Windows (Jetson/Linux), so rib Q9 Windows process attribution stays open; the record
  schema (phase-attributed telemetry columns per prompt) is the stealable part.
- Quote: "aggregate latency alone hides key deployment effects: backend structure changes
  where latency is introduced"
- Overlap: NOT in catalog, NOT in register. New.

### 8. Tetra: Serving Leech-Lattice Quantized LLMs at 2.7 Bits per Parameter
- arXiv 2609.35465, 2026-09-28. https://arxiv.org/abs/2609.35465 (full HTML read)
- The instructive NEGATIVE for Q5: a 2.148 bits/weight trellis decode kernel (six table loads,
  two small lookups per 48-bit block) and 2.70-2.73 bpw Qwen3-4B/8B/14B models, yet decode is
  SLOWER than 4-bit AWQ on the same L40S (Qwen3-8B: 95.0 vs 123.2 tok/s; FP16 46.3) and MMLU
  sits 4.21 points under AWQ at 8B. The win is the memory frontier, not speed: their 8B at
  ~2.7 bpw beats AWQ-4B by +1.44 MMLU at similar memory. Not in llama.cpp; custom CUDA engine
  (github.com/pjmalandrino/llvq, MIT/Apache-2.0); QTIP benchmark kernel is GPLv3, not
  redistributed.
- Sub-3-bit does not beat 4-bit on commodity-CUDA decode speed. For our lanes: 4-bit AWQ-class
  quants remain the local tok/s sweet spot; fancy sub-3-bit buys memory, not throughput.
- Quote: "The kernel decodes a block with six table loads and two small lookups inside the
  matrix-vector product, and reads 2.148 bits per weight."
- Overlap: catalog.jsonl already holds the abstract; NOT in register. Deep read adds the
  honest slower-than-AWQ numbers.

## Not banked but noted (seen, not read)

- Speculative decoding for small models is an ACTIVE 30-day front (25 fresh entries):
  self-speculation for looped transformers (2609.34538, 4.0-6.96x; 2609.23033 WaveFront, 4.81x
  on Huginn-3.5B), acceptance-aware draft training (2609.24150), SpecQuant INT4/FP8/FP16
  multi-parent routing (2609.21704, 35-43%), PELM DVFS+speculation on mobile (2609.09662,
  52.4% energy savings). None targets the consensus-shape question; most need training or
  multi-model memory budgets beyond the janitor lanes. Feed-level only; not deep-read.
- Web-search leads for Windows attribution (search-sourced ONLY, primaries not fetched,
  therefore NOT banked and NOT asserted): ETW Microsoft-Windows-DxgKrnl GPU events for
  per-process GPU time; uberAgent 7.3 per-process GPU KPIs without kernel drivers; CHAOS
  ETW-logged per-process power models. If the estate wants rib Q9 closed driverless, the ETW
  route is the lead; OWED: no primary source read.
- Door health: all 7 arXiv API queries and 9 article fetches returned normally; one degraded
  surface: WebSearch ran through the Z.ai hosted search and returned processed summaries with
  partial links; treated as leads only. 1302-style rate walls did not fire this session.

## Estate connections

- Feeds lens estate map: ollama janitor lanes (items 1, 2, 5), GPU-adjacent corpus shadertoy21k
  (no direct hit in window), burn-wave throughput measurement (item 3's fixed-vs-step split is
  a candidate instrument for per-lane burn cost), Hermes dispatch economics (Q5 verdict:
  dispatch shape stays binding for the 109.4M tok/h envelope; kernel wins are local-only).
- Open-questions impact: Q1 consensus-decode redesign has a published design shape (item 4)
  but correctness measurement stays ours; Q7 cool/heat map gets two driverless instruments
  (items 3, 6) and a work-type-to-energy mapping; Q9 Windows process attribution UNRESOLVED
  on arXiv (leads only).
