# Estate Systems Check and Full-Depth Orphan Audit

**Timestamp:** 2026-10-18T15:00:00Z  
**Author:** Antigravity Primary (Bob Seat)  
**Classification:** ESTATE HEALTH & STRUCTURAL INTEGRITY AUDIT  
**Audit Scope:** Extended Surfaces (`queue/`, `bridge/`), Inbox Root, Subdirectories, Config Seal, Claim Drift Patrol, and Living Test Suites  
**House Law Compliance:** Strictly zero unicode em-dashes (`--` and `-` only); monotonic ledger integration.

---

## 1. Executive Status Dashboard

A full-depth structural audit of the `local_sovereign_agent` estate was executed following the completion of ORG SYSTEM V2 (Pours 1-5) and the Archival / RefreshBot invariant percolation.

| Subsystem | Audit Status | Live Measurement | Detail / Action |
| :--- | :--- | :--- | :--- |
| **Inbox Top Level** | **PRISTINE** | 0 root orphans | Every single top-level file in `watch/inbox/` is indexed in `INDEX.json`. |
| **Extended Surfaces** | **COMPLIANT** | `queue_ok=True`, `bridge_ok=True` | `queue/` (`handoff`, `lanes`, `results`) and `bridge/` (`inbox`, `outboxes`) fully verified. |
| **Handoff Integrity** | **PASS** | 42 scanned, 0 violations | 36 grandfathered pre-widening rows, 0 non-compliant rows (Falsifier F4). |
| **Root %TEMP%* Fossils** | **CLEAN** | 0 root fossils | 39 fossils quarantined to `watch/inbox/quarantine_temp_fossils/`. |
| **Config Register Seal** | **SEALED (72/72)** | `modified=0, unsealed=0` | All 72 configuration files verified byte-identical to `configs/.config_seal.json`. |
| **Promotion Ledger** | **ACTIVE** | 5 rows banked | Minted under `promotion.v1` schema; verified by `mag/contract_widening.py`. |
| **Test Suites** | **100% PASS** | 54/54 tests green | `test_shared_surface.py` (38), `test_contract_widening.py` (4), `test_root_temp_sweep_patrol.py` (2), `test_archive_guard.py` (10). |
| **House Skills Lint** | **0 ERRORS** | 77 skills scanned | 0 house errors across all skills, including the 12 newly installed archival skills. |
| **Subdirectory Backlog** | **CLASSIFIED** | 19,750 unindexed files | Nested historical batch runs and hook caches categorized below. |

---

## 2. Full-Depth Orphan Analysis (`tools/surface_orphan_walk.py`)

The full-depth recursive orphan walk (`tools/surface_orphan_walk.py`) audited 23,990+ files across the estate.

### 2.1 Top-Level Surface
- **Root Orphan Count:** **0**
- Every file sitting directly in `watch/inbox/` has an active entry in `INDEX.json` and a corresponding event in `index_events.jsonl`.
- Control files (`INDEX.json`, `INDEX.md`, `SHARED_SURFACE_CONTRACT.json`) are correctly recognized as discovery pointers, not payload.

### 2.2 Subdirectory Distribution (Top 20 Clusters)

The 19,750 unindexed files are strictly confined to nested subdirectories from historical operations, model evaluations, and hook caches:

| Directory | Orphan Count | Origin & Payload Category | Proposed Governance |
| :--- | :--- | :--- | :--- |
| `watch/inbox/qdrop_export/` | 4,979 | Historical Q-drop crawl exports | Retain in place as cold research corpus; do not pollute primary index fold. |
| `watch/inbox/mrpool_export/` | 2,856 | Historical MrPool financial / prophecy crawl | Retain in place as cold research corpus. |
| `watch/inbox/.mimosa/` | 1,597 | Finding ledger events and session hook state | Ephemeral execution cache; candidate for archival via `archive_guard.py`. |
| `watch/inbox/model_garden/` | 1,434 | HuggingFace / local model metadata and specs | Static reference cache. |
| `watch/inbox/gala_20260925/` | 1,373 | Gala burn run artifacts (Sept 2026) | Historical run directory; completed and sealed. |
| `watch/inbox/burn_wave_20260926/` | 789 | Burn wave run artifacts (Sept 2026) | Historical run directory; completed and sealed. |
| `watch/inbox/hermes_burn/` | 661 | Hermes model execution trails | Historical run directory. |
| `watch/inbox/playground/` | 570 | Scratchpad and exploratory files | Semi-active workspace files. |
| `watch/inbox/frontier_olm_adhoc/` | 540 | Ad-hoc frontier model sweeps | Historical run directory. |
| `watch/inbox/burn_reset_20260927/` | 391 | Burn reset run artifacts | Historical run directory. |
| `watch/inbox/frontier_olm_2026-10-06/` | 335 | Daily frontier scout runs | Historical daily lane. |
| `watch/inbox/mates_leave_protocol/` | 306 | Mate harness receipts and departure tokens | Historical governance receipts. |
| `watch/inbox/secret_gate_results/` | 305 | Secret gate automated test outcomes | Verification history. |
| `watch/inbox/frontier_olm_2026-10-03/` | 290 | Daily frontier scout runs | Historical daily lane. |
| `watch/inbox/last_mile_20260930/` | 224 | End-of-month delivery packages | Historical milestone release. |
| `watch/inbox/wave_20260916/` | 181 | Wave protocol runs | Historical milestone release. |
| `watch/inbox/tortoise_wow_backend_20261010/` | 158 | Local TTS / audio backend artifacts | Subsystem prototype. |
| `watch/inbox/gstd_perimeter_build_20261010/` | 140 | Perimeter build test outputs | Historical security build. |
| `watch/inbox/ractor_engine/` | 98 | Singing network and interaction files | Subsystem prototype. |
| `watch/inbox/task_bank/` | 74 | Longitudinal benchmark prompts | Benchmark evaluation fixtures. |

**Governance Conclusion:** The 19,750 files are NOT active operational drift; they are cold run logs, export caches, and historical burn archives. Per B2-338 and Organ 4 law, they are surfaced as non-blocking `WARNING` entries so that active operational alerts remain loud and visible.

---

## 3. Extended Surfaces & Contract Widening (`mag/contract_widening.py`)

Organ 4 contract widening verified:
1. **Queue Surface (`queue/`):**
   - Standard subdirectories `handoff/`, `lanes/`, `results/` all exist and are healthy.
   - Handoff rows across `queue/handoff/` comply with Falsifier F4 (sha256 + receipt requirement for all rows past `WIDENING_TS_THRESHOLD`).
2. **Bridge Surface (`bridge/`):**
   - Standard subdirectories `inbox/`, `outboxes/` exist and are structured.
3. **Root Sweep Rule:**
   - Evaluated by `tools/root_temp_sweep_patrol.py`: 0 root fossils detected.
4. **Promotion Ledger:**
   - [`watch/inbox/PROMOTION_LEDGER.jsonl`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/PROMOTION_LEDGER.jsonl) active, fully schema-compliant, recording all 5 official promotions.

---

## 4. Archival and Safety Guard Health

- **Triple-Gate Protocol:** [`tools/archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tools/archive_guard.py) verified with delimiter-aware lookaround boundaries.
- **Test Integrity:** 10/10 test cases passing in [`tests/test_archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tests/test_archive_guard.py).
- **Installed Skills:** 12 skills present in [`.agents/skills/`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/), linted with 0 house errors, cataloged in [`configs/skills.yaml`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/configs/skills.yaml), and sealed under `CONFIG-SEAL`.

---

## 5. System Check Verdict

The estate is in a **HEALTHY, FULLY INDEXED, AND STRUCTURALLY REINFORCED** state. Top-level drift is zero, configuration registers are sealed, test suites are 100% green, and all extended surfaces are continuously audited under automated machine checks.
