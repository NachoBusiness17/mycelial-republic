# BREAK - hostile second pass over the 48h dogfood lens set (2026-10-02)

Role: break-dogfood. Every evidence byte of the four banked findings in
dogfood.md was re-checked against the live estate this sitting (checks ran
11:05Z to 11:25Z, 2026-10-02, local EDT clock). Additions are what BOTH the
lens and the prior synthesis (watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md,
~06:58Z) missed. Nothing below is asserted that was not read or run here.
No em-dash bytes.

## Verdicts

### F1 pidfile guard vs the surviving pre-guard driver - CONFIRMED (strengthened)

Re-ran every leg, four minutes after the lens's own read, and the exposure is
still live:

- Process: powershell Get-CimInstance Win32_Process -Filter 'ProcessId=44072'
  returns bash.exe alive, CreationDate 10/1/2026 5:31:24 PM EDT, CommandLine
  "bash.exe scripts/descent_driver.sh".
- Birth equals beat cycle 1: memory/runs/hermes_burn/driver.beat:1 reads
  "BEAT 2026-10-01T21:31:24Z cycle=1" - the running loop was parsed at birth,
  10h before the guard existed. The lens's cycle 933 at 11:01:01Z (beat:933)
  had advanced to cycle 941 at 11:07:33Z (beat:941) by my read: still draining.
- No pidfile: the full state/ listing contains no descent_driver.pid (checked
  11:05Z). The guard block sits at scripts/descent_driver.sh:10-23 (PIDFILE
  line 13, refusal exit 3 line 18, stale reclaim line 20, write+trap lines
  22-23; the lens said 10-24, one line generous), and
  git log -1 -- scripts/descent_driver.sh = e3c7d341c 2026-10-02 03:31:54 -0400.
  A driver born without the guard never wrote the pidfile, so the guard is
  blind to it by construction. QED.
- No dollar damage yet, re-derived independently: driver.log tail is all
  "cost=$0.00 (skipped)" with "HERMES-BURN: PASS ... ledger total $37.76", and
  my own re-sum of memory/runs/hermes_burn/usage.jsonl reads 236 rows,
  $37.7591, max ts 2026-10-01T21:53:52Z - zero spend since 21:53Z yesterday.
  The lens's falsifier (pidfile present, or PID gone) did not trigger.

The lens's move (STOP, wait one ~48s beat, relaunch guarded) is sound; note
the beat cadence measured across cycles 503-941 is ~48.6s/cycle here, while
the prior synthesis measured 55.2s/cycle across its window - both are
moment instruments, consistent with the mixed-instrument cadence finding.

### F2 INDEX lags events; headline receipts registered nowhere - WEAKENED (core holds, two bytes off)

Core confirmed on every leg:

- watch/inbox/INDEX.json mtime Oct 2 00:18 EDT = 04:18Z (ls); index_events.jsonl
  appended through 11:02Z+ (last row autoseal of dogfood.md at 11:02:24+00:00).
- Register rows after 04:18Z, my rule (json parse, ts[:19] > 2026-10-02T04:18:00):
  107 at 11:10Z, 109 at 11:20Z - the surface is live and still diverging. The
  lens's 114 does NOT reproduce under that rule (3 unparseable lines noted;
  even all-ops-after-0418 is 208, histogram register=109 / autoseal=97 /
  invalidate=2). Same class, count not byte-identical.
- fillball/citation-lint.md: events count=2, first ts 2026-10-02T06:16:46Z,
  INDEX count=0 - exactly the lens's bytes. percolator-candidates.md and
  census_refresh_20261002.md same shape (events 2 each, INDEX 0).
- NIGHT_CLOSE_20261002.md and POSITION_CHANNEL_RESULT.md: grep 0 in BOTH
  surfaces, confirmed. POSITION_CHANNEL_RESULT.md EXISTS at
  watch/inbox/model_garden/POSITION_CHANNEL_RESULT.md (13,416 bytes, mtime
  Oct 2 02:09 EDT = 06:09Z, matching the prior synthesis's NTFS creation
  06:09:53Z), so the lens's hand-register move is legitimate - but the
  finding's framing "the night's two headline receipts" is wrong for it: it is
  a POST-close 06:09Z artifact, not a night receipt (NIGHT_CLOSE:40-42 said
  "never existed" truthfully at its 05:14Z close). One of the two is a
  boundary case, not a co-equal headline receipt.
- schtasks /FO CSV /V via powershell findstr: "index_fold" 0 matches (which
  also covers any action referencing scripts/index_fold_host.mjs, since the
  sweep reads all columns), control "census_patrol" 1 match; the mjs host
  exists (40,108 bytes, Sep 30 08:11) and is scheduled nowhere; the rebuild
  verb is documented at mag/shared_surface.py:15 exactly as cited.

### F3 patrol re-registration proven for 1 of 4 - CONFIRMED (with the not-yet-due precision)

- Get-ScheduledTask + Get-ScheduledTaskInfo this sitting: MagFtsIndexDaily
  LastRun 10/01/2026 09:00 Result=1 NextRun 10/02/2026 09:00;
  MagImproveDaily 10/01 08:00 Result=1 NextRun 10/02 08:00;
  MagLeaveProtocolDaily 10/01 08:00 Result=1 NextRun 10/02 08:00 - and all
  three actions are now DIRECT (powershell -NoProfile -ExecutionPolicy Bypass
  -File ...\fts_index_daily.ps1 / improve_daily.ps1;
  .venv\Scripts\python.exe ...\leave_dispatcher.py), byte-matching the
  re-registration claim inside e3c7d341c.
- Log dark-legs: logs/fts_index.log last write Sep 30 09:00 (lens said last
  stamp 2026-09-30 09:00:02 - mtime agrees), logs/improve_daily.log Sep 30
  08:01; no leave log exists under logs/ at all.
- Census proven by hand-fire: logs/census_patrol.log ends
  "[2026-10-02 03:29:15] END exit=1" (the COLLECT-DRIFT), task LastRun
  10/02/2026 03:29:29 Result=1, answered byte-exact by
  watch/inbox/census_refresh_20261002.md (4,147/496 at 10:08Z).
- Fifth task unswept: mag-docker-watchdog still fires
  wscript.exe ...\watch\docker_watchdog.vbs every 5 minutes (LastRun 10/02
  07:10:10 Result=0, NextRun 07:15:15).
- invisible_runner.vbs: referenced by ZERO tasks (findstr over full CSV /V),
  unchanged since commit 662dc739e (2026-09-30), worktree clean;
  %TEMP%\invisible_runner_rc.log reads "1" - the lens's byte, and see
  Addition A1 for what that byte hides.

Precision the lens under-weighted (its own blind spot admits it): at its
11:01Z check, the three unproven tasks' first post-fix fire times (NextRun
08:00/09:00 EDT = 12:00Z/13:00Z) had NOT yet come due - the B2-465
no-START-stamp test is not yet applicable to them. "Dark-unproven" is honest;
"dark by the estate's own test" overstates until after 13:00Z. The falsifier
resolves itself this afternoon.

### F4 citation-lint wiring uncommitted - CONFIRMED (one label corrected, move cost wrong)

- git log -3 -- githooks/pre-push: f0768f3be (2026-09-30 17:38:26 -0400),
  dffd32a72, 48f7f5ace - no spine commit touched the hook. Correction: at
  2026-09-30T21:38Z, f0768f3be is INSIDE the stated window (from 20:00Z);
  the right label is pre-spine, not pre-window. Immaterial to the finding.
- git diff HEAD -- githooks/pre-push: 16 "^+" lines = the +++ header + exactly
  15 added lines, including "+echo \"PUSH-GATE: citation_lint check --changed\""
  and "+.venv/Scripts/python.exe tools/citation_lint.py check --changed || exit 1".
- git config core.hooksPath = githooks (the local hook does run here);
  tools/citation_lint.py last commit 3c83da5b0 with a clean worktree row;
  tools/code_swarm.py is M in the worktree (+48/-1, characterized, unaudited).

Move correction (see A6): "commit the diff now (~5 min)" would arm a gate that
FAILS on the current changed tree (blocking=3). Committing it without fixing
or baselining those three findings bricks the next push. The real move is
fix-or-baseline first, then commit the hook, ~25 min.

## Additions (what the lens missed)

### A1 A SECOND unattributed invisible_runner fire at 06:20:49Z overwrote the 23:32 evidence mid-audit

%TEMP%\invisible_runner_rc.log (Windows temp, read via powershell this
sitting): content "1", LastWriteTime 10/02/2026 02:20:49 EDT = 06:20:49Z.
The prior synthesis quoted the 23:32:51 EDT launch as "exit code 7"
(SYNTHESIS.md:93); for that figure to be true its lens must have read the
file between the run's 06:11Z start and 06:20:49Z, because at the synthesis's
own 06:53-06:58Z verification stamp the file already read "1". So a NEW
wrapper fire happened at 06:20:49Z, rc=1, while all four dailies still pointed
at the wrapper (re-registration committed 07:31:54Z) and no task is scheduled
at 02:20 EDT - unattributed, unnamed by any receipt (grep found none), and it
destroyed the rc=7 byte both passes argue over. The single-overwritten-file
audit design claimed its second victim inside the audit window itself.
Falsifier: a receipt or scheduler trace naming a 02:20 EDT fire, or USN
journal evidence of a different writer. Move: prior-synthesis move 6 (append-
mode audit jsonl with timestamp, cmdline, rc) plus add 06:20:49Z to the
attribution ask (~15 min).

### A2 The census patrol moment is EDT-mislabeled-as-Z in two carriers, off by 4 hours

census_refresh_20261002.md:3 says "hand-fired 2026-10-02T03:29:15Z"; the
AGENTS.md census bullet says "the 10-02T03:29Z patrol". Three local-clock
instruments agree the fire was 03:29 EDT = 07:29Z: the log file mtime (Oct 2
03:29 local) matching its bracket stamps [2026-10-02 03:29:15],
MagCensusPatrolDaily LastRunTime 10/02/2026 03:29:29 (scheduler local), and
e3c7d341c committed 03:31:54 -0400 two minutes later. Internal proof from the
receipt itself: it cites autoseals at 06:59Z and 07:24Z as evidence of the
sibling being live "in that window" (census_refresh:35) - a real 03:29Z fire
would predate its own evidence. B2-216's law says name the moment; the named
moment is wrong by 4h. Falsifier: census_patrol_daily.ps1 stamping its
brackets in UTC (would require explaining away both the mtime and the
scheduler LastRunTime as coincidences). Move: one-line erratum at
census_refresh_20261002.md:3 and the AGENTS.md bullet, "03:29Z" to "07:29Z
(03:29 EDT)" (~5 min).

### A3 kpi.jsonl OWED item still live and actively growing, writer confirmed

logs/kpi.jsonl = 753,324,704 bytes at my read (mtime Oct 2 07:12 EDT =
11:12Z - the writer is hot), versus 748,222,017 bytes at the ractor-topic
read (~06:5xZ): +5,102,687 bytes in ~4.3h = ~1.2 MB/h = ~28 MB/day at the
observed rate. Writer confirmed at mag/records.py:138 (write_kpi, schema
mag_records_kpi.v1). memory/attention.md:463 still carries the unanswered
response line ("find WHAT grew (the 1.1GB kpi.jsonl zero-reader class)").
No rotation, no truncation receipt. Falsifier: a later size reading at or
below 748,222,017, or a rotation receipt. Move: prior-synthesis move 5 stands
(rotation at the writer + last-consumed-offset meter, ~30 min).

### A4 The engine topic-undefined fix HELD, now verified at the schema layer

.zcode/workflows/ractor-engine.dwf.ts:29-32 declares the topic arg
"required: true" inside the metadata block (byte-read this sitting), and
ListSavedWorkflows this sitting echoes "topic (string, required)". Behavioral
leg: this very run's ask carried the full topic text. The lens's blind spot
("code-level fix unconfirmed") closes: the fix is a byte-present required
flag. Falsifier: a post-2026-10-02 CreateWorkflow succeeding with topic
absent. Move: none required; optionally assert topic non-empty at runtime
(the unrun second half of prior-synthesis move 8, ~10 min).

### A5 Prior-synthesis OWED items re-verified STILL LIVE this sitting

- Commit-queue law (named OWED in 2093ca518): grep over
  watch/inbox/hermes_burn/TICKET_LEDGER.md, queue/todo.md, memory/law/,
  memory/rib/ returns no ticket (rc=1 no-match). Ticketed nowhere, still.
- NIGHT_CLOSE erratum unpaid: watch/inbox/NIGHT_CLOSE_20261002.md mtime Oct 2
  01:14 EDT (05:14Z, untouched since close); :40-42 still reads "never
  existed" with no re-scope, no excluded-$1.0077 line, :58 still "~48s".
- T1W2 19:17-19:18Z double-fire cause still unattributed: the only 19:17
  mentions outside the ractor runs (watch/inbox/hermes_burn/DAY1_CROSS_RACTOR.md:285,
  T1R1_roast_descent_protocol.md:13) document the empty-evidence re-run, not
  a trigger. TICKET_LEDGER row two re-verifies: issued 65 / run 48 / parked 17.
Falsifier: a TICKET_LEDGER/todo row naming commit-queue; NIGHT_CLOSE mtime
advancing with an erratum; any receipt naming the 19:17 trigger. Move:
execute prior-synthesis moves 3 and 7 as one sitting (~45 min).

### A6 The window's instruments self-test green, and the lint's first live run convicts the garden night's own receipts (blocking=3)

Ran this sitting: .venv/Scripts/python.exe -m pytest tests/test_citation_lint.py
tests/test_seed_seal.py tests/test_percolator_candidates.py
tests/test_sw1_tickets.py -q -p no:cacheprovider = 48 passed in 10.00s.
Then the live dogfood: .venv/Scripts/python.exe tools/citation_lint.py
check --changed exits rc=1, "FAIL records=19 anchors=63 numbers-checked=19
blocking=3 warns=36" - the three blocking rows are
watch/inbox/model_garden/STOCHASTIC_LENSING.md:44 PHANTOM-NUMBER 8062 and
2419 (in none of the sentence's named sources) and
watch/inbox/model_garden/SWARM_1.md:55 EMPTY-SPAN (mag/gpu_ghost.py:174
blank). The instrument built on 10-01 catches live defects in the 10-01/02
night's own changed receipts the first time it is pointed at real prose -
and this simultaneously corrects F4's move (see above): landing the pre-push
wiring requires fixing or baselining these three first. Dogfood status of
the rest: seed_seal green on tests, enforcement caller still operator-gated
(known); percolator --candidates code leg green on tests, production leg
(mine rows reaching review) not re-verified this sitting; code_swarm carries
+48/-1 uncommitted lines, in-flight, unaudited. Falsifier: a green rc=0 run
of the lint on this tree, or a red test run. Move: fix or
--baseline the three blocking findings, commit them WITH the pre-push diff
(~25 min).

## Not run (honest limits)

- No Nous balance API call; the ~$47.54 balance is receipt-carried, not
  re-verified. The hermes ledger leg IS re-verified ($37.7591, 236 rows,
  matching driver.log's $37.76).
- The 61 librarian primaries (90.6MB), code_swarm 50 clusters / $0.22,
  rib_swarm 102.5 to 205, water_computer 66v134: receipts exist, numbers not
  re-derived (same limit the lens declared; still OWED to any later pass).
- The schtasks sweep for a 23:32 EDT LastRunTime cannot disprove the 23:32
  launch (a later fire overwrites LastRunTime); inconclusive by design.
- Sibling-guard sweep scope: scripts/*.sh contains exactly one true bash
  looper (descent_driver.sh, now guarded; teach_recorder.sh's "while" is a
  comment word, zero sleeps); leave_dispatcher.py is one-shot;
  mag/autodrain.py writes state/autodrain.pid and night_cadence.pid exists -
  the manually-launchable-twin disease is descent-only as of this sweep;
  queue-lane runner internals not opened (time-boxed).

## Verification stamp (this sitting, 11:05-11:25Z)

Ran: powershell Get-CimInstance Win32_Process (PID 44072); powershell
Get-ScheduledTask/Get-ScheduledTaskInfo (5 tasks); powershell schtasks /FO
CSV /V findstr sweeps (census_patrol=1, index_fold=0, invisible_runner=0,
docker_watchdog=1); ls/Read of driver.beat (whole, 941 lines), driver.log
tail, census_patrol.log tail, TICKET_LEDGER greps; python counts over
watch/inbox/index_events.jsonl (8,676 lines) and INDEX.json string search;
python re-sum of memory/runs/hermes_burn/usage.jsonl; git log / git diff /
git config / git status on githooks/pre-push, tools/citation_lint.py,
tools/code_swarm.py, scripts/descent_driver.sh, scripts/invisible_runner.vbs;
Read of scripts/descent_driver.sh:1-40, mag/records.py:125-149,
mag/shared_surface.py:1-22, .zcode/workflows/ractor-engine.dwf.ts:22-51,
watch/inbox/NIGHT_CLOSE_20261002.md (whole), watch/inbox/census_refresh_20261002.md
(whole), ractor-topic/SYNTHESIS.md (whole); pytest 4 files (48 passed);
tools/citation_lint.py check --changed (rc=1, blocking=3); find logs/kpi.jsonl
(753,324,704 bytes); powershell Get-Item %TEMP%\invisible_runner_rc.log.

Filed by break-dogfood, 2026-10-02 ~11:25Z. $0 metered. No em-dash bytes.
