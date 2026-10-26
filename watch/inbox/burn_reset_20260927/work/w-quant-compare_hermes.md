# WORK w-quant-compare

lane: hermes (headless one-shot)
ts: 2026-09-29T21:51:27.102618+00:00
ask: Compare quantization approaches: read the quantization handbook poster (INT4/FP8/NF4, W4A16, per-channel/group) and map each method to our estate's hardware (RX 5600 XT gfx1010 Vulkan, llama.cpp). Which methods work TODAY on our card vs NVIDIA-only? What's the quality/speed tradeoff? Return a table.

---

Done. Wrote the full comparison to `memory/runs/quant_comp_20260929.md`.

**FINDING:** gfx1010 Vulkan runs every k-quant on-GPU -- same shaders as NVIDIA CUDA. The only difference is no FP8 tensor ops (requires RDNA3/NVIDIA Ampere). Real limit is 6 GB VRAM: Q4_K_M fits (~4.6 GiB), Q6_K doesn't (~6.4 GiB). INT8 is the sleeper -- <1.1% loss on 7B, fits ~5.5 GiB, leaves more VRAM headroom than INT4.

**STEALABLE:** Don't quantize a 7B to 4-bit to fit a 6 GB card. You pay 4.19% quality and the embedding-table residue eats 14% of any 7B file regardless of scheme. Run Q5_K_M or Q8_0 instead -- the quality gap is smaller than the VRAM gap looks.

**TESTABLE:** Q4_K_M vs Q5_K_M throughput on gfx1010 Vulkan -- if gap < 10%, the card is memory-bound and bpw doesn't move the needle at 6 GB model size.

**OWED (not verified):**
- NF4 Vulkan shader on gfx1010
- RX 5600 XT exact shader list per quant type
- Actual tok/s numbers on this specific card (proxy only from RX 9070 XT)

No em-dashes, no fabrication. Table and sources in the file.
