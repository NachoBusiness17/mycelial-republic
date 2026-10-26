# WB - WATER ORGAN CENSUS (lane 2/6, 2026-09-30)

| Organ | Physics it has | Gap | Tests |
|---|---|---|---|
| mag/water_graph.py | Integer graph: gravity-only check valves, crest siphons, XOR/sill gates, steam->cold condensation, starvation pooling | No pressure/head-rate (cap constant regardless of drop), no momentum, no 2D | 11 pytest (graph+starvation) |
| mag/water_computer.py | Legacy 3-tank mark-per-tick + steam/rain/ice phase cycle; graph mode delegates | Same discrete physics; fixed legacy topology | 7 pytest |
| mag/hydro_xor_sim.py | Only continuous sim: mL integration, siphon prime/dump/break, conservation, skew | 2-bucket geometry only; constant rates | 15 pytest (P1-P8) |
| games/arena_operator_field.html | grad/div/curl scalar fields, momentum marbles, GPU/CPU divergence receipt | Navigation field, not fluid; no incompressibility | in-page receipt only |
| games/maze_arena.html | BFS flood distance field + handed curl | Static map; zero volume/flow | in-page smoke only |
| roblox_to_godot/systems/water_graph.gd | Faithful port | Never executed pre-2026-09-29 | none |
| roblox_to_godot/systems/flock.gd | Pheromone deposit/decay/steer | No diffusion/advection | none |
| corpus/df_mine | None - biome name strings only; DF's 7-level cellular water absent (twaterlvl.lua = display toggle) | everything | n/a |

## Three missing organs, ranked
1. Pressure/head network - flow prop. to elevation head (Torricelli), upgrading water_graph, the engine everything rides.
2. Continuous 2D advection/incompressible field - unites maze flood + operator field into real currents carrying agents.
3. Erosion/sediment - water reshapes elevations, closing the terrain loop, DF-style emergence.
