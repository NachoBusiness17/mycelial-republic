## Finding — what your cell yields

The bundle's own integrity claims are not reproducible from disk — the softest assumption is that "1,564 files / 20.5MB" describes a delivered package. It doesn't. `audit_bundle/` on disk is 5 files / 36K. The manifest is a description, not a package. Steiniger's abliteration instinct strips the packaging first; what remains is an unsigned claim with no artifact to verify.

## Evidence — what in the repo supports it (file/shape, no invention)

- `audit_bundle/audit_bundle_manifest.md:10` claims "1,564 files, 20.5MB" across 6 categories
- `terminal`: `audit_bundle/` = 5 files, 36K total (INDEX.json, manifest, report, reading_path_schema_TABLE.md, verkle_chain_schema.md)
- `audit_report.md:29` claims "28,874 knot files" — stale vs `watch/inbox/mickey/G2_1_recount.md:4` (29,165 files as of Sep 11)
- `audit_bundle_manifest.md:89` — Gap 1 admits parable-removed control test (Condition B) was never run; Cold Read Test baseline is unidirectional
- `memory/biography/verkle_chain.jsonl` — 7,924 lines (not 7,700+), tip moved since Sep-6 freeze (per `CHAIN_STOP_INVESTIGATION_20260911.md`)
- `EXTERNAL_AUDIT_FALSIFIER_LEDGER_CELL_20260912.md` exists and is substantive — the falsifier ledger itself is real; the packaging around it is not

## Risk if wrong — what the audit breaks on if this is missed

Steiniger walks the abliteration path: strip the claim, test the artifact. If the bundle is only a manifest describing a manifest, the audit fails at step one — there is no 1,564-file bundle to inspect, no 20.5MB artifact to hash, no tri-state rows to trace. The three self-admitted gaps (parable control, cite gate, schema) become fatal, not advisory. The chain-tip mismatch (Sep-6 freeze) is a live integrity question the auditor will find independently — it must be disclosed, not discovered.

## The act — the concrete prep step (file/spec/number)

1. Build the actual bundle: `C:\Users\foste\Documents\projects\local_sovereign_agent\audit_bundle\` must contain 1,564 files / 20.5MB or the manifest must be corrected to reflect what ships. Decide which.
2. Run the parable-removed control (Condition B) — `corpus/canon/COLD_READ_TEST_20260912.md` gap, explicitly admitted in the manifest itself. Three readers, parable stripped, derive organs, record count.
3. Close the chain-stop disclosure: `watch/inbox/CHAIN_STOP_INVESTIGATION_20260911.md` root cause (poisoned tip file `a57b50f3…` vs recomputed `8bd58896…`) must be a row in the bundle with the one-command re-arm proposal and operator GO status.
4. Update `audit_report.md:29` knot count (28,874 → 29,165 per G2-1 recount) or annotate the discrepancy.
5. Verify the reading-path table entries all resolve: `scripts/analyze_claim_timing.py` (exists, 117 lines), `dashboard/static/claim_check.html` (exists), `docs/ref/RTFM_20260904.md` (exists), `audit_prep/verkle_chain_READING_GUIDE.md` (exists), `audit_prep/CLAIM_METRIC_SCHEMA.md` (exists) — all confirmed present.

## Falsifier — what would prove this wrong

- Bundle delivered at 1,564 files / 20.5MB with manifest matching actual contents → this cell's core finding is wrong; the packaging is real.
- Parable-removed control (Condition B) derives ≥5/7 organs → the parable is structural, not causal, and the falsification protocol's Condition B prediction fails.
- Chain re-arm succeeds and tip root matches recomputed root → the Sep-6 stop was a transient gate failure, not a systemic integrity defect; the disclosure overstates the risk.
- Steiniger finds the bundle on disk without being told where to look → the "1,564 files" claim was never meant to be a deliverable, and this cell misread intent for omission.