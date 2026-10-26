# CENSUS — WORKSPACE (cage side, lane 1) — 2026-09-01 14:00Z

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: cage workspace holds ~56 active tools + 27 doctrine files, and the crown-jewel Mag CLIs live host-side while the cage re-implements the same invariants (duplication-as-emphasis) — SUPPORTED (direct file-by-file inventory, 2026-09-01) · falsifier: current cage listing diverges materially (tools promoted/archived, Mag modules now present cage-side)

Scope: /root/.openclaw/workspace (17MB, excludes node_modules). This is the **OpenClaw cage (Linux)**
side of the Mag sovereign framework. The cage talks to the operator's host (Windows venv) via
FILE hooks: reads `/board` (shared bus), drops writeables in `/patches` -> `python -m mag.openclaw_patches apply`.
The host runs Mag Python modules; the cage runs these mjs Node CLIs + OpenClaw spawns.

---

## 1. TOOL INVENTORY — ACTIVE-TOOL (18 × .mjs + 12 × .py + 6 × bench + 5 × physical .js)

### Cage mjs CLIs (18) — each is a small Node script, never prints keys, writes to /board
| File | B | Purpose | Feeds |
|------|---|---------|-------|
| `cost_gate.mjs` | 2812 | Pre-dispatch cost guardrail: estimate-before-fire vs rate card; PASS/BLOCK | /board dispatch receipts |
| `ctx_watch.mjs` | 1193 | NO-SILENT-100% law executor: measures active main-session transcript MB | night_shift_ticker |
| `invariant_root.mjs` | 6029 | Rolling sha256 root + proof over invariant proposals (Exp-002b) | /board/invariants_proposals.jsonl |
| `keyshape.mjs` | 728 | Shape-checks a named /mag/.env key (no secret material printed) | env hygiene |
| `mag_api.mjs` | 1028 | One-liner Mag gateway CLI (GC call to mag-sovereign:8001) | gateway /room/thread keep |
| `memory_rib_bounds.mjs` | 1648 | Sidecar sha256 bounds for append-only tapes (idempotent) | <tape>.bounds.jsonl |
| `memory_rib_deref.mjs` | 3074 | Lossless read_archive(span); --check verifies ALL rib bounds | /board/MEMORY_RIB.jsonl |
| `memory_rib_write.mjs` | 2812 | RIB-format memory catalog writer + warmer | /board/MEMORY_RIB_CONCEPTS.json |
| `memory_riddler_sync.mjs` | 2375 | ONE-WAY mirror /board/riddler_common.jsonl -> memory/riddler_common.md | memory search surface |
| `staging/deepseek_month_analysis.mjs` | 15863 | DeepSeek monthly analysis script (staging) | sweep/campaign intel |
| `staging/corpus_tier_d/fetch.mjs` + `hash.mjs` | 409/234 | Corpus grab (browser-UA) + sha256 hash | corpus_tier_d source |
| `night_battery.mjs` | 3784 | Night Shift S1: frozen 20-probe battery on a lane, per-lane receipt | /board/lineage_genC_<lane>.md |
| `night_cache.mjs` | 4048 | Night Shift S2: cache-mining probe (bonded-prefix) | /board/night_cache_receipts.jsonl |
| `percolator.mjs` | 3607 | /keep/ board trajectory overlay; fingerprints posts | /board/percolator_out.md |
| `ponytail.mjs` | 3132 | Drain-cycle hook injector; fires organs incl FAIL reporting | state + /board/.ponytail_state.json |
| `steer.mjs` | 3374 | Operator steer queue with edit-before-read rights | /board/steers.jsonl |
| `steering_probe.mjs` | 5575 | S4: does a steering instruction survive a cached prefix? | /board/s4_steering_receipts.jsonl |
| `sweep_tail.mjs` | 2721 | Tail-seat sweep harness, lerps D toward target (STEER-001) | /board/steer_exp_001_receipts.jsonl |
| `together_battery.mjs` | 3280 | Raw-API (Together) gen-C battery, $0.05 cost gate | /board/lineage_battery_v1.json |
| `water_windows.mjs` | 5393 | Watercomputer window clock: quota/window countdowns | /board windows reservoirs |

### staging Python — Self-Steal / switchboard suite (12 .py)
| File | B | Purpose | Class |
|------|---|---------|-------|
| `switchboard.py` | 12916 | BBS-driven agent control plane + reference monitor | ACTIVE-TOOL (v1) |
| `switchboard_v2.py` | 31445 | v2 + policy enforcement + receipt chain (Track B, SELF_STEAL spec) | ACTIVE-TOOL |
| `policy_engine.py` | 16949 | MAG policy as data, authority checkpoints | ACTIVE-TOOL |
| `effect_broker.py` | 19913 | Unified effect-execution layer (all side effects routed through) | ACTIVE-TOOL |
| `harness.py` | 24001 | Integration harness wiring switchboard+broker+policy | ACTIVE-TOOL |
| `ask_router.py` | 8220 | Outcome-ledger-driven ask routing ($0 control plane) | ACTIVE-TOOL (v1) |
| `ask_router_v2.py` | 11462 | v2 + effect_broker integration | ACTIVE-TOOL |
| `swarm_cycle.py` | 8340 | Composite flywheel turn over existing organs | ACTIVE-TOOL (v1) |
| `swarm_cycle_v2.py` | 9694 | v2 + broker integration | ACTIVE-TOOL |
| `session_bridge.py` | 10236 | Cross-session relay + riddler sanitization (tree-isolated sessions) | ACTIVE-TOOL |
| `riddler_sanitize.py` | 8391 | Riddler process as sanitization engine (public-safe surrogates) | ACTIVE-TOOL |
| `test_switchboard_hypervisor.py` | 12028 | Five Hypervisor Tests acceptance runner (S3) | ACTIVE-TOOL (test) |

### bench/ (6 .js + 1 .py) — model pricing/latency harness
`analyze/client/latency/models/pricing/probe(.js/.py)/retest_refactor/run/run2/synthesize/tasks.js` + REPORT.md + results.jsonl
Class: **ACTIVE-TOOL / legacy bench** (feeds model circuit decisions; results.jsonl = 25KB receipt).

### moe/ (8 src .js + tests) — separate mixtrue-of-experts runtime proto
`prompt_compiler/orchestrator/analyzer/logger/config/client/merger/moe.js` + adapters + test. Class: ACTIVE-TOOL / fielded-sidecar (design + test).

### physical-computing/ (3 .js) — Verkle lance / knot tooling
`verkle_lance_port.js` (12.6K) Verkle chain timeline; `knot_labeler.js` (5K) + `knot_templates.js` (7K) knot templating + 2×300KB-662KB patch JSON. Class: ACTIVE-TOOL (Verkle/RIB lane).

---

## 2. DOCTRINE INVENTORY (authoritative md)
| File | B | Purpose |
|------|---|---------|
| `AGENTS.md` | 4111 | Cage workspace law + DROP WINDOW SOP (standup for this seat) |
| `TOOLS.md` | 4932 | Tool/skills cheat-sheet (camera/ssh examples → gap: mostly boilerplate) |
| `SOUL.md` / `IDENTITY.md` / `USER.md` / `PRIMER.md` / `HEARTBEAT.md` | ~3.4K | Identity + operator brief |
| `GOPHER.md` | 3314 | GOPHER law: mechanical fetch/grep/verify → DS-Flash spawns; HOT needs ≥3/4 consensus |
| `MAG_TOOL_MAP.md` | 9175 | The capability map: cage vs host, 16 crown-jewel tools |
| `MEMORY.md` | 21056 | Long-term doctrine: NO-SILENT-100%, BETTER-BY-DEFAULT, duplication=emphasis, convergence-dissection, plan-models=lanes, riddler law |

Skills dir (7 skills, SKILL.md + refs): archivist, chan, fireball-cycle, front-door, operator-corrections, quixote-planner, ractor-cast — all **ACTIVE** (loaded on demand).

---

## 3. ORPHANS + RISKS

**ORPHAN / dead-weight:**
- `memory_rib_bounds/deref/write.mjs` — RIB toolchain; **MEMORY.md says "Verkle/RIB architecture is operator's own"** but these 3 cage sidecars reference /board/MEMORY_RIB* which may be superseded by rival memory designs. Verify liveness. (class: RISK/SUSPECT-LIVE)
- `bench/` — legacy model bench (Aug 30), likely superseded by night_battery suite. Candidate archive.
- `staging/__pycache__/` — 5 stale .pyc (effect_broker/harness/policy_engine/switchboard/_v2). Regenerable, safe to prune.
- `dogfood/forensic_ledger.jsonl` — one-off probe output.
- `sweeps/` + `xauth/` — z.ai sweeps (devpack/pricing), OAuth pkce.json; research scratch, low re-use.
- `moe/`.` — separate runtime (DS v4 era), fielded but uncoupled to the newer self_steal suite; candidate merge/archive.

**RISK:**
- `memory/2026-09-01-0555_secrets.md` (1131B) — filename says SECRETS inside a mirrored memory dir. Verify sanitization / cage isolation; riddler law says bus is sanitized lane, so a secrets file in memory conflicts.
- `staging/steiniger_zenodo_21680954/` — 8MB incl 6.9MB Athena-class dataset jsonl + logos + chat exports + training py/bash. Corpus/download artifact; large; check license/redaction before promotion.
- `memory/riddler_common.md` (78KB) — generated mirror; marked "do not edit". Correct but large in memory search index.
- `openclaw-workspace-state.json` (120B) — runtime state, do not touch.

---

## 4. STAGING DISPOSITION
| Layer | Files | Verdict |
|-------|-------|---------|
| `.py` self_steal suite (12) | switchboard/v2, policy_engine, effect_broker, harness, ask_router/v2, swarm_cycle/v2, session_bridge, riddler_sanitize, test_switchboard | **PROMOTE** — proven per MEMORY.md doctrine (converged 3-lab authority architecture). Kept as ACTIVE-TOOL. |
| `.md` research briefs (16) | ARCHIVIST_DESIGN_BRIEF (dupe of skills/archivist/references/), BRIDGE_*, SWITCHBOARD_GAP, VAULT_PRICING, LANE_MAP, MONEY_MAP, GLM53/HARDWARE/PHYSICS deepdives, PLANNING_ORGANS, SELF_STEAL_MASTER_SPEC | **REFERENCE/KEEP** — feeds /board roadmaps. Duplicate ARCHIVIST_DESIGN_BRIEF → fold into skill only, keep one copy. |
| `corpus_tier_d/` | 3.6MB lessig_code_v2.pdf (4.3M) + blavatsky (2M) + bernays (227K) + fetch/hash.mjs | **KEEP as corpus** source (creative/games lane), hash-anchored |
| `steiniger_zenodo_21680954/` | Athena-class v12d dataset + 6.9M jsonl + chat exports + train script | **QUARANTINE/REVIEW** — external 8MB model-training artifact; verify provenance before any promotion |
| `__pycache__/` | 5 .pyc | **PRUNE** (regenerable) |

---

## 5. SURPRISE
`MAG_TOOL_MAP.md` (the authoritative capability doc) lists 16 crown-jewel tools as **host Python `python -m mag.*`** — but the cage census shows NONE of those Mag module CLIs are present here. The cage's real load-bearing tools are the 18 mjs + 12 py that RE-IMPLEMENT the invariants (RIB, policy, switchboard) as fork/cage-native code. i.e. the "capability list" lives on the host; the cage is a parallel re-implementation, which is exactly the "duplication is emphasis / convergence" doctrine in MEMORY.md.

---

## COUNTS
- **ACTIVE-TOOL:** 18 mjs + 12 staging py + 14 bench/ + 9 moe + 3 physical .js = **56**
- **DOCTRINE:** 11 top-level md + 9 memory/long + 7 skills = **27**
- **RECEIPT/scratch:** memory daily (~60) + bench results + sweeps + dogfood + xauth = **~70**
- **ORPHAN/RISK:** ~8 flagged (moe legacy, bench legacy, RIB sidecar liveness, secrets file, Zehnodo corpus, __pycache__)
- Total files inventoried: ~165 incl 78KB riddler mirror + 25KB results + 2 large PDFs. **0 files >2MB besides the 2 corpus PDFs + 1 dataset jsonl (noted only).**
