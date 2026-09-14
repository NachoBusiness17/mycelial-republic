# CACHE YIELD MATH — S5 S/N (2026-09-01)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: DeepSeek off-peak is the load-bearing cache reservoir — $0.03/1M cached at 100% hit-rate, ~$2.61/mo saved on ~24M cached tokens — SUPPORTED (rates measured in NIGHT_CACHE_RECEIPTS; monthly yield is stated-assumption extrapolation) · falsifier: re-measured hit-rate well below 100% or cached $/1M materially above $0.03 on the DS lane

Source: NIGHT_CACHE_RECEIPTS. All rates MEASURED/gate-PASS (no provider calls). $/1M + monthly yield at fleet overnight scale.

## $/1M cached vs uncached (per reservoir)

| reservoir | model | status | cached $/1M | uncached $/1M | hit-rate (identical-prefix) |
|---|---|---|---|---|---|
| 1 — DS off-peak | deepseek-chat | **CLEAN PASS** | **$0.03** | $0.14 | 100% (par1/3/4, 4864→7808 tok) |
| 2 — z.ai Lite | glm-4.7-flash | cache-LIVE / RATE-GATED (1305) | n/p | n/p | 4604 tok live, not extrapolatable |
| 3 — z.ai credits | glm-4.7-flash | GATED (1305) | n/p | n/p | — (no batch) |

z.ai reservoirs 2–3: cache mechanism measured live but tonight's 5h credit bucket is fenced (error 1305). Cannot price $/1M reliably this window → **DEFFERED**, not burn. Refund count: 0 (nothing spent).

## Best reservoir — DS off-peak (reservoir 1)

- Savings per 1M cached vs cold: **$0.14 − $0.03 = $0.11/1M**; $/1M cached **$0.03** (7808 tok/600-rep ≈ $0.0002/call).

## Monthly yield extrapolation (fleet overnight workload scale)

Assumptions (stated inline): independent-day run-rate DS lane ≈ $1.33/day ⇒ ~9.5M input tok/day at $0.14/1M; off-peak window = 06–10Z = 4h = 4/24 of daily volume; 50% of window reads cacheable (identical-prefix reuse); 30-day month; 100% hit-rate (measured).

- Daily cacheable = 9.5M × (4/24) × 0.50 = **0.79M tok**
- Monthly cacheable = 0.79M × 30 = **23.8M tok**
- Monthly uncached = 23.8M × $0.14/1M = **$3.33**
- Monthly cached = 23.8M × $0.03/1M = **$0.71**
- **Monthly savings from caching = $2.61** (≈ 78% of uncached cost eliminated on this slice)

Verdict: DS off-peak is the load-bearing cache reservoir for the $200 deployment rec — sub-cent reads at 100% hit-rate, ~$2.6/mo saved on ~24M cached tokens.

## Labels
R1 DS: MEASURED. R2/3: cache-LIVE + rate-gate MEASURED; yield DEFFERED. No UNVERIFIED claims.
