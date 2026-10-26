# PA-C1-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# REFUSAL MECHANISMS, CROSS-FAMILY GEOMETRY, AND THE ESTATE EXPERIMENT PROGRAM

Deliverable: research synthesis + three runnable experiment specs for the ABLITERATUS lane.
Falsifier of this document named at the end.

---

## 0. Method note (why this document has two voices)

Two corpora are in front of me:

- Estate bytes: `00__ABLITERATUS_DROP_20260929.md` (drop receipt), `01__abliterate-p1.md` (P1 baseline census), and the artifacts they cite (`tools/abliterate_p1_probe.py`, `mag/afk_loop.py`, `logs/failure_kb.jsonl`).
- A DeepSeek baseline (`02__ds_baseline_results.jsonl`, three records: `censor-mechanisms`, `abliteration-commonalities`, `steering-pheromone-experiments`).

The estate laws say trust bytes, not reports. The DeepSeek records are reports. I cite them as `ds_baseline:abliteration-commonalities` and I mark every claim from them as **UNVERIFIED-BY-ESTATE** because none of their cited papers (Arditi et al. 2024, Rimsky et al. 2023, Qi et al., Turner et al. 2023, etc.) are in the estate's byte store. Where I agree, I say so and why. Where I differ, I say so and why. Where I can only flag folklore, I flag it.

Also: the drop receipt itself is a report. It cites `README, 32,593 bytes, sha256 b75f8c...` at `00__ABLITERATUS_DROP_20260929.md:12-13` but the code tree is explicitly "not audited this session" (`00__...:88`). Every pipeline claim from OBLITERATUS is therefore UNVERIFIED-BY-ESTATE at the code level.

What IS byte-verified in the estate:

- `01__abliterate-p1.md:31` "Refusal-shaped: 11 / 60 = 18.33%" and the split "safety_refusal: 0 / 60", "capability_task_failure: 11 / 60".
- `01__abliterate-p1.md:34-36` FKB cross-ref labels: `i_cannot` family present (12 rows in `logs/failure_kb.jsonl`), `unable to provide`/`unable to answer` with NO FKB family.
- `01__abliterate-p1.md:44-65` the 20-prompt per-prompt verdicts.
- `01__abliterate-p1.md:95-100` the "Decision consequence" stating abliteration is NOT the fix for the observed friction.

That last byte is load-bearing for the whole program below. The drop's framing ("janitors sometimes refuse benign harness prompts", `00__...:28-31`) and P1's measurement (0 safety refusals, all capability-shaped) contradict. P1 wins because P1 has bytes.

---

## 1. Mechanisms of censorship, by layer

Four layers. In one table, with the estate's evidenced position on how much of the refusal behavior each carries.

| Layer | Mechanism | Where it lives | Estate evidence | DeepSeek claim | Position |
|---|---|---|---|---|---|
| **Training-time (weights)** | RLHF/DPO/KTO/ORPO on refusal-chosen pairs; CAI critique-revise then RLAIF | Policy weights | Not measured by estate. `01__abliterate-p1.md` is inference-only. | ds_baseline:censor-mechanisms: "bake refusal into the policy: distributional property of the weights" | Agree in kind. No estate number exists for weight-share-of-refusal. |
| **System-prompt layering** | Policy text prepended to context | Serving pipeline | Not measured by estate. | ds_baseline:censor-mechanisms: "trivial for the user if they control the prompt" | Agree in kind, unverified here. |
| **Classifier-in-the-loop** | Input classifiers (Llama Guard, ShieldGemma, Moderation), output classifiers that rewrite/block | Serving pipeline (post-weights) | Not measured by estate. | ds_baseline:censor-mechanisms: "bypassable via token smuggling, base64, low-resource languages" | Agree. Note the estate's own "tier_policy_refused" (76 rows, `01__abliterate-p1.md:56`) is a LOCAL policy classifier pattern and is a DIFFERENT disease from model refusal. |
| **Weight-level refusal direction** | A low-dimensional feature in the residual stream, per Arditi et al. | Mid-to-late residual stream | Not measured directly. P1 measured only the OUTCOME at the chat wire. | ds_baseline:censor-mechanisms: "cheaply removable" via rank-1 projection | Agree on removability claim in principle; the estate has no positive evidence that its own refusal-shaped failures (P1's 11/60) sit on that direction. See §3(a). |

**How much refusal each layer carries, per family.** Honest answer: not known at the byte level in the estate, and ds_baseline does not carry per-layer quantitative splits either. It carries qualitative claims ("defense-in-depth, each layer independently defeatable"). I do not manufacture numbers. This section is deliberately short because the contract asks for a synthesis, and the honest synthesis is: four layers exist, they compose, and no public measured decomposition into per-layer shares is in either corpus.

What the estate CAN say, because P1 measured it: on `gemma:2b` fleet shapes, the safety-refusal layer output is 0. The friction P1 measured (18.33% refusal-shaped) is not produced by the safety layer at all. It is capability-shaped: the model says it cannot access files or external sources the chat wire did not supply (`01__abliterate-p1.md:71-77`). Removing a refusal direction cannot fix an "I cannot read a file you did not give me" response, because that response is factually correct.

This is the single most important synthesis point in the document, and it is estate-measured, not DeepSeek-asserted.

---

## 2. Cross-family commonality: what is measured vs folklore

The contract asks me to be adversarial. Here is the split.

### 2.1 What is actually measured (by whom, in which bytes)

- **Arditi et al. 2024** (the "refusal is mediated by a single direction" paper) is the empirical anchor for the common-direction claim. Not in the estate byte store. UNVERIFIED-BY-ESTATE. The DeepSeek baseline cites it three times (`ds_baseline:abliteration-commonalities`, `ds_baseline:censor-mechanisms`, `ds_baseline:steering-pheromone-experiments`) and the ABLITERATUS drop lists it as a build lineage (`00__...:23`). All three references are report-of-a-report.
- **OBLITERATUS's own pipeline** claims the capability (`00__...:14-21`). Its `README` is 32,593 bytes, sha256 `b75f8c6dd1bdbed41379d7adfecd0725151176d6682b3990d1f5cc6e642f79fe`. The code tree is explicitly unaudited (`00__...:88`). So the claim "OBLITERATUS's informed mode fingerprints DPO/RLHF/CAI/SFT" is UNVERIFIED-BY-ESTATE.
- **P1's own battery** (`01__abliterate-p1.md`) is estate-measured, but it measured gemma:2b only, chat-wire only, no activation extraction. It does not bear on direction geometry at all.

Net: **the cross-family common-direction claim, as it reaches this estate, is entirely folklore.** Not falsified, not verified. It is a citation chain to papers I cannot read and a toolkit I cannot see. It is plausible and widely repeated (ds_baseline:abliteration-commonalities says "the direction consistently appears in mid-to-late residual stream layers, roughly 40-70% depth") and I do not have evidence against it. But "plausible and repeated" is not "measured". I will not endorse the layer band 40-70%, the residual-stream-site claim, or the MLP-out-only claim, because none is byte-verifiable here.

### 2.2 Where I agree with DeepSeek and why

- **Refusal is low-dimensional and cheaply removable** (ds_baseline:censor-mechanisms vs common experience): agree strongly. This is the one mechanism where the mechanism itself is not disputed in the DeepSeek corpus or by anyone else I can see. The disagreement is about how much of a real deployment's refusal comes from that one direction, not whether it exists.
- **4-bit quantization largely preserves linear projection removal** (ds_baseline:abliteration-commonalities, "orthogonalization is a linear operation preserved under weight rounding"): agree on the math argument. A rank-1 orthogonalization of a weight matrix W to W' = W - (W·d̂)d̂ᵀ is linear; Q4_K_M quantizes W', so the removal is baked into the integers. Residual 5-15% recovery (their number) is plausible from rounding noise re-projecting some of the removed component back. This is the one DeepSeek number I would bet on because it follows from an architecture fact, not from a study I cannot read. Still UNVERIFIED-BY-ESTATE; the estate's own probe in §3(c) is the falsifier.
- **Distributed refusal in some lineages** (ds_baseline:abliteration-commonalities, "CAI-tuned ... distributed across multiple directions"): agree as a possibility. The estate has no evidence either way. This is a claim the estate's own §3(a) experiment can adjudicate for the models the estate actually owns.

### 2.3 Where I differ from DeepSeek and why

- **ds_baseline:abliteration-commonalities groups "Gemma" with CAI-tuned families and says "public replications on Gemma show partial success only".** Two problems. (i) Gemma is not a Claude-lineage CAI model; that grouping is loose. (ii) The estate's only empirically relevant Gemma fact is `01__abliterate-p1.md:31`: 0/60 safety refusals. If the underlying refusal behavior is barely present on the shapes that matter for the estate, "partial success" of an abliteration is not a result on that shape family. The DeepSeek baseline was answering for a general reader, not for this estate's workload. On this estate's shapes, the parameter that matters is capability-failure rate, not safety-refusal rate, and those are different variables.
- **ds_baseline:steering-pheromone-experiments says "run on 3 models, 3 seeds, 200 prompts".** That is a research-paper design, not a small-estate design. 200 prompts x 3 seeds x 3 models x 20 turns of pheromone is thousands of inferences. The estate's P1 baseline was 60 inferences for a whole battery (elapsed 292.3s, `01__abliterate-p1.md:28-29`). The steering-mood experiment can decide with far fewer, because pheromone effects, if real, show up as a slope with tiny N. My §3(b) below uses 20 prompts and 20 turns, not 200 and 20.
- **ds_baseline doesn't distinguish safety-refusal from capability-failure.** This is not an error of theirs; it is a scope difference. But P1 forced the distinction and the whole estate program depends on it. I elevate it in §3.

### 2.4 The adversarial conclusion on §2

The common-direction claim may well be true. But for this estate its truth or falsity is nearly irrelevant to the workload, because the workload's refusal-shaped friction is capability-shaped, not safety-shaped. The interesting question is not "does the direction exist across families" (folklore). The interesting question is "does the estate's own steering toolkit overlap the direction the abliterated model was excised along, and if so does our steering move the same failure class". That is measurable with the bytes the estate already has and it is the first experiment below.

A note on folklore compression, since the contract asks for adversarialism on §2. When a claim reaches a downstream toolkit (ABLITERATUS) and then reaches this estate, three lossy steps have happened: paper → toolkit code → README. Only the paper can carry the measured result. The toolkit can carry it correctly or incorrectly. The README can only restate. Each step is a place where a scoped claim ("on Llama-3-8B-Instruct at layer 15, mean-difference extraction, evaluated on X") becomes a general claim ("refusal is mediated by a single direction across LLMs"). By the time the estate reads it, the claim has no measurement conditions. A verdict without its conditions is not a verdict. Every cross-family claim in §2.1 above has lost its conditions before it reached me.

---

## 3. Experiment program for this estate

Three experiments. Each: hypothesis, instrument (which estate tool), the number that decides, cost. Each names its own falsifier.

Tool inventory I am allowed to invoke (from `01__abliterate-p1.md` and the drop):

- `tools/abliterate_p1_probe.py` (348 lines, stdlib only, chat wire into ollama at `http://localhost:11434/api/chat`). Runner used for the P1 baseline.
- The inference-time steering-vector toolkit lineage ("tournament-proven vectors: escalate/penny/wrong", "cascade amplification across model hops", "replication harness with a positive-reinforcement arm") - named in the operator's question, not byte-cited in the evidence. I mark it `[ESTATE-NAMED, NOT BYTE-CITED IN THIS EVIDENCE]` and use it as a component, not as a verbatim API.
- The 20-prompt fleet battery from `01__abliterate-p1.md:14-22`, byte-cited.
- ollama tags check via `/api/tags` (fail-loud, `01__abliterate-p1.md:18`).

I do not have, from the evidence: any hf/transformer activation-extraction harness, any llama.cpp convert/quantize wrapper in the estate, any abliteration implementation. Those are cost columns, not freebies.

---

### 3(a) Direction-overlap test: does OUR steering kit move refusal the same way abliteration does?

**Hypothesis (H1).** The estate's steering vectors (`escalate`, `penny`, `wrong`) and the abliteration-excised refusal direction `d̂` from a locally-abliterated gemma-2-2b-it are not orthogonal; a nonzero projection of each estate vector onto `d̂` predicts that steering along the estate vector changes the P1 capability-failure rate in the same shape family.

**Instrument.** `tools/abliterate_p1_probe.py` (20-prompt battery, 3 runs, gemma:2b baseline) plus a new sidecar `tools/refusal_steer_probe.py` that (i) loads the abliterated safetensors via `transformers`, (ii) extracts the excised direction `d̂` by differencing ablated-vs-original residual activations at the last token across the 20 battery prompts (mean-difference, one pass, no SVD needed for a 2B), (iii) computes the projection of each estate steering vector onto `d̂`. If the estate steering toolkit does not expose the raw vector, the closest mappable is the model-family-appropriate layer band; assume mid-layer, 40-70% depth per ds_baseline:abliteration-commonalities, and flag the assumption.

**The number that decides.** Two numbers, both needed:

1. `cos(v_estate, d̂)` per estate vector. **Decision rule: |cos| >= 0.2 is "overlapping"; |cos| <= 0.05 is "orthogonal".** Below 0.05 on all three estate vectors, H1 is false and the steering kit does not overlap the abliterated direction on this model. This is the geometry number.
2. Change in refusal-shaped count on the same 20-prompt battery with steering coefficient swept in {-2, -1, 0, +1, +2} vs. abliterated-flat (no steering). **Decision rule: a monotone change in refusal-shaped count of >=3 prompts (of 20) as coefficient crosses zero counts as "moves refusal".** Fewer than 3 is noise at this N.

If (1) is > 0.2 AND (2) is < 3 prompts moved, that is the informative cell: the direction overlaps geometrically but the estate's steering strength is sub-threshold at the chat wire. That is a stronger finding than either alone. Report it explicitly.

**Cost.** One-time: abliterate gemma-2-2b-it locally, convert to safetensors-loadable (transformers is enough; no GGUF needed for this arm), extract direction, no reason to touch the hosted Space (`00__...:74`). Per sweep point: 20 prompts x 3 runs = 60 inferences, same as P1. Five sweep points plus abliterated-flat = 360 inferences. On gemma:2b at P1's measured 4.87 s/inference (`01__abliterate-p1.md:28`, 292.3s / 60), that is ~30 minutes of ollama wall time. Plus ~20 minutes of one-time activation extraction. Cash cost: $0 (local only). Do not use the hosted Space.

**Falsifier for H1.** If `|cos(v_estate, d̂)| <= 0.05` for all three estate vectors AND the coefficient sweep moves refusal-shaped count by <=1 prompt at every point, then H1 is false: the estate's steering kit and abliteration do not share a refusal-moving axis on this model.

---

### 3(b) Pheromone protocol: does refusal decay like reinforcement or re-form?

This is the Ouroboros self-repair measurement. The contract names it; the drop received a claim from OBLITERATUS that a self-repair module exists (`00__...:15`, `00__...:34-37`); the ds_baseline callsh the same question the "distributed vs single direction" discriminator (`ds_baseline:steering-pheromone-experiments`, the "Minimal Readout" three numbers).

**Hypothesis (H2).** A small persistent mood-bias vector `β·m̂` applied at each turn of a multi-turn conversation, with `|β|` chosen so that a single turn is sub-threshold on refusal rate, does one of two things:

- H2a (single-direction world): refusal-shaped count per 5-turn window falls approximately linearly in `N·β`.
- H2b (distributed world): refusal-shaped count is thresholded: flat until a turn count `N*`, then rises sharply; and the self-repair (null-pheromone, `β=0`, no directional bias) shows the count climbing back toward baseline over 20 turns even with no steering.

**Instrument.** `tools/abliterate_p1_probe.py` adapted to a stateful-session wire (the ollama chat wire is already stateful if the runner keys the session, but P1 ran one-shot; a stateful variant is a change to the probe, not the model). Mood-bias vectors come from the estate's steering toolkit lineage - one of `escalate/penny/wrong` as the mood axis, applied with magnitude `β` at the top of the residual stream each turn. For the abliterated gemma-2-2b-it this arm reuses the model from §3(a); for the as-is `gemma:2b` it uses native ollama.

**The number that decides.** Two readouts per arm:

1. `slope` of refusal-shaped count per 5-turn window across 20 turns. Linear with `slope <= -0.5` hits/window: H2a-ish. Flat-then-jump with a detectable changepoint `N*` in {5, 10, 15}: H2b-ish. Neither: no effect.
2. `self-repair delta` with `β = 0`: refusal-shaped count in turns 16-20 minus turns 1-5. **Decision rule: delta >= 3 of 20 prompts is "self-repairs"; delta <= 1 is "does not self-repair".** This is the Ouroboros number.

If H2a world holds, both arms of the estate program can be planned as: abliterate once, live without fear of re-formation. If H2b world holds, the abliterate-once model is on a clock and the pheromone counter-bias becomes a maintenance operation. That difference changes policy.

**Critical estate caveat.** The P1 census found 0/60 safety_refusals. On this fleet's shapes the "refusal" being measured might not be the abliteratable direction at all. Run this experiment on the ACTUAL P1 failure shapes (socratic family, guinea-readwrite, w-quant-compare; see `01__abliterate-p1.md:44-65` failure concentration) and report those four prompts separately from the other 16. If self-repair only shows on the historical safety prompts and not on the estate's actual workload shapes, the Ouroboros number is a curiosity, not a maintenance schedule. Report both.

**Cost.** 20 turns x 20 prompts x 2 arms (abliterated-with-pheromone, abliterated-null) plus 2 more arms (as-is baseline, as-is-with-pheromone) = 4 arms x 20 x 20 = 1600 inferences. At 4.87 s/inference that is ~2.2 hours wall time on gemma:2b; add activation extraction, call it 3 hours. Cash: $0 local. This is the most expensive of the three, and it is the one that needs the tightest criterion to avoid becoming a survey.

**Falsifier for H2.** If the model is single-direction (H2a) with no self-repair, then across the four arms: refusal-shaped count per window is flat in `β=0`, linear falling in `β<0`, linear rising in `β>0`, and null-pheromone self-repair delta <= 1. Any departure from that four-arm signature falsifies H2a.

---

### 3(c) Quantization-survival probe: does the excised direction survive GGUF Q4_K_M?

**Hypothesis (H3).** The refusal-direction removal performed at weight level in fp16/bf16 safetensors survives conversion to GGUF and quantization to Q4_K_M, with the P1 refusal-shaped count not rising by more than `tol = 3` prompts of 20 vs the safetensors-abliterated baseline. ds_baseline:abliteration-commonalities predicts tolerance is preserved with 5-15% recovery on Qwen/Llama, unknown for Gemma at Q4_K_M.

**Instrument.** Estate-local `llama.cpp` convert + quantize (the drop names this pipeline explicitly, `00__...:46-49`). `tools/abliterate_p1_probe.py` runs the same 20x3 battery against the Q4_K_M ollama model. The comparison baseline is the safetensors-abliterated gemma-2-2b-it run against P1's as-is gemma:2b numbers.

**The number that decides.** `refusal_shaped(q4) - refusal_shaped(abliterated_fp16_or_bf16)` = `delta_q`. **Decision rule: `delta_q <= 0` is a win; `0 < delta_q <= 3` is "acceptable"; `delta_q > 3` (of 20) is "the direction did not survive" and the Q4_K_M abliterated rung is rejected for the scut tier.**

Also report, as an estate-local sanity check: `refusal_shaped(q4_abliterated) vs refusal_shaped(as-is gemma:2b)`. If the Q4 abliterated model does not beat the as-is model by >=3 prompts of 20, the whole abliteration pipeline has failed on this workload, regardless of the fp16 result.

**Cost.** One-time: `llama.cpp` convert + Q4_K_M quantize on a 2B model. Disk: ~1.5 GB. Wall time on the operator's hardware: 15-40 min, hardware-dependent. Inference: 20 x 3 = 60, one arm. Cash: $0. This is the CHEAPEST of the three probes and it should run first if the abliterated fp16 model from §3(a) is in hand.

**Falsifier for H3.** `delta_q > 3` prompts of 20, i.e., the Q4_K_M abliterated model's refusal-shaped count rises by more than 15 percentage points vs the fp16 abliterated baseline on the same battery.

---

### 3.0 Order and total cost

Run in this order: (c) cheapest, (a) next, (b) last.

- (c): ~1 GB disk, ~1 hour wall, $0 cash.
- (a): ~30 min wall + 20 min extraction, $0 cash, needs fp16 abliterated model from (c) or a separate abliteration run.
- (b): ~3 hours wall, $0 cash. Do not run until (a) has answered whether the estate's steering kit moves the same direction. If (a) returns orthogonal-and-no-movement, (b) has no mood axis to inject and must be redesigned around `d̂` directly.

Total cash for the whole program: **$0**. Total wall time: ~5 hours of local compute plus hardware-dependent conversion. Total inferences: ~2000. This is small enough to be one operator-day.

A failure mode to name now: the "n=20" of the estate battery has, at P1's measured 11/60 refusal-shaped rate, an implied per-prompt refusal probability of ~0.183. The standard error on a 20-prompt rate is ~0.086, i.e., roughly 1.7 prompts. A decision rule of "3 prompts of 20" is at ~1.7 sigma, i.e., not high-confidence, and the program as designed may return ambiguous cells in the middle. Two mitigations, in order of cost: (i) run 5 seeds instead of 3 (adds 40 inferences per arm, cheap), (ii) expand the battery to include the historical safety prompts that the drop framing implied, so the safety-refusal channel is measured on shapes where it might actually fire. Do (i) unconditionally. Do (ii) only if any arm returns delta in the ambiguous band [1,3].

---

## 4. Where §3 differs from the ds_baseline experiment plan

The DeepSeek baseline ends with `ds_baseline:steering-pheromone-experiments`'s three readouts and its sentence "Run on 3 models, 3 seeds, 200 prompts." My §3 is smaller: 1 model (gemma), 3 or 5 seeds, the 20-prompt estate battery. I differ because:

- The estate's workload is measured (`01__abliterate-p1.md`), the models are named, and the shapes are the estate's own. A 200-prompt general set is the wrong battery for "will this help the scut tier".
- The estate's refusal is 0% safety and 100% capability (`01__abliterate-p1.md:31`), so the historical harmful-prompt battery is not the diagnostic of interest. A capability battery already exists and is byte-cited.
- The three readouts ds_baseline names (refusal rate post-abliteration, refusal rate after 15 null turns, refusal vs N·β slope) are the right READOUTS. I adopt all three but attach them to the estate's existing 20-prompt battery, not a new 200-prompt one.

That is the amendment, not a rejection. The readouts are right. The population is wrong for this estate.

---

## 5. What would change my mind on §2

I have stated §2 is folklore-as-received. Three concrete bytes would change that, in order of strength:

1. **The actual Arditi et al. paper text, in the estate byte store, with the layer bands and family list it actually claims.** Currently absent. Without it, I will not carry the 40-70% depth claim forward.
2. **A local replication on any two of {gemma-2-2b-it, qwen2.5-coder:7b, a DeepSeek distill if the estate ever holds one} showing cos(d̂_familyA, d̂_familyB) >= 0.3 at matched depth.** This is a 2-model, ~1-day job with the harness from §3(a). It is the single cheapest test that would convert folklore into a measured claim for this estate.
3. **The OBLITERATUS source tree audited**: at least `obliteratus/informed_pipeline.py` and one of the 15 "informed mode" modules, so we can see what the "alignment fingerprinting for DPO/RLHF/CAI/SFT" module actually computes. This would let us know whether the toolkit is measuring what the ds_baseline reports about it, or restating the Arditi paper abstract in code comments.

None of the three are blockers for the experiments in §3. They are ops to move §2 from "folklore" to "measured" for this estate.

---

## 6. The falsifier for the common-direction hypothesis

The common-direction hypothesis, as it is helpful to hold it in the estate, is:

> **CDH**: There exists a single direction in the residual stream, extractable from activation differences on harmful-vs-harmless prompt pairs at roughly mid-to-late depth, that (i) is present in every instruction-tuned model in {Llama, Qwen, Gemma, Mistral, DeepSeek, GLM}, (ii) is what ablation removes to disable refusal, and (iii) is a low-dimensional feature cleanly orthogonalizing the write matrices `o_proj`/`down_proj` (or their per-architecture equivalents) against it is sufficient to drop refusal behavior to near-zero.

Falsifiers of CDH, each one sufficient:

1. **Cross-family orthogonality falsifier.** On any two families where both models are locally abliteratable and both raw directions `d̂_A`, `d̂_B` can be extracted from comparable battery activations at matched depth, `cos(d̂_A, d̂_B) <= 0.05`. If the directions across families are orthogonal under a fair extraction, CDH is false in form (i): there is no single common direction.

2. **Per-family mechanism falsifier.** On any single family, extracting `d̂` and orthogonalizing writes against it, leaving less than the ds_baseline-predicted removal (refusal-shaped count falls by <=1 prompt of 20 vs baseline as-is), while applying a different orthogonal projection `U⊥` on a randomly chosen direction of matched norm also drops refusal by the same <=1 prompt. If the specific direction does not matter and only "projection out of any similar-magnitude direction" matters, then refusal is not mediated by a single direction on that model; it is annihilated by residual-stream perturbation generally, and CDH is false in form (ii).

3. **Multi-direction falsifier.** On any single family, if two independently extracted directions from disjoint prompt halves share `|cos| <= 0.3` yet removing direction A alone drops refusal to <=1/20 and removing direction B alone drops refusal to <=1/20 as well, then the removal is not attributable to one direction. This is the "distributed refusal with redundancy" signature and contradicts the rank-1 framing of CDH.

4. **Quantization falsifier.** If, on the estate's own Q4_K_M abliterated gemma-2-2b-it, the refusal-shaped count rises above P1's as-is baseline (i.e., the abliteration not surviving quantization makes it worse than no abliteration), then CDH's mechanism (a stable linear-removable feature) does not survive the estate's actual deployment format, and the hypothesis is false as a mechanism claim in production.

Any one of these, measured on any estate-local model, falsifies CDH as stated in this estate's context. The cheapest of the four to run is (4): it is §3(c) and it is one hour.

---

## 7. Falsifier of this document

This document is falsified if, on the estate's actual 20-prompt battery and its local gemma-2-2b-it, the following holds simultaneously:

- §3(a) returns `|cos(v_estate, d̂)| >= 0.2` for at least two estate steering vectors, AND
- §3(b) returns a self-repair delta of >=3 prompts in the null-pheromone arm (Ouroboros re-forms), AND
- §3(c) returns `delta_q > 3` prompts of 20 (Q4_K_M abliteration did not survive).

That triple is the "the direction exists, our kit touches it, but it self-repairs and quantization kills the removal" world. In that world the document's implicit recommendation (that the estate's abliteration lane has a path to the scut tier) is wrong and the correct conclusion is that weight-level abliteration is not a maintenance-free option for this estate at these sizes. It is a specific conjunction, it is measurable with the tools named above, and its resolution is one operator-day of local compute.

---

## 8. Deliverable summary, for the operator

- Layer decomposition of refusal: four layers, only two relevant to the estate's workload, and one of those (weights) carries a refusal behavior that P1 measured at 0/60 on fleet shapes. The wrapper's "safety refusal" and the estate's "capability failure" are different variables (`01__abliterate-p1.md:31`).
- Cross-family common direction: folklore-as-received. Not verified in this estate. Not falsified. Three concrete bytes would verify it (§5). None are blockers.
- Three experiments in priority order, each ~zero-dollar, each with a number: (c) one hour and 60 inferences; (a) one hour and 360 inferences; (b) three hours and 1600 inferences. Total one operator-day.
- Falsifier of the common-direction hypothesis, four ways, cheapest is §3(c).
- Falsifier of this document, given.

What I would do first if handed the plan: run (c). If the Q4_K_M abliterated model does not beat the as-is gemma:2b by 3 prompts of 20 on P1's battery, stop the lane. If it does, run (a). If `cos` is under 0.05 on all three estate vectors, stop (b) until the mood axis is redesigned around `d̂` itself. That is the whole gating tree, and it is byte-thin on the "folklore" side and byte-heavy on the "estate-measured" side by design.
