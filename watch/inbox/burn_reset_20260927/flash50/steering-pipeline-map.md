# steering-pipeline-map (s2-15, 2026-09-28)

Full map of the Mag steering pipeline: operator input -> steering intake -> lane
dispatch -> execution -> banking. Every code claim cites file:line read this ask;
every number comes from a command run this ask (census script `_s2_15_census.py`
run via `.venv/Scripts/python.exe`, plus the targeted probes listed in the
receipt `s2-15.md`). No number is copied from any prior report.

## 0. Vocabulary warning (read first)

"Steering" names FOUR disjoint mechanisms in this repo that do not talk to each
other. Any audit that merges them produces fiction:

1. **operator_inbox breadcrumbs** (mag/steer_bridge.py, mag/operator_inbox.py):
   deferred guidance drained at agent checkpoints.
2. **WINDOW_STEER bus** (mag/steer.py + mag/bus_cadence.py): `[STEER]` marker
   packets in `memory/runs/steer/` folded into the relation by a cadence.
3. **steer_bus estate directives** (mag/steer_bus.py): gated `STEER-<id>` grammar
   posts, governor-only execution, receipts to `watch/steer_bus_receipts.jsonl`.
4. **live-seat steer** (mag/agent_cli.py `!steer`/`!pause`, mag/pigeonhole.py
   mailbox for headless workers, mag/hermes_steering.py `steer --resume`):
   mid-run redirection of a running process.

Adjacent but NOT operator steering: `steer_telemetry` (measures whether a steer
changed the outcome), `steer_engine` (compiles steering sources into injection
blocks), `telegram_desk` (public Q&A, not fleet control), `phone_door` (door
health only), `seat_steer` (agent->external seat messages, the reverse direction).

## 1. Stage A: operator input surfaces

| Surface | Entry code | What it carries |
|---|---|---|
| Terminal REPL | mag/agent_cli.py:1969-1990 (`_STEER_QUEUE`, stdin listener gated mid-turn) | `!steer` / `!pause` / `!continue` / `!escape` |
| Dashboard REST | dashboard/rest.py:5312-5314 (`/api/v1/agents/{id}/cmd`, `/api/v1/agents/{id}/steer`), :5341-5342 (`/api/v1/operator-inbox`), :5410 (`/api/v1/seat/steer`), :4530 `h_agent_steer_post` | mid-run cmds, queued guidance, overseer steers |
| Broadcast | mag/governance.py:87-131 `broadcast_steer` | one cmd fanned to chat queue + desk + every non-terminal orchestrator task |
| Terminal CLI | main.py:852-860 `steer-agent`, :1120-1126 `steer` | one-shot guidance; WINDOW_STEER packet emit |
| Drop file | queue/steer_agent.md -> mag/steer_bridge.py:83-113 `sync_guidance_file` | idempotent by sha256 against `memory/working/steer_bridge_seen.json` |
| Phone (health) | mag/phone_door.py:40-50, tailscale ping `moto-g-5g---2024` | fire-rate log only, no steering content |
| Phone (decisions) | mag/phone_relay.py:162-215 `ask()` via Discord DM | approve/deny ONLY (token set phone_relay.py:37-38), not free text |
| Telegram | mag/telegram_desk.py:131-162 `run()` | public Q&A on the deepseek lane; never touches fleet state |
| Supervisor auto-steer | mag/orchestrator.py:576-584 | stall nudge `!steer` re-anchor before killing a silent child |

Live-state evidence (this ask): phone_relay_log.jsonl = 138 rows, asks per day
{09-24: 1, 09-26: 76, 09-27: 7, 09-28: 41}; phone_door_log.jsonl = 2 rows;
`memory/runs/telegram_trail.jsonl` MISSING (the Telegram surface has never run
or its trail is gone); queue/steer_agent.md holds 2 active lines, BOTH unsynced
(seen state frozen at 2026-08-07T19:18:16Z, 6 hashes).

## 2. Stage B: steering intake

- **operator_inbox** (memory/operator_inbox.json; commit mag/operator_inbox.py:128-152):
  dedup by exact text; veto/pause classifier (:66-82, negation-guarded); vague
  inputs become Socratic questions at drain (:250-262 `_is_ambiguous`,
  :286-334 `drain_pending_at_checkpoint`). The single drain consumer is
  mag/agent_cli.py:2390-2416 `_absorb_operator_inbox` (dashboard desk path:
  mag/desk_dialogue.py:255). Store census: 50 committed (AT the -50 cap),
  4 pending, 100 processed (AT the -100 cap). All 4 pending are machine-sourced
  and dated today: 3x ghost (one is literally `[ghost] Test steer for
  deployment.`) + 1x press_digest. Zero human-sourced items in the live backlog.
- **WINDOW_STEER bus** (mag/steer.py:45-57 emit -> memory/runs/steer/<id>.json +
  trail.jsonl): consume() scans session transcripts and control trail for
  `[STEER]` markers (:64-107) and compiles memlang tokens; bus_cadence.cadence()
  (mag/bus_cadence.py:112-146) folds unconsumed packets into RIB + party
  subchain, routes to seats, marks consumed in a `finally` (a route failure can
  never block the fold). Fired from mag/governor_autorun.py:1990-2005 every
  MAG_STEER_EVERY=120 ticks. Census: 12 packets, 1 unconsumed (press-JEV-1,
  emitted 2026-09-28T22:45:14Z by press_digest), trail 2,508 lines.
- **steer_bus gated directives** (mag/steer_bus.py:52-75 `authorize`): closed
  enum {nudge, clamp, purge, route}, ttl cap 60s, anchor sha required, receipt
  row written on every attempt. Census: 2 receipt rows lifetime, 1 still
  `applied: false` reason `authorized-request-awaiting-governor`. The only
  production caller is the swarm gate (mag/swarm_tools.py:316-328); NO code path
  was found that consumes the nonce and applies the directive (the "governor"
  executor of mag/steer_bus.py:3 does not exist as code). The wire side
  (mag/steer_receipt_wire.py) only re-emits receipts into the hash-chained
  event stream; census: wire offset 872 == receipts 872 bytes, fully drained.
- **interrupt_pipeline** (mag/interrupt_pipeline.py:107-152): pin current ->
  value the new instruction (novelty = knowledge_graph coverage OR steal-corpus
  filename overlap >= 0.4 = cache_hit, :76-103) -> steer_router.steer -> assemble
  batch via session_rib. Census: interrupt stack 0, batches.jsonl 1 row lifetime.
- **steer_engine** (mag/steer_engine.py:54-129): compiles frontier invariants +
  operator_directives.md + rib_bus RIBs + grok_bot directives into one injection
  block. Census: telemetry.jsonl 3 rows lifetime; `memory/steer_telemetry.jsonl`
  0 rows (the probe-pass store, read by mag/lens_knot.py:103 and
  mag/governor_autorun.py:847, is empty).

## 3. Stage C: lane dispatch

- **rightsize classifier** (mag/steer_router.py:72-95): keyword scores map a
  steer to `now` / `enqueue` / `pin`; zero keyword hits default to `pin`
  (:80-84). `enqueue` -> mag/orchestrator.py:932-1000 `enqueue` (duplicate-goal
  refusal :946-961, factory gate :938-943). `pin` -> pin stack
  memory/runs/steer_router/pins.json; resume is a manual CLI action
  (steer_router.py:109-119) plus one automated consumer (mag/afk_cadence.py:194).
  Census: pin stack 0. Every decision appends to the behavioral corpus
  (steer_router.py:161-170): census shows 1 row lifetime, mode=enqueue.
- **lane ladder** (mag/lanes.py:168-175 `goal_lane`, configs/lanes.yaml):
  L0 local / L1 free remote / L2 specialist (requires `[priority]`/`[grok]`/
  `[L2]` marker, budget max 2/day, attach brief not chat) / L3 human-wait.
- **lane_runner** (mag/lane_runner.py:172-196 `gate_drop`): every
  queue/lanes/<lane>/inbox.jsonl drop is gated on required fields ts/from/task/
  where/why + ttl + anchor existence before the lane acts; verdict trailed as
  GATE_VERDICT. Judge cascade gate_verdict_v2 (configs/lanes.yaml, tau 0.90
  routine band, derivation band always escalates) wired via load_gate_block
  (lane_runner.py:208-227). Census of the 12 lane dirs: inbox rows research 14,
  builder 13, day_work 6, prose 3, forge 3, night 2, economist 1, android_
  surface/bard_ledger/elder/harvest/jev 0; trail rows research 2,204,
  day_work 1,622, builder 1,113, others 6-38.
- **orchestrator** (mag/orchestrator.py): tasks in memory/runs/orchestrator/
  tasks, queue in .../queue. Census: 6,032 task files; statuses done 889,
  failed 2,244, timeout 1,821, died 915, killed 160, stalled 1, running 2
  (5,141 of 6,030 terminal tasks = 85.3 percent ended non-done); 449 queue
  files pending; orchestrator_trail.jsonl 31,891 rows.
- **mailbox binding**: spawn injects `MAG_TASK_ID` (orchestrator.py:502);
  supervisor->agent channel is memory/mail/<task_id>/inbox.txt
  (mag/pigeonhole.py:135-156 `post_cmd`/`post_steer`, steer framed
  `!steer #sid:...#` with an accepted event row). Census: 4,909 mailbox task
  dirs, only 14 inbox.txt ever created (12 nonempty) - mid-run steering of
  workers is rare relative to spawns. Steer lifecycle events: 10
  steer_events.jsonl files, 12 `accepted`, 0 `received`, 0 `applied`.

## 4. Stage D: execution

- **Interactive seat**: agent_cli run_turn drains `_STEER_QUEUE` between tool
  rounds and in bounded 0.15s mid-round windows (mag/agent_cli.py:1211-1234,
  :1483, :1542); `!pause` blocks rounds while still absorbing queued steers.
- **Headless worker**: ph.drain_inbox(_TASK_ID) reads-and-clears inbox.txt and
  stamps `received` events (mag/pigeonhole.py:208-229; consumed at
  mag/agent_cli.py:2214); steer text is injected into the running conversation
  via `_handle_steer_cmd` (agent_cli.py:2419+).
- **Hermes body**: mag/hermes_steering.py:207-254 dispatch prepends the
  FLEET_PREAMBLE (:194-204) to every goal, runs `hermes chat -Q`, banks output
  to memory/runs/hermes_jobs/<ts>.md + a receipt row; `steer --resume` (:257-286)
  nudges a live session. Census: 98 log rows (37 dispatch, 31 steer, 30 kabuki).
- **External seats**: mag/seat_steer.py:117-196 `send()` resolves surface
  aliases (:56-68), mounts the party subchain + RIB, drives chatgpt_bot /
  grok_bot / browser_driver / desktop seats, folds answer + spend, banks a JSON
  report (486 reports in memory/runs/seat_steer/); the headless path is
  `enqueue` -> `[seat-steer]` prefix task -> inline handler
  (mag/orchestrator.py:758-775).
- **Lanes**: in-cage docker exec cycles per SCHEDULE (lane_runner.py:53-70).

## 5. Stage E: banking

| Tape | Path | Census |
|---|---|---|
| Hermes receipts | memory/runs/hermes_dispatch_log.jsonl + hermes_jobs/*.md | 98 rows |
| Seat steer reports | memory/runs/seat_steer/*.json | 486 |
| Orchestrator trail | memory/runs/orchestrator_trail.jsonl | 31,891 rows |
| Lane trails | queue/lanes/<lane>/trail.jsonl | research 2,204 / day_work 1,622 / builder 1,113 |
| Steer bus receipts | watch/steer_bus_receipts.jsonl -> steer_receipt_wire -> state/vast/event_stream.py | 2 rows, wire offset == size |
| Behavioral corpus | memory/pile/behavioral_corpus.jsonl | 1 row |
| Steer bus trail | memory/runs/steer/trail.jsonl | 2,508 lines |
| Lane usage | logs/usage.jsonl | 163,136 rows, 70,096,413 B |
| Phone approvals | watch/inbox/phone_relay_log.jsonl | 138 rows |
| Steer engine telemetry | memory/steer_engine/telemetry.jsonl | 3 rows |

Durable cross-surface work is banked under watch/inbox/ per the shared artifact
boundary (AGENTS.md table; machine contract watch/inbox/SHARED_SURFACE_CONTRACT.json).

## 6. Where information gets lost (each verified this ask)

- **L1 transcript scan caps**: steer.py:76-78 reads only the first 40 jsonl
  files per transcript dir and first 200,000 chars of each; `[STEER]` markers
  beyond the caps are invisible to consume() forever.
- **L2 consume output evaporates**: consume() returns compiled memlang tokens to
  its caller; the only scheduler caller (mag/governor_autorun.py:1994-1997)
  prints `found N | compiled M` and discards them. Nothing persists the tokens.
- **L3 operator_inbox cap eviction**: committed[-50:] and processed[-100:]
  (mag/operator_inbox.py:135, :150, :337) - at cap, the oldest entries
  (possibly still pending) are silently dropped from the store. Both caps are
  currently AT capacity (50/100).
- **L4 "now" route executes nothing**: steer_router.py:154 returns
  `{"action": "run_now"}` and does nothing else; interrupt_pipeline passes it
  through without executing (:129-140). A "now"-classified steer is recorded
  and dropped unless an external caller happens to act.
- **L5 behavioral corpus dark**: 1 row lifetime against the promise "every
  steering decision recorded" (steer_router.py:19-20, :161-170). The
  human-AI learning tape is effectively unused.
- **L6 steer_bus has no executor**: 1 of 2 lifetime receipts is stuck
  `authorized-request-awaiting-governor` (watch/steer_bus_receipts.jsonl);
  no consumer of the nonce exists in mag/ (grep this ask: only swarm_tools
  calls authorize). Directed steers die authorized-but-unapplied.
- **L7 phone approvals unresolved**: 125 approval cards posted, 12 terminal
  decision rows (7 approve / 5 deny); 121 cards have no terminal row because
  the waiting process died before the timeout path could log a deny
  (phone_relay.py logs timeout only if the poll loop survives, :213-215).
  Fail-closed holds at runtime but is unprovable from the ledger for 96.8
  percent of cards.
- **L8 interrupt cache_hit hard drop**: overlap >= 0.4 -> `dropped_cache_hit`
  (interrupt_pipeline.py:99, :137-139); the instruction is batched nowhere and
  never re-queued.
- **L9 duplicate-goal refusal swallows re-steers**: orchestrator.py:946-961
  rejects an enqueue whose normalized goal matches a queued/running one; the
  new steer text is returned as an error string, not merged into the queued work.
- **L10 execution loss at scale**: 5,141 of 6,030 terminal orchestrator tasks
  (85.3 percent) ended failed/timeout/died/killed/stalled; goals are not
  auto-retried; 449 queue files sit unspawned.
- **L11 mailbox ack half-open**: 12 `accepted` steer events, 0 `received`,
  0 `applied` across 10 steer_events.jsonl files. post_steer is instrumented;
  the agent-side ack (`ack_steer`, pigeonhole.py:158-166) has no recorded use,
  so overseers cannot distinguish applied steers from ignored ones.
- **L12 Hermes receipt degradation**: SUMMARY:/DELIVERABLE: extraction is a
  best-effort regex (hermes_steering.py:133-147); absent sections reduce the
  banked receipt to raw output; session id harvest is best-effort empty string
  (:87-101), which breaks later `steer --resume` chains.
- **L13 seat_steer truncation**: reports keep message[:400] and answer[:2000]
  (seat_steer.py:173-176, :193); longer answers exist only in the driver's own
  store, if anywhere.
- **L14 drop-file drift**: steer_bridge seen state last updated 2026-08-07;
  2 of 2 active queue/steer_agent.md lines unsynced as of today.
- **L15 Telegram surface dark**: telegram_desk promises "offer to pass it to
  the operator" (telegram_desk.py:119-128) with no forwarding mechanism in
  code, and memory/runs/telegram_trail.jsonl does not exist.

## 7. The handoff chain, compressed

operator text -> (A) surface capture [REPL queue / REST handler / DM reply /
drop file] -> (B) intake store [operator_inbox.json | steer packet | mailbox
line | gated directive] -> (C) route [rightsize now/enqueue/pin | lane gate
GATE_VERDICT | orchestrator enqueue/spawn] -> (D) execute [checkpoint drain |
mailbox drain | hermes dispatch | seat send | in-cage cycle] -> (E) bank [trail
rows + job md + reports + receipts -> event stream / RIB fold / watch/inbox].

The weakest links, by measured volume: L7 (121/125 approval cards with no
terminal record), L10 (85.3 percent of dispatched tasks end non-done), L11
(steer ack loop never closed), L5/L6 (two promised organs - behavioral corpus
and steer_bus governor - have no live writer/executor).
