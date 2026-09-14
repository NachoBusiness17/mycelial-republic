# ZAI LITE PLAN LAW — one-week right-sizing (2026-09-01 04:48Z)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the ~10k credits/week Lite pool only stretches under three laws — off-peak only, flash for scut with salon (not 5.3) escalation, never cold-long-context on 5.3 — SUPPORTED (credit arithmetic receipted in card; multipliers flagged ESTIMATED pending calibration probe) · falsifier: stated in card metering — the first calibration probe computing real multipliers that diverge from the ESTIMATED table amends the law

Pool: ~10,000 credits/week · 2,000 rolling per 5h (use-it-or-lose-it per bucket) · resets every 7 days from unlock.

## The three laws
1. **OFF-PEAK ONLY.** Peak = Mon–Fri 06:00–10:00 UTC = 3.5–4.3× the credits (Flash 1.2× vs 0.4×; 5.3 3× vs 1× on legacy table). Weekends = all-day off-peak. If a call can wait, it waits.
2. **FLASH FOR SCUT; ESCALATION = THE SALON, NOT 5.3** (operator correction 05:02Z). No single model — 5.3 included — beats the tandem brought in for their gifts (Grok/GPT/Claude/Mistral/DeepSeek + seats in tandem), each maximized for its gift, internal gap analysis implicit — never duplicated. We ask and steer by knowing deterministically what we desire from the stochastic. 5.3's honest gift on this plan: the coding endpoint's native agentic model — deterministic steered tool loops in zcode, cache-mined batches. Unknown-data extraction goes to the tandem with deterministic asks; 5.3 is a seat, not a brain.
3. **NEVER COLD-LONG-CONTEXT ON 5.3.** Cached input is NOT free on plan credits (1.7 vs 6.9 mult, 24.6% of fresh). A single cold 100k-context 5.3 call ≈ 70+ credits ≈ 0.7% of the whole week. Long reads stay on zai-pro Max / DeepSeek cache; Lite gets frozen-prefix work only.

## Weekly allocation (arithmetic receipt, xai sandbox 04:47Z)
| slice | credits | mode | calls/week | calls/day |
|---|---|---|---|---|
| 80% | 8,000 | Flash off-peak | ~17,400 (est) | ~2,500 |
| 15% | 1,500 | 5.3 off-peak — ONLY deterministically-steered coding/tool work | ~258 | ~37 |
| 5% | 500 | reserve / peak emergencies | — | — |

Pacing: ~1,428 credits/day = one 5h bucket covers a day with headroom. Spread across buckets; a bucket unspent for 5h evaporates. Don't binge one window.

## Seat routing
- **zcode (coding CLI):** default GLM-5.3-Flash; escalate to GLM-5.3 only per law 2. This is the primary Lite consumer.
- **Main session:** NO — stays zai-pro (Max, funded, $0-marginal) per ECONOMIST_ROUTE (a). Lite is not the driver.
- **Gopher overflow:** Lite Flash as burst lane ONLY when cerebras (1M TPD) + groq quotas dry. Harvest/steering lanes stay on their existing $0 lanes — don't burn plan credits on what's already free.
- **zai-2 coding endpoint (old 1310 wall):** if this unlock IS that key's reset, same laws apply; if separate, prefer the fresh pool and leave the 09-02 12:52Z reset as backstop.

## Metering (better-by-default ladder)
- First live call = calibration probe: capture usage fields, compute real mults, replace ESTIMATED above, amend this file via index_fold.
- Log burn per session: `node` one-liner append to `/board/zai_lite_burn.jsonl` {ts, seat, est_credits}. Weekly review: if reserve dips <5% before day 6, cut Flash slice 10%.
- Dead-query law: a use pattern that yields INFLATED/UNVERIFIED results 2× gets demoted off Lite to free lanes.

## What Lite is NOT for
Main-session driving · cold-context document reads · steering loops (already $0) · harvest (already free) · **the escalation rung (the salon tandem is; 5.3 is not the brain)** · anything billable elsewhere at $0.
