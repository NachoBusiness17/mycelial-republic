# trail_core_1 — stale-docs-cleanup

## Completed

- Added deprecation banners to `docs/COORDINATION.md` and `docs/BEHAVIORAL_ROUTER_INTERFACE.md` only: cursor lane lapsed 2026-08-27; current seats Codex, Grok x2, DeepSeek; pointer to `docs/ref/ZAI_API_EXPERT_REFERENCE.md`.
- Rewrote stale cursor-active claims in those two files to the current roster. Historical `watch/cursor_bridge.py` kept as a lapsed pointer (sacred cows: no deletions).
- Touched no other docs, no code, no covenant.

## Artifacts

- `docs/COORDINATION.md`
- `docs/BEHAVIORAL_ROUTER_INTERFACE.md`
- `jobs/stale-docs-cleanup/trail_core_1.md`

## Acceptance

```text
=== ACCEPT 1: grep | grep -v | wc -l ===
0
=== ACCEPT 2: head -5 COORDINATION.md ===
> **Deprecation banner:** cursor lane lapsed 2026-08-27 — current seats are Codex, Grok x2, DeepSeek. See `docs/ref/ZAI_API_EXPERT_REFERENCE.md` for current lanes.

# Cross-seat coordination

Mag routes work by **depth** so Grok, DeepSeek, and local janitors each do what they are good at — without burning tokens on the wrong seat.
=== ACCEPT 3: head -5 BEHAVIORAL_ROUTER_INTERFACE.md ===
> **Deprecation banner:** cursor lane lapsed 2026-08-27 — current seats are Codex, Grok x2, DeepSeek. See `docs/ref/ZAI_API_EXPERT_REFERENCE.md` for current lanes.

# Behavioral Router Interface

**Status:** Desk migration contract · 2026-08-06
```

## Failures

- None.

## Checkpoint

- completed: true
- artifacts: `docs/COORDINATION.md`, `docs/BEHAVIORAL_ROUTER_INTERFACE.md`, `jobs/stale-docs-cleanup/trail_core_1.md`
- failures: none
- budget_used_pct: not tracked (docs-only cage)
- next_action_one_line: stop; this cage is done

## Handoff

- done: banners + stale cursor-lane rewrites in the two named docs; acceptance greps 0; files not deleted
- untested: whether `watch/cursor_bridge.py` still runs (out of scope; not deleted)
- blocked: false
- resume_command: `grok#2: read jobs/stale-docs-cleanup/seat_contract.json + latest trail_core, do next_action, run acceptance, write trail_core_N`
