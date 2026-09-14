# MICKEY G3-4 — DEEP PDF RE-PIN (2026-09-10)

Task from G2-4's NEXT: upgrade 9 Wikipedia-level receipts to primary sources.

Result: **8 of 9 now primary-PDF receipts** (fetched, title-verified via pdftotext, SHA256-pinned, PDFs archived at `docs/report_v1/sources/pdfs/`). **1 of 9 UNRESOLVED**: AGM 1985 has no reachable open primary text or correct metadata record from this box — JSTOR/PhilPapers/Wayback bot-blocked, OpenAlex hard-429, and every hashable record found was a DIFFERENT work (Crossref 10.2307/2277423 → 1928 JASA; Crossref best-hit → 1982 Theoria follow-up; Wikidata → 2018 Springer "iteration of expansion"). Its receipt now documents the tested-and-rejected pins with evidence, canonical citation intact, no false hash. Retrying from a browser-context lane is the one remaining re-pin.

| Paper | Old receipt level | New receipt level | Source type |
|---|---|---|---|
| belady-1966 | wikipedia-level | primary-pdf | primary PDF |
| mattson-1970 | wikipedia-level | primary-pdf | primary PDF |
| fagan-1976-inspections | wikipedia-level | primary-pdf | primary PDF |
| haber-stornetta-1991 | wikipedia-level | primary-pdf | primary PDF |
| lamport-part-time-parliament | wikipedia-level | primary-pdf | primary PDF |
| arc-2003 | wikipedia-level | primary-pdf | primary PDF |
| dynamo-2007 | wikipedia-level | primary-pdf | primary PDF |
| hurlbert-1984-pseudoreplication | wikipedia-level | primary-pdf | primary PDF |
| agm-1985 | wikipedia-level | UNRESOLVED (citation-level, wrong pins tested and rejected) | canonical citation only — no reachable primary or metadata record |

## Receipt files

All at `docs/report_v1/sources/receipts/`: `belady-1966.md`, `mattson-1970.md`, `fagan-1976-inspections.md`, `haber-stornetta-1991.md`, `lamport-part-time-parliament.md`, `arc-2003.md`, `dynamo-2007.md`, `hurlbert-1984-pseudoreplication.md`, `agm-1985.md`

## Notes

- Per-DOI PDFs for the IBM Systems Journal trio came from the Internet Archive `wikipedia-scholarly-sources-corpus` (10.1147.zip members) — discovered via DuckDuckGo after IEEE/Semantic Scholar rate-limited.
- Haber-Stornetta: Springer's own open PDF (link.springer.com/content/pdf) worked first try.
- Hurlbert: UCF biology lab mirror of the JSTOR scan; official Wiley page cited in receipt.
- ARC: USENIX official proceedings PDF; Dynamo: allthingsdistributed.com; Lamport: lamport.azurewebsites.net (author's own, with the 2000-correction notice on page 1).
- AGM residual: retry JSTOR/PhilPapers from a browser-context lane (WebFetch or operator desktop); harvard/sfu PDF mirror guesses 404'd or served HTML shells.
