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

