# WORK m012

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-10-23T23:28:47.579395+00:00
finish: stop cached_tokens: 48
ask: Benchmark Vulkan vs CPU quantization throughput on gfx900 (RX 5600 XT): run llama-server with a 4-5GB Q4_K_M 7B model at -ngl 0 (CPU-only), -ngl 33, -ngl 66, -ngl 99 (full Vulkan offload), measuring prompt+generation tokens/s at 512 ctx. The hypothesis from w-quant-compare_hermes is that Vulkan is slower than CPU for small layers because missing DP4A forces float fallback. Produce a table: ngl lev

---

(1) FINDING
No verified Vulkan vs CPU quantization throughput benchmark for gfx900 RX 5600 XT with llama-server Q4_K_M 7B at -ngl 0, 33, 66, 99 and 512 ctx exists in public sources. The requested table cannot be filled from verified data.

(2) STEALABLE idea worth keeping
Run the same llama-server Q4_K_M 7B benchmark on gfx900 with -ngl 0, 33, 66, 99 and log tokens/s, VRAM used and perplexity for prompt + generation at 512 ctx. Publish the raw llama-bench JSON and `llama-server` logs with driver version, ROCm/Vulkan loader version and kernel. This is the single measurement that decides hybrid CPU+Vulkan vs pure CPU ceiling on this card.

(3) TESTABLE hypothesis
On gfx900 RX 5600 XT, Vulkan Q4_K_M offload with -ngl >=33 is slower than CPU-only -ngl 0 for small layer counts because missing DP4A forces float fallback in the Vulkan quant kernels, so tokens/s decreases as ngl increases up to a crossover point.

(4) EVIDENCE or OWED
OWED. No public benchmark table for ngl level | backend | tokens/s | VRAM used | quality for gfx900 RX 5600 XT with llama-server Q4_K_M 7B at 512 ctx was found. Existing public Vulkan quant data is for gfx1100+ RDNA3/4 cards. Sources checked: none exist for this exact config.
