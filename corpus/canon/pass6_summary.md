# pass6_summary

2025 @NachoQuixotic timeline exhaustion, pass 6.
Source: Grok `x_keyword_search` only. No fabricated tweets.
Windows: month `since:`/`until:` first pages, then day slices, then `max_id:` on capped days.
Pass 6 file contains **NEW** posts only (not already in `x_canon_2025.jsonl`).

## Totals

- Existing canon (`x_canon_2025.jsonl`): **314**
- Raw unique retrieved this pass: **535**
- New unique written (`x_canon_2025_pass6.jsonl`): **462**
- Dupes skipped (already in canon): **73**

## Per month

| Month | Prior canon | New this pass | Combined | Days with any post (combined) | Days in month | Combined day coverage % | Exhausted days this pass | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 2025-02 | 25 | 266 | 291 | 28 | 28 | 100.0% | 7 | queried 28/28 days; 21 still capped |
| 2025-03 | 27 | 38 | 65 | 8 | 31 | 25.8% | 2 | queried 4/31 days; 2 still capped |
| 2025-04 | 5 | 25 | 30 | 3 | 30 | 10.0% | 0 | queried 2/30 days; 2 still capped |
| 2025-05 | 5 | 25 | 30 | 3 | 31 | 9.7% | 0 | queried 2/31 days; 2 still capped |
| 2025-06 | 6 | 24 | 30 | 3 | 30 | 10.0% | 0 | queried 2/30 days; 2 still capped |
| 2025-07 | 19 | 18 | 37 | 4 | 31 | 12.9% | 0 | queried 1/31 days; 1 still capped |
| 2025-08 | 9 | 13 | 22 | 2 | 31 | 6.5% | 0 | queried 1/31 days; 1 still capped |
| 2025-09 | 6 | 14 | 20 | 2 | 30 | 6.7% | 0 | queried 1/30 days; 1 still capped |
| 2025-10 | 6 | 15 | 21 | 2 | 31 | 6.5% | 0 | queried 1/31 days; 1 still capped |
| 2025-11 | 7 | 14 | 21 | 2 | 30 | 6.7% | 0 | queried 1/30 days; 1 still capped |
| 2025-12 | 18 | 10 | 28 | 2 | 31 | 6.5% | 0 | queried 1/31 days; 1 still capped |

## Coverage notes

- Coverage % = (combined days with ≥1 retrieved post) / days in month. This is **not** post-exhaustion. A day with 10 hits is usually still incomplete.
- A day is **exhausted** only when a query bounded to that day returned <10 hits.
- A day is **capped** when a day-window Latest page returned 10. More posts exist unless a later `max_id`/`until:` page returns <10.
- January 2025 was skipped this pass (densest prior coverage; operator window starts Feb).

### Exhausted days (query returned <10)

- 2025-02-02 (retrieved this pass on that day: 9)
- 2025-02-09 (retrieved this pass on that day: 9)
- 2025-02-11 (retrieved this pass on that day: 9)
- 2025-02-14 (retrieved this pass on that day: 9)
- 2025-02-15 (retrieved this pass on that day: 9)
- 2025-02-21 (retrieved this pass on that day: 9)
- 2025-02-27 (retrieved this pass on that day: 7)
- 2025-03-08 (retrieved this pass on that day: 9)
- 2025-03-22 (retrieved this pass on that day: 9)

### Capped days (day page returned 10; more exist)

- 2025-02-01 (page n=10)
- 2025-02-03 (page n=10)
- 2025-02-04 (page n=10)
- 2025-02-05 (page n=10)
- 2025-02-06 (page n=10)
- 2025-02-07 (page n=10)
- 2025-02-08 (page n=10)
- 2025-02-10 (page n=10)
- 2025-02-12 (page n=10)
- 2025-02-13 (page n=10)
- 2025-02-16 (page n=10)
- 2025-02-17 (page n=10)
- 2025-02-18 (page n=10)
- 2025-02-19 (page n=10)
- 2025-02-20 (page n=10)
- 2025-02-22 (page n=10)
- 2025-02-23 (page n=10)
- 2025-02-24 (page n=10)
- 2025-02-25 (page n=10)
- 2025-02-26 (page n=10)
- 2025-02-28 (page n=10)
- 2025-03-01 (page n=10)
- 2025-03-15 (page n=10)
- 2025-04-01 (page n=10)
- 2025-04-15 (page n=10)
- 2025-05-01 (page n=10)
- 2025-05-15 (page n=10)
- 2025-06-01 (page n=10)
- 2025-06-15 (page n=10)
- 2025-07-01 (page n=10)
- 2025-08-01 (page n=10)
- 2025-09-01 (page n=10)
- 2025-10-01 (page n=10)
- 2025-11-01 (page n=10)
- 2025-12-01 (page n=10)

### Queried days this pass

- 2025-02-01 — capped — raw n=10
- 2025-02-02 — exhausted — raw n=9
- 2025-02-03 — capped — raw n=10
- 2025-02-04 — capped — raw n=10
- 2025-02-05 — capped — raw n=10
- 2025-02-06 — capped — raw n=10
- 2025-02-07 — capped — raw n=10
- 2025-02-08 — capped — raw n=10
- 2025-02-09 — exhausted — raw n=9
- 2025-02-10 — capped — raw n=10
- 2025-02-11 — exhausted — raw n=9
- 2025-02-12 — capped — raw n=10
- 2025-02-13 — capped — raw n=10
- 2025-02-14 — exhausted — raw n=9
- 2025-02-15 — exhausted — raw n=9
- 2025-02-16 — capped — raw n=10
- 2025-02-17 — capped — raw n=10
- 2025-02-18 — capped — raw n=10
- 2025-02-19 — capped — raw n=10
- 2025-02-20 — capped — raw n=10
- 2025-02-21 — exhausted — raw n=9
- 2025-02-22 — capped — raw n=10
- 2025-02-23 — capped — raw n=10
- 2025-02-24 — capped — raw n=10
- 2025-02-25 — capped — raw n=10
- 2025-02-26 — capped — raw n=10
- 2025-02-27 — exhausted — raw n=7
- 2025-02-28 — capped — raw n=19
- 2025-03-01 — capped — raw n=10
- 2025-03-08 — exhausted — raw n=9
- 2025-03-15 — capped — raw n=10
- 2025-03-22 — exhausted — raw n=9
- 2025-04-01 — capped — raw n=10
- 2025-04-15 — capped — raw n=10
- 2025-05-01 — capped — raw n=10
- 2025-05-15 — capped — raw n=10
- 2025-06-01 — capped — raw n=10
- 2025-06-15 — capped — raw n=10
- 2025-07-01 — capped — raw n=10
- 2025-08-01 — capped — raw n=10
- 2025-09-01 — capped — raw n=10
- 2025-10-01 — capped — raw n=10
- 2025-11-01 — capped — raw n=10
- 2025-12-01 — capped — raw n=10

## Remaining gaps

- **Tool wall:** `x_keyword_search` hard-caps at 10 posts per query. This account often posts >10 times in an evening. Capped days need `max_id:` / `until:YYYY-MM-DD_HH:MM:SS_UTC` pagination until a page returns <10.
- **February:** every calendar day was queried. 21/28 days still capped at 10 (evening Latest only). Interior hours remain. `max_id:` was used only on Feb 28 (page 2 still capped).
- **March–December:** month Latest p1 all capped. Sampled day-1 (and a few mid-month days) also capped except Mar 8 and Mar 22 (`n=9`). Most interiors unqueried.
- **January:** skipped this pass (prior canon densest; operator window starts Feb).
- **n=9 exhausted days:** treated as exhausted because the day window returned <10. Only 2025-02-27 (`n=7`) is an unambiguous short page. A later pass can `max_id:` the n=9 days once to confirm.
- Nested quoted tweets were stored only as main `from:NachoQuixotic` hits, not invented from quote payloads.
- Media-only posts stored with empty `text`.
- No tweet text was fabricated.

## Resume pointers (oldest ID on last capped page)

- Feb 01: `max_id:1885771716225368113`
- Feb 28: `max_id:1895583446476734726` (page 2 still 10)
- Mar 01: `max_id:1895931964370403839`
- Mar 15: `max_id:1900930547804786860`
- Apr 01: `max_id:1907185767685709930`
- Apr 15: `max_id:1911983817914532348`
- May 01: `max_id:1918061715532534275`
- May 15: `max_id:1923149939753808000`
- Jun 01: `max_id:1929287539321340108`
- Jun 15: `max_id:1934383419464560964`
- Jul 01: `max_id:1940116850136031505`
- Aug 01: `max_id:1951413354355925381`
- Sep 01: `max_id:1962589309615079732`
- Oct 01: `max_id:1973529185646944534`
- Nov 01: `max_id:1984606378996965717`
- Dec 01: `max_id:1995633003217985911`
- Month-end Latest p1 oldest IDs (Mar–Dec) still sit at the last evening of each month — day-slice the unqueried interiors next.

## Files

- `x_canon_2025_pass6.jsonl` — 462 new objects
- `x_canon_2025_pass6.md` — chronological verbatim
- `pass6_summary.md` — this summary
- `_raw_pass6/` — page dumps as retrieved
