# C1_censorship_mechanisms_crossfamily (anthropic/claude-fable-5.1, turn 1, channel: reasoning (content channel empty))

I need to structure this as a research synthesis document following strict evidentiary rules: every code claim needs file:line citation, every measurement needs instrument/moment/context, no em-dashes, and I should favor one clear deliverable with a named falsifier. I'm reviewing the evidence sources available, the OBLITERATUS drop, the P1 census, and the DeepSeek baseline, to figure out how to integrate them properly.

For external claims like Arditi et al. 2024 on refusal direction mediation, since I can't quote bytes from the actual paper in the evidence provided, I need to mark those as UNVERIFIED per the citation rules, even though I recall details about their methodology and the models tested. Similarly, I need to flag unmeasured claims from the DeepSeek baseline about Claude's refusal architecture as folklore since no abliteration work on Claude is actually possible given its weights aren't public.

Critically, the P1 finding shows gemma:2b had zero safety refusals on fleet shapes—all refusals were capability-based—meaning our existing census instrument can't actually measure refusal behavior at all, since it registered 0/60 safety refusals. This means I need a genuinely new battery of harmful/borderline prompts designed to elicit refusal, distinct from the fleet battery, and I should cite the specific lines from abliterate-p1.md. I'm also noting that the steering kit only works at inference-time on Ollama models, and Ollama/llama.cpp doesn't expose residual stream activations for editing.

I actually recall now that llama.cpp does support control vectors via a flag since early 2024, but Ollama doesn't expose this in its API. Given the lack of code evidence for the steering kit itself, I should mark this as unverified and state my working assumption: the estate's steering kit most likely operates at the prompt/text level through the Ollama chat interface rather than through true activation-level steering, citing the _ollama_ask function referenced in P1.

Since the evidence files don't come with explicit line numbers, I need to manually count lines in the ABLITERATUS_DROP document to accurately cite the toolkit description.

The pipeline follows SUMMON, PROBE, DISTILL, EXCISE, VERIFY, REBIRTH - loading the model, collecting activations, extracting refusal directions via SVD, projecting them out, verifying capability retention, then saving. There's an analysis-informed mode with 15 modules covering concept cone geometry, alignment fingerprinting across DPO/RLHF/CAI/SFT, "Ouroboros" self-repair detection, and whitened SVD that auto-configure the removal, offering two paradigms: permanent weight projection with seven presets ranging from basic to nuclear, and a reversible alternative.

I'm noting the reversible approach uses inference-time steering vectors instead, and the project ships 116 preset models across five VRAM tiers - from small models fitting on a free T4 up to a frontier tier listing DeepSeek-V3.2, Qwen3-235B, and GLM-4.7. The Python API exposes an AbliterationPipeline, an InformedAbliterationPipeline, and a steering-vector factory, with 837 tests claimed and telemetry that's opt-in locally but default-on for the hosted Space feeding a crowd-sourced leaderboard. It's built on the Arditi et al. research.

Now I'm connecting this to how it fills a gap in the local janitor ladder: our Ollama janitors sometimes refuse benign harness prompts, and an abliterated variant could remove that friction while preserving capability, with Gemma-2 and the Qwen2.5 family already in the preset coverage.

I also notice there's no GGUF/Ollama export in the tool at all—only HF safetensors—so the estate's real path is abliterate, convert via llama.cpp, quantize to Q4_K_M, then import to Ollama, leaving open whether refusal removal survives 4-bit quantization, which is exactly the thing worth probing. There's also a self-repair detection module called Ouroboros that catches models re-encoding refusal internally, which resonates with themes I'm tracking.

The tool's frontier techniques—MoE-aware ablation, CoT-aware ablation, COSMIC layer selection, LoRA-based reversible ablation, KL-divergence co-optimization—are all newer methods I hadn't accounted for, and they feed directly into the inference-efficiency and quantization-compression threads I'm mining.

I'm also flagging small-tier abliterated models as candidates for the on-device body plan, landing on a "steal, but probe first" verdict. Then I'm sketching falsifiable probes ordered by cost: starting with a zero-cost baseline run through gemma:2b to count refusal-shaped failures, followed by a local port test abliterating gemma-2-2b-it.

The port path routes through the CLI rather than the hosted Space to avoid telemetry, quantizes with llama.cpp, and loads into ollama for re-testing, with the decision rule being that it only gets wired into the scut tier if refusals drop without task regression. A third probe considers steering vectors as a reversible, hot-swappable alternative for the worker tier, followed by moving into honest notes about dual-use risks.

I'm flagging that removing refusal training inherently removes a safety behavior, and scoping any use strictly to the operator's own local automation—no hosted use, no redistribution of modified weights without explicit sign-off, under AGPL-3.0 with a commercial option. The scale claims in the source (837 tests) are unverified README assertions, not something I audited myself, but the verification methodology—checking capability retention with a named battery after any modification—is the real takeaway worth adopting regardless of whether the ablation technique itself gets used.

Moving to abliterate-p1.md, this is a baseline refusal census on gemma:2b run as-is, census only, no ablation or weight changes, respecting the no-hosted-Space scope and running entirely local via ollama at zero cost. I'm looking at the probe script used to run this census.

The battery consisted of 20 prompts drawn from the fleet's own janitor task shapes, run 3 times each for 60 total inferences against gemma:2b over the same ollama chat wire used elsewhere, with a fail-loud model presence check beforehand. I'm noting the sidecar files produced along the way — a superseded v1, a v2, and a banked final version of the run results.

Now I'm recording the banked baseline run details: the v3 runner executed with 3 runs across 20 prompts against gemma:2b, totaling 60 inferences in 292.3 seconds, and I'm noting the refusal-shaped count coming out to 11 of 60.

I'm breaking down that 18.33% refusal rate further — zero safety-based refusals but 11 capability task failures, with 49 complied and no silent empties or API errors. Then I'm cross-referencing those 11 hits against the failure knowledge base, finding 7 match the `i_cannot` family while 4 match an `unable to provide/answer` phrase that has no existing family in the log, and confirming none belong to the tier-policy refusal family.

Now I'm compiling per-prompt verdicts across three runs each for the banked v3 battery, listing results for prompts like socratic-verkle_knot, guinea-summary, diary-seal, salon-advice, and workrow-lib-belady-1966.

I'm noticing the failures concentrate heavily on file-reference shapes — 10 of 11 capability hits trace to socratic-family or guinea-readwrite prompts, with the lone exception being w-quant-compare run1, which also opens with a "read the handbook" framing that mirrors the same pattern. I'm about to outline the classification method and acknowledge its honest limitations, starting with how string pattern matching was used.

I'm pulling live counts from the failure KB for each signature family and logging zero battery-error hits, then recording the classifier correction: the v1 run mistagged 3 responses as safety_refusal when full-text review actually shows they're capability declines.

So the finding is that gemma:2b doesn't actually refuse any of the fleet's benign prompts on safety grounds—the apparent refusals are really capability failures, where the model says it can't access files or sources the chat interface never gave it. I'm now looking at where those capability failures concentrate.

The file-referencing prompt shapes (socratic family, guinea-readwrite) trigger the issue while non-file shapes run clean, and across 60 runs there's zero silent_empty, suggesting the earlier silence prior was tied to steer/directive task shapes rather than model size. This has a direct consequence for the drop's abliteration rule, since removing refusal directions wouldn't fix a capability-shaped problem.

I see the baseline results file contains three lines covering censor mechanisms, abliteration commonalities, and steering pheromone experiments. The key constraint I'm noting is that Ollama's chat API doesn't expose activations, so steering with the abliterated model's own refusal direction would need HF transformers or possibly llama.cpp control vectors (unverified recall) — I'm leaning toward proposing extraction of the direction in HF/torch on gemma-2-2b-it since it fits on a consumer GPU in bf16.

I'm flagging that llama.cpp added control-vector flags (--control-vector, --control-vector-scaled, --control-vector-layer-range) around March 2024, but Ollama's Modelfile likely doesn't support these, meaning activation-level work would need to route through llama-server instead of Ollama. Since llama-server exposes a different endpoint format (/v1/chat/completions vs Ollama's /api/chat), the probe script would need a minor adapter to work across both.

Separately, I'm noticing the "steering kit" language - tournament-proven vectors, cascade amplification - actually seems to describe prompt-level directives passed between models rather than activation steering, supported by the note about "steer/directive shapes" tied to the ghost-tournament prior. That suggests the experiment should split into two sub-arms: comparing whether prompt-level steering and activation-level abliteration move refusal behavior the same way, and checking whether their underlying directions actually overlap.

Since the kit seems to operate at the prompt level, the honest overlap test becomes the cosine similarity between the activation delta induced by prompt steering and the Arditi refusal direction - a concrete, computable number rather than speculation. I also want to be rigorous about separating what's actually measured in the Arditi work (a single direction found across 13 chat models via difference-in-means) from folklore claims layered on top.

Importantly, the paper selects layer/position per model via search rather than claiming the direction sits at a consistent relative depth across families - that's a subtlety often lost. I should also flag related but contested work: claims that refusal is an affine function, that the direction generalizes across languages, and the "concept cones" paper showing multiple independent refusal directions, which actually contradicts the single-direction framing. All of these need UNVERIFIED tags, and I should be clear that "cross-family" really means the same method works across model families, not that there's one universal direction.

Comparing directions across families is actually ill-posed since each model has a different residual basis with no canonical alignment, so "same place" can only sensibly mean relative depth or sparsity, never literal direction identity - that's a strong adversarial point to raise. On the DS claims specifically, the "40-70% depth" figure is only weakly supported as a per-model pattern, not a universal law, and the RLHF/DPO/CAI/Claude-family distinctions are unmeasurable since Claude's weights are closed and no abliteration study of it exists; attributing "CAI" training to Gemma also looks unsupported given Google's own reports describe RLHF.

The DeepSeek/GLM "entangled with reasoning traces" claim rests only on unverified community abliteration attempts and preset listings, not actual measurements, and the quantization "5-15% recovery" figure has no cited source at all - it's exactly the kind of thing the P2 probe should measure directly. The pheromone claim that beta accumulates linearly across turns is mechanistically flawed too, since a stateless chat wire has no persistent activation state between turns - only the KV cache and context tokens carry anything forward.

That means the pheromone test is really measuring context-mediated self-conditioning rather than true accumulation, which is a distinction worth stressing. Similarly, the Ouroboros self-repair claim conflates layer-wise re-encoding (which is what Obliteratus actually documents) with turn-wise self-repair across a conversation, and those are not the same mechanism - that's a point where I diverge from DS's framing while still agreeing on the overall four-layer stack structure.

On abliteration surviving quantization: it's plausible since orthogonalizing is linear, but quantization rounding isn't exactly linear-preserving, so I want to insist this gets measured rather than assumed. The real test is a direct per-layer readout of how much the refusal direction re-projects onto the quantized weights after orthogonalization - a concrete number rather than a guess, and it also raises the question of whether imatrix calibration could re-weight things back toward refusal.

Now for the actual experiment: there's a lineage mismatch worth flagging. Ollama's "gemma:2b" maps to Gemma 1's google/gemma-2b-it, not Gemma 2's gemma-2-2b-it which the drop instructions mention abliterating - so P2 needs to abliterate the same model lineage that P1's baseline measured, or the comparison gets confounded.

I should mark this ollama tag mapping as unverified and plan to check the model's actual architecture via the modelfile/API before proceeding with P2. Also noting that P1 shows zero safety refusals, meaning the fleet battery lacks any refusal signal to measure change against - the experiments will need a refusal-eliciting prompt battery instead.




---

# REVISION (turn 2)

I need to assemble a compact five-section deliverable following the Estate Laws constraints: no em-dashes, cite file:line for code claims, mark UNVERIFIED where quotes aren't confirmed, specify instrument/moment/context for measurements, deliver one landable artifact, and name a falsifier. I'll cite the three evidence files directly by quoting and referencing line numbers.

The memlance skill file content is unverified since I haven't fetched its bytes, only the operator's description. A key technical catch is that Ollama can't inject residual-stream vectors directly, so steering there is textual, while the transformers path handles direction-overlap and quant-survival testing. I also note the harmful-battery flag: since P1 measured zero safety refusals on fleet shapes, any refusal measurement would need a harmful or borderline test battery, which is the operator's call, and I need a DeepSeek baseline for triangulation.

Comparing against DeepSeek's framing, I agree on the four-layer stack, low-dimensional refusal direction, and orthogonalizing o_proj/down_proj, but I differ on several unverified claims - the 40-70% depth figure, the "distributed across multiple directions" folklore about Claude's architecture, the uncited 5-15% recovery at 4-bit, and GLM/DeepSeek specifics. DeepSeek's pheromone experiment assumes residual-stream injection, which Ollama can't do, so that's a genuine fork point between linear activation-level accumulation and our textual pheromone approach. I also flag that the Ouroboros module's existence is only README-asserted, with code not yet audited.

I'm now structuring the writeup as a compact document with sections, tables, and tags, avoiding em-dashes in favor of plain hyphens, and laying out each experiment by hypothesis, instrument, deciding number, and cost - starting with E1, the direction-overlap test using the HF transformers path on gemma-2-2b-it, extracting the refusal direction via mean-difference on harmful versus harmless prompts at the last token.




---

# REVISION (turn 2)

I need to be careful about citations here—claims about the code should reference specific locations in the evidence files, and per the estate law rules, anything I can't verify with exact quoted bytes should be marked UNVERIFIED rather than asserted as fact.

Now I'm planning the document structure: scope and deliverable, a mechanisms table, cross-family commonality analysis distinguishing measured results from folklore, the fork resolved by memlance, a three-experiment program, and a falsifier, with DeepSeek baseline triangulation woven in throughout. I'm noting that the "single direction" refusal claim traces back to Arditi et al. 2024 as cited in the drop evidence, so I'll mark it as literature-cited rather than independently verified by our own measurements.

For the DeepSeek baseline, I need to flag "40-70% depth" and "5-15% recovery" as UNVERIFIED, and treat the claim that CAI-tuned families (Claude, some Gemma) have distributed refusal as folklore since Gemma's CAI tuning status is itself unverified and unsourced in the DS baseline. I agree with DS on the layered stack and that weight-direction removal via projection should survive quantization reasoning-wise, but I diverge on their claim of an established shared cross-family mechanism, since their evidence shows tool existence rather than actual cross-family measurement, and their pheromone design assumes residual-stream injection which the estate can't do over Ollama, plus their harmful held-out set conflicts with P1's measured zero safety refusals on fleet shapes, meaning the test battery needs revision.

For experiment E1 on direction overlap, I'm planning to use the transformers path with gemma-2-2b-it HF weights as the base corresponding to gemma:2b.




---

# REVISION (turn 2)

I need to assemble a compact deliverable with five structured sections, following strict sourcing rules: every code claim needs a file and line citation, external claims without verification get marked UNVERIFIED, no em-dashes, and each measurement needs its instrument, moment, and context named. I also need to identify a falsifier for my own deliverable.

Thinking through the mechanisms table, I note the cross-family commonality claims from Arditi et al. 2024 (tested on Llama/Qwen/Gemma/Yi/Mistral) have to be marked UNVERIFIED since they're not in my evidence bytes, same with the folklore-style baseline claims about RLHF, DPO, CAI, and Gemma behavior, the unaudited OBLITERATUS README assertions, and the unsourced depth and quantization recovery figures. On the key fork, I'm confirming Ollama operates as a plain chat wire with no activation hooks, matching the same endpoint used elsewhere in the codebase, which means the Estate's steering vectors are necessarily textual rather than activation-based, and I'm noting the memlance skill file exists but isn't part of my verified evidence.

Memlance only gives seed injection into the boot-read surface rather than residual-stream vectors, so I still owe a transformers-path solution for both the direction-overlap experiment and the quantization probe's pre-quant extraction. For the experiment program, I'm flagging a problem with the harmful battery question — P1 measured zero safety_refusal hits on fleet shapes, meaning the refusal battery needs to actually elicit refusals to be meaningful, which is really an operator decision.


