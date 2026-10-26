# WORK w-quant-compare

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-09-29T22:09:54.064085+00:00
finish: stop cached_tokens: 210
ask: Compare quantization approaches: read the quantization handbook poster (INT4/FP8/NF4, W4A16, per-channel/group) and map each method to our estate's hardware (RX 5600 XT gfx1010 Vulkan, llama.cpp). Which methods work TODAY on our card vs NVIDIA-only? What's the quality/speed tradeoff? Return a table.

---

(1) FINDING
Current verifiable support for RX 5600 XT gfx1010 Vulkan in llama.cpp is limited to GGUF quantized INT types implemented via the Vulkan compute backend. INT4 / W4A16 via GGUF Q4_0, Q4_1, Q5_K_M, Q8_0 is usable today. FP8 and NF4 native kernels are NVIDIA-only or require hardware FP8/NF4 support not present on gfx1010. Per-channel and per-group quantization is supported in GGUF metadata but execution on gfx1010 Vulkan depends on llama.cpp kernel availability.

(2) STEALABLE idea worth keeping
Use GGUF Q4_K_M with per-group 32 as default estate baseline for RX 5600 XT. It gives best quality/size tradeoff on Vulkan and avoids NVIDIA-only formats. Keep a second profile Q8_0 for quality-sensitive tasks.

(3) TESTABLE hypothesis
Q4_K_M per-group on RX 5600 XT Vulkan will run >1.5x faster than Q8_0 with <5% perplexity degradation on 7B models, while FP8 will be unsupported or fall back to emulation.

(4) EVIDENCE or OWED
OWED. No verifiable sources were provided for the quantization handbook poster and no live hardware test results for RX 5600 XT gfx1010 Vulkan with llama.cpp are available in this session. Sources for llama.cpp GGUF support and AMD FP8 capability were not cited. None exist in provided context.

Comparison table

Method | Works TODAY on RX 5600 XT gfx1010 Vulkan llama.cpp | NVIDIA-only | Quality/Speed tradeoff
INT4 W4A16 GGUF Q4_0/Q4_1/Q4_K_M | Yes, via llama.cpp Vulkan GGUF INT4 kernels | No | Highest speed, lowest VRAM, moderate quality loss
INT4 per-channel/group | Partial, group supported in GGUF metadata, execution depends on kernel | No | Better quality than per-tensor INT4, slightly slower
NF4 | No native hardware support on gfx1010; may load but falls back | Yes, native on H100/A100 with FP8/NF4 kernels | High compression, quality close to FP16, unsupported on AMD
FP8 | No hardware FP8 on gfx1010; llama.cpp Vulkan does not expose FP8 kernels | Yes, NVIDIA Hopper/Blackwell FP8 | High speed on NVIDIA, low quality loss, not usable on RX 5600 XT
W4A16 | Yes as INT4 GGUF W4A16 | No | Same as INT4 W4A16 above

Note: Table entries are based on general llama.cpp GGUF support. Exact kernel availability for gfx1010 Vulkan is OWED without source verification.
