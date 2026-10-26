---
name: grounding-chain-built
description: Grounding chain controller built (commit f0e992d3e) — reads state
  from every system, evaluates conditions, fires the matching driver, records
  WHY as a grounded row; replaces timer-crons + operator reminders
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---
Grounding chain controller BUILT (commit f0e992d3e, `scripts/grounding_chain.py`) — the wiring
between the fleet's chained skills. Reads state from every system (research queue depth, build
briefs remaining, lock ages, schedule window), evaluates conditions, fires the matching driver,
appends a grounding row explaining WHY. Dry-run verified. Static commands only (no computed
values reach the shell); the drivers handle batching and locks.

**Grounding principle:** the state of the system IS the evidence. The next action is determined
by what the evidence says, not by a clock or a hope. Replaces timer-based crons deciding blind,
the operator reminding, and drivers firing without knowing why.

**Conditions evaluated per pass:**
- research queue > 0 + lock clear/stale → fire research batch 16
- build briefs > 0 + lock clear/stale → fire build batch 2
- research queue < 6 → tender signal
- hour ≥ 11 → dual-primary rotation note (glm free window)
- all clear → honest idle report

**Stale-lock handling:** locks older than 900s are treated as clear (crashed holders
self-clear). Log at `watch/inbox/union_fullsend_20260917/grounding_chain.jsonl`.
Related: [[union-fullsend-day-20260917]], [[cron-context-accumulation-lesson]],
[[wing-chun-operating-lenses]] (rolling = the heartbeat in permanent contact).
