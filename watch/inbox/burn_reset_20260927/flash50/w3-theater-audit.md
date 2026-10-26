# w3-theater-audit: estate THEATER audit, 2026-09-28

Item: audit the estate for THEATER, tools/gates/checks that exist but never fire on real work. Criteria per ask: (1) does it run on a schedule? (2) does it check something that could actually fail? (3) has it ever caught anything? The ask states an audit seat found 3 of 4 self-checks were theatre; find more.

Seat: w3 gopher, 2026-09-28. Everything below was read or run this session. Banked to `watch/inbox/burn_reset_20260927/flash50/w3-theater-audit.md` per the ask.

## Ask-given premise, searched and not found

The "audit seat found 3 of 4 self-checks were theatre" receipt: I searched `watch/inbox/burn_reset_20260927/` (root, flash50, queue) for theat(er|re), "3 of 4", "three of four", "self-check(s) were". Only incidental mentions in 3 flash50 deep-*.md essays. The receipt is not in the tree I searched; the claim is taken as ask-given context, not verified.

## Method (commands actually run this ask)

- `schtasks /Query /FO CSV` + per-task `Get-ScheduledTaskInfo` / `Get-ScheduledTask ...Actions` (14 Mag/Estate tasks).
- `ls -la` + content reads of logs/census_patrol.log, ratchet_daily.log, fts_index.log, vision_nightly.log, corpus_rescan_daily.log, improve_daily.log, day_end_pile.log, docker_watchdog.log, endpoint_news.log.
- Read `githooks/pre-push` (333 lines, 9 gate blocks), `scripts/census_patrol_daily.ps1` (196 lines), `scripts/ratchet_daily.ps1`, `watch/docker_watchdog.ps1`, `watch/docker_watchdog.vbs`, heads of the pythonw task scripts.
- Wiring census: `git grep -l -F <tool>` across githooks/ scripts/ mag/ main.py configs/ docs/ '*.md' for all 34 tools/*.py.
- Live runs: `tools/config_seal.py verify` (rc=1, 4 MODIFIED), PS `Parser::ParseFile` on census_patrol_daily.ps1 (4 errors), `ls` on the state_quantizer placeholder path (exit 2), grep counts on memory/attention.md.

---

## Findings

### Class A: registered, scheduled, and silently dead

**F1. MagCensusPatrolDaily: the whole morning patrol has been unrunnable since 09-27 10:55. Parse-dead, not dark-by-schedule.**
Four checks die with it: the B2-246 census deep check (`--collect`), the B2-469 meter patrol, the fleet task doctor, and the FOSSIL_CENSUS P0-3 fossil check (scripts/census_patrol_daily.ps1:1-6, 113-164, 159-188).
Evidence, all from this ask:
- `Parser::ParseFile` on scripts/census_patrol_daily.ps1: 4 errors, first two `[TerminatorExpectedAtEndOfString] line 194` and `[MissingEndCurlyBrace] line 183`, plus cascade (Try missing Catch at 196). The script cannot execute at all.
- Task truth: `Get-ScheduledTaskInfo MagCensusPatrolDaily` = LastRunTime 9/28/2026 8:30:30 AM, LastTaskResult 1, NextRunTime 9/29 8:30. It ran today and exited 1.
- Log truth: logs/census_patrol.log (33 lines) ends at `[2026-09-27 08:30:02] END exit=0`. Zero 09-28 bytes, file mtime Sep 27 08:30. A run that launched would Write-Log START first (ps1:52); it never got there.
- Root cause: commit 8763e6809 (09-27 10:55, "fossil churn complete ... census patrol single-artifact check replaced") added the fossil arm containing an em-dash inside the fossil here-string (ps1:178, `FOSSIL_CENSUS_20260927.md — recompile`), and the file is UTF-8 without BOM (`head -c 8 | od` = `23 20 4d 61 67 ...`). The task host is Windows PowerShell 5.1.19041 (verified `$PSVersionTable`), which reads no-BOM files as ANSI and treats smart-quote characters as string delimiters: the em-dash's tail byte 0x94 becomes a quote and bursts the here-string. The estate's own no-em-dash law killed its own watchman, through an encoding the law never anticipated.
- Why nobody noticed: nothing gates .ps1 syntax (the ratchet covers py in mag/+tools/; no test parses the patrol; the landing lane never hand-ran the script), and the LastTaskResult=1 that would name it is watched by the task doctor, which lives inside this same broken file. The monitor died with the monitored. The script's own dark-surface law (ps1:28-30: "No START stamp for today in this log: the surface is dark") has had no enforcer for a full day.

**F2. The task doctor's design blindspot: Disabled fossils are invisible forever.** census_patrol_daily.ps1:125-126 (`if ($_.State -eq "Disabled") { return }`). The two dead registrations in F3/F4 cannot ever be named by the one check built to name dead tasks. (Doctor itself dead per F1, so doubly dark until repair.)

### Class B: dead registrations still on the books

**F3. MagLabKit8765.** Last run 8/1/2026, LastTaskResult 4294967295 (0xFFFFFFFF), NextRunTime 1/1/2099, State Disabled. Fossil.
**F4. MagPrivateOffice8765.** Last run 8/1/2026, LastTaskResult 3221225786 (0xC000013A, STATUS_CONTROL_C_ABORT), NextRunTime 1/1/2099, State Disabled. Fossil. Both crash codes from Aug 1; nothing cleaned them up in 8 weeks.
**F5. MagMimoWatchClose.** LastRunTime 11/30/1999 (never ran, result 267011). Its sole action is `cmd /c schtasks /delete /tn MagMimoWatchHourly /f & schtasks /delete /tn MagMimoWatchClose /f`, scheduled 17:25 today. A registered task whose only job is deregistration; after it fires, the hourly MiMo frontier watch (MagMimoWatchHourly, alive, last ran 15:58 result 0, writing watch/inbox/mimo_watch.jsonl, freshest row ts 2026-09-28T20:58:01+00:00) is silently un-armed with nothing to re-arm it. By design perhaps, but the design is a self-destruct with no replacement plan on the task books.

### Class C: the check fires, claims an alarm, and the alarm channel holds nothing

**F6. attention.md is a mute alert channel for the patrol.** logs/census_patrol.log:8 claims `[2026-09-26 11:33:20] ALERT appended to memory/attention.md` (the real COLLECT-DRIFT catch), and :32 claims `[2026-09-27 08:30:02] TASK-DOCTOR: 1 unhealthy task(s) named, alert appended`. This ask, on memory/attention.md (40KB, mtime today): `grep -ic census` = 0, `grep -ic "unhealthy|task.doctor"` = 0. The file's 121 `###` headers are bulk session-record dumps (first header: "### Session record ready"). Both claimed alerts are gone or never landed; which, I cannot prove (the file churns daily), but a standing-attention surface that holds neither of two alerts appended within 48h is not carrying alerts. What the 09-27 doctor flagged ("1 unhealthy task") is now unknowable.
**F7. secret_scan_weekly's prepend arm has the same hole, louder.** scripts/secret_scan_weekly.py:9,27,57 documents "when any critical/high rule count is above zero, prepends a dated alert line at the TOP of memory/attention.md". Its beat row for 2026-09-26T21:13Z shows `critical: 1, high: 48544` (watch/inbox/SECRET_SCAN_BEAT.jsonl). Today attention.md: `grep -ic secret` = 0. A critical finding from Monday has no trace in the surface it is supposed to stand in. Second defect in the same beat: the row is unbounded (files_with_rule_hits dumps thousands of corpus paths; the beat file is 1.3MB after one run) and the counts are corpus noise (dfhack/protobuf third-party code), so even delivered, the alarm is unreadable. Alarm that always screams = alarm nobody reads.
**F8. Daily ratchet: red two days running, log-only, no fan-out.** scripts/ratchet_daily.ps1 is Write-Log only, no alert channel. logs/ratchet_daily.log: 09-27 `END seal=0 freshness=0 ratchet=1` (RATCHET: FAIL), 09-28 `END seal=1 freshness=0 ratchet=0` (CONFIG-SEAL: FAIL, modified=1). Live run this ask: `tools/config_seal.py verify` = rc=1, `sealed=56 live=56 modified=4` (fossil_registry.json, improve.yaml, mirrors.json, violation_baseline.json), "re-seal by NAME". The seal also gates pre-push ENFORCING (githooks/pre-push:11-12, `|| exit 1`), so the next push hits a wall until someone re-seals, and the meter that was supposed to surface the drift two days ago wrote it to a file nobody reads. Not theater in the never-fires sense: it fires, it catches, and it is being ignored, which is the end state theater decays into.

### Class D: pre-push WARN-ONLY advisory gates (fire on every push, cannot block, flip never pulled, catch record)

All in githooks/pre-push, all carrying `|| true` and a TODO-FLIP-TO-ENFORCE comment:

**F9. description_pin (hook:19-24).** WARN-ONLY since 09-25. The 09-26 audit (watch/inbox/audit_20260926/LANE3_GATE_ENFORCEMENT.md:44,227) found it entirely SKIPPED because configs/tools/ did not exist. configs/tools now exists (9 manifests, counted this ask), so it runs; zero offender receipts anywhere in watch/inbox. A gate whose first act was to not run and whose second is to never mind.
**F10. freshness_gate (hook:41-57).** WARN-ONLY, 5-receipt cap. Only recorded fire is a FALSE POSITIVE: watch/inbox/gala_20260925/afterparty/lanes/t51.check.txt captures `PUSH-GATE: freshness WARN: watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md`, which the hook's own t62 comment (hook:32-35) confirms was prose misread as a stamp. Never caught a true stale.
**F11. census push block (hook:76-102).** STALE is WARN-ONLY. The hook's own B2-338 comment (hook:67-75) confesses that before the case-arm fix every fully green push took the WARN arm, output contract bug, and "trained operators to dismiss this channel". In-repo admission of an advisory channel that taught its audience to ignore it. (Its scheduled sibling did catch for real on 09-26, see control group; that sibling is now dead via F1.)
**F12. checkbox_receipt_gate (hook:112-117).** WARN-ONLY since B2-316 (09-26). git grep of watch/inbox finds only its landing receipt, zero WARN outputs on record.
**F13. caption_ledger_verify (hook:140-167).** WARN-ONLY and conditional: fires only when the50_t21_q_caption_ledger{,_verify}.py change (both last touched 09-27, 383fed94f). Zero WARNs on record.
**F14. refold_gate (hook:203-235).** WARN-ONLY and conditional on 3 paths (last touched 09-27). The hook comment (hook:171-179) records that the gap it guards was found by HAND-mutating seqOrderKey and pushing dry-run: the gate was built after the manual catch and has produced none since.
Not classed theater, for the record: workflow_gate_scenarios (hook:280-307) is enforcing and the scenario payload is real, but it triggers on changes to tools/workflow_gate.py only, and the cards dir is untracked by explicit decision (hook:256-261), so card drift alone can never fire it. Narrow by documented design.

### Class E: exists, has no caller, has no input

**F15. tools/prompt_compiler.py.** Wiring census this ask: zero references anywhere in githooks/ scripts/ mag/ main.py configs/ docs/ or any tracked .md. No schedule, no hook, no caller. Born 09-28 (flash50 same wave). A compiler whose compile no process has ever invoked is, by the ask's own criteria, theater on day one until something calls it.
**F16. mag/state_quantizer.py chain fold: zero input by construction.** state_quantizer.py:48 sets VERKLE_CHAIN to the placeholder `memory/biography/# CHAIN_QUERY_MIGRATION_NEEDED: replace with chain.tail() or chain.by_type()`; my `ls` on that path exits 2 (absent); `_read_jsonl` returns `[]` on a missing file (state_quantizer.py:57-58); the fold output memory/ghost/quantum_state/summary_knots.jsonl last wrote Aug 10 (6578 bytes). The chain-side quantize therefore folds zero knots and can never do otherwise until the path is repaired. Corroborates queue/Q-048.md section 7; re-verified independently here.
**F17. MagVisionNightly: a nightly schedule over a finished job.** logs/vision_nightly.log: 11 runs end `END no-op (0 remaining, corpus complete)`; grep for `remaining=[1-9]` across the whole log = zero matches. It has never once done work. It fires, it could in principle fire-for-real if the corpus grows, but as of today it is a 02:30 alarm clock with no alarm.
Classification note: tools/stealth_fanout_wave2.py, tools/derived_dag.py, tools/session_cards.py also have 0-1 references, but each is a dated one-shot runner with its own receipt (Q-010, Q-003), not a standing check; excluded from the theater list.

---

## Control group: alive checks, verified this ask (what non-theater looks like here)

- violation_ratchet: enforcing at push and daily. ratchet_daily.log 09-28: `hits=885 registered=885 NEW=0`, plus two un-accepted GROWTH claims named (secret_gate_scan.py +6, stealth_driver.py +45); 09-27 it FAILed for real. Catches.
- MagFtsIndexDaily (B2-465): logs/fts_index.log 09-26 15:27 `PRE: exit=2` (index older than catalog) then sanctioned REBUILD exit=0, 489548 rows. Caught and self-healed. Fresh today, exit 0.
- census_drift_patrol scheduled (pre-break): 09-26 11:33 COLLECT-DRIFT exit=1, alert path taken, operator refreshed carrier to 1910 the same minute (log lines 6-16). A real catch by the now-dead surface (F1).
- workflow_gate submit gate: memory/workflows/REGISTRY.jsonl, 30 runs, 9 rows `"verdict": "FAIL"` (e.g. tree-doctrine-dig 09-25). Catches.
- MagQCaptionVerifyDaily (B2-271): watch/inbox/QCAPTION_VERIFY_BEAT.jsonl, PASS rows for 09-26/27/28, `RESULT: PASS - 267 rows` each. Young, alive, no catch yet.
- mag-docker-watchdog: every 5 minutes, result 0; watch/docker_watchdog.ps1 logs only on RELAUNCH/DEGRADED, so silence since Sep 24 means healthy engine by design. Alive, not theater.
- MagCorpusRescanDaily: 09-27 exit 1 blip, 09-28 exit 0 with real work (14732 added, 1710 vanished). Alive.
- MagImproveDaily, MagEndpointNewsDaily, day_end_pile: all stamped today with real output (improve 08:00, endpoint 06:30, pile 15:00 classified 1). Alive.
- secret_gate at push (--changed, enforcing, zero baseline, landed 09-27): no catch on record yet; young.
- mimo_watch hourly: freshest ledger row 2026-09-28T20:58:01+00:00. Alive (until F5 deletes it at 17:25).

## Scoreboard

Surface | scheduled | could fail | ever caught | verdict
--- | --- | --- | --- | ---
MagCensusPatrolDaily compound patrol | yes | yes | yes (09-26 drift catch) | F1 parse-dead since 09-27 10:55, exit 1, zero output
task doctor blindspot | rides F1 | yes | n/a | F2 Disabled fossils invisible
MagLabKit8765 | was | yes | no | F3 fossil (Aug 1 crash, Disabled)
MagPrivateOffice8765 | was | yes | no | F4 fossil (Aug 1 crash, Disabled)
MagMimoWatchClose | pending 17:25 | n/a | n/a | F5 self-destruct, un-arms hourly watch
attention.md alert channel | n/a | n/a | 2 claimed appends absent | F6 mute
secret_scan_weekly prepend | weekly | yes | critical=1 on 09-26, no trace | F7 mute + unreadable (48544 high)
daily ratchet / config seal | daily 09:45 | yes | yes, red 2 days | F8 catches, unheeded, log-only
description_pin | every push | yes (now armed) | no | F9 WARN-ONLY, was fully skipped
freshness_gate | every push | yes | 1 false positive | F10 WARN-ONLY
census push block | every push | yes | no (channel self-admits dismissal training) | F11 WARN-ONLY
checkbox_receipt_gate | every push | yes | no | F12 WARN-ONLY
caption_ledger_verify | on caption-script change | yes | no | F13 WARN-ONLY
refold_gate | on fold-host change | yes | no (gap found by hand first) | F14 WARN-ONLY
tools/prompt_compiler.py | nothing | n/a | n/a | F15 zero callers
state_quantizer chain fold | via mag/ghost.py | cannot (empty input) | n/a | F16 folds zero by construction
MagVisionNightly | nightly | no (corpus complete) | never | F17 perpetual no-op

## The pattern (one paragraph)

The estate's failure mode is not missing checks, it is checks whose output has nowhere to go and whose death nobody is structurally able to see: a parse-broken ps1 that kills four checks at once while the scheduler still says Ready (F1), an alert file that doubles as a bulk dump (F6/F7), a red meter with no fan-out (F8), seven WARN-ONLY push gates whose one documented fire was a false positive and whose own comments admit the channel was trained into dismissal (F9-F14), and fossils that the dead doctor would have skipped anyway (F2-F4). Repair order implied by the evidence: fix census_patrol_daily.ps1 (drop the em-dash, add a BOM, parse-gate ps1), re-arm or delete the three fossil tasks before MagMimoWatchClose fires, wire the daily ratchet's exit 1 to attention, and give the WARN-ONLY family a dated flip decision or a tombstone.
