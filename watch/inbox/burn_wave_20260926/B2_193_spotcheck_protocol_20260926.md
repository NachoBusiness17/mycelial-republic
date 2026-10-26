# B2-193 CAW/F2 spot-check protocol

## Verdict

LANDED. F2 (">15% of confidence >= 0.9 verdicts overturn at spot-check") now has all four missing pieces pinned in watch/inbox/SPOTCHECK_PROTOCOL_20260926.md: (1) DENOMINATOR = all GATE_VERDICT_V2 verdicts with max axis confidence >= CAW_CONF_HIGH 0.90 (not all verdicts, not only escalations); (2) WHO SAMPLES = the rolling cluster organ (cluster_report_step) samples automatically, deterministically (first K high-confidence verdicts of each window), with SPOTCHECK_SAMPLE_K=5 emitted inside every CLUSTER_REPORT as a new "spot_check" section; (3) WHO EXECUTES = the operator is the spot-checker of record, the local janitor may pre-score but a janitor re-score never counts as calibration (F2 is about local confidence lying); (4) HOW MANY + WHERE FILED = at least 20 executed spot-checks per calibration verdict (binomial bound roughly +/-15 points at p=0.15), filed as append-only watch/inbox/SPOTCHECK_<lane>_<yyyymmdd>.jsonl rows; shortfall files SPOTCHECK_SHORTFALL and F2 stays OPEN. The escalation-proxy caw rate remains the always-on automatic tripwire; the spot-check rate is the calibration verdict of record, decidable for the B2-113 falsifier run.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md:31: "F2: if >15% of confidence >= 0.9 verdicts overturn at spot-check, local confidence is uncalibrated; all verdicts defer to frontier until recalibrated."
- mag/lane_runner.py constants: CAW_CONF_HIGH = 0.90, CAW_TRIPWIRE = 0.15, MIN_RATE_EVENTS = 10, and the new SPOTCHECK_SAMPLE_K = 5 with its B2-193 comment.
- mag/lane_runner.py cluster_step (post-change): the new spot_check section {sample_ids, sample_k, population, protocol} rides the same report dict as confident_and_wrong; sampler loop keeps only window verdicts with max axis confidence >= CAW_CONF_HIGH and a verdict_id.
- B2_34_cluster_detectors_20260926.md:11 (the proxy the sampler complements): "fires only when the escalation parent carries max axis confidence >= CAW_CONF_HIGH (0.90) and the frontier decision differs ... rate only at >= MIN_RATE_EVENTS (10), tripwire > 0.15 = falsifier F2".
- watch/inbox/SPOTCHECK_PROTOCOL_20260926.md (the protocol itself, all four definitions + filing home + decidability clauses).

## Work done

1. Read the three pointers; confirmed the gap: Detector 2 is an escalation-parent proxy (distribution statistics are not calibration, per the code comment) and no surface defined a spot-check's who/how-many/where/denominator; pass e counted only 2 clear overturns across 65 LEDGER rows (no denominator to divide).
2. Landed the protocol doc (SPOTCHECK_PROTOCOL_20260926.md) with the four definitions, the filing-home schema, and the void rule (a discharged spot-check whose verdict_id appears in no CLUSTER_REPORT is void).
3. Wired the sampler into cluster_step: deterministic first-K high-confidence sample emitted in every CLUSTER_REPORT; py_compile OK; no changes to the existing detectors or gating.
4. Added a pin (tests/test_lane_runner_cluster.py): window with 2 above-bar + 1 below-bar + 1 id-less verdict samples exactly ["v1", "v3"]; suite 27 passed.
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Decidability is the deliverable: after this lands, the B2-113 falsifier run can compute F2 as overturns/executed over SPOTCHECK_*.jsonl with the pinned denominator and threshold; any pass claiming calibration with fewer than 20 discharged samples, or with samples not traceable to a CLUSTER_REPORT, is invalid by the protocol's own void rule. Code-side pin: a future edit that drops or empties the spot_check section fails test_spot_check_samples_high_confidence_verdicts (red run). Reproduction: run pytest tests/test_lane_runner_cluster.py -q (27 passed) and grep the protocol doc for the four definitions.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md (:31 F2 text)
- watch/inbox/BURN_judge-lane-spec_20260926_e.md (pass-e convention, MIN_RATE_EVENTS alignment)
- watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md (Detector 2 anatomy)
- mag/lane_runner.py (cluster_step, constants, sampler)
- tests/test_lane_runner_cluster.py (pin appended; 27 passed)
- watch/inbox/SPOTCHECK_PROTOCOL_20260926.md (the protocol)
- Nothing owed.
