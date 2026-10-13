"""verdict_feed -- the return leg: world ticks -> gwap payload -> gps ledger.

The tie-it-all move's second leg (X11, 2026-09-29). The first leg
(mag/gwap_to_gps.py, Mickey17 Wave 1) built the fail-closed bridge from gwap
session ledgers to the gps capability ledger, but only synthetic demo
sessions ever crossed it. This module is the bridge's first PRODUCTION meal:
after each MountainWorld tick the feed mints one gwap payload describing
that tick and drives it through the bridge, so the estate's own world server
becomes a measured (model_id, task_shape) row in the router's truth table.

WHAT ONE TICK BECOMES:
  scene_id  the tick's own gwap session id, "{session_id}.t{tick:04d}" --
            ONE gwap session per tick, so every feed_session walk covers
            exactly one fresh row and a re-feed can never double-count a
            verdict (the per-tick file plus the TICK_SESSION_EXISTS guard
            make one-verdict-per-tick structural, not conventional).
  claims    the tick's ACTION rows (kind=="action", tick==n), each mapped
            through the gwap_mud event mapping (closed verb table below).
            Physics narration ("Junction gate1 holds...") has no author and
            mints no claims: gwap claims are authored acts, and the closed
            {move, attack, kill} vocabulary cannot express world physics.
            Q23 (2026-10-01): feed_tick(exclude_bots=True) builds claims
            from PLAYER action rows only (actor_class absent or "player"),
            so agreement scoring can exclude the house bot's own hands;
            rows without an actor_class field are players (grandfathered).
  verdict   VERIFIED_AGREE when world.verify_log() holds, DISPUTE when it
            does not. The agreement is real, not decorative: the intent
            struct is what the game loop staged (arrival order), the report
            struct is the chain's reconstruction (dedup + reversed); a
            broken chain files one disjoint claim ("chain broke verify"),
            scores 0.0, and the engine itself returns DISPUTE. The gps
            verdict is therefore literally the chain check: pass means the
            log verified, fail means it was tampered with.

KEY-BOUND ATTRIBUTION (Q27, 2026-10-01, watch/inbox/mountain_climb/
FIFTY_QUESTIONS_ANSWERED.md; the Q05 dependency landed in server/server.py
V7): a verdict row is attributable to a KEY, not just an unkeyed sid. The
feed's sid (its session_id, the sid the per-tick gwap sessions hang off)
may carry a recorded identity binding -- the server's
session_identities[sid] = {"user", "fingerprint"} record, passed in as
identities=. When it does, feed_tick stamps identity_fingerprint into the
gwap payload BEFORE the ledger row is hashed (the actor_class precedent,
server/world.py _apply: the field goes into the dict before the sha is
computed), so the fingerprint is tamper-evident with the rest of the row
and the gps evidence hash (the gwap row's row_sha256) covers it: the
auditor walk verdict_log -> gwap row -> world tick grows one honest step,
payload.identity_fingerprint -> the key. meter_credit.receipt_sha256 is
recomputed over the extended body so the gwap_payload receipt law ("the
credit is earned by exactly these bytes") stays true. Unbound sids (the
compat default under allow_unbound_hello=True) keep feeding byte-identical
pre-Q27 rows: the payload OMITS the field (absent == unkeyed, the
grandfather law) and the feed report says identity_fingerprint: None, so
bound and unbound rows stay distinguishable without rewriting history.
Grammar cap (honest residue): gwap's session-id regex bounds the per-tick
scene id at 64 chars TOTAL, so a feed's session_id must leave room for
the ".t{tick:04d}" suffix; a granted 64-hex sid cannot ride the scene
grammar as-is (alias or shorten it when binding -- the cap itself lives
in mag/gwap_payload.py, outside this module's ownership).

WHY THE COLLUSION FINGERPRINT CAN NEVER FIRE HERE (proof, not hope): the
fingerprint needs the two full claim sequences EQUAL with min length >= 2.
The report sequence is reverse(dedup(intent)). Equality would require
intent to be duplicate-free (else the lengths differ) and a palindrome; a
duplicate-free palindrome of length >= 2 cannot exist, because its
symmetric pair repeats a triple. Duplicates also collapse in
agreement_score (per-triple max weight), so the score is exactly 1.0
whenever both sides carry the same triple set. A verified tick therefore
ALWAYS lands VERIFIED_AGREE, and no downstream consumer has to trust this
comment to believe it.

WIRING (world -> gps):
  model_id    "mountain-world-v0" -- the server under measurement (also the
              replay_tape engine_version; override both roles separately if
              a fork ever needs to).
  task_shape  "world-tick"
  evidence    the gwap row's row_sha256 (the bridge law), and the payload's
              replay_tape_ref.sha256 is the WORLD tick row's own sha, so an
              auditor walks a gps verdict_log row -> its gwap row -> the
              exact world tick that earned the verdict, all offline.

FAIL-CLOSED LAWS: feed_tick refuses when the world's last log row is not
the tick row being fed (NOT_A_TICK_ROW / EMPTY_LOG); refuses unknown world
verbs (UNKNOWN_WORLD_VERB) and unprojected join targets (UNKNOWN_NODE)
before any payload exists; refuses to re-feed a tick whose gwap session
file already exists (TICK_SESSION_EXISTS); refuses a recorded identity
binding with no usable fingerprint (BAD_IDENTITY_BINDING) before anything
is minted; an idle tick (no action rows)
scores nothing (skip IDLE_TICK) because an empty claim set is "no evidence,
no agreement", not a failure. Clock: one touch -- ts_utc is injected, and
only defaults to now inside feed_tick.

Run (demo: 5 world ticks against the production gps ledger):
  python -m server.verdict_feed
"""
from __future__ import annotations

import hashlib
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.gwap_mud import claim_from_event  # noqa: E402
from mag.gwap_payload import (  # noqa: E402
    DISPUTE,
    VERIFIED_AGREE,
    SessionLedger,
    anon_id,
    build_payload,
    canonical,
    utc_now_iso,
)
from mag.gwap_to_gps import feed_session  # noqa: E402
from server.world import ACTOR_BOT, ACTOR_PLAYER  # noqa: E402
from tools.gps_mcp.ledger import CapabilityLedger  # noqa: E402

SERVER_ID = "mountain-world-v0"
TASK_SHAPE = "world-tick"
PRODUCTION_GPS_DB = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"

# The closed world-verb -> mud-action table. gwap_mud fails closed on any
# action outside {move, attack, kill}; this table is the only translation
# layer, and a world verb outside it refuses rather than invents a verb.
WORLD_VERB_TO_MUD = {
    "join": "move",     # arrival at a place
    "boil": "attack",   # striking the water
    "valve": "attack",  # throwing a pipe's switch
    "tag": "kill",      # taking the fish
}

# The board projection for move claims: (column, row) = (board order,
# elevation), both real facts of the Mountain slice's board. gwap_mud
# renders positions as integer tiles, so "ada joins at terrace" reads as
# the triple (ada, moved, tile 1 6).
NODE_TILES = {
    "spring": (0, 10),
    "terrace": (1, 6),
    "gate1": (2, 5),
    "hollow": (3, 3),
    "waste": (4, 0),
    "crown": (5, 14),
}

# The single claim the report side files when the world chain does not
# verify. Its verb can never collide with an intent claim: intent verbs
# come from the closed mud set {moved, attacked, killed}.
BROKEN_CHAIN_CLAIM = {"subject": "chain", "verb": "broke", "object": "verify"}


class VerdictFeedError(Exception):
    """Reason-coded refusal (house pattern: .reason carries the machine code)."""

    def __init__(self, reason: str, message: str = "") -> None:
        self.reason = reason
        super().__init__(message or reason)


def _require(condition: bool, reason: str, message: str) -> None:
    if not condition:
        raise VerdictFeedError(reason, message)


def mud_event(action_row: dict[str, Any]) -> dict[str, Any]:
    """One world action log row -> one mud-shaped event for gwap_mud."""
    verb = action_row.get("verb")
    _require(
        verb in WORLD_VERB_TO_MUD,
        "UNKNOWN_WORLD_VERB",
        f"world verb {verb!r} has no mud mapping",
    )
    user = action_row.get("user")
    _require(
        isinstance(user, str) and bool(user.strip()),
        "BAD_ACTION_ROW",
        "action row must carry a non-empty user",
    )
    target = action_row.get("target")
    _require(
        isinstance(target, str) and bool(target.strip()),
        "BAD_ACTION_ROW",
        "action row must carry a non-empty target",
    )
    if verb == "join":
        _require(
            target in NODE_TILES,
            "UNKNOWN_NODE",
            f"join target {target!r} has no board tile",
        )
        col, row = NODE_TILES[target]
        return {"player": {"id": user, "x": col, "y": row}, "action": "move"}
    # attack/kill carry the target id; gwap_mud reads no position for them.
    return {
        "player": {"id": user},
        "action": WORLD_VERB_TO_MUD[verb],
        "target": target,
    }


def tick_action_rows(
    world_rows: list[dict[str, Any]], tick_no: int,
    actor_class: str | None = None,
) -> list[dict[str, Any]]:
    """The structural events of one tick: its action rows, arrival order.

    Q23 (2026-10-01): actor_class filters by the row's stamped class
    ("player" | "bot"; a row with no actor_class field IS a player row,
    the grandfather default, so pre-Q23 tapes filter honestly too).
    None keeps every action row — the pre-Q23 behavior — leaving existing
    callers unchanged; pass ACTOR_PLAYER to keep players only, which is
    how agreement counting excludes the bot's own hands from the score.
    """
    return [
        r for r in world_rows
        if r.get("kind") == "action" and r.get("tick") == tick_no
        and (actor_class is None
             or r.get("actor_class", ACTOR_PLAYER) == actor_class)
    ]


def _dedup_reversed(claims: list[dict[str, str]]) -> list[dict[str, str]]:
    """First-occurrence dedup, then reverse: the report-side ordering that
    the module docstring proves can never equal the intent ordering at
    min length >= 2 (no duplicate-free palindrome of length >= 2 exists)."""
    seen: set[tuple[str, str, str, str]] = set()
    out: list[dict[str, str]] = []
    for claim in claims:
        key = (
            claim["subject"], claim["verb"],
            claim["object"], claim["qualifier"],
        )
        if key not in seen:
            seen.add(key)
            out.append(claim)
    return list(reversed(out))


class VerdictFeed:
    """Feeds one MountainWorld's ticks into the gps capability ledger.

    world is the live MountainWorld (duck-typed: .rows, .verify_log()).
    gps is a CapabilityLedger or a path to one (the bridge opens/opens it
    per feed; a shared instance is fine too). store is the directory the
    per-tick gwap session ledgers land in. identities (Q27) is the sid ->
    {user, fingerprint} registry (the server's session_identities); when it
    holds this feed's session_id, every fed row carries the key fingerprint
    inside the hashed payload.
    """

    def __init__(
        self,
        world: Any,
        gps: CapabilityLedger | str | Path,
        store: Path | str,
        *,
        session_id: str = SERVER_ID,
        model_id: str = SERVER_ID,
        task_shape: str = TASK_SHAPE,
        identities: Mapping[str, Any] | None = None,
    ) -> None:
        for name, value in (
            ("session_id", session_id),
            ("model_id", model_id),
            ("task_shape", task_shape),
        ):
            _require(
                isinstance(value, str) and bool(value.strip()),
                f"BAD_{name.upper()}",
                f"{name} must be a non-empty string",
            )
        _require(
            identities is None or isinstance(identities, Mapping),
            "BAD_IDENTITIES",
            "identities must be the sid -> {user, fingerprint} mapping "
            "(the server's session_identities) or None",
        )
        self.world = world
        self.gps = gps
        self.store = Path(store)
        self.session_id = session_id
        self.model_id = model_id
        self.task_shape = task_shape
        # Q27: the identity registry this feed's sid is looked up in. The
        # server's session_identities dict is passed BY REFERENCE, so grants
        # landing after construction are seen by the next feed_tick. None
        # (the compat default) means no sid can be bound.
        self.identities = identities

    def _identity_binding(self) -> dict[str, Any] | None:
        """The key binding recorded for THIS feed's sid (Q27), or None.

        identities is keyed by sid and the feed's session_id is the sid its
        gwap sessions hang off, so the lookup answers "which key holds the
        sid this verdict row binds to". None -- no registry, or this sid
        not recorded (the unbound compat default under
        allow_unbound_hello=True) -- stays honestly unkeyed. A record that
        IS present but carries no usable fingerprint refuses typed
        (BAD_IDENTITY_BINDING) rather than minting a mislabeled row: a
        malformed binding is a wiring defect, and this feed fails closed
        on it.
        """
        if self.identities is None:
            return None
        record = self.identities.get(self.session_id)
        if record is None:
            return None
        fp = record.get("fingerprint") if isinstance(record, dict) else None
        _require(
            isinstance(fp, str) and bool(fp.strip()),
            "BAD_IDENTITY_BINDING",
            f"identities[{self.session_id!r}] must be a record carrying a "
            "non-empty fingerprint string",
        )
        return record

    def feed_tick(self, ts_utc: str | None = None, *,
                  exclude_bots: bool = False) -> dict[str, Any]:
        """Mint + feed the payload for the world's LAST tick row.

        Call once after each world.tick(). Returns the feed report; the
        gps write happens only when a verdict was minted (an idle tick
        returns a skip and touches nothing).

        Q23: exclude_bots=True builds the claim set from PLAYER action
        rows only (actor_class absent or "player"), so the house bot's
        own hands (the innkeeper's says, a fish's moves) never count as
        agreement evidence; bots_excluded in the report says how many bot
        rows were left out. Default False keeps the whole tick — the
        pre-Q23 behavior every existing caller relies on.
        """
        _require(
            bool(self.world.rows), "EMPTY_LOG", "no tick to feed yet"
        )
        tick_row = self.world.rows[-1]
        _require(
            tick_row.get("kind") == "tick",
            "NOT_A_TICK_ROW",
            "the world's last log row is not a tick row; feed after world.tick()",
        )
        tick_no = tick_row["tick"]
        # Q27: resolve the key binding BEFORE anything is minted, so a
        # malformed record refuses this feed outright (fail-closed) instead
        # of minting a row it cannot attribute honestly.
        binding = self._identity_binding()
        identity_fp = binding["fingerprint"] if binding is not None else None
        all_actions = tick_action_rows(self.world.rows, tick_no)
        bots_excluded = (
            sum(1 for r in all_actions
                if r.get("actor_class", ACTOR_PLAYER) == ACTOR_BOT)
            if exclude_bots else 0
        )
        actions = (
            tick_action_rows(self.world.rows, tick_no,
                             actor_class=ACTOR_PLAYER)
            if exclude_bots else all_actions
        )
        if not actions:
            return {
                "tick": tick_no,
                "scene_id": None,
                "chain_verified": self.world.verify_log(),
                "verdict": None,
                "claims": 0,
                "bots_excluded": bots_excluded,
                "fed": 0,
                "skip": "IDLE_TICK",
                "evidence_hash": None,
                "ledger_path": None,
                "identity_fingerprint": identity_fp,
                "feed": None,
            }

        chain_ok = self.world.verify_log()
        ts = utc_now_iso() if ts_utc is None else ts_utc
        robber = anon_id(f"{self.session_id}:world-intent")
        cop = anon_id(f"{self.session_id}:chain-report")
        intent_claims = [claim_from_event(mud_event(r)) for r in actions]
        report_claims = (
            _dedup_reversed(intent_claims) if chain_ok
            else [dict(BROKEN_CHAIN_CLAIM)]
        )
        tick_sid = f"{self.session_id}.t{tick_no:04d}"
        payload = build_payload(
            scene_id=tick_sid,
            intent_struct={"author": robber, "claims": intent_claims},
            report_struct={"author": cop, "claims": report_claims},
            participants=[
                {"anon_id": robber, "role": "robber"},
                {"anon_id": cop, "role": "cop"},
            ],
            consent=True,
            created_utc=ts,
            replay_tape_ref={
                "sha256": tick_row["sha"], "engine_version": SERVER_ID
            },
        )
        # The docstring proof says the engine MUST return VERIFIED_AGREE on a
        # verified chain and DISPUTE on a broken one; if a future edit breaks
        # the dedup+reverse ordering (or the broken claim), refuse rather
        # than mis-score the chain check.
        expected = VERIFIED_AGREE if chain_ok else DISPUTE
        _require(
            payload["verdict"] == expected,
            "VERDICT_MISMATCH",
            f"engine returned {payload['verdict']!r} for a "
            f"{'verified' if chain_ok else 'broken'} chain",
        )
        if binding is not None:
            # Q27: the fingerprint lands inside the payload BEFORE
            # ledger.append computes row_sha256 (the actor_class precedent,
            # server/world.py _apply -- the field enters the dict before
            # the sha), so a bound verdict row is tamper-evident in its key
            # attribution and the gps evidence hash (this row's sha) covers
            # it. Unbound rows OMIT the field (absent == unkeyed, the
            # grandfather law), keeping pre-Q27 bytes legal and distinct.
            payload["identity_fingerprint"] = identity_fp
            # The gwap_payload receipt law: meter_credit.receipt_sha256
            # hashes the canonical payload BODY (every field except
            # meter_credit) -- recompute it over the extended body so the
            # credit stays "earned by exactly these bytes". Same formula as
            # build_payload/_row_hash: sha256(canonical(...)).
            body = {k: v for k, v in payload.items() if k != "meter_credit"}
            payload["meter_credit"]["receipt_sha256"] = hashlib.sha256(
                canonical(body).encode("utf-8")
            ).hexdigest()
        ledger = SessionLedger(tick_sid, store=self.store)
        _require(
            not ledger.path.exists(),
            "TICK_SESSION_EXISTS",
            f"{ledger.path.name} already holds a fed tick; one verdict per tick",
        )
        ledger.append(payload, ts_utc=ts)
        feed = feed_session(
            ledger.path,
            self.gps,
            task_shape=self.task_shape,
            scene_to_model={tick_sid: self.model_id},
        )
        return {
            "tick": tick_no,
            "scene_id": tick_sid,
            "chain_verified": chain_ok,
            "verdict": payload["verdict"],
            "claims": len(intent_claims),
            "bots_excluded": bots_excluded,
            "fed": feed["fed"],
            "skip": None,
            "evidence_hash": (
                feed["evidence_hashes"][0] if feed["evidence_hashes"] else None
            ),
            "ledger_path": str(ledger.path),
            "identity_fingerprint": identity_fp,
            "feed": feed,
        }


# -- demo ---------------------------------------------------------------------------


def _gps_counts(gps_path: Path) -> tuple[int, int, dict[str, Any] | None]:
    ledger = CapabilityLedger(gps_path)
    try:
        mine = ledger.verdict_log_rows(SERVER_ID, TASK_SHAPE)
        total = ledger.connection().execute(
            "SELECT COUNT(*) AS c FROM verdict_log"
        ).fetchone()["c"]
        cap = ledger.report_capability(SERVER_ID, TASK_SHAPE)
    finally:
        ledger.close()
    return len(mine), int(total), cap


def _demo(gps_db: str | None = None) -> None:
    import tempfile

    from server.world import MountainWorld

    gps_path = Path(gps_db) if gps_db else PRODUCTION_GPS_DB
    mine_before, total_before, _ = _gps_counts(gps_path)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        world = MountainWorld(log_path=tmp / "world_log.jsonl")
        try:
            world.register_session("s1", "ada")
            feed = VerdictFeed(world, gps_path, store=tmp / "gwap")
            # a played session: four action ticks, then one pure-physics tick
            script = [
                ("boil", "spring"), ("tag", "hollow"),
                ("valve", "p_bypass"), ("join", "terrace"),
                None,
            ]
            for step in script:
                if step is not None:
                    world.stage("s1", step[0], step[1])
                world.tick()
                rep = feed.feed_tick()
                label = rep["verdict"] or rep["skip"]
                print(
                    f"tick {rep['tick']:>2}  verdict={label:<13} "
                    f"claims={rep['claims']}  fed={rep['fed']}"
                )
        finally:
            world.close()  # release the log handle before the tmpdir cleanup
    mine_after, total_after, cap = _gps_counts(gps_path)
    print(f"gps ledger: {gps_path}")
    print(
        f"  ({SERVER_ID}, {TASK_SHAPE}) verdict_log rows: "
        f"{mine_before} -> {mine_after}"
    )
    print(f"  total verdict_log rows: {total_before} -> {total_after}")
    print(f"  capability row: {cap}")


if __name__ == "__main__":
    _demo()
