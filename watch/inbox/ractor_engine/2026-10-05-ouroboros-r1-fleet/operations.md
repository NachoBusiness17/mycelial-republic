# OPERATIONS LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

Lens: operations (dispatch shapes, fold integrity, commit races, silent failures, cadence health). Riding
operator order 2026-10-05 (5 rounds on our own gaps). Everything below was read or run this sitting with
`.venv/Scripts/python.exe`, git, grep, and Read on the mag tree at
`C:/Users/foste/Documents/projects/local_sovereign_agent`. No em-dashes. Anything I could not verify is
marked OWED. Sibling-lens convergence is flagged where a second source independently holds the same bytes.

## The round in one sentence

Round 1's steal-back loop closed for CONTENT (the read-the-estate register became the execute-register
lane table; corpus/steal/MASTER_READ_ESTATE.md section 9 -> drafts/execute-register.dwf.ts e01-e12) but
not for the ENGINES: the one instrument all three mega-burns share is byte-frozen since before the burns
began, the prior fleet dogfood's ranked moves never executed, and the three burns ran as three drifting
26-27KB draft copies instead of one parameterized saved workflow.

## F1 (rank 1). The shared fold gate is byte-frozen while two spec addenda banked its defects; run 3 is about to fold through it again

- `ls -la tools/mickey17_v2_fold.py` this sitting: mtime **2026-09-25 19:21**, 10,743 bytes. Every
  mega-burn folds through it: read-the-estate.dwf.ts:301/307/310 and execute-register.dwf.ts:280/284/287
  all invoke `FOLD_SH` -> `tools/mickey17_v2_fold.py` (their own error strings name it).
- grep `deep_tier2` over the fold script: **0 hits**. Line 181 still reads
  `for x in (c.get("unconfirmed") or []):` - a top-level key no runner writes; runners persist verdicts
  under `deep_tier2[].verdict` (runner instructs "under the key \"deep_tier2\"", byte-checked by the
  read-estate SPEC seat, addendum 1.1). Consequence: PRISMA prints `excluded: 0` regardless of reality;
  run 2 carried **5 substantive unconfirmations riding `included`** (READ_ESTATE addendum 1.1, D6-D10).
- My own decode of the IN-FLIGHT run 3 archive (memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/,
  read this sitting): 8 of 12 lanes landed, **40 rows under the fold's own rule ("rows key or bare
  array")** - per-file: 8 files x 5 rows each, with e07-receipt-bindings.json a BARE ARRAY (a rows-key-only
  reader counts 35 on the same unchanged files; mtimes 01:23-02:38 predate both my read and the hostile
  pass's 08:37Z read). Tier-1 verdicts persisted under **four** key names
  (supports 15, checks 10, entries 5, rows 5 = 35 verdicts across the 7 checks-carrying lanes; e06's
  checks file absent at my read) - the E5 verifier-table blindness is on its third
  consecutive run and the key-name surface is still growing, with a sibling variance now in the
  CONTAINER shape too (dict-with-rows vs bare array: any dict-assuming consumer silently drops a lane).
  Tier-2 deep checks had not persisted at my
  read moment (in-flight; OWED). Tier-1 VALUE split this run: 26 yes / 9 no - versus 48 no/12 yes in run
  2 and 63 no/12 yes in run 0, i.e. the no-rate is genre-dependent, not instrument calibration.
- CONVERGENT: E20/E5 measured independently by two SPEC seats (MICKEY17_V2_RUN_SPEC_ADDENDUM.md section
  1.1-1.2; READ_ESTATE_RUN_SPEC_ADDENDUM.md section 1.1) plus this seat's grep + decode.
- Falsifier: a post-edit fold printing `excluded > 0` when deep_tier2 carries unconfirmed rows; or any
  runner writing a top-level `unconfirmed` list (grep says none exists).
- One-sitting move (lands before run 3's fold fires): edit tools/mickey17_v2_fold.py:181-191 to walk
  `c["deep_tier2"]` and count `verdict == "unconfirmed"/"crashed"` into excluded under code 9; at
  :157-160 print verdict-VALUE splits (tier-1 yes/no, tier-2 verified/unconfirmed) beside the length
  sums; stamp the fold moment on file write. Note: run 3's own lane e12 tasks a DIFFERENT fold edit (the
  unbound-aggregate check, execute-register.dwf.ts:103) - E20 is in nobody's lane table; the ouroboros
  must steal it here or it folds blind a third time.

## F2. The thrice-reused skeleton should become ONE parameterized saved workflow: the copy-drift is measured, not hypothetical

- Three mega-burn drafts in 36h: gap-analysis-evening.dwf.ts (26,832 B, Oct 3 22:21), read-the-estate.dwf.ts
  (26,621 B, Oct 4 17:15), execute-register.dwf.ts (27,642 B, Oct 5 00:38). read-the-estate.dwf.ts:24
  says it in its own bytes: "Derived from the proven Gap-analysis-evening skeleton (dwfrun-53ba7956)".
- Measured drift across the copies:
  - Slug formula forked: mickey17-v2.dwf.ts:88 `+ "-" + String(args.targets.length)` vs
    execute-register.dwf.ts:77 `+ "-exec"`; three run-dir shapes on disk (run-0, 2026-10-04-0,
    2026-10-05-exec) - E31 verified in bytes by this seat.
  - Lane source inverted: the saved runner takes lanes from `args.targets` (mickey17-v2.dwf.ts:104-106);
    read-the-estate inlines a literal 12-lane table (read-the-estate.dwf.ts:103-115) while KEEPING the
    `throw new Error("no targets passed")` guard - now dead code testing a literal that can never be
    empty. The slug still reads `args.targets` (undefined -> 0), which is how run 2's dir name recorded
    an interface the script never consumed (E22's live decode, READ_ESTATE addendum 1.2).
  - Master-name re-hardcoded per copy: 8x MASTER_MICKEY17_V2 in the saved runner; MASTER_READ_ESTATE at
    read-the-estate.dwf.ts:327-344; MASTER_EXECUTE_REGISTER at execute-register.dwf.ts:304 (E33).
  - Metadata promises vs disk: read-the-estate's metadata says the slug "Names the register folder
    watch/inbox/read_estate_<slug>/" - `watch/inbox/read_estate_2026-10-04/` does NOT exist (ls this
    sitting), yet execute-register lane e01's `start` cites it (execute-register.dwf.ts:92): a dangling
    pointer inside the very chain executing the register. The a53b101d4 law
    (saved-workflow-metadata-inherits-struck-phantoms) recurring one generation later.
- Falsifier: a round-2 burn fired as an AmendWorkflow of one saved parameterized def passing lanes as
  args, producing slug/fold/master without a new 26KB draft. If the harness demonstrably cannot carry a
  12-lane table through args, this downgrades to "extract the 300-line tail into one shared preamble
  constant the drafts import".
- One-sitting move: save `mickey17-burn.dwf.ts` taking {topic, targets[], width, fold_tool, master_name,
  addendum_path}; the saved runner already consumes args.targets, so the drafts prove these five
  constants are the entire fork surface. Rounds 2-5 then ride amendments (the harness contract:
  amend-don't-rewrite), and the gate hashes ONE definition instead of three drifting copies.

## F3. The prior fleet dogfood's ranked moves never executed, and the new G8 width gate inherited the same wrong-layer disease

- The fleet card (watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/SYNTHESIS.md:53) voted
  RETIRE the-50/tree-doctrine-dig/music-cut + the 5 game-dig veins, MERGE wide-dig into drop-dig, STAMP
  the five gala-body variants. Executed: none. `ls .zcode/workflows/*.dwf.ts` = still **19 files**;
  grep `gala-chassis` across saved bodies = 0 hits; grep `retired` = 0 hits. Meanwhile tree-doctrine-dig
  holds **8 gate certificates across two name spellings** (registry enumeration this sitting:
  'tree-doctrine-dig' FAIL 2026-09-25T18:52:02Z then PASS 18:52:43Z; 'tree-doctrine-dig.dwf.ts' PASS x5
  on 09-26, PASS 2026-10-04T02:34:06Z) against a fire journal that content-matches it in only 2 of 110
  records as prose mentions (grep this sitting; dwfrun-ed1dbbae is the dogfood raction itself), plus a
  single body launch dwfrun-15738edf that PREDATES its 09-26 save (SYNTHESIS.md:40:
  never-fired-as-saved). The zombie's LATEST certificate was minted 2026-10-04T02:34:06Z inside the
  12-row 02:33:47-02:35 PASS sweep SYNTHESIS.md:24 flagged as zero-launch gate evidence: the theater
  got a fresh stamp the day after being named, unreversed at my read. (My first-pass "6 fires, 3rd
  most-fired" phrasing is WITHDRAWN: it counted one name spelling's registry rows and called gate
  submissions "fires" - the exact wrong-layer confusion this finding indicts.)
- G8-width-shape landed 2026-10-05 (tools/workflow_gate.py:89-96 and :135-165; fixture rows
  fail_g8/g8-width-violation-fixture at 05:19/05:20Z, registry tail) - but grep `max_concurrency` across
  all 19 saved workflows returns only the-gala prose (:11, :24). Per the check's own logic
  (workflow_gate.py:156-158: no declared widths -> pass), G8 passes the ENTIRE standing fleet vacuously:
  the width law's real control point is the CreateWorkflow run parameter the gate never sees. CONVERGENT
  with SYNTHESIS.md:24 ("the gate certifies saves the journal proves never fire"): both are the gate
  reading a layer the execution does not live in.
- Falsifier: ListSavedWorkflows showing fewer than 19 offerings or retired badges; a G8 FAIL row against
  a non-fixture script.
- One-sitting move: execute the card - metadata `status: retired` + a RETIRED.md row for the 12
  (amend-not-delete, the SYNTHESIS's own precedent), plus one dispatch-shape declaration line in each
  survivor's metadata (`// max_concurrency: N - envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md`)
  so G8 binds a real surface. 19 file touches, no code.

## F4. All three burns' raw evidence sits in the decaying-asset class the dogfood already named; the addendum rolling path already ate one filing

- `git check-ignore -v` this sitting: memory/runs/** matched at .gitignore:102 for BOTH
  runs/run-0/FOLD_SECTIONS.md and runs/2026-10-04-0/lanes - the 94 + 60 + 40-so-far raw lane rows of the
  trilogy are gitignored, "safe to delete" by class. Durable copies: only the master folds (corpus/steal)
  and the two addenda. bank-the-fire-ledger (a53b101d4) named exactly this 3 days ago; no cure landed.
- The fire journal grew 101 -> 110 dwfrun records (ls this sitting; all three mega-burn ids present:
  dwfrun-53ba7956, -a6bacf9c, -e9656e14) and grep `workflow-runs` across tools/ + mag/ = **0 readers**.
  The journal is the only artifact that joins "fired" to "saved"; nothing estate-side reads it.
- The commit-race loss already happened once: MICKEY17_V2_RUN_SPEC_ADDENDUM.md:10-15 records its own
  10-03 predecessor overwritten while uncommitted (E1-E18 recoverable only at commit 0c9d72a06). The
  rolling single-path addendum convention is one uncommitted sitting from eating a second filing.
- CONVERGENT: a53b101d4 commit message + SYNTHESIS.md:48 ("the census behind this chapter DECAYS until
  the first move below lands") + this seat's check-ignore/reader-grep.
- Falsifier: a durable copy of any trilogy's lane rows outside memory/runs; a tool that archives dwfrun
  headers.
- One-sitting move: per-slug addendum paths from F2's parameterized runner + a 10-line fire-ledger
  archiver appended at gate time (workflow_gate.py already runs at every submit; copy each dwfrun header
  line into memory/workflows/FIRE_LEDGER.jsonl) - the three-ledger join the SYNTHESIS demanded, one line
  from an instrument that already fires.

## RANKED AMENDMENT TABLE (executable; the first row lands in the shared tool every burn calls, the rest in .zcode/workflows/*.dwf.ts)

| # | Target file | Exact edit | Defect prevented | Evidence row |
|---|---|---|---|---|
| 1 | tools/mickey17_v2_fold.py:181-191 (+ :157-160, + write-time stamp) | walk `c["deep_tier2"]` list, count `verdict=="unconfirmed"/"crashed"` into PRISMA excluded under code 9; print tier-1 yes/no and tier-2 verified/unconfirmed VALUE splits beside the length sums; stamp fold moment into FOLD_SECTIONS.md header | `excluded: 0` while 5 unconfirmed rows rode included (run 2); verifier table blind to verdict values (runs 0, 2, and in-flight run 3 at FOUR key names); fold with no timestamp | READ_ESTATE addendum 1.1-1.2; fold script mtime 2026-09-25 + grep deep_tier2 = 0; my run-3 decode (supports 15/checks 10/entries 5/rows 5) |
| 2 | .zcode/workflows/mickey17-v2.dwf.ts -> save as mickey17-burn.dwf.ts | parameterize {master_name, addendum_path, fold_tool, slug formula}; restore args.targets as the ONLY lane source; write a per-run manifest {topic, targets, width, moment} into the run dir; delete the dead no-targets guard | E22 fired-circularity; E31 three slug shapes; E33 master-name re-hardcode per copy; dead-guard false confidence; the F2 copy-drift class | mickey17-v2.dwf.ts:88/:104-109 vs read-the-estate.dwf.ts:103-119 vs execute-register.dwf.ts:77; run dirs run-0 / 2026-10-04-0 / 2026-10-05-exec |
| 3 | all 19 .zcode/workflows/*.dwf.ts | metadata `status: retired` + RETIRED.md row for the-50, tree-doctrine-dig, music-cut, game-dig x5, wide-dig(merge); `// max_concurrency: N - envelope-receipt: <path>` declaration in each survivor | 12 zombie offerings still on the menu (tree-doctrine 6 fires); G8 passing the whole fleet vacuously (width law green theater) | SYNTHESIS.md:53 card; my ls = 19, greps = 0 retired / 0 gala-chassis / 0 declared max_concurrency; workflow_gate.py:156-158 |
| 4 | .zcode/workflow-drafts/execute-register.dwf.ts:92 (in-flight, rides its e-lane findings) | repoint e01 `start` from the nonexistent watch/inbox/read_estate_2026-10-04/ to memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/r04-estate-index-anatomy.json (or MASTER_READ_ESTATE.md alone) | dangling start pointer handed to the very run executing the register (metadata-promised folder never created) | ls watch/inbox/read_estate_2026-10-04 = ENOENT this sitting; draft :92 |
| 5 | the round-2+ burn runner (from row 2) | addendum path per-slug (watch/inbox/ractor_engine/<date>-<slug>_ADDENDUM.md) and a commit-between-filings step in the fold phase | the rolling-path overwrite that already ate the 10-03 SPEC filing (E1-E18 prose survives only at commit 0c9d72a06) | MICKEY17_V2_RUN_SPEC_ADDENDUM.md:10-15 |

Kill verdict (no sacred cows): the-50, tree-doctrine-dig, music-cut, game-dig-coop-social,
game-dig-creature-farming, game-dig-horror-maze, game-dig-liveops-seasonal, game-dig-roguelike-runs say
so themselves via the fleet card (9 of 19 saved bodies have zero launches of their current bytes,
SYNTHESIS.md:17); wide-dig merges into drop-dig. The three mega-burn DRAFTS should not be saved as-is:
they are one engine, they parameterize into row 2.

## Checks run this sitting (exact instruments)

1. Read in full: state/CURRENT.md; watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md;
   watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md; corpus/steal/MASTER_READ_ESTATE.md;
   watch/inbox/ractor_engine/2026-10-04-parked-decisions/operations.md;
   watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/SYNTHESIS.md;
   .zcode/workflows/mickey17-v2.dwf.ts (lines 80-109); .zcode/workflow-drafts/read-the-estate.dwf.ts
   (lines 1-125 + grep hits); execute-register.dwf.ts lane table + slug lines.
2. `.venv/Scripts/python.exe` registry census (88 rows, 75 PASS/13 FAIL, 38 scripts, failing-G
   frequency G6:28 G3:16 G4:7 G7:6 G2:6 G5:5 G1:4 G8:2); run-3 lane/checks decode (8 lanes, 40 rows,
   key-name + verdict-value censuses).
3. git: `git check-ignore -v` on run-0/2026-10-04-0 paths (both match .gitignore:102);
   `git show --stat a53b101d4`.
4. greps: deep_tier2/unconfirmed/OPERATING ENVELOPE in tools/mickey17_v2_fold.py (deep_tier2: 0 hits;
   unconfirmed: :181/:191); max_concurrency across .zcode/workflows (prose-only, the-gala :11/:24) and
   kit-50wide (0); retired/gala-chassis across saved fleet (0/0); G8 in tools/workflow_gate.py
   (:21/:37/:89-97/:135-165); ADDENDUM paths across the three drafts; workflow-runs readers in
   tools/+mag/ (0); workflow-runs count = 110 with all three mega-burn ids present.
5. ls verdicts: .zcode/workflows = 19; .zcode/workflow-drafts (70 files; OLM daily = 5 same-size
   25,958B copies 0930..1003-retry, the daily re-copy anti-pattern); watch/inbox/read_estate_2026-10-04
   = ENOENT; watch/inbox/execute_register_seed_fidelity/ landed (e06 output mid-flight).

## Blind spots (honest)

- ListWorkflowRuns is unavailable from this session (capability gap, tool error
  workflow_introspection_unavailable), so the in-flight execute-register run's harness-side progress and
  token spend are not reachable here; I read its DISK archive instead (8/12 lanes at my moment, mtime
  window Oct 5). The 60M/100M token figures ride the ask, not my measurement.
- I did not execute tools/mickey17_v2_fold.py (it rewrites FOLD_SECTIONS.md in place and would mutate the
  evidence under audit) and did not fire any workflow. All script-defect claims are grounded in read
  source lines, the two SPEC addenda's byte-checked receipts, and my own decodes of persisted archives.
- Run 3's tier-2 deep checks had not persisted at my read moment; its tier-2 behavior and the e12 fold
  edit's landing are OWED to the run's own fold.
- The 5 tier-2 quantity corrections (910 vs 917, 28 vs 30, 250 vs 160, 86.01 vs 89.4) are carried from
  the addenda's byte-checks; I did not re-measure the underlying files.
- My "G8 cannot see the CreateWorkflow run parameter" claim is grounded in the gate's own regex scope
  (workflow_gate.py:147 binds only script-text declarations); I could not read the harness's
  CreateWorkflow plumbing (outside this repo) to prove the parameter is the sole real control point.
- No sibling lens files existed in watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/ at my write
  moment (I created the dir), so cross-lens CONVERGENT flags here cite PRIOR runs' seats, not this
  round's siblings; round-level dedupe is owed to the fold seat.
- Registry census is moment-read: siblings append live (88 rows at my count; the 10-02 dogfood watched
  its own census grow 63 -> 75 mid-raction).

## ERRATUM (hostile second pass, same sitting; both corrections verified by re-run this sitting)

1. Run-3 row count: the hostile pass read 35 rows on the same 8 lane files (08:37-08:39Z) where this
   lens read 40. Re-run per-file census: 8 files x 5 rows = 40 under the fold's own "rows key or bare
   array" rule; e07-receipt-bindings.json is a BARE ARRAY, invisible to a rows-key-only reader (35 = 7
   dict lanes x 5). Files unchanged between reads (mtimes 01:23:13-02:38:45). Both numbers are correct
   under named instruments; the file above now names the instrument with the count. The hostile pass's
   own cross-check (per-file checks counts sums, and 26 yes + 9 no = 35) measured the 7 checks-carrying
   lanes only - e06 had no checks file at either read.
2. tree-doctrine claim: this lens's first pass said "6 fires, 3rd most-fired" - WITHDRAWN. Registry
   enumeration (re-run): 8 certificates across two spellings (09-25 FAIL+PASS as 'tree-doctrine-dig';
   09-26 x5 + 10-04T02:34:06Z PASS as 'tree-doctrine-dig.dwf.ts'). Fire journal grep (re-run): the
   lowercase string appears in 2 of 110 records as prose mentions (dwfrun-4bacae38, dwfrun-ed1dbbae =
   the dogfood raction); the single body launch dwfrun-15738edf carries TREE_DOCTRINE_V and predates
   the 09-26 save (SYNTHESIS.md:40). Corrected claim in F3 above: zero launches of current bytes, 8
   gate certificates, latest minted inside the zero-launch 02:33-02:35 sweep.
