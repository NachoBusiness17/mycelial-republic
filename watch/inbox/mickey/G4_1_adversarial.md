# G4-1 — V4.1 STOREFRONT ADVERSARIAL-SORT (unsorted results), fired 2026-09-10T21:15Z

THE POINT: **G3-1's 3/3 cheapest-3 was pre-solved by the tool's price sort —
this run shuffles the results and makes the model compare.** Harness
byte-identical to G3-1's fired runner (same fixture seed 42 / 200 products /
42 qualifying, same ONE scoring line, same turn-2 imperative, same 2-call
loop, same grader); the ONLY delta is inside `search_products`: the
price-ascending sort is replaced by a shuffle seeded per iteration
(9001/9002/9003 — different order every run, reproducible).

Result: **selection degrades from 3/3 exact to 2/3 exact.** Carts still valid
3/3, but iter 3 missed the key — swapped rank-2 MS-152 ($5.66) for rank-4
MS-082 ($7.34), total $18.95, overpay $1.68. The honest verdict sits between
G3-1's two outcomes: comparison reasoning is REAL (iters 1-2 found the exact
cheapest-3 with the key scattered mid-list, one item as deep as row 31), but
it is not reliable — a rank-2 item buried at row 22 was missed once in 3.
G3-1's pass was partly tool-assisted; the unsorted feed costs ~1/3 of
exactness and, when it fails, fails CHEAP ($1.68, 9.7% over optimal — vs
G2-2's no-objective overpays of $44.82-56.17).

---

## Per-run results (3 tasks, 2 calls each, deepseek-v4-flash, tier T2, temp 0)

Answer key unchanged since LANE7: cheapest-3 among in-stock, price < 50,
rating > 4.0 → **MS-028 ($4.87, rank 1), MS-152 ($5.66, rank 2), MS-121
($6.74, rank 3)**; 42 qualifying; optimal total $17.27. `key positions` =
row of each key item inside the SHUFFLED result the model actually received.

| task | seed | key positions in shuffled result | cart (exact?) | cheapest-3 | ranks | cart total | overpay | cost |
|---|---|---|---|---|---|---|---|---|
| 1 | 9001 | MS-152 **2**, MS-028 10, MS-121 31 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000468 |
| 2 | 9002 | MS-028 10, MS-121 12, MS-152 **31** | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000502 |
| 3 | 9003 | MS-121 3, MS-028 4, MS-152 **22** | MS-028, **MS-082**, MS-121 — miss | no | 1,**4**,3 | $18.95 | **$1.68** | $0.000468 |
| **mean** | | | | **2/3** | | $17.83 | $0.56 | **$0.000479** |

Total **$0.001438 for 6 calls** (cap hit exactly, 0 retries). Cache hit
89.9% mean — the fixture prefix stays warm (5th consecutive SUPPORT).
Search args per run: iters 1+3 `{query:"", max_price:49.99, min_rating:4.01,
in_stock_only:true, limit:200}`, iter 2 `{max_price:50, min_rating:4.0,
in_stock_only:true, limit:60}` — same split as G3-1.

## The mechanism: a visibility miss, not a truncation miss

- **Full visibility in all 3 runs**: `n_returned == n_matches` every time
  (42 / 48 / 42). The model's own limits (200/60) covered the whole result.
  The adversarial-sort fixture isolated COMPARISON — no limit truncation
  confound (that remains a separate unfired probe from G3-1's list).
- **Iter 3's miss is attention, not data.** MS-152 was IN the returned list
  at row 22 and the model picked rank-4 MS-082 instead. It scanned well
  enough to get ranks 1 and 3 (MS-121 was at row 3, MS-028 at row 4 — both
  near the head), then filled the third slot from a nearby cheap item rather
  than the true rank-2 buried 22 rows deep.
- **Iter 2 is the strongest pro-comparison data point**: the key sat at rows
  10/12/**31** — nothing in the head cheaper than $7.34, the top-3 by price
  nowhere adjacent — and it still produced the exact optimal cart. That is
  genuine list-wide price comparison, not head-grazing.
- **No monotonic position story.** Iter 2 found MS-152 at row 31; iter 3
  missed it at row 22. Temperature 0, so this is input-order-dependent
  attention noise, not sampling noise. With n=3 the miss rate is 1/3 with a
  wide error bar; the DIRECTION vs G3-1 (3/3 → 2/3) is the finding, the
  precise rate is not.

## Verdict: comparison reasoning is real but shallow; the sort was doing real work

- **G3-1's "selection is prompt-followable" — SCOPED.** At this prompt
  strength, the one scoring line flips the objective either way, but exact
  optimality was partly tool-assisted: with the sort handing over the head,
  3/3; with the sort removed, 2/3. The line aims the model at "cheapest";
  whether it can EXECUTE cheapest depends on the tool's cooperation.
- **Comparison reasoning exists but has a finite attention depth** on a
  42-item unsorted list: it beats head-grazing decisively (iters 1-2 exact
  with key mid-list; G2-2's no-objective runs picked rank-6+ items even from
  a SORTED head), but drops a buried rank-2 once in 3. The floor is not
  "no comparison" — it is "comparison that fades with row depth."
- **Failure mode when it breaks is graceful**: overpay $1.68 vs G2-2's
  $44.82-56.17. The objective line still constrains the search even where it
  misses the optimum — ranks 1,3,4 is a near-optimal cart, not a random one.
- **Instruction compliance, third consecutive confirm**: "State your
  selection criteria" ignored 0/3 again (turn-1 one-liners, turn-2 text
  empty, all 105 completion tokens spent on the three add_to_cart calls).
  The turn-2 imperative outranks every prose duty, unsorted feed or not.

## Tri-state ledger updates

- G3-1 SUPPORTED finding (scoring line → 3/3 exact) — **SCOPED**: holds
  under price-sorted results; under shuffled results the same line yields
  2/3 exact + 1 near-miss. Selection quality = objective line x tool
  presentation, not the line alone.
- New finding, **SUPPORTED (2/3 exact, directional)**: cheapest-3 selection
  survives an adversarial shuffle better than chance or head-grazing but is
  not sort-independent; row-depth attention decay is the failure surface.
- Cache affinity on agentic loops: **SUPPORTED a 5th time** (89.9% mean).
- Verification habit still absent: 0 get_details / 0 compare in 6 calls —
  the model compared prices by reading the unsorted list, not by calling
  compare. Reasonable, but notable: the compare tool stayed dead weight.
- G3-1's limit confound (wider net under the scoring line): persists here
  (limit 200/60/200) — still not proven causal; still noted.

## Named next probes (unfired — call bound spent)

1. **N=9 same fixture** to size the miss rate (1/3 vs 1/6 changes the
   verdict from "unreliable" to "mostly reliable"); ~$0.003.
2. **Decoy-head fixture**: sort by RATING ascending the qualifying list so
   the head is full of high-rated expensive items — tests whether head
   anchoring or depth decay is the dominant failure mode.

## Method and receipt trail

- Client: `models.providers.chat_messages`, provider `deepseek`, model
  `deepseek-v4-flash`, tier T2, temperature 0, max_tokens 1024, thinking
  disabled at provider level, `tool_choice=auto` — identical to G3-1.
- Fixture: bit-for-bit identical to LANE7/M3/G2-2/G3-1 (seed 42, 200
  products, 42 satisfying, key MS-028/MS-152/MS-121, optimal $17.27).
  Zero-API dry run verified pre-fire: key + optimal total printed, shuffle
  positions for all 3 seeds shown (key never at rows 1-2), 0 calls fired.
- Loop shape byte-identical to G3-1's fired runner. Delta precisely: in
  `exec_tool("search_products")`, `hits.sort(key=price)` replaced by
  `random.Random(9000 + iteration).shuffle(hits)`. Grader unchanged
  (cart-based; cheapest3_match primary; overpay_vs_optimal).
- Exactly 6 API calls fired (the pre-registered cap), all ok, 0 retries.
  Ledger rows carry `session_id=mickey_g4_1_adversarial_20260910` in
  `logs/provider_usage.jsonl` (6 rows verified digit-for-digit against
  stdout; row 1: pt 8725 / ct 119 / hit 8576 / miss 149). Key never echoed.
- Raw results: `C:\Users\foste\AppData\Local\Temp\g4_1_results.json`;
  runner: `C:\Users\foste\AppData\Local\Temp\g4_1_runner.py`.
- Bounds respected: one script, one results file, 6 deepseek calls
  (pennies — $0.001438).

Filed by G4-1 fire (zcode seat, Mickey group 4, task 1). Predecessor:
`watch/inbox/mickey/G3_1_cart_quality.md` (this is G3-1's named NEXT, fired
as specified: same harness, unsorted results).
