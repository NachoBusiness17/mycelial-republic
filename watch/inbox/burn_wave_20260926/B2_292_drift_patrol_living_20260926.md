# B2-292 receipt: drift-patrol living adoption (2026-09-26)

## Verdict

PARTIAL: measured and provisioned, the switch itself OWED because the writer it would change does not exist on disk. The patrol's whole-file refresh disease is quantified on bytes (drift-patrol-cron registered /board/inbox/LINKS.jsonl 11 times, not just the 4-in-2-hours the brief cited), the living-row universe the law applies to is now a dated artifact (15 rows, B2_292_living_rows_20260926.json), and the adoption door is confirmed present in the fold host (scripts/index_fold_host.mjs add --living / --living-open, verify counts living-ok/living-open). But the patrol that performs the refreshes is writer drift-patrol-cron and NO script on disk carries that writer (grep of scripts/ tools/ mag/ finds only fold-host comments), so the hash-refresh step cannot be edited until the cron hunt (this board's B2-211, also in this lane's slice) finds the mint source or files its absence. Filing the switch as owed is the no-fabrication move; the receipt pins the row list and the law point so the future fix is a one-line flag change against a named target.

## Evidence file:line quotes

- watch/inbox/LIVING_HASH_LAW_20260926.md:72-74 (law point 6): "No other writer changes: md_record_seal.py autoseal registers stay whole-file (one-off receipts are not living); the drift patrol must stop daily whole-file refreshes of living rows and may use this law instead."
- Measured 2026-09-26 over watch/inbox/index_events.jsonl: writer drift-patrol-cron register counts: /board/inbox/LINKS.jsonl 11, REPLUNA_RACTOR_20260916.md 4, RASHOMON_SURFACE_ELEPHANT_20260914.md 3, QUIET_RADAR_20260921.md 3, MD_RECORD_AUDIT.json 3, plus 6 more files at 2 each (the brief's "4 refresh registers in about 2 hours" for LINKS.jsonl understates the full-day count).
- scripts/index_fold_host.mjs:690-694: "--living seals (sha256, size) over the file's first size bytes (append-only originals); --living-open declares an edit-shaped board with no byte seal"; :578,627 verify already reports living-ok / living-open / living-unverified classes. The adoption door exists; the caller does not.
- Living-flag universe (this lane's artifact): 15 rows including LINKS.jsonl, burn_wave_20260926/QUEUE.md, mimo_watch.jsonl, quote_hitrate.jsonl, watch/inbox/DATED_METERS.jsonl, verb_trace.jsonl, endpoint_news/endpoint_news.jsonl, union_fullsend build-lane ledgers, FULL_SCAN_REPORT_20260923.md.
- Pointer briefs cited: drift-patrol-cron batch events seqs 1789823567015749449-477 in watch/inbox/index_events.jsonl (line 3028 onward: composed /board/inbox/ paths, writer drift-patrol-cron).

## Work done

1. Quantified the disease on bytes: per-file patrol register counts for the whole 2026-09-26 window (LINKS.jsonl 11 whole-file refreshes; a file the fold holds under a living/open flag).
2. Built watch/inbox/burn_wave_20260926/B2_292_living_rows_20260926.json: the dated register of all 15 living-flagged rows (schema living_row_register.v1, last flag ts per row), so the future patrol switch has its exact target list and the falsifier is greppable.
3. Verified the fold host already implements both living doors and their verify classes, so the switch is purely a caller-side flag change (add --living / --living-open, or an explicit skip-register per row), NOT new machinery.
4. Named the owed arm: edit the patrol's hash-refresh step to consult the living register for its rows; blocked on B2-211 finding the cron (schtasks query returned no drift-patrol task on this host; the writer exists only in event bytes). This receipt does not claim the behavior changed.

## Falsifier

The owed switch becomes decidable when B2-211's cron hunt resolves: (a) if a patrol source is found, the fix is proven when the next daily fire registers each of the 15 living rows exactly once with a living/open seal or an explicit skip event, and zero whole-file refresh registers for those rows appear afterward (grep writer drift-patrol-cron + file LINKS.jsonl must stop growing at 11 for whole-file ops); (b) if the cron is filed absent, the patrol writer is a phantom and this receipt's register artifact becomes the contract for whichever writer inherits the patrol duty; (c) until then, every additional whole-file LINKS.jsonl refresh register past 11 is a fresh count of the disease this receipt pinned.

## Bibliography closed

All read this lane: watch/inbox/LIVING_HASH_LAW_20260926.md (law point 6, implementation contract), watch/inbox/index_events.jsonl (patrol register census, seqs 1789823567015749449+, living/open flags), scripts/index_fold_host.mjs (living doors 690-694, verify classes 578-635, composed-path comments 113/203), tools/md_record_seal.py (autoseal writer exclusion confirmed), QUEUE.md B2-292 and B2-211 rows, B2_292_living_rows_20260926.json (written this lane).
