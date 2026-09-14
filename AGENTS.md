# local_sovereign_agent — harness rules

**LLMs: load framework first → `docs/FRAMEWORK_LOAD.md`** (or repo root `LOAD.md`) · then **`docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md`** (compass)

This project is the **Mag Resource Harness** (standalone product home): local Ollama **janitors** first (`gemma:2b` scut, `gemma4` short worker), **remote specialist scarce** for hard inference, Hermes **dormant but dispatch-capable** (dispatch log active 2026-09-09, $220 armed — audit 2026-09-14), biographer + orchestrator.

**DNA:** residual + registry + leaf = filed workdays (`docs/DNA.md`). Lab is optional ops.  
**Zeitgeist:** beads (this repo) + forest (mycelial-republic) — `docs/archive/ZEITGEIST.md` (era 003: THE POUR; the `docs/ZEITGEIST.md` path cited before 2026-09-14 never existed). No core-mirror throne.

## Shared artifact boundary — every client

All durable cross-surface work lands on the shared inbox. A VS Code, Cursor, z.code, Grok, Codex, PowerShell, Linux, WSL, or OpenClaw-local session directory is cache only and must never be the sole copy.

| Context | Read first | Durable write root |
|---|---|---|
| Windows host / Mag venv | `watch\inbox\INDEX.json` | `watch\inbox\` |
| Docker / OpenClaw | `/board/inbox/INDEX.json` | `/board/inbox/` |
| WSL | `/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/INDEX.json` | same directory |

The machine contract is `watch/inbox/SHARED_SURFACE_CONTRACT.json`. Read the index, classify content before reuse, preserve hashes and bounded pointers, and leave a receipt before promotion. Model text can propose; only the switchboard/effect broker authorizes effects. Validate with `.venv\Scripts\python.exe -m mag.shared_surface validate`.

## 🖇️ Clippy — standing reminders (always-on, verkle-knotted)

> It looks like you're trying to work on Mag. Would you like a reminder? *(You do not have a choice. The rope is verkle-committed.)*

- **New window?** → execute the frozen spec: `/memories/session/next-window-handoff.md`. Design is done; this is **execution → LOW tier** (flash-off or local).
- **Tests:** 1,341 tests / 264 files (2026-09-14 census: 1305 passed / 34 failed / 9 skipped, ~12 min — the old "39 deterministic green" was a fossil). Run `pytest -q` before claiming done, file the real numbers, and never trust a hand-written count. **Trust bytes, not reports.**
- **Deliberate-ask:** strong asks = frozen RIB (system+bootloader+manifest+verkle tip) + small ask + output contract + quantize target. **Pay the context tax once.**
- **Thinking-mode is the axis** (not flash vs pro) — tune it before tier (design_vague proved it).
- **Pile habit:** escalation/session-close → `mag.state_snapshot.capture_summary`; overnight → `main.py pile-classify`. Contribute your state summary before you go.
- **Tier ladder:** ollama → free tiers (gemini/groq/z.ai…) → deepseek flash → pro/grok (only judgment climbs).
- Invocable: `python main.py clippy` · full doctrine in repo memory (DELIBERATE-ASK · PUPPETEER GAUNTLET · PILE).

## Load order (agents — do not skip)

| # | File | Why |
|---|------|-----|
| 1 | `docs/FRAMEWORK_LOAD.md` | Navigation, metaphors, use cases, commands |
| 2 | **`docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md`** | **Compass** — vision, agent loop, v1–v10 arc, sovereignty |
| 3 | **`docs/ref/MYCELIAL_SCIENCE_MAP.md`** | **Biology ↔ protocol** — mycelial science map |
| 4 | `docs/ref/MAG_DIRECTION_ARTIFACT_v2.md` | Phase gates, v3–v5 mold |
| 5 | `docs/ref/MAG_PROJECT_PROPOSAL.md` | Problem depth |
| 6 | `docs/ref/OPERATOR_CARD.md` | FIND · FILE · LOAD |
| 7 | `AGENTS.md` | This file — env + commands |
| 8 | `mag.cmd context-pack` | Min-token pack for your seat |

Machine arc: `configs/version_roadmap.yaml` · Version index: `docs/ref/releases/VERSION_REGISTRY.md`

Then: `memory/briefs/latest.md` · `queue/todo.md` · `HANDOFF_MAG_AGENT_TODOS.md` if implementing.

## When a specialist seat is used

- Prefer `memory/briefs/latest.md`, `memory/live_from_grok.md`, `memory/attention.md`, `queue/todo.md`.
- L2 escalate needs `[priority]` / `[L2]` (see `configs/lanes.yaml`) unless force.
- Mag escalations may call the harness or `queue/handoff/*.json` with **brief attached**, not full chat.
- Do not claim R0; T0/T1 stay local.

## Python env (do not skip)

**Default shell `python` is often Hermes** (`…\hermes-agent\venv\…`) — no Mag deps → `No module named 'langgraph'`.

Always use **this repo's** interpreter:

```text
mag.cmd doctor                # preferred (no PS execution policy issues)
mag.cmd context-pack
.\.venv\Scripts\python.exe main.py <cmd>
```

Repair / create venv: `powershell -ExecutionPolicy Bypass -File .\scripts\ensure_venv.ps1`  
Agents: call `.venv\Scripts\python.exe` or `mag.cmd`, **never** bare `python` on PATH (Hermes).

## Commands

```text
mag.cmd lab                   # product UI :8765 (+ flags for watch/mag)
mag.cmd dashboard             # UI only
mag.cmd brief                 # L0 dossier → memory/briefs/
mag.cmd ask "…"               # biographer Q&A local
mag.cmd mag --once            # companion cycle
mag.cmd watch                 # tail specialist sessions
mag.cmd run "goal"            # single graph job
mag.cmd context-pack          # min-token pack for TUI (bonds+brief)
mag.cmd bonds                 # residual next-session edges
mag.cmd improve --once        # daily scout + eval → memory/improve/
mag.cmd improve --status
mag.cmd promote --apply c-…   # human gate for candidates
mag.cmd research-pack …       # public URL → local pack
python main.py autorun --once --dry   # plan drainer (no execute)
python main.py verkle-audit --dry
```

**Metaphors + use cases:** `docs/FRAMEWORK_LOAD.md` §1–§3  
**Seats / habit:** `memory/improve/SEATS.md` · `memory/improve/HABIT.md`  
**Daily task:** `scripts\register_improve_task.ps1` → MagImproveDaily 08:00  

## Constitution

See `CONSTITUTION.md` → mycelial-republic `docs/CONSTITUTION.md`.
