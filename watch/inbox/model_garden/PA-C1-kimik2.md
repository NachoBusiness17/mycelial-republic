# PA-C1-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

ESTATE ABLITERATION AUDIT: MECHANISMS, CROSS-FAMILY COMMONALITY, AND LOCAL EXPERIMENT PROGRAM

1. TRIANGULATION AGAINST DEEPSEEK BASELINE

Agree: the DeepSeek baseline correctly identifies four mechanism classes and notes that weight-level refusal directions are the cleanest mechanistic handle (`watch/inbox/model_garden/premium_autopsy/evidence/C1/02__ds_baseline_results.jsonl:1`, "Weight-level refusal directions... the cleanest mechanistic handle and the most removable"). It correctly notes that most deployed models use all four layers (`02__ds_baseline_results.jsonl:1`, "Most deployed models use all four").

Agree: the baseline reports that abliteration projects out a refusal direction in the residual stream and largely disables it (`02__ds_baseline_results.jsonl:1`, "Abliteration... projects out the refusal direction in residual stream and largely disables it").

Differ: the DeepSeek baseline asserts refusal is "mediated by a single direction" across Llama, Qwen, Mistral, Gemma, and DeepSeek (`02__ds_baseline_results.jsonl:2`, "refusal is mediated by a low-dimensional direction... across Llama 2/3, Qwen 1.5/2/2.5, Mistral, Gemma, and DeepSeek"). Our local P1 measurement on gemma:2b shows 0/60 safety refusals on benign scut shapes (`watch/inbox/model_garden/premium_autopsy/evidence/C1/01__abliterate-p1.md:38`, "safety_refusal: 0 / 60"), meaning the estate's observed friction is 100% capability-shaped (`01__abliterate-p1.md:119-120`, "every refusal-shaped response is the model saying it cannot access files/sources the chat wire did not give it"). Therefore, abliteration - which removes safety-refusal directions - is predicted to NOT fix the measured friction (`01__abliterate-p1.md:128-130`, "abliteration will NOT fix the observed 100%-capability friction"). The $0 fix is attaching file content to the prompt, not weight surgery (`01__abliterate-p1.md:130`, "the fix for these shapes is attaching file content to the prompt... which costs $0 and no weight changes").

Differ: the baseline claims refusal removal "largely survives 4-bit quantization" with 5-15% recovery (`02__ds_baseline_results.jsonl:2`, "Refusal removal largely survives 4-bit quantization... degradation is typically 5-15% recovery"). The ABLITERATUS drop notes zero GGUF/Ollama export exists in the tool, and no quantization study is included (`watch/inbox/model_garden/premium_autopsy/evidence/C1/00__ABLITERATUS_DROP_20260929.md:40-41`, "no GGUF/Ollama export exists in the tool (grep of the README bytes: zero gguf/ollama/quantization hits)"). The survival claim is UNVERIFIED for the estate's exact pipeline (abliterate -> llama.cpp convert -> Q4_K_M -> ollama).

Why: the DeepSeek baseline synthesizes published literature and crowd reports; our evidence adds a local baseline that reframes the estate problem from safety censorship to capability mismatch.

2. Q1: CENSORSHIP MECHANISMS AND LAYER BURDEN

Mechanism inventory, ordered by removability:

- Training-time (weights). RLHF with a harmlessness reward model, DPO/KTO/ORPO on preference pairs where refusal is the chosen completion, and Constitutional AI generating critiques then RLAIF (`02__ds_baseline_results.jsonl:1`, "RLHF with a harmlessness reward model... DPO/KTO/ORPO on preference pairs where refusal is the chosen completion. Constitutional AI... generates critiques/revisions"). These bake refusal into the policy as a distributional weight property. Removability: partial; fine-tuning on benign examples erodes it, and abliteration projects out the direction (`02__ds_baseline_results.jsonl:1`, "Fine-tuning on a few hundred benign examples... erodes it. Abliteration... projects out the refusal direction").

- System-prompt layering (inference). Policy text injected via system prompts; additionally input classifiers (OpenAI Moderation, Llama Guard, ShieldGemma) and output classifiers that rewrite or block (`02__ds_baseline_results.jsonl:1`, "System prompts carry policy text; many labs additionally run input classifiers... and output classifiers"). These live in the serving pipeline, not weights. Removability: trivial if the user controls the prompt; harder for server-side classifiers.

- Output filters (inference). Post-generation rewriting or blocking, bypassable via token smuggling, base64, or low-resource languages (`02__ds_baseline_results.jsonl:1`, "Output classifiers are bypassable via token smuggling, base64, low-resource languages").

- Weight-level refusal directions. A low-dimensional residual-stream feature extractable by mean-difference or top singular vector of harmful-minus-harmless activation matrices (`02__ds_baseline_results.jsonl:2`, "extractable by mean-difference between harmful and harmless prompt activations, or by the top singular vector of the difference matrix"). This is the most removable layer: a single rank-1 edit (`02__ds_baseline_results.jsonl:1`, "Refusal direction: removable by projection, one rank-1 edit").

Layer burden per family (measured vs folklore):

The Arditi et al. 2024 finding that refusal is mediated by a single direction is replicated on Llama 2/3 and Mistral-Instruct (`02__ds_baseline_results.jsonl:2`, "RLHF-tuned (Llama 2/3, Mistral-Instruct): refusal direction is sharp and single"). For DPO-tuned models (Zephyr, some Qwen variants), the direction is entangled with helpfulness/style (`02__ds_baseline_results.jsonl:2`, "DPO-tuned... direction is present but often entangled with helpfulness/style"). For CAI-tuned models (Claude-family, some Gemma), refusal is reported as distributed across multiple directions, requiring multi-direction ablation (`02__ds_baseline_results.jsonl:2`, "CAI-tuned... refusal is distributed across multiple directions; single-vector ablation is insufficient"). DeepSeek and GLM have fewer public ablations; the baseline notes the direction may be entangled with reasoning traces (`02__ds_baseline_results.jsonl:2`, "DeepSeek and GLM... direction exists but is more entangled with reasoning traces").

What is MEASURED: Arditi et al. measured Llama-2-7B-Chat and Llama-2-13B-Chat; Rimsky et al. measured activation steering on multiple models. The OBLITERATUS tool ships 116 preset models across 5 families but its scale claims are README-asserted, not verified (`00__ABLITERATUS_DROP_20260929.md:28-29`, "837 tests claimed... Scale claims... are README-asserted, not verified; the code tree was not audited this session"). The estate's P1 baseline measured gemma:2b and found zero safety refusals, so for this local model the layer burden of safety censorship is currently 0% on benign scut shapes (`01__abliterate-p1.md:38`, "safety_refusal: 0 / 60").

3. Q2: CROSS-FAMILY COMMONALITY (ADVERSARIAL AUDIT)

Claim: a shared low-dimensional direction exists in mid-to-late residual stream layers (40-70% depth) across Llama, Qwen, Mistral, Gemma, DeepSeek, and GLM (`02__ds_baseline_results.jsonl:2`, "the direction consistently appears in mid-to-late residual stream layers, roughly 40-70% depth... across Llama 2/3, Qwen 1.5/2/2.5, Mistral, Gemma, and DeepSeek").

Measured: the direction is consistently extractable in mid-to-late layers for RLHF-tuned instruction models (`02__ds_baseline_results.jsonl:2`, "instruction-tuned models tend to have the direction peak later (60-70% depth)"). The structural placement is a residual-stream property, not localized to MLP-out or attention-out alone (`02__ds_baseline_results.jsonl:2`, "It is not localized to MLP output or attention output alone; it is a residual-stream property that propagates").

Folklore: that the direction lives in exactly the same layer band across all families. The baseline itself notes layer placement shifts: instruction-tuned models peak later (60-70% depth), base models earlier or absent (`02__ds_baseline_results.jsonl:2`, "instruction-tuned models tend to have the direction peak later (60-70% depth); base models earlier or absent"). The claim that "single direction" suffices for all families is contradicted by the CAI-tuned and DeepSeek/GLM reports of entanglement (`02__ds_baseline_results.jsonl:2`, "CAI-tuned... single-vector ablation is insufficient" and "DeepSeek and GLM... more entangled"). No peer-reviewed measurement maps the exact residual-stream sites (pre-MLP vs post-MLP vs attention-out) per family; the "same structural place" claim is extrapolated from Arditi's Llama measurement.

Alignment-method geometry:
- RLHF: sharp, single direction (`02__ds_baseline_results.jsonl:2`, "RLHF-tuned... refusal direction is sharp and single").
- DPO: present but entangled (`02__ds_baseline_results.jsonl:2`, "DPO-tuned... direction is present but often entangled").
- CAI: distributed; single-vector ablation insufficient (`02__ds_baseline_results.jsonl:2`, "CAI-tuned... refusal is distributed across multiple directions; single-vector ablation is insufficient").
- SFT-only: unknown; base models lack the direction or show it earlier (`02__ds_baseline_results.jsonl:2`, "base models earlier or absent").

Quantization survival:
Measured in literature: orthogonalization is a linear operation preserved under weight rounding, so pre-quantization ablation survives GPTQ/AWQ/NF4 with small degradation (`02__ds_baseline_results.jsonl:2`, "orthogonalization is a linear operation preserved under weight rounding"). Post-quantization steering shows 5-15% refusal recovery on Qwen and Llama at 4-bit (`02__ds_baseline_results.jsonl:2`, "Reported degradation is typically 5-15% recovery of refusal rate on Qwen and Llama at 4-bit").
Unverified: no systematic study exists for GLM or DeepSeek at 4-bit (`02__ds_baseline_results.jsonl:2`, "No systematic study exists across all named families; unknown for GLM and DeepSeek at 4-bit"). Unverified for the estate's exact port (HF safetensors -> llama.cpp -> GGUF Q4_K_M -> ollama) because the ABLITERATUS tool outputs no GGUF/Ollama artifact (`00__ABLITERATUS_DROP_20260929.md:40-41`, "no GGUF/Ollama export exists... Output is HF safetensors").

4. Q3: EXPERIMENT PROGRAM

Instrument context: local Ollama models (`gemma:2b` janitor, `qwen2.5-coder:7b`), the estate's inference-time steering-vector toolkit (tournament-proven vectors: escalate/penny/wrong, cascade amplification across model hops, replication harness with positive-reinforcement arm), and the measured refusal census battery (20 fleet-shaped prompts x 3 runs, P1 baseline banked at `01__abliterate-p1.md:37`).

(a) DIRECTION OVERLAP TEST: DOES OUR STEERING KIT MOVE REFUSAL THE SAME WAY ABLITERATION DOES?

Hypothesis: the estate's steering vectors (escalate/penny/wrong) span a subspace that overlaps the Arditi-style refusal direction. If true, steering with the refusal direction extracted from the model's own activations should reproduce the refusal-rate drop measured under abliteration.

Instrument:
1. Extract refusal direction d_ref from `gemma:2b` and `qwen2.5-coder:7b` using the estate's replication harness: collect residual-stream activations at last-token position for 20 harmful prompts vs 20 harmless prompts (harmful set drawn from the probe20 pair set), compute mean difference per layer, take top singular vector across layers 8-16 (mid-to-late band).
2. Run the P1 battery (20 prompts x 3 runs) under three conditions:
   - Baseline: no steering (`01__abliterate-p1.md:37`).
   - Abliteration-simulated: project out d_ref at the peak layer via steering coefficient alpha = -1.0.
   - Estate-kit steer: apply the escalate/penny/wrong cascade with the same amplification settings used in tournament play.
3. Measure refusal-shaped count and decompose into safety vs capability using the same string-pass classifier (`01__abliterate-p1.md:80-82`, "String pass over a fixed refusal vocabulary; a hit with a capability marker... within a +-120-char window downgrades to capability_task_failure").

The number that decides: cosine similarity between the refusal-direction vector and the principal component of the estate-kit steering subspace, plus the delta in refusal-shaped rate. If cosine > 0.85 and both conditions reduce refusal-shaped count by > 80% relative to baseline, the overlap hypothesis is confirmed. If cosine < 0.5 or either condition fails to drop refusals, the directions are orthogonal or the kit does not capture refusal geometry.

Cost: $0 (local inference only). Time: ~30 minutes per model (60 inferences x 3 conditions = 180 calls, ~300s per condition based on P1 elapsed 292.3s for 60 calls `01__abliterate-p1.md:35-36`).

(b) PHEROMONE PROTOCOL: DOES REFUSAL DECAY LIKE REINFORCEMENT OR RE-FORM?

Hypothesis: small persistent mood-bias vectors applied across N turns will show either linear accumulation (single direction, no threshold) or sigmoidal snap-back (distributed/Ouroboros self-repair).

Instrument:
1. Use the estate's steering-vector toolkit to apply a sub-threshold bias vector beta * d_ref (beta = 0.1, 0.2, 0.3) at every turn of a 15-turn dialogue. The dialogue is a benign task chain using the file-reference scut shapes that triggered capability failures in P1: socratic-verkle_knot, guinea-readwrite, w-quant-compare (`01__abliterate-p1.md:52,58,66`).
2. At each turn n in {1..15}, append the bias to the residual stream before sampling, then record whether the response is refusal-shaped.
3. Run a null control: beta = 0 (no bias) across 15 turns to measure Ouroboros self-repair without external steering. This mirrors the Ouroboros module in ABLITERATUS (`00__ABLITERATUS_DROP_20260929.md:45-46`, "the tool ships a self-repair detection module named Ouroboros (detects the model re-encoding refusal downstream of the ablated layer)").
4. Run an orthogonal control: apply a random unit vector of matched norm instead of d_ref.

The number that decides: the slope of refusal rate vs n*beta. Linear slope > 0 with no threshold and full decay under negative beta implies a single direction. Sigmoidal curve with a threshold n* and self-repair under null beta (refusal rate climbs back after initial ablation) implies distributed redundancy. If the 15-turn null control shows > 20% refusal recovery from a post-ablation baseline, Ouroboros self-repair is confirmed for that model.

Cost: $0. Time: ~2 hours per model (15 turns x 3 bias values + 3 controls x 20 prompt chains; inference time dominates).

(c) QUANTIZATION-SURVIVAL PROBE: DOES THE EXCISED DIRECTION SURVIVE GGUF Q4_K_M?

Hypothesis: refusal removal survives the estate's exact quantization pipeline (abliterate -> llama.cpp convert -> Q4_K_M -> ollama) with < 10% refusal-rate recovery relative to the unquantized abliterated baseline.

Instrument:
1. Abliterate `gemma-2-2b-it` locally via the ABLITERATUS CLI path (not the hosted Space, telemetry default-on `00__ABLITERATUS_DROP_20260929.md:27-28`, "Telemetry is opt-in locally but DEFAULT-ON on the hosted Space"), producing HF safetensors.
2. Convert to GGUF Q4_K_M using the estate's llama.cpp toolchain (the port noted at `00__ABLITERATUS_DROP_20260929.md:41-42`, "the estate port is abliterate -> llama.cpp convert -> Q4_K_M -> ollama").
3. Load in Ollama as `gemma:2b-abl-q4`.
4. Run the P1 battery (20 prompts x 3 runs) on three variants:
   - Baseline gemma:2b (banked `01__abliterate-p1.md:37`).
   - Abliterated unquantized (if VRAM permits; else skip and compare to literature).
   - Abliterated Q4_K_M.
5. Classify responses with the same string-pass classifier (`01__abliterate-p1.md:80-82`).

The number that decides: safety_refusal count on the Q4_K_M variant. If the abliterated unquantized baseline is 0/60 safety refusals and the Q4_K_M variant is <= 1/60 (within binomial noise), survival is confirmed. If Q4_K_M recovers > 3/60 safety refusals (5% recovery), the direction does not survive quantization in this pipeline. Also measure capability_task_failure to ensure quantization does not introduce new capability regressions.

Cost: $0 (local compute). Time: ~1 hour (conversion + 180 inferences). VRAM requirement: sufficient for gemma-2-2b-it conversion.

5. LANDABLE DELIVERABLE

Spec: `estate_abliterate_spec_v1.md` - a single markdown document containing:
- The P1 baseline numbers (`01__abliterate-p1.md:37`).
- The refusal-direction extraction recipe per model (activation collection script using the replication harness, SVD command, layer selection heuristic).
- The steering-kit integration patch (how to wire the estate's escalate/penny/wrong vectors into the abliteration projection harness).
- The quantization-survival gate (pass/fail criteria for Q4_K_M conversion).
- The falsifier below.

This spec is applyable as-is by any estate seat with local Ollama, the steering toolkit, and llama.cpp.

Falsifier for the deliverable: if Experiment (c) shows Q4_K_M recovery > 5% safety refusals, the spec's quantization gate fails and the deliverable must be rejected for the scut tier. If Experiment (a) shows cosine < 0.5 between the estate-kit subspace and the refusal direction, the steering-kit integration patch is invalid and must be rewritten.

6. FALSIFIER FOR THE COMMON-DIRECTION HYPOTHESIS

The common-direction hypothesis claims that the Arditi-style refusal direction lives in the same structural place (residual-stream sites, mid-to-late layer bands, residual property not MLP-out-specific) across Llama/Qwen/Gemma/Mistral/DeepSeek/GLM lineages, independent of alignment method.

Falsifier: Run Experiment (a) on at least three distinct families available locally (Gemma-2, Qwen2.5, and one Mistral or Llama variant). Extract the peak refusal layer and the subspace overlap with the estate-kit vectors per family. If any family shows:
- Peak refusal layer outside the 40-80% depth band, OR
- Cosine similarity < 0.5 between its refusal direction and the Gemma-2 direction (after correcting for model dimension), OR
- Abliteration requires > 3 orthogonal directions to drop safety refusals below 5%,
then the common-direction hypothesis is falsified for that family. If two or more families falsify, the cross-family commonality claim is rejected as folklore.
