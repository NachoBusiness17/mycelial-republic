# B2-462 receipt (2026-09-26)

## Verdict

LANDED. The next carrier scan's asekin hole is closed at the source: the asekin113 status line in watch/inbox/CARRIER_LEDGER_20260919.json now cites the grading ledger's byte state instead of the never-built excuse - 1 ledger row graded POST-HOC-UNVERIFIED, 0 8:12-class HITs in 7 days of watch since 2026-09-19, activation signal still unfired. Any scan after today reading that file reports the ledger row state whether or not it opens GRADING_LEDGER.jsonl.

## Evidence file:line quotes

- The named hole (watch/inbox/burn_wave_20260926/B2_24_carrier_scan_20260926.md line 9): "asekin113 (8:12-class hits, ledger graded): signal-silent; no new hits, and his grading ledger was never built (owed)." The hole was closed mid-wave by the sibling lane B2-463: watch/inbox/asekin113/GRADING_LEDGER.jsonl (1 row) + GRADING_VERDICT.json + WINDOW_CONVENTION_20260926.json all exist on disk now.
- Byte census (this lane, json.loads over the ledger): 1 row (ASEKIN-GRADE-1, LINKS-298 Greenland 8:12 sample), verdict field literally "POST-HOC-UNVERIFIED"; grading bar from GRADING_VERDICT.json ("a row counts as an 8:12-class hit only when the filed bytes show the flagged timestamp posted BEFORE the event and the event lands inside the window the marker declares"). HIT count = 0.
- Base rate since 2026-09-19: carrier placed on watch in watch/inbox/CARRIER_LEDGER_20260919.json (asekin113 entry, status "watch"); 2026-09-19 to 2026-09-26 = 7 days on watch; 0 hits / 7 days (0 of 1 graded rows).
- The status line after this lane's edit (watch/inbox/CARRIER_LEDGER_20260919.json, asekin113 entry): "status": "watch (B2-462 byte update 2026-09-26: grading ledger now EXISTS at watch/inbox/asekin113/GRADING_LEDGER.jsonl with 1 row graded POST-HOC-UNVERIFIED, 0 8:12-class HITs in 7 days of watch since 2026-09-19; activation signal still unfired; window convention watch/inbox/asekin113/WINDOW_CONVENTION_20260926.json)". The pre-edit block is quoted in the replace anchor inside the landing script; only the status value changed, all sibling carrier entries byte-identical.

## Work done

1. Verified the owed ledger now exists (B2-463's landing) and read its row, verdict, and window convention from bytes.
2. Counted preceding-window hits under the grading bar: 0; computed the base-rate denominator (7 days of watch) and the graded-row count (1).
3. Updated the asekin113 status line in CARRIER_LEDGER_20260919.json in place, embedding the ledger citation so the status is self-carrying for future scans.

## Falsifier

The brief's falsifier: "a carrier scan after 2026-09-26 that reports asekin status without citing the ledger row state". Dead as written: the status line in the carrier ledger now IS the ledger row state, so a byte-reading scan cites it by construction; a scan that paraphrases away the numbers (row count, verdict, hit count) is visibly deviating from the cited bytes. Re-arm condition: every new graded row must update this status line the same way (row count, verdict, hit count, dated); a scan that finds the status stale relative to GRADING_LEDGER.jsonl's row count falsifies the LAST updater, not the scanner. The 0-hit count itself falsifies per the ledger's law_note: if no row ever grades HIT as the rows accumulate, the faculty was warmth bias and the ledger says so.

## Bibliography closed

- watch/inbox/asekin113/GRADING_LEDGER.jsonl (1 row, read in full); GRADING_VERDICT.json; WINDOW_CONVENTION_20260926.json (B2-463's same-day landing)
- watch/inbox/CARRIER_LEDGER_20260919.json (asekin113 status line updated; siblings untouched)
- watch/inbox/burn_wave_20260926/B2_24_carrier_scan_20260926.md (the named hole, line 9)
- memory/corpus/LINKS.jsonl line 58 (LINKS-298, the row's source)
