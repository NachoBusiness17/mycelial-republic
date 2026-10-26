---
name: 12-wide-background-architecture
description: 2026-09-17 architecture ruling — the 12-wide salon mechanic runs in
  BACKGROUND windows (fresh context, verdicts return); the foreground window is
  the conductor only; provider global capacity is the only real collision and U8
  says it tolerates it
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator question 2026-09-17 night: "we could be utilizing the 12 wide mechanic on the
window as well... or would that be better on a background window? would that starve out
the other?"

**The ruling:** 12-wide (Rashomon/salon shapes) runs in BACKGROUND windows — subagents or
salon_phone fires, each with its own fresh context, returning only verdicts. The foreground
window is the CONDUCTOR: plans, reads verdicts, promotes through gates, commits. Never the
fan-out body.

**Why (two starvation resources, two answers):**
- Context: fan-out in-window makes every shape's full output permanent ballast (the 5.7M
  cron lesson). Background windows return digests — nothing accumulates here.
- Provider capacity: the only REAL collision — both windows share OpenRouter's global pool
  (extra keys don't help, per U8). But U8 measured 24-concurrent tolerated (limit = latency
  not rejection), so a 12-wide salon + the 16-worker drive ≈ 28 in-flight = inside the
  envelope; they interleave, they don't starve.

**How to apply:** salon_phone.py already productizes the 12-shape mechanic (the 6/7-survived
trajectory salon). First candidate fire when operator says go: 12 shapes attacking the
5-item enhancement plan (one per enhancement), folded to a build order. See
[[union-fullsend-day-20260917]], [[rashomon-surfacing-style]], [[salon-50-and-basecamp-20260916]].
