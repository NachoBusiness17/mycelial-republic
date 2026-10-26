# B2-314 receipt: census patrol liveness tripwire (2026-09-26, lane SW-03)

## Verdict

LANDED. The attended surface mag.cmd context-pack now reads the last bracketed START stamp from logs/census_patrol.log and NAMES the darkness: "census patrol dark since <stamp> (<hours>h > 26h; check schtasks /Query /TN MagCensusPatrolDaily)" when the stamp is older than 26 hours, with distinct dark lines for a missing/blank log ("no START stamp found ... never ran, log deleted, or task deregistered") and an unparseable stamp. Live check today: "census patrol live: last START 2026-09-26 11:34:24 (5.0h ago)". The deregistration falsifier is simulated at the byte level in tests (stale/empty/missing logs all produce named darkness); 6/6 tests pass. The B2-246 falsifier class (a week with no scheduled deep check and zero signal) now surfaces within one context-pack run of the silence.

## Evidence file:line quotes

- scripts/census_patrol_daily.ps1:28-29 (the operator paragraph that defined the condition, previously read by nobody attended): "No START stamp for today in this log: the surface is dark (machine off, logged out, task deregistered). Respond: `schtasks /Query /TN ..."
- scripts/census_patrol_daily.ps1:39,41-43: "$Stamp = Get-Date -Format \"yyyy-MM-dd HH:mm:ss\"" / "Write-Log ... $line = \"[$Stamp] $Msg\"" (the stamp format the module parses).
- logs/census_patrol.log line 1 and 10: "[2026-09-26 11:33:20] START census deep check (--collect) cwd=..." / "[2026-09-26 11:34:24] START census deep check (--collect) cwd=..." (last stamp wins; live status 5.0h at check time).
- QUEUE.md B2-314 row (brief): "read the last bracketed START stamp from logs/census_patrol.log and name 'census patrol dark since <stamp>' when it is older than 26 hours ... falsifier: deregister the task, run the checking surface, and it must name the darkness, today nothing does".

## Work done

- mag/census_liveness.py (new): patrol_status() parses the last "[YYYY-MM-DD HH:MM:SS] START" stamp, computes age against wall clock (26h = daily 08:30 cadence + slack), never touches mtime (B2-237 law), never self-repairs, and never raises on log problems (unreadable/stamp-less logs are named darkness). report() is the one-line attended-surface hook.
- main.py context-pack branch: calls census_liveness.report() after the pack print (both the pack and the --agent preamble paths return before it; the full-mode surface carries the tripwire, matching the brief's "mag.cmd context-pack" choice).
- tests/test_census_liveness.py (new, 6 tests): fresh stamp live; stale stamp names darkness with the exact prefix and the schtasks response path (51.48h case); missing and stamp-less logs dark with reason; last-stamp-wins and garbage tolerance; report() prints the line; main.py wiring pinned (import + call inside the context-pack branch).

## Falsifier

The brief's falsifier, executable: deregister the task (schtasks /Change /TN MagCensusPatrolDaily /Disable or /Delete), wait out the 26h window (or backdate a test log, as the stale test does), run mag.cmd context-pack, and the output must contain "census patrol dark since <stamp>" (test_stale_start_names_darkness_with_stamp pins the exact line shape; the wiring test proves the surface calls it). Additional kills: (a) a mtime-based "liveness" check replacing the stamp read (the module has no mtime input by construction), (b) the tripwire silently repairing (rescheduling, log rewrite: the module writes nothing), (c) the context-pack branch dropping the call (wiring test red).

## Bibliography closed

- scripts/census_patrol_daily.ps1 (stamp format, operator paragraph, log path)
- logs/census_patrol.log (real stamps read; live status computed)
- main.py (context-pack branch, wired)
- mag/census_liveness.py (new module)
- tests/test_census_liveness.py (new)
- watch/inbox/burn_wave_20260926/B2_237_touch_law_20260926.md (the mtime law constraining the design)
- QUEUE.md B2-314 row (brief; self-fed by B2-246 lineage per its renumber note)
