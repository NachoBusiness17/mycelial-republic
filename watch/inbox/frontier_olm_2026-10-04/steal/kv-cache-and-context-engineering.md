# STEAL CARD: kv-cache-and-context-engineering (round 1, 2026-10-04)

Source: "Validating Hybrid-State Cache Recovery for GLM-5.3-Flash with vLLM and LMCache", Frank Li, arXiv 2609.15030, submitted 14 Sep 2026, https://arxiv.org/abs/2609.15030

## Verification ledger (what this seat ran, this ask)

- Paper verified by fetch of the arXiv abstract page (2026-10-04): the find's quote is the abstract's first sentence verbatim; the abstract names strict-prefix lookup as the alignment cure, "fixed per-rank kernel configurations", a RedHatAI/GLM-5.3-Flash-NVFP4 checkpoint under four-way tensor parallelism on the 45-layer model, agreement improving from 34/36 to 36/36 generations after alignment, and CPU reload cutting time to first token by 46-64% and total request time by 1.9-7.0% vs modified cold recomputation. Stated scope limit: one model revision, controlled configuration, no concurrent-serving or capacity claims.
- Overlap claim verified: `grep -c "hybrid-state\|2609.15030" catalog/catalog.jsonl` returned 0; `grep -c "2609.15030" memory/runs/corpus_gap_research/ARXIV_REGISTER.json` returned 0; the only prior trace is exactly 1 mention of 2609.15030v1 in the 10-03 raw census `watch/inbox/frontier_olm_2026-10-03/sweep/_raw/q1_candidates.json`. Never banked as a find before this card. The find is lane item 2 at `watch/inbox/frontier_olm_2026-10-04/sweep/kv-cache-and-context-engineering-arxiv.md:35`.
- Shelf verified: `corpus/library/lmcache-src/` is on disk (lmcache/, csrc/, examples/, benchmarks/ trees). Row count: `grep -c "lmcache-src" catalog/catalog.jsonl` reads 2,333 at this moment; the lens moment read 2,331 (`watch/inbox/frontier_olm_2026-10-04/lens/corpus.md:20`). The +2 is catalog drift between the two moments (moving-tree law, B2-246); both numbers are cited, the claim rides the instrument and moment, not a constant.
- Area fit verified: this is area 6, `watch/inbox/frontier_olm_2026-10-04/lens/questions.md:82`; Q1 asks which lmcache offload/transfer features are unwired into the estate's serving path (:87) and Q5 asks whether KV quantization interacts with the reasoning-quant ladder rungs (:91). This paper answers Q1 with a named feature list and feeds Q5 with NVFP4 evidence. Estate map for the area: `questions.md:93`.

## The steal, as a mechanism

Token-prefix validity does not imply state validity. On a hybrid-architecture model (GLM's interleaved attention layers), an externally transferred KV cache can report a COMPLETE hit while the resumed model is internally inconsistent: the cache boundary proves which tokens were seen, not that every layer's state actually matches the checkpoint, kernels, and schedule that produced it. The paper's cure is a recovery contract with three portable moves:

1. STRICT-PREFIX RECEIPT: recovery aligns on the longest token prefix whose blocks verify, never on the nominal complete-hit boundary. A hit is claimed by token identity but consumed by state identity.
2. DETERMINISM PINNING: per-rank kernel configurations are fixed so a resumed state is reproducible; the mismatch that credited one fewer token came from unpinned kernels, not missing data.
3. CPU-RELOAD TIER: for the resume path, reloading state from a CPU tier beats modified cold recomputation on TTFT (46-64% cut) at 1.9-7.0% total-time cost, and measured agreement went 34/36 to 36/36 once alignment was in.

The one-line law to mint: NO CACHE RESUME WITHOUT A VERIFIED-PREFIX RECEIPT, AND NO HIT KPI THAT COUNTS UNRECEIPTED HITS.

## Estate map (organ + concrete port move)

- Primary organ: CONTEXT PACK and its checkpoint/reuse machinery. `mag/context_checkpoint.py:1-13` already moves compressed checkpoints (Verkle chain pointer + summary) so consumers skip re-reading history; `tools/prefix_cache_sim.py:32` cites the estate pack shape (`mag/context_pack.py:1416` clip) and `tools/lru_null_arm.py` replays real trail tapes through a freeze+tail pack at the real 4800-char budget (`mag/context_pack.py:67`). PORT MOVE: give every reused checkpoint/pack prefix a strict-prefix receipt (hash of the longest verified frozen prefix plus a config-generation tag) and gate skip-recompute on receipt match, so a "complete hit" that cannot prove its state costs the same as a miss. Split `tools/cache_kpi.py`'s tok_hit% KPI (`tools/cache_kpi.py:22-30`) into nominal vs receipt-verified hits so the estate's provider cache economics measure usable cache, not claimed cache.
- Secondary organ: QUANTIZER (Q5 rung evidence). `mag/state_quantizer.py:1-4` runs the quantization analogy on estate state; the reasoning-quant ladder probe is open (`lens/questions.md:84`, `:91`). The paper is direct evidence that an NVFP4 (4-bit) checkpoint of GLM-5.3-Flash serves on vLLM+LMCache with 36/36 agreement once recovery is aligned: quantization interacts with cache recovery, not only with accuracy. PORT MOVE: the ladder probe's metric set gains recovery-agreement-under-cache-resume (and, same shape, the ECE addition already banked by the 10-04 inference-efficiency lane at `watch/inbox/frontier_olm_2026-10-04/sweep/inference-efficiency-hn.md:41`), so a quant rung is not called safe from accuracy and tok/s alone.
- Third organ: the SIMULATOR SURFACE. `tools/prefix_cache_sim.py:11` already implements strict-prefix lookup semantics for its radix cache (block-by-block walk from the root, stop at the first absent block); the paper supplies the missing failure-mode arm for it (see probe).

Honest scope: the estate does not run vLLM+LMCache serving today; the shelf is in-corpus source awaiting exactly the Q1 unwiring pass (`questions.md:87`). This card banks the receipt law and the simulator arm first; wiring the serving path is a later, separately gated move. The paper's own scope limit (one model revision, controlled config, no concurrency claims) travels with the steal.

## Falsifiable probe (cheap, this week, local, zero paid dispatch)

Add a generation-mismatch arm to the existing null-arm replay: tag every cached block in `tools/prefix_cache_sim.py` with a config-generation id, poison a fixed slice (10%) of cached blocks with a stale generation so the radix tree reports a complete hit over state that a resumed model could not actually use, then replay the same trail tapes through `tools/lru_null_arm.py` twice: once resuming on the nominal complete hit, once gated on the strict-prefix generation receipt. CLAIM TO FALSIFY (from the paper): the nominal arm shows measurably worse agreement (pack-level equivalence: byte-identical frozen prefix plus transcript-tail hash) than the receipt-gated arm. FALSIFIER: if the two arms agree at the injected rate across all capacity points on the estate's tape distribution (delta = 0), the failure mode does not manifest in the estate's reuse pattern and the receipt wire is not justified by measurement; any delta > 0 mints the estate's measured null arm for cache-resume claims, the G1 gap law's shape (`tools/lru_null_arm.py:2-5`). Runtime: the existing CLI replay, minutes, stdlib only.

## OWED (not verified in this ask)

- Full-text details (8pp/3fig/7tab per the sweep lane) ride the lane's read at `sweep/kv-cache-and-context-engineering-arxiv.md:35`; this card verified the abstract only.
- Today's measured baseline from `tools/cache_kpi.py` over `logs/provider_usage.jsonl` was not pulled in this ask; it is probe-week work, not needed for the card.
