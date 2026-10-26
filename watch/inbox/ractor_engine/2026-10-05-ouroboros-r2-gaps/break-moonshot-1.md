# HOSTILE PASS: break-moonshot-1 (2026-10-05, ouroboros round 2)

The hostile second pass over lens moonshot-1. Every byte below was executed
this sitting by this seat (instrument named per claim). Note: the lens report
as delivered was TRUNCATED mid finding 3's move ("max_con..."), so any finding
below rank 3 was not visible to this pass; verdicts cover the three received
findings plus the six blind spots.

## VERDICTS

### FINDING 1 (RANK 1, ESTATE_INDEX unstamped rewrite): CONFIRMED, two evidence bytes corrected, severity UPGRADED

Confirmed bytes (my instruments):
- Both copies exactly 2,523,006,985 B, mtimes 2026-10-05 06:57:52 (dashboard)
  and 06:58:02 (watch) EDT (PowerShell Get-Item, this sitting).
- last_run.json stale at ts 2026-10-04T18:28:51Z, and the full JSON I read
  carries NO skip-list key (e01's code stamps `skipped_skip_list` at
  tools/index/projects_index.py:180; its absence proves the running writer was
  not e01's code).
- dashboard/data/ESTATE_INDEX.pointer.json absent (Test-Path False; grep -i
  pointer over dashboard/data/ rc=1).
- New master still carries massive .mimosa content: 378,529 byte-occurrences
  of b'.mimosa' in the first 200MB (python chunk.count). The lens's 354,495 is
  the line-count instrument; both support the ~350K+ claim.

Corrections (bytes that do not reproduce):
- The first-1MB sha256 computes 2ca872e434dffd41 on BOTH copies (python
  hashlib), not 6f62bbb1 as the lens banked. The copies ARE identical to each
  other (identity claim holds); the cited digest value does not reproduce.
- The mtime-to-path assignment is reversed: watch = 06:58:02, dashboard =
  06:57:52 (the lens listed them in the other order).

Severity upgrade (new bytes the lens did not have):
- wc -l on the new master: 6,584,869 rows. The Oct-4 walk it replaced indexed
  10,661,260 files (last_run.json total_files). 4,076,391 rows vanished.
- The new master's FIRST row (rows sort by mtime_epoch descending at
  projects_index.py:150) carries mtime 2026-10-01T14:08:16Z. The newest row in
  the "fresh" 06:58 master is four days old. This is not a compaction and not
  a walk: it is a REGRESSION that installed ~Oct-1-era content over the Oct-4
  walk. Neither e01's skip-list profile (~1.13M rows if fully pruned) nor the
  pre-e01 full walk (10.66M rows) matches 6.58M.
- Write ORDER contradicts every version of the walker: dashboard 06:57:52 then
  watch 06:58:02. projects_index.py writes MASTER (watch, :40, :154) first in
  every version; the old code then copyfile'd to DASH_MASTER, the new code
  never writes the dashboard master at all. No version writes dashboard first.

Falsifier re-checked and survived: no last_run or walk log stamped 06:57-07:00
exists; last_run.json was still stale at my read. The writer remains
unattributed. Nearest known writer-by-timing: the spore-sharing fleet
(dwfrun-27c7e7b2, launched 06:56 EDT, args read this sitting from
.zcode/workflow-runs/dwfrun-27c7e7b2-5fcf-489d-9d81-341b7b2f3bf5.mjs) whose
lenses demonstrably wrote mangled-path files into the repo root at 07:03:46
(%TEMP%spore_ci.txt), 07:03:54 (%TEMP%spore_state.txt), and 07:37:44 (two
C:UsersfosteAppDataLocalTempspore_ls*.txt files) (my stats). That is a
suspect window, NOT a verdict; no byte names the index writer.

The lens's one-sitting close stands, amended: run
.venv\Scripts\python.exe tools/estate_index_compact.py --check on the new
master, bank the profile PLUS the newest-row regression (first-line mtime vs
last_run ts) to the r2-gaps receipt, then fire the sanctioned walk once under
the current projects_index.py so last_run + pointer stamp a writer. Blocked-by:
none.

### FINDING 2 (RANK 2, fold cannot count itself): CONFIRMED, and the executor-fence is VOID

Confirmed bytes (my runs):
- grep -c deep_tier2 tools/mickey17_v2_fold.py = 0.
- fold :181 reads `for x in (c.get("unconfirmed") or []):` (grep -n) and :191
  banks excluded["9 verifier-unconfirmed"]; the verifier table counts every
  list-valued key (my read of the vc loop) while PRISMA consults only the
  "unconfirmed" key no runner writes.
- Runners persist tier-2 verdicts as deep_tier2 into <id>.checks.json (my sed
  of .zcode/workflows/mickey17-v2.dwf.ts:274-290, the TIER-2 PERSIST phase).
- run-0's FOLD_SECTIONS.md byte-exact at the cited lines: :27 "- verdicts:
  checks 15, deep_tier2 16, rows 10, supports 50" and :40 "- excluded: 0" (my
  sed -n '25,42p'). The same file counted 16 deep_tier2 verdicts and excluded
  zero of them.
- CONVERGENT x3 re-checked at the R1 leg: R1 SYNTHESIS.md:97 row 1 carries the
  identical edit; both spec addenda not re-read this pass (carried).

Fence correction (new bytes): the blocked-by "executor-fence (e12 edits the
same file)" is void. The executor dwfrun-e9656e14 has been DEAD since
02:37:56 EDT: its newest session file across all 8 actor dirs is
2026-10-05+02:37:56 (my find over
/c/Users/foste/.zcode/cli/exec/sess_dwf-dwfrun-e9656e14*); lanes e09-e12 never
landed (lanes dir holds only e01-e08, newest mtime 02:38:45); and
tools/mickey17_v2_fold.py is untouched since 2026-09-25 19:21 EDT (my stat).
No competing editor exists. The close is unblocked NOW.

Adjacent fact: R1 row 2 (tier-1 merge fix) IS landed in the saved workflow
bytes (my sed of mickey17-v2.dwf.ts:150-152, "keep every existing key verbatim
(including deep_tier2)"), so the writer side no longer destroys tier-2
verdicts while the counter side stays blind. The asymmetry makes R1 row 1 the
sole remaining leg.

### FINDING 3 (RANK 3, zombie certificates + unjoinable fires): WEAKENED (timeline inverted, mechanism bytes stand)

Confirmed legs (my runs):
- sed -n '75p' memory/workflows/REGISTRY.jsonl: ts 2026-10-04T02:34:06Z,
  tree-doctrine-dig.dwf.ts, verdict PASS, byte-exact as cited.
- grep -cE 'stop-cert|FIRE_LEDGER' tools/workflow_gate.py = 0.
- e04's G8 card landed at tools/workflow_gate.py:94-97 (my sed); e04 lane file
  mtime 01:46 EDT (my ls); suite 9 cards green per e04 lane row 4.
- Fire journal census RE-RUN with an unbroken instrument (the R1-era "rc=0
  zero readers" greps were pipe-broken; this pass ran grep without head):
  grep -rln "workflow-runs" tools/ mag/ returns nothing, rc=1. The journal now
  holds 112 dwfrun records (my ls count; R1 said 110, the dogfood 101) and
  still has zero readers.

Broken leg (bytes): "mints ... PASS ... two days after the 10-02 fleet
retirement verdict" is false on every readable anchor. The retirement
verdict's own artifact is stamped "moment 2026-10-04" (git show
a53b101d4:watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/SYNTHESIS.md,
line 3) and the commit's author AND committer dates are both
2026-10-04T05:19:00Z (git log -1 --format). The cert at 2026-10-04T02:34:06Z
PRECEDES the verdict's authoring and its commit by ~2h45m; the cert rode the
dogfood run's own 12-row zero-launch PASS sweep BEFORE the verdict existed.
R1 SYNTHESIS.md:80-81 ("postdating a53b101d4") was already inverted and the
lens inherited it while re-checking only the registry row, not the commit.

The surviving defect is real but differently shaped: now that the verdict HAS
landed, nothing strikes or annotates row 75 (no stop-cert bytes exist to do
it), so a retired script still presents a fresh PASS cert, and no artifact
joins fires to width. The one-sitting close (stop-cert clause + scenario card
+ FIRE_LEDGER append) remains valid; the evidence row's ordering claim must be
rewritten as "cert stands unstruck after the death verdict; nothing connects
verdict to certifier", not "minted after the verdict".

## BLIND SPOT SETTLEMENTS

1. Executor wave-2 liveness: SETTLED, DEAD since 02:37:56 EDT (instruments
   above). Register rows 7-cures-2/3, 8, 9, 10 (the e09-e12 assignments)
   reopen unowned. The lens's fear was correct and worse than feared: not
   "unknown", but dead 6.5h before this pass with no instrument having
   noticed.
2. Rewrite attribution: still unattributed; suspect window named above
   (spore fleet). OWED: the actual writer.
3. Fire-journal census: re-run this pass (112 records, zero readers).
4. Cache plumbing: models/quota.py:75-83 record_usage(cache_hit_tokens,
   cache_miss_tokens, session_id) exists and mag/tesuji_fire.py:146-149 stamps
   cache fields with session_id=SEAT (a seat constant, not a frozen API
   session prefix). The deepseek ds_workhorse session-prefix trace remains
   OWED (not traced this pass).
5. e02/e06/e07/e08 mined by this pass (see additions); e07 row 4's
   citation-lint blocker is NOW GREEN (I ran the exact reproducer:
   .venv/Scripts/python.exe tools/citation_lint.py check --changed =>
   "ok records=9 blocking=0"). Do not re-mine it.
6. Fleet ledger duplication reproduced and WORSE: last 40 rows of
   memory/runs/free_lane_fleet/ledger.jsonl hold 5 distinct work_ids, 35
   duplicate rows (python Counter; lens measured 20-of-40).

## ADDITIONS (what the lens missed, ranked)

1. EXECUTOR DEATH + ORPHANED ROWS (verbs, high): the 12-lane map will never
   complete; rows 7-cures-2/3, 8, 9, 10 of the curiosity register are
   unowned. Move: lift every executor-fence in the R2 close list and re-rank
   those rows (~15 min re-dispatch decision; the sittings are the rows
   themselves). Falsifier: any e09+ lane file or e9656e14 session activity
   after 02:38 EDT (none exists at pass moment 09:0x).
2. ESTATE_INDEX CONTENT REGRESSION (bytes, high): newest row 2026-10-01T14:08:16Z,
   6,584,869 rows vs 10,661,260 in the replaced walk; dashboard now serves
   4-day-stale index. Fold into RANK 1's close: the recheck receipt must diff
   first-line mtime vs last_run ts, and the incident class is regression, not
   stamp gap. Falsifier: a walk log naming a legitimate 06:57 run whose output
   excludes Oct 2-4 rows (none found).
3. UNMINED LANE STEALS = CHEAPEST OPEN CLOSES (verbs, high, from the lanes the
   lens admitted not reading): (a) e06 row 2: all 131 SEED.json tape_refs
   point at the dead 102-row tape; cure = repoint mag/worldline_seed.py:84
   TAPE at the live stream (mag/trajectory_step.py:50) + regression test
   (~25 min); (b) e08 row 5: two live O_TRUNC siblings in the cured errno
   family, mag/lane_runner.py:161-165 (_mirror trail writes, live hit
   2026-10-05T03:59:15Z) and mag/prose_census.py:145; cure = the proven
   tmp+replace pattern from mag/lane_runner.py:124-149 (~25 min). Falsifier:
   those files already carrying the fixes (they do not; e08 banked the
   residual as open).
4. REGISTRY APPEND-ONLY CONTRACT ANOMALY (bytes, medium):
   memory/workflows/REGISTRY.jsonl mtime 2026-10-05 06:57 with last stamped
   row ts 2026-10-05T05:20:28Z (my stat + tail) - the append-only file was
   modified 1.6h after its last append, same minute as the ESTATE_INDEX
   rewrite. Move: hash-bank the 88-row tail in the R2 receipt; add a tail-hash
   probe. Falsifier: a row stamped later than 05:20:28Z appearing (then the
   touch was an in-flight append).
5. FLEET PROBE AMENDMENTS (feed the instrument, medium-high):
   tools/free_lane_fleet.py probe_items (:158+) draws probes ONLY from
   memory/percolator/candidates.jsonl rows[-12:] falsifier/claim fields (my
   read). Today's two silent failures (a 1.63GB unstamped regression live for
   2+h; an executor dead 6.5h unnoticed) are both outside its sensing surface.
   Move (~20 min): append candidate rows whose falsifiers encode (a) ESTATE_INDEX
   coherence: master mtime vs last_run ts staleness, newest-row regression,
   twin-copy divergence; (b) dwfrun liveness: lane-archive stall vs expected
   lane count; (c) REGISTRY tail hash; (d) dead-pointer census (worldline
   tape_ref class). Falsifier: any standing probe already covering one of
   these classes (none; work assembly is queue + corridor + candidate probes
   only, my sed :255-300).
6. FLEET LEDGER DUPLICATION WORSENED (defects, medium): 35-of-40 duplicate
   rows vs the lens's 20-of-40. The retirement reader scans only the last 40
   lines with a 900s cutoff (tools/free_lane_fleet.py:291-299) while banked
   duplicates accumulate. Move: retire by work_id at bank time or widen the
   read window (~20 min). Falsifier: a fresh census under 20 after one fleet
   cycle with a replenished queue.

## The one-line truth

The lens's two byte-level anchors (fold blindness, index rewrite) survive
hostile fire with corrections; its zombie-cert chronology was inherited
un-checked from R1 and is inverted (the cert preceded the verdict); and the
estate changed under everyone: the executor died at 02:38, R1's writer-side
fixes landed at 06:41-06:43, and something regressed the estate's largest
artifact to Oct-1 content at 06:57 while the only append-only ledger in the
loop got touched in the same minute. Every fence built on "the executor will
finish" is void.
