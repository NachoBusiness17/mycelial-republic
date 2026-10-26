# IMP2 D2: Amendment 9 drafted, calibration survivorship kill (spec-only)

Date: 2026-09-30 (lane dating). Owner lane: IMP2-D2, AA1 read-side kill 2.
File owned and touched:
watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md (AMENDMENT 9,
batch IMP2-D2, appended after the IMP3/AMENDMENT 10 batch). No code
changed; no tests written (spec-only per mission). Amendment 8 remains
reserved for the D1 sibling (kill 1, drift-window guard); the IMP3 batch
header confirms the allocation.

## The kill (AA1_OPUS_REFIRE.md section 4, verbatim banked)

"CALIBRATION IS CERTIFIED FROM THE WRONG REGION. T1 verifies answers
below min_confidence, but low-confidence stops go ungated, so evidence is
sampled almost entirely ABOVE the threshold: survivorship bias in cell
rates and ECE."

## What was read before drafting

BASELINE_SPEC.md full body (4.3 T1/T4 ladder, 3.4 cascade attribution,
4.1-4.2, section 5 grammar), AMENDMENT 5 (cold start: m is the single
boundary, n < m is measurement territory, low confidence there does not
climb), AMENDMENT 6 (per-class counters), AMENDMENT 7 (n_eff Wilson
denominator), the fresh IMP3 AMENDMENT 10 (model fingerprint; its header
reserves 8/9 for D1/D2 and states the in-amendment-delta practice for
section 5), JUDGED.md lines 36-41 (T1 fires only on verified, kept).

## Amendment 9 in one line each

- Kill mechanism, named: gatedness rises with confidence (final answers
  are the confident ones; stops hand work up-tier ungated), so the ECE
  window fills from [0.8, 1] while T1 acts on [0, 0.8). Low-confidence
  stops remove exactly the events T1 needs; the label certified the
  region the trigger never reads.
- Clause 1: window = last m gated answers, NO exclusions by stop status,
  confidence, cascade position, or tier; pair = (receipt.confidence,
  verdict bit) joined on receipt_ref; 10 equal-width bins; no verdict
  schema change.
- Clause 2: on cells seeking verified (n >= m), every low-confidence stop
  MUST be gated at the cheapest canonical gate before the climb executes
  (3.4 MAY -> scoped obligation); outcome feeds FUTURE windows, not the
  current climb; 3.4 cold-start and ungated-stop protections unchanged;
  spend is M1 gate cost, never probe budget.
- Clause 3: verified needs n_low >= k_low (DEFAULT 10) window pairs below
  min_confidence; alternative path = inverse-stop-probability weighting
  with DESIGN weights only (seeded sample at p_stop DEFAULT 0.25, flag
  sampled_stop_gate, weight 1/p_stop, k_low floor on weighted mass,
  single-pair dominance cap); modeled missing-at-random IPW REFUSED
  (stop decision is deterministic in the calibrated variable, weights
  degenerate 0/infinity).
- Clause 4 (high stop-rate): rolling stop-rate s from the receipt spine,
  carried on receipts as stop_rate; s > s_max (DEFAULT 0.5) forces
  calibration_state = unverified, T1 disarms (trigger none), fail closed
  in both directions (ungated: censoring is the majority; gated: T1's
  climb would be standing policy the pass-rate must license, T2
  precedent); operator-visible anomaly, no auto-remediation.
- Clause 5: label map (verified/poor/unverified conjuncts, supersedes
  only Amendment 5's ECE sentence), M6 reports per-region ECE + n_low,
  grammar delta stated in-amendment per IMP3 precedent (stop_rate,
  sampled_stop_gate).
- Five test predicates: censorship injection, region separation (the
  kill demonstrated: identical survivors, different low regions must
  split labels), design-weight equivalence + recycle audit, high
  stop-rate fail-closed, grammar presence.

## Decisions with rationale

- Gate-the-stop as primary, IPW as sampled-design fallback, per mission's
  "(or explicitly weight by inverse stop-probability)". Modeled MAR IPW
  refused with the deterministic-selection argument; sampling weights are
  exact by construction, no assumption to launder.
- Scope held to calibration per mission. The kill's cell-rates half is
  named as Residual B, not silently fixed: cold-start and never-armed
  cells keep survivor pass-rates BY DESIGN (3.4 poison-protection is
  load-bearing); flagged to the kill 1 lane and the harness.
- Grammar delta in-amendment, not in-place: IMP3/AMENDMENT 10 already
  amended section 5 by description for the same collision reason; two
  lanes editing the JSON block in place would fork it.

## Verification

- Em-dash count over the whole spec after the edit: 0 (U+2014 and
  U+2013 both 0), the file's own law holds; batch footer states it.
- Amendment numbering cross-checked live: IMP3 header reserves 8 (D1) and
  9 (D2); Amendment 8 not present yet, sibling-owned, untouched.
- Shared-surface validate run after the write: exit 0, ok: false (its
  steady-state advisory posture). This lane's footprint in the drift list:
  hash mismatch on gps_baseline_ractor_20260929/BASELINE_SPEC.md and the
  new unindexed receipt. Same footprint every amendment lane leaves
  (AD4/AH11/IMP3 preceded me; BASELINE_SPEC's index row itself reads
  "hash refresh: race-heal pass 2 (patrol 20260930)"); the patrol owns
  the heal, no manual INDEX surgery from this seat. Pre-existing drift
  from other lanes (STEALTH_SWEEP_LATEST, PACK_OFFLOAD, Q_OPERATION_RACTOR
  receipt, unindexed W/Y files) untouched and not mine to heal.

## Defaults introduced (all DESIGN DEFAULT, tunable)

k_low = 10, p_stop = 0.25, s_max = 0.5, ECE bins = 10 equal-width.
