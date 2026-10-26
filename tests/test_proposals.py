"""proposals: per-seat signing, quorum, and the non-GLM adoption rule (2026-10-17).

Harness2 gave every leave-protocol mate its OWN Ed25519 key (seat ids
"mate:<name>"). These bands pin: mate seat ids validate and never reach a
filename with a colon; quorum counts distinct seats with the author out; a
room of GLM mates cannot adopt alone (quorum.require_non_glm_approval,
default on); one seat's key can never speak for another. All keys here are
generated in memory per test; no real key file is opened.
"""
from __future__ import annotations

import json

import pytest

from mag import proposals as P
from mag import seat_handshake as sh

SEATS = ("mate:composer", "mate:jester", "mate:mariner", "grok", "zcode", "nacho")


@pytest.fixture
def world(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "PROPOSALS_DIR", tmp_path / "proposals")
    seeds, rows = {}, {}
    for s in SEATS:
        seeds[s] = sh.generate_seed()
        rows[s] = {"public_hex": sh.public_from_seed(seeds[s]).hex()}
        if s.startswith("mate:"):
            rows[s].update(kind="mate", model_family="glm")
    rows["zcode"]["model_family"] = "GLM-4.7"  # a non-mate seat that is still GLM
    al = {"schema": "seat_allowlist.v1", "skew_s": 60,
          "quorum": {"default": 2, "require_non_glm_approval": True},
          "operator_seats": ["nacho"], "seats": rows}
    return al, seeds


def _sign(kind, payload, seat, seeds):
    return P.sign_message(kind, payload, seed=seeds[seat], seat_id=seat)


def _propose(al, seeds, seat="mate:composer"):
    msg = _sign("proposal", {"title": "harness2 test", "targets": ["configs/mates.yaml"],
                             "diff": "--- a/x\n+++ b/x\n@@ -1 +1 @@\n-a\n+b\n",
                             "rationale": "test"}, seat, seeds)
    return P.submit(msg, allowlist=al)["proposal_id"]


def _review(al, seeds, pid, seat, verdict="approve"):
    return P.submit(_sign("review", {"proposal_id": pid, "verdict": verdict, "reason": "t"},
                          seat, seeds), allowlist=al)


def test_mate_seat_ids_validate_and_slug(tmp_path, monkeypatch):
    for good in ("mate:jester", "mate:editor_inv", "grok", "bob-agy"):
        assert sh.SEAT_RE.fullmatch(good)
    for bad in ("mate:", "x:y", "mate:mate:x", ":jester", "mate:-x", "mate: x"):
        assert not sh.SEAT_RE.fullmatch(bad)
    assert sh.seat_slug("mate:jester") == "mate__jester"
    monkeypatch.setenv(sh.ENV_KEY_DIR, str(tmp_path / "keys"))
    assert sh.default_key_path("mate:jester") == tmp_path / "keys" / "mates" / "mate__jester.key"
    assert sh.default_key_path("grok") == tmp_path / "keys" / "grok.key"


def test_review_and_promotion_filenames_carry_no_colon(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "grok")
    P.submit(_sign("promotion", {"proposal_id": pid, "state": "ready"}, "mate:jester", seeds), allowlist=al)
    names = [p.name for p in (P.PROPOSALS_DIR / pid).iterdir()]
    assert any(n.startswith("review_mate__jester_") for n in names)
    assert all(":" not in n for n in names)


def test_two_mate_approvals_are_not_enough(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "mate:mariner")
    t = P.tally(pid, allowlist=al)
    assert t["approvers"] == ["mate:jester", "mate:mariner"]
    assert t["require_non_glm_approval"] is True
    assert t["non_glm_ok"] is False and t["ready"] is False


def test_mate_plus_non_glm_seat_is_ready(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "grok")
    t = P.tally(pid, allowlist=al)
    assert t["non_glm_approvers"] == ["grok"] and t["ready"] is True


def test_non_mate_glm_family_seat_does_not_count_as_non_glm(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "zcode")
    t = P.tally(pid, allowlist=al)
    assert len(t["approvers"]) == 2 and t["non_glm_approvers"] == [] and not t["ready"]


def test_rule_defaults_on_and_can_be_switched_off(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "mate:mariner")
    del al["quorum"]["require_non_glm_approval"]
    assert P.tally(pid, allowlist=al)["ready"] is False  # missing key = on
    al["quorum"]["require_non_glm_approval"] = False
    assert P.tally(pid, allowlist=al)["ready"] is True   # plain quorum of 2


def test_operator_approval_is_ready_alone(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "nacho")
    t = P.tally(pid, allowlist=al)
    assert t["ready"] and t["operator_override"] and t["non_glm_approvers"] == ["nacho"]


def test_operator_reject_blocks(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "grok")
    _review(al, seeds, pid, "nacho", "reject")
    assert P.tally(pid, allowlist=al)["ready"] is False


def test_author_excluded_and_duplicate_votes_count_once(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:composer")
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "mate:jester")
    t = P.tally(pid, allowlist=al)
    assert t["author"] == "mate:composer" and t["approvers"] == ["mate:jester"]


def test_cross_key_forgery_is_rejected(world):
    al, seeds = world
    pid = _propose(al, seeds)
    # jester's key claiming to be mariner
    forged = P.sign_message("review", {"proposal_id": pid, "verdict": "approve", "reason": "x"},
                            seed=seeds["mate:jester"], seat_id="mate:mariner")
    with pytest.raises(ValueError):
        P.submit(forged, allowlist=al)
    # a valid jester review with the verdict flipped after signing
    good = _sign("review", {"proposal_id": pid, "verdict": "reject", "reason": "x"}, "mate:jester", seeds)
    tampered = json.loads(json.dumps(good))
    tampered["payload"]["verdict"] = "approve"
    with pytest.raises(ValueError):
        P.verify_message(tampered, al)
    # a forged file dropped straight into the folder is counted as invalid, not as a vote
    (P.PROPOSALS_DIR / pid / "review_mate__mariner_forged.json").write_text(json.dumps(forged), encoding="utf-8")
    t = P.tally(pid, allowlist=al)
    assert "mate:mariner" not in t["approvers"] and "review_mate__mariner_forged.json" in t["invalid_messages"]


def test_unknown_mate_seat_cannot_sign(world):
    al, seeds = world
    stranger = sh.generate_seed()
    msg = P.sign_message("proposal", {"title": "x", "targets": ["a.txt"], "diff": "d\n", "rationale": ""},
                         seed=stranger, seat_id="mate:stranger")
    with pytest.raises(ValueError):
        P.submit(msg, allowlist=al)


def test_promotion_refused_until_ready(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    with pytest.raises(ValueError, match="quorum"):
        P.submit(_sign("promotion", {"proposal_id": pid, "state": "ready"}, "mate:jester", seeds), allowlist=al)


def test_revoked_mate_vote_stops_counting(world):
    al, seeds = world
    pid = _propose(al, seeds)
    _review(al, seeds, pid, "mate:jester")
    _review(al, seeds, pid, "grok")
    assert P.tally(pid, allowlist=al)["ready"]
    al["seats"]["mate:jester"]["revoked"] = True
    assert P.tally(pid, allowlist=al)["ready"] is False


def test_shipped_allowlist_names_the_rule_and_ships_public_keys_only():
    al = sh.load_allowlist()
    assert al["quorum"]["require_non_glm_approval"] is True
    assert "private" not in json.dumps(al.get("seats"))
    for seat, row in (al.get("seats") or {}).items():
        if seat.startswith("mate:"):
            assert row["model_family"] == "glm" and len(row["public_hex"]) == 64
