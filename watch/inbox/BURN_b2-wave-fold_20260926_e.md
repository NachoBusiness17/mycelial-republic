# BURN b2-wave-fold: single-writer lock build (e)

## Verdict
steal

## Evidence
- Falsifier fired: "4 are true self-feed renumber corrections" in the next-50 window; "Both readings exceed >2, so the single-writer lock build is forced" (watch/inbox/BURN_b2-wave-fold_20260926_c.md).
- Species to shape against: "restore-clobber duplication, concurrent whole-file restores erased landed rows" and "stale lock-holder starvation, four hung git PIDs held .git/index.lock from 16:54" (same receipt).
- Fold law: "shared-file writes need single-writer locks" (memory/burns/MANIFEST.json, self_steal_fold b2-wave-fold).
- Fresh web: "open(path, O_CREAT | O_EXCL) atomically creates a lockfile; failure with EEXIST means another process holds the lock. Works cross-platform but requires stale-lock cleanup (crash leaves an orphan lockfile)"; also "on Windows, msvcrt.locking() requires the file to have content and the file pointer at position 0" (WebSearch cross-process file lock query, run 2026-09-27T00:07Z; msvcrt byte-range shape rejected in favor of lockfile).
- "The above constants are available on Unix and Windows" (O_EXCL, docs.python.org/3/library/os.html, fetched 2026-09-27T00:08Z; atomicity semantics deferred to open(2)).

## Steal or Vacuous
Steal. Built tools/ledger_lock.py (stdlib only, Windows-safe): LedgerLock context manager plus `append` CLI. Acquire is os.open(lock, O_CREAT|O_EXCL|O_WRONLY) writing a pid+host+acquired-at stamp; a lock older than 600s is broken and the break recorded in "<lock>.log"; append is flush + os.fsync; release removes the lockfile only if the stamp still matches. JSON is validated before the lock is acquired. Live test on watch/inbox/LEDGER_LOCK_TEST.jsonl, actual outputs:
- 5 sequential appends: five times "OK appended 1 row to watch/inbox/LEDGER_LOCK_TEST.jsonl under lock watch/inbox/LEDGER_LOCK_TEST.lock", exit=0 each.
- Invalid line: "REFUSE invalid JSON line (checked before lock): Expecting value: line 1 column 22 (char 21)", exit=2; target stayed 5 lines; lockfile absent.
- Fresh foreign lock (dead-holder-sim stamp): "REFUSE lock held: watch/inbox/LEDGER_LOCK_TEST.lock held and fresh (age 0s, stale threshold 600s)", exit=3.
- Stale break via os.utime backdate 660s: append succeeded, exit=0; lock log row {"age_seconds": 660.2, "event": "stale-break", "threshold_seconds": 600}; 6 rows landed in order; no lockfile remained.
One defect self-caught and fixed mid-build: log rows carried an "acquired" timestamp on release/stale-break rows; post-fix only acquire rows carry it (verified in the rerun log). Not wired into any live writer. Writer adoption contract: every LEDGER.jsonl appender switches to `python tools/ledger_lock.py append --target memory/burns/LEDGER.jsonl --lock memory/burns/LEDGER.lock --line '<json>'` (or the LedgerLock context manager), rows as canonical single-line json.dumps, lock log audited at the falsifier rerun; adoption is cross-window and this pass wires nothing.

## Falsifier
Rerun the concurrent-claim counter over the following 50 B2 rows after adoption: pass is 0 self-feed renumber corrections and 0 restore-clobber doubles caught only post-hoc. Added instrument check: 0 stale-break rows younger than adoption (a fresh stale-break means a writer crashed holding the lock).

## Bibliography (closed)
watch/inbox/BURN_b2-wave-fold_20260926_c.md; memory/burns/MANIFEST.json (self_steal_fold b2-wave-fold); tools/ledger_lock.py (built this pass); watch/inbox/LEDGER_LOCK_TEST.jsonl and LEDGER_LOCK_TEST.lock.log (live run outputs); WebSearch "cross-process file lock O_EXCL lockfile pattern msvcrt locking atomic append Windows POSIX" (2026-09-27T00:07Z); docs.python.org/3/library/os.html (fetched 2026-09-27T00:08Z).
