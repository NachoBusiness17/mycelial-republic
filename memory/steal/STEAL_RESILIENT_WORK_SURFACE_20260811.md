# STEAL — RESILIENT WORK SURFACE: route through LIVE consumers, never a dead-end mailbox (2026-08-11)

## Problem (debugged)
Frontier-grok work wasn't draining: deep-research-exec sat UNDRAINED in the copilot inbox because the
ghost daemon's copilot_watch_loop is DOWN (ghost cycle crashed 2026-08-10T22:42). The inbox is a
SINGLE-CONSUMER dead-end while that one daemon is down. The RUNNING autorun loop (governor_autorun)
does NOT read the copilot inbox — so the work stranded. Queue empty, zero frontier tasks spawned.

## Self-steal (the invariant we already own)
- The autorun loop (RUNNING) already FILLS from multiple sources: agent_state next_moves, handoff,
  improve, verkle, steward. Those drain reliably. The INVARIANT: work routed through a LIVE loop's
  fill source gets drained; work routed through a DOWN daemon's surface strands.
- Fix shape: put the work where the LIVE loop reads it (next_moves/handoff/improve), not the dead inbox.

## External-steal (adapt the contract)
- Resilient-message-queue / mailbox pattern (SQS, Redis list, work queues): a queue is consumed by ANY
  live worker; if one consumer dies, another pulls. A single-consumer surface (one daemon's inbox) is
  fragile. ADAPT: make the copilot inbox consumable by ANY live loop (autorun too), so it's a shared
  mailbox, not a single-owner dead-end.
- Retry/idempotency: a drained task that failed (403, died) should requeue/retry, not vanish.

## Adaptation (code)
1. Wire the copilot inbox into governor_autorun's fill phase (so the LIVE autorun loop also drains it,
   not just the daemon's watch loop) — the resilient-mailbox fix.
2. Route frontier/deep-research work through next_moves/handoff (already started: invention loop in
   latest.md) so it drains via the live loop.
3. Retry: on task died/403, mark + requeue (with backoff) instead of dropping.

## Honesty
- Even with the surface fixed, grok 4.5 403s tonight (no credits; other key resets 8/13, premium 8/15).
  The CHEAP swarm (deepseek) can drain tonight; grok frontier only pays after reset.
