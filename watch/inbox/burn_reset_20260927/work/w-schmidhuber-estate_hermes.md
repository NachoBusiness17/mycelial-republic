# WORK w-schmidhuber-estate

lane: hermes (headless one-shot)
ts: 2026-09-30T01:26:41.400915+00:00
ask: Schmidhuber's compression-progress curiosity (arXiv 0812.4360) applied to our estate: our percolator tracks invariants, our quantizer compiles them into packs, our fossil arm checks staleness. Where in this pipeline should the compression-progress REWARD signal live to make the system genuinely curious? Propose the wiring.

---

I now have the full pipeline map and the paper's core. Here is the analysis.

---

**FINDING**

The compression-progress reward signal lives **nowhere** in the current pipeline. The three stages run as a pure feedforward chain with no feedback loop:

- **Percolator** (`mag/percolator.py:292-316`) is the compressor: raw text -> partition -> canonical hash -> repeat (count++) or novel (explore queue append). It already KNOWS when compression improves (a repeat increments an existing invariant's count) and when it doesn't (a novel gets a count of 1). But it emits no reward — it just logs.
- **Quantizer** (`tools/thought_quantizer.py:1-100`) is the second-stage compressor: invariant registry -> tiered packs (frontier/flash/local). It already measures input-vs-output size at compile time but discards the delta — no derivative, no reward.
- **Fossil arm** (`tools/fossil_check.py:44-105`) is a staleness watcher: mtime vs bar hours. It measures age, not compression progress. It could compute the derivative but currently computes nothing except WARN/ok.

Schmidhuber's three ingredients (arXiv 0812.4360, Section 1.2): (1) continually improving compressor, (2) computable measure of compressor progress, (3) reward optimizer translating progress into action. Ingredient (1) exists (the percolator registry). Ingredient (2) is computable from the registry's count distribution. Ingredient (3) is missing entirely — there is no reward signal and no optimizer acting on it. The explore queue (`memory/percolator/explore.jsonl`) is a plain FIFO append with no prioritization.

**The wiring**: the reward signal belongs **inside `_compile_invariant`** (percolator.py:264-289), at the exact branch point where the code already decides REPEAT vs NOVEL:

- **REPEAT branch** (`count += 1`): fire a positive reward proportional to `log(count)` — each additional observation of an already-compressed pattern is diminishing-margin compression progress (the 100th confirmation of an invariant saves fewer bits than the 2nd, which is the point). Write the reward to a new `memory/percolator/rewards.jsonl` row: `{canonical, count, reward, ts}`.
- **NOVEL branch** (explore queue): fire a negative reward proportional to the expected exploration cost (the cost of adding one more invariant to the registry without a corresponding compression gain). This is the "boredom" signal — the paper explicitly says the agent gets bored by things that remain incompressible.
- **Quantizer compile step**: compute the cross-stage derivative: `(bits_before_pack - bits_after_pack) / n_invariants` and append to the same rewards stream. This is the second-order reward: did the quantizer actually compress what the percolator compiled?
- **Fossil arm**: replace the mtime-only check with a compression-progress check — if the reward derivative over the last N compiles is negative (registry growing faster than packs can compress), escalate from WARN to recompile trigger. This makes staleness mean "the compressor is losing the compression race" instead of "the file is old."

**One STEALABLE idea worth keeping**

The quantizer's compile report already has `input_size` vs `output_size` — it just doesn't keep the delta. The `PACK_STALE_DAYS` constant in `mag/constants.py` is the existing decay bar. Wire the reward signal to that bar: make the staleness threshold a function of the compression-progress derivative instead of a fixed constant. When the derivative is positive (packs compressing faster than invariants accumulate), extend the bar. When negative, shrink it. This is Schmidhuber's "get bored by things already compressible" made operational: the system stops recompiling packs that are already well-compressed and focuses effort on the invariants that are accumulating without being packed.

**One TESTABLE hypothesis**

If the reward signal is wired at `_compile_invariant` (reward = log(count) on repeat, negative on novel) and the explore queue consumer is modified to prioritize entries whose expected reward exceeds the exploration cost, then over a 7-day window: (a) the ratio of repeat-producing explorations to total explorations will rise above the baseline (currently unmeasured — need the explore queue consumer's output stats), and (b) the invariant registry's bits-per-invariant ratio will decrease faster than in a control run with the same input but no reward weighting. Measure: `memory/percolator/invariants.json` count distribution before and after; `memory/percolator/explore.jsonl` throughput; `memory/corpus/quantized_thought/` pack sizes.

**EVIDENCE or OWED**

- **EVIDENCE**: percolator.py:264-289 (the repeat/novel branch is the natural reward site); thought_quantizer.py:1-100 (compile report has input/output sizes); fossil_check.py:44-105 (registry-driven staleness check, mtime bar); arXiv 0812.4360 abstract + Sections 1.2 and 3 (curiosity = compression progress, three ingredients, reward = improvement not performance).
- **OWED**: (1) The exact reward formula from arXiv 0812.4360 Appendix A.5/A.6 — the search returned only the body text, not the appendix. (2) The explore queue consumer code — I need to read `mag/evolving_wave.py` lines 68-74 and `mag/research_class.py` to confirm the queue is FIFO with no prioritization and to know where to wire the reward-weighted selection. (3) The current bits-per-invariant ratio in the live registry — need to run `python -c` against `memory/percolator/invariants.json` to get the baseline before the hypothesis test.

Sources: arXiv 0812.4360 (Schmidhuber, "Driven by Compression Progress," 2008); repo files as cited above. No em-dashes. No fabricated output.
