# SYNTHESIS: the register converts but cannot record

GAP_REGISTER dogfood chapter, ractor_engine run 2026-10-01-dogfood-gaps.
Written 2026-10-02T00:28-00:36 EDT by the synthesis lens. Every claim below is
either run this sitting (command and output named, moment stamped) or carried
from a surviving lens receipt and marked (carried). No em-dashes.

## The end, first

At 00:29:50 EDT on 10-02 I counted the register's twelve rows against the disk:
six show motion, six are byte-live, and the register file itself has not moved
since 18:41:58 yesterday (Get-Item: watch/inbox/gap_analysis_20261001/
GAP_REGISTER.md, 16,660 bytes, mtime 2026-10-01T18:41:58, sole file in its
directory).

The motion side: rank 1 fixed-in-waiting (rode commit 5d2263f10); rank 2
filled at 00:09:37 tonight (queue/lanes/elder/inbox.jsonl now 2,024 bytes: one
banked lens from seat-salvage-fillball-1001, falsifier clock closing
2026-10-09T04:05:56Z, card watch/inbox/fillball/elder-salvage.md); rank 3
half-landed and growing under me (tools/citation_lint.py 34,217 bytes at
00:27:43, 34,606 bytes at 00:29:49, untracked; grep citation_lint
githooks/pre-push = 0 hits, not wired); rank 4 filled minutes ago
(watch/inbox/48h_synth/STORY.md:240 re-anchored at 00:29:21, striking the
191.8M clause and binding it to memory/workflows/REGISTRY.jsonl lines 31-35
and 38; watch/inbox/48h_synth/ERRATA.md was ABSENT in my 00:29:50 check and
EXISTS by 00:33, untracked); rank 7 filled (watch/inbox/frontier_olm_2026-09-30/
top level now carries DIGEST.md, register.jsonl, percolator_candidates.jsonl,
lens/, steal/, sweep/ while the register still says the fold step is missing);
rank 8 filled 5 of 6 (my INDEX.json scan: unique frontier_olm_2026-10-01 paths
38 to 43; DIGEST.md, register.jsonl, percolator_candidates.jsonl, RECEIPT.md
and steal/quantization-compression.md each 1 row; arxiv_deepread 0).

The live side, byte-checked tonight: rank 5 (~/.mag holds only
steer_seal_seen/); rank 6 (mag/percolator.py:716-724 argparse has no
--candidates flag; the file is modified in the working tree but the intake
surface is unchanged); rank 9 (grep -c 2606.03458
memory/runs/corpus_gap_research/ARXIV_REGISTER.json = 0, and
watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-x.md:52 still
reads "Banked degraded per recipe ... Confidence 0.55" while GAP_REGISTER.md
:241 declares the number primary-confirmed); rank 10 (day-2
steal/quantization-compression.md: 0 hits for 1sy7srk, 0 for 2609.21341);
rank 11 (watch/inbox/hermes_burn/TICKET_LEDGER.md untouched since 17:35
yesterday, grep SS-1/CP-1/R2-1 = 0); rank 12 (not re-run this sitting; live
per the security lens receipt, carried).

## The thesis

The register works as a work-order and fails as a ledger, and the failure is
the finding. Its own framing ("This file is the lane table for the NEXT
100M-token job", GAP_REGISTER.md:5-6) is being proven true within hours: seats
are reading it and filling it, tonight, in an uncommitted working tree. But
nothing records the fills back. The table has no status column
(GAP_REGISTER.md:72: rank|gap|lane|sev|fill cost|owner); its only update law
covers late lane landings, not closures (:13-15); zero pointers to it exist in
queue/todo.md, state/CURRENT.md or memory/attention.md (my Select-String:
register_pointers=0); zero TICKET_LEDGER rows carry its ids. So liveness is
invisible in both directions at once: rank 1 went stale-open within two hours
of writing (fixed by the same commit that shipped the table), and by 00:29 six
rows were stale-open in the other direction (filled or moving, table says
open). A consumer who re-derives liveness gets a different answer every hour;
I got a different answer twice in ninety minutes (citation_lint.py grew 389
bytes between my reads; ERRATA.md appeared between my checks). That
re-derivation tax, paid hourly by every later seat, is exactly the cost the
table was built to remove.

The steering-corrected count (exactly 1 of 12 rows moved on day one, and the
register itself converted zero) was the truth of its moment and was already
stale when this ask reached me: rank 8's own falsifier ("an INDEX.json row for
any member of rank 8's named set voids the 1-of-12 count") fired before I sat
down. MINED-NEVER-SCHEDULED (GAP_REGISTER.md:44-49) survives as the dominant
meta-gap, but its mechanism refines into something more precise and more
hopeful: conversion-by-reader works, conversion-by-ledger does not exist. The
estate no longer has a gap-finding problem, and for one-sitting rows it no
longer has a gap-filling problem; it has a closure-recording problem.
Fixed-never-recorded is the same disease from the other side, three instances
in one day: rank 1 (fixed inside 5d2263f10's headline, table unamended), the
FTS index (hand-rebuilt at 19:45:12 per catalog/catalog_fts.sqlite mtime while
its only healing surface, logs/fts_index.log, ends 2026-09-30 09:00:02), and
tonight's four untracked/modified fills.

The elder lens, banked tonight into the dying lane it describes, arrived at
the same disease from inside: "the cadence layer has no liveness meter and no
answerer-obligation" (queue/lanes/elder/inbox.jsonl, ts 04:09:37Z). One
sentence, three altitudes. The wrapper kills four cadences and no surface
answers their death rows. The register converts six rows and no column records
them. The estate's fixes land and no law obliges anyone to write them down.
Work happens; nothing is obliged to record it. That is the thesis no single
lens could see, because each lens held one altitude.

## The dogfood test, answered

Still real (byte-verified tonight): 5, 6, 9, 10, 11, with receipts above; 12
carried. Already fixed: 1 (scripts/estate_walk_daily.ps1:5-11 PATH LAW with
absolute $repo; the task action is direct powershell -File with absolute paths
per my Get-ScheduledTask read; hand smoke wrote "END 2026-10-02T00:37:54Z
exit=0" to logs/estate_walk_daily.log; the task still carries result=1 from
the pre-fix 10-01 09:15 fire, so the true verdict lands at today's 09:15
fire), 7, 8, and 4 as of 00:33. Half-landed: 3 (tool exists, hook unwired).
Misranked: rank 1, by freshness, which is the no-status-column cost made
visible. Misworded: rank 10 (the ids ride 8+ files estate-wide per the
operations lens; the day-2-scoped zero is what my greps confirm). Half-true in
a dangerous direction: GAP_REGISTER.md:241-242 asserts a closure (0.55
primary-confirmed) the artifact does not carry, instantiating the register's
own phantom-citation class (meta-gap 3, :55-62) on page one day.

## What the register structurally missed

1. The wrapper kill, the sharpest live S1: scripts/invisible_runner.vbs:21-27
   quote-wraps every argument and routes through cmd /c, whose quote-stripping
   mangles the command line; the header (:11-14) claims exit-code propagation
   the exit7-to-rc1 probe disproved (a13-cadence.json, carried). My
   Get-ScheduledTask reads at 00:29 tonight: MagImproveDaily,
   MagCensusPatrolDaily, MagFtsIndexDaily and MagLeaveProtocolDaily all
   exec=wscript.exe invisible_runner.vbs, all result=1, last fired 10-01, next
   fires today 08:00/08:30/09:00; their logs end 09-30 or earlier with zero
   bytes since. The same wave carried non-wrapper reds, untriaged:
   MagGapSentinelDaily result=1 (direct powershell, its own defect), Estate
   KeyAudit result=1, Estate Ratchet result=1, MagCorpusRescanDaily and
   MagVisionNightly result=2147946720, MagTipWitnessDaily and MagXRadarDaily
   result=2. Twelve tasks wore non-zero LastTaskResult the night the register
   shipped; the register named one.
2. Five S1-class rows in the unmerged a09-a14 lanes (operations lens,
   carried): the balls-lane impeachment of 2093ca518's headline (byte-verified
   by that lens: Select-String judge on tools/abliterate_p1_probe.py = 0), key
   rotation OPEN, the recovery pack and the M1 bench falsifier clocked at
   2026-10-02T23:59Z (a11-build-queue.json), the wrapper kill
   (a13-cadence.json), the Studio checkboxes (a10-drops.json citing
   queue/todo.md:204-205). The register's negative-finding block (:237)
   declares these lanes "did not land" while my lanes-dir listing holds them
   with mtimes 18:45-19:30, minutes after the register's 18:41 write; the
   shipping commit's message says "15/15 lanes, 75 rows" over a register that
   says 8 merged. The amendment law (:13-15) has still never been exercised.
3. Repo weight: my git show --stat 5d2263f10 shows
   dashboard/data/ESTATE_INDEX.jsonl growing Bin 1,945,896,570 to
   2,523,006,985 bytes and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl Bin 92 to the
   same 2.5GB. No row tracks clone cost.
4. The denominator: the 100M-token frame is about 8.3x under its own ledger
   (coverage lens, carried, byte-receipted): CYCLE_BRIEF_20260930.md:33 reads
   714,810,462 recorded on 300 fires plus 49 unrecorded x mean 2,382,701 =
   831,562,811 estate-lifetime, cache-inclusive.
5. The census blackout: logs/census_patrol.log ends 2026-09-30 08:30:02 END
   exit=1 with COLLECT-DRIFT verdicts at :6 (+31), :46 (+107), :72 (+42), :98
   (+183); tests/ holds 494 test_*.py files tonight against the 455 the
   AGENTS.md census line claims (my Get-ChildItem count). The estate's
   count-truth instrument has been dark two days behind the wrapper.
6. The clock-label defect: GAP_REGISTER.md:12 stamps its lanes-dir poll
   "~18:30Z" and :243 an "18:37Z" door check, but the lanes it read in full
   carry EDT mtimes 18:13-18:39 and the register was written 18:41:58 EDT;
   under the UTC reading the poll precedes its own inputs. Local mislabeled Z:
   the phantom-citation class, in the provenance block.

## Corrections this synthesis owes

The final (truncated) surviving finding claims logs/ratchet_daily.log:58 holds
"NEW 013cbb63c8c4912e except-pass tools/hermes_burn.py:237". The bytes
disagree with the attribution: my read of ratchet_daily.log:57-61 names three
NEW except-pass rows, mag/lane_supervisor.py:29, tools/audio_channel.py:31,
tools/mickey17_v2_fold.py:94, and the log ends "[2026-10-01 09:45:02] END
seal=0 freshness=0 ratchet=1". tools/hermes_burn.py:230-244 today carries the
evidence-preflight raise (fail-closed), and git diff --stat 43f50ed71..HEAD on
that file reads +156/-9. The finding's conclusion stands (ratchet fired red
10-01 09:45, task result=1, rerun-and-record owed, the fixed-never-recorded
mirror); its specific row is contradicted, and I could not reconstruct where
013cbb63c8c4912e came from. Marked: contradicted-in-part.

Completed falsifier: the strict-python parse of a01-olm-day2.json that one
lens left PS-only. My .venv python 3.11 json.load fails with "Expecting ','
delimiter: line 38 column 587 (char 14084)", matching PS 5.1's char 14085. One
of fifteen evidence lanes is machine-unreadable on two instruments, so the
75-row denominator cannot be reproduced by the register's own amendment path
(a loose counter reads 78 across the other 14; loose instrument, marked loose,
carried).

OWED, all still true tonight: the EstateWalk alarm channel has never fired in
anger (grep ESTATE-WALK memory/attention.md = 0), so the fix's loud half is
unverified until an injected failure proves it; rank 12 not re-verified this
sitting; the a09-a14 row contents and the CYCLE_BRIEF arithmetic ride lens
receipts, not my runs.

## The clocks, in order

Today 08:00 MagImproveDaily and MagLeaveProtocolDaily, 08:15 MagGapSentinelDaily
(own red), 08:30 MagCensusPatrolDaily, 09:00 MagFtsIndexDaily: the four wrapper
tasks burn red again unless the quoting fix lands first. 09:15 EstateWalkDaily:
rank 1's verdict fire, first wrapper-free run. 09:45 Estate Ratchet (three NEW
rows pending) and Estate KeyAudit (red). 2026-10-02T23:59Z: the M1 bench F2
falsifier clock (a11-build-queue.json, carried). 2026-10-09T04:05:56Z: the
freshly banked elder lens' own falsifier clock. Continuously: the B2-215
census-carrier 7-day staleness bar over a dead patrol.

## Ranked moves (full why-first in the run result)

1. Fix the wrapper quoting or swap the four task actions to direct powershell
   -File (the smoke-proved EstateWalkDaily pattern), re-probe expecting rc=7,
   hand-fire each task, require an exit=0 END line per log before today's
   08:00-09:00 wave. ~45 min.
2. Exercise the register's own amendment law: status/checked-at/checked-by
   columns; record tonight's six closures with path receipts; merge a09-a14;
   relabel the Z stamps; scope rank 10; add the S4 repo-weight row and the
   831.5M denominator note. ~60-90 min.
3. Finish rank 3: wire citation_lint into githooks/pre-push and run it once
   over GAP_REGISTER.md itself. ~30 min.
4. Mint SS-1/CP-1/R2-1 into TICKET_LEDGER.md plus one P0 todo row pointing at
   the register with the two live clocks. ~15 min.
5. Prove rank 1's loud half: one sandboxed injected failure must write the
   attention.md line, or mark the channel OWED; land the bake receipt beside
   48h_synth. ~20 min.
6. Repair a01-olm-day2.json and rerun a fixed-schema row census (75 vs 78)
   before any machine merge consumes the denominator. ~30 min.
7. After the wrapper heals: hand-run census_patrol_daily.ps1 and file the real
   census with attribution (494 vs 455); rerun the ratchet and record the
   three named NEW rows. ~30 min.
8. Close the residue: KVarN line, the 0.55 receipt plus relabel, the rank-10
   rewording. ~20 min.

One reader, one line: for six hours the estate has been proving the register
right (seats fill what it ranks) while the register proves itself broken
(nothing records what seats filled); the status column is not bookkeeping, it
is the difference between a lane table and a mirror, and until it exists every
seat after this one pays for tonight's hour again.
