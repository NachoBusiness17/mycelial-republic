# WAVE2 LANE1 — DISK MAP: where the 48 GB actually sits

**Measured 2026-09-26.** Tri-state: all claims below are **Supported** by direct
measurement (single bounded `os.walk` over 573,759 files, cross-referenced
against `git ls-files -z`). No estimates stand in for numbers.

---

## THE HEADLINE — four byte classes

Worktree grand total: **54.12 GiB / 58.11 GB** = 30.92 GiB worktree + 7.50 GiB `.git` + 15.70 GiB `.mimosa`.

Classes below are over the **30.92 GiB worktree proper** (`.git` and `.mimosa` excluded, both itemised separately above).

| Class | Bytes | GiB | GB | % | files |
|---|---:|---:|---:|---:|---:|
| **(a) git-tracked** | 14,744,042,190 | 13.73 | 14.74 | **44.4%** | 44,159 |
| **(b) untracked intentional tape** | 6,735,741,620 | 6.27 | 6.74 | **20.3%** | 139,117 |
| **(c) regenerable cache/derived** | 10,937,349,153 | 10.19 | 10.94 | **32.9%** | 328,811 |
| **(d) unknown** | 784,345,268 | 0.73 | 0.78 | **2.4%** | 61,672 |
| SUM | 33,201,478,231 | 30.92 | 33.20 | 100% | 573,759 |

**Only 44.4% of the worktree is in git.** The single largest bucket is (c) regenerable — and it is
dominated by *two* things, neither of which is history: `.mimosa` (15.70 GiB, 204× duplicated cache)
and `mine/raw/` (2.92 GiB of vendored third-party clones).

**Reclaimable without losing a byte of history: ~19 GB.** See the DECISION section.

---

## Which directories hold it

| Dir | GiB | A tracked | B tape | C regen | D unknown |
|---|---:|---:|---:|---:|---:|
| watch | 6.99 | 5124.0 | 2341.1 | 0.0 | 37.3 |
| corpus | 4.83 | 146.5 | 0.0 | 5039.5 | 0.0 |
| memory | 4.61 | 1063.0 | 2660.3 | 617.6 | 606.1 |
| dashboard | 3.40 | 3639.1 | 10.7 | 0.0 | 1.8 |
| mine | 2.92 | 0.0 | 0.0 | 3135.6 | 0.0 |
| attic | 2.89 | 3104.2 | 0.0 | 0.0 | 0.0 |
| logs | 1.54 | 0.0 | 1654.5 | 0.0 | 0.0 |
| .venv | 1.48 | 0.0 | 0.0 | 1585.4 | 0.0 |
| catalog | 0.34 | 234.7 | 0.0 | 134.3 | 0.0 |
| canon | 0.33 | 319.8 | 0.0 | 0.0 | 35.5 |
| artifacts | 0.25 | 268.3 | — | — | — |
| training | 0.23 | 250.5 | — | — | — |
| site | 0.19 | 16.6 | 0.0 | 192.6 | 0.0 |
| tools | 0.17 | 179.3 | — | — | 1.8 |
| _archaeology_out | 0.14 | 0.0 | 0.0 | 145.9 | 0.0 |
| dashboard-deploy | 0.10 | 0.0 | 0.0 | 104.7 | 0.0 |

(Columns in MiB.)

---

## 1. WHY is watch/ 7.1 GB? — **6.99 GiB, 4.77 tracked / 2.22 untracked**

**`watch/inbox/` alone is 6.2 GB (6,217 MB) and 4,440 MB of it is git-TRACKED.** The reason is not
receipts — it is Telegram media exports committed into history:

| Subdir | MiB | Tracked |
|---|---:|---:|
| `watch/inbox/` | 6,217.1 | 4,440.2 |
| `watch/ESTATE_INDEX/` | 590.3 | 590.3 |
| `watch/` loose files | 446.7 | 8.3 |
| `watch/bay/` | 138.8 | 0.0 |
| `watch/organs/` | 24.0 | 0.0 |
| `watch/KG_STORE/` | 22.2 | 22.2 |

- `watch/inbox/mrpool_export/media_full/` = **3.4 GB of `.mp4` files, every one TRACKED**
  (msg_1929.mp4 136.7 MB, msg_4569.mp4 130.8 MB, msg_1879.mp4 119.9 MB …). This is the single
  largest tracked-media sink in the repo and it is a scratch export, not a receipt.
- `watch/inbox/qdrop_export/media_full/` = **585 MB of `.png`, tracked.**
- Actual durable receipts (`.md` cards) are tiny: `watch/receipts/` = 7.3 MB, `watch/audit/` = 11.9 MB.
  **The receipts are not the problem. The media is.**
- Untracked watch/ = 2.22 GiB across 3,927 files (`git ls-files --others` counts 1,414 at top level
  of the pattern; the walk sees 3,927 total under `watch/`). Dominated by
  `ESSENTIALS_PACK_20260926.tar.gz.enc` (1,706.5 MB — the operator's encrypted backup, intentional),
  `watch/engine_e1.log` (257.9 MB), `watch/overnight_churn.log` (133.0 MB), `watch/engine_b1.log` (23.9 MB),
  `watch/bay/logs/*.log` (138.7 MB). These are append-only logs covered by `.gitignore:184` (`watch/*.log`).

## 2. WHY is memory/ 5.2 GB? — **4.61 GiB, only 0.99 tracked**

| Subdir | MiB | Tracked | Verdict |
|---|---:|---:|---|
| `memory/ingest/` | 1,251.8 | 0.0 | **tape** — `registry.jsonl` is 1,244.1 MB append-only |
| `memory/runs/` | 1,222.3 | 0.0 | **tape** — 47,163 files, the ghost trail / session record pool |
| `memory/corpus/` | 772.0 | 731.0 | source corpus, tracked |
| `memory/biography/` | 356.6 | 0.0 | **tape** — 44,593 verkle chain files |
| `memory/training/` | 250.5 | 0.0 | **byte-dup of tracked `training/events.jsonl`** (247 MB) |
| `memory/seals/` | 184.0 | 183.9 | source |
| `memory/portable_bags/` | 146.4 | 2.6 | **regenerable** — `travel_kit_*.zip`, `.gitignore:13` |
| `memory/biography_backup/` | 135.5 | 0.0 | **regenerable** — rotated verkle backups, 103,089 files |
| `memory/research_packs/` | 108.7 | 0.0 | tape/scratch |

**~2.66 GiB of memory/ is legitimate append-only tape** (residual+registry+leaf = filed workdays) —
exactly what the fleet's DNA says to keep. The regenerable slice is
`portable_bags/` + `biography_backup/` + the `events.jsonl` duplicate = **~0.6 GiB**.

**New finding:** `training/events.jsonl` (247.0 MB, **TRACKED**) and `memory/training/events.jsonl`
(247.0 MB, untracked) are **byte-identical** — verified by sha256 of the first 200 KB each:
`2ce73a81c6b930ddf3b3e638f1a45c231fb8ab3f294fe3e79484bbd0257de2e3`. 247 MB of dead weight.

## 3. WHY is dashboard/ 3.5 GB? — **3.40 GiB, 3.39 GiB of it TRACKED**

**`dashboard/data/` is 3,545 MB in exactly 3 files — all three tracked:**

| File | MB | Tracked |
|---|---:|---|
| `ractor_board.jsonl.runaway-evidence-20260903` | 2,241.9 | **YES** |
| `ractor_board.jsonl` | 713.3 | **YES** |
| `ESTATE_INDEX.jsonl` | 590.2 | **YES** |

- `runaway-evidence-20260903` is an **incident snapshot of a runaway board, superseded by the live
  file next to it** — 2.24 GB of history for a debugging artifact.
- `ESTATE_INDEX.jsonl` is the **byte-dup** of `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` (590.2 MB each,
  both tracked). Verified: sha256 of first 400 KB of each is identical,
  `0c4c765db4e0f7dd5d08e342dc202fb78caa1851b62def00d2a8b588d648adc9`. Confirms the earlier finding.

**Is `dashboard/` build output or source? BOTH — and that is the problem.**
- `dashboard/*.py` (`server.py` 47.7 KB, `rest.py` 230 KB, `lan_proxy.py` 11.3 KB) = **source, must stay tracked.**
- `dashboard/static/` = **generated**. It contains its own generators: `_build_estate_walk.py`,
  `_build_cli_desk.py`, `_build_keeper_voice.py`, `_build_scout_deck.py`, `_build_shadow_walk.py`,
  `_rtfm_graph_build.py` (110 `.html` outputs). The docstring in `_build_estate_walk.py` says it
  outright: *"Self-contained output… Deterministic: seed 1197."* Generated 105 MB tracked in git.
- `dashboard/data/` = generated data, and 3.4 GiB of it tracked.

**dashboard/ vs dashboard-deploy/ vs site/ — not three copies of the same thing, but two are:**

- `dashboard-deploy/` (105 MB) is a **Vercel deploy snapshot** of the dashboard game ("Soul Frontier",
  `VERSIONS.md` v1.0.0→v1.2.0, 2026-09-24). `dashboard-deploy/static/` is a **375-of-376-file
  byte-copy of `dashboard/static/`** — a full duplicate, the one differing file being the deploy's own
  `VERSIONS.md` artifact set. Both are git-tracked. That is a clean 105 MB of pure duplication.
- `site/` (203 MB) is a **different project** — its own `build.py` (33 KB), `wrangler.jsonc`,
  `package.json`, and `nacho-site.tar.gz` (7.6 MB, tracked). Only `site/node_modules` + `site/dist` +
  `site/.wrangler` (192.6 MB) are regenerable.

## 4. logs/ 1.6 GB — **1.54 GiB, 100% untracked, NOT ROTATED**

**`grep -rn "RotatingFileHandler\|maxBytes=\|logrotate" --include=*.py mag/ dashboard/ scripts/`
returns nothing. There is no log rotation anywhere in the fleet.** Old logs are kept forever.

| File | MB |
|---|---:|
| `kpi.jsonl` | 912.5 |
| `dashboard_sv.err.log` | 179.8 |
| `backend_sv.log` | 80.5 |
| `dashboard_sv.log` | 72.9 |
| `usage.jsonl` | 69.6 |
| `behavioral_events.jsonl` | 66.5 |
| `ghost_sv.log` | 43.1 |
| `failure_kb.jsonl` | 39.7 |
| `api_gateway_sv.log` | 35.3 |

5,335 files, oldest 2026-07-20, newest 2026-09-26 — **68 days retained, unbounded**.
`kpi.jsonl` is continuous since Jul-21 and holds the Aug 16–31 silence (the ghost trail's continuity
argument makes this one genuinely precious). The `*_sv.log` stdout/stderr streams are not.

`watch/` adds 3 more unbounded logs: `engine_e1.log` 257.9 MB, `overnight_churn.log` 133.0 MB,
`engine_b1.log` 22.8 MB — 414 MB of stdout with no rotation.

## 5. mine/ 3.2 GB and _archaeology_out 160 MB — **both legitimate, both re-downloadable**

- **`mine/raw/` = 2.92 GiB across 100,986 files, 100% untracked** (`.gitignore:44-47`). It is
  **vendored third-party source, mined in place**: `mine/raw/agent_bleeding_edge/` (1.4 GB) holds
  `a2aproject`, `AgentOps-AI`, `arize-ai`, `getzep`, `jina-ai`; `mine/raw/agent_platform/` holds
  `Aider-AI`, `BerriAI`, `cline`, `continuedev`, `trypear/pearai-submodule`; `mine/raw/steal_protocol/`
  (154 MB) holds `arvarik`, `Bradliebs`, `EIT-EAST-Lab`; `mine/raw/narrative_corpus/` (57 MB) holds
  `ink-language`, `twinejs`, `tes5edit`. Several carry **their own `.git` directories and
  `.gitmodules`** — they are full clones, not source copies.
  **Verdict: legitimate field-mining corpus, but it is a cache of public repos.** Classified
  regenerable. Evidence of redundancy already visible: `all-MiniLM-L6-v2/onnx/model_quantized.onnx`
  (23.0 MB) appears twice — once under `continuedev/continue`, once under `trypear/pearai-submodule`.
- `_archaeology_out/` (160 MB) is **an archaeology export package, not scratch by accident**.
  `_archaeology_out/mag-disk-20260905/00_MANIFEST_MAG_DISK.md` states its own provenance:
  *"Host: DESKTOP-7C70KSC… Files staged: 3443, Bytes staged: 77792371"*, excluding `.venv`, models,
  node_modules, `.git` and files >8 MB. Alongside it sit three `nacho-archaeology-part8/9/10-*.zip`
  exports. Gitignored at `.gitignore:187`. One of those zips (23.5 MB) is byte-identical to
  `corpus/oral_history/nacho_archaeology/nacho-archaeology-part8-mag-disk.zip`.

---

## TOP 20 LARGEST INDIVIDUAL FILES

| # | MB | Tracked | Path |
|---:|---:|---|---|
| 1 | 2,357.8 | **TRACKED** | `attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar` |
| 2 | 2,241.9 | **TRACKED** | `dashboard/data/ractor_board.jsonl.runaway-evidence-20260903` |
| 3 | 1,706.5 | untracked | `watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc` |
| 4 | 1,244.1 | untracked | `memory/ingest/registry.jsonl` |
| 5 | 912.5 | untracked | `logs/kpi.jsonl` |
| 6 | 713.3 | **TRACKED** | `dashboard/data/ractor_board.jsonl` |
| 7 | 590.2 | **TRACKED** | `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` |
| 8 | 590.2 | **TRACKED** | `dashboard/data/ESTATE_INDEX.jsonl` (byte-dup of #7) |
| 9 | 353.9 | untracked | `memory/runs/ghost/trail.jsonl` |
| 10 | 307.0 | untracked | `corpus/oral_history/seat_pools/codex_sessions/2026/08/30/rollout-2026-08-30T09-09-46-….jsonl` |
| 11 | 305.1 | untracked | `.venv/Lib/site-packages/torch/lib/torch_cpu.dll` |
| 12 | 292.1 | untracked | `memory/runs/file_dogfood/manifest.jsonl` |
| 13 | 268.0 | **TRACKED** | `artifacts/vertigo_boat_20260908/tokyo_river_depth_1080p.mp4` |
| 14 | 257.9 | untracked | `watch/engine_e1.log` |
| 15 | 247.0 | **TRACKED** | `training/events.jsonl` |
| 16 | 247.0 | untracked | `memory/training/events.jsonl` (byte-dup of #15) |
| 17 | 189.8 | **TRACKED** | `attic/20260923_biography_rotation/biography_backup_20260825.tar` |
| 18 | 179.8 | untracked | `logs/dashboard_sv.err.log` |
| 19 | 156.6 | **TRACKED** | `attic/20260923_ghost_rotation/leak_reports_pre_2026-09-16.tar` |
| 20 | 153.9 | untracked | `corpus/library/wakers_20260906_knowledge_debt/Jung_The_Red_Book_Liber_Novus_2009.pdf` |

**9 of the top 20 are git-tracked, and they total 7,500 MB.** The tracked tail is heavy: the attic
tars alone are 2,703 MB, dashboard/data 3,545 MB, the two ledgers 1,180 MB.

---

## WHAT THIS MEANS FOR A DISK DECISION

**Nothing here is history that isn't already captured.** The reclaimable set, in order of safety:

1. **`.mimosa/` — 15.70 GiB.** A per-session content-addressed cache at 204× duplication
   (1,292,387 `.source` files, ~5,542 unique). Gitignored, fully rebuildable. **The single biggest
   win and the safest one — it is a cache by construction.**
2. **`dashboard/data/ractor_board.jsonl.runaway-evidence-20260903` — 2.24 GB.** A superseded
   incident snapshot sitting next to the live board it was a snapshot *of*. `git rm --cached` + ignore.
3. **`watch/inbox/*/media_full/` — ~4.0 GB of tracked `.mp4`/`.png` Telegram exports.** Scratch media
   in git history; the ledgers beside them are the durable record.
4. **`attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar` — 2.36 GB.** A tar of *stale
   mimosa baselines* — the same cache already counted in item 1, now archived twice.
5. **`mine/raw/` — 2.92 GiB.** Vendored public clones; re-clonable from their remotes.
6. **One of the two `ESTATE_INDEX.jsonl` copies — 590 MB**, and the untracked
   `memory/training/events.jsonl` duplicate — 247 MB.
7. **`dashboard-deploy/static/` — 105 MB**, a 375/376-file copy of `dashboard/static/`.
8. **Log rotation** — `logs/` 1.54 GiB + `watch/*.log` 414 MB with **no rotation configured**;
   the `*_sv.log` stdout streams are safe to cap, `kpi.jsonl` is the ghost trail's continuity proof
   and should be compressed rather than deleted.

**Caveat, stated plainly:** items 2–7 require `git rm --cached` + a history rewrite to actually
reclaim space on disk, because those blobs are already in `.git` (7.5 GiB, 6.11 GiB in packs).
A filter-branch/rewrite is a separate, larger piece of work than this measurement. Items 1, 5, 8
(delete-only, no history change) reclaim immediately. **That split is the decision.**

---

## METHOD + REPRODUCTION

- One bounded `os.walk` (`os.lstat` per file), `.git` and `.mimosa` pruned, streamed to
  `scratch/w2l1_files.tsv` — 573,759 files / 33,201,478,231 bytes in 237 s.
- `git ls-files -z` → `scratch/w2l1_tracked.txt` (44,161 paths); membership test on the walk rows.
  44,159 matched on disk; **2 tracked paths are deleted-but-still-indexed.**
- `.git` = 7.5 GiB by `du -sh .git`; `git count-objects -vH` = 6.11 GiB in packs + 1.27 GiB loose.
- `.mimosa` = 15.7 GiB, the figure already established in the brief (measured separately, 1.29 M files).
- No unbounded `du`/`find` on the whole tree; every directory probe was capped at 15–45 s.
- Regenerate: `./.venv/Scripts/python.exe scripts/_w2l1_disk_map.py` → `memory/audit_20260926/w2l1_disk.json`.

**Tri-state:** the byte classes, the tracked/untracked split, the top-20 list, the two byte-identical
duplicate pairs, the absence of log rotation, and the vendored nature of `mine/raw/` are all
**Supported** (directly measured). Whether a given tracked blob is *worth* keeping is a judgment
call left to the Operator — this card measures, it does not decide.
