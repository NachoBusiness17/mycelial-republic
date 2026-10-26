# WIDTH LEDGER v1 — THE STANDING CONCURRENCY INSTRUMENT — 2026-09-26

Born from the operator order: "what's the max concurrence between flash and regular glm... maximizing our work, keeping models useful and cheap." Self-steal of the census-carrier pattern: one living table, receipt-cited rows only, session data banked on entry (unbanked claims rot into folklore per the B2-476 unanchored-rows lesson).

## THE TABLE (receipt-cited where cited; session-banked rows marked SB)

| lane / transport | measured clean | first failure | throughput | confidence |
|---|---|---|---|---|
| Main GLM-5.3-Flash, Task agents (maxAttempts 11) | 3, 6, 10, 12 | ~15 (2 deaths, refired ok); 12 post-burst 1302-holds until window decays | 109.4M tok/h at width 10; 85.6M wave 2 | HIGH (B2-25, AFTERPARTY_CLOSE B2-476, GALA) |
| Main acct, workflow children (maxAttempts 0) | law caps 3; SB: 50 children (5x10) ran hours before first 429, held not died | 9/25 50-wide storm (tether-confounded, 11 terminal actors) | n/a | MEDIUM (storm receipt-cited; the hours-clean 50 is SB) |
| Lite/start-plan lane, workflow children | SB: 20 (2 veins x 10) no contact; 12 lanes x 4-wide 9/12 clean, pennies | none observed | n/a | LOW |
| Hermes/Nous credits | SB: 6 parallel workers to completion (150/150) | none | n/a | LOW |
| Free external lanes (OpenRouter/Cohere/DeepSeek) | SB: 12 workers clean; OpenRouter holds 18 free lanes x 1000/day | none; Mistral direct DEAD (limit-0, B2-61) | n/a | LOW |
| Regular (non-flash) GLM | NOTHING: zero data in the entire estate | n/a | n/a | DARK |

Key reframing (B2-98 tally JSONs): "clean" means zero terminal failures, NOT zero rate-limit contact. Width 10 rode on 129+35 absorbed 1302 retries; one session carried 1,780 429/1302 events with 1,741 absorbed. Width works because retry absorbs; the binding constraint is ROLLING THROUGHPUT, not width. Record burst state (fresh vs post-burst) with every width claim.

## THE STAGED PROBE PLAN (single wave per rung, no refire inside a probe: the death is data)

- Stage 0 (done at filing): bank today's session data (this document).
- Stage 1: Task width 15 per the armed B2-97 card (GO check: python tools/operator_go.py width-15). Kill on any terminal or surfaced 1302. Measure via provider_error_tally (clean claim without the tally is VOID per B2-436).
- Stage 2: workflow children 5x8 (40) on a stable link. Kill: any child 429/1302 death = pull to 5x5. Success = first receipt-cited clean workflow rung, amends the 3-cap law append-only.
- Stage 3: lite lane 3x10 = 30. Kill: first surfaced 429 on that lane = revert to 20.
- Stage 4: Hermes 6 -> 12. Kill: any worker death or credit anomaly (rescue lane, do not cook it).
- Stage 5: free lanes 12 -> 18 via lane-pinning (one worker per distinct OpenRouter free lane; per-lane kill, global revert only if 3+ lanes 429 simultaneously).
- Stage 6: off-peak A/B: refire the first-failing width off-peak (flash quota multiplier 0.4x off-peak vs 1.2x peak per TETHERED_LINK_STEAL) to measure the multiplier instead of guessing it.

## ANSWER WITH HONEST BOUNDS (today)

- Flash Task agents: 10 sustained, 12 fresh, 15 where deaths start. Already in constant silent contact; 12 is burst-gated, not free.
- Workflow children: program against the 3-cap law until Stage 2 banks a clean rung; the hours-clean 50 says the real line is near 50 on a stable link but it is unbanked.
- REGULAR GLM vs FLASH: the honest surprise: regular GLM concurrency has NEVER been measured on this account; every wave in the estate is flash. The only documented asymmetry is the quota multiplier. A Stage-1-style baseline wave on regular GLM is owed before any flash-vs-regular routing claim.
- Other models: Hermes safe 6; free lanes safe 12, stretchable 18; Mistral direct dead.
- Fleet-wide today: roughly 50+ concurrent model calls across all lanes simultaneously without terminal loss. Cheapest unexploited capacity: free lanes (18 exist, 12 used) and the lite lane (unbanked headroom above 20).

## ROUTER RULE (head of the ledger, from the LANE panel doctrine)

Per wave, one question: is the binding constraint COST or JUDGMENT? Cost -> lite/free lanes. Judgment -> heavy/Hermes. Routing is per-run and per-organ, never per-subscription.
