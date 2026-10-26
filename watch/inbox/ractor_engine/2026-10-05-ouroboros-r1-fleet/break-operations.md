# BREAK-OPERATIONS PASS - OUROBOROS ROUND 1: the fleet (2026-10-05)

Seat: break-operations (hostile second pass) over the operations lens report
(watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/operations.md, this round's fleet lens).
Everything below was read or run this sitting on the tree at
C:/Users/foste/Documents/projects/local_sovereign_agent with bash, .venv/Scripts/python.exe,
git, rg, Read, ListSavedWorkflows (succeeded here; ListWorkflowRuns failed with the same
workflow_introspection_unavailable error the lens hit, confirming that blind spot is a
seat-class gap, not a lens failure). No em-dashes. Nothing mutated except this file: the fold
tool was NOT executed, no workflow fired, no test run. Run 3 was still IN FLIGHT at my final
moment-read (2026-10-05T08:49:17Z, lanes dir grown 15 -> 16 files, no FOLD_SECTIONS.md yet),
so the E20 window the lens's move targets was still open.

The ask's transmission of the report truncated mid-F3 and dropped F4; the on-disk
operations.md carries four findings, and all four are verdicted below.

## VERDICTS

### F1 (fold gate byte-frozen, dead unconfirmed wiring): CONFIRMED, with two numeric nits

Byte-checked this sitting, every load-bearing element:

- Frozen: `stat` tools/mickey17_v2_fold.py = 10,743 bytes, mtime 2026-09-25 19:21:06 -0400;
  `git log -1 -- tools/mickey17_v2_fold.py` = 2026-09-25 19:24:20 -0400 commit 00e4883b7;
  `git status --porcelain` on it = clean. Exactly as the lens stated.
- Dead wiring: `rg deep_tier2 tools/mickey17_v2_fold.py` = 0 hits; :181 reads
  `for x in (c.get("unconfirmed") or []):`; :191 `excluded["9 verifier-unconfirmed"] += 1`;
  :157-160 sums list LENGTHS (`vc[k] += len(v)`) with no key-name control and no value read.
- Runner side: the runner instructs tier-2 persistence under deep_tier2
  (execute-register.dwf.ts:267-270 "under the key \"deep_tier2\""); rg '"unconfirmed"' across
  mickey17-v2.dwf.ts + both live drafts hits only the verdict TYPE UNION (:58/:59) and
  in-memory filters (:255/:262/:346/:368) - no runner persists a top-level unconfirmed list.
  The lens's falsifier premise holds by bytes.
- My own decodes (python over the three lane archives, .venv interpreter):
  - run-0: 15 checks files, tier-1 supports values 12 yes / 63 no (lens: 12/63 - exact);
    deep_tier2 16 entries = 15 verified / 1 unconfirmed.
  - 2026-10-04-0 (run 2): 12 checks files, 12 yes / 48 no (lens: 12/48 - exact); deep_tier2
    12 entries = 7 verified / 5 unconfirmed (the 5 unconfirmations riding included, matching
    READ_ESTATE_RUN_SPEC_ADDENDUM.md 1.1 D6-D10 and its lines 60-61 "7 verified / 5
    unconfirmed across 12 deep_tier2 entries").
  - 2026-10-05-exec (run 3, in flight): 8 lane .json, 7 checks files; tier-1 lists under FOUR
    key names with lengths supports 15 / checks 10 / entries 5 / rows 5 (lens: exact); tier-1
    values 26 yes / 9 no (lens: exact); deep_tier2 still absent at 08:39Z (lens's OWED stands).
- e12 tasks a DIFFERENT fold edit (the unbound-aggregate check,
  execute-register.dwf.ts:103 "(b) add the unbound-aggregate check to
  tools/mickey17_v2_fold.py"); rg over the e01-e12 lane table finds no lane tasked with the
  deep_tier2/verdict-wiring fix. "E20 is in nobody's lane table" CONFIRMED.
- CONVERGENT status upgraded within the round: economics.md amendment row 1 independently
  specifies the identical fix (walk checks[lid].deep_tier2, count verdict VALUES, code 9,
  generated_at header) and dogfood.md F1 carries the same :181/:157-160 cites.

Nits (do not touch the verdict): (a) "40 rows" for run 3 does not reproduce - my instrument
(sum of lane .json rows, cross-checked against the per-file counts sums) reads 35 rows, and
the lens's own 26 yes + 9 no = 35 agrees with 35, not 40; the live run cannot have shrunk.
(b) Line drift on cites: the drafts live at .zcode/workflow-drafts/ (the finding prose omits
this; the lens's own amendment row 4 has the path right); "Derived from the proven
Gap-analysis-evening skeleton" sits at read-the-estate.dwf.ts:27, not :24; the fold-tool
invoke chain reads :300/:307/:310-adjacent.

### F2 (three drifting copies, should be one parameterized saved workflow): CONFIRMED

- Three drafts on disk at .zcode/workflow-drafts/: Gap-analysis-evening.dwf.ts 26,832 bytes
  Oct 3 22:21 (capital G - a case-sensitive grep misses it; the lens's lowercase name is the
  only defect), read-the-estate.dwf.ts 26,621 bytes Oct 4 17:15, execute-register.dwf.ts
  27,642 bytes Oct 5 00:38. All three size/date cites exact. Fire records confirm the cadence:
  .zcode/workflow-runs/dwfrun-53ba7956*.mjs mtime 2026-10-03 22:21:44 -0400,
  -a6bacf9c*.mjs 2026-10-04 17:42:48 -0400, -e9656e14*.mjs 2026-10-05 00:39:20 -0400.
  Measured span 26h20m, not the ask's 36h (the 36h rides the operator order, not bytes).
- Slug fork confirmed: mickey17-v2.dwf.ts:88 and read-the-estate.dwf.ts:87 append
  String(args.targets.length); execute-register.dwf.ts:77 appends literal "-exec". Three
  run-dir shapes on disk: run-0 / 2026-10-04-0 / 2026-10-05-exec.
- Dead guard confirmed: read-the-estate.dwf.ts:103-117 inlines the 12-lane ALL table, :118
  slices, :119 `throw new Error("no targets passed")` - unthrowable over a literal;
  execute-register.dwf.ts:92-103 same shape, dead guard at :107.
- Master hardcode count: rg -o "MASTER_MICKEY17_V2" over mickey17-v2.dwf.ts = 8 OCCURRENCES
  (on 6 lines). The lens's 8x is correct; a line-count (my first attempt) undercounts - two
  lines carry two occurrences each. MASTER_READ_ESTATE 9x in the read-the-estate draft
  (:327/:338/:344/:357/:361...), MASTER_EXECUTE_REGISTER 7x in execute-register (:304/:315/
  :321/:330/:334/:336...). E33 stands.
- Dangling pointer confirmed: watch/inbox/read_estate_2026-10-04/ does not exist (dir ls =
  ENOENT; repo-wide file census shows no such folder), read-the-estate.dwf.ts:22 metadata
  promises "Names the register folder watch/inbox/read_estate_<slug>/", and
  execute-register.dwf.ts:92 (e01 start) cites it. The a53b101d4
  metadata-inherits-struck-phantoms recurrence is real.
- Journal-side proof of E22 mechanics: the e9656e14 record's args = {"slug":"2026-10-05"};
  the run dir name "2026-10-05-exec" = slug + literal. Run 2's dir "2026-10-04-0" recorded an
  args.targets length the script never consumed. The fork surface is exactly what the lens's
  move parameterizes; note ListSavedWorkflows shows the saved mickey17-v2 already advertises
  "Pass topic + targets + width" - the parameterized engine EXISTS, the drafts just bypass it
  by inlining lane tables.

### F3 (prior dogfood's moves never executed; G8 vacuous): CONFIRMED, one evidence clause WEAKENED

Confirmed by bytes:

- SYNTHESIS.md:53 is the fleet card (KEEP/MERGE/RETIRE/STAMP) and :24 is "the gate certifies
  saves the journal proves never fire" - both present as quoted (my sed of
  watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/SYNTHESIS.md lines 20-28 and 50-56).
- ls .zcode/workflows/*.dwf.ts = 19 files; rg "retired" across saved bodies = 0 hits;
  rg "gala-chassis" = 0 hits (both rc=1). The RETIRE/STAMP moves executed: none.
- Falsifier TESTED from this seat (the lens could not run it): ListSavedWorkflows returns
  exactly 19 offerings, zero retired badges, zero gala-chassis stamps. The falsifier does
  not fire; the finding survives its own kill-switch.
- G8 confirmed at tools/workflow_gate.py:94-98 (check tuple, comment block :89-93),
  :135-148 (law comment + G8_MAX_CONCURRENCY_RE at :147 binding ONLY script-text
  `max_concurrency[:=]N` declarations), :151-164 (g8_width_shape_ok; :157-158 "if not widths
  or max(widths) <= 3: return True" - scripts declaring nothing pass). rg max_concurrency
  across all 19 saved bodies hits only the-gala.dwf.ts:11 and :24, both prose/metadata.
  Registry tail carries the two fail_g8 fixture FAIL rows at 2026-10-05T05:19:34Z and
  05:20:28Z. G8 passes the standing fleet vacuously: confirmed.

WEAKENED clause: "the registry (88 rows at my read) shows tree-doctrine-dig at 6 fires, the
3rd most-fired script in gate history". Wrong on the number AND the instrument:

- Registry rows with script containing tree-doctrine-dig = 7, not 6 (all PASS; ts 2026-09-26
  x6 then 2026-10-04T02:34:06Z).
- Those are SUBMISSIONS, not fires: SYNTHESIS.md:24 (the same line the lens cites for its
  convergence quote) says the registry "is a submission ledger, not a fire ledger". The fire
  journal (.zcode/workflow-runs/, 110 dwfrun records) content-matches tree-doctrine-dig in
  only 2 records.
- The corrected claim is sharper than the lens's: the zombie's most recent certification
  (2026-10-04T02:34:06Z) sits inside the 02:33:47-02:34 PASS sweep SYNTHESIS.md:24 flagged
  as minting gate evidence for workflows with zero launches in the window. Voted dead,
  still notarized - by the known-suspect rows specifically.

The finding's core (moves never executed; G8 reads a layer the execution does not live in)
stands, strengthened by the tested falsifier.

### F4 (trilogy evidence in the decaying-asset class; rolling addendum path ate one filing): CONFIRMED

- `git check-ignore -v` this sitting: both memory/runs/mickey17_v2/runs/run-0/FOLD_SECTIONS.md
  and .../2026-10-04-0/lanes match .gitignore:102 "memory/runs/**". Exactly as cited.
- Fire journal: 112 files / 110 dwfrun records (ls + count this sitting), all three mega-burn
  ids present; rg "workflow-runs" over tools/ + mag/ *.py = 0 readers.
- MICKEY17_V2_RUN_SPEC_ADDENDUM.md lines 9-15: the supersession note confirms the 10-03
  filing was overwritten while uncommitted, E1-E18 recoverable only at commit 0c9d72a06.
- CONVERGENT with dogfood.md F2 (the unversioned fold_run.sh wrapper finding - same
  decaying-class diagnosis at the gate's entry point).

## WHAT THE LENS MISSED (additions)

1. THE FIRE JOURNAL WAS ON DISK, BANKED, AND UNREAD. The lens hit the ListWorkflowRuns
   capability block and declared the in-flight run's harness-side state unreachable, then
   read only the lane archive. But SYNTHESIS.md:24 - which the lens itself cites in F3 -
   documents .zcode/workflow-runs/ as the on-disk fire ledger ("ListWorkflowRuns tool
   failures were three times recorded by prior passes as ledger-absence; the ledger was on
   the disk the whole time"). This sitting read the ledger: it answers fire times
   (22:21:44 Oct 3 / 17:42:48 Oct 4 / 00:39:20 Oct 5) and fired args
   ({"slug":"2026-10-05"}). What it does NOT answer: progress and token spend (the record is
   a compiled payload module; rg token/progress = 0 hits). The lens's "token spend
   unreachable" stands; its "harness-side progress unreachable" was half-curable from bytes
   the estate already banked. This is the descent protocol's prior-art-sweep law violated
   inside the ouroboros itself. Falsifier: a dwfrun record format carrying progress/token
   telemetry (none read this sitting). Move (~10 min): before any "unreachable" claim about
   a run, ls .zcode/workflow-runs/ and stat + head the record; pairs with operations F4's
   FIRE_LEDGER archiver.
2. NO ARTIFACT ANYWHERE JOINS A FIRE TO ITS REAL WIDTH. The e9656e14 record's payload
   envelope carries exactly {lowered, args} (python extraction this sitting;
   maxOldSpaceSizeMb appears only as a V8 flag guard outside the payload); the token
   maxConcurrency is absent from the record's bytes entirely. So G8's script-text-only
   binding is not merely pre-fire blind - it is post-facto UNAUDITABLE: after any 429-storm
   the estate could not reconstruct which width any of the 110 fires actually ran. The gate
   already executes at every submit (88 registry rows prove the hook fires); it could stamp
   the dispatch shape into the row at the moment it sees the CreateWorkflow call. Falsifier:
   any dwfrun record or registry row carrying a run's actual max_concurrency value (none
   found in the exec-run record; a 4-record mention set exists in the journal and was not
   envelope-verified this sitting - OWED). Move (~15 min): workflow_gate.py appends
   {ts, script, fired_args, max_concurrency} to memory/workflows/FIRE_LEDGER.jsonl at
   check time; the three-ledger join SYNTHESIS demanded, one line from an instrument that
   already fires.
3. THE TIER-1 VALUE CURE IS ONE LINE, NOT A KEY-NAME WALK. Every checks file already
   persists a top-level counts dict {rows, yes, no} (e.g. e01-index-compact.checks.json
   "counts": {"rows": 5, "yes": 3, "no": 2}); summed across files they reproduce my
   entry-level decodes EXACTLY in all three runs (75 = 12+63, 60 = 12+48, 35 = 26+9).
   Amendment row 1 should sum c["counts"] instead of walking the four key names - a fifth
   key name (the surface grew from three names in run 2 to four in run 3) cannot hide from
   it, and the per-burn SPEC-seat hand-decode the estate pays every run retires. Falsifier:
   a checks file whose counts sums disagree with its entry-level supports values (0 such
   files across the 34 checks files decoded this sitting). Move: fold into the same
   operations/dogfood/economics row-1 edit (~5 extra minutes on top of their fix).
4. ROUND-LEVEL CONVERGENCE LANDED WHILE THE LENS WROTE. The lens's blind spot said no
   sibling files existed at its write moment; at my moment the round dir holds EIGHT lens
   files (accuracy, communication, dogfood, economics, logic, moonshot-1, moonshot-2,
   operations). The fold defect is now independently held by THREE seats in this round
   (operations F1, dogfood F1, economics row 1) on top of the two prior SPEC seats - under
   the duplication law this CONVERGENT x3 row outranks every novel single-source row at
   fold-dedupe time, and the three seats' edits should merge into ONE landed fix, not three.
   Falsifier: the economics row targeting different lines (it does not: its :154-166 /
   :179-193 is the same verifier+PRISMA block as operations :157-160 / :181-191).
5. NUMERIC CORRECTIONS FOR THE FOLD SEAT (all re-derivable from the commands below):
   run-3 rows 35, not 40; tree-doctrine-dig 7 registry submissions / 2 journal matches, not
   "6 fires"; trilogy span 26h20m by fire records, not 36h; drafts root is
   .zcode/workflow-drafts/ with Gap-analysis-evening.dwf.ts capitalized; MASTER_MICKEY17_V2
   = 8 occurrences on 6 lines (count with rg -o, never rg -c).

## CHECKS RUN THIS SITTING (exact instruments)

1. stat/git: `git log -1 --format="%ci %h" -- tools/mickey17_v2_fold.py` (2026-09-25 19:24:20
   -0400 00e4883b7); `git status --porcelain tools/mickey17_v2_fold.py` (clean); stat mtime
   2026-09-25 19:21:06, 10,743 bytes; `git check-ignore -v` both run-archive paths
   (.gitignore:102 both).
2. rg: deep_tier2/unconfirmed in the fold tool (0 / :181+:191); '"unconfirmed"' across the
   saved runner + both live drafts (type unions and filters only); retired and gala-chassis
   across .zcode/workflows/*.dwf.ts (0 / 0); max_concurrency across saved bodies (the-gala
   :11/:24 only); workflow-runs across tools/ + mag/ *.py (0 readers); MASTER_MICKEY17_V2
   -o occurrence count (8); deep_tier2 in execute-register.dwf.ts (:267-270, :351).
3. python (.venv): registry census (88 rows; 7 rows script=tree-doctrine-dig, all PASS, ts
   list banked above; tail rows fail_g8 FAIL 05:19:34Z / 05:20:28Z, execute-register PASS
   04:39:04Z); three-archive decode (rows, list-key lengths, supports-field values,
   counts-dict sums, deep_tier2 verdict values - all banked above); e9656e14 payload
   extraction (keys {lowered, args}; args {"slug":"2026-10-05"}; no maxConcurrency token).
4. ls/dir: .zcode/workflows (19 defs); .zcode/workflow-drafts (all three mega-burn drafts,
   sizes/dates banked); .zcode/workflow-runs (112 files / 110 dwfrun; 3 mega-burn records
   stat'd); watch/inbox/read_estate_2026-10-04 (ENOENT); exec lanes dir at 08:49:17Z
   (16 files, no FOLD_SECTIONS.md, run still in flight).
5. Read: tools/mickey17_v2_fold.py :140-209; workflow_gate.py :75-184; both drafts at cited
   regions; SYNTHESIS.md :20-28 + :50-56; MICKEY17_V2_RUN_SPEC_ADDENDUM.md :8-16;
   operations.md and dogfood.md in full (round siblings); economics.md amendment row 1.
6. Harness tools: ListSavedWorkflows (19 offerings, no retired badges - F3 falsifier
   tested); ListWorkflowRuns (failed: workflow_introspection_unavailable - same as the lens).
7. NOT run: tools/mickey17_v2_fold.py itself (would mutate FOLD_SECTIONS.md); no workflow
   fired; no pytest (no code changed by this seat).
