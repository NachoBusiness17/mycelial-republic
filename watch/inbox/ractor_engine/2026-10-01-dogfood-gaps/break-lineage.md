# break-lineage: hostile second pass on the lineage lens report

Moment: 2026-10-01 23:16-23:45 EDT (-04:00). Topic: the lineage lens report on
watch/inbox/gap_analysis_20261001/GAP_REGISTER.md. Method: every evidence cite
in the lens report re-probed from disk this session; probes ran via script files
in %TEMP%\ractor_break (the shell wrapper eats inline $vars in PowerShell
one-liners; two early probe attempts were invalidated by PowerShell not waiting
on the wscript GUI process and were redone with Start-Process -Wait). Nothing
was fixed; this pass only measures. Laws held: no fabrication, no em-dashes,
every claim carries a path:line or a command-with-output.

## VERDICT 1: register-staleness finding. CONFIRMED.

Lens claim: 10 of 12 rows still real at ~23:00 10-01; rank 1 fixed, rank 8
half-fixed; no status column or moment stamp; the a09-a14 amendment clause sits
unexercised.

Byte-checks (all run this session):
- GAP_REGISTER.md read in full. 12 ranked rows at :74-85. Table header at :72
  is "rank | gap | lane | sev | fill cost | owner": no status column, no
  per-row moment stamp anywhere in the file. Amendment clause at :13-15: "if
  a09-a14 land later, they amend this register, they do not rewrite it."
- Register mtime 2026-10-01 18:41:58. Lanes a09-a14 main JSONs: a11 18:45:43,
  a14 18:48:13, a09 18:49:19, a10 18:53:47, a12 18:54:58, a13 19:30:04 (listing
  of memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/).
  All landed after the register wrote; the register is untouched since 18:41:58.
  Amendment clause unexercised: confirmed by mtimes.
- Rank 1 fixed: scripts/estate_walk_daily.ps1:5-13 carries the PATH LAW block
  with absolute paths ($repo at :11, $log :12, $alarm :13). Task action for
  EstateWalkDaily is direct, no wrapper: "[powershell] args=[-NoProfile
  -ExecutionPolicy Bypass -File ...estate_walk_daily.ps1]" (my
  Get-ScheduledTask enumeration, lastrun 2026-10-01 09:15:15 result=1, that is
  the pre-fix fire). logs/estate_walk_daily.log last line is
  "END 2026-10-02T00:37:54Z exit=0" (full log read: the 09-29 END plus the
  smoke END only). Log mtime 20:46:30 equals the gap-analysis landing commit
  5d2263f10 committer-date 2026-10-01T20:46:30-04:00 (git log -1), binding the
  smoke run to that closure.
- Rank 8 half-fixed: watch/inbox/INDEX.json (mtime 18:00:56, items=2420,
  fold_warnings=165) contains 38 raw occurrences of 'frontier_olm_2026-10-01'
  but dir-qualified regex counts for DIGEST.md, register.jsonl,
  percolator_candidates.jsonl, RECEIPT.md are each 0; all four exist on disk
  (34,328 / 24,955 / 23,260 / 8,084 bytes, listing in probe output). Nuance:
  INDEX.json has no 'window' property; "38 window rows" is the count of raw
  day-2 dir-string mentions across items, matching the mine commit's "window
  rows 0 to 37" phrasing. Number right, label borrowed.
- The 10 still-real rows re-verified: row 2 queue/lanes/elder/inbox.jsonl
  0 bytes mtime 2026-09-04 10:43:28; row 3 tools/citation_lint.py ABSENT;
  row 4 watch/inbox/48h_synth/STORY.md:240 carries "191.8M tokens spent" while
  frontier_olm_20260928/DIGEST.md has 0 lines containing '191' and no *ERRATA*
  file exists anywhere in the repo (name sweep over every top-level dir minus
  .git/.venv/node_modules: zero hits); row 5 ~/.mag holds only steer_seal_seen
  and seed_seal.py exists nowhere (recursive hunt), verify_seal.py lives at
  seed/verify_seal.py, spec at watch/inbox/localfirst/pam.md; row 6
  mag/percolator.py has 0 lines containing 'candidates'; row 7
  frontier_olm_2026-09-30 top level is lens/steal/sweep only; row 9
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json mtime 2026-09-29
  05:59:04, KVarN 0 hits; row 10 corpus/steal contains 1sy7srk in 0 files;
  row 11 TICKET_LEDGER.md (122 lines, mtime 2026-10-01 17:35:33) has 0 hits
  for SS-1, CP-1, R2-1 and depends_on, while memory/percolator/invariants.json
  carries exactly 639 rows (properties) with 0 depends_on: the CP-1 fact is
  byte-exact as the lens stated; row 12 watch/inbox/spiking_wide/ newest file
  is 14:42:08, no post-register probe receipt.

## VERDICT 2: invisible_runner.vbs finding. CONFIRMED, and strengthened.

Lens claim: the register's true rank 1 is a row it never carried:
scripts/invisible_runner.vbs never launches its child; four cadences dark
(Improve, CensusPatrol, FtsIndex, LeaveProtocol all result=1 on 10-01); the
lens reproduced it (rc=1, rc.log "1", proof file never created); FTS stayed
alive only via an unlogged 19:45 hand-heal.

Byte-checks:
- scripts/invisible_runner.vbs:22 builds the quoted child string, :27 runs
  shell.Run("cmd /c " & cmd, 0, True), :28-31 write rc to
  %TEMP%\invisible_runner_rc.log and WScript.Quit rc. Live PATHEXT:
  ".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL": no .PS1.
- My reproduction, exact task shape (powershell.exe + quoted args, the form
  MagCensusPatrolDaily's action carries): wscript rc=1, rc.log=[1], proof file
  never created. Raw cmd driver for the identical string prints "The filename,
  directory name, or volume label syntax is incorrect." with INNER_RC=1: the
  failure is cmd's own multi-quote strip (rule 2) mangling the first token to
  powershell.exe", before PATHEXT is ever consulted. This matches all four
  tasks in my Get-ScheduledTask table: MagImproveDaily 08:00:00 result=1,
  MagCensusPatrolDaily 08:30:30 result=1, MagFtsIndexDaily 09:00:00 result=1,
  MagLeaveProtocolDaily 08:00:00 result=1, each action routing through
  wscript.exe + invisible_runner.vbs. The lens's probe numbers (rc=1, rc.log 1)
  reproduce exactly.
- Control: the same vbs with a .cmd child propagates rc=7 and the proof file
  lands. The harness is repairable without losing exit-code propagation.
- FTS arc: a13-cadence.json:76 records the replay
  "tools/corpus_fts_rebuild.py --check --deep -> rc=2, index_state stale";
  catalog.jsonl mtime 19:43:53, catalog_fts.sqlite 19:45:12,
  logs/fts_index.log mtime 2026-09-30 09:00:21 (silent heal confirmed). My own
  check now: ".venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check
  --deep" returns index_state "fresh", deep "match", rc=0 in 0.9s.
- Provenance note: the vbs discovery is a13's (a13-cadence.json:9, "NEW
  DEFECT, first fired Oct 1 ... rc file wrote 1", vbs mtime Sep 30 10:59); the
  lens disclosed reading a13 and re-proved it independently at 23:12:30. The
  finding's register-facing claim ("a row it never carried") is true: the
  register text greps 0 for invisible_runner, vbs, Sentinel, loop_gaps.
- Estate Ratchet result=1 (lastrun 09:45:45, direct powershell action) and
  MagTipWitnessDaily/MagXRadarDaily result=2 confirmed in my table. Note: the
  result=2 pair is NOT vbs-class; both .ps1 files exist; attention.md's tail
  attributes tip_witness exit 2 to "no token / network / gist-scope denial ...
  The witness surface is dark until the credential is fixed."

Strengthening (see additions): a second failure shape the lens did not test,
a correction to half of the lens's proposed fix, and the healer attribution
the lens left OWED.

## VERDICT 3: first-of-kind-over-living-organs finding. CONFIRMED on the visible portion; the report arrived truncated.

Lens claim as received: the register declared first-of-kind over living organs;
training/loop_gaps.jsonl is a machine-written gap ledger (337 rows, schema
mag_loop_gap.v1... [text ends mid-sentence here in what I was handed; the
finding's tail, falsifier and move fields are cut]).

Byte-checks on everything visible:
- GAP_REGISTER.md:16-19 scopes the grep to corpus/steal, memory/research_polished,
  watch/inbox/*.md and declares "This is the first." at :18; negative-finding
  line :240 repeats it. The register mentions loop_gaps 0 times and Sentinel
  0 times (regex over the raw file).
- training/loop_gaps.jsonl: 337 lines; line 1 is
  {"schema": "mag_loop_gap.v1", "ts": "2026-08-06T23:11:28.407393+00:00", ...
  "dedupe": "c4f076b1e0205c27", ...} (field named "dedupe", not
  "dedupe_key"); last line ts 2026-10-01T22:38:06.579534+00:00; file mtime
  18:38:06 -04:00 = 22:38:06Z, exact.
- MagGapSentinelDaily lastrun 2026-10-01 08:15:15 result=1 (my task table);
  a13-cadence.json:63: "MagGapSentinelDaily 08:15 (exit 1 BY DESIGN: flagged
  local_sovereign_agent 10.60 GiB in 0.99d, 'find WHAT grew (the 1.1GB
  kpi.jsonl zero-reader class)' - unanswered)." The lens's "by design, flag
  unanswered" is byte-true.
- Sibling instruments uncited by the register: a10-drops.json (mtime 18:53:47)
  carries SCHEDULED x5, OWED x14, DEAD x3 (a master list); a11-build-queue.json
  (18:45:43) carries '48h' x13 and 'cost' x29 (a cost ranking); a09-balls.json
  has 'idem' x5; a13-cadence.json has 'idempotency_key' x5.
- The register's own line-17 zero-grep claim was true at its moment and is
  stale at mine: watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md (mtime 20:31:12)
  and watch/inbox/RACTORSWARM_MAP_20261001.md (21:54:19) both contain
  'gap_register'; both post-date the register's 18:41:58. Moment-true,
  unstamped, now stale: the no-moment-stamp disease visible on the register's
  own body. This strengthens, not weakens, the lens's thesis.
- The lens's blind-spot line "I grepped the register and found none" is
  confirmed (loop_gaps 0, Sentinel 0).

Caveat stated plainly: the truncated tail was not verifiable; the verdict
covers only the visible portion.

## Blind-spot closures (the lens's own confessed gaps)

1. "a09-a14 detailed claims verified by me nowhere": advanced, not closed. My
   spot-checks hold (a10/a11 shapes, a09/a13 idem fields, a13:9/:63/:76). A
   row-by-row replay of a09-a14 was NOT run and is OWED.
2. "never located or read the card whose own terms define the clock": mostly
   closed. The clock's terms live at a05-ractor50.json:32 ("bank one lens from
   48h-synthesis/STORY.md into the elder inbox before ~10-02 and the card
   resurrects by its own terms") and :133 (the clock row, noting a 35KB elder
   surface.md + trail.jsonl went active Oct 1 08:00 while the falsifier organ
   stayed empty; confirmed: queue/lanes/elder/surface.md is 35,198 bytes,
   trail.jsonl and runner_state.json both mtime 2026-10-01 08:00:23,
   inbox.jsonl still 0 bytes). The card itself (.agents/skills/elder-lens/
   SKILL.md, 2,220 bytes, mtime 09-29 11:51:44) carries neither 'resurrect'
   nor '10-02', so the card-text-defines-the-clock chain still runs through
   a05's quote: one step short, stated as such.
3. "10-02 09:15 fire pending": still pending; the 09:15:15 result=1 in my
   table is the pre-fix fire. Not verifiable tonight.
4. "Author of the 19:45 rebuild OWED": RESOLVED to attribution-grade. The
   healer is the librarian-expedition integration lane: 
   watch/inbox/librarian_exp/gathering-log.md:99 ("B2-465 FTS heal: ...
   rebuilt through the sanctioned writer (821,776 rows, 0 malformed), recheck
   index_state: fresh"), gen_receipt.py:86 (measured the sqlite at Oct 1
   19:45, 234,754,048 bytes), integration.md:49 ("Both daily freshness
   surfaces were DARK today ... zero 2026-10-01 stamps") and :58 (the two
   writer commands), landing in commit 962e41054 (committer-date
   2026-10-01T20:54:07-04:00, subject: "Integration lane found ... the B2-465
   FTS gate stale at exit 2 - healed via the two sanctioned writers"). The
   "unlogged" half stands: fts_index.log was never written.
5. "estate-wide ERRATA search not run": CLOSED. Name sweep (every top-level
   dir minus .git/.venv/node_modules, recursive, filter *ERRATA*): zero files.
   Content sweep of watch/inbox for '191.8': every carrier is flag-side except
   the original sin: measure.md:81 flags it UNVERIFIED,
   gala_20260925/48h-synthesis_RECEIPT.md:48 says "flagged UNVERIFIED (grep
   rc=1 on its named source DIGEST.md)", MICKEY17_V2_RUN_SPEC_ADDENDUM.md:63
   quotes the a08 defect row, GAP_REGISTER.md:56 describes it. STORY.md:240
   remains the only endorser. Rank 4 does not flip. pytest and the estate
   bake: NOT run by this pass either (out of scope of the register's claims;
   reported as not run).
6. "five quotes taken on the register's word": CLOSED. All five sibling quotes
   re-checked against their named lane files with Select-String -SimpleMatch:
   1 line-hit each, 5/5 (GAP_REGISTER.md:226-233).

## ADDITIONS (what the lens missed)

A1. The vbs failure has TWO shapes and half of the lens's proposed fix is a
    trap. Probe B2 (task shape) dies loud: wscript rc=1, cmd error "The
    filename, directory name, or volume label syntax is incorrect." Probe A2
    (a single quoted .ps1 child, the shape a naive fix would produce) dies
    SILENT: wscript rc=0, rc.log=[0], proof file never created: a false
    success that would read green in Task Scheduler. Probe D2 (control, .cmd
    child) proves rc propagation works (rc=7 + proof). Consequence: the lens's
    fix option "drop cmd /c and shell.Run the quoted child directly" routes a
    .ps1 to its document association, not execution; only the explicit
    powershell.exe form (the lens's other option) or a .cmd shim is safe.
    Falsifier for any fix: the task-shape probe must return the child's real
    code (7) WITH the proof file; a bare rc=0 with no proof is still broken.
    Move: +5 minutes on the lens's 25-minute fix.

A2. The dark-cadence census is 12, not 4. On 10-01's fires: 4 vbs-class red
    (Improve 08:00, CensusPatrol 08:30, FtsIndex 09:00, LeaveProtocol 08:00,
    all result=1), MagGapSentinelDaily red-by-design with its flag unanswered
    (a13:63), MagTipWitnessDaily + MagXRadarDaily result=2 (scripts exist;
    credential darkness per attention.md tail), MagCorpusRescanDaily +
    MagVisionNightly 0x800710E0 (refused, never ran), Estate KeyAudit result=1
    (09:45), Estate Ratchet result=1 (09:45), EstateWalkDaily result=1 (the
    pre-fix fire), Estate LaneSupervisor disabled since 09-28. Damage extends:
    logs/census_patrol.log dark since 2026-09-30 08:30:28, so the B2-246
    census-deep-check protection missed 10-01 entirely. The register carries
    none of this: SCHEDULED-BUT-DARK is the inverse of its dominant
    MINED-NEVER-SCHEDULED class and has no row, no meta-gap, no mention.
    Falsifier: re-query the task table after the 10-02 08:00-09:15 window;
    rows that return 0 kill their instances. Move: one a13-style census
    receipt plus the four fix shapes, ~1 wave.

A3. The healer is no longer anonymous. The lens's OWED resolves to the
    librarian-expedition integration lane on three receipts plus the landing
    commit (evidence in blind-spot closure 4). Only the "unlogged" half of the
    lens's claim survives, and it is confirmed (fts_index.log mtime still
    2026-09-30 09:00:21). Move: 0 minutes; name it in the next receipt.

A4. Rank 1's fix is half-proven against the register's own spec. Fill spec 1
    (GAP_REGISTER.md:89-92) requires proving BOTH channels on an INJECTED
    FAILURE before 10-02 09:15. The log channel is proven (END line, absolute
    paths, commit-bound smoke); the alarm channel is rewritten
    (estate_walk_daily.ps1:19-21) but has never fired: the log contains no
    ESTATE-WALK-BAKE-FAILED line ever and attention.md's tail carries none. If
    the 10-02 bake passes green, the loud channel stays unproven indefinitely.
    Move: one injected-failure smoke before 09:15, ~10 minutes.

A5. The elder clock is hours from killing rank 2's asset. inbox.jsonl was 0
    bytes at 23:16:27 with the a05 clock set "before ~10-02" and the lane
    awake since 08:00:23 (surface/trail/runner_state mtimes) without banking.
    The lens reported the clock as pending with roughly a day left; at this
    moment the rescue is the register's own fill 2 (a05's 20-minute write) and
    it expires tonight. Move: bank the lens tonight, 20 minutes.

A6. The amendment debt is content loss, not process hygiene. The six unmerged
    lanes include a10-drops.json, itself a SCHEDULED/OWED/DEAD master list
    (5/14/3), and a11-build-queue.json, a cost-if-unpaid-48h ranking: the
    register bills itself as "the lane table for the NEXT 100M-token job"
    (:5-6) while omitting its largest sibling's master lists. Add the register's
    now-stale zero-grep line (:240, stale via two post-register files) and the
    case for the lens's VERIFIED-AT column is stronger than the lens made it:
    the column would catch both the fixed rows and the register's own rotting
    negative findings. Move: the lens's 45-minute amendment, now carrying six
    lanes plus the healer attribution plus a vbs row.

A7. Meta-gap census answer for the topic. The register's meta-gap 1
    (MINED-NEVER-SCHEDULED, declared "dominant class" at :44) is confirmed
    dominant among its own rows: rows 2, 6, 9, 10, 11, 12 = 6 of 12. But the
    engine-level answer this pass adds: the inverse class (SCHEDULED-BUT-DARK,
    12 live 10-01 instances, zero register rows) means neither writing-without-
    scheduling nor scheduling-without-executing dominates alone; the dominant
    meta-gap is the missing status surface that would notice either direction.
    The register's own no-status-column design (VERDICT 1) and the vbs wrapper
    (VERDICT 2) are the same defect viewed from the ledger side and the
    scheduler side.

## NOT RUN / OWED by this pass

- pytest suite, the estate bake: not run (out of scope; no register verdict
  here depends on them).
- The 10-02 08:00-09:15 scheduler fires: pending, unverifiable tonight; the
  finding-2 falsifier and A2's falsifier both bind to it.
- Row-by-row replay of a09-a14's gap claims: not run; spot-checks only.
- The elder card's own resurrection text: one step short (SKILL.md lacks the
  clock tokens; chain runs through a05:32).
- The "two sanctioned writers" of the 19:45 heal: identified by name from
  integration.md:58 and the commit subject, not separately executed.
- The 639-row invariants count was taken at ~23:40; per B2-216 it is a
  moment-bound snapshot, not a constant.

Probe scripts and raw outputs: %TEMP%\ractor_break\ (probe_files.ps1,
probe_tasks.ps1, probe_vbs.ps1, probe_vbs2.ps1, probe_greps.ps1, probe_fts.ps1,
probe_misc.ps1, probe_final.ps1, probe_micro.ps1, probe_last.ps1,
probe_inv2.ps1) plus this session's tool log.
