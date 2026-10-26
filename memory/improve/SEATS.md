# Mag seat matrix — canonical (Phase α)

**Commitment:** `chord-local-first-token-bleed-001`  
**Rule:** Small local models = **janitors**. Grok TUI = **scarce judgment**. Hermes = **parked** (optional lab only).

| Job | Seat | Provider |
|-----|------|----------|
| Route, ask, status, synthesize field brief | **L0 janitor** | Ollama **`gemma:2b`** (clerk/router) |
| Short local write / multi-smoke worker | **L0 worker** | Ollama **`gemma4`** — load, run, prefer unload |
| Scout / improve ledger (no LLM or clerk only) | **L0** | Mag improve (local) |
| Public cheap draft | **L1** | OpenRouter / DeepSeek (keys + budget) |
| Hard code / architecture / promote gate | **L2-TUI** | **Grok TUI** — `[priority]` + context-pack only · **scarce** |
| Multi-file refactor in IDE | **L2-Cursor** | **Cursor IDE** — `launch_cursor_seat.cmd` + hooks → Verkle trail · REST bridge: `watch/cursor_bridge.py` → `POST /api/v1/agent` |
| Tool loop when Grok empty | **L2-agent-cli** | `mag.cmd agent --provider deepseek` — Mag tools + DeepSeek (or ollama) |
| Long autonomous agent (optional) | **L2-Hermes** | **Parked.** Explicit `via hermes` only; 8B+64k on 6GB VRAM is hybrid/slow |
| Big GPU capacity | **L1-cap** | Vast later — not identity |
| Secrets / irreversible | **L3** | Human |

## Janitor doctrine (cooked in)

1. **Useful:** classify, brief polish, field_brief, ask, improve scout/eval, status.  
2. **Not useful:** hour-long self-improve, multi-step Mag CLI under Hermes bash, replacing Grok.  
3. **One model hot** when possible — don’t leave gemma4-hermes + gemma:2b both loaded.  
4. **Grok stays** for hard inference; local keeps context cheap. Leaving Hermes cold does not break Mag.

## Invariants

1. Improve scout never uses paid remote (`remote_llm_for_scout: false`).
2. No auto `ollama pull` unless `max_auto_pull_gb` raised (default 0).
3. Model seat changes need human `promote` + manual `lanes.yaml`.
4. Grok TUI ≠ always-on. Mag L0 is always-on for routing + field improve.
5. Vast is capacity, not identity.
6. Hermes is **not** the router. Private/recall never routes to Hermes.
7. Hermes Mag CLI must use bash-safe paths (`./.venv/Scripts/python.exe`) if re-enabled — PowerShell `.\` paths break under Hermes bash.

## Commands

```text
python main.py lab
python main.py ask "what was I doing?"
python main.py bonds                   # residual bonds → memory/bonds_active.md
python main.py improve --once          # scout + eval + field brief
python main.py improve --synthesize
python main.py dispatch "…"            # default local janitor
python main.py context-pack            # bonds+brief before [priority] Grok
python main.py context-pack --refresh-bonds
python main.py dispatch "…" --seat hermes   # explicit only; expect weak agent
python main.py hermes-status
launch_cursor_seat.cmd                       # Cursor seat: preamble + :8765
python watch/cursor_bridge.py pack           # Cursor REST bridge: fetch context pack
python watch/cursor_bridge.py ask "goal"     # Cursor REST bridge: run Mag agent turn
queue_deepseek.cmd "goal"                    # orchestrator queue → DeepSeek drain
python main.py orchestrator drain --once     # run one queued DeepSeek task
mag.cmd agent --provider deepseek          # tool REPL when Grok tokens empty
mag.cmd agent -q "read memory/working.md" --provider deepseek
```

## CODE TEAM (2026-08-14 rightsizing)

Unused organs, one lane. Not a new throne. GLM Lite is an optional Hermes brain when the key exists — not Mag janitor, not lantern, not grok replacement.

| Job | Seat | Notes |
|-----|------|-------|
| Cheap file edit / complete | **local_coder** | Ollama qwen2.5-coder:7b — already in lanes.yaml worker |
| Multi-file / pytest / implement | **deepseek_agent** | mag.cmd agent --provider deepseek + queue_deepseek |
| Tool loop / skills | **hermes** | Unparked for code only. Brain: GLM-5.2 coding plan IF GLM_API_KEY, else gemma4-hermes local |
| IDE surface | **cursor** | launch_cursor_seat + cursor_bridge — files land in Verkle trail |
| Architecture / invariant | **grok** | [priority] only. Never the mill |

Hermes is still not the router. Private residual never routes to Hermes. Cadence stays L0.

See also: `HABIT.md`, `configs/lanes.yaml`, `configs/providers.yaml`.

## 2026-09-27 REALITY REFRESH (ATLAS_SELF_STEAL Q2; supersedes anything above that contradicts it)

The August-era seat picture below is history. The fleet as it actually stands:

- **Primary seat:** ZCode on the z.ai GLM-5.3 individual coding plan (this repo main agent + workflow children + Task agents). Flash is the workhorse; GLM-5.3 max for judgment lanes.
- **Width laws (measured, see WIDTH_LEDGER_20260926.md):** Task agents clean 3/6/10/12 (109.4M tok/h at 10); workflow children: law caps 3, 50-wide ran hours-clean 2026-09-26 before first 429 (unbanked rung, Stage-2 probe owed); the LITE/start-plan lane is the staff lane for wide-shallow fan-out (quota EXHAUSTED 2026-09-27 in the daily mine: finite, drains in hours of 20-wide digging).
- **Other engines:** Hermes/Nous credits (LAW-11 rescue + second-engine verification, $180 armed, 6 parallel clean); free API lanes (OpenRouter 18 free models / Mistral / Cohere / DeepSeek, 12 parallel clean); local ollama (gemma4 present); offpeak idle gophers.
- **Routing law (LINKS-342):** lite/free = mass, heavy = judgment, Hermes = rescue; per-run per-organ, never per-subscription; the flywheel is the ORGAN STATE (ledgers, saved workflows, catalog, bonds), lanes are bearings.
- **Discipline organs born since August:** workflow gate G1-G7 + scenario cards (LAW-12), burn program (hourly cron, PAT demotion), falsifier registry, drift instrument + probe20, stateless visor, ledger lock.
- **Load order truth:** state/CURRENT.md is the live brief (briefs/latest.md FROZEN 2026-09-26; context-pack serves CURRENT since the Q1 fix this day).

## COMPILED SEAT REALITY (tools/compile_seats.py; regenerated, do not hand-edit below this line)

Source anchor (newest source timestamp): 2026-10-21T12:51:40+00:00. Every bullet names its source file.

### Seats and lanes as configured

- Default lane: L0 [src: configs/lanes.yaml]
- Lane L0: local via ollama [src: configs/lanes.yaml]
- Lane L1: free_remote via openrouter [src: configs/lanes.yaml]
- Lane L2: specialist via grok_harness [src: configs/lanes.yaml]
- Lane L3: human via wait [src: configs/lanes.yaml]
- Local models: clerk=gemma:2b, router=gemma:2b, orchestrator=gemma:2b, desk_orchestrator=qwen-desk:latest, desk_conductor=qwen-desk:latest, voice=gemma:2b, worker=qwen2.5-coder:7b, critic=qwen-desk:latest, biographer=qwen-desk:latest, embed=nomic-embed-text [src: configs/lanes.yaml]
- Load policy: mode sequential, max_resident 1 [src: configs/lanes.yaml]
- Hermes: parked=False, role=code_team_tools, not_router=True [src: configs/lanes.yaml]
- Grok budget: max_escalations_per_day=2, require_priority=True [src: configs/lanes.yaml]
- Provider prefer_order (16): ollama, z_ai, openrouter, groq, together, github_models, moonshot, fireworks, cohere, hf_router, dashscope, deepseek, deepseek_overmind, anthropic, openai, xai [src: configs/providers.yaml]
- Provider blocks: 28 declared, 22 not dormant, 6 dormant (cerebras, gemini, mistral, nvidia, saelis, z_ai3) [src: configs/providers.yaml]
- Leave-protocol mates (8): cartographer, locksmith, archaeologist, innkeeper, jester, lamplighter, mariner, gambiter; schema mag_mates.v1 v2026-10-12 [src: configs/mates.yaml]
- Lane runner bard_ledger (seat bard_ledger): last_run 2026-10-20T20:00:38.262038+00:00, last_result `row` [src: queue/lanes/bard_ledger/runner_state.json]
- Lane runner builder (seat builder): last_run 2026-10-21T12:34:15.484193+00:00, last_result `gated=0` [src: queue/lanes/builder/runner_state.json]
- Lane runner day_work (seat day_work): last_run 2026-10-21T12:34:16.130632+00:00, last_result `mirrored, stalled=1` [src: queue/lanes/day_work/runner_state.json]
- Lane runner economist (seat economist): last_run 2026-10-21T06:00:30.577243+00:00, last_result `hunger rc=0, sweep_flags=6` [src: queue/lanes/economist/runner_state.json]
- Lane runner elder (seat elder): last_run 2026-10-21T12:00:41.731670+00:00, last_result `lens` [src: queue/lanes/elder/runner_state.json]
- Lane runner forge (seat forge): last_run 2026-10-21T12:00:41.923790+00:00, last_result `forged=0 left=0 err=0` [src: queue/lanes/forge/runner_state.json]
- Lane runner harvest (seat harvest): last_run 2026-10-21T06:31:49.304293+00:00, last_result `fetched=300 new=300 hits=6` [src: queue/lanes/harvest/runner_state.json]
- Lane runner night (seat night): last_run 2026-10-20T23:02:16.186412+00:00, last_result `monitor rc=0; march rc=0` [src: queue/lanes/night/runner_state.json]
- Lane runner prose (seat prose): last_run 2026-10-21T05:37:55.100358+00:00, last_result `census files=30448 stale=16758 fossil=24 ghost=3529 launchers=336` [src: queue/lanes/prose/runner_state.json]
- Lane runner research (seat research): last_run 2026-10-21T12:51:40.911691+00:00, last_result `monitor rc=0, drops gated=0` [src: queue/lanes/research/runner_state.json]
- Orchestrator (DeepSeek drain) events in the 7d before 2026-10-20T17:02:32+00:00: done 2, failed 275, killed 1, queue-add 201, queue-defer 21, queue-end 20, queue-fail 184, queue-purge-failed 7, queue-start 23, seat-steer-inline 142, spawn 295, timeout 17 [src: memory/runs/orchestrator_trail.jsonl]
- Operator session cards: 35 zknot cards; newest 2026-10-19_sess_75613dea-007b-4b22-a2cc-b00b44a04cf7.md (2026-10-19 15:45 ET to 2026-10-21 06:45 ET (38h 59m)) [src: memory/zknot/]
- Live brief present: state/CURRENT.md (load-order truth per the 2026-09-27 refresh) [src: state/CURRENT.md]

### Drift: hand matrix vs live config

- Hand matrix says L0 worker = gemma4; live config local_models.worker = qwen2.5-coder:7b [src: configs/lanes.yaml]
- Hand matrix says L2-Hermes = Parked; live config hermes.parked = false (role code_team_tools) [src: configs/lanes.yaml]

Rebuild: `python tools/compile_seats.py --swap` (registered in configs/fossil_registry.json).
