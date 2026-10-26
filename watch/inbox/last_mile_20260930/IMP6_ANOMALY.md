# IMP6 anomaly flagger (2026-09-30)

Mission (operator, refire after provider blip — prior attempt left zero
artifacts, fresh start confirmed): flag anomalies on (1) steps.jsonl
(malformed JSON, hash-shape, ts non-monotonic runs), (2)
ORAL_LAW_INDEX.jsonl (ts sort, duplicate thread_ids), (3) burns LEDGER
verdict_enum OTHER/REVIEW counts joined to
memory/burns/verdict_enum_map.json plus evidence-path existence on a
sample; exit 0 clean / 1 anomalies with rows named; under 60s; run live.
FILE OWNERSHIP: `tools/anomaly_flagger.py`,
`tests/test_anomaly_flagger.py`, this receipt.

## 1. What landed

- `tools/anomaly_flagger.py` (sha256 142c21de29912f65) — spec-first
  docstring, then code. Three surfaces; shared descent engine (named
  rows + run grouping); burns join follows the map's own law
  (ledger.verdict -> census[verdict], census misses fall back live to
  `tools.burns_verdict_enum.normalize()`); deterministic evenly-spaced
  evidence sample (default 50, `--sample 0` = all); CLI path overrides
  for tests/frozen snapshots; exit 0 clean / 1 anomalies / 2 IO-usage.
- `tests/test_anomaly_flagger.py` (ce7fb6b5c940ddfc) — 11 tests:
  per-row naming, run grouping, gap-surviving and mixed-offset
  (Z vs +00:00) descent detection, equal-ts not a descent, dup ids
  naming every row, OTHER/REVIEW informational vs fallback_unknown and
  missing-evidence anomalies, deterministic sampling, all three exit
  codes.

## 2. Live findings (run 2026-09-30T17:49Z, 1.82s, exit 1)

Row counts are one-moment snapshots — the steps stream is append-live
(it grew 37446 -> 37457 rows across this lane's own scans (AGENTS.md
census-denominator law); 37457 is the receipted moment).

### steps.jsonl (memory/trajectory/steps.jsonl, 37457 rows)

- malformed_json: 34 rows -> 7176, 7549, 7724, 7801, 8036, 10775,
  10820, 13049, 20833, 23156, 23181, 23192, 23472, 23600, 23715,
  24018, 25109, 28379, 29714, 30373, 30623, 30945, 31006, 31089,
  31137, 31519, 32160, 32308, 32608, 32723, 33154, 33307, 33342,
  37192. Two shapes: "Expecting value: line 1 column 1" (torn fragment
  starting mid-JSON, e.g. 7176 = `ory/corpus/ai_canon:...`) and
  "Extra data" (e.g. 7549 = `true}}`, a spilled object tail). Observed
  as torn/interleaved concurrent-append artifacts, not blank lines
  (0 blanks).
- hash_shape: 1 row -> 6165, a `face: "milestone"` row with NO
  step_hash field at all (writer-shape drift; the v1 bash writer always
  emits sha256(basis)[:16], mag/trajectory_step.py:152).
- ts_non_monotonic: 1 descent in 1 run -> 28456
  (2026-09-28T17:03:53.648+00:00 -> .647, a 1 ms clock jitter — real
  but benign; named for the operator to judge).

### ORAL_LAW_INDEX.jsonl (watch/inbox/operator_model/, 153 rows)

- ts_sort: 58 descents in 35 runs -> rows 2, 4, 6, 8, 12, 13, 14, 16,
  17, 21, 24, 26, 27, 28, 30, 31, 34, 35, 37, 41, 42, 43, 46, 47, 49,
  51, 54, 55, 56, 58, 60, 61, 62, 63, 66, 67, 70, 73, 76, 78, 80, 81,
  84, 85, 87, 88, 90, 91, 92, 93, 94, 97, 100, 103, 106, 109, 112,
  146. ROOT CAUSE structural, not corruption: the miner
  (oral_law_mine_20260930.py:145) shuffles its sample with a fixed
  seed, so the index is deliberately unsorted vs ts; descents measure
  distance-from-sorted against the ascending source index
  (corpus/oral_history/seat_pools/session_index.jsonl). Fixing means
  either sorting the index or amending the miner — operator call.
- dup_thread_id: 0 over 153 rows.

### burns LEDGER (memory/burns/LEDGER.jsonl, 693 rows)

- verdict_enum (join verdict_enum_map.json census, informational):
  OTHER=14, REVIEW=89, fallback_unknown=0 — every verdict known to the
  map (matches its own summary block; no map-age drift).
- evidence_paths: sample 50/693 landing paths, 0 missing, 0 lacking
  the field.

## 3. Verification (instruments named per the census law)

- `pytest -q tests/test_anomaly_flagger.py`: 11 passed in 1.06s.
- `pytest -q tests/test_anomaly_flagger.py tests/test_burns_verdict_enum.py
  tests/test_oral_dedupe.py`: 69 passed, 1 failed — the failure is
  test_oral_dedupe.py::test_live_index_census_and_founding_law, a
  PRE-EXISTING live pin (asserts 33/59/29; live index now reads
  153/307/73 because the four 2026-09-30 seat-local miner runs appended
  120 rows after the 09-29 pin). Not this lane's file; named for the
  owning seat.
- `python tools/violation_ratchet.py check --changed`: 0 findings on
  anomaly_flagger.py (NEW=0). The run reports FAIL from NEW debt in
  sibling lanes' uncommitted working-tree files (tools/pain_replication,
  tools/gps_mcp, tools/mountain_*, tools/cost_rollup.py,
  tools/ldt_lattice.py) — not this lane's ownership.
- Live CLI run: exit 1 (anomalies present, rows named), 1.82s — under
  the 60s budget with ~30x headroom.
