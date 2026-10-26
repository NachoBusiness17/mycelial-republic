---
name: oneshot-50-percent-mandate-20260927
description: Operator demand 9/26-27 "oneshot 50% right now fullblast all
  surfaces blowing cheap/free tiers" — 20% max burned in 24h was inadequate;
  claritas repos + open-sourced CLI named as unused resources
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Operator escalation 2026-09-26 late / 2026-09-27 early: after the flash-lane burn landed 397 briefs (~816M witnessed tokens), the operator measured the result and said "i've burned 20% max" against the 5.3-flash lane window. His demand: "oneshot 50% right now to the best of your ability fullblast amongst all surfaces blowing our cheap/free tiers."

**Why:** The 10x analysis correctly identified width stacking and free-lane tandem as the compute multiplier, but the executed burn still used FCFS dispatch with 10-minute refill gaps. The peak (109M tok/h at width 10) was real but not sustained — dispatcher gaps, the stale-restore restore loop, and the 1302 wall cost hours. The operator expected "burn like we used to" = the gala/afterparty pace, not the polite refilled pace.

**How to apply:** When the operator says burn or fullblast, the target is continuous max-width dispatch with instant refill — not a 10-minute cron cadence. The free-lane tandem runner, the claritas repos, and the open-sourced CLI are named resources that were identified but not yet leveraged. If he says a number (50%, 10x), treat it as the actual target, not a rough direction. The gap between "we produced 816M tokens and 400 receipts" and "that's only 20% of the window" is the real signal: the fleet's throughput ceiling is much higher than any single measurement suggests.

Related: [[ten-x-analysis-20260926]], [[width-envelope-amendment-20260926]], [[depth-not-width-finding-20260927]], [[operator-building-vs-using-pattern]]
