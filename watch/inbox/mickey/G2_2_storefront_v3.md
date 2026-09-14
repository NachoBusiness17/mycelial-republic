# G2-2 — V4.1 STOREFRONT V3 (the imperative turn-2), fired 2026-09-10T20:54Z

THE POINT: **the deferral was prompt-followable, not a depth floor.** Same 2-call
shape, same fixture, same client — the ONLY change is the turn-2 prompt, swapped
from M3 v2's soft clause ("turn 2 is your FINAL turn: using the results you saw,
issue any remaining add_to_cart calls") to the task's exact imperative ("TURN 2
IS FINAL. You must call add_to_cart NOW with your best 3 items. Do not verify.
Do not compare. Add to cart immediately."), delivered twice: in the SYSTEM turn
budget AND as a user message right before call 2 (v2 said nothing at turn 2;
tool results just appeared). Result: **3/3 carts completed** — every iteration's
turn 2 fired exactly 3 `add_to_cart` calls, zero `get_details`, zero `compare`.
M3 v2's verification habit (get_details x3, empty cart, 0/2 graded) is gone
entirely. And the mission got CHEAPER: **$0.000439/task mean vs v2's $0.000492**
(-10.7%, same call count — better cache on the warm iterations), **~112x under
the viral $0.049**. First completed carts in the storefront arc (Lane 1: 0/3,
v2: 0/2 graded). Total spend **$0.001318 for 6 calls**, ledger-exact, cap hit
exactly, no retries.

---

## Per-run results (3 tasks, 2 calls each, deepseek-v4-flash, tier T2, temp 0)

Pricing pre-registered: input $0.15/M, cache-hit $0.003/M, output $0.60/M.
Fired 20:54Z = Beijing 04:54, off-peak — flat prices were the live vendor prices.

| task | turn 1 | turn 2 | cart | pass | cheapest-3 match | cart total | prompt tok | cache hit | out tok | wall s | task tok/s | cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | search_products | **add_to_cart x3** | MS-018, MS-022, MS-197 | **PASS** | no | $73.44 | 18,766 | 16,512 (88.0%) | 207 | 4.69 | 44.2 | $0.000512 |
| 2 | search_products | **add_to_cart x3** | MS-022, MS-076, MS-197 | **PASS** | no | $62.09 | 18,760 | 17,280 (92.1%) | 205 | 3.28 | 62.4 | $0.000397 |
| 3 | search_products | **add_to_cart x3** | MS-018, MS-022, MS-197 | **PASS** | no | $73.44 | 18,780 | 17,280 (92.0%) | 221 | 3.14 | 70.4 | $0.000409 |
| **mean** | | | 3 distinct, all valid | **3/3** | 0/3 (bonus stat) | | | **90.7% (all 6 calls)** | | | 59.0 | **$0.000439/task** |

Carts graded from executed calls (post-final execution, identical to v2's
grader): every cart holds exactly 3 distinct in-stock products under $50 with
rating > 4.0. None matched the cheapest-3 answer key (MS-028/MS-152/MS-121) —
that was a bonus stat, and it was never hit in any prior lane either.

Per-call raw (from `g2_2_v3_results.json`, all receipted in
`logs/provider_usage.jsonl`, session `mickey_g2_2_storefront_v3_20260910`,
6 rows, token totals match stdout digit-for-digit):

```json
iter 1: t1 {pt:8710, hit:7808, miss:902,  ct:102, wall:2.984, cost:$0.000220, tools:["search_products"]}
        t2 {pt:10056, hit:8704, miss:1352, ct:105, wall:1.703, cost:$0.000292, tools:["add_to_cart","add_to_cart","add_to_cart"]}
iter 2: t1 {pt:8710, hit:8576, miss:134,  ct:100, wall:1.629, cost:$0.000106, tools:["search_products"]}
        t2 {pt:10050, hit:8704, miss:1346, ct:105, wall:1.655, cost:$0.000291, tools:["add_to_cart","add_to_cart","add_to_cart"]}
iter 3: t1 {pt:8710, hit:8576, miss:134,  ct:116, wall:1.425, cost:$0.000115, tools:["search_products"]}
        t2 {pt:10070, hit:8704, miss:1366, ct:105, wall:1.715, cost:$0.000294, tools:["add_to_cart","add_to_cart","add_to_cart"]}
```

## Verdict: prompt-followability vs depth floor

**Prompt-followable. M3's depth-floor reading is rejected at this prompt
strength.** The evidence is not a marginal improvement — it is a phase flip:

| metric | viral claim | Lane 1 (1-call) | M3 v2 (soft turn-2) | **this run (imperative turn-2)** | call |
|---|---|---|---|---|---|
| carts completed | unreported | 0/3 | 0/2 graded | **3/3** | **PASS — failure class closed** |
| turn-2 composition | — | n/a (no turn 2) | get_details x3, 0 add_to_cart | **add_to_cart x3, 0 get_details** | behavior inverted |
| $/task | $0.049 | $0.000531 | $0.000492 | **$0.000439** | **PASS — 112x cheaper than viral, cheaper than every prior lane** |
| cost/successful task | n/a | undefined (0 passes) | undefined (0 passes) | **$0.000439** | first time measurable in the arc |
| tok/s | 295 (stream) | 56-70 | 66-70 task-level | 44-70 task-level | FAIL parity, as pre-registered |

Why it flipped, mechanistically: v2's turn-2 prompt was (a) soft in register
("issue any remaining add_to_cart calls") and (b) positioned in the system
prefix ~10K tokens upstream of the decision point, while fresh `get_details`
results sat directly adjacent to generation. v2's model narrated the habit
aloud — "Let me verify three of them with details before adding" — and followed
the habit. v3 puts an imperative at the recency position, names the forbidden
actions explicitly, and the habit loses 3/3. Note what did NOT matter: turn 1's
user prompt still says "Verify with your tools" (left byte-identical to v2 on
purpose), and verification language still shaped turn 1 (search_products every
time). The deferral was a local, last-turn phenomenon — controllable by the
last-turn instruction.

Two honest caveats:

- **Compliance cost the prose.** `turn2_text` is empty in all 3 iterations —
  the model spent its 105 output tokens entirely on the three add_to_cart
  calls and skipped the "state the final cart" reply-text clause. The grade is
  cart-based (unchanged from v2), so passes stand, but full-instruction
  compliance is 2-of-2 clauses at best: the imperative outranked the reporting
  duty. A softer tail on the imperative ("then state the cart") is the fix if
  the prose ever matters.
- **N=3, one fixture, one model.** This establishes the deferral is
  prompt-followable HERE, at THIS strength, on THIS fixture. It does not
  establish how weak the prompt can be and still work (v2's soft clause is one
  measured point of failure; the imperative is one measured point of success;
  the threshold between them is unmapped).

## Tri-state ledger updates

- M3 v2's finding "flash always reserves one more verification round before
  terminal actions; an explicit 'this is your final turn, add now' instruction
  was ignored 2/2" — second half now **DISPUTED**: the soft version was
  ignored; the hard imperative is followed 3/3. The first half ("reserves one
  more round" under soft/absent turn-2 instruction) survives as SUPPORTED.
- Lane 1's named fix "2 calls/task completes carts, ~$0.002-0.006 total": both
  halves now **SUPPORTED** — $0.001318 total, 3/3 carts (was cost-SUPPORTED /
  completion-DISPUTED after v2).
- M3 v2's "new finding" of verification-first behavior: **SCOPED**, not
  general — it is conditional on the turn-2 instruction register, not a
  property of the model at all instruction strengths.
- Cache affinity on agentic loops: **SUPPORTED a third time** (90.7% across 6
  calls; iter 1 call 1 hit 7,808 cached tokens off the two-day-old v2 prefix,
  then 8,576 warm within-run — cross-run cross-day reuse again).
- Temperature-0 non-determinism (v2 finding): **SUPPORTED again** — iters 1
  and 3 sent near-identical prompts and produced ct=102 vs 116; picks
  converged (identical carts), bytes did not. Iter 2 picked a different third
  item (MS-076) — valid, just not the mode.
- "Do not verify" did not damage correctness: 3/3 valid carts with zero
  get_details calls. On THIS fixture, the verification round v2's model kept
  taking was not load-bearing for constraint satisfaction — it was latency and
  $0.00029 of pure habit.

## Named next probe (unfired — call bound spent)

The cost/completion axis is closed; the open axis is cart QUALITY (0/3
cheapest-3 matches). Cheapest probe: keep the v3 harness byte-identical and
add one line to turn 1's mission rules — "prefer the cheapest qualifying
candidates; your score is the cart total" — 6 calls, ~$0.0013, tests whether
optimal-selection is prompt-followable the same way completion turned out to
be. If selection quality is NOT prompt-followable, that is the real depth
floor, and it is a reasoning floor, not an action floor.

## Method and receipt trail

- Client: `models.providers.chat_messages`, provider `deepseek`, model
  `deepseek-v4-flash`, tier T2, temperature 0, max_tokens 1024, thinking
  disabled at provider level, `tool_choice=auto` — identical to M3 v2.
- Fixture: bit-for-bit identical to LANE7/M3 (seed 42, 200 products, 42
  satisfying, key MS-028/MS-152/MS-121) — zero-API dry run verified pre-fire.
- Loop shape: identical to v2 except the turn-2 prompt. Delta precisely: (a)
  SYSTEM turn-budget turn-2 sentence replaced with the exact imperative
  wording (execute-note and final-cart tails carried over from v2); (b) the
  same imperative appended as a user message immediately before call 2. Turn-1
  prompt byte-identical to v2's. Any tool calls emitted in call 2 still
  execute post-final; grading identical to v2.
- Exactly 6 API calls fired (the pre-registered cap), all ok, 0 retries. 3/3
  iterations fully graded (no runner bugs this time — v2's metrics crash is
  fixed in the carried code). Ledger rows carry
  `session_id=mickey_g2_2_storefront_v3_20260910` in
  `logs/provider_usage.jsonl` (6 rows verified). Key never echoed.
- Raw results: `C:\Users\foste\AppData\Local\Temp\g2_2_v3_results.json`;
  runner: `C:\Users\foste\AppData\Local\Temp\g2_2_runner_v3.py`.
- Bounds respected: one script, one results file, 6 deepseek calls (pennies —
  $0.001318).

Filed by G2-2 fire (zcode seat, Mickey lane group 2, task 2). Predecessor:
`watch/inbox/mickey/M3_storefront_v2.md` (this is M3's named NEXT (b), fired
with the imperative at full strength).
