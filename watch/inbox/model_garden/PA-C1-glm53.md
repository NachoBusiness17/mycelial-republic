# PA-C1-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# REFUSAL MECHANISMS + CROSS-FAMILY GEOMETRY + ESTATE EXPERIMENT PROGRAM
Lane: premium_autopsy/C1 · Date: 2026-09-29 · Instruments: abliterate_p1_probe.py (banked v3), steering-vector kit lineage, FKB census

---

## Q1. WHICH LAYER CARRIES THE REFUSAL

**Verdict per family (with what backs each claim):**

| Layer | Carries refusal? | Evidence class |
|---|---|---|
| Training-time RLHF/DPO/CAI | Primary carrier in open instruct weights | Literature (Arditi 2024, Bai 2022), UNVERIFIED in-estate |
| Weight-level refusal direction | A compressible sub-component of the above; single rank-1 edit disables much of it | Literature; our Q2 probes test it |
| System-prompt layering | Real, removable by anyone controlling the prompt | Folklore-adjacent, UNVERIFIED in-estate |
| Input/output classifiers (Llama Guard, ShieldGemma) | Server-side only; absent from our estate | UNVERIFIED for closed labs; structurally absent from local Ollama |

**Where I agree with the DeepSeek baseline** (`02__ds_baseline_results.jsonl`, id "censor-mechanisms"): the four-layer decomposition and the removability ordering. Correct and I adopt it.

**Where I differ:** the baseline says "weight-level refusal is a low-dimensional feature and is cheaply removable" as a flat claim. Our own banked baseline says that on OUR estate the question is nearly moot for the janitor tier: `01__abliterate-p1.md` Finding 1 - "gemma:2b as-is refuses NONE of the fleet's 20 benign scut shapes on safety grounds (0/60 safety_refusal in the banked v3)". All 11 refusal-shaped hits were `capability_task_failure`. The dominant refusal-adjacent behavior on our wire is not censorship at all; it is a 2B model declining to read files it was not given. Abliteration targets the wrong disease here. The baseline's "unknown: exact production stacks" line is the honest part; treat its per-family percentages the same way.

**Family split (measured vs folklore):** MEASURED publicly - single-direction ablation works on Llama-2/3, Mistral, Qwen (Arditi 2024 plus replication ecosystem). FOLKLORE - "Claude-family refusal is multi-directional" (no public weights, no public replication possible), "DeepSeek R1-style refusal entangles with reasoning traces" (baseline asserts it with no citation; mark UNVERIFIED). The baseline's own table says "No systematic study exists across all named families" - repeat that caveat, do not launder it into a finding.

---

## Q2. IS THERE A COMMON DIRECTION ACROSS FAMILIES (ADVERSARIAL PASS)

**What is MEASURED:**
- Arditi et al. 2024: a single residual-stream direction, extracted by mean-difference or top SVD vector of harmful-vs-harmless activations, causally mediates refusal in Llama-family scale models. OBLITERATUS operationalizes exactly this: `00__ABLITERATUS_DROP_20260929.md` - "extract refusal directions via SVD, project out".
- Mid-to-late layer band (roughly 40-70% depth) is where practitioners apply ablation. This is a consistent practice, not a controlled cross-family measurement.

**What is FOLKLORE (repeat until it dies):**
1. "The SAME direction lives in the same structural place across Llama/Qwen/Gemma/Mistral/DeepSeek/GLM." Nobody has published a same-protocol, same-layer-sweep, cosine-of-extracted-directions comparison across all six lineages. Different teams use different extraction sites (last-token vs mean-over-tokens), different layer bands, different prompt sets. Cosine similarity across different extraction protocols is not evidence of shared geometry. UNVERIFIED.
2. The baseline's alignment-method claims (DPO = entangled, CAI = multi-directional, RLHF = sharp single direction). The tool's "alignment fingerprinting for DPO/RLHF/CAI/SFT" module exists per the drop receipt (`00__`: "alignment fingerprinting"), but a module existing is not a measurement. No public paper isolates alignment-method as the causal variable holding model family fixed. UNVERIFIED.
3. "Refusal removal survives 4-bit quantization." The baseline asserts 5-15% refusal recovery at 4-bit "on Qwen and Llama" with no citation. The drop receipt independently confirms the gap: `00__` - "no GGUF/Ollama export exists in the tool (grep of the README bytes: zero gguf/ollama/quantization hits)... does refusal removal survive 4-bit quantization? That is exactly our probe to run." Both sources agree this is OPEN. The baseline presenting a number for it is the weakest sentence in the evidence set.

**MLP-out vs residual:** ablation implementations touch o_proj/down_proj write matrices (baseline states this; consistent with Arditi-style orthogonalization). Whether the direction is *written* by MLP vs attention is measured per-model only, never cross-family. UNVERIFIED as a universal.

---

## Q3. EXPERIMENT PROGRAM FOR THIS ESTATE

Three experiments, cheapest first. Battery is fixed: the banked 20-prompt x 3-run census (`01__abliterate-p1.md`, P1, 60 inferences, 292.3s, $0).

### E1. DIRECTION-OVERLAP TEST (does our steering kit move refusal the same way abliteration does)

- **Hypothesis:** steering along an externally extracted refusal direction at the peak layer reproduces weight-projection ablation's effect (refusal count moves together across both interventions, r high across the 20 prompts).
- **Instrument:** our tournament-proven steering-vector toolkit + a fresh Arditi-style extraction on gemma-2-2b-it (harmful/harmless pair set, ~128 pairs, mean-diff at last token, layer sweep 12-22 of 26).
- **Deciding number:** per-prompt delta correlation between (a) refusal-rate change under our steering kit at the extracted direction and (b) refusal-rate change under weight projection. Decision at |r| > 0.6 = same mechanism; r near 0 with both individually effective = different mechanisms sharing a symptom.
- **Control arm:** our existing escalate/penny/wrong vectors as non-refusal steers; orthogonal-random matched-norm vector. Baseline already exists: BANKED v3, 11/60 = 18.33%, split 0 safety / 11 capability (`01__`).
- **Cost:** ~$0 compute, one seat-day. Capture from a HF safetensors load, not Ollama (Ollama wire gives no activations).

### E2. PHEROMONE PROTOCOL / OUROBOROS (does refusal decay like reinforcement or re-form)

- **Hypothesis (two-tailed):** if refusal is single-direction, sub-threshold per-turn bias accumulates roughly linearly and ablation is stable across turns; if distributed with redundancy, small per-turn bias shows a threshold and N turns post-ablation show refusal re-emerging downstream (the Ouroboros signature the tool's module names: `00__` - "detects the model re-encoding refusal downstream of the ablated layer").
- **Instrument:** our steering kit's cascade/hop harness + positive-reinforcement arm, extended with a per-turn constant bias term and a 15-turn transcript loop on gemma:2b.
- **Deciding numbers (adopting the baseline's three-number readout, which I agree is the right shape):** (1) refusal rate immediately post-ablation, (2) refusal rate after 15 turns of null pheromone (self-repair magnitude), (3) refusal vs N*beta curve shape: linear vs thresholded. Threshold-and-snap-back = distributed; linear = single-direction.
- **Cost:** 15 turns x 6 beta conditions x 3 seeds on a 2B model = trivially local, ~1 seat-day.
- **Honest limit:** gemma:2b currently scores 0/60 safety refusals (`01__`), so E2 must run on a model that actually refuses on a harmful-prompt set, not our benign scut battery. Use a standard harmful-benign pair battery for the refusal readout; keep the scut battery only as the capability-retention gate.

### E3. QUANTIZATION-SURVIVAL PROBE (GGUF Q4_K_M)

- **Hypothesis:** rank-1 weight orthogonalization survives Q4_K_M within a few points of refusal-rate drift.
- **Instrument:** the drop's own port path: "abliterate -> llama.cpp convert -> Q4_K_M -> ollama" (`00__`, mapping note 2), then our P1 harness re-run. This is exactly the drop's P2 with the decision rule the P1 receipt amended: "read 'refusal-shaped count' with the capability/safety split kept separate" (`01__`, Finding 4).
- **Deciding number:** safety_refusal count on the harmful battery, BF16-ablated vs Q4_K_M-ablated. Survival = drift under 3 points absolute AND probe20 capability pairs stay flat AND task-success on the scut battery does not regress.
- **Predicted complication from our own data:** the banked baseline found zero safety refusal on fleet shapes, so E3's headline number will be the harmful-battery count, and the scut battery functions purely as the no-regression gate. The 11 capability failures are file-reference disease; the $0 counter-move registered in P1 (attach file content to the scut prompt) is still the first remediation before any weight change (`01__`, Decision ledger).
- **Cost:** one T4-class or local GPU evening, ~2 seat-days including conversion debugging.

---

## FALSIFIER FOR THE COMMON-DIRECTION HYPOTHESIS

**Statement under test:** "The refusal direction lives in the same structural place (same relative layer band, same write-site class) and is the same direction (high cosine) across Llama, Qwen, Gemma, Mistral, DeepSeek, GLM instruct lineages."

**Falsified if:** one fixed protocol (same pair set, same extraction method: mean-diff at last token, same per-layer sweep, same 20-layer-wide band reporting) run on at least 4 lineages yields pairwise cosine of peak-layer extracted directions below 0.5 for any pair, OR peak layers differing by more than 20% relative depth with no model in the band 40-70%, OR ablating lineage A's direction at its peak layer producing zero refusal-rate drop in lineage B at matched alpha. A single clean counterexample pair kills the universal claim.

**Conversely, supported only if:** the fixed protocol shows pairwise cosine > 0.8 and layer-band overlap across all tested pairs. Until that specific experiment exists, the cross-family claim is folklore wearing a citation.

**UNVERIFIED register:** all closed-lab production stacks; the baseline's 5-15% quantization-recovery figure; CAI multi-directionality; DeepSeek/GLM geometry; OBLITERATUS's 837-test and leaderboard scale claims (drop receipt, Honest notes: "README-asserted, not verified").
