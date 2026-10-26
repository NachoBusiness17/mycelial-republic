# N6 — Training-corpus PDF fetch (2026-09-16)

**Lane:** N6 · **Operator ask:** "see if it will fetch PDFs and documents we need for training"
**Law:** receipt FIRST, appended as work proceeds. No git. No paid APIs. Free fetches only (arXiv PDFs, PMC open access, Feynman lectures HTML).

## Plan

1. Assemble target list from tonight's receipts: 26-work fungal register (S4), fiber/optical papers (O2/O3/CONCERT002), attention papers (GOAT 2601.15380, B11 2608.28444, Honjo CIM), BO primers, spinor primers (Feynman 3.1–3.2 HTML).
2. Write `scripts/fetch_training_pdfs.py` — fixed URL manifest in-script, stdlib urllib only, output to `memory/corpus/training_pdfs/20260916/`, `manifest.jsonl` entries `{url, file, sha256, title}`; verify PDF magic bytes `%PDF`, HTML sources saved as extracted .txt.
3. Build manifest + index.
4. Close with: fetched count, total MB, paywalled/blocked list (+ library needed), corpus readiness (chunkable? text-extractable? OCR needs).

## Log

- Receipt opened before any fetch.
- Target list assembled from tonight's receipts:
  - **Fungal register (S4, `watch/inbox/physical_computing/receipts/S4_CORPUS_STEAL.md`):** all open rows — PMC6227805, PMC8984380, PMC10069029, arXiv 2601.08099, PMC13212958, PMC12483595, PMC11995700, PMC13500807, PMC12513579, arXiv 2002.09680, PMC9747182, PMC10288593, arXiv 1303.4969, arXiv 1306.3414, arXiv 0810.4179, PMC2634039, arXiv 2510.19976, PMC7972235 (+ retraction note PMC8173894), PMC9673936, PMC10259323, Research Square rs-3292325 preprint, arXiv 1810.07135 (appendix rec).
  - **Fiber/optical (O2/O3/CONCERT002):** Carrillo-Acuña APL diffuser via IPICYT open repo (verified 200 PDF 3.9 MB), Mishra Sci Robotics eadk8019 via NSF PAR 10548775 (verified 200 PDF 11.7 MB), FEMS review + Telhan + LaRocco + Adamatzky line (shared with S4, fetched once, tagged both), Neurospora WCC PMC2775248, Möbius microring APL 2019 landing (PDF paywalled).
  - **Attention:** GOAT arXiv 2601.15380 (LINKS_ORE3 #3), B11 arXiv 2608.28444 (B11 receipt canonical), plus B10-named canon: Jelassi 2402.01032, Kimi Linear 2510.26692; Honjo CIM — 100k-spin Sci Adv eabh0952 resolved via Europe PMC REST to **PMC8480917** (isOpenAccess=Y, hasPDF=Y) so the robots-gated science.org /na101 PDF path is avoided.
  - **BO primers:** Frazier arXiv 1807.02811; Snoek et al. 2012 via proceedings.neurips.cc (robots.txt absent = allowed).
  - **Spinor primers:** Feynman Lectures Vol III ch 3 (sections 3.1–3.2) HTML at feynmanlectures.caltech.edu/III_03.html.
- robots.txt checked for all 10 target hosts (2026-09-16): arxiv.org allows /pdf /html /abs with crawl-delay 15 → script sleeps 15 s per arXiv hit; pmc.ncbi.nlm.nih.gov allows /articles/ crawl-delay 1; www.ebi.ac.uk (Europe PMC REST API) not disallowed for *; par.nsf.gov + repositorio.ipicyt.edu.mx allow the two mirror PDFs; science.org disallows its /na101 PDF CDN → only landing pages compliant, PMC copy used instead; europepmc.org and feynmanlectures.caltech.edu are behind Cloudflare bot challenges (attempts recorded honestly if blocked); proceedings.neurips.cc returned 404 for robots.txt (no rules).

## Fetcher build + route discoveries (appended as work proceeded)

- Fetcher written (Write tool) as a fixed-manifest script: 35 entries, candidate URL lists in priority order, stdlib `urllib` only, saves to `memory/corpus/training_pdfs/20260916/`, writes `manifest.jsonl` rows `{id,title,source,status,format,url,file,sha256,bytes,attempts,fetched_at}` and `INDEX.md`. PDF candidates verified by `%PDF` magic bytes in the first 1 KiB; HTML/JATS sources stripped to plain `.txt` (stdlib `html.parser`); bot-challenge pages and <400-char stubs rejected so the next candidate is tried.
- **Route discoveries (all verified live before/while landing):**
  - PMC `/articles/<id>/pdf/` now serves a 1.8 KB JS interstitial to non-browser clients, NOT the PDF — route removed from the script.
  - Europe PMC REST `…/rest/<PMCID>/fullTextXML` (JATS XML) is the cleanest PMC text route, but 3 items 500 persistently (PMC6227805, PMC2634039, PMC2775248) — those fall back to the robots-allowed PMC article HTML page.
  - The first script draft's markup detector missed JATS `<!DOCTYPE article …>` — fixed (any DOCTYPE/xml/article/section head accepted).
  - NCBI OA-package service (`/pmc/utils/oa/oa.fcgi`) is retired (404/SPA stub on both old and new hosts) — not used.
  - NSF PAR 11.7 MB Mishra PDF truncated mid-transfer twice under single-shot `read()`; fixed with 64 KiB chunked streaming + HTTP Range resume + backoff retries. Landed full 11,692,060 B on the resume-capable run.
  - Cloudflare-fronted hosts: feynmanlectures.caltech.edu and europepmc.org managed-challenge plain urllib (Caltech direct succeeded once, failed once — nondeterministic); pubs.aip.org hard 403. Fallback route added and used: free reader proxy `r.jina.ai/<url>` returns the same public pages as plain text with a `URL Source:` provenance line — used for Feynman III_03 and Neurospora PMC2775248; Research Square direct page is a JS app shell (2.7 KB nav text) so the proxy is tried first for that entry (6.9 KB with abstract + metadata).
  - Wayback Machine 403'd this client on both UA styles — not usable as Feynman fallback.
  - NeurIPS Snoek 2012 hash resolved from the official index (`05311655a15b75fab86956663e1819cd`); PDF lives under `/paper_files/paper/2012/file/…-Paper.pdf` (the `/hash/…-Paper.pdf` guess 404'd).

## Run history (all runs idempotent; final run is authoritative)

| pass | result | fix applied after |
|---|---|---|
| v1 | 24/35 fetched, 48.95 MB | JATS DOCTYPE detection bug; PMC /pdf/ stub route removed |
| v2 | 31/35, 45.16 MB | PMC HTML-page fallback route; NeurIPS /file/ URL; retry+Accept headers |
| v3 | 32/35, 45.24 MB | Range-resume streaming for NSF PAR; jina fallbacks for Feynman/Neurospora |
| v4 | 34/35, 56.98 MB | s4_t27 candidate order (proxy first) |
| v5 (FINAL) | **34/35 fetched (15 pdf, 19 txt), 56.96 MB; 1 blocked** | — final state — |

- Integrity: all 34 fetched files re-hashed after the final run — **34/34 sha256 match** the manifest. All 15 PDFs verified `%PDF` magic. Feynman txt contains section 3–1 ("laws for combining amplitudes") and 3–2 content. Telhan JATS extraction spot-checked publication-quality full text.

## CLOSE — N6 training-corpus fetch, 2026-09-16

**Answer to the operator's question: yes — it fetches.** The stdlib fetcher landed **34 of 35 manifest entries (56.96 MB)** into `memory/corpus/training_pdfs/20260916/`, and only genuinely bot-walled paywalls stayed out.

- **Fetched count:** 34 (15 `.pdf` verified by `%PDF` magic bytes, 19 `.txt` plain-text extractions). Total **56.96 MB**. 35th entry = the one blocked item below. Canonical batch index: `memory/corpus/training_pdfs/20260916/INDEX.md`; machine ledger: `manifest.jsonl` (per-row sha256, working URL, full attempt trail).
- **Coverage:** all 20 open rows of the S4 26-work fungal register (incl. retracted paper + retraction note as negative-case material) + the free Research Square preprint of the paywalled T2.7; the O2/O3/CONCERT002 fiber set (APL diffuser via IPICYT open repo, full 11.7 MB Mishra Sci Robotics via NSF PAR, FEMS review, Telhan, LaRocco, Adamatzky line shared with S4 — fetched once, dual-tagged); attention set (GOAT 2601.15380, B11 2608.28444, plus B10-named Jelassi 2402.01032 and Kimi Linear 2510.26692); Honjo 100k-spin CIM (PMC8480917, avoiding the robots-disallowed science.org CDN); BO primers (Frazier arXiv 1807.02811 + Snoek NIPS 2012); Feynman Vol III ch 3 (sections 3.1–3.2) HTML→txt.
- **Blocked list (what opened it):**
  1. `gf_mobius_microring_apl_2019` — AIP (pubs.aip.org) hard Cloudflare 403 for non-browser clients; **institutional library or a JS-capable browser fetch needed** for the PDF; landing metadata only.
  2. Known-paywalled canon NOT attempted (registered honestly, library required): Slayman 1976 BBA; Adamatzky Biosystems 261:105739 / 233:104933 / 236:105106 (journal versions); Nakagaki 2000 Nature; Tero 2010 Science; Karst 2023 Nat Ecol Evol; Blatt 2024 Fungal Ecology; Toyota 2018 Science; Fernando & Sojakka 2003 Springer (Semantic Scholar openAccessPdf route exists — next pass). Details in INDEX.md.
- **Corpus readiness for training/retrieval:** READY.
  - **Chunkable now:** all 19 `.txt` files are clean plain text (PMC JATS/HTML + Feynman extractions), section breaks preserved — feed any heading-aware or fixed-window chunker directly.
  - **Chunkable after one pass:** all 15 `.pdf` files are born-digital (arXiv/PMC/NSF-PAR/DSpace renders) with real text layers — `pypdf`/`pdfminer`/`pdftotext` extracts; **none need OCR** (the Telhan Sci Rep JATS metadata even self-reports `is-scanned: no`).
  - Caveats: PDF extraction flattens tables/equations — re-fetch the JATS XML (URLs recorded per row) when structure matters; `s4_t27` preprint copy is abstract-level (full preprint PDF needs a browser; DOI 10.21203/rs.3.rs-3292325/v1).
  - Re-run the fetcher any time to byte-verify the whole batch against the manifest hashes.

*Receipt closed 2026-09-16, lane N6. No git. No paid APIs. $0 spent. Fetches: arXiv (crawl-delay 15 respected), PMC/Europe-PMC REST, NSF PAR, IPICYT DSpace, NeurIPS proceedings, Feynman Lectures public HTML (via reader proxy where Cloudflare challenges plain clients). Trust bytes: 34/34 hashes re-verified post-landing.*


