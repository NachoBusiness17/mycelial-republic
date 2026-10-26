# SYNTHESIS - reboot patches 2026-10-03, ractor pass 2026-10-04 (filed ~08:40 ET)

Run ractor_engine / 2026-10-04-reboot-patches. Shape self-stolen from
watch/inbox/ractor_engine/2026-10-03-grokbot-estate (lens files, one break.md, SYNTHESIS).
Lenses: correctness.md, container-host.md, concurrency.md, rollback.md, operator-laws.md;
hostile pass: break.md. Live code tree untouched (mag/ and tests/ byte-match HEAD
acb1a0c1d for the patched files). Edits only in the staging worktree (index, no commit);
the only live writes are this folder plus the regenerated 01/05 diffs and APPLY_ORDER.md
in watch/inbox/reboot_patches_20261003 (originals kept in staging under
watch\inbox\ractor_engine\2026-10-04-reboot-patches\orig_20261003\). No .env reads.
Cage touched read-only (stdin-piped scripts, nothing written).

## Verdict counts
Lens findings 28: confirmed 25, weakened 3, killed 0. Real bugs: 2 code, 1 apply order.

## Bugs found and fixed
1. 01: governor TERMINAL missed orchestrator "died" and "stalled". Such a janitor task sat
   pending 6 h and blocked its signature. Fixed (union set + drift test asserting
   orchestrator.TERMINAL is a subset). 01 regenerated; tests 11/11.
2. 05: double-break race. Two waiters judging the same dead marker could each unlink; the
   second deleted the first's fresh lock (two chain writers). 05 makes dead-holder breaks
   real on Windows, so exposure grows. Fixed: re-read marker / re-stat mtime right before
   unlink. 05 regenerated; tests 7/7 + test_verkle_lock 1/1.
3. APPLY_ORDER: 02 applied before a ghost restart un-dams the OLD in-memory janitor loop
   (no governor, stop file ignored, paid tier, verkle --fix quest, spawn-time knots).
   Fixed: new order 01, 03, 04, 05, operator `docker compose restart mag`, in-cage status
   check, then 02, then enable janitor. Rollback 02, 05, 04, 03, 01.

Verification: all patch tests 35 passed; test_verkle*/test_ghost* 80 passed, 3 failed
(pre-existing, identical to the overnight baseline). New order applied to live HEAD in a
temp index: clean, blobs identical to staging for all 13 files. `git apply --check` on the
live worktree: 01, 02, 04, 05 clean.

## Not fixed (documented)
- 02 cage classifier: the 6 mag_launch children read as leaks (measured). Report-only;
  never set MAG_REAPER_LINUX_LIVE=1 until fixed. Expect leak_report.jsonl noise.
- 01 PAID_PROVIDERS is a deny-list (fail-open for new names). Owed: allow-list.
- 05 finally-unlink of a lock broken at 900 s (pre-existing). No lock-break receipt.

## Go / no-go
01 GO (regenerated). 03 GO. 04 GO. 05 GO (regenerated). 02 GO only as step 6, after
the restart and the in-cage `janitor_governor status` shows enabled=false; NO-GO before.

No em-dash bytes.
