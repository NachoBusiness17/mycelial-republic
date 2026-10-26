# concurrency.md - lens 3 (2026-10-04 reboot-patches run)

K1 (05) TRUE, BUG. verkle_lock: waiter judges a marker dead, then LOCK.unlink(). Two
waiters can judge the same dead marker; A unlinks and re-creates (O_EXCL) with its own
marker; B then unlinks A's live lock and creates its own: two writers on the chain.
Pre-existing, but before 05 a dead host holder on Windows was only ever broken by the
900 s mtime rule (APPLY_ORDER Ctrl-C lead), so the race was rare. 05 makes same-namespace
dead-holder breaks real on the host, which widens exposure. FIXED in staging: right before
unlink the breaker re-reads the marker (pid path) or re-stats mtime (stale path) and only
unlinks if unchanged. Residual window is the re-read-to-unlink gap (microseconds), not the
psutil/OpenProcess probe. Test: test_breaker_does_not_unlink_a_lock_retaken_after_judgement.
K2 (05) PRE-EXISTING, owed. The finally block unlinks LOCK unconditionally, so a holder
whose lock was broken at 900 s deletes the next holder's lock on exit. Not touched.
K3 (05) TRUE. Old-code processes (anything not restarted) keep the old probe; an old cage
writer calls os.kill(host_pid, 0), gets ProcessLookupError and breaks a live host lock.
Covered by the step 5 restart in the new APPLY_ORDER.
K4 (01) LOW. Governor state is load/modify/save once per cycle in one process (the cage
ghost). A CLI `clear` landing during exec_copilot can be overwritten by the loop's save.
Workaround documented: re-run clear if status still lists the sig. Not fixed.
K5 (03) UNCHANGED. The fold still runs synchronously inside the async loop (as before) and
can block it up to the 60 s lock timeout. Same as pre-patch behavior.

No em-dash bytes.
