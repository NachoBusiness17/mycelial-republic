# ERRNO-22 RUNNER_STATE CURE (register row 7, cure pack item 1) - 2026-10-05

Cure receipt for MASTER_READ_ESTATE.md TS-10 / section 9 item 7(1): "single-writer-guard or path-fix the errno-22 runner_state write (910 rows, use the corrected counts)". Filed beside watch/inbox/BURNDOWN_20261004.md as ordered. Lane: e08-writer-guard, burn run 2026-10-05.

## Corrected counts (the only family numbers this receipt cites)

910 trail rows, byte-verified 2026-10-05 from dashboard/static/trails by parsing each row's quoted failing target path:

- builder 370, target /app/queue/lanes/builder/runner_state.json
- research 513, target /app/queue/lanes/research/runner_state.json
- night 26, target /app/queue/lanes/night/runner_state.json
- prose 1, target /app/watch/PROSE_CENSUS_20261004.md (the census report write, not a runner_state write; counted in the family per the register)
- day_work 0 (its 1 raw Errno-22 row is a TESUJI_DROP prose relay of the research failure, not a day_work writer failure)

Sum: 370 + 513 + 26 + 1 + 0 = 910. A raw grep of "Errno 22" over the mirrors reads 917 because 7 rows are TESUJI_DROP relays (6 in builder.jsonl, 1 in day_work.jsonl, all "from research", Sep 14 to 16). 917 and 376 stay struck; this receipt never uses them as family counts.

## The diff against BOARD_REPAIR_INCIDENT_20260926 (watch/inbox/burn_wave_20260926/)

Same errno class, different surface and ruling:

- Same class: OSError [Errno 22] Invalid argument raised at file open.
- The incident: the SW-07 lane's Errno-22 retries on QUEUE.md were ruled "a concurrent-writer artifact (the same write succeeded moments later)"; the separate truncation there was its own 'w'-mode diagnostic open, and the incident's process fix was "never open a shared file with mode 'w' for a probe".
- The cage trails: the 2026-10-04 diagnosis in mag/lane_runner.py's _save_state comment ruled the lock "external and transient, not code-side" on the evidence that a same-mount 40x open('w') probe ran clean between live failures through the cage bind mount.
- Single-writer census (this sitting, 2026-10-05): a repo-wide grep finds exactly one live-code writer of queue/lanes/<lane>/runner_state.json: mag/lane_runner.py _save_state. watch/monitor_lane.py:31 only references the state file in prose (the rotation_epoch mirror); tools/compile_seats.py:126 and scripts/build_deck.py:83 read it. A concurrent-writer guard is therefore moot for this file: there is no second writer. The sanctioned leg landed as the path fix.

## The cure (code leg, landed 2026-10-04)

mag/lane_runner.py:124-149 `_save_state`: atomic tmp+replace. The tmp file is named .runner_state.json.tmp-<pid>-<ns>, written fresh, then os.replace()d over the live path; on failure the tmp is unlinked and the error re-raised. The failing O_TRUNC open of the live state file is never taken; readers see the old or the new inode, never a half-written state. Landed in commit 9c52757f9 (2026-10-04T04:52:11-04:00, night shift lane 4/10), pattern credited to mag/bay_organs.py's rename-CAS. Companion ordering cure in cycle_night (mag/lane_runner.py:932-938): trail the CYCLE row before persisting last_night, so a state-write failure can no longer swallow the composite row.

## Live proof (this sitting, 2026-10-05)

- The old in-cage daemon (pid 28, running pre-cure code) kept failing after the commit: loop exc research Errno-22 rows through 2026-10-04T12:31:38Z and builder CYCLE_FAIL 12:05:50Z (logs/lane_scheduler.log:10009-10025).
- New daemon UP pid=35138 at 2026-10-04T12:49:43Z on the cured code (logs/lane_scheduler.log:10032).
- Zero runner_state Errno-22 rows since the restart, across ~18h of cycles at 15 to 30 min cadence. The only Errno-22 line in the scheduler log after the restart is a different write path: "2026-10-05T03:59:15Z mirror fail research: [Errno 22] Invalid argument: '/app/dashboard/static/trails/research.jsonl'" (logs/lane_scheduler.log:10152).
- State writes flow continuously through the atomic path: queue/lanes/builder/runner_state.json last_run 2026-10-05T05:00:13Z, queue/lanes/research/runner_state.json last_run 2026-10-05T04:58:13Z.
- Tests: .venv pytest tests/test_night_march_cure_20261004.py tests/test_lane_runner_cluster.py = 33 passed (includes test_save_state_atomic_and_readable, tests/test_night_march_cure_20261004.py:82, which asserts tmp+replace leaves no tmp dotfile).

## Residuals (named, not silently fixed)

1. _mirror (mag/lane_runner.py:161-165) still write_text()s the dashboard trail and surface copies in place: the same O_TRUNC class through the same mount, hit live at 2026-10-05T03:59:15Z (it self-heals next cycle, but the class persists). Fix shape is the same tmp+replace. Outside this row's named scope (the runner_state write) and adjacent to cure pack item 2's trail-EOL territory; left to the owning lane.
2. mag/prose_census.py:145 write_text() of watch/PROSE_CENSUS_<date>.md is the write path behind the family's single prose row. Same class, same fix shape, outside the named scope.

## Falsifier

Reopen if: any runner_state Errno-22 row appears in logs/lane_scheduler.log or any trail after 2026-10-04T12:49:43Z; or a second live-code writer of queue/lanes/<lane>/runner_state.json appears without its own guard; or the corrected counts above fail to reproduce from the trail bytes by the target-path parse.
