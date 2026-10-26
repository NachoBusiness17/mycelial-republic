# LITE LANE PULL - 2026-10-03 (operator order, verbatim)

"i gave the lite lane to adam he's been using it we should remove it from
rotation"

Seat: zcode GLM-5.3 strategy window (sess_a8c2ebd2), same evening as
process-improve wave 1 (watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md).

## What the lane was

z_ai3, "Calcifer": the GLM Coding Lite V3 yearly package key
(ZAI_API_KEY_Lite in .env), glm-5.3-flash, fleet cache-mining lane +
the lane_runner flash door (LAW-058) + a rescue rung in fuel_feed, paced by
mag/lite_guard (law 15, 10K credits/wk). Relit 2026-09-04 after two prior
pulls (08-27, 08-29 - the pull/relit history lives in mag/fuel_feed.py's
lane table comments).

## The removal (four layers, each verified live before commit)

1. **configs/providers.yaml**: z_ai3 `dormant: true` with the dated operator
   order. The standing B2-133 dormant gate drops it from fuel_feed
   FREE_LANES + CACHE_LANES at import (verified: FREE_LANES now
   ox / openrouter-a1 / openrouter-a2 / groq) and B2-204 keeps it
   unpickable at the quota seam. Operator GO flips the flag back; no code
   edit (the cerebras shape).
2. **mag/lite_guard.py check()**: RETIRED gate - denies every door by
   default with the dated reason BEFORE any pacing math or quota probe;
   env LITE_LANE_ACTIVE=1 is the operator re-arm lever (verified: deny
   carries the retirement message).
3. **mag/lane_runner.py flash_call**: the z.ai leg is gone entirely. The
   lane door is now the env-pinned OPENROUTER model (OPENROUTER_MODEL +
   OPENROUTER_API_KEY). This also kills the old plain-ZAI_API_KEY fallback,
   which had been riding the operator's own working lane against the
   2026-08-29 hands-off fence - the pull fixes that fence violation as a
   side effect. LAW-058 amended in the module header + docstring.
4. **.env**: ZAI_API_KEY_Lite commented out (value preserved in the
   comment for operator reference) so direct env readers
   (autoglm/fanout/lite_scale/p20_pending_wave/research_fanout/model_bakeoff
   + lite_guard's own _key) find no key and refuse - the estate's
   no-key-equals-lane-down pattern.

## Attribution correction to wave 1 (appended, not rewritten)

PROCESS_IMPROVE_WAVE1_20261003.md symptom 5 attributed the elder/harvest
429 starvation to "the flash windows saturate the Lite lane all day." The
operator's order names the other rider: adam has been using the lane. The
starvation was shared-account contention (windows + adam), not solely the
windows; the cure stands (the estate no longer touches the lane at all).

## Side effects (named, one needs a routing call)

- **CACHE_LANES is now empty** (it was z_ai3-only): swarm cache-mining is
  paused until a replacement lane is named. Candidate per providers.yaml:
  z_ai free (glm-4.7-flash, 200K ctx, "the default" cache-mining lane) -
  but that is a routing call, OPERATOR: say "cache on z_ai free" (or name
  another lane) and it is a one-line flip in fuel_feed.
- **The 10 lite_guard-gated doors** (cooker, fuel_feed, lane_supervisor,
  free_tier, lite_scale, gopher_lite, rib_cache, swarm_worker,
  research_fanout, lane_runner) now refuse loudly at check() - visible
  denials, not silent re-routes. If any of those doors is on a cron you
  care about, its next fire files a "retired" refusal in its trail; that
  is the removal working, not a defect.
- **flash_call consumers** (elder lens at 12:00, any flash helper user)
  now need OPENROUTER_MODEL + OPENROUTER_API_KEY in the cage env; both are
  already set on the host (.env carries them) - if the cage env is baked
  separately, refresh it on the next compose cycle.

## Tests (tests/test_lite_lane_pull_20261003.py, 5 passed)

- z_ai3 absent from FREE_LANES + CACHE_LANES empty (live-config tripwire:
  flipping dormant back without operator GO fails this test and names this
  receipt)
- lite_guard denies by default; LITE_LANE_ACTIVE=1 re-arms to pacing
- flash_call: openrouter-only dispatch (fake opener records exactly one
  request, openrouter host, env-pinned model, no z.ai anywhere); refuses
  with the retirement message when the pin is unset

## Numbers (instrument-named, per B2-216)

- targeted: 19 passed this sitting across wave-1 + pull tests
  (test_lite_lane_pull 5 + wave-1 files 14)
- collected: 4,216 / 503 files, `pytest --collect-only -q`,
  2026-10-04T00:30Z, 19.69s, zero collection errors; +5/+1 vs the 23:47Z
  refresh = this file's 5 tests
- the wave-1 full-suite run (`pytest -q`, fired 2026-10-03T23:48Z) was
  still executing at this receipt's filing on the loaded box; its verdict
  banks to PROCESS_IMPROVE_WAVE1_20261003.md when it lands


## AMENDMENT 2026-10-04 ~03:10Z: the pull exposed a cost_truth seam gap

The B2-133 dormant gate only REMOVED dormant providers from the
free-or-credit set, which sufficed for cerebras/nvidia (no rate table
carries their models). z_ai3 carries a real glm-5.3-flash rate, so after
the pull its historical rows still priced at exact API dollars and
test_dormant_gate_b2133::..._never_reprice_to_spend failed (the test's
byte-anchor scan correctly grew to cover z_ai3). Fixed: dormancy now
intercepts the rate path too (mag/cost_truth.py _lookup_rate ->
state unpriced, source dormant_provider, the B2-522 decision class:
package credits are not API dollars). test_zai_burst's lane-table test
flipped to pin the PULLED world. Change-surface blast + cost_truth pair
all green (142 passed).
