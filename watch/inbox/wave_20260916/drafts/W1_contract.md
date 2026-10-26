# W1 contract — draft `mag/wow_world.py` (bones-world skeleton, blueprint M0)

You are drafting ONE Python module for an existing, tested codebase. Output exactly one
complete Python module in a single ```python code block. No prose before or after.
The module must run on Python 3.11+, stdlib only, deterministic, $0, no timestamps in
game state, no network, no prints outside `main()`.

## Context you build on (DO NOT re-implement any of this)

`mag/wow_bones.py` provides kernels:
- `Dispatch(fixture)`: gate-first verb dispatch. `dispatch(name, status)` returns
  `{"ok": True, "reason": "DISPATCHED", "handler": row["handler"], "processing": ..., "handler_ran": True}`
  or `{"ok": False, "reason": <UNKNOWN_OPCODE|UNKNOWN_STATUS|STATUS_NEVER|STATUS_UNHANDLED|STATUS_MISMATCH>, "handler_ran": False}`.
  It reads `fixture["tables"]["client_opcodes"]` (rows: `opcode`, `name`, `status`,
  `processing`, `handler`; keyed internally by `name`) and `fixture["enums"]["session_status"]`
  (dict name->int, membership-tested only).
- `Instance(fixture)`: encounter law. `set_boss_state(boss_id, state, *, world_boss_alive=False)`;
  first write to a TO_BE_DECIDED boss is a LOAD (commits, returns False); repeat is False;
  DONE refused (False) while `world_boss_alive`; real transition returns True. `is_done(id)`,
  `name(state)`, `.state` dict, `.enums`.
- `Stream(seed)`: `next()` -> int 0..99, records `{"index","value"}`; `.index`, `.log`, `.replay(log)`.

`mag/wow_bones_session.py` provides:
- `BonesSession(fixture, seed, *, world_boss=False)` with `.dispatch`, `.instance`, `.stream`,
  `.session_status` (starts `AUTHED="STATUS_AUTHED"`, promotes to `LOGGEDIN="STATUS_LOGGEDIN"`),
  `.turn_count`, `.draws`, `.moves`, `.session_id`, `.verdict()` (COMPLETE if boss 0 done,
  EXHAUSTED at TURN_LIMIT=8 else OPEN), `.receipt()` (schema `wow_session.v1`, keys:
  schema, session_id, seed, world_boss_alive, bones_digest[:12], session_status,
  encounter_state, draw_index, moves, verdict, sha256 over `canonical(body-minus-sha256)`),
  `.save()`, `.load(session_id)`, `.write_receipt()`.
- `canonical(obj)` = `json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` —
  the ONLY serialization allowed.
- Constants: `AUTHED`, `LOGGEDIN`, `DRAW_TARGET=3`, `TURN_LIMIT=8`, `BOSS_ID=0`.
- `load_fixture()` from `mag.wow_bones` (bones fixture; may be None).

## Module contract — `mag/wow_world.py`

Header docstring in the repo's house style (why the module exists, what it is NOT, RUN line,
schema line ending like: `Schema: wow_world.v1 . deterministic + $0 . session + receipt files are the only writes`).

```python
from mag.wow_bones import Dispatch, load_fixture
from mag.wow_bones_session import (AUTHED, BOSS_ID, DRAW_TARGET, LOGGEDIN, TURN_LIMIT,
                                   BonesSession, canonical)
```

Constants:
- `WORLD_SCHEMA = "wow_world.v1"`, `SESSION_SCHEMA = "wow_world_session.v1"`,
  `RECEIPT_SCHEMA = "wow_session.v1"` (world receipts keep the bones receipt contract).
- `OUT_DIR = ROOT / "memory" / "runs" / "wow_world"`; `RECEIPTS_DIR = OUT_DIR / "receipts"`.
  Get ROOT the same way the two modules above do (try `from config import ROOT` except fallback
  `Path(__file__).resolve().parent.parent`; then `sys.path.insert(0, str(ROOT))`).

`DEFAULT_WORLD` — EXACTLY this table (verbatim, it is data not draftwork):

```python
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
```

Exit values: a `str` is an open door; a `dict {"room": rid, "locked": True}` is a LOCKED door.

Functions:

1. `world_digest(world) -> str` — `hashlib.sha256(canonical(world)).hexdigest()[:12]`.
2. `room_fixture(world) -> dict` — build a Dispatch-shaped fixture view from the world:
   - `enums = {"session_status": {f"ROOM:{r['id']}": i for i, r in enumerate(world["rooms"])}}`
   - one row per legality, name-UNIQUE as `f"{VERB}@{status}"` (the gate keys rows by name,
     so the room suffix prevents cross-room collisions):
     - for each room, for each verb in `verbs_allowed` (normalized `verb.strip().upper()`):
       row `{"opcode": "0x0", "name": f"{VERB}@ROOM:{id}", "status": f"ROOM:{id}",
       "processing": "INPLACE", "handler": f"WorldSession::Handle{VERB.title().replace('_','')}"}`.
     - for each room, for each exit direction `d` (normalized upper): target = exit value;
       locked dict -> row status `"STATUS_NEVER"` (the gate's first-class lock);
       open str -> row status `f"ROOM:{id}"`; name `f"GO_{D}@ROOM:{id}"`,
       handler `f"WorldSession::HandleGo{D.title()}"`, processing `"INPLACE"`.
   - return `{"tables": {"client_opcodes": rows}, "enums": enums}` — this is ALL the gate needs.
3. `world_session_id(seed, world_boss, world) -> str` —
   `"wworld-" + sha256(f"{SESSION_SCHEMA}:{world['id']}:{seed}:{int(bool(world_boss))}")[:12]`.
4. `class WorldSession(BonesSession)`:
   - `__init__(self, fixture, seed, world=None, *, world_boss=False)`:
     `super().__init__(fixture, seed, world_boss=world_boss)`; `self.world = world or DEFAULT_WORLD`;
     `self.room_gate = Dispatch(room_fixture(self.world))`; `self.room = self.world["start"]`;
     `self.route = [self.room]`; override `self.session_id = world_session_id(self.seed, self.world_boss, self.world)`.
   - `_room_status(self) -> str`: `f"ROOM:{self.room}"`.
   - `_row_name(self, verb_name) -> str`: `f"{verb_name}@{self._room_status()}"`.
   - `turn(self, verb, arg=None) -> dict` — the pipeline, in this exact order:
     1. `self.turn_count += 1`.
     2. Resolve `verb_name`: `("GO_" + arg.strip().upper()) if verb.strip().lower() == "go" and arg else verb.strip().upper()`.
     3. `gate = self.room_gate.dispatch(self._row_name(verb_name), self._room_status())`
        — THE GATE DECIDES. Composing the row name is addressing, not legality.
     4. Entry `{"n": self.turn_count, "verb": verb, "arg": arg, "room": self.room,
        "ok": gate["ok"], "reason": gate["reason"], "handler_ran": gate["handler_ran"]}`.
        If refused: append entry to `self.moves`, return it. Refused turns change NOTHING else
        (no draw, no status change, no move) — the bones refusal law.
     5. Success: add `"handler": gate["handler"]` to entry.
        - Movement (`verb_name.startswith("GO_")`): resolve destination from the CURRENT room's
          exits dict (str, or dict["room"]); set `self.room = dest`; `self.route.append(dest)`;
          entry `"to" = dest`. Movement draws NOTHING and loads NOTHING.
        - Else if `self.session_status == AUTHED`: `self.session_status = LOGGEDIN` (promotion
          draws nothing — inherited law).
        - Else if boss (BOSS_ID) is in the CURRENT room's `encounters` and
          `self.instance.state[BOSS_ID] == self.instance.enums["TO_BE_DECIDED"]`:
          `self.instance.set_boss_state(BOSS_ID, "IN_PROGRESS")` — a LOAD, returns False; no draw.
        - Else: `self.stream.next(); self.draws += 1;` and if the boss is loaded
          (`state == enums["IN_PROGRESS"]`) and `self.draws % DRAW_TARGET == 0`:
          `self.instance.set_boss_state(BOSS_ID, "DONE", world_boss_alive=self.world_boss)`
          — the inherited guarded terminal; refused forever under world_boss.
     6. Append entry to `self.moves`; return it.
   - `receipt(self) -> dict` — bones receipt contract PLUS world keys:
     `{"schema": RECEIPT_SCHEMA, "session_id", "seed", "world": self.world["id"],
     "world_sha256_12": world_digest(self.world), "world_boss_alive", "room": self.room,
     "route": list(self.route), "bones_digest": fixture bones_digest[:12], "session_status",
     "encounter_state", "draw_index": self.stream.index, "moves", "verdict": self.verdict()}`;
     then `body["sha256"] = sha256(canonical(body)).hexdigest()` (canonical body EXCLUDES sha256).
     No timestamps anywhere.
   - `save(self) -> Path` — canonical JSON at `OUT_DIR / "sessions" / f"{self.session_id}.json"`
     with `{"schema": SESSION_SCHEMA, "session_id", "seed", "world_boss_alive",
     "world_id": self.world["id"], "world_sha256_12": world_digest(self.world), "room",
     "route", "session_status", "boss0", "draws", "turn_count", "stream_log", "moves"}`.
   - `@classmethod load(cls, session_id, fixture=None) -> "WorldSession | None"` — read the
     save file; `fixture = fixture or load_fixture()`; None if either missing; None if saved
     `world_sha256_12 != world_digest(DEFAULT_WORLD)` (a changed world is not resumable);
     rebuild with `cls(fixture, seed, world_boss=...)`, then restore room, route, status,
     boss0, draws, turn_count, stream log, moves, `stream.index = max(indexes, default=-1)+1`.
   - `write_receipt(self) -> Path` — canonical receipt at `RECEIPTS_DIR / f"{self.session_id}.json"`.
5. `main(argv=None) -> int` — argparse CLI `wow-world`: `start --seed S [--world-boss]`,
   `turn --session ID --verb V [--arg A]`, `status --session ID`, `receipt --session ID`,
   `verbs --session ID` (rows whose status equals the current room status, excluding
   STATUS_NEVER — the legal verbs HERE), `map --session ID` (current room name + exits).
   Emit one canonical JSON object per command via `print(canonical(obj))`; return 0/1.
   No fixture -> `{"ok": false, "reason": "NO_FIXTURE"}`.

## Laws you must not break

- The Dispatch gate is REUSED (an instance over a world table); never re-implement gating logic.
- Refusals are typed, from the gate's own vocabulary, with handler_ran False; never silent,
  never raised.
- Movement costs no draws. The DONE guard is the Instance kernel's own, called with
  `world_boss_alive` — never bypassed.
- Deterministic: no datetime, no randomness, no set/dict iteration order dependence in output
  (build rows in world-list order). Same seed + same route -> byte-identical receipt.
- House style: module docstring with a RUN section; type hints; small functions; comments that
  carry law citations, not filler.

Return the complete module now, one ```python block.
