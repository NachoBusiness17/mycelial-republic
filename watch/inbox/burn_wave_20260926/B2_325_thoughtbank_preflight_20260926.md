# B2-325 Rocinante thought-bank size preflight (2026-09-26)

## Verdict

LANDED, and the count falsifies the recipe's own assumption: the exportable
fleet thought-bank is 1,841 unique reasoning parts (raw union 1,865), not the
~10K the B2-74 receipt and the UF-130 recipe assume. Consequences, stated
plainly: (1) the corpus sits INSIDE arXiv 2511.00130's measured sweep
(8..8192 samples) but NOT at its top as the receipt claims ("10K reasoning
parts lands at the top of the regime ... validation peaked at 8192") - at
1,841 parts it is ~4.4x below the peak, so the paper's data-scarce conclusions
apply a fortiori and the packing-OFF posture holds; (2) a QLoRA run on the
bank as-is is defensible per the paper, but reaching the assumed 10K needs
roughly 4,200 more parts (about 9 more burn-waves at this one's receipt rate)
before the Oct 27 deadline; (3) trajectory steps.jsonl (22,402 rows) is
tool trajectory (99.9% face=bash), the WRONG corpus class for a reasoning
recipe, and is excluded by name. The count is re-derivable by one command
(falsifier-ready): the persisted preflight script.

## Evidence file:line quotes

- Preflight run 2026-09-26 (B2_325_thoughtbank_preflight.py, results in
  B2_325_thoughtbank_preflight_results.json): per_source_raw
  {"inbox_receipts_md_ge400b": 1467, "burns_ledger_rows": 370,
  "salon_verdict_fold_docs": 6, "trajectory_milestones": 22,
  "trajectory_bash_rows_excluded": 22380}, raw_union 1865,
  "unique_after_dedup": 1841, dedup_rule "sha256 of whitespace-normalized
  text across all sources". (An earlier in-lane pass read 1,859/1,835; the
  tree grew by 6 receipts and 3 ledger rows between passes - the delta is
  live wave activity, and the persisted script is the arbiter.)
- The assumption under test, watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md:5
  "small reasoning corpus (~10K reasoning parts, single 12-24GB GPU)" and :29
  "10K reasoning parts lands at the top of the regime 2511.00130 actually
  measured (validation peaked at '8192 training samples and 6k training
  steps')".
- The steps.jsonl exclusion evidence (this lane, bytes): 22,402 parseable
  rows, faces {bash: 22380, milestone: 22}, 22,402 distinct step_hash (the
  fold's own identity), 9 unparseable lines; sample row is a command/result
  pair, schema trajectory_step.v1.

## Work done

1. Searched the tree for a named thought-bank export: none exists (no
   export command, no corpus manifest under that name); the bank had to be
   defined, so the definition is named in the script docstring and here.
2. Censused candidate sources; rejected tool trajectory as a class (wrong
   corpus type for a reasoning recipe) and kept four prose sources.
3. Wrote the persisted preflight script (source list, >=400B floor, dedup
   rule, JSON results) and ran it twice to expose live-tree drift.
4. Compared to the regime: 1,841 in-range but 4.4x below peak; named the
   growth gap (about 4,200 parts) against the Oct 27 deadline.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This preflight is inverted if any of the following holds: (a) rerunning
B2_325_thoughtbank_preflight.py yields a unique_after_dedup that cannot be
reconciled with 1,841 + receipts-and-ledger-rows landed since (the counter
is not re-derivable, which is the brief's exact falsifier);
(b) a named export surface exists that this lane failed to find (a corpus
manifest or export command producing reasoning parts in a different unit
than file/row; then the count is measuring the wrong unit);
(c) the >=400B floor or the bash-row exclusion is shown wrong, i.e. a real
reasoning part under 400B or a bash row that belongs in a reasoning corpus
(then the definition needs amendment, with a receipt, not silence).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md (read in full:
assumption line 5, regime line 29, falsifier line 37);
memory/trajectory/steps.jsonl (censused, excluded by class with counts);
memory/burns/LEDGER.jsonl (row count); watch/inbox/**/*.md and
memory/runs/**/VERDICT.md+FOLD.md (censused). arXiv 2511.00130 regime
numbers accepted from the B2-74 receipt's byte-verified quotes (same-day
fetch by that lane), not re-fetched. No network calls this lane.
