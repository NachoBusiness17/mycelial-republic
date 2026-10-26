# GRAVE 19: queue/handoff/VERKLE_RIB.json

- **Filed:** 2026-09-29 by lane grave-supersede (division C, GRAVEDIGGER, ball 20260929)
- **Classification:** FOSSIL (machine row watch/inbox/ball2/graves/grave-supersede.jsonl)
- **Buried entry:** `queue/handoff/VERKLE_RIB.json` (schema verkle_rib.v1, 6,497 knots, dim 8, 2,226,441 bytes, last write 2026-09-02 03:13)
- **Nothing was deleted, moved, or edited. Deletions are operator-gated.**

## What justifies the burial

This is a derived export, not a work order: `mag/verkle_rib.py` line 38 sets
`RIB_OUT = ROOT / "queue" / "handoff" / "VERKLE_RIB.json"` and line 85's
docstring says the module writes the verkle->RIB map there. The rebuild
receipt documents it: `docs/ref/VERKLE_REBUILD_COMPLETION_20260901.md`
line 69, "Verkle -> RIB export | Refreshed after the audit;
`queue/handoff/VERKLE_RIB.json` now contains 6,497 knots".

It is stale: the live chain `memory/biography/verkle_chain.jsonl` is 8,390
knots and its tip moved 2026-09-29T14:42:49Z (minutes before this grave).
The export is 27 days behind its own source and has no reader in tracked
code: `git grep -l VERKLE_RIB` (py/md/json) returns 21 files, and the only
code reference is the writer itself; the other hits are docs and
archaeology. This is the FOSSIL_CENSUS_20260927.md disease (artifact derived
once, consumer cadence moved on), instance shape of census row 2
(aud_files.json) except here a regenerator exists (`mag/verkle_rib.py`) and
simply has not been re-run since 2026-09-02.

## ERRATUM (same window)

This lane's first-pass recursive grep printed empty output and was read as
"zero consumers"; that reading was wrong and is corrected in the check log
(watch/inbox/ball2/graves/grave-supersede.check.txt, ERRATUM section). The
git grep above is the evidence of record.

## Successor surfaces (resolving pointers)

- `memory/biography/verkle_chain.jsonl` - the live knot chain (8,390 knots)
- `memory/biography/verkle_tip.json` - the live tip
- `mag/verkle_rib.py` - the regenerator; re-run it to refresh the export
  if the operator wants the RIB view back

## Operator note

If any operator gate later archives this file, first re-run
`mag/verkle_rib.py` or accept losing the Sep-2 RIB snapshot; this grave
claims no deletion.
