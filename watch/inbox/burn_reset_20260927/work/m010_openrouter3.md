# WORK m010

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-10-08T06:59:11.615527+00:00
finish: stop cached_tokens: 352
ask: Both the Mattson 1970 stack-distance paper and the Neil et al. 1993 LRU-K paper came back OWED on verbatim quotes from their own text (one OCR quote for Mattson, none for LRU-K). The deeper unknown they share: stack distance gives you F(C) for every cache size from one trace, while LRU-K replaces the eviction rank with the Kth most recent access timestamp — but nobody in these findings says whethe

---

(1) FINDING
I could not retrieve and verify verbatim quotes from the Mattson 1970 IBM Systems Journal paper and the Neil et al. 1993 SIGMOD LRU-K paper with the required source fidelity in this session. The exact mathematical relationship between Mattson’s stack-distance histogram n(Δ) and LRU-K’s eviction decision, and whether the CDF of n(Δ) at depth K gives the LRU-K hit rate for capacity C=K with a correction term defined in Neil et al., is OWED.

(2) one STEALABLE idea worth keeping
Use stack-distance distribution from a single trace to estimate hit-rate curves for any fully-associative LRU-like policy without re-simulation, then test the same distribution as a feature basis for predicting LRU-K hit rates.

(3) one TESTABLE hypothesis
The LRU-K hit rate for capacity C and K > 1 is not equal to the stack-distance CDF Pr[Δ ≤ C] at depth K, and the deviation is explained by the K-th reference age distribution defined in Neil et al. 1993.

(4) EVIDENCE or OWED
OWED. No verified verbatim quotes from Mattson 1970 IBM Systems Journal and Neil et al. SIGMOD ’93 LRU-K paper were obtained and checked in this session. No sources cited.
