# f-13: promise-vs-reality gap analysis - FRAMEWORK_LOAD.md + MAG_MYCELIAL_REPUBLIC_COMPASS.md

**Item:** f-13 (census) · **Date:** 2026-09-28 · **Seat:** workflow child fire-f-13
**Subjects read in full:** `docs/FRAMEWORK_LOAD.md` (289 lines, commitment framework-load-001, as-of 2026-08-05) and `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md` (259 lines, commitment mag-mycelial-republic-compass-001, as-of 2026-08-05, section 4 FROZEN-stamped 2026-09-26).
**Question:** do the two load-order docs promise things the repo actually has?

## Method (every command run this pass)

1. Existence sweep of 78 paths (76 doc-cited + 2 AGENTS.md cross-checks) via venv python script over `os.path.isfile/isdir` (script: temp, numbers below are its stdout).
2. `.venv/Scripts/python.exe main.py --help` - full argparse subcommand list captured.
3. `ollama list` - full model inventory (16 models).
4. `netstat -ano | grep :8765`.
5. `./mag.cmd doctor` - executed 2026-09-28T21:47:49Z.
6. `.venv/Scripts/python.exe main.py fkb stats`.
7. `.venv/Scripts/python.exe main.py v3-status`.
8. `.venv/Scripts/python.exe main.py context-pack --help | grep mode`.
9. `git ls-files | grep -i gstd` and `git ls-files | grep -iE "grok_hook|escalate_grok|handoff_loop"`.
10. Greps: `configs/releases.yaml` (v2/v3/v4 gates + status), `docs/ref/releases/VERSION_REGISTRY.md` (v1-v10 table), `configs/version_roadmap.yaml` (service_milestones), `configs/lanes.yaml`.
11. Read: `LOAD.md` (root pointer), `memory/briefs/latest.md` head, `queue/todo.md` head, `watch/inbox/GSTD_T0_PROBE_20260918.json`.

## 1. File promises: 77 doc-cited paths checked, 75 exist (97.4%), 2 missing

The two docs between them cite 77 discrete repo paths (every backticked path in both files was swept; per-path line citations in the sweep output). Both missing are on ONE line of FRAMEWORK_LOAD (Tier 3, `docs/FRAMEWORK_LOAD.md:114`):

| Missing path | Cited at | Reality found |
|---|---|---|
| `docs/ref/DECISION_LAYERS.md` | FL:114 | no such file anywhere tracked |
| `docs/ZEITGEIST.md` | FL:114 | missing; real file is `docs/archive/ZEITGEIST.md` (exists, verified). AGENTS.md already concedes this: "the `docs/ZEITGEIST.md` path cited before 2026-09-14 never existed". FL:114 still cites the dead path |

Everything else the docs promise exists, including all 25 Tier-2 role files (`docs/FRAMEWORK_LOAD.md:95-110`: MAG_v2_PLAN, modules.yaml, v3 RESEARCH/BACKLOG/SWARM/SWITCHBOARD, BUILD_PIPELINE, FACTORY_PILOT, BUILD-TEMPLATE, MOBILE_VOICE_SPEC, JONES_AGENT_FLEET_PACK, MAG_AGENT_ERROR_CATALOG, LLM_FEED_PACK, NEXT_CODING_RUN, V3_DISPATCH_PLAN, BEHAVIORAL_COMPOUNDING, PONYTAIL_CAVEMAN_SKILLS, v4_THEORY, HOW_TO_MAG_DASHBOARD, LAYMAN_OFFICE_VISION, CONTAINER, AGENTIC_LANDSCAPE_2026, STEAL_AUTOPILOT, strike_origin, MAG_Activation, memory/handoff/ACTIVATION), all release artifacts (RELEASE_NOTES_v1/v2/v3.md, MAG_V4_CONDUCTOR_LOOP_DRAFT.md, MAG_v5_PIPE.md, VERSION_REGISTRY.md), all configs (version_roadmap.yaml, releases.yaml, data_tiers.yaml, lanes.yaml, modules.yaml, cost_rates.yaml), the runner scripts (mag.cmd, mag.ps1, home_sync.cmd, launch_cursor_seat.cmd, pull_mesh_comm_repos.sh, pull_gstdcoin_repos.sh), and the root pointer `LOAD.md` which does point at exactly these two docs first (`LOAD.md:3,10`).

## 2. Command promises: 20 distinct commands exist in main.py argparse; 4 executed

`main.py --help` confirms every promised verb exists: run, doctor, context-pack, ask, brief, watch, dashboard, lab, bonds, improve, promote, research-pack, autorun, verkle-audit, fkb, v3-status, skill-seat, cost-sim, orchestrator, mag. Executed this pass:

| Command | Promise | Result |
|---|---|---|
| `mag.cmd doctor` | FL:76 "After read: doctor"; FL:134 "See if Mag is healthy"; compass §5 install gate "doctor green" | **RAN: status=degraded, ok=false** (2026-09-28T21:47:49Z). Missing: "integral Mag process". JSON: `"up": false`, `"pid_alive": false` while the same block's heartbeat says `"alive": true, age_seconds: 0.29` - a self-contradictory integral check. Lanes all green: L0_ollama ok, L1_openrouter ok, L2_grok ok; `port_8765: true`, `board_api: true`, `backend_api: true`. So the tool exists and runs, but the promised green gate is red today |
| `main.py fkb stats` | FL:143 "Check what failed before" | **RAN: ok=true** - 10,000 events, 1,421 signatures, 393 recurring, 10 with_remedy, logs/failure_kb.jsonl. Promise kept |
| `main.py v3-status` | FL:217 | **RAN: ok** - "Shipped: 8, Research: 6, Pilot: 4" registry table; resonance/spider/conductor/grove all "research" as FL:217 claims. Promise kept |
| `main.py context-pack --help` | FL:159 `--mode janitor` | **RAN: flag exists**, choices {janitor,route,build,audit,plan,full}. Promise kept |

Exists-but-not-executed (existence verified only, no runtime claim): ask, brief, watch, run, dashboard UI, lab, bonds, improve --once/--status, promote --apply, research-pack, autorun --once --dry, verkle-audit --dry, skill-seat, cost-sim, mag.ps1, home_sync.cmd, launch_cursor_seat.cmd, pull_mesh_comm_repos.sh.

## 3. Live-surface promises verified TRUE

- **Office :8765** (FL §1, compass §2.2): `netstat` shows `127.0.0.1:8765 LISTENING` PID 14308.
- **Local seats** (FL §6 gemma:2b/gemma4; compass §2.1 qwen-desk): `ollama list` has all three - gemma:2b, gemma4:latest, qwen-desk:latest (16 models total; also qwen2.5:7b/32b, gemma4-desk, gemma4-hermes).
- **handoff.v1** (compass §2.2): `queue/handoff/` 133 entries, `queue/results/` 93 entries.
- **Training events** (compass §2.2): `memory/training/events.jsonl` exists, 573,031 lines.
- **grok_hook / escalate_grok** (compass §2.2/§4 "Shipped"): tracked at `watch/grok_hook.py` and `agents/escalate_grok.py`.
- **Meta lanes** (compass): `configs/lanes.yaml` exists, `default_lane: L0` matching "janitor first".
- **tier_refuse gate** (compass §6): `configs/releases.yaml:65` gate id tier_refuse, description "T0/T1 never hit remote providers (tests)".
- **Machine truth pointers** (compass §0): version_roadmap.yaml has `service_milestones` at line 158 as promised; both configs exist.
- **Compass §4 live-truth pointers**: state/CURRENT.md, watch/inbox/INDEX.json, and SEED_SELF_STEAL_AUDIT_20260926.md (found at `watch/inbox/SEED_SELF_STEAL_AUDIT_20260926.md`) all exist.
- **In-tray** (FL §1): queue/todo.md has live content (P0 Cerebras decision logged PARKED by operator).

## 4. The gaps (ranked)

**G1 - Compass version table contradicts its own declared machine truth (v3, v4).** Compass §3.2 (`MAG_MYCELIAL_REPUBLIC_COMPASS.md:126-127`) says v3 "in_progress", v4 "planned". Its own "Machine truth" (`:9`) is configs/releases.yaml, which says `id: v3 ... status: shipped` (`configs/releases.yaml:70`) and `id: v4 ... status: shipped` (`:95`); VERSION_REGISTRY.md agrees (`:31` v3 shipped, `:32` v4 shipped). The compass's own amend protocol (`:242-243`: "New version gate passed -> release record + update VERSION_REGISTRY") was followed for the registry but the §3.2 table was never amended. Partial excuse on file: the §4 FROZEN stamp (`:141`) froze only §4 and explicitly left "Vision prose (section 1-3, 5+) untouched this turn" - so the stale table is deliberate leave-alone, but it is still live contradiction for any reader the compass tells to trust releases.yaml. Compass honesty clause `:118` ("v3-v5 have planning artifacts and partial implementation") is also outdated: v3 and v4 have graduation notes recorded green.

**G2 - "doctor green" install milestone is red today.** Compass §5 (`:172`): install = "doctor + routing_smoke green". `mag.cmd doctor` on 2026-09-28 returns ok=false / status=degraded (integral pid check contradictory: heartbeat alive:true, pid_alive:false, up:false) while every lane and both ports answer green. Not run: `scripts/routing_smoke.py` (the other half of the gate), so the gate is half-measured; the doctor half fails as of this pass. FRAMEWORK_LOAD also opens with doctor (`:76`) with no degraded-state caveat.

**G3 - FL promises "Current dossier (L0)" that is a sealed fossil.** FL Tier 1 row 5 (`docs/FRAMEWORK_LOAD.md:82`): `memory/briefs/latest.md` "Current dossier (L0)". The file's own head: "FROZEN as-of 2026-09-26 (Mag P0-1 warm-face) ... body below is a fossil ... writers sealed ... Truth instead: verkle_tip.json, state/CURRENT.md, watch/inbox/INDEX.json". The doc was not updated after the freeze; a Tier-1 reader is pointed at a file that orders them not to consume it.

**G4 - Tier 3 dead links (the only file-existence misses).** `docs/ZEITGEIST.md` (dead path, live twin at docs/archive/) and `docs/ref/DECISION_LAYERS.md` (no twin found), both `docs/FRAMEWORK_LOAD.md:114`. FL has no FROZEN stamp or as-of update since 2026-08-05 header despite 7+ weeks of drift.

**G5 - GSTD "6/6" claim unverifiable; only tracked probe artifact is 404s.** Compass §4 (`:155`): "GSTD probe 6/6 repos". The probe module is real (`mag/gstd_probe.py` tracked, plus scripts/pull_gstdcoin_repos.sh/.cmd and docs/ref/GSTDCOIN_REPOS_INDEX.md). But the one tracked probe result, `watch/inbox/GSTD_T0_PROBE_20260918.json`, contains six endpoints each answering `"error": "HTTP Error 404: Not Found"` - a forensics artifact of a dead service, not a 6/6 pass. I did not re-run the probe (not asked; remote-side). The 6/6 claim is a frozen 2026-08 snapshot presented in a table the freeze stamp itself says not to trust.

**G6 - "handoff_loop" has no named artifact.** Compass §2.2 (`:99`) and §4 (`:159`) list handoff_loop as a shipped surface. `git ls-files | grep handoff_loop` returns nothing and main.py has no such subcommand (nearest real surfaces: main.py `deep-handoff`, the 133/93-entry queue dirs, agents/escalate_grok.py). The function likely lives under other names; the promise is unverifiable by the name the compass gives.

**G7 (minor) - the two docs disagree with each other on load order.** FL §0 copy-paste block lists 7 items (`:16-23`); FL §2 Tier 0 lists 9 rows adding MAG_VISION_AUTOMATION.md and docs/DNA.md and double-numbers two rows "4" (`:64-74`); compass §0 lists 8 steps (`:19-27`). A navigation doc with three different load orders is self-drift.

## 5. Not run / not verifiable this pass (stated, not guessed)

- `scripts/routing_smoke.py` (install gate second half) - not run.
- GSTD probe re-run and the "6/6" figure - not re-run; only artifact found shows 404s.
- qwen-desk "~69 t/s" (compass `:150`) - no benchmark run.
- T0/T1 tier_refuse tests execution - gate config verified, tests not run.
- "Fork the repo and run :8765 without permission" (compass §1 operator test) - not tested.
- G1-G4 autorun gates (FL:188-189) - autorun --dry not executed this pass.
- FL seat table's DeepSeek/Grok/Cursor runtime behavior - lane booleans from doctor only (L2_grok ok=true; DeepSeek/Cursor not probed).

## 6. Verdict

The docs are excellent at file navigation and slightly dishonest at status: **75 of 77 cited paths exist (97.4%)**, all 20 promised commands exist in argparse, the desk is live, the named models exist, and the four executed commands run (three green, one red). The reality gap is concentrated in **status claims**: the compass's version table trails its own machine truth by two shipped versions (G1), the promised green doctor is degraded (G2), the promised current dossier is a sealed fossil (G3), and the GSTD 6/6 figure has no supporting live artifact (G5). The compass partially protects itself with FROZEN stamps and "trust tip not this table" (`:143`) - an honesty device FRAMEWORK_LOAD entirely lacks, which is why FL carries the dead links and the fossil-pointer without any on-page warning. Net: load-order trust high, status-table trust low, and both docs should inherit the compass's stamp discipline.

*Receipt: watch/inbox/burn_reset_20260927/flash50/f-13.md (+ byte-identical mirror promise-gap.md), item f-13, 2026-09-28.*
