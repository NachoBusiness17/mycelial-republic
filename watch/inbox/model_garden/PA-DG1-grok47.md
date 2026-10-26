# PA-DG1-grok47 (grok-4.7 @ xai, turn 1, channel: content)

(1) THE DOOR

Kill first. A mated parent exported as a full expert is a learned-gate ensemble, not an MoE. DeepGEMM's win is a grouped GEMM over small expert tiles: one launch, tokens packed per expert, persistent threadblocks pulling `(expert, tile)` items (DG1/00, `deepgemm-mechanics`). That math assumes experts are FFN slices, not 2B-7B transformers. Routing one full parent per token pays one full forward plus a router. Active FLOPs match the best parent. Weights scale as N. On a 6GB box, two 7B Q4 checkpoints already miss (~4GB each plus KV; DG1/00, `fp4-fp8-precision`). You bought memory and a dispatch, not sparsity.

The same note is already in the evidence: if each parent is a full expert, grouped GEMM does not help, and no named population-fusion paper emits MoE (DG1/00, `moe-mating-connection`). Sparse upcycling (Komatsuzaki 2022) is the inverse: duplicate a dense FFN into expert slots, then train a router. Mating dense checkpoints does not create that graph. RDNA1 (gfx1010) has no MFMA and no WMMA, so DeepGEMM's FP8/`wgmma` path does not port (DG1/00, `amd-vulkan-equivalents`). DeepGEMM is not a candidate runtime on this box even if the export existed.

It is a real mechanism only if the exported object is sparse in activated weights, not merely gated. Condition: one shared trunk, experts that are small (FFN-only copies or low-rank deltas), top-1 (or top-2 of tiny experts), router over skills or over hidden state, active params ≈ trunk + one small expert. It beats a soup when parents interfere in weight space (task arithmetic sign conflicts) and beats an ensemble when you refuse N forwards. Per-token routing of full parents never meets that condition. Per-capability routing of full parents can win quality and still lose the MoE claim: that is model selection.

Uncertainty: I have not read Komatsuzaki or arXiv:2508.16204 here. The "no paper exports mating as MoE" line is the sherpa's claim, not a citation I verified. I am confident about the FLOPs identity (full expert ≡ one parent forward). I am less sure a cheap skill router cannot beat a soup on disagreeing specialists; that is what part 3 measures.

(2) THE DESIGN

Do not ship full parents as experts. Minimal format for a 2B-7B fusion pipeline, only if part 3 feeds it:

- Trunk: one architecture, one weight tensor. Pick the mate closest to the population mean, or the literal average of layers that agree (attention, embeddings, norms). Everything else is a delta.
- Experts: per parent, only the layers that disagree. Default: FFN `w1/w2/w3` (or `gate/up/down`) stored once per parent. If those still blow 6GB, store rank-16 or rank-32 deltas on those FFNs, not full matrices. Attention stays shared. No second copy of embeddings.
- Router: one linear map from trunk hidden size to E (E = 2..8), plus a per-layer top-1 index. Optional skill prior: a 1-hot or embedding of task id added to the router logit. Not a second model. Not token-wise top-k over full parents.
- Sharing rule: any tensor whose pairwise cosine across parents exceeds ~0.95 is trunk-only. Record that mask in the file so the pipeline does not re-decide at load.
- File: one GGUF (or safetensors) with Mixtral-style expert FFN tensors plus `router.weight`, expert count, and the shared-layer mask. Quantize trunk and experts the same way (Q4_K_M or Q5_K_M). No FP8, no FP4 tensor-core layout. RDNA1 cannot use them (DG1/00, `amd-vulkan-equivalents`, `fp4-fp8-precision`).

Runtime: llama.cpp, dense-or-MoE GGUF, Vulkan or CPU. It already runs small MoE graphs as ordinary expert FFNs; it does not need DeepGEMM's persistent grouped scheduler. vLLM is the wrong box (ROCm, 6GB, RDNA1). DeepGEMM is CUDA NVRTC + Hopper/Blackwell MMA (DG1/00, `deepgemm-mechanics`). Dead here.

If experts cannot be made smaller than the trunk, stop. There is no export to design. Serve the best parent, or a soup, as one GGUF.

(3) THE FALSIFIER

One sitting, CPU or 6GB AMD, no new kernels. Two or three same-shape local models that fit one-at-a-time at Q4 (2B-class if 7B pair does not fit). Fifty prompts, tagged code / chat / math, twenty of them held out.

Four arms, same activated budget (one forward each):

- A: best single parent on the train tags.
- B: one TIES or mean soup, one forward.
- C: skill router with no training. Map tag to the parent that won that tag on 30 prompts. One forward. This is the ensemble-in-disguise ceiling.
- D: MoE-shaped stub. Trunk = mean of attention and embeddings. Experts = each parent's FFN only, top-1 by a frozen linear on the trunk hidden state (init: parent-id probe, or 100 CPU steps on the 30 prompts). One forward. If FFNs do not fit, use rank-32 FFN deltas and call that D2.

Scores: tag accuracy or exact-match on a tiny set, plus a simple preference count. Log peak RSS.

Kill the export if D (or D2) does not beat B by a margin you would ship, or if C accounts for all of D's gain over A. Feed it only if D beats both A and B at equal RSS order and equal forwards. C beating A while D ties B means: route whole models, do not build an MoE file.

Falsifier for this memo: if D beats A and B on that 50-prompt set at one forward and under 6GB, the kill in part 1 is wrong for small-expert export. If D loses, part 2 is not worth implementing.
