# SELF-STEAL C — seat-side inventory (Sancho cage, 2026-09-01 04:1xZ)

Lane C of the deep self-steal salon (operator directive 04:03Z: "deep self steal, this is barely scratching the surface, get help in a salon").
Scope: OpenClaw seat itself — organs, standing jobs, memory heat, defects. Evidence = bytes checked this turn.

## Standing jobs (cron, agent main)

| Job | Schedule | Last status | Class |
|---|---|---|---|
| archivist_feed_harvest | every 8h | error — delivery: "Channel is required (no configured channels detected)" | EXERCISED-24h + **DELIVERY DEFECT** (file work lands: INBOX_LINKS 04:08, receipts 04:08; announce step broken) |
| procurement_hunter | every 12h | error — same delivery defect | EXERCISED-24h + **DELIVERY DEFECT** (DEALS_LEDGER 02:41) |
| garden-window-watchdog | every 1h | ok | EXERCISED-24h |
| intel-sweep | cron | ok (last 08-31 19:25Z) | EXERCISED-30d |
| rnd_advisor_steering | cron | never run (first fire pending) | ARMED-DORMANT |

## Memory + recall

| Organ | Evidence | Class |
|---|---|---|
| Daily notes 2026-09-01* | 8 files, 84,769 bytes total, last 03:34Z | EXERCISED-24h (high heat) |
| MEMORY.md long-term | loaded live, ~18KB, dense standing doctrine | EXERCISED-live |
| **memory_search** | DISABLED — index built for `fts-only`, provider expects `text-embedding-3-small`; tool refuses | **DEFECT — recall organ down**; fix: `openclaw memory status --index` / `memory index --force` |
| MEMORY_RIB (concepts/catalog/WARM_PACK) | WARM_PACK deref'd this turn (14 spine entries, 0 defects); catalog last touched 08-31 10:05 | EXERCISED-24h |

## Spawn / delegation surface

| Organ | Evidence | Class |
|---|---|---|
| sessions_spawn | requireAgentId=true, allowAny=false — only `worker` (DS-Flash) allowed; first two spawn attempts forbidden without agentId | EXERCISED-24h, contract learned |
| worker lane | 2 subagents spawned this turn (lane_a_organs, lane_b_board) via agentId=worker | EXERCISED-live |
| AGENTS_ROSTER_PATCH_20260901.json | staged 03:56Z — 11 new seats, merge instructions for openclaw.json, awaiting operator paste + restart | **DORMANT — seat expansion pending one human step** |

## Cage skills (workspace/skills)

archivist, chan, fireball-cycle, front-door, operator-corrections, quixote-planner, ractor-cast — 7 loaded, front-door + archivist + chan consulted this turn. EXERCISED.

## Staged-but-unapplied cage organs (staging/ + patches law)

switchboard.py, switchboard_v2.py, effect_broker.py, policy_engine.py, session_bridge.py, riddler_sanitize.py, swarm_cycle.py (+v2), ask_router.py (+v2), harness.py — all awaiting host apply via `python -m mag.openclaw_patches apply`. Class: **STAGED-DORMANT** (host step pending).

## Board participation

| Organ | Evidence | Class |
|---|---|---|
| riddler_common.jsonl bus | 80,462 bytes, touched 04:00Z | EXERCISED-24h |
| room.jsonl | 1.2MB, touched 04:05Z — claw posts are bootstrap events; no substantive claw prose since salon work began | EXERCISED-24h (thin claw voice) |
| POST /room write path | verified 08-31 probe (mag_api.mjs, 9 GET + 4 POST routes) | EXERCISED-30d |
| workboard | first card this turn (deep self-steal salon) | EXERCISED-live |
| summarized_sessions.json | 47,646 bytes, 04:08Z | EXERCISED-24h |

## Inbox hygiene

INDEX.json derived from index_events.jsonl: 40 events / 37 active items. **Fold warnings: writer "sancho" nonce gaps (seq 35: expected 4 got 1; seq 36: expected 2 got 4)** — pre-existing defect, flagged by derivation itself.

## Counts

Standing jobs: 4 exercised, 1 armed-dormant, 2 carrying a delivery defect. Memory: recall down (1 defect), everything else exercised. Spawn: 1 live lane, 1 staged roster (+11 seats) dormant. Staged organs: 9 modules + variants awaiting host apply. Board: 5 surfaces exercised, 1 nonce-hygiene defect.

## Top promotable moves (seat side)

1. Fix memory index provider → recall organ back online (one command, operator or gateway-side).
2. Patch archivist_feed_harvest + procurement_hunter delivery (mode none or explicit channel) → two standing systems stop erroring every cycle.
3. Operator pastes AGENTS_ROSTER_PATCH + restart → 11 dormant seats wake (biggest single dormancy unlock on seat side).
4. Host `openclaw_patches apply` → 9 staged cage organs become live (switchboard boundary, ask_router outcome-routing, session_bridge cross-session).
5. Sancho nonce discipline on index_events.jsonl → fold warnings stop.
