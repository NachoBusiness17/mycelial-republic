# rollback.md - lens 4 (2026-10-04 reboot-patches run)

R1 TRUE. Every diff reverses cleanly with -R (same flags as apply). Files 01/03 share
mag/ghost.py, so 03 must be reverted before 01 (already stated).
R2 TRUE, hazard, documented. Reverting 01 (and restarting) while 02 stays applied gives
the ungoverned janitor with the cage un-dammed. New APPLY_ORDER: full rollback order
02, 05, 04, 03, 01; never leave 02 applied with 01 reverted. Fast stop without rollback:
python -m mag.janitor_governor disable.
R3 TRUE. Leftovers after rollback are inert: memory/runs/ghost/janitor_governor.json,
state\janitor.off, 3-field lock markers (old code reads split()[0]).
R4 TRUE. 04 rollback needs the stop file first (stated).
R5 TRUE. Rollbacks land live in the cage for new processes only; a restart is needed to
unload reverted ghost/verkle code from long-lived processes.

No em-dash bytes.
