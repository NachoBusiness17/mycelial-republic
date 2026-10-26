# break-operations: hostile second pass on the operations lens report (gap register dogfood)

Pass time: 2026-10-01 ~23:00 EDT. Every cite below was read or run in THIS session against
estate bytes. Local mtimes are EDT (-0400); the register's own "Z" labels are addressed in A1.
Method: byte-checked every evidence atom of the four findings, reproduced the wrapper probe
independently, re-ran the FTS deep check, then spot-verified the lens's declared blind spots
(a13's other four rows, a12's git forensics, REGISTRY traceability, rank 9-12 reality).

## Verdicts

### F1 (six late lanes a09-a14 landed minutes after GAP_REGISTER.md and were never folded in): CONFIRMED, one clause weakened

Byte-checked, all exact:
- Lane mtimes match the lens to the second: a11-build-queue.json 18:45:43, a14-coverage 18:48:13,
  a09-balls 18:49:19, a10-drops 18:53:47, a12-commits 18:54:58, a13-cadence 19:30:04
  (memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/, ls --time-style=full-iso).
- watch/inbox/gap_analysis_20261001/GAP_REGISTER.md: 16,660 bytes, mtime 18:41:58 (lens said
  18:41:00; actual 18:41:58, immaterial). The six main lane JSONs sum to 87,112 bytes (~90KB as claimed;
  120,357 with the .checks.json files).
- GAP_REGISTER.md:237 "Lanes a09-a14 did not land; 8 siblings merged." and the amend law at
  GAP_REGISTER.md:13-15 ("if a09-a14 land later, they amend this register, they do not rewrite it").
- No amendment exists: watch/inbox/gap_analysis_20261001/ holds exactly one file, GAP_REGISTER.md;
  register mtime still 18:41:58 as of this pass (~23:00). Falsifier not triggered.
- Zero folded rows: grep -c "a09|a10-drops|a11|a12|a13|a14" over the register = 3, and all 3 are the
  "did not land" mentions at lines 13, 15, 237. None of the 12 ranked rows cites a09-a14.

Weakened clause: "zero consumers" is overbroad. watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md
(mtime 20:31:12) cites a09 (3x), a10-drops, a11-build-queue, a12-commits, a13-cadence with
grep -cF byte-checks (addendum lines 136-137), and the six sibling ractor lens reports in
watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/ reference the lane names. a14-coverage has no
consumer I found. The precise claim that survives: zero REGISTER consumers; the register's own
amend law never fired.

Sharpening the lens missed: the staleness is now committed to history. Commit 5d2263f10
(2026-10-01 20:46:30 -0400) says "15/15 lanes, 75 rows" and "EstateWalkDaily ... smoke-proved by
hand" in its own message while committing the 18:41 register that says "8 siblings merged" and
that rank 1 "repeats 10-02 09:15 with the same relative-path defect". The commit message and the
register it commits contradict each other; any fix now needs a new commit, not an edit.

### F2 (invisible_runner.vbs kills its child; four daily tasks fired Oct 1 rc=1, zero log bytes 36+ hours): CONFIRMED, independently reproduced

Byte-checked:
- Get-ScheduledTaskInfo (my run): MagImproveDaily, MagCensusPatrolDaily, MagFtsIndexDaily,
  MagLeaveProtocolDaily all result=1, lastrun 10/01/2026 (08:00:00, 08:30:30, 09:00:00, 08:00:00),
  exec=wscript.exe with args routing through scripts/invisible_runner.vbs. NextRun 10/02 08:00,
  08:30:30, 09:00, 08:00.
- logs/fts_index.log ends "[2026-09-30 09:00:02] END exit=0" (file mtime 09-30 09:00:21);
  logs/improve_daily.log ends "[2026-09-30 08:00:01] END exit=0"; logs/census_patrol.log ends
  "[2026-09-30 08:30:02] END exit=1"; logs/leave_protocol.log ABSENT. All four: zero bytes for 36+ hours.
- scripts/invisible_runner.vbs mtime 2026-09-30 10:59:12.
- a13-cadence.json:6-14 wrapper-kill row: exit-7 probe, powershell never executed, rc file wrote 1.
- My own probe (this session): `wscript.exe invisible_runner.vbs cmd.exe /c exit 7` from scripts/
  returned wscript-rc=1 and %TEMP%\invisible_runner_rc.log contains 1, not 7. The child's exit code
  did not propagate; combined with a13's Set-Content proof (child never ran), the kill is confirmed
  by two independent probes.
- Root cause the lens did not name (see A2): invisible_runner.vbs:24 wraps EVERY argument in quotes
  (including bare flags like -NoProfile) and :27 routes through `cmd /c`, whose >2-quote handling
  strips the first and last quote of the whole line, mangling the command. The vbs's own usage
  comment at :11 shows a different, workable quoting shape than the registered actions use.
- Cross-check re-run by me: `.venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check --deep`
  returned exit=0 with "deep": "match"; catalog/catalog_fts.sqlite mtime 2026-10-01 19:45:12,
  exactly as the lens said, while logs/fts_index.log has no 10-01 entry: an unlogged hand rebuild
  healed the index tonight while the only healing cadence stays dead.
Falsifier not triggered: result still 1 on all four, actions still wscript.exe as of this pass.

### F3 (register rank 1 already fixed; register text stale; bake receipt never landed; alarm channel never exercised): CONFIRMED

Byte-checked:
- scripts/estate_walk_daily.ps1:11 is `$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"`
  under the PATH LAW comment (lines 5-10 naming the System32 CWD cause and the a08 lane); file
  mtime 2026-10-01 20:35:34.
- EstateWalkDaily action: direct powershell.exe, absolute -File (no wrapper), NextRunTime
  10/2/2026 9:15:15 AM, LastTaskResult=1 from the 10-01 09:15:15 pre-fix fire.
- logs/estate_walk_daily.log (full read, 1,166 bytes) contains exactly two END lines:
  "END 2026-09-29T22:16:50Z exit=0" (manual) and "END 2026-10-02T00:37:54Z exit=0" (hand smoke,
  file mtime 20:46:30, after the 20:35 edit). Zero exit!=0 lines; no Sep 30 or Oct 1 09:15 entry
  at all, which is the both-channels-silent fact in log form.
- watch/inbox/48h_synth/ holds only Sep 30 files (STORY, lattice, laws, measure, next, steals);
  no bake receipt. grep -c "ESTATE-WALK" memory/attention.md = 0 (rc 1).
- GAP_REGISTER.md:74 still reads "repeats 10-02 09:15 with the same relative-path defect": stale
  against the 20:35 script fix and the re-registered action.
Falsifier not triggered: no receipt file, no injected-failure exit=1 log line, no alarm line.
Not run by me, same as the lens: the injected-failure bake proof itself. It writes an alarm line to
the shared memory/attention.md surface, so it stays a speced move, marked OWED, not executed.

### F4 (registration/consumption gap block; finding text truncated in the ask): evidence CONFIRMED in full, composite claim not adjudicable

The ask's copy of this finding is cut off mid-evidence, so its claim, falsifier and move were not
available to break. Every visible evidence atom checked out:
- grep -c "GAP_REGISTER" and "gap_analysis" over queue/todo.md, state/CURRENT.md,
  memory/attention.md: 0, 0, 0 for both patterns (rc 1).
- watch/inbox/hermes_burn/TICKET_LEDGER.md: mtime 2026-10-01 17:35:33; grep -c "SS-1|CP-1|R2-1" = 0.
- queue/lanes/elder/inbox.jsonl: 0 bytes, mtime 2026-09-04 10:43:28 (register rank 2 re-confirmed).
- tools/citation_lint.py: absent (register rank 3 re-confirmed).
- watch/inbox/48h_synth/STORY.md:240 contains "191.8M tokens spent" (register rank 4 re-confirmed;
  ERRATA still unwritten).
- C:\Users\foste\.mag: only steer_seal_seen/ (register rank 5 re-confirmed).
- grep -c "candidates" mag/percolator.py = 0 (register rank 6 re-confirmed).
- watch/inbox/frontier_olm_2026-09-30/: no top-level files, only lens/, steal/, sweep/ subdirs
  (register rank 7 re-confirmed).
- watch/inbox/INDEX.json frontier_olm_2026-10-01 rows: 6 lens/ + 4 steal/ + 28 sweep/, and zero
  rows for the window's top-level files (DIGEST, register, candidates, RECEIPT unindexed;
  register rank 8 re-confirmed).

## Additions (what the lens missed)

### A1. The register's "~18:30Z" labels are byte-impossible as UTC; they are local EDT mislabeled Z
GAP_REGISTER.md:12 claims the lanes-dir poll at "~18:30Z" and :243-244 an "18:37Z" door check, but
the eight lanes it says it read in full have mtimes 18:13-18:28 EDT (= 22:13-22:28Z) and the
register was written 18:41:58 EDT. Under the UTC reading the poll precedes every input's existence.
So the register's provenance timestamps are local time written with a Z suffix, which resolves the
lens's blind spot 6 into a defect of the register's own meta-gap-3 class (phantom citation).
Falsifier: an earlier version of the eight lane files at 14:30 EDT later rewritten in place would
rescue the Z reading, but then the register byte-checked quotes against stale bytes; either branch
leaves the provenance block defective.
Move: one-line errata in GAP_REGISTER.md provenance block relabeling Z labels as local EDT; 5 min.

### A2. The wrapper kill has a named code-level cause: per-arg quoting + cmd /c
invisible_runner.vbs:24 appends EVERY argument wrapped in quotes; :27 runs `cmd /c <line>`. With
more than two quotes, cmd strips the first and last quote of the whole line, producing
`powershell.exe" "-NoProfile" ...` which never executes (a13's probe), and rc degrades to 1 (my
probe). The header comment (:12-14) claims exit-code propagation that :27 cannot deliver through
cmd /c. The lens's move (re-register tasks direct) fixes the symptom; a13's steal (shell.Run the
command directly, or quote once whole, re-probe expecting rc=7) fixes the cause for every future
registrant. Either is fine; pick one and record which.
Falsifier: `wscript invisible_runner.vbs cmd.exe /c exit 7` returning 7 after the fix.
Move: fix the vbs, re-probe rc=7, re-register nothing; 15 min.

### A3. The blackout hides an older unresolved red: the census patrol's own last two runs were COLLECT-DRIFT exit=1
logs/census_patrol.log line 72: "COLLECT-DRIFT - pytest holds 2478 vs carrier claim 2436 (delta +42)"
ending :90 "[2026-09-29 08:30:02] END exit=1"; line 98: "3403 vs carrier claim 3220 (delta +183)"
ending :118 "[2026-09-30 08:30:02] END exit=1". The 09-30 drift was healed only by the same-day
18:51Z hand refresh of the AGENTS.md census line; since 10-01 08:30 no enforcement surface exists,
and tests/ has since grown to 492 test files vs the 455 census claim (find tests -name "test_*.py"
| wc -l, this session). The B2-215/244/246/249 chain is aging unwatched.
Falsifier: a fresh `pytest --collect-only -q` census landing in AGENTS.md with a dated receipt, or
the patrol restored and green.
Move: after the wrapper fix, hand-run scripts/census_patrol_daily.ps1 and file the numbers; 20 min.

### A4. The Oct-1 red count is ~10 cadences, not 4
Beyond the four wrapper-killed tasks: Estate Ratchet result=1 at 09:45:45 (logs/ratchet_daily.log
"[2026-10-01 09:45:02] END seal=0 freshness=0 ratchet=1" with four GROWTH claims: estate_bridge +102,
concept_predictor +154, duel_harness +120, env_contract +180); MagTipWitnessDaily result=2
(logs/tip_witness.log 403 gist-scope line byte-identical to the a13 quote, ALERT appended, 7 gist
mentions in memory/attention.md); MagXRadarDaily result=2; MagCorpusRescanDaily and MagVisionNightly
result=2147946720 (0x800710E0 launch-refused, 03:59:59, machine asleep, no catch-up); MagGapSentinelDaily
result=1. All unacted as of this pass. The register's S1 band should carry the wrapper kill and the
ratchet debt; neither has a row because a13 landed after the register.
Falsifier: any of these tasks returning 0 after a named fix, or a triage row appearing in the register.
Move: append a13's five rows and the launch-refused pair to the register as S1/S2 with tonight's
timestamps; 15 min.

### A5. a13's ratchet row is already half-obsolete in HEAD, the "fixed-never-recorded" mirror of rank 1
The NEW violation the ratchet named (logs/ratchet_daily.log line 58: "NEW 013cbb63c8c4912e
except-pass: tools/hermes_burn.py:237") no longer exists at HEAD: git show HEAD:tools/hermes_burn.py
carries the fail-closed EVIDENCE-PREFLIGHT raise in the 230-245 range and grep -c "except Exception:"
on HEAD's file = 0. Commit 43f50ed71 (17:41:17 EDT) landed the fix after the 09:45 fire. But
configs/violation_baseline.json mtime is 06:23:01 (predates the fire: no acceptance), the four GROWTH
claims remain open, and the ratchet has not been rerun (log's last line is the 09:45 red). Same shape
as rank 1: healed in code, red on the record.
Falsifier: a rerun of scripts/ratchet_daily.ps1 ending seal=0 freshness=0 ratchet=0 plus the four
GROWTH claims re-accepted by name in configs/violation_baseline.json.
Move: rerun the ratchet, baseline-update the 4 claims by name, append the rerun END line; 20 min.

### A6. The lens's blind spot 2 is now closed: a13's other four rows byte-verify
- estate-walk-born-dead: confirmed. Log has exactly two END lines (09-29 manual, 10-02 smoke); no
  Sep 30 or Oct 1 09:15 entry; watch/inbox/48h_synth/measure.md:142 is the Ready-not-executed row,
  byte-exact: `| tapestry bake 09:15 | EstateWalkDaily "10/1/2026 9:15:00 AM Ready" | schtasks ...`.
- tip-witness-dark-unread: confirmed. Quote byte-exact in logs/tip_witness.log (10-01 09:30:02),
  END exit=2, MagTipWitnessDaily result=2.
- dated-meters-nobs-unconsumed: confirmed. Python read of watch/inbox/DATED_METERS.jsonl: exactly 4
  institutional rows dated 2026-09-30 (g20_blackout_gt1m_6h, national_alert_nonweather, moex_xrp_halt,
  g20_circuit_breaker), all state NOBS, all pointer_count=0.
- wrapper-kill: confirmed above, plus my independent probe.
Falsifier: any row contradicting disk on a re-read.
Move: none beyond folding a13 into the register (F1 move); 0 extra min.

### A7. Blind spot 3 closed: a12-commits' forensics all reproduce
- git cat-file -s 12bef9c2f = 27346599, exactly a12's "27,346,599 bytes" (the trajectory steps.jsonl
  as a git blob; the working-tree memory/runs/trajectory/steps.jsonl is a different, 136,202-byte file).
- 93f85e0dd, fcfd414c5, dbe5f682c: `git cat-file -t` returns commit in
  C:\Users\foste\Documents\projects\Mag-backup.git and "fatal: Not a valid object name" in the working
  repo, for all three. "Seeded hashes exist only in Mag-backup.git" confirmed.
- Commit count: 68 since 2026-09-30 00:00 now vs a12's "64 commits since 09-30 00:00" at its earlier
  moment; consistent, not contradictory.
Falsifier: none pending; these were the checkable claims.
Move: none; 0 min.

### A8. Rank reality census and the dominant meta-class, per the dogfood ask
Ranks re-verified this session: 1 fixed-but-record-stale; 2, 3, 4, 5, 6, 7, 8, 11 real exactly as
written; 9 real (memory/runs/corpus_gap_research/ARXIV_REGISTER.json: 0 hits for 2606.03458, mtime
2026-09-29 05:59); 10 real but its fill target is ambiguous (see A9); 12 real (watch/inbox/
spiking_wide/ holds 8 files, zero matching vulkan|move|receipt). Misranked: none proven, but the
wrapper kill (a13) outranks several S1 rows and has no row at all; rank 1 should flip to a
closed-with-receipt row or be struck.
Dominant class in MY pass is the mirror of the register's meta-gap 1: FIXED-NEVER-RECORDED. The
estate heals faster than its records close: estate-walk fixed at 20:35 with no receipt beside
48h_synth; hermes_burn fixed at 17:41 with the ratchet still red and the baseline untouched; FTS
healed by an unlogged 19:45 hand rebuild while the healer task is dead; the register stale against
its own amend law within 5 minutes of writing (lanes landed 18:45+, register written 18:41:58);
the addendum mines lanes the register never merged. Second class: ALARM-CHANNEL-COLLAPSE, roughly
10 red cadence results on 10-01 with no triage surface (a13-cadence.json:66 names it: "the estate
has no cadence that audits the cadences").
Falsifier: a register amendment landing tonight that absorbs A2-A5 would falsify "the amend law
never fires"; it has not fired as of this pass.
Move: the register amendment (F1 move) plus one receipt-per-fix law line; 30 min combined.

### A9. Rank 10's fill target path does not exist where it reads like it does
Register fill 10 says append to "steal/quantization-compression.md's OWED ledger". corpus/steal/ has
no such file (find over corpus and watch/inbox: only
watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md and the four sweep copies).
1sy7srk has 0 hits in the day-1 window copy, so the trio remains unfetched and the target is the
window's steal/ subdir, not corpus/steal (consistent with the register's own meta-gap 2, but the
fill spec's bare "steal/" path will misroute the next job).
Falsifier: a corpus/steal/quantization-compression.md appearing would flip this to a real route.
Move: one-line clarification in fill 10 naming the full path; 2 min.

### A10. Registry traceability stays inconclusive, now with a name census
memory/workflows/REGISTRY.jsonl: grep -ic "gap" = 0 (rc 1), confirming the lens; the name census
shows 7 rows "ractor-engine.dwf.ts", 12 "the-gala.dwf.ts", 3 "mickey17-v2.dwf.ts", and no
gap-analysis-named workflow. The run dir sits under memory/runs/mickey17_v2/runs/gap-analysis-*/,
so it may ride the mickey17-v2 rows; I did not adjudicate that and mark it OWED, same as the lens.
Move: if the run was gated, add the workflow name to the register's provenance block; 5 min.

## Not run (stated, not guessed)
- The injected-failure bake proof of the attention.md alarm channel: not executed (writes to the
  shared memory/attention.md surface); stays OWED per F3.
- pytest --collect-only census: not run; A3 cites file-count growth (492 files) only.
- All 24 estate tasks enumerated: I checked 11 tasks by name (the lens's 4, EstateWalkDaily, Estate
  Ratchet, TipWitness, XRadar, CorpusRescan, VisionNightly, GapSentinel); a13 claims a 24-task sweep.
- Tiers-2/3 of the six late lanes: I read a13 in full, a10/a12 row ids, and the headers of
  a09/a11/a14; the full ~120KB remains unmined by me too, same admission as the lens.
- Ranks 10's archive fetches and 12's RX 5600 XT probe: not run; verified only their absence.

Receipt: this file. Verdicts and additions also returned via submit_result.
