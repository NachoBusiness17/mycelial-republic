---
name: drift-patrol-cron-a7c71ad1
description: Daily 08:00 drift-patrol automation (automation-a7c71ad1) — 4 runs
    done; auto-pushed 7+43+14 overnight commits; fold self-heals inside patrol (root
    pinned to /board/inbox); validate baseline 107; top risk = event-path convention debt
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

ZCode automation `automation-a7c71ad1` ("Drift patrol daily 08:00 — fleet vitals, backup push, inbox fold staleness"), created 2026-09-14 at the operator's order ("do another cron job i canceled the last one" — the board was empty; don't assume older patrols exist, verify with CronList). Recurring daily 08:00 local.

Each run: (1) count unpushed commits vs remote branch `run-beta1-factory-audit-20260914` on `local` (Mag-backup.git) and push if any; (2) `docker ps` the three mag containers, `docker compose restart mag` if any down; (3) INDEX.json fold age — **now refold via `node scripts/index_fold_host.mjs rebuild` when stale** (see [[shared-inbox-index-fold-stale]]); (4) `mag.shared_surface validate` error count vs the 2026-09-14 baseline of 73; (5) `mag.link_library dupes`. Files `watch/inbox/DRIFT_PATROL_<YYYYMMDD>.md` + one register event, commits and pushes if the tree changed, reports top-3 risks boldest-first.

**Run history:**
- **Run 1, 2026-09-15** (`DRIFT_PATROL_20260915.md`, `bd1cc9c88`): all green except fold staleness. Lessons: use `"$TEMP"` not `/tmp` inside patrol scripts ([[gitbash-tmp-invisible-to-venv]]); doctor's "degraded" is a false alarm while the host integral is dead *by design* under DOCKER_ONLY.
- **Run 2, 2026-09-15** (`DRIFT_PATROL_20260915_run2.md`, `d36af8774`): caught + auto-pushed **7 unpushed overnight game commits**. Naming lesson: same-day reruns must suffix (`_run2`) — never overwrite a patrol receipt.
- **Run 3, 2026-09-16** (`DRIFT_PATROL_20260916.md`, `457ebb852`): caught + auto-pushed **43 overnight commits** (biggest night yet — night audits, syllabus batches, steals ledger 74/74, basecamp + estate catalog, 486-free-API scout, ractor salon, boss(death), the 12-item operator ask `39304cf5`). **Folded the INDEX itself** (tolerant reader → `scripts/index_fold_host.mjs`, 156 events → 140 items) — closing its own #1 risk after two runs.

**Why:** the audit's #1 risk was commits on a single disk; the patrol has now caught 50 commits across two runs that would otherwise have been single-copy. It also fixed its own top finding rather than re-reporting it.

**How to apply:** If a patrol receipt exists for today, read it instead of re-running. The validate baseline moved **73 → 107** on run 4 (73 legacy + 34 event-path convention debt) — compare against 107 until the path-normalization fix session lands. Standing top risks as of run 4: event-path convention debt is #1 (needs a normalizing fold pass or subpath-aware validator), the operator's 12-item ask awaits rulings (day 3+), two fold homes risk (inbox REVIEW artifact vs `scripts/index_fold_host.mjs`), and the netlify maze_arena fix (f81735212) still undeployed (day 4). Related: [[repo-git-hygiene-checkpoint-20260914]], [[operator-ask-20260916]], [[full-audit-20260914-findings]].
