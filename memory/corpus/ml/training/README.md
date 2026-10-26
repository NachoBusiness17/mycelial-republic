# THE LABELED CORPUS: estate history as ML training data

Lane ml1-ledger-corpus, run ml-moonshot-20261007, built 2026-10-07T16:20:45Z
(see `build_manifest.json` for the exact build stamp, per-source sha256, and
the 12 pinned trail-file hashes). Every table exists as parquet AND csv; the
parquet is canonical, the csv is the readable mirror. Builder:
`memory/corpus/ml/build_corpus.py`, rebuild with:

```
.venv/Scripts/python.exe memory/corpus/ml/build_corpus.py
```

Snapshot law: the estate trails are LIVE (row count moved between two builds
minutes apart), so a training run must pin the `build_manifest.json` it trained
on; counts below were measured at the stamped build.

## Files and byte origin

| table | rows | bytes come from |
|---|---|---|
| gauntlet | 16 | `watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl` (sha256 430625f8579f...) |
| usage | 3038 | `memory/runs/hermes_burn/usage.jsonl` (sha256 4144253b9fd7...) |
| registry | 160 | `memory/workflows/REGISTRY.jsonl` (sha256 489c08ecb552...) |
| gps_capability | 30 | `tools/gps_mcp/gps_ledger.db3`, sqlite table `capability` |
| gps_verdicts | 703 | `tools/gps_mcp/gps_ledger.db3`, sqlite table `verdict_log` |
| trail_events | 8591 per build_manifest.json | `dashboard/static/trails/*.jsonl` (12 lane files, sha256 per file in the manifest) |
| incidents | 14 | derived: trail_events byte counts + receipt anchors (each row names its `evidence_path`) |

## Column-by-column mapping

### gauntlet (cheap-seat falsifier trials; register: `watch/inbox/GAUNTLET_FREE_LANDED_20261006.md`)

| column | byte origin |
|---|---|
| source_line | 1-based line number in GAUNTLET_REGISTER.jsonl |
| ts, work_id, family, provider | same-named fields of that register line |
| animal | the register line's `model` field (the seat that ran the trial) |
| verdict | register `verdict`: PASS / FAIL / BANKED |
| pass_label | derived: 1 for PASS, 0 for FAIL, empty for BANKED |
| onsets_made, onsets_total, onsets_frac | parsed from the register note text "N/M onsets" |
| overlap_1, overlap_2, overlap_3 | parsed from consensus note "overlap A/B/C" |
| corrected | true when the note carries CORRECTED (the grader self-strike rows: the first beat regex demanded an "ms" suffix the format never mandated, per the register receipt) |
| superseded | true when a later line with the same work_id carries the CORRECTED note; the register appends corrections and never rewrites, so artifact rows stand as history |
| note, expensive_ref | verbatim register fields (the expensive-vs-cheap delta reference) |

### usage (paid dispatch ledger)

| column | byte origin |
|---|---|
| ts, id, model, turn, prompt_tokens, completion_tokens, reasoning_tokens | same-named fields of the usage line |
| total_tokens | derived: prompt_tokens + completion_tokens |
| cost_usd, ok | same-named fields; ok is a real boolean in the source |
| ok_label | derived int of ok; empty where ok is absent |
| http_status, finish_reason, transport_error, refused, channel, error | same-named fields, sparse (absent on most rows) |

### registry (workflow-gate verdicts)

| column | byte origin |
|---|---|
| ts, name, digest, script, verdict | same-named fields of the REGISTRY.jsonl line |
| pass_label | derived: 1 PASS, 0 FAIL, empty STATUS-ROW |
| n_checks | len(checks) on that line |
| n_checks_failed | count of checks with ok false on that line |
| new_digest | derived: first appearance of this (name, digest) pair in file order |
| check_g1_multiplicity ... check_g8_width_shape | one boolean per gate check id on that line, id lowercased with dashes to underscores; empty where the line lacks that check |

### gps_capability / gps_verdicts (model x task_shape capability ledger)

Same-named sqlite columns of `tools/gps_mcp/gps_ledger.db3`; verdict is renamed
verdict_label (0 or 1); ts normalized to UTC ISO8601. capability carries the
aggregates (pass_rate, sample_size, cost_usd_per_call); verdict_log is the
703-row event stream those aggregates summarize.

### trail_events (the feature-level stream, 12 lanes)

| column | byte origin |
|---|---|
| lane | file stem of dashboard/static/trails/<lane>.jsonl |
| source_line | 1-based line number in that file |
| ts, actor, event | same-named fields of the trail row |
| errno | first `[Errno N]` or `errno N` match inside the detail text |
| errno22 | errno equals 22 |
| rc | first `rc=N` token in detail |
| monitor_rc, march_rc | `monitor rc=N` / `march rc=N` in night composite details (the generic rc column reads the FIRST rc token, which is monitor on composites) |
| is_429, is_1302 | the token 429 / 1302 appears in detail |
| is_cycle_fail | event equals CYCLE_FAIL |
| detail_len, detail, artifacts | the row's detail (length and verbatim text); artifacts joined with ";" |
| parse_error | the line failed JSON parse (kept, never dropped) |

### incidents (the labeled-failure table; label = 1 on every row, class is the target)

| column | byte origin |
|---|---|
| incident_id, class | derived identifier and failure class |
| surface, evidence_path | the trail file or receipt that owns the incident |
| first_seen, last_seen | min/max ts of the matching trail rows; empty for receipt-anchored rows (no byte timestamps claimed) |
| measured_count | counted from bytes (trail_events filter named in evidence_path) or as stated by the receipt (count_basis = receipt) |
| register_count | the errata number from `corpus/steal/MASTER_READ_ESTATE.md` section 10 where one exists (D6 errno-22 family, D7 elder streak, D8 night march) |
| count_basis | bytes or receipt |
| quote | byte-copied line extracted from evidence_path at build time (truncated to 38 words) |
| cured | cure status with pointer, or the owed cure |
| label | 1 (failure class present) |

The 14 rows: 6 errno22_runner_state (builder, day_work, forge, night, prose,
research), 3 http_429_storm (elder streak, research monitor, dwf 1302 storm),
2 hung_cycle (night march rc=1 composites, output-dead lanes), 2 stash_sweep
(the R3 incident and its detector cure), 1 phantom_number (the struck 191.8M
headline, gated by `tools/citation_lint.py` PHANTOM-NUMBER).

## Feature documentation (what predicts what, measured at this build)

1. **gauntlet: onsets_total predicts beat verdict.** Live (non-superseded)
   beat rows: the 6-count and both 8-count trials PASS at frac 1.00; the
   12-count trial FAILs at frac 0.25. Free seats hold the grid to 8 counts;
   the arithmetic collapses at 12 (register receipt, "the difference has a
   number"). Family predicts PASS outright: dice 2/2, metagame 0/2,
   consensus BANKED. The `corrected`/`superseded` columns mark the grader
   self-strike: four beat rows graded FAIL 0/8 by the artifact regex are
   superseded by corrected PASS rows; train on live rows or on verdict
   history, never on the blend.
2. **usage: model predicts cost and survival.** Mean cost_usd per row spans
   0.0040 (claude-haiku-4.5) to 0.2340 (z-ai/glm-5.3-prime); ok_label mean
   spans 1.000 (haiku, 672 rows) to 0.608 (fable, 418 rows). Silence is the
   failure mode: of the 726 not-ok rows only 8 carry an error string, so a
   model that needs error text to predict failure is blind here; ok_label is
   the trainable target.
3. **registry: new_digest does NOT predict verdict in this window** (PASS
   0.769 on first attempts vs 0.765 on reruns). The discriminating features
   are the check columns: on the 29 FAIL rows the most-failed checks are
   g4_salvage and g3_steering (16 each), then g6_receipts (14) and
   g8_width_shape (11).
4. **trail_events: lane predicts errno22; event separates first-hand from
   hearsay.** errno22 rows: research 513, builder 378, night 26, day_work 4,
   prose 1, forge 1. Builder's own failures are the 370 CYCLE_FAIL rows
   (register D6 says 370); the other 8 are TESUJI_DROP rows quoting research
   failures, so event==CYCLE_FAIL is the first-hand filter. Research matches
   D6 exactly at 513; night matches at 26.
5. **incidents: measured vs register_count is the label-noise column.**
   builder 378 bytes vs 370 register (the TESUJI_DROP hearsay); elder 15
   rows carry a 429 token vs the register's 14-day CYCLE_FAIL streak (the
   extra row is a 2026-09-18 manual cycle noting a cage 429 fallback);
   night_march_rc1 measures exactly 28, matching register D8.
6. **gps: task_shape is the strongest pass_rate lever in capability** (the
   table spans world-tick 1.0 to adversarial-review ~0.44 on prime models);
   verdict_log's evidence_resolved flag marks whether the verdict's evidence
   was actually resolved, a data-quality feature for credibility weighting.

## Splits and cautions

- No time-based split is baked in; every table carries ts. Train/test by ts
  to avoid leakage across the fleet's chronological drift.
- gauntlet BANKED rows are not pass/fail trials (consensus group members);
  keep pass_label NaN out of binary training.
- usage rows are turns, not calls: an id can repeat across turns/retries.
- trail detail text carries the estate's own bytes verbatim, em-dashes
  included; treat it as quoted source data, not house style.
- The dwf_429_1302_storm row is receipt-counted (896 events in CLI logs the
  corpus does not ship); its evidence lives at
  `watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md`.
