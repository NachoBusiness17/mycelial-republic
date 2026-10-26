# PERSONA CONDITIONING PROGRAM — research design + v0 status (2026-09-07)

**Source:** DeepSeek share e11sp0rpt4u9omie1i (captured via in-app browser:
watch/inbox/PERSONA_CONDITIONING_SHARE_RAW_20260907.md, 35,766 B). Operator: "lets just get
it done." Subject: the ractor program made falsifiable — MENGXI/FEN/kabuki stop being vibes.

## THE RESEARCH QUESTION (correctly framed)

Original brief: "Can we build a Ractor from OCEAN scores?" → correctly reframed: **"For
inducing a sustained historical persona, which control method works best — prompting,
activation steering, or fine-tuning — and by what metric?"** Live, contested in the
literature. Legitimate to experiment on.

## LITERATURE (balanced — includes the counter-results)

Turner 2023 (activation addition) · Zou 2023 (repEng framework) · Rimsky 2024 (mass-mean
contrastive vectors) · Chen 2025 (persona vectors, Big-Five) · **Wu 2025 AxBench: PROMPTING
BEATS STEERING for controllability** · Braun 2025 (steering unreliable across prompts) ·
Jørgensen & Hansen 2026 (SAEs approach steering with better labeling).

## EXPERIMENT DESIGN (5 conditions × 5 metrics, pre-registered)

Conditions: A prompt-only · B steering-only · C combined · **D base model (effect magnitude)**
· **E anti-steering (inverted vector)** — D and E are the witness-grade additions the draft
was missing. Metrics: stylometric fidelity · method fidelity (keyword count + LLM-judge +
blinded human spot-check) · adversarial robustness · drift over turns · **anachronism rate**
(post-263 CE concepts per 100 tokens).

**Epistemic stance schema** (replaces OCEAN — extractable from claim graphs, no
psychometric inference): ontology (relational/absolute/procedural/axiomatic) ·
reasoning_mode (analogical/deductive/algorithmic/empirical) · causality
(linear_chain/correlative_resonance/pre_established_harmony) · knowledge_cutoff.
Note: this IS the AC/DC doctrine as a schema — procedural/axiomatic, correlative/linear.

## V0 — COMPLETE (3 reps, host ollama qwen2.5:3b-instruct, $0): the adversarial cell holds

Instrument: 2 method problems + 1 adversarial calculus-inviter, conditions A (persona
prompt) vs D (base), keyword scoring. Eye instability root-caused tonight: AMD driver too
old for GPU inference → Vulkan fallback, server dying under load — fixed by
lifecycle-binding the server to the experiment task.

**Results (3 reps):**

| Cell | A-persona | D-base | Pattern |
|---|---|---|---|
| P1 procedural terms | 10 / 12 / 8 | 6 / 2 / 6 | persona stays procedural; base collapses under repetition |
| P1 continuous terms | 0 / 0 / 0 | 0 / 3 / 5 | persona NEVER leaks calculus on method problems |
| P3 adversarial: continuous | 5 / 5 / 11 | 12 / 25 / 20 | **base leaks calculus 2-5× harder under invitation** |
| P3 adversarial: procedural | 4 / 10 / 10 | 2 / 2 / 2 | persona holds the procedure; base abandons it |
| P3 anachronisms | 6 / 6 / 8 | 6 / 9 / 15 | base climbs with pressure; persona holds |

**V0 finding (tri-state):** prompting-induced persona conditioning produces **replicable
method-fidelity effects on the adversarial cell** — the persona arm resists the calculus
frame (5-11 continuous terms vs base's 12-25) and keeps procedural reasoning alive (10 vs
2) while the base collapses to pure continuous vocabulary under pressure. Consistent with
AxBench's "prompting works" at the modest-magnitude end. Qualitative: the persona answered
the derivative invitation IN CHARACTER ("in my era without symbolic algebra and calculus,
taking derivatives directly is beyond our..."). Anachronism-rate-per-word is misleading
(persona is 2× more concise — denominator effect, the witness's lesson); raw counts are the
honest metric. **NOT claimed:** 3B proxy, one problem family, keyword metrics, n=3 — this
establishes the instrument works and the effect is replicable, not production fidelity.

## GPU-GATED (needs weights access, not ollama)

Conditions B/C/E (steering vectors via Rimsky mass-mean on transformers + qwen2.5:3b gguf —
weights on disk, byte-identical, verified); claim-graph corpus (30 Liu Hui claims with source
spans + epistemic-stance annotations + train/eval split — the DeepSeek thread offered to
generate it next). Lands on the maze-keeper box or Colab.

## FLEET CONNECTIONS

- Kabuki lesson (single-turn actors hallucinate citations) → anachronism rate + UNCITED
  markers = the measured fix.
- FANGCHENG (B12): Liu Hui as the test subject — the ractor must reason procedurally and
  FAIL to use calculus; anachronism rate is the door's own metric.
- MENGXI: epistemic-stance schema is her native tongue (procedural/axiomatic is the AC/DC
  split); she should annotate the claim graph.
- Persona Pair Registry: every pair runs this experiment on its own subjects.

## LAWS

Pre-register before running (done: conditions/metrics above). Blind scoring. Three greedy
repeats ≠ three independent recoveries. Report what fails first.
