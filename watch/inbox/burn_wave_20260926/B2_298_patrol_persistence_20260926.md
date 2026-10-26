# B2-298 receipt: drift-patrol prompt persistence, verification close (2026-09-26)

## Verdict

LANDED, with the landing owned by the B2-267 lane and closed on bytes by this
lane. The exposure the brief names (amended living-law patrol prompt living
only in the automations DB row, no repo copy, no check diffing the row against
a copy) is already closed on disk: configs/drift_patrol_prompt.txt holds 4438
bytes, sha256 95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9,
byte-identical to this lane's fresh DB readback of automation row
automation-a7c71ad1-f43f-403d-8677-105f5176df2b, and
tests/test_drift_patrol_prompt_copy.py diffs copy against DB in the
freshness_check pattern (this lane reran it: 3 passed in 0.52s). This lane's
own duplicate-copy attempt (configs/drift_patrol_prompt_a7c71ad1.txt, landed
from the same DB bytes, same sha) was retracted within the hour once the
canonical copy was found, so exactly one repo copy exists. The B2-298 queue
row read checked at dig time with no landing receipt and no LEDGER row; this
receipt, the LEDGER row and the dated row annotation are that missing record.
The row's B2-251 audit note "no repo-side prompt copy found" does not match
the disk at close time; it is left standing no-erase and resolved by the dated
annotation on the row.

## Evidence file:line quotes

- DB readback (this lane, .venv python, sqlite SELECT prompt FROM automations
  WHERE automation_id = 'automation-a7c71ad1-f43f-403d-8677-105f5176df2b'):
  len 4438, sha256 95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9;
  markers "index_fold_host.mjs verify", "--living-open",
  "LIVING PREFIX MISMATCH" and "hand-appended seq=epoch-ms events are retired"
  all present; zero em-dash and zero en-dash in the prompt text. The
  automation TITLE still carries an em-dash character; the prompt does not.
- configs/drift_patrol_prompt.txt: 4438 bytes, sha256
  95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9
  (byte-identical to the readback above; both hashes computed this lane).
- tests/test_drift_patrol_prompt_copy.py:59-65: "def
  test_repo_copy_matches_live_db_bytes(): ... assert live == db, (\"drift-patrol
  prompt drifted from its repo copy: the DB prompt was amended without
  rerunning watch/inbox/burn_wave_20260926/B2_267_update_prompt.py ...\")."
- This lane's pytest run: ".venv/Scripts/python.exe -m pytest
  tests/test_drift_patrol_prompt_copy.py -q" produced "3 passed in 0.52s".
- Lineage drift this lane proved: watch/inbox/burn_wave_20260926/
  B2_199_update_prompt.py NEW_PROMPT, parsed via ast (never imported; the
  module executes an UPDATE at import time), is len 2977, sha256
  e2f6c007f4a32280841a46c7fbb8952e12083d4b3e1c7348faf0bae6022b32f1, which
  DIFFERS from the live row (len 4438). B2_254_update_prompt.py and
  B2_267_update_prompt.py are the known later writers; the B2-267 receipt
  Verdict records "4,438 chars, block present exactly once".
- Automation row metadata (this lane readback): cron 0 8 * * *, enabled 1,
  created_at 1789374280137, updated_at 1790424020316 equals last_run_at
  1790424020316 (2026-09-26T12:00:20Z, the morning run), run_count 13. The
  updated_at column mirrors the last run, so the row alone cannot date an
  amendment (filed forward as B2-552).
- Timeline bytes (local mtimes): B2_267_update_prompt.py 16:24:41,
  configs/drift_patrol_prompt.txt 16:24:52, tests/test_drift_patrol_prompt_copy.py
  16:25:16, B2_267 receipt 16:25:52, B2_251 audit receipt 16:55:02 whose
  census line 81 still reads "B2-298 patrol-prompt persistence (no repo-side
  prompt copy)". Both facts stand: the copy predates the audit receipt file,
  and the audit note contradicts the disk. This lane does not guess which
  (census-before-write, or a missed file); it records both.
- Row state bytes at dig time: QUEUE.md line 360 read
  "- [x] B2-298 drift-patrol prompt persistence: ..." with the B2-251 audit
  annotation inline and a "[board-repair 2026-09-26]" suffix, while
  memory/burns/LEDGER.jsonl contained no B2-298 row and no
  B2_298_patrol_persistence receipt existed on disk before this lane filed
  one.

## Work done

1. Read the brief row (QUEUE.md line 360) and its pointers: the B2-199
   receipt and update script, tools/freshness_check.py pattern.
2. Re-ran the DB readback with .venv python only and fingerprinted the
   prompt (sha above); confirmed all living-law and touch-law markers.
3. AST-parsed B2_199_update_prompt.py and proved the live row postdates the
   B2-199 constant (4438 vs 2977 chars); located B2_254 and B2_267 update
   scripts as the later writers and read the B2-267 receipt.
4. Landed a repo copy from DB bytes via
   watch/inbox/burn_wave_20260926/B2_298_land_prompt.py (compare DB vs script
   constant, write configs copy, readback assert, dash guard), then found
   B2-267's canonical configs/drift_patrol_prompt.txt already on disk
   byte-identical and retracted the duplicate
   (rm configs/drift_patrol_prompt_a7c71ad1.txt; its sha equaled the
   canonical sha above). One canonical copy remains, B2-267's.
5. Verified B2-267's check on this machine: pytest
   tests/test_drift_patrol_prompt_copy.py = 3 passed.
6. Filed the LEDGER row via .venv python json.dumps; appended a dated
   no-erase close annotation to the B2-298 row; self-fed two Open briefs:
   B2-552 (prompt lineage sidecar; updated_at mirrors last_run_at so
   amendments are undatable from the row) and B2-553 (the copy check treats
   a reachable DB with a missing row as a skip, which is exactly the harness
   rebuild exposure the brief warns about).

## Falsifier

This close is falsified if any of the following stops holding: (a)
configs/drift_patrol_prompt.txt exists with sha256
95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9; (b) a
fresh DB readback of the automation row equals those bytes; (c) pytest
tests/test_drift_patrol_prompt_copy.py passes on a DB-reachable machine; (d)
exactly one repo-side copy of the prompt exists under configs/. Any sha
change must arrive with a named writer (until B2-552 lands, the writer is
discoverable only from a burn-wave update script or a dated receipt).
Residual exposure, filed as B2-553: a harness rebuild that drops the DB row
entirely still passes today's check as a skip, so the rebuild signal is
silent until that split lands.

## Bibliography closed

- watch/inbox/burn_wave_20260926/QUEUE.md (B2-298 row line 360; tail rows
  B2-549 through B2-551 for append format)
- C:/Users/foste/.zcode/v2/tasks-index.sqlite, automations row
  automation-a7c71ad1-f43f-403d-8677-105f5176df2b (SELECT prompt, title,
  cron_expr, enabled, created_at, updated_at, last_run_at, run_count)
- watch/inbox/burn_wave_20260926/B2_199_patrol_living_20260926.md (read in
  full; falsifier section names this exposure)
- watch/inbox/burn_wave_20260926/B2_199_update_prompt.py (AST read)
- watch/inbox/burn_wave_20260926/B2_254_update_prompt.py (presence read)
- watch/inbox/burn_wave_20260926/B2_267_touch_law_patrol_prompt_20260926.md
  (read in full) and B2_267_update_prompt.py (presence read)
- configs/drift_patrol_prompt.txt (hashed) and
  tests/test_drift_patrol_prompt_copy.py (read in full, executed)
- watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md (line 81
  census, mtimes noted above)
- watch/inbox/burn_wave_20260926/B2_298_land_prompt.py (this lane's
  lander/comparator, kept as evidence)
- tools/freshness_check.py (pattern reference)
- memory/burns/LEDGER.jsonl (row appended)
