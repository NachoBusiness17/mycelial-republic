# B2-388 Stale-tip writer hunt

## Verdict

LANDED WITH AN INCIDENT, fully disclosed. (1) The hunt found the defective path: mag/usage_digest.py commit_day's amend arm never bound `root`, so on a same-day re-commit the chain rows were rewritten by _rewrite_chain_unlocked and then the tip construction raised UnboundLocalError BEFORE _write_tip_atomic ran: chain moved, tip left behind, the exact disease the brief hunted and the live dual of the 06:12Z freeze B2-82 repaired. Fixed: the amend arm now recomputes root from the rewritten hashes; probe proves the tip follows the rewrite and equals the recomputed merkle root. (2) THE INCIDENT: this lane's first probe run was not hermetic (it patched mag.usage_digest names but the amend arm's rewrite went through mag.verkle_knot._rewrite_chain, which writes the REAL CHAIN global, and the tip write hit the REAL TIP), so the probe reproduced the disease ON THE ESTATE: memory/biography/verkle_chain.jsonl fell from 9,890 rows to 2 sandbox rows and verkle_tip.json was overwritten. Recovery: both files restored from the matched knotnight-20260912 snapshot pair; the chain verifies (gate: "chain consistent (7757 leaves)", tip_matches_chain true) but TWO WEEKS of chain rows (09-12 to 09-26, roughly 2,100 rows) are lost from the chain INDEX while their underlying knot leaf files remain on disk; a backfill brief (B2-521) is filed. (3) The sweep of all other chain writers found every other path healthy; named below.

## Evidence file:line quotes

- mag/usage_digest.py:212-215 (pre-fix): `if existing_i is not None: rows[existing_i] = chain_row; all_hashes = _rewrite_chain_unlocked(rows); amended = True` with NO root binding; :232 `tip = {"schema": "verkle_tip.v1", "root": root, ...}` raised `UnboundLocalError: cannot access local variable 'root' where it is not associated with a value` (live, captured in B2_388_falsifier_results.json first run).
- mag/verkle_knot.py:723-728 (healthy contrast): the main append/amend path computes `root = _merkle_root(all_hashes)` for BOTH arms after the if/else, then writes the tip; :363-377 prune followed by `_write_tip_atomic(tip)`; :622 repair followed by `_write_tip_atomic(tip)`.
- Probe results (watch/inbox/burn_wave_20260926/B2_388_falsifier_results.json): pre-fix run `amend_exception: "UnboundLocalError..."`; post-fix run `amended: true, chain_rows_rewritten: true, tip_moved: true, stale_tip_state: false, tip_matches_recomputed: true`.
- Incident bytes: chain_guard post-probe: rows 2, tip_root 133bca5f0d848d87 (the probe's sandbox append root); post-restore: rows 7757, tip_root 7c459c004496d18f == chain_root, gate True "chain consistent (7757 leaves)"; state "regression" with flag_drift 2 and marker_root_drift (the guard honestly reporting the snapshot rollback vs the B2-82 marker e26157d613efd104).
- Lost tip (last pre-incident bytes, from this lane's read at lane start): root tail cf38516f284ddd3b7ba1, n_leaves 9896, last_filename 2026-09-26_1947_mag_01a0df42_ce73ddbb.knot.json, last_leaf_hash 8357a7b54cd2..., updated_minute 2026-09-26T19:47:00Z.
- Incident containment: no other estate file was touched (topic_evolution.json carries zero usage-digest mentions; latest.knot.json mtime 15:48 pre-incident; the clobbered intermediates preserved as verkle_chain.jsonl.bak-PROBEINCIDENT-20260926 and verkle_tip.json.bak-PROBEINCIDENT-20260926).

## Work done

1. Swept mag/ and scripts/ for every writer of verkle_chain.jsonl: five rewrite/append sites total (verkle_knot append/amend :723, prune :363, repair :622, usage_digest amend :214, diary_node append :507). Audited each for a following tip refresh: all healthy except usage_digest's amend arm.
2. Wrote the falsifier probe (B2_388_falsifier_probe.py) and caught the defect live: UnboundLocalError on the amend arm.
3. INCIDENT (owned): the first probe run was not hermetic and clobbered the real chain and tip; scoped the damage to exactly two files by mtime and content census; preserved the clobbered bytes as .bak-PROBEINCIDENT files; restored the matched knotnight-20260912 chain+tip pair; verified the gate (chain consistent, 7757 leaves) and chain_guard (tip_matches_chain true); recorded the guard's honest regression signals (963 dangling-unflagged, flag_drift 2, marker_root_drift) as the true cost of the rollback.
4. Fixed the defect with a receipt-carrying comment in mag/usage_digest.py (root recomputed from the rewritten hashes on the amend arm); py_compile OK; ratchet check --changed PASS NEW=0.
5. Made the probe hermetic (sandboxed mag.verkle_knot.CHAIN/TIP/KNOTS/BIO too, scar-tissue comment in the probe) and re-ran: amend returns ok, tip moves with the rewrite, tip root equals the recomputed merkle root, real chain verified untouched after the run (7,757 rows, gate True).
6. Filed the backfill brief B2-521 in QUEUE.md for the lost 09-12..09-26 chain rows (knot leaf files survive; the rebuild is a designed project, not a lane-sized patch), plus this receipt and the LEDGER row.

## Falsifier

The brief's falsifier: "a live code path that rewrites chain rows and leaves the tip root behind, or a named sweep proving none exists." BOTH arms executed: (a) the live path exists and was caught red-handed (UnboundLocalError after rewrite; and the probe's own incident is a second, involuntary, full-scale proof that an unrefreshed tip after a chain rewrite is reachable in practice); (b) the sweep named all five sites with their tip-refresh evidence. Post-fix inversion check: re-running the hermetic probe must show stale_tip_state false and tip_matches_recomputed true; the fix comment names the evidence. Reproduction: run B2_388_falsifier_probe.py (hermetic), and `git diff mag/usage_digest.py` for the amend-arm root binding.

## Bibliography closed

- mag/usage_digest.py (defect site, fixed)
- mag/verkle_knot.py (all five chain-write sites audited; _write_tip_atomic, _rewrite_chain, repair_tip_if_consistent)
- mag/chain_guard.py check output (pre/post incident and restore)
- memory/biography/verkle_chain.jsonl + verkle_tip.json (restored to knotnight-20260912 bytes; clobbered intermediates preserved as .bak-PROBEINCIDENT-20260926)
- watch/inbox/burn_wave_20260926/B2_82_verkle_reanchor_20260926.md and B2_18_stone2b_20260926.md (the brief's named pointers, read)
- watch/inbox/burn_wave_20260926/B2_388_falsifier_probe.py + B2_388_falsifier_results.json (probe and its outputs)
- QUEUE.md row B2-521 (the filed backfill brief for the lost rows)
- Owed: the 09-12..09-26 chain-row backfill itself (B2-521); the diary_node non-atomic tip write (TIP.write_text instead of _write_tip_atomic, torn-tip risk noted in usage_digest.py:243 comment) is registered here as an observation, not fixed in this lane.
