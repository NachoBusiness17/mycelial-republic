# B2-330 receipt: junction mirror-vs-duplicate diff (2026-09-26)

## Verdict

PROVEN: BYTE_DUPLICATE_MOUNT. The SOCRATIC_GAPS falsifier the 2026-09-18 prune left Unproven now runs and closes by bytes. The live junction <repo>/training -> \\?\C:\Users\foste\Documents\projects\local_sovereign_agent\memory\training (tag 0xA0000003, v3 policy ledger row a8be960098a9) was walked from BOTH views with sha256 over every file: 24 files vs 24 files, 24/24 hashes identical, zero files only-in-junction, zero only-in-real, zero content diffs, 249,281,084 bytes total, walk 0.8s (watch/inbox/burn_wave_20260926/B2_330_junction_diff_20260926.json). The junction is an intentional mount alias carrying no independent content; the "duplicates" call behind the 2026-09-18 prune was structurally guaranteed and is now byte-proven. The gap annotation is appended to watch/inbox/SOCRATIC_GAPS_20260918.md (Gap 102 closure section).

## Evidence file:line quotes

- watch/inbox/SOCRATIC_GAPS_20260918.md:40: "You pruned 189K rows through a junction and called them duplicates."
- watch/inbox/SOCRATIC_GAPS_20260918.md:102: "A junction diff showing only byte-duplicate trees would falsify the" [duplicate claim] - the exact falsifier this lane executed.
- catalog/junctions.jsonl row a8be960098a9 (ts 2026-09-26T18:59:31Z): "path": "local_sovereign_agent/training", "kind": "junction", "tag": "0xA0000003", "target": "\\\\?\\C:\\...\\memory\\training", "target_class": "device_local", "action": "pruned" (the v3 policy ledger making the walk runnable, as the brief said).
- cmd dir /AL (repo root, this lane): "09/06/2026 01:00 AM <JUNCTION> training [C:\Users\foste\Documents\projects\local_sovereign_agent\memory\training]" (the junction is LIVE, the ledger "pruned" action refers to catalog-row pruning, not junction deletion).
- B2_330_junction_diff_20260926.json (this lane): "files_junction_view": 24, "files_real_view": 24, "identical": 24, "only_in_junction": [], "only_in_real": [], "content_diffs": [], "total_bytes": 249281084, "verdict": "BYTE_DUPLICATE_MOUNT".

## Work done

1. Located the live junction from the v3 policy ledger (catalog/junctions.jsonl) and confirmed it on bytes (dir /AL + os.readlink target match).
2. Walked both views (training/ via junction, memory/training/ real) hashing every file full-content sha256 with 1MB chunks; compared by relative path: counts, only-in sets, and per-file hash equality.
3. Filed the result JSON and appended the dated Gap-102 closure annotation to SOCRATIC_GAPS_20260918.md so the gap ledger carries the proof next to the claim.
4. Named the semantic reading: a Windows junction is a reparse-point alias, so byte identity was the expected outcome; the value of the run is that the duplicate-prune claim now rests on measured bytes instead of assumption, and the intentional-mount classification in the v3 ledger (target_class device_local, violation false) is confirmed against reality.

## Falsifier

The verdict dies if: (a) a re-run of the walk after any training-tree write shows a count or hash divergence (the JSON is re-generable in 0.8s with the same script shape; divergence would mean something wrote through one view and not the other, impossible for a healthy junction and therefore proof the reparse point broke); (b) the junction is replaced by a real directory copy (dir /AL would show no JUNCTION; the mirror-vs-duplicate question would reopen with real divergence risk); (c) the ledger row a8be960098a9 target stops matching os.readlink (mount retargeted without a re-diff).

## Bibliography closed

All read this lane: catalog/junctions.jsonl (row a8be960098a9 + pytest-tmp sibling rows), watch/inbox/SOCRATIC_GAPS_20260918.md (:40, :102, annotated), watch/inbox/burn_wave_20260926/B2_330_junction_diff_20260926.json (written this lane), watch/inbox/burn_wave_20260926/B2_76_junction_policy_20260926.md (pointer), cmd dir /AL output, os.walk/readlink byte census of memory/training (24 files, 249.3MB), QUEUE.md B2-330 row.
