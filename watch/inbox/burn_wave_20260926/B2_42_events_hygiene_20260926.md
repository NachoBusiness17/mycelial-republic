# B2-42 events-log hygiene, 2026-09-26

## Verdict

LANDED. Lines 94-96 of watch/inbox/index_events.jsonl are the only malformed lines in the 3074-line log at scan time (byte scan, not a report). They are now (a) documented by an appended note event (seq 1789823567015749478, writer zcode-b2-42-events-hygiene, nonce 1) per the no-erase law, (b) grandfathered by content sha256 in configs/events_malformed_baseline.json, and (c) gated: mag.shared_surface validate now ERRORS on any NEW malformed line whose bytes are not in that registry. 8 new tests pass; the fold still skips exactly 94,95,96.

## Evidence with file:line quotes

Raw bytes (python repr, content sha256 with trailing CRLF stripped):

```
line 94 325c9ea76971007fe89a5a4ce508096c7e44ed22084b6c6bc47a7ed9fe341c18
b"{'seq':NEXT,'ts':'2026-09-01T13:56:50Z','op':'register','file':'/board/inbox/workspace_snapshot_20260901_1345Z.tar.gz','sha256':'PENDING_CODEX','class':'COMMIT','purpose':'workspace tool forge + doctrine snapshot v5 basecamp'}\r"
line 95 db87cd15ad3378a8c677f43c9024b8d48d67abd7fc53c4e14b6c11a347dbafdc
b'{"seq":NEXT,"ts":"2026-09-01T13:57:11Z","op":"amend","file":"/board/inbox/workspace_snapshot_20260901_1345Z.tar.gz","sha256":"2c50eb6e7449e474e57a7111d7c08b9165fb830f25437d335bb2cff184d54474","class":"COMMIT","purpose":"amend: real sha256 replaces placeholder"}\r'
line 96 bfa769b3b7fd35675aab204edcb3cf4ba1c483f932348de356fe5a8d304072e8
b'{"seq":NEXT,"ts":"2026-09-01T13:57:25Z", ... same content as 95 except ts}\r'
```

- scripts/index_fold_host.mjs:90: `skipped.push(idx + 1);  // tolerant reader: keep folding over legacy junk (line 94, PENDING_CODEX)`; the fold skips malformed lines forever, so validate is the only gate that can fail on NEW ones.
- index_events.jsonl:98: the 2026-09-01 sancho note names line 94 only ("a register attempt with single-quote JSON"); lines 95-96 were undocumented until this lane.
- index_events.jsonl:99: proper register seq 1788238807135 sha 2C50EB6E... ("registered properly by sancho after codex malformed attempt; malformed line preserved in log"); :908 repair op "repairs 3 unparseable template lines (09-01, seq:NEXT)".
- validate before vs after (B2_42_validate_before.json / B2_42_validate_after.json): errors 4 to 5, but the added error is `hash mismatch: burn_wave_20260926/QUEUE.md`, concurrent-lane drift, not mine; events_log_malformed = {total: 3, grandfathered: 3, new: 0}; zero malformed or baseline errors added.

## Work done

1. configs/events_malformed_baseline.json (spec/registry first): schema events_malformed_baseline.v1, 3 entries keyed by content sha256 with verified why-fields.
2. mag/shared_surface.py: docstring spec (Events-log hygiene section); scan_events_log() (strict json.loads, NaN/Infinity rejected to match JS JSON.parse, CRLF and blank lines handled like the fold); inspect_surface wiring: NEW malformed line = error, missing baseline = error, missing log = warning, stale registered line = pruning warning; events_log_malformed added to status output.
3. tests/test_shared_surface_events.py: 8 tests (new line fails, grandfathered passes, CRLF/blank tolerated, NaN rejected, missing baseline errors, stale warns, missing log warns, real baseline and real log checked against the 3 shas).
4. Note event appended (O_APPEND bytes, python, never bare python), fold rebuilt: `skipped malformed lines: 94,95,96`, event_count 3081 of 3084 lines, active 974, no warnings on the new writer.

Honest deviation: the note seq 1789823567015749478 is even (exactly representable in float64, ordering exact) but was emitted as a NUMBER literal where the B2-40 scheme prescribes decimal STRING past 2^53. Functionally harmless (fold nextSeq emits "1789823567015749479" as string next); filed as B2-156 instead of patched (log is append-only).

## Falsifier

- If a malformed line appended after 2026-09-26 does not produce a `NEW malformed line` error from `.venv\Scripts\python.exe -m mag.shared_surface validate`, the gate is broken.
- If validate errors while events_log_malformed.new == 0 on a surface with a present baseline and log, the grandfather matching is broken.
- If the next fold append repeats seq 1789823567015749478 or my number literal sorts wrong, my claim that even past-2^53 literals compare exactly is wrong (cross-check: `node scripts/index_fold_host.mjs events | tail -2`).

## Bibliography closed

mag/shared_surface.py; scripts/index_fold_host.mjs; watch/inbox/index_events.jsonl (lines 92-99, 908, tail); watch/inbox/INDEX.json; watch/inbox/SHARED_SURFACE_CONTRACT.json; configs/events_malformed_baseline.json; tests/test_index_fold_host.py; watch/inbox/burn_wave_20260926/QUEUE.md, B2_42_validate_before.json, B2_42_validate_after.json; memory/burns/LEDGER.jsonl.
