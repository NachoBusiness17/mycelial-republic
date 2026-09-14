# GAUNTLET W1 CURVES — Riichi Mahjong Tutor (DEEPSEEK)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: A2 L0+L2 prefix arm hits H=0.8036 (PASS-weak) but 55.1% savings FAIL the pre-registered 75% floor, on self-built fallback corpus — SUPPORTED (measured n=30/arm curves, honest label) · falsifier: re-run on builder-original corpus reaches H≥0.85 and savings≥75%

Run: 2026-09-01T19:03:45.566Z · provider deepseek-chat · max_tokens 300 · waves of 5 · 30 req/arm
Rate anchors $/1M: in 0.14 / out 0.28 / cache 0.03 (r=0.214) · spend cap $0.05
Corpus label: **SELF-BUILT-CORPUS** (fallback draft, not builder-original)

## Arm comparison (n=30 each)

| arm | H(wtd=cached/in) | H(mean) | in tok | cached tok | cost $ | p50ms | p95ms |
|---|---|---|---|---|---|---|---|
| A0 naive | 0.0000 | 0.0000 | 1483 | 0 | 0.0027 | 4952 | 5524 |
| A2 L0+L2 prefix | 0.8036 | 0.8042 | 79639 | 64000 | 0.0057 | 3459 | 4316 |

## H curves (per-request cachedTok/promptTok)

64000 cached tokens across A2 against 79639 input tokens; A0 holds ~0 cache (naive single-prompt has no shared prefix).

## Cost curves

A0 est spend $0.00273 · A2 est spend $0.00574 · total $0.00846 (cap $0.05) · wall 56.0s

A2 uncached-equivalent input cost = 0.01278 → savings = 55.1%

## Verdict vs pre-registered thresholds

- Pred 1 (A2 H ≥ 0.85, FAIL < 0.75): H=0.8036 → **PASS-weak**
- Pred 2 (savings ≥ 75% at r=0.214, FAIL below H(1−r) floor): savings=55.1% → **FAIL** (floor 78.6%)

Honest label: this corpus is SELF-BUILT (fallback drafts), so H reflects cache mechanics + our own prefix reuse, NOT builder-original corpus quality. On a cold-start A2 first request H≈0; warm re-entry drives the measured curve.