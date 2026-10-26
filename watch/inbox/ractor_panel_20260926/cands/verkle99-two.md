# verkle99 candidate two: orchestrator noise compaction design

Writer: cand-verkle99-two (GLM-5.3 max) · 2026-09-26/27 · card verkle99 · scratch receipts in this
directory: `_verkle99_two_sim.py`, `_verkle99_two_sim_out.txt`, `_verkle99_two_audit_dry_pre.txt`.

## Approach

Fold the orchestrator noise leaf CLASS into one counter leaf, not a stale hand count. The card and
queue/todo.md:31 say "99 orchestrator noise leaves"; the byte truth on the live chain at my
simulation moment (2026-09-26 21:05 EDT / 2026-09-27 01:05 UTC) is 950 noise leaves of 7,811
rows. Census law B2-216
applies: 99 was a hand count frozen when the item was filed (it still reads 99 on the 09-15 and
09-17 fifty-wide boards); the design folds the class and the counter leaf records the byte count.

The noise class, defined by bytes and verified on the live chain (all three predicates together,
`_verkle99_two_sim.py::is_noise`):

1. chain row `session_id` starts with `mag-agent-orc-` (the orchestrator seat prefix;
   mag/tapestry.py:364-371 already treats this prefix as second-class and buckets it separately),
2. `dominant_theme` is null (filename slug collapses to `session`, mag/verkle_knot.py:207-211),
3. zero duration (`start_minute == end_minute`, both present).

Measured on the live chain: 950 rows match (895 landed 2026-08, 55 in 2026-09; the minting writer
is no longer in the tree, grep for the prefix finds only consumers, so this is a bounded backlog
with a small straggler tail). 176 of the 950 carry `evidence_lost`; 464 point at knot files that
are already gone. The other 1,753 `mag-agent-orc-*` rows carry real themes (biography 1,158,
mag_hands 406, constitution 106, ...) and are signal: they stay.

The fold (new module `mag/verkle_compaction.py`, sibling of `mag/usage_digest.py`, which is the
estate's own precedent for a non-session leaf type committed through the chain-native primitives,
mag/usage_digest.py:44-56):

- Under `verkle_lock` (mag/verkle_knot.py:90) and only after `_verify_chain_consistent()` passes
  (mag/verkle_knot.py:536-556): partition rows into keep (6,861) and folded (950).
- Write one counter leaf, type `orchestrator_noise_counter_leaf`, schema `verkle_noise_counter.v1`,
  `session_id` `mag-agent-orc-noise-counter-v1`, hashed with the same `_leaf_hash` scheme
  (`sha256(b"leaf:" + canonical json)`, mag/verkle_knot.py:143-145) so `verify_leaf`
  (mag/verkle_artifact.py:59-67) and `prove()` (mag/verkle_knot.py:485-524) treat it as any leaf.
  Fields: `count`, `first_start_minute`, `last_start_minute`, `folded_leaf_hashes_root` (Merkle
  root over the folded rows' leaf hashes in chain order), `folded_evidence_lost`, `folded_dangling`,
  `pre_fold_root`, `pre_fold_n_leaves`, `folded_at`, `folded_by`.
- Insert the counter's chain row at the index of the FIRST folded row (chronology of where the
  noise lived; the tail stays a real session, current tail `mag-agent-orc-t676b4a919a` is themed
  `dashboard` and survives), then `_rewrite_chain(kept + counter)` (mag/verkle_knot.py:407-435,
  byte-exact LF law B2-393 built in) and `_write_tip_atomic` (mag/verkle_knot.py:587-596).
- The recompute is the estate's own O(n log n) path: measured 0.45 s for root + all prefix roots
  over 6,862 leaves on this machine (sim output line `rewrite timing`), 7,811 -> 6,862 leaves.
- Idempotent and re-runnable like `consolidate_chain_one_leaf_per_session` ("safe to run anytime",
  mag/verkle_knot.py:321): a second run finds the counter by session_id and amends it in place,
  folding stragglers into a cumulative count with `folded_leaf_hashes_root` recomputed over ALL
  archived folded hashes, so the chain always commits to everything ever removed.

Why fold instead of delete (this answers the Q-001 roam verdict "deletion on the integrity
substrate", queue/queue_index.jsonl row 1): nothing is deleted from the commitment. Every folded
leaf hash stays provable through the counter leaf, and the raw rows move to an archive, so the
migration is a move under commitment, with an executable inverse. The operator gate stays: the
live fold fires only on operator GO; everything up to that gate is dry.

## Moves with estate paths

1. `mag/verkle_compaction.py` (new). `plan()` (pure: chain bytes -> fold plan JSON),
   `apply()` (lock, verify, archive, rewrite, tip), `unfold()` (inverse), `verify_archive()`
   (migration proof, read-only), importing the private primitives exactly as mag/usage_digest.py:44-56
   already does (`verkle_lock`, `_verify_chain_consistent`, `_load_chain_rows`, `_merkle_root`,
   `_rewrite_chain`, `_write_tip_atomic`, `knot_filename`).
2. `main.py`: register `verkle-compact` next to `verkle-audit` (registration block main.py:1662-1670,
   dispatch near main.py:2764) with `--dry`, `--apply`, `--verify-archive`, `--unfold`.
3. Archive + register: `memory/biography/compaction/orc-noise-<foldts>.jsonl` (byte-exact folded
   chain rows, LF-only write per the B2-393 byte law, each row carrying its original `index`) and
   `memory/biography/compaction/register.jsonl` (one row per fold run: pre/post roots, counts,
   archive path). Backup-first copy of chain + tip to `memory/biography_backup_compact_<ts>/`,
   the pattern of mag/_flag_dangling_20260925.py:34-39.
4. Knot/pointer hygiene inside the same lock: write the counter's knot file + `by-session_v2`
   pointer; delete the 486 existing folded knot files and their `by-session_*` pointers (the
   464 already-missing ones are skips); drop folded sids from `topic_evolution.json` series with
   reindex, mirroring the consolidation path mag/verkle_knot.py:379-397.
5. `mag/verkle_audit.py`: `verkle_gaps` gains a compaction-aware branch: residuals whose sid is in
   the compaction register report `folded (archived)` info instead of `orphan_residual` warn
   (today's loop mag/verkle_audit.py:175-190 would otherwise light up 950 new warns in `--full`);
   audit output gains a `compaction` block reading the counter leaf so `verkle-audit --dry` shows
   fold state (count, roots, archive paths).
6. Canary: after the fold lands, re-mark per the contract at mag/chain_guard.py:54-66:
   `python -m mag.chain_guard mark --expected 442 --root <new root> --note "orc-noise fold v1"
   --by verkle_compaction` (442 = live 618 flagged minus 176 folded; the fold also removes 336
   unflagged-dangling noise rows from the 948 the live check reports). No change to `check()` law.
7. `tests/test_verkle_compaction.py` (new): fixture chain in tmp_path; cases: plan determinism
   (same bytes -> same plan), fold then `verify_leaf` on the counter, fold then `prove()` at the
   counter index, fold then unfold reproduces the pre-fold root byte-exactly, refusal on an
   inconsistent chain, dry makes zero writes, archive is LF-only (`b"\r" not in bytes`).
   Existing surfaces that must stay green: tests/test_verkle_audit.py, tests/test_verkle_lock.py,
   tests/test_chain_byte_exact_io.py.
8. `queue/todo.md` Q-001 line and queue/queue_index.jsonl row 1: annotated, not closed, until the
   operator GO lands the live fold.

## Falsifier

The kill condition disarmed by construction, with commands the judge can run TODAY:

- Dry-run command (estate's own, read-only, ran during this ask, exit 0, output saved to
  `_verkle99_two_audit_dry_pre.txt`): `python main.py verkle-audit --dry`. The judge runs it
  before and after any live fold; it prints tip root + n_leaves + gaps with `dry: true` and writes
  nothing (dry gate at mag/verkle_audit.py:393-400).
- Fold-plan dry-run: `python main.py verkle-compact --dry` once landed; TODAY the judge runs the
  scratch simulation `_verkle99_two_sim.py` (same directory;
  `.venv\Scripts\python.exe watch\inbox\ractor_panel_20260926\cands\_verkle99_two_sim.py`),
  which computes the whole plan read-only on the live chain: matched rows, counter leaf hash
  `98fb050d...`, witness root `6b5b5629...`, would-be new root `c5f4e750...`, 7,811 -> 6,862
  leaves. Output saved in `_verkle99_two_sim_out.txt`. Zero writes: it touches no chain, tip, or
  knot file.
- Migration proof (the "tip changes with no migration proof" clause): four legs, all verified in
  the sim at live scale.
  1. Commitment continuity: the counter leaf carries `folded_leaf_hashes_root`, the Merkle root of
     all 950 folded leaf hashes in chain order; since the counter is itself a leaf of the new
     chain, the new tip commits to every folded leaf hash. Any single folded leaf stays provable:
     inclusion path against `folded_leaf_hashes_root` + the counter's own `prove()` path.
  2. Executable inverse: slot reconstruction (folded rows re-inserted at their archived original
     indexes; kept rows fill the complement slots in order) reproduces the pre-fold chain root.
     Sim verdict: `round trip (slot reconstruction): root == old root: True`. The naive inverse
     (block insert at the first index) FAILS, I broke it on purpose first: noise rows are
     scattered (indexes 1..7809), so the archive MUST carry per-row original indexes; that is why
     `verify_archive` is a command, not a claim.
  3. Kept-row invariance: any mutation of a kept row's leaf_hash or any dropped non-noise row
     breaks leg 2's root equality; the unfold check is the tripwire.
  4. Live-chain safety: the pre-fold root and n_leaves are captured UNDER the lock at apply time
     (the chain moved three times during this ask: tip root bc4a51ef -> 413008f8 -> cbb7bbc6,
     7,810 -> 7,811 rows), then `_write_tip_atomic` lands the new tip, then
     `python -m mag.chain_guard check` must report `tip_matches_chain: true` (it verifies
     recomputed root == tip, mag/chain_guard.py:96-107; live run during this ask shows the check
     working: `ok: false, state: regression` with `tip_matches_chain: true` on the untouched
     chain, output in the transcript).
- Post-apply command set for the judge: `python main.py verkle-compact --verify-archive` (re-runs
  leg 2 against the archive on disk, no writes), `python main.py verkle-audit --dry` (new tip +
  compaction block), `python -m mag.chain_guard check`.
- Pre-registered failure conditions (any one means the design or its landing is wrong):
  (a) `--verify-archive` ever reports root mismatch; (b) post-fold `chain_guard check` shows
  `tip_matches_chain: false` or CR bytes; (c) plan() is non-deterministic on identical chain
  bytes (fixture test); (d) the counter leaf fails `verify_leaf` or `prove()`; (e) dry mode writes
  anything (fixture test asserts zero file mutations).

## Owed

- The live fold itself: operator GO required, Q-001's needs-operator verdict stands until then;
  this card delivers the design plus the runnable dry instruments only.
- `verkle-compact` CLI + module + tests are designed, not landed: no code was modified in this ask
  (the fold was simulated read-only; the sim and its output are the receipts).
- Post-fold canary state stays `regression`: the fold removes 336 unflagged-dangling noise rows
  but roughly 612 unflagged-dangling non-noise rows remain (live check 2026-09-26: 948 unflagged
  dangling of 1,374); healing those (flag or re-fold, the mag/_flag_dangling_20260925.py pattern)
  is separate janitor work this design does not absorb.
- Orphan knot surplus (23,665 knot files vs 7,811 chain rows) predates this card; the fold deletes
  only folded rows' knot files; a general orphan sweeper is owed elsewhere.
- Straggler cadence: 55 noise leaves landed in September after the writer era; a standing re-fold
  cadence (janitor slot, monthly) is an operator decision, the fold is merely re-runnable.
- The card's "99" needs correcting wherever it is copied (queue/todo.md:31,
  watch/inbox/FIFTY_WIDE_BOARD_20260915.md:51, :20260917.md:83) to the class + byte count at fold
  time; per B2-216 the count is a snapshot, the counter leaf is the durable record.
- Not verified this ask: whether folded orc sessions have residual files under
  memory/biography/residual/ (move 5's gap reclassification handles either answer, but the count
  is unmeasured); whether `prove()` at the counter's index collides with any downstream index
  caching (no consumer found that caches chain indexes across appends, but the survey was grep +
  read of the direct chain consumers, not an exhaustive behavioral test).
