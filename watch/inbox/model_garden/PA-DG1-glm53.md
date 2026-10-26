# PA-DG1-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

**(1) THE DOOR**

Kill first, steelmanned: mated-parent-as-MoE is an ensemble in disguise whenever the router fires per-token over full-size parents. A 2-parent "MoE" with two 7B experts runs every token through a full 7B (or both at k=2); you pay dense inference plus router overhead and call it sparsity. The evidence says this directly: "If each parent becomes a full expert, you get a mixture of dense models, which is just an ensemble with learned gating, not a sparse MoE" (DG1/00__deepgemm_results.jsonl:4, entry `moe-mating-connection`), and "full-size parents defeat the sparsity win" (same line). Worse: two experts is not a mixture distribution, it is a switch; learned gates on N=2 are a noisy binary classifier, and its errors are unrecoverable because the parents were never trained to specialize. Training-free routing over general-purpose dense chat models is known-weak; the router has no signal.

It lives only if you change what the experts are, not just bolt a gate on. Three conditions, all required:

- **Small experts relative to the model**: fragments (layer slices, pruned/shrunk derivatives, LoRA-stacked deltas) not whole checkpoints. Grouped GEMM only pays when experts are small and routing is sparse (DG1/00__deepgemm_results.jsonl:4).
- **Router over capability, not token position**: route per-request or per-skill-segment (code vs. prose vs. math), decided once per context or per paragraph, not per token. This sidesteps the N=2 token-level gate problem: a per-request gate trained on task labels or even model-routing benchmarks has real signal.
- **Shared backbone, divergent deltas**: the parents must share ancestry (same base architecture, ideally same pretrain run) so deltas are low-rank and commensurable. This is exactly the population-fusion precondition; without it, "shared" is fake and you are back at ensemble.

Under those three it is a real mechanism, not an ensemble: compute is amortized across a shared trunk, experts are deltas not models, and the gate predicts task class (learnable) not token fit (not learnable from 2 parents). Under any one condition missing, it is an ensemble and the door closes.

**(2) THE DESIGN**

Export format, minimal:

- One shared trunk: the averaged/mated dense base (parents are already near-linear-mode-connected; population fusion gives you this for free), stored as a single GGUF.
- Per-parent expert deltas: per-layer low-rank or quantized delta weights, D = parent minus trunk, applied only on routed layers (every nth transformer block; start with MLP blocks only, attention stays shared). Expert = delta stack, not checkpoint.
- Router: a tiny per-request classifier, a 2-6 layer head over the mean-pooled prompt embedding, outputs soft weights over experts at temperature ~1, fixed for the request. Fallback: a heuristic router keyed on task tags. No per-token gate at N=2-4.
- Container: a new GGUF arch variant (e.g. `llama_moe_delta`) reusing existing tensor naming with a `expert.N.delta` suffix and a one-page metadata block (expert count, routing interval, gate path). This is a patch to llama.cpp's loader plus a new convert script; llama.cpp is the only runtime that runs on your box (RDNA1 has no MFMA and no cooperative matrix, so DeepGEMM patterns do not map, DG1/00__deepgemm_results.jsonl:2; Vulkan path is plain tiled GEMM/GEMV shaders, same line).

Runtime verdict: **plain llama.cpp with an MoE-delta loader patch**. DeepGEMM grouped GEMM is irrelevant here: no RDNA1 support, no Vulkan backend, FP8 requires tensor cores absent on gfx1010 (DG1/00__deepgemm_results.jsonl:2). vLLM needs ROCm Far GPU targets and expects true MoE checkpoints, not deltas. Sharing means your "MoE" costs one trunk + one small delta per routed layer, so you do not need grouped GEMM; you need conditional weight application, which is a loader/scheduler concern, not a kernel concern. That is the honest sizing: the mechanism lives or dies at the format layer, not the GEMM layer.

Falsifier of this deliverable: if the router must run per-token to beat a single fused dense model on quality, the design is dead (it collapses to ensemble at dense cost).

**(3) THE FALSIFIER**

One sitting, CPU or 6GB AMD, no new infrastructure:

1. Take two 2B Q4 GGUF parents sharing a base (e.g. two fine-tunes of Qwen2.5-1.5B or Llama-3.2-2B-class).
2. Build the trunk by plain weight averaging of safetensors (CPU, minutes).
3. Extract per-MLP-block deltas, truncate to top-50% magnitude per tensor (this is your sparsity claim in miniature).
4. Serving A/B in llama.cpp, three arms, same prompts (200 items: 100 general chat, 50 code, 50 math):
   - A: fused dense merge (trunk + mean delta), full weights always.
   - B: hand-tagged routing, no learned router: code prompts apply parent-code deltas, math prompts apply parent-math deltas, chat uses bare trunk. This tests the mechanism with the router signal held at its best case, which is the honest kill test.
   - C: parent A alone (control).
5. Score with an LLM judge on 1-5 plus task accuracy on the code/math slices.

**Kill condition**: B does not beat A by a margin the judge reproduces (judge agreement >70% on the A-vs-B delta) on at least one task slice, while using less effective compute. Then expert deltas carry no task-specific signal beyond the merge, and mated-as-MoE is confirmed as an ensemble in disguise. **Feed condition**: B wins a slice. Then the learned per-request router is worth building and the GGUF-delta format spec is the next landable artifact.

Cost: zero API dollars, one evening, existing models.
