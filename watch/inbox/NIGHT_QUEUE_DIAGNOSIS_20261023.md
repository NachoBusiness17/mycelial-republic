# NIGHT DIAGNOSIS: the free ask-queue lost its drainer (2026-10-22/23 night)

## The finding

`queue/hermes_247_free/` (13 ask dirs pending) has been DARK since
2026-10-19T11:33Z. The usage ledger (memory/runs/hermes_burn/usage.jsonl,
4,794 rows, 3,103 ok lifetime) stops at 10-19T11:33Z mid-429-storm: the
last 8 rows are gemma-4-31b transport failures on a 2-minute retry
cadence, then silence for 3.5 days.

## What it is NOT

- NOT the scheduled task being down. MagHermesBurn247 fires hourly, last
  ran 10-22 11:36 PM, exit 0. But that task drives a DIFFERENT queue:
  hermes_driver.ps1 reads seats/hermes/QUEUE.md (checkbox tasks, fires
  hermes.exe headless on local qwen2.5:7b). The seats lane is ALIVE - it
  completed FREEWIDTH_SMOKE twice tonight.
- NOT MagBoxBurnNightly. Disabled since 10-17, and the ask-queue drained
  until 10-19 anyway.

## What it is

The ask-dir drainer was an in-session cadence (the 2-minute retry spacing
is the signature), not a scheduled task. Its session ended on 10-19
morning and the drain died with it. The queue's AGENTS.md claim
("MagHermesBurn247 re-enabled 2026-10-16 on the free queue") is now
stale: the task was rewired to the seats lane, and no scheduled task
drains the ask dirs.

## Repair options (operator decision, NOT done at night)

1. Repoint or twin the hourly task at a box_burn-style headless script
   that drains queue/hermes_247_free via tools/hermes_burn.py (the
   scripts/run_hidden.vbs pattern is the sanctioned zero-blink shape).
2. Or accept the seats lane as the one true lane and archive the 13
   stale asks (most served programs that have since moved: BOOK
   COMPLETION predates BOOK_V2, NIGHT_ROTATION is 10-19).
3. Either way: AGENTS.md's MagHermesBurn247 line needs its stale claim
   corrected.

Also noted: hermes247_headless.cmd references
C:\Users\etfag\.zcode\workspace\...\hidden_run.vbs (the etfag profile
exists and the vbs is there, so it resolves - but it is a cross-profile
dependency living outside the repo; if etfag ever cleans that workspace
the task silently goes dark with exit 0. Worth repatriating the vbs
into scripts/ on the next touch.)

## Why not fixed tonight

Scheduler rewiring during a sleep window is an operator call (the
Checkpoint incident class: launchers change what the box does while he
is away), and the 13 pending asks are mostly stale - relighting them
blind is open-loop burn (harvest without digestion). Filed for morning.

Consumer: the free-lane burn program + the morning window.
Verifier: usage.jsonl grows again after the repair, or the archive
receipt lands under option 2.
