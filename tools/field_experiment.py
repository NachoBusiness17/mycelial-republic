"""field_experiment -- FIELD-2 (THE FOUNDATION POUR): field steering vs list steering.

Spec: watch/inbox/model_garden/STEERING_FIELD_THEORY.md sec 3 (the falsifiable
minimal experiment). Claim to kill or prove: allocating the day's work by
relaxing a GPS-elevated integer field with boid-family advection beats the
current driver's sequential queue, at equal-or-lower cost, judged on real
outcomes.

ASSEMBLY (six organs + one adapter, per the spec's table; all imported, none
forked):
  task stream        tools/k8s_water_sim.py workload_from_ledger (GPS ledger
                     verdict_log feed; tested by tests/test_k8s_water.py)
  FIELD kernel       mag/field_flow.py via mag/river.py (sill erosion ON)
  advection law      mag/flock_positive.py step_positive (LM9, one school per
                     model family; satiation explore/exploit)
  impulse organ      mag/steer_seal.py seal + admit_text (the sealed pour)
  doctrine           mag/water_swarm.py water_doctrine (the impulse payload)
  goal field         mag/flock_field.py (PhiField descent picks the lure cell)
  work census        mag/flock_scheduler.py plan (board column order + tiers)
  LIST arm (control) tools/k8s_water_sim.py simulate, exactly as shipped
  gates              mag/water_graph.py (serve pipe cap, waste boil, esc lane)
  adapter (new)      seed_terrain() below (~40 lines): the L2 wire

DEVIATIONS (spec text vs bytes; bytes win, per lane order):
  D1 ELEVATION POLARITY. Spec sec 3: "elev = pass_rate scaled 0-255". The
     bytes fight: field_flow pours DOWNHILL (strictly-lower heads only), so a
     literal pass_rate terrain would advect work TOWARD failing coordinates
     (pass_rate 0 = lowest = the sinks), inverting the spec's own metric 2
     (wasted dispatches at DECLINING coordinates). flock_field's bytes resolve
     the fight: its field phi is "distance-to-solution" and agents steer by
     -grad(phi) (descent to goal, low = good). So the board's elevation is the
     COST terrain: elev = 4 + round((1 - pass_rate) * 200). Good coordinates
     are valleys work pools in; bad coordinates are ridges work sheds off.
  D2 PER-CELL CROSS_SECTION. Spec sec 2: "cross_section[c] = GPS sample_size".
     field_flow bytes carry ONE board-wide cross_section; the L2 wire needs
     per-cell. Implemented as a _head override in FieldBoard (the river.py
     precedent: subclass, override the one law that needs more state).
  D3 SERVE BUDGET SHAPE. Both arms get the same total serve capacity per tick
     (4 units: the k8s demo's quota 2 + burst cap 2). The list arm's 4 is
     conditional (burst primes only at mux backlog >= crest); the field arm's
     serve pipe is a flat cap 4. Logged, not hidden.
  D4 WASTED-DISPATCH COUNTING. The list arm replays the driver's historical
     dispatches (its arrivals ARE its sends), so its wasted dispatches are
     counted at arrival time from the ledger rows; the field arm re-routes
     work through the terrain before service, so its wasted dispatches are
     counted at service time (the coordinate the gate drew from). Both name
     the coordinate where work executed; the asymmetry is the arms' own.
  D5 FISH LAYER FLOATS. The water/ledger/gate layers are integer-only (the
     estate determinism law). The boid layer rides flock_positive's own float
     constants (the game's 60Hz law, LM9); determinism verified by double-run
     digest on the same machine.

Budget: the sim is $0 (integer Python, stdlib). Only the judge turns cost
(fired separately through tools/model_garden.py; hard cap $1 per lane order).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.field_flow import HEAD_SCALE, DEPTH_SCALE  # noqa: E402
from mag.river import River  # noqa: E402
from mag.flock_positive import (  # noqa: E402
    DT, FOOD_PREF_DIST, Fish, FoodSource, POOLS, seed_school, step_positive,
)
from mag.water_graph import WaterGraph  # noqa: E402
from tools.k8s_water_sim import (  # noqa: E402
    simulate as k8s_simulate,
    spec_from_workload,
    workload_from_ledger,
)
from tools.gps_mcp.ledger import (  # noqa: E402
    MOMENTUM_RISING_DELTA, MOMENTUM_WINDOW,
)

SCHEMA = "field_experiment.v1"
DB_PATH = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
GARDEN = ROOT / "watch" / "inbox" / "model_garden"
BOARD_SPEC_PATH = GARDEN / "FIELD2_BOARD_SPEC.json"

MAX_TICKS = 400          # both arms, identical (the work-tick budget)
if os.environ.get("FIELD2_MAX_TICKS"):       # debug override, never in anger
    MAX_TICKS = int(os.environ["FIELD2_MAX_TICKS"])
SERVE_CAP = 4            # units/tick through the gate (quota 2 + burst 2)
FISH_SUBTICKS = 60       # one scheduler tick = one 60Hz fish-second
SCHOOL_N = 12            # seed_school default (one school per family)
WEAK_PASS = 0.5          # pre-registered weak-coordinate threshold
IMPULSE_FOOD = 30.0      # the sealed pour's lure size (LM9: lure, never chase)

# fish-board geometry: 9x9 cells laid on the game's own board scale
CELL_W, CELL_H = 120.0, 66.0
CELL_X0, CELL_Y0 = 90.0, 75.0
POOL_KEYS = ("spring", "terrace", "gate1", "hollow", "waste", "crown")


def cell_center(r: int, c: int) -> tuple[float, float]:
    return (CELL_X0 + c * CELL_W, CELL_Y0 + r * CELL_H)


# --------------------------------------------------------------------------
# 0. ledger reads (the GPS terrain + the arrival stream)
# --------------------------------------------------------------------------
def read_ledger(db_path: Path = DB_PATH) -> dict:
    """Everything the experiment needs from gps_ledger.db3, read-only:
    verdict_log rows in (ts, rowid) order, the capability table, and the
    per-pair momentum badges computed by the estate's own constants."""
    con = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT ts, model_id, task_shape, verdict FROM verdict_log"
            " ORDER BY ts, rowid").fetchall()
        cap = con.execute(
            "SELECT model_id, task_shape, pass_rate, sample_size FROM capability"
        ).fetchall()
    finally:
        con.close()
    # momentum per pair, the estate formula verbatim (ledger.py momentum()):
    # window = last MOMENTUM_WINDOW verdicts, oldest half vs newest half.
    verdicts: dict[tuple[str, str], list[int]] = {}
    for _ts, m, s, v in rows:
        verdicts.setdefault((m, s), []).append(int(v))
    momentum = {}
    for pair, vs in verdicts.items():
        window = vs[-MOMENTUM_WINDOW:]
        half = len(window) // 2
        if half == 0:
            start = recent = sum(window) / len(window)
        else:
            start = sum(window[:half]) / half
            recent = sum(window[half:]) / (len(window) - half)
        delta = recent - start
        badge = ("RISING" if delta > MOMENTUM_RISING_DELTA
                 else "DECLINING" if delta < -MOMENTUM_RISING_DELTA
                 else "STEADY")
        momentum[pair] = badge
    return {"rows": rows, "capability": cap, "momentum": momentum}


def weak_set(led: dict) -> set[tuple[str, str]]:
    """Pre-registered weak-coordinate rule: pass_rate < 0.5 OR the estate's
    momentum badge says DECLINING. These are the dollar-leak coordinates."""
    out = set()
    for m, s, pr, _n in led["capability"]:
        if float(pr) < WEAK_PASS:
            out.add((m, s))
    out |= {p for p, b in led["momentum"].items() if b == "DECLINING"}
    return out


# --------------------------------------------------------------------------
# 1. seed_terrain -- THE ADAPTER (the L2 wire, ~40 lines)
# --------------------------------------------------------------------------
def seed_terrain(led: dict, column_order: list[str]) -> dict:
    """The ledger-to-board adapter: pass_rate -> elevation (cost terrain,
    deviation D1), sample_size -> per-cell cross_section (the L2 wire,
    deviation D2). Output is the persisted board spec (frozen bytes)."""
    cap = {(m, s): (float(pr), int(n)) for m, s, pr, n in led["capability"]}
    models = sorted({m for m, _s, _pr, _n in led["capability"]}
                    | {m for _ts, m, _s, _v in led["rows"]})
    shapes = [s for s in column_order
              if s in {sh for _m, sh, _pr, _n in led["capability"]}]
    shapes += sorted({sh for _m, sh, _pr, _n in led["capability"]}
                     - set(shapes))
    elev, cs = [], []
    for m in models:
        erow, crow = [], []
        for s in shapes:
            if (m, s) in cap:
                pr, n = cap[(m, s)]
                erow.append(4 + int(round((1.0 - pr) * 200)))  # D1
                crow.append(max(1, n))                          # D2 / L2
            else:
                erow.append(150)          # unmeasured = expensive neutral
                crow.append(1000)         # the field_flow default tank
        elev.append(erow)
        cs.append(crow)
    return {"schema": SCHEMA, "models": models, "shapes": shapes,
            "elev": elev, "cross_section": cs,
            "cell": {"models": len(models), "shapes": len(shapes)},
            "pass_rate": {f"{m}|{s}": cap[(m, s)][0] for m in models
                          for s in shapes if (m, s) in cap},
            "sample_size": {f"{m}|{s}": cap[(m, s)][1] for m in models
                            for s in shapes if (m, s) in cap}}


def column_order_from_scheduler(shapes: list[str]) -> list[str]:
    """flock_scheduler.plan() over the day's unique work items: its
    embedding/cluster pass orders the board's columns (the swarm-allocates
    organ contributes the layout; the run reads the persisted order, so
    determinism never depends on a live Ollama)."""
    from mag import flock_scheduler as fs
    plan = fs.plan(shapes)
    seen, order = set(), []
    for a in plan.get("assignments", []):
        t = a["task"]
        if t not in seen:
            seen.add(t)
            order.append(t)
    return order + [s for s in shapes if s not in seen]


# --------------------------------------------------------------------------
# 2. the seat list (BLIND, pre-registered BEFORE any arm runs)
# --------------------------------------------------------------------------
def seat_list(led: dict) -> list[dict]:
    """What this seat would route where, from the capability bytes only:
    per shape, the highest pass_rate with sample_size >= 3 (fallback >= 1);
    ties break to the larger sample, then alphabetical model_id."""
    by_shape: dict[str, list[tuple[float, int, str]]] = {}
    for m, s, pr, n in led["capability"]:
        by_shape.setdefault(s, []).append((float(pr), int(n), m))
    picks = []
    for s in sorted(by_shape):
        cands = sorted(by_shape[s], key=lambda t: (-t[0], -t[1], t[2]))
        strong = [t for t in cands if t[1] >= 3] or [t for t in cands if t[1] >= 1]
        if strong:
            picks.append({"shape": s, "model": strong[0][2],
                          "pass_rate": round(strong[0][0], 4),
                          "sample_size": strong[0][1]})
    return picks


# --------------------------------------------------------------------------
# 3. FIELD arm
# --------------------------------------------------------------------------
class FieldBoard(River):
    """River (field_flow + sill erosion) with the L2 wire: per-cell
    cross_section from GPS sample_size (deviation D2). The silt mantle is
    seeded uniform (4/cell): river's own law requires loose material before
    any cell can carve ("an initial silt mantle bounds total carving"), and
    a zero mantle would silently disable the erosion the spec demands ON."""

    SILT_MANTLE = 4

    def __init__(self, spec: dict) -> None:
        super().__init__([row[:] for row in spec["elev"]],
                         silt=[[self.SILT_MANTLE] * len(spec["elev"][0])
                               for _ in spec["elev"]])
        self.cs_grid = [row[:] for row in spec["cross_section"]]

    def _head(self, y: int, x: int, v: int) -> int:
        return (self.elev[y][x] * HEAD_SCALE
                + v * DEPTH_SCALE // self.cs_grid[y][x])

    def draw(self, y: int, x: int, n: int) -> None:
        """The serve gate removes n units from a cell (attention spent)."""
        if n < 1 or self.vol[y][x] < n:
            raise AssertionError(f"draw {n} at ({y},{x}) vol {self.vol[y][x]}")
        self.vol[y][x] -= n
        self._mark_dirty(y, x)


def run_field_arm(led: dict, spec: dict, seal_home: Path) -> dict:
    models, shapes = spec["models"], spec["shapes"]
    ridx = {m: i for i, m in enumerate(models)}
    weak = weak_set(led)

    # arrival stream: same feed law as the k8s arm (verdict=1 -> pour at its
    # historical coordinate; verdict=0 -> pre-shed into the waste basin)
    ticks: dict[str, int] = {}
    arrivals: dict[int, list[tuple[int, int]]] = {}
    waste_origin: list[tuple[int, int]] = []
    for ts, m, s, v in led["rows"]:
        t = ticks.setdefault(ts, len(ticks) + 1)
        if int(v):
            arrivals.setdefault(t, []).append((ridx[m], shapes.index(s)))
        else:
            waste_origin.append((ridx[m], shapes.index(s)))
    n_arrival_ticks = len(ticks)

    board = FieldBoard(spec)
    g = WaterGraph()
    g.add_node("field_out", elev=2)
    g.add_node("served", elev=0)
    g.add_node("waste", elev=0, kind="waste", volume=len(waste_origin))
    g.add_node("crown", elev=200, kind="cold")
    g.add_pipe("serve", "field_out", "served", cap=SERVE_CAP)

    # schools: one per model family, seeded by pool rotation (no quality info)
    schools = []
    for i in range(len(models)):
        schools.append(seed_school(seed=20261001 + i,
                                   pool=POOL_KEYS[i % len(POOL_KEYS)],
                                   n=SCHOOL_N))
    fish_all = [f for sch in schools for f in sch]

    # the sealed impulse (steer_seal, offline $0): lure at the goal-field
    # minimum. Payload carries the water doctrine (water_swarm organ).
    lure = None
    seal_receipt = {"fired": False}
    goal_pair = impulse_target(led, spec)
    if goal_pair is not None:
        env, receipt = mint_sealed_pour(seal_home, goal_pair)
        seal_receipt.update(receipt)
        if env is not None:
            seal_receipt["fired"] = True
            seal_receipt["coordinate"] = (
                f"{models[goal_pair[0]]}|{shapes[goal_pair[1]]}")

    queue: list[tuple[int, int]] = []       # field_out FIFO: (row, col) tags
    waste_fifo: list[tuple[int, int]] = waste_origin[:]  # esc-lane tags (historical cells)
    served_events: list[tuple[int, int, int]] = []
    trace: list[dict] = []
    total_work = len(waste_origin) + sum(len(v) for v in arrivals.values())
    expected_cum = len(waste_origin)   # the waste seed lands before tick 1
    arrived_cum = 0
    t80 = None
    t80_literal = None
    impulse_tick = None

    for tick in range(1, MAX_TICKS + 1):
        # 1. arrivals pour onto the terrain (the workload feed)
        for (r, c) in arrivals.get(tick, []):
            board.add_water(r, c, 1)
            arrived_cum += 1
            expected_cum += 1
        if tick == 1:
            arrived_cum += len(waste_origin)
        # 2. relaxation + erosion (one Jacobi tick, dirty-block law)
        board.tick()
        # 3. boid advection: one fish-second at the game's 60Hz
        food = [FoodSource(pos=cell_center(r, c), amount=float(board.vol[r][c]))
                for r in range(len(models)) for c in range(len(shapes))
                if board.vol[r][c] > 0]
        # the sealed pour fires ONCE at placement time (half the day arrived)
        if lure is None and seal_receipt["fired"] and arrived_cum * 2 >= total_work:
            lure = FoodSource(pos=cell_center(goal_pair[0], goal_pair[1]),
                              amount=IMPULSE_FOOD)
            impulse_tick = tick
        if lure is not None and lure.amount > 0:
            food.append(lure)
        sim_t = float(tick - 1)
        for _ in range(FISH_SUBTICKS):
            for sch in schools:
                for f in sch:
                    step_positive(f, sch, food, DT, sim_t)
            sim_t += DT
        # 4. attendance: a cell is attended when a fish is GRAZING ITS PATCH.
        # The arrival gate is FOOD_PREF_DIST (game.gd's own "arrived at the
        # pool" radius, where the pull stops), not EAT_RADIUS (mouth-on-food,
        # which stays the organ's bite law): the dead band 10-30px is where
        # a milled school stands ON the patch. The A/B harness's t80 uses
        # the same convention (TARGET_RADIUS 25 = "at target").
        att: dict[tuple[int, int], int] = {}
        for f in fish_all:
            r = round((f.pos[1] - CELL_Y0) / CELL_H)
            c = round((f.pos[0] - CELL_X0) / CELL_W)
            if (0 <= r < len(models) and 0 <= c < len(shapes)
                    and math.hypot(f.pos[0] - cell_center(r, c)[0],
                                   f.pos[1] - cell_center(r, c)[1]) <= FOOD_PREF_DIST):
                att[(r, c)] = att.get((r, c), 0) + 1
        ranked = sorted(((n, board.vol[r][c], r, c) for (r, c), n in att.items()
                         if board.vol[r][c] > 0), reverse=True)
        # 5. escalation: boil 1 unit/tick of shed work; the steam condenses
        # at the cold crown, and the condensed RETRY re-pours onto the
        # terrain at its historical cell (the field's second chance: the
        # retry walks the terrain like every other dispatch; the k8s arm's
        # esc lane feeds its mux directly -- each arm's own law).
        if g.nodes["waste"].volume > 0:
            g.boil("waste", 1)
        g.tick()          # condense steam -> crown (no pipes left to flow:
        # field_out is empty between offers, so this tick only condenses)
        for _ in range(g.volume("crown")):
            if waste_fifo:
                r, c = waste_fifo.pop(0)
                board.add_water(r, c, 1)
                g.nodes["crown"].volume -= 1   # the retry leaves the crown
        # 6. the gate: attended cells feed field_out; the serve pipe caps
        # the tick's total at SERVE_CAP
        offered = 0
        for _n, _v, r, c in ranked:
            if offered >= SERVE_CAP:
                break
            take = min(board.vol[r][c], SERVE_CAP - offered)
            if take <= 0:
                continue
            board.draw(r, c, take)
            queue.extend([(r, c)] * take)
            g.nodes["field_out"].volume += take
            offered += take
        served0 = g.volume("served")
        g.tick()
        got = g.volume("served") - served0
        assert g.volume("field_out") == 0, f"tick {tick}: gate backlog"
        for _ in range(got):
            served_events.append((tick, *queue.pop(0)))
        # 7. audit + trace
        vol_total = (board.total_volume() + g.volume("field_out")
                     + g.volume("served") + g.volume("waste")
                     + g.volume("crown")
                     + sum(n.steam for n in g.nodes.values()))
        assert vol_total == expected_cum, f"tick {tick}: leak {vol_total}"
        silt_total = sum(sum(row) for row in board.silt)
        assert silt_total == FieldBoard.SILT_MANTLE * len(models) * len(shapes), \
            f"tick {tick}: silt leak {silt_total}"
        shed_now = g.volume("waste") + sum(n.steam for n in g.nodes.values())
        served_now = g.volume("served")
        trace.append({"tick": tick, "served": served_now, "shed": shed_now,
                      "arrived": arrived_cum, "attended_cells": len(att),
                      "standing_board": board.total_volume(),
                      "gate_queue": len(queue), "wetted": board.last_processed})
        # t80 primary (pre-registered fix): first tick with >= 80% of the
        # whole 242-unit workload SERVED. The spec's literal variant (served
        # + standing-waste over arrived) is degenerate here: the 67-unit
        # waste seed stands as "shed" from tick 1, so it reads 1 for both
        # arms; both variants are reported.
        if t80 is None and served_now * 5 >= 4 * total_work:
            t80 = tick
        if t80_literal is None and arrived_cum and (
                served_now + shed_now) >= 0.8 * arrived_cum:
            t80_literal = tick
        idle = (not any(t > tick for t in arrivals)
                and board.total_volume() == 0 and len(queue) == 0
                and g.volume("field_out") == 0 and g.volume("crown") == 0
                and g.volume("waste") == 0
                and all(n.steam == 0 for n in g.nodes.values()))
        if idle:
            break

    # wasted dispatches: service events at weak coordinates (D4)
    wasted = sum(1 for _t, r, c in served_events
                 if (models[r], shapes[c]) in weak)
    # per-shape service tallies (the decision record for the duel)
    tally: dict[tuple[str, str], int] = {}
    for _t, r, c in served_events:
        k = (models[r], shapes[c])
        tally[k] = tally.get(k, 0) + 1
    dbg = os.environ.get("FIELD2_DEBUG")
    if dbg:
        Path(dbg).write_text(json.dumps({
            "trace": trace,
            "board_vol": board.vol, "board_elev": board.elev,
            "board_silt": board.silt,
            "fish": [[f.pos[0], f.pos[1], round(f.satiation, 2)] for f in fish_all],
            "served_events": served_events,
            "waste_fifo_left": len(waste_fifo),
        }, default=str), encoding="utf-8")
    return {"arm": "field", "ticks_used": trace[-1]["tick"] if trace else 0,
            "t80": t80, "t80_literal": t80_literal,
            "served": g.volume("served"),
            "wasted_dispatches": wasted, "service_events": len(served_events),
            "tally": {f"{m}|{s}": n for (m, s), n in sorted(tally.items())},
            "ticks_arrivals": n_arrival_ticks,
            "seal": seal_receipt, "impulse_tick": impulse_tick,
            "erosion_total": board.total_eroded,
            "wetted_total": board.total_processed,
            "trace": trace}


# --------------------------------------------------------------------------
# the impulse organ: goal-field descent + sealed pour
# --------------------------------------------------------------------------
def impulse_target(led: dict, spec: dict):
    """flock_field's PhiField picks the lure cell: goal = the seat list's top
    pick for the day's heaviest shape, invariants = the weak coordinates
    (penalty bubbles). Returns (row, col) of the phi minimum."""
    from mag import flock_field as ff
    models, shapes = spec["models"], spec["shapes"]
    ridx = {m: i for i, m in enumerate(models)}
    counts: dict[str, int] = {}
    for _ts, _m, s, _v in led["rows"]:
        counts[s] = counts.get(s, 0) + 1
    seat = seat_list(led)
    if not seat or not counts:
        return None
    heavy = max(counts, key=lambda s: (counts[s], s))
    pick = next((p for p in seat if p["shape"] == heavy), None)
    if pick is None:
        return None
    gy, gx = ridx[pick["model"]], shapes.index(heavy)
    weak = weak_set(led)
    invariants = [cell_center(models.index(m), shapes.index(s))
                  for m, s in weak if m in ridx and s in shapes]
    field = ff.define_distance_field(cell_center(gy, gx), invariants=invariants,
                                     weights=[6.0] * len(invariants), dim=2)
    best, best_phi = None, None
    for r in range(len(models)):
        for c in range(len(shapes)):
            p = field.value(cell_center(r, c))
            if best_phi is None or p < best_phi:
                best, best_phi = (r, c), p
    return best


def mint_sealed_pour(seal_home: Path, coord: tuple[int, int]):
    """steer_seal leg (offline, $0): keyfile OUTSIDE ROOT (the X5 precedent),
    sealed envelope, admit through the single gate. Key and nonce are
    DERIVED from the payload (sha256) so the double-run determinism check
    holds byte-identical; a production ingress would use os.urandom."""
    from mag import steer_seal as ss
    seal_home.mkdir(parents=True, exist_ok=True)
    keyfile = seal_home / "steer_seal_key"
    # the seen-store is per-run temp state (outside ROOT): the nonce is
    # deterministic for the double-run digest law, so a shared store would
    # make run 2 fail closed as "nonce reuse" -- which is exactly what
    # happened on the first double-run attempt (the replay guard works).
    import tempfile
    seen = Path(tempfile.mkdtemp(prefix="field2_seen_"))
    from mag import water_swarm
    payload = (water_swarm.water_doctrine()
               + f"\nPOUR: place food {IMPULSE_FOOD:.0f} units at board cell"
                 f" ({coord[0]},{coord[1]}) and let the school graze. Lure,"
                 " never chase (LM9). No mid-task redirects.")
    key = hashlib.sha256(b"field2-seal-key-v1:" + payload.encode()).digest()
    nonce = hashlib.sha256(b"field2-seal-nonce-v1:" + payload.encode()).hexdigest()[:32]
    ss.write_keyfile(keyfile, key, force=True)
    env = ss.seal(payload, key=key, nonce=nonce, timestamp=20261001)
    admitted = ss.admit_text(json.dumps(env), mode="enforce",
                             keyfile=keyfile, seen_dir=seen, now=20261001)
    receipt = {"authority": admitted.authority, "event": admitted.event,
               "key_id": env["key_id"], "nonce": env["nonce"],
               "envelope_sha256": hashlib.sha256(
                   json.dumps(env, sort_keys=True).encode()).hexdigest()[:16],
               "payload_head": payload[:60]}
    if admitted.authority != "operator-seal":
        return None, receipt          # fail closed: no pour without the seal
    return env, receipt


# --------------------------------------------------------------------------
# 4. LIST arm (the control, exactly as shipped)
# --------------------------------------------------------------------------
def run_list_arm(led: dict) -> dict:
    wl = workload_from_ledger(DB_PATH)
    spec = spec_from_workload(
        wl,
        classes=[{"name": "critical", "elev": 60, "sill": 1},
                 {"name": "burstable", "elev": 40, "sill": 2}],
        quota=2, burst={"cap": 2, "crest": 2}, budget=1, ticks=MAX_TICKS)
    res = k8s_simulate(spec)
    weak = weak_set(led)

    arrived_cum = spec["waste_seed"]
    served_cum = 0
    t80 = None
    t80_literal = None
    arr_by_tick: dict[int, int] = {}
    for a in spec["arrivals"]:
        arr_by_tick[int(a["tick"])] = arr_by_tick.get(int(a["tick"]), 0) + int(a["units"])
    for row in res["trace"]:
        arrived_cum += arr_by_tick.get(row["tick"], 0)
        served_cum += row["served"]
        if t80 is None and served_cum * 5 >= 4 * res["total"]:
            t80 = row["tick"]
        if t80_literal is None and arrived_cum and (
                served_cum + row["waste"]) >= 0.8 * arrived_cum:
            t80_literal = row["tick"]
    # wasted dispatches: the driver's own sends at weak coordinates (D4)
    wasted = sum(1 for _ts, m, s, _v in led["rows"] if (m, s) in weak)
    # per-shape dispatch tallies (its decision record: where it sent work)
    tally: dict[tuple[str, str], int] = {}
    for _ts, m, s, _v in led["rows"]:
        tally[(m, s)] = tally.get((m, s), 0) + 1
    return {"arm": "list", "ticks_used": res["ticks_used"], "t80": t80,
            "t80_literal": t80_literal,
            "served": res["served"], "wasted_dispatches": wasted,
            "service_events": res["served"],
            "tally": {f"{m}|{s}": n for (m, s), n in sorted(tally.items())},
            "ticks_arrivals": spec["workload_meta"]["ticks"],
            "waste_final": res["waste"], "mux_final": res["mux"]}


# --------------------------------------------------------------------------
# 5. comparison
# --------------------------------------------------------------------------
def agreement(arm: dict, seat: list[dict]) -> tuple[float, list[dict]]:
    """Mechanical decision-agreement: per shape, does the arm's top coordinate
    match the seat's blind pick?"""
    top: dict[str, tuple[str, int]] = {}
    for key, n in arm["tally"].items():
        m, s = key.split("|", 1)
        if s not in top or n > top[s][1]:
            top[s] = (m, n)
    rows = []
    hit = 0
    for p in seat:
        got = top.get(p["shape"], ("-", 0))[0]
        ok = got == p["model"]
        hit += ok
        rows.append({"shape": p["shape"], "seat": p["model"], "arm_top": got,
                     "agree": ok})
    return hit / len(seat), rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="field_experiment")
    ap.add_argument("--db", default=str(DB_PATH))
    ap.add_argument("--seal-home", default=str(Path.home() / ".mag_field2"))
    ap.add_argument("--setup-only", action="store_true")
    a = ap.parse_args(argv)

    led = read_ledger(Path(a.db))
    shapes_seen = list(dict.fromkeys(s for _ts, _m, s, _v in led["rows"]))
    column_order = column_order_from_scheduler(shapes_seen)
    spec = seed_terrain(led, column_order)
    seat = seat_list(led)
    GARDEN.mkdir(parents=True, exist_ok=True)
    BOARD_SPEC_PATH.write_text(json.dumps(spec, indent=1), encoding="utf-8")

    if a.setup_only:
        print(json.dumps({"schema": SCHEMA, "board": spec["cell"],
                          "seat_list": seat}, indent=1))
        return 0

    field = run_field_arm(led, spec, Path(a.seal_home))
    listarm = run_list_arm(led)
    agr_f, rows_f = agreement(field, seat)
    agr_l, rows_l = agreement(listarm, seat)

    report = {"schema": SCHEMA,
              "workload": {"rows": len(led["rows"]),
                           "verdict0": sum(1 for r in led["rows"] if r[3] == 0),
                           "arrival_ticks": field["ticks_arrivals"],
                           "weak_pairs": len(weak_set(led))},
              "seat_list": seat,
              "field": {k: v for k, v in field.items() if k != "trace"},
              "list": {k: v for k, v in listarm.items() if k != "trace"},
              "agreement": {"field": round(agr_f, 4), "list": round(agr_l, 4),
                            "rows_field": rows_f, "rows_list": rows_l}}
    dump = json.dumps(report, sort_keys=True)
    report["digest"] = hashlib.sha256(dump.encode()).hexdigest()[:16]
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
