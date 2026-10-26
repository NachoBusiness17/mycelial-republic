# B2-471 Fold B2-178 caption-structure classes into a media census

## Verdict

LANDED. The one-page census is filed at watch/inbox/burn_wave_20260926/B2_178_caption_census.md: 1,234 enrich rows on file join to 1,195 verdict rows (39 raw-payload parse failures named, 0 ledger join failures, 0 duplicate item rows); class counts (link-preview leading), archive_worthy split by ledger status (have 1,074 / have-recovered 106 / metadata-only 15 rows split archive vs not-archive), lane distribution, and the cross-lane disagreement section (rows scored by 2+ lanes: 0 - the enrichment lanes did not overlap on any msg_id, so class disagreements 0 and archive_worthy disagreements 0). The falsifier holds both arms: every census count derives from the 1,195 joined rows (class counts sum 1,195 = parsed), and caption text quoted in the census is 0 (counts, class names, cites and msg_ids only - the metadata law).

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_178_caption_census.md (the deliverable): "enrich rows on file: 1234", "raw payload parse failures: 39", "joined verdict rows (the denominator for every count below): 1195", "class counts sum 1195 == parsed 1195", "caption text quoted in this census: 0".
- The join key is the runner's own assignment (watch/inbox/burn_wave_20260926/B2_178_freelane_runner.py:215 `"id": "ce-%04d" % n_cap` with n_cap the 1-based CAPTION_LEDGER row number), so ce-NNNN maps to ledger row N deterministically; 0 join failures over 1,234 rows.
- Split by status read from the ledger rows themselves: have 1,074 / have-recovered 106 / metadata-only 15.
- Disagreement section: "rows scored by 2+ lanes: 0; class disagreements: 0; archive_worthy disagreements: 0" (each scored row has exactly one lane: openrouter-k2, nous-hermes, groq, together per the lane distribution).

## Work done

1. Read the enrich file schema (item/lane/raw), the runner's ce-NNNN assignment, and the ledger (2,726 rows).
2. Built the join (ce id -> ledger row), parsed the raw payloads (39 unparseable named, not hidden), computed class counts, the status split, and cross-lane disagreements.
3. Wrote the census with the falsifier check inline (class sum == parsed; caption text 0).
4. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "any census count that does not equal the join output row count, or any caption text quoted in the census (metadata law, the census is counts only)." Checked: class counts sum 1,195 equals the joined denominator 1,195; the file contains no caption text (grep the census for any ledger caption prefix returns nothing - the only free strings are class names, lanes, statuses, cites and msg_ids). The 39 unparseable raw rows are named as a count, never silently dropped. Reproduction: rerun the join; any delta between a census number and the join output inverts the receipt.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_178_out_caption_enrich.jsonl (1,234 rows)
- watch/inbox/CAPTION_LEDGER_20260926.jsonl (2,726 rows, join target)
- watch/inbox/burn_wave_20260926/B2_178_freelane_runner.py (the ce-NNNN assignment law)
- watch/inbox/burn_wave_20260926/B2_178_caption_census.md (the deliverable)
- watch/inbox/burn_wave_20260926/B2_12_caption_ledger_20260926.md (the ledger's own receipt)
- Nothing owed (the 39 unparseable rows are named; re-scoring them is the enrichment lanes' next-pass decision, not this census's).
