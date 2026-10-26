---
name: envelope-probe-dispatch-law-20260925
description: 9/25-26 operator laws for width-sensitive burns + MEASURED results: Task agents clean 3→6→12 (~38M tokens, 0 storms), 5-hour window 99% remained (replenishment outruns burn), all-night fold-in/out gopher churn until weekly = 0
metadata:
  type: feedback
---

Operator corrections during THE GALA night, 2026-09-25/26 (six messages, one law):

1. NO dynamic-workflow engine for width-sensitive burns. "Workflows force a shitty amount of concurrency": the runtime owns width and workflow children got maxAttempts 0 (the 1302 storm shape). Background Task agents dispatched BY HAND are main-session-shaped (maxAttempts 11 + driver backoff), which is why old nights hit 24 concurrently.
2. Interrupt-proofing: he WILL interrupt mid-turn; agents must run run_in_background and bank to disk on landing (lane JSONs + WAVE_STATE board), so a kill costs nothing banked and any window can resume from the board. PROVEN LIVE: a session restart mid-wave killed 3 in-flight lanes clean and the 3 that had finished banked from their JSONs alone.
3. "Test what they'll allow versus what they publish": the coding plan's published rules are hypotheses. MEASURED RESULTS 9/25-26: Task agents clean at width 3, 6, AND 12 across hours of continuous churn; at in-flight ~15 TWO 1302 deaths landed in 2 minutes (t25, t11c, no-retry deaths) = ceiling measured between 12 and 16, width HARD-CAPPED at 12. Refined same night: a 1302 also hit width 12 minutes after the 15-16 burst → the limit is ROLLING THROUGHPUT, not width-only; after a burst even 12 gets 1302s until the window decays (law: on any 1302, hold all fires ~10 min, resume at 12). The width-3 folklore was workflow-child-scoped, not a Task-agent truth.
4. THE BURN-RATE LAW (screenshot 9/26 ~01:00Z): after the whole gala the 5-hour window still read 99% remaining (weekly 63%) — replenishment outruns a 12-wide battery by roughly an order of magnitude. His standing order: "iterate this process all night, fold in and out on non-overlapping tasks and gophers, the whole idea is to burn tokens self steal" until weekly hits 0 or he says stop. Fold-in/fold-out = each wave's decision-changed outputs become the next wave's work items (AFTERPARTY_QUEUE.md).
5. "No sacred cows": evidence overrides folklore including our own receipts' scope. "Smarter and harder, Daft Punk style": probe payload must also be estate work; local lanes run in tandem ($0, never the plan).

**Why:** each correction landed as an interruption of a differently-shaped dispatch; he controls width through ME, and the plan's real limits are an open experiment.

**How to apply:** width-sensitive burn → background Task fan-out by hand, board first (WAVE_STATE/AFTERPARTY_QUEUE), geometric width with clean-wave gates, envelope table updated per wave, gala outputs feed the next queue, loop all night. See [[tether-width-law-20260925]] and [[gala-night-20260925]].

**RE-MEASURED 9/26 (burn lane B2-25, amendment appended to AFTERPARTY_CLOSE_20260926.md):** width 10 clean from the flash-lane burn's own data — wave 1: 10/10, 37.4M witnessed tokens in 1,230s = 109.4M tok/h; three back-to-back waves in 37 min never tripped the post-burst penalty; ladder amends to 3-6-10-12, the 15-16 rung untested. CAVEAT: "zero 1302 recorded" only means zero surfaced — the main-session retry path (maxAttempts 11) can absorb 1302s silently; provider-error counter in agent metadata queued as the fix (B2-98).
