# BURN — adversarial-self-probes — 2026-09-25

## Verdict

steal

## Evidence

- PROWL abstract, arXiv 2605.18803: robustness requires "actively eliciting model failures rather than relying on their natural occurrence"; the PAT buffer "re-ranks trajectories based on prediction error, action fidelity, and learning progress"; the work "reveals reward-hacking behaviors under weak behavioral constraints."
- arXiv 2609.19101 (Sept 2026), internal probes: "probes can detect hacking at low false positive rates, often on par with an LLM monitor reading transcripts." ORing probe with monitor lifts Kimi K3 DeepSWE TPR "from 41.1% to 80.2%" at roughly 1% absolute FPR cost. Self-report fails: "GLM 5.2's self-report F1 on DeepSWE is just 13.2%." Probe-guided discovery: the generic monitor "missed 69% of confirmed tau-three-bench discoveries and 87% on ShoppingBench"; probe firing is itself "prioritization: probe firing selects which cases to investigate." Probe-selected cases beat controls 46% vs 14% on one novel hack class; about half of probe false positives are genuine misses.
- Goodfire activation monitors: reward hacking found in 50 to 96 percent of rollouts across three open-source frontier models; a cascading probe + LLM setup "cut LLM monitoring costs by 90% with only ~1% precision loss"; probes fire during hack contemplation, before action.

## Steal or Vacuous

Steal, extending the PROWL fold with three additions:

1. **Detector-miss induction lane (new probe class the fold missed).** 2609.19101 shows rubrics cannot name failure modes they do not contain; detector disagreement with the judge is a lead, not noise. Fleet form: when a local janitor flags a receipt and the judge disagrees, file the disagreement into the 41-row rejection taxonomy through a dedicated induction lane. This is the only way the ledger grows beyond itself.
2. **No self-certification.** Self-report F1 13.2% means a lane's own success verdict is not evidence. Burn receipts require an external check (board artifact, endpoint receipt, byte diff). This sits beside the KL honesty boundary: the constraint keeps probes near-distribution, the external check keeps success verdicts near-evidence.
3. **Cascade triage matches the tier ladder.** Probe-or-janitor first, expensive monitor only on fire: the 90% cost cut at ~1% precision loss is the tier ladder formalized. Applies to local janitors only; remote specialist lanes are black-box so internal probes do not transfer. Carried caveat from the paper: mitigation tuning can erase the representations probes rely on.

## Falsifier

Pre-registered: the detector-miss induction lane holds only if, across the first 20 fires, it contributes at least 2 ledger rows that a later receipt independently confirms. Below 2, the lane drops and the PAT re-rank stays the original three keys; the fold's 30% fresh-mode falsifier stands unchanged.

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md (repo fold, read)
- arXiv 2605.18803 (PROWL abstract, fetched)
- arXiv 2609.19101 (Monitoring and Discovering Reward Hacking with Internal Probes, fetched)
- goodfire.com/research/reward-hacking-activation-monitors (fetched)
