# PA-DG1-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## (1) THE DOOR

**Verdict: ensemble in disguise under the naive export. One narrow condition revives it.**

- If each mated parent becomes a full expert, total parameter count = sum of parents.
- No token is skipped; every forward pass loads one full expert.
- This is a learned-gate ensemble, not sparse MoE. The sparsity win is zero.
- Source: evidence/DG1/00__deepgemm_results.jsonl, id "moe-mating-connection", field "out": "If each parent becomes a full expert, you get a mixture of dense models, which is just an ensemble with learned gating, not a sparse MoE."
- Source: same file, same field: "Grouped GEMM helps only if experts are small and routing is sparse; full-size parents defeat the sparsity win."
- No prior art exists. Closest is Sparse Upcycling (Komatsuzaki et al. 2022), which initializes experts from a dense checkpoint by splitting layers, not by mating whole models.
- Source: same file, same field: "MoE-as-merge is not an established named method."

**The condition under which it wins:**

- Experts must be small relative to the full model (adapter-sized or distilled sub-networks).
- Router must dispatch over tasks/capabilities, not tokens, so each request activates exactly one expert.
- The router itself must be cheaper than running all experts (a linear probe on embeddings, not a full transformer layer).
- If these hold, the mechanism is "capability-dispatched adapter ensemble" - still not classical MoE, but it saves compute vs running all parents.

**Steelman kill:**

- If experts are small (LoRA-rank adapters), the mated parents' distinctiveness is already captured in the merged weights. The adapters add negligible variance.
- If experts are large enough to preserve parent identity, you have an ensemble. The door is a dilemma with no gap.

---

## (2) THE DESIGN

**Assumes the door condition holds (small experts, capability routing). If it does not, skip to (3).**

Format:

- Shared backbone: the merged/mated dense model, quantized to Q4_K_M. This is the trunk.
- Experts: per-parent LoRA deltas (rank 8-16), stored as small adapter matrices. Each is ~10-50 MB for a 2B-7B base.
- Router: a linear probe (d_in x num_experts) over the final hidden state of a prompt-classification head, or over the first-layer residual. No learned gating over tokens.
- What shares: the full backbone is shared. Experts are additive deltas applied at designated layers.
- Inference: router picks one expert per request. Apply that LoRA to the shared backbone. One forward pass.

Runtime fit for RDNA1 6GB:

- DeepGEMM: excluded. Requires NVRTC, Hopper wgmma, FP8 tensor cores. RDNA1 has none.
- Source: evidence/DG1/00__deepgemm_results.jsonl, id "amd-vulkan-equivalents", field "out": "On RX 5600 XT (gfx1010, RDNA1) MFMA is absent."
- vLLM: excluded. Requires CUDA with tensor core support for MoE kernels.
- llama.cpp: viable. Supports LoRA hot-swap natively (`--lora` flag, merge at load or apply at runtime). Grouped GEMM is not needed because experts are small deltas, not full matrices.
- Source: evidence/DG1/00__deepgemm_results.jsonl, id "amd-vulkan-equivalents", field "out": llama.cpp Vulkan path exists but "no FP8 path on Vulkan."

Minimal spec:

- 1 shared GGUF Q4_K_M backbone (2B-7B).
- N LoRA adapter files (one per parent contribution), rank 8-16.
- 1 router: a small classifier (even a heuristic keyword matcher for v0).
- Total VRAM: backbone (~2-4 GB at Q4) + one active LoRA (negligible) + KV cache. Fits 6 GB.

---

## (3) THE FALSIFIER

**Experiment: "router beats average" test. One sitting. CPU or 6GB AMD.**

Setup:

- Take two mated 2B models (already produced by your pipeline).
- Quantize both to Q4_K_M via llama.cpp.
- Run 50 prompts covering distinct capability domains (math, code, creative, factual).
- Baseline A: run model 1 on all prompts. Record outputs.
- Baseline B: run model 2 on all prompts. Record outputs.
- Baseline C: average logits of both models per prompt (or use the merged model if you have it). Record outputs.
- Test: build a trivial router (even a manual domain-label lookup). Route each prompt to the "correct" parent. Record outputs.

Kill condition:

- If routed outputs do not beat Baseline C (the merged/averaged model) on a blind eval, the mechanism is dead. The merge already captured the variance; routing adds nothing.

Feed condition:

- If routed outputs beat Baseline C on at least one capability domain without degrading others, the door condition holds and the design in (2) is worth building.

Cost: two llama.cpp inference runs + one eval pass. Under 30 minutes on CPU. No GPU required.

**Falsifier of this deliverable itself:** if a 2025 paper demonstrates population-fusion-to-MoE export with measured sparsity gains over the merged dense baseline, this adjudication is wrong. I name no such paper. UNVERIFIED.
