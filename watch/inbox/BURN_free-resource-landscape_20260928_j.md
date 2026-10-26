## Verdict

steal

## Evidence

- Full dump (GET https://api.featherless.ai/v1/models, no params, keyless, HTTP 200, attempt 1, read 2026-09-28): 7,073,570 bytes, single envelope key "data", 22,054 rows counted by parse. Baseline 22,044 (receipt h, 09-27): same instrument, +10 in one day, alive.
- Paged route (GET .../models?sort=-created_at&per_page=100, HTTP 200): page 1 pagination {"current_page": 1, "per_page": 100, "total_items": 50652, "total_pages": 507}, top-level "total": 50652. Page 2 (followed via current_page): total_items 50652, total_pages 507, per_page 100. Page 3: identical. Counter stable across all three pages; 300 rows served, 300 distinct ids, zero repeats.
- Paged-implied sum: 507 pages x 100 per_page = 50,700, bounded by total_items 50,652 (last page 52 rows). Full dump does not match it: 22,054 vs 50,652, gap 28,598.
- Overlap probe (local parse, zero extra network): all 300 newest paged ids are present in the full dump, 0 absent. The dump serves the newest roster; the counter's extra rows are not served by the no-params route.
- Gap drift: 09-27 gap 28,542 (22,044 vs 50,586, receipt h) to 09-28 gap 28,598. Paged counter grew +66 over that window, dump grew +10. The reported counter outgrows served rows.
- Web search "Featherless models total count 2026": thin, stated honestly. Results (featherless.ai landing, tensorwave.com talk coverage, getlatka.com revenue page) carry no exact model count. Nothing contradicts the byte readings.

## Steal or Vacuous

Steal. The Featherless instrument-mismatch gap is closed: both routes are live, the paged counter is internally stable and cleanly paginated, and the roughly 28.6k gap is real, not an artifact. Canon per bytes-not-reports and the census-denominator law: the roster-diff tool standardizes on the full-dump instrument (count parsed from actually served bytes), because its rows are the iterable roster and every newest paged id is byte-proven inside it. The paged total_items is a reported-superset telemetry counter, directionally corroborating receipt h's gated-or-archived hypothesis (counter +66 vs served rows +10 in one day), and is filed as a separate freelane telemetry lane, never differenced against the dump count. The content of the unserved ~28.6k rows stays unverified (deep-page walk outside the 3-attempt probe budget) and is owed.

## Bibliography

- https://api.featherless.ai/v1/models (GET 2026-09-28, HTTP 200 keyless, 22,054 rows byte-backed)
- https://api.featherless.ai/v1/models?sort=-created_at&per_page=100 (plus page=2 and page=3 via the envelope, GET 2026-09-28, HTTP 200 keyless, byte-backed)
- watch/inbox/BURN_free-resource-landscape_20260928_g.md (read 2026-09-28, the mismatch as landed)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-28)
- WebSearch 2026-09-28, query "Featherless models total count 2026": thin, summaries only, no exact count
