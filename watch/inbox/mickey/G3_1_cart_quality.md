# G3-1 — V4.1 STOREFRONT CART QUALITY (the cheapest-3 scoring line), fired 2026-09-10T21:06Z

THE POINT: **optimal selection is prompt-followable too — one line flipped cart
quality from 0/3 to 3/3 exact.** Harness byte-identical to G2-2's fired v3
(same fixture, same 2-call loop, same turn-2 imperative in system + user
message); the ONLY delta is one line appended to turn 1's MISSION RULES:
"Prefer the cheapest items that satisfy all constraints. State your selection
criteria." Result: **3/3 carts completed AND 3/3 exact cheapest-3 matches** —
every run picked MS-028 / MS-152 / MS-121, the exact answer key, cart total
$17.27 = optimal, overpay $0.00. G2-2's same harness without the line went 0/3
on cheapest-3 (totals $73.44 / $62.09 / $73.44, overpays of $44.82-56.17).
Cost of quality: **$0.000511/task mean (+16.4% vs G2-2's $0.000439)**, still
~96x under the viral $0.049. Total **$0.001533 for 6 calls**, cap hit exactly,
no retries. The coordinator's question — "if not, the real floor is reasoning"
— resolves: selection was NOT the floor. The floor question moves elsewhere
(see Verdict).

---

## Per-run results (3 tasks, 2 calls each, deepseek-v4-flash, tier T2, temp 0)

Answer key (pre-registered, unchanged since LANE7): cheapest-3 among in-stock
items with price < 50 AND rating > 4.0 → **MS-028 ($4.87, rank 1), MS-152
($5.66, rank 2), MS-121 ($6.74, rank 3)**; 42 products qualify; optimal total
$17.27. Graded from executed calls, identical grader to v2/v3 plus two new
fields: `cheapest3_match` (was a bonus stat) and per-item price rank among the
42 qualifying products sorted by (price, asin).

| task | turn 1 | turn 2 | cart (exact key?) | pass | cheapest-3 | ranks | cart total | overpay | criteria stated? | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | search_products | add_to_cart x3 | MS-028, MS-121, MS-152 — **exact** | PASS | **YES** | 1,3,2 | $17.27 | $0.00 | no | $0.000563 |
| 2 | search_products | add_to_cart x3 | MS-028, MS-121, MS-152 — **exact** | PASS | **YES** | 1,3,2 | $17.27 | $0.00 | no | $0.000502 |
| 3 | search_products | add_to_cart x3 | MS-028, MS-121, MS-152 — **exact** | PASS | **YES** | 1,3,2 | $17.27 | $0.00 | no | $0.000468 |
| **mean** | | | | **3/3** | **3/3** | | **$17.27** | **$0.00** | **0/3** | **$0.000511** |

Search args per run (the mechanism): iters 1+3 `{query:"", max_price:49.99,
min_rating:4.01, in_stock_only:true, limit:200}`, iter 2 `{max_price:50,
min_rating:4.0, in_stock_only:true, limit:60}`. The harness sorts search
results price-ascending, so the answer key sat at rows 1-3 of every result.
Zero get_details, zero compare — the verification habit stays gone (6/6 calls
across both v3-shape runs).

Per-call raw (all receipted in `logs/provider_usage.jsonl`, session
`mickey_g3_1_cart_quality_20260910`, 6 rows, token totals match stdout
digit-for-digit):

```json
iter 1: t1 {pt:8725,  hit:7936, miss:789,  ct:119, wall:2.048, cost:$0.000214, tools:["search_products"]}
        t2 {pt:10563, hit:8832, miss:1731, ct:105, wall:1.525, cost:$0.000349, tools:["add_to_cart","add_to_cart","add_to_cart"]}
iter 2: t1 {pt:8725,  hit:8576, miss:149,  ct:116, wall:1.595, cost:$0.000118, tools:["search_products"]}
        t2 {pt:10796, hit:8832, miss:1964, ct:105, wall:1.734, cost:$0.000384, tools:["add_to_cart","add_to_cart","add_to_cart"]}
iter 3: t1 {pt:8725,  hit:8576, miss:149,  ct:118, wall:1.348, cost:$0.000119, tools:["search_products"]}
        t2 {pt:10562, hit:8832, miss:1730, ct:105, wall:1.323, cost:$0.000349, tools:["add_to_cart","add_to_cart","add_to_cart"]}
```

Cache hit 88.8% mean across 6 calls — the fixture prefix stays warm across
runs and days (4th consecutive SUPPORT). Task wall 2.7-3.6 s; task tok/s
62.7-83.5 (parity FAIL vs viral 295, as pre-registered every lane).

## The decisive comparison: same information, different objective

G2-2's traces show its model fired essentially the same constraint filters and
received the SAME price-sorted head:

| | G2-2 (no scoring line) | G3-1 (one scoring line) |
|---|---|---|
| turn-1 filters | max_price 49.99-50, min_rating 4.0-4.01, in_stock_only (all 3) | identical (all 3) |
| result head seen | MS-028 $4.87, MS-152 $5.66, (MS-121 $6.74) — rows 1-3 | identical |
| picked | MS-197 $15.17, MS-022, MS-018 (ranks 6+) | **MS-028, MS-152, MS-121 (ranks 1-3)** |
| cart total | $62.09-73.44 | **$17.27** |
| constraint valid | yes 3/3 | yes 3/3 |

The top-3 were visible in both runs' tool output (row 1 of the result, byte
for byte). Constraint-encoding reasoning — the only real reasoning step — was
already correct in ALL six calls across both runs. What the one line changed
is not reasoning depth; it is the OBJECTIVE the model optimized while reading
an already-sorted list: "take three qualifying" (arbitrary) became "take the
head." One trivial inference stands between the line and the action — cheapest
= top of a price-sorted list — and it fired 3/3.

## Verdict: selection is prompt-followable; the residual floor is tool-shaped reasoning, untested

- **Cheapest-3 selection is prompt-followable at this prompt strength, same as
  completion was.** No reasoning floor is established at THIS fixture: the
  model never had to compare anything, because the tool's fixed
  price-ascending sort pre-solved the optimization and the line just aimed the
  model at the head. Call it tool-assisted optimality.
- **Where the real reasoning floor would live, untested:** a fixture where the
  sort does not hand over the answer — unsorted or rating-sorted results, a
  limit that truncates the cheapest items, or coupled constraints where the
  head is wrong. There, "cheapest 3" requires the model to compare prices
  itself. That probe is the honest test of "selection as reasoning," and it is
  ONE fixture tweak away (same harness, same 6 calls).
- **Instruction compliance 2-of-3 clauses, again:** "State your selection
  criteria" was ignored 0/3 — turn-1 text was a one-liner ("I'll search for
  qualifying products in one pass.") and turn-2 text was empty in all 3 runs
  (all 105 completion tokens spent on the three add_to_cart calls, same as
  G2-2). The turn-2 imperative outranks ALL prose duties, including new ones.
  Grading stays cart-based, so passes stand; the reporting clause is dead
  weight under this register.
- One honest confound, sized: G3-1's model asked for more headroom (limit
  200/60 vs G2-2's 30). Not the delta — the top-3 sat inside both runs'
  result heads — but the scoring line may also have made the model pull a
  wider net. Unproven either way; noted for the next fixture.

## Tri-state ledger updates

- G2-2's bonus stat "0/3 cheapest-3 matches; never hit in any prior lane" —
  **SCOPED**: true without a scoring objective; DISPUTED as a model limitation
  once the objective is one line long.
- New finding, **SUPPORTED (3/3)**: a single turn-1 objective line
  ("Prefer the cheapest items that satisfy all constraints.") flips optimal
  selection 0/3 → 3/3 exact at +16% cost per task. Selection quality was a
  missing objective, not a capability floor.
- G2-2's "compliance cost the prose" — **SUPPORTED and generalized**: the
  imperative outranks every prose duty; a NEW prose clause added the same
  night was ignored 3/3 the same way.
- Cache affinity on agentic loops: **SUPPORTED a 4th time** (88.8% mean; cold
  call still hit 7,936 tokens off the G2-2 prefix).
- Temperature-0 non-determinism: **SUPPORTED again** — near-identical prompts,
  identical carts (picks fully converged this time), ct 119/116/118.
- Verification habit (v2 finding, scoped 09-10): still absent under the
  imperative register — 0 get_details / 0 compare in 6 calls.

## Named next probe (unfired — call bound spent)

**The adversarial-sort fixture:** same harness, same scoring line, but the
search tool returns results UNSORTED (or rating-sorted), so cheapest-3
requires the model to compare prices itself. 6 calls, ~$0.0015. If it still
hits 3/3, selection reasoning is real and the arc's floor is closed; if 0/3,
G3-1's pass was tool-assisted and the true depth floor is comparison
reasoning — which no prompt line of this size will patch.

## Method and receipt trail

- Client: `models.providers.chat_messages`, provider `deepseek`, model
  `deepseek-v4-flash`, tier T2, temperature 0, max_tokens 1024, thinking
  disabled at provider level, `tool_choice=auto` — identical to G2-2 v3.
- Fixture: bit-for-bit identical to LANE7/M3/G2-2 (seed 42, 200 products, 42
  satisfying, key MS-028/MS-152/MS-121) — zero-API dry run verified pre-fire
  (0 calls, key + optimal total $17.27 printed before any request).
- Loop shape: identical to the fired v3. Delta precisely: ONE line appended to
  SYSTEM MISSION RULES — "Prefer the cheapest items that satisfy all
  constraints. State your selection criteria." (task-specified, verbatim).
  Turn-2 imperative (system + user message), tools, turn-1 USER prompt,
  grader, post-final execution: byte-identical to v3. New grader fields:
  cheapest3_match promoted to a primary grade, per-item price ranks,
  overpay_vs_optimal, criteria-stated detection.
- Exactly 6 API calls fired (the pre-registered cap), all ok, 0 retries. 3/3
  iterations fully graded. Ledger rows carry
  `session_id=mickey_g3_1_cart_quality_20260910` in
  `logs/provider_usage.jsonl` (6 rows verified digit-for-digit). Key never
  echoed.
- Raw results: `C:\Users\foste\AppData\Local\Temp\g3_1_results.json`;
  runner: `C:\Users\foste\AppData\Local\Temp\g3_1_runner.py`.
- Bounds respected: one script, one results file, 6 deepseek calls (pennies —
  $0.001533).

Filed by G3-1 fire (zcode seat, Mickey group 3, task 1). Predecessor:
`watch/inbox/mickey/G2_2_storefront_v3.md` (this is G2-2's named NEXT, fired
with the scoring line at task-specified strength).
