# B2-179 dogfood meters, lane receipt and byte-verification pass (2026-09-26)

## Verdict

LANDED, verified on bytes, pointer repaired. The dispatcher's brief for this lane names a receipt at watch/inbox/burn_wave_20260926/B2_179_dogfood_meters_20260926.md; the lane's work itself had already landed once at 2026-09-26T18:50:31Z (memory/burns/LEDGER.jsonl row 244) with the meters filing at watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md, and the SW-07 board truncation and repair then dropped the landing pointer from the B2-179 row. This dispatch therefore executed as verification and repair, not refiling: every byte anchor in the original receipt re-verified green (details under Evidence), the meter truth stays owned by the DOGFLOOD filing (renaming or duplicating it would rot the B2-453, B2-454 and B2-455 rows that cite it), and this card is the lane receipt the dispatcher's filename pins. Meter truth carried by the brief, recorded once in the primary filing and not forked here: reading 1, operator screenshot ~13:0xZ (5h window 80 pct used, reset 10:06 out; weekly 55 pct, reset Sep 27; ZCode MCP 100 pct, reset Sep 26; average cache hit rate 97.3 pct); late-afternoon operator follow-up (5.3flash window ~50 pct compute remaining against ~250M witnessed burn tokens); delta lesson: window meters reset and refill, so a point-in-time pct is not a budget and burn rate against window depth is the real denominator; the 97.3 pct cache rate is the receipt that the byte-identical prefix law is the cost engine. The panel percentages and the 250M total are operator-reported readings with no in-repo measurement surface; they are recorded as such and no byte substitute was fabricated.

## Evidence file:line quotes

- watch/inbox/BURN_WAVE_PIN_20260926.md:19 "width 10 clean, 109M tok/h measured, 97.3pct cache hit rate." and :8 "Witnessed subagent tokens through the flash lane: ~95M across 37 reported": both resolve verbatim; the primary receipt's cache-rate corroboration stands.
- watch/inbox/ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md:123 "about production resurrection (GLM-5.3-flash Max, 235K/1M window, 97.3% cache": the same 97.3 figure on an earlier witness, so the number is a stable worldline property, not a one-panel fluke.
- memory/burns/LEDGER.jsonl:244: the 2026-09-26T18:50:31Z B2-179 row, verdict LANDED, landing pointer to DOGFLOOD_METERS_20260926.md: resolves; the append-only ledger was left untouched by this pass except for this pass's own row at the tail.
- watch/inbox/burn_wave_20260926/B2_98_tally_current_wave.json totals block: matched_events 507, network_completed 363, network_failed_events 144 with statusCode_counts {"429": 144}, absorbed_retries 143, terminal_failed_turns 0. One precision note against the original receipt's "all absorbed by retries" sentence: the byte count is 143 absorbed of the 144 rate-limited events, 0 terminal failed turns; the conclusion (the lane absorbed the storm) is unchanged.
- watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md: five fixed sections on disk (Verdict, Evidence, Work done, Falsifier, Bibliography closed); readings marked operator-reported with the no-byte-substitute honesty note.
- watch/inbox/burn_wave_20260926/QUEUE.md B2-179 row: this dispatch's first read showed the row UNCHECKED; a re-read minutes later showed it flipped bare to [x] with no landing pointer (a concurrent writer; the flip-without-pointer state the board repair's note-less recoveries also produce). The work and receipts predate the flip, so the check is earned; the defect this pass fixes is the missing pointer. Self-fed briefs from the original landing verified in place: B2-453 and B2-455 still Open UNCHECKED, B2-454 landed (receipt B2_454_cache_rate_audit_20260926.md, BLOCKED-AT-SOURCE arm: the cacheReadTokens fields are redacted in the day log, no rate computable in-repo).

## Work done

1. Read the brief row and the board law header; found the lane's original landing already on disk and in the ledger; switched this dispatch to verify-and-repair instead of refiling (no double briefs, no forked meter text, no second ledger claim of the same work).
2. Re-verified every byte anchor listed under Evidence by grep and direct JSON reads; all resolve; the 143-vs-144 precision note is recorded here and touches no conclusion.
3. Filed this lane receipt at the dispatcher-named path; the primary meters filing stays DOGFLOOD_METERS_20260926.md.
4. Board edit per the claim law on freshly-read bytes: filed the CLAIM line, ran the B2-343 restore-guard pre-write check (green), appended the landing note with both receipt pointers to the B2-179 row, self-fed 1 new brief UNCHECKED at dynamic highest+1, retired the claim to CLAIMED in the same write.
5. Appended this dispatch's LEDGER row via the repo venv python json.dumps (append-only; the 18:50:31Z row untouched).

## Falsifier

This receipt dies if any of these fails: (a) DOGFLOOD_METERS_20260926.md loses the two-reading structure or the 97.3 cost-engine paragraph; (b) memory/burns/LEDGER.jsonl lacks either the 18:50:31Z B2-179 row or this pass's row; (c) the B2-179 row on QUEUE.md lacks a resolvable receipt pointer after this landing; (d) any quoted line under Evidence fails to resolve by grep; (e) the self-fed brief is checked at birth or double-spends an id. Standing meter caveat unchanged from the primary filing: the four panel percentages and the 250M total have no in-repo measurement surface; the settlement authority is the operator panel, not this receipt.

## Bibliography closed

watch/inbox/burn_wave_20260926/QUEUE.md ; watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md ; watch/inbox/BURN_WAVE_PIN_20260926.md ; watch/inbox/ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md ; watch/inbox/burn_wave_20260926/B2_98_tally_current_wave.json ; watch/inbox/burn_wave_20260926/B2_454_cache_rate_audit_20260926.md ; watch/inbox/burn_wave_20260926/BOARD_REPAIR_INCIDENT_20260926.md ; memory/burns/LEDGER.jsonl.
