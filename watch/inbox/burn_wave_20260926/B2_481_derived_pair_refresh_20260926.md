# B2-481 Derived-pair refresh after the catalog rebuild (SW-07, 2026-09-26)

## Verdict

LANDED. The derived trio is refreshed against the rebuilt 489,548-row map without clobbering B2-22's receipt artifact: the FTS index was rebuilt through a redirected-path build (B2_481_fts_build.py importing B2_22's own build_index/reference_counts/fts_expr byte-for-byte, writing results ONLY to watch/inbox/burn_wave_20260926/B2_481_fts5_results.json), and the three required spot-checks pass: kind=ledger 12,976/12,976 tagged ids present in the FTS map (0 missing), kind=card 1,807/1,807 (0 missing), and the ruins_go freshness join returns 10 hits whose mtimes are 2026-09-21/22 fresh bytes. Falsifier discharged: corpus_stats.total_rows 489,548 == wc -l of catalog.jsonl 489,548.

## Evidence file:line quotes

- QUEUE.md row: "rerunning B2_22_fts5_spike.py as-is would clobber B2_22's receipt artifact via its hardcoded RESULTS path; re-run the tag pass and the FTS build with the results path redirected to a new dated artifact, then spot-check three joins (kind=ledger, kind=card, ruins_go freshness); falsifier: corpus_stats total_rows disagreeing with wc -l of catalog.jsonl after the refresh, or a kind join returning ids absent from the rebuilt map".
- The redirect, B2_481_fts_build.py header: "Mirrors B2_22_fts5_spike.py build_index()/reference_counts()/fts_expr() byte for byte in what it builds; owns only the RESULTS path and the extra spot-check block"; `RESULTS = .../B2_481_fts5_results.json` while the spike's own `B2_22_fts5_results.json` was not touched this run.
- Build output: `{"rows_indexed": 489548, "malformed_lines": 0, "rows_table_s": 4.15, "fts_rebuild_s": 3.45, "total_build_s": 7.6, "db_bytes": 134295552, ...}`; catalog_lines 489,548.
- Spot checks (B2_481_fts5_results.json): `"kind_ledger": {"tagged": 12976, "in_fts": 12976, "sample_missing": []}`; `"kind_card": {"tagged": 1807, "in_fts": 1807, "sample_missing": []}`; `"ruins_go_fts_hits": 10` with sample mtimes "2026-09-21T22:31:42Z", "2026-09-22T00:51:49Z", ... (fresh, post-rebuild bytes).
- Query parity on the rebuilt index: ruins_go fts 10 / substring reference 10; verkle 1179/1179; qdrop 4977/4977 (the C6 term now HITS on the current map; 0 on the Sep-18 fossil map per the B2-22 record).
- corpus_stats live run: `"ok": true, "tool": "corpus_stats", "total_rows": 489548` == `wc -l catalog/catalog.jsonl` = 489548.
- Tag pass: already re-run against the current map by the 19:16:46Z beat (tags.jsonl 489,548 rows == catalog.jsonl; TAG_REPORT.md header quotes the current mass) -- verified this lane rather than re-burned, since the sidecar already carried zero stale mass.

## Work done

- watch/inbox/burn_wave_20260926/B2_481_fts_build.py: import-the-spike builder with redirected RESULTS, plus the three-join spot-check block; run to completion (in-place DB rebuild, derived data per the spike's own header law).
- Verified tags.jsonl/TAG_REPORT.md currency on bytes (equal mass, refreshed header) instead of re-running the tag pass redundantly.
- corpus_stats-vs-wc falsifier check executed and green.

## Falsifier

The brief's falsifiers are both discharged by measurement (total_rows == wc -l; both kind joins return 100 percent of tagged ids with empty sample_missing). Reopen if: a later rebuild leaves catalog_fts.sqlite built from different row mass than catalog.jsonl (re-run B2_481_fts_build.py; rows_indexed must equal wc -l), or ruins_go hits again return 0 (the C6 disease, would mean the map went stale again).

## Bibliography closed

Read: watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py (build_index/reference_counts/fts_expr/RESULTS path), catalog/catalog.jsonl + tags.jsonl (line counts), catalog/TAG_REPORT.md (header), watch/inbox/burn_wave_20260926/B2_481_fts5_results.json (this run), tools/corpus.py corpus_stats (live run), watch/inbox/CORPUS_MAP_SALON_20260918.md:353-362 (Appendix B law, via QUEUE row pointer). No external sources.
