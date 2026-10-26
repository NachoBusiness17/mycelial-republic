# MASTER FOLD - ML MOONSHOT (run ml-moonshot-20261007)

- run: ml-moonshot-20261007 (MICKEY-17 v2.1, genre: execute), 8 lanes, 38 rows
- folded_at: 2026-10-07T23:09:28Z, fold script sha256 58bd72c79c6d. The script's sections are authoritative; this fold writes prose around them.
- lane archive: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/lanes` (8 lane JSON + 8 persisted checks files)
- fold rule: every steal sentence carries lane id + row index; every number comes from the scripted sections, the lane files, or the persisted verifier verdicts shipped with the fold. Folder arithmetic is labeled where it appears.

## CASUALTY HEADER (script, verbatim)

- fired: 8
- landed (parseable files): 8
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.
- tombstones: [] (scripted run metadata: `tombstoned: []`, `refired: []`; nothing subtracted from owed)

## SCOREBOARD (script, verbatim)

- rows: 38
- estate_status: executed 36, executed-with-deviation 2
- leverage: high 21, medium 16, low 1

## PRISMA FLOW (script, verbatim)

- identified: 38
- screened: 38 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 38
- invariant: identified == included + excluded **HOLDS** (38 = 38 + 0)

## EXECUTIONS - TOP-K (script-computed, 12 steals, all [high])

The script's TOP-K rule: a lane-claimed top steal outside this list files as DISPUTED. No lane file makes a top-steal claim outside the list (no row carries an explicit top-steal marker; the 12 entries are the high-leverage rows of ml1/ml2/ml3/ml4), so disputed = 0. Verdict grammar: tier-1 `supports` from the persisted checks files (38 rows total: 22 yes / 16 no), `deep_tier2` from the gate's byte-checks (12 checks run, 12 verified).

### 1. ml1-ledger-corpus#0 - the labeled corpus [high]
- claim: Built the labeled corpus at memory/corpus/ml/training/: 7 tables, each as parquet AND csv (gauntlet 16, usage 3038, registry 160, gps_capability 30, gps_verdicts 703, trail_events 8591, incidents 14), pandas 3.0.6 backed, plus build_manifest.json pinning per-source sha256 and all 12 trail lane files. Verified parquet/csv row parity by pandas read-back on every table.
- quote: `trail_events: 8591 rows from dashboard/static/trails/*.jsonl`
- source: `memory/corpus/ml/training/build_manifest.json`
- verdicts: tier-1 supports=no (the quote proves only the trail_events count); deep_tier2=verified (gate re-ran the read-back: all 7 tables parquet==csv with exact claimed counts, ALL_TABLES_OK; manifest pins 4 source sha256 + exactly 12 trail lanes. Honest drift finding: 5 sources appended post-build, 4 trail lanes plus the gauntlet register, so current source hashes no longer all match pins; snapshot-vs-live, stated as found, not a fabrication signal).

### 2. ml1-ledger-corpus#1 - incidents measured from bytes [high]
- claim: Incidents are labeled failures measured from bytes, not hand-copied: errno-22 per lane (research 513 and night 26 match register D6 exactly; builder measures 378 = 370 own CYCLE_FAIL + 8 TESUJI_DROP hearsay, D6 says 370), night march_rc=1 measures exactly 28 matching D8, elder 429 rows measure 15 vs the 14-day streak (one 2026-09-18 manual 429-fallback cycle), plus receipt-anchored rows for the dwf 1302 storm (896), the stash sweep (R3, 3 stashes) and its detector cure, and the struck 191.8M phantom number.
- quote: `night march_rc==1: 28 | monitor_rc==0: 30 ... errno22 rows: research 513, builder 378, night 26`
- source: `memory/corpus/ml/training/incidents.csv`
- verdicts: tier-1 supports=no (the quote is a garbled paraphrase: double-equals grammar plus an injected monitor_rc clause exist nowhere in the CSV; disclosed, not silently passed); deep_tier2=verified (the gate re-derived every number from disk bytes: errno-22 research 513 / night 26 matching register D6, march rc=1 = 28 matching D8, elder 429 = 15 vs register 14 as the label-noise pair, builder 378 = 370 CYCLE_FAIL + 8 TESUJI_DROP reproducing from the landed instrument, and all receipt-anchored rows byte-found).

### 3. ml1-ledger-corpus#2 - feature columns documented [high]
- claim: Feature columns documented in README.md (what predicts what): gauntlet onsets_total predicts beat verdict (6/8-count trials PASS at frac 1.00, the 12-count trial FAILs at 0.25); usage model predicts cost (haiku 0.0040 to glm-prime 0.2340) and ok rate (haiku 1.000 to fable 0.608), and only 8 of 726 not-ok rows carry an error string; registry new_digest does NOT predict verdict (PASS 0.769 new vs 0.765 rerun) while g4_salvage and g3_steering are the most-failed checks (16 each on 29 FAIL rows).
- quote: `the 6-count and both 8-count trials PASS at frac 1.00; the 12-count trial FAILs at frac 0.25`
- source: `memory/corpus/ml/training/README.md`
- verdicts: tier-1 supports=no (quote covers only the gauntlet section); deep_tier2=verified (quote byte-found at README.md:113-114; the gate independently reproduced the usage cost/ok-rate numbers, the 8-of-726 error-string count, the registry 0.769-vs-0.765 non-prediction, and g4_salvage/g3_steering at 16 each).

### 4. ml2-nasa-circuitry-census#0 - lineage census receipt [high]
- claim: Lineage census receipt landed: 142-file NASA NTRS shelf classified into defect-dataset / code-standard / simulator shapes, plus pc_* analog-compute bytes, electronics canon, RL phases, interference-search, and the 2026-09-20 physical-compute self-steal; trainable-from-shelves list of 5 items.
- quote: `NEGATIVE FINDING (first-class): the JPL/NASA "Power of 10" coding rules and Drexler rod-logic are NOT on the shelves.`
- source: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/ML2_NASA_CIRCUITRY_LINEAGE_CENSUS.md`
- verdicts: tier-1 supports=no (the quote is the negative finding, not the census execution); deep_tier2=verified (quote byte-found at receipt lines 21-22; gate re-counted exactly 142 files, 72 txt + 70 pdf, on disk; all shelf classes, the 5 pc_*.txt files, 12 RL phase dirs, the 255,053-byte interference-search artifact, and the 8,008-byte self-steal pack each re-measured. One counting imprecision noted: electronics canon "27 files" reconciles as flat entries vs 30 recursive; shelf and class otherwise confirmed).

### 5. ml2-nasa-circuitry-census#1 - defect-frame builder [high]
- claim: Defect-frame builder executed with .venv/Scripts/python.exe: one row per mag/+tools/ .py module, features from module bytes + git log, labels from configs/violation_baseline.json + configs/citation_lint_baseline.json + fix-like commits (NASA MDP defect-dataset shape on estate code).
- quote: `modules=1443 defect_prone=1055 (73.1%) in_violation_baseline=767 in_citation_lint_baseline=1 total_loc=415702`
- source: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/lanes/ml2_build_defect_frame.py`
- verdicts: tier-1 supports=yes; deep_tier2=verified (quote byte-found in three landed files; 1,443 rows by wc -l; 1,055 true / 388 false; 767 in_violation_baseline; 1 in_citation_lint_baseline; loc sum 415,702; label logic 0 violations over all rows; the mag/agent_cli.py 22-commits / 8-fixes row re-derived independently from git log. Tree drift +9 modules post-build, consistent).

### 6. ml2-nasa-circuitry-census#2 - the defect dataset [high]
- claim: Dataset landed and byte-verified: 1,443 JSONL rows (1,055 defect_prone true / 388 false); first row is mag/agent_cli.py with 8 fixes over 22 commits, 3,205 LOC, ratchet rules except-pass + file-too-long.
- quote: `"module": "mag/agent_cli.py", "loc": 3205, "is_test": false, "commits": 22, "fix_commits": 8, "last_fix_date": "2026-09-28", "in_violation_baseline": true, "in_citation_lint_baseline": false, "violation_rules": ["except-pass", "file-too-long"], "defect_prone": true`
- source: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/lanes/ml2_defect_frame_v1.jsonl`
- verdicts: tier-1 supports=yes (the quote is verbatim first-row JSONL matching every stated detail); no dedicated deep check ran on this row (tier-2 byte-check named as owed by tier-1); the deep check on ml2#1 independently verified the same artifact (1,443 rows, first-row byte-match, 1,055/388 split).

### 7. ml3-router-classifier#0 - GPS router v0 landed and executed [high]
- claim: GPS ROUTER v0 trainer landed at tools/gps_router_v0.py and executed to exit 0 (.venv/Scripts/python.exe tools/gps_router_v0.py): unifies ml1's corpus into the GPS row contract (node, animal, task_shape) -> success per tools/gps_mcp/ledger.py verdict_log schema, 3753 rows / 25 task shapes / 17 animals, and lands metrics + route table + fitted joblib model under watch/inbox/ml_moonshot_20261007/.
- quote: `"source_counts": { "usage": 3038, "gps_verdicts": 703, "gauntlet": 12 }`
- source: `watch/inbox/ml_moonshot_20261007/ml3_router_metrics.json`
- verdicts: tier-1 supports=yes (the counts sum to exactly the claimed 3,753 rows, a real run-output fragment proving the trainer executed); no deep check ran on this row (tier-1 verdict stands).

### 8. ml3-router-classifier#1 - held-out validation [high]
- claim: Held-out validation landed: on the primary time-based 75/25 split (corpus README anti-leakage rule) gradient boosting measures accuracy 0.8722 / ROC AUC 0.9434 and logistic regression 0.8754 / 0.9288, versus the named percolator hand-tuned baseline at accuracy 0.7135 / AUC 0.5012 (chance: its lexicon scores text and the 703 ledger rows carry none) and the incumbent ledger-capability pass_rate baseline at accuracy 0.2812 / AUC 0.5198; stratified split agrees (GB 0.8775 / 0.9479).
- quote: `"accuracy": 0.8722, "balanced_accuracy": 0.8583, "roc_auc": 0.9434`
- source: `watch/inbox/ml_moonshot_20261007/ml3_router_metrics.json`
- verdicts: tier-1 supports=yes (the GB numbers match the claimed primary metrics verbatim); no deep check ran on this row (tier-1 verdict stands).

### 9. ml3-router-classifier#2 - the v0 route table [high]
- claim: The v0 route table landed: 25 task shapes ranked per animal by predicted P(success) with an evidence gate (>= 5 training rows per shape, added after the ungated argmax routed every shape to grok-4.7 off 9 thin ledger rows); gated picks include legality-water-graph-v1 -> legality-propagator-v1 (the specialized tool beats every LLM on its own shape) and tavern-turn (1824 rows) -> claude-haiku-4.5, while 10 thin shapes return best_animal null with a do-not-route fallback.
- quote: `"task_shape": "legality-water-graph-v1", "n_train_rows": 100, "best_animal": "legality-propagator-v1",`
- source: `watch/inbox/ml_moonshot_20261007/ml3_route_table.json`
- verdicts: tier-1 supports=yes (the quoted gated pick carries n_train_rows 100, satisfying the >=5 evidence gate); no deep check ran on this row (tier-1 verdict stands).

### 10. ml4-verdict-regression#0 - classical forecaster executed [high]
- claim: Classical regression forecaster executed with .venv/Scripts/python.exe: 238 lane-archive units over 16 run groups, 222 lanes, 1236 checkpoints built from memory/runs/*/lanes/ + a 1130-row steps.jsonl slice scan; mean / Ridge / HistGradientBoosting trained leave-one-run-out; outputs ml4_checkpoints.jsonl + ml4_forecast_report.json landed.
- quote: `checkpoints=1236 runs=16 lanes=222`
- source: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/lanes/ml4_build_lane_forecaster.py`
- verdicts: tier-1 supports=no (a bare counts line names no interpreter or outputs); deep_tier2=verified (the landed report carries every count: full JSON parse read 1,236 checkpoints / 16 runs / 222 lane_ids / 238 units, three models each trained leave-one-run-out over 16 folds, built_at matching the file mtimes; +4/+1/+23 drift vs today's tree is post-17:22 landings on an append-only archive, consistent).

### 11. ml4-verdict-regression#1 - the MIRA bar [high]
- claim: Headline bar for the MIRA critic set: pooled held-out Spearman 0.9804 / MAE 0.191 rows over 1236 checkpoints across 16 whole-run folds (worst fold Spearman 0.9608); the A1 falsifier clause (beat the mean baseline on held-out runs) passes on MAE 0.191 vs 1.397, so any paid MIRA training must beat this number on the same split or the spend is theater.
- quote: `"hgb": { "n": 1236, "spearman": 0.9804, "p_value": 0.0, "mae": 0.191 }`
- source: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/ml4_forecast_report.json`
- verdicts: tier-1 supports=no (the quote carries no fold structure or baseline number); deep_tier2=verified (hgb block byte-found; 16 folds' held-out sizes sum to exactly 1,236; worst fold 0.9608 read from the folds; the mean baseline on the same pooled split reads MAE 1.397 / Spearman -0.1094, so the beat-the-mean clause passes on the landed bytes. The "A1 falsifier" naming is the ask's framing, the numbers are the file's).

### 12. ml4-verdict-regression#2 - the checkpoint corpus [high]
- claim: Checkpoint corpus landed and byte-verified at 1236 lines: per-checkpoint run, lane_id, family, k, T, remaining, rows_so_far, frac, elapsed_sofar_min, run_lanes_started, plus steps_mentions / mention_span_min sensitivity columns for a measured-clock rebuild.
- quote: `"run":"2026-10-04-0","lane_id":"r01-steps-jsonl","family":"r","k":1,"T":5,"remaining":4,"rows_so_far":1,"frac":0.2,"elapsed_sofar_min":4.8972324173,"elapsed_lane_span_min":0.0,"run_lanes_started":4,"steps_mentions":0,"mention_span_min":null`
- source: `memory/runs/mickey17_v2/runs/ml-moonshot-20261007/lanes/ml4_checkpoints.jsonl`
- verdicts: tier-1 supports=no (one sample row cannot prove the corpus); deep_tier2=verified (wc -l reads exactly 1,236 lines; the quote byte-found at line 1; full-corpus schema sweep: 0 bad JSON, 0 missing fields across all 12 claimed columns plus the 13th, elapsed_lane_span_min, one distinct key-set over all lines, sha256 prefix edbda3eb2854c51b. mention_span_min is present and uniformly typed but null on all 1,236 lines: the sensitivity column exists, its values are owed by a future rebuild).

### Scripted annex (verbatim numbers)

- FIDELITY: rows with all of quote/source/steal/estate_status non-empty: 38/38 (100.0%)
- VERIFIER TABLE: lanes with persisted checks: 8; verdicts: deep_tier2 12 (verified 12), supports 38 (no 16, yes 22); deep_tier2 join: 10/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 2
- WIDTH-ECONOMICS: rows/lane median 5, max 5, min 4; top-10 lanes share 100.0%; exact cross-lane duplicate quotes (normalized): 0; gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)
- URL LIVENESS: unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0 (nothing to check)

Deep-check coverage note (folder arithmetic over the gate's 12 deep checks): they cover 8 of the 12 TOP-K rows (ml1 x3, ml2 x2, ml4 x3) plus 4 rows outside the TOP-K (ml5-anomaly-head#0, ml6-es-mesh-trainer#0 and #1, ml7-quantizer-bridge#0), all 12 verdicts verified. The 2 join-misses are truncation paraphrases in the check row_keys (ml1#1, ml6#1), labeled not fatal by the script; their substance is verified either way.

## BLOCKED TIER

Four blocked items. None tombstoned (script: tombstoned []).

- **B1. ml6-es-mesh-trainer#3 - live ES round refused, wallet gate closed.** Quote: `WALLET GATE BLOCKED: no per-device wallets in .env (owed: GSTD_WALLET_DESKTOP, GSTD_WALLET_BOB, GSTD_WALLET_PIXEL); P0 INPUTS OWED; live es round refused`. The blocked-world proof itself executed (--status exit 0, --round exit 3 before any byte leaves the box, no state file written) and the ml6#0 deep check exercised the gate-blocked path with zero network attempts. Next-sitting unblock: operator pastes the three P0 per-device wallets (same owed input as the fleet lane), then one seat fires generation 0 and re-measures the 5502-byte headline against real completion lengths (ml6#1 residual, same sitting).
- **B2. ml4-verdict-regression (lane gaps) - paid A1 MIRA spec dispatch died 402.** The paid A1 MIRA spec (H247_A1_MIRA_LANE_FORECASTER_SPEC) never landed: memory/runs/hermes_burn/usage.jsonl carries 2 rows, both transport-failed after 2 tries with HTTPError 402 Payment Required; this lane is the free classical baseline that context demanded. Fold-gate classification: a 402 TERMINAL, not a refire. Next-sitting unblock: not refireable until funded; the standing precondition is ml4-verdict-regression#4's residual, the close-time not-landed-unit recorder, so the landed-flag head stops being survivorship before any paid critic trains on it.
- **B3. ml8-rollshape-classifier data tier (#0, #3) - 49 rows excluded as blocked/banked.** 45 BLOCKED rows (copsilent: the independent cop produced no verdict, so no mechanical label exists) and 4 BANKED rows (consensus, no mechanical verdict) sit outside the 699-row training set, excluded and counted first-class, never silently dropped. Next-sitting unblock: cop verdicts landing re-enables the 45; if the operator wants CHALLENGE as its own class the trainer needs a 3-class head, not a binary remap (ml8-rollshape-classifier#3 residual); rerun the trainer as the register grows (ml8-rollshape-classifier#1 residual).
- **B4. Shared-tree gate debt blocking push (coordinator tier; ml3-router-classifier#4 + its gaps, ml6-es-mesh-trainer#4, ml7-quantizer-bridge#4).** Ratchet exit 1 on 3 NEW sibling debts (blast_radius_probe.py:217, classify_probe.py:48, longrunner_patrol.py:408) plus tools/hermes_burn.py GROWTH (accepted at 428, now 552); citation-lint findings in memory/zknot/LATEST.md and watch/inbox/DAWN_REPORT_20261006.md; 6 pre-existing tests/test_context_pack_delivery.py failures (identical before and after the bridge). Zero hits name the filing lanes' own files. Note the cure already landed in-lane: ml7's thought_quantizer NEW debt was cured by extraction, and the gate's deep check re-ran the ratchet at PASS NEW=0. Next-sitting unblock: each owner accepts by name (baseline-update --by / citation baseline) or cures; then the push gate runs clean. Left for the coordinator by design, not a refill.

## NEGATIVE RESULTS (counted reasons table)

Folder arithmetic over cited rows; tombstones per script: **[]** (zero hard failures, nothing subtracted from owed).

| # | reason class | count | items (lane#row) |
|---|---|---|---|
| 1 | Held-out lens/model at or below the 0.5 noise floor, no consensus-gate ladder rung cleared: the roll-shape lens DIES on gauntlet at current sample size (LOO n=14: LR AUROC 0.5102, GB 0.3061 vs rungs 0.58/0.71/0.89) | 1 | ml8-rollshape-classifier#1 |
| 2 | Named hand-tuned baseline at chance: percolator lexicon 0.7135 / AUC 0.5012 because it scores text and the 703 ledger rows carry none (itself the finding) | 1 | ml3-router-classifier#1 |
| 3 | Survivorship head, not skill: 238 archived positives vs 3 negatives, logistic in_sample_accuracy 1.0 on 241 units | 1 | ml4-verdict-regression#4 |
| 4 | Sought source absent from shelves: JPL Power of 10 + Drexler rod-logic NOT on the shelves; NASA MDP itself not on the shelves (its SHAPE realized on estate code instead) | 2 | ml2-nasa-circuitry-census#0, ml2-nasa-circuitry-census#4 |
| 5 | Citation gate PHANTOM-NUMBER caught on the lane's own prose before landing: 8591 in ml1's README, 1236 in ml4's receipt (the founding defect class this run labels, caught live twice) | 2 | ml1-ledger-corpus#3; ml4-verdict-regression lane gaps |
| 6 | In-lane defect caught and cured before landing: ml5's first head run crashed on an X/y length mismatch (fixed to label-align before the validated rerun); ml7's first inline draft hit 636 lines of NEW ratchet debt (cured by extraction) and its two models collided on the 12-char pack id (caught by the new pin test, keys became bridge_ml3_router / bridge_ml4_forecast); ml2's builder first run failed on an off-by-one repo-root path (first run FATAL, second clean, per the receipt) | 3 | ml5-anomaly-head negatives; ml7-quantizer-bridge#0 and #3; ml2-nasa-circuitry-census receipt section 5 |
| 7 | Deviation rows at fold (executed-with-deviation per scoreboard): ml6's remaining gate failures are sibling files it does not own; ml8's binary PASS/FAIL map over the gwap engine's 4-rung verdict ladder (BLOCKED precedence, VERIFIED_AGREE, CHALLENGE, DISPUTE), 45+4 excluded as blocked | 2 | ml6-es-mesh-trainer#4, ml8-rollshape-classifier#3 |
| 8 | Pre-existing debt measured, not caused (before/after identical): 6 delivery-suite failures identical before and after the bridge; the deliberate-ask law displaced past the 1800-char render cap by the two ~220-char classical rows; ml5's fixture tests parameterize recorded incidents because no ts-keyed series of them exists | 2 | ml7-quantizer-bridge#4; ml5-anomaly-head negatives |
| 9 | Sparse label coverage: gps ledger evidence_resolved and capability cost_usd_per_call largely 0/None, so no credibility weighting attempted in v0 | 1 | ml1-ledger-corpus gaps; ml3-router-classifier gaps |
| 10 | Tombstones (hard failures subtracted from owed) | 0 | [] |

Totals: 15 negative items across 9 reason classes, 0 tombstones. Note: further honest deviations are filed inside rows whose estate_status reads "executed" (ml4's uniform-write interpolation of per-checkpoint elapsed; ml5's hung/dead classifiers being adaptive cadence-multiple logic rather than sklearn models); the scoreboard's executed-with-deviation count of 2 counts rows, not deviation notes (ml6-es-mesh-trainer#4 and ml8-rollshape-classifier#3).

## NEXT REGISTER (top 10 residuals, one seat one sitting)

1. **ml6-es-mesh-trainer#3** - paste the three P0 per-device wallets (GSTD_WALLET_DESKTOP, GSTD_WALLET_BOB, GSTD_WALLET_PIXEL), fire generation 0, and in the same sitting re-measure the 5502-byte wire headline against real completion lengths (ml6-es-mesh-trainer#1 residual). Unblocks B1.
2. **ml4-verdict-regression#4** - wire the close-time not-landed-unit recorder: TERMINAL'd asks become landed=0 negatives at run close, curing the survivorship head; precondition for B2 and for ml4-verdict-regression#2's residual (feed v2 training rows from close-time not-landed units).
3. **ml8-rollshape-classifier#1** - rerun ml8_build_rollshape_classifier.py as the gauntlet register grows past per-animal n=1-2 (the standing 30-min gauntlet clock is the admission-growth path); the lens stays dead until then, honestly.
4. **ml2-nasa-circuitry-census#1** - v2 relabel (fix_commits >= 2 or a fix-rate threshold) for a balanced positive class; then ml2-nasa-circuitry-census#2's residual: feed the frame to the interference-search trained-judge recipe for a first module-level defect-prone classifier.
5. **ml3-router-classifier#3** - refresh the corpus, re-measure AUC against the stated escalation bar (~0.75 on a refreshed corpus); only if it reads below does the driving-ladder climb to the MIRA-style generative critic unblock (behind B2's funding and item 2's recorder).
6. **ml4-verdict-regression#0** - measured-clock rebuild using the banked steps_mentions / mention_span_min columns instead of the uniform-write interpolation; kills the run's one interpolation deviation. Note the deep check found mention_span_min null on all 1,236 lines, so the rebuild first needs a steps-scan that fills it.
7. **ml7-quantizer-bridge#0** - register future run models' artifact paths in tools/classical_law_feed.py constants so the next run's classical laws ride the same bridge; watch classical_models_in in compile_report.json (a future 0 there is the falsifier for seats silently losing the classical layer, ml7-quantizer-bridge#2).
8. **ml1-ledger-corpus#0** - corpus refresh on a standing cadence plus manifest-pin discipline: 5 of the pinned sources appended post-build (+50 trail rows by the gate's recount), trainers must pin build_manifest.json (ml1 gaps); the dwf 1302 storm row stays receipt-counted until the corpus ships those logs (ml1 gaps).
9. **ml8-rollshape-classifier#2** - intent-only probe that strips verb identity, separating the cop's engine arithmetic from genuine roll shape; only if the operator asks, ml8-rollshape-classifier#3's 3-class head for CHALLENGE as its own class.
10. **ml2-nasa-circuitry-census#0** - harvest JPL Power of 10 + Drexler rod-logic bytes into corpus/library if a later wave wants them (the census's one open harvest residual; the greps today resolve only to coincidental hits, ml2-nasa-circuitry-census#4).

Coordinator item (not a seat sitting): B4's acceptance-by-name or cure of the shared-tree gate debt, then full-tree pytest triage at the push gate (ml7-quantizer-bridge#3 note; ml3-router-classifier#4's full-suite scope statement).

---

*Fold written by the folder seat, 2026-10-07. Scripted sections verbatim from FOLD_SECTIONS.md (script sha256 58bd72c79c6d); claims and quotes from the lane archive; verdicts from the persisted checks and the gate's deep checks. Workspace copy for publishing: `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_ML_MOONSHOT_20261007.md`.*
