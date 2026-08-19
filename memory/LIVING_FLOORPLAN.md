# THE LIVING FLOORPLAN — one readable map of the whole system

> Purpose: turn the quilt into a floor plan. Not a rewrite — a map of what exists,
> what's load-bearing, what's worn, and what's dead. The difference between a quilt
> and a system is whether someone can see the whole thing and know what each part does.
>
> This file is the ONE map. When something changes, update it here. When you can't
> hold the castle in your head, read this. Generated 2026-08-17 from real bytes.
>
> Status legend:
>   ✅ PROVEN — rib-debugged / has a test / get_errors clean / verified working
>   ⚠️ WORN  — works but fragile or known-broken seam
>   💀 DEAD  — no caller, safe to retire (candidate)

---

## 0 · The one-sentence shape

**Local-first, sovereignty-grounded agent architecture:** cheap local models (Ollama) do the
scut, Grok gets scarce judgment with a thin pack, DeepSeek is the cheap paid research bus, and
the **governor** is the heartbeat that runs the whole thing while the operator sleeps. Memory is
a **verkle chain** — content-addressed, provable. Nothing phones home.

---

## 1 · The layers (top → bottom)

| Layer | What it is | Where | Status |
|-------|-----------|-------|--------|
| **Operator** | The human. Promote, secrets, irreversible decisions | — | ✅ |
| **Surfaces** | How the operator/agents touch the system: CLI, dashboard :8765, REST :8001, seats | `main.py`, `dashboard/`, `mag/api_gateway.py` | ✅ |
| **Governor** | The heartbeat loop. Runs cadences while idle: grok drive, game flow, distill, janitor | `mag/governor_autorun.py`, `mag/governor.py` | ✅ |
| **Orchestrator** | The queue + drainer. `enqueue()` → `drain_once()` → spawn task. THE work engine | `mag/orchestrator.py` | ✅ |
| **Router / dispatch** | Picks the seat/lane for each ask (local → deepseek → grok tier ladder) | `mag/dispatch.py`, `mag/router.py`, `mag/route.py` | ✅ |
| **Agents / seats** | The actual LLM surfaces: ollama seats, grok seats, chatgpt, deepseek | `mag/agent_cli.py`, `mag/grok_seat_burner.py` | ⚠️ |
| **Memory / state** | Verkle chain, session store, ledgers, piles, case law | `mag/verkle_*.py`, `memory/` | ✅ |
| **Learn / ghost** | The closed learning loop: SENSE→MATCH→DEPLOY→MEASURE→CATALOG→COMPOUND | `mag/ghost.py`, `mag/self_steal.py`, `mag/percolator.py` | ✅ |
| **Game** | The deliverable (the Mirror Sea / Land of Forgetfulness MUD) | `mag/game_*.py` | ⚠️ WORN |

---

## 2 · The five loops that actually run

These are the beating heart. Everything else hangs off them.

| Loop | What it does | Cadence | Engine | Status |
|------|-------------|---------|--------|--------|
| **Governor loop** | Tick → run due cadences (grok drive, game flow, distill, janitor) | continuous | `governor_autorun.tick()` | ✅ |
| **Queue drain** | Eat the orchestrator queue: enqueue → spawn → monitor → finalize | continuous | `orchestrator.drain_once/parallel` | ✅ |
| **Grok drive** | Drive the grok seats (nacho + sd) on contract, watch + correct | 120s | `grok_seat_burner`, `grok_steer` | ⚠️ |
| **Game flow** | The async test→fix loop for the game pieces | 300s | `game_flow`, `game_piece_tandem` | ⚠️ WORN |
| **Ghost/learn** | Sense the field → fold outcomes → compound into reusable core | cadence | `ghost`, `living_map` | ✅ |

---

## 3 · The build image (what we're building right now)

From `memory/game/FLOW_IMAGE.json` — the game pieces in flight:

| Piece | Target module | Status |
|-------|--------------|--------|
| nomic_rules_patch | `mag/game_rules.py` | ⚠️ not built (no such module yet) |
| diplomacy_multi_party | `mag/game_diplomacy.py` | ⚠️ not built |
| pandemic_common_pool | `mag/game_threat.py` | ⚠️ not built |

---

## 4 · Known seams (the honest part)

These are the places the quilt shows. Fix these first; they're the *actual* cleanup targets.

| Seam | What's wrong | Status |
|------|-------------|--------|
| **Witness store** | `flow_autopilot` read results from `swarm_worker`; tests run through `orchestrator`. Two stores never connected → "no result yet" forever. | ✅ FIXED 2026-08-17 |
| **Double-drainer** | Autopilot called `drain_once()` while the governor also drains → `reap_stale()` mis-marked completed tasks `died`. Removed the drain "nudge"; governor is the single drainer. | ✅ FIXED 2026-08-17 |
| **Container→ollama** | Governor container couldn't reach host ollama (dead sidecar + provider hardcoded 127.0.0.1). Fixed `OLLAMA_HOST=http://host.docker.internal:11434/v1` + `base_url_env: OLLAMA_HOST` + breaker reset. | ✅ FIXED 2026-08-17 |
| **Local model tool-calls** | Wiring works, but `qwen2.5-coder:7b` on 6GB VRAM returns `tool_calls: 0` (echoes JSON as prose) — can't reliably run the tool loop. **Model-capability ceiling**, not a wiring bug. A 24GB card fixes it. | ⚠️ OPEN (hardware) |
| **Game flow test lane** | Test agent reaches ollama and proposes the test; needs a tool-capable model that completes the loop. | ⚠️ OPEN (see above) |
| **Hermes venv on PATH** | Bare `python` resolves to Hermes venv (no pytest/deps). Always use `.venv\Scripts\python.exe`. | ✅ known (documented) |
| **Governor not always up** | The cadence loop is a separate process (`mag_up.cmd`), not the container supervisor. Must be started explicitly. | ⚠️ |

---

## 5 · Map engines (these keep the map alive)

These regenerate the map from code — don't hand-edit their outputs.

| Engine | What it produces | Command |
|--------|-----------------|---------|
| `framework_map.py` | Functional grouping (steer/decide/state/learn/run/ops/agents/launch/routes/providers) | `python -m mag.framework_map --json` |
| `code_map.py` | Every module's purpose + invariants → `queue/handoff/CODE_MAP_RIB.md` | `python -m mag.code_map build` |
| `system_map.py` | Live snapshot of direction/learning/operator state | `python -m mag.system_map` |
| `living_map.py` | The distilled core thread: how we got here + what's reusable | `python -m mag.living_map` |

---

## 6 · The game's design canon (point a model here to build it)

The game is buildable-from **these** artifacts — they already exist, this is the "yes" answer:

- `handoff/GAME_DRIVER_RIB_20260814.md` — the driver RIB (cold start, one beat, proof gate, no fan-out)
- `handoff/game_rib_coding_instructions.md` — the 6 build RIBs
- `memory/game/SYSTEM_MAP.md` — the game's self-knowledge
- `memory/game/STORY_ORG.md` — the four-shelf storytelling org
- `memory/game/hero_journey.md` — the tone PROOF (it lands)
- `memory/steal/GRAB_WRITE_DOCTRINE_20260815.md` — reach-before-write; write as the reach lands

---

## 7 · Standing laws (non-negotiable, do not violate)

- **Honesty over over-claiming.** Verify, never hand-wave. "Trust bytes, not reports."
- **Grab-write:** never let the write get ahead of the reach.
- **No monkeypatch on the function-under-test.** Extract pure functions, test deterministically.
- **Route through the architecture,** not ad-hoc terminal spawns. Async-able → queue it.
- **Rightsize, don't pattern-match.** Thin context, not full context.
- **One gated beat at a time.** Do NOT fan out into 5 modules at once.
- **Rib-debug every finished piece** — get_errors + drive the real function + read output.
- **Self-steal before answering.** Check our own system + repo memory first.

---

*This is the living floorplan. Update it as the system grows. When the map and the system
disagree, trust the system — then fix the map.*
