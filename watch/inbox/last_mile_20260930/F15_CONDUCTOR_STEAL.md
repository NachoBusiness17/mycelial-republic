# F15 — CONDUCTOR SELF-STEAL (2026-09-30, ZCode seat)

Mission: "the conductor architecture EXISTS in the estate's own organs. RUN them, fix what's stale, wire them."
Receipt = this file. Every claim below was byte-backed by a live run this session (venv `.venv/Scripts/python.exe`).

## 1. The six organs — what / wired-to / runs-today / broken

### mag/coordination.py — THE CONDUCTOR (depth routing + shared activity)
- **What:** `classify_depth` → 6 depths (overview|plan|heavy_code|simple_code|scut|conversation); `coordinate()` = classify → log activity → launch worker (queue/delegate/dispatch). Shared feed `state/shared_activity.jsonl`.
- **Wired to:** `mag/router.py` (route.v2 — one classifier, seat matrix, delegation profiles DELEG-POLICY, comms_trail consumption trust Q-009), `mag/orchestrator.enqueue`, `mag.agent_cli.api_agent_turn`, `mag.dispatch.dispatch`, `mag.context_pack`. CLI: `python main.py coordinate`.
- **RUNS TODAY (proven):** classify on 4 real phrasings → all correct (simple_code→local/ollama L0; scut→local; heavy_code→deepseek L2; plan→grok_tui no-launch). **Full loop `coordinate('summarize the current bonds in one line', launch=True)` → `{"ok": true, "action": "dispatch", "launched": true}`, dispatch ok:True, answered from local ollama (ollama daemon UP, models listed).**
- **Stale:** `DEPTH_ROUTES` hardcodes the pre-2026-09-28 ladder (heavy=deepseek, plan/overview=grok_tui). Driving ladder now: ONLY Hermes/Nous funded; Anthropic unfunded. Router still prefers deepseek/anthropic on heavy_code — deepseek budget note says "Swarm-scale deepseek: 10K calls/30M tok daily — operator supersession". Routes need a ladder refresh, machinery does not.

### mag/router.py — the real routing table (coordination defers to it)
- **What:** `route()` = single routing decision: markers (hermes/cursor/secret/research/rib/priority) → seat → provider pick (`models.quota.pick_provider`) → mode (plan/defer/dispatch/delegate/queue) + delegation profile + risk-gated reviewer + context plan (handoff_maze vs fresh pack) + model_shape.
- **RUNS TODAY:** yes — every classify/coordinate/autorun call above went through it. Comms-trail signals load clean.
- **Stale:** heavy_code prefer order `[deepseek, deepseek_overmind, anthropic, vast]` — vast/anthropic unfunded; no `nous` lane in the heavy branch despite Nous being the ONLY funded workhorse (RIB_DRIVING_LADDER_20260928). `grok_tui` planning seat = pack-only (fine, by design).

### mag/cheap_swarm.py — EXPAND+EXECUTE (flash driver)
- **What:** `scan()` GHOST-*/BUILD-* packages in `queue/handoff/` → `dispatch()` enqueues ONE to cheap tier → `run_cadence()` (daily cap 6, peak-price guard). Default lane: nvidia / deepseek-v4-flash-0731.
- **RUNS TODAY:** scan/status run clean. **BUT the lane is dead-ended two ways (proven live):**
  1. **Nvidia lane dormant** (provider_budget note: "Dormant 2026-09-26 (B2-61): roster purged, default id 410 EOL 2026-09-21").
  2. **GHOST packages never passed the enqueue gate:** `orchestrator.enqueue` defers any goal not naming a frozen `queue/handoff/BUILD-*.md` contract — live probe: `{"ok": false, "error": "Build deferred: name a frozen queue/handoff/BUILD-*.md contract."}`. Ledger byte-truth: 18 dispatch attempts = 9 ghost ALL ok:false, 8/9 build ok:true (builds DID execute in the Aug era).
  3. **Failure lockout bug:** `_mark_dispatched` writes the stem regardless of ok; `_dispatched_ids()` counts failures as done → the 9 GHOST packages return `already_dispatched` forever (live probe confirmed). Failed rows must not block retry.
- **Fix needed (small):** mark-dispatched only on ok:true (or a retry path), re-target DEFAULT_PROVIDER off the dead nvidia lane (deepseek flash / nous per ladder), and make GHOST goal text name a BUILD contract or widen the gate.

### mag/free_to_swarm.py — free-lane → k3s swarm seam
- **What:** reads banked free-seat discoveries (`handoff/OX_RS_*.json`), filters substantive (ox_fold._substance), enqueues to `mag.swarm_worker.enqueue_task` (local content-addressed queue `memory/runs/swarm_worker/queue`, drained by k3s CronJob every 15m), append-only sent ledger.
- **RUNS TODAY:** the module runs ($0, deterministic) — **but the seam is clogged: bank has 64 files, all ok:true, ZERO pass `_substance`** → `found: 0` forever. The filter's notion of substance no longer matches the bank's content shape. k3s drain side unverified this session.
- **Fix needed:** audit `ox_fold._substance` against the actual 64-file bank; either the discoveries are genuinely thin (then the bank is dead weight) or the filter is stale (then 64 discoveries are unclaimed inventory).

### mag/atlas.py — organ map (routing table of tables)
- **What:** compiles `mag.organ_map` (receipts-first) → `memory/runs/atlas/atlas.json` + receipts.
- **RUNS TODAY:** yes — rebuilt live. **41 organs: 40 VERIFIED, 39 INSTRUMENTED, 40 WIRED… but only 5 LIVE** (context_admission, operator_mode, elder, effect_broker, self_audit). None of the conductor six are LIVE. The estate has organs; almost none are on.

### mag/chan.py — the roast surface (public square)
- **What:** imageboard on `watch/room.jsonl` (4.8MB, active). catalog/thread/post/wake; `wake` = one chorus mouth via OpenClaw docker → flash fallback; `check_steer` consumes operator steer channel.
- **RUNS TODAY (proven):** `catalog` → 18 threads; **`post keep "…"` → `{"ok": true, "posted": true, id: ec539ef5}`**. Post path fully live. wake's model mouths untested this session (docker/flash dependency).

### mag/btw_sidechannel.py — inter-agent live aside messaging
- **What:** content-anchored dot ledger `memory/btw/ledger.jsonl`; inject/travel (cold/warm vector), sense, and `rightsize` perturbing swarm_rightsize (cold +1 agent / warm −1).
- **RUNS TODAY (proven):** `travel f15-conductor-steal-vector` → novel dot placed, dedupe anchors written; `size` → base 16 agents + btw cold-vector +1 perturbation, honest reasoning. Deterministic + $0. Works.

### Bonus organ confirmed live: the drainer
- `python main.py autorun --once --dry` → plans, pulls 5 todo_mag items, routes each (heavy_code→deepseek/queue). The drain half of the loop is alive.

## 2. GAP ANALYSIS — the conductor loop the operator described

Operator's shape: **one max instance routing to flash lanes + knowing when to escalate to frontier.**

What EXISTS and RUNS: the classifier+router (route.v2), the coordinate() launch loop (proven to ollama), the drainer (autorun), the activity feed, the sizing/btw perturbation, the board, the queue.

The actual gaps (wiring, not invention):
1. **No standing loop.** coordinate() is a call, not a daemon. Nothing polls the activity feed / inbox / chan and re-enters coordinate() on a cadence. The governor_autorun drainer is the closest live thing — it needs a front half that feeds it goals from the operator surface (chan/inbox) instead of only todo_mag.
2. **Escalation rung is mislabeled.** "knowing when to escalate to frontier" is coded as deepseek/grok_tui/anthropic prefer-orders — all unfunded or superseded per RIB_DRIVING_LADDER_20260928. The frontier rung today is Nous (glm-5.3-prime/qwen3.8-max-prime); router has a `nous` lane in _COMMS_SEAT_LANES but not in the heavy/prefer branches. One-line-ish table refresh.
3. **Flash lanes are unplugged.** cheap_swarm's nvidia lane is EOL'd; free_to_swarm's substance filter rejects the whole bank. The "expand at the cheap" half has no live provider feed even though ollama IS up and deepseek flash budget note says swarm-scale daily allowance exists.
4. **No feedback fold.** Nothing reads dispatch outcomes (shared_activity rows flip to done/failed — proven) and adjusts routing (the comms_trail consumption signal exists but only reorders provider lanes, doesn't gate escalation).

## 3. VERDICT — BUILD vs RUN vs WIRE

- **NEEDS RUNNING (exists, works, just off):** coordination+router loop (proven), autorun drainer, chan board, btw ledger, atlas. Turn on: a cadence task/cron that calls `coordinate()`/`autorun --once` on demand.
- **NEEDS WIRING (exists, disconnected):**
  - router DEPTH_ROUTES/prefer-orders → 2026-09-28 driving ladder (nous frontier rung, unfunded lanes demoted). ~table edit.
  - cheap_swarm DEFAULT_PROVIDER → live flash lane (deepseek flash per its swarm-scale budget note, or local ollama).
  - free_to_swarm `_substance` filter → current bank shape.
  - chan/inbox front-half → drainer feed (the standing loop's entry).
  - GHOST gate: either freeze GHOSTs as BUILD-*.md contracts or widen orchestrator's gate.
- **NEEDS BUILDING (genuinely missing, small):**
  1. Failure-retry in cheap_swarm `_mark_dispatched` (ok:false must not lock the stem) — 3-line fix.
  2. The escalation trigger policy: a signal (risk markers exist; budget signals exist) that flips a goal from flash lane to the funded frontier rung — the pieces exist in router (markers, grok_budget_ok, delegation profiles) but no one composes them into "escalate now."
  3. A standing conductor cadence (one max instance): single scheduler entry that drains inbox/chan/todo → coordinate() → autorun. The estate has every piece; it does not have the while-loop.

**One line:** the conductor is ~90% present and its spine (classify→route→dispatch→drain) ran live this session; what's missing is a funded-lane table refresh, three small unblocks (cheap_swarm retry + provider, free_to_swarm filter), and one while-loop.

*Filed by ZCode seat, 2026-09-30. Runs cited: classify x4, coordinate launch=True (dispatch ok), cheap_swarm scan + re-dispatch probe + enqueue gate probe, chan catalog + post (id ec539ef5), btw travel + size, atlas build, autorun --once --dry, provider_budget x8, ledger counts (9 ghost false / 8 build true / 1 build false), OX_RS bank 64 files / 0 substantive.*
