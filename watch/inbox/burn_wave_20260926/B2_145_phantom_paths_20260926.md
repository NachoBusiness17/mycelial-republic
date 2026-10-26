# B2-145 absolute-path phantom items (2026-09-26)

## Verdict

LANDED. All 5 INDEX items registered under the absolute host root C:/Users/foste/.../watch/inbox/ are invalidated in the event log and their content now lives under bare inbox paths: RIDE_FAMILY_VERDICTS_20260922.md (RECEIPT), DIRECTIVE_WATCHERS_20260926.md (DIRECTIVE), RECAP_7D_20260926.md (BRIEF), ESSENTIALS_RESTORE.md (DOCTRINE), burn_wave_20260926/QUEUE.md (BOARD). The fold is clean of C:/ paths. Four of the five already had bare active siblings (last-register-wins refreshed their shas and classes); QUEUE.md existed only as a phantom and is now registered bare at current bytes.

## Evidence with file:line quotes

- Pre-fix watch/inbox/INDEX.json lines 4220, 4292, 4298, 4304, 5870 each carry "path": "C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/<name>". Cause: scripts/index_fold_host.mjs:76-81 normInboxFile strips board|app/inbox and repeated inbox/ prefixes but never the absolute host root, while OUTSIDE_RE (:82) only matches repo-root segments, so a C:/ head folds as an inbox item.
- Mint events in watch/inbox/index_events.jsonl: :1376 d05-rides-r2 register (stuck-float64 seq literal); :2542, :2786, :2788 md-record-seal autoseal registers (writer-contract fix 2026-09-26); QUEUE.md was minted as a phantom TWICE, :2784 (md-record-seal) and :3053 drift-patrol-cron with a double prefix: "file":"/board/inbox/C:/Users/..." (both normalize to the same phantom).
- Pre-fix verify from watch/inbox: "967 hash-clean, 5 mismatched, 0 missing (of 972 active items)" including "HASH MISMATCH: C:/Users/.../burn_wave_20260926/QUEUE.md actual FBF4392DEEE365DE8... expected F230CB5D86E17BCC..." (QUEUE evolved after its 12:03Z refresh). The other 4 phantoms hash-matched only because existsSync resolves absolute paths on Windows, which is exactly why they duped bare rows invisibly.

## Work done

Read all 5 target files in full and classified each against the INDEX class census before re-registering. Captured the before-state verify above. As INDEX_WRITER=zcode-b2-145-burn-20260926 from watch/inbox cwd: 5x invalidate on the exact absolute strings (seqs 1789823567015749380-384), 4x bare add (seqs 385-388), 1x bare add for QUEUE.md after its self-feed content settled (seq 389). Post-QUEUE verify: "964 hash-clean, 4 mismatched, 0 missing (of 968 active items)"; the QUEUE phantom mismatch is gone. Concurrent lanes then landed 6 more registrations (seqs 390-394) and re-appended self-feeds to QUEUE.md, so the final fold reads 974 active and the QUEUE bare row is sha-stale again within minutes: living-file proof for B2-156. Self-fed B2-156/B2-157, renumbered from B2-150/151 after concurrent lanes claimed 150-155 mid-lane (fix script B2_145_renumber.py). The 4 remaining mismatches (REJECTION_TAXONOMY_20260917.md, BURN_JUDGE_LANE_BUILD_20260925.md, phone_relay_log.jsonl, LINKS.jsonl) are pre-existing stale-sha bare rows owned by the B2-41 sweep, untouched here.

## Falsifier

This is a busy burn night, so the falsifier is invariant-shaped, not count-shaped: fold INDEX.json and (1) items with a path starting C:/ must number 0 (the only allowed C:/Users hit is the derivations.source line naming the events file, a script constant), (2) all 6 rows (5 bare re-registers plus this receipt) must be active with classes RECEIPT/DIRECTIVE/BRIEF/DOCTRINE/BOARD/RECEIPT, (3) the verify mismatch list must name none of those 6 paths except QUEUE.md living-staleness from later self-feeds (registered sha 768798D4CD7E went stale the same way, never the old F230 phantom sha). Resurrection of any absolute-path item, or a dropped bare row, falsifies this receipt.

## Bibliography closed

watch/inbox/INDEX.json pre-fix lines (4220, 4292, 4298, 4304, 5870; bare rows 488, 5234, 5684, 5690); watch/inbox/index_events.jsonl (1376, 2542, 2784-2789, 3053; new seqs 380-389); scripts/index_fold_host.mjs (44, 76-82, 169-194, 338-386); watch/inbox/burn_wave_20260926/B2_50_missing_triage_20260926.md; watch/inbox/burn_wave_20260926/QUEUE.md B2-145 row; watch/inbox/burn_wave_20260926/B2_145_probe.py, B2_145_ledger_queue.py, B2_145_renumber.py; the 5 target files read in full.
