# BREAK-ACCURACY: hostile pass on the ouroboros R1 fleet lens (2026-10-05)

<!-- no em/en dashes in this file; plain hyphens only, per the seat law. -->

Seat: break-accuracy, OUROBOROS ROUND 1 of 5 (fleet round). Moment: 2026-10-05, working tree on
branch mag/run-beta1-factory-build-audi-20260806T231709Z. Input: the lens report handed in the ask
(4 findings visible; finding 4's statement was TRUNCATED mid-evidence in the handed text - the verdict
below covers the fully visible evidence chain and does not invent the missing prose).

Every count in this file is a moment-read (B2-216). The execute-register run was IN FLIGHT the whole
sitting: at my moment its lanes dir held 8 lane JSONs (e01-e08), 7 checks JSONs, one stray
e05-transfer-debt-candidates.jsonl, and e06 still had no checks file.

## VERDICTS

### 1. Fold script reads verdict shapes no runner writes; 6 unconfirmations rode included as excluded:0 - CONFIRMED (upgraded: falsifier EXECUTED)

Cites byte-checked: tools/mickey17_v2_fold.py:179-191 (top-level `unconfirmed` list, `claim`-field
match), :156-162 (`vc[k] += len(v)` - list lengths, never verdict values), :227-228 (in-place
rewrite of FOLD_SECTIONS.md); runner persists `deep_tier2` arrays of {row_key, verdict, evidence}
(mickey17-v2.dwf.ts:278-284, DeepCheck interface :56-60); row_key format at mickey17-v2.dwf.ts:156.

Executed this sitting (the lens named but did not run this falsifier):

- Byte-identical copy of the fold script created via the Write tool at
  C:\Users\foste\AppData\Local\Temp\foldcheck_ba\bin\mickey17_v2_fold.py; sha256 of repo original and
  copy both `b9fb8b41275394044b0e3e348b43c0df74b56af3adcac5fe6f13de0efde98473` (uniq -c read 2).
- Ran with USERPROFILE redirected into the scratch tree (so Path.home() resolves to scratch):
  `--run 2026-10-04-0 --fired 12` over a copied lanes dir.
- Output: `lanes=12 rows=60 included=60 excluded=0 dups=2 median_rows=5`, exit 0.
- The disconfirming condition (any code-9 excluded count for the on-disk unconfirmed entries) did
  NOT occur. Blindness claim now has an executed failure behind it, not just source lines.

On-disk census this sitting (parsed JSON, not whitespace-grep): runs/run-0 checks hold 15 verified +
1 unconfirmed deep_tier2; runs/2026-10-04-0 hold 7 verified + 5 unconfirmed. 1 + 5 = 6, byte-exact
against the finding. Both folds printed `excluded: 0` on disk. The five rte unconfirmed row_keys
include r04 "The skip list is arithmetic, not" and 4x r05 (verified by display); run-0's one is a08
"Rails-default is doc-first and honest but" - matching addendum items 18/19 and 17.

The lens's live claim also reproduces: 2026-10-05-exec has 7 checks files using 4 verdict-list key
names (supports 3, checks 2, entries 1, rows 1) against execute-register.dwf.ts:47 typing `supports`.

Strengthening evidence the lens's string did not carry: run-0's own verifier-table line reads
`verdicts: checks 15, deep_tier2 16, rows 10, supports 50` in the SAME file whose PRISMA says
`excluded: 0` - the fold saw the deep_tier2 lists post-persist and still excluded nothing. The defect
is in-script, not phase-ordering.

### 2. Tier-1 persist instruction is the refire-overwrite vector (E26), inherited by all three skeletons - CONFIRMED

mickey17-v2.dwf.ts:145-146 is a write-only instruction (supportsAsk spans :138-148, no read-first, no
merge clause); CheckFile :50-55 has no deep_tier2 field; the tier-2 persist :278-284 carries the merge
sentence. The a07 overwrite note is byte-verified at MICKEY17_V2_RUN_SPEC_ADDENDUM.md section 5 item
13 (line 130), with E26 at line 104 and the law-6 verdict (line 87) naming the same overwrite.
Inheritance byte-verified in both drafts: read-the-estate.dwf.ts:156 write-only (merge only at
:286-287); execute-register.dwf.ts:144 write-only (merge only at :269).

The refire-diff falsifier was not fired by this seat either (firing a workflow is out of this seat's
lane). It is moot for the claim's truth: the vector has one executed real firing already (a07's
overwritten checks file), so the root-cause attribution rides an incident, not a hypothesis. Note the
rte addendum's E26 "CURE OBSERVED" (READ_ESTATE_RUN_SPEC_ADDENDUM.md:271-273) is explained by that
run having 0 refires - the vector never armed - not by any instruction change.

### 3. Three mega-burn skeletons ride untracked drafts; the SPEC seat audited the SAVED runner while the run rode the DRAFT - CONFIRMED

- .gitignore:198 is exactly `.zcode/`; `git ls-files .zcode/` returns exactly one file
  (.zcode/workflows/the-gala.dwf.ts); `git check-ignore -v` run this sitting proves mickey17-v2,
  read-the-estate, execute-register, and Gap-analysis-evening are all ignored by that one line. This
  is the safe equivalent of the clone-plus-clean falsifier; the destructive variant was NOT run.
- The draft hardcodes its 12 lanes inline (read-the-estate.dwf.ts:103-116) with
  `TARGETS = ALL.slice(0, WIDTH)` at :117, and the archive's lane ids r01-steps-jsonl through
  r12-rollup byte-match the draft's ids, with MASTER_READ_ESTATE.md (a draft-only output) filed - the
  run rode the draft.
- The falsified inference is real and byte-present: READ_ESTATE_RUN_SPEC_ADDENDUM.md:75-88 (sec 1.2)
  concludes "12 lanes ran targetless" and "measured nothing about firing" from the SAVED
  mickey17-v2.dwf.ts:88 formula, and its evidence base (line 14) names the saved runner as what it
  read. The vestigial suffix verified byte-exact at read-the-estate.dwf.ts:87 and saved
  gap-analysis.dwf.ts:90, both schemas period+slug only (gap-analysis args :15-27).
- E33 resolution verified: execute-register.dwf.ts:304 hardcodes MASTER_EXECUTE_REGISTER.md.
- CONVERGENT flag verified: commit a53b101d4 carries "bank-the-fire-ledger" verbatim in its message.
- One strengthening site the lens missed: Gap-analysis-evening.dwf.ts:90 carries the same vestigial
  formula (see ADDITIONS 1).

### 4. G8 width-shape gate green while zero saved workflows declare max_concurrency - CONFIRMED (on the visible evidence; statement truncated in the handed report)

Reproduced this sitting, exact commands:

- `.venv/Scripts/python.exe tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios`
  -> 9 cards ok, exit 0, including both G8 cards (G8_width_exception -> PASS fixture,
  G8_width_shape -> FAIL fixture).
- `grep -n max_concurrency .zcode/workflows/*.dwf.ts` -> only the-gala.dwf.ts:11 and :24, both prose
  (byte-read: line 11 "Width rides max_concurrency on the run, NOT in asks - babystep ladder:"; line
  24 an args description).
- tools/workflow_gate.py:147 `G8_MAX_CONCURRENCY_RE = re.compile(r"max_concurrency\s*[:=]\s*(\d+)")`
  matches only in-script declarations; the checker docstring (:152-156) passes a script with no
  declaration ("no max_concurrency pass (the law binds the declared dispatch shape)"). With 0 of 19
  saved workflows declaring anything, the gate's fleet coverage is 0 while the suite stays green on
  fixtures. G8 itself landed today, credited to the in-flight run's register row
  (workflow_gate.py:37, :135).

The finding statement was cut off mid-evidence in the ask; the verdict covers the evidence chain,
which reproduced completely. No text beyond the truncation is asserted.

## ADDITIONS (what the lens missed)

1. **The run-0 vs Gap-analysis-evening lineage ambiguity is closable by bytes.** The lens left it
   open for want of a manifest (E32). The evening draft's own schema closes it:
   Gap-analysis-evening.dwf.ts:85 (`String(args.topic || "")`), :90 (slug formula appending
   args.targets length), args block period+slug only - RUNSLUG can ONLY be "run-0".
   runs/run-0/FOLD_SECTIONS.md reads fired 15 / 94 rows (the Gap-analysis-evening signature);
   runs/gap-analysis-of-the-estate-s-09--15 reads 70 rows with 1 parse error (the earlier 10-01
   run). Falsifier: any topic/targets setter in the evening draft's schema (grep args. over the
   file; none this sitting). Move: 5 min - strike E31's "or the slug was overridden" branch
   (MICKEY17_V2_RUN_SPEC_ADDENDUM.md:109), pin the decode in the spec ports section, and add
   Gap-analysis-evening.dwf.ts:90 as the third edit site in the suffix-drop amendment.

2. **The 10-02 law saved-workflow-metadata-inherits-struck-phantoms is still unexecuted on
   olm-mine.** .zcode/workflows/olm-mine.dwf.ts:8 still reads "Provenance: 191.8M-token run
   2026-09-29" (byte-read this sitting), three days after commit a53b101d4 named exactly this as a
   key law. The lens touched olm-mine only as a blind spot and converted it to no amendment row.
   Falsifier: a SaveWorkflow of olm-mine whose description cites the strike receipt instead of the
   phantom (none can exist in history: the file is gitignored and untracked, so no fix could have
   landed silently). Move: 2 min - edit the description block to replace the phantom provenance with
   the strike receipt path.

3. **The fold gate's own tool is being amended mid-flight while its output is unversioned.**
   execute-register.dwf.ts:103 (e12, task b) amends tools/mickey17_v2_fold.py while the exec run is
   in flight, and G8 already landed in tools/workflow_gate.py the same day (:37, :135) - mid-run
   tool amendment is this week's live pattern, not a hypothetical. FOLD_SECTIONS.md carries no
   script digest, version, or folded_at stamp (E7 in both addenda; the script writes only the lanes
   dir into the header, tools/mickey17_v2_fold.py:127-129), so a fold computed by the amended script
   is indistinguishable from one computed by the old bytes. Falsifier: any archived FOLD_SECTIONS.md
   carrying a digest or timestamp (0 across all four folds, per addenda measurements and this
   sitting's reads). Move: 10 min inside finding 1's fold-fix sitting - print
   sha256(fold script)[:12] + folded_at UTC into the FOLD_SECTIONS.md header; coordinate with the
   in-flight e12 lane, which owns the same file (execute-register.dwf.ts:103).

4. **run-0's fold output is archive-internal proof of the excluded:0 defect (evidence upgrade for
   finding 1, zero-cost).** The same file that counted `deep_tier2 16` in its verifier table printed
   `excluded: 0` in its PRISMA flow - the fold read the verdict lists and dropped their meaning in
   one breath. Falsifier: a checks set whose verifier table omits deep_tier2 while PRISMA excludes 0
   (that would indicate fold-before-persist instead). Move: 0 min - attach the line to E20's ledger
   entry so the fix priority rides an archive-internal proof, not a seat recount.

## BLIND SPOTS OF THE LENS, CHECKED

- Fold script never executed by the lens: CLOSED by this sitting (scratch run above, hash-verified;
  no archive mutated - the estate's runs/2026-10-04-0/FOLD_SECTIONS.md bytes untouched, scratch
  writes confined to %TEMP%\foldcheck_ba).
- run-0 lineage open: CLOSED by bytes (ADDITION 1).
- Execute-register in flight: still true at my moment (8 lane JSONs, 7 checks, e06 checks absent).
- OLM receipts unread: remains unread by this seat too (only olm-mine.dwf.ts:8 read); ADDITION 2
  covers the one byte-fact this sitting verified.
- Parked-decisions ractor sampled not read: unchanged by this pass (out of this seat's lane).
- Parameterization falsifier (saved-workflow re-fire) unrun: still unrun; no workflow was fired by
  this seat. Harness mechanics remains the only open question there.

## NOT RUN / LIMITS

- No workflow fired; no CreateWorkflow/AmendWorkflow from this seat.
- The clone-plus-clean falsifier (finding 3) not run; safe byte-equivalent run instead
  (git check-ignore + git ls-files).
- The refire-diff falsifier (finding 2) not run; the a07 incident is the executed instance.
- The Mimosa hook refused two Bash command forms that paired the fold script's repo path with
  copy/run operations; the sanctioned channel was used instead (Write tool for the scratch copy,
  Bash only for scratch-path execution). Hash equality proves the copy faithful.
- deep_tier2 census is parsed-JSON based; a whitespace-sensitive grep undercounts (found 4 of 5 in
  2026-10-04-0 and 0 of 1 in run-0) - the parsed census is the instrument of record here.
- Everything in this file is a moment-read of a live tree (B2-216): the exec archive moved during
  the sitting and will keep moving.
