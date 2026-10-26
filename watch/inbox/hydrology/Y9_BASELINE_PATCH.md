# Y9 - BASELINE PATCH: N2's three kills folded into the spec

- Lane: batch 2, lane 9/12. Date: 2026-09-29. No commit (per mission).
- File owned: watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md.
  Change: appended the AMENDMENTS section after the section 10 close;
  the v1 body above it is byte-unchanged (append-only respected).
- Kill source: N2 hostile-implementer digest in
  watch/inbox/hydrology/X5_NIGHT_READ.md (row of
  watch/inbox/mates_leave_protocol/NIGHT_BURN_output_20260930.jsonl,
  $0.0188, 15.2s; X5's verdict: N2 earned the night).

## What landed (BASELINE_SPEC.md AMENDMENTS 1 through 4)

- AMENDMENT 1, kill 1 (T1 dead-code window n 20..49): calibration
  window is now m_eff = min(m, n) floored at n_min; T1 is reachable
  from n = n_min, so its reachability boundary equals the routing
  qualification boundary; n < n_min stays unverified and routes low
  confidence to T4; the shorter window's ECE variance is assigned to
  harness M6 with e_max = 0.10 kept a tunable DESIGN DEFAULT.
- AMENDMENT 2, kill 2 (no chain-concurrency story): single writer,
  WAL + BEGIN IMMEDIATE, tip check inside the transaction; on chain
  contention the writer waits busy_timeout (5000 ms default) and
  re-bases onto the new tip (contention delays, never forks); fork
  test predicate named (planted fork quarantines the losing branch's
  cells; N concurrent submissions must yield one linear chain);
  production resolution is longest-valid-chain-wins with quarantine
  never delete, capability rebuilt by replay, and K5 owning forging
  paths.
- AMENDMENT 3, kill 3 (unenforceable recusal): principal DDL gains
  operator_id TEXT NOT NULL (stable across rotation; family =
  rotated_from closure under one operator_id); enforced insert-time by
  the single writer (cell operators resolved from the receipt spine
  plus registry owner_principal; same-family G1/G2/G3 verdict
  rejected) and audit-time by chain replay (violation quarantines the
  cell); G0 exempt per 3.2; K5 adds the same-operator rejection test.
- AMENDMENT 4: N2's five missing test predicates written as first-wave
  build assertions: chain fork detection; G3 cap transition (atomic,
  no qualifying intermediate); decay monotonicity vs probe injection;
  idempotency under replay (UNIQUE keys, byte-identical aggregates,
  replay rebuild equality); T2 advisory differential (advisory branch
  byte-identical to T2-compiled-out; measured branch climbs).

## Verification

- Em-dash grep on the amended BASELINE_SPEC.md: 0 (law kept; the spec's
  closing "Em-dash count: 0" claim stays true, and the amendments
  self-report the same).
- Spec-only patch, no code touched: satisfies the build-discipline law
  (spec before behavior change; tools/gps_mcp v0 superseded by this
  spec is untouched until the harness licenses a build).
- Amendment-wins-over-body rule stated in the AMENDMENTS preamble,
  mirroring the JUDGED.md fix pattern.
