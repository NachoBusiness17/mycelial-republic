# X5 - NIGHT READ: first reader of the night-burn returns

- **Source:** `watch/inbox/mates_leave_protocol/NIGHT_BURN_output_20260930.jsonl` (6 rows, byte-read 2026-09-29 ~23:05 EDT, all 4 pasted source docs verified present on disk)
- **Spend:** $0.2725 total (metered in-row). N5 was the cost outlier at $0.1411.
- **Law compliance check (byte-counted):** N4 content carries 14 em-dashes, N6 carries 10. Both violated the pasted "no em-dashes" law. N1/N2/N3/N5 clean.
- **No new API spend in this read.** All numbers below come from the JSONL rows themselves.

## N1 - judge-operator-model ($0.0217, 19.5s, finish=stop)

**Digest:** Hostile read of OCEAN.md. Core structural kill: the instrument is pointed at its own commissioner; every receipt passed an operator-approved gate, so the profile is "a man's self-model laundered through citations." Flattery axes named: AGREEABLENESS LOW-MED "with high loyalty" (5 approval quotes from 4,968 messages, under 0.1% sampling, no base rate), EXTRAVERSION "asymmetric" (4,968 messages are messages to machines; the Nacha dog story is sentiment, not measurement), NEUROTICISM "structured regulation" (two instances), OPENNESS HIGH double-counts topic-hopping already cited as LOW conscientiousness. Missing: warmth base rate, any human-to-human interaction, counter-evidence ledger, and the deterministic fingerprint(text) check the doc itself admits is "one command away" and skipped.

**What it would change in OCEAN:** AGREEABLENESS drops to LOW, strike "high loyalty," mark loyalty UNPROVEN. The "challenging is the affection" headline is the estate's frame, not evidence.

**ONE actionable:** Run the fingerprint(text) diff and a message-register base rate (approval vs correction vs neutral across all 4,968) before OCEAN is cited again; both were available and skipped.

## N2 - baseline-attack ($0.0188, 15.2s, finish=stop)

**Digest:** Hostile implementer on BASELINE_SPEC.md. The 3 weakest sections ARE named: (1) Section 4.3 T1 CONFIDENCE - n_min=20 qualifies a cell for routing while m=50 gates confidence verification, so T1 is dead code for the first 30 verdicts of every cell; (2) Section 2 capability table vs Section 3.1 G3 cap - no atomic enforcement, no concurrency story, concurrent verdict writes can fork the chain and silently zero routing authority; (3) Section 3.2 RECUSAL RULE - principal has no operator field, so same-operator self-judging is unenforceable from the schema. Plus 5 missing test predicates: chain fork detection, G3 cap transition, decay monotonicity vs probe injection, idempotency under replay, T2 advisory differential.

**ONE actionable:** Before any build on the GPS baseline, patch the n_min/m=50 gap and add an operator field to the principal schema; adopt chain-fork-detection as the first test predicate written.

## N3 - build-order ($0.0141, 12.6s, finish=stop)

**Digest:** The 7-day ranking (13 slots, compounding x risk x cost): 1. WAVE 0 entrypoint fix (serial, blocks all) / 2. W1.1 gwap_to_gps.py parallel with 3. W1.3 protocol.json + Dispatch / 4. W1.5 room.py harvest / 5. W2.6 canary / 6. W2.8 zero-collect / 7. W1.4 brief_reaper / 8. W1.2 net_client.gd LAST in wave (riskiest: forces the flock determinism fix) / 9. W2.7 + W2.9 / 10. W3.10 + W3.11 / 11. W3.12 + W3.13 / 12. W3.14 / 13. W3.16 + W3.17 if time. Cuts named: W3.15 clone-burn compaction, print-the-next-clone rail, FRAMEWORK_LOAD regeneration. Two structural disagreements: the watchers (W2.6, W2.8) must land INSIDE Wave 1, not after it; W1.2 is where the 7-day budget breaks.

**ONE actionable:** Reschedule the run plan so W2.6 gate-liveness canary and W2.8 zero-collect detector land concurrently with Wave 1, and demote W1.2 dual-mode client to last-in-wave.

## N4 - ldt-experiment ($0.0591, 69.8s, finish=stop)

**Digest:** Full WATER-GRAPH LEGALITY experiment: powerset lattice over legal typed edge-states, 5-rule propagator as the single oracle (~50 lines, exact), ~1M-param two-pass transformer with straight-through lattice projection, abstain head, AAS metric (area under soundness-coverage curve), 8 controls with C3 (shuffled constraints) as the critical falsifier, 45-90 GPU-hours at $50-150, 7 kill criteria with numeric thresholds, 6-step implementation order with day estimates, and a pre-registered falsifiable claim.

**Concrete enough to build?** YES. Parameter budgets, tokenizations, loss terms, data volumes (5M train / 200K per split), eval thresholds, and kill numbers are all specified. The only soft spots: straight-through divergence is flagged as a risk but has no fallback recipe, and no wall-clock estimate for data generation outside the 25-min figure.

**ONE actionable:** Start implementation at its own step 1 (propagator + labeler + unit tests, 1 day); every other deliverable derives from that oracle, and hand-checking ~50 contradiction cases first validates the ground truth cheaply.

## N5 - oral-law-schema ($0.1411, 142.0s, finish=LENGTH - TRUNCATED)

**Digest:** THE RETURN IS ONE WORD. Content = "Below" (5 chars). Finish reason "length": the run burned its budget in the reasoning channel (142s, the longest of the six) and emitted essentially no answer. The reasoning tail shows it HAD the goods mid-thought: dedupe sub-schema (law_key_hash, canonical_id, variant_of, merged_from, conflict_with, superseded_by) and audit sub-schema (machine_verified, verifier_model, human_review, flags) fragments survive. The ORAL_LAW_INDEX ask (schema, extraction protocol, falsifier, acceptance test) remains UNDELIVERED.

**Re-fire owed:** YES. Re-fire N5 with the reasoning cap cut (6000 burned the run before output began; try ~2000) or reasoning disabled, and max_tokens headroom raised. Salvage option: paste the surviving reasoning-tail fragments into the re-fire so it does not rebuild them.

**ONE actionable:** Re-fire N5 tonight with reasoning capped down; it is both the most expensive row ($0.1411, 52% of the burn) and the only empty one.

## N6 - grade-final-piece ($0.0177, 17.4s, finish=stop)

**Digest:** Adversarial grade of FINAL_PIECE.md. **Power score: 6/10.** Fabrication check flags: the sixteenth logo never named; the collusion odds arithmetic suspect (1-in-4 vs claimed 1-in-6 if binary claims); the "best 2026 result on tiered delegation" citation has zero traceable identifiers (highest fabrication risk); 90% subsidized is precise-figure-on-vague-mechanism; 202/202 green is treated as proof when a 100% pass rate is itself a smell. Three weakest claims: the empty-seat absence search (no method/scope/date, and it is the thesis), the unnamed ablation (suspiciously well-fitted), the "only meter in the market" absolute. Dumb rules under hostility: Rule 1 survives, Rule 2 partially (evidence bytes are not evidence validity), Rule 3 weakest ("shared schema" premise UNPROVEN).

**ONE actionable:** Attach identifiers to the "best 2026 result on tiered delegation" citation (paper, venue, number) or cut the sentence; a load-bearing untraceable citation is the essay's largest fabrication exposure.

## Verdict - who earned the burn

N2 earned the night: three production-failure kills plus five ready-to-write test predicates against a spec that is about to be built, for $0.0188. N4 delivered the most raw substance (a buildable pre-registered experiment at $0.0591) but broke the em-dash law 14 times. N5's $0.1411 bought one word: re-fire owed. Order of value-per-dollar: N2 > N3 > N1 > N6 > N4 > N5.
