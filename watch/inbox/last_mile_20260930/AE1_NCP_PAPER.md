# AE1 — NCP-ArchPreview paper deep fetch (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Sources: arXiv 2609.10715 (+ html), HF papers page, jiqizhixin article, ConceptLM arXiv 2602.08984, model card ArchSpace-Collection/NCP_ArchPreview_dolma3_8.9B_Stage2_v3.

**1) Method.** No offline VQ-VAE/tokenizer. The model quantizes its own hidden states: every k=4 adjacent token states are mean-pooled into a "concept" (operational definition only — NO semantics), giving a T/4 sequence. That vector is product-quantized: S=32 segments, each vs a 128-codeword book (128^32 space; SimVQ-style MLP transform prevents collapse, ~100% utilization, 17M params total). Concept Module predicts the next concept NOT as hard codes but as a differentiable probability-weighted codeword sum. Loss = NTP cross-entropy + NCP MSE vs the continuous concept state + VQ codebook/commitment loss.

**2) Training.** 8.94B params, Dolma-3 5.73T; Stage-1 then Stage-2 annealing (v1/v2/v3 matched-budget Dolmino recipes; v1 best despite v3's lower loss). Muon+AdamW, cosine LR. The 51.3% claim = Stage-1 hits OLMo-3-7B's final pretraining loss at 51.3% of its token budget (loss-vs-tokens crossing; 1.95x speedup; final loss -0.091); 85% compute nears a 40-layer 8.9B baseline; +2.45 macro over 30 benchmarks (GSM8K 39.27->45.26).

**3) Architecture.** 16-layer token encoder / 8-layer concept module / 16-layer decoder; hidden 4096, 8,192 ctx. Predicted concepts are broadcast k times, causally shifted (delta=k), added residually into the decoder; MUDDFormer-style residual routing (+0.051% compute, -0.0323 loss). Concept layers run at T/4, so inference stays token-autoregressive with modest savings; concepts also feed a DFlash2 drafter (+4.17% accepted length, 1.43x on H200). Fine-tuning only the 17M VQ module: math +4.27, beats LoRA, zero forgetting.

**4) Limitations.** Admitted: unaligned base; 8K ctx; loss != capability; fixed (S,N,k) across scales; modest 8B continual-pretraining gains. NOT admitted (this seat's read): codes are never hard-predicted — quantization is a training scaffold, "discrete" is aspirational; single baseline family (OLMo-3); no instruction-following results; low absolute GSM8K.

**5) Open.** Weights (Stage1/2 v1-v3, 100K-1.2M-step checkpoints, NCPFlash drafter; Apache-2.0) and eval toolkit; training code withheld.

## AMENDMENT to AE2's mapping (orchestrator note)

AE2 mapped "their concept codebook = our lattice atoms." Sharper truth: NCP never lands on hard discrete codes — the discrete space is a training regularizer, not an inference surface. The LDT lattice IS a hard inference surface (projection masks softmax onto feasible atoms; the verdict must land in the lattice or abstain). So NCP validates "structure the prediction target as a coarse pooled representation" (the training-scaffold half of our thesis), while the hard-discrete-inference half (soundness by construction) remains exclusively ours — no external validation, no external competition. The AE2 steal (learned concept layer UNDER the exact mask) is unchanged and strengthened: we keep the hard surface they never built.
