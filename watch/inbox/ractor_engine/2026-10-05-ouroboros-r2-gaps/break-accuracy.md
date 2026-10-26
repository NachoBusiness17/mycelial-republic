# BREAK-ACCURACY pass, OUROBOROS R2 gap surface (2026-10-05)

Hostile second pass on the gap-surface lens report. Sitting window 2026-10-05
08:13-08:30 ET (12:13-12:30Z). Instruments actually run this sitting, all
read-only: ls with full-iso mtimes; git ls-files -s; git cat-file -s; git
hash-object on both 2.5GB copies; git reflog --date=iso; git stash list; git
stash show --name-only stash@{0}; powershell Get-ScheduledTaskInfo +
Get-ScheduledTask for Estate Spine Index and MagFreeLaneFleet; python census
of memory/percolator/candidates.jsonl (29 rows, 12 token greps); python census
of memory/runs/free_lane_fleet/ledger.jsonl (40 rows); citation_lint check
--files on the two ribs; grep for "unconfirmed" across all 7 exec checks
files; python row-count of all 8 exec lane files; full reads of
tools/free_lane_fleet.py, tools/index/projects_index.py (150-214),
tools/mickey17_v2_fold.py (150-209), dashboard/server.py (160-219),
scripts/free_lane_fleet_cycle.ps1, logs/free_lane_fleet.log,
watch/ESTATE_INDEX/last_run.json, e01/e02/e05 lane files,
watch/inbox/build_wave_20261005/b9_doors_tier.md (28-57),
corpus/steal/MASTER_READ_ESTATE.md (219-251),
watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl (10 rows
listed). Not run: the fold script, the index writer, any pytest, any live API
call, workflow run introspection (ListWorkflowRuns returned
workflow_introspection_unavailable in this session).

## VERDICTS

### F1 ESTATE_INDEX compaction cure broken in production: CONFIRMED (strengthened past the lens's evidence)

Every byte the lens cited reproduces, and two inferences are upgraded to
byte-proof:

- Sizes and mtimes: dashboard/data/ESTATE_INDEX.jsonl 2,523,006,985 B at
  2026-10-05 06:57:52 -0400; watch/ESTATE_INDEX/ESTATE_INDEX.jsonl same size
  at 06:58:02 (ls, this sitting).
- Content identity, new this pass: git hash-object on BOTH copies returns
  cb136109569bcf8f7095dc3c310c72dc7a0e35cd, exactly the HEAD blob
  (git cat-file -s = 2,523,006,985; last commit touching it 5d2263f10
  2026-10-01 20:46:30 -0400). The lens had blob-length only; the rewrite
  restored the literal 10-01 content, both copies.
- Pointer absent: ls ENOENT on dashboard/data/ESTATE_INDEX.pointer.json and
  watch/ESTATE_INDEX/ESTATE_INDEX.pointer.json; the committed writer writes
  it unconditionally (tools/index/projects_index.py:198).
- Writer state stale: watch/ESTATE_INDEX/last_run.json mtime 2026-10-04
  14:29:00, content ts 2026-10-04T18:28:51Z, predates the skip-list code, no
  skipped_skip_list field.
- Door hardcode: dashboard/server.py:188 ESTATE_INDEX_PATH = DATA /
  "ESTATE_INDEX.jsonl"; grep "pointer" over server.py returns zero lines.
- Task state: Estate Spine Index LastRunTime 10/4 9:00 AM, NextRunTime
  10/5 9:00 AM, LastTaskResult 0. At this sitting (08:15 ET) the 10/5 fire
  has NOT happened, so "the skip list has never fired on a live walk" held
  byte-true at check time. The 9:00 fire runs the new committed code (task
  action is the repo venv python on tools/index/projects_index.py) and will
  rewrite the watch master, refresh last_run.json, and mint the pointer, but
  it will never touch the dashboard copy again, so the door-vs-writer split
  survives the fire. The repoint (door default to the watch master, or
  pointer-following) is the durable close either way.
- The 06:57 actor, upgraded from inferred to byte-corroborated: stash@{0}
  exists on base 23d76bb71 (committed 06:48:04); git stash show --name-only
  stash@{0} lists BOTH dashboard/data/ESTATE_INDEX.jsonl and
  watch/ESTATE_INDEX/ESTATE_INDEX.jsonl; a stash-create resets those modified
  files to HEAD, which is exactly a 06:57 rewrite to cb136109; the recovery
  commit 9d3b4b572 (07:05:16, "recovered byte-exact from stash@{0}") names
  the same stash. The exact shell command is still unlogged (stash-create
  writes no HEAD reflog line); that residue of the OWED is a formality, the
  attribution is no longer guesswork.
- Executor contradictions confirmed: e01-index-compact.json row 3 (line 27)
  claims "The frozen 2026-10-04 dashboard copy was never opened for write and
  stays on disk"; that copy now hashes to the 10-01 blob with an 06:57 mtime.
  e02-index-query.json notes (line 55) "today's walk already produced
  10,661,260 rows"; both copies now hold the 10-01 content instead. e01 row 2
  (line 21, "live proof lands at the next scheduled walk's last_run.json
  skipped_skip_list field") is still pending and the 9:00 fire is its
  tripwire moment.

Clause correction, not a kill: "5.05 GB duplication back" is the current
state; after the 9:00 fire it becomes one fresh master plus one permanently
stale 2.52 GB dashboard copy until the door is repointed.

### F2 Ten frontier_olm_2026-10-04 candidates never entered the master store: CONFIRMED (CONVERGENT, fence discharged)

- Census rerun wider than the lens's: memory/percolator/candidates.jsonl has
  29 rows; grep for "frontier_olm_2026-10-04" = 0 hits; case-insensitive
  grep for 11 distinctive tokens (AQLM, two-clause, REGEXROUTE,
  fetch-before-bank, KV-prefix, TV-flip, addressability, Goodhart,
  not-fine-tuning, intrinsic-motivation, merge-turn) = 0 hits each, over the
  full serialized rows (all fields, not just the file field).
- The window file holds exactly 10 rows, read in full this sitting; claims
  match the lens's named list (addressability, Goodhart/Z15 extension,
  TV-flip, token-prefix validity, FETCH-BEFORE-BANK, open-answers round 2,
  intrinsic-motivation pair, two-clause AQLM rule, centralized merge turn,
  three-mechanisms card).
- e05 byte-verified: e05-transfer-debt.json before_state rows 19, after_state
  29 with all 10 new rows LINKS-sourced (candidates_filed cites only
  watch/inbox/LINKS.jsonl lines), idempotence rerun n_dupe 10.
- The b9 fence is retired: watch/inbox/build_wave_20261005/b9_doors_tier.md
  lines 39-42 hold the row verbatim ("Another live workflow owns
  memory/percolator/candidates.jsonl writes this window... Owed to that owner
  or the next window"); that window closed, and the next owner-window (e05)
  filed only the r07 list. CONVERGENT per the lens's own flag: b9 receipt +
  e05 scope + this pass's greps.
- Executor-fence check the lens left conditional, now discharged: the
  remaining register rows are 7 items 2+3 (trail cure units), 8 (catalog
  rescan), 9 (research lane consumption verdict), 10 (falsification receipt
  plus fold-gate check), per corpus/steal/MASTER_READ_ESTATE.md:229-232.
  None is a percolator ingest. The gap is unfenced and unowned; the 20-minute
  sanctioned-writer close stands as written.

### F3 Fleet probe battery re-fires the same last-12 rows every 30 minutes forever, blind to window files: WEAKENED (structure confirmed, live behavior claim false, replaced by a worse finding)

Code cites all reproduce: tools/free_lane_fleet.py is 332 lines, CANDIDATES
constant at :54, probe_items at :158 reading rows[-12:] at :168, retire logic
unlinks only QUEUE.glob("*.json") at :301-304, and the only globs in the
module are queue globs (no window-file glob anywhere). Commit e80f48b8f
(2026-10-05 03:36:34 -0400) and the 30-min task both check out
(StartBoundary 2026-10-05T03:03:00, fires on :03/:33).

But the falsifier census the lens named and did not run, run this sitting,
kills the headline behavior: memory/runs/free_lane_fleet/ledger.jsonl holds
40 rows, ALL timestamped 2026-10-05T06:47:58Z through 07:01:51Z (02:47-03:01
ET, the manual pre-commit validation cycles). ZERO rows from any task fire.
All 20 probe rows carry ONE work_id, "probe-DROP-SCHMIDHUBER-COMPRESSION"
(20x): only one store row has both claim and falsifier/amended_metric fields
(:169-172), so the battery is a single probe, not "the last-12". And the tail
tracks the store (it moved when e05 grew 19 to 29), so "forever" overstates.
The task-driven loop the finding describes does not exist in production: see
addition A1; every one of the 10 scheduled fires died before python could
resolve the module.

The dedupe half is confirmed in the only cycles that ever ran (20 fires of
one probe id, zero queue work, zero rotation), and the window-blindness half
is confirmed by code. The verdict is weakened because the finding prices a
30-minute repetition that is not occurring; the repair order inverts (fix the
dark loop first, then rotation matters).

## ADDITIONS (what the lens missed)

### A1 The 24/7 fleet is DARK in production: every scheduled fire fails, green the whole way

Evidence: logs/free_lane_fleet.log lines 1-10 show ten fires, 07:33:04Z
through 12:04:16Z, every one "ModuleNotFoundError: No module named 'tools'".
scripts/free_lane_fleet_cycle.ps1:10 runs `& $py -m tools.free_lane_fleet
--cycle` without ever Set-Locationing to the repo; Task Scheduler starts in
System32, so -m cannot resolve the package. The ps1's own header
(free_lane_fleet_cycle.ps1:2-4) names this exact class (EstateWalkDaily
lesson) and fixed only the interpreter path, not module resolution. The
try/catch at :12 never fires (a nonzero native exit does not throw in
PowerShell), so Get-ScheduledTaskInfo reads LastTaskResult 0 (green) at
LastRunTime 10/5 8:03:03 AM while the ledger has banked nothing in 5.5+
hours. The e80f48b8f commit claim "registered + verified (03:33 first fire)"
is contradicted: the 03:33 fire is log line 1 and it failed; verification was
task-exists, not banking. Same class as R1's vacuous green G8.
Falsifier: any ledger row timestamped at a fire moment, or a log line
carrying "FREE-LANE CYCLE" output from a scheduled fire.
Move: one sitting, 10 min: add `Set-Location $repo` before the -m call (or
invoke the file path directly), wait one fire, byte-check ledger growth at
fire timestamps; land a liveness tripwire on ledger mtime age beside the FTS
daily's no-START-stamp-means-dark law so a green-but-dead task cannot hide.

### A2 The 10-04 walked index content survives only inside stash@{0}

Evidence: git stash show --name-only stash@{0} lists both
dashboard/data/ESTATE_INDEX.jsonl and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl
(plus catalog files, trails, REGISTRY, proofs); both working copies now hash
to the 10-01 blob cb136109. The 4.15GB / 10,661,260-row walk of 10-04 (which
e01 profiled and e02 served) exists nowhere on the working tree; the stash
snapshot is its only copy. Regeneration at the 9:00 fire is by design
mimosa-pruned, so the full row mass is not regenerable.
Falsifier: `git stash drop` or a stash clear (then it is gone entirely); or
materializing the stash and finding different content.
Move: fold into F1's sitting: decide recover-vs-regenerate before any stash
GC; the decision is one sentence in the F1 receipt.

### A3 The executor is 5h40m+ cold on lane landings; the fence column is claim, not bytes

Evidence: memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ holds e01-e08
only, newest mtime 02:38 ET (e06-fidelity-audit.json); no manifest or state
file exists in the run dir beside lanes/; e09-e12 (register rows 7 items 2+3,
8, 9, 10) were absent at every check this sitting. ListWorkflowRuns is
unavailable in this session (capability gap), so run-state cannot confirm
in-flight lanes; disk truth is 8 of 12 landed, silent for 5h40m+.
Falsifier: e09+ lane files appearing (executor alive, just slow), or a
run-state source showing the run stopped (then rows 7i2+3/8/9/10 are orphaned
and must be re-gapped next window).
Move: no code; the R2 closure table's blocked-by column should read
"executor-fence CLAIMED (ask), lanes cold 5h40m+, not byte-confirmed live".

### A4 Blind-spot counts now byte-backed, two cite drifts caught

- blocking PHANTOM-NUMBER recount, run this sitting:
  `.venv/Scripts/python.exe tools/citation_lint.py check --files
  memory/rib/RIB_INFERENCE_BUDGET_20261001.md
  memory/rib/RIB_MODEL_GARDEN_ROUTING.md` -> "FAIL records=2 anchors=1
  numbers-checked=25 blocking=7", six in RIB_INFERENCE_BUDGET_20261001.md
  (:27 x3, :32, :36, :41) plus one in RIB_MODEL_GARDEN_ROUTING.md:158. The
  carried "7" is now byte-backed.
- The exec fold's "excluded: 0" prediction, mechanism-verified without
  running the fold: all 8 lane files carry exactly 5 rows (no single-row dead
  lanes) and all 7 checks files grep zero "unconfirmed" keys, so the excluded
  Counter at tools/mickey17_v2_fold.py:184-193 stays empty and line 198
  prints "excluded: 0". Cite drift: the print is :198, not :181 (:181 is
  inside the unconfirmed-collection loop of the same block). No
  FOLD_SECTIONS.md exists under the exec run dir: the fold has not fired.
- providers.yaml (in-repo at configs/providers.yaml, not operator-side):
  lines 195-196 carry inclusionai/ling-3.0-flash-fin:free stamped "B2-202
  gate PASS 2026-09-26 (200, ALIVE)", 9 days stale; the e03 404 residual is
  still unlive-verified (no API call made this sitting). Adjacent byte:
  fleet health.json shows openrouter-free-1 (model ling-3.1-flash per
  tools/free_lane_fleet.py:113, a different id than the yaml rows) at
  consecutive_fails 2.
  Falsifier: a live chat call returning 200 on ling-3.0-flash-fin:free kills
  the staleness concern; the yaml stamps aging past every free lane's
  re-verify window confirms a currency-sweep amendment is owed.
  Move: fold into the fleet's sitting: a model-currency sweep of PROVIDERS
  against a live probe, stamped with date, same shape as B2-202.

## Feed for the fleet work-generator amendments (the ask's instrument clause)

1. Precondition: A1's ps1 fix; no generator amendment matters while the loop
   cannot resolve its own module.
2. Liveness as a first-class probe: the fleet should bank a heartbeat row per
   cycle even when providers are dead, and a tripwire should flag
   ledger-mtime age, so task-green-but-dark is visible without reading logs.
3. Rotation: consume probed work_ids from the ledger tail instead of
   re-reading rows[-12:] each cycle; currently one probe (the only store row
   with claim+falsifier fields) would absorb every fire.
4. Qualification breadth: 28 of 29 store rows lack falsifier fields; either
   the percolator writer requires a falsifier on ingest or the probe battery
   falls back to claim-only asks, else the "candidates owe probes" surface is
   1/29 of the store.
5. Window sensing: a glob over watch/inbox/**/percolator_candidates.jsonl
   (ingest-pending windows) turns F2-class gaps into a fleet-visible signal;
   the sanctioned writer stays the only ingest path.

## NOT RUN (named, not substituted)

The fold script itself, the index writer, any pytest subset or suite, any
live provider API call, workflow run introspection (tool unavailable in this
session). Every claim above cites bytes read or commands run this sitting;
nothing is carried from the lens without re-derivation except where explicitly
marked (the ask's own assertion that rows 18-19 of the store are the
Schmidhuber metric rows).
