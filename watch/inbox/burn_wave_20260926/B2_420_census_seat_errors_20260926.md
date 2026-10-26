# B2-420 Relabel the behavioral census "seat errors" claim (SW-07, 2026-09-26)

## Verdict

LANDED (classification branch of the brief's either/or). mag/improve.py's behavioral row now counts only error-kind rows (kind FIELD contains error/fail/crash/exception, case-insensitive -- the same field rule the pinned census counts) for the "seat errors" number, keeps the full census naming in claim and detail, and demotes a zero-error tail from kind "risk" to "census" so lifecycle chatter stops flagging the promote pipeline. Falsifier state: a pure-lifecycle tail (70 pro_fire + 5 cloud_handoff + 5 improve_cycle) now reads "0 recent seat errors of 80 behavioral rows" with error_kind_events=0 -- the old text would have claimed "80 recent seat errors" with zero error kinds. Pinned suite updated to the new contract: tests/test_improve_behavioral_scout.py 10 passed. Note: SW-05 held an active claim on mag/improve.py (B2-418, crash scout region); per the claim law this lane claimed, re-read fresh bytes, and touched only the behavioral row emission region -- the scout region bytes were not touched by either lane's edits.

## Evidence file:line quotes

- QUEUE.md row: "the pinned census counts EVERY tail kind but the claim still says 'N recent seat errors' ... today the live tail-80 is 70 pro_fire + 5 cloud_handoff + 5 improve_cycle with zero seat errors, so the row claims 80 seat errors over pure lifecycle chatter and the promote pipeline reads it as a risk signal".
- Pre-fix bytes, mag/improve.py:1027-1030: `claim = (f"Behavioral events log: {events} recent seat errors " f"(census events={events} kinds={len(kinds)})")` with `"kind": "risk"` unconditional.
- New fix-comment (in the emission block): "CAUSE: the claim hardcoded '{events} recent seat errors' while the pinned census counts EVERY tail row kind ... FIX: kinds are classified error-vs-lifecycle by marker ... the 'seat errors' number is now the error-kind count ... a zero-error tail demotes the row kind from 'risk' to 'census'".
- Falsifier probe (census function untouched, classification at the emission): lifecycle tail -> events 80, error events 0, claim "0 recent seat errors of 80 behavioral rows"; tool_fail row -> error-kind count 1.
- Pinned tests updated with the B2-420 receipt note (assertions now pin error_kind_events in claim/detail and the full census token set incl. error_kinds=['tool_fail']); suite 10 passed.

## Work done

- mag/improve.py behavioral row emission: error-kind classification, relabeled claim, detail gains error_kind_events + error_kinds, conditional risk/census kind; claim line appended before edit (21:33:10Z, foreign SW-05 claim honored, region-disjoint rebase).
- tests/test_improve_behavioral_scout.py: two assertions updated from the old text shape to the relabeled contract with the cause named.
- Probe + suite run green.

## Falsifier

The brief's falsifier ("a tail of pure lifecycle kinds reporting 'N recent seat errors' with N>0 and zero error kinds") is now impossible by construction: the seat-errors number IS the error-kind count. Reopen if: a claim row again reports seat errors greater than the error-kind count, or the promote pipeline flags a zero-error behavioral tail as kind "risk".

## Bibliography closed

Read: mag/improve.py (behavioral_events_census pinned contract + emission block), tests/test_improve_behavioral_scout.py (pins, pre/post), watch/inbox/burn_wave_20260926/B2_374_behavioral_pin_20260926.md (referenced via row), QUEUE.md B2-420 row, probe transcripts. No external sources.
