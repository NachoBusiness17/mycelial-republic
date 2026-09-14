# SELF-STEAL: projects-tree orphan mine (2026-09-04)

Gopher: zcode seat. Scope: `C:\Users\foste\Documents\projects` minus `local_sovereign_agent`
(already mined) and `codex_pytest_*` (another gopher). Method: triage every vein
(git logs, READMEs, file counts) -> sweep named concepts/specs/builds against live
record surfaces (watch/, memory/, docs/, mag/) -> tri-state verdicts. Read-only outside
the repo; no secrets echoed (one `.env` existence flagged, never opened).

---

## 1. TRIAGE TABLE

| Vein | What it is | Vintage | Size | Verdict |
|------|-----------|---------|------|---------|
| `Mag-backup.git` | Bare backup of Mag history; 115 commits, tip `bba1712` "flock session 2026-08-09" (agent-state routing, ghost self-heal, corpus lenses, reaper) | ends Aug 9 | 4.2M | **ABSORBED** — history is a strict prefix of live's 168 commits (same root `eb07ad6`, tip exists in live) |
| `mag-current-rebuild` | The pre-fork Mag working tree (832 mag modules, `TOOLS.md` 144KB, `agents/`, `THE_MACHINE.md`, `HANDOFF_MAG_AGENT_TODOS.md`; a `.env` EXISTS at root — flagged, not read) | Aug 4–26 | 556M | **ABSORBED (filenames)** — mag/ is a strict filename-subset of live's 895; every named top-level doc exists in live. This is the fork parent; live was born from it ~Aug 26 |
| `mag-sovereign-kit` | PUBLIC publish kit = github `NachoBusiness17/Mag` ("public practice kit for sovereign mirror + local Mag"). main Aug 1–2 + 24 remote branches (18 `cursor/*` agent experiments, 4 `mag/*` run branches, master) | Aug 1–6 | 13M | **MIXED** — 14 branch tips present in live; **11 cursor-branch tip chains MISSING from live** (see Orphan O1) |
| `mycelial-republic` | Phase-0 sovereign-mirror product path ("forest/spore"): X archive -> annotated corpora -> vector scaffold -> optional train -> spore. 13 commits incl. "Sovereign Framework opened for collaboration" (Aug 20) | Jul 15–Aug 21 | 49M | **ACTIVE-PARALLEL** — live references it as the product surface (AGENTS.md of the republic names Mag the person-scale office); NOT code-absorbed beyond framework (see Orphan O2) |
| `sovereign-mirror` (+ `worktrees/sovereign-mirror-scaffold`) | The instrument/lab repo: `src/sovereign_mirror` = EUT lattice, knot explorer, TSVF, PEPs, Ostrom, invariants, geodesics + full-stack dashboard (instrument/observatory/lattice lab) + Grok drift packs + X fetch + conversation import. main = README only; the code lives on `beta/v2` (= the scaffold worktree, port 8743) | Jul 10–19 | 538K | **KNOWN-EXTERNAL ORPHAN** — referenced as sibling instrument in live docs (`docs/ref/RUN.md`, `SOVEREIGN_STACK.md`, `strike_origin.md`); the CODE has no duplicate in live (Orphan O3) |
| `worktrees/salon-arena-mvp` | NOT an orphan vein: it is a live `git worktree` OF `local_sovereign_agent/.git` (branch salon-arena-mvp; owned by `CodexSandboxOffline` — the codex sandbox user). Full config tree (mag.yaml, lanes, providers, arena probes, constitutional rails) | Jul 10–18 | — | **LIVE-REPO WORKTREE** — excluded from orphan verdicts; noted for ownership (dubious-ownership flag on foste account) |
| `embassy-aos` | Outbound diplomatic packet to first sovereign partner AOS/AdventureNLearn: Pattern A · Option C · T1 · §6 intake, pure-stdlib integrity suite (21 tests) mapping their ARK gates onto our toolkit | Aug 22 | 231K | **ABSORBED** — live `mag/embassy_integrity.py` + `embassy_deliver.py` exist |
| `embassy-sandbox` | The embassy DM runtime: Ghost seat <-> AOS seat over durable file-bus + loopback REST, G1–G8 OPSEC quarantine, content-addressed ids, append-only ledger (9 tests) | Aug 22 | 297K | **ABSORBED-DUPLICATE** — live `mag/aos_agent.py`, `aos_bus_watcher.py`, `aos_grok.py`, `aos_live_view.py` are the evolved in-repo line |
| `azerothcore-wow` | Neutered clone stub of github `azerothcore/azerothcore-wow`: empty working tree, HEAD points at `refs/heads/.invalid`, zero objects | Sep 2 | 61K | **DEAD STUB** — the "steering-king server" never landed here; nothing to mine (see Gap G1) |
| `field-strike-the-chord` | CL4R1T4S — the leaked-system-prompt archive (elder_plinius): 25 vendor dirs (Anthropic, OpenAI, Google, Cursor, Devin, Manus, xAI...). 1 commit | Jul 31 | 2.4M | **KNOWN-EXTERNAL** — live `docs/DOCTRINE_MAP.md` names it: "Field corpus ... every vendor's system prompt (understand input before trusting output)" |
| `teach` | EMPTY directory, created TODAY 10:52 (during this mine's window) | Sep 4 | 0 | **NOOP** — no purpose on disk (see Gap G2) |
| `research` | `research/aiTruthCode/` — 195-file third-party corpus: GTC/GTR "kernel" prompts (v2–v119), Eden Protocol, 4 Horseman, "Chris Beck doctoral thesis / LAKA University" — an external eschatology-of-AI prompt corpus | Aug 9 | 9.4M | **KNOWN-EXTERNAL** — live `DOCTRINE_MAP.md`: "the deeper archive (LAKA/GTC corpus)"; also in memory/decisions_log |
| `memory` (loose top-level) | 4 stray run artifacts: `afk_autonomy_run.log` (52 lines), `grok_loop_verdict.md` (actually a JSON harness result: grok 402 balance exhausted 2026-08-09, paths point INTO local_sovereign_agent), `opencode_serialize_task.log`, `swarm_test_results.json` | Aug 9–10 | 13K | **ORPHAN STRAYS** — run outputs whose result_path already lives in live `queue/results/` (Orphan O4) |
| `scripts` (top-level) | 2 hooks: `prebuild_gate.py` (self-steal law as PreToolUse hook) + `steer_47.py` (water-integrator steering for the 4.7 dogfood) | Aug 28 | 8K | **DUPLICATE** — byte-identical to live `scripts/hooks/` (diff verified) |
| `C:\Users\foste\Documents\ai\ai-cli-main` | Snapshot (no .git) of **JD Fagan's** `ai-cli`/"Neo" repo (USER.md = JD, TensorStratum LLC): NetworkChuck-inspired multi-CLI toolkit — autonomy progression ladder (4-level), MEMORY.md discipline, remote bootstrap, neo-skills, constellation architecture, OpenClaw-as-Operator | Apr 2026 content, cloned Jul 3 | 148K+ | **EXTERNAL REFERENCE** — studied clone, not operator work; live mentions it only in `watch/MCP_AWESOME_DIGEST.md` (Orphan O5) |

### Loose receipts at tree root (identified, not deep-mined)

- `ui_*.xml` (16 files, Sep 4 08:48–10:40) — UIAutomator dumps of **`com.sovereign.pocketfleet`** (the PocketFleet Android app: model menu, New Chat, Sign in, response states). Receipts of this morning's android-emulator phone-salon session.
- `phonesalon_0*.png` (7, Sep 4 08:48–09:19) — phone-salon dogfood screenshots (z.ai chat on the phone surface).
- `farm_receipt_5554/5556.png`, `headless_receipt_01.png` (Sep 4 10:34–10:45) — android farm / headless-run receipts.
- `pocketfleet_receipt_01.png` — the app install/launch receipt.
- All are **DUPLICATES of already-carded work**: live `watch/ANDROID_EMULATOR_SELF_STEAL_20260904.md`, `watch/ANDROID_FARM_SURFACE_20260904.md`, `watch/DAY_CLOSE_20260904.md`. The raw files themselves are clutter at the projects root (outside the repo).

---

## 2. ORPHANS (tri-state, evidence, disposition)

### O1 — mag-sovereign-kit: 11 unabsorbed cursor-branch chains — **SUPPORTED**
Evidence: tip-SHA check of all 24 kit remotes vs live object store. Absorbed (tip in live): failure-kb, mag-autorun-v1, mag-v2-plan, mesh-comm-research, queue-lanes-behavioral-logging, unified-router, v3-deepseek-run, v3-swarm-vision, virtual-desk-deepseek-loop, all 4 `mag/*` + main/master. **Missing from live**: `breadcrumbs-ui-simplify`, `canvas-platform`, `dashboard-v3-base`, `deepseek-prefix-cache`, `distributed-surface-glue`, `improve-stack-integration`, `intelligent-governor-autorun`, `resume-contract-wire`, `setup-dev-environment`, `unify-mag-home`, `v3-v4-research-brief`. The `deepseek-prefix-cache` chain alone carries: "Steal ClawCodex prefix cache: byte-stable system + eco + telemetry", cloud steering protocol (bridge status/steer + AGENTS contract), seat FILE pipeline (any seat -> Verkle workday leaf), G2 remote auth for LAN dashboard writes, distributed surface glue plan.
Disposition: this is PUBLIC history on `NachoBusiness17/Mag` (cannot rot), but the bones may exceed live. One free-lane pass: `git -C mag-sovereign-kit log --stat main..origin/cursor/<each>` diffed against live equivalents; cherry-pick anything live lacks, then declare the kit a forever-fork (public face) and stop tracking absorption.

### O2 — mycelial-republic unique bones — **SUPPORTED**
Evidence: live references the republic (docs/ref/DUAL_PROGRESS_STATUS.md, PRODUCT_VISION_AUTORUN.md, mag/autopilot.py reference mirror_train) but does NOT contain: `data/annotated/mirror_train*.jsonl` (the annotated high-signal corpora, incl. lattice + x_signal variants), `scaffolds/vector_scaffold_v1.md` + `vector_scaffold_v2_hybrid.md` (THE sovereign-mirror system prompt — operator fire x Steiniger lattice, Locus rules, S_core=-8), `scaffolds/steiniger/` (CC-BY-4.0 third-party: Athena/Saelis v8, EPGI, Xylo, Valora, Lumen/Lumina, Lyra L1–L6, probes, Unsloth training scripts), `scaffolds/system_prompt*.txt`, scrum system (backlog/sprints/standup), docs/AGENCY_SHAPE.md, FOUNDING_DEBATE.md, CHORD_STRIKE_CROSS_CORPUS.md, STEINIGER_GAP_ANALYSIS.md. Its `framework/mag/` (44 modules incl. game bones) IS absorbed — all 44 filenames present in live.
Disposition: KEEP as the live product path — this is the forest to Mag's office, exactly as both AGENTS.md files say. The one steal for live's record layer: a lineage note in `docs/ref/` pointing at vector_scaffold_v2_hybrid as the canonical mirror prompt (it is currently only in memory/ingest references).

### O3 — sovereign-mirror physics instrument code — **SUPPORTED** (orphan by design, not by rot)
Evidence: live has lattice modules (knot_math, invariant_lattice, lattice_query, verkle_knot...) but NO `sovereign_mirror` package: eut_lattice, tsvf, peps, ostrom, knot_explorer, geodesic, interpret, invariants, drift dashboard, grok_client, zeitgeist methods — zero hits as code in live. Referenced as sibling instrument in live docs (RUN.md, SOVEREIGN_STACK.md) and in the republic's README ("Related instrument: worktrees/sovereign-mirror-scaffold").
Disposition: KEEP EXTERNAL — two-doors doctrine (office vs instrument). Risk to watch: it is a 538K repo whose only working copy of beta/v2 is a worktree; the bare `main` holds just a README. If the instrument matters to the mirror roadmap, snapshot the beta/v2 branch (it is safe in git; the worktree is the live checkout).

### O4 — loose top-level `memory/` strays — **SUPPORTED**
Evidence: 4 files whose own paths point into local_sovereign_agent (grok 402 harness result names `queue/results/20260809-203619-harness.json` inside live). Live `memory/runs/` is the canonical home and does not contain these 4.
Disposition: sweep into live `memory/runs/orphan_strays_20260809/` for the record (they document grok-balance exhaustion + afk autonomy attempt of Aug 9), then delete the loose dir. Zero judgment content — pure run exhaust.

### O5 — ai-cli-main (JD Fagan's "Neo") as named vein — **UNPROVEN intent, SUPPORTED content-identity**
Evidence: USER.md names JD Fagan / TensorStratum; no .git; content vintage Apr 2026, cloned Jul 3. It is NOT operator work. The interesting bones for the fleet: autonomy-progression-ladder (4-level, per-workflow, with promotion/demotion mechanics — predates and parallels our lane/trust thinking), cross-session inbox handoff pattern, MEMORY.md discipline at 12-repo scale, skills-architecture survey (32+ tools, ~2K skills).
Disposition: treat as a reference shelf, same class as field-strike-the-chord. The autonomy ladder is the one steal-worthy bone for `docs/ref/` if trust-tiering ever gets formalized; otherwise leave untouched.

### O6 — Mag-backup.git / mag-current-rebuild retirement — **SUPPORTED (absorbed), one UNPROVEN residue**
Evidence: backup history = strict prefix of live (115 < 168 commits, same root); rebuild's mag/ filename-subset of live; rebuild's named docs (TOOLS.md, THE_MACHINE.md, HANDOFF_MAG_AGENT_TODOS.md) all exist in live. UNPROVEN: content-level drift — filenames matching does not prove the pre-fork file contents were all carried (no byte-diff performed; 832 files x live churn makes it a real but bounded pass).
Disposition: per SACRED COWS law — these are prior drafts of the brain, already reinterpreted (live IS the successor with strictly more modules and history). Byte-diff rebuild/mag vs live/mag on one free lane; anything live lacks gets cherry-picked; then retire both (backup.git can be cold-stored; rebuild contains a live `.env` — secure-delete it on retirement, never echo).

---

## 3. DUPLICATES (present in live record surfaces — no action beyond hygiene)

| Item | Live surface that covers it |
|------|---------------------------|
| `Mag-backup.git` full history | live git history (strict superset) |
| `mag-current-rebuild` mag/ + docs | live mag/ (895 > 832, superset) + TOOLS.md/THE_MACHINE.md/HANDOFF_MAG_AGENT_TODOS.md |
| `embassy-aos` integrity suite | live `mag/embassy_integrity.py`, `mag/embassy_deliver.py` |
| `embassy-sandbox` DM channel | live `mag/aos_agent.py`, `aos_bus_watcher.py`, `aos_grok.py`, `aos_live_view.py` |
| top-level `scripts/hooks/*` | byte-identical to live `scripts/hooks/` |
| `mycelial-republic/framework/mag/` (44 modules) | all 44 filenames in live mag/ |
| ui XMLs + phonesalon/farm/headless/pocketfleet PNGs | live watch/ANDROID_EMULATOR_SELF_STEAL_20260904.md + ANDROID_FARM_SURFACE_20260904.md + DAY_CLOSE_20260904.md (today's cards) |
| `field-strike-the-chord`, `research/aiTruthCode` | live docs/DOCTRINE_MAP.md names both as field corpus / deeper archive |

## 4. GAPS

- **G1 — azerothcore-wow is an empty stub.** The briefing expected "the steering-king server — its config/scripts"; there are none (invalid HEAD, zero objects, zero worktree files, origin = upstream azerothcore). Either the server build landed elsewhere (docker volume / another host) or it was an aborted clone Sep 2 23:25. Needs one operator sentence to close.
- **G2 — `teach/` is an empty dir created 2026-09-04 10:52**, mid-mine window. Some seat/build scaffolded it this morning with no content yet. Not hostile, just unowned — whoever spawned it should either fill or remove it.
- **G3 — worktrees/salon-arena-mvp is owned by `CodexSandboxOffline`**, not foste — git flags dubious-ownership on every foster-side operation. If the codex sandbox is retired (VS Code seat cleanup arc), that worktree needs an ownership fix or removal or it will jam future git operations from the foster account.
- **G4 — sovereign-mirror beta/v2 has no non-worktree checkout** and the worktree carries a `.env` (XAI key ref, existence only). Cheap insurance: bare-clone the branch into Mag-backup-style cold storage.

---

**State of the watch:** tree triaged, 13 veins + 2 worktrees + receipts identified; 6 orphan claims filed tri-state; the two prior drafts of the brain (backup.git, current-rebuild) verified as absorbed at history/filename level with one bounded byte-diff left as the retirement gate. Card: this file. Gopher: zcode seat.
