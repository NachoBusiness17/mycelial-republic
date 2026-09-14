
## ANTIREZ BENCH — the Oct 27 day-one probe protocol (intake 22/25 BUILD NOW, 09-04)
antirez (Salvatore Sanfilippo) ran GLM-5.3 Q4 on two Macs with tensor-parallel, scored 10/12 hard tasks. His table IS the day-one probe: same tasks, same quant, TP across the 4x — beat 10/12 and the substrate is proven on a named stranger's benchmark. Card: watch/INTAKE_ANTIREZ_GLM_QUANT_20260904.md. Gauntlet addition from his reply thread: the stays-on-task / out-of-answer damage axis.

## LILY — Perplexity's local inference engine (DIG 2026-09-04, flag: watch/scout/HARVEST_FYP_20260904.md item 1)

The monitor's read — "the Rocinante thesis getting corporate engineering" — is
Supported but NARROWED by measurement. Lily is the single-Mac edge leg of a hybrid
split, not a cluster play. Perplexity's other garden projects (fabric-lib, p2p-all-to-all)
are datacenter RDMA for AWS EFA — no multi-Mac story anywhere in the repo. The 4x
thesis is still ours (and NVIDIA PAIR's — pending search).

### MEASURED ($0, primary sources)
- REPO: github.com/perplexityai/pplx-garden, subdirectory `lily/` (announced @perplexity_ai
  status 2095241544383226274, Sep 2 2026; blog: perplexity.ai/hub/blog/optimizing-on-device-inference-for-apple-silicon).
  Garden: 791 stars / 88 forks / 13 open issues; lily pushed 2026-09-02.
- LICENSE: Apache-2.0 (lily/LICENSE + NOTICE; NOTICE credits Metal kernels adapted from
  MLX/MLX-LM). Garden root is MIT; Lily itself is Apache-2.0.
- MODEL: exactly ONE — Qwen3.6-35B-A3B, MLX affine 4-bit group-64, pinned to immutable
  revision 38740b847e4cb78f352aba30aa41c76e08e6eb46 of mlx-community/Qwen3.6-35B-A3B-4bit
  (~19.4 GB). Load-time validation rejects everything else: dense Qwen, smaller Qwen, BF16,
  GGUF, AWQ, GPTQ, int8, fp8. (Third-party DeadByDawn101/lily-engine is a detached re-upload
  attempting model-agnosticity — Unproven, 0 stars, watch only.)
- HARDWARE: Apple GPU family 10+ = **M5 and newer only**, macOS 26+, Rust 1.92 pinned.
  Will not run on M1-M4. Benchmarked on M5 Max 40-core GPU, 128 GB unified memory.
  This is exactly Rocinante's silicon class — the engine is BORN on the horse's generation.
- API: OpenAI-compatible minimal subset — POST /v1/chat/completions, GET /v1/models,
  GET /health. Greedy decode only, non-streaming, text-only, thinking disabled, no tools,
  no multimodal. Two-entry LRU token-prefix session cache keyed by `prompt_cache_key`
  (reports reused tokens — the KV-cache-economics arc in vendor voice).
- BENCHMARK (their numbers, reproduction steps + fail-closed matrix runner shipped):
  1.23x prefill / 1.35x decode vs MLX-LM 0.32.2 average; at 4K/4K: 5,750 prefill t/s,
  187 decode t/s. Gains are prefill + attention-path engineering (fused dequant-in-GEMM
  +77%, GPU-resident MoE routing +89%, GQA packing +24% at 32K); MoE decode GEMMs already
  at 97.9% of sustained memory bandwidth — near-zero decode headroom left for anyone.

### MAP (fleet ties)
1. **UZU LANE CALIBRATION FLAG (the big one):** Lily's docs measure speculative decoding
   as **18% SLOWER** at batch-1 for this MoE model on M5, and reject it at the API level.
   This directly tensions the uzu day-one slot (ROCINANTE_PREP_20260903.md: uzu claims ~2x
   via spec-decode for Qwen3.6 27B on M5). Not a contradiction — different checkpoint
   (dense 27B vs sparse 35B-A3B, different decode economics) — but the day-one test is now
   a HEAD-TO-HEAD: uzu vs lily on the same silicon, measured, not assumed. uzu loses its
   default-pole status until it wins that run.
2. **Maze-keeper brain runtime:** Lily as-is is crippled for a brain runtime (greedy-only,
   no streaming, no tools, one pinned checkpoint — our QLoRA adapter can't load). It stays
   runtime candidate #2 behind uzu, promoted to candidate for the BASE model serving leg
   if the head-to-head wins. The steal is the KERNEL PATTERNS (Apache-2.0 lets us lift them):
   fused dequant-in-GEMM, GPU-resident expert routing, token-prefix session cache — the
   session-prefix cache pattern maps straight onto our lane-router conversation reuse.
3. **Hybrid-compute pattern = our lane router in vendor voice:** Perplexity Computer splits
   on-device (Lily) vs cloud (ROSE engine) so "on-device compute doesn't bottleneck" — the
   exact bulk→local/judgment→cloud routing the fleet router table already encodes.
   Corporate confirmation the lane-router shape is the production pattern, not a hack.
4. **Timing:** M5-only requirement means zero testable surface before Oct 27 — Lily and
   Rocinante land together. Nothing to do today; everything shortened on day one.

### VERDICT
- Claim 1 "Lily = the Rocinante thesis, corporate-engineered": **Supported, narrowed** —
  single-Mac edge leg only; no cluster story in the repo (fabric-lib is AWS RDMA).
- Claim 2 "uzu spec-decode ~2x on M5": **Disputed-adjacent** — Perplexity's contrary
  measurement on the same chip class; settle on Rocinante, not in the watch.
- ACTION: **BUILD (windowed to Oct 27)** — a day-one head-to-head slot: lily vs uzu serving
  Qwen3.6-35B-A3B-4bit on the 4x M5 Ultra, batch-1 and batched, tokens/s + memory. ~30 min
  setup (cargo build --release --locked + pinned hf download + curl). Until then: CALIBRATE —
  watch the repo for model-coverage widening ("future work: more models, chips, serving
  workloads") and the DeadByDawn101 generalization fork for traction.

## GROK CLI PRIMER — Rocinante sizing data (09-04, headless door confirmed)
The grok CLI headless door WORKS: `~/.grok/bin/grok --always-approve -p "<prompt>"` (single-turn, stdout, auth pass-through, Grok 4.6 high). Sizing intel for the 4x M5 Ultra (~768GB unified):
- GLM-5.3 (743B) MLX 2-bit ≈ **322GB at ~80% quality retention** — FITS the 4x with headroom.
- 4-bit: 15–20 tok/s on a 512GB Studio — the per-box rate; 4x TP scales it.
- HAZARD NAMED: mlx-lm bug corrupts GLM past 2K tokens — long-context LOCAL agents flagged unsafe until the fix lands. Day-one probe must include the 2K+ context test.
- Second headless research door confirmed (claude CLI + grok CLI) — the scout runs on either.
Source: watch/scout/GROK_CLI_PRIMER_20260904.md (6/6 URLs fresh, zero overlap with the web run — the two doors are complementary senses).

## R-1 PIN — GLM-5.3-Flash Unsloth-GGUF speedup benchmark (card-worker build, 09-04)
- R-1 = ROCINANTE_DAYONE_BENCH: pull unsloth/GLM-5.3-Flash-GGUF 4-bit (164-212GB; fits 512GB unified with headroom), llama.cpp with the Unsloth PR, MTP n=2-3.
- Script: scripts/rocinante_r1_bench.mjs (zero-dep Node; --engine ollama|llama.cpp|custom-command; 5 fixed prompts x N=3; JSON out: tok/s, p50/p90 latency, success rate; MTP toggle placeholder).
- Gates: beat 63 tok/s baseline; reach 110-125 (uzu targets); speedup >= 1.6x Unsloth GGUF+MTP vs vanilla (ceiling 3.4x long-ctx).
- HARDWARE GATE: Oct 27 (Rocinante unbox). Source: watch/INTAKE_UNSLOTH_GLM53FLASH_LOCAL_SPEEDUP_20260904.md.
