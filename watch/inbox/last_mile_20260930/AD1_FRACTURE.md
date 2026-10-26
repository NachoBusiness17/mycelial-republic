# AD1_FRACTURE — AC2's pipe-fracture mechanic, landed

**Seat:** water_graph engine + .gd mirror + propagator owner · **Date:** 2026-09-29 · **No commit (working tree).**
**Files owned this lane:** `mag/water_graph.py`, `roblox_to_godot/systems/water_graph.gd`, `tools/legality_propagator.py`, `tests/test_water_graph.py`, `tests/test_propagator.py`, this receipt.

**Spec source note:** the mission cited `watch/inbox/last_mile_20260930/AC2_DESIGN.md` §4 — that file is NOT on disk (find over the repo returns nothing). The mission text itself carried the full §4 law; this lane built exactly that law, nothing more.

## The law (as specified, as built)

1. **`Pipe.stress: int`** — in `_move`, `p.stress += flow` only when `flow == cap` (full bore). Partial flow loads nothing.
2. **Threshold = `120 + hash(name) % 240`** → [120, 359]. Deterministic, zero RNG. The "hash" is **djb2 32-bit written as an explicit loop** (`name_hash`, h=5381, h*33+ord, &0xFFFFFFFF): Python's builtin `hash()` is salted per process (PYTHONHASHSEED) — it could never be cross-run deterministic NOR agree with the Godot mirror, so the law carries its own byte-stable hash, identical loop in both languages.
3. **On exceed** (`stress > threshold`, strictly): `p.fractured = True`, `p.open = False`, **this tick's flow sprays to the lowest-elevation node other than dst** (first-min in insertion order; `min(key=elev)` / strict-`<` loop), event grammar exact: `Pipe X FRACTURES (stress N): spray to Y.` Conservation: src -= flow, spray += flow — nothing deleted.

## Where it landed

- **`mag/water_graph.py`** (387 lines): `name_hash`/`fracture_threshold` module-level; `Pipe.stress/.fractured`; `_fracture()` helper hooked in `_move` before the volume commit; tick loop skips `p.fractured or not p.open`; **`open()` refuses a fractured pipe** (the valve verb routes through it — server/world.py `_apply` and dataset `engine_apply` both land there, so the burst is permanent everywhere at one choke point); `to_spec`/`from_spec` carry `stress`/`fractured` (LW5 roundtrip law — a burst pipe must survive the estate roundtrip closed).
- **`roblox_to_godot/systems/water_graph.gd`**: same fields, same `name_hash`/`fracture_threshold` (static), same `_fracture_if_past_threshold` + `_spray_target`, hooked in **both** `_move` head laws (boolean + Z10 graded — a stressed pipe does not care which law computed its flow; AC5 precedent); `open_pipe` refuses bursts; tick skip; `to_dict` emits the two keys. First cut broke game.gd's preload (tab/space mix) — fixed, smoke re-run green.
- **`tools/legality_propagator.py`** (361 lines): a fractured pipe is **closed for legality purposes** (FLOW skip), the valve action **never toggles** a fractured pipe (mirrors the engine's refused reopen), and `_carry` re-derives the full stress/spray law engine-free (own djb2 copy — the independence test still passes). Rationale: a fresh board cannot reach threshold ≥120 in the one-tick horizon (W3K caps ≤2), but specs can CARRY stress/fractured state, and the agreement law is total.

## Verification (bytes, instruments named)

- **Tests:** `tests/test_water_graph.py` **16 passed** (11 old + 5 new: full-bore-only accumulation; burst exactly at threshold with exact event grammar + dst skipped; threshold determinism/range/spread; one-shot burst conserves volume + reopen refused; spec roundtrip preserves stress/fractured). `tests/test_propagator.py` **19 passed** (15 old + 4 new: fractured-closed verdict agreement incl. the adversarial open=True+fractured shape; valve-on-fractured agreement; mid-tick fracture spray agreement at verdict AND state level). Instruments: `pytest -q`, this session; collect-only reads 35 for the two files.
- **Negative control (the test bites):** with the stress key stripped from the spec, the oracle reads `legal_gain` where the engine reads `legal_no_gain` — the propagated stress law is load-bearing, not decorative.
- **7,100 agreement sweep (CLI, post-change):** seed 17 n=5000 → **5000/5000**; seed 99 n=1000 → **1000/1000**; seed 4242 n=1000 → **1000/1000**. **Total 7,100/7,100 (100.00%)**; seed-17 label distribution byte-identical to AC7's record (dry_pool 1377 / unknown_target 1212 / unknown_verb 473 / legal_gain 213 / legal_no_gain 1725) — the family cannot reach the fracture law; the hand-built boards are the coverage.
- **Adjacent families:** `pytest tests/test_water_graph.py tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py tests/test_water_computer.py tests/test_hydrology.py tests/test_k8s_water.py tests/test_propagator.py tests/test_legality_dataset.py -q` → **85 passed**.
- **Godot:** headless smoke `--quit-after 60` → **exit 0, zero ERROR/WARNING** (banner only). Functional probe (throwaway `ac2_probe.gd`, SceneTree mode, created-run-DELETED): **20/20 PASS, exit 0** — hash+threshold parity against Python-computed values for 5 names (a=190, burst=253, one_shot=316, p_climb=291, p_spring=207), full-bore-only stress, burst at 253 with exact event, spray lands/conserved, reopen refused, graded-head branch identical. Probe log `/tmp/ac2_probe.log`; `git status roblox_to_godot/` clean of the probe.
- **Ratchet:** `tools/violation_ratchet.py check --changed` → 0 hits on this lane (387/361 lines, under the 400 cap). The 2 NEW hits (file-too-long `tools/concept_predictor.py:494`, `tools/env_contract.py:563`) are untracked sibling-lane co-tenants; debt not accepted here (only their owner accepts by name).

## Flagged for other owners (not smuggled in)

- **`mag/hydrology.py` `_move` override** does not carry the fracture law (it overrides the base `_move` wholesale) — the .gd's graded branch now outruns its Python counterpart; also still lacks the V5 waste-accumulation (pre-existing, AC5 noted the mirror side). Owner: hydrology lane.
- `tools/legality_dataset.py` `make_graph_spec` never emits stress/fractured (fine — defaults hold; fractured-state coverage lives in the hand-built propagator tests).

**Every count above read from executed runs this session; no hand-written numbers.**
