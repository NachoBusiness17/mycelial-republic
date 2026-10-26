"""tests for server/verdict_feed.py -- the world -> gwap -> gps return leg.

Laws under test: a played session feeds exactly one gps verdict per ACTION
tick under (mountain-world-v0, world-tick), and that verdict IS the chain
check (pass means the world log verified); an idle tick scores nothing; a
tampered world chain lands DISPUTE (verdict 0: a fail row, never a minted
VERIFIED_AGREE); duplicate-claim ticks still verify (the dedup+reverse
proof, guarded by VERDICT_MISMATCH); the mud mapping is closed and refuses
unknown verbs and unprojected nodes; a tick can never be fed twice; the
gps evidence hash walks back to the gwap row and the gwap tape ref walks
back to the world tick row.

Q27 (key-bound attribution, the Q05 dependency landed in server/server.py
V7): when the feed's sid carries a recorded identity binding (the server's
session_identities[sid] = {"user", "fingerprint"}), the fed row carries the
key fingerprint INSIDE the hashed payload -- bound rows verify, tampering
the fingerprint breaks the chain verify, and unbound sids (the compat
default) keep feeding rows that honestly omit the field (absent ==
unkeyed, the grandfather law) while the report says None.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.gwap_payload import (  # noqa: E402
    DISPUTE,
    VERIFIED_AGREE,
    GwapError,
    SessionLedger,
    canonical,
    verify_chain_file,
)
from server.verdict_feed import (  # noqa: E402
    NODE_TILES,
    SERVER_ID,
    TASK_SHAPE,
    VerdictFeed,
    VerdictFeedError,
    mud_event,
    tick_action_rows,
)
from server.world import ACTOR_BOT, ACTOR_PLAYER, MountainWorld  # noqa: E402
from tools.gps_mcp.ledger import CapabilityLedger  # noqa: E402

UTC = "2026-09-29T12:00:00Z"
PLAYED = [("boil", "spring"), ("tag", "hollow"),
          ("valve", "p_bypass"), ("join", "terrace")]

# Q27 fixtures: a sid-shaped session id and two clearly distinct (fake,
# never-real) ssh key fingerprints. NOTE the grammar cap: a granted sid is
# 64 hex chars but gwap's _SESSION_ID_RE caps the per-tick scene id at 64
# chars TOTAL ("{sid}.t{tick:04d}"), so a feed's session_id must leave
# room for the tick suffix -- 32 hex is the shape used here (residue: the
# cap itself lives in mag/gwap_payload.py, outside this lane's ownership).
BOUND_SID = "f" * 32
KEY_FP = "SHA256:q27BoundFixtureFingerprintNotARealKey0000000000000"
EVIL_FP = "SHA256:q27MalloryFingerprintDefinitelyNotTheBoundOne000000"


@pytest.fixture()
def gps(tmp_path):
    ledger = CapabilityLedger(tmp_path / "gps.db")
    yield ledger
    ledger.close()


@pytest.fixture()
def world(tmp_path):
    w = MountainWorld(log_path=tmp_path / "world_log.jsonl")
    w.register_session("s1", "ada")
    yield w
    w.close()


def refuses(exc_info, reason):
    assert exc_info.value.reason == reason


def play(world, gps, tmp_path, steps):
    """Stage (or idle) + tick + feed, one report per step."""
    feed = VerdictFeed(world, gps, store=tmp_path / "gwap")
    out = []
    for step in steps:
        if step is not None:
            assert world.stage("s1", step[0], step[1])["op"] == "ack"
        world.tick()
        out.append(feed.feed_tick(ts_utc=UTC))
    return out


def gwap_payload(tmp_path, scene_id):
    return SessionLedger(scene_id, store=tmp_path / "gwap").rows[0]["payload"]


# -- the played session: the meter's production meal --------------------------------


def test_played_session_produces_gps_rows(world, gps, tmp_path):
    reps = play(world, gps, tmp_path, PLAYED)

    assert [r["verdict"] for r in reps] == [VERIFIED_AGREE] * 4
    assert all(r["fed"] == 1 and r["skip"] is None for r in reps)
    assert [r["scene_id"] for r in reps] == [
        f"{SERVER_ID}.t{i:04d}" for i in (1, 2, 3, 4)
    ]
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 4)
    logged = gps.verdict_log_rows(SERVER_ID, TASK_SHAPE)
    assert len(logged) == 4
    assert all(r["verdict"] == 1 for r in logged)

    # evidence law: the hash is the gwap row's row_sha256, so an auditor
    # walks verdict_log -> gwap row -> world tick offline
    first = SessionLedger(reps[0]["scene_id"], store=tmp_path / "gwap").rows[0]
    assert logged[0]["evidence_hash"] == first["row_sha256"]


def test_claims_are_the_mud_mapping_of_the_tick_actions(world, gps, tmp_path):
    world.stage("s1", "join", "terrace")
    world.tick()
    rep = VerdictFeed(world, gps, store=tmp_path / "gwap").feed_tick(ts_utc=UTC)

    payload = gwap_payload(tmp_path, rep["scene_id"])
    assert payload["intent_struct"]["claims"] == [
        {"subject": "ada", "verb": "moved",
         "object": f"tile {NODE_TILES['terrace'][0]} {NODE_TILES['terrace'][1]}",
         "qualifier": ""},
    ]
    # the tape ref binds the payload to the exact world tick row
    assert payload["replay_tape_ref"]["sha256"] == world.rows[-1]["sha"]


def test_idle_tick_scores_nothing(world, gps, tmp_path):
    reps = play(world, gps, tmp_path, PLAYED + [None])

    assert reps[-1]["skip"] == "IDLE_TICK"
    assert reps[-1]["verdict"] is None and reps[-1]["fed"] == 0
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 4)  # untouched


# -- the tampered chain refuses to pass ----------------------------------------------


def test_tampered_chain_lands_dispute_never_verified_agree(world, gps, tmp_path):
    play(world, gps, tmp_path, PLAYED[:2])
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 2)

    world.rows[0]["user"] = "mallory"  # hash now lies; no re-fix
    assert world.verify_log() is False
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    world.tick()
    feed = VerdictFeed(world, gps, store=tmp_path / "gwap")
    rep = feed.feed_tick(ts_utc=UTC)

    assert rep["chain_verified"] is False
    assert rep["verdict"] == DISPUTE  # the engine itself, not an override
    assert gwap_payload(tmp_path, rep["scene_id"])["verdict"] == DISPUTE
    logged = gps.verdict_log_rows(SERVER_ID, TASK_SHAPE)
    assert logged[-1]["verdict"] == 0  # fail row: the tamper is recorded
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (2 / 3, 3)


def test_tampered_gwap_ledger_refuses_through_the_bridge(world, gps, tmp_path):
    world.stage("s1", "boil", "spring")
    world.tick()
    feed = VerdictFeed(world, gps, store=tmp_path / "gwap")
    rep = feed.feed_tick(ts_utc=UTC)
    path = Path(rep["ledger_path"])
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace("ada", "evil-ada")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # the bridge's own fail-closed law: a tampered gwap file refuses with
    # the gps ledger untouched by THAT walk (the earlier honest row stands)
    from mag.gwap_to_gps import GwapToGpsError, feed_session

    with pytest.raises(GwapToGpsError) as ei:
        feed_session(path, gps, task_shape=TASK_SHAPE,
                     scene_to_model={rep["scene_id"]: SERVER_ID})
    refuses(ei, "BROKEN_CHAIN")
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 1)


# -- the collusion-proof ordering ----------------------------------------------------


def test_duplicate_claims_in_one_tick_still_verify(world, gps, tmp_path):
    # two identical actions in one tick: the claim multiset is a palindrome,
    # the exact case the dedup+reverse ordering exists for
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    world.tick()
    rep = VerdictFeed(world, gps, store=tmp_path / "gwap").feed_tick(ts_utc=UTC)

    assert rep["claims"] == 2
    assert rep["verdict"] == VERIFIED_AGREE  # not CHALLENGE, not a skip
    assert rep["fed"] == 1


def test_two_distinct_claims_in_one_tick_verify(world, gps, tmp_path):
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    assert world.stage("s1", "tag", "hollow")["op"] == "ack"
    world.tick()
    rep = VerdictFeed(world, gps, store=tmp_path / "gwap").feed_tick(ts_utc=UTC)

    assert rep["claims"] == 2
    assert rep["verdict"] == VERIFIED_AGREE
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 1)


# -- fail-closed refusals -----------------------------------------------------------


def test_feed_before_any_tick_refuses(world, gps, tmp_path):
    feed = VerdictFeed(world, gps, store=tmp_path / "gwap")
    with pytest.raises(VerdictFeedError) as ei:
        feed.feed_tick()
    refuses(ei, "EMPTY_LOG")
    assert not gps.task_shape_has_history(TASK_SHAPE)


def test_staged_but_unticked_action_refuses(world, gps, tmp_path):
    # staged actions do not touch the log until the tick applies them, so a
    # pre-tick feed meets an empty log
    world.stage("s1", "boil", "spring")
    with pytest.raises(VerdictFeedError) as ei:
        VerdictFeed(world, gps, store=tmp_path / "gwap").feed_tick()
    refuses(ei, "EMPTY_LOG")
    assert not gps.task_shape_has_history(TASK_SHAPE)


def test_trailing_non_tick_row_refuses(world, gps, tmp_path):
    # defensive guard: a log whose last row is not a tick row (unreachable
    # through the public API, reachable through log surgery) refuses
    world.rows.append({"seq": 99, "prev": "0" * 64, "kind": "action",
                       "tick": 99, "user": "ada", "verb": "boil",
                       "target": "spring", "event": "x", "sha": "0" * 64})
    with pytest.raises(VerdictFeedError) as ei:
        VerdictFeed(world, gps, store=tmp_path / "gwap").feed_tick()
    refuses(ei, "NOT_A_TICK_ROW")
    assert not gps.task_shape_has_history(TASK_SHAPE)


def test_a_tick_cannot_be_fed_twice(world, gps, tmp_path):
    world.stage("s1", "boil", "spring")
    world.tick()
    feed = VerdictFeed(world, gps, store=tmp_path / "gwap")
    assert feed.feed_tick(ts_utc=UTC)["fed"] == 1

    with pytest.raises(VerdictFeedError) as ei:
        feed.feed_tick(ts_utc=UTC)
    refuses(ei, "TICK_SESSION_EXISTS")
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 1)


def test_mud_mapping_is_closed():
    assert mud_event({"user": "ada", "verb": "boil", "target": "spring"}) == {
        "player": {"id": "ada"}, "action": "attack", "target": "spring",
    }
    assert mud_event({"user": "ada", "verb": "tag", "target": "hollow"}) == {
        "player": {"id": "ada"}, "action": "kill", "target": "hollow",
    }
    col, row = NODE_TILES["terrace"]
    assert mud_event({"user": "ada", "verb": "join", "target": "terrace"}) == {
        "player": {"id": "ada", "x": col, "y": row}, "action": "move",
    }
    with pytest.raises(VerdictFeedError) as ei:
        mud_event({"user": "ada", "verb": "dance", "target": "spring"})
    refuses(ei, "UNKNOWN_WORLD_VERB")
    with pytest.raises(VerdictFeedError) as ei:
        mud_event({"user": "ada", "verb": "join", "target": "mars"})
    refuses(ei, "UNKNOWN_NODE")


def test_custom_model_and_shape_land_under_their_own_key(world, gps, tmp_path):
    world.stage("s1", "boil", "spring")
    world.tick()
    feed = VerdictFeed(
        world, gps, tmp_path / "gwap", model_id="mw-fork", task_shape="tick-x",
    )
    rep = feed.feed_tick(ts_utc=UTC)

    assert rep["verdict"] == VERIFIED_AGREE
    assert gps.get_rate("mw-fork", "tick-x") == (1.0, 1)
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) is None


# -- Q23: agreement counting can exclude the bot ------------------------------------


def test_tick_action_rows_filters_by_actor_class():
    """Q23: one tick's action rows can be split by actor_class. A row with
    no actor_class field IS a player row (the grandfather default), so
    pre-Q23 tapes filter honestly too."""
    rows = [
        {"kind": "action", "tick": 1, "user": "ada", "verb": "boil",
         "target": "spring"},                          # pre-Q23 player row
        {"kind": "action", "tick": 1, "user": "ben", "verb": "tag",
         "target": "hollow", "actor_class": "player"},  # stamped player
        {"kind": "action", "tick": 1, "user": "innkeeper", "verb": "join",
         "target": "spring", "actor_class": "bot"},     # the bot's own hand
        {"kind": "action", "tick": 2, "user": "ada", "verb": "boil",
         "target": "spring"},                           # another tick
        {"kind": "tick", "tick": 1, "events": [], "nodes": {},
         "winner": False},                              # not an action row
    ]
    assert [r["user"] for r in tick_action_rows(rows, 1)] == [
        "ada", "ben", "innkeeper"]
    players = tick_action_rows(rows, 1, actor_class=ACTOR_PLAYER)
    assert [r["user"] for r in players] == ["ada", "ben"]
    bots = tick_action_rows(rows, 1, actor_class=ACTOR_BOT)
    assert [r["user"] for r in bots] == ["innkeeper"]


def test_feed_tick_excludes_bots_from_agreement_evidence(world, gps, tmp_path):
    """The wired consumer (Q23): with exclude_bots=True the claim set drops
    the bot's rows and scores only the player; with the default flag the
    whole tick counts, byte-for-byte the pre-Q23 behavior."""
    world.register_session("s_bot", "innkeeper")
    feed = VerdictFeed(world, gps, store=tmp_path / "gwap")

    # tick 1: one bot hand, one player hand, both mud-mappable
    assert world.stage("s_bot", "join", "spring")["op"] == "ack"
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    world.tick()
    rep = feed.feed_tick(ts_utc=UTC, exclude_bots=True)
    assert rep["claims"] == 1 and rep["bots_excluded"] == 1
    assert rep["verdict"] == VERIFIED_AGREE and rep["fed"] == 1
    payload = gwap_payload(tmp_path, rep["scene_id"])
    subjects = [c["subject"] for c in payload["intent_struct"]["claims"]]
    assert subjects == ["ada"]                  # the innkeeper never counts

    # tick 2: same shape, default feed — the bot's join counts as before
    assert world.stage("s_bot", "join", "terrace")["op"] == "ack"
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    world.tick()
    whole = feed.feed_tick(ts_utc=UTC)
    assert whole["claims"] == 2 and whole["bots_excluded"] == 0
    assert whole["verdict"] == VERIFIED_AGREE and whole["fed"] == 1

    # tick 3: a bot-only tick under exclude_bots is no evidence at all
    assert world.stage("s_bot", "join", "terrace")["op"] == "ack"
    world.tick()
    bot_only = feed.feed_tick(ts_utc=UTC, exclude_bots=True)
    assert bot_only["skip"] == "IDLE_TICK"
    assert bot_only["fed"] == 0 and bot_only["bots_excluded"] == 1

    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 2)


# -- Q27: verdict rows are attributable to a key, not just a sid ---------------------


def _bound_feed(world, gps, tmp_path, *, sid=BOUND_SID, fp=KEY_FP,
                record=None):
    """A feed whose sid carries a recorded identity binding -- the server's
    session_identities record shape (server.py V7: {"user", "fingerprint"}),
    keyed by sid exactly as the landed dependency records it."""
    return VerdictFeed(
        world, gps, tmp_path / "gwap", session_id=sid,
        identities={sid: record or {"user": "adam", "fingerprint": fp}},
    )


def test_bound_sid_row_carries_the_key_fingerprint(world, gps, tmp_path):
    """(a) a bound sid's verdict row carries the key fingerprint inside the
    HASHED payload, the chain verifies, the bridge still feeds it, and the
    receipt law survives: meter_credit.receipt_sha256 hashes the canonical
    body (every field except meter_credit) with the fingerprint in it, so
    the credit is earned by exactly these bytes."""
    world.stage("s1", "boil", "spring")
    world.tick()
    rep = _bound_feed(world, gps, tmp_path).feed_tick(ts_utc=UTC)

    assert rep["verdict"] == VERIFIED_AGREE and rep["fed"] == 1
    assert rep["identity_fingerprint"] == KEY_FP
    assert rep["scene_id"] == f"{BOUND_SID}.t0001"  # session-bound, tick-locked
    payload = gwap_payload(tmp_path, rep["scene_id"])
    assert payload["identity_fingerprint"] == KEY_FP
    # the row verifies through the ledger's own chain check
    assert SessionLedger(
        rep["scene_id"], store=tmp_path / "gwap").verify_chain() == (True, None)
    # the receipt stays honest over the extended body
    body = {k: v for k, v in payload.items() if k != "meter_credit"}
    assert hashlib.sha256(
        canonical(body).encode("utf-8")).hexdigest() \
        == payload["meter_credit"]["receipt_sha256"]
    # and the evidence walk is intact: gps evidence == this row's sha
    logged = gps.verdict_log_rows(SERVER_ID, TASK_SHAPE)
    assert logged[0]["evidence_hash"] == SessionLedger(
        rep["scene_id"], store=tmp_path / "gwap").rows[0]["row_sha256"]


def test_unbound_sid_rows_stay_legal_and_marked_unbound(world, gps, tmp_path):
    """(b) the compat default: with no registry at all (today's production
    wiring), and with a registry that simply does not hold this sid, the
    row works and is honestly unbound -- the payload OMITS the field
    (absent == unkeyed, the grandfather law; pre-Q27 bytes stay legal) and
    the report says identity_fingerprint: None."""
    world.stage("s1", "boil", "spring")
    world.tick()
    rep = VerdictFeed(world, gps, tmp_path / "gwap").feed_tick(ts_utc=UTC)
    assert rep["verdict"] == VERIFIED_AGREE and rep["fed"] == 1
    assert rep["identity_fingerprint"] is None
    assert "identity_fingerprint" not in gwap_payload(tmp_path, rep["scene_id"])

    # a registry that holds OTHER sids changes nothing for this one
    world.stage("s1", "tag", "hollow")
    world.tick()
    rep2 = VerdictFeed(
        world, gps, tmp_path / "gwap",
        identities={"deadbeef": {"user": "eve", "fingerprint": KEY_FP}},
    ).feed_tick(ts_utc=UTC)
    assert rep2["verdict"] == VERIFIED_AGREE and rep2["fed"] == 1
    assert rep2["identity_fingerprint"] is None
    assert "identity_fingerprint" not in gwap_payload(tmp_path, rep2["scene_id"])
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 2)


def test_tampered_fingerprint_breaks_the_chain_verify(world, gps, tmp_path):
    """(c) the fingerprint lives inside the hashed envelope: editing it in
    the ledger file breaks the row hash, the chain check fails at that row,
    the SessionLedger refuses to open the file, and the bridge refuses to
    feed it -- a forged attribution cannot ride a bound row's evidence."""
    world.stage("s1", "boil", "spring")
    world.tick()
    rep = _bound_feed(world, gps, tmp_path).feed_tick(ts_utc=UTC)
    path = Path(rep["ledger_path"])
    lines = path.read_text(encoding="utf-8").splitlines()
    assert KEY_FP in lines[0]  # the field really is in the row's bytes
    lines[0] = lines[0].replace(KEY_FP, EVIL_FP)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    assert verify_chain_file(path) == (False, 1)
    with pytest.raises(GwapError) as ei:
        SessionLedger(rep["scene_id"], store=tmp_path / "gwap")
    assert ei.value.reason == "BROKEN_CHAIN"
    from mag.gwap_to_gps import GwapToGpsError, feed_session

    with pytest.raises(GwapToGpsError) as ei2:
        feed_session(path, gps, task_shape=TASK_SHAPE,
                     scene_to_model={rep["scene_id"]: SERVER_ID})
    assert ei2.value.reason == "BROKEN_CHAIN"
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 1)  # only the honest row


def test_malformed_binding_record_refuses_typed(world, gps, tmp_path):
    """A recorded binding with no usable fingerprint refuses typed
    (BAD_IDENTITY_BINDING) before anything is minted, rather than labeling
    a row with a broken attribution: the registry entry exists, so the
    unbound default must NOT silently fire."""
    world.stage("s1", "boil", "spring")
    world.tick()
    feed = _bound_feed(world, gps, tmp_path,
                       record={"user": "adam"})  # fingerprint missing
    with pytest.raises(VerdictFeedError) as ei:
        feed.feed_tick(ts_utc=UTC)
    refuses(ei, "BAD_IDENTITY_BINDING")
    assert gps.get_rate(SERVER_ID, TASK_SHAPE) is None  # nothing fed
    assert list((tmp_path / "gwap").glob("*.jsonl")) == []  # nothing minted
