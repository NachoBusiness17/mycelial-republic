# PA-S4verkle-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

ATTACK SURFACE MAP (verkle_knot.py + chain_repair.py + tip_witness.py + grounding_wave.py)

AMEND-IN-PLACE MECHANISM (v1 mode, default):
- File: 00__verkle_knot.py:47-62 (chain_mode docstring and function)
- Design: "v1 (default): amend-in-place - a re-save of an existing session replaces its row and rewrites the WHOLE chain file"
- Forensics cited: "2,821/8,626 rows were amend rewrites"

WHAT A WRITE-CAPABLE INSIDER CAN DO:

1. INTERIOR ROW REWRITE WITHOUT TIP CHANGE (witness misses this)
   - Mechanism: Recompute merkle root after modifying any non-leaf row
   - File: 00__verkle_knot.py:131-138 (_merkle_root function)
   - The merkle root at line 131-138 is computed from leaf_hashes list only
   - Any interior row can be modified if leaf_hashes list is preserved and root recomputed
   - The tip witness (tip_witness.py) only sees root + n_leaves
   - File: 02__tip_witness.py:79-86 (compare function)
   - Verdict: WITNESS-MATCH even if interior rows differ, as long as final root and count match

2. CHAIN FILE REWRITE WITH RECOMPUTED ROOTS (full history laundering)
   - File: 00__verkle_knot.py:102-129 (verkle_lock context manager)
   - Lock is advisory per-process; insider with write access can bypass or break stale lock
   - File: 00__verkle_knot.py:102-103 (_LOCK_STALE_SECONDS = 900.0)
   - 15-minute window allows forced unlock by deleting lock file
   - Chain file rewrite: 00__verkle_knot.py (implied in _rewrite_chain, truncated but referenced at line 47)

3. KNOT FILE DELETION/REPLACEMENT (orphaned chain pointers)
   - File: 00__verkle_knot.py:78-81 (session_pointer_v2)
   - File: 00__verkle_knot.py:83-97 (latest_leaf_pointer)
   - Chain rows reference knot files by filename; knot files are unlinked on amend
   - No integrity check verifies knot file existence at chain verify time
   - Forensics: "1,044 chain rows referenced knot files that no longer existed"

4. POINTER POISONING (v2 mode downgrade attack)
   - File: 00__verkle_knot.py:99-114 (latest_leaf_for_session)
   - Falls back to "LAST matching chain row" if pointer missing
   - Insider can delete pointer files to force v1-style resolution
   - No detection of pointer/chain divergence

WITNESS CAPABILITY BOUNDARY (what it catches vs misses):

CATCHES:
- Tip hash change with same leaf count (WITNESS-DIVERGENT at 02__tip_witness.py:79-86)
- Chain shrink (n_leaves decrease, WITNESS-DIVERGENT)
- Append-only growth with honest root computation (WITNESS-LAG triggers publish)

MISSES:
- Interior row rewrite with recomputed root preserving leaf count
- File: 02__tip_witness.py:79-86 compare function: "same count but root differs" is DIVERGENT
- BUT: if root is recomputed to match new interior, witness sees MATCH
- The merkle root is computed from leaf_hashes only, not from row content
- File: 00__verkle_knot.py:131-138: _merkle_root takes leaf_hashes list, not full rows

TOOL BUG SURFACE:
- chain_repair.py: 01__chain_repair.py:44-67 (repair function)
- Repairs "bad tail index" by recomputing root from hashes
- Does not verify leaf content matches stored rows
- Tool can propagate hash-only consistency while content is corrupted

THE 3 WEAKEST JOINTS (ranked):

1. WEAKEST: Merkle root computed from leaf hashes only, not full row content
   - File: 00__verkle_knot.py:131-138 (_merkle_root)
   - Line 135-136: "layer = leaf_hashes[:]" - operates on hashes, not row data
   - Attack: Modify any row field except leaf_hash; recompute root; undetected
   - Falsifier: A row where claim text is modified but leaf_hash unchanged, passing verify

2. SECOND: Tip witness only binds root+count, not interior tree
   - File: 02__tip_witness.py:79-86 (compare function)
   - No interior witness (no per-era snapshots, no frozen copies)
   - Attack: Rewrite history, recompute all roots to match, witness advances normally
   - Falsifier: A chain where first 1000 rows differ but final root matches witness

3. THIRD: Advisory locking with stale break allows forced entry
   - File: 00__verkle_knot.py:102-129 (verkle_lock)
   - Lines 114-129: Stale lock detection via PID check, breakable on PID death
   - Attack: Kill legitimate holder, wait 15min or force stale, acquire lock
   - Falsifier: Lock acquisition by non-holder process without coordination

PATCH SPEC:

JOINT 1 (merkle root from hashes only):
- Location: 00__verkle_knot.py:131-138
- Patch: Include canonical row JSON in hash input, not just leaf content
- New _merkle_root takes list of (row_hash, leaf_hash) pairs
- Row_hash = SHA256(canonical JSON of full row minus hash fields)
- Migration: v2 chain mode required; v1 chains get frozen read-only

JOINT 2 (tip witness only):
- Location: 02__tip_witness.py (new function)
- Patch: Interior-tree witnesses via per-era snapshots
- Implementation: Every N leaves (era boundary), write frozen copy to knots/era_{start}_{end}.json
- Witness line includes: root, n_leaves, era_count, last_era_root
- Era files are append-only, never amended; witness binds era sequence

JOINT 3 (advisory lock):
- Location: 00__verkle_knot.py:102-129
- Patch: Replace file lock with atomic rename-based consensus
- Implementation: Write to CHAIN.new, atomic rename to CHAIN; readers tolerate 1-version lag
- Lock file becomes advisory only for writers; readers never blocked
- Stale detection: Chain file mtime vs tip file mtime divergence alarm

RESTORE DRILL PROOF BOUNDARY:

PROVED (by chain_repair.py existence):
- Chain tail can be repaired when committed root != recomputed root
- File: 01__chain_repair.py:44-67 (repair function)
- Repair recomputes root from leaf hashes, rewrites row
- Post-repair verify passes if hashes list is consistent

DID NOT PROVE:
- Leaf content integrity (hashes may be wrong, not just roots)
- File existence (knot files may be deleted, not checked)
- Pointer consistency (v2 pointers may mismatch chain)
- Historical interior rows (repair stops at first bad tail, does not scan full chain)
- Evidence binding (grounding_wave evidence hashes not cross-checked with verkle chain)

UNVERIFIED: Full chain verify that recomputes all roots from original row content, not cached leaf hashes.
