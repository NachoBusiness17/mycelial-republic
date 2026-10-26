# BREAK PASS - moonshot-2 (ouroboros r1 fleet, 2026-10-05)

Seat: break-moonshot-2, hostile second pass. Everything below was read or run this sitting on the same
tree. No em-dashes. Instruments named per claim; not-run stated as not-run.

## Commands run this sitting (the instruments behind every verdict)

1. `git log --format="%h %ad %s" --date=short -3 -- tools/mickey17_v2_fold.py` -> exactly 00e4883b7 +
   59413d255, both 2026-09-25 (F1's commit claim reproduces byte-for-byte).
2. Full reads: tools/mickey17_v2_fold.py (234 numbered lines), .zcode/workflows/mickey17-v2.dwf.ts (381),
   .zcode/workflow-drafts/read-the-estate.dwf.ts (388), .zcode/workflow-drafts/execute-register.dwf.ts
   (360), tools/workflow_gate.py:100-179, both addenda, moonshot-2.md itself.
3. Census: `.venv/Scripts/python.exe` json walk of memory/workflows/REGISTRY.jsonl -> 88 rows (file ends
   with a newline; 88 is the true count), full check-id scan, digest scan, per-name last-gate table.
4. Census: python glob over all five archived FOLD_SECTIONS.md (excluded/fired/missing lines printed) and
   all 98 `*.checks.json` under memory/runs/mickey17_v2 (top-level `unconfirmed` key count, deep_tier2
   field shapes, verdict values).
5. `git show 0c9d72a06:watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md` (header read) +
   `git log --oneline -3 --` that path; `git log --format="%h %s" -1 a53b101d4`.
6. Dir listings `.zcode/workflows/` (19 .dwf.ts, no FLEET.md) and `.zcode/workflow-drafts/` (RETIRED.md:1
   "Q7 sweep, 2026-09-27"); grep -i retired over all 8 retired-by-verdict headers (0 hits each).
7. `sed -n '195,200p' .gitignore` + `git check-ignore -v .zcode/workflows/mickey17-v2.dwf.ts` (rc=0,
   matches `.gitignore:198 .zcode/`).
8. grep -o "MASTER_MICKEY17_V2.md" over the runner -> 8 occurrences (lines 321 x2, 332, 338, 351, 355,
   357); grep -rn "ADDENDUM" over .zcode/workflows/ + .zcode/workflow-drafts/ -> 7 hits, all write-sites
   ("Write the run's spec update to"), zero read-sites.
9. grep -n over SYNTHESIS.md pinned :27 and :53 exactly as the lens cited them.

Not run / not resolved: the harness's CreateWorkflow submit path (is the gate load-bearing or
honor-system) - the dynamic-workflows skill is not on disk under C:/Users/foste/.zcode/skills (dir
listing checked) and corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md greps empty for
workflow_gate/CreateWorkflow; reported unresolved, same as the lens's blind spot. Whether the harness
re-materializes saved workflows from outside .zcode/workflows/ - also unprobed. The fold tool itself was
NOT executed (same read-only reason as the lens: it rewrites FOLD_SECTIONS.md in place).

## VERDICTS

### F1 (E-ledger never compiles to bytes): CONFIRMED

Every byte cite reproduced: vc[k] += len(v) at tools/mickey17_v2_fold.py:158-160; the dead
c.get("unconfirmed") wiring at :181-183; fired = a.fired or n_files at :120 with missing at :125; the
hardcoded screened literal at :197; alphabetical TOP-K at :204 with the 110-char cut at :207; no
timestamp at the write (:227-228); no OPERATING ENVELOPE string anywhere in the file; G8 comment block
dated 2026-10-05 citing "curiosity-register row 3 r03#1" at tools/workflow_gate.py:135-146; lane e04 at
execute-register.dwf.ts:95; lane e12 at :103 touching the fold tool for the 191.8M class only (all 12
lane whats read; none owns E5/E20); MASTER_READ_ESTATE.md:225 is register row 3 (the G8 citation chain
holds end to end). "No workflow reads addenda" upgraded from inference to grep fact: all 7 ADDENDUM
references across workflows and drafts are write-sites. My own 98-file checks census (0 top-level
`unconfirmed` keys, deep_tier2 uniformly {evidence,row_key,verdict}, 34 verified / 6 unconfirmed) proves
E5/E20 at full-tree scale the lens only held via the addenda's 27-file walks. Two corrections, neither
fatal: (a) the tool is 234 lines, not 235 (wc -l; the MICKEY addendum itself says 234 at its line 19;
READ_ESTATE says 235 at its line 14; the lens propagated the wrong one); (b) the falsifier as phrased
("any archived FOLD_SECTIONS.md printing excluded > 0") IS tripped - see Addition 1 - by the legacy
top-level fold, whose excluded: 1 rides the phantom-source path, not the verifier-unconfirmed path. The
falsifier must be re-scoped to "any fold printing a verifier-unconfirmed exclusion reason or a
verdict-value split"; under that scope my census reads 0 across all five folds and the finding stands
stronger than filed.

### F2 (three drifting hand-clones + the overwrite): WEAKENED

The core survives byte-check: three slug formulas (mickey17-v2.dwf.ts:88; read-the-estate.dwf.ts:87 with
args.topic || args.slug at :84; execute-register.dwf.ts:77 "+ \"-exec\""), clone 2's 12 hardcoded
targets at :103-116 (args.targets never read, so the slug suffix decoded 0), master/addendum renames at
:327/:352, 8 MASTER_MICKEY17_V2.md occurrences in the runner, .gitignore:198 with check-ignore rc=0,
addendum supersession note at lines 10-15 recording a real uncommitted overwrite, digest chain
f190bf31e2ef -> 9b51b8e2ee05 -> dbc2eeeac52b -> 5ad12f1aae09 at registry rows 3/4/11/73. Three evidence
defects: (1) "the fold's --fired 0 fell back to file count" is mechanically FALSE - clone 2's fold call
(read-the-estate.dwf.ts:301) passes String(TARGETS.length) and TARGETS is the hardcoded 12-lane ALL, so
the wrapper received --fired 12; had it been 0 the throw at :118-120 would have killed the run. The 0
lives only in the RUNSLUG suffix (:87). The error originates in READ_ESTATE addendum 1.2 and the lens
repeated it without byte-checking the clone's fold call site. The conclusion "fired measured nothing"
survives by a different route: both 12s (the fired arg and n_files) derive from the same hardcoded
array. (2) "the overwritten bytes survive only as digests at commit 0c9d72a06" inverts the note: git
show 0c9d72a06 at that path returns the 2026-10-01 GAP-ANALYSIS filing (E1-E18; its own header carries
the wave-1 ledger forward), and the addendum's note says the overwritten 10-03 bytes survive as a
digest plus substance, i.e. NOWHERE as bytes. The data loss is worse than the lens stated; the citation
of where things survive is wrong (inherited from a7ca49be1's loose "prior filing's bytes recoverable at
0c9d72a06" commit line). (3) The parity claim "I matched SWEEP -> TIER-2 PERSIST -> FOLD -> REVIEW ->
SPEC -> FILE call sites across all three files" is FALSE: execute-register.dwf.ts has NO spec phase at
all - no spec-writer agent, no addendum write (the ADDENDUM grep returns nothing for it), and its
estate-filer at :328-331 verifies 2 items (lanes + master) where the runner verifies 3. The clones
differ by a whole missing phase, so "only four parameters differ" is killed as scoped. All three
defects push the same direction as the thesis (drift is worse), which is why this is weakened, not
killed.

### F3 (G8 certifies only honest declarers; no post-G8 re-gate): WEAKENED

Substance confirmed and strengthened: the gate logic quote is verbatim at tools/workflow_gate.py:157-159
(undeclared max_concurrency returns True), the width-law comment at :140-143 says the dispatch shape is
the retry strategy, the 8-wide Promise.all ramp is real (mickey17-v2.dwf.ts:180-181 with :229-230;
execute-register.dwf.ts:223-224), and G8 first appears in the registry at row 87 (2026-10-05T05:19:34Z)
on the fail_g8 fixture only - no standing member carries a G8-era row. The census arithmetic around it
fails byte-check: the registry holds 88 rows, not 89; "the 19 standing workflows were last gated
2026-10-04T02:33:47-02:34:06Z (rows 63-75)" is false on three axes - that window is rows 64-75 (12
members), row 63 (music-cut) sits at 2026-10-03T21:56:30Z outside it, only 15 distinct standing members
were EVER gated (one of them, law12-genesis-repass, no longer exists on disk), and the 5 game-dig veins
have no registry row at all; "rows 76-86 (post-G8)" is doubly wrong (they predate G8's row 87 and
contain no fixtures - they are ractor-engine/-2, primer-adjacent, kit-50wide, and the two clones); and
read-the-estate's Promise.all sits at :239-240, not the cited :223-224. A quantifier breach inside the
one finding about gates that certify by silence. Re-based numbers make the finding stronger: 5 of 19
on-disk members have never been gated even once.

### F4 (unexecuted retirement verdict): CONFIRMED

19 .dwf.ts files on disk with no FLEET.md among them; all 8 retired-by-verdict files (the-50,
tree-doctrine-dig, music-cut, the 5 game-dig veins) carry no RETIRED stamp (grep -i retired, 0 hits
each); SYNTHESIS.md:27 carries the manifest demand and :53 the KEEP/MERGE/RETIRE card, both byte-exact
as cited; a53b101d4's commit message carries minimum-viable-fleet (19 badges -> 7 members);
.zcode/workflow-drafts/RETIRED.md:1 names the Q7 sweep precedent. The lens scoped its absence claims
honestly. No defect found.

## WHAT THE LENS MISSED (additions)

1. The F1 falsifier is tripped as written, and the exclusion engine is not dead - only the
   verifier-unconfirmed reason is. The legacy top-level fold (memory/runs/mickey17_v2/FOLD_SECTIONS.md)
   prints "excluded: 1 phantom-source (dead-lane negative row): 1" and "fired: 9 / missing (no file):
   -49". The single_row_dead path at mickey17_v2_fold.py:186-189 CAN fire; the defect is precisely that
   the :181-191 unconfirmed path never has. The -49 is also the earliest live evidence of the E22
   fired/n_files class (a 9-lane wave folded against a 58-file mixed top-level archive - the mixed-fold
   catch that drove the per-run archive fix in 00e4883b7). Falsifier: another fold printing a negative
   missing (the other four all read missing: 0). Move: re-scope F1's falsifier and fold the -49 row into
   R2's evidence; 5 minutes.
2. Full-tree proof of E5/E20 the lens held only via the addenda: 98 checks files censused, 0 carry a
   top-level `unconfirmed` key, 17 carry deep_tier2 with the uniform field shape (evidence, row_key,
   verdict) and no claim field, verdict values 34 verified / 6 unconfirmed - and the 6 decomposes
   exactly as the two addenda measured (1 run-0 a08 + 5 read-estate). Falsifier: any checks file whose
   deep_tier2 entries carry a claim field or whose top level carries `unconfirmed` (census says none).
   Move: bank this census one-liner as R1's dogfood assertion (the amended tool must print excluded: 6
   on the current tree); 10 minutes.
3. Clone 3 lost the SPEC phase entirely, which falsifies the lens's parity claim AND doubles F1:
   execute-register.dwf.ts writes no run addendum (no spec-writer agent; estate-filer checks 2 items,
   not 3), so the one burn built to EXECUTE a register is structurally mute about its own engine
   lessons - the 60M run's defects will never even reach the E-ledger channel F1 says has no executor.
   Falsifier: an addendum write or spec seat anywhere in execute-register.dwf.ts (grep: none).
   Move: add a file_addendum arg (default true) to R4 and restore the spec phase in clone 3 before its
   next fire; ~15 minutes.
4. The registry's true arithmetic (88 rows; 12-member window rows 64-75; 15 standing members ever
   gated; 5 game-dig veins never gated at all) re-bases F3 and changes R5/R6's sweep: "re-gate all 19"
   would mint FIRST-EVER gate rows for 5 members, not refresh rows. Falsifier: any registry row naming a
   game-dig vein (census: none). Move: rerun the census command and paste real numbers into R5/R6; 5
   minutes.
5. The "--fired 0" mechanic is wrong in the READ_ESTATE addendum 1.2 itself (inherited by lens F2/R2):
   clone 2 passes --fired 12 (TARGETS.length of the hardcoded ALL at :301); the 0 is only the slug
   suffix. The addendum's own limit note ("stated as inference") does not cover this - the clone bytes
   settle it. Falsifier: a fold output or wrapper trace showing --fired 0 for run 2026-10-04-0 (the
   archived fold prints fired: 12, consistent with 12 passed or with the 0-fallback; the clone bytes
   decide). Move: correct R2's evidence text; the manifest amendment is unchanged; 5 minutes.

## Net

F1 and F4 survive intact (F1 stronger than filed after my census). F2 and F3 keep their theses but ship
with evidence errors a hostile reader would find in minutes: F2's --fired mechanics, its survival
citation, and its phase-parity claim all fail byte-check; F3's registry numbers fail on four counts.
The amendment table's directions all survive; R1, R2, R3, R5, R6 each need the evidence-row corrections
above before anyone executes them, and R4 gains the file_addendum clause from Addition 3.
