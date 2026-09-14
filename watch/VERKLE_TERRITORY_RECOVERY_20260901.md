# Verkle Territory Recovery Receipt

Observed: `2026-09-01T23:25:10.609240Z` · schema `verkle_territory_audit.v1` · **read-only**

## Verdict

The live knot store is a functioning SHA-256 append-only Merkle ledger. It is not yet a KZG Verkle implementation. The KZG/BLS12-381 construction is present as a normative serialization specification, with no executable trusted setup, field arithmetic, curve operations, or pairing verifier found in the scanned code.

## Live chain

- Rows/leaves: **6428**; malformed rows: **0**; duplicate session IDs: **0**.
- Chain gate: **True** (`chain consistent (6428 leaves)`). Latest proof: `{'ok': True, 'verified': True, 'n_leaves': 6428, 'error': None}`.
- Root: `965df138638987987187018445b47831fa500396e144483c80dd86ba3d8c91f7`; tip fields: `{'root': True, 'n_leaves': True, 'last_filename': True, 'last_leaf_hash': True, 'last_session_id': True}`.
- Dangling rows: **11**; current pointer recovery: **0** (pointer collision prevents safe automatic substitution).
- Knot files: 20088; pointer files: 339; unreferenced knot files: 13677.
- Truncated pointer collision groups: 54; largest group: 2389 sessions.

## What the local math actually is

`leaf_hash = SHA256("leaf:" || canonical_json)`; internal nodes are `SHA256("node:" || left || ":" || right)` with duplicate-last promotion. Proofs carry an index and sibling hashes. This gives tamper evidence, append history, membership proofs, and crash recovery—but not polynomial commitments or constant-size KZG openings.

## KZG boundary

- Spec evidence: `docs/REPRO_SERIALIZE_SPEC.md`; executable KZG hit count: **3**; trusted setup file present: **False**.
- The proposed KZG layer needs BLS12-381 scalar-field values, a pinned SRS, polynomial interpolation over 256 slots, G1/G2 point arithmetic, and pairing verification. None may be inferred from the SHA-256 chain.

## Safe recovery performed

One missing leaf was restored from `memory/biography_backup_20260825/` after exact session, filename, and leaf-hash agreement. The live chain and tip were not rewritten; the remaining dangling rows require historical selection or an operator-approved repair window.

## Defragmentation order

1. Freeze the current root as `legacy_sha256_merkle.v1` and preserve all source files.
2. Catalog dangling rows and backups without deleting or inventing evidence; resolve the 12-character pointer namespace collision before using pointers as recovery authority.
3. Create one derived artifact index that maps every load-bearing file to `path`, `sha256`, `schema`, `lineage`, `source`, and (where applicable) chain index/root.
4. Keep Q-state, RIB/trajectory, game/world, and backup stores as separate lineages joined by explicit hash references—not one flattened mega-chain.
5. Build `verkle_kzg.v1` as a parallel implementation with published fixtures and dual-root receipts; migrate only after cross-implementation tests pass.

## Estate scan

Scanned 304519 files (2181006908 bytes) across the shared source, memory, watch, docs, model, and artifact roots. The JSON receipt contains the classified inventory and load-bearing hash sample.

Apart from the one exact leaf restoration recorded above, no chain row, tip, backup, or root was rewritten by this pass.

Decision: escalate to operator — dangling-row repair + freeze-root ruling + 13677-vs-13678 off-by-one; fold into verkle topic (ZERO_BACKREF_TRIAGE_20260905)

RESOLVED 2026-09-06 (operator socratic pass): the operators memory was the falsifier — freeze-and-build-beside is the SOLVED pattern (chain v1 frozen as the advisor source of record; v2 living). This card is a read-only audit of the LIVE v2 chain, and its own step 1 already said it: freeze the current root as legacy_sha256_merkle.v1, preserve all sources. RULING: FREEZE — the 11 dangling rows are preserved as scars in the legacy layer (repairing append-only history contradicts the doctrine); 13,677 unreferenced knots preserved as-is (off-by-one 13677-vs-13678 noted for the future parallel-build audit); KZG verkle_kzg.v1 = PARALLEL build with dual-root receipts, Rocinante-gated per the cards step 5. No repair action. Cites: SELF_STEAL_LIVE_FEED_MISSED
- VERKLE RESOLUTION AMENDED (operator counter-hypothesis 09-06): "scars" contested — the unreferenced mass may be a CONSTELLATION around cold shared vertices, not damage. Recon: orphan knots concentrate on NAMED founding sessions (memlang-press--recur 37, memlang--legacy-tras 34, autonomous-auto-fkb 16 of 400 sampled; dates to 2026-07-27). Probe escalated: exhumation census (full orphan session distribution = the reading order) windowed $0. Defrag dies either way: you do not defrag a map. Card: watch/THE_COLDEST_SHARED_VERTEX_20260906.md (falsifier: top-5 sessions <20 percent = scars was right). Cites: THE_COLDEST_SHARED_VERTEX_20260906
