# DG1_moe_mating_door (anthropic/claude-opus-5.5, turn 1, channel: content)

## (1) THE DOOR

**Steelman the kill.**
- If each mated parent becomes a full expert (all layers, all weights), the result is k dense models behind a gate. That is a learned-gate ensemble. Memory is k x parent, and the sparsity win disappears (deepgemm_results.jsonl:4, "a mixture of dense models, which is just an ensemble with learned gating").
- If the router picks one parent per sequence, that is model routing. It is cheap per token, but it still needs k x memory and has no MoE mechanics.
- Grouped GEMM pays only when experts are small and routing is sparse (deepgemm_results.jsonl:4).
- On a 6GB card, memory is the binding constraint, not FLOPs (deepgemm_results.jsonl:3, "7B at Q4 (~4GB weights + KV)"). An ensemble of 7B parents cannot load at all.

Verdict on the naive form: **dead**.

**Correction to the sherpa.** The claim that "nobody exports merged models as MoE" (deepgemm_results.jsonl:4) is likely wrong. Two pieces of prior art, both from my recall and not in the evidence:
- mergekit's `mergekit-moe` builds Mixtral-style MoE from dense same-base models, with hidden-state prompt gating (UNVERIFIED).
- Branch-Train-MiX (Sukhbaatar et al. 2024) branches a seed model, trains specialists, averages attention, and stacks the FFNs as routed experts (UNVERIFIED).

The door is therefore not unbuilt. It is built for hand-picked parents, not for population-fusion output.

**Win condition. All four must hold:**
1. **Common ancestor.** Parents share a base, so attention, embeddings, and norms merge cleanly. Only the FFNs diverge enough to keep separate.
2. **Experts are FFN blocks, not models.** Routing is per token, per layer, top-1 or top-2. Active parameters stay near one parent.
3. **Parents are specialists.** Their population fitness diverged on different capabilities. If they are all-rounders, a dense merge already captures them and the MoE is dead weight.
4. **Router is calibrated per capability.** It is initialized from the fitness tasks that made each parent survive.

Examples:
- Positive: same-base Coder and Math fine-tunes give FFN experts with token routing. This is a real MoE.
- Negative: an unrelated 2B and 7B, or k all-rounder siblings, or any whole-model sequence gate. Each of these is an ensemble in disguise.

## (2) THE DESIGN

**Export spec `MATE_MOE_v0`.** A seat can apply this as-is.

| Component | Source | Rule |
|---|---|---|
| Gate check | all parents | Reject if architecture, tokenizer, or base hash differ. Reject if parent-to-parent FFN cosine is above 0.99 (no specialization). |
| Shared: embed, attn, norms, lm_head | TIES or linear merge of all parents | One copy |
| Experts: layer l, expert i | parent i's MLP (gate/up/down) at layer l | Verbatim |
| Router W_r[l], shape [E x d] | mean layer-l hidden state of parent i on its top-fitness prompts | mergekit "hidden" mode equivalent (UNVERIFIED flag name) |
| Routing | top-2 if E >= 3, else top-1 | Per token |
| Container | Mixtral layout (Llama-arch parents) or Qwen2-MoE layout (Qwen2 parents, to keep attention bias) | then `convert_hf_to_gguf.py` -> Q4_K_M |

**Sizing on 6GB.** FFN is roughly 2/3 of a dense model's parameters (rule of thumb, UNVERIFIED).
- 4 x 2B parents: about 0.7B shared plus 4 x 1.3B experts, roughly 6B total. That is about 3.5GB at Q4, so it fits. Top-2 active is about 3.3B.
- 7B parents: E is at most 2 even at Q4, and it does not fit 6GB with KV. Cap the pipeline at **2B-3B parents, E of 4 or less**.

**Runtime.**
- **llama.cpp: yes.** It loads Mixtral and Qwen2-MoE GGUF on CPU and Vulkan (arch support UNVERIFIED in evidence). ggml-vulkan has tiled `mul_mat` (deepgemm_results.jsonl:2).
- **DeepGEMM: no.** It needs `wgmma`/`tcgen05` (deepgemm_results.jsonl:1), and gfx1010 has no MFMA, WMMA, or cooperative matrix (deepgemm_results.jsonl:2).
- **vLLM: no.** ROCm on gfx1010 is unsupported (UNVERIFIED).

The persistent (expert, tile) scheduler (deepgemm_results.jsonl:1) is a later Vulkan port target, not a v0 dependency.

## (3) THE FALSIFIER

This is also the falsifier of this deliverable. One sitting, CPU only.

**Setup**
- **Parents:** two same-base 0.5B specialists, for example Qwen2.5-0.5B-Instruct and Qwen2.5-Coder-0.5B-Instruct (same-base status UNVERIFIED; run the gate check first).
- **Artifacts:**
  - **A:** TIES dense merge.
  - **B:** `MATE_MOE_v0`, E=2, top-1.
  - **P1, P2:** the parents alone.
- **Instrument:** transformers, fp32, CPU, context 512, 20k tokens per slice, with `output_router_logits=True` on B. Log the date, commit hashes, and CPU model with every number.
- **Slices:**
  - **S_code:** held-out Python files.
  - **S_prose:** wikitext-2 test.

**Metrics**
- Perplexity per slice for each artifact.
- B's expert-usage share per slice.

**Feeds (door lives)**
- On each slice, B's perplexity is within 3% of that slice's specialist parent.
- A is more than 5% worse than the specialist on at least one slice.
- Expert usage differs between slices by more than 30 points, showing the router routes by capability.

**Kills**
- **Kill: dense suffices.** B is at or above A's perplexity on both slices.
- **Kill: router is not specializing.** Expert usage is within 10 points across slices.
- **Kill: shared attention broke the experts.** B is more than 3% worse than the specialist on its own slice.

If it feeds, rerun at 2B, E=4, on Q4_K_M in llama.cpp (Vulkan, gfx1010). Log tok/s against the best dense parent at the same quant.
