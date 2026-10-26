# B2-281 Pin the year-first keeper row in check7 (SW-07, 2026-09-26)

## Verdict

LANDED. scripts/the50_t21_q_caption_ledger_verify.py check7 now requires the exact byte-equal year-first keeper row ("7175228", "2041-12-31", "2041 Dec 31", 0.9) through a new B2_281_YEARFIRST_KEEPER constant joined into the keeper union. Real ledger: full verifier PASS, keepers byte-equal 77/77 (was 76/76 + the unpinned row). Falsifier demo executed on a scratch ledger minus the 0.9 row: check6 stays PASS (extractor reproduces the shrunk ledger -- the silent-vanish gap) while check7 FAILs naming gone=[('7175228', '2041-12-31', '2041 Dec 31', 0.9)], RESULT FAIL, exit 1. The demonstrated gap is closed.

## Evidence file:line quotes

- The pinned row on live bytes, watch/inbox/qdrop_export/q_caption_ledger.jsonl:191: `{"id": "7175228", "date": "2041-12-31", "claim": "2041 Dec 31", "confidence": 0.9}` (ledger post sha 72884939492b3a05 per the B2-258 landing).
- The gap, restated in the new constant's comment: "check6 proves ledger-equals-extractor, so a refactor that deletes the YEAR_FIRST loop and regenerates would silently vanish the row from BOTH sides and stay verifier-green (the demonstrated gap)".
- Pre-pin protection was only the scoped spare: `("2041 Dec 31", 0.65, 0.75)` in B2_243_SCOPED_CLAIMS -- it nets the killed twin class but never requires the 0.90 row.
- Falsifier demo transcript (scratch copy, 266 rows): "check6 extractor reproduces ledger: 162 drops re-run, missing rows: PASS none" followed by "check7 guard pin ...: resurgent 0, keepers byte-equal 76/77 FAIL ... gone=[('7175228', '2041-12-31', '2041 Dec 31', 0.9)]" and "RESULT: FAIL - 266 rows"; exit code 1.
- Real ledger after the pin: "check7 guard pin (B2-68/B2-220/B2-219/B2-242/B2-243): resurgent 0, keepers byte-equal 77/77 PASS", "RESULT: PASS - 267 rows".

## Work done

- scripts/the50_t21_q_caption_ledger_verify.py: B2_281_YEARFIRST_KEEPER constant added (byte-for-byte from the landed ledger row, per the B2-259 pin maintenance law with the cause/evidence comment); keeper_pairs and keeper_want unions extended to include it.
- Falsifier demo run against a scratch ledger (no production bytes touched) proving the pin catches the vanish that check6 cannot see; full verifier re-run green on real bytes.

## Falsifier

The brief's falsifier, executed: delete the YEAR_FIRST keeper row (the demo's proxy for deleting the loop and regenerating), run the verifier -- pre-pin it printed RESULT PASS, post-pin it prints check7 FAIL on the missing keeper and exits 1. Reopen if: the demo path (vanished row, green RESULT) reproduces again (would mean the union lost the constant), or the pinned tuple drifts from the ledger bytes without a pin-maintenance audit note.

## Bibliography closed

Read: scripts/the50_t21_q_caption_ledger_verify.py (check7 block, keeper constants, B2-258/B2-259 comments), watch/inbox/qdrop_export/q_caption_ledger.jsonl:191, watch/inbox/burn_wave_20260926/B2_258_yearfirst_20260926.md (referenced via row and comments), live + scratch verifier runs. No external sources.
