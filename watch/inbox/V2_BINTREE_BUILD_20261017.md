# V2 BINTREE BUILD 2026-10-17 (coordination note)

Seat: Grok Bot executor ("Ghost" build lane), started 1:58 PM ET Oct 17 2026. Operator: Nacho approved all 8 v2 decisions ("do it all").

## What is changing and why
Building the v2 append-only binary-tree chain (EIP-7864-style, labeled SHA-256, index-ordered rows) alongside the v1 verkle chain.
v1 is frozen as a seed (rows 0..N-1, verified as an exact extension of the signed Oct 15 restore), imported into v2 as rows 1..N, and later
v1 rows are mirrored by a catch-up reconciler and a flag-gated shadow hook (default OFF). Spec: box /workspace/verkle-v2/BINTREE_V2_SEED_SPEC.md.

## Files touched by this build
- NEW mag/bintree_v2.py, scripts/verify_knot_v2.py, scripts/freeze_v1_seed.py, scripts/catchup_v2.py, scripts/checkpoint_v2.py, tests/test_bintree_v2.py
- NEW data dir memory/biography_v2/ (seed/, row log, tip, knots_v2/, checkpoints)
- EDIT mag/verkle_knot.py: one shadow hook (<10 lines) after the v1 append + tip write complete; inert unless chain_v2_shadow is true
- EDIT configs/mag.yaml: add chain_v2_shadow: false (and chain_v2_signing: false); nothing enabled
- Ghost daemon restart in mag-sovereign (kill only the ghost daemon; lab stays stopped)

## Not touched
memory/biography/verkle_chain.jsonl, verkle_tip.json, knots/ (read only). No git. No signing, no publishing. memory/trajectory/steps.jsonl never read.

## Request to other seats
Please do not edit mag/verkle_knot.py, configs/mag.yaml, mag/bintree_v2.py or memory/biography_v2/ until this note is marked DONE.

Status: DONE (2:36 PM ET Oct 17 2026). The file-edit hold is lifted.

## Outcome
- Code is in, uncommitted (no git was run). Hook at mag/verkle_knot.py L1165-1171 is inert: configs/mag.yaml chain_v2_shadow: false.
- Also edited tests/conftest.py: memory/biography_v2 added to the live-estate write fence.
- FREEZE REFUSED on the live chain (decision 4). The live chain (12,157 rows, sha 27da7fd3...) no longer has the Oct 15 restore
  (0da8026d..., 12,016 rows) as an exact prefix. The first 12,016 rows hash to a42477fe....
  - v1 amend-in-place rewrote 4 historical rows: 7, 9, 10 (sessions mag-agent-cl/cu, 8:06-8:07 AM ET today)
    and 5234 (rib_bus_doct..., 9:41 PM ET Oct 16).
  - That re-rooted 12,005 more rows.
  - Report: memory/biography_v2/FREEZE_REFUSED_20261017T181221Z.json. No seed or genesis exists, and catchup refuses.
- Rehearsal on the certified restore copy, into %TEMP%\v2_rehearsal_20261017 (never live):
  - Freeze OK: n=12,017 and root 6d26f329...; 10 bodies missing, 0 withheld.
  - Catch-up against live: +141 knot and +4 amend rows, giving n=12,162 and root 66868c0b...
  - Both proofs verified from an empty folder.
- Ghost: mag-sovereign was restarted by ANOTHER seat at 2:15:44 PM ET. mag_launch spawned ghost pid 12 and lab pid 13.
  The lab is RUNNING (R/D), not stopped. This seat killed nothing.
- Zero new chain rows between 1:40 PM ET and 2:31 PM ET. No FOLD-SKIP in any log.

## Update 3:05 PM ET Oct 17: LIVE v2 seeded from the certified restore (operator-approved)
- Code change: `freeze_v1_seed.py --source-restore FILE`. It refuses unless all of these hold:
  - the file hashes to 0da8026d;
  - it holds 12,016 rows;
  - its v1 root equals the seal's arc_root (ab595c33);
  - the Oct 15 seal verifies with public data only. That means chain_sha = .chain.json, seed_sha = .md, seed_root is recomputed, key de5fc05e962c43ab is pinned, and the Ed25519 signature checks out.
  - `bintree_v2.Chain.genesis` gained doc_extra.
- Genesis and manifest record seed_source=restore_copy plus the live chain at freeze time:
  - live chain: sha b50fc378..., 12,157 rows, restore_is_prefix false;
  - 24 rewritten restore rows, as indexes and field names only.
- Live v2 (memory/biography_v2):
  - Freeze: n=12,017 (genesis + 12,016 seed rows); 12,006 bodies copied, 10 missing, 0 withheld.
  - catchup_v2: +141 knot rows and +24 amend rows, giving n=12,182, root 7a89fb705067cf62e613075e5c3543bae55659c35ef74d0696ac495a841d0b10, chain_id b62c19fe....
  - `--check`: 0 pending. One unsigned checkpoint at n=12,182.
- Amended v1 indexes: 7, 9, 10, 13, 14, 15, 17, 18, 20-24, 718, 972, 4934, 4951, 4958, 4961, 4965, 5234, 6826, 7264, 7907. 20 more were rewritten between 2:15 and 2:44 PM ET, after the container restart.
- Verified from an empty folder:
  - seed row 8009 (full proof, pure Ed25519 backend), the latest row 12181, and the amend for v1 row 7: all OK;
  - a tampered root, a root-swapped proof and a tampered value: all FAIL.
- Tests: 184 passed, 1 skipped (blake3), 1 flaky failure. test_ah19_append_leaves::test_rib_bus_first_ts_survives_republish failed once and passed 3 of 3 rerun alone; it is unrelated to v2.
- Still off: shadow, signing, publishing. No scheduler, no git. Docker and the lab were not touched.

## v1 rewriter (read-only finding, not changed)
- The container lab (`main.py lab`, pid 13, spawned 2:15:46 PM ET) runs the chain:
  1. runtime.run_integral
  2. mag/runtime.py:135 catch_up() (it also runs every mag cycle via mag/daemon.py:63)
  3. mag/health.py:356 chat_source.file_dirty_agent_sessions (mag/chat_source.py:471)
  4. file_agent_session (:480) -> biography.summarize_session(amend=True) (mag/chat_source.py:444)
  5. session_dossier.write_session_pack -> append_verkle_knot (mag/session_dossier.py:544)
  6. mag/verkle_knot.py:1075-1088 (`rows[existing_i] = chain_row` + `_rewrite_chain`)
- Why it repeats: pack_status reports complete:false for these seats (mag/biography.py:453-464), so the unchanged-chat skip never fires and every seat is re-amended.
  - The sweep walks all 3,033 seats in sorted order (logs/mag.jsonl agent_workday_amend n=3033).
  - Each amend gets a new ts and leaf.
- rib_bus_doctrine row 5234 came from the rib_bus fold (mag/rib_bus.py:123 append_verkle_knot, v1 amend).


## Turn 5 update (2026-10-17 ~3:30 PM ET) - v1 append-only amends + v2 shadow ON (Nacho approved)
- configs/mag.yaml L8 `chain_mode: v2` (AH19 append-leaves; was v1), L11 `chain_v2_shadow: true`. Signing/publish stay false. Backup: configs/mag.yaml.bak_20261017T1510.
- mag/verkle_knot.py (backup verkle_knot.py.bak_20261017T1510), gated on chain_mode v2 only:
  L1004-1008 `prev_i` = newest row of the same session; L1018-1021 dedupe fallback for sessions with no v2 pointer file;
  L1083-1085 new row carries `supersedes_index` + `supersedes_leaf_hash`. Old rows are never rewritten under v2.
- rib_bus.py:123 goes through append_verkle_knot -> covered by chain_mode, no change.
- NOT changed (still able to rewrite v1 history via _rewrite_chain): diary_node.py:507, usage_digest.py:266, verkle_knot.py:636 consolidate.
- biography.py:453-464 root cause NOT changed: mark_summarized caps metadata at 200 sessions, so most of the 3,033 seats have no chat_mtime; dropping `not incomplete` alone would not stop the sweep, and L414-415 says incomplete packs are re-filled on purpose.
- Running processes (ghost 2:15 PM, lab PID 1328 2:43 PM [state T, frozen by someone else], autorun 2:45 PM) read chain_mode/shadow from yaml per call -> append-only + shadow live now; they do NOT have the supersedes_*/fallback code until restarted.
- v2 after: N 12,182, root 7a89fb70...0b10, --check 0 pending. 10-min watch 3:17-3:29 PM: no v1 writes at all (lab frozen), 0 old rows changed, shadow_mismatch.jsonl absent.
