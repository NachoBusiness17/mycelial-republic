"""Grok Bot box seats as Mag harness seats (2026-10-18, roster swap adapter).

Pins: grokbot-<name> ids validate and sign like any seat (mate: behaviour
unchanged); revoked grokbot tombstones are rejected everywhere; a grokbot
seat does NOT satisfy quorum.require_non_glm_approval unless
quorum.grokbot_counts_as_non_glm is true. Keys are generated in memory per
test; no real key file is opened.
"""
from __future__ import annotations

import json

import pytest

from mag import proposals as P
from mag import seat_handshake as sh

SEATS = ("mate:composer", "mate:jester", "grokbot-ghost", "grokbot-research", "grok")
RETIRED = ("grokbot-research", "grokbot-newbot", "grokbot-archival", "grokbot-refreshbot")


@pytest.fixture
def world(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "PROPOSALS_DIR", tmp_path / "proposals")
    seeds, rows = {}, {}
    for s in SEATS:
        seeds[s] = sh.generate_seed()
        rows[s] = {"public_hex": sh.public_from_seed(seeds[s]).hex()}
        if s.startswith("mate:"):
            rows[s].update(kind="mate", model_family="glm")
        if s.startswith("grokbot-"):
            rows[s].update(kind="grokbot", model_family="grokbot")
    al = {"schema": "seat_allowlist.v1", "skew_s": 60,
          "quorum": {"default": 2, "require_non_glm_approval": True},
          "operator_seats": [], "seats": rows}
    return al, seeds


def _sign(kind, payload, seat, seeds):
    return P.sign_message(kind, payload, seed=seeds[seat], seat_id=seat)


def _propose(al, seeds, seat="mate:composer"):
    msg = _sign("proposal", {"title": "t", "targets": ["configs/mates.yaml"],
                             "diff": "--- a/x\n+++ b/x\n@@ -1 +1 @@\n-a\n+b\n",
                             "rationale": "t"}, seat, seeds)
    return P.submit(msg, allowlist=al)["proposal_id"]


def _review(al, seeds, pid, seat, verdict="approve"):
    return P.submit(_sign("review", {"proposal_id": pid, "verdict": verdict, "reason": "t"},
                          seat, seeds), allowlist=al)


def test_grokbot_ids_accepted_and_mate_rule_unchanged(tmp_path, monkeypatch):
    for good in ("grokbot-ghost", "grokbot-mag", "grokbot-refreshbot", "mate:jester", "grok"):
        assert sh.SEAT_RE.fullmatch(good)
    for bad in ("grokbot:ghost", "x:y", "mate:", "mate:-x", "-grokbot"):
        assert not sh.SEAT_RE.fullmatch(bad)
    monkeypatch.setenv(sh.ENV_KEY_DIR, str(tmp_path / "keys"))
    assert sh.default_key_path("grokbot-ghost") == tmp_path / "keys" / "grokbot-ghost.key"
    assert sh.default_key_path("mate:jester") == tmp_path / "keys" / "mates" / "mate__jester.key"


def test_enrolled_grokbot_envelope_verifies(world):
    al, seeds = world
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    env = sh.wrap(body, seed=seeds["grokbot-ghost"], seat_id="grokbot-ghost")
    assert sh.verify_envelope(env, allowlist=al, cache=sh.ReplayCache()) == ("grokbot-ghost", body)


def test_revoked_grokbot_rejected(world):
    al, seeds = world
    al["seats"]["grokbot-research"]["revoked"] = True
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    env = sh.wrap(body, seed=seeds["grokbot-research"], seat_id="grokbot-research")
    assert sh.seat_public(al, "grokbot-research") is None
    assert sh.verify_envelope(env, allowlist=al, cache=sh.ReplayCache()) is None
    msg = P.sign_message("proposal", {"title": "x", "targets": ["a.txt"], "diff": "d\n", "rationale": ""},
                         seed=seeds["grokbot-research"], seat_id="grokbot-research")
    with pytest.raises(ValueError):
        P.submit(msg, allowlist=al)
    # keyless tombstone row (as shipped) is inert too
    assert sh.seat_public({"seats": {"grokbot-newbot": {"public_hex": None, "revoked": True}}},
                          "grokbot-newbot") is None


def test_grokbot_not_non_glm_by_default(world):
    al, seeds = world
    assert P.is_non_glm_seat("grokbot-ghost", al) is False
    assert P.is_non_glm_seat("grok", al) is True          # unchanged for other non-mate seats
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "grokbot-ghost")
    t = P.tally(pid, allowlist=al)
    assert t["approvers"] == ["grokbot-ghost", "mate:jester"]
    assert t["non_glm_approvers"] == [] and t["non_glm_ok"] is False and t["ready"] is False


def test_grokbot_counts_when_flag_true(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "grokbot-ghost")
    al["quorum"]["grokbot_counts_as_non_glm"] = True
    assert P.is_non_glm_seat("grokbot-ghost", al) is True
    t = P.tally(pid, allowlist=al)
    assert t["non_glm_approvers"] == ["grokbot-ghost"] and t["ready"] is True
    al["quorum"]["grokbot_counts_as_non_glm"] = "false"
    assert P.tally(pid, allowlist=al)["ready"] is False


def test_shipped_allowlist_grokbot_rows():
    al = sh.load_allowlist()
    assert al["quorum"]["grokbot_counts_as_non_glm"] is False
    assert al["operator_seats"] == ["nacho"]  # enrolled 2026-10-18, operator's own key; was [] at grokbot enrollment
    assert al["seats"]["nacho"]["kind"] == "operator" and al["seats"]["nacho"]["model_family"] == "human"
    assert not any(al["seats"][sid].get("kind") == "grokbot" for sid in al["operator_seats"])
    seats = al["seats"]
    for sid, aid, role in (("grokbot-ghost", "4a30dd44-e0bc-4e3c-af2a-13da6e62cef5", "front_door"),
                           ("grokbot-mag", "27002d7d-d9f6-4e11-8eb9-27eaab9b0ebe", "estate_brain")):
        row = seats[sid]
        assert row["kind"] == row["model_family"] == "grokbot"
        assert row["box_agent_id"] == aid and row["role"] == role and not row.get("revoked")
        assert sh.seat_public(al, sid) is not None
        assert P.is_non_glm_seat(sid, al) is False
    for sid in RETIRED:
        row = seats[sid]
        assert row["revoked"] is True and row["retired"] == "2026-10-18"
        assert "283907df0fe5697412c18f0d2ebe1307831933977a32fbe93f8f772ff8bfa95b" in row["archive_receipt"]
        assert sh.seat_public(al, sid) is None
    assert "private" not in json.dumps(seats).lower()
