# GENE POOL TOMBSTONE + FOSSIL ARM GENERALIZED — 2026-09-27 (fossil churn)

Operator: "just churn through the fossils." Executes FOSSIL_CENSUS P0-2 and
completes P0-3. Prior landings this arc: QUANTIZER_V03 (P0-1), the context
pack delivery vehicle (3eb6dc251).

## P0-2: the gene pool family is TOMBSTONED, not regenerated

Root-caused before choosing: mag/gene_pool_feeder.py builds genes from five
2026-09-04 audit JSONs, but (a) NO regenerator exists anywhere (byte search:
no tool writes aud_*.json), and (b) NOTHING consumes the output — grep finds
zero readers of gene_pool_gen*.json and zero callers of the module; the
meta_percolate seam injection happens only when the script runs, which was
once. Dead-at-birth, same disease as the packs one layer worse.

Decision (no-bulk-self-processing law): regenerating inputs for an
unconsumed output is meters-not-work. TOMBSTONE instead:
- mag/gene_pool_feeder.py carries the tombstone header (dormant, cause,
  revive condition: a named consumer lands FIRST, then a tools/ audit
  builder, then rerun). The operator law (duplication-is-emphasis) and
  fitness v1/v2 remain recorded experiment truth — deletion-monotonic-
  safety law: no one-way deletion.
- Registry disposition tombstoned for aud_files.json + gene_pool_gen2.json.

## P0-3 complete: the arm is registry-driven

- tools/fossil_check.py: stats every configs/fossil_registry.json entry;
  dispositions recompile (age bar enforced) / tombstoned (never warns) /
  fixed-oracle (tracked, no bar) / watch (bar, no action). Exit 0/1(WARN)/2
  (registry unreadable = cannot-verify incident, fail-closed).
- configs/fossil_registry.json — six entries: quantizer compile_report
  (168h bar), the tombstoned gene-pool family, jev trail (720h watch),
  adversarial_arc (fixed-oracle: the wave stats its size by design), SEATS
  (168h). Adding artifacts = a named config edit, the secret-baseline shape.
- scripts/census_patrol_daily.ps1: the single-artifact quantizer check is
  REPLACED by fossil_check (same WARN-only, attention.md alert, fail-open
  self-error guard; exit>=2 logs cannot-verify per the census law).
- LIVE first run: 6 registered, 0 WARN, 0 HARD (jev 191h vs 720h bar;
  quantizer 0h; SEATS 13h).
- 5 tests pin the arm (WARN fires, tombstones never warn, missing
  registered = HARD, missing tombstoned = ok, unreadable registry = exit 2).
  RATCHET PASS.

## Fossil queue state after the churn

P0-1 done (compiler + recompile + vehicle). P0-2 done (tombstone). P0-3 done
(registry arm). Remaining fossil-adjacent items are NOT artifact fossils but
the suite's 31 pre-existing failures (registered in
WINDOW_CLOSE_20260927_GATEFIX_LENS.md; memlang-first) — a different churn.
