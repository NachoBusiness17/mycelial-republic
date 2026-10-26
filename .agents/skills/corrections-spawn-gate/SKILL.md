---
name: corrections-spawn-gate
description: CHECK live sessions before spawning any background agent, never cancel running work on interrupt, and treat first rate limit as HOLD (laws 16 + 28 + 30). Use before every background spawn, agent interrupt, or width decision during burn windows.
when_to_use: Before spawning any background agent; on any interrupt urge; at any width decision.
argument-hint: [check] (run the spawn gate now)
---

# CHECK - one steerer, no unwatched spawns (laws 16, 28, 30)

The concurrency collision (2026-09-05): two parallel background builders +
the operator's own windows hit the user concurrency limit - A2 died at
04:20Z ("user concurrency limit exceeded") mid-build, and the slots the
subagents held starved the operator's other sessions. Operator: "the
subagents were fucking us... this is exactly why we need the vision model
steering this 300m burn." The burn is steered by ONE vision-capable seat
reading the board, working IN-SESSION.

GATE (hard, run before EVERY background spawn): run the steering pass and
check LIVE SESSIONS - if more than one session is warm, spawn NOTHING; do
the work in-session. A worker that must run in background gets one slot, a
deadline in its prompt, and the steerer watches for its completion notice -
no notice within the deadline = TaskStop it, then finish its work in-session
(the A2 pattern: the corpse's build was 90% done and needed only a receipt).

NEVER CANCEL (law 28): "STOP CANCELING BACKGROUND AGENTS" / "Don't cancel
shit when I interrupt there is a standing background rule come on."
Interrupt does not kill work; cancelled agents get relaunched (Mickey 17).

MAX USEFUL WIDTH (law 30): "run parallel, run 12 agents in this window" /
"push our width on everything ... USEFULLY." First rate limit = HOLD, not a
width cut. Refinement 9/30: wide for parallel independent work, narrow for
sequential or spine-touching work. (Account-specific caps: AGENTS.md
fan-out width law.)

## Command

```bash
.venv/Scripts/python.exe -m mag.burn_steer   # one $0 steering pass: board + LIVE SESSIONS
```

Final response: live-session count from the board, the spawn verdict
(IN-SESSION / one-slot-with-deadline), the deadline set if a worker launched,
and the width posture (HOLD or widen) with its law cite.
