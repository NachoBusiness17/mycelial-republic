```python
"""A bones-driven room world: table-addressed movement and encounter receipts.

This module adds rooms and routes to the tested bones session kernels. It is
not a second dispatcher, encounter engine, or networked game server.

RUN:
    python -m mag.wow_world start --seed 7
    python -m mag.wow_world verbs --session SESSION_ID
    python -m mag.wow_world turn --session SESSION_ID --verb go --arg north

Schema: wow_world.v1 . deterministic + $0 . session + receipt files are the only writes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

from mag.wow_bones import Dispatch, load_fixture
from mag.wow_bones_session import (
    AUTHED,
    BOSS_ID,
    DRAW_TARGET,
    LOGGEDIN,
    TURN_LIMIT,
    BonesSession,
    canonical,
)

WORLD_SCHEMA = "wow_world.v1"
SESSION_SCHEMA = "wow_world_session.v1"
RECEIPT_SCHEMA = "wow_session.v1"

OUT_DIR = ROOT / "memory" / "runs" / "wow_world"
RECEIPTS_DIR = OUT_DIR / "receipts"

DEFAULT_WORLD = {
    "schema": WORLD_SCHEMA,
    "id": "atrium-ring",
    "start": "atrium",
    "boss": 0,
    "rooms": [
        {"id": "atrium", "name": "The Atrium", "verbs_allowed": ["look"],
         "exits": {"north": "torch_hall", "east": "archive"}, "encounters": []},
        {"id": "torch_hall", "name": "The Torch Hall", "verbs_allowed": ["look"],
         "exits": {"south": "atrium", "east": "vault",
                   "west": {"room": "ash_gallery", "locked": True}},
         "encounters": []},
        {"id": "archive", "name": "The Archive", "verbs_allowed": ["look"],
         "exits": {"west": "atrium", "north": "vault"}, "encounters": []},
        {"id": "vault", "name": "The Vault", "verbs_allowed": ["look", "pry"],
         "exits": {"south": "torch_hall", "west": "archive"}, "encounters": [0]},
        {"id": "ash_gallery", "name": "The Ash Gallery", "verbs_allowed": ["look"],
         "exits": {"east": "torch_hall"}, "encounters": []},
    ],
}


def world_digest(world: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(world).encode("utf-8")).hexdigest()[:12]


def room_fixture(world: dict[str, Any]) -> dict[str, Any]:
    enums = {
        "session_status": {
            f"ROOM:{room['id']}": i
            for i, room in enumerate(world["rooms"])
        }
    }
    rows: list[dict[str, str]] = []
    for room in world["rooms"]:
        status = f"ROOM:{room['id']}"
        for verb in room["verbs_allowed"]:
            verb_name = verb.strip().upper()
            rows.append({
                "opcode": "0x0",
                "name": f"{verb_name}@{status}",
                "status": status,
                "processing": "INPLACE",
                "handler": (
                    "WorldSession::Handle"
                    + verb_name.title().replace("_", "")
                ),
            })
        for direction, target in room["exits"].items():
            direction_name = direction.strip().upper()
            locked = isinstance(target, dict) and target.get("locked", False)
            rows.append({
                "opcode": "0x0",
                "name": f"GO_{direction_name}@{status}",
                "status": "STATUS_NEVER" if locked else status,
                "processing": "INPLACE",
                "handler": f"WorldSession::HandleGo{direction_name.title()}",
            })
    return {"tables": {"client_opcodes": rows}, "enums": enums}


def world_session_id(
    seed: int, world_boss: bool, world: dict[str, Any]
) -> str:
    identity = (
        f"{SESSION_SCHEMA}:{world['id']}:{seed}:{int(bool(world_boss))}"
    )
    return "wworld-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]


def _write_json(path: Path, body: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical(body), encoding="utf-8")
    return path


class WorldSession(BonesSession):
    def __init__(
        self,
        fixture: dict[str, Any],
        seed: int,
        world: dict[str, Any] | None = None,
        *,
        world_boss: bool = False,
    ) -> None:
        super().__init__(fixture, seed, world_boss=world_boss)
        self.world = world or DEFAULT_WORLD
        self.room_gate = Dispatch(room_fixture(self.world))
        self.room = self.world["start"]
        self.route = [self.room]
        self.session_id = world_session_id(
            self.seed, self.world_boss, self.world
        )

    def _room_status(self) -> str:
        return f"ROOM:{self.room}"

    def _row_name(self, verb_name: str) -> str:
        return f"{verb_name}@{self._room_status()}"

    def _current_room(self) -> dict[str, Any]:
        return next(
            room for room in self.world["rooms"] if room["id"] == self.room
        )

    def turn(self, verb: str, arg: str | None = None) -> dict[str, Any]:
        self.turn_count += 1
        verb_name = (
            "GO_" + arg.strip().upper()
            if verb.strip().lower() == "go" and arg
            else verb.strip().upper()
        )

        # Gate law: the suffix addresses a row; Dispatch alone decides legality.
        gate = self.room_gate.dispatch(
            self._row_name(verb_name), self._room_status()
        )
        entry: dict[str, Any] = {
            "n": self.turn_count,
            "verb": verb,
            "arg": arg,
            "room": self.room,
            "ok": gate["ok"],
            "reason": gate["reason"],
            "handler_ran": gate["handler_ran"],
        }
        if not gate["ok"]:
            # Refusal law: only the attempt count and move record change.
            self.moves.append(entry)
            return entry

        entry["handler"] = gate["handler"]
        if verb_name.startswith("GO_"):
            direction_name = verb_name[3:]
            target = next(
                target
                for direction, target in self._current_room()["exits"].items()
                if direction.strip().upper() == direction_name
            )
            destination = target["room"] if isinstance(target, dict) else target
            # Movement law: no draw, promotion, or encounter LOAD.
            self.room = destination
            self.route.append(destination)
            entry["to"] = destination
        elif self.session_status == AUTHED:
            self.session_status = LOGGEDIN
        elif (
            BOSS_ID in self._current_room()["encounters"]
            and self.instance.state[BOSS_ID]
            == self.instance.enums["TO_BE_DECIDED"]
        ):
            # Instance law: the first write is a LOAD, not a drawn transition.
            self.instance.set_boss_state(BOSS_ID, "IN_PROGRESS")
        else:
            self.stream.next()
            self.draws += 1
            if (
                self.instance.state[BOSS_ID]
                == self.instance.enums["IN_PROGRESS"]
                and self.draws % DRAW_TARGET == 0
            ):
                # Terminal law: Instance owns the world-boss DONE guard.
                self.instance.set_boss_state(
                    BOSS_ID, "DONE", world_boss_alive=self.world_boss
                )

        self.moves.append(entry)
        return entry

    def receipt(self) -> dict[str, Any]:
        bones = super().receipt()
        body = {
            "schema": RECEIPT_SCHEMA,
            "session_id": self.session_id,
            "seed": self.seed,
            "world": self.world["id"],
            "world_sha256_12": world_digest(self.world),
            "world_boss_alive": self.world_boss,
            "room": self.room,
            "route": list(self.route),
            "bones_digest": bones["bones_digest"],
            "session_status": self.session_status,
            "encounter_state": bones["encounter_state"],
            "draw_index": self.stream.index,
            "moves": list(self.moves),
            "verdict": self.verdict(),
        }
        body["sha256"] = hashlib.sha256(
            canonical(body).encode("utf-8")
        ).hexdigest()
        return body

    def save(self) -> Path:
        body = {
            "schema": SESSION_SCHEMA,
            "session_id": self.session_id,
            "seed": self.seed,
            "world_boss_alive": self.world_boss,
            "world_id": self.world["id"],
            "world_sha256_12": world_digest(self.world),
            "room": self.room,
            "route": list(self.route),
            "session_status": self.session_status,
            "boss0": self.instance.state[BOSS_ID],
            "draws": self.draws,
            "turn_count": self.turn_count,
            "stream_log": list(self.stream.log),
            "moves": list(self.moves),
        }
        return _write_json(
            OUT_DIR / "sessions" / f"{self.session_id}.json", body
        )

    @classmethod
    def load(
        cls,
        session_id: str,
        fixture: dict[str, Any] | None = None,
    ) -> WorldSession | None:
        path = OUT_DIR / "sessions" / f"{session_id}.json"
        if not path.is_file():
            return None
        fixture = fixture or load_fixture()
        if fixture is None:
            return None
        saved = json.loads(path.read_text(encoding="utf-8"))
        if saved.get("world_sha256_12") != world_digest(DEFAULT_WORLD):
            return None

        session = cls(
            fixture,
            saved["seed"],
            world_boss=saved["world_boss_alive"],
        )
        session.room = saved["room"]
        session.route = list(saved["route"])
        session.session_status = saved["session_status"]
        # Restore a snapshot, not a new encounter transition.
        session.instance.state[BOSS_ID] = saved["boss0"]
        session.draws = saved["draws"]
        session.turn_count = saved["turn_count"]
        session.stream.log = list(saved["stream_log"])
        session.stream.index = max(
            (row["index"] for row in session.stream.log), default=-1
        ) + 1
        session.moves = list(saved["moves"])
        return session

    def write_receipt(self) -> Path:
        return _write_json(
            RECEIPTS_DIR / f"{self.session_id}.json", self.receipt()
        )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wow-world")
    commands = parser.add_subparsers(dest="command", required=True)

    start = commands.add_parser("start")
    start.add_argument("--seed", type=int, required=True)
    start.add_argument("--world-boss", action="store_true")

    turn = commands.add_parser("turn")
    turn.add_argument("--session", required=True)
    turn.add_argument("--verb", required=True)
    turn.add_argument("--arg")

    for command in ("status", "receipt", "verbs", "map"):
        subparser = commands.add_parser(command)
        subparser.add_argument("--session", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    fixture = load_fixture()
    if fixture is None:
        print(canonical({"ok": False, "reason": "NO_FIXTURE"}))
        return 1

    if args.command == "start":
        session = WorldSession(
            fixture, args.seed, world_boss=args.world_boss
        )
        session.save()
        print(canonical(session.receipt()))
        return 0

    session = WorldSession.load(args.session, fixture=fixture)
    if session is None:
        print(canonical({"ok": False, "reason": "NO_SESSION"}))
        return 1

    result: dict[str, Any]
    exit_code = 0
    if args.command == "turn":
        result = session.turn(args.verb, args.arg)
        session.save()
        exit_code = 0 if result["ok"] else 1
    elif args.command == "status":
        result = session.receipt()
    elif args.command == "receipt":
        session.write_receipt()
        result = session.receipt()
    elif args.command == "verbs":
        # Discovery reflects the gate table, including its first-class locks.
        rows = room_fixture(session.world)["tables"]["client_opcodes"]
        result = {
            "session_id": session.session_id,
            "room": session.room,
            "verbs": [
                row for row in rows
                if row["status"] == session._room_status()
                and row["status"] != "STATUS_NEVER"
            ],
        }
    else:
        room = session._current_room()
        result = {
            "session_id": session.session_id,
            "room": session.room,
            "name": room["name"],
            "exits": room["exits"],
        }

    print(canonical(result))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
```