# B2-80 lifecycle row reason carry (2026-09-26)

## Verdict

LANDED. mag_loop_gap.v1 rows sourced from the lifecycle now carry the _policy_should verdict (`should`), the policy reason string (`should_reason`) and the probe inputs (`signals`: queue_depth, fleet_running, operator_active, drainer_allowed, browser_enabled), so a gap-vs-waste flip is auditable from the row alone. The row-shape spec landed in the module docstring before the code change; the carry rides a new optional `lifecycle` kwarg on track_loop_gap fed by a _lifecycle_carry helper in track_lifecycle_into_improve; non-lifecycle rows stay variable-field per the existing improve_candidate/pointer precedent. Targeted suite 8 passed (6 prior + 2 new pins), lifecycle suite 7 passed, ratchet check --changed NEW=0 PASS, and a live-system probe landed real carried rows with the production log byte-still. Checkbox note: B2-80 sat [x] from birth with no receipt (the B2-238 disease); this landing earns it.

## Evidence

- Defect on bytes at fix time: memory/training/loop_gaps.jsonl held 313 rows (grown from the B2-20 census of 304), drainer lifecycle_gap 18 vs lifecycle_waste 88 (17/87 at B2-20), and zero rows carried should/should_reason/signals; every row showed only the 9-key base shape (schema, ts, ts_unix, name, detail, where, kind, dedupe, stack).
- Flip pattern live: same-piece gap/waste pairs inside one hour exist (2026-08-09T10:57 vs 11:16, 18.8 min apart; 2026-09-02, 56.7 min; 2026-09-26 12:11 vs 13:08, 57.0 min), and each row's only verdict context was the constant detail string, so the flips were unauditable after the fact, exactly the B2-20 finding.
- Policy source: mag/lifecycle.py:445 _policy_should returns (should, reason) from queue_depth/fleet_running/operator_active/drainer_allowed/browser_enabled, and build_lifecycle (:527) already returned pieces[].reason plus top-level signals; the caller track_lifecycle_into_improve consumed only the gaps/waste id lists and dropped both.

## Work done

1. Re-read QUEUE.md per the shared-file claim law, appended 3 CLAIM lines (mag/temperature_stack.py, tests/test_temperature_stack.py, the board itself) at 16:37:11Z; no foreign claim existed on the target files; rebased on current bytes including the B2-79 landing already in the working tree.
2. Spec first: the mag_loop_gap.v1 row-shape law (base fields always; lifecycle rows add should/should_reason/signals; non-lifecycle rows variable-field) written into the mag/temperature_stack.py module docstring and the track_loop_gap docstring before any behavior change.
3. Code: track_loop_gap (mag/temperature_stack.py:390) gained `lifecycle: dict | None`; when truthy the row gains should (bounded 8), should_reason (bounded 400) and signals (dict copy), with the fix comment naming cause and evidence (B2-20 census 17 vs 87 and 4 sub-hour flips; 18 vs 88 on 313 rows at fix time, zero rows carrying the keys pre-fix). track_lifecycle_into_improve (:528) feeds each gap and waste row through _lifecycle_carry (:511) pulling the piece's should/reason plus the build_lifecycle signals. B2-79's _gaps_log seam untouched; the em-dash-bearing detail strings kept byte-identical.
4. Tests: two pins appended to tests/test_temperature_stack.py, one direct carry plus a negative (plain rows gain no carry keys) and one end-to-end through a fake build_lifecycle asserting both rows carry the real verdict strings and all five signals; training_events.emit, improve.append_candidates and file_pointer_knot are patched so the tests create no new B2-86-class pollution; MAG_GAPS_LOG and STATE_PATH point into tmp_path.
5. Live probe: track_lifecycle_into_improve() against the real system with the log redirected to a tmp file returned n=2 and landed lifecycle_gap:lab ("Heartbeat + live board; idle loop is cheap local") and lifecycle_gap:scribe ("supervisor wants scribe (cheap local)"), each row carrying all five probe inputs; production loop_gaps.jsonl sha256 and size unchanged across the run.

## Falsifier

The fix dies if a lifecycle-sourced row lands without the three keys: any future mag_loop_gap.v1 row named lifecycle_gap:* or lifecycle_waste:* missing should/should_reason/signals refutes it. The audit value dies if the carried reason is not the _policy_should string: compare a fresh row against GET /api/v1/lifecycle pieces[].reason for the same minute. The no-pollution claim dies if memory/training/loop_gaps.jsonl changes size during tests/test_temperature_stack.py (both new tests pin it byte-still). Re-derive the defect counts by parsing the jsonl and counting names; every pre-fix row shows the 9-key base shape only.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_20_loop_gaps_20260926.md ; memory/training/loop_gaps.jsonl (313 rows at fix time) ; mag/temperature_stack.py:10 (row-shape spec), :390 (track_loop_gap), :434 (fix comment), :511 (_lifecycle_carry), :528 (track_lifecycle_into_improve) ; mag/lifecycle.py:445-524 (_policy_should), :527-670 (build_lifecycle) ; tests/test_temperature_stack.py (2 new pins + side-sink isolation) ; configs/temperature_stacks.yaml:119 (gap_tracking, dedupe_hours 12) ; watch/inbox/burn_wave_20260926/QUEUE.md (claims, landing, self-feeds B2-337/B2-338) ; memory/burns/LEDGER.jsonl.
