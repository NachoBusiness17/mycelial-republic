# correctness.md - lens 1 (2026-10-04 reboot-patches run)

Scope: the five diffs in watch/inbox/reboot_patches_20261003, read against the staging
worktree (lsa_reboot_staging, branch reboot-staging-20261003) and live HEAD acb1a0c1d.

C1 (01) TRUE, BUG. janitor_governor.TERMINAL = {done, failed, timeout, killed, error,
cancelled}. mag/orchestrator.py:73 TERMINAL = {done, failed, timeout, stalled, killed,
died}. A "died" (watchdog, orchestrator.py:1706/1789/1810/1813) or "stalled" (:624) task
was never seen as terminal, so it sat in pending until PENDING_MAX_AGE_S (6 h) and
allow() returned "attempt still pending" for its signature the whole time. Census
(memory/runs/orchestrator/tasks, mtime last 14 d, read-only): 1,204 records, died 85;
janitor (tag copilot-auto-*) died 2 of 630. FIXED in staging, test added.
C2 (01) TRUE. exec_copilot returns outcome "spawned" plus the spawn_task task_id
(ghost.py:1129-1130, orchestrator.py:843-871), so record_spawn's pending path is reached
on a real spawn. Duplicate-goal refusals come back ok=False and count as one failure.
C3 (01) TRUE. Quest output paths match the goal text (ghost.py:1492 vs :1499; :1516 vs
:1522). The FKB diag-file pre-check (:1480) already suppresses a handled signature.
C4 (01) WEAK SPOT, not a bug. The spider quest carries no count, so the
fresh-recurrence rule never applies to it; it retries at the 60 min _auto_dedup cadence
until STUCK after 3. Bounded.
C5 (03) TRUE. _fold_janitor_knot's dossier matches the old one except tension_index (full
sig) and created_at (spawn ts); verkle_knot.py:414-424 passes both through as strings.
C6 (02) TRUE. Module __getattr__ (PEP 562) keeps h.CAGE_DOCTOR and from-imports working;
no other importer of CAGE_DOCTOR exists (rg mag scripts dashboard backend tests main.py).
C7 (04) TRUE. todo moved before the backup only after the REPORT ONLY / seed-sweep
returns, so report output is unchanged. The dwf drop now also applies to --seed-sweep
(behavior change, see break.md B6).
C8 (05) TRUE, BUG (concurrency, see concurrency.md K1). FIXED in staging, test added.

No em-dash bytes.
