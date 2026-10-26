# BURN: judge-lane-spec pass e (2026-09-26)

## Verdict

steal

## Evidence

- memory/burns/LEDGER.jsonl read in full: 65 rows, 33 added since pass d (32). failure_class adopted by ZERO writers: grep for `"failure_class"` as a key returns 0; the only hit is row 34's own text, "one optional failure_class field".
- C8 check (due at row 56, run at 65): marker-strict match (falsifier, prereg, pre-registered, receipt) gives 24 receipts-attached vs 41 bare; adding kill/pass/reject-text rows without marker words (19, 24, 27, 30, 35, 54) gives 30 vs 35. Both clear min-10.
- Overturn test: 2 clear events. Row 7 "43 open items" corrected by row 16 "census corrected 43 -> 35 true-open" (attached). Row 13 "GEPA edge partly via 9.2x longer prompts" withdrawn by row 22 "INVERTS the pass-b watch item... prompt-inflation charge withdrawn", confirmed dead by row 54 (bare). Borderline: row 33 "Cerebras triple-dead" vs 50 "key answering HTTP 200" / 52 "cerebras 402 no-credit" (docs vs API surface). Row 2 vindicated not overturned: 34/49 corrected the SIX_DROPS 0.36x fold row 2 had flagged. Rate: attached 1/24, bare 1-2/41; direction flips on the borderline. Row 39: "convention must be pinned or the every-20-rows checks are not comparable"; at 2-3 events the rate is unreadable.
- Baseline: row 49 F3 "taxonomy baseline 39/41 vs 40/42 both ~95%"; row 60, 304 loop_gaps rows: "293 infra (96.4 pct...)", "rejection-taxonomy finding holds on merit axis (100 pct non-merit vs 95.1) but class taxonomy does not transfer".
- Schema drift: fresh_failure_mode holds prose strings (rows 36, 46, 50); verdict field prose in 10+ rows ("prereg gated; one red finding").
- Fresh web: arXiv 2601.15195 (MSR 2026, fetched): 33k agent PRs, 600 coded into a "hierarchical taxonomy of rejection patterns": "Lack of meaningful reviewer engagement, Duplicate PRs, Unwanted feature implementations, Agent misalignment"; rejected PRs "often fail CI/CD validation".

## Steal or Vacuous

1. Second C8 check filed: classes 30/35 (tolerance) or 24/41 (marker-strict), both over min-10; overturn direction NOT established at 2-3 events. Keep every-20-rows as event logging; never gate on rate below 10 events.
2. failure_class dead as a per-burn ask (0 of 33 new rows): re-propose once as a burn-wave writer default, withdraw if the next wave omits it too.
3. Baseline upgraded: infra share ~95-96% holds on two populations (taxonomy, loop_gaps 293/304); the <70% gate keeps margin regardless of the 41-vs-42 denominator.
4. CLUSTER_REPORT shape from MSR 2601.15195: hierarchical taxonomy, pinned class names; add duplicate and agent-misalignment classes; declare cluster keys per population since class taxonomy does not transfer.
5. New failure mode named: ledger schema drift (verdict enum diluted to prose, boolean fresh_failure_mode carrying strings): the ledger is unreadable to machine gates.

## Falsifier

Pre-registered: pin the C8 convention as marker-strict regex over row content (falsifier|prereg|pre-registered|receipt) plus explicit kill/pass/reject criteria. Next check at row 85. If fewer than 10 overturn events exist by then, demote the per-class rate check to event logging permanently.

## Bibliography

- Read: watch/inbox/ GOOGLE_CODIRECTOR_STEAL_20260925.md, SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md, BURN_judge-lane-spec_20260925_d.md; memory/burns/LEDGER.jsonl (all 65 rows)
- Fetched: arxiv.org/abs/2601.15195 abstract (quotes verbatim; PDF owed)
- Owed: TechTimes, lokeshreddy.dev (titles only, unfetched)
