# LANE 7/8 — V4.1-FLASH MICRO-AGENT COST REPLICATION SPEC (pre-registered 2026-09-10)

THE POINT: a viral run drove an Amazon shopping agent with V4.1 Flash — 5 minutes,
$0.049 total, 295 tok/s. Our agent runs are multi-hour and multi-lane. This spec
pre-registers a same-task-class micro-agent run on OUR stack so the comparison is
settled by measurement, not vibes. Design only; nothing fired yet. No live calls
were made writing this file.

Tri-state discipline: everything below labeled Supported / Disputed / Unproven.
Prices marked ASSUMED must be pinned from the live price table before first fire.

---

## 1. What we already meter (Supported — read from bytes)

Source: `logs/provider_usage.jsonl` (56,287 rows), writer sits in the shared fleet
client path — metering is automatic and free for any lane run. Per-call row schema:

```
ts, provider, model, calls, prompt_tokens, completion_tokens,
cache_hit_tokens, cache_miss_tokens, session_id, latency_ms,
tokens, ok, meta{chars, tool_calls, key_idx, key_env}
```

Verified arithmetic across the 12-row tail (orc-t812f7cce5f, deepseek-v4-flash):
`tokens == cache_miss_tokens + completion_tokens` in 12/12 rows — the ledger's
`tokens` field is the BILLABLE proxy, not prompt+completion. Use it for $ math.

Verified price constants (`mag/budget_refactor.py`, grounded in the real bill):
- deepseek cache-miss input: $1.4e-7/tok
- deepseek cache-hit input:  $2.8e-9/tok  (50x multiplier)
- Observed cache affinity on agentic loops: 96%+ hits (tail shows ~412 tok/turn
  prefix growth, ~448-512 tok/turn miss — misses stay flat while context grows).

Verified speed prior from the same tail: per-turn completion tok/s 55-185
(104 tok / 1.9 s ... 391 tok / 2.1 s); aggregate over 12 turns ~77 tok/s.

Prior art in-repo: `docs/ref/ZAI_API_EXPERT_REFERENCE.md` line 149 already puts
the frontier at "$0.045/task on AA Index v4.1.1" — the viral $0.049 sits in the
same cost class. Supported as context, Unproven for our own lanes until fired.

## 2. The replication design

### 2.1 Task (comparable difficulty — same task class, deterministic fixture)
MOCK STOREFRONT PROCUREMENT. A generated local catalog (200 products, JSON file,
seeded RNG so the answer key exists before the run) + a 3-item shopping mission:

> "Build a cart: coffee grinder, kitchen scale, gooseneck kettle. Budget $150
> total. Constraints: rating >= 4.3, in stock, seller rating >= 95. Pick the
> CHEAPEST satisfying product per item, then check out."

Same cognitive shape as the viral run: multi-step search, filter, compare on
price/attributes, ranked choice under constraints, terminal checkout action.
Deterministic, in-cage, zero external egress. Answer key graded by script.

### 2.2 Tool surface (our organs — stdlib only, no new runtimes)
1. `catalog_search(query, max_price, min_rating, in_stock_only)` — greps fixture
2. `product_get(asin)` — full record
3. `cart_add(asin)` / `cart_remove(asin)` / `cart_view` — state + running total
4. `checkout()` — terminal; writes the receipt row; ends the loop

Harness loop: system prompt + tool schemas -> lane -> parse tool_call -> execute
locally (ms) -> append result -> repeat. Same fire-shape as `mag/ractor_vessels.py`
(mask = task card, steer = mission); receipts land in `memory/runs/vessels/`.

### 2.3 Lanes
- PRIMARY (paid, real $): deepseek flash lane via fleet config — the class match
  to V4.1 Flash. GOPHER = deepseek through the fleet client; no key echoed.
- SHADOW ($0 by construction): z_ai free flash lane, same task, measures what the
  free-lane delta looks like on identical fixtures.
- Output price for $ math: pin from the provider price table AT FIRE TIME into
  the receipt (constant `OUT_PRICE`). Current value in this spec: ASSUMED, not
  asserted — input-side math below uses only the verified constants.

### 2.4 Caps and metering per step
- Hard caps: 14 model turns max, 12 tool calls max, 1,024 max_tokens/call,
  temperature 0, hard spend abort at $0.25/run (5x the viral number).
- Per step: one provider_usage.jsonl row per call (automatic). Derived per-step:
  tok/s = completion_tokens / (latency_ms/1000); miss share; tool_calls count.
- Per run (rolled up by session_id): total_tokens(billable proxy), total_$ =
  miss*1.4e-7 + hit*2.8e-9 + completion*OUT_PRICE, aggregate tok/s = sum(completion)
  / sum(latency), wall-clock, tool-call count, PASS/FAIL from the answer key.
- Run series: N=5 seeded catalog variants. Report median and min. One viral run
  is one sample; >=3/5 at parity is the minimum for a Supported claim.

## 3. Success criteria (pre-registered, graded by script)
- CORRECTNESS: all 3 items in cart, each cheapest-satisfying per answer key,
  cart total <= $150. Binary. A run that spends less but fails the key is a FAIL.
- PRICE PARITY: total_$ <= $0.049 (headline). Also report the ratio.
- SPEED PARITY: aggregate tok/s >= 295 by the viral definition AND per-turn
  median tok/s (both reported — stream-level vs turn-level tok/s may not be the
  same measurement; if the viral 295 is stream-level, the comparison must say so).
- EFFICIENCY: <= 12 tool calls, <= 14 turns, wall clock <= 300 s.
- COST PER SUCCESSFUL TASK: total_$ / passing runs (the operator-facing number).

## 4. Pre-registered comparison table

| Metric | Viral (V4.1 Flash) | Ours: prediction (pre-registered) | Ours: measured (fill at fire) |
|---|---|---|---|
| $/task | $0.049 | $0.003-$0.015 (input side ~$0.003 from verified miss/hit prices + observed 96% hit affinity; output side at OUT_PRICE) — predict BEAT, >=3x margin | — |
| tok/s | 295 | 55-185 per-turn, ~77 aggregate (observed deepseek flash band) — predict FAIL parity, ~2-4x slower | — |
| Wall time | 5 min | 1-3 min (14 turns x ~2 s + ms tools) — predict PASS | — |
| Tool calls | unreported | <= 12, ~8-11 typical | — |
| Correctness | unreported | 5/5 (deterministic fixture) or the fixture is broken | — |
| $ per successful task | n/a | <= $0.015 | — |
| Free-lane shadow | n/a | $0.000 by construction; correctness same or worse on constraint-following | — |

Falsifiers: (a) if our total_$ > $0.049 on the median run, the "cache-affinity
makes agentic loops cheaper" claim is DISPUTED and the miss-burst explanation in
budget_refactor is suspect; (b) if aggregate tok/s >= 295, my latency prior is
wrong and the viral speed is replicable on paid flash; (c) if any run exceeds
$0.25 or 14 turns, the harness cap leaked and the series is void.

## 5. Fire commands (when operator GOes spend)
1. Generate fixtures: `python -m mag.micro_shop gen --seeds 5 --out memory/runs/micro_shop/` (new ~80-line organ, stdlib; per design above)
2. Run: same loop with `--lane deepseek` (primary) then `--lane z_ai` (shadow)
3. Grade + rollup: `--grade` reads answer keys + provider_usage.jsonl by session_id
Nothing here touches external networks beyond the lane call itself.

## 6. Claim ledger
- Metering schema + price constants + cache affinity: SUPPORTED (files cited above).
- Viral numbers ($0.049, 295 tok/s, 5 min): taken as given from the operator's
  paste — UNPROVEN here, no primary source fetched this lane.
- Our predictions: UNPROVEN until the 5-seed series fires; that firing is the
  whole point and needs only spend GO, since every organ it needs already exists.

Filed by LANE 7/8 (cost replication spec). Sibling lanes: see watch/inbox/v41_paces/.
