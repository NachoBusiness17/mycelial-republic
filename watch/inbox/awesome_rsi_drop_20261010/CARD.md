# AWESOME RSI drop card (operator link, 2026-10-10)

Source read first-hand: github.com/lobehub/awesome-rsi README (raw fetch). Community
research map of Recursive Self-Improvement: "processes in which AI systems improve their
own capabilities and can also improve the mechanisms that generate subsequent
improvements." Honest caveat carried in their own intro: "Not every work listed here
demonstrates RSI in the strict sense. Some represent bounded self-improvement."

## Their taxonomy (sections)

Model-level (self-training/self-reward, synthetic data/self-distillation, self-play,
self-taught reasoning); Harness-level (prompt/program optimization, CONTEXT AND MEMORY
EVOLUTION, harness/scaffold evolution, extensible harness substrates, self-verification
and self-correction, self-evolving agent frameworks); Multi-agent (co-evolution,
INFERENCE-TIME DEBATE); Coding/SE (self-modifying coding agents, iterative repair);
Automated AI R&D; Embodied and physical; Benchmarks; Safety.

## Where the estate sits in their map (the honest position)

- HARNESS-LEVEL RSI IS OUR LAYER, and we run the full loop they describe: the estate
  improves the mechanisms that generate improvements (gap-analysis -> fill-ball ->
  ractor on the ambiguous -> improve --once -> ratchet that never loosens). The tools
  improve the tools.
- CONTEXT AND MEMORY EVOLUTION: ribs, receipts, verkle knots, zknot, the seed-rib. Our
  distinct claim nobody on the list carries: the self-improvement substrate is
  CRYPTOGRAPHICALLY AUDITABLE (verkle proofs, sha256-pinned receipts, sealed bounded
  pointers) - improvement claims are checkable, not narrative.
- SELF-VERIFICATION AND SELF-CORRECTION: our falsifier law + the dead-salmon controls
  (random-model/label-shuffle arms on any self-grading). The answer to "who checks the
  grader" the RSI field is still asking.
- INFERENCE-TIME DEBATE = the academic name for the singing network's heterogeneous
  consensus layer. GB's "nodes confirm the ability of different models to generate a
  consensus answer" IS inference-time debate with economic settlement - naming gift for
  the design doc and the pitch.
- MULTI-AGENT CO-EVOLUTION: ractors, lenses, pheromone swarms, the gala divisions.
- MODEL-LEVEL: we deliberately do not touch weights yet (GPS verdict: strings win at
  our scale); the JIT fine-tuning law (today's coinage) names the mechanism for when
  we do - the pitfall-bypass corpus is the dataset class their Self-Distillation
  section formalizes.
- EMBODIED: nascent (DF/ROBLOX mountain, Lumena browser agent).

## What to steal (ranked)

1. THE NAMING LAYER: "inference-time debate," "bounded self-improvement," "harness
   evolution" - vocabulary that slots our instruments into the field's index. The
   singing-network synthesis should use their terms.
2. THE BENCHMARK SECTION as our honesty check: our evals are task-shaped and ad hoc
   (dogfood matrix, GPS ledger); their benchmark list is the reference set the
   consensus harness can adopt for cross-model comparability.
3. THE SAFETY SECTION mapped onto our gates (ratchet/citation-lint/workflow-gate =
   self-modification safety in their language). A positioning piece exists here: "RSI
   with receipts" - the audit-substrate gap in their list is our slot.
4. The citation corpus itself: primary sources for the OLM register and any future
   magatama-steal-class deep read.

## Falsifier

If the estate's loop cannot show, from bytes, at least one improvement per wave to the
IMPROVING MECHANISM ITSELF (not just outputs), we are bounded self-improvement wearing
the RSI badge - their caveat, applied to us first.
