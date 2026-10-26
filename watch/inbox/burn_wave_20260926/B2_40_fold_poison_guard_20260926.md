# B2-40 FOLD POISON GUARD: OUTSIDE-DROP WARNING + 2^53 SEQ SCHEME (2026-09-26)

## Verdict

Both defects B2-02 filed as owed are fixed in scripts/index_fold_host.mjs with tests.
(1) OUTSIDE_RE register drops are no longer silent: the fold counts them per top-level
path segment and reports them as fold_warnings on the existing WARN + exit-2 channel.
The real rebuild surfaces watch/ x235 (229 distinct paths) plus stragglers
corpus/ x1, dashboard/ x1, memory/ x1, tools/ x2.
(2) nextSeq no longer sticks: seq arithmetic runs in BigInt, emitting a plain JSON
number while under 2^53 and a decimal STRING beyond, so node appends never repeat a
seq. Real INDEX.json rematerialized: folded 3062 events -> 972 active items; verify:
968 hash-clean, 4 mismatched, 0 missing. Targeted suite: 5 passed.

## Evidence

- Cause 1: scripts/index_fold_host.mjs:82 OUTSIDE_RE includes `watch|`, and old line
  114 `if (ev._outside) { outsideItems.push(ev.file); continue; }` dropped such
  registers with no warning. Bytes: 235 register events with file starting watch/
  (writers exp002a, d05-rides-r2) plus 1 memory/ stray; 230 distinct paths including
  the invalidate.
- Cause 2: old nextSeq took a float64 max and added 1. Live proof, node v22.23.1:
  max=1789823567015749400, `max + 1 === max` -> true; BigInt(JSON.parse of that
  literal) -> 1789823567015749376 (ulp 256 at that magnitude). 559 events in the
  1789823567* family, 481 with the exact stuck literal, max literal 1789823567015749477
  (python exact int).
- Fix: index_fold_host.mjs:105-121 MAX_SAFE_SEQ + seqOf + compareBySeqTs; :123 nextSeq
  in BigInt (Number while <= 2^53-1, else decimal string); :171-177 drop counting;
  :206-210 outsideWarnings; :227 fold_warnings concat; sorts :94 and :203 compare via
  BigInt while no-seq events (md_record_seal appends none) keep ts ordering, matching
  the old NaN tie behavior.
- After: rebuild stderr ends "outside-dropped register events excluded from items:
  watch/ x235 (229 distinct path(s)): register inbox files with an inbox-relative
  path"; INDEX.json carries all 5 segment warnings (derived_at 2026-09-26T13:02Z run
  and the final re-run).

## Work done

Edited scripts/index_fold_host.mjs (header spec first, then code); wrote
tests/test_index_fold_host.py (5 tests, node CLI against a throwaway inbox via the
new INDEX_INBOX_DIR seam; tests never touch the durable inbox). Rehearsed on a copy
of the 3062-line log before touching the real index. Rematerialized
watch/inbox/INDEX.json with the warnings; rebuild exits 2 while any warning stands
(nonce-gap channel). Self-feed: B2-147/148/149 in QUEUE.md (renumbered after
colliding with live B2-145/146; numeric sort, not lexicographic, is the law).
Filed as owed, not faked:
1. add/invalidate still MINT outside events; the warning covers legacy drops only.
   Writer-side refusal is B2-147.
2. md_record_seal.py registers carry NO seq and absolute Windows paths: B2-148.
3. normInboxFile does not strip the absolute host root, so C:/-path registers land as
   items that verify cannot resolve (QUEUE.md mismatch is one): B2-149.
4. 4 verify hash mismatches (REJECTION_TAXONOMY_20260917.md,
   BURN_JUDGE_LANE_BUILD_20260925.md, QUEUE.md absolute path, +1): bytes moved after
   registration; pre-existing debt, not this lane's.

## Falsifier

F1: rebuild on watch/inbox prints no "outside-dropped register" line: claim dead.
F2: INDEX.json fold_warnings lacks the watch/ x235 entry: claim dead. F3: two
consecutive adds on a log seeded with seq 1789823567015749400 produce equal seqs:
claim dead (tests/test_index_fold_host.py::test_seq_never_sticks_at_production_scale).
F4: a sub-2^53 append emits a string seq or a past-2^53 append emits a number: claim
dead (test_seq_stays_number_within_2pow53 pins int 6;
test_seq_advances_past_2pow53_as_exact_string pins "9007199254740992").
F5: pytest tests/test_index_fold_host.py does not pass 5/5: claim dead (5 passed,
0.87s). F6: full pytest -q census broke fold/inbox collectors: claim dead. Two full
runs: 39F/1732P/9S/1E in 17:59, then 38F/1748P/9S/1E in 18:44 (suite grows as lanes
land tests; failures are pre-existing flaky Windows debt in unrelated domains). Byte
check: .pytest_cache lastfailed holds 12 entries, none fold/inbox/surface; my 5 tests
plus tests/test_shared_surface_events.py: 32 passed in 3.34s.

## Bibliography closed

scripts/index_fold_host.mjs; tests/test_index_fold_host.py;
watch/inbox/index_events.jsonl; watch/inbox/INDEX.json;
watch/inbox/burn_wave_20260926/B2_02_writer_debt_20260926.md;
state/fuel/b2_02_register_driver.py; tools/md_record_seal.py;
watch/inbox/burn_wave_20260926/QUEUE.md; memory/burns/LEDGER.jsonl.
