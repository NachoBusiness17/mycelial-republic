# ARENA BENCH TRIPWIRE - door 2 of the 24-wide dig, landed (2026-10-04)

Operator order: "go" on the build order, then mid-flight "actually ractor it
out self steal then go" - the remaining doors ride the ractor-engine
(dwfrun-3b5af1ac, 8 lenses + 2 moonshots); door 2 landed in parallel because
it is a pure defect fix + test addition with no design surface to ractor.

## The defect, diagnosed (not "drift" - a stub)

The 24-wide receipt called it "arrakis.html shape drift ... ValueError at
mag/arena_bench.py:102, zero tests referencing the file". The byte truth is
sharper: dashboard/static/arrakis.html has been a 459-byte REDIRECT STUB
since the 2026-09-22 surfaces-functional dedupe (the canonical copy moved to
dashboard/static/games/arrakis.html, 17.5KB, still carrying THE BLIND GATE
with its crown=50 / ghost-signs inscription the bench parses). The bench's
ARRAKIS_PATH never followed the move, so load_ground_truth() parsed a
redirect page, found zero gates, and raised honestly - on every run, silent
to every gate, for 12 days. The honest-raise design worked; nothing was
listening.

## The fix

mag/arena_bench.py ARRAKIS_PATH repointed at the canonical
dashboard/static/games/arrakis.html. The parse stays strict (raise on shape
change, never fabricate a verdict) - the design was right, the pointer was
wrong. DUNGEON_PATH verified still-canonical (dashboard/static/dungeon.html,
8.4KB, 6 inv: rows, not a stub).

Proof: python mag/arena_bench.py --selftest exits 0 and mints BOTH synthetic
verdicts (2 PASS + 2 FAIL records, zero_human: true) - the pass/fail split
is proven, the instrument is alive again.

## The tripwire

tests/test_arena_bench.py, 4 passed (2026-10-04, pytest -q):
1. --selftest exits 0 and proves the split (synthetic PASS + FAIL present)
2. load_ground_truth() parses the canonical surfaces: gates >= 1, the blind
   gate present
3. THE STUB TEST - the exact disease as an assertion: neither surface may be
   a redirect stub (meta-refresh check + minimum-size check), so the next
   dedupe move fails pre-push at the stub instead of rotting the bench
4. selftest output decodes as JSON records (instrument discipline)

## What this changes

The bench is live again for the pass@K diagnostic (EG-20, the dig's only
measured-effort item rides this instrument). Pre-push now covers the bench:
surface renames, moves, stub-ification, and parse-shape changes all fail the
gate.

Writer: zcode-53-strategy-window
fetched: 2026-10-04
