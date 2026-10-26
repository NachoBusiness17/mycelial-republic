# PD3 — Founding-law canon fetch (2026-09-16)

**Lane:** PD3 · **Operator ask:** "the founding-law canon — the append-only amendment lineage the fleet's VOID procedure inherits, to memory/corpus/founding_law/ with manifest."
**Law:** receipt FIRST, appended as work proceeds. No git. Public-domain fetches via archives.gov, congress.gov, Project Gutenberg, avalon.law.yale.edu — all legal.

## Plan

1. Target list (all public domain / US-Gov-work / PD-translation):
   - **Magna Carta 1215** — BL translation preferred, but bl.uk is outside the sanctioned fetch domains; sanctioned-domain equivalent is the Yale Avalon 1215 translation (public-domain 1914 G.R.C. Davis-era translation). Record provenance honestly.
   - **US Constitution (National Archives transcript)** — `archives.gov/founding-docs/constitution-transcript` (original 7 articles, unaltered text intact — the append-only proof at civilization scale).
   - **All 27 amendments** — `archives.gov/founding-docs/bill-of-rights-transcript` (1–10) + `archives.gov/founding-docs/amendments-11-27` (11–27), including Amendment XXI repealing XVIII (repeal-by-addition: the VOID mechanism) and Amendment XIX (retroactive-fix: the past's meaning changed by append).
   - **19th Amendment separately** — `archives.gov/milestone-documents/19th-amendment` (transcript + background).
   - **Federalist Papers** — Project Gutenberg ebook #1404 (Hamilton/Madison/Jay), full text saved; **Federalist No. 78 extracted standalone** (judicial review: who interprets the ledger).
   - **Neutral secondary #1** — living-constitution-vs-originalism debate primer: CRS "Modes of Constitutional Interpretation" (R45129) via congress.gov/crsreports.congress.gov (US Gov work).
   - **Neutral secondary #2** — Delgado (CLS/CRT standpoint critique of neutral rules): search congress.gov CRS catalog for a neutral overview; if the sanctioned domains carry none, record the gap honestly rather than fabricating.
2. Check robots.txt for each target host before fetching.
3. Write `scripts/fetch_founding_law.py` — fixed URL manifest in-script, stdlib urllib only, output to `memory/corpus/founding_law/`, HTML sources saved as extracted .txt + raw .html, sha256 per file; manifest.json entries `{url, file, sha256, title, status}`.
4. Extract Federalist #78 as standalone canon file.
5. Close with: fetched table + the VOID design's pedigree table (which civilization-scale precedent backs each VOID rule: append-only, amendment-not-deletion, ratified interpretation).

## Log

- Receipt opened before any fetch.
- robots.txt checked for all 5 hosts (2026-09-16): archives.gov crawl-delay 10 (targets allowed); congress.gov crawl-delay 2 (/search disallowed — not used); crsreports.congress.gov no rules; gutenberg.org only /ebooks/search disallowed (not used); avalon.law.yale.edu no robots.txt (error page = no rules).
- Pre-fetch probes: avalon `/medieval/magframe.asp` is a 407-byte frameset → real text at `/medieval/magna.asp` (200, 35 KB). archives.gov transcript pages all 200. Gutenberg pg1404.txt 200 (1.19 MB). `crsreports.congress.gov/product/pdf/R/R45129` → **403** (Akamai bot wall).
- Fetcher written: `scripts/fetch_founding_law.py` (stdlib urllib, fixed manifest, HTML→txt extraction, content checks, crawl-delay honored, manifest.json).
- Fetch run: all 6 primaries 200 OK. Two check-string mismatches investigated byte-level and corrected (checks were wrong, not content): Avalon uses "freemen" (clauses 39/40 verified present: "lawful judgment of his peers", "law of the land"); NARA keeps original period punctuation "Article. VII". No refetch needed — verified by grep on saved bytes.
- Byte-level verification: BoR has Amendments I–X all present; amendments file has all 17 headings XI–XXVII; XIX text verified ("...shall not be denied or abridged ... on account of sex", Passed June 4 1919, Ratified Aug 18 1920); XXI repeal sentence verified verbatim ("The eighteenth article of amendment to the Constitution of the United States is hereby repealed."); constitution transcript has "We the People" through "Article. VII" + signatures-era chrome.
- Federalist No. 78 extracted standalone (`federalist_no78_judicial_review.txt`, 18,721 chars) from Gutenberg #1404, cut verified against the "FEDERALIST No. 79" marker; canonical judicial-review passages confirmed in the bytes: "contrary to the manifest tenor of the Constitution void", "least dangerous" (to the rights / political constitution), "fundamental law".
- Manifest hashed: `memory/corpus/founding_law/manifest.json` — 12 files, sha256 per file, per-entry status; finalize step in `scripts/finalize_founding_law.py` (idempotent).
- **Blocked so far:** CRS R45129 (Modes of Constitutional Interpretation) — 403 on crsreports.congress.gov via curl AND python urllib (Akamai TLS fingerprinting); congress.gov `/crs-product/R45129` and constitution.congress.gov also 403 via curl. Attempting alternate fetch path before recording a gap.

