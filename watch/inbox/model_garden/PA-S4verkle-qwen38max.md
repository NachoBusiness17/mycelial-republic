# PA-S4verkle-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

# SURFACE 4: VERKLE CHAIN - STRANGER AUDIT

## 1. ATTACK SURFACE MAP

### What amend-in-place permits

- `00__verkle_knot.py` `chain_mode()` docstring: "v1 (default): amend-in-place - a re-save of an existing session replaces its row and rewrites the WHOLE chain file (O(n) bytes per save; live forensics: 2,821/8,626 rows were amend rewrites)."
- Amend replaces one row in the series array, reindexes all rows, recomputes the Merkle root over the new leaf set, and atomically rewrites the chain file under `verkle_lock`.
- A write-capable insider who can invoke the same code path (or replicate it) can replace any row's content, recompute the root, and produce a self-consistent chain. No in-repo byte survives to contradict the rewrite. This is stated explicitly in `02__tip_witness.py` module docstring: "the writer can rewrite the whole chain and no in-repo byte survives to contradict the rewrite."

### What the tip witness WOULD catch

- Same-count root change: `02__tip_witness.py` `compare()`: if `witnessed["n_leaves"] == live["n_leaves"]` and roots differ, verdict is `WITNESS-DIVERGENT` with message "same-length rewrite, laundering alarm."
- Chain shrink: `compare()`: if `live["n_leaves"] < witnessed["n_leaves"]`, verdict is `WITNESS-DIVERGENT` with message "chain SHRANK."

### What the tip witness MISSES (proved from code)

- Interior rewrite when the chain has grown since last publish: `compare()` returns `WITNESS-LAG` whenever `live["n_leaves"] > witnessed["n_leaves"]`, regardless of root value. The root is not compared in this branch. An insider rewrites row 50 of a 150-leaf chain; the witness last saw 100 leaves; comparison sees 150 > 100 and reports LAG ("normal growth; publish due"). The rewrite is invisible.
- Any rewrite before the first publish: no gist exists, no external checkpoint, `run_verify` returns exit 2 (cannot verify). The chain is purely internal and fully rewritable.

### The witness is not yet operational

- `02__tip_witness.py` module docstring: "Scope probe 2026-09-30: the current fine-grained PAT has gist READ but gist WRITE denied (POST /gists 403, GET /gists 200). First real publish fails exit 2 with the SCOPE note until the operator widens the PAT."
- Until the flag is flipped, the external witness provides zero protection. The entire chain is a single-writer internal artifact.

### Tool-bug vector: chain_repair

- `01__chain_repair.py` `repair()`: finds the first row whose `verkle_root != _merkle_root(hashes)`, rewrites that row's root fields, and atomically replaces the chain file. A subtle bug in `find_bad_tail_index` (e.g., an off-by-one in hash accumulation) could "repair" a correct row to an incorrect root, or a malicious invocation could target a specific row index.
- The tool stamps `chain_race_repaired` on the row it touches, providing an audit trail. But the audit trail is in the same file it just rewrote.

---

## 2. THREE WEAKEST JOINTS (ranked)

### Joint 1 (critical): Witness gap during chain growth

- Location: `02__tip_witness.py` `compare()`, the `live["n_leaves"] > witnessed["n_leaves"]` branch.
- Claim: Any interior rewrite is undetectable while the chain's leaf count exceeds the last-witnessed count. Since the chain grows continuously (every session commit appends), the window between witness publishes is the entire attack surface.
- Falsifier: If `compare()` also compared roots when `n_leaves > witnessed`, this joint would close. It does not.

### Joint 2 (high): Witness not yet published

- Location: `02__tip_witness.py` module docstring, scope probe paragraph; `run_publish` gated on `--go` flag and PAT scope.
- Claim: The external witness has never been written. The chain currently has zero external anchoring. Every attack in Joint 1 is moot because there is no witness to diverge from.
- Falsifier: A successful `--publish --go` run producing a gist with a valid `MAG-TIP-WITNESS.v1` line would close this. No such receipt exists in the evidence.

### Joint 3 (medium): chain_repair rewrites without independent verification

- Location: `01__chain_repair.py` `repair()`, the block that sets `bad["verkle_root"] = true_root` and rewrites the file.
- Claim: The repair tool recomputes the root from the current leaf hashes. If a leaf hash was already corrupted (by a prior amend or by a concurrent writer), the "repair" cements the corruption as truth. The tool verifies internal consistency (root matches leaves) but cannot verify that the leaves themselves are authentic.
- Falsifier: An independent copy of leaf hashes (e.g., a per-era snapshot) that the repair tool checks against would close this. No such copy exists in the evidence.

---

## 3. PATCH SPEC PER JOINT

### Patch for Joint 1: Per-era interior witnesses

- Spec: After each witness publish, store the full Merkle root at that leaf count as a frozen checkpoint. On `compare()`, when `live["n_leaves"] > witnessed["n_leaves"]`, additionally verify that the subtree root for leaves `[0, witnessed_n_leaves)` still matches the witnessed root. This requires the chain file to expose prefix roots (it already does: each row carries `verkle_root` which is the root of all leaves up to that row).
- Implementation: In `compare()`, when LAG is detected, load the chain row at index `witnessed["n_leaves"] - 1`, extract its `verkle_root`, and compare against `witnessed["root"]`. Mismatch = DIVERGENT (interior rewrite detected).
- Cost: One additional file read per verify. No new storage.

### Patch for Joint 2: Unblock the publish path

- Spec: Widen the fine-grained PAT to include Gists: Read and write, or swap to a classic PAT with `gist` scope. Run `python tools/tip_witness.py --publish --go`. Verify exit 0 and gist URL in state file.
- Falsifier: `tip_witness_state.json` containing a non-empty `gist_id` and a `last_line` matching the live tip.

### Patch for Joint 3: Frozen leaf-hash snapshots

- Spec: At each witness publish, write `memory/biography/snapshots/epoch_{n_leaves}.json` containing the ordered list of leaf hashes at that moment. `chain_repair` must verify its recomputed root against the latest snapshot before writing. If the snapshot disagrees with the live chain, the repair refuses (exit 2) and files an incident.
- Cost: One additional file per publish (~64 bytes per leaf, so ~500 KB for 8,000 leaves). Acceptable.

---

## 4. WHAT THE RESTORE DRILL PROVED AND DID NOT PROVE

### Proved (from `01__chain_repair.py` docstring and code)

- The chain can recover from a race-condition corruption where a concurrent writer committed a root computed over a stale leaf set. The repair tool recomputes the correct root and the chain passes `_verify_chain_consistent()` afterward.
- The single-writer lock (`verkle_lock`) prevents future occurrences of the same race class.
- The repair is atomic (tmp + rename for chain file; `_write_tip_atomic` for tip, per the T1W1 ticket 4 comment in `chain_repair.py`).

### NOT proved

- The drill does not prove that leaf content is authentic. A deliberately forged leaf hash passes the repair because the repair only checks root-vs-leaves consistency, not leaves-vs-reality.
- The drill does not prove resistance to a single-writer insider who controls the lock. The lock is process-local (`O_CREAT|O_EXCL` on a filesystem path); an insider with filesystem access can delete the lock file, hold it, or bypass it entirely.
- The drill does not prove that the chain has not been rewritten in the past. There is no independent baseline. The `chain_race_repaired` stamp is self-attesting: it lives in the same file it claims to have repaired.
- No evidence of a restore-from-external-backup drill exists in the provided files. UNVERIFIED: whether any off-machine copy of the chain or its leaf hashes exists.

---

## DELIVERABLE FALSIFIER

This audit is falsified if: (a) `compare()` is shown to check the prefix root on LAG (it does not, per visible code); (b) a successful gist publish receipt predates this audit (none is present); (c) an independent leaf-hash snapshot mechanism exists elsewhere in the codebase (none is referenced in the provided evidence).
