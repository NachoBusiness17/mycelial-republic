# AE4 — TabFM-Auto research (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Sources: arXiv 2609.37989 + 2609.37959, deqingfu.github.io/tabfm-auto/, research.google blog, github.com/google-research/tabfm.

**(1) Mechanism.** No cross-attention fusion — it's decoupled. A frozen 400M-param TabFM does prediction: alternating row/column attention -> each row compressed to one dense vector -> a Transformer does in-context learning over compressed rows (train + query rows as a single prompt; agent samples context within ~16,384 rows). Pretrained on hundreds of millions of synthetic SCM tables. An LLM coding agent (Antigravity + Gemini) supplies the semantics: it reads column names, task description, auxiliary files, and validation scores (3-fold CV), then evolves Python hooks — `preprocess`, `engineer` (features), `sample`, `TABFM_KWARGS`, `postprocess`. Fu: "LLMs provide knowledge while TabFM makes predictions."

**(2) "Auto" vs prior.** Base TabFM ignores column names/metadata; TabFM-Ensemble was a fixed hand recipe. Auto replaces it with agentic pipeline search (no gradients, no training). 1785->2013 Elo; top-5 spots on all of TabArena; pipelines transfer zero-shot to TabPFN-3 (+131) and TabICLv2 (+143).

**(3) Benchmarks.** TabArena: 51 datasets (38 classification, 13 regression, 700-150k rows), #1. MLE-Bench tabular: 8 Kaggle comps, #1 (1827 Elo, golds on volcanic-eruptions, nomad2018).

**(4) Open?** Base TabFM: YES — HF `google/tabfm-1.0.0-pytorch`, GitHub, BigQuery `AI.PREDICT`. TabFM-Auto: pipelines browsable per dataset, but no code/weights repo linked yet.

**(5) Estate fit (AE5's census is the pairing).** Caveat: it's a predictor, not a query engine — it won't replace FTS5 retrieval or propagator causality, and 16k-row context means sampling our millions of rows. The directly analogous win: Amazon_employee_access (opaque integer IDs -> graph-degree features, -26.6% error) maps exactly onto hash-cell ledgers — agent-evolved structural features + zero-shot verdict/anomaly/missing-cell scoring with no per-ledger training.

The tweet image never loaded (404 on every attempt).

URLs:
- https://arxiv.org/abs/2609.37989
- https://arxiv.org/abs/2609.37959
- https://deqingfu.github.io/tabfm-auto/
- https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/
- https://github.com/google-research/tabfm
