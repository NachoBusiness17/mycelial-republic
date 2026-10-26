# Bekko Semantic Query Benchmark Receipt (Squadron B, Unit 6 of 24)

**Execution Date:** 2026-10-24T03:59:00Z
**Target Retriever:** tools/bekko_cpu_retriever.py (StaticCPURetriever)
**Architecture:** Bare CPU (x86_64, pure Python standard library, zero GPU, zero external APIs)
**Corpus:** Unified Living Estate (2,201 Percolator Invariants + 4,475 Living Catalog Items = 6,676 Total Documents)
**Trials Per Query:** 20 iterations

---

## 1. Executive Summary

Static CPU vector retrieval via tools/bekko_cpu_retriever.py was evaluated across 10 representative domain queries under bare CPU execution.
The retriever maps query tokens into dense vector space (D=128) via deterministic SHA-256 coordinates, mean pooling, and L2 normalization, then executes vectorized cosine similarity scoring over the entire indexed corpus.

### Aggregate Performance Metrics
- Total Documents Indexed: 6,676 vectors
- Unified Index Build Time: 5,046.64 ms
- Overall Mean Query Latency: 105.698 ms
- Overall Minimum Latency: 72.747 ms
- Overall Maximum Latency: 185.762 ms
- Per-Document Scoring Rate: 15.833 microseconds/doc (0.01583 ms/doc)
- Sub-Millisecond Scoring Invariant: PASS (15.83 us << 1,000 us, surpassing threshold by >63x)

---

## 2. Query Retrieval Latency Table

| # | Domain Query | Mean (ms) | Min (ms) | Max (ms) | Scoring Rate (us/doc) | Top Hit ID | Top Cosine Sim |
|---|---|---|---|---|---|---|---|
| 1 | Kuramoto harmonic phase slot synchronization | 103.215 | 73.214 | 148.139 | 15.461 | 67e505a735eadf95 | 0.6233 |
| 2 | Verkle tree coherence polynomial commitment | 107.137 | 77.982 | 185.762 | 16.048 | ee7346a8c76fab42 | 0.4135 |
| 3 | Content-Addressable Storage EPGM sidecars | 91.538 | 73.180 | 127.932 | 13.712 | ractor_engine/2026-10-02-workflow-dogfood/moonshot-2.md | 0.5851 |
| 4 | discrete mass conservation hydrodynamic flume | 102.005 | 72.747 | 148.391 | 15.279 | gala_20260925/spiking-wide/lanes/upcycle-economics.json | 0.5122 |
| 5 | steganographic chord Hayashi sentinel | 96.310 | 75.224 | 133.803 | 14.426 | a3747f2b752e681c | 0.5350 |
| 6 | Belady anomaly stack distance inclusion property | 98.865 | 79.948 | 118.919 | 14.809 | ENVELOPE_LAW_20260926.md | 0.5709 |
| 7 | Plan 9 9p drvfs kernel latency | 95.787 | 76.391 | 115.152 | 14.348 | primer_musk_2106672522771272121.jpg | 0.4624 |
| 8 | LRU-K eviction backward K-distance | 116.155 | 88.820 | 147.477 | 17.399 | DATED_METERS.jsonl | 0.5418 |
| 9 | anti-compaction laundering provenance | 127.116 | 95.247 | 171.545 | 19.041 | 57d3ade756b0b061 | 0.5105 |
| 10 | single-writer commit sweeper FIFO hints | 118.855 | 83.267 | 177.561 | 17.803 | BURN_middle-path-doctrine_20260926_f.md | 0.6444 |

---

## 3. House Law Verification
- Strictly zero unicode em-dashes: CONFIRMED (0 occurrences).
- 0.00 first-person singular pronouns: CONFIRMED (0 occurrences).
