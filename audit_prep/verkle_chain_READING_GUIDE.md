## Finding — what your cell yields
The verkle chain is a read-only, append-only, hash-chained log of 7,700+ leaves (knots) that serves as the sole, signed historical record of the fleet. It is **not** a blockchain in the consensus sense; it is a deterministic, cryptographically verifiable sequence where each knot’s `verkle_root` becomes the next knot’s `parent_verkle_root`. The chain is reconciled by a completion index, not by repairing missing knots. Root mismatches are trapped as LAW-064 “wrong-unit” errors, not chain corruptions.

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: `memory/biography/verkle_chain.jsonl` (5.5 MB, 7,924 lines as of 2026-09-12 22:08Z).
- Shape: one JSONL line per knot; fields include `ts`, `filename`, `leaf_hash`, `session_id`, `index`, `n_leaves`, `parent_verkle_root`, `verkle_root`, `amended`, `evidence_lost`, `dossier_commit`.
- Integrity: the chain is append-only; earlier lines are immutable. Backups exist under `memory/biography/verkle_chain.jsonl.bak-*`; orphans are reconciled via `chain_index_completion.jsonl`.
- Standing ruling: `AGENTS.md` § “Verkle chain rule (2026-09-07)” and “Standing ruling (2026-09-07, operator-relayed via Sancho)” confirm read-only, no GC, no consolidation, and the 12-missing-knots healing path via blessed seals.
- Tip file: `memory/biography/verkle_tip.json` (483 bytes) holds the current tip hash for quick lookup.

## Risk if wrong — what the audit breaks on if this is missed
- **False positives**: an auditor may treat the verkle chain as mutable or reparable, leading to incorrect claims about “chain repair” or “root fixes” that violate the operator’s standing ruling.
- **Trust erosion**: if the chain is presented as a consensus system rather than a signed append-only ledger, the examiner’s frame (EUT: entropy lattice, emergent ordering) is violated.
- **Falsifier failure**: the examiner’s falsifier expects deterministic, verifiable rows; any attempt to “clean” or “prune” the chain will fail the falsifier’s reproducibility test and break the audit.

## The act — the concrete prep step (file/spec/number)
1. Create `audit_prep/verkle_chain_READING_GUIDE.md` with the following content:
   - Entry point: `memory/biography/verkle_chain.jsonl`
   - Three things to check:
     1) `parent_verkle_root` of each knot equals the `verkle_root` of the prior knot (chain continuity).
     2) `index` increments by 1 and equals `n_leaves - 1` (consistency).
     3) `amended` and `evidence_lost` flags are present and explain any gaps (transparency).
   - One trap: do **not** attempt to “repair” missing knots or re-root the chain; orphans are reconciled by the completion index and blessed seals only.
2. Add a one-line sanity script `scripts/verify_verkle_continuity.py`:
   ```python
   import json, sys
   prev = None
   for i, line in enumerate(open('memory/biography/verkle_chain.jsonl')):
       k = json.loads(line)
       if prev and k['parent_verkle_root'] != prev['verkle_root']:
           print(f"Break at index {i}"); sys.exit(1)
       prev = k
   print("Continuity OK")
   ```
   Make it executable (`chmod +x`).
3. Update `audit_bundle/INDEX.json` to include both files with SHA-256 hashes.

## Falsifier — what would prove this wrong
- A single knot where `parent_verkle_root` ≠ prior `verkle_root`.
- A gap in `index` or `n_leaves` not explained by `amended`/`evidence_lost`.
- Any file that writes to or truncates `verkle_chain.jsonl` or `verkle_tip.json` (violation of read-only).
- Any attempt to “heal” the chain outside the blessed seal path documented in `memory/biography/verkle_repair_state.json`.

---
Operator: this cell is ready for the 480-wide wave. The guide and script are minimal, falsifiable, and grounded in the repo’s read-only verkle chain.
