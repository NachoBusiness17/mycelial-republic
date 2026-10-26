# B2-226 Aging-guard board test

## Verdict

LANDED. Three new pins in tests/test_drift_dashboard.py push a synthetic W40 FRAGILE-ALIGNED v2 stamp row through history_cell, drifting_days and _verdict_color, pinning every clause of docs/DRIFT_BOARD_SPEC.md section 3: it renders as "2026-W40=FRAGILE-ALIGNED*" in the history cell, it colors amber-green #b9e77a (never the #ddd fallback, never the VACUOUS/INSUFFICIENT gray), it breaks a trailing DRIFTING streak (drifting_days returns (0, "")), and it never extends one (a fragile week between DRIFTING weeks starts the streak at the later DRIFTING stamp only). Suite: 25 passed (22 prior + 3 new) across tests/test_drift_dashboard.py + tests/test_drift_pairs_stamp.py. The B2-218 vocabulary-sweep falsifier is now decidable for the board: any sweep that drops or renames the FRAGILE-ALIGNED vocabulary turns these pins red.

## Evidence file:line quotes

- docs/DRIFT_BOARD_SPEC.md:48-51: "FRAGILE-ALIGNED (tools/drift_pairs_stamp.py _apply_aging_guard, landed 2026-09-26 after this spec's first filing) renders as ALIGNED's provisional form: amber-green, never the unknown-gray fallback, and it counts as ALIGNED for DRIFTING-day streak semantics (it breaks a DRIFTING streak, it never extends one)."
- tools/drift_pairs_stamp.py:408-425 _apply_aging_guard: "Only ALIGNED downgrades: DRIFTING / INVERTED / VACUOUS / DEGENERATE / INSUFFICIENT mean what they mean at any referent age." (REFERENT_MATURE_DAYS = 7 at :137)
- tools/drift_dashboard.py:197-204 _verdict_color: `"ALIGNED": "#6ee7a0", "FRAGILE-ALIGNED": "#b9e77a"` with the comment "styled amber-green, never default-gray".
- tools/drift_dashboard.py:136-156 drifting_days: returns (0, "") unless "v2[-1].get('verdict', {}).get('verdict') == 'DRIFTING'".
- tools/drift_dashboard.py:112-127 history_cell: renders f"{wk}={vd}{mark}" with "*" on the last week.

## Work done

1. Read the spec clause and the three consumers (history_cell, drifting_days, _verdict_color) plus the producer _apply_aging_guard; confirmed the gap: tests/test_drift_pairs_stamp.py pinned the downgrade itself but NO test fed a FRAGILE-ALIGNED row into the board functions (grep over tests/test_drift_dashboard.py: zero FRAGILE-ALIGNED mentions before this lane).
2. Appended three tests to tests/test_drift_dashboard.py in the file's existing fixture style (_v2 helper rows, synthetic W40 of 2026, stamped 2026-09-28):
   - test_fragile_aligned_history_cell_and_amber_green_color (render + color clauses)
   - test_fragile_aligned_breaks_a_drifting_streak (W38+W39 DRIFTING, W40 FRAGILE-ALIGNED -> (0, ""))
   - test_fragile_aligned_never_extends_a_streak (W39 FRAGILE-ALIGNED between DRIFTING weeks -> streak starts at W40 only, (1, "2026-09-28"))
3. Ran the two touched suites: 25 passed, 0 failed, 0 em-dashes in added test bytes.
4. No production code touched: the pins passed against the landed implementation on first run, which is itself evidence the spec clause and the code agree.

## Falsifier

The brief's falsifier target is the B2-218 vocabulary sweep decidability: with these pins, any future sweep that removes, renames, or re-grays the FRAGILE-ALIGNED vocabulary in tools/drift_dashboard.py or drift_pairs_stamp.py fails the suite (red run names the exact clause). Inversion check ran live pre-commit of the pins: _verdict_color("FRAGILE-ALIGNED") returns "#b9e77a" on current bytes and drifting_days breaks the streak as asserted; if a future edit makes any of the three asserts false, the falsifier has caught the regression.

## Bibliography closed

- docs/DRIFT_BOARD_SPEC.md section 3 (clause source, read at lines 40-60)
- tools/drift_pairs_stamp.py (_apply_aging_guard, REFERENT_MATURE_DAYS)
- tools/drift_dashboard.py (history_cell :112, drifting_days :136, _verdict_color :197)
- tests/test_drift_dashboard.py (3 pins appended), tests/test_drift_pairs_stamp.py (suite run for context)
- Nothing owed.
