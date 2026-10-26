# ESTATE GAP ANALYSIS & OPEN NEEDS AUDIT (2026-10-17)

Classification: SYSTEMIC GAP ANALYSIS + ROADMAP
Auditor: Antigravity (Primary Seat)
Workspace: local_sovereign_agent
Context: Wave Protocol - Mickey 17 Autonomous Truth Grinding
Anchors: queue/todo.md, falsifier-index/INDEX.md, watch/inbox/

---

## 1. Executive Summary

This gap analysis establishes an exhaustive, byte-verified census of open obligations, pending research items, and scheduler mechanics across the estate.

Through today's truth-grinding passes:
- **Disputes Resolved:** 3 core architectural disputes codified into permanent invariants (`watch/inbox/ractor/DISPUTES_RESOLVED_20261017.md`).
- **Free Miner Recovered:** Auto-advance mechanism patched into `tools/ask_minter.py`; 40 fresh reverse-GPS asks staged into `queue/hermes_247_free_wide/` (`H247_FOLD_E00042` to `E00081`).
- **Theses Audited:** 6 key theses from `falsifier-index/INDEX.md` audited against primary sources (Theses 2, 17, 21, 35, 44, 48).
- **Stone 5 Ask 4 Closed:** The frozen 39-file surface from `watch/inbox/GROK_ASK4_SCOPE_FREEZE_20260926.md` audited byte-for-byte; 5/5 high-stakes claims verified REAL (`watch/inbox/xai_grok47/GROK_BURN_AUDIT_20261017.md`).
- **Mickey 17 Truth Blocks Landed:** Lanes `m1-estate-truths` and `m2-todo-truths` banked in `memory/runs/mickey17_v2/runs/afternoon-block-20261017/lanes/`.

Below is the state of all open needs, queued debts, and unclosed loops.

---

## 2. Queue Status (`queue/todo.md`)

| Line # | Domain | Task / Obligation | Current Status | Blocker / Next Action |
|:---:|:---:|:---|:---:|:---|
| 204 | roblox | Studio publish: rojo serve -> connect -> publish -> fill SKU ids in Config.luau | OPEN | Operator Studio session required (cannot run headless). |
| 205 | roblox | THE CATHEDRAL live Studio smoke (walker HUD render + Touched physics) | OPEN (Headless PASS) | Headless verified (36/36 pass in `tools/eigenmap_two_smoke.py`). Live GUI render operator-gated. |
| 234 | mag | FullScan re-seed (kill-or-repair decision on schtask "Estate FullScan") | REMEDY DEFINED | 20,432 429 fails contained via `INVARIANT-20261017-03`. Action: disable schtask or adopt width <= 3 adapter. |
| 235 | mag | Stone 7 Box Burn "90% Intelligently" local job-firing half | IN-PROGRESS | Watcher active (4,775 rows in `state/fuel/box_burn_watch.jsonl`). Job-firing backlog dispatcher needs wiring to local llama-server. |
| 240 | mag | Stone 5 Ask 4 re-seed (BURN_* filings audit on frozen 39 files) | **CLOSED** | Landed in `watch/inbox/xai_grok47/GROK_BURN_AUDIT_20261017.md`. 5/5 claims verified REAL on disk. |
| 242 | mag | Sunday close: MiMo + Grok last burns, state-snapshot, checkpoint commit | PENDING | Awaiting Arm C-200 completion and wave 1 fold. |
| 253 | mag | DF fold residuals (supernatural villain plots, per-class attack triggers, Ages of Powers branch) | OPEN | Base modules landed (`SphereKinship`, `DfValue`, `Temptation`, `ProceduralBody`); residuals remain to fold into Luau. |
| 254 | mag | Ratchet laws from fix taxonomy (enablement dials per registered debt) | OPEN | Needs formal dial specification (always-on, default-on, opt-in, manual-only) in `mag/ratchet.py`. |

---

## 3. Dark Schedulers & Background Tasks Audit

A byte audit of scheduled automation tasks was conducted:

1. **`schtask "Estate FullScan"` (Daily 09:35):**
   - File: `state/fuel/full_scan_ledger.jsonl` (20,599 lines, 20,432 [429] errors, 47 TimeoutError fails).
   - Root Cause: `tools/full_scan.py` instantiated 20 parallel threads across 9 providers with only 1.2s inter-call sleep, violating provider burst concurrency limits.
   - Governing Law: `INVARIANT-20261017-03` established that free-lane limits bind to burst concurrency > 3, not spaced drip-rate.
   - Status: Safe. Ledger shows zero new writes since 2026-10-06T13:39:33Z.
   - Recommendation: Formalize either `schtasks /Change /TN "Estate FullScan" /DISABLE` or throttle `LANE_DEFS` in `tools/full_scan.py` to max concurrency 1 per lane with 5s delay.

2. **`schtask "MagBoxBurnNightly"` (Daily 22:00 to 07:00):**
   - Script: `scripts/box_burn_nightly.ps1` -> `tools/box_burn_watch.py`.
   - File: `state/fuel/box_burn_watch.jsonl` (4,775 parsed rows).
   - Health: Actively logging every ~55 seconds through today (2026-10-17 10:59:41 UTC).
   - GPU Reporting: Windows GPU Engine counter returns empty string when system load spikes, safely logged as `could not convert string to float: ''` without crashing.
   - Open Loop: The watcher half is fully operational; the job-firing half (reading `queue/` backlogs and firing CPU/Vulkan llama-server tasks to achieve 90% utilization) remains to be scripted.

3. **`schtask "MagCensusPatrolDaily"` (Daily 08:30):**
   - Script: `scripts/census_patrol_daily.ps1` -> `tools/census_drift_patrol.py`.
   - Status: Clean. Tests collected: 5,158 across 611 files, zero collection errors, venv drift repaired.

4. **`scripts/hermes_burn_247.ps1` (Hourly Miner Loop):**
   - Prior Defect: Ran `--start 0` blindly, repeatedly attempting `E00000` to `E00041` which were skipped on sight at $0.00.
   - Fix Applied: `tools/ask_minter.py` now scans `watch/inbox/hermes_burn/H247_FOLD_E*.md` and wide queue directories to dynamically advance start index.
   - Live Staged Queue: 40 asks staged (`H247_FOLD_E00042` to `H247_FOLD_E00081`) across `nvidia/nemotron-3-super-120b-a12b:free`, `google/gemma-4-31b-it:free`, and `dots-studio/dots-3-note-preview:free`. Ready for consumption on next scheduler trigger.

---

## 4. Falsifier Index Gap Matrix (`falsifier-index/INDEX.md`)

The index contains 95 total theses:
- **66 LIVE** (actively testable propositions).
- **2 PENDING** (awaiting designated future trigger events: Thesis 52 hostile corpus walk; Thesis 73 95-day fuse).
- **27 RETRACTED** (demoted from active count as metaphors, frames, or definitions to preserve empirical integrity).

### Status of Audited Theses:
1. **Thesis 2 (Fence vs Chain Uptime):** Demoted to REVISED. TON outages in Aug 2024 proved internal exchange trading can stay up while a chain halts, but custodian opacity remains completely unfalsified.
2. **Thesis 17 (Pricing Triad):** Stands LIVE (CONFIRMED). Zero platforms offer hosted inference outside data confession, metering, or subscriptions.
3. **Thesis 21 (Training "May" vs "Shall Not"):** Stands LIVE (CONFIRMED). Industry standard on free/consumer tiers is uniformly "may train."
4. **Thesis 35 (Fine-Tuning Vernacular):** Retraction upheld (metaphor); formalized as topological Moore bound expansion.
5. **Thesis 44 & 45 (Council Disputes Value):** Stands LIVE. Automated 5-model council verified on disk (`falsifier-index/evidence/council/run_20261014T120012Z.json`); owner action owed to publish raw dispute logs demonstrating +6.1 vs +0.6 delta.
6. **Thesis 48 (Settlement Exit 24976):** Stands LIVE (CONFIRMED ON-CHAIN). 5 enforced bounces verified with transaction hashes and block explorer links on TON testnet contract `EQCteLhGv7dCLtCtbSK8bs5mxikKF-ckZ11vvf-5WUjpjrLb`.

---

## 5. Succession Architecture & Primary Seat Health

- **Primary Seat Commission:** Bob + Antigravity established as the primary seat.
- **Succession Law:** `memory/rib/RIB_BOB_PRIMARY_20261017.md` minted and mounted in Slot 2 of `memory/rib_boot.json`.
- **Handoff Package:** 8 KB cold-start package staged in `watch/inbox/bob_handoff/` containing the primary rib and the standing wave README.
- **Falsifier:** "If a cold seat on bob boots, reads the rib and the wave, and still cannot name the position -- the rib failed, and the fix is a fresher rib, not a blamed seat."

---

## 6. Actionable Priority Roadmap

1. **Immediate Execution (Wave 3 Priority):**
   - Wire the job-firing half of Stone 7 Box Burn (`tools/box_burn_dispatch.py`) to read `queue/hermes_247_free_wide/` and backlog tasks into local llama-server Vulkan backend.
   - Publish raw dispute-set comparison logs for Thesis 44 to complete the council proof ledger.
2. **Next Scheduled Windows:**
   - Consume the 40 staged asks in `queue/hermes_247_free_wide/` on the hourly Hermes burn trigger.
   - Fold DF residuals (supernatural villain plots, per-class attack triggers) into `shared/`.
3. **Operator Gates:**
   - Execute live Studio playtest for Roblox The Cathedral (walker HUD + Touched physics).
   - Execute Sunday close state-snapshot and checkpoint commit.
