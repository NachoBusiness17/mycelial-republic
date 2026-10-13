"""world: the authoritative Mountain (world server v0).

Owns a WaterGraph imported from mag.water_graph (the estate's physics
organ, the single source of hydraulic truth; the Godot port in
roblox_to_godot/systems/water_graph.gd mirrors it line for line) built
with the Mountain slice's EXACT board:

    nodes  spring elev10 vol6 · terrace elev6 · gate1 elev5 XOR ·
           hollow elev3 vol2 · waste elev0 · crown elev14 COLD
    pipes  p_spring spring->gate1 · p_terrace terrace->gate1 ·
           p_out gate1->hollow · p_drain hollow->waste ·
           p_bypass spring->terrace siphon crest2 STARTS SHUT
    WIN    crown volume >= 4   (total water in the world: 8)

Determinism law: the tick is the ONLY mutator. Client actions are
validated at receipt and STAGED; they apply, in arrival order, at the
start of the next tick, before the physics. No RNG, no floats, no wall
clock inside log rows (rows carry seq + tick numbers only), so the same
(action, tick) interleaving from two fresh worlds produces byte-identical
node-volume sequences and byte-identical logs.

Event log: append-only, hash-chained (the wow_player/gwap house pattern:
row hash covers the row minus its own hash field, genesis prev = 64
zeros), held in memory AND persisted as JSONL. Reopening a log path
continues the chain (seq and prev sha resume from the file's last row)
and refuses to boot on a corrupt file, so the file is genuinely
append-only across runs even though v0 does not restore world state.

v0 does not freeze on WIN: the crown has no outlet, so winner:true is
sticky and the mountain keeps drinking. A match-reset op is v1 debt.

Chat v1 (LW6, S19's spec, 2026-09-30): the world speaks the CHAT contract
(protocol_table.CHAT_TABLE: the four v0 verbs plus say/whisper, so every
existing path is unchanged). `say` rides the ordinary stage->tick channel
— staged at receipt, applied in arrival order, event "user: text", zero
new wire ops, determinism law untouched. `whisper` ('user|text') is the
one verb applied at receipt: it mutates no world state, so it lands on
the per-sid direct outbox (drain_direct) outside the canonical tick and
never appears in tick events. Text law: empty or >240 chars -> BAD_TEXT.
Any registered session can say or whisper — a bot (a fish, the innkeeper)
registers via register_session and rides the same channel as a player.

Actor classes (Q23, 2026-10-01, watch/inbox/mountain_climb/
FIFTY_QUESTIONS_ANSWERED.md): authored rows (kind action/whisper) whose
user is a registered bot carry actor_class "bot" INSIDE the hashed body;
player rows omit the field, so absent == "player" and every pre-Q23 row
in every log file and save doc stays legal and replays byte-for-byte
(the grandfather law: classify, never rewrite). actor_class_of() reads
the BOT_USERS registry; classification is a PURE FUNCTION OF THE USER
NAME (never the sid, never the roster) because action rows record only
`user` and persistence replay re-derives rows through _apply/_whisper
under exact byte-equality — the class must re-derive from the row's own
user field alone or saves stop booting.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402
from server.protocol_table import CHAT_TABLE  # noqa: E402

GENESIS = "0" * 64
DEFAULT_JOIN_AT = "spring"

# Q23 actor classes: the tape itself must be able to tell a bot's hand from
# a player's — "innkeeper" is just a user string, so before this the GWAP
# agreement rounds could not exclude the bot from tape evidence. Values are
# exactly "player" | "bot"; a row that carries no actor_class IS a player
# row (the structural default every pre-Q23 row relies on).
ACTOR_PLAYER = "player"
ACTOR_BOT = "bot"
# Seeded with the LW8 innkeeper (server/innkeeper.py INNKEEPER_USER, the one
# bot the estate ships). register_bot() declares any other bot (a fish) at
# boot, before it acts, so its rows and their replays agree on the class.
BOT_USERS: set[str] = {"innkeeper"}


def register_bot(user: str) -> None:
    """Declare a user name a bot: its authored rows carry actor_class "bot".

    Law: call at boot BEFORE the bot acts. Save-doc replay re-derives
    actor_class from this registry, so a bot registered after its rows were
    written makes those rows replay as player rows and the doc refuses to
    boot (fail-closed, the replay byte-equality law) rather than misclassify.
    """
    BOT_USERS.add(user)


def actor_class_of(user: str) -> str:
    """The row-level actor class for a user name (pure, deterministic).

    Player is the structural default: rows without an actor_class field are
    player rows, so historical rows and unchanged callers stay legal without
    rewriting a byte. Bot rows stamp the field explicitly, which puts it
    inside the sha-covered body (tamper-evident with the rest of the row).
    """
    return ACTOR_BOT if user in BOT_USERS else ACTOR_PLAYER

# LW6 chat v1 (S19's spec): the world speaks the CHAT contract (the DEFAULT
# v0 rows plus say/whisper, a strict superset compiled in protocol_table —
# PROTOCOL_DIGEST stays byte-identical; CHAT_DIGEST is the new version).
# Say rides the existing action op and the tick; whisper bypasses the tick.
VERBS = CHAT_TABLE.verbs
MAX_SAY = 240  # chars; the chat v1 text law (empty or over-length -> BAD_TEXT)


def build_mountain_graph() -> WaterGraph:
    """The Mountain slice's board, verbatim (roblox_to_godot game.gd)."""
    g = WaterGraph()
    g.add_node("spring", elev=10, volume=6)
    g.add_node("terrace", elev=6)
    g.add_node("gate1", elev=5, kind="xor")
    g.add_node("hollow", elev=3, volume=2)
    g.add_node("waste", elev=0, kind="waste")
    g.add_node("crown", elev=14, kind="cold")
    g.add_pipe("p_spring", "spring", "gate1", cap=1)
    g.add_pipe("p_terrace", "terrace", "gate1", cap=1)
    g.add_pipe("p_out", "gate1", "hollow", cap=1)
    g.add_pipe("p_drain", "hollow", "waste", cap=1)
    g.add_pipe("p_bypass", "spring", "terrace", cap=1, siphon=True, crest=2, open_=False)
    return g


def row_sha(row: dict[str, Any]) -> str:
    body = {k: v for k, v in row.items() if k != "sha"}
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def verify_log_rows(rows: list[dict[str, Any]]) -> bool:
    """Chain check: seq strictly increments from 1, prev links, hashes hold."""
    prev = GENESIS
    expected_seq = 1
    for row in rows:
        if row.get("seq") != expected_seq or row.get("prev") != prev:
            return False
        if row.get("sha") != row_sha(row):
            return False
        prev = row["sha"]
        expected_seq += 1
    return True


def load_log_rows(path: Path | str) -> list[dict[str, Any]]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    if not verify_log_rows(rows):
        raise ValueError(f"{path}: event log chain is corrupt, refusing to append")
    return rows


class MountainWorld:
    WIN_CROWN = 4
    TICK_MS = 800

    def __init__(self, log_path: Path | str | None = None,
                 save_path: Path | str | None = None,
                 save_interval: int = 0) -> None:
        self.graph = build_mountain_graph()
        self.pending: list[dict[str, Any]] = []
        self.roster: dict[str, dict[str, str]] = {}   # sid -> {user, at}
        self.scores: dict[str, int] = {}
        self.winner = False
        # LW6 whisper outbox: direct lines waiting for ONE sid each, outside
        # the canonical tick. Never broadcast, never in tick events.
        self.direct: list[dict[str, Any]] = []
        self.rows: list[dict[str, Any]] = []
        self._seq = 0
        self._prev = GENESIS
        self.log_path = Path(log_path) if log_path is not None else None
        self.save_path = Path(save_path) if save_path is not None else None
        self.save_interval = int(save_interval or 0)
        self._log_fh = None
        if self.log_path is not None:
            if self.log_path.exists():
                # continue the on-disk chain: seq and prev resume from file
                self.rows = load_log_rows(self.log_path)
                if self.rows:
                    self._seq = self.rows[-1]["seq"]
                    self._prev = self.rows[-1]["sha"]
            else:
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self._log_fh = open(self.log_path, "a", encoding="utf-8")
        if self.save_path is not None and self.save_path.exists():
            # S18 v1 replay-on-boot (LW5): restore world state by replaying
            # the save doc's chained tail; server/persistence.py owns the law
            from server.persistence import restore_world
            restore_world(self, self.save_path)

    # ---------------------------------------------------------- sessions ----
    def register_session(self, sid: str, user: str, at: str = DEFAULT_JOIN_AT) -> None:
        self.roster[sid] = {"user": user, "at": at}

    # -------------------------------------------------------------- view ----
    def node_volumes(self) -> dict[str, int]:
        return {name: n.volume for name, n in self.graph.nodes.items()}

    def snapshot(self) -> dict[str, Any]:
        snap = dict(self.graph.to_spec())
        snap["winner"] = self.winner
        snap["win_crown"] = self.WIN_CROWN
        snap["tick_ms"] = self.TICK_MS
        snap["roster"] = {sid: dict(info) for sid, info in self.roster.items()}
        snap["scores"] = dict(self.scores)
        return snap

    def wettest_pool(self) -> str:
        """The school's pool: wettest non-waste node, ties by board order
        (the Godot slice's _wettest_pool law, deterministic)."""
        best, best_v = "", 0
        for name, node in self.graph.nodes.items():
            if node.kind == "waste":
                continue
            if node.volume > best_v:
                best, best_v = name, node.volume
        return best

    # ------------------------------------------------------------ actions ----
    def validate(self, sid: str, verb: str, target: str) -> tuple[bool, str | None]:
        """(ok, why). Validation reads current world state; the physics may
        still dry a pool between receipt and application, which _apply
        handles honestly (boil lifts 0 and the row says so)."""
        if sid not in self.roster:
            return False, "UNKNOWN_SID"
        if verb not in VERBS:
            return False, "UNKNOWN_VERB"
        if verb == "say":
            # LW6: target IS the text — free-form, never a node name
            if not target or len(target) > MAX_SAY:
                return False, "BAD_TEXT"
            return True, None
        if verb == "whisper":
            # LW6: target is 'user|text' (first '|' splits; the text may
            # contain more). Malformed or over-length -> BAD_TEXT, a user
            # with no registered session -> UNKNOWN_TARGET.
            to_user, sep, text = target.partition("|")
            if not sep or not to_user or not text or len(text) > MAX_SAY:
                return False, "BAD_TEXT"
            if not any(info["user"] == to_user for info in self.roster.values()):
                return False, "UNKNOWN_TARGET"
            return True, None
        if verb == "valve":
            if target not in self.graph.pipes:
                return False, "UNKNOWN_TARGET"
            return True, None
        if target not in self.graph.nodes:
            return False, "UNKNOWN_TARGET"
        if verb in ("boil", "tag") and self.graph.nodes[target].volume <= 0:
            return False, "DRY_POOL"
        return True, None

    def stage(self, sid: str, verb: str, target: str) -> dict[str, Any]:
        """Validate and stage a client action. Returns the wire reply
        (ack or typed reject). Staged actions apply at the next tick.
        Whisper is the one exception (LW6): it mutates nothing, so it is
        delivered as a direct line at receipt, outside the canonical tick."""
        ok, why = self.validate(sid, verb, target)
        if not ok:
            return {"op": "reject", "why": why, "verb": verb, "target": target}
        user = self.roster[sid]["user"]
        if verb == "whisper":
            return self._whisper(user, target)
        self.pending.append({"sid": sid, "user": user, "verb": verb, "target": target})
        return {
            "op": "ack",
            "verb": verb,
            "target": target,
            "user": user,
            "applies_at_tick": self.graph.tick_count + 1,
        }

    # ---------------------------------------------------------- chat (LW6) ----
    def _whisper(self, user: str, target: str) -> dict[str, Any]:
        """Deliver one whisper: a direct line onto the outbox for every sid
        registered to the target user, then one audit row. OUTSIDE the
        canonical tick by construction: no pending entry, no tick event,
        no world mutation — the direct line is readable by the target sid
        alone (drain_direct); the log keeps the server-side audit trail."""
        to_user, _, text = target.partition("|")
        to_sids = [s for s, info in self.roster.items() if info["user"] == to_user]
        for to_sid in to_sids:
            self.direct.append(
                {"to": to_sid, "msg": {"op": "whisper", "from": user, "text": text}})
        row = {
            "kind": "whisper",
            "tick": self.graph.tick_count + 1,
            "user": user,
            "verb": "whisper",
            "target": target,
            "event": f"{user} whispers to {to_user}.",
        }
        if actor_class_of(user) != ACTOR_PLAYER:
            # Q23: only bot rows carry the field; a player row omits it
            # (absent == "player") so pre-Q23 rows replay byte-identically.
            row["actor_class"] = ACTOR_BOT
        self._append_row(row)
        return {"op": "ack", "verb": "whisper", "target": target, "user": user}

    def drain_direct(self, sid: str) -> list[dict[str, Any]]:
        """Take the direct lines waiting for THIS sid (whisper v1). Delivery
        is per-sid, never broadcast: the call returns lines for the named
        session only and leaves everyone else's untouched."""
        theirs: list[dict[str, Any]] = []
        keep: list[dict[str, Any]] = []
        for d in self.direct:
            (theirs if d["to"] == sid else keep).append(d)
        self.direct = keep
        return [d["msg"] for d in theirs]

    # --------------------------------------------------------------- tick ----
    def tick(self) -> dict[str, Any]:
        """One authoritative tick: staged actions apply in arrival order,
        then the physics runs, then the tick row is chained to the log.
        Returns the broadcast payload."""
        tick_no = self.graph.tick_count + 1
        events: list[str] = []
        for act in self.pending:
            events.append(self._apply(act, tick_no))
        self.pending.clear()
        events.extend(self.graph.tick())
        if self.graph.nodes["crown"].volume >= self.WIN_CROWN:
            self.winner = True
        row = self._append_row({
            "kind": "tick",
            "tick": tick_no,
            "events": events,
            "nodes": self.node_volumes(),
            "winner": self.winner,
        })
        if (self.save_path is not None and self.save_interval > 0
                and tick_no % self.save_interval == 0):
            # S18 v1 (LW5): periodic kind:snapshot row + save doc, same chain.
            # Fires at END of tick, after pending drained, so the snapshot
            # never catches half-applied actions.
            from server.persistence import save as persist_save
            persist_save(self, self.save_path)
        return {
            "op": "tick",
            "n": row["tick"],
            "nodes": row["nodes"],
            "events": events,
            "winner": self.winner,
        }

    def _apply(self, act: dict[str, Any], tick_no: int) -> str:
        user, verb, target = act["user"], act["verb"], act["target"]
        if verb == "boil":
            lifted = self.graph.boil(target, 1)
            if lifted:
                ev = f"{user} boils 1 at {target}; it rises."
            else:
                ev = f"{user} boils at {target}: pool went dry between ask and tick."
        elif verb == "valve":
            pipe = self.graph.pipes[target]
            if pipe.open:
                self.graph.close(target)
                ev = f"{user} shuts {target}."
            else:
                self.graph.open(target)
                ev = f"{user} opens {target}."
        elif verb == "join":
            self.roster[act["sid"]]["at"] = target
            ev = f"{user} joins at {target}."
        elif verb == "say":
            # LW6: the event IS the chat line, exactly the spec shape
            ev = f"{user}: {target}"
        else:  # tag: the school follows water; a dry pool holds no fish
            self.scores[user] = self.scores.get(user, 0) + 1
            ev = f"{user} tags a fish at {target} (score {self.scores[user]})."
        row = {
            "kind": "action",
            "tick": tick_no,
            "user": user,
            "verb": verb,
            "target": target,
            "event": ev,
        }
        if actor_class_of(user) != ACTOR_PLAYER:
            # Q23: only bot rows carry the field — it lands in the dict
            # BEFORE _append_row computes row_sha, so actor_class is
            # tamper-evident with the rest of the row. A player row omits
            # it (absent == "player"), which keeps every pre-Q23 row and
            # its replay byte-identical (the grandfather law).
            row["actor_class"] = ACTOR_BOT
        self._append_row(row)
        return ev

    # ---------------------------------------------------------------- log ----
    def _append_row(self, row: dict[str, Any]) -> dict[str, Any]:
        self._seq += 1
        row = {"seq": self._seq, "prev": self._prev, **row}
        row["sha"] = row_sha(row)
        self._prev = row["sha"]
        self.rows.append(row)
        if self._log_fh is not None:
            self._log_fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
            self._log_fh.flush()
        return row

    def verify_log(self) -> bool:
        return verify_log_rows(self.rows)

    def close(self) -> None:
        if self._log_fh is not None:
            self._log_fh.close()
            self._log_fh = None
