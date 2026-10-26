# WORK w-schmidhuber-estate

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-09-30T01:44:24.315945+00:00
finish: stop cached_tokens: 204
ask: Schmidhuber's compression-progress curiosity (arXiv 0812.4360) applied to our estate: our percolator tracks invariants, our quantizer compiles them into packs, our fossil arm checks staleness. Where in this pipeline should the compression-progress REWARD signal live to make the system genuinely curious? Propose the wiring.

---

FINDING
I have no verified internal documentation or verified external citation confirming where the compression-progress reward signal should be placed in your specific percolator → quantizer → fossil arm pipeline. The arXiv paper 0812.4360 describes compression progress curiosity in general terms only. No sources exist in my accessible context to verify your estate's architecture details.

STEALABLE idea worth keeping
Place the compression-progress reward signal at the quantizer compile-to-pack boundary, not at percolator invariant tracking nor at fossil staleness check. Compute reward as reduction in description length of the invariant set produced by percolator when encoded by the quantizer, i.e. reward = L_prev - L_curr for the pack. This keeps curiosity driven by model improvement rather than raw data novelty.

TESTABLE hypothesis
If the reward is emitted at quantizer output and fed back as an intrinsic bonus to percolator invariant proposal rate, then average bits per invariant per pack will decrease faster than with reward at percolator input or fossil arm alone.

EVIDENCE or OWED
OWED. No verifiable evidence for your estate's percolator, quantizer, or fossil arm implementation, and no citation confirming the optimal placement of the compression-progress reward in this specific pipeline.
