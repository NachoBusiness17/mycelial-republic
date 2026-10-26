# GRAVE 01: queue/handoff/HANDOFF-2026-09-16-index-foldback.json

- **Filed:** 2026-09-29 by lane grave-supersede (division C, GRAVEDIGGER, ball 20260929)
- **Classification:** DONE-ELSEWHERE (canonical label; machine row watch/inbox/ball2/graves/grave-supersede.jsonl)
- **Buried entry:** `queue/handoff/HANDOFF-2026-09-16-index-foldback.json` (handoff.v1, owner zcode, assignee hermes, T1-local)
- **Nothing was deleted, moved, or edited. Deletions are operator-gated.**

## What justifies the burial

The handoff's own `closure` block records the work landing elsewhere:
closed 2026-09-26T03:37:50Z by `gala-lane-b5-index-foldback`, verdict
"MET-WITH-DRIFT", evidence `watch/inbox/gala_20260925/w2/lanes/b5-index-foldback.check.txt`
(142,913 bytes, verified on disk this window). The fold deliverable landed:
INDEX.json grew 140 items (2026-09-16 baseline) to 730 at fold time.

Note: "MET-WITH-DRIFT" is the b5 verdict string, not a canonical grave label;
this grave's canonical label is DONE-ELSEWHERE (the work landed outside the entry).

## Successor surfaces (resolving pointers)

- `watch/inbox/INDEX.json` - the folded index, now 1,943 items (counted this window)
- `watch/inbox/index_events.jsonl` - the event register, now 6,557 non-empty rows (3 legacy Sep-1 rows carry `"seq":NEXT` placeholders and fail JSON parse; pre-existing damage, recorded as-is)
- `watch/inbox/gala_20260925/w2/lanes/b5_validate_raw.json` - raw validate output of the fold
- `watch/inbox/wave_20260916/receipts/H1_validate_baseline_20260916.json` - baseline of record

## Open work NOT buried

The closure's drift note ("next fold pass owns the 26 hash mismatches + 197
unindexed") is live work owned by future fold passes. This grave retires the
queue ENTRY, not that debt.
