# RIB_FREE_USAGE_POLICY — how and when to use free seats, and how to iterate (2026-08-23)

**Law:** Free seats are an OPPORTUNISTIC sensing surface, never a forced workhorse. Use them when
they're cool; the moment you try to force them, they throttle into empty (429) — that's spinning
plates, not work.

## The two kinds of limits (do not conflate)
- **OUR limits (CPU/RAM/concurrency/pipeline):** push hard — rightsize to the real workload, use
  our own compute fully. No external penalty. This is where REAL work gets forced through
  meaningfully.
- **PROVIDER limits (free lanes):** shared, enforced, capped. Cannot be skirted. Pushing them
  returns empty throttled responses = junk, not work. Reward patience, not pressure.

## The decision rule (how to use free)
Use free seats ONLY when ALL hold:
1. **The pool is cool** — no active upstream throttle (ox-alpha 429 today = hot; don't fire).
2. **The work is sensing, not execution** — free seats discover/propose (reasoning streams), they
   do NOT produce trusted content (substance_chars=0 is the norm). Real work goes to DeepSeek/local.
3. **The work is distinct** — dedup by core; N copies of one question collapse to one opinion (n*).
4. **There's a drain path** — free discoveries → bank → free_to_swarm → k8s queue → cluster folds.
   Otherwise the discovery just sits (spinning).

## The routing ladder (when to use what)
- **Local VRAM / k3s** — default execution + write + verify. Free, ours, deterministic.
- **DeepSeek (funded)** — the reliable workhorse for real volume. Can take heavy concurrency.
- **Free OpenRouter lanes** — opportunistic sensing ONLY when cool. ~18 lanes × 2 accounts,
  ~144 reliable parallel agents max, riding the warm FROZEN_PREFIX (~98% cache-hit).
- **Grok seats (nacho+sd)** — scarce frontier, only the coldest high-value reasoning.

## The iteration loop (how to get better at when)
Every cycle (cadence) measure and fold:
1. **Seat hunt** — discover lanes/accounts; probe live quota (free_lanes/quota/accounts).
2. **Fire** — real_swarm runs the free lanes; only when cool, only substantive.
3. **Fold the signal** — record which lanes yielded substance vs 429'd (ledger + exhaustion file).
   This IS the learning: over time we build a per-lane, per-time-of-day cool/heat profile.
4. **Feed the model** — the ledger becomes the "when is this lane cool" map; rotation + exhaustion
   get smarter each pass (rightsize constantly, iterate don't repeat).

## Standing (the honest gate)
- Banked ≠ verified, always. Free seat proposes; local basecamp disposes.
- Never hammer a hot lane (re-fire-throttled = the anti-pattern we paid to learn, ox 429 today).
- Meaningful work through OUR pipeline, hard — yes. Skirting free-provider limits — no.

**Iterate:** update this RIB with every observed cool/heat signal. The policy is a living map,
not a fixed rule.

## POST-DATUM VERDICT 2026-10-05 (D3 resolved by instrument; appended by lane e03-rib-vault,
## append-never-rewrite: the law block above is untouched)

The OPEN contradiction vs RIB_MODEL_GARDEN_ROUTING.md:192 (459 rows, ZERO 429, 69h+ sustained
forced mining) was resolved by the forced-width cool/heat re-probe this rib's own iterate
clause ordered: watch/inbox/ribvault_20261005/R062_FREE_USAGE_RESOLVE_20261005.md
(+ probe_results.jsonl beside it). Measured 2026-10-05, 13 lanes, 52 asks, one key:
COOL (width 1, spaced, the sanctioned shape): 0 x 429 in 13 asks -- the drip-rate evidence
class holds. HEAT (instantaneous width 13, zero spacing, 3 waves): 2 x 429 in 39 asks, both
poolside/laguna-xs-2.1:free ("temporarily rate-limited upstream") -- THE MECHANISM THIS RIB
NAMES IS MEASURED REAL at forced instantaneous width. Ruling: forcing them DOES throttle
(this law stands, now instrument-carried); the 459-row zero-429 record is honest at its own
drip rate and does not witness the forced-width case. The throttle signal is the 429 class;
EMPTY-at-200 is confounded at max_tokens 16 by reasoning models burning the budget
(RIB_INFERENCE_BUDGET one-bug) and was not adjudicated as throttle here.
