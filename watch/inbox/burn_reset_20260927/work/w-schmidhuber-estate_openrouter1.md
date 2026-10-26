# WORK w-schmidhuber-estate

lane: openrouter model: stealth/space-bunny-alpha
ts: 2026-09-30T01:33:00.824812+00:00
finish: stop cached_tokens: 128
ask: Schmidhuber's compression-progress curiosity (arXiv 0812.4360) applied to our estate: our percolator tracks invariants, our quantizer compiles them into packs, our fossil arm checks staleness. Where in this pipeline should the compression-progress REWARD signal live to make the system genuinely curious? Propose the wiring.

---

1. **FINDING**

The compression-progress **reward signal belongs primarily at the percolator boundary**, where a candidate invariant changes the compressor’s ability to predict or reconstruct recent observations. It should be computed **before and after tentatively incorporating that invariant**, not from whether the quantizer successfully emits a pack.

The quantizer is an actuator. The fossil arm is a verifier and decay monitor. Neither should define curiosity by itself.

Proposed wiring:

```text
observations
    |
    v
percolator
    |-- candidate invariant I_n
    |
    v
counterfactual compression test
    |-- compression loss without I_n: L_before
    |-- compression loss with I_n:    L_after
    |
    v
compression-progress reward
R_n = clip(L_before - L_after - lambda, 0, R_max)
    |
    +--> quantizer compiles I_n into a pack
    |
    +--> fossil arm re-tests I_n against newer observations
              |
              |-- persistent gain: retain reward credit
              `-- decay or contradiction: emit fossil correction,
                  invalidate/revise pack, penalize future credit
```

Use held-out or time-shifted data for the compression test. Otherwise, the reward can reward overfitting or merely rediscover known structure. The fossil arm should feed its validation result back into the same compressor, so rewards for failed invariants can be partially reclaimed.

Do not use:

- pack size reduction alone, because trivial recoding can compress without discovery;
- quantizer success alone, because it rewards compiler behavior rather than explanatory progress;
- fossil novelty alone, because it rewards accumulated data rather than increased compressibility;
- raw reconstruction improvement without a complexity penalty, because an expensive model can always memorize more.

2. **STEALABLE IDEA**

Keep **compression progress as an intrinsic reward measured by counterfactual predictive loss**, but make the invariant lifecycle transactional:

```text
candidate invariant
    -> tentative incorporation
    -> measured predictive gain
    -> pack compilation
    -> temporal validation
    -> retained, revised, or invalidated
```

This separates discovery, compilation, and survival. Curiosity is rewarded at the discovery step; the quantizer makes the discovery durable; the fossil arm determines whether it remains useful.

3. **TESTABLE HYPOTHESIS**

Compared with a quantizer-only reward, wiring compression-progress reward into the percolator will produce:

- lower held-out prediction or reconstruction loss per candidate;
- fewer stale or contradicted invariants entering the quantizer;
- fewer pack revisions caused by fossil checks;
- higher novelty-adjusted predictive gain;
- no increase in compressor size sufficient to erase the net benefit.

A suitable ablation is:

- **A:** pack success reward only;
- **B:** fossil novelty reward only;
- **C:** percolator compression-progress reward, with fossil feedback;
- **D:** C without a complexity penalty or held-out evaluation.

Test whether C dominates A and B on retained, non-stale compression progress:

```text
score = held-out loss reduction - model-complexity cost - staleness penalty
```

4. **EVIDENCE OR OWED**

**Evidence:** Schmidhuber, *Compression Progress: A Novel Measure of Curiosity for Autonomous Agents*, arXiv:0812.4360, supplied by the task. The paper motivates intrinsic reward from improved compression or prediction of data, rather than from external goals.

**OWED:** I cannot verify the implementation-specific behavior of this estate, the exact definitions used by the percolator, quantizer, and fossil arm, or empirical results for the proposed wiring. A source visit or repository inspection is needed to map `L_before`, `L_after`, complexity cost, and fossil staleness to concrete interfaces.
