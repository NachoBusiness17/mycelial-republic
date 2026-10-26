# s2-11: full boot path trace, ZCode.exe launch to context pack render

Census lane s2-11, 2026-09-28. Every number below was produced by a command run in this session, or by code read at the cited path and line. Instruments and moments are named per the B2-216 census denominator law: latency numbers are one tree at one moment (2026-09-28 ~18:52-19:15 EDT), with dashboard :8765 UP, tool backend :8000 UP, Ollama :11434 UP (port probes run in-session, 7.0/0.3/0.3 ms).

## The path, stage by stage

### Stage 0: ZCode.exe native launch

- The binary is the Windows Store app OpenAI.Codex, version 26.917.9434.0, install location `C:\Program Files\WindowsApps\OpenAI.Codex_26.917.9434.0_x64__2p2nqsd0c76g0` (`Get-AppxPackage -Name OpenAI.Codex`, run in-session). The dir `C:\Users\foste\AppData\Local\Programs\ZCode` exists but is empty (ls run).
- Its own internal boot latency is NOT measurable from inside a live session; no instrument was run for it and none is claimed. What was verified is the file surface it reads at launch, from disk:
  - `~/.zcode/cli/config.json`: plugins (8 enabled incl github, mimosa, android-emulator, mapbox; example-plugin, cloudbase-skills, lumen disabled), hooks.enabled true, and 7 MCP servers (node_repl, cua_repl, web-search, web-search-sd, web-reader, web-reader-sd, zread, zai-vision). Key/secret values redacted at read time; structure enumerated via json key walk.
  - Skill discovery dirs, all verified on disk with counts: `~/.zcode/skills` 19 entries, `~/.agents/skills` 14 entries, repo `.agents/skills` 18 entries (54 skill surfaces total; the repo 18 matches the f-02 census).
  - Workspace `AGENTS.md` (repo root) is injected verbatim into the seat context at launch. Verification: it is reproduced in full in this session's own system context, including the Clippy census line claiming 2,303 tests / 352 files (2026-09-27 census, within its 7-day tripwire window today).
  - The AGENTS.md load order (docs/FRAMEWORK_LOAD.md, compass, MYCELIAL_SCIENCE_MAP, etc.) is instructed reading, not harness-enforced: those docs are read by the agent choosing to, not by ZCode.exe. `memories/session/next-window-handoff.md` exists on disk (ls).
- Hook taxes that ride EVERY tool call once the session is live (from config.json hooks.events, timings run in-session via subprocess against the venv python, 2 runs each):
  - PreToolUse Write|Edit: `projects/scripts/hooks/prebuild_gate.py` 722/946 ms (timeout 60s) + `tools/md_record_seal.py gate` 550/613 ms (timeout 15s).
  - PostToolUse Write|Edit: `tools/md_record_seal.py seal` 596/1405 ms (timeout 15s).
  - PostToolUse Bash: `mag/trajectory_step.py hook` 752/1043 ms (timeout 15s).
  - So one Write/Edit round trip pays roughly 1.9 to 3.0 s of hook python startup plus work; one Bash pays 0.75 to 1.0 s.

### Stage 1: agent warm boot (`python -m mag.hermes_warm_boot`, AGENTS.md warm-boot law)

Code read in full: `mag/hermes_warm_boot.py` (124 lines). Reads, in order:
1. `memory/biography/verkle_chain.jsonl` last line only (`_chain_tip`, hermes_warm_boot.py:39-59; full file read then last line taken).
2. `vercel-deploy/` recursive walk for .html/.json/.md names (`_deployments`, hermes_warm_boot.py:62-73). No network: the known_urls list is hard-coded; the AGENTS.md 302-SSO caveat applies to manual curl checks, not this stage.
3. `memory/briefs/latest.md` (`_session_brief`, hermes_warm_boot.py:76-81).
4. Writes `memory/warm_state.json` (hermes_warm_boot.py:111).

Measured: 606 / 612 / 822 ms end to end, 3 runs, exit 0 each (`subprocess` timing harness against `.venv/Scripts/python.exe -m mag.hermes_warm_boot`).

### Stage 2: `mag.cmd context-pack` process start

- `mag.cmd` is a shim: venv existence check then `"%PY%" "%ROOT%main.py" %*` (file read in full, 10 lines).
- `main.py` module import does, in order: ROOT on sys.path (main.py:14-16); imports audit, config, handoff.schema, handoff.verify, models.env_load (main.py:18-23); stdout/stderr reconfigure to UTF-8 (main.py:26-31); `load_dotenv()` reads repo `.env`, 129 lines, does-not-override semantics (models/env_load.py:5-27); `install_no_window_defaults()` monkey-patches subprocess for CREATE_NO_WINDOW process-wide (main.py:36-39, mag/headless.py).
- Measured bare `import main`: 197.8 ms (v c 311, one run). The argparse build is in-memory only.

### Stage 3: `build_context_pack(mode="full")` (mag/context_pack.py:571-973), the ordered read list

Exact order of reads as written in the function, each with its source:

1. `mag.lanes.latest_brief_text()` (lanes.py:218-243): `memory/briefs/latest.md`; if it starts `# FROZEN`, serves `state/CURRENT.md` instead (Q1 poison fix, 2026-09-27).
2. `mag.health.sanity()` (health.py:228-263, non-fast path only, context_pack.py:614-617): reads `watch/heartbeat.json` via runtime.read_heartbeat (runtime.py:40-55), `watch/mag.pid`, `watch/active_session.json`, `memory/live_from_grok.md` + `watch/session_digest.jsonl` ages; sockets to 127.0.0.1:8765 and :8000 (0.4s timeout each); HTTP GETs to `:8765/api/board` and `:8000/health` bounded at 1.0 s each (health.py:115-139).
3. `models.multi_smoke.last_smoke()` reads `models` latest smoke json (multi_smoke.py:177-183).
4. `models.registry.inventory()` (registry.py:190-212): parses `configs/lanes.yaml` by hand-stripped YAML (registry.py:42-80), then `ollama_tags()` probes `http://<ollama>/api/tags` on a daemon thread with a hard 1.0 s cap and 2 s success / 5 s failure cache (registry.py:99-141).
5. `memory/live_from_grok.md` clip 800, `memory/attention.md` clip 600, `memory/operator_directives.md` clip 2800, `queue/todo.md` clip 500 (context_pack.py:619-622).
6. Bonds block (631-647): `memory/bonds_active.md` + `memory/bonds_active.json` (bonds.py:17-18), re-ingest if missing.
7. Resonance (651-663): `mag.resonance._collect_sources` (resonance.py:45-125) reads up to 40 files from `memory/remedies/*.md` (31 on disk), `memory/improve/candidates.jsonl` (118 KB), `queue/todo.md`, `memory/decisions_log.jsonl` (76,376,007 bytes, whole file read then tail-40 kept), and `mag.failure_kb` signatures.json (1.0 MB).
8. Run trail (676-682): `mag.run_trail.trail_pack_excerpt` (run_trail.py:931-946) with repair + load_run.
9. Skills (685-691): `configs/skills.yaml` via mag/skills_pack.py:11,14-17.
10. IJL skills (694-707): `ijl_core.skill_excerpt_for_goal`, which reads 22 skill bead files (ijl_core.py:258).
11. Verkle tip badge (712-730): `memory/biography/verkle_tip.json`; then `_residual_census` over `memory/biography/residual/*.json` cached 1 h in `memory/working/residual_census.json` (context_pack.py:528-568; the 2026-09-22 3.7k-file wedge note is in the docstring).
12. Agent state (745-759): `memory/agent_state/LATEST.json` + LATEST.md (agent_state.py:28-33,120-126).
13. Continuity (762-767): `memory/working/OPERATOR_CONTINUITY.md` clip 2200.
14. Nervous system (770-775): `mag.nervous_system.pack_excerpt()` with no glance arg runs `build_glance(write=True)` (nervous_system.py:495-497,301-344), which re-runs `sanity()` a SECOND time (nervous_system.py:315-317), probes port 8765 again, probes Ollama, reads `memory/biography/verkle_tip.json` + `memory/agent_state/tip.json` + smoke again, then `mag.seat_registry.list_registered(live_only=True)` which walks `mag.orchestrator.list_tasks()`.
15. `orchestrator.list_tasks()` (orchestrator.py:1599-1629): globs `memory/runs/orchestrator/tasks/*.json` and reads EVERY file. Verified on disk: 6,032 files, 5,736,845 bytes. The 1.0 s TTL cache (orchestrator.py:77) is process-local and always cold in a fresh CLI boot. This one call made 6,032 of the 6,254 `Path.read_text` calls in the profile.
16. Behavioral + compass (780-797): `memory/improve/daily/*-behavioral.md` newest (governance.py:16,21-31) + compass.FRAMEWORK_BLOCK (compass.py:62, an in-code constant).
17. Tesuji (800-817): `memory/improve/daily/*-tesuji-shells.md` newest (tesuji_shell.py:20,230-241).
18. Coordination (820-842): `memory/state shared_activity.jsonl` (coordination.py:21,116-124), `memory/boot/tripartite_latest.json` (tripartite_boot.py:22,485-492), `queue/handoff/peer-*.json` newest 3 (peer_handoff.py:20,157-165).
19. Decision tips (851-860): `mag.decision_framework.surface_tips` reads `logs/behavioral_events.jsonl` (67,099,819 bytes) and `memory/decisions_log.jsonl` (76,376,007 bytes) via `_read_jsonl`, which does `read_text` of the WHOLE file then keeps only the last 40-60 lines (decision_framework.py:22-23,41-52,83,97). Both 100+ MB files are parsed per boot for a tail slice.
20. Mirror/clue (gated off by default, env MAG_INJECT_MIRROR_VOICE / MAG_INJECT_CLUE_CHAIN, context_pack.py:193-258) and zeitgeist: `docs/archive/ZEITGEIST.md` then `docs/ZEITGEIST.md` fallback (261-274).
21. Build/scope excerpts (871-882): optional `docs/ref/BUILD-<slug>.md`, newest `memory/steward/scope_cards/*.md`.
22. Proven moves: `memory/improve/skill_ledger.jsonl` (1,626,993 bytes, whole-file read, skill_ledger.py:31,94-106). Solved: `memory/improve/pro_library.json` + all 43 `memory/rib/*.md` files re-read (solved_surface.py:47-77). Dirac count: `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` (context_pack.py:19-31, dirac_loop.py:228).
23. Doctrine: every `memory/rib/*.md` again for title+goal lines (context_pack.py:305-340).
24. Quantized laws: `memory/corpus/quantized_thought/instructions_flash.jsonl` + `compile_report.json`, visible 7-day staleness debt pointer (context_pack.py:343-391).

### Stage 4: render and write (main.py:3485-3525)

`format_context_pack_text` renders the ladder (context_pack.py:993-1272; shed stages append rows to `watch/inbox/PACK_OFFLOAD.jsonl`, verified live rows at 2026-09-28T23:13:09Z from a concurrent janitor seat). Then the CLI writes `memory/context_pack_latest.md` + `.json` (main.py:3503-3508) and runs `mag.census_liveness.report()` (main.py:3523-3524). Verified in-session that `format_context_pack_text` does NOT mutate the pack dict (47 keys before, 47 after, direct test).

## Total boot latency (the numbers)

End-to-end `mag.cmd context-pack` equivalent (`.venv/Scripts/python.exe main.py context-pack`, full mode), 3 runs at the moment named above: **8563 / 7547 / 9118 ms, median 8563 ms**, exit 0, 4559 B stdout each.

cProfile attribution of one build+format (7683 ms total, 960,207 function calls, 6,254 Path.read_text calls):

| Stage | cum ms |
|---|---|
| nervous_system.pack_excerpt (build_glance: sanity #2 + port re-probe + seat_registry) | 2336 |
| decision_framework.surface_tips (whole-reads 67 MB + 76 MB jsonl) | 1954 |
| health.sanity call #1 | 1629 (2 calls total) |
| seat_registry.list_registered via orchestrator.list_tasks (6,032 file reads) | 1581 (inside build_glance figure) |
| resonance.top_cards / _collect_sources (76 MB decisions_log + 51 remedy/candidate reads) | 1088 |
| str.splitlines on the big jsonl files | 944 |
| yaml.safe_load, 13 calls | 514 |
| interpreter import of main.py (separate measure) | 198 |

Breakdown verdict: of the 8.5 s boot, roughly 0.2 s is interpreter+import, ~5.9 s is the double sanity + glance probe suite (network probes are bounded 0.4-1.0 s each but stack), and the rest is whole-file reads dominated by three artifacts: 6,032 orchestrator task files (5.7 MB across 6k syscalls), `memory/decisions_log.jsonl` 76.4 MB read twice (resonance + decision_framework), `logs/behavioral_events.jsonl` 67.1 MB read once, all to serve tail slices of under 100 rows.

## What fails silently

Structural census across the 29 boot-path files (counted by regex over `try:` / `except` / swallow-shaped bodies, run in-session): **203 try blocks, 200 except handlers, 112 of them swallow without logging** (pass / continue / return empty). Heaviest: context_pack.py 13, tripartite_boot.py 12, nervous_system.py 9, run_trail.py 8, decision_framework.py 7, agent_state.py 7.

The silent paths that matter, with their hiding spots:
- `context_pack.py:662-663, 690-691, 796-797, 816-817, 825-826, 833-834, 841-842, 859-860`: resonance, skills, behavioral, tesuji, coordination x3, decision tips all degrade to empty string with zero trace. A broken `mag/resonance.py` import would vanish from every pack with no error anywhere.
- `context_pack.py:30`: a dead dirac module is indistinguishable from "0 loops closed".
- `context_pack.py:405, 426, 31`: proven moves and solved surface silently blank out.
- `mag/orchestrator.py:1612-1613`: unreadable task files are skipped one by one, forever.
- `dashboard/rest.py:4053-4055`: the dashboard's own pack write failures are `except: pass`.

Live check (fresh full build in-session): none of those error paths fired. All layers rendered: brief served live `state/CURRENT.md` (`# CURRENT`, 2026-09-27 body), bonds 1600 ch, skills 600 ch, ijl 420 ch, behavioral 957 ch, compass 900 ch, coordination 1466 ch, zeitgeist 799 ch, proven_moves 419 ch, solved 972 ch, doctrine 4235 ch, resonance 3 cards, dirac closed=6/total=8, quantized laws compile v0.3 2026-09-28 (fresh), tip ok with 8,261 verkle leaves, health `degraded` (ports up, integral heartbeat down). Zero "(ijl skills:" / "(agent_state" / "(continuity" / "(mount failed" error markers in the rendered dict.

## Cross-lane findings (verified, not speculation)

1. **A concurrent writer serves stale boot content.** `memory/context_pack_latest.json` is last-writer-wins with at least three live writers: main.py:3503-3508, dashboard/rest.py:4049-4055, mag/autorun_common.py:40-55. At 18:56 EDT the on-disk pack had 44 keys and a `# FROZEN` fossil brief; current code builds 47 keys and the Q1 fix serves live truth. By 19:13 EDT the file carried ts 2026-09-28T23:13:09Z, mode janitor, root_short b14fb972 matching PACK_OFFLOAD rows from a concurrent seat. Conclusion supported by the bytes: a long-lived seat (dashboard :8765 has been UP throughout) is running pre-2026-09-27 in-memory code and re-poisoning the shared pack file with the fossil brief the Q1 fix removed. Every consumer that "reads the latest pack file" instead of rebuilding gets that seat's stale world. Which process it is cannot be proven from disk alone; stated as not attributed.
2. **Container path leak in bonds.** `memory/bonds_active.md` (ingested 2026-09-26 by session mag-agent-orc-t4b36c9dec1) records its path as `/app/memory/bonds_active.md`, a Linux container path; the Windows-host pack prints a pointer that does not exist on this filesystem. Verified in the rendered pack json (bonds_meta.path) and the file header.
3. **Sanity runs twice per boot** (context_pack.py:617 + nervous_system.py:317 inside build_glance), doubling the probe suite cost for zero new information.
4. **mag.cmd adds one more interpreter-free hop** (cmd.exe shim) that my timings did not include; the 8.5 s figures are python-entry to render-end.

## Not run / limits

- ZCode.exe internal startup latency: no instrument exists from inside a session; not measured, not estimated.
- `pytest --collect-only` was not part of this item and was not run.
- The 44-key stale pack's owning process was not identified beyond "a concurrent seat, likely the long-lived dashboard or an autorun drainer".
- Hook timings used direct subprocess invocation of the hook scripts, not a live ZCode Write/Edit event; interpreter startup dominates in both paths but the live-path figure could differ slightly.
