# ESTATE_INDEX.jsonl compaction design - night shift 2026-10-04 (free lane, design only)

Scope: dashboard/data/ESTATE_INDEX.jsonl (3,409,161,472 bytes = 3.17 GiB, the single
biggest file in the repo). Design only. Nothing executed against the file; every
measurement below was a read-only pass. No commits. The 3.2 GB file was never opened
for write.

Two honest corrections to the briefing before the design, because the design hangs on them:

1. "Unbounded append" is disproven. The writer opens the master with mode "w"
   (tools/index/projects_index.py:107) - one full snapshot per run, no append. Proof:
   tonight's full chunked count reads exactly 8,803,599 non-blank rows and
   watch/ESTATE_INDEX/last_run.json (writer's own state, ts 2026-10-03T13:59:56Z) says
   total_files = 8,803,599. A cross-run concatenation would make the file count exceed
   the run's file count; it does not. The file is one run's snapshot that grows because
   the walk scope grows, not because rows accumulate.
2. The gap-sentinel 29.5 GiB/day alert does not measure this file. The instrument is
   tools/gap_sentinel.py (daily task MagGapSentinelDaily), which diffs the SMALL rollup
   snapshots (dashboard/static/index_data/rollup.json, not the 3.2 GB master) and flags
   per-project indexed-byte growth (tools/gap_sentinel.py:61, logs/gap_sentinel.log,
   window 2026-10-01T14:11:53Z -> 2026-10-02T14:29:59Z: "local_sovereign_agent 29.89
   GiB (29.52 GiB/day)"). That is the estate's indexed CONTENT growth. The index file
   itself grew 1.95 GB (2026-09-29, tools/estate_index_dedup.py receipt) -> 3.41 GB
   (2026-10-03). But the index AMPLIFIES the disease it measures: 2x byte-identical
   copies, a full 3.2 GB rewrite + 3.2 GB copy every daily run (~6.8 GB of disk writes
   per day at current size), and a git-tracked 2.52 GB blob (cb136109, committed in
   5d2263f10) that re-stores wholesale on every commit because every row's mtime/temp
   churns daily, defeating delta compression.

## 1. Writer map (who appends/rewrites, file:line)

| # | Writer | Where | Behavior |
|---|--------|-------|----------|
| W1 | tools/index/projects_index.py:107-109 | writes watch/ESTATE_INDEX/ESTATE_INDEX.jsonl, mode "w", one row per walked file, sorted mtime desc, CRLF line endings (text-mode open without newline="\n") | THE writer |
| W1b | tools/index/projects_index.py:138 | shutil.copyfile(MASTER, dashboard/data/ESTATE_INDEX.jsonl) | THE 3.2 GB mirror step |
| W1c | tools/index/projects_index.py:139-140 | copies rollup.json + last_run.json only to dashboard/static/index_data/ (small) | fine |
| W2 | seed/engines/spine_walk.py:107-109,139 | the shipped seed variant of the same walker (root via argv); not scheduled in this repo | no live writes here |
| S | Scheduler: Windows task "Estate Spine Index" | action = .venv\Scripts\python.exe tools\index\projects_index.py, daily 09:00 local, registered 2026-09-23; last walk took 3498.3s (~58 min, finishes ~10:00 local) | daily cadence |

Walk root: C:\Users\foste\Documents\projects (tools/index/projects_index.py:25) - the
WHOLE projects folder: all sibling projects, their venvs, node_modules, .git internals,
and the repo's own .mimosa cache. The walk itself is read-only against the estate; only
the four constant-name outputs are written (the "fixed mouths" v5 design, header comment
lines 1-19).

## 2. Row shape and measured duplication (instruments named)

Row shape (first row of file, exact):

```json
{"path": "local_sovereign_agent\\memory\\training\\events.jsonl", "proj": "local_sovereign_agent", "rel": "memory estate", "mtime": "2026-10-03T13:57:40Z", "mtime_epoch": 1791035860, "size": 358750424, "ext": ".jsonl", "depth": 3, "temp": "HOT"}
```

Nine fields; entity key is "path"; volatile-per-run fields are mtime, mtime_epoch, temp.
Rows sorted newest-mtime-first; the tail of the file is epoch-0 pytest litter (e.g.
local_sovereign_agent\agents\pytest-tmp-47224\...\nul, mtime 1970-01-01, size 0).

Measured numbers (all instruments read-only, .venv\Scripts\python.exe, tonight):

| Metric | Value | Instrument |
|---|---|---|
| file size | 3,409,161,472 B (3.17 GiB) | os.stat + ls; identical size on both copies |
| rows | 8,803,599 non-blank | full streaming pass, 8 MiB chunks, bytes-only line split, 89 s |
| avg row | 387.3 B, CRLF-terminated | same pass |
| exact duplicate whole-row lines | 93 of 8,803,599 (~1e-5) | same pass; blake2b-64 per line, sorted-adjacent count |
| exact duplicate path keys | 94 of 8,803,599 (~1e-5) | same pass; blake2b-64 of path field |
| rows with ext ".source" | 7,707,174 (87.5%) | targeted ext-field probe, 25 s |
| ".source" home | 7,384,451 under local_sovereign_agent\.mimosa\ + 317,460 under .mimosa\hook-state\ | prefix grouping probe |
| .mimosa rows total | 7,402,705 = 84.1% of rows = 87.2% of bytes (2,972,345,730 B) | byte-accounting pass, 33 s |
| projected size excluding .mimosa rows | 437 MB (12.8% of file) | same pass |
| venv/node_modules rows | 130,061 (1.5% rows, 1.1% bytes) | same pass |
| pytest-tmp litter rows | ~83,910 (0.95%) | mmap string count of "pytest-tmp-" |
| temp buckets | HOT 74,746 / WARM 1,205,557 / COLD 3,687,092 / FROZEN 3,836,204 | full pass |
| indexed content growth | 125.6 -> 198.9 GiB total, lsa project +73 GiB, over 2026-09-29 -> 10-03 | logs/gap_sentinel/history.jsonl (5 snapshots) |
| size timeline | 590.2 MB per copy 2026-09-26 (memory/audit_20260926/w2l1_disk.json) -> 1,945,896,570 B 2026-09-29 (dedup receipt) -> 3.41 GB 2026-10-03 | receipts |
| git state | BOTH copies tracked, same blob cb136109 (2,523,006,985 B, commit 5d2263f10); both currently Modified vs that blob | git ls-files / cat-file / status |
| prior mirror dedup | applied 2026-09-30T02:25:42Z (pointer swap, shas banked); CLOBBERED by the next daily run because W1 rewrites the master and W1b re-copies it | watch/ESTATE_INDEX/ESTATE_INDEX.jsonl.dedup_shas.json + tools/estate_index_dedup.py:20-22 |

Conclusion from the numbers: within one snapshot there is nothing to dedupe (duplicate
rate ~1e-5). The duplication that costs disk is BETWEEN the two byte-identical copies
(2x), BETWEEN daily runs (every row re-encoded daily although only a small fraction of
files change), and BETWEEN git commits (full-blob restorage). And 87.2% of every copy
is a catalog of .mimosa - a gitignored (.gitignore:200), per-session, content-addressed
cache the 2026-09-26 disk audit already called "C_regenerable ... 204x duplication"
(scripts/_w2l1_disk_map.py:34-48, memory/audit_20260926/w2l1_disk.json).

## 3. Reader map (who consumes ESTATE_INDEX, file:line)

| # | Reader | Where | Pattern | Cost at 3.2 GB / 8.8 M rows |
|---|--------|-------|---------|------------------------------|
| R1 | dashboard server /data door | dashboard/server.py:622-639 (allowlist line 624) | streams the whole file per request, Content-Length = 3.2 GB | worst network reader; the ractor tail door (server.py:592-598) already exists as the bounded pattern for the sibling board |
| R2 | the_index.html UI | dashboard/static/the_index.html:118-129 | fetch("/data/ESTATE_INDEX.jsonl", {cache:"no-store"}), r.text(), split, JSON.parse EVERY row into ROWS[] | worst browser reader: multi-GB RAM, minutes of parse; UI only filters by rel/proj/temp/search |
| R3 | librarian coldload | scripts/librarian.py:39-51 | idx.read_text().splitlines() (whole file into RAM), linear keyword scan, first 120 hits | OOM/minutes at current size |
| R4 | estate atlas | tools/estate_atlas.py:35,95-110 (+ seed/engines/estate_atlas.py:35) | streaming line-by-line json.loads of the watch master | 8.8 M JSON parses per run (~minutes) |
| R5 | gap sentinel | tools/gap_sentinel.py:61 (ROLLUP_RELPATH = dashboard/static/index_data/rollup.json) | reads ONLY the 20 KB rollup copy, never the master | fine; no port needed |
| R6 | battery rerun | tools/battery_rerun.py:51 ("index_sha256", dashboard/data/ESTATE_INDEX.jsonl) | full-file sha256 per battery run | ~30-60 s digest each run |
| R7 | frontdoor links | dashboard/static/frontdoor/index.html:39,58 | href links to rollup + watch master | trivial |
| R8 | knowledge graph map | scripts/build_knowledge_graph.py:56 | path-presence mapping only | trivial |
| R9 | estate_index_dedup | tools/estate_index_dedup.py:42-43 | verifies/copies between the two | the sanctioned mirror tool |
| R10 | citation lint io | tools/citation_lint_io.py:28 | comment-only mention (big-file skip rationale) | none |

## 4. Options evaluated

**A. Dedupe-to-last-wins per entity key (jsonl rewrite).** Rejected as primary. The
file is already last-wins-clean: one row per path per run (93/8.8 M duplicates). A
dedupe pass reclaims nothing inside a snapshot; it would only rebuild the same 3.2 GB.
The variant that IS worth keeping is killing the 2x mirror (R9 pointer swap) - but the
2026-09-30 attempt proves it is futile alone: W1/W1b clobber the pointer next morning.
Any mirror dedup must ship together with the writer change or it is scheduled litter.

**B. Snapshot + delta split.** Rejected. It optimizes the writer's daily write but makes
every reader (R1-R4, R6) implement a merge layer over base + N deltas, needs periodic
rebasing, and preserves HISTORY of regenerable metadata - the disk is the source of
truth and the walk is repeatable in ~58 min. Highest blast radius, lowest payoff.

**C. Cap + rotate with cold archive.** Rejected as primary. Rotation bounds the live
file but each daily run still walks 8.8 M files and rewrites a full snapshot, the
archives themselves accumulate multi-GB copies of regenerable data (the ractor_board
runaway-evidence precedent, 2.2 GB, is evidence-class for a REAL runaway, not a
regenerable catalog), and the sentinel keeps flagging the same growth. Rotation is
adopted only for the migration archive step (one sealed copy, then stop).

**D. SQLite migration with a scoped walk (corpus FTS5 precedent).** RECOMMENDED. The
estate already proved FTS5/sqlite beats jsonl scanning (corpus catalog precedent,
B2-465 machinery; tools/citation_lint_io.py:28 exists precisely because jsonl scans of
this file are unbearably slow). A files table keyed on path makes last-wins-per-entity
a CONSTRAINT (PRIMARY KEY) rather than a post-hoc pass; readers get bounded queries;
size after scope-fix ~400-600 MB instead of 2x 3.2 GB; daily write becomes an upsert
of changed rows instead of a 6.8 GB rewrite+copy.

The decisive first move inside D is the skip list, not the engine swap: excluding
.mimosa alone cuts the artifact 87.2% (3.41 GB -> 437 MB measured projection) because
it is a gitignored regenerable cache. No engine choice survives contact with a walk
that catalogs 7.4 M cache files daily.

## 5. Recommended design

Target state:

- One sqlite spine: watch/ESTATE_INDEX/estate_index.sqlite (regenerable, gitignored;
  provenance lives in its runs table, not in git).
- The walk skips, by operator-approved list (default: .mimosa, .venv, venv,
  node_modules, __pycache__; .git is an explicit operator call since ancestor .git dirs
  are currently cataloged, e.g. Mag-backup.git 12,757 rows): projected ~1.27 M rows,
  ~400 MB jsonl-equivalent, DB likely 150-350 MB.
- rollup.json + last_run.json keep their exact shape (R5 sentinel reads the rollup;
  zero sentinel changes). Skipped roots are NAMED in last_run.json (new "skipped_roots"
  key) and in the runs table row, so the skip decision is auditable and reversible -
  a later run can re-include a root and the DB absorbs it.
- The fat jsonl master + mirror are retired: one cold archive copy of the 2026-10-03
  master is kept; the mirror becomes a pointer again (this time the writer no longer
  clobbers it); the /data door keeps serving during a one-week transition, then 410s.

Schema (design):

```sql
CREATE TABLE files (
  path TEXT PRIMARY KEY,      -- entity key, last-wins by construction
  proj TEXT NOT NULL, rel TEXT, mtime TEXT, mtime_epoch INTEGER,
  size INTEGER, ext TEXT, depth INTEGER, temp TEXT
) WITHOUT ROWID;
CREATE INDEX files_proj ON files(proj);
CREATE VIRTUAL TABLE files_fts USING fts5(path, content='files', content_rowid='path');
  -- FTS optional at landing; LIKE 'pattern%' on the PK prefix serves librarian
  -- keyword hits too; FTS5 is the upgrade path (corpus precedent)
CREATE TABLE runs (
  run_id INTEGER PRIMARY KEY, ts TEXT, total_files INTEGER, total_bytes INTEGER,
  walked_root TEXT, skipped_roots TEXT,   -- JSON array; the audit trail
  source TEXT                             -- 'jsonl-migration' | 'walk'
);
```

Upsert policy: INSERT ... ON CONFLICT(path) DO UPDATE WHERE excluded.mtime_epoch !=
files.mtime_epoch OR excluded.size != files.size - unchanged rows cost no page write;
changed rows update; vanished rows DELETE (one anti-join per run, batched). The
deleted-row names land in a per-run tombstone jsonl under watch/ESTATE_INDEX/tombstones/
(bounded by a keep-N rotation, operator call) so deletion from the index is itself
reversible-by-record.

Why this is lossless by construction (estate law: never delete sibling data):

1. Nothing on disk changes: the walk stays read-only against the estate.
2. The 2026-10-03 jsonl pair is not deleted - archived (one copy) with sha256 banked in
   the dedup-shas receipt format; rollback can restore it byte-identically.
3. Row loss cannot happen in the DB: rows only enter via walk or migration, both of
   which are verified against counts before cutover (below); row exit is tombstoned.
4. The .mimosa exclusion removes no tracked or curated data - .gitignore:200 already
   declares it non-estate; the disk files remain untouched.
5. Total index catastrophe (DB corrupt) = re-run the walk once (~58 min); the index is
   class C_regenerable by the estate's own 2026-09-26 audit classification
   (scripts/_w2l1_disk_map.py:44).

## 6. Dry-run tool spec: tools/estate_index_compact.py

Modes and exit codes follow the estate convention (0 ok, 1 drift/divergence, 2 error).
Nothing below mutates estate data except --apply, and --apply refuses to run unless
--check and the sqlite parity gates passed in the same invocation or a fresh prior one.

- --check (default, READ-ONLY, the first command anyone runs):
  - jsonl facts: size, row count (full chunked count, instrument named in output),
    duplicate path count, top-10 top2 prefixes, byte share of each skip-list root.
  - projection: rows and bytes that WOULD remain under the skip list (from the measured
    pass, not estimates).
  - mirror state: reuse tools/estate_index_dedup.py check_pair (dup / deduped /
    divergent).
  - git state: both copies tracked? dirty? blob size (git ls-files + cat-file -s).
  - reader inventory: hard-coded list of the R1-R4/R6 call sites
    (server.py:624, the_index.html:118, librarian.py:39, estate_atlas.py:35,
    battery_rerun.py:51); each site is grepped for its expected token; a changed set
    exits 1 with the diff named - a new reader cannot silently appear mid-migration.
  - schedule state: task "Estate Spine Index" present, last fire, last_run.json age.
  - exit 0 = facts stable and consistent (row count == last_run total_files within 0);
    exit 1 = drift (counts disagree, reader set changed, mirror divergent); exit 2 =
    missing files / errors.
- --build-sqlite (no cutover): stream the jsonl into a temp DB (%TEMP%), then verify:
  row parity (DB count == jsonl count minus skip-list rows), per-proj counts equal
  rollup.json per-proj counts for non-skipped projects, spot-check 100 random paths by
  field-equality against the jsonl, print DB size vs jsonl size. Leaves the DB in
  %TEMP% and prints its path; touches nothing under watch/.
- --build-sqlite --apply: same build into watch/ESTATE_INDEX/estate_index.sqlite-new;
  on ALL gates green: bank sha256 of both jsonl copies (dedup_shas.json format), rename
  -new over the live DB name (atomic os.replace, same-volume; the estate_index_dedup
  WinError-5 retry lesson applies), swap the mirror pointer via the existing dedup
  tool's --apply, write the runs row (source='jsonl-migration', skipped_roots=[...]),
  file the receipt under watch/inbox/. Any gate red: nothing under watch/ is touched,
  exit 1, the failed gate is named.
- --verify: re-run parity between the live DB and the archived jsonl (read-only).
- --dry-run-walk: simulate the new writer's walk (os.walk with the skip list, NO
  writes) and report projected rows/bytes + runtime, so the operator sees tomorrow's
  numbers before the task is ever repointed.

## 7. Migration plan (phases, never-lossless-order)

- P0 (done tonight): this design; no execution.
- P1 operator decisions (see section 9), then a watch/inbox receipt recording them.
- P2 tools/estate_index_compact.py --check, then --build-sqlite (temp). Both read-only
  against estate data. Numbers filed.
- P3 cutover of the artifact: --apply (DB lands, mirror becomes pointer, shas banked,
  cold archive of the master written once: watch/ESTATE_INDEX/archive/
  ESTATE_INDEX.jsonl.pre-sqlite-20261004 + its sha256 sidecar).
- P4 writer change (tools/index/projects_index.py): skip list honored; sqlite upsert
  path; rollup.json/last_run.json shapes unchanged; during a one-week transition it
  ALSO writes a thin jsonl export (post-skip rows only, ~437 MB -> smaller daily) so
  unported readers keep working on real data. Task "Estate Spine Index" keeps its
  action unchanged (same script path).
- P5 reader ports, in cost order: R2 the_index.html -> new bounded door
  /api/v1/estate/query?q=&proj=&rel=&limit= (LIMIT-capped SQL; the server already has
  the bounded-tail precedent at server.py:592-610); R1 /data door -> keep during
  transition, then 410 with pointer to the query door; R3 librarian --coldload ->
  sqlite prefix/LIKE query (or FTS5) for its 120 keyword slices; R4 estate_atlas ->
  SQL aggregates (one GROUP BY replaces 8.8 M json.loads); R6 battery_rerun ->
  integrity = DB page_count + runs-table content sha instead of a 3.2 GB digest.
- P6 retirement: stop the thin jsonl export; git rm --cached both jsonl paths (they
  are class C_regenerable; committing them contradicts the estate's own audit
  classification) + .gitignore entries; update the dedup tool's default pair to
  point at the archive + pointer for its --check history mode.

## 8. Rollback story

Every phase has a named rollback because nothing is deleted:

- After P3/P4: repoint the writer to legacy mode (one flag in projects_index.py; the
  jsonl write path is kept in-tree, not deleted) and restore the master from the cold
  archive if the current one is thin (sha256 sidecar verifies byte-identity with the
  2026-10-03 state). The mirror pointer's rollback is tools/estate_index_dedup.py's
  banked shas.
- After P5: each reader port is an independent revert; the /data door can be re-enabled
  from the archive copy alone.
- The DB itself needs no rollback story beyond sqlite's own durability: worst case,
  delete it and re-walk (~58 min) - the estate's source of truth never moved.

## 9. Operator decision points

1. Skip list contents. Recommendation: .mimosa (the 87.2% win), .venv, venv,
   node_modules, __pycache__. Open call: .git (currently the walk catalogs ancestor
   .git dirs and the repo's own; if "body file" relations over .git internals matter
   to the atlas, keep .git in and accept ~+10-15% rows).
2. DB in git or not. Recommendation: NOT tracked (regenerable; provenance in runs
   table + receipts). The alternative (commit a ~200-350 MB binary) re-creates the
   blob-churn disease at smaller scale.
3. Retirement of the jsonl pair from git (git rm --cached + .gitignore) and whether to
   schedule the existing big-blob history purge work separately (the 2.52 GB blob
   cb136109 and its ancestors stay in .git until that purge - this design does not
   touch git history).
4. FTS5 at landing or LIKE-prefix first. Recommendation: LIKE/prefix first (librarian
   needs substring hits on path; measure first, add FTS5 only if query times hurt).
5. Tombstone retention N (default 30 runs) for the vanished-rows record.
6. Timing of the R2/R1 port (the browser whole-file fetch is the worst live reader;
   earliest port = earliest real relief).
7. One-week thin-jsonl transition window: confirm or shorten.

## 10. File map (absolute paths, for the next seat)

- Writer: C:\Users\foste\Documents\projects\local_sovereign_agent\tools\index\projects_index.py
- Seed twin: C:\Users\foste\Documents\projects\local_sovereign_agent\seed\engines\spine_walk.py
- The file (do not modify casually): C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\data\ESTATE_INDEX.jsonl (mirror) + C:\Users\foste\Documents\projects\local_sovereign_agent\watch\ESTATE_INDEX\ESTATE_INDEX.jsonl (master)
- State: watch\ESTATE_INDEX\last_run.json, rollup.json, ESTATE_INDEX.jsonl.dedup_shas.json
- Readers: dashboard\server.py, dashboard\static\the_index.html, dashboard\static\frontdoor\index.html, scripts\librarian.py, tools\estate_atlas.py, tools\gap_sentinel.py, tools\battery_rerun.py, tools\estate_index_dedup.py, scripts\build_knowledge_graph.py
- Sentinel evidence: logs\gap_sentinel.log, logs\gap_sentinel\history.jsonl, logs\gap_sentinel\alerted.jsonl
- Disk audit prior art: memory\audit_20260926\w2l1_disk.json, scripts\_w2l1_disk_map.py
- Scheduled tasks: "Estate Spine Index" (the writer), "MagGapSentinelDaily" (the alert), "EstateWalkDaily" (a different thing: bakes the estate walk page, scripts\estate_walk_daily.ps1)

Instruments used tonight (all read-only, .venv\Scripts\python.exe): full chunked row
count + exact dup detection (89 s pass), ext/prefix probes (25 s + 33 s), head/tail
line reads, git ls-files/cat-file/status, schtasks query, gap_sentinel log/history
reads. The 3.2 GB file was read, never written.
