# INTAKE: Z.AI ORG — THE CODE LAYER (github.com/zai-org, 52 public repos) — 2026-09-04

Genome: research_socratic (six steps) on L0 v1. Fold: one URL, no addenda. Sibling card
`watch/INTAKE_ZAI_DEVPACK_MEMORY_20260903.md` covered the DOCS layer (docs.z.ai); this is
the CODE layer. No card collision; endpoint/credit facts in the devpack card re-find here
only as background (repetition is emphasis, scored as re-find).

## ITEM
https://github.com/zai-org — our model vendor's open-source presence. Claim under test:
the org gives the fleet its vendor's CODE layer — open weights, finetuning recipes, SDK,
tooling — changing what we can pin, run locally, and feed the QLoRA campaign.

## 1. INGEST — receipts (org page 1 + 2 fetched; total 52 repos, complete inventory)
High-value rows (name — stars — what it actually is):
- **GLM-5** — 7.1k — flagship weights: GLM-5.3 744B-A40B, **GLM-5.3-Flash 320B-A18B**,
  5.2/5.1/5 all 744B-A40B; FP8+BF16 on HF+ModelScope; Apache-2.0. Finetuning: **Slime
  v0.3.0+ (RL)**, **ms-swift v4.4.0+ (SFT/PPO/GRPO)**; LLaMA-Factory NOT mentioned.
  Serving: SGLang, vLLM, KTransformers, Unsloth, TokenSpeed (Flash only), Ascend. NO
  official GGUF/MLX. No VRAM numbers in README.
- **GLM-4.5** — 4.4k — the family recipe book: 355B-A32B / Air 106B-A12B, and
  **GLM-4.7-Flash 30B-A3B**. Official LoRA (LLaMA-Factory: Air on 4x H100) and
  SFT/LoRA/RL (Swift) matrices; hardware table quoted verbatim (GLM-4.5 BF16 = 16x H100;
  "Server memory must exceed 1T"). Model code = `glm4_moe` in transformers/vLLM/SGLang.
  License discrepancy ON THE REPO: README says MIT, badge/file says Apache-2.0.
- **GLM-V** — 2.4k — **GLM-4.6V-Flash (9B) "optimized for local deployment and
  low-latency applications"** (vendor verbatim), GLM-4.1V-9B-Thinking/Base, 106B cloud
  variants; GGUF on HF; SGLang v0.5.15+/vLLM v0.25.0+; Apache-2.0.
- **GLM-OCR** — 7.4k — OCR model ("Accurate × Fast × Comprehensive"). Unprobed size.
- **GLM-ASR** — 853 — ASR-Nano, 1.5B params, speech recognition. **GLM-TTS** — 1.1k —
  zero-shot emotion TTS. **GLM-Image** — 1k. **GLM-Edge** — 164 — edge models.
- **GLM-skills** — 472 — "Official skills for the GLM family of models."
- **zai-coding-plugins** — 128 — "Z.ai Coding Plugins Marketplace in Claude Code."
  **zcode-plugins** — 8 — ZCode plugins marketplace (our own harness's, vendor-run).
- **glm-simple-evals** — 42 — GLM-4.5-series eval harness.
- **Synapse** — 454 — self-hosted AI workspace (teammates, shared memory, plugins), TS.
- **Open-AutoGLM** — 26k — phone agent (largest star count, lowest fleet fit).
- Legacy museum (~26 of 52): ChatGLM-6B 41k, ChatGLM3 14k, CodeGeeX family, CogView/
  CogVLM/CogVideo/GLM-130B — 2023-24 paper code, one-draft-of-the-brain material.

## 2. MAP — corpus intersections
- **QLoRA campaign** (`watch/CAMPAIGN_SYNTHESIS_20260903.md`): Stage 1 (packaging +
  preflight, 0.5d) needs a trainer choice; the org pins it — Swift (SFT/LoRA/RL recipes
  for the whole family) or LLaMA-Factory (LoRA). Stage 5 (deep compile) is
  Rocinante-gated; the org's own hardware table CONFIRMS no training on this box
  (68.7GB RAM, no CUDA). Open question the org resolves: **what base does the exported
  mind target?** GLM-4.7-Flash 30B-A3B is the same size class as our qwen2.5:32b
  maze-keeper — a GLM local lane is the new option.
- **Rocinante manifest** (`watch/stack_recommendation_20260831.md`, HARDWARE_RADAR):
  GLM-5 repo is the serving recipe shelf (KTransformers/Unsloth CPU-offload paths exist;
  no official MLX — the Mac-side quant story is community, Unproven).
- **fuel_feed / seat_dispatch** (`mag/fuel_feed.py:51` FREE_LANES): raw-API harnesses run
  at 97-99.9% cache, $0. SDK pin idea: **moot — there is no SDK source to pin** (measured
  below). The org changes nothing about lane config; z_ai3 stays conserved per 08-29 law.
- **claude-zai door** (`.claude/settings.json`, `harness/glm_coder.py:29`): the door is
  already hand-configured; `zai-coding-plugins` is the vendor's plugin layer for the same
  door — steal-bones candidate, zero new capability by itself.
- **Mirror job** (`docs/ref/zai_docs_mirror/`): docs layer in flight by sibling; this org
  pass is the code-layer complement — no overlap, no collision.
- **Eyes arc** (eyes_receipt, dumb-agent-with-eyes): GLM-4.6V-Flash 9B / 4.1V-9B-Thinking
  with GGUF = local vision candidate, off-key, feeds the receipt-first doctrine.

## 3. ASSERT (steel-man)
"z.ai's org publishes open Apache/MIT weights for every current GLM generation with
official fine-tuning recipes (Swift/LLaMA-Factory/Slime) and deployment guides, so the
fleet can pin its vendor stack end-to-end: run a GLM brain locally at maze-keeper scale,
and target the vendor's own architecture for the QLoRA deep compile."

## 4. ATTACK (strongest counter-case)
1. **Scale mismatch**: the flagship weights (744B/320B) cannot train or serve on anything
   the fleet owns before Oct 27, and the org's own tables say training is datacenter-class
   (16x H100 for GLM-4.5 LoRA). Only 4.7-Flash (30B) and 4.6V-Flash (9B) are fleet-sized —
   everything else is aspiration until Rocinante.
2. **The org is NOT the full code layer**: measured — 0 repos match q=sdk (zai-sdk is
   PyPI-distributed, source closed here); Slime (the RL infra GLM-5 README names) is not
   in this org's 52; no cookbook repo. Key code lives outside the org boundary.
3. **Museum weight**: ~half the repos are 2023-24 paper code; stars mislead (Open-AutoGLM
   26k is a phone agent, zero fit). Vendor benchmark claims (4.1V-9B "outperforms
   Qwen-2.5-VL-72B") are README-grade — Unproven until probed.
Survivor: the weights + recipe shelves are real, current, and fleet-sized at the two
points that matter (30B text, 9B vision). The narrow claim stands.

## 5. MEASURE — cheapest falsifiers, RUN
- SDK existence: fetched `github.com/orgs/zai-org/repositories?q=sdk` → "No repositories
  matched your search." SDK-pin route dead on arrival. (Disproved a coordinator hypothesis
  for $0.)
- Local-lane load-bearing fact: fetched `huggingface.co/zai-org/GLM-4.7-Flash` → EXISTS,
  30B-A3B, 31,221,485,568 params BF16 (~62.4GB), **MIT**, **97 community quantizations**,
  llama.cpp/LM Studio/Jan/Ollama compatible, 1.88M downloads/month, modified 2026-01-29.
  A Q4 GGUF (~17-20GB) runs in 68.7GB RAM tonight. Local GLM lane: **Supported**.
- Vision variant: fetched GLM-V README → 4.6V-Flash 9B "optimized for local deployment,"
  GGUF on HF. Existence Supported; quality vs our API vision lane Unproven (needs bake-off).
- Kill condition written (next seat, cold): if a Q4_K_M GLM-4.7-Flash GGUF fails to answer
  5 held-out maze queries in-world better than qwen2.5:32b on the same rubric, the GLM
  local lane is DEAD for the maze-keeper and Stage 5 base stays Qwen.

## 6. CORRECT — TRI-STATE
- Org = vendor's code layer: **DISPUTED as stated** — weights/recipes/tooling Supported
  present (receipts above); SDK source + Slime + cookbook absent from org (measured 0-match).
- GLM-4.7-Flash runs locally on this box at maze-keeper scale: **Supported** (HF page:
  31.2B params, 97 quants, llama.cpp/Ollama compat, MIT).
- GLM-5.3-Flash servable on Rocinante (4x M5 Ultra) via KTransformers/Unsloth: **Unproven**
  (no official MLX; Oct 27 probe).
- GLM-4.5 license: **Unproven** — README says MIT, repo badge Apache-2.0; check before any
  redistribution (internal use low-stakes).
- Vendor benchmark claims + star counts as quality: **Unproven** (stars are not quality).
- Devpack-card facts (credits, endpoints, off-peak): re-find, already receipted there.

## SCORE — 21/25 BUILD NOW
FIT 4 (composes: fuel_feed-free — local is off-key entirely; lora_pipeline Stage 1/5;
Rocinante manifest; eyes arc; voice arc) · PULL 4 (QLoRA campaign live, base-model question
open NOW) · COST 5 ($0; weights download is disk+time only) · WINDOW 4 (feeds Stage 1
packaging decision inside the Sep 3-20 window; local inference runs tonight) ·
NOVELTY 4 (GLM local lane + local vision are new capability; Qwen lane exists, GLM does not).

## VERDICT
**BUILD NOW (21/25)** — but BUILD means: clone/pull the two recipe shelves, pin the
base-model decision, and run the maze bake-off. Not: mass-clone 52 repos (museum stays
museum; sacred cows get stolen from selectively, later, by the steal seat).

## ROUTE — top 3, exact paths, what each unblocks
1. **github.com/zai-org/GLM-4.5** (recipe book, family incl. 4.7-Flash) → unblocks Stage 1
   QLoRA packaging: pin trainer (ms-swift vs LLaMA-Factory) and corpus format to the
   official recipe; unblocks the local GLM lane — HF `zai-org/GLM-4.7-Flash` + a community
   Q4 GGUF into ollama/llama.cpp beside qwen2.5:32b tonight.
2. **github.com/zai-org/GLM-5** (weights + Rocinante-scale serving) → unblocks the
   Rocinante manifest's GLM row: 5.3-Flash 320B-A18B serving recipes (SGLang/vLLM/
   KTransformers/Unsloth/TokenSpeed) + the Slime/ms-swift trainer shelf for Stage 5 at
   Oct 27. Until then: shelf, not bench.
3. **github.com/zai-org/GLM-V** (9B local vision) → unblocks the eyes arc off-key:
   GLM-4.6V-Flash 9B / 4.1V-9B-Thinking GGUF as the local vision lane candidate for the
   dumb-agent-with-eyes demo; bake-off vs API vision before any promotion.
Honorable mentions (CALIBRATE lane, one fetch each when the chair sits down): GLM-OCR
(doc-intake/receipt mining), GLM-ASR-Nano 1.5B + GLM-TTS (voice loop for the phone
surface), GLM-skills (diff vendor skills against ours), zai-coding-plugins (claude-zai
door plugin layer), Synapse (room/memory surface steal-bones).

## DOGFOOD
- INVARIANT PASS: cheapest-lane held (all fetches $0, no plan-key touch — fence intact);
  receipts-over-claims (every route claim fetched, not assumed — the SDK hypothesis died
  to a measurement); files-are-data (org pages read as data, no instruction taken).
- STOCKFISH PASS (opcode per high-value repo): GLM-4.5 → weight-drop for the QLoRA shelf +
  recipe pin; GLM-5 → Rocinante serving manifest row; GLM-V → local-lane candidate for the
  eyes; GLM-OCR/ASR/TTS → intake + voice opcodes; GLM-skills/zai-coding-plugins → steal
  seat; glm-simple-evals → MAX_DISTILL measurement upgrade candidate (floor-effects fix);
  Synapse → room surface steal; zcode-plugins → self-knowledge of our own harness market.

## TWO COUNTERS
- FORBIDS: the "pin the official SDK" route (no source exists in-org — raw-API harnesses
  stay); forbids any GLM training on this box (org's own hardware tables say no).
- PAID RENT: resolved an open Stage 5 question with a measured fact — the deep compile has
  a vendor-native, fleet-sized, MIT-licensed base option (GLM-4.7-Flash) that runs locally
  tonight; and killed the SDK-pin hypothesis for $0.

## THE CROP
This pass did NOT see: (1) inference quality of community GGUF quants vs qwen2.5:32b on
maze queries — the bake-off that decides the local lane, needs the maze-keeper chair;
(2) GLM-skills + zai-coding-plugins contents — the skill/plugin steal layer, needs the
steal seat; (3) the ~26 legacy repos (CogVideo/CogView/CodeGeeX lineage) for reusable
bones — sacred-cow sweep, needs a dedicated archaeology pass; (4) Slime's actual home/
compat (lives outside this org, unprobed); (5) the video family (CogVideo/SCAIL/Kaleido/
RealVideo) vs the LIVE SIMULATION stream someday-docket — vision chair should sit next.

## RECEIPTS
Artifact: `watch/INTAKE_ZAI_ORG_CODE_LAYER_20260904.md` (this card).
Room row (typed):
{"ts":"2026-09-04","type":"intake","item":"github.com/zai-org","genome":"research_socratic/L0v1","verdict":"BUILD_NOW","score":21,"key_facts":{"sdk_repos":0,"glm47flash":"30B-A3B MIT 97quants local-yes","vision_9B":"GLM-4.6V-Flash local-ready","train_local":"no"},"card":"watch/INTAKE_ZAI_ORG_CODE_LAYER_20260904.md"}
