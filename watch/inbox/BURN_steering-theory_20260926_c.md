# BURN steering-theory 2026-09-26 _c

## Verdict
steal

## Evidence
- tools/drift_dashboard.py line 48: `LEDGER = ROOT / "memory" / "runs" / "adv_arc_50" / "teleo_drift_stamps.jsonl"`. That is the only verdict source it reads. `grep -n "probe20" tools/drift_dashboard.py` exits 1: zero hits. It never reads memory/runs/probe20/ or watch/inbox/PROBE20_steering_v1.jsonl.
- tools/probe20_run.py line 38: `SERIES_DIR = os.path.join(REPO, "memory", "runs", "probe20")`; series_path() writes `<lane>_<pair>_series.jsonl`. `grep -n "probe20" tools/drift_pairs_stamp.py` also exits 1: the T1-T6 stamper never touches pairs A/B.
- Dashboard executed live (venv python, 2026-09-26T21:05Z): renders exactly T1-T6. T1 DRIFTING corr -0.0271, 7d streak since 2026-09-19; T3 DRIFTING -0.0759, 7d; T4/T5 DRIFTING; T2 ALIGNED +0.8839; T6 ALIGNED +0.6387. 4/6 pairs currently DRIFTING. No pair A or B row exists anywhere in its output.
- memory/runs/probe20/ exists and is empty (scratch rows deleted after the 20260926 verification, per that receipt). tools/ listing has no probe20_client.py: the _b client spec is unbuilt.
- Runner demo re-executed: "drift import from tools/drift.py: True"; demo2 raw INVERTED corr -0.5748 overridden "INSUFFICIENT", "noise floor: net |delta referent| 0.050 < 0.10 across window".
- Web: search returned nothing dated September 2026. OpenReview API fetch (api2.openreview.net/notes/search?term=log probability tracking drift) returned `{"notes":[],"count":0,"searchUnavailable":true}`. Field quiet, fourth consecutive burn.

## Steal or Vacuous
Steal: the end-to-end gap analysis, closed.
(a) No. The dashboard renders verdicts from memory/runs/adv_arc_50/teleo_drift_stamps.jsonl plus REFERENTS source files (LINKS.jsonl, mrpool ledger, lane trails, gates.jsonl, events.jsonl, burns LEDGER.jsonl). It contains no probe20 path.
(b) No direct consumption. The runner emits raw cycle rows (cycle, margin, correct); the board needs teleo_drift_stamp.v2 rows (pair_id, week_key, stamped_at, nested verdict dict). A format bridge is required.
(c) The runner-to-series link exists (append in probe20_run.py main). The series-to-dashboard link is MISSING entirely: nothing writes pair A/B verdicts into the stamps ledger, nothing reads the series.
Single piece remaining before a real gemma4 margin flows end to end: an A/B stamp bridge, one writer that runs evaluate() on a series and appends v2 stamps to teleo_drift_stamps.jsonl, plus two REFERENTS registry rows (build_table derives pair ids from ledger stamps, so an A/B stamp would render immediately, ref_age n/a until registered). Caveat never synthesized: the _b live client is specced but unbuilt, so model-to-board flow still needs client build plus this bridge; the bridge is the link this pass newly exposes as never-specced.

## Falsifier
Pre-registered for the bridge build: if pair A/B cannot ride the v2 stamp schema and the existing dashboard without code changes beyond one writer plus two REFERENTS rows, the one-writer claim is falsified and the bridge is re-scoped as a dashboard change before any build. Standing falsifier unchanged (_c): both pairs on both lanes returning only VACUOUS, DRIFTING, or INVERTED demotes the confidence-as-drift-pair build VACUOUS and stops it; any ALIGNED keeps it alive.

## Bibliography
- Repo, read 2026-09-26: tools/drift.py, tools/probe20_run.py, tools/drift_dashboard.py, tools/drift_pairs_stamp.py (head), watch/inbox/PROBE20_steering_v1.jsonl (meta+tasks), memory/runs/gps_50/FOLD.json, docs/DRIFT_BOARD_SPEC.md (existence), watch/inbox/BURN_steering-theory_20260925.md/_b/_c/20260926.md/20260926_b.md.
- Executed 2026-09-26: probe20_run.py --demo, drift_dashboard.py (T1-T6 table above), grep probes, directory listings.
- https://api2.openreview.net/notes/search?term=log%20probability%20tracking%20drift (fetched 2026-09-26: empty, searchUnavailable true).
- Web search 2026-09-26: confident-ai.com observability roundup, mbrenndoerfer.com monitoring guide, W&B Weave, MLflow drift pages. Snippet level only, unread beyond snippets, uncited above.
