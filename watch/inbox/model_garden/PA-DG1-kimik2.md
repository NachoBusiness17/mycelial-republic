# PA-DG1-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

(1) THE DOOR

The kill: mated-model-as-MoE is ensemble in disguise unless the experts are *substantially smaller than the dense parents* and the router operates over *task-level or capability-level distribution shifts*, not per-token position. Evidence: Komatsuzaki 2022 (Sparse Upcycling) initializes experts from dense checkpoints but requires a frozen backbone plus small FFN experts; full-parent experts collapse to learned-gate ensemble because (a) no sparsity: every forward pass touches all parameters, (b) router capacity approaches uniform averaging under similar parent distributions, (c) grouped GEMM's persistent threadblock win assumes small expert tiles that fit shared memory—full 7B weights per expert explode register pressure and memory bandwidth, negating the dispatch/compute overlap DeepGEMM optimizes for (evidence/DG1/00__deepgemm_results.jsonl: "grouped MMA where each expert's tile range is dispatched by an expert-id lookup"—tile ranges imply small, uniform expert shapes).

Condition for win: experts are *skill-fragmented submodules* (attention heads, FFN slices, or LoRA banks) under *per-capability routing* where the router selects based on task embedding, not token position. This requires parents to decompose into complementary, non-overlapping function regions—rare in practice unless mating is *structured* (e.g., parent A = code heads, parent B = math heads, explicit router training on capability probes).

(2) THE DESIGN

Format: **Skill-MoE JSON** with three fields:

- `backbone`: shared weights (intersection of parents via task-arithmetic merge, TIES or DARE, ~40% of total params)
- `experts`: list of delta-weights (parent minus backbone, quantized to Q4_K_M), each tagged with `capability_probe` (embedding centroid of tasks where parent outperforms backbone)
- `router`: small MLP (2 layers, 512 hidden) mapping task embedding to expert logits, trained on synthetic capability probes post-mate

Runtime: **llama.cpp with custom MoE patch**—not DeepGEMM (RDNA1 lacks MFMA, evidence/DG1/00__deepgemm_results.jsonl: "FP8/FP16 tensor-core tiling does not map") and not vLLM (no grouped GEMM for CPU/RDNA). llama.cpp's `ggml-vulkan` backend supports shader-tiled GEMM with subgroup ops; extend with:

- Pre-load expert deltas into host-pinned buffers (6GB constraint: only 2 experts resident in VRAM, rest paged)
- Router dispatch in CPU graph: select top-2 experts by capability_probe cosine, async upload deltas, run backbone + expert GEMM sequentially (no true grouped launch, but avoids per-token kernel overhead)

Sharing: backbone weights, KV cache, and capability_probe embeddings. Falsifier-named deliverable: `skill_moe_spec_v0.md` with llama.cpp patch against `ggml-vulkan` commit `b3602`.

(3) THE FALSIFIER

Experiment: **Capability-Router Collapse Test**

Setup: Mate two 2B models—Qwen2.5-1.5B-Instruct (code) and DeepSeek-Coder-1.3B-Instruct (math)—via TIES merge for backbone, deltas as Q4_K_M experts. Train 256-dim capability probes on 1K synthetic (code vs. math) prompts. Router MLP: 256 -> 512 -> 2, 10K steps.

Test: HumanEval (code) and GSM8K (math) with three routing modes—(a) oracle (ground-truth task label), (b) learned router, (c) uniform average (ensemble baseline).

Kill condition: (b) does not statistically beat (c) on either benchmark (p > 0.05, paired bootstrap) → router collapses to ensemble, sparsity illusion confirmed.

Feed condition: (b) beats (c) by >3 points on both tasks with <2x latency vs. single expert (CPU, 6GB, measured via `llama-bench`) → mechanism lives, scale to 7B.

Cost: CPU-only, no GPU hours; 6GB RAM sufficient for 2B Q4; runtime <4 hours on 8-core AMD. Artifact: `falsifier_skill_moe.json` with per-mode accuracies and latency samples.
