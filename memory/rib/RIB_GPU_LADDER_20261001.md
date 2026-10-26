# RIB_GPU_LADDER - when a card makes DeepGEMM-class runtimes worth adopting

Row zero minted 2026-10-01 from the DeepGEMM drop dossier
(watch/inbox/x_intel_deepgemm_20261001.md, sha256 2f008c46...931b).
The estate box is AMD RX 5600 XT (RDNA1, gfx1010): no MFMA, no cooperative
matrix, no FP8 path. DeepGEMM (DeepSeek, MIT: NVRTC runtime kernels, per-block
FP8 scaling, grouped GEMM for MoE) pays ONLY on NVIDIA tensor-core arch.
This rib is the tripwire so the memory-supercade radar has gates, not vibes.

## The five gates (ALL must be true before a card buys adoption work)

1. ARCH: SM90 (Hopper) or SM100 (Blackwell) = full pay. SM120 (Blackwell
   consumer) = verify-first (FP4 support varies by SKU). Never buy Ada/older
   for this purpose.
2. VRAM: 24 GB minimum (mates + 7B FP8 + KV), 32 GB preferred.
3. PRICE TRIGGER: 24GB+ Blackwell under ~$1200, or 5090-class under ~$1700,
   or used H100 under ~$4000. Above these, the quant lane (GGUF on current
   box) keeps winning per dollar.
4. SOFTWARE: CUDA 12.8+ with NVRTC reachable via cuda-python, plus vLLM or
   SGLang running FP8 on that arch in a container we can dogfood.
5. WORKLOAD: only fires when there is real FP8/MoE QPS demand - either the
   mating->MoE export door is built (DG1 adjudication pending) or local
   inference volume makes FP8 throughput the binding constraint.

## Standing verdict on the drop

Ignore DeepGEMM itself on this box; the steals already banked are (a) the
JIT-plus-disk-cache pattern (ticketed for the Godot parity twins:
tools/rule_parity.py:975, tools/flock_parity.py:454 re-pay engine boot +
GDScript compile every run), (b) the quant corrections (gemma:2b was Q4_0,
pulls ordered 2026-10-01), (c) this rib.
