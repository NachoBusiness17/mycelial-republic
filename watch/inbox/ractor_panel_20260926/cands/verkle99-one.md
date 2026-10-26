# verkle99 - candidate one: orchestrator noise compaction design (dry-run proven)

Card: verkle99 · Candidate: verkle99-one · Date: 2026-09-26/27 UTC (session crossed midnight)

## The 99 is a fossil - measured, not inherited

The todo line (queue/todo.md:31, mirrored queue/queue_index.jsonl Q-001) says "99 orchestrator
noise leaves". No byte backing exists for 99 anywhere I could find:

- `memory/biography/**` is gitignored (`.gitignore:53`), so the chain has no history to
 reconstruct the count from; `git show cb26bc2cd:memory/biography/verkle_chain.jsonl` fails
 ("exists on disk, but not in 'cb26bc2cd'").
- The 09-15 and 09-17 boards seeded the same job as a dry-run receipt
 (memory/plans/fifty_wide_20260915.md:51, fifty_wide_20260917.md:83 → FW48_verkle_compact.md);
 `memory/runs/fifty_wide/` does not exist and no FW48 receipt landed - the dry run never ran.
- A prior janitor roam already ruled Q-001 "needs-operator: Merkle chain rewrite is deletion on
 the integrity substrate" (watch/inbox/BURN_queue-field_20260925_c.md:19,
 queue/queue_index.jsonl Q-001 roam_verdict).

Per the estate's own census law (AGENTS.md Clippy: "a count is a snapshot of one tree at one
moment, never a constant" - the retired 1,341-test headline disease), this design defines the
noise predicate deterministically and measures the live count at dry-run time instead of
inheriting 99. Measured 2026-09-27 ~00:55 UTC over the live 7,810-row chain: 128 fold
candidates (see Falsifier for the recompute). The chain also moved twice during this session
(7,809 → 7,810 rows, root c492e0ff… → cbb7bbc6…), so every count below is a named moment.

## Approach

Fold the orchestrator's dead ballast, never live evidence, as a hash-anchored migration.

A row is a fold candidate iff ALL hold (byte-checked at run time, in this order):

1. `session_id.startswith("mag-agent-orc-")` - the estate's own orchestrator segmentation
 (mag/tapestry.py:367-370; ids minted by the orchestrator drain, mag/orchestrator.py:501
 orc-<task_id> lineage).
2. `dominant_theme is None` - never gained theme signal (build_leaf_from_dossier's null path,
 mag/verkle_knot.py:282).
3. `theme_vector_normalized` is all zeros - zero theme energy (the default vector,
 mag/verkle_knot.py:265).
4. The knot file named by `filename` is absent from `memory/biography/knots/` - the same
 dangling definition chain_guard uses (mag/chain_guard.py:72). The leaf's evidence is
 already gone; the row is pure chain ballast.

Theme-carrying orchestrator rows (1,158 biography-themed) and every row with a live knot stay.
Nothing verifiable is destroyed: the residual JSONs for all 128 candidates are still present
(checked live), and the pre-fold chain is archived byte-exact with its sha256 embedded in the
counter leaf.

The fold: remove the N candidate rows, insert ONE counter row at the first candidate's
position (order-preserving), recompute the whole chain via the existing `_rewrite_chain`
(mag/verkle_knot.py:407 - reindexes every row, recomputes every prefix root, writes LF-only
bytes per the B2-393 byte law), rewrite the tip atomically (`_write_tip_atomic`,
mag/verkle_knot.py:587), and re-mark the chain_guard canary. The counter row is a first-class
leaf: `leaf_hash = _leaf_hash(payload)` under the same `b"leaf:"` scheme, so the existing
VerkleProof machinery proves its membership unchanged.

Counter payload (schema `verkle_counter_leaf.v1`): count, session_prefix,
`folded_root` (Merkle root over the N folded leaf_hashes in chain order, `_merkle_root`),
`folded_leaf_hashes_sha256` (sha256 of the LF-joined hash list), first/last index and ts span,
`pre_fold_root` + `pre_fold_n_leaves` (the migration anchor), `archived_chain_sha256`,
folded_at/folded_by. `session_id = "orc-noise-counter-v1"`, `filename = null` (chain_guard's
dangling check only counts rows with a truthy filename, mag/chain_guard.py:72, so a null
filename can never read as dangling).

## Why the tip change is a proven migration, not a silent rewrite

The kill condition is "changes the tip with no migration proof". The proof stack:

1. Preflight gate: `_verify_chain_consistent()` must pass before anything moves
 (the 2026-08-16 never-build-on-a-lie gate, mag/verkle_knot.py:536). Refuse on mismatch.
2. Backup-first (the estate's own law, mag/_flag_dangling_20260925.py:34-39): copy
 `verkle_chain.jsonl` + `verkle_tip.json` + `verkle_repair_state.json` to
 `memory/biography/compaction_archive/<UTC-ts>/`; record the chain-bytes sha256.
3. The old tip is not discarded - it is doubly anchored: byte-exact archive on disk, AND
 `pre_fold_root` embedded in the counter leaf now inside the live chain. Any third party
 recomputes the archive's Merkle root and matches it to the counter's `pre_fold_root`;
 any folded leaf's membership in the old chain still proves via `VerkleProof` against the
 archive. The old chain keeps verifying forever as an archived artifact; the live chain
 carries the pointer to it.
4. All under `verkle_lock` (mag/verkle_knot.py:89): the chain moved twice during this design
 session, so the fold must hold the single-writer lock across
 preflight → archive → fold → rewrite → tip → canary re-mark.
5. Post-verify: `_verify_chain_consistent()` green, recomputed root == new tip,
 `prove(counter_index).verified == True`, `python -m mag.chain_guard check` → healthy with
 `tip_matches_chain: true`, zero CR bytes (B2-393), and the canary re-marked with the
 post-fold expected evidence_lost count (the marker is already stale - expected 1031 vs
 live 618, queue/todo.md:198 - so the fold re-marks it with today's truth).
6. Idempotence: the predicate can never re-match folded rows (they are gone); a second run
 finds 0 candidates and writes nothing.
7. Consumers: every tip reader reads the live files (boot_check reports the tail row,
 mag/boot_check.py:54-57; context_pack, bonds, agent_state all load the current tip);
 frozen RIBs embed old tips as snapshots by design and stay verifiable against the archive.

Simulated offline end-to-end on a sandbox copy of the live chain (never touching
memory/biography): numbers and commands in Falsifier.

## Operator gate

The live fold stays operator-gated: the roam verdict ("needs-operator") stands. The CLI ships
dry by default - `python main.py verkle-audit --compact` plans only; the fold executes only
with `--compact --execute` after operator GO, and lands a receipt in watch/inbox/ (shared
artifact boundary law). This design's deliverable is the proven dry path, not a live fold.

(Sections ## Moves, ## Falsifier, ## Owed below - numbers fill from the sandbox simulation
run in this session.)

## Simulation - the migration proof, run on real bytes (2026-09-27T01:20Z snapshot)

`./.venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/cands/sim_compaction.py` copies
the live chain/tip/evolution into `cands/_sim/`, patches module paths the way the estate's own
tests do (tests/test_verkle_audit.py:52-60 patches vk.CHAIN/vk.TIP), runs the FULL migration,
and asserts every obligation. Live memory/biography is never opened for write. Results:

- Preflight: chain consistent, 7,812 leaves, root `c91206a7d8746922…`, 5,470,420 bytes, no CR.
- Candidates: **464** (not 99) - all distinct sessions, ts span one orchestrator drain night
 2026-09-11T17:12→23:24Z, 128 flagged / 336 unflagged, all 464 residual JSONs still present.
- Archive: chain sha256 `348872d048f2a88a…` (recorded in the counter leaf).
- Post-fold: 7,349 rows (464 folded − 1 counter), root `1fa76e568b6bde80…`, tip == recomputed
 root, 341,294 bytes saved (6.2%), zero CR bytes. Counter leaf hash
 `3d2fb741cfabe828…`, lands at new index 25.
- `prove(counter_index).verified == true` - the counter is a first-class leaf under the
 existing proof machinery.
- Archive anchor: recomputed archive root == counter's `pre_fold_root` AND archive sha256 ==
 counter's `archived_chain_sha256` - the old tip is doubly anchored, not discarded.
- Guard strict delta (all exact): dangling 1,374 → 910 (−464), unflagged-dangling 948 → 612
 (−336), flagged 618 → 490 (−128). The fold removes only dangling rows, adds none.
- Idempotence: second scan over the folded chain = 0 candidates. No duplicate session ids.
- Canary re-marked at post-fold truth (`expected 490`, root `1fa76e568b6de80…`).

Numbers are moment-snapshots (the chain grew 7,809 → 7,812 during this session); the
execute-time preflight re-derives everything under the lock.

## Moves with estate paths

1. `mag/verkle_knot.py` - add `compact_orchestrator_noise(*, dry, execute)` under
 `verkle_lock`: preflight `_verify_chain_consistent()` (refuse on fail, mag/verkle_knot.py:536),
 backup-first to `memory/biography/compaction_archive/<UTC-ts>/` (the
 mag/_flag_dangling_20260925.py:34-39 law), predicate scan, counter row build
 (`verkle_counter_leaf.v1`, `_leaf_hash` scheme), reuse `_rewrite_chain` (:407, LF-only
 bytes) + `_write_tip_atomic` (:587), evolution trim via the consolidate precedent
 (:379-397), chain_guard re-mark. No new hash scheme; every primitive already exists.
2. `mag/verkle_audit.py` - `--compact` plan flag; `run_audit` gains a `noise_compaction`
 section (predicate, live candidate count, would-be counter hash/root, archive target);
 `--dry` stays read-only so the estate's own command surfaces the plan.
3. `main.py:1662-1670` - wire `--compact` and the operator-gated `--execute` onto the
 verkle-audit subparser.
4. `tests/test_verkle_compaction.py` - tmp-chain migration test (patch vk.CHAIN/TIP/KNOTS):
 preflight refusal on a broken chain; fold 3 synthetic noise rows among live-shaped rows;
 assert counter count/folded_root/pre_fold_root/archive sha; prove(counter) verifies;
 second run no-op; LF byte law; guard delta obligations hold.
5. `queue/todo.md:31` + `queue/queue_index.jsonl` Q-001 - flip only after operator GO and a
 live execution, citing the receipt; until then the row stays open (roam verdict respected).
6. Receipt to `watch/inbox/` + INDEX row, validate with
 `.venv\Scripts\python.exe -m mag.shared_surface validate` (shared artifact boundary law).

## Falsifier

The judge's runnable commands (named by the kill condition, both run in this session):

- `python main.py verkle-audit --dry` - exit 0 today (ran twice: 01:02Z and 01:23Z, ok:true,
 schema verkle_audit.v1, no report written in dry). Post-landing it additionally surfaces
 `noise_compaction` (plan-only, zero writes).
- `./.venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/cands/sim_compaction.py` -
 re-runs the full offline migration on a fresh snapshot; asserts preflight, archive anchor,
 prove(counter), guard strict-delta, idempotence, byte law; exits non-zero on any breach.
 Writes only inside `cands/_sim/`.
- `python -m mag.chain_guard check` - INSTRUMENT NOTE: exits 0 regardless of state
 (mag/chain_guard.py:208 returns 0 unconditionally); the `state` field is the verdict.
 Live right now: `regression`, 948 dangling-unflagged, marker stale 2026-09-26T16:39 -
 PRE-EXISTING, checked before any fold; this design reduces it by 336 and does not hide it.
- Post-execute (operator-gated) kill tests: counter's `pre_fold_root` must equal the archived
 chain's recomputed root; `tip_matches_chain: true`; dangling-unflagged reduced by exactly
 the folded-unflagged count; second `--compact` = 0 candidates. Any breach → rollback =
 restore archive chain+tip under verkle_lock + re-mark canary.
- Predicate falsifier: if a reviewer names an orchestrator row that is theme-None,
 zero-vector, knot-gone but NOT noise (or vice versa), the predicate is wrong - that is the
 honest dispute surface; it is byte-checkable in one scan.

## Owed

- Operator GO for the live fold (Q-001 roam verdict stands; this lane ships the proven dry
 path, not a live execution).
- Pre-existing guard regression: 948 unflagged-dangling (live 01:14Z) + stale marker - a
 separate batched flag pass (mag/_flag_dangling_20260925.py pattern) is owed to reach
 healthy; the fold alone lands at 612.
- 23,665 knot files vs 7,812 chain rows (~15.8k orphan knots, reverse direction) - separate
 wart, named, untouched here.
- `verkle_gaps`' `chain rows != knot files` check (mag/verkle_audit.py:136) already
 mismatches on the live corpus; the counter row's null filename does not worsen it, but the
 check needs an owner.
- Test landing updates the AGENTS.md census carrier line per the census-denominator law
 (name instrument, moment, delta - never hand-copy a count).
- The 99 in queue/todo.md:31 should be corrected to the measured-at-execution count when the
 row flips; leaving a fossil constant in place after a measured 464 would be the
 retired-1,341-headline disease again.
