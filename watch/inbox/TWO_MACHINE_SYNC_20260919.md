# TWO MACHINE SYNC (fostertron Drive) — filed 2026-09-19

**Decision:** whole-folder Google Drive sync (fostertron@gmail.com) is the transport between this host and the laptop. GitHub private repo was evaluated and rejected as the primary bridge.

**Why not GitHub first:** this repo carries 54 blobs over GitHub's hard 100 MB limit (biggest: `dashboard/data/ractor_board.jsonl.runaway-evidence-20260903` at 2.2 GB). The fat is partly durability by design: Mr Pool media lives in `watch/inbox/`, training ledgers append forever (`training/events.jsonl` has 29 historical versions over 100 MB). Pushing to GitHub would require history surgery, and rewriting history falsifies the commit hashes the fleet files as provenance receipts. Drive does not care about file size, and syncing the folder including `.git` gives both machines byte-identical history and hashes.

## REVISED same evening: warmed-RIB port supersedes whole-folder sync

The operator challenged the whole-folder plan and the full tree audit proves him right. The portable unit of this fleet is the warmed RIB (frozen kernel + tier packs + Librarian imprint + kifu ledgers), and it weighs about **4,000 files under 0.1 GB**. The other 1.19M files are debris (about 917k: `.mimosa` machinery 390,679 files, the knot store plus its two backups plus ghost 441,558, runs/agent_state/logs exhaust ~95k) and ore (about 196k: vendored repos, corpora, Mr Pool media, dashboard fat, git history). See THE MAP below.

New decision: the laptop receives the **travel kit** (tier 1 of the map: code, live ledgers, packs/imprint, `.env`). A cold machine boots the fleet from packs and answers from the imprint; raw artifacts stay archived on this machine and travel by bounded pointer (path + hash) only when a receipt needs checking against source. That is already the shared-surface contract's own rule. Transport becomes trivial: a git remote, a Drive folder, or a USB stick all carry a 4k-file kit. The whole-folder Drive sync below becomes the fallback for making a machine byte-identical, not the plan. Debris cleanup is operator-gated: `memory/biography` is the live record and stays; the two `biography_backup` dirs (256,996 files) are compress-to-archive candidates; `memory/ghost` and `.mimosa` await a keep/drop ruling.

## The contract (both machines)

1. **One machine live at a time.** Never run the fleet (dashboard/lab, lane runners, improve tasks) on both machines at once. Drive cannot merge two writers, and nothing can merge two `.git` dirs.
2. **Before switching:** commit the live branch, close editors and dashboard, wait until Drive reports fully synced.
3. **On the receiving machine:** wait for the full sync to finish before opening anything. Do not boot the fleet while the tree is still downloading.
4. **First boot on the laptop:** run `git worktree prune` (worktrees registered with the other host's absolute paths dangle), then rebuild the venv with `powershell -ExecutionPolicy Bypass -File .\scripts\ensure_venv.ps1` (venv binaries embed the old machine's paths), then `mag.cmd doctor`.
5. The `local` remote (`...\Mag-backup.git`) is host-local by design. Ignore it on the laptop or repoint it at a laptop-local bare.
6. `.env` is gitignored and travels through Drive as a plain file. That is the point (keys stay working), and also the exposure: anyone with the Drive account sees it. Keep the account tight.

## Host setup (this machine, one time)

1. Install Google Drive for desktop, sign in as fostertron@gmail.com, mirror My Drive to local disk.
2. Stop the fleet (dashboard/lab, lane runners). Move the repo into the mirrored My Drive tree, e.g. `C:\Users\foste\GoogleDrive\projects\local_sovereign_agent` (same volume, instant rename). Do not copy while processes hold files open.
3. Recreate the old path as a junction so every existing absolute path keeps working:
   `cmd /c mklink /J "C:\Users\foste\Documents\projects\local_sovereign_agent" "<MyDrive>\projects\local_sovereign_agent"`
   The junction sits outside Drive's sync scope; Drive sees real files only.
4. Let the initial upload finish (multi-GB, one time). Verify `git status`, `mag.cmd doctor`, dashboard :8765 through the old path.

## Laptop setup (one time)

1. Install Drive for desktop, same account, mirror to local disk. Wait for the full download.
2. Archive the old laptop backup folder (rename it, do not merge). The Drive tree is now the single source of truth.
3. `git worktree prune`, rebuild venv (`ensure_venv.ps1`), `mag.cmd doctor`.

## GitHub, later, optionally

A private GitHub repo remains viable as a code-only secondary after hygiene (untrack the runaway `dashboard/data` files, strip those paths from history in a throwaway clone, push that). Do not push this repo's history to GitHub as-is; the push will be rejected and any rewrite breaks receipt hashes.

## THE MAP (2026-09-19, robocopy per dir, reconciles to 1,200,905 files / 42.6 GB)

| tier | where | files | size |
|---|---|---|---|
| **Fleet proper** (the travel kit) | mag 1,881, scripts 211, tools 48, queue 715, configs 52, docs 528, tests 275, memory live ledgers (rib 40, rib_bus 51, packs 31, knowledge_packs 9, law 11, frontier 4, percolator 10, portable_bags 186, research_packs 700, briefs digests), `.env` | ~4,000 | <0.1 GB |
| Debris: machinery | `.mimosa` | 390,679 | 4.95 GB |
| Debris: knot store + copies | memory/biography 39,492 (live record, stays), biography_backup 214,747, biography_backup_20260825 42,249, memory/ghost 145,070 | 441,558 | 0.71 GB |
| Debris: run exhaust | memory/runs 44,165, memory/agent_state 35,979, logs 4,796, memory/mail 4,562, agent_sessions 2,805, working 1,518 | ~95,000 | ~2.6 GB |
| Ore: vendored + corpora | mine/raw 103,033 (5.34 GB), corpus 54,775 (6.10 GB), memory/corpus 22,418 (0.72 GB) | 180,226 | 12.16 GB |
| Ore: media | watch (mrpool_export 2,528 files / 3.40 GB) | 16,029 | 5.29 GB |
| Ore: fat + history | dashboard data 3.32 GB in 573 files, .git 6.13 GB in 187 files | 760 | 9.45 GB |

About 79 percent of all files are debris that the fleet never reads after the run that made them. 34 empty `.pytest-*` husks from 19-day-old test runs sit at the root; this shell is denied rmdir on them, clear with an admin `rd /s /q` sweep. Already deleted this day: 2,323 `__pycache__` dirs, stray `%SystemDrive%`, `%TEMP%ssv.json`, a 1.27 GiB garbage pack.

Travel kit composition is the export contract: everything a cold machine needs to boot the fleet and answer from packs. Raw ore stays archived here and answers by bounded pointer (hash + path), which is the shared-surface contract's own rule.

- Secrets: tracked tree clean (only test fixtures and corpus noise match key shapes); `.env` untracked and gitignored.
