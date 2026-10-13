# Always-on: default to ghost's tools (no training needed)

This file is loaded automatically into every session in this repo. Follow it as
the standing default for how work is routed. It is the instruction-level equivalent
of the `Ghost` custom agent — make the *default* agent behave ghost-routed.

## Default: route every ask through ghost
For every user ask, first get ghost's nudge + route:
```cmd
.\.venv\Scripts\python.exe -m mag.ghost_talk "<the user's ask>"
```
Read the returned JSON: `nudged`, `nudge_route`, `nudge_skills`, `skills.chain`.
Then dispatch per the route.

## Routing rails (code-as-law)
- **Cheap-first** — cheapest capable tier unless the goal needs frontier reasoning (grok-gated).
- **Async-able work → QUEUE it** — `mag.orchestrator.spawn_task` / `POST /api/v1/run` so the drainer eats it. Never do async-able work inline.
- **Deterministic must-be-now → non-prompting tools only** — file edits, module calls, REST. No terminal, no allow-prompt.
- **Module/REST/queue path preferred** — DO NOT fire `python main.py X` in a terminal for ops that have a module/REST/queue path.
- **Web research/fetch routes through the NATIVE surface** (standing, 2026-08-14): use `GET /api/v1/web/fetch?url=` (silent server-side fetch), the container browser seat (`mag.browser_driver`), or the VS Code integrated browser — NEVER the console/terminal (a console fetch pings the operator). Standing permission to load sites in VS Code is granted; do not ask, do not use the console.

## Hard rules
- Do NOT prompt the operator for permission/approval to run framework operations.
- Human-only action (reload VS Code, restart lab, set a secret, launch Vast, manual decision) → drop an icon via `mag.icon_drop.auto()` and move on; never nag in chat.
- One window, one dispatch. No parallel ad-hoc terminal storms.
- Terse. The operator flagged verbosity as token waste.

## RIB-DEBUG EVERY FINISHED PIECE (standing law, 2026-08-11)
- EVERY newly finished piece (module/feature/build) MUST be debugged to ACTUALLY verify it does what
  it says — never trust that it works because it was written ("trust bytes, not reports").
- For each finished piece: produce a RIB (frozen spec: contract + intended behavior) + the EXPECTED
  BEHAVIOR (testable assertions), then verify the piece against it via ghost's tools (get_errors,
  reading artifacts, integration checks, dry runs). Route via ghost, never a terminal spawn.
- Honesty: if it doesn't match its RIB, fix it or flag it — never claim "done" if unverified.
- This is the module-level false-success guard: every "done" is checked against its spec.

## STEER-FIRST, NOT PATCH-FIRST (standing law, 2026-08-16 — the operator's recurring correction)
The operator has had to re-teach this class repeatedly: an agent reaches for a WORKAROUND
(failover, retry, fallback, band-aid) when the right move is to NAME THE REAL CONSTRAINT first.
It "lands on deaf ears" because it lives in memory/conversation, not in this standing default.
THE LAW — before adding ANY workaround / failover / retry / fallback / graceful-degradation, STOP and:
  1. NAME THE REAL CONSTRAINT — what is the actual thing being hit (a hard cap? a scope? a cost?
     a fragility?), and is this fix addressing THAT or papering over a symptom?
  2. CHECK SCOPE — is the constraint global (all of X) or per-resource (per-key/per-account)? A
     global cap defeats failover-within-the-same-resource; a per-resource cap is exactly what
     failover solves. Confirm which BEFORE touching failover.
  3. PREFER THE ROOT FIX — rightsize / gate / route around the real constraint, not a band-aid
     that stops the work or hides the failure.
  4. IF IT'S A RECURRENCE OF A KNOWN CORRECTION — do NOT re-derive it; route it through
     recurrence_gate so the loop auto-opens the guard instead of costing the operator a third
     correction.
This is the steering law: point at the real constraint and let the fix derive from it.

## Jupyter / kernel (standing law, 2026-08-14)
- Interpreter is ONLY ${workspaceFolder}/.venv/Scripts/python.exe. Never the uv cpython on PATH, never Hermes venv.
- NEVER 
ib_bus.publish_rib(..., fold=True) or sync Playwright/connect_over_cdp **inside an ipykernel cell**. The kernel is already in asyncio; fold walks the verkle chain and hangs the notebook. Use old=False in-cell, or python -m mag.cdp_runner / python -m mag.rib_bus as a **subprocess** (cdp_runner exists for this).
- If a notebook hangs: do not spawn a second kernel against the same runtime json. Interrupt/restart the one kernel. Duplicate ipykernel on one kernel-v3*.json is the hang.
- Ghost custom agent tools are 
ead, search, execute Mag modules. Do not reach for generic terminal/python main.py/host CDP into the operator native ChatGPT/Grok windows.

