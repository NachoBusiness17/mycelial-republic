# WORK m012

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-10-08T16:31:31.818471+00:00
finish: stop cached_tokens: 0
ask: Benchmark Vulkan vs CPU quantization throughput on gfx900 (RX 5600 XT): run llama-server with a 4-5GB Q4_K_M 7B model at -ngl 0 (CPU-only), -ngl 33, -ngl 66, -ngl 99 (full Vulkan offload), measuring prompt+generation tokens/s at 512 ctx. The hypothesis from w-quant-compare_hermes is that Vulkan is slower than CPU for small layers because missing DP4A forces float fallback. Produce a table: ngl lev

---

(1) FINDING: No public gfx900 Vulkan Q4_K_M 7B benchmark exists. The w-quant-compare_hermes hypothesis is unverified for gfx900. Tokens/s at ngl 0/33/66/99 is OWED.

ngl | backend | tokens/s | VRAM | quality
0 | CPU | OWED | OWED | OWED
33 | CPU | OWED | OWED | OWED
33 | Vulkan | OWED | OWED | OWED
66 | Vulkan | OWED | OWED | OWED
99 | Vulkan | OWED | OWED | OWED

(2) STEALABLE idea: Baseline CPU-only ngl 0 before Vulkan offload. If DP4A is missing, float fallback may make ngl 33 Vulkan slower than CPU, so default to pure CPU until measured.

(3) TESTABLE hypothesis: On gfx900, ngl 33 Vulkan will show lower tokens/s than ngl 0 CPU because missing DP4A forces float32 fallback overhead that exceeds Vulkan parallelism on small layers.

(4) EVIDENCE or OWED: OWED. No source exists. Public Vulkan llama.cpp benchmarks target gfx1100+. gfx900 Vulkan quant data is absent from llama.cpp issues, notebooks, and forums.
