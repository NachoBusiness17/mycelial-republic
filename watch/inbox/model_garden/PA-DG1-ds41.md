# PA-DG1-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

## (1) THE DOOR

**Kill first.** `moe-mating-connection` line 6 states it flatly: "If each parent becomes a full expert, you get a mixture of dense models, which is just an ensemble with learned gating, not a sparse MoE." That is correct and it is the default. A 2B parent as a full expert, gated per token, is an ensemble. Sparsity buys nothing: you still load and run every selected expert at full width, and if the router is dense you run all of them. Dead.

**Steelman.** The kill assumes the expert carries the parent's full parameter count. Break that. If parents are *decomposed* into capability slices before mating, each slice is small, the router selects slices not models, and grouped GEMM's persistent-block scheduler (`deepgemm-mechanics`, MoE optimization paragraph) is exactly the right runtime. The condition under which the door is real:

- **Experts are sub-parent.** A 2B parent shatters into 4-16 adapters or FFN blocks of 100-500M each. Not the parent.
- **Router is over capability, not token identity.** Routing on task/skill signature (prompt class, tool availability, language) rather than per-token hidden state. Per-token routing on 2-3 experts is a soft ensemble. Per-capability routing on 8+ slices with top-2 is sparse.
- **Shared backbone is explicit.** Attention and embeddings are shared or merged once. Only FFN/MLP-expert slices are per-parent. This is the Mixtral shape, not the "N independent models behind a gate" shape.

**Verdict.** Mated-model-as-MoE export is a real mechanism *if and only if* the export operates on decomposed parents and routes per capability. Otherwise it is an ensemble wearing MoE clothes, and the sparsity math does not close.

## (2) THE DESIGN

**Minimal export format, `fusion.moe.v1`:**

```
fusion.moe.v1/
  manifest.json        # {parents:[{id,hash,slice_map}], shared:[...], router:{...}}
  shared/              # attention (q,k,v,o), embeddings, layernorms - merged once
    attn.safetensors
    embed.safetensors
  experts/
    e{NN}.safetensors  # one per (parent, slice): FFN gate/up/down only, 100-500M each
  router.safetensors   # small linear or MLP, input = pooled prompt signature
  tokenizer/           # identical across parents or error
```

**What becomes the router.** Not a trained gate. A frozen probe: mean-pooled last-hidden of the shared attention stack at layer 2, projected to N_experts, top-2 with softmax. Trainable for one hour on a task-labeled mix, or initialized from `(task -> parent)` labels you already have from the mating pairs. Do not learn routing from scratch; seed it.

**What shares.** Everything except FFN. Two 2B parents share 60-70% of FLOPs, so per-expert cost is the FFN width. 8 experts of 400M at top-2 gives ~800M active FFN + shared backbone, which fits the 7B Q4 envelope on your 6GB card.

**Runtime.** llama.cpp, not DeepGEMM. `amd-vulkan-equivalents` line "FP8/blockwise scaling: requires tensor cores; not applicable to gfx1010." DeepGEMM's whole point is FP8 grouped GEMM on Hopper coalescing (`deepgemm-mechanics`, Precision paths). RDNA1 has no MFMA and no FP8. The transferable pattern is the *scheduler* (persistent CTAs pulling (expert,tile) work), not the arithmetic. llama.cpp's `mul_mat` shader (`amd-vulkan-equivalents`, llama.cpp Vulkan path) has no persistent-kernel support but adding a count-based work-item dispatch is a 100-line shader diff. Ship the format; patch llama.cpp; do not chase DeepGEMM onto gfx1010.

## (3) THE FALSIFIER

**Cheapest kill, one sitting, CPU or 6GB RDNA1.** Take two 2B local checkpoints. Merge only the FFN blocks with TIES or DARE (free, `moe-mating-connection` line "task arithmetic, TIES, DARE"). Produce three artifacts:

- **A: dense merged.** Full TIES merge of parent1+parent2.
- **B: MoE-export.** Shared attn+embed merged; FFN blocks from each parent become experts 1 and 2; router = hardcoded by prompt-class label (math vs chat) to prove the routing surface exists. Top-1.
- **C: ensemble baseline.** Run both parents independently, pick by a trivial score.

Measure on 200 held-out prompts, half math half chat, on Q4_K_M via llama.cpp ROCm (`fp4-fp8-precision`, "GGUF Q4_K_M or Q5_K_M via llama.cpp ROCm").

**Kill condition:** if B is not strictly better than A on both math and chat slices (per-slice wins, not aggregate), the sparsity is not buying routing value and the door is an ensemble. If B does not beat C at equal wall-clock tokens/sec (B must be faster because it runs one expert, not two), the door is expensive dressing. If both hold, scale to 8 parents as experts 3-8 and the mechanism feeds.

**My deliverable's falsifier:** this design dies if `router.safetensors` cannot be replaced by the hardcoded label router in test B without dropping below merged-dense quality. That would mean the capability decomposition failed at the slice boundary, and the export should not be built.
