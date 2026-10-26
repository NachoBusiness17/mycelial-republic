---
name: repo-git-hygiene-checkpoint-20260914
description: 2026-09-14 hygiene line (d575bc16→9669eec5b) — ~2GB excluded then
  backup twin untracked (−4.7M lines); pushed as branch run-beta1-factory-audit-20260914
  on local Mag-backup (diverged old tip preserved, never force-push)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

Commit `d575bc16` on branch `mag/run-beta1-factory-build-audi-20260806T231709Z` ("checkpoint 2026-09-14: Zenodo 17811909 capstone mined + forge-window recovery receipt"): 29,881 files, +7.37M/−8.5K, includes `memory/corpus` (22K files, ~299MB) deliberately. Followed same night by `36ee3917b` ("feat(link_library): canonical URL registry + Rashomon elephant surface + 25-task seed") — see [[link-library-canonical-registry]]. The line advanced through `99826e153` (maze optics) and `f81735212` (maze_arena netlify fix) to `bd1cc9c88` (first drift patrol); the backup branch `run-beta1-factory-audit-20260914` is now current and the daily patrol ([[drift-patrol-cron-a7c71ad1]]) auto-pushes it, so "unpushed" should normally read 0. `core.longpaths` set true (Windows path-limit fix).

.gitignore now excludes (all still on disk, unprotected by git): `*.log`, `node_modules/`, `corpus/oral_history/` (1.4GB archive), `corpus/library/` (6 embedded clones: anthropic-courses, hf-agents-course, human-atlas, ms-agents-beginners, ms-genai-beginners, openai-cookbook), `watch/organs/kimodo/` (7th clone), `watch/bay/logs/`, `memory/corpus/shadertoy21k/all_codes.zip`, `_archaeology_out/`, `.zcode/`, `.claude/`, `.mimosa/`, `.obsidian/`, `.mag_active_auth`, `%SystemDrive%/`, `watch/*.log`, `.pytest-*/`.

**Why:** A blind `git add -A` swept ~2GB of junk; embedded clones staged as broken zero-hash gitlinks — 100% of the bloat, 0% of the backup. A 258MB `watch/engine_e1.log` + 133MB churn/bay logs would have poisoned every future commit. Repo convention is `checkpoint <date>: <desc>` messages.

**How to apply:** Before committing, group untracked files first (`git status --porcelain | grep '^??'`) and check for nested `.git` dirs; commit breadth but never logs/node_modules/clones, and report exclusions. Open decisions: vendor the 7 embedded clones (strip their `.git`) or leave re-downloadable; give corpus/oral_history a real backup (LFS/external). If a backup push is rejected non-fast-forward, push to a dated new branch — never force-push the backup. Daemon rewrites trails/lanes state continuously — a few modified files right after a commit is churn, not an error. See [[operator-saves-everything]], [[shared-inbox-index-fold-stale]].
