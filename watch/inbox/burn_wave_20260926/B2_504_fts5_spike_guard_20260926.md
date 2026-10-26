# B2-504 receipt: B2_22_fts5_spike.py re-run guard (2026-09-26)

## Verdict

LANDED, both fix arms applied and the falsifier inverted. The spike's baseline arm now FORCES the scan path in-process (tool.FTS_DB pointed at an absent path, the B2-102 A/B pattern, restored in a finally block), so post-wiring runs still measure the scan arm; the spike's classification reads the ACTUAL engine each arm reported (res.engine + index_state) instead of the hardcoded "scan" label, and the full-scan class is computed on the measured rows_scanned. Fresh post-wiring A/B numbers over the live 489,548-row catalog: forced-scan full-scan class = 4 queries (garden, referee, ruins_go, adventure_2d6) at median 3,336.0 ms / best 3,282.7 ms versus the FTS5 arm's 0.185 ms median / 0.16 ms best on the same queries (all-10 max 6.75 ms) - FTS5 is ~18,000x faster on the same-query class. The brief's falsifier ("the unfixed spike prints full_scan_queries [] with full_scan_median_ms null") is INVERTED: the fixed spike prints 4 named full-scan queries with a real median.

## Evidence file:line quotes

- Brief (QUEUE.md B2-504 row): "baseline arm line 155 calls the production tool with no scan force, line 159 hardcodes engine=scan, line 196 classifies the full-scan class by rows_scanned >= rows_indexed, a predicate only true under pre-wiring lines-read semantics" and "falsifier: the unfixed spike prints full_scan_queries [] with full_scan_median_ms null".
- B2_22_fts5_spike.py (post-patch, baseline arm): `fts_db_saved = tool.FTS_DB` / `tool.FTS_DB = tool.Path(..., "__absent_forced_scan__.sqlite")` / `assert not tool.FTS_DB.exists()` inside `try:` with `finally: tool.FTS_DB = fts_db_saved`; each entry records `"engine": engine, "index_state": res.get("index_state")` from the production tool's own result dict (no hardcoded label).
- tools/corpus.py:149: `if not FTS_DB.exists():` - the freshness gate that the absent-path injection deterministically drives to "absent", forcing the JSONL scan fallback (the injection point the B2-102 A/B pattern names).
- Fresh results (watch/inbox/burn_wave_20260926/B2_22_fts5_results.json, written this run): scan arm rows - verkle 13,477 rows / 82.5 ms median, hermes 77,653 / 566.8, corpus 14,872 / 93.6, falsifier 17,824 / 109.4, grounding 12,316 / 74.2, garden 489,548 / 3,303.3, referee 489,548 / 3,402.6, ruins_go 489,548 / 3,308.5, adventure_2d6 489,548 / 3,363.5, qdrop 453,407 / 3,176.9, all engine "scan" index_state "absent"; classes: full_scan_queries [garden, referee, ruins_go, adventure_2d6], full_scan_median_ms 3336.0, full_scan_best_ms 3282.7, fts5_same_queries_median_ms 0.185, fts5_same_queries_best_ms 0.16, fts5_all10_max_ms 6.75.

## Work done

1. Applied the forced-scan arm: the baseline section now points the loaded module's FTS_DB at an absent sibling path (creating nothing), asserting absence, restoring the original in finally - the production tool's own _fts_state then reports absent and corpus_search falls back to the JSONL scan, so the baseline measures the scan arm even post-wiring.
2. Applied the honest-classification arm: entries carry the tool-reported engine and index_state; the classes computation requires engine == "scan" and uses the measured rows_scanned against rows_indexed (a row with None rows_scanned can no longer silently join a class).
3. Re-ran the spike end-to-end for fresh post-wiring A/B numbers (RESULTS rewritten at B2_22_fts5_results.json); py_compile clean; one mid-fix repair (FTS_DB needed a Path, not a str - the tool's freshness gate calls .exists()) caught by the first run's AttributeError and fixed before results were accepted.
4. Note the measured shape: the wide queries (verkle/hermes/corpus/falsifier/grounding) early-break under limit=20 even on scan, which is why only the 4 narrow/zero queries walk all 489,548 rows; qdrop (zero hits) walks 453,407 - the rescan's honest numbers, matching the original class intent.

## Falsifier

The brief's falsifier is now permanently inverted and pinned: a rerun of the spike prints full_scan_queries as a non-empty list with a real full_scan_median_ms (4 queries / 3,336.0 ms today). This guard dies if: (a) the baseline arm ever again reports an engine other than "scan" (the absent-path injection broke, meaning corpus.py changed its fallback contract - files against this receipt and tools/corpus.py _fts_state); (b) a rerun's rows_scanned stops matching the catalog row count for the full-scan class (489,548 today; catalog growth must move it in lockstep); (c) the classes computation regresses to a hardcoded engine label (grep the spike for '"engine": "scan"' - post-fix the only engine strings come from the tool's response).

## Bibliography closed

All read this lane: watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py (QUERIES roster lines 35-46, baseline arm 150-172, FTS arm 174-198, classes 199-209, pre + post patch), tools/corpus.py (_fts_state 144-172, _search_fts fallback contract, FTS_DB module global), watch/inbox/burn_wave_20260926/B2_22_fts5_results.json (rewritten this run), watch/inbox/burn_wave_20260926/B2_464_caller_census_20260926.md (Falsifier 1, via queue pointer), QUEUE.md B2-504 row.
