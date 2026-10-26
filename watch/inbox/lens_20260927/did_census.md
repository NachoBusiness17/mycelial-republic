# DID census - lens 2026-09-27 (48h receipt harvest, mtime >= 2026-09-25 12:00 EDT)

**Total receipts harvested: 778** (rows in `did_census.jsonl`)

- Instrument: `find watch/inbox -maxdepth 2 -name "*.md" -newermt "2026-09-25 12:00"` (local EDT) plus explicit coverage of `burn_wave_20260926/`, `gala_20260925/`, `ractor_panel_20260926/`, `audit_20260926/`, `full_blast_20260926/` and `HANDOFF_*2026092[567]*.md`. Zero files in those subdirs and zero HANDOFF-pattern files fall outside the mtime window, so the find enumeration IS the census.
- Snapshot moment: 2026-09-27 ~09:45 EDT. Same-instrument reruns minutes apart already read +2 files (live repo, hourly burn cron); per the census denominator law this count is one tree at one moment, never a constant.
- Sibling-lens disclosure: `lens_20260927/are_inventory.md` existed at snapshot time and is counted (it matches the mechanical spec); `lens_20260927/doctrine_revisit.md` and `lens_20260927/external_links.md` landed inside my output dir after the snapshot and are NOT counted (same-session lens outputs, not landed-work receipts).
- Claim extraction: each `claim` field is a verbatim byte-substring of the file (whitespace-collapsed, bullet-stripped, cut at 160 chars with an `...[cut]` marker). Methods: 486 landed-line, 287 first-substantial-line, 5 What-landed-section. Skipped: 0 (one file, `ELDER_ASK_SEED_AUDIT_20260926.md`, is UTF-16 LE with BOM and was decoded, not skipped). No claim is fabricated; every line traces to file bytes.
- Date caveat: a handful of counted files carry older dates in their FILENAMES (e.g. `FLEET_IMPRINT_20260917.md`, `REJECTION_TAXONOMY_20260917.md`, `MICKEY17_V2_ENGINE_SPEC_20260924.md`) because they were amended/touched inside the window; grouping below is by MTIME, which is the instrument.
- Wave-scale context (byte-true from `burn_wave_20260926/CLOSE_20260927_NOON.md`): "402 landed with 5-section receipts in watch/inbox/burn_wave_20260926/".

## Counts by day (mtime)

| Day | Receipts |
|---|---|
| 2026-09-25 | 65 |
| 2026-09-26 | 635 |
| 2026-09-27 | 78 |
| **total** | **778** |

## Counts by prefix lane

| Prefix | Receipts |
|---|---|
| B2_ (burn_wave_20260926/ + B2_-named) | 425 |
| BURN_ (freelane burn lanes) | 129 |
| AUDIT (audit_20260926/ + AUDIT_-named) | 30 |
| RACTOR (ractor_panel_20260926/ + RACTOR-named) | 11 |
| GALA (gala_20260925/ + GALA-named) | 8 |
| other | 175 |
| **total** | **778** |

## Strongest landings (20, durable artifacts: tools built, gates wired, laws registered, panels completed)

1. **LAW-12 registered** (`burn_wave_20260926/B2_163_law12_register_20260926.md`): "LAW-12 \"amendment_gate\" (T0) is registered in memory/law/registry.json between LAW-11 and LAW-13, composed from verified bytes".
2. **Scenario-suite gate wired into pre-push** (`B2_164_scenarios_gate_20260926.md`): "githooks/pre-push now carries a workflow_gate_scenarios block" so a workflow_gate.py change cannot push a red suite.
3. **Corpus FTS5, build + wiring** (`B2_22_fts5_spike` + `B2_102_fts5_wiring_20260926.md`): index built "in 12.352s; db 207.6 MB" and corpus_search now "index-preferred ... engine=fts5 (live measured 1.5 to 2.45ms".
4. **FTS rebuild on cadence** (`B2_465_rebuild_schedule_20260926.md`): closes the gap that "The B2-102 freshness gate could detect staleness but nothing rebuilt on cadence" (MagFtsIndexDaily).
5. **Secret scan on a schedule** (`B2_351_secret_scan_schedule_20260926.md`): "schtask MagSecretScanWeekly registered (Mondays 06:40 local, next run 9/28/2026 6:40 AM)".
6. **Census patrol deep check scheduled** (`B2_246_collect_schedule_20260926.md`): the `--collect` deep check "existed only as a flag a human had to remember to type" until it rode MagCensusPatrolDaily.
7. **Estate MCP server as always-on docker** (`B2_291_estate_mcp_docker_20260926.md`): "an always-on docker service: compose service `mcp` (container mag-mcp, image mag-sovereign:local" - landed and running.
8. **SEED-RIB over MCP** (`B2_181_seed_mcp_20260926.md`): "tools/seed_mcp.py (371 lines, schema seed_mcp.v0) serves the SEED-RIB over MCP stdio (JSON-RPC 2.0".
9. **Seed-paired uplift harness** (`B2_155_seed_paired_harness_20260926.md`): "tools/seed_paired_uplift.py implements law D verbatim (paired means, k = ..." - exists and is testable.
10. **Sanctioned-tasks whitelist** (`B2_396_mag_tasks_whitelist_20260926.md`): "configs/sanctioned_scheduled_tasks.yaml (13 rows, each with its register source and expected" schedule).
11. **Writer-key schema registry** (`B2_342_schema_registry_20260926.md`): "configs/events_key_schema.json (events_key_schema.v1) registers every" writer key of index_events.jsonl.
12. **Queue dupes gate** (`B2_486_queue_dupes_gate_20260926.md`): "tools/queue_dupes_check.py ... exit 1 on any id claimed by two or more briefs" - "LANDED and biting".
13. **Checkbox receipt gate** (`B2_316_checkbox_gate_20260926.md`): "tools/checkbox_receipt_gate.py fails a checked Open row" that has no receipt on disk.
14. **Refold gate in pre-push** (`B2_328_refold_gate_20260926.md`): "githooks/pre-push now carries a refold_gate block (WARN-ONLY first landing ...)" running tools/refold_gate.py.
15. **Caption-ledger verifier in pre-push** (`B2_260_verifier_gate_20260926.md`): "githooks/pre-push now carries a caption_ledger_verify block (WARN-ONLY first landing)".
16. **Drift board served** (`B2_64_drift_dashboard_20260926.md`): "The weekly teleo verdict history is now a served lab-UI panel with a spec filed before the code. dashboard/static/drift_board.html".
17. **Test-census truth reset** (`B2_69_test_census_20260926.md`): "The \"1,341 tests\" headline is retired as a hand-copied fossil ... One truth now: 1,837 tests collected" (the number AGENTS.md now carries as 2,303 after later same-day landings).
18. **Ractor panel completed** (`ractor_panel_20260926/`, eight cards, survivor-revised): verkle99.final.md records "Three revisions landed on top of the survivor, each forced by a check".
19. **GALA closed clean** (`GALA_20260925.md`): "punch list: all 5 rows fixed, spot review 8/8 SOLID. All 4 DF owed folds landed as wired".
20. **Spot patrol instrument** (`SPOT_PATROL_LANDED_20260927.md`, 09-27): "tools/ledger_spot_patrol.py, the WARN-ONLY claim-vs-artifact instrument" (pairs with the 09-27 append-gate wiring in APPEND_GATE_WIRED_20260927.md).

Honorable mentions that just missed the 20: `tools/secret_gate.py` built/staged/banked (SECRET_GATE_BUILD_20260927.md), `tools/queue_close.py` close verb (QUEUE_CLOSE_VERB_20260927.md), `tools/envelope_harvest.py` (B2_424), `tools/transport_precheck.py` (B2_327), `tools/openrouter_free_gate.py` live rotation (B2_295), the 30-receipt audit wave under `audit_20260926/`, and the 50-wide workflow envelope proof (ENVELOPE_50W_HIT_20260926.md).
