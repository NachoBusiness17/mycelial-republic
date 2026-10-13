## Finding — what your cell yields
**Supported with one correction.** The chain-stop (DR-01) and recount (DR-02) are reconciled and falsifiable. The twelve-ledger claim (DR-03) is **not a migration** — it is a rope-and-loom metaphor in GROUNDING_WAVE.jsonl misread as a technical claim. No migration ever executed; the "twelve ledgers" never existed as separate ledgers to consolidate.

## Evidence — what in the repo supports it (file/shape, no invention)
- **DR-01 chain-stop**: `memory/biography/verkle_chain.jsonl` — 7,924 rows, index 0–7923 continuous, parent chain zero breaks, tip root matches `verkle_tip.json`. The Sep-6 stop is healed; `repair_tip_if_consistent()` executed 2026-09-13, backup at `verkle_tip.json.bak-poison-20260913T022403Z`.
- **DR-02 recount**: `memory/vault/astra_v2_companions/failure-ledger-recount.json` — 74,842 valid JSON rows total; the 24,854 figure is `distinct_raw_row_hashes` for signature `run_shell:c73866f2f1b5` across 706 sessions (2026-08-06 to 2026-09-11), not a chain leaf count. Chain has 7,924 leaves. These are different counts — no discrepancy.
- **DR-03 twelve-ledger**: `watch/GROUNDING_WAVE.jsonl` — 114 rows, 1 loom reference, a metaphor line ("canon_weld: staying-is-the-sport + the rope-and-loom line"). `docs/audit_prep/DISPUTED_ROWS_INDEX.md` cites `dist_audit/.../packs/p80_loom3_20260912.json` line 215 — file does not exist in repo. No migration executed.

## Risk if wrong — what the audit breaks on if this is missed
If the examiner treats DR-03 as a real migration claim, he will look for the typed loom ledger, find nothing, and conclude the house filed a falsifiable claim it cannot support — which destroys trust in the other two rows. The meta-risk: the house's "answer before he asks" strategy fails if the answer itself is built on a misread.

## The act — the concrete prep step (file/spec/number)
- **File**: `audit_prep_verkle/DISPUTED_ROWS_CELL.md` — this cell.
- **Spec**: Correct DR-03 status from UNPROVEN → DISPUTED (metaphor, not a migration); remove the non-existent `p80_loom3_20260912.json` citation from `docs/audit_prep/DISPUTED_ROWS_INDEX.md`; add the 24,854 = `run_shell` signature count footnote to DR-02.

## Falsifier — what would prove this wrong
- DR-01: A parent-chain break or index gap in `verkle_chain.jsonl`.
- DR-02: A row in the failure ledger with `distinct_raw_row_hashes` ≠ 24,854 for `run_shell:c73866f2f1b5`.
- DR-03: An executed migration row in `GROUNDING_WAVE.jsonl` or an actual `p80_loom3_20260912.json` file with a twelve-to-one ledger migration script.
