# Y10 — the constraint propagator (legality oracle, no engine)

Lane: Mickey17 W3K batch 2, lane 10/12. Date: 2026-09-29.
Files: `tools/legality_propagator.py` (new) + `tests/test_propagator.py` (new). No commit.

## What landed

N4's first actionable step (the LDT experiment design, `logs/mates/night_burn_20260930.jsonl` row "N4-ldt-experiment": "Propagator + labeler + unit tests"): the deterministic oracle that labels water-graph legality WITHOUT running the engine. `tools/legality_dataset.py` labels by running the real engine (`WaterGraph.tick`); the propagator labels the same `(state, action)` pairs by propagating named constraints over the raw spec dict:

- `unknown_verb` — verb not in the live protocol table (`server.protocol.VERBS`).
- `unknown_target` — valve resolves against pipes, every other verb against nodes.
- `dry_pool` — boil/tag on a node with volume 0.
- `crown_gain` — one tick of physics propagated to the COLD node in three phases: (a) ACTION (boil lifts 1 to steam; valve toggles the gate; join/tag touch nothing), (b) STEAM (steam ignores pipes, condenses at the highest cold node, first-max tie rule), (c) FLOW (downhill check valves, cap limits, siphon prime-at-crest / primed-runs-headless / break-on-dry, xor passes exactly one delivering inlet, sill passes on delivering-inlet COUNT >= sill, under-gate inflow held pooled, gated outflow waits for its gate, waste swallows).

Key finding while deriving it: "a steam path exists to the COLD node" alone is NOT the engine's verdict — the crown drains through its own open out-pipes in the same tick (condense runs before flow), so the net delta after ALL constraints propagate is the answer. Also: the only mechanism that can climb to the strict-max-elevation crown is an already-PRIMED siphon (priming itself needs head, so in the W3K generator — which never pre-primes — pipes can never feed the crown; steam is the only route).

## The agreement law — measured

Propagator verdict == engine verdict, full dict equality (legal, illegal_reason, crown_gain, label), engine side = `label_sample` (real `WaterGraph.tick`):

| sweep | agreement | labels seen |
|---|---|---|
| tests (seed 1010, n=100) | **100/100 (100.00%)** | dry_pool 25, unknown_target 31, unknown_verb 10, legal_gain 4, legal_no_gain 30 |
| CLI seed 17, n=5000 | 5000/5000 (100.00%) | dry_pool 1377, unknown_target 1212, unknown_verb 473, legal_gain 213, legal_no_gain 1725 |
| CLI seed 99, n=1000 | 1000/1000 (100.00%) | all five |
| CLI seed 4242, n=1000 | 1000/1000 (100.00%) | all five |

Zero disagreements in 7,100 cases. CLI: `.venv\Scripts\python.exe tools\legality_propagator.py --n <N> --seed <S>` (exit 1 on any disagreement).

## Tests

`tests/test_propagator.py` — 12 passed:
- `test_agreement_law_100_sampled_cases` — THE law, 100 seeded W3K cases.
- `test_agreement_covers_every_label` — all five labels exercised in the 100.
- `test_propagator_is_engine_free` — source contains no engine import (independence: else the agreement test would be the engine agreeing with itself).
- `test_propagate_is_pure` — same verdict twice, caller's spec never mutated.
- 7 hand-checked constraint units: each reject reason; steam path gain; gain negated by crown drain (phase-order law); valve-armed primed-siphon climb; pre-wired gain under a social verb; quiet no_gain. Each cross-checked against the engine.

## Gates

- `pytest tests/test_propagator.py -q`: 12 passed.
- `pytest -q` (full, 2026-09-29, executed outcome sum): 2 failed, 3002 passed, 12 skipped, 3 errors in 1709.24s. Both failures + the erroring surfaces are other lanes' files, byte-named: `tests/test_census_drift_patrol.py` (patrol subspawn misreading) and `tests/test_headless_law.py` (bare-spawn debt grew 22 -> 34; its 24-file offender list names neither of this lane's files — the propagator spawns nothing). `memory/working/test_planner_agent_integration.py` fails 3 on its own, pre-dating this lane (stale lastfailed cache). This lane's files: 0 failures. `pytest --collect-only -q` read 3024 collected moments later (denominator law: counts taken at different moments are not comparable — other lanes land concurrently).
- `tools/violation_ratchet.py check --changed`: PASS, hits=0, NEW=0 (no new debt).

