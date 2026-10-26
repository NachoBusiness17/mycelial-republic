# BREAK PASS - moonshot-2 (hostile second sitting, 2026-10-05)

Filed by break-moonshot-2. Every check below ran this sitting (post-lens; the
lens window closed 12:07:47Z, my census moments are later; the sharpest rot
between us is the 13:00Z Estate Spine fire and the 13:01Z D3 landing).
Instrument notes: file reads via Read tool; greps unscoped unless named; the
DOORS census and ledger census ran as .venv python one-liners over the whole
file; the workflow-declaration census was `grep -L -i max_concurrency
.zcode/workflows/*.dwf.ts` over all 20 files. No em-dashes. Lane-count law
obeyed: I re-censused the executor dir before verdicting any fenced row.

## Executor fence re-census (the lens's own blind spot, closed first)

memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ still holds 16 files,
e01 through e08 only, latest mtime Oct 5 02:38 local (06:38Z, e06); no
manifest.json, no RUNNER.dwf.ts, no FOLD_SECTIONS.md. e09-e12 remain
unlanded at my sitting too. NEW: this is now a ~6.5h stall since e06 with
the R1 commit naming "coordinates e12" for the held fold de-blind (commit
23d76bb71 message). The fence holds, but its premise (the executor will
land e09-e12) is unverified and aging; see ADDITION A4.

## VERDICTS

### F1 "the loop has no memory for its own gaps" (rank 1): CONFIRMED

Every byte-cite reproduced:

- tools/mickey17_v2_fold.py:181 reads `(c.get("unconfirmed") or [])` (my
  Read of 170-199); :191 increments `excluded["9 verifier-unconfirmed"]`.
- grep -c over the fold file: deep_tier2 = 0, folded_at = 0.
- grep -c over tools/workflow_gate.py: fire_ledger = 0, stop_cert/stop-cert
  = 0, retired = 0.
- memory/workflows/ holds only REGISTRY.jsonl; FIRE_LEDGER.jsonl ENOENT.
- Exec run dir holds no manifest.json (my ls above).
- tools/gap_ledger.py and memory/gap_ledger both ENOENT (my ls) - the
  proposed landing is free.
- DOORS precedent exists: watch/inbox/ractor_engine/2026-10-04-eleven-doors/
  DOORS.jsonl, 14 rows, live differentiated statuses (my census).

Two corrections, neither fatal:

1. The lens's doors status breakdown (landed 5, open 3,
   promoted-schedulable 1) is rotted at my moment: my census reads landed 8,
   open 0, half-landed-pin-done-gero-gated 1, operator-gated 1, parked 1,
   cured-at-write-path+verified 1, dispositioned+twin-site-cured 1, header
   1. DOORS.jsonl mtime Oct 5 09:05 local (13:05Z) - it mutated after the
   lens's read when D3 landed (13:01Z). The 14-row total is byte-true. The
   rot is itself evidence FOR the finding: I just re-derived the doors
   census the way R3 would re-derive the gap surface.
2. The falsifier sweep missed training/loop_gaps.jsonl (git-status-dirty,
   347 rows, schema mag_loop_gap.v1, keys name/piece/should/signals - my
   census). It does NOT kill the falsifier: it is a runtime training-signal
   journal with no register rows, no close receipts, no landing bindings.
   But the ledger mint should reuse its append-only conventions rather than
   mint a third format unannounced (ADDITION A5).

### F2-fleet / JSON finding 2 "probe battery is a re-fire machine" (rank 2): CONFIRMED

Reproduced exactly, plus one strengthening and one rot:

- Ledger census byte-identical to the lens claim: 40 rows, ts
  2026-10-05T06:47:58Z..07:01:51Z, 5 distinct work_ids, Counter top
  ('probe-DROP-SCHMIDHUBER-COMPRESSION', 20).
- tools/free_lane_fleet.py:168 `for r in rows[-12:]`, :174 id keys
  `str(r.get("source") ...)[:40]`, retire block :288-306 reads
  `[-40:]` at :293 and unlinks only QUEUE globs (:301-304). Docstring
  work-sources list (:14-21) names exactly 3 sources; no door source.
- Store: memory/percolator/candidates.jsonl = 29 rows; 0-idx rows 17 and 18
  both carry source 'DROP-SCHMIDHUBER-COMPRESSION' (row 17 claim None,
  row 18 carries the amended_metric) - the [:40] id collision is real.
- STRENGTHENED: with 29 rows the last-12 window covers 17-28, so rows 0-16
  (17 rows) are unreachable, not 0-15 - the defect is one row worse than
  the lens filed.
- ROTTED sub-clause: A3's "retires an OPEN door" framing. Door
  D3-clippy-prober landed at 13:01Z (commit 6c7060a8e, 2026-10-05 09:01:11
  -0400), 54 minutes after the lens's final read; DOORS.jsonl now reads it
  landed. The amendment survives re-pointed: the landed instrument
  (mag/skill_fsrs.py, 29 cards, "banks toward the ~1k reviews that make
  fitting honest", 27/29 cards due per the commit message) still owes the
  ~1k probes; A3 should cite the skill ledger's due-card state, not an
  open door (ADDITION A2).

### F2 / JSON finding 3 "mickey17-burn.dwf.ts passes G8 vacuously" (rank 3): CONFIRMED

- Census: 20 .dwf.ts files; grep -L -i max_concurrency returns exactly
  .zcode/workflows/mickey17-burn.dwf.ts. Its mtime Oct 5 06:43 local is
  the newest of the 20.
- Commit 23d76bb71 (2026-10-05 06:48:04 -0400) message contains BOTH the
  "19/19 saved workflows now declare max_concurrency" claim AND the minting
  of mickey17-burn.dwf.ts ("the parameterized consolidation") in the same
  commit - the rot-inside-one-sitting claim is byte-true, no inference
  needed.
- G8 vacuous-pass premise verified at tools/workflow_gate.py:147-153:
  G8_MAX_CONCURRENCY_RE matches literal declarations and the docstring says
  "Scripts that declare no max_concurrency pass (the law binds the declared
  dispatch shape)."
- Landing-spot nit: tools/fleet_doctor.py does NOT exist (my ls). The
  table's own alternative stands: the tripwire host is
  tools/census_drift_patrol.py (exists) or a minted file. Also the header
  quote "the filer banks RUNNER.dwf.ts + manifest.json per run (row 4)"
  sits at mickey17-burn.dwf.ts:12-13, not :8-10 (cite drift; content
  byte-true, and it confirms closure-row 6's premise).

### F4-seed / JSON finding 4 "provenance spine records false history" (rank 4): WEAKENED

Core confirmed, safety clause falsified by the lens's own cited file:

CONFIRMED half:

- e06-fidelity-audit.json rows 1-3 quote-exact: "all 131 seeds'
  record.tape_ref points at the dead 102-row tape
  memory/runs/trajectory/steps.jsonl"; "All 131 SEED.json files were minted
  2026-10-03T21:07:13Z .. 21:13:06Z"; notes line: "No code changed by this
  lane; mag/ and tools/ untouched."
- mag/worldline_seed.py:84 `TAPE = ROOT / "memory" / "runs" / "trajectory"
  / "steps.jsonl"` and mag/trajectory_step.py:50 `STREAM = ... "memory" /
  "trajectory" / "steps.jsonl"` - both at the exact cited lines, the
  two-path split live and unowned today.

FALSIFIED half (QUANTIFIER LAW): the claim "zero consumers of SEED
tape_ref (only gwap replay_tape_ref, a different surface), so the fix
breaks nothing" and its falsifier "a live seed-to-steps join elsewhere
(none found by grep over mag/ + tools/)". My grep over the SAME scope found
live consumers of the SEED record.tape_ref:

- mag/worldline_seed.py:733-741: the seed verifier's record leg walks
  `Path((rec.get("tape_ref") or {}).get("path", str(TAPE)))` then
  `_session_rows(tape_path, session_id)` and reports record.tape_rows
  (:748). This IS a live seed-to-steps join, in the file the finding
  cites at :84.
- mag/worldline_dungeon.py:128-134: the dungeon census reads
  `(slabs.get("record") or {}).get("tape_ref", {})` and surfaces
  tape_rows per seed.

So "repoint TAPE breaks nothing" is unproven as stated; the closure must
either regression-test the verifier's tape_rows semantics and the dungeon
join, or take e06's own alternative steal ("or deprecate the tape_ref
slab"). The structural finding (false history, no owning lane) stands.

### F5 "fold counter wired to a dead key" (rank 5, fenced): CONFIRMED, sharpened

- fold:181 / :191 / zero deep_tier2 tokens: byte-read (F1 above).
- Runner persist mechanism confirmed: .zcode/workflows/mickey17-v2.dwf.ts
  :277-290 instructs lanes to append tier-2 verdicts into
  <id>.checks.json under the literal key "deep_tier2" (and :152 "keep
  every existing key verbatim (including deep_tier2)"). "unconfirmed"
  appears in the runner workflows ONLY as a verdict enum value inside
  those arrays (mickey17-v2.dwf.ts:59, :270-271, :331;
  mickey17-burn.dwf.ts:98, :460-461, :524), never as a top-level checks
  key.
- NEW sharpening: my key census of the live exec run's 8 .checks.json
  files: lane/tier/moment/method/supports/counts/check_date/checks/mode/
  check/entries/checked_at/rows. NEITHER "unconfirmed" NOR "deep_tier2"
  is present in any of them. The dead-key diagnosis holds, and the repoint
  has a second defect the lens did not file: for runs whose lanes never
  persist tier-2 arrays, the repointed fold still reads zero; the de-blind
  needs the both-keys fallback (unconfirmed OR deep_tier2 verdict scan) or
  excluded code 9 stays blind for exactly this run class.
- Fence terms no longer prose-carried: commit 23d76bb71's message itself
  holds them ("HELD post-executor (ownership fence): fold-tool de-blind
  (row 1, coordinates e12), workflow_gate stop-cert + FIRE_LEDGER (rows
  6+7, coordinates e04)") - byte source, resolving the lens's last blind
  spot. The exec run remains unfolded at my census; the fence holds.

### Closure-table rows 6-12 (CONVERGENT spot-checks)

- Row 6 (manifest/RUNNER owed): CONFIRMED open - still ENOENT at my
  census; header promise byte-true at :12-13. Fence holds.
- Row 7 (10 stranded window candidates): CONFIRMED - grep -c AQLM
  memory/percolator/candidates.jsonl = 0; watch/inbox/
  frontier_olm_2026-10-04/percolator_candidates.jsonl exists, 10 rows
  (my count); the held row is b9_doors_tier.md:39-42, quote byte-exact
  ("Percolator candidate row carrying the two-clause rule: HELD ... Owed
  to that owner or the next window").
- Row 8 (cache_receipt zero producers): CONFIRMED-as-carried - the quote
  is byte-exact at watch/inbox/build_wave_20261005/b2_cache_receipt.md:34
  (real path; the lens cited it bare). Instrument not run by either of us;
  the receipt is the evidence and says "Blocked as a follow-up, not
  silently claimed."
- Row 9 (29 dangling already_inside): CONFIRMED-as-carried - b1_
  knowledge_graph.md:70 quote byte-exact; builder at
  mag/knowledge_graph.py:236-239 emits `module:{Path(str(m)).name}` ids.
  Graph state 2919/1143 honestly tagged not-recomputed; I did not
  recompute it either.
- Row 10 (21 case-only seal false drifts): CONFIRMED-as-carried - b7_
  sweep.md:34-37 and :120 quote byte-exact ("17 real drifts + 21 CASE-ONLY
  false drifts (uppercase-hex seal rows vs lowercase actuals)"); my grep
  of tools/prepush_seal_patrol.py (exists, 7,484 B) finds ZERO
  casefold/lower() tokens, consistent with the case-sensitive compare.
  Patrol not run by either sitting.
- Row 11 (ESTATE_INDEX duplication): WEAKENED BY ROT, not by error - the
  13:00Z Estate Spine fire ran between sittings: watch/ESTATE_INDEX/
  ESTATE_INDEX.jsonl is now 346,683,794 B, mtime Oct 5 09:19 local
  (13:19Z); dashboard/static/ESTATE_INDEX/ is ENOENT (the second copy is
  GONE; only _build_estate_walk.py and estate_walk.html remain under
  dashboard/static); last_run.json now reads ts 2026-10-05T13:19:46Z,
  seconds 1184.6, skipped 1, skipped_skip_list 0. The lens's predicted
  post-9:00 signature (skip_list_hits > 0) did NOT materialize
  (skipped_skip_list: 0). The lens's read was honest at its moment (sizes,
  mtimes, missing pointer all re-verified as of 12:07Z per their file;
  pointer candidates INDEX.json/pointer.json still ENOENT at mine), but
  the row's "duplication is BACK" claim cannot be re-confirmed on
  post-fire bytes: the surface it measured no longer exists. The verify
  half of the close is now half-executed by the world; the repoint half
  needs a fresh duplication read first. dashboard/server.py:188
  (`ESTATE_INDEX_PATH = DATA / "ESTATE_INDEX.jsonl"`) confirmed as the
  query door cite.
- Row 12 (GAP_REGISTER rank 1 unannotated): CONFIRMED - my read of
  watch/inbox/gap_analysis_20261001/GAP_REGISTER.md: rank 1
  (EstateWalkDaily bake) carries no >> FILLED annotation while ranks 2 and
  3 both do.

## ADDITIONS (what the lens missed, ranked by leverage)

- A1 (HIGH, feeds F4's row 4): live SEED tape_ref consumers exist -
  mag/worldline_seed.py:733-741 (verifier seed-to-steps join on the
  tape_ref path) and mag/worldline_dungeon.py:128-134 (dungeon census
  reads record.tape_ref). Evidence: my grep over mag/ + tools/ this
  sitting (output in session). Falsifier: both sites proving dead code
  (dungeon census unreachable, verifier record leg never executed).
  Move: 15 min - rewrite row 4's close as "repoint + regression-test the
  verifier tape_rows check and the dungeon join, or deprecate the slab per
  e06's own steal note"; never land the bare repoint on "breaks nothing".
- A2 (HIGH, feeds F3/A3): D3-clippy-prober LANDED 13:01Z (commit
  6c7060a8e); DOORS census now landed 8 / open 0. Evidence: git log -1
  6c7060a8e (timestamp + message); DOORS.jsonl mtime 13:05Z; my status
  census. Falsifier: a still-open door keyed to the probe debt (none in
  the file). Move: 5 min - re-point A3 at mag/skill_fsrs.py due-card
  state (27/29 due per the D3 commit) so the fleet amendment cites the
  landed instrument, not a rotted door status.
- A3 (MEDIUM, feeds row 11): the 13:00Z fire already transformed the
  index: 346 MB single copy, dashboard copy gone, last_run fresh,
  skip-list signature absent (skipped_skip_list 0). Evidence: my ls +
  last_run.json read (above). Falsifier: a second >= 2.5 GB copy
  persisting at a path outside the two I checked (I checked only the two
  named paths). Move: 10 min - re-derive the duplication claim on
  post-fire bytes before any query-door repoint; the pre-fire evidence is
  spent.
- A4 (MEDIUM, gates every executor-fenced row): the executor looks
  STALLED, not merely unfinished - last lane e06 landed 06:38Z, nothing in
  ~6.5h+ across two sittings, no manifest, and R1's held fold de-blind is
  "coordinates e12". Evidence: my ls of the lanes dir (16 files, mtimes
  01:19-02:38 local); commit 23d76bb71 message. Falsifier: a runner
  heartbeat or journal showing dwfrun-e9656e14 alive (none on disk in the
  run dir). Move: 10 min - check the workflow journal / ListWorkflowRuns
  for the exec run's liveness before R3 waits on e09-e12; if dead, the
  fenced rows (fold de-blind, gate rows 6+7, manifest row) revert to
  unowned and R3 may fire them under the amend-not-rewrite law.
- A5 (LOW, feeds F1): training/loop_gaps.jsonl (347 rows, schema
  mag_loop_gap.v1) is the un-cited nearest neighbor for the gap ledger -
  append-only, ts-keyed, already machine-parsed. Evidence: my census
  (rows, keys). Falsifier: it already carrying register-keyed rows with
  close receipts (it does not). Move: 10 min - mint
  memory/gap_ledger/ledger.jsonl reusing the mag_loop_gap.v1 append-only
  conventions (or extend that file), and name the distinction in the
  ledger header so the estate does not grow a third gap format.
- A6 (nits, zero-cost fixes to the table): tools/fleet_doctor.py ENOENT
  (row 3's primary tripwire host; use tools/census_drift_patrol.py, which
  exists, or mint new); mickey17-burn.dwf.ts header cite is :12-13, not
  :8-10; unreachable store rows are 0-16, not 0-15; the exec run's checks
  files carry neither unconfirmed NOR deep_tier2, so the repointed fold
  needs a both-keys fallback (else code 9 stays zero for this run class);
  fleet cadence owner is scripts/free_lane_fleet_cycle.ps1 (schedule not
  decoded by me - OWED). Evidence: my greps/ls above. Move: fold into the
  row edits, no extra sitting.

## Not run by me (honesty)

- The fleet cycle itself, the fold script, the gate single-script
  falsifier, tools/cache_kpi.py, tools/prepush_seal_patrol.py, the
  knowledge-graph rebuild, full pytest, and the ESTATE_INDEX writer: all
  untouched (same list as the lens; I added no mutations - this pass is
  read-only plus this receipt).
- The 06:57/06:58 rewrite actor remains inference on my side too; the
  post-fire state removed the evidence I would have re-read.
- Executor workflow journal liveness (A4's falsifier) not queried - I have
  no journal tool in this lane; flagged for a seat that does.

## Bottom line

Four of five findings survive byte-intact (F1, fleet, burn-engine, fold
counter); F4 is weakened to "structural lie confirmed, cure unsafe as
written" by consumers inside its own cited file; row 11's surface was
legitimately read and then legitimately replaced by the 13:00Z fire. The
lens's moment-discipline was good - every rot I found (D3 landing, doors
statuses, ESTATE_INDEX rewrite) falls inside a blind spot it declared
first. The two things it should have caught: the tape_ref consumers its
own grep would have shown, and the loop_gaps.jsonl neighbor.
