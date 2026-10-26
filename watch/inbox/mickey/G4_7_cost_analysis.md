# G4-7 — V4.1 FLASH COST DEEP-DIVE: three lanes, one curve (2026-09-11, zcode seat)

THE POINT: three independent lanes measured V4.1 Flash (deepseek-flash) on the
viral shopping-task class, and the numbers form a curve, not three data points:
**each fix made the task both cheaper AND more correct.** $/task fell 17.3%
across three iterations while cart completion went 0/3 → 0/2 → 3/3. The prompt
fix had NEGATIVE marginal cost — it saved $0.000053/task while flipping
completion from 0 to 3/3, taking cost-per-completed-task from undefined
(infinite) to **$0.000439 — 112x under the viral $0.049**. All figures below
are receipted in `logs/provider_usage.jsonl`; the viral numbers are taken as
given (no primary source fetched by any lane — flagged in every card).

---

## 1. The cost curve (iterations 1 → 3, all lanes, same fixture)

Fixture constant across all three: seed 42, 200-product mock storefront, 4 local
tools, mission = 3 items under $50 / rating > 4.0 / in stock. Pricing
pre-registered everywhere: input $0.15/M, cache-hit $0.003/M, output $0.60/M.
All fires off-peak (Beijing ~04:2x-04:5x), so flat prices were live prices.

| iter | card | harness shape | $/task | carts completed | cost per COMPLETED task |
|---|---|---|---|---|---|
| 1 | `watch/inbox/v41_paces/LANE7_run.md` | 1 API call, soft budget | $0.000531 | 0/3 | undefined (÷0) |
| 2 | `watch/inbox/mickey/M3_storefront_v2.md` | 2 calls, soft turn-2 | $0.000492 | 0/2 graded (+1 ungraded) | undefined (÷0) |
| 3 | `watch/inbox/mickey/G2_2_storefront_v3.md` | 2 calls, imperative turn-2 | **$0.000439** | **3/3** | **$0.000439** |

The curve is monotonic down on cost and up on completion. That combination is
the finding: correctness work did not buy cost, it PRINTED it.

## 2. Marginal cost of each fix

- **Harness fix (1-call → 2-call, iter 1 → 2): -$0.000039/task (-7.3%).**
  Cheaper despite double the calls. Mechanism: Lane 1's mean carried a fully
  cold run ($0.001359, 8,647-token miss); M3's "cold" call still hit 7,808
  cached tokens — the provider prefix cache survived across days on the
  byte-identical catalog. The harness fix bought the existence of turn 2 at a
  negative price.
- **Prompt fix (soft → imperative turn-2, iter 2 → 3): -$0.000053/task
  (-10.7%). NEGATIVE marginal cost.** The imperative prompt is longer (extra
  user message before call 2) yet landed hotter cache: 90.7% vs 89.3%
  (G2-2 iter 2-3 hit 8,576 vs M3's 8,448 on the same-shaped call). Completion
  flipped 0/2 → 3/3 in the same step — turn-2 composition inverted from
  `get_details x3` (pure verification habit) to `add_to_cart x3`.
- **Cumulative iter 1 → 3: -17.3% $/task**, completion 0/5 graded → 3/3, and
  the deferral failure class (M3's finding) closed as prompt-followable, not a
  depth floor.
- **Whole-arc spend: $0.004387 across 15 receipted calls** — the entire
  three-iteration cost curve cost less than one-ninth of a SINGLE viral-priced
  task ($0.049).

Cache sub-curve across lanes: 97.7% (identical single-call repeats) → 89.3%
(2-call, turn-2 suffix grows) → 90.7% (imperative). LANE3 pins the mechanism:
hit ratio scales with prompt length (93.0% at 2,477 tokens, 78.3% at ~1k; the
trailing partial 64-token block never hits), and cache is a COST play, not a
speed play — the 93% hit call was 252 ms SLOWER end-to-end at that size.

## 3. Speed axis (LANE3)

`watch/inbox/v41_paces/LANE3_speed.md`: measured true decode rate **138-177
tok/s** across 5 streamed calls (best single 176.6). The loop cards measure
44-70 tok/s task-level — that is e2e including TTFT and harness turns, not
decode rate. The viral 295 tok/s claim: **DISPUTED on our surface** (we reach
45-60% of it, cold or warm, no call close). Verdict from LANE3 stands: ~150-175
tok/s decoder with aggressive prefix caching; the marketing speed number is not
on our key.

## 4. Pareto position vs the viral benchmarks

Virals: ego_agent $0.049/task, BridgeMind $0.03/task, both at claimed 295 tok/s.

| axis | viral claim | ours (receipted) | who holds the axis |
|---|---|---|---|
| $/task | $0.049 (unproven) | $0.000439 (112x cheaper); vs $0.03 = 68x cheaper | us, massively |
| tok/s | 295 (unproven) | 139-177 decode | them (on their claim), ~1.7-2.1x |
| completion | unreported | 3/3 measured, $0.000439 per success | us — theirs is undefined |

In 2D (cost, speed) neither point dominates the other, so both sit on the
frontier of the measured set — but the exchange rate is the headline: the viral
point offers under 2x speed for 68-112x cost. Nobody should take that trade for
this task class. Two sharper points:

- **The frontier status of the viral point is UNPROVEN.** No lane fetched a
  primary source; if $0.049 settles anywhere near normal vendor pricing for a
  full loop, it was never a frontier point at all.
- **A benchmark that doesn't report completion has no cost-per-success.** Our
  iter-3 number is the first defined cost per COMPLETED cart in the arc. Any
  comparison at equal definition favors us further.

## 5. The complexity-gap caveat (the honest part)

Our fixture is simpler than the viral benchmarks. Stated plainly:

1. **Loop shape.** Ours: 2 API calls, ~3-5 s wall, static 200-item JSON catalog
   in context, 4 tools the harness executes instantly. Viral: a real storefront,
   minutes-long loop (5 min cited), growing context, likely dozens of turns of
   navigation. Their $0.049 buys a full expedition; our $0.000439 buys two turns.
2. **Same-shape comparison.** Lane 7's derived (explicitly UNFIRED) estimate for
   a full 14-turn loop on OUR fixture was ~$0.006/task. That is the honest gap:
   ~8x under the viral number, not 112x. The 112x compares our 2-turn fixture to
   their full loop. Prices per token are identical — loop DEPTH is the cost
   driver, and ours is shallow.
3. **Quality axis still open.** 3/3 carts were VALID (all constraints met, in
   stock, under budget) but 0/3 matched the cheapest-3 answer key. Completion
   proved prompt-followable; optimal selection is untested. G2-2's named next
   probe (one line: "your score is the cart total") is the cheapest test of it.
4. **Scale.** N=3 per run, one seed, one fixture, one model, off-peak flat
   pricing, temperature 0 (which proved approximate, not deterministic).

## Verdict

We sit at the cheap end of the frontier, with receipts, and every step of the
curve says the lever is prompt/harness shape, not model spend. Claim this card
supports: **the shopping-task class costs tenths of a cent per completed task on
the flash lane once the loop shape and final-turn instruction are right — on our
fixture.** Extending to the viral fixture's complexity is the next measured
step; expect it to move us toward (not to) the ~$0.006 same-shape estimate,
still an order of magnitude under $0.049.

---
Sources: `watch/inbox/v41_paces/LANE7_run.md` (iter 1) ·
`watch/inbox/mickey/M3_storefront_v2.md` (iter 2) ·
`watch/inbox/mickey/G2_2_storefront_v3.md` (iter 3) ·
`watch/inbox/v41_paces/LANE3_speed.md` (speed + cache mechanics).
Receipts: `logs/provider_usage.jsonl`, sessions `lane7_v41_shop_20260910`,
`mickey_m3_storefront_v2_20260910`, `mickey_g2_2_storefront_v3_20260910`.

Filed by MICKEY G4-7 (zcode seat). Compile-only — no API calls spent.
