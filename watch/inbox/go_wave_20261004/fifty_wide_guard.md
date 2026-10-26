# FIFTY-WIDE GUARD - GO item 8 lane receipt (fifty-wide-guard, 2026-10-04)

GO item 8 (a07-fifty-wide-waves#1, D1 ruling): "make the wave dispatch assert
len(units)==lanes and print any dropped-unit list into the receipt; operator
sub-item: retain the dispatch log so wave counts are replayable."

## 1. The runner that produced the 2026-10-03 wave

There is no runner file on disk. Both 2026-10-03 fifty-wide waves were ad hoc
main-session Task-agent fan-outs, not saved workflows:

- Wave 1 (envelope measurement): watch/inbox/envelope_50w_20261003.md, "Shape:
  50 Task agents (Explore type) launched in ONE wave on the main-session retry
  path" (line 10-11, byte-read this ask).
- Wave 2 (the burn audit): watch/inbox/burn_claims_50wide_20261003.md, "One
  Task agent per unit, self-contained byte-check prompt, ONE-line verdict
  contract, main-session retry path" (PROTOCOL SHAPE step 3, lines 35-36).

Search commands that proved it (this ask, Git Bash, repo root):

- `git grep -ln "burn_audit_claims\|fifty" tools/ scripts/ .zcode/workflows/`:
  no burn_audit_claims runner anywhere; the only .zcode hit for fifty/50-wide
  shapes is `.zcode/workflows/the-gala.dwf.ts` (the prior THE-50/gala program,
  a different wave family that never touched burn_audit_claims).
- `git grep -ln "burn_audit_claims" -- '*.py' '*.ps1' '*.js' '*.ts'` (llamacpp
  excluded): zero hits. Only catalog/catalog.jsonl, catalog/tags.jsonl and
  corpus/steal/MASTER_MICKEY17_V2.md name the extraction artifact.
- `memory/workflows/REGISTRY.jsonl`: no burn_audit_claims row.

So the wave dispatch lived in the firing session's head; the durable
countermeasure had to become a file. Filed as a Python pre-flight tool the
firing session runs BEFORE dispatch (the runner's language and home: repo
tools/, venv python), plus its test.

## 2. The guard (tools/fifty_wide_guard.py, new, 303 lines)

Shape: fail-closed pre-flight over the extraction artifact and the dispatch
plan, run before any lanes fire.

- `.venv\Scripts\python.exe tools\fifty_wide_guard.py --units
  memory/runs/burn_audit_claims.json --plan <plan.json> [--lanes N] [--receipt
  <wave.md>] [--log <dispatch_log.jsonl>] [--no-log]`
- PASS requires: extraction unit count == lane count (plan length or explicit
  --lanes), zero duplicate plan keys, zero plan keys absent from the
  extraction, and every unit carrying a countable identity. It never
  renumbers, trims, or pads to make counts meet.
- FAIL (exit 1) prints the mismatch and the full dropped-unit list to stdout
  and appends a "fifty-wide guard FAIL" section naming every dropped unit to
  the receipt given in --receipt.
- CANNOT-VERIFY (exit 2): missing or unparseable units/plan files, or a
  dispatch-log write failure. Never a silent pass.
- Dispatch-log retention (sub-item 2, in code): every passing pre-flight
  appends one JSONL row to
  `memory/runs/fifty_wide/dispatch_log.jsonl` (moment UTC, units path,
  units sha256, unit-key sha256, units count, lanes, plan entries) so wave
  counts are replayable from disk after the fact.
- Operator-owed retention convention (per-agent results, code cannot force a
  human to archive): after each wave, archive per-agent outputs under
  `memory/runs/fifty_wide/<wave-name>/agents/` next to the dispatch log. That
  is the path convention to keep; without it the 10-unit mechanism stays
  unknowable exactly as D1 found.

## 3. Tests (tests/test_fifty_wide_guard.py, new, 166 lines)

Instrument: `.venv\Scripts\python.exe -m pytest tests/test_fifty_wide_guard.py -q`
Final run this ask: **10 passed, 0 failed, 0 skipped in 1.43s** (also 10 passed
in 2.14s on the first full-green run; both moments 2026-10-04).

Bands, each pinned:

- Clean fixture (3 units == 3 lanes) passes exit 0 and banks exactly one
  dispatch-log row with units_count 3 and lanes 3.
- Known dropped unit (4 units vs 3-lane plan): exit 1, the dropped key
  `b.md:9` prints on stdout AND lands in the receipt under "DROPPED UNITS (1".
- Unknown plan key fails exit 1 even when lengths match (renumbering smell).
- Duplicate plan keys fail exit 1 (one lane cannot own two units).
- Explicit `--lanes 50` vs 3 units fails exit 1 with both numbers printed.
- Missing units file and unparseable plan fail closed exit 2.
- A unit with no file+line/id identity fails exit 1 (identity error), never a
  silent pass.
- CLI exit codes (0/1/2) pinned through a real subprocess.

One test bug was caught live and fixed, cause and evidence named: the plan
helper wrote every plan to the same `plan.json` path, so in the subprocess
band the second write clobbered the first before the child process read it and
the pass case read the short plan (assert read (1, 1, 2), expected (0, 1, 2)).
Fix: plans take distinct filenames; the helper comment carries this receipt.

## 4. Live demonstration against the real artifact

Fed the real extraction and a synthetic 50-lane plan (the wave-2 shape, first
50 of 60 keys), the guard exits 1 and names exactly 10 dropped units
(BURN_adversarial-self-probes_20260927_e.md:19/:23/:27, _f.md:9/:15/:27,
_g.md:23, _h.md:9, BURN_b2-wave-fold_20260926.md:10/:13). That is the exact
failure shape D1 recorded, now structurally impossible to repeat silently on
any future wave that pre-flights through this tool.

## 5. D1 amendment: the em-dash mechanism is REFUTED; the guard is the countermeasure

The prior hypothesis that em-dashes dropped the 10 units is refuted by byte
measurement. This ask's instruments (venv python over
memory/runs/burn_audit_claims.json):

- `units 60, distinct (file,line) 60, filings 16, em-dash units 2` - never 10;
  the same figures the refire lane banked (a07#1 CORRECTED text), re-measured
  here and matching byte for byte.
- Receipt tally re-summed: 30+11+3+6 = 50 verdicts tallied in
  watch/inbox/burn_claims_50wide_20261003.md vs 60 extraction units; gap 10.

D1 record (corpus/steal/MASTER_MICKEY17_V2.md section 7, not edited by this
lane per ownership): the drop mechanism is unknown and stays unknown; no
per-agent artifact exists for either wave. This lane's ruling-amendment: the
countermeasure is not a mechanism explanation but a structural guard - the
dispatch may not fire unless the counts meet, and the dispatch log plus the
operator-owed agents/ archive make the next gap explainable if one ever
appears.

## 6. Files touched (disjoint ownership held)

- tools/fifty_wide_guard.py (new; the guard)
- tests/test_fifty_wide_guard.py (new; the tests)
- watch/inbox/go_wave_20261004/fifty_wide_guard.md (this receipt)

Clean-file proof (this ask): `violation_ratchet.violations_in` over both .py
files reads CLEAN (0 violations each); em-dash/en-dash grep reads 0 bytes in
both files; lengths 303 and 166 lines (under the 400-line bar). The ratchet
`check --changed` FAIL rows this ask sit entirely in sibling lanes' files
(mag/route_chat.py, tools/dungeon.py, tools/prepush_credential_shape.py,
tools/prepush_seal_patrol.py rows) and name no file of this lane.

## 7. Blockers and operator-owed

- BLOCKED (sub-item 2, partial): archiving per-agent outputs is an operator
  behavior, not code. Owed convention: after each fifty-wide wave, file the
  per-agent results under `memory/runs/fifty_wide/<wave-name>/agents/` beside
  the dispatch log the guard banks at
  `memory/runs/fifty_wide/dispatch_log.jsonl`. Until that habit exists, a
  future count gap still cannot be attributed to a mechanism.
- The drop mechanism of 2026-10-03 remains unknown (D1 stands); this guard
  prevents silent recurrence, it does not explain the past 10.
- No git commit made (coordinator commits).

Filed by the fifty-wide-guard lane, 2026-10-04. Zero em-dash bytes in every
file this lane wrote.
