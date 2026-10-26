# MIGRATION CLEANUP 2026-09-19

writer: zcode-seat (sess_833dd189) · order: "top the madness and clean it up" + "scan everything launched today, we did a migration and everything broke, fix it dogfooding our systems and swarms"

## THE FLOOD, EXPLAINED (no live spawner exists)

The 51 "You are a code archaeologist..." chats plus "Reply with exactly CLAUDE"
that appeared in the new ZCode desktop this morning are GHOSTS OF SEP 3, not a
runaway loop. The desktop's first-boot migration (onboarding 08:42, import sweep
08:42:55-08:45:53) wrote 65 claude-import-*.json files under
`C:\Users\foste\.zcode\v2\sessions\8af8c49a6c1b\`, 51 of them the old Sep-3
Claude-Code churn sessions, stamped as created today by the UI. The "Reply with
exactly CLAUDE..." rows are imported lane probes (CLAUDE-ZAI-PONG 09-04,
LANE_OK 09-11). Verified against db.sqlite: zero archaeologist sessions created
since 09-03; zero hits in today's CLI log. The originals remain under
`.claude/projects/`. Safe to bulk-delete the imported copies in the new UI.

## KILLED (process debris)

- 2x host ghost cycle loops (`python -c "from mag.ghost import cycle; while True..."`
  pids 10208, 24812): duplicates of the container ghost daemon, spawned by the
  host supervisor while its reaper was blind. Violated state/DOCKER_ONLY.
- 2x `watch/inbox/_glm_burn.py` (pids 35868, 25064): duplicate v2 burn runs,
  both spinning on HTTP 429 (quota exhausted, matches the GLM BURN ACCOUNTING
  commit). Rerun post-reset on the 20th as already planned. 177 rows of pure
  429 errors in raw_v2.jsonl.
- 1x duplicate `http.server 8799` (uv python pid 24664); kept the venv one.
- 1x unexplained `http.server 8080 --bind 0.0.0.0` (pid 25152, system python,
  no repo or docs reference, exposed to the network). Killed on the
  unexplained-and-exposed rule. If yours, say so and re-serve on 127.0.0.1.

## FIXED (dogfooded, in this commit)

1. **Elder trail lie (owed since 09-18)** `mag/lane_runner.py::cycle_elder`:
   max_tokens 900 -> 1536 (flash_call law: the always-thinking channel eats
   sub-1536 budgets and returns 200 with empty content), and an empty or
   sub-80-char lens now files CYCLE_FAIL instead of a success-shaped CYCLE row.
   Today's 12:00Z "lens on 2 cards" row was written during a 429 lane-down.
2. **Engine bay parked** `watch/engine_spec.json`: engines A(4)/B(1)/E(1)/Z(2)
   -> replicas 0, dated note. The bay's queues are Sep 2-3 fossils mining the
   RETIRED hermes client, dispatched through the openclaw seat. Operator:
   "we don't even use openclaw." The reconciler diffs this spec, so parking the
   spec is the dogfood fix (no process killing needed; nothing resident).
3. **Host supervisor ghost-daemon** `mag/process_supervisor.py` LOOP_DEFS:
   default True -> False. Host spawns were blocked by ghost.py's Docker-only
   law and auto-restarted forever (crash loop, 2 respawns in 8s on 09-18 and
   09-19 per logs/supervisor.jsonl). Container runs the real daemon.
4. **Blind reaper** `mag/process_reaper.py`: bare `powershell` not on PATH in
   the launch context produced 79,864 reaper-enumerate-error rows, so the
   reaper could not see running daemons and supervisors spawned duplicates
   (L8 family). Now resolves the full path (PATH then System32 fallback) and
   logs an honest error if enumeration is impossible. Live-tested: ok.

## CRON SURGERY (automations)

- **Union fullsend 24/7 (*/20)**: deleted automation-b499da5b and recreated
  lean as automation-609237f7. The old one appended into sess_199e4b14
  ("Union fullsend day drive", 09-17) which grew past 723 messages and died
  every fire on `zod: messages[723].parts[5].url too_small`: ~99 failed runs
  across 09-18/19. This is the cron-context-accumulation lesson biting again;
  the new fire is stateless (state files only, one-line reply).
- **Duplicate free-resource scouts**: deleted the 07:30 (automation-5affac13);
  kept the 09:00 (automation-8fdc1a77, has the ALERT-row addition).
- Left alive on purpose: FORGE DAEMON (*/20, 09-13 "2B burn window", 111 runs,
  zero failures) because the operator wants GLM quota burned before the 20th
  reset. WARNING: it appends into sess_712a3b7b (09-13, six days old) and will
  die the same zod bloat death as the union session. Retire or re-seat it at
  the reset.

## OWED (filed, not fixed today)

- Container lanes intermittently fail `EXC OSError 22 Invalid argument` writing
  `/app/queue/lanes/*/runner_state.json` (research/builder trails): container
  writes a timestamp the Windows mount rejects. Migration-era FS mismatch.
- `mag/seat_dispatch.py` still declares openclaw/opencode/mag-openclaw seats
  for a container that no longer exists. Vestigial; harmless while the bay is
  parked. Remove or re-point when a replacement gateway exists.
- ZCode import replays old transcripts with created-today stamps: upstream UI
  complaint + local note. `export-log-stage/` still empty (shadow-steal law
  owed since 09-18).
- Supervisor state.json still records ghost-daemon "crashed"; clears on the
  next supervisor pass with the default off.
