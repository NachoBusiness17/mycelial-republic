# SHADOW WORK — WEIGHTS-VOLUME CARTOGRAPHER (sw50, 2026-09-06)

**Seat:** sw50 (shadow walker, 50/50 heavy instrument)
**Charter:** watch/SELF_STEAL_SHADOW_WORK_20260906.md — turn the model on our disk into an
environment you traverse.
**Instrument:** `mag/gguf_cartography.py` — pure-stdlib GGUF container parser + weights-volume
extractor. $0, no network, no dequant, read-only mmap on the GGUF.
**Subject:** `C:\Users\foste\.lmstudio\bridge-inbox\Qwen2.5-3B-Instruct.gguf` (1,929,903,008 B)
**Output JSON:** `state/shadow_work/weights_volume_qwen3b.json` (sha16 `867ffa24c9e710db`)

## Tensor census

| | |
|---|---|
| GGUF version | 3 |
| Arch / blocks / ctx | qwen2 / **36** / 32768 |
| Quant | Q4_K_M (embedding upgraded to Q6_K) |
| Tensors | **434** |
| Tensor data | 1,923,946,496 B = **99.69%** of file |
| Header | 5,956,490 B (data section starts at aligned 5,956,512) |
| Unaccounted | **0 B** — data_start + data == file size, perfectly packed |

Structure closes exactly: 1 embedding + 36 blocks x 12 (4 attn weights + 3 qkv biases +
2 norms + 3 ffn) + 1 output_norm = 434. **No `output.weight` exists** — Qwen2.5-3B ties
word embeddings, which is why token_embd.weight got upgraded to Q6_K [2048,151936]
(255 MB, the single largest tensor). The task's "28-layer ballpark" is **DISPUTED by the
file itself**: 28 is the 1.5B/7B shape; the 3B arch is 36 layers.

## Layer-gradient finding (first REAL weights structure we have ever rendered)

Exact F32 RMSNorm weights (attn_norm + ffn_norm, full-read, no sampling error) across all
36 blocks:

- **NORM SCALE RISES WITH DEPTH**: first-to-last ratio **3.97x** (blk0 = 0.381 → blk35 = 1.514),
  geometric growth **1.0402/layer** (~4%/layer), pearson r = 0.739.
- Shape: blk0 is a low outlier (0.381), ramps to ~1.0 by blk3, dips mid-network (min 0.679
  @ blk13), then a steady late-network ramp from blk19 to blk35. This is the classic
  first-block norm anomaly + late-network amplification, now measured on OUR disk.
- Method note: the first verdict said FLAT — a linear-fit threshold under-calls a geometric
  ramp. Re-classified on end-to-end ratio (>=1.25 RISES / <=0.8 FALLS / else FLAT). The fix
  is in `layer_gradient()` and travels with the instrument.

## Quant-proxy honesty (v1 law)

F32/F16 tensors get exact float stats; every quantized dtype gets byte-level PROXY stats
only (NO dequant in v1), sampled 4 MB/tensor in 16 aligned windows.

- Byte entropy on Q4_K_M/Q6_K payloads: 7.70–7.94 bits — **saturated** against the 8.0 max.
- Consequence found the hard way: entropy and zero-byte ratio (~0.2%) are flat and do NOT
  track weight scale on K-quants. The layer gradient is only provable on the exact F32 norm
  tensors. Honest label: PROXY stats describe the byte surface, not the weight distribution.

## What transfers to 5.3-flash's GGUF (P2, when downloaded)

1. The instrument runs unmodified — parser is arch-agnostic (any GGUF v1–v3, all 31 dtypes
   mapped incl. IQ1_M/IQ-quants). Point `scan` at the new path, change `--out`.
2. Same falsifier applies: census must close to ~100% of file with 0 B unaccounted, and
   tensor count must decompose as 1 + blocks x per-layer-shape + tails. Any mismatch = a
   parse bug or a nonstandard file, never a shrug.
3. The gradient question repeats verbatim: does 5.3-flash's norm scale RISE with depth,
   and does it carry the blk0 outlier? If the vendor ships F32/F16 norms again, the
   measurement is exact; the ratio thresholds (1.25/0.8) carry over.
4. Tied-embedding detection by absence of output.weight carries over as a structural check.
5. Proxy saturation is expected to repeat on any K-quant — do not re-derive a norm from
   entropy. If deeper weight-scale signal on quantized tensors is ever needed, that is a
   v2 decision (scale-field extraction = dequant-lite), gated as new work.

## Falsifiers

- Re-run `scan`: census and gradient reproduce deterministically (sampling is positional,
  not random — same file, same numbers).
- Census falsifier: `totals.unaccounted_bytes != 0` or tensor count not decomposing by the
  block formula → parser defect, DISPUTED.
- Gradient falsifier: recompute norm RMS with 10x tighter sampling (or full read) — ratio
  must stay >= 1.25; if it collapses to FLAT, the ramp was a sampling artifact (it will not:
  norm tensors are read in full).
- Proxy falsifier already logged: byte entropy vs depth correlation ~0 — if someone claims
  entropy is a norm proxy, this card DISPUTES it with numbers.

## Map cells (A6, seat sw50, verify PASS 90 cells tip=821c33df3ddf)

- SW/weights-volume/container-parsed #ccf0800db36b
- SW/weights-volume/tensor-census #a08b856e034f
- SW/weights-volume/layer-gradient #28e400799475
- SW/weights-volume/quant-proxy #821c33df3ddf
