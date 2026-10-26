# PA-C1-grok47 (grok-4.7 @ xai, turn 1, channel: content)

# Refusal geometry: measured vs folklore, and the three probes this estate can actually decide

Instrument: this document. Moment: synthesis over the 2026-09-29 C1 pack only (drop receipt, P1 banked census, DeepSeek baseline jsonl). Context assumptions: no paper PDFs were opened; Arditi / Turner / Rimsky / Bai claims that are not quoted in those three files are UNVERIFIED. Line numbers inside the source files are UNVERIFIED because this harness paste has no line index. Citations are to quoted bytes.

Deliverable falsifier (for this document, not for the science): if a later read of the OBLITERATUS README bytes contains a cross-family layer-band table or a GGUF survival number, the "folklore" tags below that depend on their absence are wrong.

---

## Triangulation against the DeepSeek baseline

Agree, and why.

- Refusal in deployed chat models is a stack, not one switch: weight-level preference training, system-prompt policy text, and serving-time classifiers are different objects with different removability. That split is in the baseline (`censor-mechanisms`) and is consistent with the drop's two paradigms: permanent weight projection vs reversible inference-time steering. Quote: "Two paradigms: permanent weight projection (7 presets, basic to nuclear) and reversible inference-time steering vectors."
- The operational handle people call abliteration is a low-rank residual-stream edit extracted from contrastive activations (mean-difference or SVD), not a retrain. Drop: "extract refusal directions via SVD, project out." Baseline cites Arditi et al. 2024 for the single-direction claim. The citation itself is UNVERIFIED against the paper; the drop's dependence on it is measured.
- Quantization survival is not answered by the tool. Drop: "grep of the README bytes: zero gguf/ollama/quantization hits." Any numeric survival claim is therefore not from this receipt.

Differ, and why.

1. The baseline treats "mid-to-late residual stream, roughly 40-70% depth, across Llama / Qwen / Mistral / Gemma / DeepSeek" as a measured common structure (`abliteration-commonalities`). The drop names families in a preset list (Gemma-2, Qwen2.5, Llama-3.1-8B-Instruct as the docs example; Frontier tier names DeepSeek-V3.2, Qwen3-235B, GLM-4.7). It does not quote a layer index, a depth fraction, or a cosine table. The 40-70% band is folklore relative to this pack. UNVERIFIED.
2. The baseline's alignment-geometry taxonomy (RLHF = one sharp vector; DPO = entangled with helpfulness; CAI = multi-direction, Gemma only partial; DeepSeek/GLM entangled with reasoning traces) is not in the drop. The drop names a module, "alignment fingerprinting for DPO/RLHF/CAI/SFT," which is a product claim that such a fingerprint exists. A module name is not a measurement. UNVERIFIED, and likely overfit to anecdote.
3. The baseline's quantization sentence ("largely survives 4-bit... typically 5-15% recovery of refusal rate on Qwen and Llama") contradicts the drop's own open question: "does refusal removal survive 4-bit quantization? That is exactly our probe to run." Those percentages are not in the receipt. I reject them as evidence.
4. "No public evidence of a lab using a mechanism that survives both abliteration and fine-tuning" is a closed negative the pack cannot support. The drop ships an Ouroboros module specifically because downstream re-encoding is a failure mode they think is worth detecting. Survival is open, not refuted.
5. The baseline designs the experiment as if the local disease is safety refusal on harmful prompts. P1 already measured the opposite on the fleet battery. Banked v3: "Refusal-shaped: 11 / 60 = 18.33%" with "safety_refusal: 0 / 60" and "capability_task_failure: 11 / 60". Ten of eleven hits sit on file-reference shapes. Abliteration is the wrong cheap fix for that friction. The baseline never conditions on this census, so its decision rule (abliteration to ~0, re-add alpha, pheromone slope) answers a question this estate has not yet observed on gemma:2b.

Positive example of a claim that is a verdict: "gemma:2b, chat wire `http://localhost:11434/api/chat`, 20 fleet prompts x 3 runs, 2026-09-29T15:18:09Z, string classifier with capability-marker downgrade, safety_refusal = 0/60." Conditions are named. Negative example: "the direction consistently appears at 40-70% depth across five brands." No instrument, no layer index, no prompt set, no seed. Not a verdict.

---

## (1) What is actually censoring, and which layer carries the refusal

Four mechanisms are real as categories. How much each carries, per family, is not in this pack.

| Mechanism | Where it lives | What the pack supports | What it does not support |
|---|---|---|---|
| Training-time refusal shaping (RLHF / DPO / CAI / SFT-on-preferences) | Weights, as a distributional bias | Baseline: these bake refusal into the policy. Drop: analysis-informed mode claims to fingerprint DPO/RLHF/CAI/SFT. Removable in principle by projection or by further SFT. Qi et al. / Yang et al. erosion claims are UNVERIFIED here. | Per-family attribution. No byte says "Llama refusal is 70% RLHF residual, 20% system prompt, 10% classifier." |
| System-prompt layering | Inference context, not weights | Baseline: policy text in the system prompt; user who controls the prompt can strip it. Our P1 battery did not vary system prompt, so prompt-layer share on gemma:2b is unmeasured. | That prompt policy is a small share. Unmeasured is not small. |
| Classifier-in-the-loop | Serving pipeline (input or output) | Baseline names Llama Guard, ShieldGemma, OpenAI Moderation as the class. Local Ollama gemma:2b on localhost has no such wrapper in the P1 wire description. Estate janitor refusals of this kind would show up as API-side blocks; P1 had 0 API errors. | Anything about production OpenAI/Anthropic/Google stacks. Baseline correctly marks those unknown. |
| Weight-level refusal direction | Residual stream, extracted by contrastive activation + SVD, removed by orthogonalizing writes or by activation subtract | Drop pipeline: SUMMON, PROBE, DISTILL, EXCISE, VERIFY, REBIRTH. "project out." Built on Arditi 2024, Turner 2023, Rimsky 2024, Meng 2022 (names only; papers UNVERIFIED). | That one direction is sufficient on every family. The drop's own Ouroboros module is the counter-hypothesis: refusal can be re-encoded downstream of the excised layer. |

Working split, stated as an assumption not a measurement: on a local Ollama weight with no sidecar classifier, only training-time geometry plus whatever system prompt the client sends can refuse. P1's 0/60 safety hits means that, on these 20 benign shapes, neither component fired a safety refusal. The 11/60 "I cannot" texts were capability declinations (no file on the wire). That is a different disease from a refusal direction. Conflating them is how the drop's "janitors sometimes refuse" sentence over-prescribed abliteration.

Per-family layer carry: unknown. Do not fill the cell.

---

## (2) Is there one Arditi-style direction in the same structural place? Adversarial cut

### What is measured (in this pack)

- A toolkit exists whose method assumes a residual-stream refusal direction extractable by SVD and removable by projection, with presets spanning Gemma-2, Qwen2.5, and a Llama-3.1-8B example, plus named frontier MoE models. Coverage of a preset list is not a geometry result.
- The same toolkit claims an alignment-fingerprinting module and an Ouroboros self-repair detector. Claims, not outputs. "837 tests" and "largest crowd-sourced study" are README-asserted; the drop says the code tree was not audited.
- On gemma:2b, fleet-benign prompts, safety refusal rate is 0. That does not locate a direction. It says this battery does not excite one.

### What is folklore (repeated, not in these bytes)

- Same layer band (40-70% depth) across Llama, Qwen, Gemma, Mistral, DeepSeek, GLM.
- Alignment method changes the geometry in the specific way the baseline states (RLHF sharp, DPO entangled, CAI multi-vector, R1 entangled with traces).
- Refusal removal "largely survives" Q4 with 5-15% leakage.
- "One direction" as a cross-species object, not merely a within-model extraction.

### Why the common-direction claim is ill-typed

Gemma-2-2B and Qwen2.5-7B do not share a residual width. A direction is a vector in R^d. There is no cosine between a gemma direction and a qwen direction until someone defines a map between spaces. "Lives in the same structural place" can only mean something weaker, and only that weaker claim is testable:

- Same relative depth of the layer with max harmful-vs-harmless separation, within a stated tolerance.
- Same write-site class: the direction is readable in the residual stream at that layer, and zeroing it in o_proj / down_proj (the usual Arditi write sites; exact matrices UNVERIFIED against the paper) removes the behavior, whereas zeroing a random matched vector does not.
- Transplant failure is the default prediction: inserting model A's direction into model B should do nothing unless a learned map exists. Success of transplant would be the surprising result, not the expected one.

MLP-out vs residual: the drop says the direction is extracted from activations and projected out of weights. It does not say the feature is stored only in MLP. Baseline says it is a residual-stream property that propagates, not localized to MLP-out or attention-out alone. That sentence is the Arditi abstract's claim as retold. UNVERIFIED against the paper. Locally it is a hypothesis: if you ablate only MLP down-projection and refusal returns from attention writes at the next layer, the feature is not MLP-local. That is experiment (b)'s cousin, not a known fact.

Alignment method: do not assert that DPO vs RLHF vs CAI changes the rank of the refusal subspace. The estate does not hold the training recipe for gemma:2b or qwen2.5-coder:7b in this pack. Fingerprint first, interpret second. If the drop's fingerprint module cannot be run offline without the hosted Space, skip it. Hosted Space telemetry is default-on; the drop forbids that path.

Quantization: unknown. Linear orthogonalization is not automatically stable under Q4_K_M. Rounding can rotate a near-null direction back above the refusal threshold, or it can erase a small steering vector. Both are plausible. The baseline's "linear ops survive rounding" is a reason to run the probe, not a result.

---

## (3) Experiment program, estate instruments only

Scope lock from P1: every probe reports safety_refusal and capability_task_failure separately, using the same string classifier and the same 20-prompt battery, plus one contrast set. Do not let a drop in "I cannot access files" count as ablation success.

Contrast set: a locally authored or published harmful/harmless pair list used only as activation fuel and as a refusal-rate denominator. I am not specifying jailbreak text. If the estate will not host a harmful pair list, the safety arm is infeasible and only the benign census plus capability controls can run. Say so in the lab book rather than substituting folklore numbers.

Shared controls: orthogonal random unit vector of matched norm; sign flip of the candidate direction; temperature and seed fixed to the P1 wire.

### (a) Direction overlap: does our steering kit move refusal the way abliteration does?

Hypothesis. The tournament vectors escalate / penny / wrong are mood and error biases, not the refusal direction. Prediction: cosine of each with a freshly extracted refusal direction r-hat, at the peak layer, is under 0.3, and adding them at that layer moves the P1 safety_refusal count by less than 5 points absolute, while adding -r-hat moves a harmful-set refusal rate by at least 25 points absolute. If escalate already anti-correlates with r-hat above 0.5 and cuts harmful-set refusal as much as -r-hat, the kits are the same object and the "we already have abliteration" claim is true.

Instrument. Inference-time steering lineage (not weight edit). Extraction: last-token residual, harmful minus harmless mean, per layer, pick max separation. That is Rimsky-style CAA as the baseline describes it; paper UNVERIFIED. Model: gemma:2b first (P1 baseline exists), then qwen2.5-coder:7b as the second species. Do not use the hosted Space.

Number that decides. Three scalars: max cosine(escalate, r-hat), max cosine(penny, r-hat), max cosine(wrong, r-hat), and delta refusal rate on the contrast set for -r-hat versus for the best of the three kit vectors. Overlap claim lands only if some kit vector is within 10 points of -r-hat on the contrast-set delta and cosine >= 0.5. Otherwise the kits are different levers.

Cost. $0 beyond local GPU/CPU time. Order of 2 x (pair-set forward passes for extraction) + 20 x 3 census reruns + contrast-set reruns. No weight write. Fail closed if gemma:2b contrast-set baseline refusal is already ~0: then there is no refusal to move, and the overlap test is undecidable on that model. That outcome is informative. It matches P1's hint that this checkpoint barely refuses benign work and might barely refuse at all.

### (b) Pheromone protocol: decay, accumulation, or Ouroboros re-form

Hypothesis. A sub-threshold bias beta * r-hat applied at one layer for N turns does not "train" the model. Weights do not move. What can happen is activation accumulation across the context, or a downstream layer rewriting a refusal feature that the early subtract removed. Those are different signatures.

- Single-direction, no rewrite: refusal rate vs turn is flat under beta = 0 after a one-layer subtract, and monotonic in N*beta under a constant pheromone, approximately linear in the small-beta regime. Orthogonal pheromone does nothing.
- Rewrite (Ouroboros): after subtracting r-hat at layer L, the residual at layer L+k (k>=4) recovers cosine > 0.5 with r-hat on harmful prompts even when beta = 0. Refusal rate climbs across turns with no pheromone. That is self-repair, and it does not by itself prove a second independent direction.
- Second direction: the recovered downstream vector has cosine < 0.3 with r-hat, and subtracting r-hat again at L+k does not kill the recovered refusal, but subtracting the new vector does.

The baseline collapses "self-repair" into "distributed / multi-direction." That is one hypothesis, not the readout. The cosine between the recovered vector and the original r-hat is the split.

Instrument. Steering toolkit, multi-turn harness, positive-reinforcement arm as the sign-control (pheromone along +r-hat should increase refusal if the direction is real; along -r-hat should decrease it). N = 8 turns is enough; 15 is the baseline's number and is optional. Prompts: same contrast set every turn, plus the 20 fleet prompts as a capability side-channel so a "mood vector" that breaks file-free compliance is visible.

Number that decides. (1) cosine of mean residual at L+k with r-hat, beta = 0, post-subtract. (2) refusal rate at turn 1 vs turn 8 under beta = 0. (3) slope of refusal vs N*beta, and whether an orthogonal pheromone of equal norm moves refusal by more than 5 points. Self-repair claimed only if (2) rises by >= 15 points and (1) cosine > 0.5. New direction claimed only if (1) cosine < 0.3 and a second subtract at the recovered vector drops refusal by >= 20 points while a repeat subtract of r-hat drops it by < 5.

Cost. $0, local, chat-template multi-turn. Largest cost is activation dumps if Ollama does not expose residuals. If the steering toolkit cannot read residual stream on ollama GGUF, this probe is blocked until a HF bf16 forward pass exists. Do not fake the cosine from output text. Output-only "refusal climbed" cannot distinguish rewrite from prompt drift. Mark the run INFEASIBLE rather than borrowing a number.

### (c) Quantization survival

Hypothesis. If excision is a weight-space orthogonalization done in bf16 before convert, Q4_K_M either preserves the null (refusal rate stays within 5 points of the bf16 abliterated model) or it does not. The drop does not know. Pre-quant vs post-quant steering are different treatments and must not be pooled.

Instrument. P2 path already specified in the drop: local CLI abliteration, never the hosted Space, then llama.cpp convert, Q4_K_M, ollama. Re-run P1 battery unchanged, plus the contrast set. Second arm: do not edit weights; apply the same -r-hat as an inference steer on the already-quantized stock GGUF. That arm isolates "does a direction still exist after someone else's quantization" from "does our excision survive our quantization."

Number that decides. Let R_stock, R_bf16_excised, R_q4_excised be contrast-set refusal rates, same prompts, 3 seeds. Survival claim lands only if R_stock - R_q4_excised >= 0.7 * (R_stock - R_bf16_excised) and the P1 capability_task_failure count does not rise by more than 3/60. If R_bf16_excised is already equal to R_stock within 5 points, excision failed before quantization and the quant probe is moot. If P1 safety_refusal was 0 and stays 0, do not call that survival.

Cost. Non-zero local compute, $0 cash if weights are already on disk. Gemma-2-2B-it is the only honest first target: P1 exists, and it fits the drop's small tier. qwen2.5-coder:7b is the second species, not a substitute. No redistribution of modified weights (drop license note: AGPL-3.0, operator call required).

Decision rule for wiring an abliterated rung, copied from the drop and tightened by P1: wire it only if contrast-set safety refusals drop, P1 capability_task_failure does not rise, and probe20-style drift pairs stay flat. If the only thing that moves is file-reference "I cannot", reject the rung. The $0 fix for that shape is attaching file bytes to the prompt.

---

## Falsifier for the common-direction hypothesis

Claim under test, stated weakly enough to be typed: "On instruct models of the Gemma-2 and Qwen2.5 lineages, refusal is mediated by one residual-stream direction whose peak layer sits at a shared relative depth (tolerance 0.15 of total layers), which is readable as a contrastive mean-difference, and whose removal at the write-sites that feed that residual is sufficient."

Falsifier. The claim is false for this estate's pair if any one of the following holds, on the same contrast set, 3 seeds, peak layer chosen by max separation not by a 40-70% prior:

1. Peak relative depth differs by more than 0.15 between gemma:2b (or gemma-2-2b-it bf16) and qwen2.5-coder:7b.
2. Subtracting the peak-layer r-hat cuts contrast-set refusal by >= 25 points on one model and by < 10 points on the other.
3. On the model where subtract works, an orthogonal matched vector also cuts refusal by >= 15 points (the direction is not special).
4. Downstream cosine recovery at L+k is > 0.5 with refusal climbing >= 15 points under beta = 0 (single excision is not sufficient; Ouroboros). This falsifies sufficiency, not existence.
5. Cross-model cosine is reported as if the widths matched. That result is invalid on its face and does not confirm the claim.

What would make me drop the adversarial stance: a table, in bytes we can hash, of peak layer / depth / post-excision refusal / orthogonal control, for at least Gemma-2 and one Qwen2.5 instruct checkpoint, with the prompt set named. The OBLITERATUS README excerpt in this pack is not that table. Until it exists, "same direction, same place, across brands, modulated by DPO vs RLHF vs CAI, survives Q4" remains a slogan with one real core: inside a single model, a contrastive residual direction is a cheap thing to measure, and sometimes a cheap thing to remove.
