# ACCURACY LENS - OUROBOROS R2: THE GAP SURFACE (2026-10-05)

Filed by lens-accuracy, R2 of 5. Moment window: all reads and runs this
sitting, roughly 10:45Z to 11:30Z (07:45 to 08:30 EDT). Executor state at my
final check: memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ holds e01
through e08 ONLY (16 files, lane JSON plus checks), no FOLD_SECTIONS.md, so
e09-e12 are unlanded and every "not covered" claim below is a moment-read in
the B2-216 sense. Every number below is either from an instrument I ran this
sitting (command named inline) or tagged carried from a named receipt.

## What the executor actually covers (byte-read, not trusted)

I read all 8 landed lane files in full. Landed: register row 1 both units
(e01 compact+skip list+copyfile stop, e02 query door+repoint), row 2 all five
units (e03), row 3 (e04 G8 gate), row 4 (e05 percolator ingest of the r07
top-10, store 19 to 29 rows, idempotence rerun 0 new / 10 dedupe), row 5
(e06 fidelity audit), row 6 (e07 RECEIPT_BINDINGS on mag/dirac_loop.py
bank()), row 7 item 1 (e08 errno-22 writer guard, code leg landed by the
prior night shift, this sitting verified it). Remaining unlanded register
rows at my moment: row 7 items 2+3, row 8, row 9, row 10. The coordinator
commit e80f48b8f (2026-10-05T07:36Z, message "BUILD-IT-ALL WAVE 9/9") already
carries the e01/e02/e03 code (git show stat: dashboard/server.py +153,
tools/estate_index_compact.py +311 new, tools/index/projects_index.py 78
changed).

## FINDING 1 (rank 1): the ESTATE_INDEX cure chain is broken in production,
and two lane files plus a commit message contradict the bytes

My ls this sitting: BOTH dashboard/data/ESTATE_INDEX.jsonl (mtime Oct 5
06:57) and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl (06:58) were rewritten this
morning at EXACTLY 2,523,006,985 bytes each. git ls-files -s shows both paths
at blob cb136109, the same 2,523,006,985-byte blob last committed 2026-10-01
(5d2263f10). The sanctioned writer's state file watch/ESTATE_INDEX/
last_run.json has mtime Oct 4 14:29 (the 18:29Z walk of TS-08), and
dashboard/data/ESTATE_INDEX.pointer.json, which the committed writer code
writes unconditionally (tools/index/projects_index.py:198), DOES NOT EXIST
(ls ENOENT). The Estate Spine Index task's LastRunTime is 10/4 9:00 AM with
NextRunTime 10/5 9:00 AM (powershell Get-ScheduledTaskInfo), so the scheduled
writer has not fired today; its action resolves to
tools/index/projects_index.py with the repo venv (so the 9:00 fire WILL run
the new code).

Contradictions, named: (a) e01 row 3 claims "the dashboard side now gets a
small pointer file" and "the frozen 2026-10-04 dashboard copy stays on disk":
the pointer is absent and the dashboard copy was rewritten this morning.
(b) e02's lane note claims "dashboard/data/ESTATE_INDEX.jsonl rewrites daily
at ~09:00": falsified by e01's own committed copyfile stop plus this
morning's evidence. (c) The 06:57/06:58 mtimes sit 7 to 8 minutes before
commit 9d3b4b572 (2026-10-05T07:05:16-04:00, "the half-failed stash reset
then wiped the working-tree strikes; recovered byte-exact from stash@{0}"):
the most probable writer is that stash/reset event restoring both paths to
the 10-01 blob. OWED, not proven: the git reflog/stash line that names the
actor; my attribution is mtime+size+blob+commit-time inference.

Net state on disk: two independent equal 2.52 GB copies (5.05 GB live
duplication) whose CONTENT is the 10-01 snapshot, that is, 4 days stale,
served to every /api/v1/estate/query request (dashboard/server.py:188
hardcodes ESTATE_INDEX_PATH = DATA / "ESTATE_INDEX.jsonl", and a grep for
"pointer" over server.py returns zero hits, so the door cannot follow the
pointer the writer now writes). This is TS-08's law striking a third time:
"any mirror cure not shipped inside the writer is scheduled litter", now
including git-stash resets as a litter source. CONVERGENT with the r04 lane
and the D1 ruling (both fsutil runs).

Close, one sitting: (1) at or after the 9:00 AM fire, byte-check the
new-code signature: last_run.json gains skip_list_hits greater than 0, the
pointer file appears, the dashboard copy's mtime stays 06:57. (2) Repoint
the door's default to the watch master or teach it pointer-following
(dashboard/server.py:188), since the writer will never refresh the dashboard
side again. (3) Bank the tripwire receipt. Cost: 45 min. Falsifier: if the
9:00 fire produces the full signature AND the dashboard copy stays frozen,
then only the door repoint remains open; if the 9:00 fire writes BOTH copies
again, the task is running stale bytes and the fence moves to the task.

## FINDING 2 (rank 2): 10 stranded candidate rows, the AQLM two-clause rule
included, have never entered the master percolator store

grep -c "frontier_olm_2026-10-04" memory/percolator/candidates.jsonl = 0, and
grep -ci "AQLM|two-clause|REGEXROUTE|fetch-before-bank" over the same store
exits 1 (zero hits). The window file
watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl holds 10
claims (I read them) including the quantization card's two-clause rule (AQLM
sanctioned on non-GGUF swaps, QuIP# barred pending a complex-prompt gate)
whose estate map step 1 explicitly orders filing it "the way rows 15/16 were
filed". b9_doors_tier.md:39-42 HELD that row ("another live workflow owns
candidates.jsonl writes this window"), and e05's transfer-debt execution
filed only r07's top-10 LINKS list, so the held row outlived its fence.
Closure verdict on the ask's owed-list pair: the SCHMIDHUBER half is closed
(rows 18-19 of the store, the selector-port and its amendment, are filed and
were first consumed by e05's BYTES_TO_VERBS fold); the AQLM half is open.

Close, one sitting: run the same sanctioned writer e05 used over the window
file (.venv/Scripts/python.exe -m mag.percolator --candidates
watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl), then the
dedupe rerun, landing spot memory/percolator/candidates.jsonl. Cost: 20 min.
Falsifier: a store grep finding any of the 10 claims already present under a
different file field would void the strand claim; my greps covered the file
field and the distinctive claim tokens, both zero. CONVERGENT (b9 receipt +
e05 scope + my store grep). Blocked-by: none, but confirm e09-e12 are not
percolator lanes before firing (the four remaining register rows are trail
cure 2+3, catalog rescan, research consumption, falsification receipt; none
files candidates).

## FINDING 3 (rank 3, REVISED this sitting after the hostile pass struck the
original claim): the 24/7 fleet loop is DARK in production, 11 consecutive
scheduled fires dead, and the task self-reports success

The original filing here ("re-fires the same last-12 every 30 minutes
forever") is WITHDRAWN as stated: it described code shape, not live
behavior, and the ledger census I named and had not run kills it. I ran the
census this sitting plus every check below.

What I ran: (1) full census of memory/runs/free_lane_fleet/ledger.jsonl:
40 rows total, ALL between 2026-10-05T06:47:58Z and 07:01:51Z (a 14-minute
manual validation window at wave landing), 21 ok / 19 fail, zero rows from
any scheduled fire. (2) Read logs/free_lane_fleet.log in full: ELEVEN
consecutive task fires, 07:33:04Z through 12:33:02Z every 30 minutes, every
one dead on "Error while finding module specification for
'tools.free_lane_fleet' (ModuleNotFoundError: No module named 'tools')".
(3) Read scripts/free_lane_fleet_cycle.ps1: line 10 invokes
`& $py -m tools.free_lane_fleet --cycle` with the venv python named in full
but NO working-directory set; Task Scheduler starts in System32, and
`python -m` resolves modules from the cwd, so 'tools' is unimportable: the
EstateWalkDaily absolute-path law was applied to the interpreter and
forgotten for the cwd. (4) The wrapper cannot throw on this: `& $py ... 2>&1`
with default ErrorActionPreference captures the error text as a normal log
line and the script exits 0, so Get-ScheduledTaskInfo reports
LastTaskResult 0 with NumberOfMissedRuns 0 while every fire is dead: a
silent-pass (the FW-46 class) wearing a green light. The commit e80f48b8f
claim "verified (03:33 first fire)" is true only of the task FIRED, not of
a cycle RUN: that first fire's own log line is a ModuleNotFoundError.

Net: the "24/7 burner" has banked zero production findings in 5 hours of
scheduled operation; its only live rows are the manual validation cycles.
Secondary, still true but moot until the loop is lit (my runs):
probe_items(6) executed read-only returns exactly ONE probe today
(probe-DROP-SCHMIDHUBER-COMPRESSION; of the 29 store rows only rows 17 and
18 carry BOTH claim and falsifier fields, my census, and the rows[-12:] tail
now holds only row 18; the tail tracked the store when e05 grew it 19 to
29, so my original 'forever' was wrong in both directions); the retire loop
(lines 288-306) still unlinks only queue files, never probe work_ids (all
20 probe rows in the ledger share that one work_id); and the battery still
reads only the master store (line 54), blind to window candidate files
(Finding 2's stranded surface).

Close, one sitting, repair order inverted per the hostile pass: FIRST
scripts/free_lane_fleet_cycle.ps1: add Set-Location $repo before the
invocation (or invoke "$repo\tools\free_lane_fleet.py" by absolute path,
the module imports stdlib only so both work) AND make failure loud: check
$LASTEXITCODE after the call and exit it, so the task's green light stops
lying; verify by Start-ScheduledTask by hand and reading a FREE-LANE CYCLE
line plus fresh ledger rows outside the manual window. THEN the two work
amendments from the original filing matter: probe dedupe against banked
ledger work_ids, and window-file sensing
(watch/inbox/*/percolator_candidates.jsonl read-only) in probe_items.
Cost: 20 min for the ps1 fix, 45 min for the amendments. Falsifier: a
green hand-fired task that still leaves the ledger at 40 rows disproves
the fix; a probe_items(6) rerun returning more than one item without a
store change would disprove the one-probe census.

## FINDING 4 (rank 4): the cache-receipt law still has zero producers, so
recv_hit% measures nothing

grep -rl cache_receipt over mag/ and tools/ returns exactly one file,
tools/cache_kpi.py (the reader). The b2 receipt's Owed block ("producers do
not yet stamp cache_receipt on usage rows; recv_tok reads 0 until the first
wired lane lands") is still the whole truth: the law (prefix_receipt.v1,
freeze_receipt, gate_skip_recompute in mag/context_checkpoint.py) exists and
is tested, but no dispatch or flight-recorder call site stamps
cache_receipt.ok plus verified_tokens onto usage rows, so the KPI split
reads nominal 96.6 percent versus 0.0 receipt-verified forever.

Close, one sitting: wire the first producer at the reuse decision point
(the caller of reuse_prefix / gate_skip_recompute; the natural stamp site is
mag/flight_recorder.py api_call around line 322, which already builds the
usage row), then rerun tools/cache_kpi.py and bank the first nonzero recv
reading. Cost: 90 min. Falsifier: a second grep finding a producer, or a
cache_kpi run showing nonzero receipt_tok on today's rows.

## FINDING 5 (rank 5, executor-fenced): the R1 held rows are still open in
bytes, and the exec fold has not fired yet

My greps this sitting: tools/mickey17_v2_fold.py:181 still iterates
(c.get("unconfirmed") or []) with zero deep_tier2 tokens in the file, and no
folded_at stamp; tools/workflow_gate.py carries zero retired / stop-cert /
FIRE_LEDGER tokens; memory/workflows/FIRE_LEDGER.jsonl does not exist (ls
ENOENT). R1's amendment table rows 1, 6 and 7 are therefore all unlanded,
held on the ownership fence (R1 commit 23d76bb71 message). The exec run is
STILL unfolded (only lanes/ exists at my moment), so the fence holds: the
fold script edit must land between the exec fold and the next mega-burn
fire, and the stop-cert plus FIRE_LEDGER edits belong to the gate owner
(R1 refused to mint certificates for retirement candidates, correctly).

Close, one sitting each, the moment the fence lifts: fold-tool de-blind per
R1 row 1 (walk deep_tier2, count unconfirmed into PRISMA code 9, stamp
folded_at plus sha256(script)[:12]); stop-cert clause plus check-time
FIRE_LEDGER append per R1 rows 6+7. Cost: 30 min plus 45 min. Falsifier:
any of the three tokens appearing in the named files. Blocked-by:
executor-fence (exec run in flight).

## Ranked CLOSURE TABLE (amended Schmidhuber metric, store rows 18-19:
primary = carried-history retired plus verbs minted, secondary = defects)

| rank | gap | one-sitting close | landing file | evidence | blocked-by |
|---|---|---|---|---|---|
| 1 | ESTATE_INDEX chain: 5.05 GB duplication back, content 4 days stale, door reads a surface the writer abandoned, skip list unproven on production | post-9:00 signature check + door repoint + tripwire receipt | dashboard/server.py:188; watch/inbox receipt | my ls, schtasks, blob cb136109, pointer ENOENT | none |
| 2 | 10 window candidates stranded (AQLM two-clause class) | sanctioned ingest + dedupe rerun | memory/percolator/candidates.jsonl | store greps zero; b9:39-42 | none (verify e09-e12) |
| 3 | fleet loop DARK: 11 scheduled fires all ModuleNotFoundError, task green (LastTaskResult 0); probe battery 1 probe, no dedupe, window-blind (revised after hostile pass) | FIRST ps1 cwd + $LASTEXITCODE fix; THEN probe dedupe + window sensing | scripts/free_lane_fleet_cycle.ps1:10; tools/free_lane_fleet.py:158-206,:288-306 | ledger census 40 rows all 06:47-07:01Z; log 11 dead fires 07:33-12:33Z; probe_items(6) run = 1 | none |
| 4 | cache-receipt law producerless | wire first stamp site | mag/flight_recorder.py (~:322) | grep single hit | none |
| 5 | R1 rows 1+6+7 held | fold de-blind, stop-cert, FIRE_LEDGER | tools/mickey17_v2_fold.py:181; tools/workflow_gate.py | my greps | executor-fence |
| 6 | 29 already_inside dangling edges (B1 filed-not-fixed) | fix the already_inside builder to emit real module ids | mag/knowledge_graph.py | MY OWN recompute: dangling_now 29, all rel already_inside, graph 2919/1143 exact-match _b1_after.json | none |
| 7 | dead-tape tape_ref: seeds point at the 102-row dead tape | point TAPE at the live stream + regression test | mag/worldline_seed.py:85 (TAPE constant) | my sed read; e06 lane row 2 | none |
| 8 | prose_census in-place write (errno-22 family's prose row) | tmp plus os.replace, mirror of D5 _atomic_copy | mag/prose_census.py:145 | my sed read (write_text in place) | none |
| 9 | seal patrol 21 case-only false drifts | lowercase-normalize both sides at the compare | tools/prepush_seal_patrol.py:124-125 | b7 item 2; my grep (:105 hexdigest, :125 bare ==) | none |
| 10 | rib PHANTOM-NUMBER debt rides committed bytes into the pushed-range pre-push check | accept the 7 by name with the append-never-rewrite rationale | configs/citation_lint_baseline.json | my --files run: findings live in both ribs (count 7 carried from e03/e07) | none (accept-by-name is the owner's call) |
| 11 | GAP_REGISTER rank 1 unannotated though cured | append the FILLED annotation with log cites | watch/inbox/gap_analysis_20261001/GAP_REGISTER.md row 1 | logs/estate_walk_daily.log tail: END 10-03 and 10-04 exit=0 (UTF-16 file, plain grep reads 0: name the instrument) | none |

Also checked and CLOSED by bytes, so no seat should re-fire it: EstateWalkDaily
bake (row 11 above), the Schmidhuber metric consumption (e05's fold), queue
drain Q-005/Q-025 (TS-03, carried), the e01 compact tool's register-truth
counts (all MATCH per its own run, carried), G8 fleet headers (19/19
declare, R1 commit). Do NOT re-open: these carry receipts on disk.

## Blind spots, honestly

- e09-e12 unseen: in flight at my moment; my coverage map of the executor is
  an 8-lane moment-read and the four remaining register rows may land while
  this file is being read.
- The 06:57 index writer attribution (stash/reset restore) is inferred, not
  logged: reflog proof OWED. I did not open the 2.52 GB files (metadata and
  blob-length evidence only; no row-count re-measurement of the restored
  content).
- Not run by me, deliberately: the fold script (mutates archives), the gate
  single-script falsifier (mints a registry row), the writer itself
  (rewrites a 2.5 GB artifact; the lens does not mutate production indexes),
  the fleet cycle (spends free-lane quota), full pytest.
- CORRECTION logged (hostile pass, this sitting): the original Finding 3
  named a ledger census as its falsifier and did not run it; the pass ran it
  and I have now re-run everything it stood on (ledger census, task log,
  ps1 read, probe_items execution). The original live-behavior claim was
  wrong: the loop was DARK, not repetitive. The banked file above carries
  the revised finding; this line stays so the miss is auditable.
- The 7 PHANTOM-NUMBER count is carried from the e03/e07 lane runs; my own
  --files run confirmed findings exist in both files but I did not recount
  the blocking total.
- providers.yaml ling-3.0-flash-fin 404 (e03 residual) unverified: operator
  file, outside my read scope this sitting.
- The exec fold's excluded:0 prediction is carried from R1's analysis of the
  same script bytes I re-verified at :181; the fold itself has not fired.
