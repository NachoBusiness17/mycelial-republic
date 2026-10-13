"""walk_world -- CV3 dogfood: the first REAL session carried through mag/wow_world.py.

R2's orphan list said it plain: the atrium-ring chain had 12 green tests and ZERO real
sessions had ever carried world/room -- every receipt on disk was test residue. This
walker is the fix that orphan deserved: one NAMED traveler (a wow_player.v1 ledger,
built through the module's own create()/apply() law), one recorded route (deterministic
seed, the same turns every run), one boss resolved through the SAME kernels the tests
pin (Dispatch for every verb, Instance for the encounter law, Stream for the RNG law),
and durable files written at the end:

  * player ledger    memory/runs/wow_player/ply-<id>.json            (wow_player.v1)
  * world receipt    memory/runs/wow_world/receipts/wworld-<id>.json  (wow_session.v1)
  * session ledger   memory/runs/wow_world/sessions/wworld-<id>.json  (wow_world_session.v1)

THE REPLAY LAW, now with a character attached: run this twice with the same seed and
all three files must come out BYTE-IDENTICAL. The player ledger is append-only, so a
re-run does NOT append duplicate rows: the walker re-derives the target ledger from the
route using wow_player's own pure reducers (_new_row/_replay/verify_file), then (a)
no-ops when the file on disk already equals the target byte-for-byte, or (b) refuses
with LEDGER_CONFLICT when history diverges -- a ledger is history; the walker never
rewrites one.

ROUTE (8 turns == TURN_LIMIT; the budget is the law):
  1  look        atrium       AUTHED -> LOGGEDIN (promotion draws nothing)
  2  go north    atrium -> torch_hall        (movement draws nothing)
  3  go west     torch_hall   REFUSED: STATUS_NEVER (the locked ash_gallery door)
  4  go east     torch_hall -> vault
  5  look        vault        the load: TO_BE_DECIDED -> IN_PROGRESS (draws nothing)
  6-8 look x3    vault        one draw each; the guarded boss DONE lands on the 3rd
Verdict: COMPLETE. On COMPLETE the traveler is granted one sigil item (ledger row 4):
the character carries proof of the encounter out of the world.

RUN:
  .venv/Scripts/python.exe scripts/walk_world.py                 # seed lantern-01
  .venv/Scripts/python.exe scripts/walk_world.py --seed S --traveler NAME [--world-boss]

stdout is one canonical JSON line; nothing in any written file reads the clock
(determinism is the point). Schema: receipts belong to their own modules.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, NoReturn

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from mag import wow_player as wp                        # noqa: E402
from mag.wow_bones import load_fixture                  # noqa: E402
from mag.wow_bones_session import TURN_LIMIT, canonical  # noqa: E402
from mag.wow_world import WorldSession                  # noqa: E402

TRAVELER = "lantern-01"
DEFAULT_SEED = "lantern-01"
EXPECTED_ROUTE = ["atrium", "torch_hall", "vault"]

# The recorded route. One refused knock on the locked door is IN the script on purpose:
# a real session should meet the world's typed refusal law, not just its sunny path.
WALK: list[tuple[str, str | None]] = [
    ("look", None),      # 1  promotion; draws nothing
    ("go", "north"),     # 2  atrium -> torch_hall
    ("go", "west"),      # 3  locked ash_gallery door: STATUS_NEVER, room unchanged
    ("go", "east"),      # 4  torch_hall -> vault
    ("look", None),      # 5  the load: TO_BE_DECIDED -> IN_PROGRESS; draws nothing
    ("look", None),      # 6  draw 1
    ("look", None),      # 7  draw 2
    ("look", None),      # 8  draw 3 -> guarded boss DONE attempt
]


def fail(reason: str, **kw: Any) -> NoReturn:
    print(canonical({"ok": False, "reason": reason, **kw}))
    raise SystemExit(1)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def walk_world(seed: str, world_boss: bool) -> WorldSession:
    fx = load_fixture()
    if fx is None:
        fail("NO_FIXTURE", hint="python -m mag.wow_bones extract")
    ses = WorldSession(fx, seed, world_boss=world_boss)
    for verb, arg in WALK:
        ses.turn(verb, arg)
    return ses


def target_player_document(name: str, route: list[str], grant_item: dict[str, Any] | None,
                           stamina_max: int = 10) -> dict[str, Any]:
    """Re-derive the WHOLE ledger from the route with wow_player's own pure reducers.

    This is the byte-identity anchor: the public create()/apply() path (first run) and
    this pure derivation (every run) must agree byte-for-byte or the walker is lying.
    """
    ledger: list[dict[str, Any]] = []
    prev = wp._ZERO_HASH

    def push(event: str, data: dict[str, Any]) -> None:
        nonlocal prev
        row = wp._new_row(len(ledger) + 1, event, data, prev)
        ledger.append(row)
        prev = row["hash"]

    push("create", {"room": route[0], "stamina_max": stamina_max})
    for room in route[1:]:
        push("move", {"to": room})
    if grant_item is not None:
        push("grant_item", {"item": grant_item})

    doc = {"schema": wp.SCHEMA, "player_id": wp.player_id_for(name), "name": name,
           "traits": wp._replay(ledger), "ledger": ledger}
    ok, reason = wp.verify_file(doc)
    if not ok:
        fail("WALKER_BUG", detail=f"target ledger failed its own verify: {reason}")
    return doc


def settle_player(doc: dict[str, Any]) -> dict[str, Any]:
    """First run: build the ledger through the public create/apply law. Later runs:
    resume-from-ledger and demand byte-identity with the derived target."""
    target_bytes = canonical(doc).encode("utf-8")
    path = wp.STORE / f"{doc['player_id']}.json"
    existed = path.is_file()
    if existed:
        if path.read_bytes() != target_bytes:
            fail("LEDGER_CONFLICT", player=doc["player_id"],
                 detail="the ledger on disk is history and diverges from this route; "
                        "the walker never rewrites a ledger")
        player = wp.PlayerFile.load(doc["player_id"])   # login IS resume-from-ledger
        if player is None:                              # pragma: no cover
            fail("WALKER_BUG", detail="existing file vanished mid-walk")
        replayed = True
    else:
        genesis = doc["ledger"][0]["data"]          # genesis is row 1, NOT the final view
        player = wp.PlayerFile.create(doc["name"], room=genesis["room"],
                                      stamina_max=genesis["stamina_max"])
        for row in doc["ledger"][1:]:
            player.apply(row["event"], **row["data"])
        if player.canonical_state().encode("utf-8") != target_bytes:
            fail("WALKER_BUG", detail="public create/apply path diverged from target bytes")
        replayed = False
    traits = player.traits
    return {"player_id": player.player_id, "name": player.name, "room": traits["room"],
            "ledger_rows": len(player.ledger), "inventory": traits["inventory"],
            "replayed": replayed, "path": rel(path), "sha256": sha256_file(path)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="walk-world")
    ap.add_argument("--seed", default=DEFAULT_SEED)
    ap.add_argument("--traveler", default=TRAVELER)
    ap.add_argument("--world-boss", action="store_true")
    a = ap.parse_args(argv)
    if len(WALK) > TURN_LIMIT:
        fail("WALKER_BUG", detail=f"route is {len(WALK)} turns; the law allows {TURN_LIMIT}")

    ses = walk_world(a.seed, a.world_boss)
    verdict = ses.verdict()
    if not a.world_boss:
        # falsifiers for the walker itself: the recorded route must be the walked route
        if ses.route != EXPECTED_ROUTE:
            fail("ROUTE_DRIFT", route=ses.route, expected=EXPECTED_ROUTE)
        if verdict != "COMPLETE":
            fail("WALK_INCOMPLETE", verdict=verdict, encounter=ses.encounter_name())

    session_path = ses.save()
    receipt_path = ses.write_receipt()

    grant = None
    if verdict == "COMPLETE":
        grant = {"item_id": "sigil-atrium-ring", "kind": "boss-sigil", "boss": 0,
                 "from_room": ses.room, "session": ses.session_id}
    doc = target_player_document(a.traveler, list(ses.route), grant)
    player = settle_player(doc)

    rec = ses.receipt()
    out = {
        "ok": True,
        "walker": "scripts/walk_world.py",
        "traveler": a.traveler,
        "player_id": player["player_id"],
        "seed": ses.seed,
        "world": ses.world["id"],
        "world_sha256_12": rec["world_sha256_12"],
        "session_id": ses.session_id,
        "route_taken": " -> ".join(ses.route),
        "room": ses.room,
        "turns": ses.turn_count,
        "draws": ses.draws,
        "refusals": sum(1 for m in ses.moves if not m["ok"]),
        "encounter_state": ses.encounter_name(),
        "verdict": verdict,
        "session_status": ses.session_status,
        "player": player,
        "player_replayed": player["replayed"],
        "files": {
            "session": {"path": rel(session_path), "sha256": sha256_file(session_path)},
            "receipt": {"path": rel(receipt_path), "sha256": sha256_file(receipt_path)},
        },
    }
    print(canonical(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
