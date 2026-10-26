# Y11 — Q-001 restore prep: verkle_restore_prep (2026-09-30)

**Lane:** Batch 2, lane 11/12 · **Files:** `tools/verkle_restore_prep.py` (new, 400 lines) + `tests/test_verkle_restore_prep.py` (new, 5 tests) · No commit, no chain writes.

## What was built

The restore the operator would run for the Q-001 gate, consuming the W3n side ledger (`memory/verkle/repair_20260930.jsonl`, 300 rows classified `recoverable_by_hash`):

1. **Re-verify from bytes** — every ledger row is re-proven against TODAY's chain + disk (`verify_candidate` recomputes the canonical leaf → row `leaf_hash`; newest hash-matching backup wins). The ledger's `recovered_from` is a report, never proof.
2. **Re-embed** — byte-exact copy (tmp + `os.replace`) of the verified backup into `memory/biography/knots/<filename>`.
3. **Re-link** — post-copy, `row.filename → knots/<filename>` must resolve and the dest must recompute to the row's `leaf_hash`.
4. **Verify full chain** — merkle root over ALL leaf hashes, last-row `verkle_root` + tip agreement (the `_verify_chain_consistent` law re-rooted), links verified, and chain_guard's regression predicate cleared with the ledger merged (`dangling_unaccounted_effective == 0`).

**Gate law:** `--dry` writes nothing. `--confirm` requires the literal string `OPERATOR-GO-Q001` as its argument — anything else refuses exit 3 before a byte moves. Confirm holds the estate verkle lock (same file + law as `mag.verkle_knot.verkle_lock` on the live estate; estate-rooted so fixtures can't take the live lock) and never writes chain/tip/marker/ledger — chain+tip shas proven byte-identical under the lock. A ledger that promised N recoverable rows must account for all N; any unverifiable/gone row degrades the run to exit 1 with named keys. `latest.knot.json` refreshes only if the chain tail itself was restored (`_sync_latest_knot` law).

## Tests (5 passed, `pytest tests/test_verkle_restore_prep.py tests/test_verkle_dangling.py -q` → 13 passed)

- fixture restore end-to-end (knots return as backup bytes, hash-linked, latest.knot refreshed, chain/tip/marker/ledger byte-exact, idempotent rerun restores 0 / already-present 2)
- `--dry` reports the full plan (count, source→dest paths, expected tip) with byte-proof no-writes
- wrong confirm string refuses (exit 3, nothing written, no lock left behind)
- tampered backup skipped by hash (exit 1, shortfall surfaced with named keys)
- missing chain → cannot-verify exit 2

Ratchet: `violation_ratchet.py check --changed` → PASS (0 new debt).

## REAL `--dry` on the live 300 (exit 0, 2026-09-30)

```
rows_recoverable_in_ledger = 300    rows_to_restore = 300
rows_already_present = 0            rows_gone_from_chain = 0
rows_source_unverifiable = 0
expected_tip.root   = 722c269996b7f4c498c08cde02ea7eb9a08f20cb48f997f1af3ca81e0d6edeb5
live_tip_root       = 722c269996b7f4c498c08cde02ea7eb9a08f20cb48f997f1af3ca81e0d6edeb5   (match: true, n_leaves 8500)
chain_sha256_will_stay = cff45b179cfb4d03f534e21c22de21355b6437932f83a5bd55b23504203df0f2
post_restore: dangling 371 -> 71, unflagged 0
source backups chosen: 20260921 x182, 20260926 x114, 20260927 x3, 20260928 x1
```

Full 300-entry plan: `%TEMP%\y11_dry_report.json`. Dry no-write byte proof: chain/tip/ledger sha256 identical before/after (snapshot `%TEMP%\y11_pre_dry.sha.json`). Note: the chain grew 8499→8500 rows (a live fold) between lane inspection and the dry run — legitimate B2-387 motion; the expected tip is the recomputed root at dry time and the confirm path re-plans under the lock.

## The ask (operator)

```text
.\.venv\Scripts\python.exe tools\verkle_restore_prep.py --dry     # re-check the plan is still 300 clean
.\.venv\Scripts\python.exe tools\verkle_restore_prep.py --confirm OPERATOR-GO-Q001
```

Restore moves knot bytes only; the chain and tip must not move. On completion chain_guard's regression clears (71 flagged rows remain, honestly accounted).
