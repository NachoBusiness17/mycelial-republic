# JANITOR FIX PLAN 2026-10-03

Status: READ-ONLY diagnosis. No code changed, nothing restarted. Stage these after the operator reboot.

## 1. Confirmed cause

The read_only hypothesis is NOT the exit-1 cause. The child crashes at import, before any tool runs.

Exact error (container /app/logs/orchestrator/t1cb9a19404.out.log, also t3415811fbd, t971581e7e3):

    File "/app/mag/health.py", line 26, in <module>
      powershell_exe() + r" -NoProfile -ExecutionPolicy Bypass -File scripts\mag_exec.ps1 doctor"
    File "/app/mag/win_powershell.py", line 40, in powershell_exe
    FileNotFoundError: powershell.exe not resolvable: PATH carries no WindowsPowerShell directory and the System32 candidates are absent (B2-375)

Chain: main.py agent -> agent_cli.run_agent:2656 -> context_pack.build_context_pack:682 `from mag.health import sanity` -> health.py:25-27 evaluates CAGE_DOCTOR = powershell_exe() at MODULE IMPORT time. The container is Linux, there is no powershell, win_powershell fails closed, import dies, exit 1 in about 5s.

Origin: commit 48f7f5ace (2026-09-26 5:43 PM ET, "B2-479 reset-day exposure scoping"), the B2-375 absolute-powershell fix. Blame on health.py:25-27 and win_powershell.py:30-43 both point to it. The first exit-1 task is t501ad3739f at 9/26 5:23 PM ET (21:23 UTC, working tree ahead of the commit), whose log shows an earlier form of the same bug: `from win_powershell import powershell_exe` -> ModuleNotFoundError at health.py:14.

## 2. Timeline from receipts (memory/runs/orchestrator/tasks/*.json, tag copilot-auto-fkb-*)

- t3d3ec8307f 9/26 4:58 AM ET: timeout (300s). Log shows a normal agent run.
- t9466563e4d 9/26 5:01 AM ET: done, exit 0. LAST success. This is the "since 5:01 AM" anchor, but failures were not exit 1 yet.
- 9/26 5:58 AM to 4:23 PM ET: about 30 tasks, all status=timeout, not exit 1.
- t501ad3739f 9/26 5:23 PM ET: FIRST failed exit 1. Every janitor task since is failed exit 1 (373 failed since 9/26).
- Newest three (10/3 ET): t971581e7e3 4:06 PM, t3415811fbd 4:35 PM, t1cb9a19404 5:16 PM. All failed, exit 1, about 5s.

## 3. The read_only issue is real but secondary

- spawn_task(read_only: bool = True) at orchestrator.py:640 came from commit 3752abae2 (9/25 11:42 PM ET), not 9/26. Pre-cutover logs already carry `--read-only` and "read-only seat: 3 write tool(s) stripped from schema (write_file, pheromone_drop, blackboard_post)".
- ghost.py:1124 (copilot exec path; janitor quests arrive tagged copilot-auto-fkb) never passes read_only, so the child cannot write memory/runs/ghost/autonomous_fixes/*.md. Evidence: t9466563e4d "done" claimed it wrote the file, and the false-success guard escalated it ("claimed edits but ran no mutating tool"). So even before 9/26 PM the janitor produced no diagnoses. It went timeout/fake-success, then crash.
- Note: git blame shows orchestrator.py:635-645 as "Not Committed Yet" though git status is clean; likely a line-ending artifact. Recheck before editing.

## 4. Staged fix (after reboot), DFHack-style per corpus/df_mine/DFHACK_THESIS.md

0. Unblock (prerequisite): make health.py CAGE_DOCTOR lazy (function or try/except that yields None/"unavailable" off-Windows). Same audit for lifecycle.py and window_audit.py, which also import powershell_exe. Rule: no subprocess-resolution at import time. Add a container smoke test: `python -c "import mag.health"` inside mag-sovereign.
a. Knot only on success: ghost.py:1483 to 1506 folds every result to Verkle via append_verkle_knot, including failures. Gate the fold on outcome done plus the output file existing and being non-empty. Failures go to the trail only.
b. fix/fkb-diagnose script: a named janitor script that calls spawn_task(read_only=False) but pins writes to the single output path memory/runs/ghost/autonomous_fixes/<sig>.md (write allowlist via write_strip, not open write). Re-arm only on a fresh recurrence (occurrence count rose since last attempt). Mark the signature STUCK after 3 consecutive failures and stop spawning until an operator clears it.
c. Enable/disable register: add each loop (autonomous_task_loop and the janitor scripts) to mag/loops_registry.py with enabled flag, last_ok, fail_count, and a `disable` verb, like DFHack enable/disable. The ghost loop checks the register before each cycle.
d. Event triggers instead of the 60s timer: autonomous_task_loop(interval_s=60.0) at ghost.py:1314 polls. Replace with triggers on failure_kb.jsonl append (new or rising signature) and copilot inbox write, keeping a slow fallback poll.
e. Full signature in tension_index: store the full sig (module:hash, e.g. amd_window_guard:5c63f4a34186) and not the truncated tag (copilot-auto-fkb-17c). The empty-module sig `_:d2b80153f96b` shows the module part is also lost upstream. Fix that too.
f. Dedupe governor_autorun.py:546: the PIPE 4 spider-blind block appends the same "[janitor] Spider is blind..." todo every cycle. Guard with a same-text-already-pending check (spawn_task already has same-goal dedupe; mirror it).

## 5. Blast radius of changing the spawn_task read_only default

Callers relying on the default (rg spawn_task, mag/ main.py scripts):
mag/fork_router.py:256, mag/frontier_scout.py:479, mag/ghost_director.py:282, mag/ghost.py:1124, 2376, 2961, 3489, 3638, 3792, mag/grok_free.py:206 ("Execute build package... implement it" which needs writes, likely already broken by the default), mag/gpipes.py:122, mag/orchestrator.py:1388, 1479, 2035 (queue dispatch), mag/roadmap_runner.py:247, mag/self_drive.py:207, mag/session_maze.py:189, mag/stateless_research.py:118, mag/voice_trigger.py:139. Docs reference: mag/write_strip.py:13, mag/elevate.py:133.
Recommendation: do NOT flip the global default. Pass read_only=False explicitly only at the janitor site with the pinned path. Audit grok_free, roadmap_runner, self_drive, and queue dispatch separately, since build-type goals have been silently write-stripped since 9/25.
