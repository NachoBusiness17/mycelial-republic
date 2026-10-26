# B2-112 Reconcile V1 escalation triggers vs the V2 tau band

## Verdict

LANDED. Resolution named: the V1 triggers (a) any axis confidence < 0.7 and (b) any axis score < 0.5 AND confidence > 0.7 are SUPERSEDED, not pre-filters. The V2 two-band cascade replaces them on the routine band and bars any confidence threshold on the derivation band. V1 trigger (c) (derivation checking) survives verbatim as band_derivation.policy: always_escalate, already registered. The governor block now carries the resolution as a dated comment.

## Evidence file:line quotes

- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md:29: "Escalate to the frontier judge when ANY of: (a) any axis confidence < 0.7; (b) any axis score < 0.5 AND confidence > 0.7 (confident failure: the expensive re-derivation cases, JEV's known residual); (c) `failure_class` requires checking a derivation (math, protocol proofs, security claims)."
- configs/lanes.yaml:119-145 (pre-edit, byte-verified): the gate_verdict_v2 block holds band_routine tau 0.90, band_derivation policy always_escalate, invalid_output defer, no_referent unjudgeable. No confidence key anywhere: "cascade_exempt_seats: [rule] # deterministic rule backend ... has no confidence to threshold" then "writable_by: governor". The V1 (a)/(b) triggers appear nowhere in the block.
- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md section 1: "an axis with nothing to check against is UNJUDGEABLE (drift.py VACUOUS shape), never escalated, never accepted".
- configs/lanes.yaml band_derivation comment (pre-edit): "JudgeBench 78.6 vs 93.1; JEV wrong on a third of pairs scored in [0.9,0.95), so no confidence threshold is safe on this band (B2_08)."
- mag/lane_runner.py:236: "CLUSTER_TAU = 0.90          # mirrors gate_verdict_v2.cascade.band_routine.tau (B2-32)" and lane_runner.py:408 comment "No module reads these keys yet; the lane runner still emits scalar GATE_VERDICT rows".

## Work done

- Decided pre-filter vs superseded against bytes: superseded. Rationale on the record: band_routine escalates on score vs tau 0.90 with no confidence input, so a V1 confidence pre-filter would gate escalations on a quantity the registered cascade does not use; on the derivation band B2_08's JudgeBench numbers (93.1 gated vs 78.6 ungated, a third of high-score pairs wrong) mean no confidence threshold is safe, so V1 (a)/(b) as pre-filters would re-admit pairs the band always escalates.
- Governor write: configs/lanes.yaml gate_verdict_v2 block amended with a dated V1-TRIGGERS RESOLUTION comment naming the resolution (SUPERSEDED), the per-trigger disposition, and the evidence. No code paths touched (nothing reads the keys yet, per the block's own header and lane_runner.py:408).
- Post-edit parse check: .venv/Scripts/python.exe yaml.safe_load on configs/lanes.yaml, gate_verdict_v2 present, cascade has 6 keys.
- Queue row B2-112 flipped to carry this receipt pointer; LEDGER row appended.

## Falsifier

Falsifier candidate: any future read of gate_verdict_v2 expecting confidence-based escalate keys (confidence_below or confident_failure) finds them absent, so a V1-shaped consumer would crash or no-op rather than silently apply unregistered thresholds. Discharged: the resolution comment now names the absence as design (SUPERSEDED), so the missing keys are registered intent, not drift. If a later lane registers the V1 triggers as pre-filters without amending this resolution, this receipt's verdict is falsified.

## Bibliography closed

- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (V1 schema + escalation rule, line 29)
- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md (V2 increment, no-referent rule)
- configs/lanes.yaml:119-145 (the governor block, now amended)
- mag/lane_runner.py:236,408 (tau mirror + no-reader status)
- QUEUE.md B2-112 row; memory/burns/LEDGER.jsonl
