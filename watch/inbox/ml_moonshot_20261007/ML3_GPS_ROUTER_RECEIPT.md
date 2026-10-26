# ML3 GPS ROUTER v0 (classical) - metrics receipt

Lane ml3-router-classifier, run ml-moonshot-20261007, landed 2026-10-07.
Run command (the only training execution):

```
.venv/Scripts/python.exe tools/gps_router_v0.py
```

Artifacts this receipt cites (all under `watch/inbox/ml_moonshot_20261007/`
unless named otherwise): `ml3_router_metrics.json` (the metrics source for
every number below), `ml3_route_table.json` (25 shapes, full rankings),
`ml3_router_model.joblib` (fitted deployment model), trainer
`tools/gps_router_v0.py`, tests `tests/test_gps_router_v0.py`.

## What was executed

GPS ROUTER v0, classical per the driving-ladder law: sklearn logistic
regression + gradient boosting predict success from (node, animal, task_shape)
on ml1's corpus (`memory/corpus/ml/training/`, lane ml1-ledger-corpus, build
stamp 2026-10-07T16:20:45Z in its `build_manifest.json`). The row shape is the
GPS row contract of `tools/gps_mcp/ledger.py` (verdict_log: ts, model_id,
task_shape, verdict). Unified training frame: 3753 rows (metrics `n_rows`) =
703 gps_verdicts + 12 gauntlet live pass/fail rows + 3038 usage rows (metrics
`source_counts`): verdicts contribute animal=model_id, shape=task_shape,
label=verdict_label; gauntlet contributes its live pass/fail rows (BANKED
excluded per the corpus README splits caution, label=pass_label); usage
contributes node=id prefix, animal=model, shape derived from the id prefix by
the documented USAGE_SHAPE_MAP, label=ok_label.
Class prior 0.7034 (metrics `class_prior`).

## Held-out metrics vs baseline (source: ml3_router_metrics.json)

Primary split is time-based per the corpus README ("train/test by ts to avoid
leakage across the fleet's chronological drift"): oldest 75% train (2814
rows), newest 25% test (939 rows). Secondary: stratified random 75/25, seed 42.

| split | scorer | accuracy | balanced acc | ROC AUC |
|---|---|---|---|---|
| time_75_25 | baseline: percolator hand-tuned score | 0.7135 | 0.5123 | 0.5012 |
| time_75_25 | baseline: ledger capability pass_rate | 0.2812 | 0.4667 | 0.5198 |
| time_75_25 | logistic regression | 0.8754 | 0.8927 | 0.9288 |
| time_75_25 | gradient boosting | 0.8722 | 0.8583 | 0.9434 |
| stratified_75_25 | baseline: percolator hand-tuned score | 0.705 | 0.5039 | 0.4985 |
| stratified_75_25 | baseline: ledger capability pass_rate | 0.3408 | 0.5141 | 0.6067 |
| stratified_75_25 | logistic regression | 0.836 | 0.8356 | 0.9263 |
| stratified_75_25 | gradient boosting | 0.8775 | 0.8859 | 0.9479 |

Headline (primary time split): gradient boosting AUC 0.9434 / accuracy 0.8722
vs the percolator baseline AUC 0.5012 / accuracy 0.7135: +15.87 points
accuracy and +0.4422 AUC over the named hand-tuned baseline; logistic
regression 0.8754 / 0.9288 agrees, so the signal is in the (animal x
task_shape) structure, not in one model family.

Why the percolator baseline sits at chance: its lexicon
(`mag/percolator.py:125-145`, `_classify` at :198-210) scores TEXT, and the
rows that carry the verdict signal (the 703 ledger rows) carry no text; the
baseline degenerates to the training prior there exactly as the trainer's
docstring states. This is a real finding, not a strawman: the estate's $0
hand-tuned scorer cannot see the ledger's own rows, while the classical model
on two categorical features can.

The ledger capability baseline (the incumbent production router:
`capability.pass_rate` per (model, shape)) scores 0.2812 accuracy on the time
split - worse than predicting the majority class (0.7082) - because its
pass_rates encode stale regime mixtures against the newest 25% window. The
learned router supersedes it on both splits.

## The router output (source: ml3_route_table.json)

Evidence-gated routing: best_animal requires >= 5 training rows for that
shape; thin shapes (dice 2 rows, beat 8, grading 8, code-analysis 8,
askbank-v1-safeguard 6, world-tick 4, hourly 4, substance 4, season 2,
metagame 2; all in ml3_route_table.json) return best_animal null with
"do not route" - the ungated argmax routes everything to x-ai/grok-4.7, an
animal whose ledger footprint is 9 of the 703 verdict rows
(memory/corpus/ml/training/gps_verdicts.parquet model_id counts), which is
exactly the thin-sample trap the gate exists for (grok-4.7 remains the gated
pick only where its own shape support clears 5, e.g. adversarial-review,
68 rows, p 0.9615, both numbers in ml3_route_table.json). Gated picks on the fat shapes: tavern-turn (1824 rows) ->
anthropic/claude-haiku-4.5 p 0.9879; dnd-session (905) -> haiku 0.9342;
legality-water-graph-v1 (100) -> legality-propagator-v1 0.9882 (the
specialized tool beats every LLM on its own shape); arena-agreement-v1 (461)
-> opus 0.5227 (the hard shape stays hard); night (44) -> fable 0.2316
(the model knows fable fails; ml1's README measured fable ok mean 0.608).

Known simplification, filed for v1: routing predictions are made under the
majority source context (mode of `source` = usage); ledger-shape picks should
be conditioned on source=gps_verdicts. Animal and task_shape carry the
signal either way, but the context choice is a documented approximation.

## $0-vs-$ comparison (driving-ladder law, part of the receipt)

- Classical lane total paid cost: $0.00 (metrics `cost_block`, key
  classical_lane_paid_cost_usd). Training is local sklearn 1.9.1 on CPU; zero
  API calls; per-decision router inference is one predict_proba on the same
  process.
- The paid alternative measured on the same corpus (all numbers in metrics
  `cost_block`): 2329 usage rows carry cost_usd > 0, total $94.7436 measured
  spend, mean $0.0407 per paid call (per-animal means in
  `mean_cost_per_paid_row_usd_by_animal`: haiku $0.003972 on 672 paid rows up
  to glm-5.3-prime $0.23399 on 7; fable $0.072038). A MIRA-style
  generative-critic router would add one paid judgment per routing decision
  at that measured scale; the classical router instead PREDICTS which paid
  call is worth making (route tavern-turn/dnd-session volume to haiku at
  $0.004/call and keep fable off it at $0.072/call).
- Verdict: classical did not plateau - both model families clear the
  baselines on both splits - so per the driving-ladder law the generative
  critic is correctly DEFERRED, not skipped. Escalate to a paid critic only
  if a v1 rerun on refreshed corpus data drops AUC below ~0.75.

## Deviations and negatives (first-class)

1. The ask's start list said "ml1's corpus"; at lane start the run's lanes
   dir did not exist yet and ml1 landed minutes into this lane's exploration
   (lane file ml1-ledger-corpus.json read at 13:0x). Training used ml1's
   landed corpus as intended; no deviation in the end state.
2. gauntlet contributes only 12 of 3753 rows (BANKED consensus members are
   not pass/fail trials and are excluded per the corpus README); the
   gauntlet table alone is far too small to train on, which is why the frame
   is unified.
3. task_shape for usage rows is a derivation (id prefix map), not a recorded
   field - the derivation is deterministic and documented in the trainer.
4. capability cost_usd_per_call and evidence_resolved are sparse in the db3
   (ml1's gap note), so no credibility weighting was attempted in v0.

## Checks run (this lane, this session)

- `.venv/Scripts/python.exe tools/gps_router_v0.py` - exit 0, artifacts
  landed (the run this receipt reports).
- `.venv/Scripts/python.exe -m pytest -q tests/test_gps_router_v0.py` -
  6 passed in 17.79s.
- `.venv/Scripts/python.exe -m pytest -q tools/gps_mcp` - see lane rows for
  the outcome (read-adjacent surface: the corpus reads gps_ledger.db3).
- `.venv/Scripts/python.exe tools/citation_lint.py check --files
  watch/inbox/ml_moonshot_20261007/ML3_GPS_ROUTER_RECEIPT.md` - result
  recorded in the lane rows.
- `python tools/violation_ratchet.py check --changed` over the new tool -
  result recorded in the lane rows.
- Em-dash/en-dash grep over the new files - result recorded in the lane rows.
