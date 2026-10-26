# VERDICT m012

verifier: hermes (funded tier)
ts: 2026-10-08T16:45:00+00:00
work_item: m012
verdict: OWED

---

## What the ask demands

Benchmark Vulkan vs CPU quantization throughput on "gfx900 (RX 5600 XT)":
llama-server Q4_K_M 7B at -ngl 0/33/66/99, 512 ctx, tokens/s table.
Hypothesis: Vulkan slower than CPU for small layers because missing DP4A
forces float fallback. Fill the OWED gap — no public gfx900 Vulkan quant
benchmark exists.

## Settlement per component

| Component | Receipt | Status |
|---|---|---|
| Hardware ID: RX 5600 XT = gfx900 | lane_profiles.yaml (RX 5600 XT, no CUDA), w-quant-compare_hermes.md:5 (gfx1010), TechPowerUp Navi 10 spec, amdgpu_targets.desc | **WRONG** — RX 5600 XT = gfx1010 (Navi 10, RDNA1). gfx900 = Vega 56/64. The ask conflates two architectures. m012_hermes.md inherits the error ("RX 5600 XT (gfx900) confirmed via OpenCL ICD"). |
| "No public gfx900 Vulkan quant benchmark" | web_search found daimonionnn/amd-vega-rocm-vulkan-llm-toolkit (gfx900 iGPU benchmarks) and dhavli/llamacpp-vega-gfx900 (Vega 56, decode 13.43 t/s, int dot: 0) | **FALSE** — gfx900 Vulkan benchmarks exist. But the ask is about RX 5600 XT (gfx1010), and no ngl 0/33/66/99 comparison for Q4_K_M 7B on this card exists. |
| Hypothesis: Vulkan slower for small layers due to missing DP4A | hipfire.dev RDNA table (gfx1010 Navi 10 = scalar, no packed DOT), reserella.com (Navi 10 is only Navi without dot instructions), dhavli RESULTS.md (int dot: 0 on gfx900) | **PARTIALLY PLAUSIBLE** — DP4A absent on BOTH gfx900 and gfx1010. But dhavli data shows Vulkan beats ROCm on gfx900 (not Vulkan vs CPU). No Vulkan-vs-CPU benchmark on RX 5600 XT exists to settle this. |
| Benchmark table (ngl 0/33/66/99, tokens/s, VRAM, perplexity) | m012_hermes.md FINDING: no Q4_K_M 7B model on disk, only 128M embedding GGUF | **OWED** — never produced. Cannot run from this session. |
| Repo receipt for hardware envelope | lane_profiles.yaml: rx5600xt_actor, 6 GB VRAM, Q4_K_M fits, 7B max | **SETTLED** — repo confirms the card spec. |

## Errors in prior work

1. **m012_hermes.md** (banked answer): hardware ID wrong — "RX 5600 XT (gfx900)". Confirmed via OpenCL ICD is incorrect; the OpenCL ICD would report gfx1010 for this card.
2. **m012_verify.md**: cites m012_openrouter3.md as "absent" — it EXISTS (1753 bytes). Cites `mag/mq/m012_openrouter3.md` — wrong path, mag/mq/ absent. Claims hypothesis "reversed" based on dhavli Vulkan-vs-ROCm data — that is not a Vulkan-vs-CPU comparison, so the conclusion is not simply reversed.
3. **w-quant-compare_verify.md**: cites `configs/lanes.yaml:28-62` — actual file is `configs/lane_profiles.yaml`. Minor citation error.

## Verdict reasoning

The ask's substance is NOT fully verified:
- The hardware ID is wrong (gfx900 vs gfx1010) — a factual error in the ask that the banked answer repeated.
- The "no sources exist" claim is partially false (gfx900 benchmarks exist) but irrelevant to the specific ask configuration (RX 5600 XT + Q4_K_M 7B + ngl 0/33/66/99 comparison).
- The core measurement (benchmark table) was never produced and cannot be produced from this session — no Q4_K_M 7B model on disk, no verified AMD Vulkan driver stack confirmed from this terminal.
- The hypothesis has partial support (DP4A absent on both gfx900 and gfx1010) but the Vulkan-vs-CPU comparison is unmeasured.

Repo receipts named: lane_profiles.yaml, w-quant-compare_hermes.md, m012_hermes.md, m012_verify.md, m012_openrouter2.md, m012_openrouter3.md, w-quant-compare_verify.md.
Web receipts named: dhavli/llamacpp-vega-gfx900/RESULTS.md, daimonionnn/amd-vega-rocm-vulkan-llm-toolkit, hipfire.dev/rdna-wmma, reserella.com Navi dot instructions, TechPowerUp RX 5600 XT spec, amdgpu_targets.desc.

## What the operator needs to run this

1. Correct the hardware ID: RX 5600 XT = gfx1010 (RDNA1), not gfx900.
2. Download Qwen2.5-7B-Instruct-Q4_K_M.gguf (~4.4 GB) to the box.
3. Confirm AMD Vulkan driver: `vulkaninfo --summary` should show GPU id for Navi 10.
4. Run llama-server from the Vulkan backend build with `--verbose` for per-request tokens/s.
5. 3 warmup + 5 measured prompts per ngl level, same seed, 512 ctx.
6. CPU baseline (-dev none) first, then Vulkan offload steps.

VERDICT: OWED