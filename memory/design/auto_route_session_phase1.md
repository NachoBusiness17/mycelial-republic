# Auto-route on every surface — Phase 1 (session route)

_Schema: design doc · 2026-08-09 · status: built + tested (33 agent/session tests green)_

## The problem (operator)
Typing into a CLI window felt *un-routed*: `launch_agent*.cmd` → `main.py agent` ran a bare
provider and ignored the custom-agent-state routing (agent_state_router / self_drive) that the
queue/gpipes/ghost/handoff surfaces already used. The data behind routing existed
(12.5k decisions_log, 12k behavioral_events, 223 skill_ledger case law, 33 tesuji shells,
tier_probe) but the interactive path didn't read it. Ask: **make it default on every surface**,
**data-backed**, and load a routing invariant ("session seed") into every spawned session.

## What was built (Phase 1)
1. **`mag/session_route.py`** — the data-backed session preamble assembler (deterministic, no LLM):
   - `default_agent_state()` → `MAG_AGENT_STATE` env or `coding-agent`.
   - `read_seed()` → `state/SESSION_SEED.md` (the routing invariant).
   - `formatting_block(state)` → the custom state's resource spec as a prompt block (model/shape/
     thinking/effort/skills/tools/memory).
   - `learned_block(goal)` → failure-KB remedies + skill-ledger case law relevant to the goal
     (reuses `self_drive.learned_principles`).
   - `preamble(goal, state, with_model=True)` → folds in `self_drive.plan` to right-size the model
     (flash vs pro) for one-shot goals.
   - CLI: `python -m mag.session_route "goal"` / `main.py session-route "goal" [--state X] [--json]`.
2. **`state/SESSION_SEED.md`** — the routing-invariant block injected into every session's system
   prompt (auto-route, spend-on-spec, tesuji loop, truth rules).
3. **`mag/agent_cli.py` `_system_prompt()`** — now accepts `goal` / `agent_state` / `preamble` and
   injects `preamble_block` (agent-state formatting + seed + learned) into the system prompt **by
   default** on every path (REPL, one-shot, api_agent_turn). `run_agent` builds the preamble once
   and, for one-shot `deepseek` goals with no explicit `--model`, auto-right-sizes the model from
   `self_drive.plan`.
4. **`tests/test_session_route.py`** — 8 tests (default/env, seed, formatting, preamble shape,
   render, system-prompt injection).

## Verification (trust bytes)
- `session_route` smoke: `agent_state=coding-agent`, goal `fix the done-filter` →
  `model_hint=deepseek-v4-flash shape=cheap` (tier_probe-correct).
- `_system_prompt` default (no goal): injects seed + agent-state + law + context pack.
- Tests: `test_session_route` (8) + `test_seat_crash_guard` + `test_agent_repack` +
  `test_prompt_steering` + `test_resume_contract` (22) + `test_agent_live/desk/t1` (11) — all green.
- Caught + fixed a scoping bug: `render` import was inside `if preamble is None:` → hoisted.

## Remaining phases (not built yet)
- **P2 — Refine button**: REST `POST /api/v1/prompt/refine` wrapping `socratic.workshop` +
  fold `session_route.preamble` (learned case law) into the refined prompt. VS Code command.
- **P3 — Close the learn loop on the interactive CLI**: write route + outcome back to
  decisions_log / skill_ledger on session end (queue side already learns; CLI side mostly doesn't).
- **P4 — Make `MAG_AGENT_STATE` a first-class dashboard setting** (default agent state per surface).

## Doctrine
Spend on the spec, not the tier. Data-backed routing reads case law + remedies; every surface
routes through ONE core. Trust bytes (tests), not reports.
