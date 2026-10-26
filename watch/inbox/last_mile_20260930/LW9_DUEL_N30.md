# LW9 - DUEL SERIES n=30 CLOSEOUT - 2026-09-30

Mission (Z2_DUEL_N30.md next step 1 + operator last-mile brief): run the
remaining ~9 duels through the existing harness to n=30, then report the
final tally, the CI verdict (does it exclude zero?), and whether the Z2
slot-A position-bias finding (13 of 20 first-position wins) holds. Budget
$1.50 for this window. File ownership: rows in logs/duel/duels.jsonl plus
this receipt.

## What landed

- `watch/inbox/last_mile_20260930/lw9_duel_series.py` (new driver, exact
  X4/Z2 shape): imports tools/duel_harness.py v1.1 (blind judge, parity
  slot swap, style counts), width-1 sequential, idempotent ask_id skip,
  hard budget guard ($1.50 cap, $0.16/duel worst-case projection). 9
  fresh asks on artifacts never used by X4/Z2: 2 adversarial-review
  (tools/violation_ratchet.py, SHARED_SURFACE_CONTRACT.json +
  mag/shared_surface.py), 2 planning (contender-source refactor per
  memory/rib/RIB_DRIVING_LADDER_20260928.md, warm-boot 302 resilience),
  2 schema-design (warm_state.json v2, duels.jsonl row v3), 1 grading
  (tools/freshness_check.py vs its own docstring), 2 code-analysis
  (mag/hermes_warm_boot.py, mag/shared_surface.py defect hunt).
- 9 rows appended to logs/duel/duels.jsonl, ids `lw9-*`; ledger now 31
  rows. Swap alternated perfectly (F/T x4 + F, continuing ledger
  parity). Zero em-dashes in all 31 rows (byte check chr(0x2014)). No
  retries, no UNPARSED, exit 0.

## VERDICT: window glm 5 - qwen 4; BLIND ERA n=30 glm 17, qwen 12, TIE 1

| ask_id | winner | shape | cost |
|---|---|---|---|
| lw9-adv-ratchet | A qwen | adv | $0.1517 |
| lw9-adv-shared-surface | B glm | adv | $0.1105 |
| lw9-plan-harness-refactor | A qwen | plan | $0.1546 |
| lw9-plan-warm-boot-resilience | B glm | plan | $0.0903 |
| lw9-schema-warm-state | B glm | schema | $0.1316 |
| lw9-schema-duel-row-v3 | A qwen | schema | $0.1210 |
| lw9-grade-freshness | B glm | grade | $0.0991 |
| lw9-code-warm-boot | B glm | code | $0.1024 |
| lw9-code-shared-surface | A qwen | code | $0.1561 |

Blind-era shape totals (30 rows): adv B4/A3/T1, plan B4/A3, schema B4/A2,
grade B3/A1, code B2/A2. glm leads or ties every shape; code is even.

## CI verdict: DOES NOT exclude zero

Denominators named (census law): tally read from logs/duel/duels.jsonl
at 2026-09-30 post-run; blind era = 30 rows (all rows with the v1.1 swap
field; the unblinded v1.0 retro row 0 is excluded), of which 29 live + 1
blind retro rejudge. glm 17 of 29 decided (58.6 percent). Exact binomial
two-sided p = 0.4583 (one-sided 0.2291). Clopper-Pearson 95 percent CI
for the glm win rate: [0.3894, 0.7648] (bounds verified: CDF at each
bound equals 0.975/0.025). On the difference (p_glm - p_qwen) that is
[-0.2213, +0.5295]: the interval STRADDLES ZERO. At n=30 the mild glm
edge remains indistinguishable from a coin. No router row is justified
on skill alone; the W3 consequence line stays flagged.

## Slot-A bias: HOLDS and crossed the 0.05 line

Z2 flagged 13 of 20 live first-position wins (p=0.1316 one-sided). At
n=30 (29 live duels): slot A won 19 of 28 decided (67.9 percent),
one-sided exact binomial p = 0.0436. Per contender: glm from slot A went
11-3, from slot B 6-8-1; qwen from slot A went 8-7, from slot B 3-11.
Both contenders roughly double their win rate from slot A, so this is
first-position favoritism in the ember judge, not model skill. The
parity swap did its job (glm sat slot A 14 times, slot B 15; banked
winners are logical-contender-remapped and unaffected), but any future
router row must be position-debiased first (order-randomized double
judging or a slot term in the regression).

## Costs (metered from usage.cost in banked rows)

- This window: $1.1173 of the $1.50 cap (mean $0.124/duel; the two
  16k-char asks were the pricey ones). Ledger total across 31 rows:
  $3.3777. qwen remains the cost driver (~2.4x glm per duel this
  window).
- Style control (29 live blind rows): qwen mean 8,153 chars / 295
  headers vs glm 6,193 / 141. qwen writes ~32 percent more and 2.1x the
  headers and still does not convert volume into verdicts.

## OWED DEBT (operator driving-ladder law, 2026-09-28)

glm-side answers should come from this account's Task agents when
possible. The harness is API-shaped (Nous both halves) and qwen + judge
need Nous regardless, so pragmatic v0 fired glm through Nous too: the
glm half of this window cost $0.2158 on Nous (sum of lw9 b_cost), the
pennies waste the operator already priced in. The real fix is the
contender-source interface refactor (pluggable source: API call or
local Task agent), already spec'd as the lw9-plan-harness-refactor duel
ask; owed, not papered over here.

## Next steps (n=30 reached)

1. Alternate-judge retro sensitivity check (~$0.03, retro mode over
   banked answers) before anything downstream trusts ember-only
   verdicts; the slot-A result is one reason to want a second judge.
2. Position-debias protocol (double-judge with randomized order, or slot
   term in the style regression) before any router row rewrite; the CI
   verdict independently says no rewrite today.
3. Land the 70/30 hidden ask-bank split (schema designed this window in
   lw9-schema-duel-row-v3 groundwork) if the series extends past 30.
