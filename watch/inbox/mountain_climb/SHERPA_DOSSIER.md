# THE SHERPA — the carrier architecture (MC1)

Date: 2026-09-30 · Owner seat: ZCode (MC1, mountain climb) · File: `watch/inbox/mountain_climb/SHERPA_DOSSIER.md` · No commit (per plan).

**For a frontier model reading cold.** THE SHERPA is the carrier architecture that hauls the estate's climb: the seats, mates, stealth fleet, improve cycle, memory organs, meters, discipline organs, and compute laws — the machinery that carries the load while the operator leads. Definition source: `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md` §metaphor.

Reading laws used throughout (so you can trust the statuses):
- Every status is one of **PROVEN** (receipt or live bytes show it working), **PARTIAL** (built, known break or unwired leg), **DORMANT/PLAN** (specified or referenced, no landed receipt).
- **Trust bytes, not reports** (AGENTS.md census law): where a written note and live bytes disagreed, the bytes won and the disagreement is named.
- Counts are snapshots of one instrument at one moment, never constants (B2-216, AGENTS.md).

---

## 1. THE SEATS — where work is sat

The doctrine: **seats are disposable tools the estate uses; the estate lives in its organ state, not in any window** (`watch/inbox/SEAT_ARCHITECTURE_BRIEF_20260928.md` Part 2: "The windows are tools the estate uses, not the place the estate lives"). The estate runs with no window open at all (boot lane + stealth driver + scheduled tasks — same brief).

### 1a. ZCode orchestrator pattern — PROVEN (primary seat)
- **What it is:** this repo's main agent plus its two fan-out shapes (Task agents and gated dynamic workflows). The pattern that matters is the orchestrator discipline, not the model: per-item named actors, interagent pass-off, reviewer steering, incremental salvage, receipt landing.
- **What it carries:** all deep-work windows: coding waves, the Mickey17 24-wide edge-mining wave, dossier lanes like this one.
- **Source:** `memory/improve/SEATS.md` §2026-09-27 REALITY REFRESH ("Primary seat: ZCode on the z.ai GLM-5.3 individual coding plan"); the workflow gate enforces the pattern (`tools/workflow_gate.py`) and its registry holds 40 PASS/FAIL rows, latest PASS 2026-09-30T01:18Z (`memory/workflows/REGISTRY.jsonl`, byte-counted this session). Build-discipline laws: AGENTS.md §Build discipline.

### 1b. Hermes ambient — PROVEN as the standing ambient seat (role ruling 2026-09-28; status nuance below)
- **What it is:** the always-on headless seat: free Ling-3.0-flash-sante via Nous, Discord channel (NT-ACv2) wired to phone-visible plain text, steering intake, warm boot.
- **What it carries:** monitoring, mesh comms, phone-visible status, steering intake, the AFK cadence; rescue/second-engine verification per the driving ladder (organ 8).
- **Source:** `watch/inbox/SEAT_ARCHITECTURE_BRIEF_20260928.md` Part 2 (3 processes alive, gateway green, "Hermes = the standing 24/7 ambient seat"); warm boot works — `memory/warm_state.json` generated 2026-09-29T07:53Z carries chain tip (index 8315, verkle root) + Vercel URLs + session brief (`python -m mag.hermes_warm_boot`, AGENTS.md header).
- **Nuance, named:** AGENTS.md (older framing) calls Hermes "dormant but dispatch-capable"; the 2026-09-28 brief is the newer ruling. Both agree Hermes is never the router (HABIT.md invariant 6) and private/recall never routes to it.

### 1c. JetBrains launcher — DORMANT/PLAN
- **What it is:** an IDE-launched agent seat for JetBrains editors (the Claude-Code-style IDE-plugin surface), analogous to the proven Cursor seat (`launch_cursor_seat.cmd` + `watch/cursor_bridge.py`, `memory/improve/SEATS.md`).
- **What it carries (planned):** an editor-embedded lane whose file writes land in the Verkle trail like the Cursor seat's.
- **Source:** no launcher or receipt exists in this repo. References only: `docs/ref/zai_docs_mirror/devpack/tool/others.md` (vendor mirror: "The Claude Code IDE plugin supports VSCode and JetBrains") and `configs/agent_bleeding_edge_repos.yaml` (`steal_focus: ... jetbrains_agent_surface`). Honest status: an idea with a steal-target, nothing landed.

### 1d. Laptop second-seat — PARTIAL (routing law defined, lane not yet exercised)
- **What it is:** an M4 Mac (unified memory, MPS) as overflow compute for work infeasible on this Windows box (no CUDA).
- **What it carries (planned):** the LoRA fine-tune arm and 7B free-text arms of the AI-welfare replication study.
- **Source:** `watch/inbox/last_mile_20260930/AI5_REPLICATION_SPEC.md` §8 ("INFEASIBLE ON THIS BOX → route to M4 / laptop"). No M4-run receipt found this session — the lane is specified, not yet proven by a landed run.

### 1e. Phone-body plan — DORMANT/PLAN (two halves, honestly split)
- **Operator surface (phone as remote):** "Phone = Discord, through Hermes" — plain-text status, GO/STOP words, steering in NT-ACv2. Source: `watch/inbox/SEAT_ARCHITECTURE_BRIEF_20260928.md` Part 3. The mechanism exists end-to-end (Discord → Hermes gateway → steer intake); the proposed ONE daily plain-text digest awaits operator GO (same brief, decisions list).
- **Agent body (phone as embodiment):** the android-emulator MCP server named "the phone body" — one capability among the hands-and-eyes MCP set. Source: `watch/SELF_STEAL_MCP_LEVERAGE_20260905.md` §3. The plugin is installed in the harness, but no estate receipt of driving it was found. Plan, not organ.

---

## 2. THE MATES — 8 personas, the leave protocol — PARTIAL (machinery proven; first fire red at the auth layer)

- **What it is:** eight ractor-persona mates (cartographer, locksmith, archaeologist, innkeeper, jester, lamplighter, mariner, gambiter), each with a persona voice, a hunting ground, and a seeded thread drawn from the day's receipts; seeds rotate from previous JOURNEY dead-ends. Every mate receipt must carry a JOURNEY section (threads followed, dead ends named, why each turn).
- **What it carries:** the estate's reproductive system — mission packs propagate doctrine, receipts seed the next waves (`watch/inbox/TIE_IT_ALL_20260930.md` §1).
- **The driver story (bytes beat the note):** the register note honestly says the driver was blocked by the Mimosa security gate through three hardenings and MagLeaveProtocolDaily was "NOT registered" (`watch/inbox/mates_leave_protocol/REGISTER_NOTE.md`). That was then. What landed after: the static-runner indirection — `tools/leave_dispatcher.py` (zero variable argv; all variance in mission files under `logs/mates/missions/`) + parameter-free `scripts/run_mate.ps1` (atomic claim per mate) — receipt `watch/inbox/hydrology/X12_MATE_UNBLOCK.md`.
- **First fire 08:00 — it fired, and it failed honestly:** scheduled task bytes: MagLeaveProtocolDaily daily 08:00, Last Run 2026-09-30 08:00:01 (`schtasks /Query`, read this session). All 8 missions for 2026-09-30 were written and claimed; all 8 mate processes launched at 08:00:02 and all exited 1 within ~65s — `logs/mates/runner_20260930.log`; the run log names the cause: opencode → glm-5v-turbo → "Authentication parameter not received in Header" (`logs/mates/runs/run_20260930_01_cartographer.log`). So: dispatch machinery PROVEN (task, dispatcher, claims, STEER injection), execution layer BROKEN (mate model auth). Fix owed next window.
- **Config source:** `configs/mates.yaml` (8 mate ids byte-verified this session).

---

## 3. THE STEALTH FLEET — 24/7 free-lane sensing — PROVEN (running now)

- **What it is:** a boot-triggered (logon, never clocks), fail-open background driver rotating seven topics on 300s cycles: probe20 drift, rumor drill, fossil check, chain verify, roster churn, FKB pressure, backlog census — plus free-lane "work" sensing that mines findings on free models.
- **What it carries:** the estate's sensing surface. Its outputs are banked as findings, never trusted as done work — the funded tier or the bytes verify (`memory/rib/RIB_DRIVING_LADDER_20260928.md` Invariant 2).
- **STOP law:** one file, one word — create `state/stealth_driver.off` and it exits on the operator's word (observed live once in `logs/stealth_driver_stdout.log`, which is the law proving itself, not an outage).
- **Liveness bytes (this session):** landed 2026-09-28 00:10 (`watch/inbox/STEALTH_DRIVER_247_20260927.md`); heartbeat `state/fuel/stealth_driver.jsonl` at cycle 235, 2026-09-30T18:17Z — ≈66h continuous at last byte-read heartbeat, ~69h wall-clock at dossier time; mined-findings ledger `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` at 428 rows, appending as of 18:37Z same day. SSRF boundary enforced in code, Mimosa-guarded twice (same receipt).

---

## 4. THE IMPROVE CYCLE + SELF-STEAL AUDIT — PROVEN

- **Improve cycle:** `mag.cmd improve --once` — local scout + eval → `memory/improve/field_brief.md`; candidates ledger with a human promote gate (`mag.cmd promote --apply`; invariant: "Improve scout never uses paid remote", `memory/improve/SEATS.md` invariant 1). Daily task MagImproveDaily 08:00 registered (`scripts/register_improve_task.ps1`; schtasks bytes this session: next run 10/1 8:00 AM). Tests: `tests/test_improve_loop.py`, `test_improve_behavioral_scout.py`, `test_improve_crash_scout.py`, `test_improve_off_on.py`, `test_improve_provider_probe.py`.
- **Self-steal audit:** the estate audits its own organization with its own dig instruments. The keystone receipt is `watch/inbox/ATLAS_SELF_STEAL_20260927.md`: it found the fleet had rebuilt the L0–L6 communication layer cake, confirmed the flywheel lives in organ state (ledgers, saved workflows, catalog+FTS, bonds — lanes are bearings), named the leak law (every hop where a receipt lands without a ledger row / index key / reader), and filed fix queue Q1–Q7 (Q1 brief repoint and Q2 SEATS refresh are landed — `state/CURRENT.md` is the live truth per AGENTS.md; SEATS.md carries the 09-27 refresh). The steal family it rides: `corpus/steal/` (e.g. `ZCODE_RATCHET_LANDED_20260924.md`, `ZCODE_OPERATING_PLAYBOOK_20260925.md`, `TETHERED_LINK_STEAL_20260925.md`).

---

## 5. THE MEMORY ORGANS — how the estate remembers — PROVEN

- **Verkle chain + knots:** every session dossier is a knot leaf; the chain tip is a Merkle–Verkle-style root. Writer `mag/verkle_knot.py`; leaves `memory/biography/knots/`; chain `memory/biography/verkle_chain.jsonl`; tip `memory/biography/verkle_tip.json` — bytes this session: root `298a6d0e…`, **n_leaves 8,670**, updated 2026-09-30T18:13Z. The stealth driver verifies it every cycle ("chain consistent (8,670 leaves)", heartbeat bytes above). Tests: `tests/test_verkle_artifact.py`, `test_verkle_audit.py`, `test_verkle_compaction.py`, `test_verkle_lock.py`, `test_verkle_dangling.py`, `test_verkle_restore_prep.py`.
- **Ribs:** warmed law-memory, loaded before acting ("boot-order is load ribs → load state → then act", AGENTS.md driving ladder). 45 rib files in `memory/rib/` (byte-counted), e.g. `RIB_DRIVING_LADDER_20260928.md`, `RIB_FREE_USAGE_POLICY_20260823.md`. Status: PROVEN as doctrine; the remember-first invariant exists because a fresh seat had to be corrected three times for re-deriving what a rib held (same rib, Invariant 3).
- **Oral law index:** the operator's spoken laws mined into rows: `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` (153 rows; 59 LAWS + 29 DEBTS byte-verified in the dedupe receipt), mined by `watch/inbox/mates_leave_protocol/oral_law_mine_20260930.py`; deduped by `tools/oral_law_dedupe.py` → `ORAL_LAW_DEDUPED.jsonl` (55 rows), receipt `watch/inbox/operator_model/W3S_ORAL_DEDUPE.md`, tests `tests/test_oral_dedupe.py`.
- **Quantizer:** compresses the Verkle lattice into dense summary knots so an agent reads ONE knot instead of N (lossy like INT8, preserves dominant themes/tension trajectory). Source: `mag/state_quantizer.py` header; tests `tests/test_thought_quantizer.py`, `test_tool_quant.py`, `test_context_pack_quantized_laws.py`, `test_mcp_quantized.py`; hygiene receipts `watch/inbox/ball2/quantizer-hygiene.md`, `watch/inbox/ball3/quantizer-fallout.md`.
- **Percolator:** the $0 deterministic signal classifier — raw signal in; noise/theater stripped to noise files; repeats compiled to invariants; novel signal queued for exploration. Operator's own words (2026-08-11) in `mag/percolator.py` header; tests `tests/test_percolator_z15.py`.

---

## 6. THE METERS — how the estate measures itself — mostly PROVEN

- **GPS ledger** (`tools/gps_mcp/`): the capability ledger router — models routed on MEASURED pass-rate from a SQLite ledger (incremental running mean + positive floor, momentum/streaks/badges), every routing decision an append-only JSONL receipt. Ships TEST-DOUBLE ($0 offline; flip `test_double: false` to go live). Sources: `tools/gps_mcp/README.md`, `tools/gps_mcp/test_gps_mcp.py`; lineage `watch/inbox/GPS_FOR_DUMB_AGENTS_20260918.md`. The GWAP→GPS bridge is built (287 lines, 15 tests, `mag/gwap_to_gps.py`) but carries no live traffic yet — `watch/inbox/TIE_IT_ALL_20260930.md` §3 names this as thin spot 1. Status: PROVEN instrument, PARTIAL metabolism.
- **Duel harness** (`tools/duel_harness.py`): one ask → two model families → a third cheap judge on a rubric; every duel appends a cost-carrying row to `logs/duel/duels.jsonl` (byte-count: 73 rows; live alternate-judge rejudge banked 2026-09-30T18:21Z this session). Retroactive mode judges already-paid burn answers without re-paying contenders. Source: `watch/inbox/game_platform_basecamp_20260929/W3_DUEL_HARNESS_20260929.md`; tests `tests/test_duel_harness.py`. Status: PROVEN.
- **Anomaly flagger** (`tools/anomaly_flagger.py`): byte-level anomaly sweeps over three streams (trajectory steps, oral-law index, burns ledger verdict enum + evidence paths), exit 0 clean / 1 with rows named. Landed IMP6 2026-09-30 with spec-first docstring; 11 tests; live run 2026-09-30T17:49Z exit 1 (anomalies named, not hidden). Source: `watch/inbox/last_mile_20260930/IMP6_ANOMALY.md`. Status: PROVEN.
- **Cost rollup** (`tools/cost_rollup.py`): read-only scan of all four cost surfaces → per (day, model) calls/total_usd + trailing trend + `--json` dashboard payload; unparseable rows NAMED, never dropped. The climb plan called this "incoming"; bytes say it LANDED 2026-09-30 (7 tests passed). Source: `watch/inbox/last_mile_20260930/IMP5_COST.md`, `tests/test_cost_rollup.py`. Status: PROVEN.
- **Doctor** (`mag/doctor.py`, `mag.cmd doctor`): independent config/cost/env sanity check run before dispatch. Live evidence it tells the truth: `watch/inbox/last_mile_20260930/AA4_DOCTOR.md` — reported DEGRADED with the exact phantom (container-namespace pid not visible to host probe) and a dead gate (refold_gate) rather than a false green. Status: PROVEN.

---

## 7. THE QUEUE/DISCIPLINE ORGANS — PROVEN

- **Watch inbox:** the single shared landing zone every surface reads first; INDEX.json derived from an append-only event log (Ethereum fold pattern), contract in `watch/inbox/SHARED_SURFACE_CONTRACT.json`, validated by `python -m mag.shared_surface validate` (AGENTS.md shared artifact boundary). All durable cross-surface work lands here; session directories are cache only.
- **STEER:** the operator's mid-flight interrupt channel — one file (`watch/inbox/STEER.md`), JSONL append-only, LATEST WINS per mate, anti-forgery via the `via` field (hand-edit | hermes-dm | phone-relay; anything else renders a row a PROPOSAL, not an order). Spec: `watch/inbox/operator_model/STEER.md`; live reader `tools/steer_read.py` + `tests/test_steer.py` (9 passed); receipt `watch/inbox/W3W_STEER_LIVE.md`. A steer row beats static doctrine but can never self-authorize irreversible effects. The leave dispatcher injects the operative row into every mission pack (organ 2).
- **Corr-ids (AH14):** `corr_id = uuid4().hex[:8]` minted per lane, carried in `MAG_CORR_ID`, stamped on all three provenance writers — trajectory steps (`mag/trajectory_step.py`), game-flow burns (`mag/game_flow.py`), duel rows (`tools/duel_harness.py`) — deliberately outside the step-hash basis so old rows verify identically. Source: `watch/inbox/last_mile_20260930/AH14_CORR_ID.md`; tests `tests/test_corr_id_ah14.py` (19 passed across four files at landing).
- **Drop ledger (dead drops):** `memory/dead_drops/` — 537 `dd-*.json` drops (byte-counted), each `{drop_id, ts, domain, mode, flock_rule, targets, instruction}`: instructions dropped for flock versions to claim (e.g. "hold the invariants: the chain is the line we sign"). Writers/consumers: `mag/grok_brief.py` (briefs dropped as dead-drops), swarm_control dead_drop, `mag/hour_test.py` counts them; `tests/test_dead_hand.py` covers the companion watchdog. Adjacent queue-discipline organ: the zombie-enqueue census + graveyard (`tools/enqueue_law.py`; epitaphs in `memory/game/GRAVEYARD.jsonl`) — buries enqueues that re-promise dead modules.

---

## 8. THE COMPUTE LADDER LAW + WINDOW LAWS — PROVEN (measured)

- **Funding truth (2026-09-28, code-as-law):** ONLY Hermes/Nous is funded ($180 credits: glm-5.3-prime / qwen3.8-max-prime = workhorse + judgment); Anthropic keys in .env are UNFUNDED (no Opus rung); free stealth lanes are a SENSING surface only — outputs banked as findings, verification climbs to the funded tier; "before building any mechanism, read the ribs and the current state." Source: `memory/rib/RIB_DRIVING_LADDER_20260928.md` (supersedes the older tier ladder in AGENTS.md).
- **Measured width envelope:** Task agents clean at 3/6/10/12 (109.4M tok/h at width 10, zero terminal 1302s); 15–16 untested; workflow children ride retry (a 429/1302 is a HOLD, not a loss); 50 concurrent workflow children (5 gated workflows × max_concurrency 10) + hourly burn cron ran hours-clean before the FIRST rate-limit contact — held at width by operator order. Sources: `watch/inbox/WIDTH_LEDGER_20260926.md`, `watch/inbox/ENVELOPE_50W_HIT_20260926.md`, `watch/inbox/ENVELOPE_LAW_20260926.md`; standing law in AGENTS.md §Max-concurrency.
- **Mate concurrency law:** never more than ~12–16 SIMULTANEOUS; up to 24 via staggered admission; a 19–20 simultaneous burst = 1302 deaths. Source: `watch/inbox/mates_leave_protocol/REGISTER_NOTE.md` + enforced as the hard cap in `configs/mates.yaml` / `tools/leave_dispatcher.py`.
- **Paid-ask gate:** paid asks never fire unilaterally — operator GO required (the AA1 law, `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md` §Gates; the Opus lensing this dossier feeds rides that gate).

---

## The one-paragraph carrier truth

The sherpa is real and mostly load-bearing: the verkle chain appends (8,670 leaves), the stealth driver cycles (heartbeat live), the duel ledger grows (73 rows), the steer channel reads, the meters run and report their own degradation honestly, and the compute laws are measured, not vibes. Its honest thin spots, already named by the estate's own instruments: the mates' first 08:00 fire failed at the mate-model auth layer (machinery green, execution red); the GPS ledger has no live production traffic (test-double); the return leg gwap→gps is unwired in production (`watch/inbox/TIE_IT_ALL_20260930.md` §3); the JetBrains and phone-body seats are plans, not organs. Nothing here is claimed beyond its receipt.
