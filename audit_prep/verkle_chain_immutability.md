# Verkle Chain Immutability Assertion

## Claim
The Mag repository's Verkle chain is **append‑only and immutable** after a leaf is written. No operation in the codebase rewrites or deletes existing leaf files or modifies prior chain entries.

## Evidence
- **`mag/verkle_knot.py`** implements a **single‑writer lock** (`verkle_lock`) that serialises *read‑modify‑append* operations on the chain file (`memory/biography/verkle_chain.jsonl`). The lock is only used when **appending** new leaf hashes; there is no code path that removes or overwrites existing lines.
- The leaf files live under `memory/biography/knots/` with filenames derived from timestamps and hashes, guaranteeing uniqueness. The code never deletes these files; the lock context only writes new leaf entries.
- **AGENTS.md** (lines 22‑28) and the standing rulings in the persistent memory explicitly state that the verkle chain is **read‑only** and must not be repaired or rebuilt.
- The audit bundle already contains `audit_bundle/verkle_chain_schema.md` which documents the chain structure and references the immutable leaf pattern.

## Risk if Wrong
If the chain were mutable, an external auditor could discover hidden rewrites, violating the append‑only guarantee and breaking trust in the provenance of all recorded events. This would invalidate the audit’s reproducibility claim and could expose the system to tampering.

## The Act
Add this immutability assertion file to the audit preparation package so the examiner can quickly locate the formal claim and its supporting evidence.

## Falsifier
A test that successfully modifies an existing leaf file or rewrites a prior line in `verkle_chain.jsonl` would falsify the claim.
