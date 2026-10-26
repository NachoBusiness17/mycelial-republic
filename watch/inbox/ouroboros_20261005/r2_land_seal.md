# R2 LAND: SEAL PATROL CASE FIX (ouroboros r2 gap closure row 8)

Seat: r2-landing seal lane. Moment: 2026-10-05, afternoon EDT. Fixes the B7
finding: the seal patrol's raw sha compare cried wolf on case, burying real
post-seal drift under byte-identical false positives.

## The fix

`tools/prepush_seal_patrol.py` (patrol core, former :125): the compare read
`actual == sha` where `actual` is `hexdigest()` output (always lowercase) and
`sha` is the stored ledger value (some writers store UPPERCASE). Now
`actual == sha.lower()`, and the drifted print shows `sha.lower()[:12]`. Fix
comment carries cause + evidence in the file.

Cause: seal writers store mixed-case hex; digest equality is case-blind by
definition. Evidence: the B7 lens measurement at --rows 1000 counted 21
case-only false drifts burying 17 real ones (lens moment, ledger then
smaller); closure row 8 of
`watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/SYNTHESIS.md`.

## Rerun, instrument + moment (census denominator law)

Instrument: `.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000`
against `watch/inbox/index_events.jsonl` at 10,678 sha rows / 3 malformed,
this seat, 2026-10-05. Ledger moved past the B7 moment, so the window mix
shifted; before and after are the same moment pair, B7 numbers named as the
lens's.

- BEFORE: 331 distinct files, 280 match, 9 missing-on-disk, 42 drifts
  = 32 case-only false + 10 real (exit 1).
- AFTER: 331 distinct files, 312 match, 9 missing-on-disk, 10 drifts,
  all real, case-only = 0 (exit 1). Matched gained exactly the +32 case-only
  set; the same 10 real digest pairs survive on both sides.

The 10 real drifts now visible (files whose bytes moved after their last
seal; verdict on each belongs to the owning lane, this patrol only alarms):
watch/inbox/STEALTH_SWEEP_LATEST.md, watch/inbox/PACK_OFFLOAD.jsonl,
watch/inbox/STEALTH_MINED_FINDINGS.jsonl,
watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md,
watch/inbox/ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl,
watch/inbox/frontier_olm_2026-10-04/steal/open-and-local-language-models via x.md,
watch/inbox/frontier_olm_2026-10-04/RECEIPT.md,
watch/inbox/ribvault_20261005/r06_free_probe.py,
watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/moonshot-1.md,
watch/inbox/frontier_olm_2026-10-05/lens/laws.md.

## Gate

- pytest `tests/test_seal_patrol.py`: 7 passed in 2.86s (6 prior + 1 new,
  `test_uppercase_seal_matches_but_real_drift_still_trips`: uppercase-sealed
  file passes clean and counts as a match, genuinely byte-drifted file still
  trips exit 1 with the lowercase sealed head printed).
- Ratchet `tools/violation_ratchet.py check --changed`: PASS, hits=5,
  registered=5, NEW=0, expired-exceptions=0 (exit 0).
- Patrol tool remains WARN-ONLY at pre-push per the t40/B2-215 house pattern;
  enforcement flip stays an operator call.

## Residue (owed, not asserted)

- The 10 real drifts are unadjudicated: re-seal through the owning writer or
  restore bytes, per the patrol's own fix line. No lane claimed them here.
- B7's 21/17 split was not reproduced at its moment (ledger moved); this
  receipt banks the same-moment before/after pair instead, which is the
  falsifiable form.
