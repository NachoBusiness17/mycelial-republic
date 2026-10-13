"""mountain_units — DFHack-style `units` for the Mountain fish school (LM4).

Unit model, ported with per-line citations: brain = fish_brain.gd decide()
(pure policy; ONE motion row {verb: idle|flee|pursue|carry|dance,
intensity_q8: u8, dir: pool} per fish per tick); rig = game.gd
_step_brain/_apply_motion_row (steering, fatigue, drag, catch, move at 60Hz;
water every 0.5s); board = server/world.build_mountain_graph (the EXACT
Mountain board on the estate's own organ, mag.water_graph — fidelity over
re-implementation); gate = protocol_table.MOTION_DISPATCH.ask (every row is
gated through the real table before it applies). NOT ported: the pheromone
trail (flock.gd:96-108) — the brain path writes it but nothing on that path
reads it (only the flock fallback does); running it here would be orphan
behavior. Named, not silently skipped.
Player: player.gd follows the mouse (human input); this tool scripts it
deterministically — `hunt` (cursor chases the nearest alive fish at
CURSOR_SPEED: exercises flee->fatigue->carry->catch) or `still` (parked at
the board corner, the no-threat snapshot fish_brain.gd:84-85 models). An
illegal row is a LOUD typed failure, never a silent flock fallback.
Determinism (W1 purity): spawn jitter is the only RNG, riding
random.Random(seed) (default 20260929, game.gd:180's own seed); same (ticks,
seed, player) in, same bytes out. Exit 0 ok · 2 typed error.
Usage: units [--ticks 600] [--seed S] [--player hunt|still] [--json] ·
unit <id> [same flags] [--trace] · schema mountain_units.v1, $0
Tests: tests/test_mountain_units.py · receipt: watch/inbox/last_mile_20260930/LM4_UNITS.md
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol_table import MOTION_DISPATCH  # noqa: E402
from server.world import build_mountain_graph  # noqa: E402

SCHEMA = "mountain_units.v1"
VERBS = ("idle", "flee", "pursue", "carry", "dance")
FRAME_DT = 1.0 / 60.0   # game.gd _process cadence (60Hz)
FRAMES_PER_TICK = 30    # water Timer every TICK_SECONDS 0.5 (game.gd:47)
POP_CAP = 45            # flock.gd:22
SPAWN_COUNT = 12        # game.gd:181
DEFAULT_SEED = 20260929  # game.gd:180 rng.seed
BOARD = (16.0, 16.0, 1136.0, 632.0)  # player.gd:6 Rect2(16,16,1120,616) x0y0x1y1
CELL_PX = 20.0          # this tool's map-tile law (not an estate port)
CURSOR_SPEED = 220.0    # this tool's scripted hunter pace
# R4 2026-09-30 (Q15/V2ASK3): trued up to game_constants.gd FLEE_RADIUS 20.
# This rode fish_brain.gd's stale 14 mirror after Z14's 14->20 retune
# (V6_FISH_FLEE.md's named handoff); R7 aliased the .gd consumers, this
# true-up closes the Python twin. Pinned by tests/test_game_constants.py.
FLEE_RADIUS, SCHOOL_RADIUS, TRAIL_RADIUS = 20.0, 20.0, 38.0
TIRED, POOL_PREF_DIST = 0.7, 30.0  # game.gd:58,68-75 Z7 rig constants:
BRAIN_FLEE_PUSH, BRAIN_WIGGLE = 6.0, 0.05
BRAIN_FATIGUE_DECAY, BRAIN_DRAG, BRAIN_COAST_TIME = 0.4, 0.985, 0.8
BRAIN_CATCH_RADIUS, BRAIN_TIRED, POOL_PULL = 3.5, 0.7, 22.0
POOL_LAYOUT: dict[str, tuple[float, int, int]] = {  # game.gd:90-97 verbatim
    "spring": (130.0, 10, 6), "terrace": (430.0, 6, 0), "gate1": (280.0, 5, 0),
    "hollow": (620.0, 3, 2), "waste": (790.0, 0, 0), "crown": (1010.0, 14, 0)}

Vec = tuple[float, float]

class UnitsError(ValueError):
    """Typed, fail-closed inspector error (a bad ask or an illegal row)."""

def _sub(a: Vec, b: Vec) -> Vec: return (a[0] - b[0], a[1] - b[1])
def _add(a: Vec, b: Vec) -> Vec: return (a[0] + b[0], a[1] + b[1])
def _scale(a: Vec, k: float) -> Vec: return (a[0] * k, a[1] * k)
def dist(a: Vec, b: Vec) -> float: return math.hypot(a[0] - b[0], a[1] - b[1])
def _norm(a: Vec) -> Vec:  # Godot normalized(): a zero vector stays zero
    n = math.hypot(*a)
    return (0.0, 0.0) if n == 0.0 else (a[0] / n, a[1] / n)


def q8(x: float) -> int:
    """fish_brain.gd _q8 — Godot round() is half-away-from-zero, so floor."""
    return int(math.floor(min(max(x, 0.0), 1.0) * 255.0 + 0.5))


def _pool_by(pos: Vec, pools: dict[str, Vec], far: bool) -> str:
    """fish_brain.gd _nearest/_farthest_pool: sorted names, strict compare."""
    best_name, best_d = "", (-1.0 if far else float("inf"))
    for p in sorted(pools):
        d = dist(pos, pools[p])
        if (d > best_d) if far else (d < best_d):
            best_name, best_d = p, d
    return best_name


def decide(fish_id: int, tick: int, snapshot: dict[str, Any]) -> dict[str, Any]:
    """fish_brain.gd decide() verbatim (threat -> tire -> pool pull -> wiggle).
    PURE: no RNG, no clock, no snapshot mutation — same inputs, same row."""
    fish = snapshot.get("fish", [])
    pools = snapshot.get("pools", {})
    wettest = snapshot.get("wettest", "")
    f = fish[fish_id] if 0 <= fish_id < len(fish) else {}
    if not pools or not bool(f.get("alive", False)):
        return {"verb": "idle", "intensity_q8": 0, "dir": wettest}
    pos = f["pos"]
    fatigue = float(f.get("fatigue", 0.0))
    player = snapshot.get("player_pos")
    if player is None:  # fish_brain.gd:85 default: no threat in reach
        player = (pos[0] + FLEE_RADIUS * 4.0, pos[1])
    threat_d = dist(pos, player)
    if threat_d < FLEE_RADIUS and fatigue < 1.0:  # :91 flee
        return {"verb": "flee", "intensity_q8": q8(1.0 - threat_d / FLEE_RADIUS),
                "dir": _pool_by(player, pools, far=True)}
    if fatigue >= TIRED:  # :99 the tired window: drag owns the fish
        # R4 2026-09-30: dry-board guard, latent until the Q15 true-up
        # (FLEE_RADIUS 14 -> 20): at hunt-seed 11 tick 240 every pool but
        # waste is empty, _wettest_pool returns "", and the verbatim
        # fish_brain carry row {dir: ""} fails the real MOTION_DISPATCH
        # gate with UNKNOWN_TARGET. The game's rig degrades gracefully
        # (game.gd falls back to the old flock lane when a row fails the
        # gate), but this tool is LOUD by design — so the mirror falls back
        # to the nearest pool, the same dir the idle/dance rows use.
        # fish_brain.gd's carry branch still carries the unguarded wettest
        # (harmless in the rig, named here as its lane's debt).
        return {"verb": "carry", "intensity_q8": q8(fatigue),
                "dir": wettest if wettest in pools
                else _pool_by(pos, pools, far=False)}
    if wettest != "" and wettest in pools:  # :105 fresh fish steers to water
        if (d_home := dist(pos, pools[wettest])) > POOL_PREF_DIST:
            return {"verb": "pursue", "intensity_q8": q8(d_home / TRAIL_RADIUS),
                    "dir": wettest}
    # schoolmate identity is the INDEX (the X9 law, fish_brain.gd:117)
    schoolmates = sum(
        1 for i, o in enumerate(fish)
        if i != fish_id and bool(o.get("alive", False))
        and dist(pos, o["pos"]) < SCHOOL_RADIUS)
    if schoolmates > 0:  # :127 the wiggle is the swim
        wiggle = (math.sin(float(tick) * 0.7 + pos[0] * 0.05) + 1.0) / 2.0
        return {"verb": "dance", "intensity_q8": q8(wiggle),
                "dir": _pool_by(pos, pools, far=False)}
    return {"verb": "idle", "intensity_q8": q8(1.0 - fatigue),  # :131 rest
            "dir": _pool_by(pos, pools, far=False)}


class FishSchool:
    """flock.gd storage port: fish = [{pos, vel, fatigue, alive}]; POP_CAP
    law (add_fish returns -1 at cap); ids are indexes, order-stable."""

    def __init__(self) -> None:
        self.fish: list[dict[str, Any]] = []

    def add_fish(self, pos: Vec) -> int:
        if len(self.fish) >= POP_CAP:
            return -1
        self.fish.append({"pos": pos, "vel": (0.0, 0.0), "fatigue": 0.0,
                          "alive": True})
        return len(self.fish) - 1


class MountainUnits:
    """game.gd's Z7 brain lane ported: one decide() row per alive fish per
    frame, gated through MOTION_DISPATCH, applied as steering, with per-fish
    DFHack bookkeeping (state, age in state, target, motion-row history)."""

    def __init__(self, seed: int = DEFAULT_SEED,
                 player_mode: str = "hunt") -> None:
        if player_mode not in ("hunt", "still"):
            raise UnitsError(f"unknown player mode {player_mode!r}")
        self.seed, self.player_mode = int(seed), player_mode
        self.graph = build_mountain_graph()
        self.pools: dict[str, Vec] = {  # game.gd _elev_y 600-elev*36
            name: (spec[0], 600.0 - spec[1] * 36.0)
            for name, spec in POOL_LAYOUT.items()}
        self.school = FishSchool()
        rng, base = random.Random(self.seed), self.pools["spring"]
        for _i in range(SPAWN_COUNT):  # game.gd:179-184 spawn law
            self.school.add_fish((base[0] + rng.uniform(-60.0, 60.0),
                                  base[1] + rng.uniform(-50.0, 50.0)))
        self.player: Vec = (
            (BOARD[0], BOARD[1]) if player_mode == "still"
            else ((BOARD[0] + BOARD[2]) / 2.0, (BOARD[1] + BOARD[3]) / 2.0))
        self.sim_time, self.frame = 0.0, 0
        self.states = [{"state": "idle", "since": 0, "transitions": 0,
                        "rows": [], "killed_at": None}
                       for _ in self.school.fish]

    def _fid(self, fid: int) -> None:
        if not 0 <= fid < len(self.school.fish):
            raise UnitsError(f"unknown unit id {fid}")

    def wettest(self) -> str:
        """game.gd _wettest_pool: pools order, skip waste, strict >."""
        best, best_v = "", 0
        for name in self.pools:
            if name != "waste" and self.graph.nodes[name].volume > best_v:
                best, best_v = name, self.graph.nodes[name].volume
        return best

    def cell(self, pos: Vec) -> tuple[int, int]:  # 20px tile at board corner
        return (int((pos[0] - BOARD[0]) // CELL_PX),
                int((pos[1] - BOARD[1]) // CELL_PX))

    def unit_row(self, fid: int) -> dict[str, Any]:
        self._fid(fid)
        f, st = self.school.fish[fid], self.states[fid]
        last = st["rows"][-1] if st["rows"] else None
        age = self.frame - st["since"]
        row: dict[str, Any] = {
            "id": fid, "alive": bool(f["alive"]), "state": st["state"],
            "intensity_q8": (last or {}).get("intensity_q8", 0),
            "target": (last or {}).get("dir", ""),
            "pos": [round(f["pos"][0], 1), round(f["pos"][1], 1)],
            "cell": list(self.cell(f["pos"])),
            "age_in_state_frames": age, "age_in_state_s": round(age * FRAME_DT, 2),
            "transitions": st["transitions"]}
        if not f["alive"]:
            row["killed_at"] = st["killed_at"]
        return row

    def trace(self, fid: int) -> list[dict[str, Any]]:
        """One fish's full event history: every motion row it emitted, in
        tick order, plus the caught event that ended it."""
        self._fid(fid)
        return list(self.states[fid]["rows"])

    def summary(self) -> dict[str, Any]:
        pop, dead = {v: 0 for v in VERBS}, 0
        for i, f in enumerate(self.school.fish):
            if f["alive"]:
                pop[self.states[i]["state"]] += 1
            else:
                dead += 1
        return {"tick": self.frame, "spawned": len(self.school.fish),
                "alive": len(self.school.fish) - dead, "dead": dead, "population": pop,
                "transitions": sum(s["transitions"] for s in self.states),
                "pop_cap": POP_CAP,
                "headroom": POP_CAP - (len(self.school.fish) - dead), "wettest": self.wettest()}

    def dump(self) -> dict[str, Any]:
        return {"schema": SCHEMA, "seed": self.seed, "ticks_run": self.frame,
                "player_mode": self.player_mode, "summary": self.summary(),
                "units": [self.unit_row(i)
                          for i in range(len(self.school.fish))]}

    def _player_step(self, dt: float) -> None:
        if self.player_mode == "still":
            return  # parked at the corner, outside every FLEE_RADIUS
        alive = [(i, f) for i, f in enumerate(self.school.fish) if f["alive"]]
        target = (min(alive, key=lambda p: (dist(self.player, p[1]["pos"]),
                                            p[0]))[1]["pos"] if alive else
                  ((BOARD[0] + BOARD[2]) / 2.0, (BOARD[1] + BOARD[3]) / 2.0))
        d = _sub(target, self.player)  # chase nearest alive fish, ties by id
        if (dl := math.hypot(*d)) > 1e-9:
            self.player = _add(self.player, _scale(_norm(d),
                                                   min(CURSOR_SPEED * dt, dl)))
        self.player = (min(max(self.player[0], BOARD[0]), BOARD[2]),
                       min(max(self.player[1], BOARD[1]), BOARD[3]))

    def _apply_row(self, fid: int, row: dict[str, Any]) -> bool:
        """game.gd _apply_motion_row port; True when caught this frame
        (flock.gd:77-79: the player's verb on a tired fish)."""
        f = self.school.fish[fid]
        inten = row["intensity_q8"] / 255.0  # the X9 formula's urgency term
        pos, vel, fatigue = f["pos"], f["vel"], f["fatigue"]
        verb = row["verb"]
        rest = max(fatigue - FRAME_DT * BRAIN_FATIGUE_DECAY / BRAIN_COAST_TIME, 0.0)
        if verb == "flee":  # away from the player, toward the far pool
            vel = _add(vel, _scale(_norm(_add(
                _norm(_sub(pos, self.player)),
                _norm(_sub(self.pools[row["dir"]], pos)))),
                BRAIN_FLEE_PUSH * inten * FRAME_DT))
            fatigue = min(fatigue + FRAME_DT / BRAIN_COAST_TIME, 1.0)
        elif verb in ("pursue", "carry"):  # steer toward pools[dir]
            d = _sub(self.pools[row["dir"]], pos)
            if math.hypot(*d) > 0.0:
                vel = _add(vel, _scale(_norm(d), POOL_PULL * inten * FRAME_DT))
            fatigue = rest
        elif verb == "dance":  # flock.gd:74 wiggle, intensity-modulated
            wig = (math.sin(self.sim_time * 7.0 + pos[0] * 0.05),
                   math.cos(self.sim_time * 7.0 + pos[1] * 0.05))
            vel = _add(vel, _scale(wig, BRAIN_WIGGLE * inten * FRAME_DT))
            fatigue = rest
        else:  # idle: rest depth damps the coast
            vel = _scale(vel, (1.0 - 0.05 * inten) ** (FRAME_DT * 60.0))
            fatigue = rest
        vel = _scale(vel, BRAIN_DRAG ** (FRAME_DT * 60.0))  # drag
        f["fatigue"], f["vel"] = fatigue, vel
        if dist(pos, self.player) < BRAIN_CATCH_RADIUS and fatigue > BRAIN_TIRED:
            f["alive"] = False
            return True
        f["pos"] = _add(pos, _scale(vel, FRAME_DT))  # the move
        return False

    def step_frame(self) -> None:
        """One 60Hz frame of the Z7 lane (game.gd _step_brain): player moves,
        water may tick, ALL rows decided against ONE snapshot, gated, applied."""
        self.frame += 1
        self.sim_time += FRAME_DT
        tick = int(self.sim_time * 60.0)
        self._player_step(FRAME_DT)
        if self.frame % FRAMES_PER_TICK == 0:
            self.graph.tick()
        snapshot = {"fish": self.school.fish, "player_pos": self.player,
                    "pools": self.pools, "wettest": self.wettest()}
        rows: list[tuple[int, dict[str, Any]]] = []
        for fid, f in enumerate(self.school.fish):
            if not f["alive"]:
                continue
            row = decide(fid, tick, snapshot)
            ask = MOTION_DISPATCH.ask(row["verb"], "AUTHED",
                                      {"intensity_q8": row["intensity_q8"],
                                       "dir": row["dir"]},
                                      frozenset(self.pools))
            if not ask["ok"]:
                raise UnitsError(f"fish {fid} emitted an illegal motion row "
                                 f"at tick {tick}: {row} -> {ask['reason']}")
            rows.append((fid, row))
        for fid, row in rows:
            st = self.states[fid]
            if st["state"] != row["verb"]:
                st["transitions"] += 1
                st["state"], st["since"] = row["verb"], tick
            caught = self._apply_row(fid, row)
            f = self.school.fish[fid]
            out = {"tick": tick, "fatigue": round(f["fatigue"], 4),
                   "pos": [round(f["pos"][0], 1), round(f["pos"][1], 1)]}
            if caught:
                st["killed_at"] = tick
                st["state"], st["since"] = "dead", tick
                st["rows"].append({**out, "event": "caught"})
            else:
                st["rows"].append({**out, "verb": row["verb"],
                                   "intensity_q8": row["intensity_q8"],
                                   "dir": row["dir"]})

    def run(self, ticks: int) -> None:
        if not 1 <= ticks <= 100_000:
            raise UnitsError(f"ticks must be 1..100000, got {ticks}")
        for _ in range(ticks): self.step_frame()


def _print_units(sim: MountainUnits) -> None:
    s = sim.summary()
    print(f"MOUNTAIN UNITS - tick {s['tick']} - seed {sim.seed} - "
          f"player {sim.player_mode} - wettest {s['wettest'] or '(dry)'}")
    print(f"{'ID':>3}  {'STATE':<6} {'INT':>3}  {'TARGET':<7} "
          f"{'CELL':<6} {'POS':<15} AGE         TRN")
    for u in sim.dump()["units"]:
        pos = f"({u['pos'][0]:.1f},{u['pos'][1]:.1f})"
        tail = f" caught@{u['killed_at']}" if not u["alive"] else ""
        print(f"{u['id']:>3}  {u['state']:<6} {u['intensity_q8']:>3}  "
              f"{u['target'] or '-':<7} {u['cell'][0]}/{u['cell'][1]:<4} "
              f"{pos:<15} {u['age_in_state_frames']}f {u['age_in_state_s']}s"
              f"  {u['transitions']}{tail}")
    print("population: " + "  ".join(f"{v} {s['population'][v]}" for v in VERBS)
          + f"  dead {s['dead']}  (spawned {s['spawned']})")
    print(f"transitions: {s['transitions']} · pop_cap: {s['alive']} alive / "
          f"{s['pop_cap']} (headroom {s['headroom']})")


def _print_trace(sim: MountainUnits, fid: int) -> None:
    print(f"UNIT {fid} - tick {sim.frame} - seed {sim.seed} - "
          f"player {sim.player_mode}")
    print(f"  {json.dumps(sim.unit_row(fid), sort_keys=True)}")
    trace = sim.trace(fid)
    print(f"  trace: {len(trace)} rows")
    for r in trace:
        if "event" in r:
            print(f"    t{r['tick']:>5}  {r['event']} (fatigue "
                  f"{r['fatigue']}, pos {tuple(r['pos'])})")
        else:
            print(f"    t{r['tick']:>5}  {r['verb']:<6} q8={r['intensity_q8']:>3}"
                  f" dir={r['dir']:<7} fatigue={r['fatigue']:.3f}"
                  f" pos=({r['pos'][0]},{r['pos'][1]})")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="mountain_units")
    sub = ap.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("units", help="run the sim, dump every fish")
    ut = sub.add_parser("unit", help="one fish's card / event history")
    for p in (up, ut):
        p.add_argument("--ticks", type=int, default=600,
                       help="60Hz frames (default 600 = 10s)")
        p.add_argument("--seed", type=int, default=DEFAULT_SEED)
        p.add_argument("--player", default="hunt", choices=("hunt", "still"))
        p.add_argument("--json", action="store_true")
    ut.add_argument("id", type=int, help="fish id (0..spawned-1)")
    ut.add_argument("--trace", action="store_true",
                    help="print the fish's full motion-row history")
    a = ap.parse_args(argv)
    try:
        sim = MountainUnits(seed=a.seed, player_mode=a.player)
        sim.run(a.ticks)
        if a.cmd == "units":
            if a.json:
                print(json.dumps(sim.dump(), sort_keys=True))
            else:
                _print_units(sim)
        elif a.json:
            print(json.dumps({"unit": sim.unit_row(a.id),
                              "trace": sim.trace(a.id)}, sort_keys=True))
        elif a.trace:
            _print_trace(sim, a.id)
        else:
            print(f"UNIT {a.id}: "
                  + json.dumps(sim.unit_row(a.id), sort_keys=True))
    except UnitsError as exc:
        print(f"mountain_units: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
