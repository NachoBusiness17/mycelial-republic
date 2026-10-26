# WORK w-quant-compare

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-09-29T22:04:07.772974+00:00
finish: stop cached_tokens: 0
ask: Compare quantization approaches: read the quantization handbook poster (INT4/FP8/NF4, W4A16, per-channel/group) and map each method to our estate's hardware (RX 5600 XT gfx1010 Vulkan, llama.cpp). Which methods work TODAY on our card vs NVIDIA-only? What's the quality/speed tradeoff? Return a table.

---

FINDING: Poster not provided; mapping from repo knowledge only. On RX 5600 XT gfx1010 Vulkan + llama.cpp today: INT4 k-quant (Q4_K_M, Q5_K_M, Q6_K) runs, per-group is native, NF4 loads but Vulkan kernel status is OWED, FP8 is NVIDIA-only, W4A16 is not a llama.cpp format, per-channel is not used by llama.cpp native types.

STEALABLE idea: Ship Q4_K_M as the default estate quant because per-group INT4 is Vulkan-optimized and balances VRAM vs tokens/sec.

TESTABLE hypothesis: On gfx1010 Vulkan, NF4 tokens/sec will be >30% lower than Q4_K_M if NF4 lacks Vulkan dequant kernels, else within 10%.

EVIDENCE or OWED: OWED for FP8 Vulkan support, NF4 Vulkan optimization, W4A16 llama.cpp mapping, per-channel mapping. No source cited.

| Method | Works today on gfx1010 Vulkan | Quality/speed tradeoff |
| --- | --- | --- |
| INT4 (Q4_K_M) | Yes | 4-bit, fast, good quality |
| FP8 | No | Higher quality, NVIDIA only |
| NF4 | OWED | 4-bit norm, speed unknown |
| W4A16 | No | N/A |
| Per-channel | No | N/A |
| Per-group | Yes | Native to k-quant, best Vulkan perf |
