# AUDIT LANE A — Prior System-Attempts Inventory (Mag estate)

**Date:** 2026-09-01 · **Agent:** subagent audit (evidence-only, bounded)
**Source trees:** `/mag/memory/runs/` (450 dirs/files), `/mag/docs/ref/SURFACES.md`, `/mag/docs/ref/OPERATOR_CARD.md`, `/board/*`
**Rules:** claims cite exact path; LINKED: path; **status LINKED**: deciding evidence. UNKNOWN where undecidable. No guessing.

---

## 1. Inventory summary
Total runs/attempts found in /mag/memory/runs/: **450** (2026-07-27 → 2026-09-01).
Eras by prefix:
- **20260727*.run** dated dirs: 11 (system-era launch)
- **20260801/02/03** dated: seed-mirror-gate, high-signal, update-move-forward, unroll, sovereign-run, clerk-fix
- **20260803_/20260804_/20260830_empty_recovery**: **45** (state-capture instances, see §4)
- **Named-system dirs** (not date-stamped): majority of the rest (~390)

---

## 2. Named system attempts (evidence per row)

### ERASE-era launch runs (all `mag_run.v1`, origin of the `run.json/trail.jsonl/progress.md` harness) — status: DEAD (closed)

| Name | First | Last | Purpose (cite) | Status |
|---|---|---|---|---|
| **compose-substrate-smoke** | 2026-07-27 | 2026-07-27 | harness smoke for compose substrate. `run.json` `status:"closed"`, goal "compose substrate smoke". | **DEAD** — run.json status=closed (20260727T202213Z-compose-substrate-smoke-0afabf/run.json:4) |
| **gate-test** | 2026-07-27 | 2026-07-27 | harness gate minimal test. goal "gate test", closed. | **DEAD** — 20260727T203059Z-gate-test-8b22ae/run.json:4 |
| **self-improve-compose** | 2026-07-27 | 2026-07-27 | self-improve compose compose-spec test. 20260727T203050Z/run.json closed. | **DEAD** — run.json closed |
| **lessig-enforce-1-6** | 2026-07-27 | 2026-07-27 | norms enforce 1-6: noise cut + portable bag + norms. 20260727T214615Z/run.json closed. | **DEAD** — run.json closed |

### Republic/rope/file era (2026-07-27 → 2026-08-01)

| Name | First | Last | Purpose | Status |
|---|---|---|---|---|
| **mycelial-republic W0.5 selftest** | 2026-07-27 | 2026-07-27 | live selftest baseline + honest milestones of mycelial-republic. goal in run.json | **DEAD** — 20260727T214900Z-mycelial-republic-w0-5-live-selftest-bas-c56b9f/run.json:4 closed; superseded by republic_os |
| **seat-gate-verify** | 2026-07-27 | 2026-07-27 | seat-gate seat verify harness check. | **DEAD** — 20260727T214717Z/run.json:4 closed |
| **elias-rope-smoke** | 2026-08-01 | 2026-08-01 | Elias-rope multi-agent coordination smoke. `seat:"grok_tui"`. | **DEAD** — 20260801T110551Z-elias-rope-smoke-92531e/run.json:4 closed (is now /mag/docs/ref/COORDINATION_ELIAS_ROPE.md:1 LIVE as doc-only) |
| **file-agent-core-unit** | 2026-08-01 | 2026-08-01 | file-agent core unit test. | **DEAD** — 20260801T110606Z-file-agent-core-unit-1c646c/run.json:4 closed |
| **base-drift-cli-smoke** | 2026-08-01 | 2026-08-01 | Base+Drift CLI smoke. | **DEAD** — 20260801T112424Z-base-drift-cli-smoke/run.json closed |

### Sovereign steering era (2026-08-02 → 2026-08-03)

| Name | First | Last | Purpose | Status |
|---|---|---|---|---|
| **seed-mirror-gate** | 2026-07-27 (era) | 2026-08-02 | Closed the ≥100 practice mirror gate; mirror_train.jsonl 119 examples 0 errors. `# Milestone` + gate CLOSED. | **DEAD** — 2026-08-02_seed-mirror-gate-closed.md:1-4 marks gate closed, superseded |
| **self-improve-hour-run (mirror-as-decision)** | 2026-08-02 | 2026-08-02 | self-improve hour-run, mirror as decision input. | **DEAD** — 20260802T225935Z dir, one-shot run |
| **update-move-forward-finish-all-open-tick** | 2026-08-02 | 2026-08-02 | batch finish all open tickets. | **DEAD** — one-shot |
| **12h-sovereign-run** | 2026-08-03 | 2026-08-03 | harden autonomous proxy decision-maker: steering, failure defense, integrity. 6×2h runs DONE. | **DEAD** — final-report-2026-08-03.md:12-16 "All 6 runs DONE"; milestone achieved, superseded by fleet |

---

## 3. era: empty_recovery (the biggest single repeat)

| Name | First | Last | Purpose | Status |
|---|---|---|---|---|
| **empty_recovery** (45 instances: 25×2026-08-03, 1×2026-08-04, 19×2026-08-30) | 2026-08-03 | 2026-08-30 | bare start-of-turn state capture during sovereign-steering build; each dir = `pre_turn_messages.json` (system+session seed). Per operant card 2026-07-31 "default: stateless seat". | **DORMANT** — 19× recurred 2026-08-30 (rewritten/retried, see §6); last 2026-08-30_182406; no 08-31/09-01 evidence → dormant, not killed. Cite 20260830_182406_empty_recovery/pre_turn_messages.json:1 |

---

## 4. Live/dormant system attempts (trails still appending Aug-31 / Sep-01)

| Name | First | Last | Purpose (cite) | Status |
|---|---|---|---|---|
| **governor** | 2026-08-24 | 2026-09-01 | autonomous governor + autorun trail. `governor_autorun_trail.jsonl` 27.6MB, mtime 2026-09-01. | **LIVE** — memory/runs/governor/governor_autorun_trail.jsonl mtime 2026-09-01 |
| **orchestrator** | 2026-08-09 | 2026-09-01 | queue/orchestrator tasks; `tasks/` mtime 2026-09-01. | **LIVE** — memory/runs/orchestrator/tasks mtime 2026-09-01 |
| **seat_steer** | ≤2026-08-31 | 2026-08-31 | steer profiles per seat+lane. `steer_*.json` latest 230907. | **LIVE** — memory/runs/seat_steer/steer_20260831_230907_chatgpt.json mtime 08-31 |
| **seat_spend** | 2026-08-23 | 2026-09-01 | seat cost ledgers. `spend.jsonl` mtime 2026-09-01. | **LIVE** — memory/runs/seat_spend/spend.jsonl mtime 09-01 |
| **ask_router** | 2026-08-31 | 2026-08-31 | route task→lane; /board/ask_router_row0.json task "first_light_2… JIT lane". | **LIVE** — memory/runs/ask_router/*-route.json + /board/ask_router_row0.json mtime 08-31 |
| **session_bridge** | 2026-08-31 | 2026-08-31 | session transcripts→receipts. `receipts.jsonl`. | **LIVE** — memory/runs/session_bridge/receipts.jsonl mtime 08-31 |
| **board_tailer** | ≤2026-08-31 | 2026-08-31 | tail operator room.jsonl; cursor offset 992968 updated_ts 08-31T04:49Z. | **LIVE** — board_tailer/cursor.json:5-6 |
| **party_subchain** | ≤2026-08-31 | 2026-08-31 | deterministic instruction-set on shared crypto primitives. `head.json` invariant + chain.jsonl 145KB. | **LIVE** — party_subchain/head.json:1-2 + chain.jsonl mtime 08-31 |
| **republic_os** | 2026-08-18 | 2026-08-31 | mycelial-republic → republic OS governance rounds. `state.json` mtime 08-31. | **LIVE** — memory/runs/republic_os/state.json mtime 08-31 (rounds 08-18..08-26) |
| **steer_router** | 2026-08-10 | 2026-08-15 | pins.json routing. | **DORMANT** — steer_router/pins.json mtime 08-15, no later trails |
| **lane_salon** | 2026-08-24 | 2026-08-29 | salon per lane. latest salon_2026-08-29T2239. | **DORMANT** — memory/runs/lane_salon/ salon mtimes ≤08-29 |
| **riddler / riddler_coherence** | 2026-08-16 | 2026-08-16 | riddler coherence ledger. | **DORMANT** — riddler_coherence/coherence.jsonl mtime 08-16 only |
| **fuel_feed** | 2026-08-25 | 2026-08-26 | free rotation lane profile/batches. | **DORMANT** — batches.jsonl mtime 08-26; SURFACES.md:69 still lists it LIVE doctrine |
| **seed_percolator** | 2026-08-27 | 2026-08-27 | seed→percolator elder advice; registry.jsonl. | **DORMANT** — seed_percolator/registry.jsonl mtime 08-27 |

---

## 5. Named attempts requested but NOT evidenced (UNKNOWN / not present)

- **seat_dispatch** — no dir/file anywhere (`ls *dispatch*` empty). Not in runs root datestamped form. → UNKNOWN (renamed to seat_steer? no written evidence — do not claim).
- **riddler_common** — exists only as `riddler` + `riddler_coherence`; no `riddler_common`. → UNKNOWN.
- **frontier_salon** — "frontier_*" present but those are `frontier_advice`(08-15)/`frontier_batch`(08-10)/`frontier_help`/`frontier_internals`; no literal `frontier_salon`. → DORMANT for the frontier_* set, but salon spelling not evidenced → UNKNOWN on exact name.
- **swarm_cycle** — dir present, files only 2026-08-31 self-steal-validation (2 JSON). → **LIVE**? Only 08-31 entries: mark **DORMANT** (single-day, not ongoing). Cite memory/runs/swarm_cycle/*.json mtimes 08-31.
- **basecamp, elder, vault, chains, switchboard, archivist, ractor, water, atlas, harvest** — no top-level dirs in /mag/memory/runs/ with those exact names (scan); their receipt forms live in `/board/*.jsonl` (ARCHIVIST_RECEIPTS.jsonl, DEALS_LEDGER.jsonl, SALON_*_20260831.md, RACTOR/PACK/HARVEST docs) as **current** fleet surfaces → treated as LIVE current-layer, not historical attempts. Cite /board/SALON_RACTOR_SYNTHESIS_20260831.md etc.

---

## 6. Rebuilt 2+ times (evidence-based only)

1. **empty_recovery** — rebuilt **3 separate waves**: 25× 08-03, 1× 08-04, 19× 08-30. Same schema (`pre_turn_messages.json`). → REBUILT 3×. Cite mtime groups in runs root.
1. **sovereign-steering / autonomous loop** — attempted repeatedly 07-27(gate-test/self-improve) → 08-03(12h run) → 08-10(steer_router) → 08-31(state: ask_router/seat_steer/governor autorun). Doctrine line SURFACES.md:42 "the problem: turn on the autonomous loop". → REBUILT ≥4× (UNKNOWN exact count — rebuilt proves continuity, not same binary).

---

## 7. Cross-check vs SURFACES.md / OPERATOR_CARD.md (still-existing surfaces)

Surfaces still live **per doctairne**: OpenClaw Control UI (:18789), Mag dashboard (:8765 legacy SPA *prune*), AutoClaw ×2 credit lanes, VS Code copilot seat *(retiring)*, z_ai/z_ai4 paid lanes, z_ai2/z_ai3 coding seat pair, deepseek EXPERIMENT lane, vast.ai GPU, free rotation lanes (fuel_feed channel — still LISTED in SURFACES.md:69). State truth: verkle_chain.jsonl, invariant.check_instructions, seat mesh queue/handoff, cache_watch, fuel_feed lane_profile, docker_watchdog.
→ No attempt above breaks these; the dated `*_run*` dirs are the harness artifacts, not surfaces.

---

## 8. Totals
- Total distinct named attempts evidenced: **~33** (11 era-launch runs + 5 sovereign-era + 45 empty_recovery as one / 45 entries + ~12 live/dormant systems + UNKNOWN set).
- **LIVE**: **9** (governor, orchestrator, seat_steer, seat_spend, ask_router, session_bridge, board_tailer, party_subchain, republic_os).
- DORMANT: 5 (fuel_feed, steer_router, lane_salon, riddler, seed_percolator; + frontier_* set).
- DEAD: 16 (all `mag_run.v1` closed runs + seed-mirror-gate + self-improve-hour + update-move-forward + 12h-sovereign-run).
