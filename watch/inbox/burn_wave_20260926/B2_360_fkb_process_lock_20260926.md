# B2-360 FKB index read-modify-write cross-process lock (2026-09-26)

## Verdict

LANDED. log_failure's load+mutate+save window now holds a cross-process file
lock (a signatures.json.lock sidecar, msvcrt.locking on this Windows host,
fcntl.flock fallback on POSIX, fail-closed after a 15s wait: a timed-out
writer raises rather than writing unlocked, because a timed-out write IS a
lost update by definition). The in-process _INDEX_CACHE_LOCK still guards the
cache tuple. The brief's falsifier was run in both directions and the result
is unambiguous: two concurrent processes, 50 distinct signatures each - WITH
the lock, the final index holds 100/100; with the lock bypassed (the pre-fix
window modeled), the same probe left ONE of 100 entries (the other 99 lost to
last-writer-wins saves), a live reproduction of the exact disease the B2-87
census caught (82 log sigs vs 62 index entries).

## Evidence file:line quotes

- The disease, mag/failure_kb.py (pre-edit): "with _INDEX_CACHE_LOCK:" wrapped
  only the cache-tuple reads inside _load_index/_save_index, and log_failure
  ran "idx = _load_index() ... _save_index(idx) ... _save_index(idx)" with no
  cross-process guard; the module docstring's B2-87 block records the reset
  disease this lane's lock closes the remaining hole of.
- Post-edit mag/failure_kb.py: _lock_fd primitive (msvcrt.LK_NBLCK /
  fcntl.LOCK_EX|LOCK_NB), _index_file_lock(timeout=15.0) contextmanager with
  the cause-and-evidence docstring naming the 82-vs-62 census; log_failure's
  window comment "B2-360: the whole read-modify-write window holds the
  cross-process lock (including the remedy save below)"; the lock path derives
  from the live INDEX_PATH value so the tests' tmp_path fixture isolates the
  sidecar too.
- Falsifier (this lane, two real subprocesses x 50 distinct sigs into a tmp
  index): mode=lock -> "index signatures = 100 (expect 100)"; mode=nolock
  (lock bypassed via a no-op contextmanager, modeling the pre-fix window) ->
  "index signatures = 1". Driver and outputs under a tempdir; production
  index untouched.
- Existing suite with the lock live: tests/test_failure_kb.py "8 passed"
  (the autouse tmp_path fixture isolates both INDEX_PATH and, through it, the
  new sidecar lock path).

## Work done

1. Read log_failure/_load_index/_save_index and the B2-87 receipt block;
   confirmed the in-process lock cannot serialize across processes.
2. Added the contextlib/_time imports, the _lock_fd primitive with the
   msvcrt-first/fcntl-fallback/no-primitive-raises chain, and the
   _index_file_lock contextmanager (sidecar file, fail-closed timeout).
3. Wrapped log_failure's whole read-modify-write window (both saves) in the
   lock; left _alert_signature_pressure outside the window (it writes its own
   alert paths and must not extend the critical section).
4. Ran the two-process falsifier in both directions; ran the existing FKB
   suite (8 passed); ast.parse green.
5. Claim was filed before first byte read (QUEUE 19:40:49Z). Filed this
   receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This landing is inverted if any of the following holds: (a) the two-process
probe with mode=lock yields fewer than 100 entries on rerun (the lock is not
actually serializing; check that both processes import the edited module);
(b) a single-process log_failure now raises TimeoutError under normal load
(the sidecar file is locked by a crashed process without cleanup, and the
OS did not release it - then the timeout needs a stale-owner story, filed,
not silenced); (c) the index still loses entries while the sidecar shows
lock contention (a writer bypassing the contextmanager exists elsewhere in
the tree; grep for _save_index callers and gate them too).

## Bibliography closed

mag/failure_kb.py (read: header B2-87 block, _load_index/_save_index,
log_failure, _alert_signature_pressure; edited as above);
watch/inbox/burn_wave_20260926/B2_87_fkb_continuity_20260926.md Evidence
(accepted from the brief: 82 vs 62 census, 28=28 sig boundary);
tests/test_failure_kb.py (fixture read, suite run). No network calls.
