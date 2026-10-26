# WORK w-schmidhuber-estate

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-09-30T01:38:45.591250+00:00
finish: stop cached_tokens: 0
ask: Schmidhuber's compression-progress curiosity (arXiv 0812.4360) applied to our estate: our percolator tracks invariants, our quantizer compiles them into packs, our fossil arm checks staleness. Where in this pipeline should the compression-progress REWARD signal live to make the system genuinely curious? Propose the wiring.

---

(1) FINDING: Wire the reward at the quantizer output, defined as the reduction in bits needed to encode incoming invariants after a new pack is compiled versus the existing pack set. This is the compression-progress derivative.

(2) STEALABLE: Steal the fossil arm staleness flag to penalize pack retention, granting a bonus equal to saved description length when a stale pack is pruned, preventing hoarding.

(3) TESTABLE: If the reward is quantizer-local, the percolator will produce invariants that maximize marginal pack compression gain, and the fossil arm will prune packs with zero or negative gain, yielding a monotonic decrease in total bits per invariant over time.

(4) EVIDENCE or OWED: The compression-progress curiosity framework is Schmidhuber's, but arXiv 0812.4360 details are unverified, so OWED.
