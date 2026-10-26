# Operations lens on GAP_REGISTER.md - dogfood pass, 2026-10-01 ~22:00 EDT

Lens: operations (dispatch shapes, fold integrity, commit races, silent failures,
cadence health, theater surface). Topic: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md.
Method: every claim below re-verified by me this sitting with the named command;
nothing adopted from lane prose without a byte check of my own.

## The one-line verdict

The register's dominant meta-gap (MINED-NEVER-SCHEDULED) applies to the register
itself, and the register went stale within 4 minutes of shipping: its
negative-finding block ("Lanes a09-a14 did not land", GAP_REGISTER.md:237) was
falsified at 18:45-19:30 local when all six lanes landed, and its own amendment
law (GAP_REGISTER.md:14-15, "if a09-a14 land later, they amend this register")
never fired. GAP_REGISTER.md mtime is still 18:41, 16,660 bytes.

## Findings

### F1. The register shipped 8/14 lanes and was never amended; the six late lanes sit unmined in the archive

Evidence: `ls -la --time-style=full-iso memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/`
shows a11-build-queue.json 18:45:43, a14-coverage.json 18:48:13, a09-balls.json
18:49:19, a10-drops.json 18:53:47, a12-commits.json 18:54:58, a13-cadence.json
19:30:04 - all AFTER GAP_REGISTER.md's 18:41:00 write and after both polls the
register claims (GAP_REGISTER.md:238-239, "no late landings appeared"). The six
files total roughly 90KB of gap rows (wc -c: 77,626 bytes for a11-a14 alone)
that no ranked-table row, todo entry, or ticket consumes. The register's own
coverage honesty block (lines 13-15, 236-238) is now false as written.
Falsifier: a GAP_REGISTER amendment (mtime > 19:30) or an AMENDMENT file in
watch/inbox/gap_analysis_20261001/ would kill this; neither exists as of this pass.
Move: one sitting, ~20 min - append the six lanes' rows to the register per its
own law, marking rank-1 closed and adding a13's cadence rows at the top of S1.

### F2. Live S1 the register missed: four daily cadences are being killed by the invisible_runner.vbs wrapper and fire red again 08:00-09:00 tomorrow

Evidence (my own runs, not a13's): `powershell Get-ScheduledTaskInfo` over the
four tasks read state=Ready, exec=wscript.exe, lastrun 10/01/2026, result=1 for
MagImproveDaily (08:00), MagCensusPatrolDaily (08:30), MagFtsIndexDaily (09:00),
MagLeaveProtocolDaily (08:00). logs/fts_index.log ends "[2026-09-30 09:00:02]
END exit=0"; logs/improve_daily.log ends 2026-09-30 08:00; logs/census_patrol.log
ends 2026-09-30 08:30; logs/leave_protocol.log does not exist. a13-cadence.json
row "wrapper-kill" probed the wrapper directly (child exit-7 probe file never
written, rc 1). This matches AGENTS.md B2-465's own dark-surface definition
("no START stamp for today in the log means the surface is dark") and nobody
ran that incident protocol. a13 landed 19:30, 49 minutes after the register,
so the register could not contain it - which is exactly why F1's amendment matters.
Nuance I verified against a13: a13's sub-claim "FTS index is STALE right now"
was true at its moment and false at mine - my run
`.venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check --deep` returned
exit=0 with "deep": "match"; catalog_fts.sqlite mtime 19:45:12 shows an unlogged
hand-rebuild healed it 15 minutes after a13 checked. The healing surface (the
daily task) is still dead; the index is fresh only until catalog.jsonl next moves.
Falsifier: Get-ScheduledTaskInfo result=0 for all four tasks after a wrapper fix,
or task actions no longer exec=wscript.exe.
Move: one sitting, ~30 min - re-register the four tasks with direct
`powershell -NoProfile -ExecutionPolicy Bypass -File <abs>` actions (the
EstateWalkDaily pattern below already proved this shape works under Task
Scheduler), or fix the vbs quoting; then hand-fire each task and require an
exit=0 END line in each log tonight.

### F3. Register rank 1 is already fixed but the register still says it "repeats 10-02 09:15"; the receipt is trapped in a commit message and the alarm channel is unproven

Evidence: register row 1 (GAP_REGISTER.md:74) vs disk -
scripts/estate_walk_daily.ps1:11 carries `$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"`
with the PATH LAW comment (mtime Oct 1 20:35, commit 5d2263f10);
`Get-ScheduledTask -TaskName EstateWalkDaily` action = direct powershell with
absolute `-File ...estate_walk_daily.ps1`, WorkingDirectory blank, NextRunTime
10/2/2026 9:15:15 AM, LastTaskResult 1 from the 10-01 09:15 fire;
logs/estate_walk_daily.log ends "END 2026-10-02T00:37:54Z exit=0" (the 20:37 EDT
hand smoke). Two residues: (a) fill spec 1 (GAP_REGISTER.md:89-92) required the
receipt landed "beside watch/inbox/48h_synth/" - `ls watch/inbox/48h_synth/`
shows only Sep 30 files, no bake receipt, no ERRATA.md; the receipt lives only
in commit 5d2263f10's message, which no inbox consumer greps. (b) Fill spec 1
required proving BOTH channels "on an injected failure" - the post-fix log holds
zero exit!=0 runs and memory/attention.md has no ESTATE-WALK line, so the alarm
half is repaired by inspection, never exercised. Scheduler-context proof (the
fix surviving real System32 CWD) is also pending until the 10-02 09:15 fire.
Falsifier: a BAKE_RECEIPT file in 48h_synth/ or an injected-failure log entry
(exit=1 plus the attention.md alarm line) would kill both halves.
Move: ~10 min - land the receipt beside 48h_synth (script bytes, log END, task
action, pending-fire note) and either run one sandboxed injected-failure proof
or mark the alarm channel OWED with a named owner.

### F4. The register is itself mined-never-scheduled: zero execution pointers exist anywhere

Evidence (my greps this sitting): `grep -n "GAP_REGISTER\|gap_analysis" queue/todo.md state/CURRENT.md memory/attention.md`
= zero hits in all three. watch/inbox/hermes_burn/TICKET_LEDGER.md mtime 17:35
(precedes the 18:41 register) and `grep -n "SS-1\|CP-1\|R2-1" TICKET_LEDGER.md`
= zero rows. Of the register's 12 one-sitting fills, my byte checks show exactly
one executed post-audit (rank 1/F3), and it fired because a08 caught a live
failing task, not because anything scheduled the register. The two clocks the
register ranks S1 are running unowned: rank 2's queue/lanes/elder/inbox.jsonl is
still 0 bytes, mtime Sep 4 (`ls -la`), falsifier clock "~10-02"; rank 3's
tools/citation_lint.py still absent; rank 4's STORY.md:240 still carries 191.8M
with no ERRATA.md; rank 5's ~/.mag holds only steer_seal_seen/ (no keyfile, no
mode sentinel) and tests/test_seal_forge_drill.py is absent. Also confirmed
still-real: rank 6 (grep "candidates" mag/percolator.py = zero hits), rank 7
(frontier_olm_2026-09-30/ has no top-level DIGEST/register/candidates files),
rank 8 (INDEX.json path rows for frontier_olm_2026-10-01 cover only lens/ and
sweep/; the five top-level files incl DIGEST.md and RECEIPT.md are unindexed),
rank 9 (no 2606.03458/KVarN in memory/runs/corpus_gap_research/ARXIV_REGISTER.json).
Ranks 10-12 I did not check - reported as not run, not inferred.
Falsifier: any todo/ticket/CURRENT row naming GAP_REGISTER dated after 18:41,
or a TICKET_LEDGER SS-1 row, kills this.
Move: ~15 min - one P0 todo row pointing at the register with the two ~10-02
clocks called out, plus fill 11's three TICKET_LEDGER rows; both are pure writes.

### F5. Closure events outrun the table: the register has no status mechanics, so rank 1 went stale in 2 hours and the next reader re-fires finished work

Evidence: GAP_REGISTER.md has no status column and its only update law covers
lane landings, not gap closures (lines 13-15). Row 1's "repeats 10-02 09:15
with the same relative-path defect" was already false when the register was 2
hours old (fix at 20:35, register at 18:41). The gap-analysis commit message
(5d2263f10) simultaneously claims "15/15 lanes" while the register it ships says
8 merged - the fold's completeness claim and its own artifact disagree inside
one commit. Minor same-class wound I flag as observed, not adjudicated: the
register labels its poll "~18:30Z" (line 12) while the a01-a08 files it says it
read in full carry local mtimes 18:13-18:39, so the Z label is at minimum
unverifiable against disk and at worst the phantom-citation class (register's
own meta-gap 3) applied to the register.
Falsifier: a status/checked-at column or dated closure block in the register
would kill this; none exists.
Move: fold "status + checked-at + checked-by" columns into F1's amendment so
closures and landings both have a sanctioned write path.

## Cadence health snapshot (ops telemetry, this sitting)

- Tomorrow 08:00-09:15 has five scheduled fires: four will rc=1 through the
  broken wrapper (F2) unless fixed tonight; EstateWalkDaily should pass if the
  fix survives real System32 CWD (F3's pending proof).
- Silent-failure census: 4 of the estate's standing daily cadences produced
  zero log bytes for 36+ hours with zero alarms (F2), plus the 10-01 bake fire
  (both channels silent, register row 1). The pattern is one disease: failures
  routed through surfaces that cannot speak (hidden-window vbs swallowing
  stderr; relative paths under System32 CWD).
- Theater surface: ~90KB of finished lane audits with no consumer (F1); a
  16.6KB ranked register with no scheduler (F4); a commit-message-only receipt
  for the one thing that was fixed (F3).

## Not run / OWED (honest blanks)

- I read headlines and sampled rows of a09-a14, not all ~90KB in full; their
  complete row sets remain unmined by me too.
- a13's other rows (estate-walk-born-dead, ratchet-daily-open-debt,
  tip-witness-dark-unread, dated-meters-nobs-unconsumed) not re-verified by me.
- a12-commits' git-forensics claims (64 commits, seeded hashes only in
  Mag-backup.git, steps.jsonl 273,465,999... 27,346,599 bytes) not re-verified.
- REGISTRY traceability: `grep -c "gap" memory/workflows/REGISTRY.jsonl` = 0,
  but the registry is workflow-name-keyed (ractor-engine.dwf.ts rows exist), so
  whether the gap-analysis run gated is inconclusive - not asserted either way.
- Ranks 10-12 artifacts not checked.
- All local mtimes in this pass are host-local (EDT); the register's Z-labeled
  moments were taken at face value, so cross-timezone arithmetic in F1/F5 uses
  local mtime ordering only, which is internally consistent.
