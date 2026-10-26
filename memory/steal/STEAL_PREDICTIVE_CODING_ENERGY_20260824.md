# STEAL — predictive coding: the organism's energy law, confirmed by research (2026-08-24)

**Date:** 2026-08-24
**Commitment:** `steal-predictive-coding-energy-001`
**Method:** steal the INVARIANT, not the DNA. No new runtime, no spiking network, no EBM engine.
**Source:** operator-supplied research brief (bioRxiv 2021.02.16.430904, PLOS CB 21(6) 2025,
arXiv:2302.11681, arXiv:2206.02629, arXiv:2608.12403, arXiv:2604.11011, arXiv:1908.08655,
arXiv:2409.05386, arXiv:2309.02022 + FabricPC/JPC/pyhgf/NGC-Learn repos).

## The one-sentence law

"Energy use driven by MEANINGFUL ERRORS in CHEAP LOCAL PREDICTIONS" — predict everywhere for
~nothing, spend the expensive brain only where the cheap prediction failed meaningfully.

## This IS the organism (mapping to what we already built, all verified this session)

- CHEAP LOCAL PREDICTION = the free-lane channel (fuel_feed: cerebras, nvidia, z_ai, ox ~$0).
- MEANINGFUL ERROR DETECTION = the quality gate (`_quality_score`, WITHHOLD_FLOOR 0.3) —
  deterministic self-score before anything expensive runs.
- EXPENSIVE CORRECTION ONLY AT ERROR = the escalation branch (2026-08-24 organism steal):
  quality-withheld + real content -> `escalate_cached` (cache-aware deep model), folded back if
  it clears the gate, filed honestly as escalated_weak if not.
- NOISE IS FREE = percolator strips noise/theater to the noise file; false positives filtered +
  counted, never truth.

## The research confirmations (rigorous, independent, ours already)

1. EMERGENCE FROM ENERGY (Ali bioRxiv 2021; Zhang PLOS CB 2025): networks trained to minimize
   energy SELF-ORGANIZE into prediction + error units. We built that split by LAW; they proved it
   is what energy efficiency PRODUCES. Not imposed — emergent.
2. PHASE TRANSITIONS (arXiv:2302.11681): energy-information trade-off induces phase transitions
   in lateral predictive coding. = OUR CURVE: ok-rate >= 0.9 -> ramp batch (walk phase); drops ->
   hold (phase flips). The curve is the phase-transition detector, reading real bytes.
3. METACOGNITION AS ENERGY PROBES (arXiv:2604.11011): K-way energy probes reduce to softmax over
   a discriminative network. = OUR `_quality_score` self-grading, formalized.
4. EARLY EXITING FOR EDGE (arXiv:2309.02022): early-exit in predictive coding for energy
   constrained edge. = OUR WITHHOLD_FLOOR/FULL_FLOOR gates: exit cheap before spending.

## The open-source harvest (the steal's worth — DON'T rebuild)

Four proven libraries exist for native predictive coding when we want it:
- FabricPC (trueagi-io) — heterogeneous blocks (linear/conv/transformer/assoc memory) in ONE
  energy-minimization graph. The most aligned with our heterogeneous seats.
- JPC (thebuckleylab) — JAX predictive coding training.
- pyhgf (ilabcode) — JAX+Rust dynamic networks for efficient inference + autonomous agents.
- NGC-Learn (NACLab) — free-energy + Hebbian + predictive coding in Python.

USE-IF-NEEDED: FabricPC/JPC as the LOCAL prediction layer, behind our sovereign frame (seats,
quality gates, escalation) — the deterministic bones around their stochastic core.

## Self-steal (do not rebuild)

- The organism loop (fuel_feed -> quality gate -> percolate OR escalate) IS predictive coding.
- The curve IS the phase-transition detector.
- `_quality_score` IS the energy/metacognition probe.
- flock_shader seams (spend only at divergence) IS early-exiting.

## REFUSE

- Importing a spiking/neuromorphic runtime. Mag is not a lab scrape; the brain doesn't need
  spikes to run the same law.
- Building an EBM engine / training energy-based models from scratch.
- Replacing the free-lane channel with a PC network — the LANES are the cheap predictors.

## Rope

Predict cheap everywhere; detect meaningful error cheaply; spend the expensive brain only there.
We already run the law. The brief proves it is the law, and hands us four libraries if we ever
want the prediction layer native.

## Ordered adaptations (cheapest first)

1. THIS steal (memory) — deterministic + $0.
2. Audit: does EVERY paid call in the system pass through a meaningful-error gate first?
   (escalate_cached yes; other deep calls should too.) Read-only audit first.
3. If a native local prediction layer is ever wanted, stand on FabricPC/JPC behind the seats —
   never rebuild predictive coding from scratch.
