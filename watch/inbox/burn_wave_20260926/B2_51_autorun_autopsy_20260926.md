# B2-51 governor_autorun autopsy (owed since 9/19, run 2026-09-26)

## Verdict

The 9/19 17:31Z loop was a false crash-loop: the supervisor classified a policy exit as a crash. state/DOCKER_ONLY (created 2026-08-30 22:56 -0400, renamed stale 2026-09-22) plus the child self-block (landed 9/14, d575bc168) made every host spawn of autorun_loop print one line and exit; the pre-gate reap() marked the default loop crashed and respawned it under crashLoopBackOff: 28 auto_restarts on 9/19 (bursts 15:06-15:08Z and 17:09-17:31:17Z; the brief's "4x at 17:31Z" is the final four respawns, 17:30:39, 17:30:46, 17:31:02, 17:31:17), after 9 on 9/14 and 44 on 9/16. The 9/19 21:58Z gate (96b5f4b4e) landed after self-resolution, never fired (0 policy_blocked rows), and its fix comment carried two false evidence claims: "5,708 'blocked' lines" (actual 232; 5,708 is the streak's last line number misread as a count) and "marked 'crashed' for 20 days" (unsupported). The brief's premise is confirmed: the autopsy was offered, never run; the comment cited findings no autopsy produced. Second defect: the policy lived as three private copies (governor_autorun, ghost, process_supervisor) with drifted predicates (children gate on os.name == "nt"; the gate did not).

## Evidence

- logs/supervisor.jsonl:97093-97096: "2026-09-19T17:31:02...auto_restarted...autorun...17872", "17:31:17...37172"; 28 autorun auto_restarts on 9/19; same file 9/20T06:04:36Z: "stopped, autorun, pid 37172" (the last spawn ran ~13h).
- logs/supervisor_autorun.out.log:5477-5708: exactly 232 consecutive "[autorun] blocked: Docker-only runtime is active", bounded by healthy "[swarm-grok-watch]" lines at 5476 and 5709. 232 exceeds the 84 supervisor-logged starts across 9/14+9/16+9/19; the delta is spawn sources sharing the slot log without supervisor rows (detached relauncher pattern, logs/autorun_detached.log).
- state/DOCKER_ONLY.stale-20260922, mtime 2026-08-30 22:56:25 -0400: marker existed 8/30 until the 9/22 rename.
- git 96b5f4b4e docstring: "the 2026-09-19 autopsy found autorun marked 'crashed' for 20 days ... (5,708 'blocked' lines)".
- "20 days" refuted: supervisor.jsonl has 0 autorun rows 9/1-9/13 while the reaper logged thousands of rows daily (2,264 on 9/5); a crashed default loop with expired next_retry_at respawns on the next reap(), so it was not sitting crashed.
- failure_kb.jsonl: zero crash_loop rows in September; supervisor.jsonl: zero policy_blocked/policy_resumed rows ever.

## Work done

- New mag/runtime_policy.py: one marker constant, one predicate (host_runtime_blocked), corrected receipt in the docstring.
- mag/governor_autorun.py, mag/ghost.py: private copies deleted; both import the shared predicate.
- mag/process_supervisor.py: _policy_blocked delegates to the shared predicate (cmd-scan keeps it drainer-scoped); both false-evidence comments replaced with the corrected receipt; reap() docstring pointer updated.
- tests/test_process_supervisor.py: added test_policy_gate_matches_child_predicate.
- Verification: pytest tests/test_process_supervisor.py 11 passed; tests/test_governor_autorun.py + tests/test_ghost.py 32 passed; ratchet check --changed PASS (NEW=0). Live repro with a temp marker: autorun_loop(5.0) prints the blocked line and exits in 0.00s; the gate returns the same verdict as the child and flips when the marker lifts. Full suite (2026-09-26, this lane): 1734 passed / 38 failed / 9 skipped / 1 error in 17:34; zero failures name the four touched files; the two failures in a 14-file dependency sweep (ghost_spooky verkle proof: tip root mismatch on live state; loop_death_guards afk_routing: order pollution) reproduce verbatim with this lane's test files removed.

## Falsifier

- Count check: grep -c "\[autorun\] blocked: Docker-only runtime is active" logs/supervisor_autorun.out.log (232).
- Loop check: grep 2026-09-19 logs/supervisor.jsonl | grep -c auto_restarted.*autorun (28).
- Divergence check: any host where ps._policy_blocked("autorun") != governor_autorun._host_runtime_blocked() under the same marker/env disproves the single-source fix.
- Stated unknown, not papered over: why pid 37172 survived at 17:31:17Z while the marker file existed to 9/22. The designed route is MAG_ALLOW_HOST_RUNTIME=1, but a dead process's env is unrecorded; operator-set env and brief marker absence both fit the bytes.

## Bibliography closed

logs/supervisor.jsonl; logs/supervisor_autorun.out.log; logs/failure_kb.jsonl; logs/autorun_detached.log; state/DOCKER_ONLY.stale-20260922; memory/supervisor/state.json; mag/process_supervisor.py; mag/governor_autorun.py; mag/ghost.py; mag/runtime_policy.py; mag/headless.py; mag/process_reaper.py; tests/test_process_supervisor.py; git d575bc168, 02bcd49be, 96b5f4b4e; tools/violation_ratchet.py.
