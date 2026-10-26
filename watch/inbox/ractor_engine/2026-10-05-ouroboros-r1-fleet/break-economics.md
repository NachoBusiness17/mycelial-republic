# BREAK-ECONOMICS (hostile second pass on lens-economics) - OUROBOROS ROUND 1 (2026-10-05)

observed_at: 2026-10-05. Seat: break-economics of the ractor on OUROBOROS
ROUND 1. I byte-checked every evidence cite in the economics lens against the
estate, re-ran its censuses untruncated with my own instrument, and executed
the one check the lens declared unrunnable. Laws held: no em-dashes, every
claim cites what I read or ran this sitting. The report I was handed was
TRUNCATED inside finding 4's falsifier ("After the one-line s..."); verdicts
below cover the four visible findings; economics.md's remaining rows (5 and
6) are covered under finding 2's cluster per the lens's own banking note.

## Verdicts

### 1. Fold gate verdict blindness (economics row 1) - CONFIRMED, strongest possible byte level

- `tools/mickey17_v2_fold.py:157-160` is exactly `vc[k] += len(v)` over
  list-valued keys (loop at 157-160); `:179-183` is exactly the
  `c.get("unconfirmed")` / `x.get("claim")` block. Both cites byte-exact.
- Runner side: DeepCheck carries `row_key`/`verdict`/`evidence` only
  (mickey17-v2.dwf.ts:56-60), persisted under the key `deep_tier2`
  (mickey17-v2.dwf.ts:278; read-the-estate.dwf.ts:284).
- MY OWN untruncated censuses of BOTH archives (python over
  `runs/2026-10-04-0/lanes/*.checks.json` and `runs/run-0/lanes/*.checks.json`):
  0 of 12 and 0 of 15 files carry a top-level `unconfirmed` key; deep_tier2
  entry field shapes are exactly `{evidence, row_key, verdict}` in both;
  verdict values 7 verified / 5 unconfirmed (2026-10-04-0) and 15 verified /
  1 unconfirmed (run-0). The shapes can never meet, as claimed.
- The defective output itself is on disk: `FOLD_SECTIONS.md` in 2026-10-04-0
  prints `excluded: 0` and `verdicts: checks 10, deep_tier2 12, entries 5,
  supports 45` over that archive.
- Addenda numbers reproduce: run-0 sec 1.1-1.2 (tier-1 63 no / 12 yes = 84
  percent; a08 r9 riding included under excluded: 0), read-estate sec 1.1
  (48 no / 12 yes = 80 percent; 7 verified / 5 unconfirmed; 5 unconfirmations
  riding included). 6 substantive unconfirmations across the two burns = 1 + 5,
  checks out. "5th recurrence" is the read-estate addendum's own E5 count.
- Two minor wobbles, not verdict-changing: (a) "each costing ~400 careful
  addendum lines" fits read-estate (402 lines by my Read) but overstates
  run-0 (192 lines); (b) the finding text's "tier-2 11/12" for run-0 is the
  run-conclusion figure while the addendum's own decode is 15/16 persisted
  entries (different denominators, both real). The move's expected re-run
  values (48/12 and 7/5) match the archive truth I measured.

### 2. Fork-not-parameterize + rolling addendum data loss (economics rows 2, 5, 6) - WEAKENED: core confirmed and strengthened, evidence narrative materially wrong

CONFIRMED core:
- Fork lineage is byte-proven: `cmp` says saved `.zcode/workflows/
  gap-analysis.dwf.ts` is byte-IDENTICAL to `.zcode/workflow-drafts/
  Gap-analysis-evening.dwf.ts` (both 26,832 bytes); read-the-estate.dwf.ts:27
  ("Derived from the proven Gap-analysis-evening skeleton (dwfrun-53ba7956)")
  and execute-register.dwf.ts:22 ("Derived from the proven read-the-estate
  skeleton") name their parents.
- All six fork dimensions verify: inline lane table (a01-a15 / r01-r12 /
  e01-e12 hardcoded vs args.targets), master name (mickey17-v2.dwf.ts:321 /
  read-the-estate :327 / execute-register :304), spec-addendum name (:346 vs
  :352 vs absent), slug formula variant (:88 / :87 / :77 "-exec"), tier-2
  instrument (curl at :152-154 vs Read+grep at :164-166 and :151-153), width
  default (50 at :103 vs 12 at :101 vs none).
- The saved def absorbed none: rolling addendum path still at :346-347,
  hardcoded master (8 occurrences, read-estate E33), curl-only deepAsk at
  :150-158, no master_name arg.
- Death row (row 6) CONFIRMED and strengthened: gap-analysis.dwf.ts:107-116
  hardcodes the frozen 2026-10-03 evening audit (a01 "the hourly arena
  cadence ... $25.11"), and the file is literally the frozen draft (cmp
  IDENTICAL) - a museum snapshot wearing a runnable name, exactly as charged.

WRONG particulars (why weakened):
- "read-estate's spec filing overwrote run-0's" is FALSE. read-the-estate
  writes `READ_ESTATE_RUN_SPEC_ADDENDUM.md` (read-the-estate.dwf.ts:352; git
  log on that path shows exactly one commit, eb687f76a). It overwrote nothing.
  The overwrite at `MICKEY17_V2_RUN_SPEC_ADDENDUM.md` was run-0's OWN second
  SPEC filing over run-0's OWN uncommitted 10-03 first filing (the
  supersession note the lens cited, lines 10-15, misread).
- "whose bytes survive only in git" is BACKWARDS. Run-0's surviving filing is
  the on-disk content. The destroyed 10-03 filing was NEVER committed (the
  note: "uncommitted in the working tree at supersession"); its bytes survive
  only as the E19-E24 restatements inside the current addendum plus D1/D2 in
  the master fold. Commit 0c9d72a06 holds the OLDER 10-01 filing (E1-E18), a
  different document. The truth is worse than the claim: the destroyed bytes
  are not in git at all.
- "All three burns ran from drafts (registry rows 61-62, 85-86 name drafts
  paths)" fails for burn 1: row 61 is Wide-dig-the-Grok-bot-ecosystem (not one
  of the three burns) and row 62 names the SAVED
  `.zcode/workflows/gap-analysis.dwf.ts` path. No registry row names
  Gap-analysis-evening.dwf.ts. Burn 1 was gated under the saved path (rows 62
  and 65), which is the draft saved verbatim at gate time (file mtime 17:17
  local = row 62's 21:17:54Z minute). Burns 2 and 3 from drafts: confirmed
  (rows 85-86).
- Amendment row 2's defect cell ("the addendum overwrite that already
  destroyed run-0's 10-03 filing") is accidentally correct, so the
  per-RUNSLUG cure stands - and is stronger under the true story: the rolling
  path destroyed a filing WITHIN one run (the refire wave over the first SPEC
  pass), a failure mode the lens's cross-run narrative never considered.

### 3. G8 prices declarations, not dispatch (economics row 4) - CONFIRMED, now execution-proven

- workflow_gate.py:156 docstring is verbatim "Scripts that declare no
  max_concurrency pass (the law binds the declared dispatch shape)".
- mickey17-v2.dwf.ts:229-230 fires Promise.all over slice(0,8) then ALL
  remaining lanes (firstWave/restWaves built at :180-181), default width 50
  at :103, and no max_concurrency token anywhere in the file.
  execute-register.dwf.ts:223-224 carries the same shape (its :175-176).
- I EXECUTED the falsifier's first half read-only:
  `python tools/workflow_gate.py check --script <path> --no-register` on both
  mickey17-v2.dwf.ts and the execute-register draft. BOTH PASS, exit 0
  (mickey17 with zero warns; execute-register with one G6 soft-warn). The
  gate passes the exact unbounded-fan shape it was built to police.
- Registry rows 87-88: both FAIL with G8 ok=false (fixture failing as
  designed). e04 lane banks SUITE_EXIT=0 and 9 scenario cards exist (ls
  counts 9 *.card.json under configs/workflow_gate_scenarios).
- Convergence cite verifies: LAND_d3_wire.md:46-56 is the test-pins section
  (the old design pin pinned the buggy wire shape, went RED, was flipped).
- Addition against the lens: it declared this check not-run because
  "--script mode adds registry rows", but `--no-register`
  (workflow_gate.py:331-335, landed 2026-09-29) is the read-only instrument
  built for exactly this case. The falsifier was runnable without mutation.

### 4. G6 soft-warn calibration (economics row 3) - CONFIRMED with two arithmetic corrections

- 28 rows carry G6 ok:false: EXACT (my untruncated python census).
- Corrections: total registry rows = 88 (wc -l = 88; lens said 89), and of the
  28 G6-false rows only 25 are soft warns - rows 1, 36, 39 are HARD G6 FAILs
  (tree-doctrine-dig, two seatlaw rows). The calibrated claim is 25 of 88
  rows (28.4 percent), not 28 of 89 (31 percent). Substance intact.
- 17 of 17 ractor-engine rows since 2026-10-02 carry a soft warn on PASS:
  EXACT (rows 46-79 in my census, including ractor-engine-2 at row 78).
- Mechanism byte-proven: ractor-engine.dwf.ts:26-27 asks the caller for a
  dated slug, and my grep for the G6_STAMP_RE family
  (source-fetched|fetched|observed_at + colon + date) over the file returns
  NO match; G6_STAMP_RE sits at workflow_gate.py:105-107 as cited.
- Cure demonstrated by contrast in my gate runs: mickey17-v2.dwf.ts passes
  G6 clean via its `// source-fetched: 2026-09-26` stamp (:26); the
  stamp-less execute-register draft soft-warns. The one-line stamp fix works.

## What the lens missed (additions)

1. The G8 falsifier was runnable read-only all along (--no-register). Ran it:
   both scripts pass. Any future hostile pass or pre-flight can gate in-flight
   scripts without minting registry rows; the lens's not-run note
   (economics.md "Checks run") overstated the mutation constraint.
2. The destroyed addendum bytes are unrecoverable, and the overwrite class is
   intra-run. The rolling path killed run-0's own first SPEC filing (never
   committed; only E19-E24 restatements survive in the current addendum), not
   a cross-run victim. This makes amendment 2a (per-RUNSLUG addendum path)
   more urgent, and adds a guard the lens did not price: the spec-writer
   phase should MERGE into an existing addendum (the E26 checks-file lesson
   generalized to prose), so a refire can never destroy the first pass's
   filing again.
3. Burn 1 ran under the saved-path fork (byte-identical frozen draft; registry
   rows 62/65), and the measured burn window is ~27.4h (first gate
   2026-10-03T21:17:54Z to exec gate 2026-10-05T04:39:04Z), not the 36h the
   operator order carries. Fork-not-parameterize is real; "all three from
   drafts" is not the registry's truth.
4. A seventh fork dimension the lens's six missed: execute-register DELETED
   the spec-writer phase entirely (its phases run fold, review, file; no spec
   addendum phase anywhere in the 360-line draft). The E-ledger continuity
   that documented every prior burn breaks silently at this fork, and no gate
   checks for the phase. Related hygiene: all forks still write workspace
   copies under `.zcode/workspace/default/mickey17_v2/` regardless of family
   (execute-register.dwf.ts:74), so the exec burn's workspace master would
   land inside the mickey17_v2 dir.
5. Exec-run liveness datum at my moment: lanes e01-e08 banked (latest mtime
   02:38), e09-e12 ABSENT, no FOLD_SECTIONS.md in the run dir, no
   corpus/steal/MASTER_EXECUTE_REGISTER.md, no execute_register_<slug>
   inbox dir (only execute_register_seed_fidelity). Registry rows minted
   05:19-05:20Z prove my sitting is 3h+ past the last lane landing. Mid-sweep
   or stalled is undeterminable from this seat: ListWorkflowRuns errors here
   too (workflow_introspection_unavailable), so the lens's blind spot stands.
6. Registry arithmetic for the record: 88 rows, 25 soft-G6 warns, 9 soft-G3
   warns, 3 hard G6 fails, 17/17 ractor-engine warn. The lens's 89/28/31
   percent should not propagate into round 2's gap register uncorrected.

## Checks run this sitting (exact instruments)

- Read in full: tools/mickey17_v2_fold.py (235 lines), .zcode/workflows/
  mickey17-v2.dwf.ts (381), .zcode/workflow-drafts/execute-register.dwf.ts
  (360) and read-the-estate.dwf.ts (388), .zcode/workflows/ractor-engine.dwf.ts
  (353), tools/workflow_gate.py (385), both run addenda, economics.md.
- Census: `.venv/Scripts/python.exe` over memory/workflows/REGISTRY.jsonl
  (88 rows parsed; G6/G3/soft hard splits; ractor-engine rows; rows 61-62,
  85-88 detailed) plus `wc -l` (88).
- Archive censuses (my own instrument, untruncated): both
  `runs/2026-10-04-0/lanes/*.checks.json` (12 files) and
  `runs/run-0/lanes/*.checks.json` (15 files): top-level key census,
  deep_tier2 field shapes and verdict values.
- Executed: `python tools/workflow_gate.py check --script ... --no-register`
  on mickey17-v2.dwf.ts (PASS exit 0, zero warns) and the execute-register
  draft (PASS exit 0, one G6 soft-warn). No registry row written (--no-register
  returns before the append, workflow_gate.py:362-363).
- Git: `git log --follow` on both addendum paths (MICKEY17: a7ca49be1 /
  0c9d72a06 / 3752abae2; READ_ESTATE: eb687f76a only); `git show -s` date of
  a7ca49be1 (2026-10-04 02:15:42 -0400).
- cmp saved gap-analysis.dwf.ts vs Gap-analysis-evening.dwf.ts: IDENTICAL.
- grep: G6_STAMP_RE family over ractor-engine.dwf.ts (0 hits);
  source-fetched stamp in mickey17-v2.dwf.ts (:26); SUITE_EXIT in the e04
  lane file (present); sed of gap-analysis.dwf.ts:100-120 (a01 "$25.11"
  lane table) and LAND_d3_wire.md:40-60 (test pins).
- cat: FOLD_SECTIONS.md of 2026-10-04-0 (excluded: 0; the list-length
  verifier line). ls: runs dir, both archives, exec lanes (e01-e08), 9 cards,
  draft sizes (26,832 / 26,621 / 27,642 bytes - the lens said ~22KB,
  understated), corpus/steal/MASTER_EXECUTE_REGISTER.md (ABSENT),
  watch/inbox/execute_register_* (one dir, seed_fidelity).
- NOT run: ListWorkflowRuns (workflow_introspection_unavailable error from
  this seat; the lens's blind spot is real and shared), the fold script
  itself (would rewrite FOLD_SECTIONS.md in the live archive - the defect is
  proven from the existing output plus source plus my recount), fold_run.sh
  (outside the repo at WSOUT, unread), hermes_burn usage censuses (token
  figures still ride the operator order).
