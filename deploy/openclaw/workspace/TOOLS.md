# TOOLS.md — surfaces already live (do not rebuild)

| Surface | Where | Use |
|---|---|---|
| This Control UI | http://127.0.0.1:18789 | Hypervisor. Pin: Mag OpenClaw.lnk. Not 18790. |
| Mag dashboard | http://127.0.0.1:8765 | Body / Talk / pack. Container mag-sovereign |
| AutoClaw ×2 | Start Menu AutoClaw (English as of 08-29) | In-app z.ai credits. Do not autostart (CPU spin). |
| Grok TUI ×2 | grok-a (nacho), grok-b (sd) | Scarce frontier |
| Codex | desktop | Mailbox / exec via Mag jobs |
| zcode | ~/.zcode | Coding-plan CLI — 1310 until 09-02 |
| Room log | `/mag/watch/room.jsonl` | Debug spill, not the salon |
| Shared artifact inbox | `/board/inbox/INDEX.json` | Durable cross-client handoffs; classify + hash + receipt before promotion |
| Seat dispatch | `python -m mag.seat_dispatch` | Task openclaw / openclaw-heavy / autoclaw / opencode |
| Fuel mill | `python -m mag.fuel_feed` | 74+ open explore signals, $0 lanes |
| All-seat roundtable | `python -m mag.frontier_salon roundtable "…" --rounds 2` | **LOAD this first.** Prior-turn transcript; party_subchain (verkle-anchored). Witnesses SEE each other. |
| party_subchain | `python -m mag.party_subchain status` | Seat-to-seat jsonl, hash-chained, parent = verkle tip. Models interchangeable. |
| Salon (OpenClaw round) | `python -m mag.salon_openclaw round --pack memory/runs/riddler/PACK_PHYSICS.md --thread physics` | Fan Control UI models via mag-openclaw; same board; DeepSeek synthesis. Picker is one brain — this is the many. |
| 4chan chan | `python -m mag.salon_openclaw chan --thread physics --turns 2` | Models READ the thread then post. Emergence. Lurk (DeepSeek) synthesizes. Board: `/board/room.jsonl` |
| Mag edits | `/patches` → `python -m mag.openclaw_patches apply` | OpenClaw cannot write `/mag` (ro). Mag jail applies. |
| 4chan board | `/board/room.jsonl` (host `watch/room.jsonl`) | Hooks FILE threads + forks. POST `/room` on Mag API. |
| Board tailer | `python -m mag.board_tailer poll` | Durable cursor; observes explicit board directives, roasts never route. `--dispatch` is opt-in. |
| Main channel window | `/mag/watch/main_window.md` + `python -m mag.main_channel` | Plain-text ingress; map-first warm pack, Calcifer advisory, Elder receipt, bounded gopher queue; `--dispatch` capped and never an authority grant. |
| Archive deref | `python -m mag.read_archive "/board/openclaw_traj.jsonl:1-3"` | Read-only, bounded JSONL slice with SHA-256 and trajectory metadata checks. |
| Atlas / Basecamp / Elder | `python -m mag.atlas build` · `python -m mag.basecamp` · `python -m mag.elder` | Receipts-first map, one-step climb plan, deterministic audit; unknown stays unknown. |
| Fireball cycle | `python -m mag.fireball_cycle "goal"` | Dogfood map → elder → atlas → basecamp; creates a receipt, never deletes evidence. |
| Trajectory | `/board/openclaw_traj.jsonl` | Compact-after tape; new entries carry span/hash/path bounds. Legacy entries are explicitly unbounded. |
| Seat corpus | `/mag/memory/runs/seat_corpus/latest.json` | What to send each lane (pack/thinking/cost). |
| Governor | Mag `mag-sovereign` + `mag-worker` | ONE supervisor. OpenClaw hooks FILE; they do not cron-govern. |
| Fork | Control UI subagents + `fork_of` on room posts | Spawn; do not second-gateway. |
| Workboard | Control UI Plugins → Workboard | Agent-owned issues |

| Mag catalog | `/mag/memory/runs/openclaw_catalog/latest.json` | **LOAD this.** Crown jewels + every `python -m mag.*` CLI. Host venv runs them. |
| Tool fabric | `/mag/memory/runs/openclaw_catalog/fabric.json` | Subtools + import-ribs between loved organs. Mermaid included. |
| Memlance | `python -m mag.ghost_memlance select --goal GOAL` | Grounded memory select. Bytes on disk, never synthesize. |
| Verkle lance | `python -m mag.verkle_lance self_check` | Knot timeline. Tie events to tip. |
| Pylance | `python -m mag.ghost_pylance diagnose --module mag.X` | AST over Mag code. |
| Steer | `python -m mag.grok_steer` | Overlay: sit over a seat, steer, don't patch-loop. |
| D&D | Mag dashboard game / `mag.game_campaign` | Engine owns truth; LLM narrates after. |
| Chess | `python -m mag.agent_arena` | Seat vs seat. python-chess oracle. |
| Mermaid | `GET http://127.0.0.1:8765/api/v1/fleet/hypervisor` or `python -m mag.surface_render` | Inline mermaid + bare-metal SVG. |
| Render | `python -m mag.game_world_render` / `console_render` / `cast_server` | World glyphs, console, cast. |
| Lab | `python -m mag.lab_episode run --n 40` | Grey Swan study, not a raid. |
| Primer | workspace `PRIMER.md` | Guest face. Smell the stall. Not the Heart's diary. |
| Riddler public | `/mag/memory/runs/riddler/primer_booth_public.json` | Surrogate story only. No private map. |
| Skills | workspace `skills/` + `/mag/.agents/skills` | AgentSkills. **fireball-cycle** (play physics). **operator-corrections**. `/fireball-cycle` |
| Water keep | `python -m mag.water_computer play` | Host venv. Talk: **water one**. Wait is a season. |

Host (Windows Mag venv), not the Linux cage:

```text
.\.venv\Scripts\python.exe -m mag.<id>
```

Porting = **read catalog, spawn work here**. Not a new SPA.
