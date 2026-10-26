# BURN steering-theory 2026-09-27

## Verdict

steal

## Evidence

- tools/drift.py (2026-09-18): "The missing quantity in all five is the same number: corr(delta-M, delta-R), the correlation between the metric's movement and the referent's movement". Verdicts VACUOUS / ALIGNED / DRIFTING / INVERTED / INSUFFICIENT / DEGENERATE, plus FRAGILE-ALIGNED stamped downstream by the aging guard. Law string: "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'".
- tools/probe20_run.py (2026-09-26): pair A metric is the "mean verdict-token logprob margin over the probe at cycle t; referent = correct/20". Noise floor: a "single 0.05 task flip on the quantized referent escapes the kill" natively, so the runner forces INSUFFICIENT when net referent delta is under 0.1 ("one-flip VACUOUS escape blocked"). Live client exits 3 LIVE-UNREACHABLE / 4 LIVE-BAD-RESPONSE with "no fallback margin, no synthetic rows (pre-registered falsifier, BURN _b)".
- watch/inbox/PROBE20_steering_v1.jsonl: meta row carries version_hash bfce1f28..., recomputed and refused on every load; 20 typed TRUE/FALSE tasks (13/7), min_points 5, noise_floor 0.1.
- memory/runs/gps_50/FOLD.json (50/50 ok, $0): G38 "honest refusal - teleological drift pairs are NOT GPS pseudorange residuals (those carry multipath, clock bias, ephemeris error)"; quality note: "several lanes fabricated citations when pressed for specifics (fake arXiv ids, fake court cases); receipt discipline caught them".
- GPS_PACK G07 (zai-lite): without dead reckoning, "drift is a lagging indicator, not a live one"; steal line: "never let a fix be the only thing that moves the position".
- Web search (snippet level only, not deep-read): "Activation Steering with a Feedback Controller" (ICLR 2026) is described as "closed-loop steering design with interpretable error dynamics, connecting activation steering to classical control-theory stability guarantees (i.e., bounded interventions / drift correction)"; GCAD (arXiv 2605.10664) reports improving "average coherence drift"; DSAS (Apple) "decouples when to steer from how".

## Steal or Vacuous

Steal, two decks.
1. Instrument pair is canon now: drift.py is the verdict organ, probe20_run.py is the honest series caller (typed question, decoding-free logprob readout under a TRUE|FALSE grammar, noise floor, append-only series, version-hash refusal). Any future steering claim that names no drift pair is vacuous by this receipt.
2. Lens on the GPS-for-dumb-agents arc: 2026 frontier work converges on the fleet's own drift-pair shape (bounded, closed-loop, drift-instrumented steering). Their "coherence drift" reads as our DRIFTING verdict; their controller gain is our amendment step. The fleet holds a working referent side (correct/20, overturn rate) that the surfaced papers describe only at the metric side. Owed: full-text reads before any import; the search hits are snippet-level and one (ICLR proceedings link) is unverified beyond its abstract text in the result block.

## Bibliography

- tools/drift.py (repo, read in full 2026-09-26)
- tools/probe20_run.py (repo, read in full 2026-09-26)
- watch/inbox/PROBE20_steering_v1.jsonl (last lines, read 2026-09-26)
- memory/runs/gps_50/GPS_PACK.md and FOLD.json (read 2026-09-26)
- WebSearch result snippets 2026-09-26: ICLR 2026 feedback-controller steering paper (proceedings.iclr.cc link), arXiv 2605.10664 (GCAD), github.com/ibm/activation-steering, DSAS (Apple)
