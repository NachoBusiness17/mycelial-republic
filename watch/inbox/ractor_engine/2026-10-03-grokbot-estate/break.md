# break.md - hostile second pass + steering (2026-10-03 grokbot-estate run)

One file for all five lenses (deviation from the engine's break-<lens>.md
naming, noted; content follows break-security.md shape). Verdict vocabulary
per .zcode/workflows/ractor-engine.dwf.ts:239: confirmed / weakened / killed.
FULL COVERAGE LAW (blind_audit_ractors_20261002.md:154-157): every lens
finding gets a verdict below. Re-ran this sitting: task-receipt census, log
signature census, chain census and diff, verify_verkle_full, schtasks info.

## Verdict per finding (39)

accuracy: A1 confirmed, A2 confirmed, A3 confirmed, A4 confirmed, A5 confirmed
(the plan line is false), A6 confirmed, A7 confirmed, A8 confirmed, A9
confirmed, A10 confirmed (re-run, exit 0), A11 confirmed (git diff --cached
empty AND add33ba72 --stat shows memory/tls/lan.key 27 deletions: reworded
recheck by quantity, not phrase), A12 confirmed, A13 confirmed, A14 confirmed,
A15 confirmed.
operations: O1 WEAKENED (see H1), O2 confirmed, O3 WEAKENED (see L6: the 8
reds are not one class), O4 confirmed, O5 confirmed, O6 confirmed, O7
confirmed, O8 confirmed.
security: S1 confirmed, S2 confirmed, S3 confirmed, S4 confirmed, S5 WEAKENED
(mechanism only, no clobber event in the bytes), S6 OWED (cannot be
confirmed without reading the strip list or running the quest).
logic: L1-L6 confirmed.
economics: E1 WEAKENED (no dollar figure exists), E2-E4 confirmed.

Count: confirmed 34, weakened 4, owed 1, killed 0.

## Attacks on the top conclusions

H1. Is the import crash really universal? Partly. Survivors in the bytes:
(a) build_context_pack(fast=True) skips the health import
(mag/context_pack.py:663-680); (b) the ghost parent survives because its
health imports are lazy; (c) host-spawned tasks run (46 done since cutover);
(d) cage commands that are not orchestrator receipts were not censused.
Survives as: every orchestrator-spawned main.py agent child in the cage since
2026-09-26 17:23 ET has failed (412 of 412), plus guard.py, the dashboard deep
health route, and the cage reaper share the class.

H2. Did the backfill damage boot quality? Integrity: no (linkage break 0,
mismatch 0, tip ok). Signal: yes. dwf- rows are 2,109 of 11,203 (18.8 pct) of
the chain; the 18:16 ET boot-lane test made a dwf actor the tip until the next
janitor knot at 22:19Z (18:19 ET) replaced it with a failure knot. Every logon
adds more dwf knots while O6 stands. Read-side verkle_boot_view.py filters
both; the canonical tip does not.

H3. Did Grok Bot's edits violate one-supervisor or no-timed-schedules? No.
The boot-lane step (mag_boot_lane.cmd:31-37) is a detached one-shot under
verkle_lock, fired at logon, stoppable by state\knot_at_close.off, matching
the cmd's own law text (:2-5) and memory/operator_directives.md:102 ("One
supervisor"). Not Grok Bot's: the 8 red patrols are DailyTrigger timers.

H4. Was the lock race real? The door is real (verkle_knot.py:166-185 trusts
a cross-namespace PID probe); no event is proven. Kept as weakened.

## What the lenses missed (additions)

X1. Ctrl-C fingerprint, hypothesis only. Estate Spine Index last result
0xC000013A (STATUS_CONTROL_C_EXIT) and armC_boot_run.log ends "^C". On Windows,
signal.CTRL_C_EVENT equals 0, so os.kill(pid, 0) at verkle_knot.py:171 is not
a harmless liveness probe there (Python os.kill Windows semantics, from
documentation, not re-read this sitting). Common cause UNVERIFIED; OWED.
X2. The container was recreated at 16:40 ET today (docker inspect); the
port change is live. Attribution of that recreate is OWED.
X3. The stop file is absent right now: the next logon will knot dwf sessions
and write another ~8 MB backup unless it is created before the reboot.

## Steering round (weakened findings revised once)

O1 revised: "all orchestrator-spawned agent children in the cage" (scope
named). O3 revised: "8 nonzero, of which 1 designed signal, 2 cannot-verify,
1 Ctrl-C kill, 4 unattributed". S5 revised: "mechanism present, event
unproven, chain intact at 11,203". E1 revised: "turns free crashes into
metered calls; price OWED".

## Engine fixes applied (blind_audit_ractors_20261002.md:146-157)

1. Cross-lens contradiction gate: intersected per path. A11/S1
(memory/tls/lan.key) agree; A5/L4 agree (CONVERGENT); A6/O6/H2 agree; A9/E3
agree; A12/S2 agree; O1/O4 same class. Unresolved contradictions: 0.
2. Quantifier lint: every zero/all/every claim names its instrument and scope
(see accuracy.md quantifier section; O1 and S3 carry scope in-line).
3. Reword recheck + full coverage: A11 rechecked by quantity (27 deleted
lines in a commit) not by the word "staged"; all 39 findings verdicted above.

No em-dash bytes. Filed by the hostile pass.
