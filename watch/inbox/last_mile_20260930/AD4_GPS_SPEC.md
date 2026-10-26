# AD4 GPS spec fix receipt (2026-09-30)

Mission: close the two N2 kills from NIGHT_BURN_RECEIPT.md in the GPS spec.
Spec doc: watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md (the
estate baseline; SEAT_A_SPEC.md is the frozen seat-A draft, untouched). No
commit, per mission.

## Prior state found

Batch 2 amendments (Y9 lane, from the hydrology digest of the same burn)
had already landed: AMENDMENT 1 answered kill 1 by allowing
calibration_state = verified from n = n_min over m_eff = min(m, n); kill 2
got only the AMENDMENT 4 predicate-2 test, no schema fix.

## What landed (batch AD4, append-only on BASELINE_SPEC.md)

- AMENDMENT 5 (kill 1), SUPERSEDES AMENDMENT 1: routing is gated on
  n >= m (calibration window full, DEFAULT 50). n_min retired; m is the
  single boundary for qualification, 4.2 exploration, and T3. Cold start
  (n < m) defined explicitly: exploration + none-qualify fallback +
  forced probes only, receipts carry calibration_state: unverified, low
  confidence never climbs (trigger none). Chosen over arming T1 at n_min
  because fail-closed doctrine forbids acting on unverified confidence:
  T1's own preamble ("noise wearing a uniform"), the judge's kept rule
  that T1 fires only when verified (JUDGED.md 40-41), the T2 advisory
  precedent, and section 0's earned-authority pattern. Named cost:
  graduation 20 to 50; F3 fast-graduation defense superseded; F-S1 fence
  survives.
- AMENDMENT 6 (kill 2): gate_class_mix blob dropped; eight raw per-class
  counters added to the section 2 capability DDL in place (comment-marked,
  the one marked exception to body-unchanged). Atomic update rule: one
  AMENDMENT 2 transaction increments one counter pair, then recomputes
  blended columns by closed form over all counters (running mean
  superseded). First-non-G3 recomputation needs no special case; G3 cap
  becomes 4.1 rule 4, n_non_g3 >= 1, a column predicate, so qualification
  flips exactly at commit (AMENDMENT 4 predicate 2 now implementable).

## Verification (bytes, not reports)

- Revised capability DDL extracted from the spec and executed in
  sqlite3 :memory:: parses; columns g0_passes..g3_fails present;
  gate_class_mix absent.
- Em-dash and en-dash census over the whole doc after edits: 0 and 0.
- pytest tools/gps_mcp/test_gps_mcp.py -q: 28 passed (no code touched;
  ledger.py v0 stays superseded by the spec, no migration, gps_ledger.db3
  is fixture data).
