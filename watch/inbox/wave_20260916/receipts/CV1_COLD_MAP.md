# CV1 COLD MAP — wave 2026-09-16

- Operator: **coldest vertexes** — map the coldest, least-owned corners of the estate.
- Lane law: audit/census ONLY. Git READ-ONLY commands (`branch/log/status/diff/ls-files/worktree list`). No mutations to repo or git state. Receipt filed FIRST, appended as findings land.
- Machine: Windows Git Bash, repo `C:\Users\foste\Documents\projects\local_sovereign_agent`.

## Scope
1. **Branches** — enumerate every branch: last-commit date, ahead/behind vs HEAD → ALIVE / ATARI (stale but referenced) / DEAD candidates.
2. **Worktrees** — `git worktree list`, sovereign-mirror-scaffold check, what lives there + last touch.
3. **Files** — 50 oldest-tracked files (last-commit date) + zero-import grep sample; untracked no-man's-land (top-level outside `watch/inbox` never committed).
4. **Receipts/drafts** — orphaned drafts dirs, %TEMP% clones referenced in tonight's receipts (dtm-replication), stale bak/tmp copies.

Per item: path/branch → last touch → owned-by-anyone? → verdict **REVIVE / ARCHIVE (hash+park) / VOID (flag only)**.

## Findings

### 1. BRANCHES — 35 local branches + HEAD (HEAD = 75c030d29 on `mag/run-beta1-factory-build-audi-20260806T231709Z`, 2026-09-16 17:57)

Meter ran: `.venv/Scripts/python.exe mag/git_divergence.py` (v2, self-declared read-only, base=master, DEAD=42d). Census `{'ATARI': 12, 'DEAD': 12, 'ALIVE': 11}`. **Content census refines it** (unique commits vs HEAD via `git rev-list --left-right --count HEAD...branch`); meter's "ALIVE" labels on 41-day-old zero-unique branches are a 42d threshold artifact.

**ATARI — carries UNIQUE unmerged work (14 branches, 1 shared tip pair):**

| Branch | Last commit | Unique commits | Owned by anyone? | Verdict |
|---|---|---|---|---|
| `cursor/breadcrumbs-ui-simplify-e2ce` | 2026-08-04 | **17** | NO — no remote, no worktree | **REVIVE/salvage** |
| `cursor/intelligent-governor-autorun-e2ce` | 2026-08-04 | **16** | NO | **REVIVE/salvage** |
| `cursor/unify-mag-home-e2ce` + `unify-mag-home` (same tip 7f15f27b5) | 2026-08-06 | 13 (duplicated branch name) | NO | **ARCHIVE** (dedupe: keep one name) |
| `cursor/deepseek-prefix-cache-e2ce` | 2026-08-04 | 10 | NO | ARCHIVE |
| `cursor/distributed-surface-glue-e2ce` | 2026-08-04 | 7 | NO | ARCHIVE |
| `cursor/dashboard-v3-base-e2ce` | 2026-08-05 | 5 | checked out in PRUNABLE worktree `mag_env_dashboard_v3` | ARCHIVE (push first) |
| `cursor/canvas-platform-e2ce` | 2026-08-05 | 3 | NO | ARCHIVE |
| `cursor/improve-stack-integration-468b` | 2026-08-05 | 2 | NO | ARCHIVE |
| `cursor/setup-dev-environment-6b0b` | 2026-08-04 | 2 | NO | ARCHIVE |
| `cursor/v3-v4-research-brief-e2ce` | 2026-08-05 | 2 | NO | ARCHIVE |
| `env-test` | 2026-08-04 | 2 | NO | ARCHIVE |
| `cursor/queue-lanes-behavioral-logging` | 2026-08-04 | 1 | NO | ARCHIVE |
| `cursor/resume-contract-wire-e2ce` | 2026-08-04 | 1 | NO | ARCHIVE |
| `archive/swarm-meta-2026-08-07` | 2026-08-07 | 1 | designated archive branch — that IS its job | KEEP |

**DEAD candidates — fully merged, 0 unique commits (deletable after backup; 20 branches):** `main`, `master`, `codex/salon-arena-mvp`, `cursor/conductor-loop-epic-split` (=old `main` tip 5d20144e1), `cursor/unified-router-e2ce`, `cursor/failure-kb-e2ce`, `cursor/mag-autorun-v1-e2ce`, `cursor/mag-v2-plan-e2ce`, `cursor/mesh-comm-research-e2ce`, `cursor/v3-deepseek-run-e2ce`, `cursor/v3-swarm-vision-e2ce`, `cursor/virtual-desk-deepseek-loop-e2ce`, `mag/integration-cheap-handoff-20260806`, 5× `mag/roadmap-v5-*-probe-*`, `mag/run-beta1-factory-build-audi-20260806T004024Z`, `mag/run-beta1-factory-build-audi-20260806T004214Z`. All last touched 2026-08-04→08-06 (~42d).

**ALIVE:** HEAD branch only. **⚠ BACKUP GAP:** remote `local` → `C:\Users\foste\Documents\projects\Mag-backup.git` carries **only 2 branches** (231709Z @ bba171296 = Aug 9, and `run-beta1-factory-audit-20260914` @ 457ebb852 = today). The working branch is **198 commits ahead of its backup**; **40+ branches (incl. all cursor/* unique work above) exist in exactly ONE copy** — this `.git`. Single-point-of-failure on the whole Cursor-cloud era.

### 2. WORKTREES — 8 registered + 1 unregistered sibling

| Worktree | HEAD / branch | Last touch | State | Verdict |
|---|---|---|---|---|
| main (`local_sovereign_agent`) | 75c030d29, 231709Z | today | dirty (24 entries: trails/lanes + wave receipts) | ALIVE |
| `~/.codex/worktrees/6654`, `b13a`, `ef82`, `efa1` (4×) | detached @ a4733004a (Aug 6) | Aug 6 | clean, 0 edits, 0 divergence | **VOID** — Codex cloud session scratch; `git worktree remove` candidates (flag only) |
| `C:\...\projects\mag_env_dashboard_v3` | cursor/dashboard-v3-base-e2ce | — | **PRUNABLE** (gitdir file points to nonexistent location) | VOID registration; branch has 5 unique commits — push before pruning |
| `C:\...\projects\mag_test_env` | unify-mag-home | — | **PRUNABLE** | VOID registration; branch has 13 unique commits |
| `C:\...\projects\worktrees\salon-arena-mvp` | codex/salon-arena-mvp (fully merged) | Aug 6 | clean | ARCHIVE |
| `C:\...\projects\worktrees\sovereign-mirror-scaffold` | **NOT this repo** — worktree of sibling `projects\sovereign-mirror`, branch `beta/v2` @ 43156dc | src Aug 5; session activity Sep 7 03:47 | **37 dirty entries: 11 modified src files** (dashboard server/static, eut_lattice, knot_explorer, protocol, 2 tests) + untracked `docs/CONSPIRACY_LATTICE_LAB.md`, `data/`, `.mimosa/` | **REVIVE** — uncommitted work, coldest owned lab |

Sovereign-mirror parent repo `main` is still at its initial commit (Jul 10) — everything lives on `beta/v2` + dirty tree.

### 3. FILES

**Cold cohort (tracked):** 254 files last touched in one commit — `eb07ad62e` "Mag sovereign agent — clean publish baseline." (2026-08-04), of which 108 `.py`. Zero-import grep verification of sample:

| Sample | Referenced by | Verdict |
|---|---|---|
| `agents/{planner,critic,executor,wait_human,escalate_grok}.py` | ONLY `graph.py`; `graph.py` only by `main.py:43` (lazy `run` path) — fossil LangGraph skeleton, zero-import from live product | ARCHIVE (still owned by `mag.cmd run`) |
| `backend/` (provider_gateway) | only `tests/test_provider_gateway.py` | ATARI — cold but owned |
| `dashboard/static/_build_cli_desk.py`, `_restore_cli_desk.py` | no imports; owned as TOOLs by `watch/inbox/static_rebuild/LANE_A_classification.md` | KEEP (owned) |
| `configs/lanes_vast_rtx8000.yaml` | 1 ref | ARCHIVE |
| `configs/{blast,features,data_tiers,constitutional_rails}` | 93/108/2/3 refs — runtime-loaded | cold but ALIVE |
| `docs/archive/*`, `docs/ref/*` old sheets | docs — zero-import by nature | KEEP (filed) |
| tracked `_gl_block.tmp`, `dashboard/static/_frag_extract.tmp` | recent (Sep 12), owned by static work | KEEP |

**Untracked no-man's-land (top-level outside `watch/inbox`):**

| Item | Size / last touch | Owner | Verdict |
|---|---|---|---|
| `%SystemDrive%/` (literal dir w/ `ProgramData` inside) | 932K, Sep 2 | NOBODY — botched env-var expansion | **VOID** |
| `.pytest-*` root dirs ×35 (`ghost`, `law-isolate-1..6`, `full-next-15..22`…) | ~empty, Aug 30 | NOBODY — test-isolation residue | VOID |
| `agents/pytest-tmp-*` ×**1331** dirs | 15M, regenerated **today 17:56** by suite `tmp_path` | the test suite (active producer) | VOID residue — purgeable, will regrow; flag only |
| `config.py.bak-eyemig` (Sep 7), `docker-compose.yml.bak-eyemig` (Sep 7), `docker-compose.yml.bak-openclaw-retire` (Sep 9) | 9–12K each | migration events, superseded | **ARCHIVE** (hash + park) |
| `_archaeology_out/` (mag-disk zips: nacho-archaeology parts 8–10, mag-disk-20260905) | **160M**, Sep 5 | archaeology lane output | ARCHIVE (hash + park) |
| `state/` | 40M, heartbeat **today** | runtime (worker_heartbeat, shared_activity) | ALIVE — untracked by design, keep |
| `_brief_run.log` (Aug 14), `_gen_module_map.log` (Aug 15) | ≤8K | one-shot run logs | VOID |
| `_deck_verify.js` | Sep 16 17:27 | today's CV5/command-deck lane | ALIVE |
| `.mag_active_auth`, `.env` | — | auth/secret state | KEEP untracked |

### 4. RECEIPTS / DRAFTS / TEMP

- **`%TEMP%\dtm-replication`** (`C:\Users\foste\AppData\Local\Temp\dtm-replication`): 356M, cloned **today 14:07** — read-only shallow clone of public `pschilliOrange/dtm-replication` @ 7c22d19 (upstream tip 2025-10-29) by **C15 Extropic Lane-1**, per `watch/inbox/physical_computing/receipts/C15_LANE1_CSV_ESS_AUDIT.md` ("Lane 2 may reuse the %TEMP% clone") + `C15_EXTROPIC_REPLICATION_DESIGN.md`. Clean, 0 local edits. **OWNED, ACTIVE — not cold.** Volatility is by-design (re-clone = one command); no action.
- No orphaned `drafts/` dirs found in-repo; the only draft-like swarm is `agents/pytest-tmp-*` (above).
- `watch/inbox/wave_20260916/receipts/.dc*.json` / `.z*.json` (6 dotfiles, today 13:50–13:52) — driver session droppings. VOID (flag only).
- Sibling estate (outside repo boundary, flagged only): `projects\AGENTS.md.bak-bootapply-20260911`, `projects\mag-sovereign-kit`, `projects\sovereign-mirror`, `projects\ractor-salon`, `projects\codex_pytest_{desk,factory, factory2-4,tier_gate2-4,tmp}` ×10.

---

## COLD MAP — ranked by coldness

1. **Backup gap (structural, coldest *risk*)** — 40+ branches + 198 unreached commits exist in ONE copy (`local_sovereign_agent\.git`); `Mag-backup.git` holds only 2 branches, main line 5 weeks stale.
2. **`sovereign-mirror-scaffold` worktree** — 11 modified src files + `CONSPIRACY_LATTICE_LAB.md` uncommitted since Aug 5; parent repo main frozen at initial commit. Coldest *owned work*.
3. **`cursor/breadcrumbs-ui-simplify-e2ce`** — 17 unique commits, Aug 4, no remote, no worktree.
4. `cursor/intelligent-governor-autorun-e2ce` — 16 unique commits, same exposure.
5. `%SystemDrive%/` + 35× `.pytest-*` root residue (Aug 30) — ownerless junk.
6. 4× `~/.codex/worktrees` detached scratch + 2 prunable registrations.
7. `agents/pytest-tmp-*` ×1331 (15M) — actively regenerated residue.
8. Migration baks ×3 + `_archaeology_out/` (160M) — parkable.
9. 20 fully-merged DEAD branch pointers + `main`/`master` fossils.
10. `_brief_run.log`, `_gen_module_map.log`, wave-receipt dotfiles.

**Verdict counts:** REVIVE **3** (sovereign-mirror dirty worktree; breadcrumbs salvage; governor-autorun salvage — plus the structural "push the backup" action) · ARCHIVE **~40** (13 unique-work branches + 20 merged branch pointers + salon worktree + 3 baks + `_archaeology_out` + fossil agents/ skeleton) · VOID **~1,380** (1331 pytest-tmp + 35 .pytest-* + 4 codex worktrees + 2 prunable registrations + %SystemDrive% + logs + dotfiles) · KEEP/ALIVE (not cold): dtm-replication clone, `state/`, `_deck_verify.js`, archive/swarm-meta branch, configs cold-but-live.

**3 coldest items worth reviving first:**
1. **Push everything to `Mag-backup.git`** — one `git push local --all` (when mutation is allowed) erases the single-copy risk for all 40+ branches and the 198-commit staleness. Highest value per byte of effort.
2. **`sovereign-mirror-scaffold`** — commit or fold the 11 dirty src files + `CONSPIRACY_LATTICE_LAB.md` on `beta/v2` (sibling estate; a week of EUT-lattice/dashboard work one disk fault from zero).
3. **`cursor/breadcrumbs-ui-simplify-e2ce` (+ `intelligent-governor-autorun-e2ce`)** — the two biggest unmerged commit hoards (17+16); either cherry-pick the live pieces into the main line or tag-and-park them on the backup before any branch cleanup.

**Lane law honored:** zero mutations (no branch/worktree/file changes; only this receipt + git read-only commands). `git_divergence.py` confirmed read-only before running.
