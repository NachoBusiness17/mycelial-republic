# B2-32 GATE_VERDICT_V2 CASCADE WIRE - 2026-09-26

## Verdict

landed (config registration only; code wiring owed as self-fed lane B2-111)

## Evidence

- B2_08_judge_lane_20260926.md:25: "Cascade, two-band, thresholds frozen at registration in configs/lanes.yaml, governor-only writes: routine axes tau=0.90 (expect ~54% accept at ~99% quality retention, blended fee ~57% of frontier); derivation-class axes always escalate ... Invalid output always defers. Contested merit verdicts only: both-orders debias, ties half-credit, rationed." This sentence is the spec the block registers, keys and numbers verbatim.
- B2_08:24: "an axis with nothing to check against is UNJUDGEABLE ... never escalated, never accepted" becomes no_referent: unjudgeable.
- BURN_JUDGE_LANE_BUILD_20260925.md:29: "The judge never moves its own gate ... thresholds live in configs/lanes.yaml, writable only by the governor." becomes writable_by: governor. BUILD:27 "Every non-1.0 score must carry an evidence quote" becomes evidence_quote_law.
- Zero behavior change proven: mag/lanes.py:61 shallow-merges unknown top-level keys (`out = {**defaults, **data}`) and every consumer uses named .get() (mag/lanes.py:70,77,162,175,246; mag/lane_effort.py:99; mag/router.py:183). mag/lane_runner.py:190 (`_trail(lane, "GATE_VERDICT",`) still trails the scalar PASS/FAIL; nothing reads gate_verdict_v2 yet. matrix_router._load_lanes reads its own JSON file, not this config (mag/matrix_router.py:57-62).
- cascade_exempt_seats [rule]: the only "rule" seat shape in the estate is the deterministic fallback backend, mag/desk_conductor.py:319-320 `"backend": "rule", "model": "rule"`. A deterministic check has no confidence to threshold, so it is exempt. If the dispatcher meant another seat, this is a one-line governor amendment, flagged here honestly as the one interpretive step in the lane.
- No tests reference lanes.yaml (grep tests/ empty); SHARED_SURFACE_CONTRACT.json and INDEX.json do not register configs/lanes.yaml.

## Work done

- Appended gate_verdict_v2 to configs/lanes.yaml (lines 110-145): schema gate_verdict.v2; judge_seats [local, flash, frontier]; axes [brief_fidelity, build_quality, receipt_completeness]; scores 0.0 to 1.0 with the evidence quote law.
- Two-band cascade (lines 126-144): band_routine tau=0.90 on the three named axes, on_pass accept / on_fail escalate; band_derivation policy always_escalate for axes whose verdict requires checking a derivation; invalid_output: defer; no_referent: unjudgeable; contested_merit_only both_orders_debias true, ties half_credit, rationed true; cascade_exempt_seats [rule]; writable_by governor.
- Freeze comments carry the JEV receipts (53.7% accept, ~99% retention, ~57% blended fee, JudgeBench 78.6 vs 93.1, wrong-on-a-third inside [0.9,0.95)) so the numbers cite their source at the registration site.
- Verified through the estate loader with .venv/Scripts/python.exe: mag.lanes.load_lanes round-trips every key (tau 0.9, always_escalate, exempt ['rule'], writable_by governor) and leaves default_lane L0 plus lanes L0-L3 intact.
- No code touched. No em-dash added (file carries 4 pre-existing; the new block uses none).

## Falsifier

- F1 (pre-registered, B2_08:30): in the 50-wide burn the two-band cascade must beat the single tau=0.70 rule on escalation overturn-or-upgrade rate; else these thresholds file vacuous and the block reverts.
- F2 (B2_08:31): >15% of confidence >= 0.9 verdicts overturning at spot-check marks local confidence uncalibrated; all verdicts defer until recalibrated, and the governor amends this block, never the judge.
- Wiring falsifier: if a future code lane cannot map this block onto mag/lane_runner.py gate_drop output, the misfit files against this registration, not as a silent code-side patch.

## Bibliography closed

Read in full this lane: B2_08_judge_lane_20260926.md; BURN_JUDGE_LANE_BUILD_20260925.md; configs/lanes.yaml pre-edit whole file; mag/lanes.py 1-80; mag/lane_runner.py 160-199; mag/desk_conductor.py 290-338; mag/matrix_router.py 50-100; mag/doctor.py 195-239; QUEUE.md whole. Greps: GATE_VERDICT, cascade, governor, load_lanes call sites, tests/, SHARED_SURFACE_CONTRACT.json, INDEX.json. JEV/JudgeBench numbers carried from B2_08's closed bibliography (arxiv 2609.26550), not re-fetched; nothing synthesized.
