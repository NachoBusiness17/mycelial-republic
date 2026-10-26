# FIELD2 SEAT LIST (the blind decision control, frozen BEFORE the arms ran)

**Schema:** field_experiment.seat_list.v1 · **ts:** 2026-10-01 · **lane:** FIELD-2
**Frozen:** written from `tools/field_experiment.py --setup-only` output BEFORE
either arm ran (the OVERMIND_THEORY sec 6 duel control: the seat writes, blind
and before the hour, its own decision list for the same starting state).

**Rule (pre-registered, deterministic, capability bytes only):** per task_shape,
the highest pass_rate with sample_size >= 3 (fallback: >= 1); ties break to the
larger sample, then alphabetical model_id. No knowledge of either arm's
behavior, no knowledge of the field arm's terrain relaxation, no sim output.

| shape | seat pick | pass_rate | sample_size |
|---|---|---|---|
| adversarial-review | x-ai/grok-4.7 | 1.0000 | 9 |
| askbank-v1-safeguard | z-ai/glm-5.3-prime | 1.0000 | 3 |
| code-analysis | qwen/qwen3.8-max-prime | 0.5000 | 4 |
| grading | z-ai/glm-5.3-prime | 0.7500 | 4 |
| legality-water-graph-v1 | legality-propagator-v1 | 1.0000 | 100 |
| night-judgment | z-ai/glm-5.3-prime | 0.8333 | 6 |
| planning | z-ai/glm-5.3-prime | 0.6667 | 9 |
| schema-design | z-ai/glm-5.3-prime | 0.7500 | 8 |
| world-tick | mountain-world-v0 | 1.0000 | 4 |

Board spec frozen alongside at `watch/inbox/model_garden/FIELD2_BOARD_SPEC.json`
(9 model rows x 9 shape columns; elevations = cost terrain from pass_rate,
per-cell cross_section = sample_size; see the deviations block in
`tools/field_experiment.py` docstring).
