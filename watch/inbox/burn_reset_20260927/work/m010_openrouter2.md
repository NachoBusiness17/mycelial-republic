# WORK m010

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-10-08T06:53:37.366232+00:00
finish: stop cached_tokens: 0
ask: Both the Mattson 1970 stack-distance paper and the Neil et al. 1993 LRU-K paper came back OWED on verbatim quotes from their own text (one OCR quote for Mattson, none for LRU-K). The deeper unknown they share: stack distance gives you F(C) for every cache size from one trace, while LRU-K replaces the eviction rank with the Kth most recent access timestamp — but nobody in these findings says whethe

---

(1) FINDING: The CDF of Mattson's stack-distance histogram n(Δ) at depth K does not directly give the LRU-K hit rate for capacity C = K, because LRU-K ranks blocks by the timestamp of their Kth previous access rather than by a single reuse distance. Neil et al. 1993 define a correction term involving the recency distribution of Kth-order references, but the exact formula is not verifiable here.

(2) STEALABLE idea: Approximate LRU-K hit rates by computing the empirical distribution of the Kth-order reuse distance (the gap to the Kth prior access of each block) and comparing its CDF against cache capacity C, instead of using the first-order stack-distance CDF.

(3) TESTABLE hypothesis: For a given trace, the LRU-K hit rate with C = K equals the fraction of accesses whose Kth prior occurrence is within K positions, minus the fraction of blocks with fewer than K total occurrences, and this difference predicts the hit rate observed in a direct LRU-K simulation.

(4) EVIDENCE or OWED: OWED. Verbatim quotes and exact formulas from Mattson 1970 and Neil et al. 1993 could not be retrieved and verified; no sources are cited because the exact textual passages are not confirmed.
