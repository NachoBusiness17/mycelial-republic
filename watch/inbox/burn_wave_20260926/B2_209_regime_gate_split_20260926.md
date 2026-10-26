# B2-209 receipt: regime gate display split (2026-09-26, lane SW-03)

## Verdict

LANDED. Contamination was live before the fix: v5 read gates_passed 5 with 3 of them era milestones (regime_violation_ratchet, regime_fanout_width_law, regime_drift_registry_t1_t6). The fix aligns the code with the owning spec (docs/ref/releases/VERSION_REGISTRY.md already ruled regime milestones "not a graduation gate and never flips a version to shipped"; the code was the orphan, so no spec change was needed for the rule itself): _gates_passed_for excludes the regime_ prefix, a new _regime_passed_for mirrors it, and status_summary reports regime_passed + regime_ids beside gates_passed. Live after: v5 gates_passed 2, regime_passed 3 with ids. 3 new tests; release registry suite 6 passed, subprocess map 2 passed.

## Evidence file:line quotes

- mag/release_registry.py:116-124 (pre-fix _gates_passed_for): "for row in read_gate_log(limit=200, version=version_id): if row.get("ok") and row.get("gate_id"): gid = str(row["gate_id"]); if gid not in out: out.append(gid)" (unfiltered; regime rows counted).
- mag/release_registry.py:58-73 (pre-fix status_summary): "gates_passed": len(passed) with no regime separation.
- Live bytes before fix (this lane): read_gate_log(limit=200) = 19 rows, 3 regime_ rows all ok:true, versions v2/v3/v4/v5; v5 passed list carried all 3 regime ids (5 total).
- watch/inbox/burn_wave_20260926/B2_65_registry_revival_20260926.md:5 (the disclosure that pre-registered this fix): "Disclosed: release status counts regime rows into v5 gates_passed (mag/release_registry.py:116-124 reads the log unfiltered); self-feeds filed to split display and arm the tripwire."
- watch/inbox/burn_wave_20260926/B2_65_registry_revival_20260926.md:24 (the falsifier this fix closes): "If v5 ever flips shipped on regime rows alone (gates_passed math), the regime_ prefix must be excluded from _gates_passed_for (mag/release_registry.py:116-124)."
- docs/ref/releases/VERSION_REGISTRY.md:107 (owning spec, pre-existing): "It is not a graduation gate and never flips a version to shipped."

## Work done

- mag/release_registry.py: REGIME_PREFIX constant; _gates_passed_for skips regime_ rows (fix-comment carries the receipt: B2-209 aligning code to VERSION_REGISTRY.md); _regime_passed_for added (regime-only mirror, failed rows never counted); status_summary emits regime_passed/regime_ids per version beside gates_passed.
- docs/ref/releases/VERSION_REGISTRY.md:107: one-sentence display-split amendment documenting the new fields (spec-first for the display surface).
- tests/test_release_registry.py: +3 tests (regime rows excluded from gates_passed incl. a failed regime row and dup dedupe; _regime_passed_for counts only ok regime rows; status_summary reports both fields on v5). 6 passed; test_release_subprocess_map.py 2 passed.
- Live verification post-fix: v5 gates_passed 2, regime_passed 3 with the three ids.

## Falsifier

The B2-65 falsifier, closed and pinned: a version flipping shipped on regime rows alone is now impossible through gates_passed math (excluded at the source) and any regime row still leaking into gates_passed turns test_regime_rows_excluded_from_gates_passed red. Kill conditions going forward: (a) a gates_passed count on any version that includes a regime_ id (test red), (b) a failed regime row counted into regime_passed (test red), (c) a consumer of status_summary that re-conflates the fields by summing them into a shipped decision (none exists today; the fence is the separate field names).

## Bibliography closed

- mag/release_registry.py (status_summary, _gates_passed_for, read_gate_log, record_gate)
- watch/inbox/burn_wave_20260926/B2_65_registry_revival_20260926.md (read in full: disclosure, falsifier, backfilled regime rows)
- docs/ref/releases/VERSION_REGISTRY.md (Regime milestones section, read and amended)
- memory/improve/releases/gates.jsonl (live log, 19 rows, read via read_gate_log)
- tests/test_release_registry.py (conventions read, extended), tests/test_release_subprocess_map.py (regression run)
