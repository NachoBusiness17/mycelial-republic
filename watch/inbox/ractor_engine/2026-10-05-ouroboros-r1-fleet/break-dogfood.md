# break-dogfood: hostile second pass on the dogfood lens (ouroboros r1, fleet)

Filed 2026-10-05 by the break-dogfood seat. Verdicts on the four findings of
`dogfood.md` (the report under break), each byte-checked this sitting against the
estate. No em-dashes; every claim below cites what I read or ran. Instrument
note: all checks ran from `C:/Users/foste/Documents/projects/local_sovereign_agent`
via coreutils stat/find/grep plus `.venv/Scripts/python.exe` JSON walks; git was
reachable from this seat (unlike the lens seat, see blind spots).

## Verdicts

### F1 (E-ledger has no compiler, zero byte landings; lawlog pattern never ported): CONFIRMED

Byte-checks run this sitting:

- mtimes reproduce exactly: `tools/mickey17_v2_fold.py` 2026-09-25 19:21:06 (-0400),
  `.zcode/workflows/mickey17-v2.dwf.ts` 2026-09-26 16:33:33, `tools/lawlog.py`
  2026-10-03 19:34:07, 4158 bytes. Both engine files predate the Oct 3-5 burns.
- Both engine files read in full. The E-item defect surface is unchanged in bytes:
  fold `:120 fired = a.fired or n_files` (E22), `:157-162 vc[k] += len(v)` counts
  list lengths never verdict values (E5), `:181 c.get("unconfirmed")` reads a
  top-level key no runner output contains (E20), no OPERATING ENVELOPE section in
  `:127-228` (E3).
- `find memory -name "E_LEDGER*"` = 0 hits. The seed target does not exist.
- `grep -rn E_LEDGER tools/*.py`: every hit is the substring "E_LEDGER" inside
  "WAVE_LEDGER" filenames (tools/brief_reaper.py:4, tools/cost_rollup.py:45, etc).
  Zero engine-ledger readers. The lens's grep conclusion holds; its grep string was
  substring-noisy, not that it changed the answer.
- E20 filed twice: `watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:95` and
  `watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:256` ("RECURRED at 5x").
- CONVERGENT verified: `operations.md:106,125` (the ledger's fragility: E1-E18
  recoverable only at commit 0c9d72a06 after the rolling-path overwrite) and
  `economics.md:23` ("the saved def IS the frozen fork; burns 2-3 ran from drafts").

Precision dents, none verdict-changing:

- "E1-E35" is a range, not a count. Unique items across both addenda: 26 (holes
  E2, E4, E8-E14, E16; grep -oE "E[0-9]+" | sort -u -V on both files).
- `tools/lawlog.py` is the block METER (jsonl rows + weekly tally, 122 lines read);
  the 66-law compile artifact is
  `.agents/skills/operator-corrections/LAWS_COMPILED_20261003.md` (20748 bytes,
  exists; "66 laws: 20 old + 46 new" per `watch/inbox/LAWLOG_20261003.md:7`,
  receipt-carried). The compile-pattern contrast stands; the lens paired the
  number with the wrong file.
- "Zero byte landings" extends further than stated: the three mega-burns rode
  DRAFT clones, not the saved runner, and the drafts carry no E-wiring fixes
  either (diff of TARGETS/fired/unconfirmed/supports/deep_tier2 lines between the
  saved runner and Gap-analysis-evening / read-the-estate / execute-register
  drafts shows prompt-text drift only).

### F2 (fold_run.sh exists only as unversioned workspace bytes; two live decisions ride it): CONFIRMED

- `find . -name fold_run.sh -not -path "./.git/*"` = 0 repo hits this sitting.
- Workspace copy read in full (723 bytes,
  `~/.zcode/workspace/default/mickey17_v2/fold_run.sh`): `--check-urls`
  unconditional on both branches (:9, :11), `--fired "${1:-0}"` on both branches.
- The silent-default chain is byte-true end to end: wrapper default 0 -> fold
  `:101` default 0 -> `:120 a.fired or n_files` -> `:125 missing = fired - n_files`
  = 0 by construction.
- One nuance the lens left implicit (the addendum states it, E22 note): the runner
  always passes the fired count explicitly (`mickey17-v2.dwf.ts:295,304`,
  `[FOLD_SH, String(TARGETS.length), RUNSLUG]`), so the `"${1:-0}"` default bites
  only on hand-invocation. The wrapper defect and the always-on liveness surface
  (E21, 0-for-3 reproducibility per run-0 addendum 1.3) stand regardless.
- Scoping verified correct: the six GALA-family workflows point at
  `GALA_ROOT + "/fold_gate.sh"` where GALA_ROOT is the ESTATE path
  `watch/inbox/gala_20260925` (the-gala.dwf.ts:91), and that wrapper IS in-repo
  (`./watch/inbox/gala_20260925/fold_gate.sh` found). fold_run.sh is the only
  workspace-only gate wrapper.

### F3 (ractor engine ships the world-read defect class in its own receipt check): CONFIRMED

- `ractor-engine.dwf.ts:315-320` read this sitting: `files.glob(OUT + "/SYNTHESIS.md")`
  on a literal no-wildcard path, catch -> receiptBanked false; `:321-323` then
  prompts "The synthesis file ... does not exist. Write it now" - which would have
  a banked SYNTHESIS.md rewritten on any false empty-read.
- `:184-186` carries the WORLD-READ LAW prose the engine violates; `:311-313`
  carries the tolerance-not-fix comment ("must route to the repair ask, never
  kill" - the cure for the first dogfood's death was routing, not files.read).
- Carried premise, honestly inside the lens's own falsifier: this seat also
  cannot exercise the workflow-runtime `files.glob` facade, so "the sandbox
  rejects literal no-wildcard globs" remains carried from the engine's own prose
  (OLM 2026-10-03 class). The defect as filed (glob-on-literal plus a
  "does not exist" repair prompt that can rewrite banked bytes) is byte-true
  regardless of whether the rejection fires.

### F4 (verifier table inverts meaning; tier-2 sample adversarially selected): CONFIRMED

The lens's numbers reproduce under my independent decode of the checks archives
(all list-valued keys walked, yes/no and verified/unconfirmed values counted):

- run-0 (the gap-analysis-evening refire, per commit a7ca49be1): tier-1 truth
  75 verdicts = 12 yes / 63 no (supports 2y/48n + checks 7y/8n + rows 3y/7n),
  matching the counts dicts (rows 75, yes 12, no 63) and the addendum's 1.1.
  The fold prints `verdicts: checks 15, deep_tier2 16, rows 10, supports 50`
  (run-0/FOLD_SECTIONS.md, read this sitting) - "supports 50" plain-reads as 50
  endorsements while the persisted yes count is 12.
- read-the-estate (2026-10-04-0): tier-1 60 = 12 yes / 48 no (supports 12y/33n +
  checks 0y/10n + entries 0y/5n); deep_tier2 7 verified / 5 unconfirmed; fold
  prints `supports 45`. `corpus/steal/MASTER_READ_ESTATE.md:8-9` carries "12 yes /
  48 no" and "7 verified / 5 unconfirmed" tagged carried - the seat layer
  hand-carrying what the script cannot print, exactly the trust-bytes violation
  as filed.
- Adversarial selection byte-true: `mickey17-v2.dwf.ts:240-245` builds noKeys from
  tier-1 "no" verdicts and gives them pri 0 (ranked first); conclusion at
  `:362-366` sells "tier-2 verified X/Y load-bearing rows"; verified list `:373`.
- PRISMA falsifier re-censused untruncated: `excluded: 0` in all five archived
  FOLD_SECTIONS.md (top-level, run-0, gap-analysis-of-the-estate-s-09--15,
  agent-engineering-frontier-sweep-40, 2026-10-04-0; grep "verdicts:" and
  "excluded:" run on each).
- Sharpened beyond the lens: the exclusion wiring is doubly dead. (a) No checks
  file in any run carries a top-level `unconfirmed` key. (b) Even with the right
  key, the shapes cannot meet: my walk of every deep_tier2 entry across ALL runs
  returns exactly the field set {evidence, row_key, verdict} - no claim field -
  while fold `:183/:190` match on norm(claim)[:80]. The fix must read
  `deep_tier2[].verdict` and match on row_key (lane-prefixed), or it lands
  E20 a sixth time.

## Blind spots of the lens, resolved or re-derived

- BS1 (git unreachable, spore-main unborn): seat-specific, not universal. From
  this seat `git rev-parse --abbrev-ref HEAD` returns
  `mag/run-beta1-factory-build-audi-20260806T231709Z`, and `git cat-file -t
  0c9d72a06` returns `commit`. The E1-E18 recovery point exists in history;
  `git log -1 -- watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md` names a7ca49be1
  (the gap-analysis-evening fold bank, run-0 refire, 75 -> 94 rows, "tier-2
  verified 11/12" at its moment vs 16 entries in the current archive -
  moment drift, not contradiction).
- BS3 (ListWorkflowRuns not attempted): attempted here; capability-blocked in
  this seat too ("workflow execution is not available here"). The three dwfrun
  ids (53ba7956, a6bacf9c, e9656e14) remain carried from the operator order.
- BS2/BS4/BS5: honest as filed; nothing to correct. In-flight exec census moved
  one lane since the lens's moment: 16 files / 7 checks.json now (was 15/7).

## What the lens missed (additions)

1. E20 is field-level fatal, not just key-level: deep_tier2 entries carry no
   claim field anywhere in the archive (field shapes proven above). Any fold
   amendment that reads verdict values but matches on claim lands another
   silent zero. The exact edit: read `deep_tier2[].verdict`, count
   unconfirmed/crashed into PRISMA excluded under their own codes, match rows
   to verdicts via row_key, assert before writing.
2. The E_LEDGER seed move has a git leg: E1-E18 live only at commit 0c9d72a06
   (run-0 addendum supersession note, lines 10-15; commit verified reachable
   this sitting). Seeding "from the two addenda" captures E19+ only and leaves
   E1-E18 prose-locked. Seed = run-0 addendum + read-estate addendum +
   `git show 0c9d72a06`.
3. The skeleton is six-times cloned, not thrice. `.zcode/workflow-drafts/`
   grep -l "fold_run.sh" = Boot-lane-wave-1, Gap-analysis-100m, Gap-analysis-amend,
   Gap-analysis-evening, read-the-estate, execute-register. The three mega-burns
   rode byte-divergent clones (26832 / 26621 / 27642 bytes vs saved 22248,
   stat this sitting) with prompt drift already visible (execute-register's
   tier-1 ask says "prove execution is supports:no", "Do NOT re-read files").
   The wrapper-repoint move touches mickey17-v2.dwf.ts:81 +
   gap-analysis.dwf.ts:83 + six drafts = 8 files, not 4. This is the strongest
   evidence yet for the ask's parameterize-don't-clone question.
4. agent-engineering-frontier-sweep-40 is the archive's largest verifier-table
   inversion and the tier-2-persist counterexample, absent from both the lens's
   and the operator order's run inventories: 40 lanes, 171 persisted tier-1
   verdicts (my decode: 90 yes / 81 no), fold prints `supports 171`, and ZERO
   deep_tier2 keys in all 40 checks files - the tier-2 persistence fix's own
   "first-fire fix" comment (runner :246-247) says verdicts "lived only in the
   run journal" before the fix; this run never got the fix applied.

## Standing summary

Four findings: four confirmed, zero weakened, zero killed. The lens's evidence
chain is byte-solid; its imprecisions are number-pairing (lawlog vs
LAWS_COMPILED, range vs count), scope undercount (two drafts vs six), and one
seat-specific blind spot (git) that this pass resolved in the estate's favor.
