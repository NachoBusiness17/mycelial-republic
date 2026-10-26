# events-door repair receipt (wave5-repair, division B, 2026-09-29)

Lane: events-door. Owed work: 5 schema-less rows (watch/inbox/EVENTS.jsonl lines
54-58, f-05 census 2026-09-28) made `mag/link_library.py load_events()` raise,
so the fail-closed sanctioned door served 0 of 58 rows. Repair executed per the
no-erase law, EVENTS_DRIFT_LAW_20260926 rule 2, and the charter backfill
amendment. Lane files: watch/inbox/gala_20260925/wave5-repair/lanes/
(events-door.json state, events-door.backfill.py, events-door.finishline.py,
events-door.check.py, events-door.check.txt).

## Reproduction (before)

`.venv\Scripts\python.exe -c "from mag.link_library import load_events; rows = load_events(); print('OK', len(rows))"`
raised `ValueError: EVENTS.jsonl row missing schema=event.v1 or origin block:
B2-142-HN-QWEN38-DIG`, exit 1. Bytes at repair start: 58 rows, 43,737 bytes,
sha256 ae77c7910fb5c397e7c0103aae195d69a3ffbfe194264a5ff592f6ad457ef287 -
byte-identical to the f-05 census, so nothing had touched the door since.

## What was done

1. **Spec first** (build discipline): appended section 4 "No-erase backfill
   amendment" to watch/inbox/SCOUT_CHARTER_20260926.md - the charter owns the
   event-row shape (section 1: schema event.v1 + origin block; kind vocabulary
   finding / ALERT / verdict at line 17). The amendment defines the carrier
   mechanism before the code changed.
2. **Backfill, not erase**: appended 5 corrected carrier rows (lines 59-63),
   each `id = <original id>-BACKFILL`, charter kind, writer attribution, full
   verbatim content, and an origin block naming the row it supersedes:
   origin.file = watch/inbox/EVENTS.jsonl, origin.line = 54..58,
   origin.replaces = original id, plus original_ts and the superseded line's
   sha256. The 5 bad rows are byte-untouched on file. Carriers:
   B2-142-HN-QWEN38-DIG-BACKFILL, B2-142-HN-CODEPLAN-DIG-BACKFILL,
   B2-142-TRIAL-SHAPES-LIVE-BACKFILL, B2-142-REDDIT-TRIAL-DECAY-BACKFILL
   (writer b2-142-cerebras-dig, their content, kind finding) and
   LINKS-329-CORRECTION-BACKFILL (writer events-door; the original carried no
   writer and kind "correction" outside the charter vocabulary, so the carrier
   re-mints its substance verbatim into labeled title + detail and keeps the
   corrects key). Emission script asserts zero em/en dashes and zero non-ASCII
   per carrier.
3. **Register (drift law rule 2)**: one op register row appended to
   watch/inbox/index_events.jsonl in the SAME critical section as the append
   (events-door.backfill.py): seq 1790677271642025400,
   ts 2026-09-29T10:21:11.642Z, class DATA, writer events-door, sha256
   4D7E5611381E928FDA982D6DD0411C978422EE7F7BB12CBF52A854CE1B7DDE69, size
   52596, purpose naming the append and the row count (58 -> 63). Verified
   after the fact: it is the NEWEST register row whose file names EVENTS.jsonl
   (4 such rows total) and its sha equals current bytes (rule 1).
4. **Loader amendment** (mag/link_library.py load_events, now at
   mag/link_library.py:180): two-pass parse. Pass 1 json-parses every line
   (malformed JSON still raises) and collects ids named by origin.replaces on
   conforming carrier rows. Pass 2 enforces the strict contract on every row
   EXCEPT those named ids - accepted debt by name (ratchet pattern), skipped
   from the served list, file bytes intact. Any schema-less row NOT named by a
   carrier still fails closed. No production caller depended on the raise
   (git grep: the only other reference, mag/links_split_gate.py:86, is an
   error-message string; cache_identity.py:330 is an unrelated counter;
   tools/md_record_audit.py has its own load_events for a different file).
5. **Suite coverage**: new test
   `test_load_events_skips_only_named_backfilled_rows` in
   tests/test_link_library.py proves named debt is skipped; the pre-existing
   test at tests/test_link_library.py:143-155 proves unnamed schema-less rows
   still raise. Both pass.

## Finish line (byte-checked)

`events-door.check.txt` holds raw output. FINISH LINE: PASS, exit 0:
63 non-empty lines, json.loads zero-raise on every line, `load_events()` serves
58 charter rows, the 5 superseded ids are absent from service while their bytes
remain on file, all 5 -BACKFILL carriers are served. pytest
tests/test_link_library.py: 36 passed, exit 0.

## Ratchet (cited exit, attributed, NOT force-passed)

`tools/violation_ratchet.py check --changed`: exit 1, FAIL. 4 NEW rows:
- 8dce490bf896c42a file-too-long mag/link_library.py:413 - MINE. The file was
  388 lines before this lane; the backfill mechanism plus its law docstring
  added +25 and crossed the 400 gate. I compressed once (421 -> 413) to my
  honest floor without gutting the fix-comment receipt.
- 84291bf5f2af246b file-too-long mag/corpus_gap_research.py:663, 42b721c740d1abda
  file-too-long mag/corpus_selfsteal.py:476, 2c7e16bf178da9d0 shell-true
  tools/fossil_check.py:73, plus GROWTH claim e066832a0b8edb5e
  tools/stealth_driver.py (accepted 753, now 1061) - NOT MINE: sibling lanes'
  working-tree files; this lane never touched them.
The tool has no per-hash acceptance: baseline-update registers ALL current NEW
rows in one batch under one --by name. Registering would misattribute foreign
debt, so this lane did NOT run it and leaves the accept-or-fix call to the wave
owner. NOTE: an early `--help` probe of `baseline-update` was NOT inert - it
executed and registered all 4 under the default "operator" name. That write was
fully reverted (`git checkout -- configs/violation_baseline.json`; the only
diff content was the 4 added claims plus the tool's "updated" timestamp line),
so the baseline on disk is back to HEAD. Lesson banked: this CLI has no --help;
unrecognized subcommand args run the command.

## Decision ledger

Closes the f-05 owed repair: the fail-closed events door went from serving 0 of
58 rows to serving all 58 charter rows (63 lines, 5 named debts skipped, zero
raise), with the no-erase law intact and the drift-law register current. The
loader's strictness contract is amended, not loosened: unknown schema-less rows
still raise; only carrier-named debt is accepted, by name, in-file.

## Adjacent defects observed, not owned, not fixed

- index_events.jsonl lines 94-96: 3 unparseable register rows from 2026-09-01
  (/board/ era, seq "NEXT" placeholder, single-quoted pseudo-JSON). Readers
  already parse tolerantly.
- watch/inbox/EVENTS.jsonl has 7 CRLF line endings among 58 LF lines (mixed;
  pre-existing; the loader strips, so parsing is unaffected).
- f-05 census error found while transcribing: f-05 claims line 54
  (B2-142-HN-QWEN38-DIG) lacks `detail`; the bytes carry a full detail field.
  The sha was unchanged since the census, so this was a census misread, not
  rot. The schema/origin absence - the actual defect - was confirmed.

## Not done / limits

- Full-suite `pytest -q` ran to completion in the background in 2389.58s
  (39:49): 7 failed, 2436 passed, 12 skipped, 15 errors. NONE of the failures
  touch this lane's surface: test_seed_mcp.py (15 errors, TypeError build()),
  test_context_pack_delivery.py (2), test_headless_law.py (1 - the bare-spawn
  census scans tools/ and tests/ only; this lane adds no spawn sites),
  test_organ_map.py (1), test_surface_rebuild.py (3). Those are the shared
  working tree's sibling-lane state (the ratchet saw 36 changed files).
  tests/test_link_library.py appears nowhere in the failure list - its 36
  tests are inside the 2436 passed. Raw summary banked at the tail of
  events-door.check.txt.
- Nothing was committed; the working tree carries this lane's edits
  (SCOUT_CHARTER_20260926.md, mag/link_library.py, tests/test_link_library.py,
  watch/inbox/EVENTS.jsonl, watch/inbox/index_events.jsonl, lane files) for the
  wave coordinator.
- Carrier content for lines 54-57 was transcribed verbatim from the original
  rows without re-verifying their underlying sources (that verification
  belonged to the b2-142-cerebras-dig lane when the findings were minted); the
  carriers carry the same epistemic grade as the rows they replace.
