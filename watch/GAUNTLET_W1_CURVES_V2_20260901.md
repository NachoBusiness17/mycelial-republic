# GAUNTLET W1 CURVES V2 — Riichi Mahjong Tutor (DEEPSEEK)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: builder-grade DRAFT L0 vs SELF-BUILT L0 is not load-bearing at this protocol — H 0.8237 (PASS-weak) and savings 57.1% (FAIL vs 75% gate), same band as v1 — SUPPORTED (n=30/arm measured, ledger at /board/w1_gauntlet_v2_ledger.jsonl) · falsifier: recomputing H/savings from the ledger crosses the pre-registered 0.85 H or 75% savings thresholds

Run: 2026-09-01T19:30:10Z · provider deepseek-chat · max_tokens 300 · waves of 5 · 30 req/arm
Rate anchors $/1M: in 0.14 / out 0.28 / cache 0.03 (r=0.214) · spend cap $0.05
Corpus label: **MIXED-CORPUS (builder-grade DRAFT L0 + SELF-BUILT L2_riichi)**
Experiment: SELF-BUILT-L0 (v1) vs DRAFT-L0 (v2) head-to-head, identical protocol.

## Arm comparison (n=30 each)

| arm | H(wtd=cached/in) | H(mean) | in tok | cached tok | cost $ | p50ms | p95ms |
|---|---|---|---|---|---|---|---|
| A0 naive | 0.0000 | 0.0000 | 806 | 0 | 0.00254 | 4774 | 5384 |
| A2 L0+L2 prefix | 0.8237 | 0.8239 | 124316 | 102400 | 0.02279 | 3960 | 4749 |

Total spend $0.02533 (cap $0.05) · wall A0 32.5s / A2 28.3s

## H curves — v1 (SELF-BUILT-L0) vs v2 (DRAFT-L0), side by side

| metric | v1 SELF-BUILT-L0 | v2 DRAFT-L0 | Δ |
|---|---|---|---|
| A2 H(wtd) | 0.8036 | **0.8237** | **+0.0201** |
| A2 H(mean) | 0.8042 | **0.8239** | +0.0197 |
| A2 cached tok | 64000 | **102400** | +38400 |
| A2 in tok | 79639 | 124316 | +44677 |
| A0 H | 0.0000 | 0.0000 | 0 |
| total cost $ | 0.00846 | 0.02533 | +0.0169 |

## Savings

Same method as v1 (credit/equiv where equiv = in·0.14 + out·0.28, no-cache baseline):
- v1 savings = 55.1%
- v2 savings = **57.1%** (+2.0pp)
- A2 v2 actual cost $0.02279 vs no-cache-equivalent $0.01972·(in+out)+(credit) → uncached-equiv $0.01972, credit $0.01126 → **57.1%**

## Verdict (identical pre-registered thresholds as v1)

- Pred 1 (A2 H ≥ 0.85, FAIL < 0.75): H=0.8237 → **PASS-weak** (same band as v1, no upgrade)
- Pred 2 (savings ≥ 75% at r=0.214, FAIL below H(1−r)≈78.6% floor): savings=57.1% → **FAIL** (unchanged)

## Does builder-grade DRAFT L0 change H/savings?

**Slight positive drift, no regime change.** Builder-grade DRAFT L0 (+ broader L0 + L2 SELF-BUILT) raised
cached prefix share (+60% cached tokens: 102K vs 64K) and H from 0.80→0.82. Savings moved 55.1%→57.1%.
Both land in the same weak-PASS / FAIL-savings band as v1. The DRAFT L0 is longer (~3.3K vs ~2.1K cached
prefix tokens), so it caches more absolute tokens, but the H gain is marginal (~+0.02) and does not cross
the ≥0.85 strong threshold nor the 75% savings gate. The self-built-L0 vs draft-L0 distinction is **not
load-bearing at this protocol** — corpus quality beyond the static-first cacheable prefix contributes little
to the measured curve, which is dominated by prefix reuse mechanics.

Evidence ledger: /board/w1_gauntlet_v2_ledger.jsonl
