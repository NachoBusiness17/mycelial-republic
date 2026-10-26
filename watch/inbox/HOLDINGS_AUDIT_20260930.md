# HOLDINGS AUDIT — everything acquired 2026-09-29/30 — for the librarian

_generated 2026-10-02T12:32:07.160391+00:00 · ledger rows 382 · landed claims 262 · method: `python -m mag.holdings_audit`_

## WHY THIS IS A SEPARATE REPORT

`mag.librarian` scans Markdown docs and matches receipts by **arXiv id token**
(`receipt_state()` does `ARXIV.search(p.stem)` and `continue`s on no match). The 192
documents acquired this session are Gutenberg texts, NTRS PDFs, Naval ordnance volumes,
archive.org scans and primary papers — **none has an arXiv id, so none is visible to
it.** A fresh librarian run over 5,022 documents and 298 map rows returned ZERO for
watson, bowlby, child-study, siege, shannon, turing, edvac, wilkes, frontinus, nasa,
lowenfeld, gesell and piaget.

`mag/librarian.py` was **not modified** — its scope is deliberate and I have no
operator authorization to widen it. This report is what it cannot see.

## RESULT

- ledger -> disk: **262 ok, 0 missing, 0 mismatched** (842,965,168 B re-hashed from disk)
- disk -> ledger: 263 files, 861,732,447 B; 23 unclaimed by a ledger, 0 with no receipt naming them
- duplicates: 0 byte-identical groups
- content: 0 files failed a readability/magic check
- **verdict: CLEAN**

No findings. Every landed claim re-hashes from disk, every file on disk is claimed
and receipted, no byte-identical duplicates, and every file passes a content check.
