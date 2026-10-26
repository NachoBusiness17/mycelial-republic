# RIB_RIB_GPU_LADDER_20261001 - translated by babelfish v1.0.0 (2026-10-10)

**Minted:** 2026-10-10 (caller-supplied; the module reads no clocks).
**Source bytes:** 1,775 | sha256 `472d69d94739cc2bd63499a92fbd947ad14643d3f14afa45644713ce3b830065`
**Named roles found:** Hopper, Blackwell
**Dominant terms:** blackwell (3), under (3), arch (2), memory (2), quant (2), plus (2), tools (2), zero (1)

## THE LAW AS THEY STATE IT (verbatim, their voice)

> Row zero minted 2026-10-01 from the DeepGEMM drop dossier
> (watch/inbox/x_intel_deepgemm_20261001.md, sha256 2f008c46...931b).
> The estate box is AMD RX 5600 XT (RDNA1, gfx1010): no MFMA, no cooperative
> matrix, no FP8 path. DeepGEMM (DeepSeek, MIT: NVRTC runtime kernels, per-block
> FP8 scaling, grouped GEMM for MoE) pays ONLY on NVIDIA tensor-core arch.
> This rib is the tripwire so the memory-supercade radar has gates, not vibes.

## THE INVARIANT TRANSLATION (each row names its check; status UNVERIFIED until run)

| their claim | invariant form | the check |
|---|---|---|
| 1. ARCH: SM90 (Hopper) or SM100 (Blackwell) = full pay. SM120 (Blackwell | SM90 (Hopper) or SM100 (Blackwell) = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| consumer) = verify-first (FP4 support varies by SKU). Never buy Ada/older | consumer) = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| 2. VRAM: 24 GB minimum (mates + 7B FP8 + KV), 32 GB preferred. | quantity claim (24 GB) | re-count from primary bytes; compare against the stated figure |
| 3. PRICE TRIGGER: 24GB+ Blackwell under ~$1200, or 5090-class under ~$1700, | quantity claim (24GB) | re-count from primary bytes; compare against the stated figure |
| mating->MoE export door is built (DG1 adjudication pending) or local | mating- > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |

## INSTRUMENT ROWS (measurable with a named instrument)

| claim | instrument |
|---|---|
| 5. WORKLOAD: only fires when there is real FP8/MoE QPS demand - either the | sample N instances per the universal's domain and count exceptions |
| GDScript compile every run), (b) the quant corrections (gemma:2b was Q4_0, | sample N instances per the universal's domain and count exceptions |

## REGISTER (the unmappable remainder - kept verbatim, never struck)

The babel fish preserves what it cannot translate. Register is the
seed, not the defect.

- for this purpose.
- or used H100 under ~$4000. Above these, the quant lane (GGUF on current
- box) keeps winning per dollar.
- 4. SOFTWARE: CUDA 12.8+ with NVRTC reachable via cuda-python, plus vLLM or
- SGLang running FP8 on that arch in a container we can dogfood.
- inference volume makes FP8 throughput the binding constraint.
- Ignore DeepGEMM itself on this box; the steals already banked are (a) the
- JIT-plus-disk-cache pattern (ticketed for the Godot parity twins:
- tools/rule_parity.py:975, tools/flock_parity.py:454 re-pay engine boot +
- pulls ordered 2026-10-01), (c) this rib.
- [[BABELFISH-SOURCES: memory\rib\RIB_GPU_LADDER_20261001.md]]

## FALSIFIERS

- For each invariant row: run its named check against primary bytes;
  a mismatch kills the row, not the corpus.
- For the translation itself: a second pass over the same bytes must
  produce a byte-identical rib (determinism law).
- Class-deafness: an estate-authored doc must yield nonzero invariant
  rows and a woo corpus must yield nonzero REGISTER rows (spec falsifier).

## LINEAGE

- Translated by babelfish v1.0.0 (2026-10-10); spec watch/inbox/babelfish_20261010/SPEC.md
- Operator thesis: book-to-skill == closed-corpus-to-self-improving-system,
  in the direction you set, despite the platform's best wishes (2026-10-10).
