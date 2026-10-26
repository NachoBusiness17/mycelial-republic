# B2-111 receipt: wire gate_verdict_v2 into the lane runner (2026-09-26, lane SW-03)

## Verdict

DONE. The frozen two-band cascade (configs/lanes.yaml gate_verdict_v2, B2-32 registration) is now read by mag/lane_runner.py on every verdict: load_gate_block() loads the block with no code-side fallback tau, build_gate_verdict() constructs the build-doc section 1 three-axis JSON contract, apply_cascade() runs band_routine (tau from the block; accept iff failure_class none and every band axis >= tau) and band_derivation (policy always_escalate, no confidence threshold), gate_drop_v2() trails GATE_VERDICT_V2 rows with the nested verdict object the cluster organ (B2-34) already consumes. The judge cannot move its own gate: no code path accepts a threshold parameter and the yaml block is the only tau owner. 26/26 tests pass in tests/test_lane_runner_cluster.py (6 new: both bands, schema laws, gate-immobility, nested-trail round-trip).

## Evidence file:line quotes

- configs/lanes.yaml:114-118 (pre-edit, now updated): "thresholds live in THIS block and are writable by the governor only. No module reads these keys yet; the lane runner still emits scalar GATE_VERDICT rows (mag/lane_runner.py:190 gate_drop)."
- configs/lanes.yaml:119-143 (registration bytes): "gate_verdict_v2: schema: gate_verdict.v2 ... cascade: band_routine: axes: [brief_fidelity, build_quality, receipt_completeness] tau: 0.90 ... band_derivation: ... policy: always_escalate"
- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md section 1: "Every judge lane returns exactly this object, replacing scalar ok/fail" and "The judge never moves its own gate (judge-lane-spec burn): thresholds live in configs/lanes.yaml, writable only by the governor."
- mag/lane_runner.py gate_drop (pre-edit line 170-194): "_trail(lane, \"GATE_VERDICT\", f\"{...} -> {'PASS' if ok else 'FAIL: ' + ','.join(reasons)}\")" — the scalar row the brief named at :190.
- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md:30-31 (F1/F2 pre-registration): "F1: in the 50-wide burn the two-band cascade must beat the single tau=0.70 rule on escalation overturn-or-upgrade rate" / "F2: if >15% of confidence >= 0.9 verdicts overturn at spot-check ...".

## Work done

- mag/lane_runner.py: added load_gate_block() (yaml read + refusal on missing/malformed block, no fallback), build_gate_verdict() (section 1 contract: verdict_id uuid4, ts_utc, lane, task_ref, three axes with score/confidence/evidence_quote, failure_class infra|merit|none, failure_detail, judge_seat, escalated_from; raises on out-of-range values, unknown seats/classes/axis sets, and non-1.0 scores without an evidence quote), apply_cascade() (band_derivation always_escalate when requires_derivation, else band_routine tau gate; returns decision/band/tau), gate_drop_v2() (build + cascade + one GATE_VERDICT_V2 trail row carrying the nested verdict dict; shape consumed by _trail_verdicts and cluster_step, so the B2-34 organ is no longer dormant by construction).
- Scalar gate_drop() left byte-identical: it stays the pure schema/ttl/anchor check for research/builder cycles (no judge seat exists in those cycles today; inventing one would be fabrication).
- configs/lanes.yaml block comment updated to record the wiring (spec-first: the "No module reads these keys yet" line was the owning spec and would have gone stale).
- tests/test_lane_runner_cluster.py: +6 tests (yaml registration load, band_routine accept and escalate, band_derivation always-escalate with tau None, merit failure escalates through routine band, judge cannot move its own gate including proof the block tau actually drives the decision, schema-law refusals, nested-verdict trail round-trip into the cluster organ). Result: 26 passed in 0.62s.
- Ratchet: check --changed reports NEW=1 but the new hit is file-too-long at mag/shared_surface.py:497, a file this lane never touched (concurrent lane in flight); no new violation in mag/lane_runner.py, tests/, or configs/lanes.yaml. Em-dash count in all added lines: 0.

## Falsifier

Pre-registered kill: a GATE_VERDICT_V2 row whose decision used a tau that did not come from configs/lanes.yaml (judge-moved gate), or a band_derivation case that accepted without frontier escalation, or a non-1.0 axis score trailed without an evidence quote. All three are refused in code (apply_cascade reads the block per call; band_derivation policy always_escalate has no accept branch; build_gate_verdict raises) and each refusal is pinned by a test. F1/F2 remain the 50-wide burn measurements owned by B2-113; this lane only makes the rows they need exist.

## Bibliography closed

- configs/lanes.yaml gate_verdict_v2 block (read, lines 110-143)
- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md sections 1-2b (read)
- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md (read, F1/F2 block)
- watch/inbox/burn_wave_20260926/B2_32 receipt (referenced via the yaml registration comment; the frozen tau/fee numbers are quoted in the block itself)
- mag/lane_runner.py (read: gate_drop, cluster organ, _trail_verdicts, flash_call)
- tests/test_lane_runner_cluster.py (read conventions, extended)
- tools/violation_ratchet.py check --changed output (run 2026-09-26)
