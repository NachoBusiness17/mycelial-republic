# BURN adversarial-self-probes 2026-09-25 (_c)

## Verdict

steal

## Evidence

- PROWL falsifier, PROWL_STEAL_20260925.md: the fraction of receipts naming a previously-unseen failure mode must be "above 30% over the first 20 fires" or "the prioritization is vacuous and reverts to round-robin."
- Measured on memory/burns/LEDGER.jsonl, 22 rows read in full: 7 fires of 3 parallel receipts each (10:05:50Z, 12:06:25Z, 14:06:12Z, 19:09:30Z, 19:19:25Z, 20:11:46Z, 22:06:55Z) plus 1 identifiable offpeak deep dive (judge-lane-spec build order, 10:17:30Z, single topic, matches the manifest's "offpeak idle tasks carry single-topic deep dives"). Fire receipts: 21. fresh_failure_mode true: 19. The only false fire rows: roblox-durable-lane ("PAT: green, topic demotes") and stego-canon-pipeline first pass. Fraction 19/21 = 90.5%; capped at first 20 fire receipts in file order: 18/20 = 90%.
- Ledger row 22:06:55Z, prompt-uplift-lane_c: "prompt-inflation charge withdrawn", inverting the pass-b fresh mode "prompt inflation as optimizer win condition". A named-then-retracted mode still sits in per-topic fresh and unresolved counts unless the retraction is applied against the naming row.
- Fatemi, Prioritized Replay for RL Post-training, arXiv 2601.02648 abstract (fetched): problems are selected "according to a simple, model-driven priority score derived from empirical success statistics" that "requires no predefined difficulty tiers, auxiliary predictors, or external labels".

## Steal or Vacuous

Steal, the measurement pass:

1. Falsifier verdict: PASS. 90.5% fresh-mode concentration over 21 fire receipts is triple the 30% bar; the PAT prioritization stands and no revert to round-robin fires.
2. PAT re-rank applied (unresolved-failure count, in-distribution, recency). All ten manifest topics are in-distribution lanes. Unresolved fresh modes (no adopted or pre-registered fix): free-resource-landscape 2 (plan-toggle attribution drift, headline-quote doctrine truncation); rsi-harness 2 (adaptive overfitting to own eval set, junk-retrieval masking); prompt-uplift-lane 1 (snippet direction inversion); world-models-multi-agent 1 (unreachable-verdict by path-guessing); stego-canon-pipeline 1 (repurposed-handle denominator contamination); steering-theory 1 (escalation theater); judge-lane-spec 0 (confidence-by-construction fix pre-registered); queue-field 0; adversarial-self-probes 0 (rubric blindness, self-certification, confirmation laundering all carry adopted fixes); roblox-durable-lane 0 and green, demoted.
3. Next-fire queue (top 3): free-resource-landscape, rsi-harness, prompt-uplift-lane.
4. Fresh mode named: withdrawn-charge residue. A failure mode retracted by a later receipt remains counted as fresh and unresolved unless the retraction is ledgered against the naming row. Fix adopted here: per-topic counts drop a charge only when a ledger row names the withdrawal, applied to prompt-uplift-lane's prompt inflation.

## Falsifier

none proposed

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md (read)
- watch/inbox/BURN_adversarial-self-probes_20260925.md (read)
- watch/inbox/BURN_adversarial-self-probes_20260925_b.md (read)
- memory/burns/LEDGER.jsonl (read, full, 22 rows)
- memory/burns/MANIFEST.json (read)
- arXiv 2601.02648 abstract, Prioritized Replay for RL Post-training (fetched)
