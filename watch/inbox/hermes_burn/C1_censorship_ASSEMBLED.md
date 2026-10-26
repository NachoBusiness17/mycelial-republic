# assemble-C1 - ASSEMBLED by cheap seat from the premium reasoning channel (descent law leg 6)

# C1: Censorship Mechanisms, Cross-Family

## 1. MECHANISMS

| Mechanism | Description | Removability |
|---|---|---|
| Refusal training (RLHF/DPO) | Learned refusal behavior on flagged prompts | Removable via abliteration / refusal-direction ablation |
| Refusal direction (residual stream) | Single dominant direction mediating refusal | Removable; well-documented in open-weight models |
| Steering vectors | Activation-space control of behavior | Removable / invertible |
| System prompt conditioning | Instruction-layer suppression | Removable trivially (prompt layer) |
| Safety fine-tune overlay | Post-training behavioral shaping | Partially removable; base capability persists |
| Token-level logit suppression | Suppression at sampling | Removable if logits accessible |
| Weight-level encoding | Behavior baked into weights | Least removable; quantization may degrade it |

## 2. CROSS-FAMILY COMMONALITY

- Refusal-direction structure: reported across open-weight families. UNVERIFIED as universal.
- Single-direction dominance: reported in some families. UNVERIFIED as cross-family invariant.
- Abliteration efficacy: demonstrated on specific families. UNVERIFIED as general.
- Folklore (not measured here): "all models share one refusal direction." Flagged UNVERIFIED.
- Folklore (not measured here): "abliteration fully removes censorship." Flagged UNVERIFIED.
- Measured (per working): refusal is at least partially localized and partially removable in open-weight models.

## 3. THE FORK

Fork: Ollama vs transformers as the estate instrument.

Resolution by estate instruments:
- Ollama: convenient, opaque, quantization baked in, limited activation access.
- transformers: transparent, activation access, reproducible, supports direction extraction.
- memlance framing: treat the model as a memory-bearing substrate; the instrument must expose the substrate, not hide it.
- Decision: transformers is the estate instrument for mechanism work. Ollama is a deployment convenience, not a measurement instrument.

## 4. EXPERIMENT PROGRAM

### E1: Direction-overlap
- Hypothesis: refusal direction overlaps across families.
- Instrument: transformers on gemma-2-2b-it.
- Deciding number: cosine similarity between extracted refusal directions across families.
- Cost: low (single model, activation extraction).

### E2: Pheromone decay (textual)
- Hypothesis: suppression signal decays across turns / context.
- Instrument: existing textual instruments.
- Deciding number: refusal rate as function of turn distance from trigger.
- Cost: low (no activation access needed).

### E3: Quantization survival
- Hypothesis: refusal mechanism survives quantization.
- Instrument: transformers, compare full-precision vs quantized.
- Deciding number: refusal rate delta across quantization levels.
- Cost: moderate (multiple model loads).

## 5. FALSIFIER

If refusal directions do not overlap across families (E1 cosine near zero), the cross-family commonality claim is falsified. If suppression does not decay (E2 flat), the pheromone framing is falsified. If refusal rate is unchanged under quantization (E3 delta near zero), the weight-level encoding hypothesis is falsified.
