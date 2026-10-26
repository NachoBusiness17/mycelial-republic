# LM1 — session_maze self-steal run (2026-09-30)

Operator: "self steal and run em" — audit flagged session_maze stale 4 days (evidence
`memory/graph/session_maze.json` mtime 2026-09-26 09:38 vs `stale_s: 86400` in
`mag/self_steal.py` CAPABILITIES). Owner: `mag/session_maze.py`. No code changes were
required; nothing blocked the run. Venv: `.venv/Scripts/python.exe`.

## What it does (learned from the source)

- `assemble()` — deterministic, no LLM: reads `state/CURRENT.md` (raw, 4000 cap) plus 3 pointers (`campaigns/quiet_forge/module.json`, latest `memory/research_packs/*.md`, `mag.skill_ledger.progress` decisions) plus `mag.process_supervisor.status`. Renders `session_maze.v1` dict.
- `persist()` — writes `memory/graph/session_maze.json` + renders `state/HANDOFF.md` (the "map is the territory" handoff a deeper model reads instead of a re-pasted thread).
- `deep_handoff()` / `escalate_cached()` — the dispatch half: spawn/chat on a deeper provider riding a byte-stable maze prefix (cache-hit doctrine).

## Cycle run (2026-09-30, all outputs byte-observed)

1. `python mag/session_maze.py` (assemble): clean. CURRENT.md present + fresh (updated 2026-09-30T11:56Z, goal "sovereign game platform last-mile"); research pack `THE50_W3_T15_AGM_REVISION.md`; ledger decisions 6492; supervisor loop statuses live (autorun crashed 14:03Z, ghost/ghost-daemon off).
2. `python mag/session_maze.py persist`: ok. `memory/graph/session_maze.json` (2,294 B) + `state/HANDOFF.md` (923 B) written 17:37Z.
3. `deep` guard: no-goal returns `{"ok": false, "error": "goal required"}` — correct. Not run with a real goal (default provider deepseek is unfunded per DRIVING LADDER 2026-09-28).
4. `escalate_cached` on the funded lane (provider `nous`): `z-ai/glm-5.3-prime` AND `qwen/qwen3.8-max-prime` both HTTP 402 "Insufficient available credits" (both keys in the failover chain; tiny 64-token reservation also 402). Lane is credit-dry today. The CODE degraded correctly: structured `ok: false` + surfaced error, no crash, no fallback creep.
5. `python -m mag.self_steal --cadence`: leaf `memory/runs/self_steal/self_steal_2026-09-30.md` + state.json refreshed (was frozen 2026-09-22). **session_maze is no longer in the stale findings** (10 findings remain; session_maze absent because persist() refreshed its evidence mtime — the point of the exercise). No launches enqueued (idempotent).

## Findings (no fixes made — nothing blocked)

- `main()` `deep|handoff` branch (mag/session_maze.py:273-276) is missing `return 0`: it prints the handoff JSON, then falls through to the final `print(assemble())` — stdout carries two concatenated JSON docs. Breaks any single-JSON parser of that subcommand. Not blocking the assemble/persist cycle; fix on next edit of the file.
- `DEFAULT_DEEP_PROVIDER = "deepseek"` is off the DRIVING LADDER (only Hermes/Nous funded). The dispatch half is dead-until-funded AND pointed at an unfunded default. Repoint to `nous`/`z-ai/glm-5.3-prime` when credits are topped.
- Nothing broke on stale schemas: the module reads CURRENT.md raw and degrades gracefully on every optional source. Zero schema drift since 2026-08-16.

## Honest verdict — worth the run? REWIRE, not retire.

- Deterministic half (assemble/persist): alive, cheap ($0), and genuinely load-bearing — `mag/self_drive.py` imports `persist()`, `mag/fuel_feed.py` imports `escalate_cached()`, `mag/elevate.py` imports `assemble()`, `mag/work_tiers.py` cites it in the tier ladder. Retire would break three importers.
- But the content is thin: the "maze" is CURRENT.md verbatim + 3 pointers (923 B rendered). Despite the name it mines NO session data — no history, no bonds, no conversation tail. As a drop-in-for-a-deeper-model test it has not been exercised since landing (fuel_feed's escalation consumer hit a 402-dry lane today).
- Dispatch half (deep_handoff/escalate_cached): correct code, dead lane (402 both Nous models 2026-09-30; deepseek default unfunded).
- Rewire recommendations, in order: (1) wire `session_maze.persist()` into a daily cadence (same shape as the census/fts patrols) so the self_steal freshness flag stays green without a human remembering; (2) repoint deep defaults at the funded lane; (3) add the missing `return 0`; (4) if a real deep handoff is ever re-tested, fatten the maze (bonds + last result) before judging the doctrine.

Verdict: run was worth it — surface refreshed, lane health measured (402 = operator-visible fact), three concrete rewires filed. The organ is not dead weight; it is under-fed and pointed at a dry well.
