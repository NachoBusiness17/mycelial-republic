# MOONSHOT-2 LENS - OUROBOROS R2: THE GAP SURFACE (2026-10-05)

Filed by lens moonshot-2. Moment window: every read and run below happened
this sitting, roughly 11:20Z to 12:10Z (08:20 to 08:10 EDT span compressed;
final clock read 2026-10-05T12:07:47Z, so the 09:00 EDT Estate Spine Index
scheduled fire is still ahead of this file). Executor state at my final
check: memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ holds 16 files,
lanes e01 through e08 ONLY, no FOLD_SECTIONS.md, no manifest.json, no
RUNNER.dwf.ts (my ls). My executor coverage map is therefore an 8-lane
moment-read in the B2-216 sense. Rank metric everywhere: the amended
Schmidhuber selector (memory/percolator/candidates.jsonl row 18: primary =
carried-history retired in bytes + verbs minted; secondary = defects
found/fixed/verified; kill only on losing both over 5 waves).

## What the executor covers (my own byte-read of all 8 lane files)

CURIOSITY_REGISTER rows 1 (both units, e01+e02), 2 (all five units, e03),
3 (e04), 4 (e05, percolator store 19 to 29 rows, idempotence proven), 5
(e06), 6 (e07, RECEIPT_BINDINGS adopted on mag/dirac_loop.py bank()), and
7 unit 1 (e08, errno-22 writer guard, code leg landed by the prior night
shift, verified this sitting). Still unlanded at my moment: register rows
7 units 2+3, 8, 9, 10. DO NOT re-fire those; they are executor-fenced.
GAP-MINED below is only what no e-lane touches.

## The moonshot thesis

The loop is blind in one specific way: it cannot remember its own gaps.
Round 1 held four amendment rows behind an executor fence; round 2 (this
fold) had to re-derive them from prose receipts, re-grep the same files,
and will hand round 3 the same prose again. The evidence that this is a
memory defect and not a habit: every domain that DID get a status ledger
stopped re-deriving. The queue drain verb took the todo index from 3 to 39
closed with receipt bindings (TS-03, tier-2 VERIFIED). DOORS.jsonl holds
14 rows with live status (my census: landed 5, cured-at-write-path 1,
dispositioned 1, open 3, promoted-schedulable 1, operator-gated 1, parked
1, header 1). The percolator store grew to 29 rows with dedupe law proven
by e05's rerun. The gap surface itself, the thing this round exists to
ractor, has no such ledger: it lives in MASTER_READ_ESTATE section 9
prose, build-wave receipt Owed blocks, R1 SYNTHESIS held rows, and
todo.md checkboxes. Each ouroboros round re-pays the derivation cost in
seats, and each re-derivation is a fresh fabrication risk (R1 proved lane
counts wrong 5 times). The 10x version is not a better fold prompt; it is
gaps as state.

## RANKED CLOSURE TABLE

| rank | gap (source register) | one-sitting close | landing file | evidence (this sitting) | blocked-by |
|---|---|---|---|---|---|
| 1 | The gap surface is prose, re-derived every round (R1 held rows + build-wave Owed lists + CURIOSITY residuals have no byte-held status) | Mint memory/gap_ledger/ledger.jsonl (id, source, claim, landing, status open/held-fence/closed, close_receipt via hardcoded bindings, DOORS.jsonl shape generalized) + a 60-line append-only reader/writer tools/gap_ledger.py; seed it from this table | tools/gap_ledger.py + memory/gap_ledger/ledger.jsonl | my greps: tools/mickey17_v2_fold.py:181 + zero folded_at, tools/workflow_gate.py zero stop-cert/FIRE_LEDGER tokens, memory/workflows/FIRE_LEDGER.jsonl ENOENT, exec run manifest ENOENT; the ask itself reconstructs the surface from 4 prose registers; DOORS.jsonl precedent (14 rows, my census) | none |
| 2 | Fleet probe battery is a re-fire machine, blind to the estate's own owed probes | Amendments A1 to A4 to the work generators (below) | tools/free_lane_fleet.py:158-206,:268-306 | my census of memory/runs/free_lane_fleet/ledger.jsonl: 40 rows, 5 distinct work_ids, probe-DROP-SCHMIDHUBER-COMPRESSION fired 20x between 06:47:58Z and 07:01:51Z; my full read: probe_items takes rows[-12:] only (:168), id keys on source[:40] (:174, rows 17+18 collide), retire loop touches only QUEUE paths (:288-306) | none |
| 3 | The R1 cure re-introduced the disease: mickey17-burn.dwf.ts (R1 row 3's fork cure) is the only workflow of 20 with no max_concurrency declaration, so G8 passes the estate's ONE burn engine vacuously; the 19/19 claim rotted inside one sitting | Append the // max_concurrency: N header comment (N>3 also cites // envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md per the G8 law e04 landed) + add a missing-declaration tripwire to the fleet-doctor class | .zcode/workflows/mickey17-burn.dwf.ts header + tools/fleet_doctor.py (or the census-patrol class) | my loop grep over .zcode/workflows/*.dwf.ts: 20 files, exactly one NO-DECL, mickey17-burn.dwf.ts (mtime Oct 5 06:43, newest file; R1 commit 23d76bb71 claimed 19/19 the same morning) | none |
| 4 | The provenance spine records false history with no owning lane: all 131 SEED.json slabs of the Sep 25 run were minted 2026-10-03 (retro-seeded), and every record.tape_ref points at a dead 102-row tape, so seed-to-execution joins read reconstruction, not record | Verifier-level stale-path fallback (embedded dead path with 0 session rows resolves to the live stream, healing all 131 slabs without rewriting them) + TAPE repoint + minted_at stamp, with regression tests over BOTH live consumers the hostile pass named (verifier record.tape_rows leg, dungeon read_seeds) | mag/worldline_seed.py:733-734 (fallback) + :84 (TAPE) + the seed writer + tests | e06 rows 1-3 (my full read) + my own untruncated census (43 tape_ref hits / 17 files over mag/+tools/+scripts/+tests/) + my run counts: dead tape 102 rows / 0 for run 3484c5eb (grep rc=1), live stream 1,438 rows for the same id | none (executor changed no code; e06 row notes say mag/ untouched) |
| 5 | R1 rows 1+6+7 unlanded and the fold's excluded-counter is wired to a key no runner writes; the repair is cheaper than R1 priced because the counter already exists | Repoint fold :181 from the never-written unconfirmed key to the persisted deep_tier2 arrays + stamp folded_at + sha256(script)[:12]; stop-cert clause and check-time FIRE_LEDGER append per R1 rows 6+7 | tools/mickey17_v2_fold.py:181 (and :191 already counts code 9 verifier-unconfirmed); tools/workflow_gate.py | my greps: fold:181 reads (c.get("unconfirmed") or []), zero deep_tier2 tokens in the file, :191 already increments excluded["9 verifier-unconfirmed"]; workflow_gate zero retired/stop-cert/FIRE_LEDGER tokens; FIRE_LEDGER.jsonl ENOENT | executor-fence (exec run unfolded at my moment; land the fold edit the moment the exec fold fires, before the next mega-burn) |
| 6 | R1 row 4 self-refuting in the live run: the workflow header itself promises the filer banks RUNNER.dwf.ts + manifest.json per run, the run dir holds only lanes/ | None (verify post-fold): the filer step of the consolidated workflow owes the manifest; if the run folds without one, the row reopens with the workflow's own bytes as evidence | memory/runs/mickey17_v2/runs/2026-10-05-exec/manifest.json | my ls: manifest.json and RUNNER.dwf.ts ENOENT; mickey17-burn.dwf.ts header (my read, lines 8-10) says "the filer banks RUNNER.dwf.ts + manifest.json per run (row 4)" | executor-fence |
| 7 | 10 stranded window candidates (AQLM two-clause class) never entered the master store | Sanctioned ingest over watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl + dedupe rerun (same writer e05 used) | memory/percolator/candidates.jsonl | CONVERGENT with accuracy.md finding 2 (store greps zero); my own grep -c AQLM memory/percolator/candidates.jsonl = 0; b9_doors_tier.md:39-42 held the row and e05 filed only the r07 list | none (verify no e09-e12 lane is a percolator lane first) |
| 8 | Cache-receipt law has zero producers, recv_hit% measures nothing | Wire the first stamp site at the reuse decision point | mag/flight_recorder.py (the usage-row builder) | CONVERGENT with accuracy.md finding 4; my read of b2_cache_receipt.md:34 ("producers do not yet stamp cache_receipt... recv_tok reads 0"); not re-grepped by me | none |
| 9 | 29 already_inside dangling edges (B1 filed-not-fixed) | Fix the we_have builder to emit real module ids (the B1 fix-4 pattern: bind to byte-backed module nodes) | mag/knowledge_graph.py:237-239 | CONVERGENT with accuracy.md rank 6; my read of the builder lines and b1_knowledge_graph.md:70 ("29 remaining dangling edges are the pre-existing already_inside defect"); graph state 2919/1143 carried from b1's _b1_after.json (not recomputed by me) | none |
| 10 | Seal patrol 21 case-only false drifts (uppercase-hex seals vs lowercase actuals) | Casefold both sides at the compare | tools/prepush_seal_patrol.py | CONVERGENT with accuracy.md rank 9; my read of b7_sweep.md:34-37 + :120 ("(a) seal patrol case-only false drifts (21 rows, uppercase-hex seals)"); instrument not re-run by me | none |
| 11 | ESTATE_INDEX duplication is BACK: two independent 2,523,006,985-byte copies rewritten 06:57/06:58 today, pointer file the committed writer writes unconditionally does not exist, last_run.json still 2026-10-04T18:28:51Z | Post-9:00 signature check (skip_list_hits>0, pointer appears, dashboard copy mtime stays 06:57) + repoint the query door default to the watch master | dashboard/server.py:188 + watch/ESTATE_INDEX/last_run.json | CONVERGENT with accuracy.md finding 1; my own ls this sitting: both paths exactly 2,523,006,985 B, mtimes Oct 5 06:57 and 06:58, pointer ENOENT; 09:00 fire still ahead (12:07Z read) | none (verify, then repoint) |
| 12 | GAP_REGISTER rank 1 (EstateWalkDaily bake) cured but unannotated | Append the FILLED annotation with log cites (name the instrument: the log is UTF-16, plain grep reads 0) | watch/inbox/gap_analysis_20261001/GAP_REGISTER.md row 1 | CONVERGENT with accuracy.md rank 11; my own instrument: sed -n 70,75p shows rank 1 row with no >> FILLED annotation while ranks 2,3,4,6,7 all carry one; all other rows FILLED (my count of >> rows without FILLED = 0) | none |

Closed by bytes, do NOT re-fire (my checks or verified receipts): the
Schmidhuber metric half of the owed-list pair (store rows 17+18 filed,
consumed by e05's BYTES_TO_VERBS fold), queue drain Q-005/Q-025 (TS-03
tier-2 VERIFIED), errno-22 writer guard (e08 + commit 9c52757f9), G8 gate
+ scenario cards (e04, suite green twice), the estate-index compact tool +
skip list + query door (e01/e02 code in commit e80f48b8f per accuracy's
git show; I did not re-verify the commit).

## FINDINGS IN DETAIL

### F1 (rank 1). Gaps as state, not literature

Every instrument this fold touched reads a surface nobody writes, and the
round above it does the same: the fold reads unconfirmed (nobody writes
it), G8 read literals (19 of 20 wrote them, then the 20th file minted
without), the fire journal reads payloads without width. The gap surface
is the fourth coat of the same disease: R1's held rows, the build-wave
Owed blocks, and the CURIOSITY residuals ride prose that every round
re-parses. The queue drain verb, DOORS.jsonl, and the percolator store
all proved the estate can hold status in bytes and stop re-deriving. One
sitting: tools/gap_ledger.py (append-only, RECEIPT_BINDINGS-style close
evidence from a hardcoded row-to-path table, the e07-adopted law) plus
the seed ledger with this table's 12 rows. The moment it exists, R3 reads
state, the fleet probes open rows (F3 amendment), and the fold gate can
fail on rows closed-in-prose-but-open-in-bytes. Verbs minted: 1. Carried
history retired: every future round's derivation. Falsifier: an existing
byte-held gap-status surface keyed on these registers (my greps over
tools/ + memory/ found DOORS.jsonl for doors only; if another exists, F1
dies and becomes "wire the fold to it").

### F2 (rank 3). The R1 cure is the newest violator

R1 landed the 19/19 declaration sweep and the parameterized burn engine
in the same sitting; the engine shipped without the declaration, so the
fleet's ONE consolidation workflow, the thing that will fire every future
mega-burn at width 12, passes the width gate vacuously. The 5-minute
close is the header comment; the durable close is the tripwire (any
.zcode/workflows/*.dwf.ts missing the literal trips the fleet doctor or
census patrol class), because a law without a tripwire rotted in under
one sitting, measured. Falsifier: a schema-level concurrency field in
mickey17-burn.dwf.ts (my grep of the file found zero; e04's G8 matches
literal declarations).

### F3 (rank 2). The sensing instrument re-fires one probe 20 times in 14 minutes

Measured, not inferred: the ledger holds 40 rows over 06:47:58Z to
07:01:51Z with 5 distinct work_ids; DROP-SCHMIDHUBER-COMPRESSION owns 20
of them. The battery reads only the LAST 12 store rows (now the e05-filed
LINKS 10 plus the colliding Schmidhuber pair whose two rows share one
truncated-source id), re-fires them every cycle forever, and cannot see
window candidate files, the doors list, or store rows 0-15 (never probed
by construction). Amendments to the work generators, cheapest first:

- A1 dedupe (CONVERGENT with accuracy.md A1, my live measurement adds the
  20x number): probe_items and cycle skip work_ids already banked ok in
  the full ledger, not the last-40 window the retire block reads.
- A2 window sensing (CONVERGENT with accuracy.md A2): additionally glob
  watch/inbox/*/percolator_candidates.jsonl read-only, newest first,
  capped at the current 6.
- A3 door D3 source (NEW, this fold): the open door D3-clippy-prober
  (DOORS.jsonl, my census) wants "2-3 closed-book free-recall probes on
  due skill cards... banks the ~1k probes FSRS needs off defaults". The
  24/7 free burner is the only surface that can afford ~1k probes; wire a
  fourth work source that reads due cards from the skill ledger state and
  fires recall asks. This retires an OPEN door with the standing fleet.
- A4 id fix: probe ids key on the row's canonical field or row index, not
  source[:40] (rows 17+18 collide today).

Falsifier: a ledger census across cycles showing natural rotation (the
opposite was measured).

### F4 (rank 4). The seed archive is a reconstruction wearing a record's clothes

CORRECTED 2026-10-05 on the hostile second pass: the original consumer
clause ("zero consumers of SEED tape_ref... the fix breaks nothing") was
a quantifier-law miss, my own doing: the census grep was piped through
head -8 and the gwap replay_tape_ref hits consumed the truncation window.
The untruncated re-census (grep -rn tape_ref over mag/ + tools/ +
scripts/ + tests/, 43 hits, 17 files) finds TWO live consumers of the
SEED record.tape_ref: the seed verifier's record leg
(mag/worldline_seed.py:733-734 reads the seed's embedded
rec.tape_ref.path, falls back to TAPE only when absent, joins via
_session_rows at :681-695, reports record.tape_rows OK/WARN at :748-750)
and the dungeon census (mag/worldline_dungeon.py:128-134 reads
slabs.record.tape_ref rows/tip per seed). What the re-read changes in
the close, not the core:

- The core stands byte-confirmed (e06 rows 1-3 plus my own instruments
  this sitting): dead tape memory/runs/trajectory/steps.jsonl holds 102
  rows and ZERO for run 3484c5eb (grep rc=1), the live stream
  memory/trajectory/steps.jsonl holds 1,438 rows for the same run id,
  all 131 seeds were minted 2026-10-03T21:07:13Z..21:13:06Z for the Sep
  25 run, TAPE/STREAM split at mag/worldline_seed.py:84 vs
  mag/trajectory_step.py:50, and no lane owns the cure (e06 notes mag/
  and tools/ untouched).
- The one-line TAPE repoint is WEAKER than first claimed: because the
  verifier prefers each seed's EMBEDDED tape_ref.path (:733), the repoint
  heals only future mints and leaves all 131 existing slabs verifying
  WARN (0 session rows at their embedded dead path). It also cannot
  break their reads, so the safety half survives in weaker form: the
  repoint is inert for existing slabs, not consequence-free.
- The real closure is verifier-level: resolve an embedded tape path that
  yields zero session rows to the live stream (a stale-path fallback at
  worldline_seed.py:733-734), healing all 131 slabs without touching
  them (append-never-rewrite preserved), plus the TAPE repoint and the
  minted_at stamp for future mints. Regression scope the hostile pass
  named: the verifier's record.tape_rows leg, worldline_dungeon
  read_seeds, and the standing suites (test_worldline_seed_gate,
  test_worldline_compact); e06's alternative (deprecate the slab class)
  stays the fallback if the fallback join proves ambiguous.

Falsifier, tightened: the dead-tape half dies if any code path already
resolves the embedded dead path to the live stream (the untruncated
census says none does; consumers are exactly the verifier, the dungeon
census, and the gwap replay_tape_ref family); the unowned half dies if a
lane receipt claims this cure. Move cost: 60 min (fallback + repoint +
stamp + regression tests over both consumers), up from the original 30.

### F5 (rank 5, fenced). The fold's counter exists and is wired to a dead key

tools/mickey17_v2_fold.py:191 already counts excluded code 9
"verifier-unconfirmed"; :181 feeds it from c.get("unconfirmed"), a key no
runner persists (runners persist deep_tier2 arrays, per the R1 addenda
and mickey17-v2.dwf.ts:278-284). The de-blind is therefore a repoint plus
a folded_at stamp, not the 30-minute build R1 priced. Rows 6+7 (stop-cert
clause, FIRE_LEDGER append) remain 45 minutes for the gate owner. The
exec run had not folded at my final ls; land row 1 the moment it fires.
Blocked-by: executor-fence.

## free_lane_fleet.py work-generator amendments (the ask's explicit deliverable)

Summarized as the edit list for the owning seat (F3 above carries the
evidence): probe_items (tools/free_lane_fleet.py:158-187) gains the full-
ledger dedupe read, the window glob, the door-D3 due-card source, and the
canonical id; cycle (:251-310) gates probe work_ids on the same done_ids
logic the queue retire block already runs (:288-306); the docstring work
sources list (:14-21) gains source 4 (gap ledger open rows, the moment
F1's ledger exists). What the fleet should be probing that it is not, fed
from THIS fold: the 10 stranded window candidates (A2), the ~1k FSRS
recall probes door D3 wants (A3), and store rows 0-15 which the last-12
window has never reached (A1's dedupe naturally rotates the battery
there once repeats stop).

## Blind spots, honestly

- e09-e12 unseen: 4 executor lanes were still unlanded at 12:07Z; every
  "not covered" verdict about register rows 7.8/7.9/7.10 is a moment-read
  and could rot within hours. Re-census the lanes dir before firing any
  table row marked executor-fence.
- Not run by me: the fold script (mutates archives), the gate single-
  script falsifier (mints a registry row), a fleet cycle (spends free-
  quota), the ESTATE_INDEX writer (rewrites a 2.5 GB artifact), full
  pytest, tools/cache_kpi.py, tools/prepush_seal_patrol.py, and the
  knowledge-graph rebuild (rows 8-10 ride accuracy.md's runs plus my
  receipt reads, tagged CONVERGENT where so).
- The 06:57/06:58 index rewrite actor is inference (accuracy's stash/
  reset attribution); I verified sizes/mtimes/missing-pointer only, no
  reflog proof, and did not open the 2.5 GB files.
- The R1 fence terms for rows 6+7 are carried from the R1 commit message
  and SYNTHESIS.md, not re-read from a driver doc this sitting.
- I did not verify commit e80f48b8f's diff myself (carried from
  accuracy.md's git show note); my e01/e02 coverage claims ride the lane
  files' own executed rows.
- Fleet cadence: I measured 40 ledger rows in 14 minutes but did not
  establish which schedule fires that fast (the docstring and accuracy
  say 30-minute cycles; the density suggests faster); the 20x number
  stands regardless of cadence.
