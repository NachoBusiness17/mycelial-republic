# LIBRARIAN v1 RETIRED (fix-queue Q6) — 2026-09-27

**Call:** formal retirement, not a 198-primary drain. The v1 report (2026-09-10, watch/LIBRARIAN_REPORT.md) was 16 days stale holding 198 RETRIEVAL-PLAN rows. Bulk-pulling 198 primary PDFs attaches proof to no live claim; the fleet's no-fabrication law (2026-09-19) already governs primary pulls at point-of-claim. The backlog's real debt was that sources were NAMES without metadata; that debt is now paid.

**What landed:**
- `tools/librarian_backfill_20260927.py` resolved 189/194 arXiv ids via Semantic Scholar's batch API into `corpus/papers/librarian_backfill_20260927.jsonl` (title, authors, year, abstract sha256, payload sha256; state NAMED+RESOLVED — metadata is not a primary artifact and nothing is marked PULLED+HASHED).
- Spot-checks verify: 2211.05102 = Pope, Efficiently Scaling Transformer Inference (2022); 1201.0749 = the 16-clue Sudoku paper; 2609.04611 = tau-tau-Bench (2026).
- The report header now carries the RETIRED banner with reason and date (stale-trap doctrine: refresh or register frozen).

**Honestly still owed (9 rows, by name):**
- 5 malformed arXiv ids the report itself flagged: 2007.1558 and 2008.0277 ([DOI-ARTIFACT] rows, old-style 4-digit suffix), 2026.15906 and 2026.84791 (future-dated), 3841.71428 (pi-shaped, almost certainly a mint error). These resolve on neither API; fixing them needs the original citing doc, which the report does not name.
- 4 key: rows that are not on arXiv: Belady 1966 (IBM SysJ), Kraska 2018 learned indexes, Mattson et al. 1970, LRU-K/ARC/LeCaR (O'Neil 1993, Megiddo-Modha 2003, Vietri 2018). Classical-print sources; pulled if ever cited live.

**Transport note (fold for future drivers):** this sandbox's proxy 406s python urllib to arxiv/semanticscholar while curl passes; arXiv kept this IP hard-429'd through every backoff (150s cooldown + 8 retries), so S2's batch endpoint (4 POSTs) was the resolver. Curl-as-transport with host allowlist + private-IP DNS refusal is the standing pattern (mirrors the hermes dual-burn driver law).
