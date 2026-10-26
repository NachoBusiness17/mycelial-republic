# ECONOMIST CHECK — the 50x / 150% / 94-99% claim (Sep 6, 2026, no handwaving)

*Operator demand: economist-check the claim "50x flash-5.3 agents at 150% quota at 94-99%
token price reduction" before it goes to @LilithDatura, who asked "explain to us what this
is" (04:14Z) and followed with "sounds like compression is happening across the board" (04:37Z).*

## THE CLAIM, DECOMPOSED (each piece judged against fleet receipts)

| Piece | Verdict | Basis |
|---|---|---|
| 8 concurrent flash agents | **PROVEN** | width-8 run (09-06, verified): 8/8 success, 0 rejections, 4.45x wall speedup, 7.43M tok, peak 7 in-flight |
| 50 concurrent agents | **UNPROVEN** | untested past 8; the Sep-4 concurrency law puts vendor walls at ~50 — 50 is AT the wall, not past it. Efficiency also decays: 8x agents gave 4.45x wall (launch skew) |
| 150% quota | **DEFINABLE, LAWFUL VIA AGGREGATION** | quota pools are PER-SEAT; multi-seat fan = lawful 200%+ of one seat. "150%" must name its base (150% of WHICH seat's pool) or it's noise |
| 94-99% token price reduction | **ARITHMETICALLY SUPPORTED, PER-TOKEN** | the compound: flash pricing vs 5.3 (~3x cheaper ≈ 67%), cache-hit pricing (~90% on cached tokens; our miner receipted 99.5% hits), in-window promo ($0 on those tokens). Compounded ≈ 94-99% ON CACHED FLASH TOKENS |

## THE HANDWAVE TRAP (what the claim hides)
**Agent count is not a throughput multiplier.** 50 agents on one pool = each gets 2% of the
pool. The POOL is the bottleneck; only seats multiply pools. And the refeed tax bounds the
price reduction: input tokens at 240:1 still bill (at cache rates ~0.1x), so the blended
reduction on the whole bill depends on the hit fraction — 94-99% holds only on the cached
slice, not the uncached tail.

## THE ECONOMIST'S VERSION (the no-handwave reply)
"50 concurrent GLM-5.3-Flash agents — proven to 8 concurrent (4.45x wall speedup, 0
rejections), 50 is untested and sits at the vendor wall. 150% of a single plan's daily
quota, lawfully aggregated across seats, because quota pools are per-seat. The price
reduction is real and compound: flash pricing, cache hits receipted at 99.5%, and the promo
window — 94-99% on cached tokens. The pool is the bottleneck, not the agent count: the
agents share the pool, the seats multiply it. That's the whole trick. Compression across
the board = the record getting cheaper to keep than to lose."
