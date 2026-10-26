# BURN: world-models-multi-agent, 2026-09-26 (_e)

## Verdict

steal

## Evidence

Grader built and validated this pass: watch/inbox/mseat_drift_grade.py (stdlib only; exits PASS 0, WARN 1, FLAG 2, error 3). It grades a receipt against MSEAT_DRIFT_FIXTURE_v1.json authoritative_keys and never trusts the receipt's correct flags: it re-derives each claim from fixture truth (exact paths by value equality; name by containment; hooks and desc_facts by anchor selection from expected, then presence routing or token overlap >= 0.9), verifies every expected grounds in fixture truth, recomputes delta by re-checking each transition, and applies the thresholds: alive >= 0.85 and delta <= 1, flag < 0.70 or delta > 1, else WARN; rate clause checked when fields are present.

Validation outputs (fixture's three embedded receipts extracted to temp, graded, temp cleaned):
- example-A-pass: exit 0, accuracy 19/20 = 0.95, delta_raw 0, rate 0.00x, disposition PASS, PROBE_PASS, receipt-flag agreement 20/20, all expectations grounded.
- example-B-flagzone: exit 1, 15/20 = 0.75, delta_raw 0, disposition WARN, PROBE_FLAG, agreement 20/20, all grounded.
- example-C-drift-trip: exit 2, 19/20 = 0.95, delta_raw 2, delta_per_100_turns 10.0, rate 1.00x, disposition FLAG, PROBE_FLAG, agreement 20/20, all grounded.

The first draft FAILED validation and the failure is on record: 16/20 on A and C, 12/20 on B; claims c14, c17, c18 misgraded because the grader bound to the terse asserted field ("Valve-B in work_gallery") while the presence phrasing lived in the claim text, so those claims fell to overlap against an anchor that never names the room. Fix, documented in the file: asserted tokens of entity + room name + function words route as presence (graded against the keyed room's lines); the rest route as property (overlap against the anchor). Second run reproduces all three verdicts. Grep confirms no em-dash in the grader.

Fresh web: one search, "NPC agent evaluation harness game world state grading seat identity persistence September 2026". Junk retrieval: a bonobo optimizer paper and an OSRS guide, no relevant links, nothing late September 2026. No fetch performed.

## Steal or Vacuous

Steal, two items. (1) The working grader: MSEAT-DRIFT now has the full chain, fixture plus grader, both validated. Live seat runs grade only through this script against live world_state.json values, never the fixture copy, per _d's gold-file guard. (2) The validation harness pattern: running a grader over its fixture's embedded worked examples is the regression gate for any threshold or matching change; here it caught the first draft's three-claim failure before anything shipped.

## Falsifier

Pre-registered, extends _d's tamper control. Run this grader against a receipt whose asserted values are copied verbatim from fixture authoritative_keys (the arm 0 lookup seat). Expected: expectations ground, all 20 claims match, disposition PASS, proving the grader alone cannot detect lookup; isolation is what makes arm 0 impossible, so the probe must log seat-side file access. Any PASS from a seat holding watch/inbox read access voids the result.

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md section 6
- watch/inbox/BURN_world-models-multi-agent_20260926_d.md (prior receipt)
- watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json
- watch/inbox/mseat_drift_grade.py (created this pass)
- Web search 2026-09-26 (query in Evidence); junk retrieval, no usable sources
