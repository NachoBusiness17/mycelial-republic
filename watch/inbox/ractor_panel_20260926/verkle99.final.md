# verkle99 final: orchestrator noise compaction, landed plan-only with the proof in the tree

Card: verkle99 · Survivor: verkle99-one (judge ruling in verkle99.verdict.json) · Revision:
revise-verkle99 · 2026-09-27 (UTC) · landing commit e73b60c54 on branch
mag/run-beta1-factory-build-audi-20260806T231709Z

## Final

The design holds its core: fold only orchestrator noise rows whose evidence is already
gone (session prefix `mag-agent-orc-`, dominant_theme null, zero theme vector, knot file
absent per the chain_guard dangling definition, mag/chain_guard.py:72), into ONE counter
leaf carrying the full migration anchor (pre-fold root + leaf count, byte-exact archive
sha256, Merkle root over every folded leaf hash). Nothing verifiable is destroyed; the
pre-fold chain is archived byte-exact before any write; the live chain carries the pointer.

Three revisions landed on top of the survivor, each forced by a check:

1. The counter row is a TOMBSTONE, not a session. Its window is zero-width
   (start_minute == end_minute == the first folded row's start_minute;
   first_start_minute / last_end_minute carry the real span as data, not as a window).
   The original design's wide window was a measured defect (Critique 3 below).
2. The counter session_id is `mag-agent-orc-noise-counter-v1`, inside the orchestrator
   prefix (mag/verkle_compaction.py:38-39): the one prefix-bucketing consumer
   (mag/tapestry.py:366-370) treats this class as second-class, and the counter
   represents that class. filename stays null, which is also what makes the counter
   structurally immune to its own predicate (idempotence by shape, tested at
   tests/test_verkle_compaction.py:244).
3. The proof is no longer a session script. mag/verkle_compaction.py (396 lines, commit
   e73b60c54) is the landed, tested module: plan() (read-only, reports BOTH dispositions
   of the noise class), apply() (execute=False default writes nothing; execute=True runs
   the full migration under verkle_lock through the estate's own primitives:
   _verify_chain_consistent, backup-first archive, _rewrite_chain LF bytes,
   _write_tip_atomic, evolution trim, chain_guard re-mark), prove_archived_leaf()
   (mag/verkle_compaction.py:326, the forever-provable instrument), verify_archive_anchor()
   (:360). tests/test_verkle_compaction.py: 9 tests, green. NO CLI flag is wired anywhere;
   grep for `--compact` in main.py finds nothing (main.py is untouched by this commit;
   the pre-existing RenderMan `renderman-ask compact` subcommand at main.py:999-1001
   is an unrelated surface).
   The module docstring carries the landing gate: `--compact --execute` may be wired only
   after operator GO on Q-001 and only with these tests green.

Live-scale migration proof, re-run on a fresh sandbox copy of the live chain through the
LANDED module (command: `.venv/Scripts/python.exe
watch/inbox/ractor_panel_20260926/revise_verkle99_checks/revise_verkle99_prove_archived.py`,
exit 0, receipt revise_verkle99_prove_archived_out.txt, moment 2026-09-27T04:57:46Z):
preflight consistent, 7,848 rows pre-fold, folded 463 (all distinct sessions), post-fold
7,386 rows, tip == recomputed root, prove(counter at index 25).verified true, archive
anchor root+sha+witness all match, evolution trim reported (dropped 463, series 927 to
464), second apply = 0 candidates. A drift observation is recorded in the same receipt:
between one run's in-lock scan and its post-lock re-derivation the live knots dir lost a
file (463 vs 464), because live amends delete superseded knot files; the proofs therefore
use the in-lock committed indexes (returned as folded_indexes by apply()), never a
post-hoc re-derivation.

Moment-snapshot law: the chain moved all session (7,809 at the survivor's writing, 7,845
at the class measurement, 7,848 at the sandbox snapshot, 7,850 at the audit dry-run
below); execute-time preflight re-derives everything under the lock.

## Critique addressed

### 1. prove() at an archived folded index against the archived pre-fold chain

Ran, at live scale, first + middle + last folded index, through the estate's own prover
called by the landed module (prove_archived_leaf swaps vk.CHAIN to the archive, calls
vk.prove(index), restores in finally; mag/verkle_compaction.py:326-344). Receipt
revise_verkle99_prove_archived_out.txt (04:57:46Z run): indexes 25 / 5134 / 7736 all
`verified: true`, `root_matches_archive: true`, `leaf_hash_is_archived_row: true`, and
each proof_root equals BOTH the recomputed archive root AND the pre_fold_root embedded in
the live counter leaf; each proven leaf_hash is in the folded set committed by the
counter (folded_root witness and folded_leaf_hashes_sha256 recomputed, both match). The
claim the critique quoted (folded leaves stay provable forever via VerkleProof against
the archive) is now an executable instrument and a landed regression test
(tests/test_verkle_compaction.py:169, test_prove_counter_and_prove_archived_folded_leaf,
proves archived indexes 1, 2 and 3 against the fixture archive).

### 2. Disposition of the remaining noise-class rows with live knots

Measured (command: `.venv/Scripts/python.exe
watch/inbox/ractor_panel_20260926/revise_verkle99_checks/revise_verkle99_classsplit.py`,
receipt revise_verkle99_classsplit_out.txt, moment 2026-09-27T03:55:18Z, live 7,845
rows): the noise class (prefix + theme null + zero vector) is 957 rows. Split: 463 fold
candidates (knot gone), 494 kept (knot file LIVE), 0 with null filename. The sibling
candidate's zero-duration class is the IDENTICAL set at this moment (overlap 957 of
957), so the class is unambiguous; the split is purely knot-live vs knot-gone. The keep
class spans 2026-09-11T18:47Z through 2026-09-27T03:41Z, i.e. minutes before the
measurement: the noise writer is STILL LIVE (the sibling's "bounded backlog, writer no
longer in the tree" reading does not hold; rows keep landing, their knots keep existing
until something deletes them).

Disposition, designed and recorded, replacing silence:

- Pass 1 (this card) folds evidence-gone rows only. KEEP rationale for the 494, recorded
  in code the plan surface emits every run (mag/verkle_compaction.py:73-90,
  plan()["keep"] = count_live_knot + rationale: evidence is live, not ballast; folding
  them is a second operator-gated decision, never a rider on pass 1).
- Pass 2 is designed, NOT wired: same predicate minus the dangling clause, plus explicit
  knot archival to the compaction archive BEFORE folding (move, never delete), under the
  SAME operator gate. It fires only if the operator rules those knots disposable.
- When Q-001 flips, the flip must cite both numbers at execution time (folded vs kept
  with rationale); the audit block (Critique 5) surfaces them. Silent partial coverage
  is structurally impossible now: plan() refuses to report the fold count without the
  keep count beside it.

### 3. Direct chain-row consumers beyond chain_guard and boot_check: surveyed AND tested

Survey (grep over production code, full list in the probe's docstring,
revise_verkle99_consumers.py): row-shape readers are boot_check, cache_map, chain_guard,
chain_query, data_refinery, knot_at_close, lattice_dashboard, tapestry (registry-fed),
training_packager (tail-100), holographic_q (q-knot filter), usage_digest (own sid
only); tip-only readers (hermes_warm_boot, divergence_meter, witness_snapshot,
verkle_rib, voice_self, worldline_*, agent_cli, bard) never see row shapes. gene_pool
feeds off aud_verkles.json, not the chain.

Behavioral test (command: `.venv/Scripts/python.exe
watch/inbox/ractor_panel_20260926/revise_verkle99_checks/revise_verkle99_consumers.py`,
exit 0, receipt revise_verkle99_consumers_out.txt, 04:57:50Z, post-fold sandbox with the
counter row):

- boot_check._chain_tip (mag/boot_check.py:47-57): OK on the post-fold chain, and OK on
  a counter-as-tail synthetic one-row chain (worst case): returns index/root/ts, no
  error.
- tapestry: build_tapestry_pack() runs green; the counter is NOT in the registry
  (counter_in_registry false, counter string absent from the pack) because the fold
  never writes the registry; the 368 registry orc rows bucket untouched
  (mag/tapestry.py:366-370 buckets registry rows by prefix, not chain rows).
- chain_query (mag/chain_query.py): tail(30) and root() return row dicts shape-agnostic;
  by_type("orchestrator_noise_counter_leaf") returns 0 rows today, which is CORRECT:
  by_type scans only the tail 100 (mag/chain_query.py:104-107) and the counter sits at
  index 25 of 7,386. No caller queries orchestrator types (grep of by_type callers).
- knot_at_close._chain_session_ids (mag/knot_at_close.py:90-104): the counter id joins
  the id set (counter_id_present true); inert: it matches no session DB row, so it
  filters nothing new.
- verkle_audit.verkle_gaps: numbers only (rows 7,848 to 7,386 vs 23,705 knot files; the
  mismatch is pre-existing and named in Owed).
- data_refinery._ingest_verkle_chain (mag/data_refinery.py:188-236): a counter placed in
  the LAST 500 rows (its worst case, synthetic) does not crash the loop; it yields one
  training example typed by the counter type.
- holographic_q skips non `q-knot-` sids by prefix (mag/holographic_q.py:384-386);
  usage_digest scans rows only for its own session id (mag/usage_digest.py:194-196).
- lattice_dashboard: PRE-EXISTING CRASH, fold-unrelated, found by this survey: the LIVE
  topic_evolution.json carries 22 series rows with string tension_index values
  (`fkb:amd_`, `fkb:guar`, session ids autonomous-auto-fkb-*, landed 2026-09-26) and
  build_lattice_summary raises ValueError on them (mag/lattice_dashboard.py:163-164)
  on the untouched live corpus today. The fold does not touch those rows (its evolution
  write only drops folded sids and reindexes). The counter itself renders safely in the
  chain_tail window (filename null renders as null; probed with a counter-in-tail-16
  synthetic). Owed below.

THE DEFECT THE CRITIQUE WAS FISHING FOR, found, fixed, regression-tested: the original
counter carried start_minute = cand[0].start, end_minute = cand[-1].end. The live noise
rows carry inherited ZERO-WIDTH minutes scattered across weeks (first candidate
2026-08-10T21:19Z, last 2026-09-11T23:23Z), so the counter posed a 32-DAY session
window, and the cache_map time-window join (mag/cache_map.py:150-231, last-match-wins
sweep line) re-attributed 29,360 remote provider calls from real themes to "unmapped"
(unmapped bucket 913 to 30,237 calls, totals conserved; measured in the 04:37Z probe
run, whose output was later overwritten by the post-fix rerun; the numbers are preserved
in the committed fix comment mag/verkle_compaction.py:158-168 and the regression test
docstring tests/test_verkle_compaction.py:255-263). Fix: zero-width tombstone minute.
Post-fix measurement (receipt revise_verkle99_consumers_out.txt): totals still conserved
(prompt/completion/calls identical); residual by_theme diff is bounded and one-directional:
unmapped 913 to 574 (-339 calls), real themes gain (mag_hands +19, biography +9,
autonomous_janitor +8 visible in the top list, the rest below the list cutoff) because
the folded zero-width noise windows no longer participate in the join and real
overlapping windows win. That residual is the fold's intended semantic (folded rows stop
participating), not a defect; it is accepted in Decision D2. Landed regression:
test_cache_map_theme_attribution_is_fold_invariant (tests/test_verkle_compaction.py:255)
pins by_theme as identical pre/post on the fixture (where noise windows are zero-width,
matching live shape).

### 4. Land tests/test_verkle_compaction.py before any --compact --execute flag

Landed, in that order, in commit e73b60c54: tests/test_verkle_compaction.py (9 tests)
plus the module it tests, BEFORE any CLI flag exists. Commands run this ask, exact
output scale:

- `.venv/Scripts/python.exe -m pytest tests/test_verkle_compaction.py -q` -> 9 passed
  (run repeatedly during landing; final runs green).
- `.venv/Scripts/python.exe -m pytest tests/test_verkle_compaction.py
  tests/test_verkle_audit.py tests/test_verkle_lock.py tests/test_chain_byte_exact_io.py
  tests/test_verkle_artifact.py -q` -> 22 passed (the neighboring verkle surfaces stay
  green).
- No `--compact` or `--execute` flag is wired: main.py is untouched by the commit;
  the module is reachable only programmatically and its docstring carries the gate.

Census law followed: `pytest --collect-only -q` -> 2,303 tests collected / 352 files
(moment 2026-09-27 ~04:47Z); AGENTS.md carrier refreshed to 2,303 / 352 (2026-09-27
census) with the drift from the 1,910 / 303 carrier attributed to the 09-26/27
burn-wave test landings (B2-479 6d417abd5, drift-patrol 77ff6138b, gala close
790145ab1, boot-lane 02d818bf7 + d38801265, interference burn a5dd96176) plus this
landing (+1 file, +9 collected). Verified with the estate's own instrument:
`.venv/Scripts/python.exe tools/census_drift_patrol.py --collect` -> exit 0, "collect
ok - collected claim within bar: pytest 2303 vs carrier 2303 (delta +0)". The AGENTS.md
commit also carries the 09-26 lane's uncommitted B2-215/216/249 carrier law text that
was sitting in the working tree (disclosed in the commit message; the law text is
receipted in watch/inbox/burn_wave_20260926/).

Ratchet law followed: `tools/violation_ratchet.py check --changed` initially flagged my
module with 2 NEW debts (file-too-long 419 lines; except-pass on the evolution trim).
Both fixed, not registered: the module is 396 lines and the evolution trim's skip is
reported in the apply() result (evolution_trim field), never silent. Re-run shows zero
NEW debt from mag/verkle_compaction.py (the remaining ratchet FAIL rows are other
lanes' uncommitted tools/ files in the shared tree, e.g. tools/secret_gate.py,
tools/visor.py, not mine; one such file, tools/secret_gate.py, was staged by another
lane and briefly rode my first commit attempt; I soft-reset and recommitted clean, and
it is back to untracked for its own lane).

The survivor's kill_risk admission ("the proof is a session script rather than a
landed, tested module") is retired by this commit.

### 5. Schema handling for the noise_compaction block in verkle_audit.v1

Decision: ADDITIVE NULLABLE FIELD, no version bump. The audit output gains
`noise_compaction` (null unless a compaction plan or fold state is requested), schema
stays `verkle_audit.v1`. Evidence this is safe and precedented:

- run_audit already grows additively: `backfill`, `fix`, `synth` are nullable top-level
  blocks added without version bumps (mag/verkle_audit.py:396-398; the live dry-run
  output shows all three present as null/false, receipt
  revise_verkle99_audit_dry_out.txt, exit 0, tip 7,850 leaves, root 33d3babb...).
- No downstream parser validates strict shape: grep finds no jsonschema /
  additionalProperties use anywhere in the audit path; the only consumer of the report
  files is a path glob (mag/loops_registry.py:55 "trail":
  memory/improve/daily/*-verkle-audit.json, no field switching); tests pin the v1
  string by equality (tests/test_verkle_audit.py:33,49).
- The nested plan object carries its own schema label, verkle_compaction_plan.v1
  (landed, mag/verkle_compaction.py:73), so the block is self-describing without
  touching the outer version.

Rule for the estate, recorded: bump verkle_audit.v1 to v2 only if an existing field is
removed, renamed, or changes semantics; adding an optional block is additive. Wiring
the block itself remains a move (NOT done this ask; the plan surface is reachable today
via mag.verkle_compaction.plan() and the landed tests).

## Decision for the estate

D1 (closes the critique's ordering condition): tests/test_verkle_compaction.py is landed
and green (commit e73b60c54) BEFORE any flag; the condition "until the tests land, ship
plan-only" is discharged as a live constraint. Consequence: wiring the PLAN surface
(the audit's additive noise_compaction block and/or a read-only --compact plan flag) may
proceed at any lane's discretion without violating the order; the EXECUTE surface stays
double-gated (operator GO on Q-001, whose needs-operator roam verdict stands, AND these
tests green). This card does NOT close Q-001 and does NOT execute any live fold: honest
no.

D2 (changes the spec): the counter row shape is fixed as tested: zero-width tombstone
minute (start == end == first folded row's start_minute; real span recorded as
first_start_minute / last_end_minute data fields), session_id INSIDE the orc prefix,
filename null, type orchestrator_noise_counter_leaf. Any future change to those fields
must re-run the consumer probe (revise_verkle99_consumers.py) and the landed regression
tests; the cache_map re-attribution residual (-339 unmapped to real themes, totals
conserved) is accepted as the fold's intended semantic.

D3 (changes silence into a recorded disposition): pass 1 folds evidence-gone rows only;
the live-knot noise class (494 at the 03:55Z measurement, still growing: last landed
03:41Z the same morning) is KEPT with the rationale recorded in plan()["keep"], and a
pass 2 under the same operator gate (knots archived, then folded) is the designed path
if the operator rules those knots disposable. When Q-001 flips, the flip cites both
numbers at execution time; the 99 in queue/todo.md:31 is corrected to the measured
count at that moment.

Owed (unchanged plus new): operator GO for the live fold (Q-001 open); the audit-block
wiring (D1 allows it, does not do it); the pre-existing chain_guard regression (948
unflagged-dangling live, flag pass owed); the orphan-knot surplus (~15.8k, reverse
direction); NEW from this revision: the lattice_dashboard pre-existing crash on 22
string tension_index rows in the live evolution (mag/lattice_dashboard.py:163-164)
needs an owner; the live noise writer is still minting rows (straggler tail is not
bounded), so pass 2 or a minting-side fix is a real question for the operator, not
janitor cleanup.

Shared-surface state, honestly: `.venv\Scripts\python.exe -m mag.shared_surface
validate` reports ok:false today on inbox-wide pre-existing churn (LINKS.jsonl
event-kind rows by writer b2-142-cerebras-dig; hash mismatches on files edited after
indexing, including this panel's own candidate files). This card follows the panel
precedent (uf122.final.md, dfdials.final.md are INDEX rows) and adds its own INDEX row
with sha256; the inbox-wide reds predate this card and are not healed here.

Receipts for this revision (all under watch/inbox/ractor_panel_20260926/
revise_verkle99_checks/): revise_verkle99_classsplit.py + _out.txt,
revise_verkle99_prove_archived.py + _out.txt, revise_verkle99_consumers.py + _out.txt,
revise_verkle99_audit_dry_out.txt, and the sandbox _sandbox/ (scratch, untracked by
panel precedent). Judge receipts: checks/verkle99.judge.txt, verkle99.verdict.json.
