# B2-34 CLUSTER-ORGAN DETECTORS - 2026-09-26

## Verdict

landed

## Evidence

- Spec filed BEFORE the code it owns: watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md:39, section 2b heading names this lane and the spec-before-code order.
- Detector 1 mag/lane_runner.py:332 "def _fos_match": receipt_completeness >= FOS_RECEIPT_HIGH (0.90) with build_quality <= FOS_BUILD_LOW (0.50); action "spot_check_never_auto_accept" per B2_08.
- Detector 2 mag/lane_runner.py:354 "caw_overturns += 1": fires only when the escalation parent carries max axis confidence >= CAW_CONF_HIGH (0.90) and the frontier decision differs from the parent's proposed decision (accept iff every axis score >= CLUSTER_TAU 0.90 and class none); rate only at >= MIN_RATE_EVENTS (10), tripwire > 0.15 = falsifier F2 of B2_08 (:379 "calibration_tripwire").
- Window organ mag/lane_runner.py:403 "def cluster_report_step(lane: str)": one CLUSTER_REPORT trail + surface row per CLUSTER_WINDOW_N=20 verdicts; run_lane hook :904, wrapped so the organ never breaks the lane loop.
- Dormancy proven on live bytes: real lanes answer "dormant(0 pending)", trail bytes and runner_state unchanged, because configs/lanes.yaml:112 (B2-32) records "No module reads these keys yet; the lane runner still emits scalar GATE_VERDICT rows".
- Source verified this lane against arxiv 2609.26550 HTML, verbatim: "JEV is wrong on a third of the pairs it scores in [0.9,0.95)"; "a typed probability output alone does not establish that it is calibrated"; "JEV scores 84.0% when the two answers share a style but 74.8% when the rejected answer is the more elaborately written one".
- Pass-e law honored ("never gate on rate below 10 events", BURN_judge-lane-spec_20260926_e.md:18): MIN_RATE_EVENTS guards the alarm and detector rates; counts always reported. Pass-e MSR classes NOT absorbed: unknown failure_class values key their own bucket.

## Work done

1. Owning doc amended first: 2b section (:39-92): decision rule, constants, routing, dormancy scope, sources.
2. mag/lane_runner.py: constants (:226-243); normalize_detail (:244, pinned build-doc verbs + gate families missing / ttl / anchor); cluster_step (:297, pure: per-class counts, cross-window and intra-window repeats (reported, never gated per pass d), infra repeat > 0.60 routes pipe_p1, both detectors); _trail_verdicts (:384, reads GATE_VERDICT_V2 nested verdict objects from queue/lanes/<lane>/trail.jsonl, the file gate_drop actually writes); cluster_report_step (:403, rolling driver, prev-window keys persisted in runner_state.json); import re; run_lane hook (:904). One defect caught mid-build: an or-default draft treated build_quality 0.0 as missing; explicit None checks now, test-pinned.
3. tests/test_lane_runner_cluster.py: 19 tests pass (0.29s): verbs, counts, alarm routing, min-events None rates, fos zero-score edge, caw overturn / tripwire / below-threshold / orphan / undecidable child, driver dormancy + rolling windows.
4. Gates: tools/violation_ratchet.py check --changed -> "RATCHET: PASS - no unregistered debt" (hits=5, registered=5, NEW=0). py_compile OK. Full suite (pytest -q, this lane): 38 failed / 1728 passed / 9 skipped / 1 error in 913.33s; a last-failed rerun names all 38 (memlang x5, desk_baseline_probe x6, water_computer x5, 12 more across spore_seed, falsifier_ledger, quota_billable, organ_map and singles): the pre-existing census class; zero in tests/test_lane_runner_cluster.py, zero touching mag/lane_runner.
5. Em-dash law: zero in every byte this lane wrote; 29 pre-existing docstring dashes in lane_runner.py left as history.

## Falsifier

Pre-registered: the organ is proven by replay over the frozen schema; zero live GATE_VERDICT_V2 verdicts exist, so live-fleet detector behavior is UNPROVEN until the V2 emission lane lands (configs/lanes.yaml:119 read by zero modules; B2-111 owns it). If that lane changes the row shape (nested "verdict" key, escalated_from, axis fields), tests/test_lane_runner_cluster.py must be amended in the same lane or the organ is dead code. The F2 tripwire stays undecidable until a spot-check protocol with a denominator exists (self-fed B2-193 after the B2-53 renumber deleted the first B2-126 append; the LEDGER row cites the old numbers).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md; watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (amended); BURN_judge-lane-spec_20260925_c/d + 20260926_e; configs/lanes.yaml :109-145; mag/lane_runner.py (read in full pre-edit); mag/law.py:47; tools/drift.py; arxiv.org/html/2609.26550 (quotes verbatim); LEDGER.jsonl tail; QUEUE.md.
