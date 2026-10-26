# B2-118 taxonomy 52 percent first-pass recount

## Verdict

ERRATUM FILED. The "~52% first-pass rate" line (REJECTION_TAXONOMY_20260917.md:24) is NOT reproducible at the frozen cutoff (git 3d12289f9). Its numerator "17 promoted" is a stale same-day count: the cutoff bytes hold 24 promoted_* receipt files and 19 unique promoted names, and state.json at the cutoff carries promoted = 19, matching the same taxonomy file's own line 30 ("the 19 promoted levels"). The denominator "16 transport-clean rejections" IS confirmed from committed proposals.jsonl (12 "KeyError: 'choices'" + 4 explicit "200_error_body" = 16 of the 41 FAIL rows). The 17-vs-19 reconciliation the brief called unreconciled is resolved: 19 is canonical everywhere; 17 is the only tally true mid-day (exactly 17 promoted receipts have mtimes before 17:23 -0400 on 09-17; the 18th landed 19:11:03 and six more before the 23:56:48 commit). Corrected figure: 19/(19+16) = 54.3%, so "~52%" reads "~54%"; the qualitative "about half the time" survives.

## Evidence file:line quotes

- watch/inbox/REJECTION_TAXONOMY_20260917.md:24 "half the time (17 promoted / 16 transport-clean rejections = ~52% first-pass rate)." and :30 "not just the 19 promoted levels, but the 39 transport failures" (both lines in the single commit 3d12289f9; the file is internally inconsistent).
- `git ls-tree -r 3d12289f9 --name-only | grep promoted_ | wc -l` = 24; dedupe of the `_g1`/`_g2` suffix yields 19 unique names (5 names carry both generations: D-L03-collapse, P-scale-finale, P-sentry-weave, PZ-combo-parity-door, PZ-combo-push-descent).
- `git show 3d12289f9:.../state.json` keys `promoted` = `19` (int), `rejected` = `2`.
- Committed proposals.jsonl: 71 rows, verdict PASS 30 / FAIL 41; FAIL rows with `error` = "KeyError: 'choices'": 12; rows carrying "200_error_body": 4; sum 16 (field scan: the error text lives in the `error` and `gate` fields, not `answer`).
- Disk mtimes of the receipts (working tree never re-cloned): exactly 17 promoted_*.json files have mtime before 2026-09-17 17:23 -0400; 18th `promoted_BOSS-twin-v2_g2.json` at 19:11:03; last `promoted_PZ-combo-push-descent_g1.json` at 23:51:33, five minutes before the commit.
- B2-33's frozen census (watch/inbox/burn_wave_20260926/B2_33_rejection_recount_20260926.md) independently froze the FAIL denominator at 41 with 200-error-body 16; this lane re-derived the 16 from committed bytes rather than trusting the report.

## Work done

1. Read the pointer receipt B2_33_rejection_recount_20260926.md in full for the frozen-cutoff framing.
2. Recounted the numerator at the cutoff from git bytes: 24 promoted receipt files, 19 unique names, state.json promoted 19, 30 PASS rows, 19 unique PASS briefs. No cutoff tally yields 17.
3. Tested and confirmed the stale-draft hypothesis: the receipt mtimes give exactly 17 files before 17:23 on 09-17, the only 17-tally in any bytes.
4. Recounted the denominator independently from committed proposals.jsonl: 16 transport-clean 200-error-body FAIL rows.
5. Recomputed the rate under the taxonomy's own construction: 19/(19+16) = 54.3 percent.
6. Appended a dated second ERRATUM to REJECTION_TAXONOMY_20260917.md (append-only, after B2-33's erratum; no existing line rewritten, 0 em-dashes added).
7. Filed this receipt, appended the LEDGER row, and annotated the QUEUE row.

## Falsifier

The brief's falsifier is the recount itself: "confirm or erratum the ~52 percent figure". Executed: the figure does not reproduce at the frozen cutoff (numerator 17 unsupported, true value 19), and the erratum branch was taken with the corrected 54.3 percent figure and the mid-day 17-tally named. Reproduction: `git show 3d12289f9:watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl` and count verdict PASS (30) and FAIL error classes (12 KeyError + 4 200_error_body); `git ls-tree -r 3d12289f9 --name-only | grep -c promoted_` (24, 19 after dedupe); `git show 3d12289f9:.../state.json` promoted field (19). Any different tally inverts this receipt.

## Bibliography closed

- watch/inbox/REJECTION_TAXONOMY_20260917.md (read in full; second erratum appended)
- watch/inbox/burn_wave_20260926/B2_33_rejection_recount_20260926.md (read in full; frozen cutoff + 41 FAIL census reused, 16 re-derived independently)
- git 3d12289f9: watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl (71 rows parsed), state.json (promoted 19), 24 promoted receipt paths
- Live receipt dir mtimes (watch/inbox/union_fullsend_20260917/build_lane/receipts/) for the mid-day 17-tally
- Nothing owed beyond this receipt.
