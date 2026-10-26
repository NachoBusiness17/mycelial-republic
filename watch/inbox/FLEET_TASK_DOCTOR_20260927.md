# FLEET TASK DOCTOR + HEADED-WINDOW FIX 2026-09-27

Class: RECEIPT · Writer: zcode seat · Operator order: "why do we have a bunch
of headed python windows? ... they should be headless and doctors should be
making sure these things are working properly"

## Verdict

The headed windows were four scheduled tasks firing console-subsystem
python.exe in the interactive session. All four converted to headless
pythonw.exe (same venv, same args, triggers untouched), the estate's own
hidden pattern (mag-docker-watchdog via wscript) generalized. The doctor
pass over all 13 fleet tasks found three instruments that have NEVER fired
and one failing daily, the elder's instruments-built-not-run disease in
scheduled-task form, named below.

## Evidence

Task census 2026-09-27 ~01:45 EDT (Get-ScheduledTask + Get-ScheduledTaskInfo):

| task | state | last result | doctor verdict |
|---|---|---|---|
| mag-docker-watchdog | Ready, 5-min cadence | 0 | healthy, already headless (wscript vbs) |
| MagArmC200 | RUNNING since 01:00 | 267009 (running) | interference replication Arm C-200 leg; was the persistent headed window; next fire inherits pythonw |
| MagMimoWatchHourly | Ready, hourly | 0 | healthy; hourly console flash now gone |
| MagCensusPatrolDaily / MagFtsIndexDaily / MagEndpointNewsDaily / MagVisionNightly | Ready | 0 | healthy (powershell wrappers, log-writing) |
| MagImproveDaily | Ready | 1 | FAILED its 09-26 08:00 run, nonzero result unexamined: owed |
| MagCorpusRescanDaily | never ran (267011) | next 03:30 tonight | instrument never fired since registration: owed |
| MagQCaptionVerifyDaily | never ran (267011) | next 07:30 | instrument never fired: owed |
| MagSecretScanWeekly | never ran (267011) | next 09-28 | never fired; now redundant with the live pre-push secret gate (gate 10): recommend retire to report-only or delete |
| MagLabKit8765 / MagPrivateOffice8765 | Disabled | - | fine |
| MagMimoWatchClose | future trigger 09-28 17:25 | - | self-deleting pair, fine |

## Work done

1. Enumerated all Mag* fleet tasks with actions, states, last results.
2. Converted MagArmC200, MagMimoWatchHourly, MagQCaptionVerifyDaily,
   MagSecretScanWeekly actions from python.exe to pythonw.exe via
   Set-ScheduledTask (output: headless-ok x4). Running Arm C-200 instance
   unaffected; conversion applies to its next fire.
3. Named the never-fired instruments and the failing daily above.

## Owed

- MagImproveDaily result=1 autopsy (why the 09-26 08:00 run failed).
- Standing doctor: task health (last result + log freshness per task) folded
  into a daily patrol so never-fired instruments surface within a day, not
  at operator boot time. Proposed home: drift patrol step or its own
  09:30 task; operator picks.
- MagSecretScanWeekly disposition decision (retire vs report-only), per the
  gate builder's canonical recommendation.

## Falsifier

If any converted task fails under pythonw (a script that genuinely needs a
console, e.g. stdin reads), its next fire logs nothing and last result goes
nonzero: the daily doctor catches it, revert that one task to the wscript
hidden-launcher pattern instead.
