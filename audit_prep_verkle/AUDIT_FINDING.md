## Finding — what your cell yields
The verkle chain continuity schema provides a falsifiable framework for auditing the append-only cryptographic discipline. The evidence table documents the actual chain state and implementation artifacts needed to verify claims about hash discipline, session mapping, and tip consistency.

## Evidence — what in the repo supports it (file/shape, no invention)
- **memory/biography/verkle_chain.jsonl**: 7,924 append-only leaves with hash chaining (parent_verkle_root[i] = verkle_root[i-1])
- **memory/biography/verkle_tip.json**: Current tip state with root hash 3db7799ff38b803107029eec501dcbf872f48f62f336e21ab3e7e0194a4bea2b and n_leaves: 7924
- **mag/verkle_knot.py**: Implementation with O_EXCL locking, append_verkle_knot() function, and repair_tip_if_consistent()
- **tests/test_verkle_audit.py**: 6 deterministic test cases covering gaps detection, ticket reconciliation, and tip repair

## Risk if wrong — what the audit breaks on if this is missed
The falsifier (Matthew Steiniger) would reject the entire cryptographic memory substrate if hash discipline is broken. Without the schema and evidence table, he cannot verify the append-only claim or confirm that the Sep-6 chain stop and 12 missing knots are documented gaps rather than integrity violations. The 480-lane proof fails if the chain cannot be shown to be cryptographically sound.

## The act — the concrete prep step (file/spec/number)
Created `audit_prep_verkle/` with two JSON artifacts:
1. **verkle_chain_continuity_schema.json**: Falsifiable audit schema with 4 audit targets, known gaps, and step-by-step verification procedure
2. **verkle_evidence_table.json**: Evidence table mapping actual repo files to audit claims, including chain properties and verification commands

## Falsifier — what would prove this wrong
A root hash mismatch between consecutive leaves, mutation of existing leaf data, session_id duplication across leaves, or tip inconsistency where n_leaves doesn't match actual count. The schema requires cryptographic proof of parent_verkle_root → verkle_root chaining for all 7,924 leaves.