# LANE 8/8 — ROCINANTE SIZING: DeepSeek-V4.1-Flash on 4x Mac Studio M5 Ultra

Date: 2026-09-10. Lane 8 of 8, v41_paces wave. Metadata only — no shards downloaded.
HF repo: `deepseek-ai/DeepSeek-V4.1-Flash` @ `dba1be0a` (MIT). Config + README + weight
index + reference `inference/` read directly off HF tonight.

## THE POINT

**Capacity is a non-problem; the runtime is the problem.** At native quant the whole
checkpoint is 475 GiB — it fits in 1.0 of our 2.0 TiB (4x 512 GB) with half the fleet
to spare, and the KV cache at 890 B/token is effectively free (0.85 GB at 1M context).
But **no MLX or llama.cpp build executes this architecture today**: MLX-lm has not even
merged DeepSeek-**V4** (open issues #1233/#1281), and llama.cpp merged V4 (PR #24162)
but V4.1 is a new `deepseek_v41` model type — CED encoder-decoder, CSA2, Engram
n-gram memory, all new. The only thing that runs the checkpoint is DeepSeek's own
PyTorch reference (`inference/`), which is CUDA-shaped (TP8 torchrun, custom fp8/fp4
kernels). **Rocinante buys the shelf, not the engine.** A V4.1 port (llama.cpp PR or
MLX) is the gating build between now and Oct 27.

## 1. Download size (verified from HF API, blobs=true)

- 48 safetensors shards (context said 49 — **DISPUTED**, API lists 48; recount on
  download night, `model.safetensors.index.json` is the arbiter).
- **Total: 510,296,708,312 bytes = 510.3 GB = 475.3 GiB** (index `total_size`
  confirms: 510,286,023,000 B of weights).
- Shape of the 48:
  - 2 monolith shards of **101.54 GB each** = `layers.1.engram` + `layers.14.engram`
    (6 tensors each; 12 Engram tensors repo-wide) — the **Engram conditional-memory
    tables, 203.1 GB = 40% of the whole download**.
  - 46 normal shards (~0.97–7.41 GB) = 307.2 GB backbone + vision encoder + DSpark
    draft (3 MTP layers, 128 routed draft experts).
- Native quant: dense = **FP8** (32x32 blocks, ue8m0 scales), experts = **FP4**
  (`expert_dtype: fp4`). Checkpoint is already quantized — there is no "BF16 original"
  to fall back to publicly.

## 2. Quantization ladder vs the 2 TB budget

Param census: 552B backbone + 196B Engram + ~1B vision ≈ **749B total params**,
8B active at prefill / 16B at decode. 384 routed + 1 shared expert, 6 active.

| Rung | Footprint | vs 2048 GiB budget | Notes |
|---|---|---|---|
| Native FP8 dense + FP4 experts (as shipped) | **475.3 GiB (510 GB)** | **23%** — fits 4x with 1.5 TiB spare; even 2x fits (475 into ~920 usable GiB) | The rung that exists today |
| Uniform FP8 (everything 1 B/p) | ~750 GB / ~698 GiB | 34% | No conversion gain — experts would grow 2x |
| Uniform 4-bit | ~375 GB / ~349 GiB | 17% | Costs Engram lossy; llama.cpp V4-Flash community GGUFs live here |
| Uniform 3-bit | ~281 GB / ~262 GiB | 13% | Quality cliff unmeasured; only if we wanted V4-Pro-class headroom later |

**KV cache** (claimed 890 B/token, FP4 E2M1 + E4M3 scale/16ch; global KV projected
from only `kv_source_layers [2,8,14,20]` — the CED trick — plus SWA window 128 and
`index_topk 512` sparse reads): **1M tokens = 0.89 GB**, call it 1–3 GB with indexer
keys + draft-model cache. On 2 TB this is noise; 1M context is free once weights load.

**Engram tables**: 203.1 GB resident (2 tables x ~384.0M rows x 256 dim, fp8) — but
access is a sparse per-token n-gram lookup, so the *working set* per token is
kilowatt-scale, not 203 GB. They must sit wherever layers 1 and 14 sit (both in the
20-layer causal **encoder** stage — both `kv_source_layers` 2/8/14 and candidate-source
layer 20 are encoder-adjacent too).

## 3. Runtime gap (the load-bearing finding — stated plainly)

- **MLX / mlx-lm: ABSENT.** Supports DeepSeek V2/V3 only. DeepSeek-**V4** is an open
  request (ml-explore/mlx-lm issues [#1233](https://github.com/ml-explore/mlx-lm/issues/1233),
  [#1281](https://github.com/ml-explore/mlx-lm/issues/1281)) citing CSA as the blocker.
  V4.1 (`deepseek_v41`) is not even requested yet.
- **llama.cpp: V4 yes, V4.1 no.** DeepSeek V4 support merged mainline
  (PR #24162, tracking issue #22319; CSA/HCA + hyper-connection fused ops, DSpark
  present with a known draft-KV leak #27155). But V4.1 adds on top: **CED**
  (20-layer causal encoder -> decoder whose global KV is *projected from encoder
  hidden states*, not its own layers), **CSA2** (Full/Reindex/Reuse static modes +
  hierarchical sparse indexer), **SWA Bounded Replay**, and **Engram** n-gram
  conditional memory (16M compressed vocab, 4-gram max) — none of which exist in any
  GGUF or graph today. **SUPPORTED: V4. UNPROVEN: V4.1. No V4.1 GGUF exists.**
- **What runs today:** DeepSeek's own `inference/` reference (torchrun TP8,
  dense-fp8/MoE-fp4 custom kernels) — a readable reference, not a serving engine, and
  its kernels target CUDA. On Apple silicon: nothing, as of tonight.
- **Consequence:** the port is a real build (weeks, not days), best started from the
  llama.cpp V4 base (DSAkin MLA + CSA + DSpark already in) adding CED stage split +
  Engram lookup ops. Alternative: run V4-Flash (not V4.1) on Rocinante day one —
  284B/13B-active, GGUFs exist, ~128 GB class per antirez's fork — and treat V4.1 as
  the stretch goal. That decision belongs to the operator.

## 4. Memory map (4x M5 Ultra, 512 GB unified each, 1.2 TB/s each, TB5 between)

M5 Ultra confirmed: 80-core GPU, **1.2 TB/s** bandwidth, 512 GB max
([Apple specs](https://www.apple.com/mac-studio/specs/)). Usable per box after macOS
~450–470 GiB. Interconnect: TB5 ~10 GB/s effective (or 10GbE).

**Chosen topology: PIPELINE (PP), not tensor-parallel.** TP needs per-layer allreduce
over a 10 GB/s hop — kills decode. Pipeline pays one hop per token.

| Box | Holds | Size (native quant) |
|---|---|---|
| Studio A | Embeddings + encoder layers 0–19 + **both Engram tables** + vision encoder | ~360 GB (~335 GiB) — fits ONE box |
| Studio B | Decoder layers 20–39 + output head + DSpark draft (3 MTP layers) + KV cache | ~155 GB (~145 GiB) |
| Studios C, D | Idle capacity at V4.1-Flash scale — reserve for KV at sustained 1M-ctx sessions, DSpark verification buffers, or a second model (e.g. V4-Flash GGUF) | — |

Minimum viable = **2 Studios** (A+B). 4 Studios = comfort + concurrency (two
pipeline replicas on A/B and C/D doubles batch throughput). KV 0.89 GB/1M tokens
replicates per replica for free. Engram's 203 GB both live on A; lookups are sparse
so bandwidth cost per token is small.

## 5. Expected performance band (UNCERTAINTY HIGH — no working runtime exists)

Physics anchor: decode reads the active weights each token. 16B active at ~0.6–0.8
B/param effective ≈ **10–13 GB/token** (+ sparse Engram reads, + KV top-k reads which
stay small thanks to index_topk 512). Pipeline splits the read across stages, so
per-token time ≈ max(stage read time) + hop latency (~1–3 ms on TB5).

- **Ceiling (pure bandwidth):** ~90–120 tok/s single stream on the bottleneck stage.
- **Realistic MLX-style efficiency (15–30% of peak, per M3-Ultra/671B receipts at
  ~16–18 tok/s):** **~10–40 tok/s single-stream decode**; DSpark speculative decoding
  (if ported) could push effective rate 1.5–3x on top; batch serving scales better
  than single-stream.
- **Prefill:** 8B active, compute-bound, input-heavy agentic workloads are the
  *design target* of CED — expect prefill to be the strong suit (est. thousands of
  tok/s), but entirely UNPROVEN without kernels.
- **Tri-state:** all numbers above are **UNPROVEN** (evidence: arithmetic + prior-gen
  receipts, zero V4.1 runs anywhere on Apple silicon). The only SUPPORTED claim is
  the footprint: 475 GiB < 2 TiB, KV negligible, 2 boxes minimum, 4 boxes comfortable.

## Sources

- HF API blobs: https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash?blobs=true
- config.json / inference/config.json / inference/README.md (same repo, sha dba1be0a)
- mlx-lm: [#1233](https://github.com/ml-explore/mlx-lm/issues/1233), [#1281](https://github.com/ml-explore/mlx-lm/issues/1281)
- llama.cpp V4: PR #24162, tracking #22319, DSpark leak #27155; [r/LocalLLaMA merge thread](https://www.reddit.com/r/LocalLLaMA/comments/1uj0fkw/deepseek_v4_pr_merged_into_llamacpp/)
- M5 Ultra: [Apple Mac Studio specs](https://www.apple.com/mac-studio/specs/)
