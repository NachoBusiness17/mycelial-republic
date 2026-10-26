# PIPELINE RIGHT PLAN — the Sep 7→20 window, spent right (2026-09-07)

**Commission (operator verbatim intent, 09-07):** OpenClaw retires → Hermes ($220 in).
Two z.ai plans (Lite $18 + Max), effectively unlimited 5.x usage Sep 3–20, 8AM–6PM PT,
API-accessible. "We need to focus on getting the pipeline right so I'm not managing
these things… I type and am a stochastic dynamo — you figure out how to sustain it."
Proof deadline Sep 20. This is the plan. PLAN ONLY — nothing here spends or touches
infra without the gate marks below.

**Primary-source note (tri-state):** the operator's "8AM–6PM PT unlimited" window is
byte-identical to the vendor campaign window receipted in
docs/ref/ZAI_API_EXPERT_REFERENCE.md §10.6 ("Sep 3–20, daily 23:00–09:00 UTC+8 = 15:00–01:00 UTC = 8AM–6PM PDT,
zero-quota glm-5.3-flash via ZCode, all paid plans") — and §10.4's Max-package billing row
(32,262,464 tok, $0.00, 0 credits, 09-03) already receipts zero-burn in-window on a package key.
So "daytime unlimited" = SUPPORTED (operator statement + vendor notice + billing row).
The plan keys ARE the API keys: 4f8a…6464 = "GLM Coding Lite V3 Yearly" and e18f…617f =
"GLM Coding Max V3 Quarterly" per the 09-04 billing receipts in the same reference —
SUPPORTED. The stale tension in that reference ("Lite rows showed credits on 09-03")
resolves as out-of-window traffic; falsifier F-A1 below settles it permanently.

---

## A. WINDOW ECONOMICS — routing table Sep 7→20

Posture change: conservation is OVER inside the window. Quota-hoarding was correct for
scarce pools; it is now a tax. The risk flips from "run dry" to "leave the window's
compute unspent on Sep 20."

### The routing table

| Slot (PT) | Lane | Models | Rides what |
|---|---|---|---|
| **Day 8AM–6PM** | z_ai2 (Max package key) + z_ai3 (Lite package key) | glm-5.3-flash (primary), glm-5.3 (judgment, sparing) | Salons, vision-pipeline INTERPRET, swarm bays, builder windows, corpus distillation, MAX_DISTILL epochs, citation mining. Configs: configs/providers.yaml z_ai2/z_ai3; billing rates §10.4. |
| **Day 8AM–6PM** | z_ai / z_ai4 (opencode-only plan doors) | glm-4.7-flash / 4.5-flash | Always free at all tiers (§1) — keep as bulk backstop. |
| **Night 6PM–8AM** | ollama (the eye) | 13 local models, host-side since EYE MIGRATION 09-07 (state/CURRENT.md; watch/OLLAMA_EYE_TO_HOST_20260907.md) | T0/T1 private tier, recall lane ([ollama]-only in providers.yaml routing), secrets-adjacent work, night composites. Unlimited, $0, dies with no vendor clock. |
| **Night 6PM–8AM** | free API lanes | glm-4.7-flash (concurrency **1** — single-flight only, §Addendum), openrouter 18 lanes, groq/nvidia/etc. | Scut + cache mining per configs/providers.yaml prefer_order. |
| **Night 6PM–8AM** | deepseek (off-peak only) | v4-flash | Paid workhorse per mag.offpeak; never default. |

### Metering — no seat hits a wall blind

Instruments already exist; wire them, don't build new ones:
- **logs/usage.jsonl** — the per-lane log (configs/lanes.yaml:93).
- **watch/usage_sweeps/USAGE_SWEEP_*.md** — `usage_meter_sweep.v1`, rides the lane_runner
  economist 06:00 shift (mag/lane_runner.py:280); latest 09-06 already flags output-ratio offenders.
- **mag/burn_steer.py** — $0 telemetry read of ~/.zcode/cli/db/db.sqlite → burn_board.html.
  Repoint its pool constants from "300M weekend" to "Sep-20 window" and it becomes the
  window dashboard with zero new code.
- **mag/refeed_guard.py** — B1 guard; re-arm lands Sep 8 02:19Z per configs/auth_tracks.yaml
  (`lite-rearm-sep8` track). Keep it: unlimited ≠ license to burn 50% of throughput on re-feed tax.
- **PAYG lane** (zai-apikey-entry, $15.08 + alert ON, auth_tracks 09-07) stays the designated
  spill lane when both packages are busy — it is the only cash surface.

**One small build (standing-GO):** a window-clock gate in the lane config — every z_ai2/z_ai3
lane checks current PT time before firing; outside 8AM–6PM PT it defers to ollama/free lanes.
Declarative, ~20 lines in configs/lanes.yaml + fuel_feed check, no daemons (headless law).

### Taper — what happens Sep 20 6PM PT so nothing breaks

- **Sep 18:** last day for new long-horizon launches; anything started must finish on its own.
- **Sep 19:** freeze + receipts (see D4). No new opens.
- **Sep 20 6PM PT:** the window-clock gate flips routing automatically back to the standing
  posture (free lanes + ollama + metered package credits: Lite 2,000/5h · 10,000/wk).
  Nothing structurally depends on unlimited — routing is declarative (providers.yaml/lanes.yaml),
  and no lane was retired for the window. Posture restore = one config flip.
- **Sep 21:** first post-window usage sweep reads as the canary.

**Falsifiers:**
- **F-A1:** any billing row on either package key showing cash OR credits consumed on
  glm-5.3-flash inside 8AM–6PM PT after Sep 8 → "unlimited daytime" DISPUTED; conservation
  posture re-arms same day. (This is the 09-03 Lite-row tension, settled with data.)
- **F-A2:** error 1308/1310/1316–1321 observed on a lane the gate believed in-window →
  the gate's clock or the window's true shape is wrong; fix before any long burn.
- **F-A3:** a sweep shows a lane >90% through any budget (PAYG balance, weekly credits)
  → the meter failed its one job; blind-wall incident, self-steal filed.

**Gate split:** window-clock gate + burn_steer repoint + sweeps = **standing-GO** (config +
$0 reads). Any raise of PAYG spill caps, new keys, or paid model routing = **operator-gated (KEYS/spend)**.

---

## B. THE DYNAMO PIPELINE — he types, it compounds

Target chain, one operator message end-to-end:

```
OPERATOR posts ONE message (OPERATOR_DRIVE.md paste-line / research window)
  → [1] INTAKE TRIAGE (vision pipeline: READ→FILTER→INTERPRET→CITE-GATE→RIGHTSIZE→JIT)
  → [2] CARD files to watch/inbox/ (score → file → LAUNCH — the LAUNCH LAW shape)
  → [3] SALON fires (watch/salon_runner.py v4 multi-engine; full-depth bar per
        watch/OLLAMA_MAZE_SALON_20260907.md rubric 5/5; mag/lane_salon.py bench re-fire)
  → [4] BUILD-WINDOWED items spawn builders SAME TURN (LAUNCH LAW amendment 5)
  → [5] VERIFY (mag/grounding_wave.py hash-chained tri-state GROUND rows; rotation + cite-rate)
  → [6] FOLD (mag/knot_at_close.py bridge at session close; mag/topic_index.py reindex; chain append)
  → [7] RECEIPT visible (mag/overseer.py → dashboard/static/overseer.json → live.html strip)
```

### Doors that already exist (verified on disk, 09-07)

| Door | File | State |
|---|---|---|
| Operator paste surface | `OPERATOR_DRIVE.md` (repo root) + research-window law (AGENTS.md; queue/handoff/zcode/RUNNING.md charter) | LIVE |
| Intake triage | vision pipeline; **mag/cite_gate.py** (rotation 3/3 per AGENTS.md; fetch door still operator-gated egress) | LIVE, one gate |
| Card + launch law | watch/inbox cards; LAUNCH LAW amendment 5 (AGENTS.md) | LIVE (seat-executed) |
| Salon multi-engine | **watch/salon_runner.py** v4 (door B: drop json in watch/salon_inbox/ → `drain`) | LIVE |
| Salon bench | **mag/lane_salon.py** (roshomon over reachable API lanes) | LIVE |
| Same-turn builder spawn | lane_runner ADOPT-2 gate_drop (RUNNING.md) | LIVE, seat/nudge-executed |
| Execution engine | **mag/lane_runner.py --daemon** in-cage (research 15m, builder 30m, day_work 30m, economist 06:00, bard 20:00, elder 12:00, night 23:00) | LIVE |
| Verify | **mag/grounding_wave.py** GROUND ledger (multi-seat proven) | LIVE |
| Fold | **mag/knot_at_close.py** (3 knots through gate; tranche door open) + chain | LIVE, tip-stale bug self-heals in lock |
| Surfaces | **mag/overseer.py** → overseer.json/live.html | LIVE |

### Missing connectors (exactly two)

- **C1 — the AUTO-CHAIN:** wire salon_runner door B into the research lane (inbox drop →
  drain fires automatically on the 15m research tick) and wire builder spawn off card
  disposition (OPEN-WIRE card → ADOPT-2 drop) instead of off a seat noticing. Today every
  hop is real but seat-hand-executed; the chain has no conveyor. This is glue on organs
  that all exist — no new subsystem.
- **C2 — the LEVERAGE RECEIPT:** overseer gains one intake-correlation row: "message X →
  cards Y,Z → builds A,B,C → GROUND rows → knots." The operator sees his one message's
  compound interest without opening a single file.

**The test (falsifiers):**
- **F-B1:** operator posts ONE message; a full pass (card → salon → ≥1 builder spawn →
  ≥1 GROUND row → knot/receipt) completes with ZERO hand-touch from any seat other than
  the trigger — 3 drills, 3 passes = PASS. Any nudge needed = the connector name that failed.
- **F-B2:** post→builder-spawn latency ≤ 1 research lane cycle (15 min). Slower = C1 vapor.
- **F-B3:** C2 row appears in overseer.json for every drill; absent row = pipeline not observable.

**Gate split:** C1/C2 build + drill fires = **standing-GO** (files + in-cage lanes, no host
daemons, no spend). cite_gate's external fetch egress = **operator-gated (GO, already on
record as pending)**. Anything needing ONE-STOP stays deferred per LAUNCH LAW.

---

## C. OPENCLAW → HERMES TRANSITION

### What retires (docker-compose.yml, all verified 09-07)

- `openclaw` (container **mag-openclaw**, image mag-openclaw:local, build ./deploy/openclaw)
- `tailscale-openclaw` (container **mag-openclaw-tailscale**, the shared netns)
- `cloudflared-openclaw` (container **mag-openclaw-cloudflared**, rides openclaw's netns)
- volumes `mag_openclaw_data`, `mag_openclaw_tailscale`; mounts ./deploy/openclaw/hooks
  and ./queue/handoff/openclaw/PATCHES (the governed write path).

**Method (precedent: the eye):** move the three services behind a compose profile
`retired-openclaw` (exact pattern of `retired-eye`, state/CURRENT.md 09-07) — reversible
by one `docker compose --profile retired-openclaw up -d`. Backup volumes first (backup-first law).

### What moves to Hermes as control surface

Hermes is the gopher BODY, not a second brain — Mag holds the wheel
(watch/inbox/HERMES_STEERING_20260907.md). The organ **mag/hermes_steering.py** is already
receipted: `dispatch` (pack+goal, SUMMARY:/DELIVERABLE: contract), `steer --resume`
(mid-run nudge, byte-verified), `jobs` (log tail); personas as data (mag/hermes_personas/);
the `hermes cron` cockpit door is cut, not yet wired. Migration = openclaw's remote-body
duties land on these doors, with Mag dispatching.

### What the $220 buys

**UNVERIFIED — the repo has zero Hermes pricing/product data.** Hermes on this machine is
a local CLI (hermes.exe v0.21.0) currently riding a synced copy of the fleet Lite key
(HERMES_STEERING repair note). Plausible readings: (a) its own subscription/quota so it
stops riding the Lite pool, (b) API credits, (c) hosted control-plane. Name it UNVERIFIED;
the spend itself is **operator-gated (KEYS/spend)** by definition. One probe the fleet can
do free first: what does $220 replace? If it only buys quota, the two unlimited plans may
already cover Hermes' burn via the synced Lite key — worth one sentence to the operator
before the money moves.

### Migration steps (with rollback)

1. **Inventory openclaw duties:** remote phone surface (cloudflared sidecar), tailscale
   reach-in, PATCHES governed write path, board/chan intake hooks (deploy/openclaw/hooks —
   only `mag-file` found on disk; the 4chan/board lane also lives in
   .agents/skills/chan/SKILL.md as a seat skill, so capability ≠ container).
2. **Snapshot:** volume tars + compose backup + config baks (config.yaml.bak-* pattern).
3. **Rehome:** board hooks → chan skill in-seat or a Hermes persona via dispatch; PATCHES →
   Mag direct-apply (the queue existed because openclaw couldn't be trusted with writes;
   Hermes' writes are already receipt-gated by the organ); phone surface → the standing
   Cloudflare-tunnel door (operator's one-login item, AGENTS.md morning build order).
4. **Flip:** add `profiles: [retired-openclaw]` to the three services; `docker compose up -d`.
5. **Burn-in:** 48h Hermes-carried gopher jobs via hermes_steering (cron row wired from the
   cut cockpit door), dispatch log as receipt.
6. **Rollback:** remove profile flag, up -d, restore volumes if touched. <5 min, rehearsed
   as part of step 2.

### What the fleet loses if hooks are not rehomed

The board/chan intake lane (openclaw was the container that could read/write those
surfaces unattended) and the tailscale phone reach-in. Both are loss of SENSES, not loss of
brain — per MCP-topology law senses live in the cage, so the rehome target is a cage-side
worker or a Hermes persona, never a host window.

**Falsifiers:**
- **F-C1:** 48h post-retirement with zero operator-visible surface loss AND ≥3 successful
  hermes_steering dispatches covering openclaw's old duties → migration SUPPORTED.
- **F-C2:** any duty discovered ONLY after retirement (a thing nobody inventoried that
  breaks) → inventory was vapor; rollback + re-inventory.
- **F-C3:** rollback drill exceeds 5 min → profile method failed, keep openclaw until fixed.

**Gate split:** inventory + snapshots + rehome code (personas, PATCHES-apply, persona for
chan) = **standing-GO (files only)**. Compose profile flip / container stop, and the $220
spend = **operator-gated** (fleet-process law: kill of fleet processes is operator-gated,
ORPHAN_BOARD_20260906.md item 1 precedent; money is KEYS).

---

## D. WHAT THE WINDOW BUYS — ranked builds before Sep 20

Score = survives-after-window × feeds-Sep-20-proof × operator-visibility (1–5 each).

| # | Build | Survives | Proof | Visible | Why now (unlimited 5.x makes it cheap) |
|---|---|---|---|---|---|
| 1 | **THE DYNAMO (B's C1+C2)** | 5 | 5 | 5 | It IS the commission ("I type… you sustain it") and it IS the Sep-20 demo. Outlives the window because it's posture-independent glue on permanent organs. |
| 2 | **94 OPEN-WIRE burn-down** (watch/ORPHAN_BOARD_20260906.md; watch/ORPHAN_AUDIT.json; each row names its missing artifact) + knot_at_close tranche drain (499 knotless sessions, --limit 50 passes) | 5 | 4 | 3 | Unlimited daytime = full-depth closes instead of triage; landed artifacts compound forever; the queue already exists. |
| 3 | **Keeper's Maze v3, evidence-bound** (watch/OLLAMA_MAZE_SALON_20260907.md: corrections first — tesuji count 319/310, 4.02%/layer vs 1.52%, specimen binding, one logprobs probe on v0.32.7 — then build) | 5 | 4 | 5 | The Rocinante substrate-introspection rehearsal; every observable is local and $0; survives as THE pre-Oct-27 instrument. |
| 4 | **Sep-20 proof package** (compile: tesuji 200-cell falsifier due Sep 20, X-harvest gate closed, GROUND ledger, salon receipts, window economics F-A1 receipt) | 3 | 5 | 5 | Pure assembly of what the window produces; the deadline deliverable. |
| 5 | **Corpus health pass** (topic_index 1,040 cards/23 buckets; cite-gate rotation to 100%; the Astra citation-audit corrections owed on our own record) | 4 | 3 | 2 | Judgment-heavy, token-heavy — exactly what metered lanes rationed. |

**Gate split:** all five = **standing-GO** (files, in-cage lanes, plan-lane tokens in-window,
local ollama). None needs keys. Two carry named operator gates that already exist: Maze v3's
own corrections-land-before-build condition (self-imposed, Astra receipt) and cite_gate's
egress GO.

**Window falsifiers:**
- **F-D1:** Sep 19 freeze check — any of the five NOT demonstrably advanced vs its 09-07
  state → the unlimited window was wasted on prose instead of artifacts; self-steal filed.
- **F-D2:** the Sep-20 demo (D4) must show a live dynamo pass, not screenshots of one.
- **F-D3:** OPEN-WIRE count on Sep 20 < 94 (target ≤ 40) or the burn-down lane is reclassified
  as vapor.

---

## Bottom line

The economics inverted: compute is free until Sep 20 6PM PT; the scarce inputs are now the
operator's attention and the pipeline's throughput. Spend the window on the pipeline
(Dynamo), let the pipeline spend the window on the queue (OPEN-WIRE), rehearse Rocinante
(Maze v3), and compile the proof. OpenClaw retires behind a reversible profile; Hermes
becomes the receipted gopher body; the $220 question gets one honest UNVERIFIED flag
before the money moves.
