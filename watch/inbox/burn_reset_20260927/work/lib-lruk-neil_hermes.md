# WORK lib-lruk-neil

lane: hermes (headless one-shot)
ts: 2026-09-29T18:17:04.397576+00:00
ask: Find the canonical reference for LRU-K (Neil, O'Neil, 1993?). Return: exact title, venue, year, one verbatim quote of the LRU-K eviction rule. If unreachable, say OWED with what you tried.

---

FINDING

Title: "The LRU-K page replacement algorithm for database disk buffering"
Authors: Elizabeth J. O'Neil, Patrick E. O'Neil, Gerhard Weikum
Venue: Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data (SIGMOD '93), Washington, D.C., June 1993, pp. 297-306
DOI: 10.1145/170035.170081 (proceedings); journal version ACM SIGMOD Record 22(2):297-306, DOI 10.1145/170036.170081

Verbatim quote (paper abstract, verified against Crossref + OpenAlex inverted index):

"The basic idea of LRU-K is to keep track of the times of the last K references to popular database pages, using this information to statistically estimate the interarrival times of references on a page by page basis."

STEALABLE idea

LRU-K's core trick: evict by the recency of the K-th reference, not the most recent one. This turns a one-tier recency stack into a two-tier history that separates "frequent but stale" from "frequent and hot" without external hints or manual pool tuning. Steal the shape for any cache that currently hard-codes pool sizes or access-frequency hints -- the K-th arrival time is a free signal most designs throw away.

TESTABLE hypothesis

LRU-K with K=2 will outperform plain LRU on any workload where reference interarrival times are heavy-tailed (e.g., bursty scan + steady hot set), and the gap widens as buffer size shrinks relative to working set. Falsifiable: simulate a zipfian hot set + uniform scan on buffer sizes 10-1000 pages; if LRU beats LRU-K2 at every buffer size, the heavy-tail assumption is the wrong model for that workload.

EVIDENCE / OWED

Evidence: Crossref API GET on DOI 10.1145/170035.170081 confirms title, authors, venue, pages, year. OpenAlex W2054308357 abstract matches word-for-word. Estate receipt `watch/inbox/burn_reset_20260927/flash50/r-belady-lruk.md` banks the full verification trail (bitsavers Belady/Mattson scans, pypdf extraction, API calls). ACM DL page renders the same abstract.

OWED: the paper's introduction reportedly contains the stronger claim "LRU-K provides strong, non-adaptive real-time guarantees in the face of pathological access patterns." I could not verify that sentence verbatim this session -- ACM DL served a Cloudflare challenge, archive.org was offline, the author's lru-k.ps paths return 404, Semantic Scholar API returned 429. Treat the intro "guarantees" phrasing as unverified until the full text is accessible. No em-dashes used; no fabrication.
