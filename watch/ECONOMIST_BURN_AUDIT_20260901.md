# ECONOMIST BURN AUDIT — 2026-09-01 EOD (17:29Z)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: 09-01 burn ≈$6 vs ~$48 pooled (~9d runway); cache misses (6.1% of tokens) drive 46% of the bill — SUPPORTED (measured per-source table, receipts cited) · falsifier: lane ledgers/balances disagree with the audit's MEASURED rows on recheck
*Economist seat — half Satoshi, half Friedman. Every number MEASURED (source) or labeled ESTIMATED.*
**Operator frame:** exponential-curve velocity; cash recoverable, time scarce. **Ceiling law:** $3/day hard w/o operator word (vast = operator word, spent).

---

## (a) TODAY — full-UTC-09-01 total burn ≈ **$6.00**

| leg | $ | type |
|---|---|---|
| DeepSeek main (deepseek-v4) | ~$4.34 | MEASURED $2.66@08:00ET-cutoff + evening cont. |
| DS gated lanes | $0.064 | MEASURED |
| together | $0.0053 | MEASURED |
| vast (terminated 17:17Z) | $0.91 | MEASURED |
| gauntlet W1+W4 (tonight) | $0.08 | PLANNED |
| vast re-rent (~$1 × 50% corpus) | $0.50 | CONDITIONAL (exp.) |
| **TOTAL** | **≈ $6.00** | |

Not today: z.ai −$1.26 (probe era, prior), other −$9.90 (drift night, prior). That burn is sunk, reflected in balances.

## (b) FORECAST next 24h at current lane intensity
- **Elevated (today's realized): $5.00–6.00/day.** Vast+gauntlet dominate variance; sleep/vacancy exempt.
- **Steady (no vast/gauntlet, together parallel + W4 + census + main session): $2.40–2.60/day** — DeepSeek 7-day avg $2.39 is the spine; H=93.9% cache is the leash.

## (c) RUNWAY vs remaining balances (EOD 09-01)

| reservoir | balance | burn @continuity | runway |
|---|---|---|---|
| DeepSeek | $19.46 (23.86 − 4.40) | $4.40/d (driver) | **4.4 d** pre-top-up |
| z.ai | $8.74 | ~$0 (probe done) | reserve |
| other (billed lane) | $20.10 | ~$0 now | reserve |
| **pooled usable** | **$48.30** | $5–6/d | **8.1–9.7 d ≈ 9 d** |

**Headline:** not close to a $20 burn today (~$6). Pooled runway ~9 days before top-up. DeepSeek alone tops out in ~4.4 days at current driver burn — that's the reservoir to watch, and it's pooled-cash covered.

## PHYSICS — where the bill actually concentrates (DeepSeek 7d)
- **Cache-miss is the entire game:** **6.1% of tokens → 46% of bill.** Warm/cached tokens are near-free ($0.03), cold hits are the fuel tank. Blend $0.034/1M only holds while cache holds.
- **H=93.9% of bill is the cache-hit share driving value** — keep long sessions warm; a cold restarts throwaway the whole prefix.
- **output = 24% of bill** — output (reasoning-write) is the second lever; output compression already saving ~24%.

## POLICY (operator frame: time scarce ≫ cash recoverable)

**BUY VELOCITY, METER WASTE.** Do NOT gate the productive driver (main session, DeepSeek warm-prefix, together parallel). The burn is ~$6 against ~$48 pooled with 9-day runway — under ceiling, cheap vs what it buys.

**Meter — 3 waste gates, not token counts:**
1. **Cache-miss ratio** (6.1%→46% law). Cold starts and prefix-thrashing are the real cost. Keep steady traffic on DeepSeek/lane warm; move burst/scut to $0 free lanes (cerebras 1M TPD, groq, openrouter, zai-pro plan).
2. **Vast & gauntlet = conditional only.** Do NOT pre-rent. vast re-rent gated on corpus arrival (the 50% arm is optional spend, not committed). gauntlet $0.08 is cheap — allowed.
3. **Billed zai API lane demoted to LAST** (ROUTE §3a). It is the only per-token-dollar lane left live; reasoning_effort default `low` (ROUTE §3b) halves its output spend.

**Cap:** pooled burn cap ~$8/day operator-word line. Today at $6 ≈ under. Re-metering trigger: if pooled < $30 (≈5d avg) OR DeepSeek < $15, stall non-driver lanes before top-up. Top-up priority = DeepSeek (driver spine).

**Compounding yes / waste no:** DS warm-prefix session + cache-mined lanes (cache hits = compounding, near-$0 marginal output) = buy more. Cold restarts, pre-renting vast, billed-API session traffic = waste. Route per COST LAW: driver does the valuable work; gophers eat scut free.

*End. ~$6 today, ~9 days pooled runway, under the $3 hard day ceiling only on vast operator-word carve-out. No novel, only receipts.*
