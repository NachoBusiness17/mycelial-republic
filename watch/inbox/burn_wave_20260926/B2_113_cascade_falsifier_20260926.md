# B2-113 receipt: own the 50-wide cascade falsifier run (2026-09-26)

## Verdict

UNDECIDABLE (NEED_DATA), filed as owed per the no-fabrication law. F1 and F2 are pre-registered in B2_08 but neither is decidable on current bytes: zero GATE_VERDICT_V2 rows exist in any lane trail, so the two-band cascade has never produced an escalation to measure. The sequencing precondition this brief names ("sequence after B2-111 so verdict rows exist") is unmet: B2-111 sits checked [x] on QUEUE.md:288 with no receipt file under watch/inbox/burn_wave_20260926/ and mag/lane_runner.py still emits the scalar GATE_VERDICT at the gate (line 191), its own docstring for cluster_report_step (lines 407-409) stating zero verdicts is the designed dormant state. The lane now OWNS the run: tools/cascade_falsifier_run.py is the standing harness that computes F1 and F2 mechanically from registered vocabulary the moment a burn emits V2 rows, and it ran clean today (exit 0, verdict NEED_DATA). B2-111's unearned checkbox is named here and is left to its own lane or a B2-238 sweep to reconcile; this receipt does not flip another lane's row.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md:30: "F1: in the 50-wide burn the two-band cascade must beat the single tau=0.70 rule on escalation overturn-or-upgrade rate; else the JEV-derived thresholds file vacuous."
- watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md:31: "F2: if >15% of confidence >= 0.9 verdicts overturn at spot-check, local confidence is uncalibrated; all verdicts defer to frontier until recalibrated."
- mag/lane_runner.py:191-193: `_trail(lane, "GATE_VERDICT",` ... the gate still appends the scalar event name, no V2 emitter exists on the path.
- mag/lane_runner.py:398: `if row.get("event") == "GATE_VERDICT_V2" and isinstance(row.get("verdict"), dict):` the reader half landed (B2-34), the writer half did not.
- mag/lane_runner.py:407-409: "Dormant while the lane emits no GATE_VERDICT_V2 rows: the V2 wiring is a separate gated lane ... so zero verdicts means zero reports, never an invented one."
- Measured 2026-09-26: `tools/cascade_falsifier_run.py` output `"gate_verdict_v2_rows": 0`, `"verdict": "NEED_DATA"`, exit 0; trail census 4,697 rows across queue/lanes/*/trail.jsonl, zero carry event GATE_VERDICT_V2.
- watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md:27: "zero live GATE_VERDICT_V2 verdicts exist, so live-fleet detector behavior is UNPROVEN until the V2 emission lane lands (configs/lanes.yaml:119 read by zero modules; B2-111 owns it)."
- watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md:27: "The F2 tripwire stays undecidable until a spot-check protocol with a denominator exists (self-fed B2-193 ...)."

## Work done

1. Built tools/cascade_falsifier_run.py (~150 lines, under the 400 cap): reads queue/lanes/*/trail.jsonl with the exact _trail_verdicts predicate, computes F1 (two-band escalation set per band_routine on_fail + band_derivation derivation classes vs the single tau=0.70 rule counterfactual, overturn-or-upgrade events via escalated_from pairs) and F2 (SPOT_CHECK overturn rate gated at MIN_RATE_EVENTS 10 plus the B2-34 pair_detector rate), never invents rows, exits 0 with NEED_DATA when denominators are under the gate.
2. Ran it on today's bytes: 0 V2 rows, 0 SPOT_CHECK rows, F1/F2 NEED_DATA, py_compile clean. The falsifier run is now a one-command re-run for whichever lane lands the V2 emitter or the 50-wide burn.
3. Verified the precondition breach on bytes (no B2_111 receipt on disk, scalar emission at lane_runner.py:191) and left the B2-111 row to its owner; no other lane's checkbox touched.
4. Remaining owed, named: (a) the V2 emitter (B2-111's actual work), (b) the 50-wide burn that produces escalation pairs, (c) the B2-193 spot-check protocol that gives F2 its denominator. This receipt owns (a re-run of) the measurement, not the missing upstream work.

## Falsifier

Pre-registered (B2_08:30-31): F1 two-band beats single tau=0.70 on escalation overturn-or-upgrade; F2 >15% of confidence >= 0.9 verdicts overturn at spot-check. Decidable the moment tools/cascade_falsifier_run.py reports gate_verdict_v2_rows >= 10 with spot-check denominators >= 10; today it prints NEED_DATA with both denominators 0, which is itself the falsifier of "verdict rows exist": they do not. If a future receipt claims F1/F2 decided without this tool's output naming decidable true, that receipt is void. If B2-111's emitter lands and this tool still reads 0 V2 rows from queue/lanes, the emitter writes somewhere else and files against this receipt.

## Bibliography closed

All read this lane: watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md (falsifier block lines 25-37, bibliography section), B2_32_cascade_wire_20260926.md (falsifier lines 26-28), B2_34_cluster_detectors_20260926.md (detectors and UNPROVEN note), watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (sections 1, 2, 2b, burn pass/fail), configs/lanes.yaml gate_verdict_v2 block (lines 119-139), mag/lane_runner.py (gate ~180-195, _trail_verdicts 384-400, cluster_report_step 402-420), queue/lanes/*/trail.jsonl census, memory/burns/LEDGER.jsonl B2-111/B2-34/B2-35 rows, QUEUE.md rows B2-111/B2-113.
