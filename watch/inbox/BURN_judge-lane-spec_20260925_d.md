# BURN: judge-lane-spec pass d (2026-09-26)

## Verdict

steal

## Evidence

- REJECTION_TAXONOMY_20260917.md: "41 rejection rows total. Only 2 are merit rejections"; "39 are infrastructure failures". Infra share = 39/41 = 95.1%. Found this pass: the table sums to 42 (16+11+12+2+1), one row more than the headline 41. All three prior receipts in this lineage grep-verified the file; none summed it.
- The taxonomy carries aggregate class counts only: no row ids, timestamps, or per-task repeats. A baseline repeat-failure rate is uncomputable; the only baseline statistic that exists is infra-class share.
- memory/burns/LEDGER.jsonl: 32 rows; keys exactly ts/slug/verdict/fresh_failure_mode/landing/one_line; failure_class absent (0 grep hits across all rows).
- Fresh web search for judge verdict-schema standards: 429 (z.ai 1302) twice, pass c's cap again. Error layer volunteered synthesized advice; not adopted (no-fabrication law). Owed.
- Fetch 1 landed, arxiv.org/abs/2609.26550 verbatim: "...at 0.36% of the comparator's fee"; "A frozen cascade that accepts confident verdicts and escalates uncertain ones retains 99% of the comparator's accuracy at lower cost." Closes the owed 0.36% vs 0.36x item: abstract says 0.36%; the fold's "0.36x" is wrong. PDF still unread.

## Steal or Vacuous

The fleet adopts the measured baseline plus the measurable falsifier procedure:

1. Baseline (defect-flagged): infra-class share 39/41 = 95.1%, held pending a denominator freeze. The 42-vs-41 self-inconsistency means the canon number is cited-with-defect, not canon-clean.
2. Repeat-failure rate: no baseline exists. Defined intra-burn only: fraction of verdict rows whose normalized failure_detail cluster (CLUSTER_REPORT keying) fires >= 2 times in the burn window. The pass gate compares infra share vs 95.1%; repeat rate is reported, never gated.
3. Comparison procedure: (a) recount raw rows, freeze the denominator; (b) wire GATE_VERDICT_V2 with cascade_exempt_seats [rule] per pass c; (c) run the 50-wide burn; (d) cluster verdict rows by failure_class + normalized detail; (e) pass = infra share < 70% AND >= 20% escalations overturned or upgraded; fail = infra > 85% or 100% upheld (revert to scalar).
4. Lightest ledger schema addition: one optional field failure_class on LEDGER rows, "infra|merit|none" for single-verdict receipts, or a class:count object for burn receipts reporting a verdict population. Makes the falsifier ledger-side measurable at burn time without re-parsing trail files.

Fresh failure mode named: unsummed-census baseline, a census whose table contradicts its own headline, propagated into three canon documents by grep-verification that never summed.

## Falsifier

Pre-registered: recount raw rejection rows pre-burn. If the recount yields anything but 41, correct the 95.1% figure in GOOGLE_CODIRECTOR_STEAL_20260925.md and BURN_JUDGE_LANE_BUILD_20260925.md before the 50-wide gate runs, and evaluate the < 70% pass threshold against the frozen recount, never the unverified 41. If raw rows are unrecoverable, file the baseline approximate and widen pass to < 60% to preserve the strictness margin.

## Bibliography

- watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md (read)
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (read)
- watch/inbox/BURN_judge-lane-spec_20260925.md (read)
- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (read)
- watch/inbox/BURN_judge-lane-spec_20260925_c.md (read)
- watch/inbox/REJECTION_TAXONOMY_20260917.md (read in full)
- memory/burns/LEDGER.jsonl (tail 40 = all 32 rows, read)
- arxiv.org/abs/2609.26550 abstract page (fetched, quotes verbatim)
- Judge verdict-schema web search: owed, 429 z.ai 1302, second consecutive burn
