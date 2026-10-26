# s2-07: Large-File Census (10 largest files outside .git/.venv/node_modules/corpus)

Census date: 2026-09-28. Lane: f2-s2-07 (flash50 burn reset). Census law: every number below came from a command run in this session; instrument, moment, and deltas are named. Nothing was modified; this is a read-only census.

## Method (instruments)

1. `watch/inbox/burn_reset_20260927/flash50/s2-07_scan.py` (repo venv python): cycle-safe `os.scandir` walk of `C:\Users\foste\Documents\projects\local_sovereign_agent`, pruning directories named `.git`, `.venv`, `node_modules`, `corpus` at any depth. A first naive `os.walk` was killed after 7+ minutes with no output (junction suspicion); v2 prunes dirs whose `realpath` was already visited or that resolve outside the repo root. Walk totals: **3,413,247 files / 68,114,340,735 bytes / 52,140 dirs**, skipped: 11 cycle junctions, 0 outside-root, 1 `\\.\nul` device path. Completed ~18:49-18:51 local 2026-09-28.
2. `watch/inbox/burn_reset_20260927/flash50/s2-07_characterize.py`: per-file stat (size, mtime, nlink, fileindex), head/tail hex+printable, JSONL line counts (chunked `b"\n"` count), tar member listing (first 20), and full sha256 of the two same-size ESTATE_INDEX copies. Run ~18:55-18:56 local.
3. Reference census: `git grep`, `git log -1 --format=... -- <file>`, `git ls-files --error-unmatch`, `git check-ignore`, `git cat-file -s`, `git count-objects -vH`, plus a python string scan of 1,510 code files (tracked AND untracked) under `tools/ scripts/ mag/ .agents/ githooks/ + main.py + synthesis_agent.py` for `file_dogfood`.

Headline: the top 10 files sum to **12,631,257,089 bytes = 18.5%** of the scanned tree. Repo `.git` pack is **6.11 GiB** (`git count-objects -vH`), and **6 of the 10 largest working-tree files are git-tracked blobs**.

## The top 10

| # | File | Bytes | Mtime | Git | One line |
|---|------|-------|-------|-----|----------|
| 1 | attic\20260923_mimosa_rotation\hook-state_stale_baselines.tar | 2,357,760,000 | 2026-09-23 07:37 | TRACKED (a5dd96176) | tar of 68 dead-session Mimosa baseline dirs |
| 2 | dashboard\data\ractor_board.jsonl.runaway-evidence-20260903 | 2,241,937,839 | 2026-09-03 06:05 | TRACKED (d575bc168) | frozen evidence of the ractor_board runaway append (9,202,634 lines) |
| 3 | watch\inbox\ESSENTIALS_PACK_20260926.tar.gz.enc | 1,706,469,664 | 2026-09-26 07:39 | ignored by design | OpenSSL-encrypted disaster-recovery pack |
| 4 | watch\ESTATE_INDEX\ESTATE_INDEX.jsonl | 1,291,745,128 | 2026-09-28 09:42 | TRACKED (9 commits) | estate spine, 3,485,538 rows |
| 5 | dashboard\data\ESTATE_INDEX.jsonl | 1,291,745,128 | 2026-09-28 09:42 | TRACKED (9 commits) | byte-identical serving copy of #4 (sha256 verified) |
| 6 | memory\ingest\registry.jsonl | 1,291,413,726 | 2026-09-28 18:55 (live) | ignored | append-only ingest registry, 2,525,185 rows |
| 7 | logs\kpi.jsonl | 1,058,483,724 | 2026-09-28 18:55 (live) | ignored | KPI time series, 81,945 rows, 12.9 KB/row avg |
| 8 | dashboard\data\ractor_board.jsonl | 713,252,012 | 2026-09-03 22:30 (frozen) | TRACKED (d575bc168) | organ board events, 2,959,486 lines |
| 9 | memory\runs\ghost\trail.jsonl | 386,300,080 | 2026-09-28 18:56 (live) | ignored | ghost loop receipts, 18,631 rows, 20.7 KB/row avg |
| 10 | memory\runs\file_dogfood\manifest.jsonl | 292,121,597 | 2026-09-13 11:26 (frozen) | ignored | full-projects-tree file manifest, 1,292,364 rows, no writer in repo |

Live-writer proof: sizes taken ~6 minutes apart during the census grew: kpi.jsonl +74,990 B (18:49:19 to 18:55:19), registry.jsonl +27,930 B (18:49:22 to 18:55:20), ghost trail.jsonl +56,383 B (18:51:17 to 18:56:24).

## Per-file: what it is, load-bearing?, split/archive?

### 1. attic\20260923_mimosa_rotation\hook-state_stale_baselines.tar (2.36 GB)

- **What:** uncompressed tar of 68 per-session Mimosa hook-state `.baseline` dirs (members are sha-named `*.source` files under `sess_*.baseline/`, verified by listing the first 20 members). `attic/MANIFEST.jsonl:16` records the rotation: from `.mimosa/hook-state/*.baseline (68 dirs, mtime >7d)`, why "dead-session baseline rotation GO 09-23", `tar_verified: all-dirs-present`.
- **Load-bearing:** no. It is already the archive step; the live `.mimosa` hook-state consumed by Mimosa is outside this tar.
- **Split/archive:** do not split. It is the archive. Recommendation: this is a cold copy that does not need to sit in the working tree or in git history (it was swept into commit a5dd96176, 2026-09-25). `git rm --cached` + move to the Drive mirror / offline cold store. Retention/destroy call belongs to the Mimosa lane; nothing in this census executed it.

### 2. dashboard\data\ractor_board.jsonl.runaway-evidence-20260903 (2.24 GB, 9,202,634 lines)

- **What:** frozen snapshot of `ractor_board.jsonl` captured while the board append loop was running away on 2026-09-03. Head/tail rows carry the board schema (`organ/kind/title/detail/status/evidence/ts`, organ `zcode`, engine-b1 task receipts, ts `2026-09-03T10:05:22Z` on the last row).
- **Load-bearing:** as evidence, yes and deliberate. The scar is load-bearing in three places: `mag/bay_organs.py:132-137` (`write_writer_lock`, docstring: "This is the fix for the runaway scar: every writer of ractor_board.jsonl / queue files carries pid + seat + ts"), `dashboard/server.py:75-78` (bounded 256 KB backward tail read, comment "ractor_board.jsonl hit 713MB; clients must not re-download it"), and `.gitignore:213-214` ("the 2.2GB runaway blob precedent").
- **Split/archive:** no split. Keep the evidence (it is the incident record and is not re-derivable), but it does not need to be a live git blob (committed d575bc168, 2026-09-14 checkpoint). Candidate for off-pack cold copy; destruction is an operator call.

### 3. watch\inbox\ESSENTIALS_PACK_20260926.tar.gz.enc (1.71 GB)

- **What:** single-file disaster-recovery pack. First 8 bytes are ASCII `Salted__` (OpenSSL enc format); `watch/inbox/ESSENTIALS_RESTORE.md` gives the restore: `openssl enc -d -aes-256-cbc -pbkdf2 -in ... | tar -xzf -`, passphrase lives outside the machine on purpose. Contents per the restore doc: code, configs + .env, docs, queue, state, memory canon, watch receipts; excludes .git/.venv/media corpora.
- **Load-bearing:** yes. This is the machine-loss recovery artefact (also see `memory/continuity/seat_memory_20260927/essentials-pack-disaster-recovery.md`, `memory/burns/LEDGER.jsonl`).
- **Split/archive:** no split; it IS the archive. Already handled: untracked + gitignored (`watch/inbox/ESSENTIALS_PACK_*.tar.gz.enc`, `.gitignore:213-218` never-a-blob set, 2026-09-27). Only note: it grew from the 1.59 GB the gitignore comment recorded on 09-27 to 1.71 GB now; regenerate per pack cadence and keep exactly one recent + one offsite.

### 4+5. watch\ESTATE_INDEX\ESTATE_INDEX.jsonl and dashboard\data\ESTATE_INDEX.jsonl (1.29 GB each)

- **What:** the estate spine. One row per file seen by the indexer: `{"path","proj","rel","mtime","mtime_epoch","size","ext","depth","temp"}` with a relation taxonomy (`body file`, `watch card (the record)`, `lane (sibling project)`, temp buckets HOT/WARM/COLD/FROZEN). 3,485,538 rows each, 370.6 B/row. The two copies are **byte-identical** (both sha256 `f615bf5331dab3bb903d93a082329b38f03b104e19ef2871d9460d14f7a6fb7d`) but are separate files (different NTFS fileindex, nlink=1, mtimes 10 s apart), not hardlinks.
- **Writer:** `tools/index/projects_index.py` - `MASTER = watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` (line 31) and `DASH_MASTER = dashboard/data/ESTATE_INDEX.jsonl` (line 34) are both program constants; the same run rewrites the spine then writes a full duplicate for the dashboard. `watch/ESTATE_INDEX/last_run.json`: ts 2026-09-28T13:42:43Z, 3,479,920 files / 110,488,163,407 B scanned (wider than this repo; includes sibling lanes).
- **Readers (load-bearing):** `scripts/librarian.py:39`, `tools/estate_atlas.py:35-36` (spine age guard), `dashboard/server.py:542` (download allowlist `{"ractor_board.jsonl", "ESTATE_INDEX.jsonl"}`), `scripts/build_knowledge_graph.py:56`.
- **Split/archive:** yes, this is the best split candidate in the repo. Every run is a full rewrite (each row carries mtime/size, so nearly every row changes), which means (a) the working tree holds two 1.29 GB copies, and (b) git stores a near-full new blob per commit: **9 commits touch each path** (`git log --format=%h | wc -l` = 9 and 9), HEAD blobs 1,238,673,014 B each, and both are modified-uncommitted again today. Options in preference order: (1) untrack both (add to the never-a-blob set; keep `rollup.json` + `last_run.json` tracked, they are the queryable summaries), (2) make the dashboard copy a link/junction or serve it from the spine instead of duplicating 1.29 GB, (3) roll the spine by date (daily partitions) or switch to delta rows. None of this was executed here.

### 6. memory\ingest\registry.jsonl (1.29 GB, 2,525,185 rows, live)

- **What:** append-only ingest registry. Rows: `{"id","title","kind","tags","url","filename","local_source","local_copy","local_path","html_stub","file_sha256","session_id","ingested_at","where_to_find"}`. First row is `steiniger-academia` (author profile); the newest row (ingested_at 2026-09-28T22:55:19Z) is an `extra-<sha12>` `session_extra` row from session `mag-agent-orc-t0c3b6d19ab`.
- **Writer:** `mag/ingest_registry.py` - `REGISTRY = INGEST / "registry.jsonl"` (line 42), append at lines 453-454. Session extras map to per-session `extra-*` rows at lines 468-476. Callers: `mag/session_dossier.py:20`, `mag/research_pack.py:102`, `mag/pdf_layout.py:27`.
- **Load-bearing:** yes. It is the memory of what was ingested and where to find it (the file's own header docstring, ingest_registry.py:8-12, says exactly that). It grew +27,930 B during the census itself.
- **Split/archive:** yes. It is append-only with no compaction: 2.5 M rows at 511 B/row and every re-ingest or session end appends more. Recommendation: a compaction pass (keep the newest row per `id`, archive the tail to attic) plus month-partitioned files going forward. Ignored by git (`git check-ignore` positive), so no history cost.

### 7. logs\kpi.jsonl (1.06 GB, 81,945 rows, live)

- **What:** memory-health KPI time series, schema `mag_records_kpi.v1`, one row per write since 2026-07-21T12:53:42Z (first row). Average row is **12,913 bytes**, which is the whole story: each row embeds `incomplete_ids`, the full list of every incomplete session id at that moment, and that list has grown into the thousands (the tail row's array runs for many KB).
- **Writer:** `mag/records.py:138-168` (`write_kpi`): writes `memory/biography/kpi.json` (line 164) and appends the same dict to `logs/kpi.jsonl` (lines 166-167). No rotation anywhere in the function. Callers: `mag/biography.py:551` (summarize), `mag/lanes.py:267` (board), `mag/operator_os.py:90` (operator-os), `main.py:2634` (pack-status), `main.py:2674` (migrate-lean), `mag/records.py:223` (backfill). Grew +74,990 B during the census window.
- **Load-bearing:** yes (the KPI trend is the residual+registry+leaf health signal, cited in AGENTS.md workday doctrine), but 1.06 GB from 82 K rows is a schema defect, not data volume.
- **Split/archive:** yes, cheap win. Stop embedding the full `incomplete_ids` array per row (emit count + first N ids, full list stays in `kpi.json`), and start month-partitioned files (`kpi-2026-09.jsonl`). Estimated ~10x reduction immediately. Ignored by git.

### 8. dashboard\data\ractor_board.jsonl (713 MB, 2,959,486 lines, frozen)

- **What:** the organ board event store (same schema as #2). Frozen at mtime 2026-09-03T22:30:27; no tracked writer appended since. Note the mtimes: the 9.2 M-line evidence snapshot (#2) was captured at 06:05 that day and the board file itself was last touched at 22:30 with 2.96 M lines, consistent with a same-day trim after the runaway (inference from the two mtimes/line counts, not from a receipt).
- **Writer/reader:** no active tracked writer found (`git grep ractor_board` over code shows only the server reads plus the bay_organs lock documentation); `dashboard/server.py:522` serves it via the bounded `_tail_jsonl` window read (lines 75-99) precisely so clients never re-download the 713 MB (comment at line 77). `mag/bay_organs.py:19,132` documents writer locks for its writers.
- **Load-bearing:** yes as the board's historical event store read by the dashboard tail endpoint; dormant as an append target for 25 days.
- **Split/archive:** yes. Archive everything older than a cutoff to `attic/` and start a fresh board file with a size-based rotation (the exact failure mode already happened once). Also a candidate to untrack (tracked blob since d575bc168) to stop pack growth if any writer resumes.

### 9. memory\runs\ghost\trail.jsonl (386 MB, 18,631 rows, live)

- **What:** the ghost steer-experiment loop's receipt trail, first row 2026-08-08T00:48:45Z. Each cycle row embeds a full state snapshot (`fkb_top_signatures`, guard registry, amd_window_guard, outcome, vector_id), which is why the average row is **20,733 bytes** for only 18.6 K rows.
- **Writer:** `mag/ghost.py` - `TRAIL_PATH = GHOST_DIR / "trail.jsonl"` (line 44); appends at line 1241 (`queue_stall_sweep`) and lines 3327/3332/3349 (sense/match/deploy/measure cycle). Invoked per `.github/agents/ghost-experiment-runner.agent.md:43-49` (`python -m mag.ghost` cycle). Reader: `main.py:885-888` tails ghost trails as a live feed. Grew +56,383 B during the census.
- **Load-bearing:** yes (ghost loop receipts; the trail is the loop's memory and liveness surface).
- **Split/archive:** yes. Split the per-row state snapshot into a single last-state sidecar file and keep only event deltas in the trail; that alone removes most of the 20.7 KB/row. ~7.7 MB/day average since 08-08; ignored by git.

### 10. memory\runs\file_dogfood\manifest.jsonl (292 MB, 1,292,364 rows, frozen)

- **What:** full-filesystem manifest of `C:\Users\foste\Documents\projects` from a 2026-09-13 file-dogfood run: rows `{"p","b","m","e"}` (path, bytes, mtime epoch, ext), including files outside this repo (`..\AGENTS.md`, `.mimosa\...`, `.cursor\settings.json`). The run directory contains only the manifest.
- **Writer:** **not found**. A scan of 1,510 code files (tracked and untracked) under `tools/ scripts/ mag/ .agents/ githooks/` plus `main.py` and `synthesis_agent.py` for the string `file_dogfood` returned **0 hits**; `git grep` over tracked files finds only receipt mentions. The writer was a seat-cache script that never landed in the shared surface.
- **Load-bearing:** no reader and no writer in the tree; 16 days stale; regenerable by rerunning any file scan.
- **Split/archive:** neither. Delete or move to attic; the durable receipt (what the run was for) belongs in a watch card, not a 292 MB orphan. This is the one file in the top 10 I would remove outright (operator call; not executed here).

## Honorable mentions (ranks 11-15, from the same scan)

`artifacts\vertigo_boat_20260908\tokyo_river_depth_1080p.mp4` 268,023,793 B (media asset); `watch\engine_e1.log` 257,859,878 B (engine log, frozen 09-03); `memory\training\events.jsonl` 255,334,700 B, mtime today 18:51 (live); `attic\20260923_biography_rotation\biography_backup_20260825.tar` 189,808,640 B (archive); `logs\dashboard_sv.err.log` 179,850,540 B, mtime today 18:48 (a 180 MB live error log is worth its own look). Also rank 16 `catalog\catalog_fts.sqlite` 161,345,536 B (derived index, gitignored by design, rebuilt daily by the sanctioned writer per `.gitignore:215-216`).

## Cross-cutting findings

- **F1 (git carries the giants):** 6 of the top 10 are tracked. Tracked: #1 (2.36 GB), #2 (2.24 GB), #4 and #5 (1.29 GB each, 9 commits each), #8 (713 MB). The 2026-09-27 never-a-blob gitignore set (`.gitignore:212-218`) fixed *future* adds (enc pack, catalog_fts) but left the already-tracked giants in the pack; `git count-objects -vH` puts size-pack at 6.11 GiB, and the estate spine alone contributes ~18 near-full ~1.2 GB blob versions (2 paths x 9 commits) before compression.
- **F2 (schema, not volume):** kpi.jsonl (12.9 KB/row from embedding full incomplete_ids) and ghost trail (20.7 KB/row from embedding full state) are ~1.4 GB combined that a field cap and a state sidecar would shrink roughly 10x.
- **F3 (silent duplication):** the estate spine exists as two byte-identical 1.29 GB copies written 10 s apart by the same program; the dashboard copy buys nothing that a link or on-the-fly serve would not.
- **F4 (no rotation on three live append logs):** ingest registry, kpi.jsonl, and ghost trail all have single-file append writers with no size cap, and all three grew while this census ran.
- **F5 (one orphan):** file_dogfood/manifest.jsonl has no writer or reader anywhere in the tree (0 hits in 1,510 scanned code files).
- **F6 (the runaway scar is properly institutionalized):** evidence file kept, writer locks shipped (`mag/bay_organs.py:132`), bounded tail read shipped (`dashboard/server.py:75`), precedent named in `.gitignore:214`. The remaining debt is that the evidence and the board itself still ride in the git pack.

## Recommended actions (none executed; operator calls)

1. Untrack the four tracked giants (#1, #2, #4, #5, then #8) into the never-a-blob set; move cold copies to the Drive mirror / attic off-pack.
2. ESTATE_INDEX: roll by date or delta rows; replace the dashboard duplicate with a link or serve-from-spine; keep rollup.json + last_run.json tracked.
3. kpi.jsonl: cap `incomplete_ids` per row (count + first N) and partition monthly.
4. ghost trail: split state snapshot to a sidecar.
5. ingest registry: compaction pass (newest row per id) + monthly partitions.
6. ractor_board: size-based rotation going forward; archive the 713 MB tail.
7. Delete or attic file_dogfood/manifest.jsonl (orphan).

## Receipts

Instruments banked beside this file: `s2-07_scan.py` (walker), `s2-07_characterize.py` (per-file prober), `s2-07_scan_stderr.log` (walker progress/cycle log). Item record: `s2-07.md`.
