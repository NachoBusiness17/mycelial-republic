# ACCURACY LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

Filed by the accuracy lens of the fleet ractor. Topic: dogfood the standing
WORKFLOW FLEET and steal the improvements back into the definitions. Evidence
base, all read or run this sitting: `tools/mickey17_v2_fold.py` (full read),
`tools/workflow_gate.py` (G1-G8 block + G8 impl read; scenario suite executed),
`.zcode/workflows/mickey17-v2.dwf.ts` (full read, 380 lines),
`.zcode/workflow-drafts/read-the-estate.dwf.ts` and `execute-register.dwf.ts`
(targeted reads + diff counts), `.zcode/workflows/gap-analysis.dwf.ts` (header
+ slug lines), md5s over the gap-draft trio, `git ls-files`/`git check-ignore`
over `.zcode/`, both spec addenda (`watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md`,
`watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md`), `corpus/steal/MASTER_READ_ESTATE.md`
(full read), `memory/workflows/REGISTRY.jsonl` tail, the in-flight lane archive
`memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/`, commit a53b101d4
message + stat, and one grep hit set from
`watch/inbox/ractor_engine/2026-10-04-parked-decisions/break-operations.md`.
Nothing below is adopted from a lane self-report without saying so.

## The engine state in one paragraph

The skeleton ran three mega-burns in 36h and the engine's counting layer is
still blind to the verdicts its own runners persist. The fold script
(`tools/mickey17_v2_fold.py`) reads shapes no runner writes (PRISMA, lines
179-191), counts list lengths instead of verdict values (verifier table, lines
156-162), ranks TOP-K alphabetically (line 204), never stamps a fold moment,
and its `fired` default is circular (line 120). Every one of these is
documented in the E-ledger (E5, E20, E22, E23, E7) by the runs' own SPEC
seats, twice, with byte-checks - and every one is still in the bytes this
morning, because the ledger that names them is prose the script never reads.
Meanwhile the fixes that DID land (G8-width-shape in the gate, the tier-2
merge language in the runner) prove the promotion path works when a seat
executes it.

## FINDING 1 (rank 1, CONVERGENT with both addenda's SPEC seats): the fold
## script is the engine's blind organ, and this week's worst defect lives there

`tools/mickey17_v2_fold.py:179-183` collects exclusion keys from a top-level
`unconfirmed` list whose entries carry a `claim` field, and `:190` matches
`norm(r.get("claim"))[:80]` against them. No runner in the estate writes that
shape: the runner persists tier-2 verdicts as `deep_tier2` arrays of
`{row_key, verdict, evidence}` (`.zcode/workflows/mickey17-v2.dwf.ts:278-284`,
the persist phase). Result, byte-confirmed by both SPEC seats: run-0's a08 r9
and the 2026-10-04-0 run's five unconfirmations (r04#1, r05#0-#3) all rode
`included` while the fold printed `excluded: 0` - six substantive corrections
(910 not 917, 28 not 30, 250 not 160, 86.01 not 89.4, plus two more) carried
only because seat layers hand-decoded what the script cannot see. The
verifier table compounds it: `:158-160` (`vc[k] += len(v)`) counts list
LENGTHS by key name, so the yes/no split (63/12 run-0; 48/12 read-estate) and
the verified/unconfirmed split (15/1; 7/5) exist in no fold number. And the
key names are a per-lane lottery, not a per-generation one: the in-flight
exec run's 7 landed checks files (read this sitting,
`memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/*.checks.json`) use FOUR
list key names - `supports` (e01/e05/e08), `checks` (e02/e03), `entries`
(e04), `rows` (e07) - despite `execute-register.dwf.ts:47` typing the field as
`supports`. Tier-1 checkers invent key names; nothing validates them; the
fold's table then prints the lottery as if it were a tally.

The width-gate metrics in the same script mislead at these shapes (E24, twice
documented): with a 5-row floor and 12-15 lanes, top-10 share is arithmetically
forced (53.2% floor at 15 lanes; 83.3% observed at 12) and median=max=min, so
the Law-7 gate line at `:177` prints with zero discriminating power.

NOT RUN, stated: I did not execute `tools/mickey17_v2_fold.py` - it rewrites
`FOLD_SECTIONS.md` in place (`:227-228`) and would mutate the archives this
lens measures. The defect claims are grounded in read source lines plus the
two addenda's independent recounts, not an executed failure.

Falsifier: run the fold against `runs/2026-10-04-0/lanes` with `--fired 12`
into a scratch copy; if it prints any excluded count under code 9 for the five
on-disk `deep_tier2` unconfirmed entries, this finding is wrong.

Move (one sitting, ~30 min, coordinate with the in-flight e12 lane which is
amending this same file per its lane task at
`.zcode/workflow-drafts/execute-register.dwf.ts:103`): in
`tools/mickey17_v2_fold.py`, (a) walk `deep_tier2` lists, match rows by
lane-id + claim-head prefix (row_key format is laneId + ": " + first six
claim words, per `mickey17-v2.dwf.ts:156`), count unconfirmed/crashed into
`excluded` under code 9; (b) decode verdict VALUES from any list whose
entries are dicts with a `supports`/`verdict` field and print the splits in
the VERIFIER TABLE; (c) stamp `- folded_at: <UTCISO>` in the header; (d) when
median==max==min print "gate vacuous at uniform N-row floor" instead of the
Law-7 line.

## FINDING 2 (rank 2): the tier-1 persist instruction is the refire-overwrite
## vector, inherited by all three skeleton generations, still live in the
## in-flight run

`.zcode/workflows/mickey17-v2.dwf.ts:145-146` (the tier-1 supportsAsk) says
"Write the CheckFile as JSON to ... checks.json (Write tool)" with NO merge
clause, and the CheckFile interface at `:50-55` has no `deep_tier2` field.
The tier-2 persist phase 130 lines later (`:278-284`) DOES carry merge
language ("keep any existing deep_tier2 entries... appended after them"). So
on any refire, the tier-1 writer rewrites the whole file with only
{lane, supports, counts} and destroys the prior sitting's persisted tier-2
verdicts. This is byte-proven as E26's root cause: a07's overwrite note ("the
prior deep_tier2 section is not carried forward") is quoted and byte-checked
in the run-0 addendum section 5 item 13. The defect is inherited unchanged by
both derivations: `read-the-estate.dwf.ts:156` (merge language only at
`:286-287`) and `execute-register.dwf.ts:144` (merge only at `:269`). The
in-flight exec run will re-bite on its first refire.

Falsifier: fire any lane refire against a lane whose checks file carries
deep_tier2 and diff before/after; if deep_tier2 survives the tier-1 rewrite,
finding wrong.

Move (one sitting, 15 min): paste the merge sentence from the deep-persist
phase into the tier-1 persist instruction in all three files - exact edit at
`mickey17-v2.dwf.ts:146`: after "(Write tool)" insert "Read the file first if
it exists; keep every existing key verbatim (including deep_tier2); replace
only lane/supports/counts." Mirror at rte:156 and exec:144.

## FINDING 3 (rank 3): the runs ride untracked drafts, the auditor read the
## wrong runner, and a Spec-seat inference is falsified by the draft's own bytes

`.gitignore:198` ignores the entire `.zcode/` tree; `git ls-files .zcode/`
returns exactly one file (`.zcode/workflows/the-gala.dwf.ts`). All three
mega-burn skeletons live only in `.zcode/workflow-drafts/` (untracked,
safe-to-delete). Consequences, all byte-checked this sitting:

1. The read-the-estate SPEC seat audited its run using the SAVED
   `.zcode/workflows/mickey17-v2.dwf.ts` (its evidence base says so, addendum
   line 14) and concluded (section 1.2, E22) that the casualty `fired: 12`
   "measured nothing about firing" and that "if targets was empty... 12 lanes
   ran targetless." The run rode the DRAFT
   `.zcode/workflow-drafts/read-the-estate.dwf.ts`, whose bytes define all 12
   lanes inline as a hardcoded `const ALL` (lines 103-115) with
   `TARGETS = ALL.slice(0, WIDTH)` (`:117`) - so `String(TARGETS.length)` at
   `:301` passed a genuine 12, the lanes each carried a real `what`/`start`,
   and nothing ran targetless. The "-0" suffix is a vestigial organ, not a
   broken interface: the slug formula at rte `:87` (copied from
   `mickey17-v2.dwf.ts:88`) appends `args.targets.length`, an arg the
   read-the-estate schema no longer defines (its args are `period` + `slug`),
   so EVERY fire of that draft mints "-0" regardless of lane count. The same
   vestige is LIVE in the SAVED fleet: `.zcode/workflows/gap-analysis.dwf.ts:90`
   appends `args.targets.length` while its args schema (lines 14-27) is
   `period` + `slug` only. The addendum's honest hedge ("a hand-made directory
   name cannot be excluded") does not save the stated conclusion, which it
   called "the only consistent reading."
2. E33's unresolved either/or ("the fold seat deviated from the saved runner
   or the runner's name constant is stale") resolves the same way: the draft
   that ran hardcodes its own master name (`MASTER_READ_ESTATE.md` in its fold
   phase; `MASTER_EXECUTE_REGISTER.md` at `execute-register.dwf.ts:304`). The
   saved runner's 8 `MASTER_MICKEY17_V2.md` occurrences are simply not the
   bytes that ran.
3. CONVERGENT: the 2026-10-02 fleet dogfood (commit a53b101d4) already named
   this class - "bank-the-fire-ledger (run history in gitignored
   safe-to-delete dir = the one decaying asset)". Three days later,
   `git ls-files` proves it unexecuted.

Falsifier: `git stash -u && git clean -fdx .zcode/` on a scratch clone; if the
19 definitions and 3 mega-burn skeletons survive, finding wrong. (Do NOT run
this on the live tree.)

Move (one sitting): (a) `git add -f .zcode/workflows/*.dwf.ts` + a .gitignore
exception line - the definitions are product, not cache; (b) runner amendment:
add a `script_path` arg and extend the estate-filer ask
(`mickey17-v2.dwf.ts:349-353`) to copy the running script bytes into
`runs/<slug>/RUNNER.dwf.ts` plus write `manifest.json` {topic, width, lanes,
fired, script_path, moment} - this is E22/E31's manifest demand with a named
mechanism; (c) fix the slug formulas: gap-analysis:90 and rte:87 should drop
the targets-length suffix (mickey17-v2:88 may keep it; its schema has targets
and it throws on empty at :107-109).

## FINDING 4 (rank 4): the G8 width gate landed this morning and is vacuous
## against the standing fleet; two 10-02 dogfood laws remain unexecuted prose

Verified run this sitting: `python tools/workflow_gate.py check --scenarios
configs/workflow_gate_scenarios` -> 9 cards validated read-only, exit 0,
including both G8 cards (fail_g8 FAILs, pass_g8_envelope with stamp PASSes).
G8 is real (`tools/workflow_gate.py:94-98` in CHECKS, impl `:147-164`, landed
2026-10-05 per its own comment citing curiosity-register row 3). But
`G8_MAX_CONCURRENCY_RE` (`:147`) matches only literal
`max_concurrency[:=]<digits>`, and a full-dir grep this sitting
(`grep -n "max_concurrency" .zcode/workflows/*.dwf.ts`) finds ZERO literal
declarations - only prose comments in `the-gala.dwf.ts:11,24`, whose line 11
says "Width rides max_concurrency on the run, NOT in asks." So all 19 standing
workflows pass G8 vacuously; the actual dispatch shape (the run's
max_concurrency parameter) is invisible to a text gate, and the drafts - where
literals DO appear - are the only thing G8 can bite.

Same pattern, older debt: `.zcode/workflows/olm-mine.dwf.ts:8` still carries
"Provenance: 191.8M-token run 2026-09-29" - the struck phantom (citation-lint
founding fixture class per AGENTS.md) - three days after the a53b101d4 dogfood
law "saved-workflow-metadata-inherits-struck-phantoms" named exactly this
file. Nothing can catch it: citation lint scopes to changed .md/.txt/.rst at
pre-push, and the file is git-ignored (finding 3). And the fleet is still 19
members; the 10-02 "minimum-viable-fleet: 19 badges -> 7 real members"
verdict (retire the-50/tree-doctrine/music-cut/game-dig-veins as byte-twins
or parameterized variants) was never executed - all are still present
(`ls` this sitting; the five game-dig files are same-size near-twins, Sep 27
07:21, differing md5s = topic parameterization, not divergence).

Falsifier: run `python tools/workflow_gate.py check --script
.zcode/workflows/the-50.dwf.ts`; if it FAILs on G8, the vacuity claim is
wrong. (Prediction from the bytes: PASS, no literal declared.)

Move (one sitting): add a declared-shape line to each of the 19 headers -
`// max_concurrency: 3` for the narrow ones, `// max_concurrency: 10` plus
`// envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md` for the wide
ones (file exists, verified this sitting, 1009 B, Sep 26) - so G8's regex
binds real numbers; fix olm-mine:8's provenance to the corrected figure; and
put the fleet-minimum question (delete/merge the 8 retired candidates) to the
operator with the 10-02 verdict re-attached.

## FINDING 5 (rank 5): the thrice-reused skeleton should become ONE
## parameterized saved workflow; the bytes already show both halves of the case

The reuse lineage, measured this sitting: `gap-analysis.dwf.ts` (saved),
`Gap-analysis-amend.dwf.ts`, and `Gap-analysis-evening.dwf.ts` are md5-
IDENTICAL (a02467a715532191a7e8db94ee7270a6) - the "evening burn" was a pure
file-copy refire of the saved workflow, friction a saved-workflow re-fire with
new args would have avoided. The next two derivations drifted hard:
read-the-estate differs from mickey17-v2 by 174 changed lines,
execute-register by 244, and rte vs exec by 220. Each derivation fixed organs
locally and never flowed anything back: exec hardcoded its slug suffix at
`:77` ("-exec") while rte kept the vestigial `:87`; each renamed the master
fold target; none inherited a tier-1 merge fix (finding 2). One ambiguity
stated honestly: the run-0 addendum attributes run-0's archive to the saved
mickey17-v2 runner, while read-the-estate's header (`:27`) attributes the
15-lane/94-row state to "the proven Gap-analysis-evening skeleton
(dwfrun-53ba7956... ACCEPT)" - both citations carried; without a landing
journal (E32) or run manifest, which runner's bytes produced which archive is
exactly the question nobody can answer, which is finding 3's amendment.

The estate-read genre (E35) and the execute genre are now proven (two landed
runs + one in flight, 8 of 12 exec lanes' files on disk at my read moment).
The move: promote ONE parameterized saved workflow (the mickey17-v2 skeleton
with a `genre` param: audit | estate-read | execute; master name derived from
slug; lane table = args.targets OR genre-default inline lanes; the finding-1/2
fold and merge fixes in it), then fire derivations as AMENDS of it per the
amend-not-rewrite law the fleet already ships, so fixes propagate instead of
forking. The duplication-is-emphasis flag applies: three runs independently
re-derived the same organ defects (both SPEC seats' E-ledgers + this lens's
byte reads).

Falsifier: if firing the saved gap-analysis via CreateWorkflow saved:{name}
with a fresh slug cannot produce a new run dir (RUNSLUG derives from topic,
so it should), the parameterization claim fails on harness mechanics, not
evidence.

## THE AMENDMENT TABLE (ranked; executable against .zcode/workflows/*.dwf.ts
## + the two engine organs the runners invoke)

| # | Workflow file / organ | Exact edit | Defect prevented | Evidence row |
|---|---|---|---|---|
| 1 | tools/mickey17_v2_fold.py:179-201 (+156-162, +header, +177) | Read deep_tier2 verdicts, match by lane-id+claim-head, count unconfirmed/crashed into excluded (code 9); print verdict-value splits for any verdict-like list; stamp folded_at UTC; print "gate vacuous" when median==max==min | 6 unconfirmations riding included as excluded:0 across two folds; splits hand-decoded every run; untimestamped folds; vacuous gate metrics | addenda 1.1/1.2 both runs; fold:179-191,156-162 read; 4 key names live in exec run this sitting |
| 2 | mickey17-v2.dwf.ts:146 + rte:156 + exec:144 | Insert merge clause into tier-1 persist instruction (keep existing keys incl. deep_tier2; replace only lane/supports/counts) | Refire tier-1 rewrite destroying persisted tier-2 verdicts (E26 root cause) | mickey17-v2:145-146 vs :278-284; a07 note byte-checked in run-0 addendum sec 5 item 13 |
| 3 | .zcode/ (repo level) + mickey17-v2.dwf.ts:349-353 | git add -f .zcode/workflows/*.dwf.ts; add script_path arg; filer copies script bytes to runs/<slug>/RUNNER.dwf.ts + writes manifest.json | Runs' interface record unrecoverable; auditors reading the wrong runner's bytes (falsified targetless claim, this lens) | .gitignore:198; git ls-files = 1 file; rte:103-117 inline lanes vs addendum 1.2 |
| 4 | gap-analysis.dwf.ts:90 + read-the-estate.dwf.ts:87 | Drop the args.targets.length suffix from RUNSLUG (schema has no targets); derive suffix from ALL.length or omit | Every fire minting meaningless "-0" slugs; false interface-failure decodes downstream | gap-analysis:14-27 vs :90; rte:16-24 vs :87 read this sitting |
| 5 | all 19 .zcode/workflows/*.dwf.ts headers | Add `// max_concurrency: N` (+ `// envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md` when N>3) | G8 vacuous-passing the entire standing fleet (zero literals declared) | grep this sitting: only the-gala:11,24 prose; gate:147-164 regex read |
| 6 | olm-mine.dwf.ts:8 | Replace the 191.8M provenance figure with the corrected one + ERRATA 001 cite | Struck phantom re-inherited by every seat loading the saved workflow (10-02 law, unexecuted) | olm-mine:8 read this sitting; a53b101d4 message |
| 7 | fleet membership (operator call) | Execute or re-rank the 10-02 minimum-viable-fleet verdict: retire/merge the-50, tree-doctrine-dig, music-cut, 5 game-dig near-twins | Amendment surface + saved-list noise; dead members still gate-PASS | ls: 19 present this sitting; a53b101d4 message |
| 8 | mickey17-v2.dwf.ts:88 (keep) + schema note in spec | Pin slug formula + manifest + master-name convention in one spec ports block (E31) | Third slug shape in three runs; name drift (E33) | three RUNSLUG lines read: 88 / rte:87 / exec:77 |

Rows 1 and 4-6 are one sitting each; row 2 is 15 minutes; row 3 is one sitting
plus an operator git call; row 7 is an operator decision. No sacred cows: no
workflow earns a death sentence on engine evidence alone this round - the
candidates for retirement (row 7) ride the 10-02 economics verdict, not a
defect.

## Checks run this sitting (exact instruments)

1. `python tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios`
   (venv) -> 9 cards ok, exit 0.
2. `grep -n "max_concurrency" .zcode/workflows/*.dwf.ts` -> 2 hits, both
   the-gala prose comments.
3. `git ls-files .zcode/` -> 1 file; `git check-ignore -v` on two drafts ->
   `.gitignore:198 .zcode/`.
4. md5sum over the gap trio -> identical (a02467a715532191a7e8db94ee7270a6).
5. diff line-counts: mickey17-v2 vs rte 174, vs exec 244, rte vs exec 220.
6. Key-name census over the 7 exec checks files (venv json walk) -> supports
   x3, checks x2, entries x1, rows x1.
7. Full reads: mickey17-v2.dwf.ts, fold script, MASTER_READ_ESTATE.md, both
   addenda, CURRENT.md; targeted reads: both drafts (interfaces, persist,
   slug, lane tables, fold calls), gap-analysis header/slug, gate G8 block.
8. `ls watch/inbox/ENVELOPE_50W_HIT_20260926.md` -> exists, 1009 B.

## Blind spots (honest)

- The OLM mine engine (32/32 twice, 22/24 confirmed, the daymora fabrication
  kill, the zero-overlap falsification) was NOT audited this sitting: those
  claims ride the ask's material and olm-mine.dwf.ts:8 only; its receipts are
  unread by this lens.
- The parked-decisions ractor was sampled (dir listing + break-operations.md:31
  grep hit confirming the test-pins-enforcing-the-bug catch at
  tests/test_route_chat_depth.py) not read in full; its 88-finding and
  hostile-5-3 numbers are the ask's, not mine.
- tools/mickey17_v2_fold.py was never executed (mutates archives); all its
  defect claims are read-line + addenda-recount grounded.
- The exec run is in flight: its lane files are moment-reads (B2-216 applies);
  e06 had no checks file at my moment; its fold has not run.
- The run-0 vs Gap-analysis-evening lineage is stated as an open ambiguity,
  not resolved (no landing journal exists; E32).
- I did not fire any workflow; the parameterization falsifier (finding 5) is
  named but unrun - a real fire is the only instrument.
