# ORGAN TABLE V1 - the routing keystone (2026-09-25)

Seat: organ-table, MICKEY-17 OWED wave. Source row: `project-organ-table-router-20260911` as carried in `memory/runs/mickey17/digest_mem_11.jsonl` (status OWED), ranked **1 of 512 OWED** by `memory/runs/gapwave/gap_research_to_code.md:44` (V 5 x R 5 = 25). Machine-readable table: `watch/inbox/organ_table.json` (schema `organ_table.v1`).

The row's own gate text: *"seams already exist - missing only the table file, classify step, drive-state telemetry."* This filing lands **the table**. The classify step and route-event writer stay owed; their exact hook point is named below with line evidence.

## 1. Why this is the keystone

Eight other OWED rows route through it (`memory/runs/gapwave/gap_research_to_code.md:95-96`):

| # | downstream row | seam on disk today | what the table gives it |
|---|---|---|---|
| 1 | budget warn/hard-stop caps | `models/quota.py:242` `provider_budget`, `:75` `record_usage` | per-class budget attach point: caps bind at classify time, not per provider |
| 2 | escalation ladder | `configs/lanes.yaml:71-74` (`max_escalations_per_day: 2`, `require_priority: true`), read by `mag/router.py:184` | class-to-tier-ceiling map (see section 2) |
| 3 | K-of-N verification | `mag/fanout.py:37` width lanes; no quorum code exists (gap row 12, confirmed this session) | N and quorum policy per class as data |
| 4 | organ_eval demotion | absent (gap row 16); inputs exist: `mag/organ_map.py` gap_codes + `scripts/organ_vitals.py` breaches | the registry organ_eval iterates; O03 circuit breaker: demoted organ drops to last resort 10 min |
| 5 | tide-gate throughput (50-wide measured caps) | `mag/fanout.py:37` `DEFAULT_WIDTH = 4` pace guard | per-class width/tide caps as table rows, not code constants |
| 6 | 1000-free-agent swarm rightsizing | `mag/swarm_worker.py:529` `run_rightsized_once` + `mag/cheap_swarm.py:160` daily cap | rightsizing becomes routing: BULK tier-ceiling 0 caps the swarm to free lanes by law |
| 7 | Token Render Manager R4 | `mag/verkle_knot.py` `prove_latest` (VERIFIED, receipt_stale); gap row 19 verkle byte-stable prefix | render becomes a routed class; `shared_head` convention already in fanout packs |
| 8 | mega-salon build order | `mag/lane_salon.py`, `mag/frontier_salon.py`, `memory/research_polished/ENHANCEMENT_STACK_20260920.md` | salon chairs as class-routed organ calls; no bespoke runner |

## 2. The six request classes

From the source row's steal: *"Request classes with default organ + escalation (JUDGMENT/ADVISORY/RESEARCH/BULK/SENSES/VOICE)."* Verified absent from all code this session (grep, section 6). Tier ceilings from `mag/ask_router.py` `LANE_TIERS` (0 free, 1 deepseek, 2 zai, 3 frontier).

| class | primary | fallback | last resort | tier ceiling |
|---|---|---|---|---|
| JUDGMENT | grok_tui seat (`mag/grok_terminal.py`); `mag/router.py` routes overview/plan to grok_tui, why `planning=pack_only` | research-agent state (`mag/agent_state_router.py:29`): deepseek-v4-pro, thinking high, effort high | local `llm.py` ollama chat | 3, priority-gated |
| ADVISORY | deepseek seat via `mag/dispatch.py` `_classify_job` to `mag.router.route`; shape auto via `mag/model_pick.py:34` | local balanced | refusal boundary (delegation profile, `mag/router.py:70`) | 2 |
| RESEARCH | research-agent + `mag/research_worker.py` (bounded) | `mag/cheap_swarm.py` dispatch on flash | local | 2 |
| BULK | `mag/fanout.py`: glm-5.3-flash, max_tokens 12288, width 4, `ZAI_API_KEY_Lite`, HOST_ALLOW {api.z.ai, api.deepseek.com} | `mag/cheap_swarm.py` (flash/local, daily cap) | local | 0, free tier is sacred |
| SENSES | `tools/sense_tools.py:19` `gps_key` MCP cache coordinate; 8B/VL never gets the stream, only tool results | `mag/browser_env.py` via host_resolver | report DARK via organ_vitals | 0 |
| VOICE | Mag Voice seat (`launch_voice.cmd`), capture-first | `mag/game_dm_voice.py` narrator | `mag/operator_inbox.py:50` typed channel (`_VETO_PAUSE` at :44, negation guard: "don't stop" is not a veto) | 1 |

Fallback triggers (O03 design): health_fail, 429, latency_p95, refusal. Escalation law: two-strike = escalate, bounded by `configs/lanes.yaml:72` `max_escalations_per_day: 2`.

## 3. The organ registry (32 rows, full detail in organ_table.json)

Every row verified on disk this session. Call convention as executed or as written in the module's own docstring. Full JSON carries module, callable, line, owner, drive_state, request_classes, routes per organ.

**Routing lane:** `mag/router.py:471` `route()` (schema route.v2) - the one classifier all entry points should call; `mag/dispatch.py`; `mag/model_pick.py:34`; `mag/agent_state_router.py:80,89` (`resolve`/`pick`, schema agent_state_router.v1); `mag/ask_router.py` (outcome ledger, LANE_TIERS, $0 control plane); `mag/switchboard.py:617` `route_intent`; `mag/lanes.py` + `configs/lanes.yaml`.

**Execution organs:** `mag/fanout.py:56` `fire` (STDIN pack / STDOUT `===FANOUTJSON===` / STDERR progress, zero file I/O in cage); `mag/cheap_swarm.py:116,127,160` (`scan`/`dispatch`/`run_cadence`, schema cheap_swarm.v1); `models/registry.py:155` `model_for`; `models/quota.py:242` `provider_budget`; `llm.py` (langchain-ollama with raw-HTTP fallback, traced to usage.jsonl).

**Memory lane:** `mag/context_admission.py:28` `assess` (LIVE); `mag/context_pack.py:486` `build_context_pack`; `mag/rel_mem_eval.py:131` `default_retrieve` (still the lexical stand-in per its own docstring); `mag/swarm_tools.py` `blackboard_post`.

**Governance lane:** `mag/operator_inbox.py:50`; `mag/work_tiers.py:70` `next_for` (five tier state machines; `usefulness-oracle` named as an actor at :42 - the oracle itself is still absent); `mag/policy_engine.py` `validate_authority`; `mag/self_audit.py`; `mag/elder.py`.

**Research lane:** `mag/research_worker.py`; `mag/swarm_worker.py:529`; `mag/swarm_cycle.py`.

**Senses lane:** `tools/sense_tools.py:19`; `mag/browser_env.py`; `mag/host_resolver.py` (spec `configs/organs/host_resolver.yaml`, the estate's only prior organ config, schema organ.v1).

**Telemetry:** `mag/organ_map.py` (`status`/`snapshot`, schema organ_map.v1, status law DECLARED -> INSTRUMENTED -> WIRED -> STATEFUL -> VERIFIED -> LIVE / GHOST); `scripts/organ_vitals.py` (freshness spine, breach sigs `vitals:<organ>` to `logs/failure_kb_alerts.jsonl`); `tools/estate_atlas.py` (disk custody from the ESTATE_INDEX spine); `tools/capability_manifest.py` (output `memory/capability_manifest.md` ABSENT on disk, checked).

**Other lanes:** `mag/verkle_knot.py` `prove_latest`; `mag/grok_terminal.py` (frontier ghost, RenderMan: compact at the frontier, expand at the cheap); `watch/organs/tale_re_encoder.py` (landed 09-03).

## 4. Drive-state telemetry (executed fresh during this ask)

**`python -m mag.organ_map status`** (2026-09-26T00:56:40Z): 33 organs, summary DECLARED 33 / INSTRUMENTED 31 / WIRED 32 / STATEFUL 31 / VERIFIED 31 / **LIVE 2** (context_admission, operator_mode) / **GHOST 0**. Gap codes: 15 receipt_stale, 3 receipt_not_successful (swarm_worker, switchboard_v2, policy_engine, research_worker), water_computer proof_failed, fleet_structure STATEFUL (caller_undeclared, receipt_missing, proof_failed), host_resolver receipt_missing.

**`python scripts/organ_vitals.py`** (tick 2026-09-26T00:57:03Z): 10 watched organs, **9 breaches**: cite_gate DARK (missing `memory/runs/cite_gate_latest.json`); convo_wire, overseer, refeed_guard, m12_baseline, operator_pulse, dead_hand_state, trailer_telemetry, hermes_receipts STALE.

**The structural find:** the routing keystone itself is unwatched. `mag/router.py`, `mag/dispatch.py`, `mag/fanout.py`, `mag/cheap_swarm.py`, `mag/work_tiers.py`, `mag/operator_inbox.py`, `mag/agent_state_router.py` appear in **neither** telemetry registry. The liveness spines watch 43 surfaces and miss every organ a routing decision depends on. Until the classify step lands, a dead router would be discovered by symptom, not by vitals.

## 5. The classify step (hook point named, NOT built)

- Hook: `mag/router.py:471` `route()`, after `_detect_markers` + `classify_depth` resolve. Stamp `route_class` from the six classes, emit one `route_event` row `{class, chosen, reason, latency_ms, tokens, ts}` to `state/organ_table_events.jsonl` (hash-chain ready, per O03's route_event leaf).
- Evidence the classes don't exist yet: `grep -rn "JUDGMENT\|ADVISORY" --include=*.py mag/ configs/ tools/ scripts/` returns only unrelated hits (`mag/arena_bench.py:29`, `mag/embassy_deliver.py:107`, `mag/verb.py:439`, `mag/_salon_burn.py:40`).
- Driver convention: `mag/ask_router.py` already composes organs by subprocess and never imports them; the classify step should stay equally thin.

## 6. Verification log (all commands run this session)

| check | command | output |
|---|---|---|
| configs/organs holds only the resolver | `ls configs/organs` | `host_resolver.yaml` |
| no table existed before this filing | `find . -maxdepth 3 -iname "*organ*"` | organ_map.py, bay_organs.py, host_resolver.yaml, tale_re_encoder.py, kimodo; no table, no route-event log |
| request classes absent from code | `grep -rn "JUDGMENT\|ADVISORY" --include=*.py mag/ configs/ tools/ scripts/` | 4 hits, all unrelated (see section 5) |
| organ status law live | `.venv/Scripts/python.exe -m mag.organ_map status` | 33 organs, LIVE 2, GHOST 0 (section 4) |
| freshness spine live | `.venv/Scripts/python.exe scripts/organ_vitals.py` | 10 organs, 9 breaches (section 4) |
| manifest output absent | `ls memory/capability_manifest.md` | No such file or directory |
| escalation budget | `grep -A3 grok_budget configs/lanes.yaml` | max_escalations_per_day: 2, require_priority: true |
| this JSON parses | `.venv/Scripts/python.exe -c "import json; json.load(open('watch/inbox/organ_table.json'))"` | schema organ_table.v1, 32 organs, 6 classes, 8 downstream rows, 7 checks, no em-dash |

Not run (named honestly): no pytest suite exists for organ routing (the table is data, not code); the O03 `organ_health.py` probe runner and `organ_table.html` dashboard are not built and were not attempted; `mag/organ_map.py` `snapshot` was not re-written (its `latest.json` stays the 09-02 snapshot; my fresh run was `status` only).

## 7. Next seat

1. Promote: copy `watch/inbox/organ_table.json` to `configs/organs/organ_table.json` where a boot-time dispatcher reads it.
2. Wire the classify step at `mag/router.py:471` per section 5.
3. Add the seven unwatched routing organs to `scripts/organ_vitals.py` ORGANS (a router with no freshness watch is the gap section 4 names).
4. Then fire the 8 downstream rows in order: escalation ladder and budget caps first (seams already live), K-of-N second (fanout already returns per-lane texts), organ_eval last (needs the usefulness oracle, gap rank 2).

*Filed 2026-09-25 by the organ-table seat. Falsifier for this filing: if the next dispatch decision cannot name its request class from this table without reading code, the table failed.*
