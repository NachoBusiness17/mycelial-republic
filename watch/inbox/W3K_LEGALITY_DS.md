# W3K — water-graph legality dataset (LDT corpus, $0, local, deterministic)

**Lane:** Mickey17 W3 · **Date:** 2026-09-29 · **Owner files:** `tools/legality_dataset.py` (new), `tests/test_legality_dataset.py` (new). No commit made (lane rule). Engine untouched.

## What landed

The N4 LDT experiment design (`logs/mates/night_burn_20260930.jsonl`, row `N4-ldt-experiment`) needs a legality corpus shaped `(state vector + action -> label)` as a flat token sequence. `tools/legality_dataset.py` builds it over the **real engine** (`mag/water_graph.py`), Mountain-family boards (`server/world.py build_mountain_graph` law kept: `crown` is the unique COLD node at strict max elevation, `waste` at elev 0 — so crown is fed only by steam condensation):

- **States:** seeded-random boards, |V| in [4,12], ~1.5|V| pipes, kinds plain/xor/sill, siphons, occasional pre-existing steam.
- **Actions:** live verbs from `server/protocol.py VERBS` (boil/valve/join/tag) + fake verbs/targets + dry-pool hunters so every reject reason is represented.
- **Labels (measured, never modeled):** legality = `MountainWorld.validate` verbatim minus the sid check (UNKNOWN_VERB / UNKNOWN_TARGET / DRY_POOL); one-step outcome = apply with `_apply`'s physics, run one real `WaterGraph.tick()`, `crown_gain` := crown volume strictly rose. Flat 5-way label: `illegal_{unknown_verb,unknown_target,dry_pool}` / `legal_no_gain` / `legal_gain`.
- **Render:** `[STATE] n:<name> k:<kind> z:<elev> v:<vol> s:<steam> … p:<name> <src>><dst> c:<cap> sip:<s> o:<open> … [ACTION] verb:<v> tgt:<t> [LABEL] <label>` — every field a typed token (atom vocabulary per the lattice design).
- **Determinism:** single `random.Random(seed)` stream, canonical sorted-key JSONL, no wall clock; seeded split shuffle (`Random(f"{seed}:split")`, hash-free).

## Real generation run (2026-09-29, `--seed 17 --n 20000`, 6.4 s)

| Split | Rows | Bytes | sha256 |
|---|---|---|---|
| train | 18,000 | 52,454,185 | `466ebdb02de8028ca96f1f30f55e2a411464e46988b0c18a4bb262291d21d964` |
| val | 2,000 | 5,848,523 | `039cc62416286d8251c278ce5efc5d94df9db919ed2649159486ea442f613769` |

Label distribution (train / val): `illegal_unknown_target` 4,327 / 478 · `legal_no_gain` 6,085 / 686 · `illegal_dry_pool` 5,031 / 561 · `illegal_unknown_verb` 1,804 / 186 · `legal_gain` 753 / 89 (the rare class, ~4.2%: crown gain needs steam at tick time — the boil route, the Mountain's own win law). Outputs: `logs/legality_ds/{train,val}.jsonl` + `MANIFEST.json` (sha256 `eb026d7d2a007faf…`: seed, counts, per-split label dist, file hashes).

Full-scale determinism verified by regeneration: second run to a scratch dir produced byte-identical splits (both sha256s matched).

## Tests (receipt numbers, byte-backed)

`tests/test_legality_dataset.py`: 5 tests, all green (`pytest tests/test_legality_dataset.py -q` → `5 passed in 0.89s`).

- `test_determinism_same_seed_identical_file_hashes` — same seed → identical train/val sha256.
- `test_label_spot_check_against_real_engine` — 10 samples (first of each distinct label + head fill, ≥4 labels asserted present in a 60-sample pool) re-derived **independently**: test rebuilds the board via `mag.water_graph.from_spec` (+ steam/primed restore), re-validates per `server/world.py` rules, re-applies, re-ticks, re-measures crown delta; asserts reason, crown_gain, and flat label all match. Never calls the generator's labeler.
- `test_different_seed_changes_bytes`, `test_splits_counts_and_valid_jsonl`, `test_token_render_is_flat_state_action_label`.

**Census (instrument + moment named per B2-216):** `pytest --collect-only -q` at 2026-09-29 (~19:5x local) reads **2,848 tests collected / 402 test files** — up from the 2026-09-27 headline 2,303 / 352. This lane's contribution: +1 file, +5 tests (`tests/test_legality_dataset.py`); the remainder is other lanes' landings 09-27→09-29 and is not attributed here (unattributed drift is a fabrication smell — flagged for the next census refresh, not silently absorbed).

**Full `pytest -q -n 4` (2026-09-29, 723.59 s, exit via pipe):** `4 failed, 2884 passed, 12 skipped, 3 errors`. All 4 failures + 3 errors are outside this lane's files (`test_healthz_status.py` AttributeError, `test_census_drift_patrol.py`, `test_headless_law.py`, `test_party_subchain.py`, `test_swarm_local_drain.py`) — pre-existing/other-lane territory, untouched by W3K (which only adds two new files; nothing imports them but their own test). Lane's own tests green in the same tree: `5 passed in 0.89s` standalone. Note: executed sum (2,900 incl. errors) vs the earlier same-evening collect (2,848) differ by 52 — different instruments at different moments per B2-216; not differenced as a claim.

## Notes / debt

- `legal_gain` is steam-gated by construction (crown strictly highest + cold ⇒ no pipe can feed it). v1 scope note, not a defect: the win route is the boil route, exactly the Mountain's law. A v2 richness knob (rival cold node above crown, making wins impossible on some boards) is one `make_graph_spec` branch away.
- `join`/`tag` are social verbs (no hydraulics) but their legality still labels; crown can still gain from pre-existing steam on their tick — the engine's honest answer.
