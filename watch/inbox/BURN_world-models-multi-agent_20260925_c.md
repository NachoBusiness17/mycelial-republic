# BURN: world-models-multi-agent, 2026-09-25 (_c)

## Verdict

steal

## Evidence

Authoritative state: memory/game/world/world_state.json (schema game_world.v1, verkle leaves): keys table.room.<id> and table.campaign ("turn": 11). NPCs exist as room hooks: "Pump-Janitor: Check valve holds. I will not fill OUT from a bucket." Sessions live in memory/game/campaign_runs/*.jsonl. Lane receipt law (mag/lane_runner.py): every event appends a JSONL row {ts, actor: "<lane>-cage", event, detail capped at 400 chars, artifacts} to queue/lanes/<lane>/trail.jsonl, mirrored to dashboard/static/trails/<lane>.jsonl.

Fresh web (2026-09-25). Awesome-Interactive-World-Model survey (github.com/liujiuming123/Awesome-Interactive-World-Model, README fetched today, repo updated 2026-09-25), rows quoted verbatim: "R2M-Bench: Evaluating Revisit Memory via Relative Consistency in Interactive Video World Models" (2026-8-27); "MIND: Benchmarking Memory Consistency and Action Control in World Models"; "Matrix-Game 3.5: Enhancing Real-Time Streaming Interactive World Models with Patch Memory" (2026-8-30); "PlayWorld: Benchmarking World Models with Agent Players over Long-Horizon Objectives". Two defects: the search layer's summary claimed a "Game World Model for State-Aware NPC Behavior" entry; the fetched README contains no such row. And R2M-Bench and ReWorld rows share one arXiv id (2608.23565), so the list cannot say which paper a row cites. Jenova "Persistent World Text RPG AI" (Sep 17, 2026 hit): empty JS shell, no content. Both owed, not synthesized.

## Steal or Vacuous

Steal: the fleet probe spec, MSEAT-DRIFT, for the Mirror Sea MUD lane.

(a) Per NPC seat per session. Truth = world_state.json only. Each seat narration is parsed for checkable entity claims (its room id, held valves or doors, hp and inventory for module seats, campaign turn, actors present). ENTITY-ACCURACY = correct claims / total checkable claims. TRANSITION-DELTA = narrated entity changes with no intervening world write (unexplained move or mutation), per 100 turns. Paired on purpose: accuracy alone misses over-narration (Agora-2's 7.49% vs 3.54% over-switch), delta alone misses direction.

(b) Thresholds. Seat alive: session accuracy >= 0.85 (the shipped single-step anchor) and delta <= 1 unexplained transition. Drift flag: accuracy < 0.70, or delta > 1, or narrated change rate > 2x the authoritative event rate. Two consecutive flags demote the seat to canonical-hook respawn.

(c) Receipts land in queue/lanes/game/trail.jsonl using the lane_runner row schema (events PROBE_PASS, PROBE_FLAG, SEAT_DEMOTED), artifacts naming the campaign_runs transcript and world_state leaf hash; demotions escalate to watch/inbox per the burn ledger convention.

(d) Falsifier below.

## Falsifier

Pre-registered: 10 Mirror Sea NPC seats, alternately probe-on and probe-off, matched rooms and turn counts, 5 sessions each. Probe-on seats must show lower mean entity-state drift (1 minus accuracy) and lower unexplained delta per 100 turns than probe-off seats. If they do not, the probe is instrument, not medicine, and the flag mechanism is vacuous. Grading runs against world_state.json only, never against a seat's own prior narration (no self-grading overfit).

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md section 6
- watch/inbox/BURN_world-models-multi-agent_20260925.md and _b.md (prior receipts)
- memory/game/FLOW_IMAGE.json; memory/game/STATE.md; memory/game/world/world_state.json; memory/game_modules/adventure_2d6_stub.v1.json
- mag/lane_runner.py (trail schema, read this pass)
- https://github.com/liujiuming123/Awesome-Interactive-World-Model (README fetched 2026-09-25)
- Owed: R2M-Bench and ReWorld papers (README rows only; shared arXiv id 2608.23565 blocks clean citation); MIND (2602.08025) and PlayWorld (2608.13552) papers; Jenova persistent-world page (JS shell, no content)
