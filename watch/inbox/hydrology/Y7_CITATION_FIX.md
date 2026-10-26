# Y7 -- FINAL_PIECE tiered-delegation citation fix (2026-09-29)

Batch 2, lane 7/12. File owned: `watch/inbox/mountain_climb_ractor_20260929/FINAL_PIECE.md`. N6's finding: the tiered-delegation claim was the fabrication risk (unattributed external-research claim). No commit.

## What was found

The essay's "GPS is the keystone, honestly" section opened with: "The best
2026 result on tiered delegation says so with its own ablation: a system
where a small scout produces a sandbox-verified handoff beat the best
single model at a fifth of the cost per solve, and when the researchers
removed the router, the score did not move." No source named anywhere.
No RRSI-class claim appears in the essay itself (RRSI lives only in the
source receipt).

## Check against bytes

Every element of the claim resolves to real files:

- `watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`
  item 3: "Scrouting/SuperScout (arXiv:2608.04804). A 7B scout produces a
  SANDBOX-VERIFIED handoff (false claims stripped), then a router dispatches
  to frontier fixers: 159/266 vs 158/266 for the best single model on
  SWE-bench Pro at ~1/5 cost per solve. And its own ablation ... a
  no-router ablation TIES the routed system."
- DIGEST.md row 19 carries the same numbers, trace tag S5 (the receipt).

Mapping: small scout = 7B scout; sandbox-verified handoff = verbatim; a
fifth of the cost per solve = ~1/5 cost per solve; score did not move =
no-router ablation TIES (159/266 vs 158/266 backs "beat the best single
model"). No fabrication: the sentence was true but unattributed.

## What was done (option a, fix not cut)

1. Citation added inline, replacing "on tiered delegation says so" with
   "on tiered delegation (SuperScout, arXiv:2608.04804;
   DELEGATION_RESEARCH_20260929) says so". Nothing cut.
2. Byte-check line updated from words=1197 to words=1200 (still inside the
   1,000 to 1,200 target; emdash still 0). Instrument: whitespace
   word-split + U+2014 char scan, whole file before the correction block
   was appended, re-run after the edit: words=1200 emdash=0.
3. Dated CORRECTION note appended to FINAL_PIECE.md naming the check, the
   sources, and the count update.

## Verdict

Claim was byte-backed; the defect was the missing citation, now anchored to
both the banked receipt and the arXiv paper it cites. Lane closed.
