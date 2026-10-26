---
name: fleet-task-doctor-20260927
description: 9/27 operator "headed python windows + doctors should check these
  things" — 4 schtasks converted python.exe→pythonw.exe headless; task census
  found 3 NEVER-FIRED instruments (267011) + MagImproveDaily failing (result 1);
  standing task-doctor patrol owed; wscript-vbs watchdog = the estate's hidden
  pattern
metadata:
  node_type: memory
  type: project
  originSessionId: sess_d42ed958-1e03-4724-98a6-b625a21eaea5
---

Operator 9/27 ~01:45: "why do we have a bunch of headed python windows? i'm fine with it for now but they should be headless and doctors should be making sure these things are working properly."

**Cause:** fleet scheduled tasks firing console-subsystem `python.exe` in the interactive session. The persistent window was MagArmC200 (interference replication Arm C-200 leg, running since 01:00); MagMimoWatchHourly flashed one every hour; MagQCaptionVerifyDaily + MagSecretScanWeekly would have joined at dawn.

**Fix applied (headless-ok x4):** Set-ScheduledTask action swap to `.venv\Scripts\pythonw.exe` (same venv, same args, triggers untouched) for MagArmC200, MagMimoWatchHourly, MagQCaptionVerifyDaily, MagSecretScanWeekly. Running Arm C instance unaffected; conversion applies next fire. The estate already owned the hidden pattern (mag-docker-watchdog via wscript vbs) — the fallback if any converted task genuinely needs a console is the wscript hidden launcher, not python.exe.

**Doctor census (receipt watch/inbox/FLEET_TASK_DOCTOR_20260927.md, INDEX seq ...3664):** MagCorpusRescanDaily, MagQCaptionVerifyDaily, MagSecretScanWeekly have NEVER fired since registration (last result 267011, last-run 1999) — the elder's instruments-built-not-run disease in schtasks form; MagImproveDaily FAILED its 9/26 08:00 run (result 1, autopsy owed); MagSecretScanWeekly is now redundant with the live pre-push gate (retire to report-only per the gate builder's canonical recommendation); healthy: docker-watchdog, CensusPatrol, FtsIndex, EndpointNews, VisionNightly, MimoWatchHourly.

**Why:** operator expects fleet machinery to be invisible and self-doctoring; visible windows and silent never-fired instruments are both trust damage.

**How to apply:** any new schtask gets pythonw.exe (or the wscript wrapper) from birth, and the owed standing doctor (task health = last result + log freshness, folded into a daily patrol, proposed 09:30 or drift-patrol step; operator picks) so a never-fired instrument surfaces within a day, not at his boot screen. Falsifier: a converted task failing under pythonw shows nonzero last result + dead logs → revert that one to the wscript pattern.

**STANDING HOME LANDED 9/27 (grind window):** census_patrol_daily.ps1 now runs a Mag* task-health pass every 08:30 (WARN-only, hard-catches its own errors so a broken doctor never blinds the census/meter steps, Disabled tasks skipped) alerting memory/attention.md; rule = Ready task with LastTaskResult not in {0, 267009-running}, plus 267011-never-ran with a PAST NextRunTime = dead registration. Dry-run first light caught REAL disease: (1) **MagArmC200 died 0xC000013A (console Ctrl-C) when its headed window got closed** — only a 127-byte header banked; relaunched headless and Running, and headless conversion means it can never die that way again; (2) **MagCorpusRescanDaily fired for the first time ever 3:30 AM 9/27 and FAILED exit 1** (autopsy owed); (3) MagImproveDaily autopsy closed to finding-level: the 9/26 run COMPLETED its work (field brief, latest report, candidates all on disk, llm_used false) and exited 1 anyway — the exit contract lies; root return-1 line in main.py's improve path owed to a fresh lane. Bash lesson re-confirmed: inline PowerShell with $_ in Bash gets variable-expanded into garbage — always -File a .ps1.
