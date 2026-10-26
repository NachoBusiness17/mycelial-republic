# BURN build-fold-verify 20260926 (verify other windows' landed builds against specs)

## Verdict
steal

## Evidence
1. b2-32 gate_verdict_v2: configs/lanes.yaml:119-145 carries the block as the ledger claims: "cascade: band_routine: tau: 0.90 ... on_pass: accept / on_fail: escalate", "band_derivation: policy: always_escalate", "invalid_output: defer", "no_referent: unjudgeable", "cascade_exempt_seats: [rule]", "writable_by: governor". Its comment: "No module reads these keys yet; the lane runner still emits scalar GATE_VERDICT rows". Confirmed live: mag/lane_runner.py:190 trails scalar `GATE_VERDICT`.
2. b2-34 cluster organ: mag/lane_runner.py:228-236 pins every frozen constant of build doc 2b: CLUSTER_WINDOW_N=20, INFRA_REPEAT_ALARM=0.60, MIN_RATE_EVENTS=10, FOS_RECEIPT_HIGH=0.90, FOS_BUILD_LOW=0.50, CAW_CONF_HIGH=0.90, CAW_TRIPWIRE=0.15, CLUSTER_TAU=0.90. cluster_step (:297) emits counts_by_class and repeat_rate_by_class (None below 10 events), routes "pipe_p1" on the infra alarm, fos lists "verdict_ids": fos_ids[:10] with action "spot_check_never_auto_accept", caw carries calibration_tripwire. _trail_verdicts (:384) reads only GATE_VERDICT_V2 nested verdict objects from queue/lanes/<lane>/trail.jsonl; run_lane (~:904) calls cluster_report_step in try/except.
3. B2-64 drift dashboard: tools/drift_dashboard.py renders per-pair rows "| pair | verdict history | corr | verdict | ref age | window end | DRIFTING-days |" with verdict cells from v2 stamp rows plus v1 markers; docs/DRIFT_BOARD_SPEC.md and dashboard/static/drift_board.html both exist on disk.
4. b2-10 red finding (B2_10_playtest_prereg_20260926.md): "provably lacks four landed fixes: t74 ShadowLedger UpdateAsync, t67 derived join, t63 garden signals, t72 GalleryZone annotations. Proven against build bytes by grep, not mtimes." B2-29 closure greps only two of the four on the rebuilt bytes: "UpdateAsync now 2 hits (was 0), GetAsync(key) 0 hits (was 1), t72 annotation exactness 8 hits (was 0)". No t67 or t63 grep appears in B2_29_rbxlx_rebuild_20260926.md, and grep over watch/inbox/burn_wave_20260926/ finds t67 only in the B2-10 prereg itself.

## Steal or Vacuous
- b2-32: VERIFIED as a config registration per its own claim (dormant, zero code reads it, governor-only). Gap: no conf_floor field; the build-order section 1 rule (any axis confidence < 0.7) was superseded by the B2_08 two-band shape, which per B2_08 falsifier F1 must beat the single tau=0.70 rule.
- b2-34: VERIFIED. Per-class counts, 0.60 infra alarm, both detectors, min-events rate law, bounded fos ids, and dormancy all match sections 2 + 2b byte for byte.
- B2-64: VERIFIED. Pair verdict history, corr, ref age, and DRIFTING streaks render to drift_board.html.
- b2-10: PARTIAL closure. The pre-registered P0 falsifier (UpdateAsync >= 1, GetAsync(key) == 0) is cleared on the rebuilt bytes and t72 is re-proven, but the red finding named four missing fixes; t67 derived join and t63 garden signals are never re-grepped on build bytes. The full-src rebuild implies them structurally; byte proof is absent. Residual: one grep pair owed before Sep-29.

## Falsifier
none proposed

## Bibliography (closed)
watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md · memory/burns/LEDGER.jsonl (rows b2-10, b2-29, b2-32, b2-34, B2-64) · configs/lanes.yaml · mag/lane_runner.py (185-195, 220-444, 900-910) · tools/drift_dashboard.py (grep) · docs/DRIFT_BOARD_SPEC.md + dashboard/static/drift_board.html (existence) · watch/inbox/burn_wave_20260926/{B2_10_playtest_prereg, B2_29_rbxlx_rebuild, B2_08_judge_lane}_20260926.md · burn_wave_20260926 t67 sweep
