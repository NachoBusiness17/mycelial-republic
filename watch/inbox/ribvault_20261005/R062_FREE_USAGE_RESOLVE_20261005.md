# R062_FREE_USAGE_RESOLVE_20261005 - the D3 contradiction resolved by instrument

Register: corpus/steal/MASTER_READ_ESTATE.md D3 (r06#2), DISPUTED-tier open since 2026-09-30.
The routing rib's own resolution order: "resolve with instruments, not by editing either rib
silently". This receipt is the instrument's record; the verdict rows appended to both ribs
cite this file. Fired by lane e03-rib-vault, 2026-10-05.

## The instrument

`watch/inbox/ribvault_20261005/r06_free_probe.py`, run
`./.venv/Scripts/python.exe watch/inbox/ribvault_20261005/r06_free_probe.py` (single
invocation, 2026-10-05T05:37-05:44Z, results in probe_results.jsonl + probe_summary.json
beside this file). Every ask: POST to the one literal allowlisted endpoint
(https://openrouter.ai/api/v1/chat/completions; https+host guard enforced in code on every
request and redirect per the stealth_driver allowlist law), max_tokens 16, prompt "Reply
with the single word: ALIVE" (the sanctioned openrouter_free_gate gate shape), single key
OPENROUTER_API_KEY (never printed). Roster: the 12 earned configs/providers.yaml free-block
ids + stealth/space-bunny-alpha = 13 lanes.

Phases:
- COOL: width 1, sequential, 4s spacing (the policy rib's sanctioned "cool" shape), 13 asks.
- HEAT: instantaneous width 13 (full roster in parallel, zero spacing), 3 waves back to
  back = 39 asks. This is the forcing anti-pattern at a width the banked 4-8 rows/hour
  evidence class never tested.

## The measured census (every outcome classed; the banked row's own caveat was "register may
## log successes only" -- this probe logs failures too)

| class | cool (13 asks) | heat (39 asks) |
|---|---|---|
| 200 with content | 5 | 14 |
| 200 EMPTY content | 7 | 20 |
| 404 | 1 | 3 |
| **429** | **0** | **2** |

Summary block verbatim (probe_summary.json): cool_asks 13, cool_200_ok 5, cool_429 0,
cool_other_fail 8; heat_asks 39, heat_200_ok 14, heat_429 2, heat_other_fail 23;
peak_instant_width 13; heat_429_models ["poolside/laguna-xs-2.1:free"].

The two 429s, byte-quoted from probe_results.jsonl detail fields, same lane both waves:
- heat w1 poolside/laguna-xs-2.1:free: {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"poolside/laguna-xs-2.1:free is temporarily rate-limited upstream. Please retry short...
- heat w3 poolside/laguna-xs-2.1:free: same raw message ("temporarily rate-limited upstream. Please retry shortly").

Freshness fact caught by the same instrument: inclusionai/ling-3.0-flash-fin:free returned
404 all three encounters ("This model is unavailable for free. The paid version is available
now") -- it sits in the earned providers.yaml block from B2-202 (2026-09-26) and is now
retired from the free tier; the other 404s are the same id re-encountered in waves 2-3.

## THE VERDICT (the D3 ruling, instrument-carried)

The contradiction resolves CONDITIONS-BOUND, as the register's conditional ruling
anticipated; neither rib is struck, and the policy's mechanism is CONFIRMED at the width
its evidence class never reached:

1. At the drip rate the banked evidence was taken at (4-8 rows/hour; this probe's cool
   phase, width 1, spaced): ZERO 429 across 13 lanes, matching
   animals/stealth_free_lanes.jsonl ("459 rows, ZERO 429, 69h+ sustained forced mining").
   The routing row's evidence class is honest at its own rate.
2. At forced instantaneous width (13-wide parallel, zero spacing, repeated waves): 429s
   APPEAR (2/39, one lane, upstream rate-limit). RIB_FREE_USAGE_POLICY_20260823's mechanism
   ("the moment you try to force them, they throttle") is measured TRUE -- the throttle is
   real, lane-specific, and width/time-dependent, not a myth.
3. The "throttle into empty (429)" conjunction does NOT decompose as the policy prose
   implies: the 200-EMPTY class is dominated by reasoning models burning the max_tokens 16
   budget on hidden reasoning (the known max_tokens-16 artifact, RIB_INFERENCE_BUDGET's one
   bug), so EMPTY-at-200 is NOT a clean throttle signal at this probe size; the hard 429
   class is the throttle signal. The policy's operative warning (forcing produces junk) is
   what survives byte-side: 25/52 heat asks returned no usable content.

Operative law after this instrument, stated once: free lanes are sensing surfaces whose
upstream throttles are measured real at forced instantaneous width and measured absent at
drip rate; "zero 429" claims must carry their rate and width conditions or they are not
evidence of cool.

## Caveats (honest bounds)

- 52 asks, one key (OPENROUTER_API_KEY), one moment (2026-10-05T05:37-05:44Z): a probe, not
  a sustained campaign; the 459-row drip evidence and this width evidence are different
  instruments at different rates, and the register said as much.
- The max_tokens 16 gate shape cannot separate "throttled into empty" from "reasoning burned
  the budget"; only the 429 class is adjudicated here.
- The heat waves ran back-to-back within ~7 minutes; a longer forced campaign might trip
  account-level (not upstream) limits this probe never reached.
