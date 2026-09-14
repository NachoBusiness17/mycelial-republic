# FLEET_STRUCTURE — OpenClaw harness per AutoClaw/Grokbot pattern (2026-09-01 01:52Z)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: six harness seats and five lanes can be staffed entirely from existing keys with zero acquisition — UNPROVEN (seat map mixes live and unwired; no per-lane receipts in card) · falsifier: a needed capability with no existing key, or a wired lane failing to sustain its standing job within quota

Doctrine: STRUCTURE-OVER-ACQUISITION (bus 01:52Z) + JIT RIGHT-SIZE LAW + LANE_SLOT_MAP (verbatim, /board/LANE_SLOT_MAP_20260901.md).
Nothing new to acquire. Everything below routes existing keys. Red line honored: no new cages, no second supervisor — the orchestrator already exists (sessions_spawn + workboard + seat_dispatch).

## The pattern borrowed

AutoClaw and Grokbot are not models — they are **harnesses with jobs**: dedicated seat, named role, standing budget, standing job, durable handoff. OpenClaw gets the same: every seat below is a harness block, not a raw model call.

## The seat map

| Seat | Pattern from | Backing lanes (slot-map applied) | Standing job | Status |
|---|---|---|---|---|
| **Director** (frontier direction) | Grok TUI grok-a/b | Grok TUI (scarce, judgment only) + 5.3-flash-high brain on zai-pro + full-5.3/Sol API escalation | verdicts, what-to-build calls, HOT-gate tiebreaks — never labor | live |
| **Driver** (day interactive) | AutoClaw harness | 5.3-flash billed API day / zai-pro $0-marginal | operator session, idea play, artifact birth | live, route fixed 01:21Z |
| **Hands** (coding labor) | AutoClaw | DeepSeek flash (2500 conc, off-peak) + coding-plan quota off-peak + **codex desktop seat ($0-marginal, pending paste)** | frontier coding tasks, fan-out coding, probe batteries | lanes live; codex seat idle |
| **Tail** (mechanical) | — | glm-4.7-flash ($0) + ollama local-dumb (T0, electricity) | dedupe, link-stack, formatting, digest scrub | lanes live; not yet wired into lanes |
| **Swarm** (free agents) | k8s pattern, zero k8s | cerebras 1M TPD + groq + together cached + openrouter | bulk fan-out: harvests, smell lanes, probe loops — real work, not just scut | lanes live; orchestrator exists |
| **Standing self** (cache-mined) | z_ai2 frozen prefix | zai-pro frozen-prefix mining ($0 cache-hit, 97–99.9% measured) | persistent identity/passport surfaces | live |

## The five lanes to wire (each = slot-map + window clock + handoff contract)

1. **Harvest lane** — archivist_feed_harvest (cron, 8h) — calls re-slotted per map
2. **Smell lane** — socratic intake, lensed shots on operator-dropped links
3. **Probe lane** — down-time loop, banked models probed off-peak on plan quota
4. **Coding lane** — frontier coding tasks: Hands = DS-flash + codex paste; Director reviews diffs
5. **Salon lane** — persona-lens shots (ractor), night synthesis on free lanes

## Sequencing (JIT)

Night 1 (tonight, post-apply): prefer_order patch (host: `python -m mag.openclaw_patches apply`) + codex paste → Hands seat complete.
Night 2: lanes 1–3 wiring (existing crons re-slotted).
Night 3: lanes 4–5 + closed-loop actuator (economist → water_windows gate).
Every step receipted; nothing parallel that can be sequential; nothing acquired.
