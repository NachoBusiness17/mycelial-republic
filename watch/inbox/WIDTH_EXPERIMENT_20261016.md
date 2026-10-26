# THE WIDTH EXPERIMENT - day one, measured honestly (2026-10-16)

Classification: CARD (experiment results + the revised width map)
Producer: zcode-seat-20261016
Commission: "scale all our windows - 2 then 4 then 8 and test timing... steal
API's guidance... stack multiple asks per window... 3-4 agents acting as a
single organ triaging and deduping"

## THE STOLEN GUIDANCE (OpenRouter's own limits doc - the rtfm that rewrote the map)

- 20 requests/minute per free model.
- **50 requests/day account-wide** on a never-funded account; **1,000/day**
  once $10+ credits have EVER been purchased (all-time, not balance).
- Multiple keys DO NOT raise limits - capacity is governed globally per
  user. (The two-keys-doubles assumption dies by rtfm.)
- Spreading load across MODELS is the documented lever.
- 429: exponential backoff, honor Retry-After.

## THE REVISED TRUE-WIDTH MAP (per-lane daily caps, not minute windows)

- OpenRouter free: 50/day account-wide. The minute window is generous; the
  DAY is the wall. Stacking (5 signals per completion) multiplies VALUE per
  request: 50 requests = up to 250 signals folded per day.
- Gemini Pro CLI x2 accounts: ~1,000 requests/day each at 60 RPM - THE
  2,000/DAY ENGINE, gated only on the operator's OAuth sign-ins.
- Gemini 3.8 native key: free-tier class, ~1,500/day family (5 RPM observed
  on the compat path; native works) - the adapter shim unlocks it.
- Ollama battery (15 local models): no caps, bounded only by machine time -
  the bulk filler and the independence anchor.
- OpenRouter $10 one-time: +1,000/day when funded.

## TONIGHT'S MEASUREMENT (stacked asks, 5 signals each)

- 36 stacked asks fired across the evening ladder attempts: 11 landed /
  25 failed (8x429 pacing, 16x400-class from one family's body quirk,
  1 empty-length). 52,005 completion tokens, $0.00.
- Width 4 rung: 285s for 8 stacked asks (each stack = 5 signals -> ~40
  signals per ~285s per worker-triple). Width 8 rung: insta-fail (asks
  exhausted by the preceding rungs - the rung needs a fresh mint; the
  ladder script's selection is the fix, staged).
- Ops lessons paid for: zombie carriers hold worker logs (kill by PID,
  not by name); batch_fire needs env propagation + per-worker logs (fixed);
  ladder run-roots must be dedicated (double-partitioning ate the asks);
  first-run rm -rf ate regenerable asks - regenerable is the rule: the
  backlog rows were never lost, only the ask wrappers.

## THE HONEST VERDICT TONIGHT

The width ceiling on OpenRouter free is the DAY cap (50), not the minute.
Width scaling there is bounded at ~50 requests no matter the concurrency -
so the 2,000/day USEFUL engine is: Google Pro CLI x2 (2,000/day) + Gemini
native (~1,500/day) + the ollama battery (unbounded local) + OpenRouter's
50/day spent on STACKED asks only (250 signals/day from 50 requests).
Stacking is the multiplier that makes small caps big; rotation is the
multiplier that makes many small caps one big cap.

## Next sittings

1. The 3.8 native adapter shim (the carrier drives the second Gemini lane).
2. The Pro OAuth sign-ins (operator, two clicks) -> the CLI ladder at
   width 2/4/8 against the 60 RPM lane - the real timing test.
3. The 400-family adapter or drop; then the clean ladder rerun on a fresh
   mint (the script's selection fix is staged).
4. The triage-dedup organ: the batch workers' outputs pass one dedup
   percolation before the digest (3-4 agents as one organ, dogfooding the
   stack).
