# INTAKE: Timestep-Free Iterative Solver (diffusion-as-curriculum) — 2026-09-04

Source: https://x.com/MariiaD_ML/status/2095602848155214240 (2026-09-03, 262 likes / 234 bookmarks)
Author: Mariia Drozdova (@MariiaD_ML), PhD U. Geneva / Paradigms of Intelligence @ Google.
Paper: arXiv 2609.01449 — "Diffusion as a Training Curriculum for Timestep-Free Iterative Reasoning"
Media: GIF — Sudoku-Extreple + Maze-Unique grids shown mid-search (per-step state visualization).

CLAIM: remove timestep conditioning from a denoising model, add persistent memory state
-> an "anytime iterative solver". <250k params, 99.9% Sudoku-Extreme, 98.3% Maze-Unique.
TRI-STATE: Supported (paper + metrics shown; small-author, needs replication before law).

## Rubric (0-25)
- FIT 5/5: direct hit on accumulator primitive (NNUE_SIDECAR_BRIEF_20260904) — persistent
  memory state + tiny param budget is the same thesis. Falsifier workbench can attack the
  anytime claim (accuracy-vs-steps curve = a falsifiable measurement).
- PULL 4/5: HRM-lineage numbers at 250k params; strong bookmark ratio (234/262).
- COST 3/5: training run needed, but tiny model = cheap; 20-lab sweep can host it.
- WINDOW 3/5: not on the Sep 20 proof deadline critical path; maze overlap with B1 maze_arena.
- NOVELTY 4/5: timestep-free denoising + curriculum = genuinely new angle on iterative reasoners.

## SCORE: 19/25 WINDOWED
Builder lane (per LAUNCH law, names the lane, operator gates if KEYS/spend): B-acc-solver —
replicate the Sudoku-Extreme head at 250k params as the accumulator's first falsifiable
benchmark; fold accuracy-vs-iteration curve into falsifier workbench. Sequenced behind the
key-saturation grind; maze variant feeds B1 maze_arena.
