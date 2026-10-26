# Promoted invariants

generated: 2026-10-25T18:59:06.989043Z
policy: promotion.v2 (639ba9d453ed97c0)
surface: 17 of 2335 registry rows promoted

A promoted row met the repeat gate (count >= 2 and recurrence across UTC
cycles or sources), is not probe chatter, and is not instrumentation
vocabulary. Admission is untouched: every row still exists in
`memory/percolator/invariants.json`; this is the readable subset.

Kill conditions: 6 checkable, 11 manual debts, 0 missing.
Run `python tools/falsifier_lint.py` for PASS/FAIL/UNMEASURED on each.

| count | domain | invariant | falsifier |
| ---: | --- | --- | --- |
| 29 | behavioral | [improve] smoke test claim | manual/2026-11-20 |
| 29 | behavioral | [steer] Verify with git diff / actual file bytes before declaring done. Trust bytes, not reports. | log_zero/7d |
| 19 | behavioral | [steer] Elevate with a deliberate ask: frozen prefix (cache-shared) + tight ask (~207 chars) + output contract (<=N words, shape | manual/2026-11-20 |
| 16 | behavioral | [steer] Verify via OUR systems before declaring done (get_errors + read the actual file bytes on disk). Trust bytes, not reports | log_zero/7d |
| 16 | behavioral | [steer] Escalate to the next smarter tier; stop local token bleed (escalate_on_loop). | nudge_budget |
| 16 | behavioral | [steer] Escalate to next tier; stop token bleed. | nudge_budget |
| 8 | behavioral | [steer] Training rows are accumulating. The pipeline is built but W0. 3 is blocked. Surface the gate status before starting new w | file_absent |
| 6 | behavioral | [steer] STOP asking permission / defaulting to operator for clear asks; route decisions not questions. | manual/2026-11-20 |
| 4 | org_v2_external_steal | Every long-lived switch or organ registers an owner and a purpose, is audited on a schedule, and its removal routes to the owner. | manual/2026-11-20 |
| 4 | org_v2_external_steal | Accepted decision records are immutable; reversals are written as new records linked by a superseded-by reference. | manual/2026-11-20 |
| 4 | org_v2_external_steal | Artifacts crossing a trust boundary carry a content hash and an attestation, and verification runs against the attestation rather than against a claim. | manual/2026-11-20 |
| 3 | org_v2_external_steal | Alerts fire on consumer-visible symptoms with deduplication and inhibition, and escalate by budget burn rate rather than per cause. | manual/2026-11-20 |
| 3 | org_v2_external_steal | Prose claims are tested like code: a frozen pattern per claim is checked against bytes in CI, and drift fails the build. | field_complete/verifier |
| 3 | org_v2_external_steal | Every state transition produces an immutable generation closure with an atomic switch and a one-step rollback to the previous closure. | manual/2026-11-20 |
| 2 | org_v2_external_steal | Rollback covers only managed state, and mutable live state is named as outside the guarantee. | manual/2026-11-20 |
| 2 | org_v2_external_steal | Deleting a mechanism requires a reachability check from named entry points. | manual/2026-11-20 |
| 2 | org_v2_external_steal | Competing candidates for canonical status resolve by a deterministic weighted rule, and stale-term claims are ignored. | manual/2026-11-20 |
