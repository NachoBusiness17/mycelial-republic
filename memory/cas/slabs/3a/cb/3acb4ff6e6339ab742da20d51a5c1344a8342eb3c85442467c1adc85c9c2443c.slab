# impfeed proposal — w-quant-compare depth 1

## Most interesting finding (Hermes, ling-3.0-flash-sante)
- gfx1010 Vulkan runs every k-quant on-GPU with same shaders as CUDA; only gap is no FP8 tensor ops (RDNA3+)
- 6 GB VRAM is the real ceiling: Q4_K_M ~4.6 GiB fits, Q6_K ~6.4 GiB doesn't
- **INT8 (Q8_0) sleeper: <1.1% quality loss on 7B, fits ~5.5 GiB** — more VRAM headroom than Q4_K_M
- **Embedding-table residue claim: 14% of any 7B file is embeddings regardless of quant scheme** — means aggressive 4-bit quantization wastes effort because the unquantized embeddings eat the savings
- Q5_K_M or Q8_0 beats Q4_K_M on the 6 GB card: quality gap smaller than the VRAM gap looks

## Proposed investigation (depth 1 of 2)
The 14% embedding-table residue claim is the hinge: if true, it rewrites the quantization math for any model on a VRAM-constrained card. A free-lane model with web access can verify this by checking llama.cpp source (ggml-alloc.c, token embeddings handling), bitsandbytes NF4 docs, and any benchmark that decomposes size by tensor type. Then measure: does Q8_0 actually win over Q5_K_M on a 6 GB card once context length is factored in (more VRAM headroom = larger context = fewer recompute stalls)?

## Exact investigation item
{
  "ask": "Verify the '14% embedding-table residue' claim for 7B models across quantization schemes (Q4_K_M, Q5_K_M, Q8_0, NF4). Search llama.cpp source and ggml docs for how token embeddings are quantized (or not) per scheme, find any benchmark that decomposes model file size by tensor type, and check whether the residue percentage holds across model sizes (1B-70B). Then determine: on a 6 GB VRAM card, does Q8_0's smaller residue + larger context window actually beat Q5_K_M in throughput-adjusted quality, or does the per-token compute cost of INT8 dominate at generation time?",
  "tier": "free",
  "max_tokens": 3000
}
