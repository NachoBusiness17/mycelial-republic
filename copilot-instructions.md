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
