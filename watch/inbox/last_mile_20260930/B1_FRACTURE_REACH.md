# B1_FRACTURE_REACH — the fracture-reach law: cumulative volume + the gated-inlet seam

**Seat:** water_graph engine + .gd mirror + propagator owner · **Date:** 2026-09-30 · **No commit (working tree).**
**Files owned this lane:** `mag/water_graph.py`, `roblox_to_godot/systems/water_graph.gd`, `tools/legality_propagator.py`, `tests/test_water_graph.py`, `tests/test_propagator.py`, this receipt.
**Cross-lane touches (minimal, flagged):** `tests/test_mountain_reveal.py` (untracked sibling file — one band assertion + one stress assertion HAD to change under the new law or the suite goes red), `tools/mountain_reveal.py` (untracked sibling — one docstring line naming the old band; behavior inherits via import).

## The flag (AJ4 finding 2, AJ4_PLAYTEST.md)

Thresholds `120 + hash%240` = 126-292 stress ticks, but the default Mountain holds 8 units and both sinks are terminal: max honest stress 8. The playtest's forced fracture needed a harness-fed source. And verification here found a DEEPER unreachability under the old law: **gated inlets never stressed at all** (the seam LM2 flagged) — the board's main artery `p_spring` (spring -> xor gate1) could NEVER burst, fed source or not (probe bytes: 2000 fed ticks, stress 0).

## The design decision (picked ONE: cumulative volume)

**Law:** stress accumulates as cumulative throughput — `stress += flow` each full-bore tick (flow == cap) — and the threshold is denominated in the SAME volume units: `200 + djb2(name) % 201 -> [200, 400]` volume. Accumulation shape is AC2's (already `+= flow`); what changed is the threshold's denomination and window.

**Why over "thresholds derived from board capacity":** (a) the threshold stays a pure function of the pipe NAME — one law for every board, djb2-identical across py/.gd/oracle, no graph state threaded into a static function; (b) board capacity is not stable under future sources/recirculation (exactly the mechanism the board needs), so name-anchored thresholds cannot drift when a board gains a source; (c) wear is physical: a cap-k pipe bursts in threshold/k ticks, so throughput, not calendar, kills pipes — no per-board magic. Rejected-B also breaks cross-board comparability of `mountain_reveal`'s `full_bore_ticks_to_burst`.

**Why [200, 400]:** it IS the operator's design window — on the all-cap-1 default Mountain every pipe bursts within 200-400 ticks of sustained full-bore (verified, below). The old [120, 359] band had no design anchor.

**Seam fix (part of the design, not a patch):** full-bore flow INTO a gated junction now stresses at PROBE time in all three surfaces (the water left the source through the pipe section = wear; the gate verdict was never the wear question). On burst the probe-time flow sprays (conserved) and the gate never sees that inlet.

## Where it landed (mirrored, three surfaces)

- `mag/water_graph.py` (400 lines): `fracture_threshold` = `200 + name_hash % 201`; gated branch of `tick()` calls `_fracture` before the LW5 reserve; docstrings carry law+receipt pointers.
- `roblox_to_godot/systems/water_graph.gd`: static `fracture_threshold` parity; gated branch calls `_fracture_if_past_threshold` (no probe reserve — this mirror decrements at GATE phase, its LW5 shape; the burst helper itself moves src->spray). Header's stale "hydrology does not carry the law yet" note corrected (AF2 landed the inherited hook).
- `tools/legality_propagator.py`: `_fracture_threshold` = `200 + _name_hash % 201`; burst law factored into `_stress_and_maybe_burst` shared by `_carry` AND the gated-inlet branch (one law, two call sites — mirrors the engine exactly).
- `mag/hydrology.py` **untouched and verified inheriting** (graded `_move` calls the inherited `_fracture`; tick()'s gated branch is inherited): `tests/test_hydrology.py` AF2 block green on final bytes.

## New board numbers (default Mountain, both engines, byte-identical)

| pipe | old threshold | new threshold | sustained full-bore burst tick |
|---|---|---|---|
| p_spring (gated inlet, xor) | 207 (NEVER fired — seam) | 236 | 237 |
| p_terrace (gated inlet, xor) | 226 (NEVER fired — seam) | 267 | 268 |
| p_out | 292 | 210 | 211 |
| p_drain | 282 | 335 | 336 |
| p_bypass (siphon, starts shut) | 126 | 293 | 294 |

All in [200, 400]; burst = threshold+1 (strict >); two identical runs each (deterministic).

## Verification (bytes, instruments named; all on final bytes)

- **Reach probe** (throwaway py harness, created-run-deleted; the AJ4 fed-source instrument over `build_mountain_graph`'s exact shape): 5/5 pipes PASS (table above), rerun-identical.
- **Godot probe** (throwaway `b1_probe.gd`, SceneTree mode, created-run-DELETED): **12/12 PASS, exit 0** — threshold parity for the 5 names vs Python-computed values, 64-name band [200,400], gated-inlet stress + partial-no-stress, all five sustained-full-bore burst ticks identical to Python (237/268/211/336/294, rerun-identical). Headless smoke `--quit-after 60` exit 0, zero ERROR/WARNING. `git status roblox_to_godot/` carries no probe trace.
- **Tests:** `tests/test_water_graph.py` **19 passed** (16 AD1-era + 3 new B1: gated-inlet stress; gated-inlet burst-at-probe + spray + conservation; default-Mountain reach window 5 pipes x 2 runs); `tests/test_propagator.py` **20 passed** (19 + 1 new B1 gated-inlet seam agreement pinned at verdict AND state level — without either side's seam fix the verdicts diverge and the agreement law breaks); families `test_water_graph{,_starvation,_campaign}.py test_water_computer.py test_hydrology.py test_legality_dataset.py test_mountain_reveal.py test_mountain_liquids.py` green (8-file rerun without k8s/mountain_liquids: **100 passed**; mountain_liquids green in the 10-file combined run below). Combined run (incl. k8s): 130 passed, 1 failed — the failure is **pre-existing, proven**: `tests/test_k8s_water.py::test_ledger_workload_feeds_simulator` fails IDENTICALLY on pristine HEAD engine + a sqlite-backup copy of the live ledger (served 14/110; the ledger grew to 110 events vs the 10 the test was written against; NO FRACTURES event fires in that run — data drift, not this law). Owner: k8s/ledger lane.
- **7,100 agreement sweep (CLI, post-change, final bytes):** seed 17 n=5000 -> 5000/5000; seed 99 n=1000 -> 1000/1000; seed 4242 n=1000 -> 1000/1000. **Total 7,100/7,100 (100.00%)**; seed-17 label distribution byte-identical to AD1's record (dry_pool 1377 / unknown_target 1212 / unknown_verb 473 / legal_gain 213 / legal_no_gain 1725) — fresh boards cannot reach the threshold in the one-tick horizon (W3K caps <= 2), so the retune is invisible to the sweep by design.
- **Ratchet:** `tools/violation_ratchet.py check --changed` -> zero hits on this lane's files (water_graph.py held at exactly 400 lines; first cut was 422 = NEW debt, compressed instead of registered). Remaining NEW hits are sibling-lane files (mountain_reveal/pain_replication/etc.), debt not accepted here.

## Honest reachability note (not smuggled)

The LAW now guarantees: sustained full-bore for 200-400 ticks bursts any pipe on the default Mountain, gated inlets included. Whether a PLAYER can sustain full-bore that long on a closed 8-unit board is the board owner's separate lever (source/recirculation — AJ4's named debt, unchanged). The engine debt named by AJ4 ("thresholds vs board water") is paid; the board-side decision stays flagged.

## Process incident (recorded for the trail)

One `git stash`/`git stash pop` pair against this shared tree collided with a sibling session's `index.lock`; the pop failed cleanly ("stash entry kept") and the stash list count later settled via the sibling's own activity. Working tree verified intact byte-for-byte (all lane edits present, no foreign content in lane files). No git state was mutated by this lane afterward; all further git use read-only. No commit (per mission).

**Every count above read from executed runs this session; no hand-written numbers.**
