# BURN steering-theory 2026-09-26 _d

## Verdict
steal

## Evidence
- Built tools/probe20_stamp.py (stdlib plus import of tools/probe20_run.py). The stamp verdict is the runner's own evaluate() output, never recomputed: native VACUOUS kill and the BURN _c noise-floor override ride through untouched.
- Real --dry on the live surface (2026-09-26T21:49Z): "SKIP P20A: no series on disk (nothing to bridge; refusing to synthesize)", same for P20B, "dry: 0 stamp(s) + 0 referents row(s) printed, nothing written", exit 0. memory/runs/probe20/ holds 0 files; the live ledger still reads 12 lines. Nothing appended.
- --demo (in-memory): P20A teleo_drift_stamp.v2 ALIGNED corr +1.0 deltas_used 5; P20B INVERTED corr -0.7908; plus two drift_referent.v1 rows (P20A/P20B paths, key ts). Both stamps carry week_key 2026-W39, pair_id, pair, teleo, stamped_at, nested verdict, window, sources.
- Falsifier proof, temp ledger and temp series only: --apply run 1 appended 4 rows (2 stamps + 2 referents), run 2 appended 0 ("SKIP, already stamped this week", ledger still 4 lines). Unmodified drift_dashboard.load_stamps tagged 2 v2 stamps and 0 referent rows; build_table + markdown_table rendered "| P20A ... | +1.0000 | ALIGNED | n/a () |" and the P20B INVERTED row. ref_age n/a exactly as _c line 19 predicted.
- Gates: violation_ratchet check (81 changed files): 5 NEW hits, none in tools/probe20_stamp.py; the debt is other lanes' in-flight files (mag/shared_surface.py, openrouter_free_gate.py, probe20_run.py, queue_dupes_check.py, transport_precheck.py); no baseline taken. pytest -k "drift or probe or stamp": 66 passed, 1 failed (test_desk_baseline_probe asserts id="deskLocalMode" in a dashboard index HTML; my file is untracked and imported by nothing; pre-existing).

## Steal or Vacuous
Steal: the bridge exists and is proven against the unmodified dashboard. Default dry; --apply is the operator-gated append and refuses when a series is absent. Wiring stays unlanded by design: the operator lands it by running --apply once real series exist. Still missing for end-to-end flow: the _b live client (unbuilt) to file real gemma4 margin rows.

## Falsifier
The _c pre-registered falsifier did not fire: pair A/B rode teleo_drift_stamp.v2 and the existing dashboard with one writer plus two referent rows, zero dashboard changes. Standing falsifier unchanged (_c): both pairs on both lanes returning only VACUOUS, DRIFTING, or INVERTED on real runs demotes the build VACUOUS and stops it.

## Bibliography
- Repo, read 2026-09-26: tools/probe20_run.py, tools/drift_dashboard.py, tools/drift_pairs_stamp.py, tools/drift.py, memory/runs/adv_arc_50/teleo_drift_stamps.jsonl, watch/inbox/BURN_steering-theory_20260926_c.md.
- New: tools/probe20_stamp.py (this pass).
- Executed 2026-09-26: probe20_stamp.py --dry, --demo, temp-ledger --apply twice, dashboard render check, violation_ratchet check (two scopes), pytest drift/probe/stamp slice.
