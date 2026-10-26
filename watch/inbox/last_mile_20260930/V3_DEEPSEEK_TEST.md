# V3_DEEPSEEK_TEST — DeepSeek V4.1 Flash as bulk workhorse (2026-09-30)

Lane: `watch/inbox/last_mile_20260930/` · seat: ZCode subagent · budget $0.50, **spent $0.01227** (receipts below).
Model: `deepseek/deepseek-v4.1-flash` on Nous (pinned host `inference-api.nousresearch.com`).
Runner: `v3_deepseek_test.py` (same dir); raw outputs + ground truth: `v3_deepseek_results.json`.

## Pricing bytes (trust bytes, not headlines)

Catalog `/v1/models` (2026-09-30): prompt **$0.0198/M**, completion **$0.396/M**, cache read $0.0029/M (listed "original": $0.30/$1.20). The "$0.63/M" headline does not match catalog bytes; measured per-call costs below are the truth. Cheapest DeepSeek on the catalog; `deepseek-v4-flash` ($0.005/$0.16) is cheaper still but untested here.

## Task A: oral-law extraction (glm's miner job, A/B on the same 5 threads)

Exact miner ASK (`oral_law_mine_20260930.py`) re-run on 5 ORAL_LAW_INDEX rows (0, 4, 9, 14, 22).

| row | thread | ds cost | glm cost | verdict |
|---|---|---|---|---|
| 0 | Audit maps and system organs | $0.00091 | $0.0051 | parity: same audit laws, DS splits atomic, misses glm's stale-maps DEBT |
| 4 | Verify Z.AI GLM-5.3 effort transport | $0.00009 | $0.0058 | **miss**: DS skipped ("no explicit law") while glm caught restore-package DEBTs |
| 9 | New voice chat | $0.00093 | $0.0074 | **over-extract**: DS mined soft child-learning laws (lit 0.65) where glm skipped |
| 14 | Design puzzle-as-art door | $0.00103 | $0.0096 | near-verbatim match on both signature laws (lit 0.97) |
| 22 | Choose the real fleet move | $0.00121 | $0.0048 | near-verbatim match, all 3 rows incl. census DEBT |

Totals: DS $0.00417 vs glm $0.0327 = **7.8x cheaper** (mean $0.00083 vs $0.00654/thread; not 10x: DS burns ~1-2K completion tokens reasoning at $0.396/M). Schema 5/5 valid JSON, em-dash law 0 violations. Quality: 3/5 parity-or-better, 1 recall miss (DEBT-shaped material; falsifier strictness backfires), 1 precision miss (over-extracts casual threads).

## Task B: water-graph legality verification (propagator's job)

Spec exercising check-valve, XOR hold-on-both-inlets, sill hold, STARVED spill (V5 economy law landed live mid-test by sibling lane W3E; ground truth computed by the real `mag/water_graph.py`, deterministic, free oracle). Operations: boil, 2 ticks, close p2, 2 ticks.

**Perfect score, $0.00400** (1030 ptok / 9970 ctok): all 9 final volumes exact (`R1:1 R2:2 U:0 R3:0 X:6 S:0 T:14 W:2 C:3`), all 7 legality booleans correct, correct empty violations list, event trace matches the engine line for line, and it even predicted the siphon break on U running dry. Caveats: needs `max_tokens` >= 12000 (first attempt at 5000 returned EMPTY content, all budget burned as reasoning; $0.004 wasted twice learning this) and minutes of wall-clock per call.

## Verdict

- **Extraction engine: conditional yes.** 7.8x cheaper at 3/5 parity, but recall on DEBTs and precision on soft threads both drop. Recommended shape: DS as bulk first pass, glm re-run only on DS skips+low-literal rows (~20% escalation) = ~$0.0021/thread blended, ~3x cheaper than pure glm with near-glm recall. Pure-DS swap loses debt material.
- **Propagator/legality verifier: yes.** Perfect deterministic-simulation verification at $0.004/call; budget `max_tokens` 12000+ and accept minutes latency.

Spend ledger: A calls $0.00418 + B attempts $0.00809 (two truncated-B retries included) = **$0.01227 total**.
