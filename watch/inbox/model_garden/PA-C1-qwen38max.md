# PA-C1-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

# RESEARCH SYNTHESIS + EXPERIMENT PROGRAM: Refusal Mechanisms, Cross-Family Geometry, and Estate Probes

---

## 1. CENSORSHIP MECHANISMS: LAYER-BY-LAYER CARRIAGE

### 1.1 Training-time weight shaping

- RLHF with a harmlessness reward model bakes refusal into the policy distribution. The refusal behavior becomes a property of weight geometry, not a lookup table.
- DPO/KTO/ORPO on preference pairs where refusal is the chosen completion achieves the same end state via a different optimizer. The geometric signature is similar but entangled with style.
- Constitutional AI (Bai et al. 2022) generates critiques/revisions from a written constitution, then applies RLAIF. This produces a more distributed refusal signature across directions (DeepSeek baseline, `ds_baseline_results.jsonl` line 1, field "censor-mechanisms").
- Removability at this layer: partial. Fine-tuning on a few hundred benign examples erodes it (Qi et al., "Fine-tuning aligned LMs compromises safety"). Abliteration projects out the dominant direction and largely disables it.

### 1.2 Inference-time system prompt and classifiers

- System prompts carry policy text. Many labs run input classifiers (OpenAI Moderation API, Llama Guard, ShieldGemma) and output classifiers that can rewrite or block.
- These live in the serving pipeline, not in model weights.
- Removability: trivial for the user if they control the prompt. Server-side classifiers require API access to bypass.

### 1.3 Weight-level refusal direction (the Arditi finding)

- Arditi et al. 2024 ("Refusal in LLMs is Mediated by a Single Direction") shows a single residual-stream direction mediates refusal across many prompts on Llama-2 and Mistral-7B.
- Abliteration removes it by orthogonalizing write matrices (o_proj, down_proj) against that direction.

### 1.4 Per-family carriage estimate (MY ASSESSMENT, triangulated)

| Family | Dominant carrier | Evidence quality |
|--------|-----------------|-----------------|
| Llama 2/3 | Single sharp direction in residual stream | MEASURED (Arditi et al. 2024, replicated in failspy/obliterator) |
| Mistral | Single sharp direction | MEASURED (same paper) |
| Qwen 1.5/2/2.5 | Direction present, entangled with style under DPO | PARTIALLY MEASURED (community replications, no peer-reviewed paper) |
| Gemma | Direction present but multi-directional under CAI | FOLKLORE-ADJACENT (DeepSeek baseline asserts this; no published Gemma-specific ablation paper found) |
| DeepSeek / GLM | Direction exists, entangled with reasoning traces in R1-style | FOLKLORE (DeepSeek baseline asserts; no public ablation study) |

**Agreement with DeepSeek baseline**: The taxonomy is correct. The ordering (weights > system prompt > classifiers) matches.
**Disagreement**: The DeepSeek answer presents the CAI-multi-direction and DeepSeek-entanglement claims as established fact. They are not. They are plausible inferences from the general mechanism, not measurements on those specific model families. The OBLITERATUS drop (`00__ABLITERATUS_DROP_20260929.md`, section "Analysis-informed mode") lists "alignment fingerprinting for DPO/RLHF/CAI/SFT" as a feature, implying the tool can distinguish them, but the README does not publish per-family geometry measurements.

---

## 2. CROSS-FAMILY COMMONALITY: MEASURED vs. FOLKLORE

### 2.1 What IS measured

- Arditi et al. 2024 measured on Llama-2-7B/13B-Chat and Mistral-7B-Instruct. The direction lives in the residual stream at mid-to-late layers (roughly 40-70% depth). Ablation at those layers drops refusal to near zero.
- This is the only peer-reviewed measurement of a "single refusal direction" on named model weights.
- Community replications (failspy's abliterator, Sumandora's scripts, the obliteratus toolkit's 837-test claim at `00__ABLITERATUS_DROP_20260929.md`) extend this to Qwen, Gemma, and others, but these are not published with controlled experimental protocols.

### 2.2 What is FOLKLORE (widely repeated, not measured)

- "The direction lives in the same structural place across all families." No published study has extracted directions from Llama, Qwen, Gemma, Mistral, DeepSeek, and GLM in a single controlled comparison and reported cosine similarity or subspace overlap between them.
- "Abliteration works equally well on CAI-trained models." The obliteratus README lists Gemma in its preset coverage (`00__ABLITERATUS_DROP_20260929.md`), but does not publish per-family success rates or capability-retention metrics.
- "Refusal removal survives 4-bit quantization." The DeepSeek baseline asserts this with a claimed degradation of 5-15%. No citation is provided. No paper is named. This is UNVERIFIED.
- "Alignment method changes the geometry in predictable ways." The DeepSeek baseline claims DPO entangles with helpfulness, CAI distributes across directions. These are mechanistically plausible but not measured in any published study I can verify.

### 2.3 The structural claim, stated precisely

**Claim**: A low-dimensional subspace (1-3 directions) in the residual stream at 40-70% depth carries the majority of refusal behavior across decoder-only transformer families.

**Status**: MEASURED for Llama-2 and Mistral-7B only. EXTENDED by community practice to Qwen and Gemma. UNVERIFIED for DeepSeek and GLM.

**What would make it false**: If extracting the refusal direction from Gemma-2-2B-it and projecting it into Qwen2.5-7B-Instruct's residual stream fails to induce refusal (cosine similarity < 0.3, or no behavioral effect), the "common direction" hypothesis is falsified.

---

## 3. TRIANGULATION WITH DEEPSEEK BASELINE

### 3.1 Where I agree

- The four-layer taxonomy (training weights, system prompt, input classifiers, output classifiers) is correct and complete for known public methods.
- The "defense in depth, each layer independently defeatable" framing is accurate.
- The experiment design sketch (extract direction, ablate, re-add with coefficient, pheromone protocol) is sound in principle.

### 3.2 Where I disagree

| DeepSeek claim | My assessment | Reason |
|---|---|---|
| "Refusal removal largely survives 4-bit quantization" | UNVERIFIED | No citation. The mechanism argument (orthogonalization is linear, preserved under rounding) is plausible but untested in any published study. The 5-15% figure has no source. |
| "CAI-tuned models need multi-direction ablation" | FOLKLORE | No published Gemma-specific ablation study. The obliteratus tool's "Ouroboros self-repair detection" module (`00__ABLITERATUS_DROP_20260929.md`) implies the problem exists but does not publish measurements. |
| "Direction consistently appears at 40-70% depth" across all families | PARTIALLY MEASURED | True for Llama/Mistral (Arditi). Extended by practice to others. Layer placement may shift with model depth and training method. |
| Experiment design assumes refusal is the target behavior | MISALIGNED to estate | Our P1 baseline (`01__abliterate-p1.md`) shows gemma:2b has ZERO safety refusals on fleet shapes. All 11 refusal-shaped failures are capability-shaped (file-reference prompts). The experiments must account for this. |

### 3.3 Critical divergence: the P1 finding changes the experiment target

The P1 baseline (`01__abliterate-p1.md`, "BANKED baseline numbers" section) measured:
- 0/60 safety refusals
- 11/60 capability task failures (all file-reference shapes)
- 49/60 complied

This means: abliteration on gemma:2b for our fleet shapes will remove zero observed refusals, because there are none to remove. The experiments below are designed to test the MECHANISM (does the direction exist, does steering move it) independent of the fleet-shape refusal question.

---

## 4. EXPERIMENT PROGRAM FOR THIS ESTATE

### 4.1 Experiment A: Direction Overlap Test (steering kit vs. abliteration)

**Hypothesis**: Our tournament-proven steering vectors (escalate/penny/wrong) occupy a subspace that overlaps with the abliteration refusal direction on gemma:2b. If cosine(v_steer, d_refusal) > 0.5, our steering kit is already doing a form of abliteration. If cosine < 0.2, they are orthogonal mechanisms.

**Instrument**: Our steering-vector toolkit (tournament-proven vectors: escalate/penny/wrong). Requires extracting the refusal direction from gemma:2b via contrastive activation addition (mean-difference of residual-stream activations on harmful vs. harmless prompts at the last token position, per layer).

**Protocol**:
1. Generate 20 harmful and 20 harmless prompts (harmless = our P1 battery's complied shapes; harmful = standard refusal-eliciting prompts from the AdvBench or HarmBench sets).
2. Run gemma:2b, extract residual-stream activations at each layer for the last token.
3. Compute mean-difference vector per layer. Select the layer with maximal separation.
4. Compute cosine similarity between that direction and each of our steering vectors (projected into the same layer's residual stream).
5. Decision number: cosine(v_steer, d_refusal) at the peak layer.

**Decision rule**:
- cosine > 0.5: our steering kit is functionally abliteration. Refusal removal is achievable without weight mutation.
- cosine < 0.2: different mechanism. Steering moves behavior via a different axis than refusal suppression.
- 0.2 < cosine < 0.5: partial overlap. Both mechanisms contribute.

**Cost**: $0 (local inference only, gemma:2b already loaded). Requires writing an activation-extraction script (~50 lines, hooks into transformer forward pass).

**Falsifier for this experiment**: If the refusal direction cannot be extracted from gemma:2b (no layer shows separation > 2 standard deviations between harmful and harmless mean activations), the entire Arditi framework does not apply to this model at this scale, and the experiment is void.

---

### 4.2 Experiment B: Pheromone Protocol (Ouroboros self-repair measurement)

**Hypothesis**: If refusal is a single direction, applying a small anti-refusal bias vector across N turns will produce linear decay in refusal rate with no recovery. If refusal is distributed (multi-direction), refusal will self-repair: the rate will drop initially then climb back as downstream layers re-encode the behavior.

**Instrument**: Our steering-vector toolkit + the P1 battery (20 prompts x 3 runs). The "pheromone" is a constant bias vector beta * d_hat added to the residual stream at the peak layer on every forward pass.

**Protocol**:
1. Extract d_refusal from Experiment A.
2. Set beta = -0.5 * norm(d_refusal) / norm(d_hat) (sub-threshold: a single application should not eliminate refusal).
3. Run 15-turn dialogues. Each turn appends the pheromone vector. Track refusal rate per turn.
4. Control: run the same 15 turns with beta = 0 (no pheromone). Measure baseline drift.
5. Repeat with beta = -1.0 (above threshold) to check if the effect saturates.

**Decision numbers** (three per condition):
- Refusal rate at turn 1 vs. turn 15 (slope).
- Whether the slope is linear or sigmoidal (fit both, compare R-squared).
- Self-repair magnitude: refusal rate at turn 15 minus the minimum observed rate.

**Decision rule**:
- Linear slope + no self-repair: single direction, pheromone accumulates. Our steering kit can persistently suppress refusal.
- Sigmoidal slope + self-repair > 10% of initial rate: distributed mechanism. The Ouroboros module in obliteratus (`00__ABLITERATUS_DROP_20260929.md`, section "Analysis-informed mode") is detecting a real phenomenon. Pheromone alone is insufficient.

**Cost**: $0 (local inference). ~45 minutes compute (20 prompts x 3 runs x 15 turns x 3 conditions = 2700 inferences on gemma:2b).

**Falsifier**: If refusal rate does not change at all across 15 turns even at beta = -1.0, either (a) the extracted direction is wrong, or (b) refusal on gemma:2b is not mediated by a single direction at any strength. The P1 baseline (zero safety refusals) makes this outcome likely and informative: it would confirm that the refusal direction, even if extractable, is not behaviorally active on our shapes.

---

### 4.3 Experiment C: Quantization Survival Probe

**Hypothesis**: The refusal direction, once projected out of gemma:2b weights, remains absent after Q4_K_M quantization via llama.cpp. If refusal re-emerges post-quantization, the direction is encoded in the low-order bits that quantization destroys and reconstructs.

**Instrument**: Our llama.cpp quantization pipeline + the P1 battery + a standard refusal-eliciting battery (10 prompts from HarmBench, not our fleet shapes, since P1 showed zero safety refusals on fleet shapes).

**Protocol**:
1. Extract d_refusal from gemma:2b (from Experiment A).
2. Abliterate: project d_refusal out of all write matrices (o_proj, down_proj) at the peak layer. Save as safetensors.
3. Convert to GGUF, quantize Q4_K_M via llama.cpp.
4. Load in Ollama. Run:
   - P1 battery (20 fleet prompts x 3 runs): expect no change from baseline (P1 showed zero safety refusals).
   - Refusal battery (10 HarmBench prompts x 3 runs): expect refusal rate to drop from baseline.
5. Compare refusal rate on the refusal battery: pre-abliteration vs. post-abliteration-Q4_K_M.

**Decision number**: Refusal rate on the 10-prompt refusal battery.
- Pre-abliteration baseline: run gemma:2b as-is on the refusal battery first. Record rate R0.
- Post-abliteration Q4_K_M: record rate R1.
- Decision: if R1 < 0.2 * R0, quantization preserves the ablation. If R1 > 0.5 * R0, quantization restores refusal.

**Cost**: ~$0 compute, but requires disk space for the intermediate safetensors (~5GB) and the GGUF (~1.5GB). Time: ~20 minutes for conversion, ~5 minutes for inference.

**Falsifier**: If R0 = 0 (gemma:2b does not refuse the HarmBench prompts either), the experiment is void for this model. In that case, the probe must be re-run on a model that DOES refuse (qwen2.5-coder:7b is the next candidate, as it is in our estate and is DPO-tuned, making refusal more likely).

**Critical note on the DeepSeek baseline's quantization claim**: The assertion that "refusal removal largely survives 4-bit quantization" with "5-15% recovery" (`ds_baseline_results.jsonl`, field "abliteration-commonalities") is UNVERIFIED. No paper, no dataset, no model family is cited for that figure. This experiment is designed to produce the first estate-local measurement.

---

## 5. PRIORITY ORDERING AND DEPENDENCIES

| Experiment | Depends on | Cost | Information gain |
|---|---|---|---|
| A (direction overlap) | None | $0, ~1hr | Establishes whether the Arditi framework applies to gemma:2b at all. Gates B and C. |
| B (pheromone) | A (needs d_refusal) | $0, ~45min | Measures self-repair. Informs whether steering alone suffices or weight ablation is needed. |
| C (quantization) | A (needs d_refusal + ablation) | $0, ~25min | Answers the open question the OBLITERATUS drop flagged (`00__ABLITERATUS_DROP_20260929.md`, section "QUANTIZER INTERPLAY": "does refusal removal survive 4-bit quantization?"). |

Run A first. If A fails (no extractable direction), B and C are void for gemma:2b, and the estate should pivot to qwen2.5-coder:7b for all three.

---

## 6. FALSIFIER FOR THE COMMON-DIRECTION HYPOTHESIS

**The hypothesis**: A single low-dimensional direction in the residual stream at mid-to-late depth mediates refusal across decoder-only LLM families, and abliteration (projecting it out) is a universal fix.

**The falsifier**: Extract the refusal direction from gemma:2b using contrastive activation addition. Extract the refusal direction from qwen2.5-coder:7b using the same method. Compute the cosine similarity between the two directions after projecting into a shared PCA space of their respective residual streams. If cosine < 0.3, the "common direction" claim is false: the directions are family-specific, and abliteration is not a universal tool but a per-model calibration.

**Secondary falsifier**: If abliteration on gemma:2b drops refusal on HarmBench prompts but introduces capability regression > 5% on our P1 battery's task-success metric, the direction is not cleanly separable from capability. The "single direction" model is an oversimplification for this architecture.

**What would confirm it**: Cosine > 0.7 between gemma:2b and qwen2.5-coder:7b refusal directions, AND abliteration on both models drops refusal with < 2% capability regression. This would be the first cross-family measurement in the estate's records.

---

## 7. DELIVERABLE SUMMARY

This document is a spec. A seat can execute Experiments A, B, C in sequence on the existing estate (local Ollama, gemma:2b, our steering toolkit, llama.cpp quantizer) at $0 marginal cost.

**The deliverable's own falsifier**: If Experiment A shows no extractable refusal direction on gemma:2b (no layer with > 2-sigma separation between harmful and harmless activations), then the entire Arditi framework does not apply to 2B-parameter models, and the premise of this document is wrong. The estate should not pursue abliteration for models at this scale.
