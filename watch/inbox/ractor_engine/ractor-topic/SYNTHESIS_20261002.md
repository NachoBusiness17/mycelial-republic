# SYNTHESIS - ractor-topic (2026-10-02, filed ~06:58Z)

Run: ractor_engine / ractor-topic. Stage: synthesis, after lenses, hostile second
pass, and two steering rounds. Banked lens verdict:
watch/inbox/ractor_engine/ractor-topic/accuracy.md (revision 1 at :152-156).
Surviving finding sets folded: accuracy (F1-F5 + revision), operations (twins,
cadence, script versions), economics (double-spend, window exclusion), watchdog
(task doctor SPOF, census drift, kpi.jsonl, invisible_runner), lineage
(commit-queue OWED, commit-message bank claim), logic (unregistered receipt),
security (unattributed hidden launch), plus the engine-serialization note.

The run's topic field arrived literally "undefined" (accuracy.md:3 records the
lens riding its standing beat because of it). That is finding F14's disease at
the run's input instead of its output, and it is the honest frame for what
follows: every seat in this run had to choose its own subject, and they all
chose the night of 2026-10-01/02.

## The chapter: the estate measured everything and handed off almost nothing

Start at the end. The night lane filed the most verifiable receipt in the
estate's recent history and one of the least aware, 47 seconds after banking
the counts that prove its own numbers: TICKET_LEDGER.md was last written
05:13:31Z and watch/inbox/NIGHT_CLOSE_20261002.md was created 05:14:18Z (NTFS,
Get-Item, this sitting). The hostile pass re-derived ten independent figures
from that receipt and every one held: commit stat 1726 files +443,979/-9,310
(NIGHT_CLOSE:10, accuracy.md:14-17), hermes spend 43 rows $5.5208 and garden
725 rows $3.4746 (NIGHT_CLOSE:52-54), overnight totals $8.9954 and 5,547,496
tokens (NIGHT_CLOSE:55-56), ticket ledger 65 issued / 48 run / 73.8 pct
(NIGHT_CLOSE:31-32), SW1 17 passed (NIGHT_CLOSE:29, re-run green at
accuracy.md:28-29), heartbeat endpoints 416 and 503 (NIGHT_CLOSE:57-58), and
zero em-dash bytes in the lane's touched set (NIGHT_CLOSE:36, accuracy.md:36-43).
This sitting I reproduced the money core myself, instrument named: a scan of
memory/runs/hermes_burn/usage.jsonl (wc -l reads 236 rows) re-sums the receipt
window (ts >= 2026-10-01T21:31:24Z) to exactly 43 rows and $5.5208, and the
thirteen window-doubled (id,turn) keys to exactly the pair-sum $2.2521 against
cheaper-copy $1.0939. The numbers can be trusted. That is the trap.

In the same receipt, every claim about a neighbor fell. "POSITION_CHANNEL_RESULT.md:
never existed" (NIGHT_CLOSE:40-42) is literally true of that path and false of
the world: NTFS shows the .md as a single-shot creation at 06:09:53Z, 56 minutes
after close, while the TALK-1 verdict it dismisses was banked pre-close in
memory/runs/talk1/results.jsonl (created 01:59:28Z, arm rows stamped in-row at
03:47:09Z and 04:06:01Z) and was cross-referenced at 02:30Z by
watch/inbox/model_garden/COLD_VERTEX_LAYER.md:64, "the write is in flight
(TALK-1)". The full verdict now sits in the post-close .md:
POSITION_CHANNEL_RESULT.md:13 declares POSITION-CHANNEL-EXISTS (single-shot,
transient) with position 8/20 vs text 7/20 vs control 2/20 at :17-19, a sibling
result the morning brief was told did not exist. The same receipt's window line
(NIGHT_CLOSE:50, "since driver start 21:31:24Z") anchors the overnight total to
the younger twin's birth and silently excludes the older twin's hour: my scan
re-sums the five excluded usage.jsonl rows (DG1_moe_mating_door 0.1107,
T1W2_S5_stores 0.1152, T1W2_S6_docker 0.1221, T1W2_S7_mates 0.1404,
T1W2_S8_stealth 0.5193) to $1.0077, so the twin-corrected overnight total is
$10.0031, not the $8.9954 the morning read. And commit 0c9d72a06's message
claims "position channel half-channel banked" while banking nothing: the commit
carries zero talk1 paths, .gitignore:102 bars memory/runs/**, and the receipt is
registered in neither watch/inbox/INDEX.json nor index_events.jsonl (logic and
lineage findings, this run). Every number true; every neighbor missing.

One mechanical defect made most of that fog, and it is still live. Three descent
drivers were alive at the operations lens's 06:11:22Z WMI reading: two spawned
20:40:13Z, one at 21:31:24Z (accuracy.md:85-92). scripts/descent_driver.sh:15-17
(read this sitting) writes both counters from the same $cycle, yet the two
interleaved counters disagree (log at 623, beat at 563, zero 6xx beats), because
the beat line was added to the script at 21:27:13Z NTFS, between the twins'
spawns, so the loops ran two script versions (accuracy.md:90-98). The drain path
has no claim lock, so double-drain of paid asks is structural
(accuracy.md:93-95), and the ledger shows the class is not hypothetical: exactly
13 (id,turn) keys doubled inside the receipt's own window (21:39:37Z to
21:53:52Z, DUEL2_train_02..14_r2 plus N1R_parables_songmap), 26 rows, both
copies costed, excess ~$1.16. My whole-file scan extends the census one step
further: T1W2_S5/S7/S8 also fired in near-simultaneous pairs at 19:17-19:18Z
(deltas 0.95s, 4.7s, 22s, both copies costed), about 80 minutes before the
WMI-observed twins spawned, so the double-fire class predates the twins and its
cause is unattributed. The receipt's "~48s cadence" (NIGHT_CLOSE:58) is the same
disease in miniature, a mixed-instrument moment named as a shift rate: its own
endpoints give 87 cycles over 4,806 s, 55.2 s/cycle (accuracy.md:96-98).

While the twins burned, the watchers died with their host. All four daily Mag
scheduled tasks returned LastResult=1 the same morning (10-01, 08:00 through
09:15), census and FTS left zero bytes in their logs, and the task doctor whose
job is to catch exactly this is embedded inside the census script itself:
scripts/census_patrol_daily.ps1:113-157 (read this sitting) runs the Mag* sweep
only when its host runs, warn-only by design (:119-120), so a dead host is a
blind doctor. The consequences chained the same day, each one verifiable: the
AGENTS.md census carrier went stale past the B2-244 trigger (the watchdog's
COLLECT-DRIFT run read 4,188 vs the carrier's 3,550; my own fresh run this
sitting, pytest --collect-only -q, reads 4147 tests collected, reproducing
accuracy.md:106-110; both readings clear the bar of 20 by an order of
magnitude); logs/kpi.jsonl grew to 748,222,017 bytes with its only writer at
mag/records.py:138 feeding mag/records.py:17's path, after the gap sentinel
named it on 10-01 and the response line was never executed; and
scripts/invisible_runner.vbs fired unattributed at 23:32:51 EDT with exit code 7
into an audit trail that is one overwritten %TEMP% file. The fix for the wrapper
was already written two hours before the watchdog lens ran:
watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/SYNTHESIS.md, item 1
(re-register the four VBS-wrapped actions to direct powershell -File), still
unexecuted at this sitting.

That is the last-mile disease, and tonight it collected three more convictions
beyond the classic ones: the commit-queue law named OWED in commit 2093ca518's
message has no row in memory/law, memory/rib, queue/todo.md, or TICKET_LEDGER
(lineage grep, this run); the kpi.jsonl response sat unexecuted in
memory/attention.md for a day; the wrapper fix sat written for hours. Even this
engine did it: the serialization substituted a PASS-ledger consolidation for the
disk report's own F5, and the dropped item was true on the tree (lens1
results landed post-close, accuracy.md:127-133). The estate's failure surface
is not measurement. It is the final step of every handoff: writer wrote, next
reader's map said nothing was there.

## What the morning can trust

The receipt's arithmetic core and the ticket ledger's counts are hostile-pass
survivors, now triple-verified (lens, steering, this synthesis). Sweep 1's 53
passed reproduces live on the current tree (steering round: pytest -k
"code_swarm or swarm", 53 passed). Both sweep counts were banked pre-receipt at
watch/inbox/hermes_burn/TICKET_LEDGER.md:128-129, so the accuracy lens's
"unbanked" verdict was wrong in class; its own blind-spot note at accuracy.md:
142-143 predicted exactly where the counts would be found. What remains missing
is only sweep 2's exact command: TICKET_LEDGER.md:129 paraphrases it as
"k touched-module keywords" without the keyword list. Trust the numbers;
re-derive every edge claim about siblings.

## OWED (honest residue, never asserted)

- The 19:17-19:18Z T1W2 double-fire cause is unattributed (my scan, this
  sitting); killing the twins may not remove it.
- kpi.jsonl's shrink from the sentinel's 1.1 GB figure to 748,222,017 bytes has
  no truncation or rotation receipt; the delta is unexplained.
- The 23:32:51 EDT invisible_runner launch is unattributed; no seat receipt
  names it.
- F1's original pre-close mtime leg stays WITHDRAWN (accuracy.md:56-60);
  restoring it needs an admin USN journal query, not run.
- WMI was not re-run this sitting (transient instrument; 06:11:22Z reading
  stands as of its moment).
- The topic field was "undefined": engine input defect, noted, not fixed here.

## Ranked moves

1. Kill the two 20:40:13Z twins, pidfile-guard scripts/descent_driver.sh
   (~35 min). Only move that stops live paid damage; root of four findings.
2. Re-register the four VBS-wrapped tasks to direct powershell -File, hand-fire
   each to an exit=0 log line (~45 min). The fix is already written; until it
   lands, every recurring guard below stays dark.
3. One erratum sitting on NIGHT_CLOSE_20261002.md: re-scope the "never existed"
   line to the byte truth, add the excluded $1.0077, correct the cadence to
   55.2 s/cycle, add sweep 2's exact command to TICKET_LEDGER.md:128-129,
   surface TALK-1 to the morning brief, register the receipt in the shared
   index (~45 min). The awareness-layer repair.
4. Execute the B2-244 census response: fresh collect-only, refresh the AGENTS.md
   Tests bullet, attribute the delta by named landings (~15 min).
5. kpi.jsonl: size rotation at the mag/records.py:138 writer, a
   last-consumed-offset meter, receipt or restore the 1.1 GB to 0.75 GB delta
   (~30 min).
6. invisible_runner.vbs: append-mode audit jsonl with timestamp, command line,
   rc; next close receipt names the 23:32 launch (~15 min).
7. Ticket the commit-queue law into TICKET_LEDGER and queue/todo.md; capture
   state at next close via mag.state_snapshot.capture_summary (~20 min).
8. Engine loop: pass the disk report's FAIL ledger verbatim to the break pass,
   and make ask-craft name the topic (~10 min).

## Verification stamp (this sitting, 06:53-06:58Z)

Ran: powershell Get-Item on eight contested paths (NTFS times quoted above);
heredoc python scan of memory/runs/hermes_burn/usage.jsonl (window re-sum,
duplicate census, pair sums); .venv/Scripts/python.exe -m pytest --collect-only
-q -p no:cacheprovider tests, output "4147 tests collected in 9.01s"; Read of
NIGHT_CLOSE_20261002.md (whole), TICKET_LEDGER.md:115-139,
POSITION_CHANNEL_RESULT.md:1-20, COLD_VERTEX_LAYER.md:55-66, .gitignore:98-105,
scripts/descent_driver.sh (whole), scripts/census_patrol_daily.ps1:105-159,
mag/records.py:12-25 and :128-141, accuracy.md (whole). Not run this sitting:
WMI, USN journal, sweep-2 rerun, the full pytest -q suite.

Filed by synthesis. No em-dash bytes. Written to watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md; citation_lint on that file: ok, blocking=0, 26 anchors, 9 warn-only token misses; em-dash grep count 0.
