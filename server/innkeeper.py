"""innkeeper: UF-01, the bot that remembers you (LW8, 2026-09-30).

Receipt: watch/inbox/last_mile_20260930/LW8_INNKEEPER.md . Lineage:
  - S11 flock-as-server-actors (MICKEY17_WAVE_LEDGER_20260929.md): the ike3
    seam - register_session(sid=...) with NO socket is a real session; fish
    ride it, and so does the innkeeper.
  - S19 chat v1 spec (the LW6 say channel): one verb say, 240-char cap,
    BAD_TEXT reject, delivered in the existing tick events, GLOBAL
    distance-free; "BOTS SPEAK THROUGH THE SAME CHANNEL (UF-01 innkeeper
    as a client-with-sid...)". The innkeeper IS a client-with-sid: every
    row it emits carries the sid the world's roster issued it. The say law
    (cap + reject) is implemented here because say has not landed in a
    protocol_table yet; when it does, this module's channel wraps it.
  - X9 motion dialect (protocol_table.py MOTION_TABLE): motion rows are
    {verb in idle/flee/pursue/carry/dance, intensity_q8: u8, dir: target}.
    Every row the brain emits is gated through MOTION_DISPATCH.ask BEFORE
    it leaves the actor - the brain never emits an illegal row.

THE BRAIN is pure: decide(tick, world_state, player_memories) -> rows.
No RNG, no wall clock, no input mutation (fish_brain.gd's law, ported).
Variety is tick-driven (tick % k selects cadence and intensity); the same
(tick, world_state, player_memories) always produce byte-identical rows.

WHAT IT SAYS (all strings deterministic):
  - greet on join: a known player (visits > 0 in memories) hears
    "Welcome back, <name> - the spring is at <N> units"; a first-timer
    hears "Welcome, <name> - ...". A known player with a ledger history
    also hears what they did: "Last visit you tagged <k> fish, <name>."
  - water-state comment, every WATER_COMMENT_EVERY ticks or when a player
    moves water (boil/valve): crown tiers vs win_crown, e.g.
    "The crown is half full." at half.
  - motion: idle at the spring (intensity breathes with tick), dance when
    a player tags a fish NEARBY. Nearby is honest co-location: the world
    has no coordinates (the S19 CMaNGOS lesson), so nearby == the tag's
    node == the innkeeper's node.

PLAYER MEMORIES are a JSON file keyed by username, fields exactly
{visits, last_action, fish_tagged}, loaded fail-closed (a corrupt file
refuses to boot, the world.py log law) and saved sorted+compact so the
same memories always write the same bytes.

Run:
    .venv/Scripts/python.exe -m pytest tests/test_innkeeper.py -q
Tests: tests/test_innkeeper.py

Schema: innkeeper.v1 . deterministic + $0 . decide() is pure, no writes
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol_table import MOTION_DISPATCH  # noqa: E402

INNKEEPER_SID = "innkeeper"
INNKEEPER_USER = "innkeeper"
INNKEEPER_NODE = "spring"      # the named node it sits at (roster 'at')
SAY_MAX = 240                  # LW6/S19: the say channel's char cap
WATER_COMMENT_EVERY = 8        # cadence; the tick drives variety, not RNG
BAD_TEXT = "BAD_TEXT"          # LW6/S19: the say channel's typed reject

MEM_FIELDS = ("visits", "last_action", "fish_tagged")


# ---------------------------------------------------------- the say law ----

def say_law(text: Any) -> tuple[bool, str | None]:
    """The LW6 channel law: (ok, why). text must be a non-empty str of at
    most SAY_MAX chars. Every violation is the one typed reject BAD_TEXT
    (one code for the whole law, the u8/BAD_INTENSITY house shape)."""
    if not isinstance(text, str) or not text or len(text) > SAY_MAX:
        return False, BAD_TEXT
    return True, None


def say_row(sid: str, text: Any) -> dict[str, Any]:
    """One say row, or the typed reject the wire would answer with. A row
    that passes the law is GLOBAL distance-free delivery payload: whoever
    owns the tick loop appends it to that tick's events (S19)."""
    ok, why = say_law(text)
    if not ok:
        return {"op": "reject", "why": why, "verb": "say"}
    return {"verb": "say", "sid": sid, "text": text}


# ------------------------------------------------- the session ledger ----
# world.py _apply fixes the event grammar byte-exactly; these parsers read
# that grammar and nothing else. Physics lines (steam/flow/starve) match no
# prefix and parse to None - the innkeeper remembers PLAYERS, not pipes.

def parse_ledger_event(ev: str) -> dict[str, Any] | None:
    """{user, verb, target[, score, rose, open]} or None. Deterministic
    prefix/suffix reads of the ledger's own event strings."""
    if not isinstance(ev, str) or not ev.endswith("."):
        return None
    body = ev[:-1]
    if " joins at " in body:
        user, _, target = body.partition(" joins at ")
        return {"user": user, "verb": "join", "target": target}
    if " tags a fish at " in body:
        left, _, right = body.partition(" tags a fish at ")
        target, sep, score = right.rpartition(" (score ")
        if sep and score.rstrip(")").isdigit():
            return {"user": left, "verb": "tag", "target": target,
                    "score": int(score.rstrip(")"))}
        return None
    if " boils 1 at " in body:
        user, _, target = body.partition(" boils 1 at ")
        return {"user": user, "verb": "boil",
                "target": target.split(";")[0], "rose": True}
    if " boils at " in body:
        user, _, rest = body.partition(" boils at ")
        return {"user": user, "verb": "boil",
                "target": rest.split(":")[0], "rose": False}
    if " shuts " in body:
        user, _, pipe = body.partition(" shuts ")
        return {"user": user, "verb": "valve", "target": pipe, "open": False}
    if " opens " in body:
        user, _, pipe = body.partition(" opens ")
        return {"user": user, "verb": "valve", "target": pipe, "open": True}
    return None


# ------------------------------------------------------------- the brain ----

def crown_tier(crown: int, win_crown: int) -> str:
    """The water-state sentence for a crown volume, deterministic tiers."""
    if crown >= win_crown:
        return "The crown is full."
    if crown * 2 >= win_crown:
        return "The crown is half full."
    if crown > 0:
        return "The crown is barely wet."
    return "The crown is dry."


def decide(
    tick: int,
    world_state: dict[str, Any],
    player_memories: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Pure brain. world_state is the actor's view
    {tick, nodes: {name: vol}, roster, scores, events: [ledger strings],
    win_crown}; player_memories is {user: {visits, last_action, fish_tagged}}.
    Neither input is mutated. Returns
      {"motion": [rows], "say": [rows], "memory": {user: deltas}} -
    'memory' is UPDATE DELTAS the actor merges and persists, never a
    mutation done here (purity law).
    """
    nodes: dict[str, int] = world_state.get("nodes", {})
    events = [e for e in world_state.get("events", [])]
    parsed = [p for p in (parse_ledger_event(e) for e in events) if p]
    players = [p for p in parsed if p["user"] != INNKEEPER_USER]

    motion: list[dict[str, Any]] = []
    say: list[dict[str, Any]] = []
    memory: dict[str, dict[str, Any]] = {}

    # motion: dance when a player tags a fish nearby (same node), else idle
    # at the spring. Intensity breathes with the tick - the only variety.
    nearby_tags = [p for p in players
                   if p["verb"] == "tag" and p["target"] == INNKEEPER_NODE]
    if nearby_tags:
        motion.append({"verb": "dance", "sid": INNKEEPER_SID,
                       "intensity_q8": 192 + (tick % 64), "dir": INNKEEPER_NODE})
    else:
        motion.append({"verb": "idle", "sid": INNKEEPER_SID,
                       "intensity_q8": (tick * 13) % 48, "dir": INNKEEPER_NODE})

    # greetings: one per join event, ledger order (arrival order is the law)
    spring_units = int(nodes.get(INNKEEPER_NODE, 0))
    for p in players:
        if p["verb"] != "join":
            continue
        user, at = p["user"], p["target"]
        mem = player_memories.get(user) or {}
        known = int(mem.get("visits", 0)) > 0
        head = (f"Welcome back, {user}" if known else f"Welcome, {user}")
        say.append(say_row(INNKEEPER_SID,
                           f"{head} - the spring is at {spring_units} units"))
        if known and int(mem.get("fish_tagged", 0)) > 0:
            say.append(say_row(INNKEEPER_SID,
                               f"Last visit you tagged "
                               f"{int(mem.get('fish_tagged', 0))} fish, {user}."))
        mem_delta = memory.setdefault(user, {})
        mem_delta["visits"] = mem_delta.get("visits", 0) + 1
        mem_delta["last_action"] = f"joined at {at}"

    # water-state comment: on cadence, or when a player moved water this tick
    water_moved = any(p["verb"] in ("boil", "valve") for p in players)
    if water_moved or tick % WATER_COMMENT_EVERY == 0:
        say.append(say_row(INNKEEPER_SID, crown_tier(
            int(nodes.get("crown", 0)), int(world_state.get("win_crown", 4)))))

    # memory deltas from every other player action this tick (tags, boils,
    # valves) - what the ledger says they did becomes what we remember
    for p in players:
        user = p["user"]
        if p["verb"] == "join":
            continue  # folded into the greeting pass above
        delta = memory.setdefault(user, {})
        if p["verb"] == "tag":
            delta["fish_tagged"] = delta.get("fish_tagged", 0) + 1
            delta["last_action"] = f"tagged a fish at {p['target']}"
        elif p["verb"] == "boil":
            verb = "boiled at" if p.get("rose") else "boiled dry at"
            delta["last_action"] = f"{verb} {p['target']}"
        elif p["verb"] == "valve":
            verb = "opened" if p.get("open") else "shut"
            delta["last_action"] = f"{verb} {p['target']}"

    return {"motion": motion, "say": say, "memory": memory}


# ------------------------------------------------------ player memories ----

class PlayerMemories:
    """The JSON file keyed by username, fields exactly MEM_FIELDS.
    Load is fail-closed (corrupt file refuses to boot, the world.py log
    law); save writes sorted+compact so identical memories write identical
    bytes (the canonical_json house law)."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.data: dict[str, dict[str, Any]] = {}
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{self.path}: player memories are corrupt, refusing to boot"
                ) from exc
            if isinstance(raw, dict):
                self.data = {
                    str(u): dict(m) for u, m in raw.items() if isinstance(m, dict)
                }

    def get(self, user: str) -> dict[str, Any]:
        """A fresh copy with every field defaulted - readers never see a
        missing key, and mutations of the copy cannot touch the store."""
        mem = dict(self.data.get(user, {}))
        mem.setdefault("visits", 0)
        mem.setdefault("last_action", "")
        mem.setdefault("fish_tagged", 0)
        return mem

    def known(self, user: str) -> bool:
        return int(self.get(user)["visits"]) > 0

    def apply(self, deltas: dict[str, dict[str, Any]]) -> None:
        """Merge decide()'s memory deltas: counts add, last_action replaces.
        Unknown fields are ignored (the file shape stays MEM_FIELDS)."""
        for user, delta in deltas.items():
            mem = self.get(user)
            mem["visits"] = int(mem["visits"]) + int(delta.get("visits", 0))
            mem["fish_tagged"] = int(mem["fish_tagged"]) + int(
                delta.get("fish_tagged", 0))
            if "last_action" in delta:
                mem["last_action"] = str(delta["last_action"])
            self.data[user] = {k: mem[k] for k in MEM_FIELDS}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        body = json.dumps(self.data, sort_keys=True,
                          separators=(",", ":"), ensure_ascii=False)
        self.path.write_text(body + "\n", encoding="utf-8")


# ---------------------------------------------------------------- actor ----

class Innkeeper:
    """The body around the brain: registers as a REAL session on the world
    (the ike3 seam - no socket, a roster row the snapshot shows), sits at
    INNKEEPER_NODE, and pumps one decide() per world tick. Every say row is
    re-validated through the LW6 law and every motion row through the X9
    MOTION_TABLE at emission: a row that fails its law is never returned to
    the tick loop; it comes back as the typed reject instead."""

    def __init__(self, world: Any, memories_path: Path | str) -> None:
        self.world = world
        self.memories = PlayerMemories(memories_path)
        self.last_rows: dict[str, Any] = {}

    def attach(self) -> dict[str, str]:
        """The ike3 seam: register_session with no socket. The roster row is
        the innkeeper's body - snapshot()['roster'] shows it at the spring."""
        self.world.register_session(INNKEEPER_SID, INNKEEPER_USER,
                                    at=INNKEEPER_NODE)
        return dict(self.world.roster[INNKEEPER_SID])

    # -------------------------------------------------------------- view ----
    def state_from_tick(self, tick_payload: dict[str, Any]) -> dict[str, Any]:
        """The brain's world_state, built from one world.tick() broadcast
        payload plus the world's roster/scores - the session ledger's voice
        IS the events list (hash-chained rows, replayable truth)."""
        return {
            "tick": int(tick_payload.get("n", 0)),
            "nodes": dict(tick_payload.get("nodes", {})),
            "roster": {sid: dict(info)
                       for sid, info in self.world.roster.items()},
            "scores": dict(self.world.scores),
            "events": list(tick_payload.get("events", [])),
            "win_crown": int(getattr(self.world, "WIN_CROWN", 4)),
        }

    # -------------------------------------------------------------- pump ----
    def pump(self, tick_payload: dict[str, Any]) -> dict[str, Any]:
        """One tick: decide, gate every row through its channel law, merge
        and persist memories. Returns the gated rows (the tick loop's
        delivery payload); self.last_rows keeps the same truth for tests."""
        state = self.state_from_tick(tick_payload)
        rows = decide(state["tick"], state, self.memories.data)

        gated_say: list[dict[str, Any]] = []
        for row in rows["say"]:
            gated = say_row(INNKEEPER_SID, row.get("text"))
            if gated.get("op") == "reject":
                # our own text violated our own law - that is a bug, not a
                # wire event; refuse to deliver, surface the reject raw
                gated_say.append(gated)
            else:
                gated_say.append(gated)

        nodes = frozenset(state["nodes"])
        gated_motion: list[dict[str, Any]] = []
        for row in rows["motion"]:
            ask = MOTION_DISPATCH.ask(
                row["verb"], "AUTHED",
                args={"intensity_q8": row["intensity_q8"], "dir": row["dir"]},
                targets=nodes)
            if not ask["ok"]:
                gated_motion.append({"op": "reject", "why": ask["reason"],
                                     "verb": row["verb"]})
            else:
                gated_motion.append(row)

        self.memories.apply(rows["memory"])
        self.memories.save()

        self.last_rows = {"motion": gated_motion, "say": gated_say,
                          "memory": rows["memory"], "tick": state["tick"]}
        return self.last_rows


def main() -> int:  # pragma: no cover - operability convenience
    from server.world import MountainWorld
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="innkeeper_"))
    world = MountainWorld(log_path=tmp / "world.jsonl")
    keep = Innkeeper(world, tmp / "players.json")
    keep.attach()
    world.register_session("s1", "ada")
    world.stage("s1", "join", INNKEEPER_NODE)
    rows = keep.pump(world.tick())
    print(json.dumps(rows, indent=2, ensure_ascii=False))
    print("memories:", keep.memories.path.read_text(encoding="utf-8").strip())
    world.close()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
