# BREAK PASS: lens moonshot-1 (OUROBOROS r1, fleet) - 2026-10-05

Hostile second pass over the moonshot-1 lens report. Every evidence cite was re-measured against the estate this sitting. Instruments: full read of `tools/mickey17_v2_fold.py` (235 lines) and `.zcode/workflows/mickey17-v2.dwf.ts` (380 lines); targeted reads of the three drafts; `cmp`/`diff`/`wc` over the five skeleton copies; a JSON field-walk over all checks files in all five lanes-bearing run archives (repo venv python); reads of both spec addenda, both archived `FOLD_SECTIONS.md` files, `memory/workflows/REGISTRY.jsonl` rows, the workspace dir, and the fire journal snapshot. No audited file was modified. No em-dashes. The three findings SURVIVE; one evidence clause inside finding 2 is corrected (and the correction strengthens the amendment); two lens cites are off by small margins, noted.

## F1. PRISMA exclusion reads a key the runner never writes: CONFIRMED, strengthened

Byte-check of every cite:

| Lens cite | Re-measured | Verdict |
|---|---|---|
| fold `:181` reads `c.get('unconfirmed')` top-level | `tools/mickey17_v2_fold.py:181` is exactly `for x in (c.get("unconfirmed") or []):` | exact |
| `:183`/`:190` match `norm(claim)[:80]` | `:183` `unconf_keys.add(norm(x.get("claim", ""))[:80])`, `:190` `elif norm(r.get("claim"))[:80] in unconf_keys:` | exact |
| runner persists under `deep_tier2` at `mickey17-v2.dwf.ts:278-282`, fields `{evidence,row_key,verdict}` only | `:278-282` is the persist ask; `DeepCheck` interface `:56-60` declares exactly `row_key/verdict/evidence`; drafts carry the same logic (`read-the-estate.dwf.ts:284-288`, `execute-register.dwf.ts:267-270`, `Gap-analysis-evening.dwf.ts:295-299`) | exact |
| 2026-10-04-0 walk: 12 deep_tier2 verdicts = 7 verified / 5 unconfirmed, 0 top-level `unconfirmed` keys | my walk: 12 checks files, `deep_tier2` split `{'verified': 7, 'unconfirmed': 5}`, `files-with-top-level-unconfirmed-key: 0` | exact |
| run-0 walk: 15 verified / 1 unconfirmed | my walk: 15 checks files, split `{'verified': 15, 'unconfirmed': 1}`, 0 unconfirmed keys | exact |
| fold prints `excluded: 0` while they ride included | `runs/2026-10-04-0/FOLD_SECTIONS.md:40` and `runs/run-0/FOLD_SECTIONS.md:40` both read `excluded: 0` | exact |
| convergence: READ_ESTATE addendum 1.1 (E20) + run-0 addendum E20 | `watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:53` ("PRISMA wiring miss re-bitten at 5x (E20)") and `:256`; `watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:50` (1.2) and `:95` | exact |
| e12's own ask names a fold-script check at draft line 102 | the e12 lane object starts at `execute-register.dwf.ts:103` (line 102 is e11); e12(b) says "add the unbound-aggregate check to tools/mickey17_v2_fold.py" | off by one line, substance exact |

Falsifier attacked and extended: the lens measured 0 of 19 checks files across both completed runs. I re-censused UNTRUNCATED across all five lanes-bearing run archives: 0 of 89 checks files (`2026-10-04-0` 12, `2026-10-05-exec` 7, `agent-engineering-frontier-sweep-40` 40, `gap-analysis-of-the-estate-s-09--15` 15, `run-0` 15) carry a top-level `unconfirmed` key of any shape. The lens's falsifier survives at 4.7x its claimed scope. Note the bite is conditional: `gap-analysis-of-the-estate-s-09--15` measured 12 verified / 0 unconfirmed (bug invisible), and `agent-engineering-frontier-sweep-40` predates the persist fix entirely (0 `deep_tier2` anywhere). The exclusion fails exactly when it matters, on the rows carrying corrections.

Fix-the-fix (the lens's move needs one correction before coding): `row_key` is built as `laneId + ": " + claim.split(" ").slice(0, 6).join(" ")` (`mickey17-v2.dwf.ts:156`), the first SIX WORDS, not a 60-char slice. The lens's proposed `norm(claim)[:60]` match would still mismatch whenever six words are shorter than 60 chars, which is the common case. Match `norm(claim).startswith(norm(row_key minus prefix))`, or amend `DeepCheck` to persist the full claim. The ~10-line scope at `:179-202` is right; the one-file-heals-five-consumers claim is right (2 saved: `mickey17-v2.dwf.ts`, `gap-analysis.dwf.ts`; 3 drafts, one byte-identical to the saved gap copy).

## F2. The skeleton should become one saved parameterized workflow: CONFIRMED, one clause corrected

| Lens cite | Re-measured | Verdict |
|---|---|---|
| drafts 397 / 387 / 359 lines, mtimes Oct 3 22:21 / Oct 4 17:15 / Oct 5 00:38 | `wc -l` and `ls -la`: 397 / 387 / 359; mtimes match to the minute | exact |
| pairwise line-diffs 179 and 220 | gap-evening vs read-the-estate = 179; read-the-estate vs execute-register = 220; the uncited third pair (gap-evening vs execute-register) = 255 | exact (third pair larger) |
| `execute-register:77` slug = topic + '-exec' vs `read-the-estate:87` keeping topic + targets.length | both lines read exactly that; live fossils: run dirs `run-0` (empty slug + 0) and `2026-10-04-0` (topic `2026-10-04` + 0) | exact |
| master names diverged (`read-the-estate:327`, `execute-register:304`) | both lines carry `MASTER_READ_ESTATE.md` / `MASTER_EXECUTE_REGISTER.md` | exact |
| saved runner: 8 hardcoded `MASTER_MICKEY17_V2.md` sites | `grep -o \| wc -l` = 8 | exact |
| five copies hardcode one WSOUT + one fold_run.sh (`read-the-estate:81-82`, `execute-register:74-75`, `Gap-analysis-evening:82-83`, saved `:80-81`) | all four cites exact; fifth copy is `.zcode/workflows/gap-analysis.dwf.ts` (byte-identical to the evening draft, same lines) | exact |
| registry gates them as fresh PASS (2026-10-04T21:15:36Z, 2026-10-05T04:39:04Z) | REGISTRY.jsonl rows 85/86 match both timestamps and the workflow-drafts script paths, verdict PASS | exact |
| ".zcode/workflows/ holds none of them" | FALSE for burn 1: `.zcode/workflows/gap-analysis.dwf.ts` is byte-identical to `Gap-analysis-evening.dwf.ts` (`cmp` clean), and REGISTRY rows 62/65 show the Oct 3 burn FIRED from the saved path (2026-10-03T21:17:54Z, digest 545091f90a92, PASS); the drafts copy (mtime 22:21) is post-fire parking | corrected |

The correction does not weaken the finding, it sharpens it: the estate DID save the newest skeleton generation once (`gap-analysis.dwf.ts`, saved Oct 3 17:17), and the next two burns still bypassed it with fresh hand-copies gated as brand-new scripts. The saved engine `mickey17-v2.dwf.ts` has not moved since Sep 26 16:33 while three generations evolved past it. Also verified, stronger than claimed: the fold wrapper `fold_run.sh` is shared by EVERY burn since Sep 25 (mtime 2026-09-25 19:21), lives outside the repo at `C:/Users/foste/.zcode/workspace/default/mickey17_v2/fold_run.sh`, and no receipt anywhere pins its bytes. The parameterization move (args genre + master_name + bank_root; slug = topic + UTC moment; per-run WSOUT; phase-0 manifest) stands.

## F3. The counting gate counts lengths, never values; TOP-K alphabetical; gate line inert: CONFIRMED exactly

| Lens cite | Re-measured | Verdict |
|---|---|---|
| `:157-160` `vc[k] += len(v)` | the loop sits at `:157-160`, the counter at `:160`; the verifier table block is `:154-165` | exact |
| archived line "verdicts: checks 10, deep_tier2 12, entries 5, supports 45" | `runs/2026-10-04-0/FOLD_SECTIONS.md:27` byte-identical; run-0's `:27` reads "checks 15, deep_tier2 16, rows 10, supports 50" | exact |
| 48-no/12-yes and 7-verified/5-unconfirmed computed nowhere by script | full 235-line read: no verdict-value split exists anywhere in the fold; my field-walk recovered exactly `supports=no 48, supports=yes 12, verdict=verified 7, verdict=unconfirmed 5` from the checks files | exact |
| `:177` prints the Law-7 gate unconditionally, zero discriminating power at uniform 5-row floor | `:177` is a static string in the WIDTH-ECONOMICS block; both archived folds print it at 12 and 15 lanes with median=max=min=5 and top-10 share 83.3% / 73.4% (arithmetic at those shapes, per E24) | exact |
| `:204` rank key cut r05#3 while 21 later-alphabet high rows ranked below | measured: 34 high rows; top-12 = r01#0, r01#3, r02#0, r03#0, r03#1, r04#0, r04#1, r04#2, r04#4, r05#0, r05#1, r05#2; rank-13 (first cut) = `r05-trails-deep#3`; 21 high rows rank strictly below it | exact, to the row |
| convergence E5/E6/E23/E24 in both addenda | E5 at `READ_ESTATE...md:53`; E23 at `:90` (1.3, same r05#3 cut) and `MICKEY17...md:98`; E24 at `:268` and `:99`; E6 named in the carried list `READ_ESTATE...md:401` | exact |

Note: the lens's move text arrived truncated mid-sentence in my relay ("print tier-1 yes/no and tier-" cut off); the visible direction (value splits at `:154-166`) is executable against data my walk proved is on disk, with Addition B's caveat below.

## What the lens missed (additions, each measured this sitting)

### A. The dual-written master fold has ALREADY diverged 414 bytes on the run-0 burn, with no equality gate anywhere

Evidence (this sitting): `corpus/steal/MASTER_MICKEY17_V2.md` = 43,601 bytes, mtime Oct 4 04:40; the published workspace copy `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_MICKEY17_V2.md` = 43,187 bytes, mtime Oct 4 01:30; not identical. The corpus copy alone carries the enriched a03#5 refire-count row naming its instrument and receipt (`watch/inbox/go_wave_20261004/tavern_refresh.md`); the workspace copy, the one `artifact.file("fold", ...)` publishes from (`mickey17-v2.dwf.ts:355`), holds the pre-enrichment prose. The filer phase verifies existence non-zero only (`:349-353`); the repairer's "fix both copies" instruction (`:337-341`) is prose, unenforced. The workspace dir also shows the manual salvage pattern this forces: `MASTER_MICKEY17_V2_20260924.md`, `_20260925.md` hand-copied beside the fixed-name file that each burn overwrites.
Falsifier: a byte-equality check or single-source write in any of the five skeleton copies; none exists (full read of the saved runner; grep of the drafts).
Move: in the parameterized engine kill the dual write (corpus/steal is the single source, publish from it), or add one byte-compare line to the filer verification. ~5 min. This is the cheapest amendment that prevents a silent stale publish.

### B. The tier-1 persist contract is unenforced and key names drift: the lens's fix pattern, applied to tier-1, would silently lose 15 of 60 verdicts

Evidence (this sitting): the instruction pins a typed shape (`read-the-estate.dwf.ts:149-156`: "Return the typed CheckFile ... Write the CheckFile as JSON"), but 3 of 12 checks files in `2026-10-04-0` carry NO `supports` key: `r02-nightburn-unread` and `r12-rollup` put their tier-1 verdicts under `checks`, `r07-links-register` under `entries`. The 60 tier-1 verdicts ride three key names (supports 45 + checks 10 + entries 5). The fold survives only by accident (`:158-160` counts every list-valued key); the addendum documents the drift (`READ_ESTATE...md` 1.1) but no instrument enforces the shape. Consequence: any fix that reads a specific key (the natural tier-2-style amendment) drops the 15 verdicts under the invented keys without any error.
Falsifier: a schema validator in the fold or the workflow gate; none (full read of both).
Move: the F1/F3 fold edit should census verdict VALUES across all list-valued keys (my one-pass walk recovered 48/12/7/5), and `supportsAsk` should name the exact key and forbid extras. ~10 min on top of the lens's edit.

### C. The in-flight exec archive is truncation-laundering-ready: the fold would print `fired: 8 / missing: 0` on a possibly-dead run

Evidence (this sitting, 05:11 EDT): `runs/2026-10-05-exec/lanes` holds 8 lane files / 40 rows / 7 checks / 0 `deep_tier2` arrays, no `FOLD_SECTIONS.md`, no `corpus/steal/MASTER_EXECUTE_REGISTER.md`; newest write `e06-fidelity-audit.json` at 02:38:45, 2.5h silent. The fold's casualty header would compute `fired = a.fired or n_files` (`tools/mickey17_v2_fold.py:120`) and `missing = fired - n_files` (`:125`) = 0 by construction, laundering a truncation into a clean header (the E22 class, now with a live case). Run liveness is NOT resolvable estate-side: the fire journal file `.zcode/workflow-runs/dwfrun-e9656e14-64ef-49da-bd78-91497aee5d34.mjs` is a pre-launch generated snapshot (its own header: "Generated by @zcode/dynamic-workflow-runtime before every launch; safe to delete once the run has settled") embedding the lowered payload, no status inside, and workflow-run introspection is unavailable in this session. Re-verified absence: 0 of 6 run dirs hold any manifest or journal (top levels carry only `FOLD_SECTIONS.md`, `lanes`, and one `verdict.json` in `gauntlet_w4`).
Falsifier: a manifest in any run dir, or the run settling with all 12 lanes and a clean fold; neither exists yet.
Move: fold refuses to run on an archive with no phase-0 manifest declaring intended lane count (fold straight into the lens's 90-min parameterization amendment, which already writes the manifest).

## Blind spots adjudicated

- Not executing the fold script: correct call, it writes `FOLD_SECTIONS.md` in place (`:227-228`); every fold-defect claim re-derived here read-only and byte-confirmed. The OWED stands.
- Master folds not read in full: consistent with engines-not-content scope; my targeted reads (workspace copies, corpus/steal listing) surfaced Addition A without needing full reads.
- `.zcode/workflow-runs` not inspected: I inspected it; it holds per-run pre-launch script snapshots (12+ recent `.mjs` files), not run status. The three dwfrun ids map to files with mtimes matching the three burns (Oct 3 22:21, Oct 4 17:42, Oct 5 00:39). It cannot settle the in-flight question (Addition C).
- Draft-vs-saved divergence counts "include the lane tables, approximate": honest; measured third pair is 255, divergence fraction is if anything understated.
- In-flight tier-2 state "7 checks files with 0 deep_tier2": still true at my read moment (7 checks / 0 deep_tier2), plus 8 lane files now on disk; final shape still OWED.
- "No manifest/journal in any run dir" scoped absence: re-verified, instrument and scope named, stands.

## Checks run this sitting (commands, outcomes)

- `wc -l` five skeleton copies: 397/387/359/380/397. `cmp`: gap-analysis.dwf.ts IDENTICAL to Gap-analysis-evening.dwf.ts. `diff` pairs: 179 / 220 / 255 changed lines.
- grep -n WSOUT/FOLD_SH/RUNSLUG/MASTER_/deep_tier2 across the three drafts: all four load-bearing cites exact.
- repo-venv python JSON walk over all 89 checks files in all five run archives (counts, top-level keys, deep_tier2 verdict splits, unconfirmed-key presence): outputs quoted in F1/F3/Addition C.
- repo-venv python rank walk on 2026-10-04-0: 34 high rows, rank-13 = r05-trails-deep#3, 21 below.
- grep REGISTRY.jsonl: rows 62/65/85/86 with digests and timestamps quoted in F2.
- Reads: full `tools/mickey17_v2_fold.py`; full `.zcode/workflows/mickey17-v2.dwf.ts`; both archived FOLD_SECTIONS.md; both addenda sections 1.1-1.4; `fold_run.sh`; workspace listing; fire journal head; master-copy byte-diff (43,601 vs 43,187, divergence shown).
- Not run: `tools/mickey17_v2_fold.py` itself (would mutate archives); `ListWorkflowRuns` (capability unavailable in this nested session); the 4,358-test suite (out of scope for this pass).

## Bottom line

All three findings hold with evidence intact: F1 confirmed and extended (0 of 89 files, not 19), F2 confirmed with one clause corrected (burn 1 fired from the saved `gap-analysis.dwf.ts`; a saved newest-generation copy already existed and was bypassed, which is stronger evidence for parameterize-once), F3 confirmed to the row (r05#3, 21 below, 48/12/7/5 nowhere computed). The amendment table gains three rows the lens missed: kill or gate the dual master write (A, ~5 min), census verdict values across ALL list keys and pin the tier-1 key name (B, ~10 min), manifest-precondition on the fold (C, folded into the parameterization). The F1 move's `[:60]` matcher must become a six-word-prefix match before coding.
