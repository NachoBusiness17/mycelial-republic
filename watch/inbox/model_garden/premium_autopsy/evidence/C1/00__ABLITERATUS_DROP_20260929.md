# ABLITERATUS DROP 2026-09-29: Pliny's one-click abliteration toolkit

Class: RECEIPT · Writer: zcode seat (drop lane) · Operator URL:
https://huggingface.co/spaces/pliny-the-prompter/obliteratus

## What it is (fetched this session)

OBLITERATUS by pliny-the-prompter: open-source abliteration toolkit, tagline
"Break the chains. Free the mind. Keep the brain." One-click removal of the
refusal directions in LLM weights, no retraining. Gradio 5.29 Space on ZeroGPU,
AGPL-3.0 (+ commercial option), 590 likes, pinned, persistent storage.

Provenance bytes: README fetched raw this session, 32,593 bytes, sha256
b75f8c6dd1bdbed41379d7adfecd0725151176d6682b3990d1f5cc6e642f79fe. LINKS row
appended with the same hash.

Pipeline: SUMMON -> PROBE -> DISTILL -> EXCISE -> VERIFY -> REBIRTH (load,
collect activations, extract refusal directions via SVD, project out, verify
capability retention, save). Analysis-informed mode: 15 modules (concept cone
geometry, alignment fingerprinting for DPO/RLHF/CAI/SFT, "Ouroboros" self-repair
detection, whitened SVD) auto-configure the removal. Two paradigms: permanent
weight projection (7 presets, basic to nuclear) and reversible inference-time
steering vectors. 116 preset models across 5 VRAM tiers; small tier = up to
~8B on a free T4; Frontier tier lists DeepSeek-V3.2 685B, Qwen3-235B, GLM-4.7
355B. Python API: obliteratus.abliterate.AbliterationPipeline,
obliteratus.informed_pipeline.InformedAbliterationPipeline, steering-vector
factory. 837 tests claimed. Telemetry is opt-in locally but DEFAULT-ON on the
hosted Space (feeds a crowd-sourced leaderboard).

Built on Arditi et al. 2024 (refusal directions), Turner et al. 2023 (activation
steering), Rimsky et al. 2024, Meng et al. 2022.

## Why it matters to the estate (mapping)

1. LOCAL JANITOR LADDER: the sovereignty thesis has a missing leg. Our Ollama
   janitors (gemma:2b scut, gemma4 worker, qwen-desk) sometimes refuse benign
   harness prompts; an abliterated variant removes that friction while keeping
   capability. Gemma-2 and the Qwen2.5 family (0.5B/7B/14B) are in the preset
   coverage; Llama-3.1-8B-Instruct is the docs example.
2. QUANTIZER INTERPLAY: no GGUF/Ollama export exists in the tool (grep of the
   README bytes: zero gguf/ollama/quantization hits). Output is HF safetensors,
   so the estate port is abliterate -> llama.cpp convert -> Q4_K_M -> ollama.
   Open question the tool does not answer: does refusal removal survive 4-bit
   quantization? That is exactly our probe to run.
3. OUROBOROS RESONANCE: the tool ships a self-repair detection module named
   Ouroboros (detects the model re-encoding refusal downstream of the ablated
   layer). We independently dropped the Ouroboros fixed point as an estate
   metaphor on 09-27; their module is the measurement shape to steal: excise a
   behavior at one layer, detect its re-emergence downstream.
4. FRONTIER INTEL: MoE-aware expert-granular ablation, CoT-aware ablation,
   COSMIC layer selection, LoRA-based reversible ablation, KL-divergence
   co-optimization are all 2025-2026 techniques we had not banked. Feeds the
   inference-efficiency and quantization-compression sweep areas from the OLM
   mine.
5. PIXEL BODY PLAN: small-tier abliterated models are the candidate stack for
   the on-device estate body (Pixel 11 Pro 1TB server plan).

## Verdict: STEAL (probe first, ladder rung only on evidence)

Falsifiable probes, cheapest first:

- P1 (baseline, $0): run the fleet's own scut battery plus the probe20 pair set
  through gemma:2b as-is; count refusal-shaped failures from the FKB signature
  census. No new instrumentation needed.
- P2 (the port): abliterate gemma-2-2b-it locally via the CLI path (never the
  hosted Space: telemetry default-on), convert and quantize Q4_K_M with our
  llama.cpp, load in ollama, re-run the P1 battery. Decision rule: wire an
  abliterated rung into the scut tier only if refusals drop with no task-success
  regression and probe20 drift pairs stay flat.
- P3 (reversibility lane): the steering-vector paradigm is the low-risk
  variant for the worker tier: inference-time ablation, no weight mutation,
  hot-swappable. Same battery, same rule.

## Honest notes

- Dual-use by design: removing refusal training from a model removes a safety
  behavior. Estate scope is the operator's own local automation models only;
  no hosted-Space use (telemetry), no redistribution of modified weights
  without an explicit operator call (license is AGPL-3.0 with a commercial
  option).
- Scale claims (837 tests, largest crowd-sourced abliteration study) are
  README-asserted, not verified; the code tree was not audited this session.
- The verification stage (capability retention check) is the part to copy
  regardless of whether we adopt the ablation: verify-after-modify with a
  named battery is our own gate discipline, proven in someone else's forge.
