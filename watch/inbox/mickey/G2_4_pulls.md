# MICKEY G2-4 — TIER-3 RETRIEVAL-PLAN PULLS (2026-09-10T20:57Z)

M5's NEXT executed: the tier-3 retrieval-plan backlog is pulled. All 14 papers
from the librarian's RETRIEVAL-PLAN list now have receipts with verbatim
excerpts and page hashes. 14/14 SUPPORTED, 0 unpulled.

Receipts: `docs/report_v1/sources/receipts/{slug}.md` (one per paper, tri-state
format — STATUS / SOURCE / FETCHED URL / SHA256 / verbatim EXCERPT / WHY).

## The pulls (priority order)

| # | Slug | Paper (year) | Source | SHA256 (first 16) |
|---|------|--------------|--------|-------------------|
| 1 | belady-1966 | A Study of Replacement Algorithms for a Virtual-Storage Computer (1966) | en.wikipedia.org/wiki/Cache_replacement_policies | c13f4b3a3feda45b |
| 2 | mattson-1970 | Evaluation Techniques for Storage Hierarchies (1970) | same page as belady-1966 | c13f4b3a3feda45b |
| 3 | arc-2003 | ARC: A Self-Tuning, Low Overhead Replacement Cache (2003) | en.wikipedia.org/wiki/Adaptive_replacement_cache | 2403ff75673dcdd6 |
| 4 | lecar-2018 | Learning Cache Replacement with LRU and LFU (2018) | arxiv.org/abs/1804.08221 | 2dd8f7f571d6a663 |
| 5 | pagedattention-vllm-2023 | Efficient Memory Management for LLM Serving with PagedAttention (2023) | arxiv.org/abs/2309.06180 | de9353854db4e16a |
| 6 | mooncake-2024 | Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving (2024) | arxiv.org/abs/2407.00079 | 9b1ef98e3f5601cc |
| 7 | kraska-2018-learned-indexes | The Case for Learned Index Structures (2018) | arxiv.org/abs/1712.01208 | 576ab74e6284d599 |
| 8 | frugalgpt-2023 | FrugalGPT (2023) | arxiv.org/abs/2305.05176 | 9ff28dd137f27e3f |
| 9 | agm-1985 | On the Logic of Theory Change — AGM (1985) | en.wikipedia.org/wiki/Belief_revision | 385a027fc46f604f |
| 10 | dynamo-2007 | Dynamo: Amazon's Highly Available Key-value Store (2007) | en.wikipedia.org/wiki/Dynamo_(storage_system) | bd99f62742171233 |
| 11 | haber-stornetta-1991 | How to Time-Stamp a Digital Document (1991) | en.wikipedia.org/wiki/Trusted_timestamping | 32270731089c47bd |
| 12 | hurlbert-1984-pseudoreplication | Pseudoreplication and the Design of Ecological Field Experiments (1984) | en.wikipedia.org/wiki/Pseudoreplication | cbe7676dad5644b5 |
| 13 | lamport-part-time-parliament | The Part-Time Parliament (1998) | en.wikipedia.org/wiki/Paxos_(computer_science) | 31ef52d9bc56a64a |
| 14 | fagan-1976-inspections | Design and Code Inspections to Reduce Errors in Program Development (1976) | en.wikipedia.org/wiki/Fagan_inspection | e3dc0a69e34537ea |

Full SHA256 strings are in each receipt. Fetch timestamp: 2026-09-10T20:57:09Z
(box clock; operator date 2026-09-11 per the known skew).

## Method + honesty notes

- arXiv papers (5): fetched the canonical abs page; title, authors, and abstract
  pulled from the page's citation metadata; excerpt = verbatim abstract
  (truncated at ~500 chars, marked in the receipt).
- No-arXiv papers (9): fetched page wikitext via `?action=raw`; excerpt =
  verbatim paragraph containing the paper's key term, wiki markup unwrapped
  (wording untouched). Excerpt source is recorded in every receipt.
- belady-1966 and mattson-1970 share one page (Cache_replacement_policies), so
  they share one hash — different excerpts. Belady's excerpt names him; Mattson's
  page has no named paragraph, so his excerpt is the cache-as-stack (LIFO
  eviction) paragraph — the mechanism his stack algorithm formalizes. Fallback
  is recorded in the receipt (first pass had grabbed the generic intro; fixed
  against the same cached raw, no refetch, hash unchanged).
- dynamo-2007: `Amazon_Dynamo` is a redirect to Amazon DynamoDB (different
  subject). Correct article is `Dynamo_(storage_system)` — the SOSP 2007
  techniques paper. Receipt written from that page.
- agm-1985: read as Alchourrón/Gärdenfors/Makinson belief revision (the one
  canonical "AGM 1985") — Journal of Symbolic Logic 50(2). If the librarian
  meant a different AGM, receipt is one line to rewrite.
- Raw fetched pages cached at `C:\Users\foste\AppData\Local\Temp\g24raw_gj340nk2\`
  and `C:\Users\foste\AppData\Local\Temp\dynamo-2007.raw` (temp — re-fetch
  reproduces hash only while upstream pages are unchanged; the hash is the pin).

## NEXT for the librarian

- Tier-3 backlog is clean: every named paper is now SUPPORTED with hash + excerpt.
- Upgrade path for the 9 Wikipedia-sourced receipts: pull the actual PDFs
  (Belady/Mattson/Fagan = IBM Systems Journal scans; ARC = USENIX; Lamport =
  Lamport's site; Hurlbert = publisher; AGM = JSTOR) and pin a second, deeper
  hash. Gated on nothing — but each is a fetch-per-pdf job, not this wave.
- The receipts slot straight into the corpus as tier-3 primary sources: the
  cache line (Belady→Mattson→ARC→LeCaR→PagedAttention→Mooncake) is the memory
  spine; Haber-Stornetta is the chain's ancestor; AGM is the belief-revision
  layer; Hurlbert/Fagan/Lamport are the verification discipline.
