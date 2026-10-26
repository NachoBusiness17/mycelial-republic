# W3M — GOD'S NUMBER FOR OUR MOUNTAIN (2026-09-29)

Mickey17 W3 lane. Seed (operator drop, Math_files): the cube's graph has ~4.3e19
states, diameter 20 = God's Number. Mission: the same artifact for the Mountain
water board — diameter of the reachable state graph under one tick OR one player
action (boil/valve), deterministic. Files owned: `tools/mountain_gods_number.py`
(new), `tests/test_gods_number.py` (new). No git commit (lane law).

## Method

Exhaustive BFS from the initial board (`server/world.py::build_mountain_graph`
over `mag/water_graph.WaterGraph`). The TICK edge is not re-implemented: each
expansion restores a scratch board from the state and runs the REAL
`WaterGraph.tick()` — the diameter is computed on the estate's own physics organ.
Boil edge obeys the server validate law (volume >= 1, else DRY_POOL); valve edge
toggles one pipe's open bit; join/tag never touch physics and are excluded.

State = tracked volumes + TOTAL steam + pipe open bits + siphon primed + sticky
won bit. Two collapses against the mission's literal tuple, both proven:

- waste volume dropped — engine law (`_move`) destroys water entering a waste
  node without crediting it, so v_waste == 0 is invariant;
- per-node steam collapsed to total — the board has exactly one cold node
  (crown, elev 14) and `_condense_steam` moves every node's steam into it;
  nothing else reads steam. Quotient proven exact by test: brute per-node-steam
  BFS projects onto the collapsed BFS with the same reachable set and collapsed
  distance == min preimage distance (preimages can sit at different depths;
  forward evolution from any placement is identical).

## Estimate (before the run, per mission)

6 tracked buckets (5 non-waste volumes + steam) with sum <= 8: C(14,6)=3003,
+5005 for the double-spend corner, x 2^5 open bits x 2 primed x 2 won
= 1,025,024 upper bound < 5M threshold -> exhaustive BFS FITS. (Actual
reachable: 339,840 — the bound was ~3x loose, as an upper bound should be.)

## Engine corner kept AS IS (two loud catches during the run)

p_spring's deferral into the XOR junction is read before p_bypass's direct
commit in the same pipe pass, so a primed open bypass double-spends spring down
to volume == -1 — reachable, and the phantom +1 it mints (the double-spend
conserves the graph sum, so a sibling node can hold w+1 units) is part of the
state space. The bounds check caught both my too-tight invariants mid-run
(phantom `total_water` drift; per-node cap of w violated by hollow=9 backed by
spring=-1) and is now the proven-invariant guard. God's Number describes the
engine we have.

## THE NUMBERS (byte truth, two runs, 11.9s / 12.8s)

- **State count: 339,840 reachable states**
- **GOD'S NUMBER (diameter): 25**
- Farthest state (unique, at depth 25):
  `volumes[spring=-1, terrace=4, gate1=1, hollow=0, crown=0] steam=4
  open[p_out] shut[p_spring, p_terrace, p_drain, p_bypass] siphon_primed[-]
  won=1 water_lost_to_waste=0` — a post-win state: crown boiled back down
  (4 steam aloft), spring double-spent to -1, every valve shut except p_out.
- **Shortest solve (start -> crown >= 4): 5 moves** = the analytic minimum
  (4 x `boil spring` + 1 `tick`; one tick condenses all 4 steam onto the crown).
  Witness replayed through the REAL `MountainWorld` (staged boils apply at tick
  start, physics condenses, winner in one tick) by test.

## Tests (real lines)

- `pytest tests/test_gods_number.py -q` -> **4 passed in 14.44s**
  (hand-computed 12-state fixture map, steam-quotient proof, server replay,
  golden 339,840/25/5 + engine invariants).
- Neighborhood: `pytest tests/test_gods_number.py tests/test_water_graph.py
  tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py
  tests/test_server_v0.py -q` -> **39 passed in 21.24s**.

Rerun: `.\.venv\Scripts\python.exe tools\mountain_gods_number.py`
(add `--board fixture` for the 2-node known-diameter board).
