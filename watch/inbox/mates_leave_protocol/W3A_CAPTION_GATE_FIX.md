# W3A — caption_ledger_verify DEAD-gate fix (sealed baseline)

date: 2026-09-29 · lane: Mickey17 W3 (mates_leave_protocol) · owner files:
`scripts/the50_t21_q_caption_ledger_verify.py` + `tests/test_pin_law_fail_output.py`
· no commit (per lane orders; gate arms itself on next push via the
prepush changed-path arm on the verifier path).

## Cause (the canary's DEAD finding)

`tools/gate_canary.py` family `caption_ledger_verify` plants the exact
known-bad "drop the last row of `watch/inbox/qdrop_export/q_caption_ledger.jsonl`"
and requires `RESULT: FAIL`. The verifier printed `RESULT: PASS` instead:
every one of its 8 checks built its denominator FROM the ledger rows it
read — check1 counted the parsed rows, checks 4/5/6 only visited ids still
present, and check6's reproducibility direction re-ran only drops that
still held rows (the blindness B2-306 already documented for vanished
cipher rows, generalized to ANY unpinned row). A deleted row was simply a
row nobody asked about.

## Fix (independent baseline, W3A)

check9 seals the ledger against constants carried in the gate's own source
(version-controlled, already watched by the prepush changed-path arm),
never read back from the file it audits:

- `SEALED_ROW_COUNT = 267`
- `SEALED_LEDGER_SHA256 = 489d5af92c3d8ee945d5761f2e01ee66511e87e188e4ca1c6015f4e4cb826053`

Sealed 2026-09-29 from the live ledger bytes (267 rows, 33,338 bytes,
zero CR). Any deletion, addition, or edit fails on count + sha. A
`--ledger PATH` drill arm runs the verifier on a copy; the seal still
applies, so tampered copies FAIL by design. FAIL output carries the SEAL
MAINTENANCE LAW (the B2-259 pin law applied to the whole file): re-derive
the constants from the new bytes only after a byte audit named in the
landing receipt; never weaken the seal to get green. Hook/daily-beat
contracts preserved: no-arg run, `RESULT: PASS/FAIL` line, exit 0/1
(`scripts/qcaption_verify_daily.py` and `githooks/pre-push` grep these
unchanged).

## Tests (real counts)

`tests/test_pin_law_fail_output.py` — 5 passed in 1.60s, incl. the new
canary regression `test_canary_row_deletion_fails_seal` (fixture ledger =
live copy minus last row -> rc 1, `check9 sealed baseline (W3A): FAIL`,
`row count 266 != sealed 267`, `RESULT: FAIL`, law line) and its control
`test_intact_copy_passes_seal` (byte-identical copy -> rc 0, check9
PASS). Existing pins intact: check7 PASS-branch bytes, green-run
RESULT line. With the pairing suite: 12 passed in 2.74s.

## Canary-style manual drill (subprocess, exact plant)

- PLANT (267 -> 266 rows): exit 1, `check9 ... FAIL row count 266 !=
  sealed 267; sha256 92676a1c991f811a... != sealed 489d5af92c3d8ee9...`,
  `RESULT: FAIL` — the token the canary greps. Gate ALIVE.
- CONTROL (intact copy): exit 0, check9 PASS, `RESULT: PASS`.
- LIVE (no args, as the hook and MagQCaptionVerifyDaily invoke it):
  exit 0, `RESULT: PASS - 267 rows, 163 drops`.

Note for the next canary run: the worktree checks out HEAD, so the family
flips DEAD -> ALIVE only once this fix is committed; the drill above is
the working-tree proof. The two regression tests double as the
seal-freshness tripwire: a legitimate regen that changes the ledger
without re-sealing turns them red by design — that is the audit trigger.
