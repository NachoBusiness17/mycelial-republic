# LANE R3 — Local MoE serving for GLM-5.3-Flash on CPU-only AM4/128GB DDR4
Date: 2026-09-01 | Fetch log: `lane_r3_fetch.log` | All claims quoted or UNVERIFIED

## 0. The model (from `/board/GLM53_LINEAGE_DROP_20260901.md` + GGUF cards)
320B total / 18B active, 288 MoE experts (top-8 + 1 tied shared expert), 45 layers: **34 KDA linear/recurrent + 11 DSA sparse (MLA-based)**, wrapped in mHC. Quant footprints (qtum card): IQ1_M **70.7GB**, IQ2_XS 92.1GB, IQ3_XXS 121GB, IQ4_XS **167GB**. Only IQ1_M/IQ2_XS/IQ3_XXS fit 128GB DDR4 with KV headroom. Task's "UD-IQ1_M / UD-IQ2_XXS" = utf8tools/Ubergarm dynamic format of these tiers (verified footprint-equivalent, exact naming UNVERIFIED).

## 1. Engine support today
- **llama.cpp (mainline): GLM5next support OPEN, NOT merged.** PR#27773 (timkhronos, Aug 26 2026) "mixes 34 KDA linear layers with 11 DSA, mHC and DeepSeek-style MoE... KDA layers reuse the Kimi-K3 implementation... mHC I reused the DeepSeek V4 implementation." MTP stripped, `indexer_compressor` tensor-naming churn (danielhanchen/timkhronos exchange) means quant shards vary by converter. Run via PR/Unsloth branch, not stock master.
- **GGUF availability is proof of runnability:** qtum's card lists arch `glm5next`, "made with llama.cpp," all 4 tiers imatrix'd in 15 shards. ug_/ubergarm/unsloth/batiai variants likewise exist. Do NOT pass `-ngl 0` manually — qtum says explicit `-ngl` **aborts auto layer-fitting** ("unable to allocate CUDA0 buffer"). For true CPU-only you set `-ngl 0` yourself and leave `-fa` off.
- **ik_llama.cpp:** supports DSA/sparse + advanced quants (PR#2045), hybrid with GLM5next lineage. Confirmed exists, CPU path quality UNVERIFIED on AM4.
- **ktransformers (kt-kernel): native day-one GLM-5.3-Flash** but is **SGLang + GPU-centric**: official FP8/BF16 weights (no GGUF), CPU expert offload needs **AVX-512/AMX** kernels + a GPU + ~350GB RAM for FP8. AM4 has no AMX; disqualifies as pure-CPU.
- **vLLM:** official recipe targets **Hopper/Blackwell GPU TP**, FP8; `--cpu-offload-gb` is "less efficient for MoE" (kvcache-ai comparison); SM120 sparse issues (#53963). Not CPU-only viable.
- **FreeToken (FlashML-org, GitHub, Apache-2.0):** edge MoE serving, explicit GLM-5.3-Flash "hybrid KDA + DSA/MLA, Manifold-Constrained Hyper-Connections" (PR#270, register.py). But requires **Linux+NVIDIA/CUDA** (the 753B 14.9t/s GPU number). Not pure-CPU on AM4.

## 2. Real t/s for 300B-class MoE CPU
- **No Ryzen/128GB-DDR4 pure-CPU GLM-5.3-Flash run is published yet** (UNVERIFIED by absence — r/LocalLLaMA still on unified-memory/GPU-offload). Closest reference:
- **batiai GGUF, CPU-only (-ngl 0), dual-Xeon 48c/96t/503GB:** `Q4_K_M ~7.16 t/s, Q3_K_M ~7.24, Q2_K ~7.66`. Quote: "Speed is largely insensitive to quant... only the ~18B active parameters (top-8) are heavily used per step." → bandwidth-bound, not quant-bound.
- **llama-moe-cache `glm53-mrow` fork (stock + M-row):** Core Ultra 9 285K + RTX 5090, IQ1_M: `17.11 → 19.29 t/s`. But CPU+GPU co-path, Windows/AVX-VNNI, mrow adds speed only for resident experts; quote "does not eliminate cold page faults... Do not present 19.29 tok/s as a cold-start guarantee." No 128GB-only read.
- Consistent physics: 18B-active MoE prefill+decode is DRAM-bandwidth-bound on CPU. AM4 DDR4 quad/dual-channel = far less bandwidth than the Xeon/Ultra9 references.

## 3. Hybrid-attention risk (KDA linear + DSA sparse) on ggml graphs
**Resolved — graphs support it.** PR#27773 explicitly reuses **Kimi-K3 for KDA linear layers** and **DeepSeek-V4 graph for mHC** (both already in ggml), MLA for DSA layers, with DSA indexer top-k + sparse masks and a `--dsa` toggle (ik_llama.cpp/#2045). KDA state tensors are protected F32 (`self_attn.A_log/k_conv1d/dt_bias`) in quants because "low bit-width destroys long-range recall." **The hybrid arch does NOT block CPU serving** — it's implemented as ggml ops usable on CPU; it predates/parallels the GPU kernels. Only blockers are (a) mainline PR not yet merged in repo, (b) quant-tensor-naming shard variance, (c) per-permutation flags to tune.

## 4. Verdict — expected t/s on 128GB AM4, UD-IQ2_XXS / UD-IQ1_M
- **Fit:** UD-IQ1_M (~70GB) and UD-IQ2_XXS (~92GB) both fit 128GB with KV/OS headroom. UD-IQ3_XXS (~121GB) is edge; skip. **IQ4_XS (167GB) does NOT fit.**
- **Expected:** roughly **3–7 t/s** on UD-IQ1_M / UD-IQ2_XXS, CPU-only. Bandwidth-scaling the batiai Xeon floor (7 t/s) down for AM4 DDR4 × fewer channels/cores gives the low single digits; with an expert-major/M2-style CPU kernel fork and warm pages, low end edges toward ~7. UNVERIFIED — no AM4 datapoint exists; 6–10 was the community top-of-mind guess for "strong Ryzen." Treat as interactive-for-chat, painful-for-agent, fine for batch.
- **Cost of going to 1-bit:** IQ1_M PPL 73.9 vs IQ4_XS 7.15 and IQ2_XS 20.3 (qtum, H100-measured) → IQ1_M is quality-degraded; IQ2_XXS is the quality/bandwidth sweet spot for this footprint.
- **Bottom line:** Hybrid KDA+DSA does **not** block CPU; llama.cpp (PR branch) is the only viable pure-CPU engine on AM4. Expect ~3–7 t/s on UD-IQ2_XXS, worse on UD-IQ1_M, no GPU. ktransformers/vLLM/FreeToken all need a GPU. If single-digit t/s is unacceptable, this lane cannot serve Flash interactively on 128GB AM4 — only a slow low-bit batch/sandbox seat. Recommend Qtum/Unsloth GGUF + PR-branch llama.cpp, IQ2_XXS first.
