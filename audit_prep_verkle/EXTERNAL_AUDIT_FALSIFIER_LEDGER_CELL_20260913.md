## Finding — what your cell yields
The house’s self-caught failures are **presented as a tri-state falsifier ledger** (Supported/Disputed/Unproven), each row backed by a named falsifier and a concrete evidence pointer. The examiner can falsify every claim by attempting to resolve the evidence path or by running the falsifier.

## Evidence — what in the repo supports it (file/shape, no invention)
- **Falsifier ledger**: `watch/GROUNDING_WAVE.jsonl` (114 rows) — every row carries `verdict`, `evidence`, and `hash`; v3 rows require a second witness to remain SUPPORTED; legacy rows auto-demote to UNPROVEN if unwitnessed. Row 61 explicitly names the twelve-ledger metaphor as a **rope-and-loom metaphor**, not a migration claim.
- **Chain integrity**: `memory/biography/verkle_chain.jsonl` (7,924 continuous rows, index 0–7923) — parent chain zero breaks, tip root matches `verkle_tip.json`; Sep-6 stop healed by `repair_tip_if_consistent()` executed 2026-09-13.
- **Recount clarification**: `memory/vault/astra_v2_companions/failure-ledger-recount.json` (74,842 valid JSON rows) — the 24,854 figure is `distinct_raw_row_hashes` for signature `run_shell:c73866f2f1b5` across 706 sessions (2026-08-06 to 2026-09-11), not a chain leaf count.
- **Disputed-row ledger**: `audit_prep_verkle/DISPUTED_ROWS_CELL.md` — reconciles DR-01 (chain-stop), DR-02 (recount), and corrects DR-03 (twelve-ledger) from UNPROVEN to DISPUTED (metaphor, not migration).
- **Receipts and manifests**: `scripts/audit_bundle.py` produces a sanitized 1,564-file/20.5MB bundle with SHA256 manifest; `dist_audit/` holds the raw evidence set referenced by the ledger.

## Risk if wrong — what the audit breaks on if this is missed
If the examiner treats DR-03 as a real migration claim, he will look for a typed loom ledger and find nothing, concluding the house filed a falsifiable claim it cannot support — which destroys trust in the other rows. The meta-risk: the house’s “answer before he asks” strategy fails if the answer itself is built on a misread.

## The act — the concrete prep step (file/spec/number)
- **File**: `audit_prep_verkle/EXTERNAL_AUDIT_FALSIFIER_LEDGER_CELL_20260913.md` — this cell.
- **Spec**: Correct DR-03 status from UNPROVEN → DISPUTED (metaphor, not a migration); remove the non-existent `p80_loom3_20260912.json` citation from `docs/audit_prep/DISPUTED_ROWS_INDEX.md`; add the 24,854 = `run_shell` signature count footnote to DR-02.

## Falsifier — what would prove this wrong
- DR-01: A parent-chain break or index gap in `verkle_chain.jsonl`.
- DR-02: A row in the failure ledger with `distinct_raw_row_hashes` ≠ 24,854 for `run_shell:c73866f2f1b5`.
- DR-03: An executed migration row in `GROUNDING_WAVE.jsonl` or an actual `p80_loom3_20260912.json` file with a twelve-to-one ledger migration script.
