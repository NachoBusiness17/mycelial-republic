# BURN: build-fold-verify 2026-09-27

## Verdict

green

## Evidence

- gate_verdict_v2 cascade wire (ledger b2-32): `configs/lanes.yaml:120` `gate_verdict_v2:` present, `tau: 0.90` (:129), `policy: always_escalate` (:136), `invalid_output: defer` (:139), `no_referent: unjudgeable` (:140), `writable_by: governor` (:158). Row claimed "lines 110-145"; actual block spans 110-158 (comment head + V1-triggers resolution), shape matches. Loader wire self-fed as B2-111 verified: `mag/lane_runner.py:207` `def load_gate_block()` fail-closed, `raise RuntimeError("gate_verdict_v2 block missing from configs/lanes.yaml")` (:215).
- Cluster organ detectors (b2-34): grep of mag/lane_runner.py for the 8 constants + detectors returned ~50 hits. `CLUSTER_WINDOW_N = 20` (:360), `INFRA_REPEAT_ALARM = 0.60` (:361), `MIN_RATE_EVENTS = 10` (:362), `FOS_RECEIPT_HIGH = 0.90` (:364), `FOS_BUILD_LOW = 0.50` (:365), `CAW_CONF_HIGH = 0.90` (:366), `CAW_TRIPWIRE = 0.15` (:367), `CLUSTER_TAU = 0.90` (:370); `def normalize_detail` (:378), `def cluster_step` (:431), `def _trail_verdicts` (:540), `_trail(lane, "CLUSTER_REPORT", ...)` (:591); both detector names in code (:469, :472), `calibration_tripwire` (:535). Row cites :226-243/:244/:297/:384: symbols byte-true, line numbers stale, drifted ~+120 lines by later edits.
- Drift dashboard (B2-64): `docs/DRIFT_BOARD_SPEC.md` (4,859 B), `tools/drift_dashboard.py` (16,092 B, `OUT_HTML = ROOT / "dashboard" / "static" / "drift_board.html"` :49), `dashboard/static/drift_board.html` (4,067 B) all on disk. Grep `DRIFTING|referent` in drift_dashboard.py: 30 hits. `tools/visor.py:55` tracks the pair.
- Mountain prereg (b2-10): `watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md` (4,357 B) carries "P0 rebuild gate. Run `bash tools/mountain_check`" (:36) and "Whole prereg falsifies if P0 passes but P1-P6 drift from the numbers above" (:65). `tools/mountain_check` exists. B2-29 receipt (3,095 B) on disk: P0 executed, "UpdateAsync 0 -> 2" at ShadowLedger.luau:59. No build claimed NOT FOUND: none owed.
- Web search: two queries 429-rate-limited; one thin 2026 hit (Augment Code, 2026-03-26, pre-merge spec-driven agent verification). Vein thin, no steal from it.

## Steal or Vacuous

All four named builds are real and match their owning specs; the fold's job was verification, and verification passed. Steal for canon: ledger rows that pin `file:line` anchors rot as files grow (b2-34's anchors are ~120 lines stale within one day). Code-build LEDGER one_lines should cite symbols, never bare line numbers; line numbers are cache, symbols are byte truth. The dormant-organ honesty already holds on disk: the organ landed without any V2-row writer existing, exactly as the spec's "DORMANT, an honest no-op" clause demanded.

## Falsifier

Pre-registered build: `tools/ledger_anchor_patrol.py`, WARN-ONLY first (census_drift_patrol shape). It re-greps each LANDED code-build row's named symbols in the named file quarterly; a row whose symbol greps zero is flagged NOT FOUND (owed) and its landing receipt re-opens. Pass: zero silent symbol loss across the ledger. Fail: any LANDED row with zero grep hits whose receipt still reads "landed".

## Bibliography (closed)

- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md
- memory/burns/LEDGER.jsonl (rows b2-10, b2-32, b2-34, B2-64)
- configs/lanes.yaml
- mag/lane_runner.py
- tools/drift_dashboard.py; docs/DRIFT_BOARD_SPEC.md; dashboard/static/drift_board.html; tools/visor.py
- watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md; B2_29_rbxlx_rebuild_20260926.md
- augmentcode.com search result (2026-03-26, title only)
