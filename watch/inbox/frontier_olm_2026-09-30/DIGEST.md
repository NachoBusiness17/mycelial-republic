# Frontier OLM fold, day-1 window 2026-09-30 (BACKFILLED 2026-10-02)

**BACKFILL BANNER.** This digest and its two companions (`register.jsonl`, `percolator_candidates.jsonl`) were written 2026-10-01 23:53 EDT / 2026-10-02 UTC by the fillball lane `fill-day1-digest` (gala_20260925/fillball-1001), NOT by the original 2026-09-30 run. The day-1 workflow's fold step never ran: GAP_REGISTER rank 7 records that this folder held 6 steal cards and 32 sweep write-ups with no DIGEST, no register, and no percolator candidates, and that the step was missing, not misplaced (`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:80`, fill spec 7 at :116-119). Everything below is assembled FROM the day-1 files already on disk; no day-1 file was edited, nothing is backdated, and every quote in the register is byte-verified against the on-disk holding named in its `source` field (verification run recorded in `watch/inbox/gala_20260925/fillball-1001/lanes/fill-day1-digest.check.txt`). This file is the only thing the 2026-09-30 window was missing to become citable like the 09-28 and 10-01 windows.

## What the day-1 run banked (inputs to this fold, all read this backfill)

- `sweep/` 32 lane write-ups (8 areas x 4 doors: open-and-local-language-models, quantization-compression, kv-cache-context-engineering, agent-memory-continuity, evals-self-improvement, finetuning-adaptation, inference-efficiency, swarm-orchestration), plus raw fetch caches under `sweep/_raw/` and helper scripts.
- `steal/` 6 cards, each carrying that area's confirmed finds and falsifiable probes: `agent-memory-continuity.md`, `kv-cache-context-engineering.md`, `open-and-local-language-models.md`, `open-and-local-language-models-x.md`, `open-and-local-language-models via reddit.md`, `quantization-compression.md`.
- `lens/` 6 files (burns, corpus, doors, graph, laws, questions).
- This fold's three outputs sit at the folder root: `DIGEST.md` (this file), `register.jsonl` (23 confirmed-find rows), `percolator_candidates.jsonl` (6 rows, one per card).

**Selection rule, stated because the original adjudication artifact never landed:** the register carries exactly the confirmed finds the six cards name as carried "from the ask" (5 memory + 6 kv + 3 olm + 1 olm-x + 4 olm-reddit + 4 quant = 23 rows, 23 unique sources). This backfill did NOT re-adjudicate day-1's mining: it selects the set the day-1 workflow itself adjudicated and passed to its steal seats, as evidenced by the cards. The sweeps bank ADDITIONAL items beyond these 23 (for example the quant-arxiv sweep banks 8 items, the memory-arxiv sweep 8, the olm-arxiv sweep 8); those remain banked and citable in their sweep files and are not duplicated here. Unconfirmed items are handled under Honest gaps.

## Executive summary

**Scale.** 32 lanes banked across 8 areas x 4 doors. 23 confirmed finds carried into 6 steal cards, each card with specced, falsifiable, mostly $0 probes. Two probes were actually RUN during day-1 and one external claim died on local bytes: the reddit card's tokenizer probe (`tools/olm_tokenizer_probe.py`, landed as a durable artifact) falsified the "2.6x context cost" claim for every locally testable tokenizer and surfaced a truncation-cap defect in the local Ollama server. The kv card ran substrate scans that re-specced its own find 6 and banked a percolator candidate for missing attestation fields.

**Janitor lane verdict (this window): KEEP gemma:2b/gemma4, and the small-model supply line is drying up.** The strongest community signal (1wrez7j, 2026-09-27, register row 17) says Qwen has shipped no new small models since the 3.5 series and rumor drops the small sizes entirely; the arxiv lane's honest RQ1 answer is that NOTHING dated after 09-28 was found (arxiv sweep:76); the in-window sub-1B/2B churn is self-reported (IronLLM-0.6B "1.48x decoding speedup" claim, unfunded-tier unverified). The estate-side reads that matter are KV-cache fatness, not weights, as the janitor eviction mechanism (register row 17) and the quantization threshold laws (register rows 20-23): never below 3 bits for agentic work (2609.32042, sweep:23), Q2_K never, and perplexity alone never gates a quantize decision.

**The window's three transferable laws, one per tier of the harness:**

1. **Admission control at the sensing-to-usable seam (2609.31540).** Intrinsic checks with a measured false-accept rate decide what stays local; escalation ships the check's diagnostic as a repair hint. The estate holds the doctrine (`lens/laws.md:23`, the driving ladder) but no measured gate; the card's $0 probe audits 50 rows of `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` with three deterministic checks to print the estate's first false-accept number.
2. **Provider choice is a second decision axis with its own physics (2609.37902).** 8.8x price and 68x latency spread for identical models; `configs/cost_rates.yaml` is exactly the static price list the paper names as the wrong instrument. Port shape: a measured facet map fed by `logs/provider_usage.jsonl` plus hourly probers of the funded set, scoped honestly to the 2-3 funded lanes and the L1 churn board.
3. **Cache byte-identity is a serving law, already landed half-built (doug.sh + LRU thread).** The frozen-prefix half exists in-tree and test-proven (`mag/context_pack.py:482-526`, `tests/test_context_freeze.py:56`); the new material is the measured recompute decomposition (17.5% TTL / 33.1% tight-loop capacity / ~49.4% unattributed), enemy #4 (randomized tool-schema key order), the ~60% fill cliff, and the attestation shape proving a cache hit certifies bytes, not skipped work.

**The graph organ got its diagnosis confirmed and its ladder named.** 823 of 825 edges dangle (`lens/graph.md:13`); two independent papers converge with the lens's fix order: identity discipline at write time BEFORE consolidation, merges destructive, contradictions superseded never overwritten (register rows 1-2). The cathedral descent-order tie gets settled by paired-build measurement, not a third-model vote (register row 3).

## The six steal cards and their probes (all OWED except where marked RUN)

1. **agent-memory-continuity** (`steal/agent-memory-continuity.md`): five probes P1-P5. P1 invariant-node emission + edge recount (half a session); P2 conjunctive eviction dry-run beside `mag/percolator.py:140` decay; P3 cathedral paired build; P4 frozen 20-query corpus_search battery, healthy vs scan-fallback; P5 read-only scope-crossing audit of `mag/context_pack.py:339,377`. Order law: P1 before any fold-path SUPERSEDES work. Warm boot left standing: no paper benchmarks it; CAMG 2609.34422 nearest.
2. **kv-cache-context-engineering** (`steal/kv-cache-context-engineering.md`): the miss-decomposition probe on the 40,842-row session-tagged subset (denominator-limited), the live-provider hit assertion (the frozen-prefix banked half is test-proven), the fill-cliff readout, the particle-flock MVP (confirmed never run), the spike-hour attribution test, and the hit-consistency check (hit+miss == prompt_tokens; the four other attestation fields have NO substrate in the rows, scanned this ask).
3. **open-and-local-language-models** (`steal/open-and-local-language-models.md`): the admission-control audit over STEALTH_MINED_FINDINGS (primary, $0), the 24-48h funded-lane probe ledger (falsifier: flat latency, zero dead windows), and the mirror cold-boot drill (falsifier: zero manual steps and zero hard network deps downgrades the find to UX polish).
4. **open-and-local-language-models via x** (`steal/open-and-local-language-models-x.md`): the three-edit date guard on `watch/salon_runner.py:242-256` (the lane is LATENT: zero zai-campaign rows ever banked) plus the one-ask in-window probe (200 at $0 confirms; 401/429/billed falsifies; 20 cap-hits falsify "unlimited"). OWED-1/2/3/4 carried honestly (hour shape, catalog-hit instrument unreconciled, window continuity, verbatim line not byte-diffed).
5. **open-and-local-language-models via reddit** (`steal/open-and-local-language-models via reddit.md`): tokenizer probe RUN and the 2.6x claim killed locally; KV/memory ollama-ps probe NOT run (multi-GB pull); the 33 tok/s MLX claim out of reach on win32 (Metal-only), stated as such; the truncation-cap flag on `mag/lattice_loop.py:280` raised, not run.
6. **quantization-compression** (`steal/quantization-compression.md`): the 40-prompt induction-vs-retrieval battery on the existing fleet (primary, $0, ~80 inferences); the 10-sample collision-count probe (20 inferences); the state_quantizer zero-fraction reader (predicted below 40%); the two-arm evidence-graded intake probe (OWED enabler: `ollama create --quantize q8_0`).

## Confirmed finds (23 rows, 23 unique sources)

Window rule: the sweep lanes preferred 2026-08-31..2026-09-30. Rows tagged (pre-window) or (marked) were carried by their lanes because the research questions named them or they were the strongest evidence for the lane's question; true dates kept, out-of-window status disclosed in the register rows.

| # | Area | Title | Source | Date |
|---|------|-------|--------|------|
| 1 | agent-memory-continuity | Curate Before You Connect | arxiv.org/abs/2608.10644 | 2026-08-11 (pre-window, marked) |
| 2 | agent-memory-continuity | EngramRAG | arxiv.org/abs/2609.32049 | 2026-09-25 |
| 3 | agent-memory-continuity | RoutePrism | arxiv.org/abs/2609.34160 | 2026-09-28 |
| 4 | agent-memory-continuity | UpliftMem | arxiv.org/abs/2609.36805 | 2026-09-29 |
| 5 | agent-memory-continuity | Scope Before You Persist | arxiv.org/abs/2609.29144 | 2026-09-24 |
| 6 | kv-cache-context-engineering | LRU is harder to beat than the KV-cache papers suggest | HN 49643543 | 2026-09-10 |
| 7 | kv-cache-context-engineering | Keeping vLLM's Prefix Cache Warm Between Agent Turns (doug.sh) | HN 49758259 | 2026-09-15 (post; HN 09-18) |
| 8 | kv-cache-context-engineering | The ~60% fill cache-break cliff and the ~5M-token effective session | HN 49735410 | 2026-09-17 |
| 9 | kv-cache-context-engineering | Ask HN: Is provider KV caching sufficient for agent swarms? | HN 49783040 | 2026-09-21 |
| 10 | kv-cache-context-engineering | Show HN: Replay - audit silent prompt cache misses | HN 49691257 | 2026-09-14 |
| 11 | kv-cache-context-engineering | A cache hit is not proof that you skipped the work | siddhantkhare.com | 2026-09-14 |
| 12 | open-and-local-language-models | Touchstone (Can You Check That?) | arxiv.org/abs/2609.31540 | 2026-09-25 |
| 13 | open-and-local-language-models | You Cannot Pick a Provider From the Price List | arxiv.org/abs/2609.37902 | 2026-09-29 |
| 14 | open-and-local-language-models | Show HN: Clippy - 90s UI for local LLMs (threshold layer) | HN 43905942 | 2025-05-06 (pre-window; verified live 09-30) |
| 15 | open-and-local-language-models via x | GLM-5.3-Flash free on ZCode, extended through Oct 7 | x.com nahid_pro09 2102229686378213649 | 2026-09-22 |
| 16 | open-and-local-language-models via reddit | Qwen, where's the small stuff? (1B/2B/4B) | r/LocalLLaMA 1wrez7j | 2026-09-27 |
| 17 | open-and-local-language-models via reddit | Best Local LLMs - August 2026 | r/LocalLLaMA 1vkmhyl | 2026-08-10 (pre-window, marked) |
| 18 | open-and-local-language-models via reddit | Local models in mid-2026 | r/LocalLLaMA 1u5fv6n | 2026-06-14 (pre-window, marked) |
| 19 | open-and-local-language-models via reddit | No wonder Qwen and Gemma are so different | r/LocalLLaMA 1vjb15v | 2026-08-09 (pre-window, marked) |
| 20 | quantization-compression | Perplexity Cost Understates What Activation Quantisation Breaks | arxiv.org/abs/2609.23125 | 2026-09-19 |
| 21 | quantization-compression | Quantization Amplifies Determinism, Not Bias | arxiv.org/abs/2609.07901 | 2026-09-07 |
| 22 | quantization-compression | Breaking the 1.58-bit Barrier for Ternary LLMs (BITCOS) | arxiv.org/abs/2609.16338 | 2026-09-14 |
| 23 | quantization-compression | When Quantization Preserves Accuracy but Not Evidence | arxiv.org/abs/2609.24799 | 2026-09-21 |

Full quotes, doors, why, and overlap evidence for every row: `register.jsonl` (byte-verified; see the check file). Re-bank labels the cards carried: rows 8 (architecture half fully held by DESK_DSV41FLASH), 9 (external demand corroboration of held finding 6), 7 (headline numbers partially held at `context_economics_1m.md:46`), 12 and 13 (abstract snapshots in catalog, findings new), 23 (partial: 09-22 abstract pull, first numbers this window), 15 (in-kind model held, extension window new).

## Honest gaps (this backfill inherits and states them; none papered over)

- **The original fold artifact is gone, not recovered.** The day-1 workflow's adjudication step produced no on-disk artifact before it died, so this register is a reconstruction from the cards' named confirmed sets, not a byte-recovery of that step's output. Anything the adjudication confirmed that did NOT reach a card is not in this register.
- **The day-1 unconfirmed trio is not on disk.** GAP_REGISTER rank 10 (`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:83`) records a day-1 unconfirmed trio dropped by day-2's dedupe (U2 r/LocalLLaMA 1sy7srk KV table, load-bearing for the KV ladder; U3 arXiv 2609.21341 serving confound). This backfill grepped the day-1 folder: `2609.21341` has zero hits anywhere in it, and `1sy7srk` appears only as a held 09-28 reference at `sweep/kv-cache-context-engineering-reddit.md:34`. The trio's day-1 evidence is unrecoverable from this folder; the two items remain a rank-10 fill for a seat that can re-fetch them. Per the no-fabrication law they are NOT registered here.
- **Quotes are the sweeps' captures, not refetched.** No source was re-fetched by this backfill; every register quote is the verbatim string in the named day-1 holding. Where a card's rendering of a quote differs from the on-disk bytes, the on-disk bytes won (row 13's snapshot reads lowercase "higher-priced", the card had capitalized it). The kv card's ask-carried phrasing of find 6's TTL decomposition ("requests arriving after a gap longer than the 5-minute provider TTL...") is NOT byte-present on disk; the register carries the sweep's on-disk sentence instead (kv-reddit:23).
- **Door degradations, carried from the sweeps:** the reddit primary doors were walled in all eight reddit lanes (Welcome-to-Reddit shell / 403 / 302 to login `reason=lor2`, root-caused in `lens/doors.md`); working fallbacks were PullPush per-id and comment endpoints (subreddit listing hard-blocked for agents), WebSearch site:reddit.com (date-stripped, several recency lies caught and dated via PullPush), and redlib mirrors (intermittent). Two GLM-5.3 reddit threads returned empty PullPush archives and stayed unverified leads (reddit sweep:13). X long-form article bodies and several snippet-only leads are marked degraded in the sweeps that hit them.
- **Day-1's own provenance labels stand:** sweep-level confidence and depth labels (abs-page vs full-text reads) are carried verbatim in the register `source` fields; the olm-x tweet is a promotional post, not an official z.ai page, with OWED-1 through OWED-4 open.
- **INDEX not healed by this lane.** Fill spec 8 (rerun the sanctioned shared-surface writer after the fold's last write so these files enter `watch/inbox/INDEX.json`) is a separate fill; this lane's ownership is the day-1 folder's new files plus its own receipt, and it did not touch the shared index. Until that runs, the three new files are unindexed.
- **Checks the backfill did NOT run:** no workflow gate, no test suite, no estate code change (nothing under `mag/` or `tools/` was touched, so the violation ratchet is not applicable and was not run); no probe from any card was executed.

## Queued for the next window

1. INDEX heal (fill spec 8): one sanctioned `mag.shared_surface` rebuild after this folder's last write registers the three new files.
2. The rank-10 pair: fetch r/LocalLLaMA 1sy7srk (KV depth tables, load-bearing for the KV ladder) and arXiv 2609.21341 (serving confound) and bank them with full evidence, closing the unconfirmed-trio debt the day-1 fold left.
3. The olm-x probe window closes Oct 7: one in-window salon fold ask settles the free-rung extension for the estate's credential.

Backfill receipt: `watch/inbox/fillball/day1-digest.md`. Check log (byte verification of all 23 register quotes plus file existence): `watch/inbox/gala_20260925/fillball-1001/lanes/fill-day1-digest.check.txt`.
