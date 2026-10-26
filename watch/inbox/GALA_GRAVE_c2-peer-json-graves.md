# GALA GRAVE RECEIPT: c2-peer-json-graves (group grave, 12 peer handoffs)

- **Lane:** c2-peer-json-graves, division C (GRAVEDIGGER), THE GALA battery 2026-09-25 (refire of a run that banked nothing)
- **Scope:** every `queue/handoff/peer-*.json` (12 files found; the brief said ~11)
- **Action:** BURIED AS A GROUP. **No file was deleted, moved, or edited.** Deletions are operator-gated and none were requested or performed.
- **Status at burial:** all 12 `schema peer_handoff.v1`, all `status: "filed"`, none closed, ages 24 to 51 days.
- **Evidence log:** `watch/inbox/gala_20260925/w3/lanes/c2-peer-json-graves.check.txt`
- **Machine rows:** `watch/inbox/gala_20260925/w3/lanes/c2-peer-json-graves.json`

## THE LAW FOR FUTURE PEERS

These handoffs are **dead letters, not open work.** Do not pick one up from `queue/handoff/peer-*.json` and execute it as written. Any revival requires a fresh re-brief against current doctrine (AGENTS.md load order, current `queue/todo.md`, configs truth) and operator sign-off where the classification below says so.

## GRAVE TABLE

| # | Handoff | Filed | From -> To | Goal one-liner | Classification | Evidence |
|---|---------|-------|-----------|----------------|----------------|----------|
| 1 | a5c69a4520 | 2026-08-05 | cursor-cloud -> home-pc | Run dashboard v3 preview on home PC (PR Mag#18) | DONE-ELSEWHERE | `dashboard/static/shell.js` + `index.html` on disk; dashboard v3 is the standing product UI (`mag.cmd dashboard` / `mag.cmd lab`) |
| 2 | 56b8cc3c06 | 2026-08-06 | codex -> grokbuild | Finish + verify Feature Lab slice, stop before merge | DONE-ELSEWHERE | `mag/feature_lab.py` exists, wired into `dashboard/rest.py` (4 refs); `queue/todo.md` line 118 Feature Lab evidence task checked [x] |
| 3 | 735bae9a90 | 2026-08-06 | codex -> grokbuild | Load CROSS_AGENT_VERKLE_HANDOFF contract before continuing 56b8cc3c06 | DONE-ELSEWHERE | chained to row 2 which landed; `docs/CROSS_AGENT_VERKLE_HANDOFF.md` still on disk for custody history |
| 4 | 046de3834b | 2026-08-06 | codex -> grokbuild | Execute the audited Project Verkle Salon assignment | SUPERSEDED-BY | Arena V2 Constellation salon: `watch/inbox/ARENA_V2_CONSTELLATION_SALON_20260913.md` (7 chairs, 7/7 landed); live worktree `C:/Users/foste/Documents/projects/worktrees/salon-arena-mvp` on `codex/salon-arena-mvp` |
| 5 | 9cdc923dc6 | 2026-08-06 | codex -> grokbuild | Provider-neutral shared_scratch experiment on Mag rails | SUPERSEDED-BY | `mag/swarm_tools.py` stateless scratchpad toolbelt (FLEET_IMPRINT_20260917.md line 825); `memory/shared_scratch/` never created; 0 September receipt hits for shared_scratch |
| 6 | a6a4e4e9b0 | 2026-08-06 | codex -> grokbuild | Riddler semantic-surrogate mode inside shared_scratch | SUPERSEDED-BY | container abandoned (row 5); riddler line alive as `mag/riddler.py` + "riddler shape" doctrine in `watch/inbox/BUILD_ORDER_LIVING_MUD_20260922.md` line 89 |
| 7 | 605e1df369 | 2026-08-08 | copilot-assistant -> deepseek | Sancho Layer spike pointer (interactive router pane) | SUPERSEDED-BY | deliverables never built (`mag/sancho_router.py`, `vscode-mag-map/sancho.js` missing); Sancho survives as fleet seat name (`docs/ref/SPORE_SANCHO.md`, BASECAMP_PROMPT_20260913.md); dispatch UX lives in `main.py autorun` drainer + deliberate-ask law |
| 8 | 9646d6beec | 2026-08-08 | copilot-assistant -> deepseek | Sancho Layer spike full spec (sancho_router + REST + webview) | SUPERSEDED-BY | same as row 7 |
| 9 | a3c9880f05 | 2026-08-08 | copilot-assistant -> deepseek | Session State History Protocol + Shared World State spike | SUPERSEDED-BY | `mag/session_state_protocol.py` + `configs/world.yaml` never built; roleplay/world line carried by `campaigns/sunless_citadel` + living-mud build order (`watch/inbox/CASTLE_TRACK_20260911.md`) |
| 10 | 7bce5aea37 | 2026-08-08 | copilot-assistant -> deepseek | Codify Mag as RenderMan-style shader system (system.yaml RIB, shader_lib, render_audit) | SUPERSEDED-BY | none of `configs/system.yaml`, `mag/shader_lib.py`, `tools/render_audit.py` built; codify goal carried by the Verkle RIB line (`queue/handoff/VERKLE_RIB.json`, 2.2 MB Sep 2; frozen-RIB deliberate-ask law in AGENTS.md) |
| 11 | a46efc8273 | 2026-08-08 | copilot-assistant -> deepseek | Dashboard-into-VS-Code spike (magMap.direct enqueue + Control Room agents/runs) | DONE-ELSEWHERE (partial) | landed half: `vscode-mag-map/control_room.js` shows drainer/orchestrator/ghost live feeds (lines 1, 48-53, 135-159); `vscode-mag-map/direct.js` never built; browser dashboard never removed so the removal gate is moot |
| 12 | 9ce633bb4a | 2026-09-01 | codex -> mag | Repair Z.AI GLM-5.3-Flash high reasoning path + recover stale supervisor | STILL-RELEVANT (re-brief first) | verified 2026-09-25: `models/providers.py` still applies `_thinking_off` on both paths (lines 360, 631), `reasoning_effort` has 0 hits in models/ + configs/providers.yaml, z_ai2/z_ai3 still lack `default_model`. Caveat: current lane law is thinking-off cache-mining (providers.yaml line 447) with nous glm-5.3-prime as reasoning tier (todo Stone 4), so executing as written needs an operator call |

## COUNTS

- DONE-ELSEWHERE: 4 (rows 1, 2, 3, 11)
- SUPERSEDED-BY: 7 (rows 4, 5, 6, 7, 8, 9, 10)
- STILL-RELEVANT: 1 (row 12)

## NOTES

- `memory/runs/feature_lab_smoke.json` (the evidence artifact row 2 promised) was not found on disk; the todo item is checked anyway. Recorded as-is; not chased by this lane.
- `watch/session_end_hook.py` contains no "verkle" string today although handoff a3c9880f05 claimed wrap-to-verkle existed there; `mag/verkle_knot.py` does exist. Recorded as-is.
- Bytes over reports: every classification above is backed by a command in the check log. Nothing here is from memory alone.
