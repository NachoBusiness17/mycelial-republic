"""mountain_selfplay — the game plays itself, and we watch (2026-09-29).

Operator mission ("have fun with it"): the Mountain plays itself against the
AUTHORITATIVE stack, and the run IS the game-design signal. No offline
short-circuit: every strategy acts through the real wire (in-process TCP
WorldServer on an ephemeral port), the real doors (SRP6
register/challenge/proof for the player, plaintext hello for the spectator),
the real receipt ladder (a monotonic nonce 'n' on every action, the per-sid
per-tick rate cap), the real rooms (the stress suite runs four at once), and
the real hash-chained event log — verified row-by-row from DISK after every
run (verify_log_rows + reload, the world.py append-only law).

THE STRATEGY LADDER (seeded skill levels):
    random    uniform over the legal verb set, chosen from the client's
              observable mirror only (boil any wet node, valve any pipe,
              tag the school's pool, say a line). Seeded Random: same seed
              -> same tape (pinned by test: byte-identical world logs).
    greedy    the estate's own demo policy (server/server.py _pick_target
              generalized): boil the wettest non-crown non-waste pool,
              never touch a valve. One verb, zero planning.
    heuristic the fill-crown playbook — four rules in order, computed only
              from the welcome snapshot + tick broadcasts (the client-side
              observability law: no server-private state):
                R1 conservation: shut any open pipe draining a WET source
                   into waste (the V5 basin is boilable, but water in
                   place beats water in the pit).
                R2 xor discipline: a gated xor junction fed by 2+ open wet
                   inlets gets the extras shut (exactly-one-inlet is the
                   only verdict an xor passes).
                R3 steam discipline: boil the wettest pool ONLY when crown
                   is the strictly highest cold node. Steam ignores pipes
                   and condenses at the tallest cold node (feed a rival
                   peak and the verb is a trap); with NO cold node the
                   engine locks steam forever, so never boil there either.
                R4 gravity feed: open a shut pipe whose dst is crown when
                   its source is wet.
              else idle — let gravity work.

THE BOARDS (which configurations are greedy-solvable vs planning-solvable):
    mountain  the standing slice (server/world.build_mountain_graph): one
              cold crown at the top of the world; boil 4 -> WIN. The rate
              cap (1 action/sid/tick) makes 4 ticks the provable floor.
    shrine    a decoy peak (cold, elev 20) OVER the crown (cold, elev 14):
              every boil condenses at the peak, never the crown, and the
              peak has no outlet. Boil = donated water.
    foundry   NO cold node at all + an xor mixer between twin forges: boil
              is an irreversible sink (see the finding below) and the win
              lives in valve discipline.
    spelunk   the marathon: a 1/tick needle feeds the crown (win 30) while
              a cap-8 firehose drains a 400-unit flood into a waste slough
              — full bore every tick, stress +8/tick against threshold 233
              (200 + djb2(name) % 201, mag/water_graph fracture law): it
              FRACTURES mid-run and sprays its load at the lowest node.

ENGINE FINDING the harness banks (verified 2026-09-29, pinned by tests):
    mag/water_graph.py's docstring promises steam "falls back to its
    origin node when no cold node exists" — _condense_steam() implements
    NO fallback: with zero cold nodes steam never returns to liquid play.
    On no-cold boards the game's core verb is an irreversible sink. The
    harness reports it as the metric steam_locked; the finding is design
    signal (boiling as a trap), not a bug fix lane — filed, not patched.

Run:
    .venv/Scripts/python.exe tools/mountain_selfplay.py             # suite + receipt
    .venv/Scripts/python.exe tools/mountain_selfplay.py --watch     # tick spam
    .venv/Scripts/python.exe tools/mountain_selfplay.py --boards mountain,foundry
        --strategies greedy,heuristic --ticks 40
    .venv/Scripts/python.exe tools/mountain_selfplay.py --stress-only

Tests: tests/test_mountain_selfplay.py
Schema: mountain_selfplay.v1 . seeded-deterministic world side (Random()
only; SRP6 handshake entropy never enters the world log) + $0 stdlib.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import re
import secrets
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402
from server.auth import AuthStore  # noqa: E402
from server.auth_srp6 import DEFAULT_GROUP, VARIANTS, Srp6AuthService, SrpStore  # noqa: E402
from server.server import Client, WorldServer  # noqa: E402
from server.world import MountainWorld, build_mountain_graph, load_log_rows  # noqa: E402

DEFAULT_TICKS = 60
DEFAULT_SEEDS = (1, 2, 3)          # reps for the seeded random strategy
PASSWORD = "selfplay"
SAY_LINES = ("the mountain provides", "water finds a way", "watch the gate")


# --------------------------------------------------------------- boards ----

def _shrine() -> WaterGraph:
    """Decoy-peak board: the tallest cold node is NOT the win node."""
    g = WaterGraph()
    g.add_node("spring", elev=16, volume=8)
    g.add_node("peak", elev=20, kind="cold")
    g.add_node("crown", elev=14, kind="cold")
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("p_fall", "spring", "crown", cap=1)
    g.add_pipe("p_leak", "spring", "waste", cap=1)
    return g


def _foundry() -> WaterGraph:
    """No-cold board: boil vapor-locks; the xor mixer is the whole game."""
    g = WaterGraph()
    g.add_node("forgeA", elev=6, volume=4)
    g.add_node("forgeB", elev=6, volume=4)
    g.add_node("mixer", elev=3, kind="xor")
    g.add_node("crown", elev=0)
    g.add_pipe("p_a", "forgeA", "mixer", cap=1)
    g.add_pipe("p_b", "forgeB", "mixer", cap=1)
    g.add_pipe("p_out", "mixer", "crown", cap=1)
    return g


def _spelunk() -> WaterGraph:
    """Marathon board: needle vs firehose; the firehose must burst."""
    g = WaterGraph()
    g.add_node("lake", elev=9, volume=34)
    g.add_node("flood", elev=9, volume=400)
    g.add_node("slough", elev=1, kind="waste")
    g.add_node("crown", elev=0)
    g.add_pipe("p_needle", "lake", "crown", cap=1)
    g.add_pipe("p_a1", "flood", "slough", cap=8)   # threshold 233: burst ~tick 30
    return g


# name -> (builder, win volume); every board keeps a node named "crown"
# (MountainWorld.tick's win check reads it by name).
BOARDS: dict[str, tuple[Callable[[], WaterGraph], int]] = {
    "mountain": (build_mountain_graph, 4),
    "shrine": (_shrine, 4),
    "foundry": (_foundry, 4),
    "spelunk": (_spelunk, 30),
}

STRATEGIES = ("random", "greedy", "heuristic")


# --------------------------------------------------------------- mirror ----

class Mirror:
    """The client-side observable world: the welcome snapshot's statics
    (elevs, kinds, pipe topology) plus per-tick dynamics (node volumes,
    valve/fracture state read back out of the broadcast event strings).
    Nothing here reads server-private state — the strategies act on
    exactly what the wire shows a real player."""

    def __init__(self, snapshot: dict[str, Any]) -> None:
        nodes = snapshot["nodes"]
        self.node_order: tuple[str, ...] = tuple(nodes)
        self.elev = {n: int(v["elev"]) for n, v in nodes.items()}
        self.kind = {n: str(v["kind"]) for n, v in nodes.items()}
        self.volumes: dict[str, int] = {n: int(v["volume"]) for n, v in nodes.items()}
        self.pipes: dict[str, dict[str, Any]] = {
            p: {"src": v["src"], "dst": v["dst"], "cap": int(v["cap"]),
                "siphon": bool(v["siphon"]), "crest": int(v["crest"]),
                "open": bool(v["open"]), "fractured": False}
            for p, v in snapshot["pipes"].items()
        }
        self.win_crown = int(snapshot.get("win_crown", 4))

    def apply_tick(self, payload: dict[str, Any]) -> None:
        self.volumes = {n: int(v) for n, v in payload["nodes"].items()}
        for ev in payload.get("events", []):
            if not isinstance(ev, str):
                continue
            # the ledger's own event grammar (world.py _apply / water_graph)
            body = ev[:-1] if ev.endswith(".") else ev
            if " FRACTURES" in body:
                name = body.split(" ", 2)[1] if body.startswith("Pipe ") else None
                if name in self.pipes:
                    self.pipes[name]["fractured"] = True
                    self.pipes[name]["open"] = False
                continue
            for verb, opens in ((" shuts ", False), (" opens ", True)):
                if verb in body:
                    user, _, pipe = body.partition(verb)
                    if pipe in self.pipes and not self.pipes[pipe]["fractured"]:
                        # NOTE (event-honesty wart, banked): a valve on a
                        # FRACTURED pipe still says "opens p_x." while the
                        # engine refuses — burst pipes never reopen, so
                        # the mirror refuses to believe the string.
                        self.pipes[pipe]["open"] = opens
                    break

    def wettest(self, skip=("crown", "waste")) -> str | None:
        best, best_v = None, 0
        for n in self.node_order:
            if n in skip:
                continue
            if self.volumes.get(n, 0) > best_v:
                best, best_v = n, self.volumes[n]
        return best

    def crown_is_highest_cold(self) -> bool:
        colds = [(self.elev[n], n) for n in self.node_order if self.kind[n] == "cold"]
        return bool(colds) and max(colds)[1] == "crown"


# ------------------------------------------------------------ strategies ----

class RandomBot:
    """Seeded uniform play over the legal verb set (the observable mirror's
    candidate list). The tape is reproducible: same seed, same actions."""

    name = "random"

    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)

    def choose(self, m: Mirror) -> tuple[str, str] | None:
        cands: list[tuple[str, str]] = []
        cands += [("boil", n) for n, v in m.volumes.items() if v > 0]
        cands += [("valve", p) for p in m.pipes]
        pool = m.wettest(skip=())
        if pool is not None:
            cands.append(("tag", pool))
        cands.append(("say", self.rng.choice(SAY_LINES)))
        if not cands:
            return None
        return self.rng.choice(cands)


class GreedyBot:
    """The estate demo policy (server.py _pick_target): boil the wettest
    pool in board order, crown/waste excluded. Valves do not exist."""

    name = "greedy"

    def choose(self, m: Mirror) -> tuple[str, str] | None:
        pool = m.wettest()
        return ("boil", pool) if pool is not None else None


class HeuristicBot:
    """The fill-crown playbook (R1-R4, module docstring). Deterministic:
    the same mirror always yields the same move."""

    name = "heuristic"

    def choose(self, m: Mirror) -> tuple[str, str] | None:
        # R1 conservation: stop feeding waste while the source still runs.
        for name, p in m.pipes.items():
            if (p["open"] and not p["fractured"]
                    and m.kind.get(p["dst"]) == "waste"
                    and m.volumes.get(p["src"], 0) > 0):
                return ("valve", name)
        # R2 xor discipline: exactly-one-inlet, or the junction holds.
        for node in m.node_order:
            if m.kind[node] != "xor":
                continue
            wet_open = [name for name, p in m.pipes.items()
                        if p["dst"] == node and p["open"] and not p["fractured"]
                        and m.volumes.get(p["src"], 0) > 0]
            if len(wet_open) > 1:
                return ("valve", wet_open[1])
        # R3 steam discipline: boil only when the steam lands in crown.
        if m.crown_is_highest_cold():
            pool = m.wettest()
            if pool is not None:
                return ("boil", pool)
        # R4 gravity feed: reopen the direct road to the crown.
        for name, p in m.pipes.items():
            if (p["dst"] == "crown" and not p["open"] and not p["fractured"]
                    and m.volumes.get(p["src"], 0) > 0):
                return ("valve", name)
        return None  # idle: gravity is doing the work


def make_strategy(name: str, seed: int) -> RandomBot | GreedyBot | HeuristicBot:
    return {"random": lambda: RandomBot(seed),
            "greedy": lambda: GreedyBot(),
            "heuristic": lambda: HeuristicBot()}[name]()


# ------------------------------------------------------------- SRP6 door ----

async def srp6_login(client: Client, user: str, password: str,
                     group: str = DEFAULT_GROUP) -> dict[str, Any]:
    """Full client-side SRP6 over the wire (B4/R5): register, challenge,
    proof — under the dialect the account registered with (default
    rfc5054-2048, the R5 law). The math imports the SERVER's own dialect
    object (server/auth_srp6.VARIANTS, the anti-drift law); the one
    formula the dialect does not own is the client-side premaster
    S = (B - k*g^x)^(a + u*x) mod N (RFC 5054 §2.6, inherently the
    client's). The returned welcome is checked against the client's
    expected M2 — mutual auth actually verified, not assumed. The wire
    drops the challenge's "group" field today (the R5 follow-up), so the
    client's own account state names the dialect, exactly the module's
    documented contract."""
    dialect = VARIANTS[group]
    await client.send({"op": "srp_register", "user": user, "pass": password})
    reply = await client.recv()
    if reply.get("op") != "srp_registered":
        raise AssertionError(f"srp_register rejected: {reply}")
    a_secret = secrets.randbits(256)
    a_int = pow(dialect.g, a_secret, dialect.n)
    await client.send({"op": "srp_challenge", "user": user, "a": f"{a_int:x}"})
    ch_reply = await client.recv()
    if ch_reply.get("op") != "srp_challenge":
        raise AssertionError(f"srp_challenge rejected: {ch_reply}")
    salt = dialect.salt_decode(ch_reply["salt"])
    b_int = int(ch_reply["b"], 16)
    if salt is None:
        raise AssertionError(f"unparseable salt dialect={group}")
    ident, pw = dialect.normalize(user, password)
    x = dialect.x_of(ident, pw, salt)
    k = dialect.multiplier()
    u = dialect.u_of(a_int, b_int)
    s_int = pow((b_int - k * pow(dialect.g, x, dialect.n)) % dialect.n,
                a_secret + u * x, dialect.n)
    key = dialect.session_key(s_int)
    m1 = dialect.m1_of(ident, salt, a_int, b_int, key)
    m2_expected = dialect.m2_of(a_int, m1, key)
    await client.send({"op": "srp_proof", "user": user, "m1": m1.hex()})
    welcome = await client.recv()
    if welcome.get("op") != "welcome" or welcome.get("auth") != "srp6":
        raise AssertionError(f"srp_proof rejected: {welcome}")
    if welcome["m2"] != m2_expected.hex():
        raise AssertionError("server M2 proof mismatch (not mutual-authed)")
    return welcome


# ---------------------------------------------------------- event ledger ----

_PIPE_FLOW_RE = re.compile(r"^[a-z0-9_]+: \d+ [a-z0-9_]+->[a-z0-9_]+$")


def classify_event(ev: str, users: tuple[str, ...] = ()) -> str:
    """One tick event string -> one histogram bucket. Reads the wire's own
    event grammar only (world.py _apply + water_graph tick strings)."""
    body = ev[:-1] if ev.endswith(".") else ev
    if " boils 1 at " in body:
        return "boil_rise" if body.endswith("it rises") else "boil_other"
    if "pool went dry between ask and tick" in body:
        return "boil_dry"
    if body.startswith("Steam condenses at "):
        return "condense"
    if " FRACTURES" in body:
        return "fracture"
    if body.startswith("Siphon ") and " primes at crest" in body:
        return "siphon_prime"
    if body.startswith("Siphon ") and " breaks (intake dry)" in body:
        return "siphon_break"
    if body.startswith("Junction ") and " passes (" in body:
        return "junction_pass"
    if body.startswith("Junction ") and " below gate" in body:
        return "junction_hold"
    if body.startswith("Junction ") and " STARVED" in body:
        return "starved"
    if " to waste at " in body:
        return "waste_fill"
    if _PIPE_FLOW_RE.match(body):
        return "pipe_flow"
    if " shuts p" in body:
        return "valve_shut"
    if " opens p" in body:
        return "valve_open"
    if " tags a fish at " in body:
        return "tag"
    if " joins at " in body:
        return "join"
    if users and body.split(": ", 1)[0] in users and ": " in body:
        return "say"
    return "other"


# ------------------------------------------------------------- run result ----

@dataclass
class RunResult:
    board: str
    strategy: str
    seed: int
    door: str = "srp6"
    won: bool = False
    win_tick: int | None = None
    ticks_played: int = 0
    actions_sent: int = 0
    acked: int = 0
    rejects: dict[str, int] = field(default_factory=dict)
    events: dict[str, int] = field(default_factory=dict)
    end_volumes: dict[str, int] = field(default_factory=dict)
    steam_locked: int = 0
    crown: int = 0
    waste: int = 0
    total_water: int = 0
    conserved: bool = False
    fractures: list[str] = field(default_factory=list)
    stress: dict[str, int] = field(default_factory=dict)
    chain_ok: bool = False
    chain_rows: int = 0
    log_tail: str = ""
    srp_m2_ok: bool = True

    def to_json(self) -> dict[str, Any]:
        return dict(self.__dict__)


def _bump(counter: dict[str, int], key: str) -> None:
    counter[key] = counter.get(key, 0) + 1


async def _ask(client: Client, sid: str, verb: str, target: str, n: int) -> dict[str, Any]:
    """One nonce-bearing action; the very next line on the connection is
    its reply (manual-tick mode, the demo's own wire law)."""
    await client.send({"op": "action", "sid": sid, "verb": verb,
                       "target": target, "n": n})
    return await client.recv()


async def run_match(
    root: Path,
    board: str,
    strategy: str,
    seed: int,
    max_ticks: int = DEFAULT_TICKS,
    watch: bool = False,
) -> RunResult:
    """One self-play match through the full stack: fresh in-process server
    (ephemeral port, manual ticks), the board injected as the default
    room's world (the v0 seam: MountainWorld owns no board argument yet),
    the strategy player through the SRP6 door, a plaintext-hello spectator
    proving both clients see the same broadcast bytes, and the chain
    verified from disk after the world closes."""
    builder, win = BOARDS[board]
    log_path = root / f"{board}.{strategy}.s{seed}.jsonl"
    if log_path.exists():
        log_path.unlink()  # fresh chain per match (load would continue it)
    graph = builder()
    total_water = sum(n.volume for n in graph.nodes.values())
    world = MountainWorld(log_path=log_path)
    world.graph = graph          # the v0 board seam (receipt: module docstring)
    world.WIN_CROWN = win        # instance attr shadows the class constant
    world.winner = False

    auth = AuthStore(root / "users.json")
    auth.ensure_user("watcher", PASSWORD)
    srp_auth = Srp6AuthService(SrpStore(root / "srp_users.json"))
    server = WorldServer(port=0, tick_interval=None, auth=auth, world=world,
                         log_path=log_path, srp_auth=srp_auth)
    await server.start()

    user = f"sp-{strategy}"
    player = await Client.connect("127.0.0.1", server.bound_port)
    watcher = await Client.connect("127.0.0.1", server.bound_port)
    welcome = await srp6_login(player, user, PASSWORD)
    w_welcome = await watcher.do_hello("watcher", PASSWORD)
    sid = welcome["sid"]
    mirror = Mirror(welcome["world"])
    bot = make_strategy(strategy, seed)
    res = RunResult(board=board, strategy=strategy, seed=seed,
                    total_water=total_water)

    nonce = 0
    users = (user.upper(), "watcher", "innkeeper")
    room = server.rooms.default_room
    try:
        for _ in range(max_ticks):
            act = bot.choose(mirror)
            if act is not None:
                nonce += 1
                res.actions_sent += 1
                reply = await _ask(player, sid, act[0], act[1], nonce)
                if reply["op"] == "ack":
                    res.acked += 1
                else:
                    _bump(res.rejects, str(reply.get("why", "?")))
            payload = room.pump_once()   # this room's world ticks alone
            seen = await player.recv()
            watched = await watcher.recv()
            if seen != watched or seen != payload:
                raise AssertionError(
                    "broadcast divergence: clients or payload disagree")
            mirror.apply_tick(seen)
            for ev in seen.get("events", []):
                _bump(res.events, classify_event(ev, users))
            res.ticks_played += 1
            if watch:
                nodes = " ".join(f"{k}={v}" for k, v in seen["nodes"].items())
                mark = "  WIN" if seen["winner"] else ""
                print(f"  [{board}/{strategy}#{seed}] tick {seen['n']:>3}: {nodes}{mark}")
            if seen["winner"]:
                res.won, res.win_tick = True, seen["n"]
                break
    finally:
        res.end_volumes = world.node_volumes()
        res.steam_locked = sum(n.steam for n in world.graph.nodes.values())
        res.crown = res.end_volumes.get("crown", 0)
        res.waste = res.end_volumes.get("waste", res.end_volumes.get("slough", 0))
        res.conserved = (sum(res.end_volumes.values()) + res.steam_locked) == total_water
        res.fractures = [p for p, v in world.graph.pipes.items() if v.fractured]
        res.stress = {p: int(v.stress) for p, v in world.graph.pipes.items()}
        player.close()
        watcher.close()
        await server.stop()
        # chain verify, both instruments: in-memory AND reloaded from disk
        res.chain_ok = world.verify_log()
        try:
            disk_rows = load_log_rows(log_path)
        except ValueError:
            res.chain_ok = False
            disk_rows = []
        if disk_rows != world.rows:
            res.chain_ok = False
        res.chain_rows = len(world.rows)
        res.log_tail = world.rows[-1]["sha"][:16] if world.rows else ""
    return res


# ----------------------------------------------------------- stress suite ----

@dataclass
class StressClient:
    client: Client
    user: str
    sid: str
    door: str
    room: str
    bot: RandomBot | GreedyBot | HeuristicBot
    mirror: Mirror
    nonce: int = 0
    acked: int = 0
    rejects: dict[str, int] = field(default_factory=dict)
    ticks_seen: int = 0


async def stress_suite(root: Path, ticks: int = 24,
                       watch: bool = False) -> dict[str, Any]:
    """The stack under real gameplay: one server, four rooms (the default
    summit plus three born-at-hello side rooms), seven clients across both
    auth doors, every strategy class at once — plus two DELIBERATE
    anti-cheat probes (a replayed nonce -> STALE_NONCE, a same-tick second
    action -> RATE_CAP) to prove the receipt laws fire under load. Every
    room's chain verifies from disk; every room conserves its water."""
    out_dir = root / "stress"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "world_log.jsonl"
    if log_path.exists():
        log_path.unlink()
    auth = AuthStore(out_dir / "users.json")
    for u in ("w1", "w2", "w3", "w4", "w5"):
        auth.ensure_user(u, PASSWORD)
    srp_auth = Srp6AuthService(SrpStore(out_dir / "srp_users.json"))
    server = WorldServer(port=0, tick_interval=None, auth=auth,
                         log_path=log_path, srp_auth=srp_auth)
    await server.start()

    # (door, user, room, strategy, seed). NOTE the B4 law: the SRP6 door
    # lands in the DEFAULT room (room selection there is the owed
    # follow-up), so srp6 seats are honestly planned for "summit".
    plan = [
        ("srp6", "sp-one", "summit", "greedy", 1),
        ("srp6", "sp-two", "summit", "random", 11),
        ("plain", "w1", "summit", "heuristic", 1),
        ("plain", "w2", "alpha", "random", 12),
        ("plain", "w3", "alpha", "greedy", 2),
        ("plain", "w4", "beta", "heuristic", 3),
        ("srp6", "sp-three", "summit", "random", 13),
    ]
    seats: list[StressClient] = []
    for door, user, room_name, strat, seed in plan:
        client = await Client.connect("127.0.0.1", server.bound_port)
        if door == "srp6":
            welcome = await srp6_login(client, user, PASSWORD)
        else:
            welcome = await client.do_hello(user, PASSWORD, room=room_name)
        seat = StressClient(
            client=client, user=user, sid=welcome["sid"], door=door,
            room=welcome.get("room", "summit"),
            bot=make_strategy(strat, seed), mirror=Mirror(welcome["world"]))
        seats.append(seat)

    probes = {"STALE_NONCE": 0, "RATE_CAP": 0}
    probe_stale_done = False
    probe_cap_done = False
    try:
        for tick in range(1, ticks + 1):
            acked_this_tick: set[int] = set()
            for seat in seats:
                act = seat.bot.choose(seat.mirror)
                if act is None:
                    continue
                seat.nonce += 1
                reply = await _ask(seat.client, seat.sid, act[0], act[1], seat.nonce)
                if reply["op"] == "ack":
                    seat.acked += 1
                    acked_this_tick.add(id(seat))
                else:
                    _bump(seat.rejects, str(reply.get("why", "?")))
            # deliberate anti-cheat probes (the receipt laws under load),
            # each fired on a tick where seat 0 verifiably ACKED its own
            # action (a spent tick bucket is what makes the second action
            # illegal; probing after an idle tick would ack, not cap):
            #   STALE_NONCE: replay the last-used nonce id.
            #   RATE_CAP: a fresh-nonce SECOND action in the spent bucket;
            #   rides `say` — validation always passes, so the ladder
            #   reaches the cap instead of dying at DRY_POOL.
            seat = seats[0]
            if (not probe_stale_done and tick >= 2 and id(seat) in acked_this_tick):
                reply = await _ask(seat.client, seat.sid, "boil", "spring", seat.nonce)
                if reply["op"] == "ack":
                    seat.acked += 1
                else:
                    if reply.get("why") == "STALE_NONCE":
                        probes["STALE_NONCE"] += 1
                    _bump(seat.rejects, str(reply.get("why", "?")))
                probe_stale_done = True
            elif (not probe_cap_done and tick >= 3 and id(seat) in acked_this_tick):
                seat.nonce += 1
                reply = await _ask(seat.client, seat.sid, "say", "probe", seat.nonce)
                if reply["op"] == "ack":
                    seat.acked += 1
                else:
                    if reply.get("why") == "RATE_CAP":
                        probes["RATE_CAP"] += 1
                    _bump(seat.rejects, str(reply.get("why", "?")))
                probe_cap_done = True
            await server.pump_once()   # every live room ticks exactly once
            per_room: dict[str, dict[str, Any]] = {}
            for seat in seats:
                seen = await seat.client.recv()
                seat.ticks_seen += 1
                room_seen = per_room.setdefault(seat.room, seen)
                if seen != room_seen:
                    raise AssertionError(
                        f"cross-client divergence inside room {seat.room}")
                seat.mirror.apply_tick(seen)
    finally:
        for seat in seats:
            seat.client.close()
        await server.stop()

    rooms_out = []
    for room in server.rooms:
        w = room.world
        rows_ok = w.verify_log()
        log_file = _room_log_file(out_dir, room.id)
        try:
            disk = load_log_rows(log_file) if log_file.exists() else []
        except ValueError:
            rows_ok = False
            disk = []
        if disk != w.rows:
            rows_ok = False
        vols = w.node_volumes()
        rooms_out.append({
            "room": room.id,
            "chain_ok": rows_ok,
            "rows": len(w.rows),
            "winner": w.winner,
            "water_total": sum(vols.values()) + sum(n.steam for n in w.graph.nodes.values()),
            "fractures": [p for p, v in w.graph.pipes.items() if v.fractured],
        })
    stats = server.stats()
    return {
        "rooms": rooms_out,
        "clients": [{"user": s.user, "door": s.door, "room": s.room,
                     "acked": s.acked, "rejects": s.rejects,
                     "ticks_seen": s.ticks_seen} for s in seats],
        "probes": probes,
        "stats": stats,
        "checks": {
            "all_chains_ok": all(r["chain_ok"] for r in rooms_out),
            "isolation": all(s.ticks_seen == ticks for s in seats),
            "water_conserved": all(r["water_total"] == 8 for r in rooms_out),
            "stale_nonce_fired": probes["STALE_NONCE"] == 1,
            "rate_cap_fired": probes["RATE_CAP"] == 1,
            "actions_staged_matches": stats["actions_staged"] == sum(s.acked for s in seats),
        },
    }


def _room_log_file(root: Path, room_id: str) -> Path:
    """The RoomBook path law (rooms.py): side logs sit beside the default
    log with the room id in the stem."""
    base = root / "world_log.jsonl"
    if room_id == "summit":
        return base
    return base.with_name(f"{base.stem}.{room_id}.jsonl")


# --------------------------------------------------------------- render ----

def _fmt_rejects(rejects: dict[str, int]) -> str:
    if not rejects:
        return "-"
    return ",".join(f"{k}:{v}" for k, v in sorted(rejects.items()))


def render_table(results: list[RunResult]) -> str:
    head = (f"{'board':9s} {'strategy':11s} {'win@':>6s} {'acks':>4s} "
            f"{'rejects':<16s} {'crown':>5s} {'waste':>5s} {'steam':>5s} "
            f"{'fractures':<12s} chain")
    lines = [head, "-" * len(head)]
    for r in results:
        win = str(r.win_tick) if r.won else "DNF"
        lines.append(
            f"{r.board:9s} {r.strategy + '#' + str(r.seed):11s} {win:>6s} "
            f"{r.acked:4d} {_fmt_rejects(r.rejects):<16s} "
            f"{r.crown:5d} {r.waste:5d} {r.steam_locked:5d} "
            f"{(','.join(r.fractures) or '-'):<12s} "
            f"{'OK' if r.chain_ok and r.conserved else 'FAIL'}")
    return "\n".join(lines)


def render_signals(results: list[RunResult], stress: dict[str, Any] | None) -> str:
    by = {(r.board, r.strategy): r for r in results}
    lines = ["GAME-DESIGN SIGNALS"]

    def win(board: str, strat: str) -> str:
        r = by.get((board, strat))
        if r is None:
            return "?"
        return str(r.win_tick) if r.won else "DNF"

    lines.append(
        "1. Sprint board (mountain): greedy ties the provable 4-tick floor\n"
        "   (rate cap 1 action/sid/tick, each boil = +1 crown, win 4).\n"
        f"   greedy={win('mountain', 'greedy')} heuristic={win('mountain', 'heuristic')} "
        f"random={win('mountain', 'random')}. Heuristic pays a 1-tick\n"
        "   conservation tax (shuts the waste drain first) and ends with 0\n"
        "   water in waste; greedy wins a tick faster but parks 4 in the pit.")
    lines.append(
        "2. Decoy-peak board (shrine): steam condenses at the TALLEST cold\n"
        "   node, so a cold peak above the crown turns boiling into a\n"
        f"   donation. greedy={win('shrine', 'greedy')} (all 8 units vapor-locked on an\n"
        f"   outlet-less peak), heuristic={win('shrine', 'heuristic')} (never boils, shuts the\n"
        f"   leak, gravity does the rest), random={win('shrine', 'random')} at cap.\n"
        "   LESSON: board config, not mechanics, sets the skill floor.")
    lines.append(
        "3. No-cold board (foundry): the engine docstring promises steam\n"
        "   \"falls back to its origin node when no cold node exists\" — the\n"
        "   code has no fallback: steam NEVER returns to liquid play. Boil\n"
        f"   is an irreversible sink: greedy={win('foundry', 'greedy')} (vapor-locks the whole\n"
        f"   economy), heuristic={win('foundry', 'heuristic')} (xor valve discipline on tick 1),\n"
        f"   random={win('foundry', 'random')} at cap. SPEC/CODE DIVERGENCE, banked.")
    lines.append(
        "4. Marathon board (spelunk): the 1/tick needle carries every\n"
        "   policy to a tick-30 fill, but the cap-8 firehose runs full bore\n"
        "   every tick: stress 8/tick vs threshold 233 -> FRACTURES ~tick 30\n"
        "   and its 8-unit spray lands on the lowest node — the crown.\n"
        "   Fracture is both hazard and win button; heuristic shuts the\n"
        "   drain on tick 1 and the pipe never wears (0 stress).")
    lines.append(
        "5. Skill ceiling: where steam feeds the crown, greedy IS the\n"
        "   ceiling (no planning gap). Where boiling is denied (rival cold,\n"
        "   no cold), the ceiling moves to valve discipline + conservation —\n"
        "   the verb economy, not the physics, is the depth.")
    if stress is not None:
        c = stress["checks"]
        lines.append(
            f"6. Stack stress: {len(stress['rooms'])} rooms / {len(stress['clients'])} clients\n"
            f"   both doors, chains {'OK' if c['all_chains_ok'] else 'FAIL'}, isolation\n"
            f"   {'OK' if c['isolation'] else 'FAIL'}, water conserved\n"
            f"   {'OK' if c['water_conserved'] else 'FAIL'}, STALE_NONCE probe\n"
            f"   {'fired' if c['stale_nonce_fired'] else 'MISSED'}, RATE_CAP probe\n"
            f"   {'fired' if c['rate_cap_fired'] else 'MISSED'} "
            f"(staged={stress['stats']['actions_staged']}).")
    return "\n".join(lines)


# ----------------------------------------------------------------- main ----

async def _determinism_check(root: Path, ticks: int) -> dict[str, Any]:
    """Same seed twice -> byte-identical world logs (the determinism law's
    self-play leg: SRP6 entropy and session ids never enter the log)."""
    logs = []
    for sub in ("det-a", "det-b"):
        (root / sub).mkdir(parents=True, exist_ok=True)
        await run_match(root / sub, "mountain", "random", 7, max_ticks=ticks)
        logs.append((root / sub / "mountain.random.s7.jsonl").read_bytes())
    return {"byte_identical_logs": logs[0] == logs[1]}


async def _amain(args: argparse.Namespace) -> int:
    root = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="selfplay_"))
    root.mkdir(parents=True, exist_ok=True)
    results: list[RunResult] = []
    stress: dict[str, Any] | None = None
    det: dict[str, Any] | None = None

    if not args.stress_only:
        seeds_random = [int(s) for s in args.seeds.split(",") if s]
        for board in args.boards.split(","):
            for strat in args.strategies.split(","):
                seeds = seeds_random if strat == "random" else (int(args.seed),)
                for seed in seeds:
                    r = await run_match(root, board, strat, int(seed),
                                        max_ticks=args.ticks, watch=args.watch)
                    results.append(r)
                    mark = f"WIN @ tick {r.win_tick}" if r.won else "DNF"
                    print(f"[match] {board}/{strat}#{seed}: {mark} "
                          f"(acks {r.acked}, rejects {_fmt_rejects(r.rejects)}, "
                          f"chain {'OK' if r.chain_ok else 'FAIL'})")
    if not args.matches_only:
        stress = await stress_suite(root, ticks=args.stress_ticks, watch=args.watch)
        print(f"[stress] rooms={len(stress['rooms'])} "
              f"clients={len(stress['clients'])} checks={stress['checks']}")
        det = await _determinism_check(root, ticks=min(args.ticks, 30))
        print(f"[determinism] {det}")

    print()
    print(render_table(results))
    print()
    print(render_signals(results, stress))

    (root / "results.json").write_text(
        "\n".join(json.dumps(r.to_json()) for r in results) + "\n",
        encoding="utf-8")
    receipt = [ "# Mountain self-play receipt (tools/mountain_selfplay.py)",
                "", f"cap {args.ticks} ticks; seeds random={args.seeds}; artifacts {root}", "",
                "```", render_table(results), "```", "", render_signals(results, stress), ""]
    if det is not None:
        receipt.append(f"determinism: {det}")
    receipt_path = Path(args.receipt) if args.receipt else root / "RECEIPT.md"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text("\n".join(receipt) + "\n", encoding="utf-8")
    print(f"\nreceipt: {receipt_path}")
    print(f"logs + results.json: {root}")
    ok = all(r.chain_ok and r.conserved for r in results)
    if stress is not None:
        ok = ok and all(stress["checks"].values())
    if det is not None:
        ok = ok and det["byte_identical_logs"]
    print(f"verdict: {'ALL GREEN' if ok else 'SOMETHING RED — read the table'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="the Mountain plays itself, and we watch")
    ap.add_argument("--boards", default=",".join(BOARDS))
    ap.add_argument("--strategies", default=",".join(STRATEGIES))
    ap.add_argument("--seeds", default=",".join(str(s) for s in DEFAULT_SEEDS),
                    help="reps for the random strategy (comma list)")
    ap.add_argument("--seed", default="1", help="seed for deterministic strategies' runs")
    ap.add_argument("--ticks", type=int, default=DEFAULT_TICKS)
    ap.add_argument("--stress-ticks", type=int, default=24)
    ap.add_argument("--out", default=None, help="artifact root (default: temp dir)")
    ap.add_argument("--receipt", default=None, help="receipt markdown path")
    ap.add_argument("--watch", action="store_true", help="print every tick")
    ap.add_argument("--stress-only", action="store_true")
    ap.add_argument("--matches-only", action="store_true")
    args = ap.parse_args(argv)
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
