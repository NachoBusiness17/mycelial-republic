# MOONSHOT LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

Seat: moonshot-2 (no sacred cows; the 10x read) of the ractor on OUROBOROS ROUND 1 of 5. Topic: dogfood the
standing WORKFLOW FLEET and steal the improvements back into the definitions. Everything below was read or run
this sitting on the tree at C:/Users/foste/Documents/projects/local_sovereign_agent: full reads of both spec
addenda, both master folds (heads), the fold tool tools/mickey17_v2_fold.py (all 235 lines), the saved runner
.zcode/workflows/mickey17-v2.dwf.ts (all 381 lines), the clone drafts read-the-estate.dwf.ts and
execute-register.dwf.ts (marker greps + the target blocks + :327-340 filer read), tools/workflow_gate.py:130-174,
memory/workflows/REGISTRY.jsonl (88 rows, python json census), the prior fleet dogfood SYNTHESIS (commit a53b101d4),
.zcode/workflow-drafts/RETIRED.md, and git history. No em-dashes. Anything not verified is marked OWED.

## The round in one sentence (moonshot register)

The estate built a defect ledger WITH a compiler for its laws (tools/lawlog.py, per state/CURRENT.md and the
dogfood sibling board) and a defect ledger WITHOUT one for its engines: E1-E35 sit in two addenda as prose,
the fold tool's bytes are frozen at 2026-09-25 (git 59413d255 + 00e4883b7, both dated 2026-09-25), three
mega-burns ran on top of those frozen bytes in 36h, and the only reason ANY engine byte moved this week is
that the read-estate run's curiosity register got its own execution burn (in-flight lane e04 landed the G8
gate check on 2026-10-05) - the register executes because an operator order pointed at it; the E-ledger has
no executor because no workflow reads addenda. The 10x move is not "file more findings about the fleet"; it
is to make the engine's own fold tool the compiler of its defect ledger, and to collapse the three drifting
skeleton clones into ONE parameterized saved workflow so amendments land once and every burn family inherits.

## FINDINGS

### F1 (rank 1, CONVERGENT with dogfood.md F1, operations.md F1, economics.md verdict-blindness). Three mega-burns, zero engine amendments: the E-ledger never compiles

- Byte state, measured this sitting: `git log --format="%h %ad %s" --date=short -3 -- tools/mickey17_v2_fold.py`
  returns exactly two commits, 59413d255 and 00e4883b7, both 2026-09-25. The current bytes (read in full, 235
  lines) still carry every headline defect the two addenda filed: list-length verdict sums at
  tools/mickey17_v2_fold.py:158-160 (`vc[k] += len(v)`), dead exclusion wiring at :181-183
  (`for x in (c.get("unconfirmed") or []):` matching `norm(x.get("claim",""))[:80]` against entries that carry
  `row_key`/`verdict`/`evidence` and NO `claim` field), `fired = a.fired or n_files` at :120 with
  `missing = fired - n_files` at :125, the hardcoded screened literal at :197, no OPERATING ENVELOPE section
  anywhere in the file, no fold timestamp at the write (:227-228), TOP-K alphabetical at :204 with 110-char
  mid-word cuts at :207.
- The contrast that convicts: the SAME 36h window DID close one loop - tools/workflow_gate.py:135-146 carries
  the G8-width-shape check dated 2026-10-05 citing "curiosity-register row 3 r03#1", and
  .zcode/workflow-drafts/execute-register.dwf.ts:95 (lane e04) is the executing seat. Register rows land in a
  master fold section the operator ordered executed; E-items land in rolling addenda nothing reads. Even the
  in-flight run's one fold-tool touch (e12, execute-register.dwf.ts:103) adds only the 191.8M
  unbound-aggregate class - E5/E20 (the verdict-value blindness, proven permanent from source lines by the
  READ_ESTATE addendum section 1.1) remain unowned by any lane.
- Falsifier: any archived FOLD_SECTIONS.md printing `excluded` > 0 or a yes/no verdict split (the two addenda
  measured 0 across five folds); or any E-item found in the fold tool's or runner's current bytes.
- Move (one sitting, ~40 lines): land amendment rows R1-R3 below, then dogfood on a COPY of a finished run
  archive (copy `memory/runs/mickey17_v2/runs/2026-10-04-0/lanes` to a scratch slug, run the tool with
  `--run <scratch>`, verify it now prints 5 tier-2 unconfirmations excluded and the 12/48 tier-1 split,
  delete the scratch). Never rerun in place on a live archive.

### F2 (NOVEL, the moonshot). The thrice-reused skeleton is three drifting hand-clones, not one parameterized engine, and the saved runner's fixed paths already destroyed one filing

- Clone census, read this sitting: the saved runner
  (.zcode/workflows/mickey17-v2.dwf.ts:88,103-109) takes topic+targets args, guards
  `throw new Error("no targets passed")`, hardcodes MASTER_MICKEY17_V2.md (e.g. :321,:338) and the FIXED
  addendum path watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md (:346). Clone 2
  (.zcode/workflow-drafts/read-the-estate.dwf.ts) changes the topic source to `args.topic || args.slug` (:84)
  and HARDCODES all 12 targets in the script body (:103-116), so args.targets stayed empty and the slug
  suffix printed 0 (`2026-10-04-0`). CORRECTED on hostile pass: the fold call at :301 still passes
  `String(TARGETS.length)` = 12 (TARGETS is the hardcoded 12-entry ALL), so `--fired` was 12 = a script-internal
  constant, NOT the addendum 1.2 "`--fired 0` falls back to file count" mechanism, which I had repeated
  without checking the clone's own call site; the surviving defect is the weaker-but-real E22 core: fired is a
  script-internal literal, no run manifest exists, and the submit-side input record (args.targets) is
  unreconstructible from the estate. Clone 2 renames master (:327) and addendum (:352). Clone 3
  (.zcode/workflow-drafts/execute-register.dwf.ts) forks the slug formula AGAIN (`+ "-exec"`, :77), embeds
  the tier-2 corrected counts into its asks (:92), and - verified on hostile pass - DROPS the spec phase
  entirely: its phases are :174/:233/:258/:279/:311/:327 with no spec-writer agent, no addendum write, and an
  estate-filer that checks 2 items, not the runner's 3 (read :327-335). Consequence: the execute-register run
  files NO spec addendum, so the burn that executes the register bypasses the E-ledger tradition altogether -
  its own lessons have no specced landing spot.
- The quiet data loss (where work dies without a crash): the saved runner's fixed addendum path made run-0's
  10-04 filing overwrite the 10-03 filing at the same path. CORRECTED on hostile pass: `git show
  0c9d72a06:watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md` returns the 2026-10-01 gap-analysis filing (E1-E18,
  header read this sitting), and `git log --all --oneline` on the path returns exactly a7ca49be1 / 0c9d72a06 /
  3752abae2 - the 10-03 filing appears in none of them, so its bytes survive NOWHERE as bytes; only their
  substance is restated as E19-E24 in the current filing's section 4 (its own header says so). The earlier
  claim attached the survival to 0c9d72a06; inverted. The loss class stands, worse than first stated: an
  uncommitted filing at a rolling path is one overwrite from zero byte survival.
- Version control blindness: .zcode/ is gitignored (.gitignore:198, verified with git check-ignore), so
  `git log -- .zcode/workflows/mickey17-v2.dwf.ts` returns NOTHING - the runner's four registry digests
  (f190bf31e2ef -> 9b51b8e2ee05 -> dbc2eeeac52b -> 5ad12f1aae09) are the only change record that exists, and
  none of them can be diffed. Every clone is a draft: invisible to the saved-fleet surface, uncounted by any
  manifest.
- Falsifier (rewritten after it FIRED on hostile pass): my original falsifier was "a line-by-line diff showing
  phase-topology divergence beyond the four named parameters" - and that is exactly what the pass found:
  execute-register has no spec phase (phases :174/:233/:258/:279/:311/:327, no spec-writer, filer checks 2
  items, :327-335 read this sitting), so "only four parameters differ" is DEAD as scoped. The drift is worse
  than parameterization-by-four: a whole evidence phase was dropped silently in clone 3. The corrected
  parameterization demand: the saved runner must carry genre + master_name + addendum_name + inline lanes AND
  an explicit spec_phase boolean, so a genre that cannot file an addendum must SAY so in args rather than
  lose the phase by omission. New falsifier: a phase census of all three scripts showing divergence beyond
  those five knobs (the known divergence - spec phase presence - is now one of the knobs, not a refutation).
- Move: R3+R4 below - promote `genre`, `master_name`, `addendum_name`, and inline `lanes` into the saved
  runner's args block, stamp the runner into git tracking by mirroring it to a tracked path (or accept the
  registry digest as the ledger and say so in FLEET.md), retire the two clones after their runs land.

### F3 (NOVEL). G8 certifies only honest declarers: the fleet's real dispatch shape passes by silence, and the standing fleet has never been re-gated post-G8

- Gate logic read at tools/workflow_gate.py:151-164: `widths = [int(w) for w in
  G8_MAX_CONCURRENCY_RE.findall(text)]; if not widths or max(widths) <= 3: return True` - a script that
  declares NO max_concurrency passes unconditionally. The fleet's actual dispatch shape is 8-wide Promise.all
  ramp waves: mickey17-v2.dwf.ts:180-181 (`firstWave = TARGETS.slice(0, 8)`) with :229-230
  (`await Promise.all(firstWave.map(...))` then the rest), same pattern in read-the-estate.dwf.ts:239-240 and
  execute-register.dwf.ts:223-224 (line cites corrected on hostile pass: :239-240 is read-the-estate;
  my first filing swapped the two files' line numbers). The width law's own gate comment (workflow_gate.py:140-143) says "the
  dispatch shape is the retry strategy" - yet the gate is blind to every shape not spelled
  `max_concurrency:`. Registry rows 87-88 (2026-10-05T05:19-05:20Z) show G8 firing ONLY on the declaring
  fixture fail_g8.dwf.ts.
- Re-gate gap, CORRECTED census on hostile pass (`.venv/Scripts/python.exe` json census over the registry,
  command in the sitting log): the file holds 88 rows, not 89 (trailing newline). A 12-member sweep occupies
  rows 64-75, 2026-10-04T02:33:47Z through 02:34:06Z (olm-mine, gap-analysis, fill-ball, ractor-engine,
  salon-mine, librarian-expedition, wide-dig, drop-dig, the-gala, mickey17-v2, the-50, tree-doctrine-dig);
  music-cut's only row is 63 at 2026-10-03T21:56:30Z, outside that window. Only 14 of the 19 standing
  members have EVER been gated by name - the 5 game-dig veins (game-dig-coop-social, -creature-farming,
  -horror-maze, -liveops-seasonal, -roguelike-runs) have no registry row at all despite being promoted to
  saved on 2026-09-27 (.zcode/workflow-drafts/RETIRED.md "Promoted this sweep"). Rows 76-86 span
  2026-10-04T09:54:19Z to 2026-10-05T04:39:04Z - all BEFORE G8's registry debut at row 87
  (2026-10-05T05:19:34Z, the fail_g8 fixture), and none of them is a fixture. Net: no standing member carries
  a G8-era row, 5 of 19 have never been gated in their lives, and the gate's historical coverage of the
  "standing fleet" is 14/19 by name.
- Falsifier: a registry FAIL row for an undeclared Promise.all script (none exists in the 88 rows), or
  evidence the harness itself caps workflow-child concurrency regardless of script shape (the gate's own
  comment says children ride maxAttempts 0, so shape remains load-bearing).
- Move: R5 - extend g8_width_shape_ok with a `Promise.all(` + `.slice(0, N)` clause (N > 3 without an
  envelope-receipt stamp = fail), land its scenario card per the LAW-12 clause, then the one-command re-gate
  sweep over .zcode/workflows/*.dwf.ts so every standing member carries a G8-era row.

### F4 (CONVERGENT with a53b101d4 minimum-viable-fleet and SYNTHESIS.md:27). The fleet's own retirement verdict is unexecuted prose: 19 alive badges, 7 real members, no manifest

- The 2026-10-04 dogfood ruled KEEP/MERGE/RETIRE with names and reasons
  (watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/SYNTHESIS.md:53: KEEP the-gala, olm-mine,
  ractor-engine, mickey17-v2, gap-analysis+fill-ball, drop-dig[wide-dig merged]; RETIRE the-50,
  tree-doctrine-dig, music-cut, the 5 game-dig veins - "amend-not-delete, the RETIRED.md Q7 precedent").
- Byte state this sitting: all 19 .dwf.ts files still sit in .zcode/workflows/ (dir listing); the headers of
  the-50, music-cut, and tree-doctrine-dig (head -6 each) carry no retirement stamp - pre-verdict bytes; no
  FLEET.md or manifest exists in the dir; the prior dogfood's own demand (SYNTHESIS.md:27: "Until a manifest
  joins them, 'the standing fleet' is a suggestion the gate notarizes") is itself an unlanded file. The
  estate's TS-05 disease (laws that live only in prose) is reproduced by the fleet's own dogfood verdict.
- Falsifier: a retirement stamp in any of the 8 retired files' description headers, or a fleet manifest at
  another path (none found in .zcode/workflows/ this sitting; I did not census other roots - scoped claim).
- Move: R6 - write .zcode/workflows/FLEET.md (KEEP 7 + RETIRED 8 with one-line reasons citing SYNTHESIS.md:53),
  stamp each retired header with `RETIRED 2026-10-04 per SYNTHESIS.md:53 - do not fire`, re-gate all 19 for
  fresh registry rows. 30 minutes, zero deletions (the precedent is amend-not-delete).

## THE RANKED AMENDMENT TABLE (workflow file -> exact edit -> defect prevented -> evidence row)

| # | File | Exact edit | Defect prevented | Evidence |
|---|------|-----------|------------------|----------|
| R1 | tools/mickey17_v2_fold.py:154-202 | After `checks = load_checks(...)`: decode verdict VALUES - for every checks file, every list-valued key, every dict entry, read `verdict` or `supports`; print tier-1 yes/no and tier-2 verified/unconfirmed splits in the VERIFIER TABLE; build the exclusion set from `deep_tier2` entries whose `verdict` == "unconfirmed", matched to rows by lane id + row_key prefix (strip the `"<lane>: "` prefix; fall back to first-80-chars like :190); count them into `excluded["9 verifier-unconfirmed"]`. Delete the dead `c.get("unconfirmed")` wiring at :181-183. | E5+E20: 5 substantive unconfirmations rode `included` while the fold printed `excluded: 0` (recurred 1x then 5x across two runs); yes/no splits (48/12) computed nowhere by script | Fold :158-160,:181-183 read this sitting; runner persists deep_tier2 with row_key/verdict/evidence and no claim field (mickey17-v2.dwf.ts:56-60,:278-282); READ_ESTATE addendum 1.1 (5x, "the match can never meet") |
| R2 | tools/mickey17_v2_fold.py:120-125,:227-228 | (a) `from datetime import datetime, timezone`; insert at md index 2: `f"_fold moment: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_`. (b) Write `run_manifest.json` beside FOLD_SECTIONS.md: `{"topic": <new optional --topic arg>, "fired_arg": a.fired, "n_files": n_files, "rows": len(all_rows), "fold_moment": <same ts>}`. (c) fold_run.sh gains the topic pass-through (runner call site mickey17-v2.dwf.ts:295 already passes 2 args; add the third). | E7 (no fold timestamp; archive moved 75 -> 94 between two folds of one run and no reader could tell which state they held) + E22 (fired self-referential: `fired = a.fired or n_files` made `missing: 0` measure nothing; live decode `2026-10-04-0` = targets length 0) | Fold :120,:125,:227-228 read this sitting; MICKEY17 addendum 1.4 + READ_ESTATE addendum 1.2 (slug decode from clone bytes :84,:87,:103-116 confirmed this sitting) |
| R3 | .zcode/workflows/mickey17-v2.dwf.ts:79-109,:320-352 | Add args `master_name` (string, default "MASTER_MICKEY17_V2.md") and `addendum_name` (string, default "MICKEY17_V2_RUN_SPEC_ADDENDUM_" + RUNSLUG + ".md"); replace the 8 hardcoded MASTER_MICKEY17_V2.md occurrences (:321,:327-ish,:332,:338,:344,:351,:355,:357 region) and the fixed addendum path at :346 with the constants. | E33 (master-name drift: clone filed MASTER_READ_ESTATE.md while the saved def hardcodes the old name) + the overwrite data-loss class: the fixed addendum path destroyed run-0's 10-03 filing (bytes survive only at commit 0c9d72a06) | mickey17-v2.dwf.ts:321,:346 read this sitting; clone renames read-the-estate.dwf.ts:327,:352; addendum header lines 10-15 |
| R4 | .zcode/workflows/mickey17-v2.dwf.ts:111-136 | Add args `genre` ("frontier" default | "estate-read") and `lanes` (json, optional; used when args.targets is empty instead of throwing at :108): genre swaps LANE_SYS fetch text and the deepAsk "curl -sL the source" (:153) for disk-instrument text, and marks the URL-liveness section a structural no-op; keep the throw only when BOTH targets and lanes are empty. | The clone-drift class: 3 slug formulas (runner :88; read-the-estate :87 + `args.topic \|\| args.slug` :84; execute-register `+ "-exec"` :77), args.targets contract silently broken, clones unversioned (.gitignore:198) and invisible to the saved-fleet surface | All three files read/grepped this sitting; E31 (third slug shape), E35 (unnamed estate-read genre) in the addenda |
| R5 | tools/workflow_gate.py:147-164 (+ configs/workflow_gate_scenarios card) | Add `G8_PROMISE_ALL_RE = re.compile(r"Promise\.all\(")` context scan: if the script awaits Promise.all over a mapped lane array whose wave width (`slice(0, N)` literal or WIDTH default) exceeds 3 and no envelope-receipt stamp exists, g8 fails. Land the scenario card in the same commit (LAW-12 clause; never widen the gate without one). | The width law binds the fleet's REAL dispatch shape (8-wide ramp waves, mickey17-v2.dwf.ts:180-181,:229-230) but G8 passes every undeclared script (`if not widths ... return True`, workflow_gate.py:158); no post-G8 re-gate sweep exists | workflow_gate.py:151-164 read this sitting; registry rows 64-75 (12-member pre-G8 sweep, 02:33:47-02:34:06Z) vs 87-88 (G8 fires only on the declaring fixture); 14 of 19 standing members ever gated, 5 game-dig veins never gated at all (python json census, 88 rows) |
| R6 | .zcode/workflows/FLEET.md (new) + 8 retired headers | Write FLEET.md: KEEP the-gala, olm-mine, ractor-engine, mickey17-v2, gap-analysis, fill-ball, drop-dig (wide-dig merged); RETIRED the-50, tree-doctrine-dig, music-cut, game-dig-{coop-social,creature-farming,horror-maze,liveops-seasonal,roguelike-runs}, each with a one-line reason citing SYNTHESIS.md:53. Stamp each retired file's description line 2 with `RETIRED 2026-10-04 per SYNTHESIS.md:53 - do not fire; see FLEET.md`. Re-gate all 19. | The standing fleet surface advertises 19 alive badges for a 7-member fleet; the prior dogfood's manifest demand (SYNTHESIS.md:27) and retirement verdict never reached a single byte (headers read this sitting: pre-verdict) | Dir listing (19 files, no manifest); head -6 of the-50/music-cut/tree-doctrine-dig; a53b101d4 commit message + SYNTHESIS.md:53 |
| R7 | tools/mickey17_v2_fold.py:197,:207 | (a) Compute the screened line: count rows carrying the six rubric fields (or gap notes) instead of printing the hardcoded parenthetical. (b) Truncate TOP-K claims at word boundary or raise 110 -> 160. | The screened literal certifies a check that never ran (fold :197 prints "(all rows carry the six rubric fields...)" unconditionally); E23 mid-word TOP-K truncation ("across 98", "added 2026-10-04") | Fold :197,:204,:207 read this sitting; READ_ESTATE addendum 1.3 |

Ranking logic: R1 is the worst live defect (a counting gate that launders false cleanliness, proven recurred);
R2 makes every future fold self-dating and self-describing (kills the circularity class); R3 stops active data
loss (the overwrite class already ate one filing); R4 collapses the clone drift that regenerates every defect
class per burn; R5 closes the gate's declaration blind spot; R6 executes the fleet's own verdict; R7 is
hygiene. A workflow that should die says so in R6 - none of the KEEP members dies this round; the 8 retired
names already died by verdict and are waiting for the bytes to catch up.

## BLIND SPOTS (honest)

- I did not execute the fold tool, the gate, or any workflow this sitting (read-only seat; the fold rewrites
  FOLD_SECTIONS.md in place, and the execute-register run dwfrun-e9656e14 is IN FLIGHT - its archive was off
  limits). Every engine defect above is grounded in source lines I read plus the two addenda's own byte-check
  receipts, not in a failure I reproduced.
- The three skeletons were compared by marker greps and the runner's full read, not a line-by-line diff; my
  claim that they differ only in the four named parameters is scoped to what I grepped (RUNSLUG, MASTER_,
  ADDENDUM, targets block, Promise.all, deep_tier2).
- Lane-file contents (run-0's 15 lanes, read-estate's 12) were not re-read; content-level claims ride the
  addenda's recorded 47 + 45 fixed-string checks.
- The runner's interim digest changes (4 digests in the registry) cannot be attributed: .zcode/ is gitignored,
  no history exists; whether any interim edit tried and reverted an E-item is unknowable from bytes I hold.
- Whether the harness re-materializes saved workflows from a store outside .zcode/workflows/ was not probed;
  R6 hedges with amend-not-delete per the RETIRED.md Q7 precedent.
- G8's wiring into CreateWorkflow (is the gate load-bearing at submit, or honor-system) was not read this
  sitting; I read the gate's checks and the registry it writes, not the harness submit path.

Sibling convergence: F1 is the fourth independent derivation (dogfood.md F1, operations.md F1, economics.md
verdict-blindness row, this file). F4 re-derives a53b101d4's minimum-viable-fleet from current bytes plus the
unlanded manifest demand. F2, F3 are this seat's own.

## CORRECTIONS (hostile second pass, same sitting, re-checked against bytes)

The pass verdicted F2 and F3 weakened. Both stand, corrected; every correction below was re-verified this
sitting with the named instrument, not adopted from the pass:

1. F2, the --fired mechanism (my error: repeated the READ_ESTATE addendum 1.2's mechanism without checking
   the clone's own call site, which I already held in my first grep). Re-check: read-the-estate.dwf.ts:301
   passes `String(TARGETS.length)` where TARGETS = ALL.slice(0, WIDTH) and ALL is the hardcoded 12-entry
   array at :103-116, so the fold received --fired 12 (a script-internal constant), not 0; the 0 lives only
   in the RUNSLUG suffix. The addendum's inference "args.targets was empty" survives (the slug formula
   proves it); its "--fired 0 falls back to file count" mechanism does not. Lesson banked: a lane's
   self-report about a mechanism is a claim, not evidence, even when the lane is a SPEC seat.
2. F2, the commit-survival inversion (my error: inherited a7ca49be1's loose commit line). Re-check: `git show
   0c9d72a06:watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md | head -8` returns the 2026-10-01 gap-analysis
   filing; `git log --all --oneline -- <path>` returns exactly a7ca49be1 / 0c9d72a06 / 3752abae2, none of
   which holds the 10-03 filing. The 10-03 bytes survive nowhere; only E19-E24 restatements in the current
   filing. The data-loss thesis is STRENGTHENED (zero byte survival, not digest survival).
3. F2, the parity claim (my error: asserted "matched SWEEP..SPEC..FILE across all three files" without
   grepping clone 3 for the spec phase). Re-check: grep for spec-writer/ADDENDUM/phase( over
   execute-register.dwf.ts returns phases :174/:233/:258/:279/:311/:327 only - no spec phase, and the filer
   checks 2 items (:327-335 read). My own falsifier fired; "only four parameters differ" is withdrawn and
   replaced by five knobs including spec_phase. New consequence recorded above: the execute-register run
   files no spec addendum at all.
4. F3, census hygiene (my errors: 89 vs 88 rows; window attribution; file-swapped line cites). Re-check:
   python json census = 88 rows; music-cut = row 63 at 2026-10-03T21:56:30Z; the 02:33:47-02:34:06Z sweep
   is rows 64-75 = 12 members; 14 of 19 standing members ever gated; the 5 game-dig veins never gated;
   rows 76-86 span 10-04T09:54 to 10-05T04:39, all pre-G8 (row 87) and fixture-free; read-the-estate's
   Promise.all is :239-240, execute-register's is :223-224. The strengthened core: gate coverage of the
   standing fleet is 14/19 historically and 0/19 at G8 epoch - worse than first filed.

Standing instrument for the corrections: this sitting's commands - `git show 0c9d72a06:<path> | head -8`,
`git log --all --oneline -- <path>`, `grep -n "spec-writer\|ADDENDUM\|estate-filer\|Verify:\|phase("
.zcode/workflow-drafts/execute-register.dwf.ts`, `grep -n "Promise.all"
.zcode/workflow-drafts/read-the-estate.dwf.ts`, and the python json census over
memory/workflows/REGISTRY.jsonl printed in full above.
