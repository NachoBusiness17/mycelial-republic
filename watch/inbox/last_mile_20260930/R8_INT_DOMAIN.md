# R8_INT_DOMAIN — the int64 saturation policy: one volume domain, both engines, measured

2026-09-30 · seat: zcode · ownership: `mag/water_graph.py`, `roblox_to_godot/
systems/water_graph.gd`, `tools/rule_parity.py`, `tests/test_water_graph_int_domain.py`
(+ `tests/test_rule_parity.py` mix amendments), this receipt. Committed at
`0b846c01f` (2026-09-30 19:20:42 -0400, the R12/D-wave commit); the refire pass
(19:45-19:47Z) re-verified every claim below on the committed bytes and completed
this receipt — details in the REFIRE VERIFICATION section.

## Mission (Q16, V2ASK3)

Python ints are unbounded; GDScript ints are 64-bit. The deepest integer product in
the estate is `depth = volume * DEPTH_SCALE` (mag/hydrology.py HydroNode AND
water_graph.gd HydroNode.depth — which `to_dict()` feeds the render layer on every
frame, hydrology flag or not). At volume > INT64_MAX/1000 the Godot product WRAPS
silently while Python computes it exactly: a cross-engine divergence with no crash,
no sensor, and (before this task) no test. Build: (1) the saturation policy; (2)
implement in BOTH engines; (3) a parity stress family in the overflow zone
(volumes ~1e15-1e17); (4) run — identical hashes through the boundary or a named
divergence; (5) tests.

## The policy (the boundary is now a law, not an accident)

**VOLUME DOMAIN LAW: volume and steam live in [0, VOLUME_SAT], where
VOLUME_SAT = (INT64_MAX − ELEV_SAT·HEAD_SCALE) // DEPTH_SCALE = 9,223,372,036,586,340
(~9.223e15). At the boundary: CLAMP + NAMED EVENT — "Node X SATURATES: N absorbed
at the volume ceiling … (int64 depth domain, R8)". Absorbed water is policy-DECLARED
deletion with a sensor (the FRACTURES/STARVED honesty), chosen over the two rejected
options: silent GDScript wrap (theft — diverges the twins invisibly) and a Python
raise (crashes the server on a board-shape problem). The ceiling is derived, not
round: volume ≤ VOLUME_SAT keeps `volume*DEPTH_SCALE` inside int64 even at
cross_section 1, and elev ∈ [−ELEV_SAT, ELEV_SAT] (clamped at ingest) keeps the
hydrology head `elev*HEAD_SCALE + depth` inside int64 with headroom — so mag/
hydrology.py's formulas are safe BY CONSTRUCTION, no edit needed there. Every
runtime increment flows through one saturating receiver `_receive()` at all seven
sites (move-plain, move-waste, gate-commit, gate-hold, starvation-spill, fracture-
spray, condensation); `boil` clamps steam (same domain, silent — no event stream in
its signature, unreachable-in-practice via the 1-unit verb path); `add_node` clamps
volume+elev at ingest silently BY DESIGN (construction precedes the event stream;
both twins clamp identically so tick-1 hashes agree).

## Implementation

- `mag/water_graph.py`: R8 constants + `_receive()` + clamps at every increment
  site + module-doc law. Additive: boards an order below the ceiling are untouched
  (pinned by test).
- `roblox_to_godot/systems/water_graph.gd`: byte-mirrored law (consts, `_receive`
  twin, all mirrored sites, BOTH head laws — the hydrology branch clamps here too).
  NAMED RESIDUAL: Python's `mag/hydrology.py` `_move` override (unowned file) still
  adds raw; the GD mirror is domain-total under both laws, so hydrology-MODE
  cross-engine parity above the ceiling waits on a one-line `_receive` swap there.
  Boolean-mode parity (what the harness measures) is total now.

## The stress family + a second hazard found and closed at the door

`tools/rule_parity.py` gains `stress_domain` (8 seqs in full, 2 in quick, carved
from random 0.46→0.38 — the V5 same-seed byte-compat claim is retired by this
amendment; frame totals unchanged: quick 1,220 ≤ budget 1,500; full 14,040). Four
shapes: one_shot_deliver (delivery across the ceiling), ingest_over (1.1e16–1e17
tank — ingest clamps; pool lands boundary-EXACTLY at VOLUME_SAT), gate_pool_ceiling
(gate-commit + waste-basin absorption), burst_spray (deliberate full-bore mega
pipe: AC2 bursts on tick 1 — threshold ≤ 400 volume — and the mega spray saturates
the sump; the AC2 and R8 laws compose). Delivery pipes run strictly sub-bore
(cap = volume + 10^12) so fracture never masks saturation.

**Probed second hazard (Godot 4.3, binary): the runner's JSON door parses numbers
as float64 — odd values above 2^53 silently round (9223372036586339 → …340),
which would diverge the boards at INGEST, before any physics. Generator law: every
stress magnitude is a multiple of 10^12 (divisible by 2^12 → exact far past 1e17)
or VOLUME_SAT-derived (multiple of 4 → exact below 2^54). Pinned by
`test_stress_family_inputs_survive_the_godot_json_door`.**

## Runs (instrument named; artifacts in `tools/rule_parity_out/`, latest.json standing)

```
.venv/Scripts/python.exe tools/rule_parity.py all --quick --source manual
PARITY: ok mode=quick rows_py=1220   (stress_domain: 2 seqs, diverged 0)

.venv/Scripts/python.exe tools/rule_parity.py all --full --source manual
PARITY: ok mode=full rows_py=14040
  economy 24/24 · fracture_loop 6/6 · gated_siblings 24/24 · mountain 20/20
  · random 18/18 · stress_domain 8/8 — ZERO divergence anywhere
```

**Verdict at the boundary: PARITY HOLDS.** Both engines produce identical
per-tick state hashes through the overflow zone — ingest above the ceiling,
runtime delivery across it, gate/waste/spray absorption, and the boundary-exact
state — on the same boards, same ticks. No divergence to declare; the one named
residual is the Python hydrology `_move` adoption above.

## Tests

`tests/test_water_graph_int_domain.py` (new; 20 tests as landed — the draft said
16, the committed file gained 4 in the landing): the derivation + no-
derived-product-crosses-int64 invariant, hydrology-scale mirror tripwire, depth at
the ceiling int64-safe, ingest clamps (volume/elev/roundtrip), runtime saturation
at all seven sites with exact absorbed accounting, sub-ceiling boards unchanged,
the float64 JSON-door law, and the R8 verdict PINNED end-to-end (one board per
shape, both engines, hashes asserted equal — unlike V5's "verdict is the
measurement", this parity is a law: a fail here means the policy broke).
`tests/test_rule_parity.py` amended (mix pins for quick/full). Focused run:
36 passed. Full-suite run: see below.

## REFIRE VERIFICATION (2026-09-30 23:45-23:47Z, this session, committed bytes)

Independent re-run of the whole verdict chain on the committed tree:

- `tests/test_water_graph_int_domain.py` — **20 passed** (2.29 s), end-to-end
  boundary test included (Godot binary present, not skipped).
- `test_water_graph.py` + `test_water_graph_starvation.py` +
  `test_water_graph_campaign.py` + `test_rule_parity.py` — **52 passed**
  (35.43 s).
- `tools/rule_parity.py all --full --source R8_refire_boundary` —
  `PARITY: ok mode=full rows_py=14040`, stress_domain 8 seqs / 960 tick rows /
  **0 diverged**; **all 8 stress sequences pinned VOLUME_SAT** (seq_074-seq_081,
  i.e., crossed the boundary, hash-identical every tick). Twins digested at run
  time: py `a0b2e30197e5`, gd `7061c783ee7b`; wall 10.33 s.
- V2ASK3 verdict re-read this session
  (`frontier_asks/volley2/results/V2ASK3_raw.json` §Q16): the landed policy is
  its Rule 1 (domain-bounded, not saturation-as-primary) + Rule 3 (one shared
  saturating helper, sticky and hashed, identical in both twins); Rule 2's
  exact q/r decomposition is unnecessary while the domain bound holds — kept as
  the named fallback if VOLUME_SAT ever widens.
- Working-tree note: `water_graph.gd` carries a whitespace-only reindent
  (tabs->spaces, the three R8 functions) over the committed bytes; the Godot
  leg of the run above parsed and executed it — validated, not assumed.

## Full-suite census (instrument: `.venv/Scripts/python.exe -m pytest -q`)

- **Collected (denominator instrument, 20:12 EDT this session):** 3,877 tests
  in 21.06 s (`--collect-only -q`) — the tree has grown past every standing
  headline (census-denominator law: instrument + moment named; the AGENTS
  2,303/352 claim is a 2026-09-27 moment).
- **Full run: ATTEMPTED, KILLED BY THE ENVIRONMENT at ~22%** (~65 min wall,
  ~870 tests executed, 2 failures visible in the progress tape, not yet
  identified when the run died; the untracked sibling test files
  test_flock_parity/test_game_constants/test_mountain_selfplay were probed
  separately — 42 passed, NOT the source). No full-suite green is claimed.
- **Lane-scoped green (the mission's scope, executed and quoted):**
  20 passed (test_water_graph_int_domain.py) + 52 passed (test_water_graph.py,
  test_water_graph_starvation.py, test_water_graph_campaign.py,
  test_rule_parity.py) = **72/72 across every suite this lane owns**.
- **Wider water/parity cluster (this seat, post-detab, 21:0x EDT):** the 4
  above + `test_hydrology.py` + `test_water_computer.py` +
  `test_hydro_xor_sim.py` + `test_k8s_water.py` + int_domain again = **117
  passed, 1 failed** in 14.62 s. The 1: `test_k8s_water.py::
  test_ledger_workload_feeds_simulator` — asserts `waste_seed == 1` against
  the LIVE ledger (`tools/gps_mcp/gps_ledger.db3`), which now holds 67
  failed verdicts: stale expectation vs shared-data growth; no water_graph
  code on its path (not R8).

## Notes

- Violation ratchet (`tools/violation_ratchet.py check --changed`, refire run):
  FAIL from 6 NEW file-too-long hits in `tools/flock_parity.py`,
  `tools/mountain_selfplay.py`, `tools/mountain_units.py`, `tools/reverse_map.py`,
  `tools/rib_fork.py`, `tools/trajectory_minimizer.py` — sibling-lane tree state
  (the draft counted 3; the tree grew since), NOT R8 files; my four owned files
  add zero violations.
- Godot-side probe scripts deleted after use (byte-truth probes only).
