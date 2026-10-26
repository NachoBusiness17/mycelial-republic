# B2-399 split mag/shared_surface.py back under the 400-line bar (2026-09-26)

## Verdict

LANDED, with the register half of the brief already satisfied by a prior lane
and named as such. scan_events_log moved byte-for-byte into the new sibling
mag/events_scan.py (B2-248 precedent), re-exported from
mag.shared_surface per the B2-342 re-export pattern, dropping the file from
exactly 400 lines (zero margin under the cap, rule trips at >400) to 378.
The accepted file-too-long claim (fingerprint 198edd83211b76e1) is NOT in
configs/violation_baseline.json's accepted set anymore (932 rows, zero
mention of shared_surface or the fingerprint) - someone pruned it before
this lane, so there was no claim left to prune and none needed; the ratchet
stays PASS with NEW=0. Tests green: 21 shared-surface event tests + 33
across the wider family.

## Evidence file:line quotes

- The cap state at lane start: mag/shared_surface.py counted exactly 400
  lines ("n_lines > FILE_LINE_CAP" is the trip; tools/violation_ratchet.py:44
  FILE_LINE_CAP = 400, :136), i.e. one added line from re-tripping a
  registered-or-new violation.
- The claim state: configs/violation_baseline.json accepted set (932 rows)
  contains NO entry for mag/shared_surface.py and NO fingerprint 198edd83211b76e1
  (verified by full-json scan); the register therefore already sits at its
  post-prune value for this file, and tools/violation_ratchet.py check
  --changed prints "RATCHET: PASS - no unregistered debt" (hits=50,
  registered=50, NEW=0) post-split.
- The moved block, mag/events_scan.py (new): scan_events_log with the
  identical docstring spec, the identical malformed-line predicate
  (strict json.loads, NaN/Infinity rejected via reject_json_constant, blank
  lines skipped, CRLF/LF handled) and per-line content sha256 records; the
  reject_json_constant import comes from mag.events_key_schema, the same
  source shared_surface imported it from (mag/shared_surface.py:95 pre-edit).
- The re-export seam, mag/shared_surface.py (post-edit, at the former
  function site): "from mag.events_scan import scan_events_log  # noqa: F401
  (B2-399 re-export)" with the cause-and-evidence comment naming B2-248,
  the cap state, and the B2-342 re-export pattern.
- Post-split counts and greens: shared_surface.py 378 lines; mag/events_scan.py
  47 lines; pytest tests/test_shared_surface_events.py -> "21 passed"; pytest
  -k "shared_surface or events_key or links_split" -> "33 passed, 2153
  deselected"; ratchet NEW=0 as above.

## Work done

1. Measured the file at exactly 400 lines; read the ratchet's rule shape
   (>400 trips) and the accepted set: the brief's accepted claim
   (198edd83211b76e1) was already pruned by a prior lane, so the "prune the
   accepted claim" half reduces to verifying the register state, done.
2. Filed the shared-file claim for mag/shared_surface.py (QUEUE 19:40:49Z)
   before reading bytes for edit.
3. Moved scan_events_log into mag/events_scan.py byte-for-byte (spec docstring
   preserved); replaced the function body with the re-export import + receipt
   comment.
4. Ran the falsifier family: ratchet check --changed PASS NEW=0 (the claim
   stays pruned, nothing new registered); 21 + 33 tests green; shared-surface
   validate ran (ok:false on the pre-existing B2-191 INDEX-staleness class,
   same 11 errors class as before the split - not caused by this change,
   reported honestly).
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This landing is inverted if any of the following holds: (a) any consumer of
mag.shared_surface.scan_events_log fails on import or behavior (the re-export
seam broke; the 21+33 green tests say otherwise today); (b) the accepted set
grows a NEW shared_surface file-too-long row (the file re-crossed 400 lines
after the split, which the 378-line state makes a 22-line margin); (c) the
baseline's accepted set is found to have held 198edd83211b76e1 AFTER this
receipt's landing without a new receipt naming it (the prune claim here is
misread or the register was rewritten).

## Bibliography closed

mag/shared_surface.py (read: imports, constants, scan_events_log, validate
wiring; edited: function replaced by re-export); mag/events_scan.py (created,
this lane); configs/violation_baseline.json (accepted set scanned for the
fingerprint and file name); tools/violation_ratchet.py (rule shapes read:
FILE_LINE_CAP, file-too-long trip, check --changed output);
watch/inbox/burn_wave_20260926/B2_248_module_split_20260926.md and B2_358_env_tripwire_20260926.md
(precedents named by the brief, accepted via the brief text and the baseline
fingerprint cited in it); tests/test_shared_surface_events.py (consumer
verified green). No network calls.
