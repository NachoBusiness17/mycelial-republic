# SYNTHESIS - Grok Bot estate work, 2026-10-03 (filed ~18:55 ET)

Run ractor_engine / 2026-10-03-grokbot-estate. Shape self-stolen from
.zcode/workflows/ractor-engine.dwf.ts (lens library :88-115, LAWS :119-129)
and watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md. Lenses:
accuracy, operations, security, logic, economics (accuracy.md,
operations.md, security.md, logic.md, economics.md), then break.md (hostile
pass, steering, the three blind-audit engine fixes). Read-only sitting; the
only writes are these files. No paid calls, no restarts, no .env reads.

## Verdict counts

Lens verdicts on 39 findings: TRUE 30, FALSE 4, THEATER 2, UNVERIFIED 3.
Hostile pass: confirmed 34, weakened 4, owed 1, killed 0. Cross-lens
contradictions after the gate: 0.

## The chapter

The headline diagnosis holds up. Every orchestrator-spawned agent child in
mag-sovereign since 2026-09-26 17:23 ET has failed: 412 of 412 cage receipts,
including all 37 non-janitor ones, with the powershell.exe signature
(mag/health.py:25-27, commit 48f7f5ace). The hostile pass narrowed "ALL" to
that scope: host tasks and the fast-pack path survive. The same disease also
blinds the cage reaper (mag/process_reaper.py:86-90, 1,056 rows today).

The plan is weaker than the diagnosis. Fix (a) cannot work where it is
written, because the fold runs at spawn time (mag/ghost.py:1472, 1506). The
plan's order (unblock first) would turn about 54 free crashes a day into
metered deepseek calls (goals labelled "$0", configs/cost_rates.yaml:9-15),
and it would arm a 7B "verkle_audit --fix" quest against the shared chain
(ghost.py:1449-1467).

Verkle: the chain is intact (verify re-run: 0 mismatch, 53 dangling, 0
linkage breaks). It is now 18.8 pct dwf actor noise (2,109 of 11,203 rows),
and the boot-lane step that is still armed adds more noise plus an ~8 MB
backup on every logon. The lock-race suspicion now has a named mechanism, a
cross-namespace PID liveness probe (mag/verkle_knot.py:166-185), but no
proven event.

## What Grok Bot got wrong today

1. lan.key was not "staged". Codex already committed it in add33ba72 (16:42
   ET) together with the .gitignore block, under a commit message about D&D
   that mentions neither.
2. The xai- token is the secret gate's synthetic fixture
   (tests/test_gate_blocking_paths.py:215 "Values are fabricated"), not a
   leak. Do not excise it.
3. "About 17" backups is really 18 today and 25 in total (166 MB), and every
   logon adds one more.
4. Plan fix (a) cannot work at ghost.py:1506. The janitor also emits a false
   "autonomous_task_completed" event (ghost.py:1515-1521), and the canonical
   tip is now a failed-task knot.
5. The plan order is unsafe (see above). The boot-lane step shipped with the
   dwf filter bug still in it and without its stop file in place.
6. The "28 pct" stealth waste is understated: probe20 and the rumor drill
   are dead on all 216 cycles too.

Confirmed as stated: the import crash and its commit, the read_only default,
the backfill split (2,157 rows: 2,109 dwf, 45 real, 3 janitor), the
knot_at_close +28/-2 change and its exact HEAD backup, verify 0/53, the live
8765 rebind (container recreated 16:40 ET), CURRENT.md stale, kpi 790 MB,
Arm C at 1/30, and the 8 red tasks.

## Ranked post-reboot sequence

0. BEFORE the reboot: create state\knot_at_close.off. Blast: the one boot-lane
   step is skipped. Verify after logon: knot_at_close_boot.log unchanged and no
   new bak-orphanlane file.
1. Govern the janitor before un-damming it: add a disable flag or register
   entry for autonomous_task_loop (plan c), STUCK-after-3 (plan b), and remove
   or quarantine the mutating verkle quest. Blast: autonomous fixes only (they
   produce nothing today). Verify: one cycle logs "disabled/stuck" and spawns
   nothing.
2. Make CAGE_DOCTOR lazy (plan 0) and audit mag/lifecycle.py:60,
   mag/window_audit.py:23 and guard.py:17. Give process_reaper a Linux path.
   Blast: all 412-class cage agent traffic resumes. Verify: docker exec
   mag-sovereign python -c "import mag.health, mag.lifecycle, mag.window_audit"
   exits 0; one api agent task reaches done; reaper-enumerate-error per hour
   falls to 0.
3. Move the janitor fold to task completion (corrected fix a). Gate it on
   done plus a non-empty output, and drop the false completed event. Blast:
   chain writes and the bus. Verify: the next failed task adds no
   autonomous- row; verify_verkle_full exits 0.
4. Fix the knot_at_close filter so it drops workflow_child (dwf-), and make
   the chain backup keep only the last N. Then remove the stop file. Blast:
   boot-lane knotting. Verify: a --limit run lists 0 dwf candidates; the
   backup count stays at N or below.
5. Lock hardening: tag the lock with host or namespace and break a foreign
   lock only on mtime staleness. Blast: every chain writer. Verify: run
   verify_verkle_full after one concurrent host plus cage write.
6. After the step 5 verify passes, the operator decides on pruning the 25
   backups to the last 2 (a delete, so operator-gated).
7. Rotate the LAN TLS pair and start dashboard/lan_proxy.py. Verify: tablet
   reaches 192.168.86.35:8765.
8. Hygiene: rotate kpi.jsonl at mag/records.py:138; refresh CURRENT.md; file
   an erratum for add33ba72's message; triage the reds (Spine Index
   0xC000013A first, then KeyAudit and Ratchet); drop the dead stealth
   routes; decide whether Arm C stays on the logon path.

## OWED

The real price of a janitor run. Who recreated the container at 16:40 ET.
Whether run_shell survives the read-only strip. Which reader a cold boot uses
(the tip or the boot view). The Ctrl-C common-cause hypothesis
(break.md X1). Contents of lan_proxy.py.

Filed by synthesis. watch/inbox/ractor_engine/2026-10-03-grokbot-estate/SYNTHESIS.md.
No em-dash bytes.
