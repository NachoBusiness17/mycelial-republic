# operations.md - ractor lens: operations (2026-10-03 grokbot-estate run)

Lens: operations (orchestration surgeon; jacket: the theater surface, running
output nobody consumes). Blast radius and ordering live here. Checks run
18:35-18:50 ET this sitting. Verdicts: TRUE / FALSE / THEATER / UNVERIFIED.

## Findings

O1. Claim under test: "the import crash breaks ALL agent tasks spawned in
mag-sovereign, not just the janitor." TRUE, scoped to orchestrator-spawned
children. Census of memory/runs/orchestrator/tasks/*.json created >=
2026-09-26T21:23Z whose cmd starts /usr/local/bin/python (the cage): 412
receipts, 0 done (375 janitor + 18 api + 13 game-flow-test-nomic_rules_patch +
6 cursor-queued). All 37 non-janitor logs carry "powershell.exe not
resolvable". Mechanism: every agent_cli context build omits fast=True
(mag/agent_cli.py:1031, 2656, 2658, 2886, 3068, 3096), so it reaches the
else-branch import at mag/context_pack.py:682. Other in-cage victims by bytes:
mag/guard.py:17 (module-level import), the dashboard /api/v1/health deep sweep
(docker-compose.yml:76-80 already documents it). Host-side tasks are
unaffected: 46 host receipts reached done after the cutover (soak-test 15,
cursor-external 14, api 10, cloud-external 6, cursor-queued 1).

O2. Arm C dead at 1/30 since 10/1. TRUE.
memory/runs/interference_replication_20260925/armC_boot_run.log (42 B, mtime
10/01 05:50 ET) reads "budget=200 [1/30] solved=True rounds=3" then "^C";
armC_gemma2b_judge_200.jsonl 127 B (one row). Startup\mag_boot_lane.cmd:41
re-runs it in the foreground every logon.

O3. Scheduled tasks failing. TRUE for 8 (Get-ScheduledTaskInfo, 18:4x ET):
Estate KeyAudit rc=1, Estate Ratchet rc=1, Estate Spine Index rc=3221225786
(0xC000013A, STATUS_CONTROL_C_EXIT), MagCensusPatrolDaily rc=1 (may be the
designed COLLECT-DRIFT signal per 2026-10-02-dogfood-48h/break-security.md:61),
MagGapSentinelDaily rc=1, MagLeaveProtocolDaily rc=1, MagTipWitnessDaily rc=2,
MagXRadarDaily rc=2. Green today: EstateWalkDaily 0, MagFtsIndexDaily 0,
MagImproveDaily 0. Estate LaneSupervisor is Disabled (last 9/28).

O4. Supervisor reaper "no powershell". TRUE, and it is the same disease class
as O1. mag/process_reaper.py:86-90: on win32 the code falls back to the
System32 path (:87-88), so the message can only come from the Linux cage.
logs/supervisor.jsonl: 1,056 reaper-enumerate-error rows dated 10-03 UTC,
95,077 lifetime. A blind reaper in the cage cannot see duplicates.

O5. Stealth driver ~28% ticks wasted on dead routes. TRUE but understated.
state/fuel/stealth_driver.jsonl, cycles with ts 2026-10-03 (UTC): 216; work
topic ERR 59 (27.3%): inkling-small:free HTTP 403 x37, llm7 gpt-4o-mini x20,
OSError x2. Also dead every cycle: probe20 "skip: llama-server not up" 216/216,
rumor drill "FAILS: ['deadline']" 216/216.

O6. Boot-lane knot step still knots dwf sessions. TRUE. Startup
mag_boot_lane.cmd:37 passes --skip-subagents --min-messages 5 --since
2026-09-11; memory/runs/knot_at_close_boot.log (18:16 ET) knotted
dwf-dwfrun-af998d42-...-actor_1_2. state/knot_at_close.off does not exist, so
the step is ARMED for the next logon.

O7 (new). Each knot_at_close run writes a full chain backup regardless of
--skip-knot-backup (mag/knot_at_close.py:248-249 copy2 of the chain; the flag
skips only the knots tar). One ~8 MB .bak per logon, no pruning. 18 today.

O8 (new). The janitor fold publishes "autonomous_task_completed" at spawn
time (mag/ghost.py:1515-1521): running output nobody can trust; any bus
subscriber counts a crash as a completion.

Tally (this lens): TRUE 8, FALSE 0, THEATER 0, UNVERIFIED 0.

## Ordering notes for synthesis

- The stop file for O6 must exist BEFORE the reboot, because the boot lane is
  the very thing the reboot fires.
- O1's fix (lazy CAGE_DOCTOR) un-dams 412-class traffic at once; anything the
  janitor would then do (metered deepseek calls, the mutating verkle quest at
  mag/ghost.py:1449-1467) must be governed first.

No em-dash bytes. Filed by the operations lens.
