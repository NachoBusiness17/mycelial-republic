# AH7 — env contract WIRED to the legality family (AD3 refire)

**Date:** 2026-09-30 · **Seat:** ZCode subagent (AH7) · **Owns:** `tools/env_contract.py` (extended: `run_legality` + `run-legality` CLI), `tests/test_env_contract.py` (+2 wiring tests), this receipt · **No commit** (per mission).

**Mission:** AD3 landed the env-contract format; this window wired it to the legality family end-to-end: manifest emitted → 100 real verdict rows through the propagator → fed into the REAL gps ledger → verified + drift-proven.

## What landed

`run_legality(cases, seed, manifest, reward, ledger, model_id)` in `tools/env_contract.py` — the AH7 spec that was already in the module docstring, now implemented to the letter:

1. **No feed under drift:** `validate_manifest` runs fail-closed BEFORE any case is judged; `MANIFEST_MISMATCH` refuses when the manifest's env_id/task_shape is not `legality-water-graph-mountain-v1` / `legality-water-graph-v1` (rows that lie about their family are worse than no rows). A refusal produces no `reward.json` rows and never opens the ledger.
2. **Judged subject = the propagator:** each seeded case (`make_graph_spec` + `sample_action`, used read-only) is judged by `label_sample` (the REAL WaterGraph) and by `propagate` (constraints only); row verdict = AGREEMENT (full verdict-dict equality); `label` = the engine's exact 5-way ground truth. `BAD_LABEL` refuses if the engine's label ever leaves the manifest `label_set`.
3. **Evidence walk:** `evidence_hash` = sha256 over canonical JSON of `{case_id, graph, verb, target, engine, oracle}` — the row's full judged material is rebuildable from the seed and both verdicts reproduce under it.
4. **Regenerated reward.json** (truncated per run, appended by `emit_reward`): same seed + same engine/verifier bytes → byte-identical rows (pinned by the new determinism test). Ledger feed is append-only through `feed_reward_file`'s two-pass law under explicit `model_id=legality-propagator-v1` (never guessed).

CLI: `python tools/env_contract.py run-legality [--cases N] [--seed S] [--manifest …] [--reward …] [--ledger …] [--model-id …] [--no-feed]`.

## Artifacts (live homes)

| artifact | path |
|---|---|
| family manifest | `tools/gps_mcp/env_manifest.v1.json` |
| reward rows (this run) | `logs/legality_env/reward.json` (100 rows, sha256 `cacc64ab8ff3..`) |
| real ledger fed | `tools/gps_mcp/gps_ledger.db3` |

Manifest pins (byte truth, `cat` of the emitted file): engine `mag/water_graph.py` sha256 `ae650fb409bfe4db167811f44de658996e833b9d0678750a8e0b776dac71e1e0` (version `63f82eb12`, git describe), verifier `tools/legality_propagator.py` sha256 `deb9d00cf553df61c23ae33a701e1f5212a544a42d8c387c298ee8df56b80e56`, task_shape `legality-water-graph-v1`, label_set = the exact 5-way vocabulary, timeout_sec 0, determinism seeded.

## Evidence

- `emit --out tools/gps_mcp/env_manifest.v1.json` → written, canonical bytes.
- `run-legality --cases 100 --seed 17` → exit 0. **Agreement 100/100 (100.00%)**; label coverage `{illegal_dry_pool: 28, illegal_unknown_target: 23, illegal_unknown_verb: 7, legal_gain: 3, legal_no_gain: 39}` — all 5 labels represented. 100 rows emitted, 100 fed.
- **sqlite verify (the REAL ledger):** `verdict_log` → **100 rows** for `model_id='legality-propagator-v1' AND task_shape='legality-water-graph-v1'` (ts 2026-09-30T12:27:45Z), verdict split `{1: 100}`; `capability` → `(legality-propagator-v1, legality-water-graph-v1, pass_rate 1.0, sample_size 100)`.
- **validate:** `OK env legality-water-graph-mountain-v1 … matches pin` — exit 0.
- **DRIFT TEST (verdict: REFUSED, fail-closed works):** copied `mag/water_graph.py` to a temp path, XOR-flipped ONE byte at the midpoint of the COPY (real engine never touched — its sha still `ae650fb409bfe4db..`, matching the pin), pointed a manifest copy's `engine_path` at the drifted copy → `REFUSED ENGINE_DRIFT: … manifest pins ae650fb409bf.. live bytes are fafe9b55ef33..` — exit 1. Temp fixture deleted after the check.
- Tests: `pytest -q tests/test_env_contract.py tests/test_gwap_to_gps.py tests/test_legality_dataset.py tests/test_propagator.py` → **48 passed**; `pytest -q tools/gps_mcp/test_gps_mcp.py` → **28 passed** (2026-09-30 run). The 2 new wiring tests pin: happy path (5 cases, feed into tmp ledger, byte-identical reward regeneration, capability row k/n), and drift+mismatch refusals leaving NO reward file and NO ledger file at all.

## Findings while wiring

- The prior AH7 refire had already landed the WIRING spec docstring + `DEFAULT_*` constants but zero implementation (working-tree `M tools/env_contract.py`); this window implemented exactly that spec — no semantic drift from the docstring.
- `label_sample` + `sample_action` import chain pulls `mag.water_graph` and `server.protocol`; imports are lazy inside `run_legality` so the contract module stays import-cheap for manifest-only consumers.
- Rerun semantics (per spec): same seed rerun appends another N samples of the same measurement to the append-only `verdict_log` (sample_size grows); `reward.json` is per-run, not cumulative.

## Next-attempt design (if re-run needed)

Nothing failed. Natural extensions: a `--collect`-style patrol re-validating every emitted manifest against live bytes on the census-patrol schedule; multi-model rollouts via `case_to_model`; and a scheduled `run-legality` heartbeat so the capability row's sample_size compounds.
