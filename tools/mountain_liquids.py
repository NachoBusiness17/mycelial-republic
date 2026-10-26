"""mountain_liquids — DFHack's liquids plugin, THROUGH THE LAW (LM3, 2026-09-30).

DFHack's `liquids` paints water at will: infinite sources, level-7 floods,
obsidian casting — there the admin IS the physics. This tool is the same
wish made lawful: every intervention must ride a REGISTERED stage verb from
the frozen table (server/protocol_table.py — MountainWorld speaks
CHAT_TABLE: boil/valve/join/tag + say/whisper), pass world validation at
receipt, and apply at the next tick (determinism law: the tick is the only
mutator). Anything not in the table FAILS CLOSED with a typed reject — the
teaching moment is the gap list (--inventory): what CAN a legitimate
admin do? Route water (boil/valve), never create, delete, or teleport it.

Ops (`liquids <node|pipe> <op> [amount]`):
    boil           verb `boil` (staged). amount N = N staged asks of 1 unit:
                   the wire envelope carries verb+target only, so an amount
                   is composed as repeated legal asks applied in arrival
                   order (the engine rows stay honest when the pool runs
                   dry mid-batch: "pool went dry between ask and tick").
    open / close   verb `valve` (staged, TOGGLE semantics — the tool reads
                   the pipe's current state so `open` can never accidentally
                   shut it). A FRACTURED pipe cannot reopen (AC2:
                   water_graph.open() refuses bursts); the tool refuses
                   loudly (FRACTURED_PIPE) instead of letting the engine
                   log "opens" while the pipe stays dead.
    source-on /    NOT IN ANY TABLE. DFHack's infinite-source wish fails
    source-off     closed UNKNOWN_VERB; the gap table names the candidate
                   spec verbs (an emission-budgeted `source`, a conserving
                   `pour`), never a create-from-nothing.

Offline lane: builds a FRESH default board (build_mountain_graph) in
memory, registers an AUTHED admin session (the world itself issues the sid
— the admin is just another session, never above the law), stages through
MountainWorld.stage, ticks once. No wire, no disk, no log path. Every ack
prints conservation (V5 economy law: deletion is theft — the board's 8
units survive every legal verb; creating water is exactly the thing no
verb does).

Typed rejects: UNKNOWN_VERB / UNKNOWN_TARGET / DRY_POOL / BAD_ARGS /
BAD_INTENSITY all come from the table vocabularies (BAD_* live in the X9
motion dialect's closed reject set — the u8 law: a bool is a verdict, not
an intensity). FRACTURED_PIPE is tool-level, mirroring the engine's silent
refusal in water_graph.open() (AC2).

Exit codes: 0 = ack/no-op · 2 = typed fail-closed reject (argparse usage
errors also exit 2 — a refusal is a refusal).

Usage:
    .venv/Scripts/python.exe tools/mountain_liquids.py hollow boil 2
    .venv/Scripts/python.exe tools/mountain_liquids.py p_bypass open
    .venv/Scripts/python.exe tools/mountain_liquids.py spring source-on   # fails closed
    .venv/Scripts/python.exe tools/mountain_liquids.py --inventory
    .venv/Scripts/python.exe tools/mountain_liquids.py --dry-run hollow boil 3

Tests: tests/test_mountain_liquids.py
Receipt: watch/inbox/last_mile_20260930/LM3_LIQUIDS.md

Schema: mountain_liquids.v1 . deterministic + $0 . stdlib only, no writes
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol_table import CHAT_TABLE  # noqa: E402
from server.world import MountainWorld, VERBS  # noqa: E402

ADMIN_SID = "liquids-admin"
ADMIN_USER = "liquids"
MAX_ASK = 255  # the X9 u8 law: 1..255, a bool is a verdict not an intensity

# The op surface. verb None = the DFHack wish has no table verb: fail closed.
OPS: dict[str, dict[str, Any]] = {
    "boil": {"verb": "boil", "target": "node", "amount": True,
             "help": "lift N units at a node to steam (staged verb boil; "
                     "amount N = N staged asks of 1)"},
    "open": {"verb": "valve", "target": "pipe", "amount": False,
             "help": "open a gate (staged verb valve; refuses FRACTURED pipes)"},
    "close": {"verb": "valve", "target": "pipe", "amount": False,
              "help": "shut a gate (staged verb valve, toggle semantics)"},
    "source-on": {"verb": None, "target": "node", "amount": True,
                  "help": "DFHack wish: place an infinite water source — "
                          "NOT a table verb, fails closed"},
    "source-off": {"verb": None, "target": "node", "amount": True,
                   "help": "DFHack wish: remove a water source — NOT a "
                           "table verb, fails closed"},
}

# The legal-vs-gap inventory: DFHack-style wishes against the frozen table.
# status: LEGAL (table verb) · GAP (no verb, candidate for the spec) ·
# REFUSED-BY-LAW (the engine's own laws refuse it — a verb would be theft) ·
# CONTRACT-ONLY (rows exist in a compiled table the wire has not adopted).
INVENTORY: tuple[dict[str, str], ...] = (
    {"wish": "lift water at a node to steam (route it uphill)", "verb": "boil",
     "status": "LEGAL",
     "note": "staged; amount N = N asks of 1; DRY_POOL at receipt; steam "
             "condenses at the cold crown — conserved, never deleted"},
    {"wish": "open a gate", "verb": "valve", "status": "LEGAL",
     "note": "toggle semantics; FRACTURED pipes refuse reopen (AC2 -> "
             "FRACTURED_PIPE fail-closed at the tool)"},
    {"wish": "shut a gate", "verb": "valve", "status": "LEGAL",
     "note": "toggle semantics"},
    {"wish": "stand at a node", "verb": "join", "status": "LEGAL",
     "note": "roster position only; mutates no water"},
    {"wish": "tag a fish at a wet node", "verb": "tag", "status": "LEGAL",
     "note": "score event; DRY_POOL on dry nodes"},
    {"wish": "speak / whisper", "verb": "say, whisper", "status": "LEGAL",
     "note": "CHAT contract rows (LW6); mutates no world state"},
    {"wish": "place an infinite water source (source-on)", "verb": "-",
     "status": "GAP",
     "note": "candidate spec verb `source <node> <u8 rate>` with an emission "
             "budget — every existing verb conserves the board total (8), "
             "so a source must say where the water comes from"},
    {"wish": "remove a water source (source-off)", "verb": "-", "status": "GAP",
     "note": "the same candidate verb at rate 0"},
    {"wish": "paint / set a node's water level (water N)", "verb": "-",
     "status": "GAP",
     "note": "candidate `pour <from> <to> <u8>` — a conserving transfer "
             "verb with a donor, never creation from nothing"},
    {"wish": "delete water outright (drain / dry a node)", "verb": "-",
     "status": "REFUSED-BY-LAW",
     "note": "V5 economy law: deletion is theft. The legal path exists: "
             "boil — steam ignores pipes and recovers at the crown"},
    {"wish": "instantly condense or kill steam", "verb": "-", "status": "GAP",
     "note": "the tick owns condensation; candidate `chill <node>` if ever "
             "needed, but it re-routes rather than deletes"},
    {"wish": "fast-forward the physics (run N ticks)", "verb": "-",
     "status": "GAP",
     "note": "the tick is the only mutator and the server owns the loop; "
             "candidate admin verb `tick <u8>`"},
    {"wish": "push fish (flee / pursue / carry / dance)", "verb": "-",
     "status": "CONTRACT-ONLY",
     "note": "rows exist in MOTION_TABLE (X9) with u8+target payload laws, "
             "but the server wire has not adopted them — rig-side today"},
    {"wish": "magma / obsidian casting", "verb": "-", "status": "REFUSED-BY-LAW",
     "note": "the engine has no magma medium — a medium gap, not a verb gap"},
)


def legal_vs_gap() -> tuple[dict[str, str], ...]:
    """The inventory as data (tests pin its shape; --inventory prints it)."""
    return INVENTORY


def contract_for(verb: str) -> str:
    """Which compiled contract carries the verb, digest-pinned (trust bytes)."""
    if verb in CHAT_TABLE.verbs:
        return f"chat:{CHAT_TABLE.digest[:12]}"
    return "none"


def _total_units(world: MountainWorld) -> int:
    return sum(n.volume + n.steam for n in world.graph.nodes.values())


def _base(world: MountainWorld, op: str, target: str,
          amount: Any) -> dict[str, Any]:
    return {"op": op, "target": target, "amount": amount, "verb": None,
            "staged": 0, "tick": world.graph.tick_count, "events": [],
            "nodes": world.node_volumes(), "total_before": _total_units(world),
            "total_units": _total_units(world), "rows": len(world.rows),
            "note": None}


def _fail(base: dict[str, Any], reason: str, note: str) -> dict[str, Any]:
    # Fail closed: nothing was staged, nothing ticked, the world is
    # byte-identical to entry (tests assert rows/tick/volumes unchanged).
    return {**base, "ok": False, "reason": reason, "note": note}


def apply_liquids(world: MountainWorld, target: str, op: str,
                  amount: Any = None, dry_run: bool = False) -> dict[str, Any]:
    """Compose the legal verb envelope for one DFHack-style wish and apply it
    offline: validate -> stage (N asks for an amount) -> one tick.

    Returns a result dict; every refusal is typed and leaves the world
    untouched (ok=False rows/tick/nodes are the entry snapshot)."""
    base = _base(world, op, target, amount)
    spec = OPS.get(op)
    if spec is None:
        return _fail(base, "UNKNOWN_VERB",
                     f"op {op!r} is not a liquids op; see --inventory")
    if spec["verb"] is None:
        return _fail(base, "UNKNOWN_VERB",
                     f"DFHack wish {op!r} has no verb in any compiled table "
                     f"(see --inventory: the gap list is the candidate spec "
                     f"verbs, never creation from nothing)")
    if spec["verb"] not in VERBS:
        # belt against contract shrink: OPS maps only table verbs, but the
        # gate is the contract the world SPEAKS, not this file's memory of it
        return _fail(base, "UNKNOWN_VERB",
                     f"verb {spec['verb']!r} is not in the contract "
                     f"MountainWorld speaks")

    # amount law (X9 u8): boil takes 1..255; valve carries no amount at all
    if spec["amount"]:
        if amount is None:
            n_asks = 1
        elif isinstance(amount, bool) or not isinstance(amount, int) \
                or not 1 <= amount <= MAX_ASK:
            return _fail(base, "BAD_INTENSITY",
                         f"amount must be an int 1..{MAX_ASK} "
                         f"(u8 law: a bool is a verdict, not an intensity)")
        else:
            n_asks = amount
    else:
        if amount is not None:
            return _fail(base, "BAD_ARGS",
                         f"op {op!r} rides verb {spec['verb']!r}, which "
                         f"carries no amount on the wire")
        n_asks = 1

    # target law: boil names a node, gate ops name a pipe
    if spec["target"] == "pipe":
        pipe = world.graph.pipes.get(target)
        if pipe is None:
            return _fail(base, "UNKNOWN_TARGET",
                         f"{target!r} is not a pipe on this board")
        if op == "open":
            if pipe.fractured:
                # AC2: water_graph.open() refuses bursts; the valve verb can
                # never reopen a fractured pipe. The engine would swallow
                # this ask silently (event says "opens", pipe stays dead) —
                # the tool refuses loudly instead.
                return _fail(base, "FRACTURED_PIPE",
                             f"{target!r} is FRACTURED (AC2): bursts are "
                             f"closed forever; no verb reopens them")
            if pipe.open:
                return {**base, "ok": True, "reason": "NOOP",
                        "verb": spec["verb"],
                        "note": f"{target!r} already open; nothing staged"}
        else:  # close
            if not pipe.open:
                why = " (fractured)" if pipe.fractured else ""
                return {**base, "ok": True, "reason": "NOOP",
                        "verb": spec["verb"],
                        "note": f"{target!r} already shut{why}; nothing staged"}
    else:
        if target not in world.graph.nodes:
            return _fail(base, "UNKNOWN_TARGET",
                         f"{target!r} is not a node on this board")

    # session law: even the admin must be AUTHED — a sid the world issued
    if ADMIN_SID not in world.roster:
        world.register_session(ADMIN_SID, ADMIN_USER)
    ok, why = world.validate(ADMIN_SID, spec["verb"], target)
    if not ok:
        return _fail(base, why, f"world validation refused the envelope")

    if dry_run:
        return {**base, "ok": True, "reason": "DRYRUN", "verb": spec["verb"],
                "staged": n_asks,
                "note": "dry-run: envelope validated, nothing staged"}

    staged = 0
    for _ in range(n_asks):
        reply = world.stage(ADMIN_SID, spec["verb"], target)
        if reply.get("op") != "ack":
            return _fail(
                base, reply.get("why", "UNKNOWN_VERB"),
                f"receipt refused ask {staged + 1} of {n_asks} "
                f"(world unchanged: staged asks never applied without a tick)")
        staged += 1
    payload = world.tick()
    return {"ok": True, "reason": "ACK", "verb": spec["verb"],
            "op": op, "target": target, "amount": amount, "staged": staged,
            "tick": payload["n"], "events": payload["events"],
            "nodes": payload["nodes"], "total_before": base["total_before"],
            "total_units": _total_units(world), "rows": len(world.rows),
            "note": None}


def _print_inventory() -> None:
    print("mountain_liquids — the legal-vs-gap table "
          "(what CAN a legitimate admin do?)")
    print(f"contract spoken by MountainWorld: chat:{CHAT_TABLE.digest[:12]} "
          f"verbs: {', '.join(VERBS)}")
    print()
    w_wish, w_verb = 46, 16
    print(f"{'DFHack-style wish':<{w_wish}} {'verb':<{w_verb}} status")
    print("-" * (w_wish + w_verb + 24))
    for row in INVENTORY:
        print(f"{row['wish']:<{w_wish}} {row['verb']:<{w_verb}} "
              f"{row['status']}")
        print(f"    {row['note']}")


def _print_result(r: dict[str, Any]) -> None:
    head = f"liquids: op={r['op']} target={r['target']}"
    if r.get("amount") is not None:
        head += f" amount={r['amount']}"
    print(head)
    if not r["ok"]:
        print(f"  FAIL CLOSED: {r['reason']}")
        if r["note"]:
            print(f"  note  : {r['note']}")
        print(f"  world untouched: rows={r['rows']} tick={r['tick']} "
              f"units={r['total_units']}")
        return
    if r["verb"]:
        print(f"  gate    : verb '{r['verb']}' -> "
              f"{contract_for(r['verb'])} (AUTHED sid '{ADMIN_SID}')")
    when = ("nothing staged" if r["staged"] == 0
            or r["reason"] in ("NOOP", "DRYRUN")
            else f"applied at tick {r['tick']}")
    print(f"  envelope: {r['staged']} staged ask(s), {when}")
    if r["note"]:
        print(f"  note  : {r['note']}")
    if r["events"]:
        print("  events:")
        for ev in r["events"]:
            print(f"    - {ev}")
    print(f"  nodes   : {r['nodes']}")
    print(f"  units   : {r['total_before']} -> {r['total_units']} "
          f"({'conserved; V5 law' if r['total_before'] == r['total_units'] else 'DRIFT'})")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="mountain_liquids",
        description="DFHack-style liquids, through the frozen verb table "
                    "(fails closed on anything not staged-verb-legal).")
    p.add_argument("node", nargs="?",
                   help="node name (boil ops) or pipe name (open/close)")
    p.add_argument("op", nargs="?", help=f"one of: {', '.join(OPS)}")
    p.add_argument("amount", nargs="?", help="u8 1..255 (boil only)")
    p.add_argument("--inventory", action="store_true",
                   help="print the legal-vs-gap table and exit")
    p.add_argument("--dry-run", action="store_true",
                   help="validate the envelope, stage nothing")
    p.add_argument("--json", action="store_true",
                   help="emit the result dict as JSON")
    args = p.parse_args(argv)

    if args.inventory:
        _print_inventory()
        return 0
    if args.node is None or args.op is None:
        p.print_usage(sys.stderr)
        print("mountain_liquids: need <node|pipe> <op> [amount] "
              "(or --inventory)", file=sys.stderr)
        return 2

    amount: int | None = None
    if args.amount is not None:
        try:
            amount = int(args.amount, 10)
        except ValueError:
            result = _fail(_base(MountainWorld(), args.op, args.node,
                                 args.amount), "BAD_INTENSITY",
                           f"amount {args.amount!r} is not an integer 1..255")
            _emit(result, args.json)
            return 2

    world = MountainWorld()  # fresh default board, in-memory, offline
    result = apply_liquids(world, args.node, args.op, amount,
                           dry_run=args.dry_run)
    _emit(result, args.json)
    return 0 if result["ok"] else 2


def _emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, sort_keys=True))
    else:
        _print_result(result)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
