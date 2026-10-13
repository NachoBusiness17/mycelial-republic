"""Tests for wow_family -- the emulator lineage, and the claim we make about it.

RIB: wow_family.v1 -- three dialects of the same family are parsed out of local clones:
AzerothCore (WotLK macros), TortoiseWoW (classic StoreOpcode), vMaNGOS (typed Handlers).
The tests pin the numbers and, above all, the CLAIM: the most content-heavy server in the
family added no verbs.

Self-skipping: skipped when the clones are absent.
"""
from __future__ import annotations

import pytest

from mag import wow_family as wf

pytestmark = pytest.mark.skipif(
    any(not p["root"].is_dir() for p in wf.FAMILY),
    reason="one or more family clones are not present",
)


@pytest.fixture(scope="module")
def lin():
    return wf.lineage()


def test_three_dialects_parse(lin):
    s = {r["id"]: r for r in lin["sources"]}
    assert set(s) == {"vmangos", "tortoise", "azerothcore"}
    assert s["vmangos"]["verbs"] == 826
    assert s["tortoise"]["verbs"] == 824
    assert s["azerothcore"]["verbs"] == 1312
    for r in s.values():
        assert r["present"] and r["sha256_12"] and r["head"]


def test_the_vanilla_line_keeps_one_lane_per_verb(lin):
    """10 named dispatch lanes in the vanilla dialect; the WotLK dialect collapsed them to 3."""
    s = {r["id"]: r for r in lin["sources"]}
    assert len(s["tortoise"]["lanes"]) == 10
    assert len(s["vmangos"]["lanes"]) >= 9
    assert len(s["azerothcore"]["lanes"]) == 3


def test_progressive_vanilla_contracts(lin):
    """One FROZEN protocol header per supported patch, and the alphabet grows with the patch."""
    s = {r["id"]: r for r in lin["sources"]}
    vc = s["vmangos"]["versioned_contracts"]
    assert vc["count"] == 9
    counts = [vc["headers"][k] for k in sorted(vc["headers"], key=lambda x: tuple(map(int, x.split("."))))]
    assert counts == sorted(counts)              # monotone: later patch, more verbs
    assert vc["headers"]["1.4.2"] == 727
    assert vc["headers"]["1.12.1"] == 826
    # the WotLK dialect has no such thing: it froze one protocol and stopped
    assert s["azerothcore"]["versioned_contracts"]["count"] == 0


def test_the_headline_delta():
    d = wf.delta()
    v = d["vanilla_delta"]
    assert d["frozen_1_12_1_contract"] == 826
    assert d["vanilla_alphabet"] == {"vmangos": 826, "tortoise": 824, "shared": 821}
    assert v["total_differing"] == 8
    assert v["pct_of_alphabet"] == 0.97
    assert v["names_outside_the_frozen_contract"] == [
        "CMSG_UNUSED", "CMSG_UNUSED2", "SMSG_ACCOUNT_DATA_TIMES"]
    assert v["slots_beyond_the_frozen_range"] == []
    assert v["unexplained_verbs"] == []


def test_claim_holds_and_is_earned():
    d = wf.delta()
    assert d["claim_holds"] is True
    assert "added no verbs" in d["claim"]
    assert len(d["digest"]) == 64
    # the digest is stable: re-deriving twice must agree (it is a contract version)
    assert wf.delta()["digest"] == d["digest"]


def test_the_rename_is_proven_at_bytes():
    """SMSG_ACCOUNT_DATA_TIMES is not a new verb: it is the frozen contract's slot 0x209."""
    frozen = wf._frozen_slots()
    tw = [p for p in wf.FAMILY if p["id"] == "tortoise"][0]
    slots = wf.parse_source(tw)["slots"]
    assert slots["SMSG_ACCOUNT_DATA_TIMES"] == 0x209
    assert frozen["SMSG_ACCOUNT_DATA_MD5"] == 0x209
    # and the two UNUSED entries are placeholder slots the frozen contract never names
    frozen_slot_values = set(frozen.values())
    for n in ("CMSG_UNUSED", "CMSG_UNUSED2"):
        assert n not in frozen
        assert slots[n] not in frozen_slot_values


def test_wotlk_is_the_outlier_in_verb_count():
    d = wf.delta()
    assert d["versus_wotlk"]["azerothcore_verbs"] > 1.5 * d["vanilla_alphabet"]["tortoise"]
    assert d["versus_wotlk"]["vanilla_lanes"] > d["versus_wotlk"]["azerothcore_lanes"]


def test_doctrine_laws_are_extracted():
    d = wf.doctrine()
    assert len(d["laws"]) == 4
    joined = " ".join(d["laws"]).lower()
    for key in ("custom behaviour", "content should be separate", "marked with the patch",
                "programming knowledge"):
        assert key in joined
