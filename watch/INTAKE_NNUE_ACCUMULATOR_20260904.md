# INTAKE CARD — Stockfish NNUE / water integrator / discrete-continuous briefing (2026-09-04)

**Paste**: operator's full research briefing (DeepSeek-thread case study:
Stockfish NNUE, Lukyanov 1936 water integrator, the analog revival, liquid
networks). **Score: 18/25 — BUILD WINDOWED** (design note spawned this turn).

**Fact-check spot-pass** (cheap, hand-verifiable claims only): HCE removed in
Stockfish 16.1 (Feb 2024) ✓ · HalfKAv2_hm + accumulator architecture ✓ ·
NNUE = shallow/sparse/incremental/int8-int16/CPU-native ✓ · Lukyanov water
integrator 1936, Karakum Canal, millimeter accuracy ✓. The briefing's
corrections of its own source thread are good faith. Deep NNUE claims
(L1-2560 SFNNv8): plausible, Unproven here.

## The five payloads (each maps to a fleet organ)

1. **THE DIAGRAM**: continuous function wrapped by discrete procedure = the
   dominant working-AI shape ("almost every serious AI system now is a
   Stockfish-shaped object"). Fleet translation: our lanes already live it —
   4.7-flash single-flight cache-miner (the cheap continuous eval, called
   constantly) inside discrete tranche/search loops.
2. **THE CALIBRATION LAW**: "a net that is usually brilliant and occasionally
   insane is poison for alpha-beta — one wild leaf poisons a cutoff."
   → Our planners wrap models the same way: the claim-organ and the queue
   need CALIBRATED receipts, not high-average-quality ones. This is the
   sharpest external statement of why Leg-1 (claim semantics) precedes scale.
3. **THE ACCUMULATOR PRIMITIVE**: NNUE patches a running latent (add/subtract
   the delta) instead of re-encoding the world. Verkle chain is already an
   accumulator (append-only patches). Agents are not: they re-encode every
   turn. Design note spawned — docs/ref/NNUE_ACCUMULATOR_DESIGN_20260904.md.
4. **THE ELO LAW, third confirmation**: Fishtest ships on Elo alone; SPSA
   tunes on it. AlphaEvolve's measurable-objective law, production-proven
   since 2018. The falsifier workbench and march verdicts are the same shape.
5. **THE DISTILLATION VINDICATION**: NNUE = supervised distillation of a
   stronger search into a cheaper eval, then quantization — "closer to how
   production ML actually works than the AlphaZero myth." MAX_DISTILL is
   this pattern; its epoch-1 floor effects match the paper's own constraint
   (frozen weights cap the system — the WHALE finding, again).

## Axes
FIT 4 (compose points into mean_field, percolator, MAX_DISTILL, Leg-1, harness
calibration) · PULL 4 (campaign design + calibration law + Rocinante substrate
notes) · COST 5 ($0) · WINDOW 3 (design note is now-input) · NOVELTY 3
(accumulator-as-agent-primitive is the new frame; Elo/calibration laws are
re-finds, honestly docked).

## Routing
1. **BUILD WINDOWED (spawned)**: NNUE accumulator design note for
   tool-using agents — maps the patch-don't-re-encode pattern onto room
   state, agent context, and the verkle precedent.
2. **REMEMBER (laws)**: calibration-under-planner law → cite in Leg-1 gate;
   Elo law third instance; "human knowledge moved, didn't vanish" → anti-hype
   citation for the campaign (Stage-0 data = domain knowledge in the input
   geometry, exactly like king-centric planes).
3. **Answer to the paste's closing question**: (b) — the accumulator design
   note is the fleet-useful artifact. The (a) architecture sheet variant we
   get for free by substituting our own lanes (4.7-flash miner = NNUE slot;
   5.3-flash 50-wide = the search fan-out) into the Stockfish column.
