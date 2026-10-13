"""LIGHT REPLAY FALSIFIER — salon_light_thesis_20260904 (S2's sharper version, built).

Thesis under test: one frontier pass lights a maze; dumb marbles navigate by the
stored light and find cheese they have no business finding. Falsifier: SAME maze
seed, one condition with FIELD.json light present, one without — count cheese
acquisitions per 100 trials, dumb marble agent, max 500 steps.

Design (stdlib-only, deterministic, seeded — same numbers every run):
  Maze:      32x32 grid, walls carved by seeded iterative DFS (odd-cell rooms).
             Same seed => byte-identical maze across BOTH conditions (maze_hash
             pins it). Cheese fixed at (15,15), the "circular object's center".
  LIGHT:     The one-time "frontier pass" is simulated by BFS from the cheese:
             every reachable cell gets d = distance-to-cheese, conf = 0.9.
             That BFS IS the expensive judgment-heavy pass; no model is called.
             Emitted as FIELD.json per the salon's minimal light schema:
             coordinates + field slice (d per cell) + target centroid + scalar
             confidence. No chain-of-thought, no secret context (Shape 1 law).
  LIT MARBLE: cannot see the maze. Knows only its own cell and the 4 neighbors'
             light values read from FIELD.json. Moves to the brightest neighbor
             (smallest d), with small seeded tie-break noise (5%) — no path tape,
             no lookahead, no wall memory.
  UNLIT:     the same marble, no field: seeded momentum-biased random walk
             (its "own wits" floor). Blocked proposals burn a step.
  MEASURE:   100 trials per condition, max 500 steps: acquisitions/100 and
             median steps-to-cheese on successes. One-sided two-proportion
             z-test (stdlib math.erfc) — thesis PASSES iff lit > unlit AND
             p < 0.01.

SHADOW BOUNDARY (docstring per the salon's shadow section): this light is
ALWAYS-FRESH BY CONSTRUCTION — the maze is regenerated from the same seed the
field was solved against, so maze_hash matches every run and stale light cannot
occur inside this harness. Stale-light detection (reject a field whose
maze_hash does not match the live maze before any marble consumes it) is
STUBBED, not implemented:
    TODO(shadow): guard_check(field, maze_hash) -> reject + fall back to unlit
    walk on mismatch; also conf-floor rejection (poisoned light, the "one wild
    leaf" calibration law) and the perturbed-maze VARIANT_GUARD. Named by the
    salon as THE DARKROOM (SALON_ARTIFACT.md Shape 3, Unproven there, still
    unproven here). This falsifier only measures the lit-vs-unlit delta.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "memory" / "runs" / "light_falsifier"
ROOM_FILE = ROOT / "watch" / "room.jsonl"

SIZE = 32
SEED = 20260904
TRIALS = 100
MAX_STEPS = 500
START = (1, 1)
CHEESE = (15, 15)  # center-ish room; the circular object's center
LIT_NOISE = 0.05        # prob the lit marble ignores the gradient (seeded)
UNLIT_MOMENTUM = 0.60   # prob the blind walk keeps heading (seeded)
CONF = 0.9              # the one scalar calibration the light carries
P_PASS = 0.01           # significance bar: lit >> unlit at p < noise
DIRS = ((0, -1), (0, 1), (-1, 0), (1, 0))


def build_maze(seed: int) -> list[list[bool]]:
    """Seeded DFS carve: True = wall. Rooms on odd coords, border stays wall."""
    rng = random.Random(f"{seed}:maze")
    grid = [[True] * SIZE for _ in range(SIZE)]
    stack = [START]
    grid[START[1]][START[0]] = False
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in DIRS:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 < nx < SIZE and 0 < ny < SIZE and grid[ny][nx]:
                neighbors.append((nx, ny, x + dx, y + dy))
        if not neighbors:
            stack.pop()
            continue
        nx, ny, wx, wy = rng.choice(neighbors)
        grid[wy][wx] = False
        grid[ny][nx] = False
        stack.append((nx, ny))
    return grid


def maze_hash(grid: list[list[bool]]) -> str:
    blob = bytes(bool(c) for row in grid for c in row)
    return hashlib.sha256(blob).hexdigest()[:16]


def frontier_solve(grid: list[list[bool]]) -> tuple[dict[str, dict], int]:
    """THE ONE-TIME FRONTIER PASS, simulated: BFS from cheese over the maze.

    Returns (light dict, cells_expanded). The expanded-cell count is the cost
    line — the capture.mp4 of this script. No model call; BFS is the judgment.
    """
    dist = {CHEESE: 0}
    frontier = [CHEESE]
    expanded = 0
    while frontier:
        x, y = frontier.pop(0)
        expanded += 1
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and not grid[ny][nx] and (nx, ny) not in dist:
                dist[(nx, ny)] = dist[(x, y)] + 1
                frontier.append((nx, ny))
    light = {f"{x},{y}": {"d": d, "conf": CONF} for (x, y), d in dist.items()}
    return light, expanded


def run_trial(grid: list[list[bool]], lit: bool, trial: int,
              light: dict[str, dict] | None) -> int | None:
    """One marble run. Returns steps-to-cheese or None if 500 steps run out."""
    rng = random.Random(f"{SEED}:{'lit' if lit else 'unlit'}:{trial}")
    x, y = START
    heading = 0
    for step in range(1, MAX_STEPS + 1):
        if (x, y) == CHEESE:
            return step - 1
        if lit:
            cands = []
            for dx, dy in DIRS:
                key = f"{x + dx},{y + dy}"
                if key in light:  # walls have no light entry — that is ALL it sees
                    cands.append((light[key]["d"], dx, dy))
            if not cands:
                continue
            if rng.random() < LIT_NOISE:
                _, dx, dy = rng.choice(cands)
            else:
                best = min(c[0] for c in cands)
                _, dx, dy = rng.choice([c for c in cands if c[0] == best])
        else:
            if rng.random() >= UNLIT_MOMENTUM:
                heading = rng.randrange(4)
            dx, dy = DIRS[heading]
            nx, ny = x + dx, y + dy
            if not (0 <= nx < SIZE and 0 <= ny < SIZE) or grid[ny][nx]:
                continue  # blind proposal hits a wall; the step burns
        x, y = x + dx, y + dy
    return None


def z_test_p(a: int, na: int, b: int, nb: int) -> float:
    """One-sided two-proportion z-test, stdlib only."""
    p1, p2 = a / na, b / nb
    pool = (a + b) / (na + nb)
    if pool in (0.0, 1.0) or p1 == p2:
        return 0.5
    z = (p1 - p2) / math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))
    return 0.5 * math.erfc(z / math.sqrt(2))


def main() -> None:
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    grid = build_maze(SEED)
    mhash = maze_hash(grid)
    light, frontier_cost = frontier_solve(grid)

    field = {
        "schema": "light.v0",
        "maze_hash": mhash,
        "seed": SEED,
        "target": {"x": CHEESE[0], "y": CHEESE[1]},
        "start": {"x": START[0], "y": START[1]},
        "frontier_pass": {"algorithm": "bfs(simulated)", "cells_expanded": frontier_cost},
        "light": light,
    }

    results = {}
    for cond, is_lit in (("lit", True), ("unlit", False)):
        runs = [run_trial(grid, is_lit, t, light if is_lit else None) for t in range(TRIALS)]
        wins = [r for r in runs if r is not None]
        results[cond] = {
            "acquisitions": len(wins),
            "trials": TRIALS,
            "median_steps_success": statistics.median(wins) if wins else None,
            "steps_on_success": sorted(wins),
        }

    lit_r, unlit_r = results["lit"], results["unlit"]
    p = z_test_p(lit_r["acquisitions"], TRIALS, unlit_r["acquisitions"], TRIALS)
    verdict = "PASS" if (lit_r["acquisitions"] > unlit_r["acquisitions"] and p < P_PASS) else "FAIL"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    field_path = OUT_DIR / f"FIELD_{ts}.json"
    field_path.write_text(json.dumps(field), encoding="utf-8")
    result = {
        "ts": ts,
        "run": "light_replay_falsifier",
        "salon": "salon_light_thesis_20260904",
        "params": {"seed": SEED, "size": SIZE, "trials": TRIALS, "max_steps": MAX_STEPS,
                   "start": START, "cheese": CHEESE, "lit_noise": LIT_NOISE,
                   "unlit_momentum": UNLIT_MOMENTUM, "conf": CONF, "p_pass": P_PASS},
        "maze_hash": mhash,
        "frontier_pass_cells_expanded": frontier_cost,
        "field_file": str(field_path.relative_to(ROOT)),
        "results": results,
        "p_value_one_sided": p,
        "verdict": verdict,
    }
    out_path = OUT_DIR / f"{ts}.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    gist = (f"lit {lit_r['acquisitions']}/100 (median {lit_r['median_steps_success']} steps) "
            f"vs unlit {unlit_r['acquisitions']}/100 (median {unlit_r['median_steps_success']}) "
            f"— VERDICT {verdict} (p={p:.2e}) — {out_path.relative_to(ROOT)}")
    receipt = {"ts": "2026-09-04", "thread": "salon", "seat": "card-worker", "type": "receipt",
               "item": "light_replay_falsifier", "gist": gist}
    with ROOM_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(receipt) + "\n")

    print(f"LIGHT REPLAY FALSIFIER  maze_hash={mhash}  seed={SEED}  "
          f"frontier pass={frontier_cost} cells (one-time)")
    print(f"{'condition':<10} {'acquisitions':>14} {'median steps':>14}")
    print(f"{'lit':<10} {lit_r['acquisitions']:>10}/{TRIALS:<3} "
          f"{str(lit_r['median_steps_success']):>14}")
    print(f"{'unlit':<10} {unlit_r['acquisitions']:>10}/{TRIALS:<3} "
          f"{str(unlit_r['median_steps_success']):>14}")
    print(f"p (one-sided) = {p:.3e}   VERDICT: {verdict}")
    print(f"result: {out_path}")
    print(f"field:  {field_path}")
    print(f"receipt appended to watch/room.jsonl: {gist}")


if __name__ == "__main__":
    main()
