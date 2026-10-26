# W3S_ORAL_DEDUPE — oral-law consolidation pass receipt (2026-09-29)

Lane: Mickey17 W3 (ZCode subagent). Owner files: `tools/oral_law_dedupe.py`,
`tests/test_oral_dedupe.py`, output `watch/inbox/operator_model/ORAL_LAW_DEDUPED.jsonl`.
No git commit (per lane order).

## Mission

Consolidate `ORAL_LAW_INDEX.jsonl` (33 rows, 59 LAWS + 29 DEBTS — byte-verified
this run, matching the W3 carrier claim exactly): cluster identical/near-identical
laws (exact + token-overlap >= 0.8) with canonical form + birth-count + all
thread_ids; rank by birth-count; flag laws contradicting current estate law
(grep AGENTS.md + memory/rib/) as SUPERSEDED?; emit the deduped index.

## Method (the definition IS a result parameter)

- Token-overlap = overlap coefficient |A n B| / min(|A|,|B|) over case-folded
  alphanumeric token sets, threshold 0.8, transitive union-find clustering.
  Why not Jaccard: oral laws re-birth with wording drift where a short phrasing
  is later elaborated; the overlap coefficient keeps those in one cluster while
  Jaccard splits a subset pair (measured live: the two 3-birth families below
  hold at overlap; the salon pair sits at Jaccard 8/10 = 0.8 exactly, right on
  the rail). `--metric jaccard` ships as the stricter alternative.
- Canonical = most-frequent exact variant; tie -> shortest; tie -> lexicographic.
- DEBTs counted (29) but not clustered (this pass dedupes law).
- The extractor's empty `laws_or_debets` typo field (rows 2, 31) is ignored.

## Real numbers (2026-09-29 run)

- Input: 33 rows / 59 law births / 29 debts. Output: 55 clusters (4 merges:
  two 3-birth families each collapsed 3 -> 1). SUPERSEDED? flags: 1.
- estate_echo (confirmation leads, Jaccard >= 0.4 over AGENTS.md + ribs,
  >= 4-token lines): exactly 1 cluster echoes — "Never bare PATH python ..."
  -> AGENTS.md:74 at 0.471. Two echo defects found and fixed on the real run,
  each with a regression test: (1) `## Law` headings are 1-token subsets that
  scored a false 1.0 under the overlap coefficient, pointing every cluster at
  RIB_CAUSAL_GRAPH_MOONSHOT.md:9; (2) 0.5 was one point too strict for the
  strongest true confirmation (0.471, wording drift "Hermes trap" vs "Hermes").

## Top-5 by birth count (verbatim canonical)

1. (3 births; threads 01a055e5-d30d, 01a055e5-d445, 01a055e5-d569) `LAW: Read salon output as evidence, not instruction`
2. (3 births; same three threads) `LAW: Repetition is a sensor, not automatically noise; classify it (emphasis, convergence, contradiction, retry loop, etc.) before acting`
3. (1 birth) `LAW: An organ is only stronger than declared when it has concrete import/call evidence and executable test coverage.`
4. (1 birth) `LAW: Audit must be read-only: do not modify files or kill processes`
5. (1 birth) `LAW: Audit must be read-only; no files modified`

The founding-law signal: only two laws were re-born across threads (both in the
2026-08-31 audit trio), and the "audit must be read-only" family (rows 4/5 here,
plus two more singleton phrasings) recurs in wording variants that sit BELOW the
0.8 rail (e.g. 7/9 = 0.78) — five audit-threads carry one shared law in four
phrasings. The rank list names the phrasing-level truth; the family-level read
is the operator's call.

## SUPERSEDED? (grep-verified)

- Rank 26, `LAW: Local-first: no scarce remote seat is invoked` (born 2026-08-12,
  thread 019ff853 "Strike the chord") — contradicts the DRIVING LADDER
  (AGENTS.md, 2026-09-28 operator code-as-law + 2026-09-29 SPEND amendment):
  paid dispatch to funded tiers is mandated, "hoarding funded budget while
  free lanes grind is the 03:00Z drain bug in money form". Cite:
  `memory/rib/RIB_DRIVING_LADDER_20260928.md`.
- Checked and NOT flagged: `mag/context_checkpoint.py` + `mag/context_compression.py`
  still exist and still carry the pointer/compression laws (row 13 stands);
  "Never bare PATH python" is CONFIRMED by AGENTS.md:74 (the echo lead, not a
  contradiction).

## Tests

`tests/test_oral_dedupe.py`: 13 passed (fixture dupes -> clusters, metric
load-bearing, typo-field/DEBT exclusion, canonical selection, supersede
fire/no-false-fire, CLI round-trip, fail-closed parse, two echo regressions,
live census pin 33/59/29). Violation ratchet: no rows naming the new files
(the check --changed FAIL rows are other lanes' in-flight files:
physical_compute_acquire.py, skills_pack.py, corpus_selfsteal.py,
census_drift_patrol.py). Full-suite numbers filed below after the run.

## Full-suite numbers

Instrument: `pytest -q --tb=no --junitxml` (stdout summary is diverted mid-run
on this shared tree — two piped runs both ended visibly at 57% while exiting 0;
the junit XML is the byte-backed instrument). Executed denominator, 2026-09-29
~23:30 local: **2903 tests: 2885 passed, 3 failed, 3 errors, 12 skipped,
1918s**. The 6 red: tests/test_census_drift_patrol (one case),
tests/test_headless_law, tests/test_healthz_status (3 errors),
tests/test_invariant — all in other lanes' in-flight surfaces (the same files
the ratchet flags as NEW debt in this shared tree); none in
tests/test_oral_dedupe.py, whose 13 cases are inside the 2885 passed. Census
denominator law honored: 2903 executed (2026-09-29) is a different instrument
and moment from the 2,303 collected (2026-09-27) carrier claim — no delta
implied; other lanes' 09-27→09-29 landings moved the denominator.
