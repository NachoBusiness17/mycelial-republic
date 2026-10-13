"""Tests for wow_bones -- the bones of AzerothCore, extracted as data and RUN as laws.

RIB: wow_bones.v1 -- extract() parses the real dispatch table + enums out of the clone; the three
kernels (Dispatch / Instance / Stream) execute the laws the map claims, so every claim on
docs/ref/WOW_ACORE_STEAL_MAP_20260915.md is falsifiable here rather than asserted in prose.

Self-skipping: the whole module is skipped when the clone is absent, so the suite stays green on
a machine that has never cloned AzerothCore.
"""
from __future__ import annotations

import pytest

from mag import wow_bones as wb

pytestmark = pytest.mark.skipif(
    not (wb.ACORE / wb.SRC_OPCODES_CPP).is_file(),
    reason="AzerothCore clone not present at ACORE",
)


@pytest.fixture(scope="module")
def bones():
    d = wb.extract()
    assert d["ok"], d.get("error")
    return d


# --- the bones themselves ---------------------------------------------------------------------

def test_counts_match_the_source(bones):
    """725 client + 587 server = 1,312 dispatch entries (the #define macro lines are not entries)."""
    assert bones["counts"] == {
        "client_opcodes": 725,
        "server_opcodes": 587,
        "session_status": 6,
        "packet_processing": 3,
        "encounter_state": 6,
    }


def test_enums_are_the_real_vocabularies(bones):
    assert bones["enums"]["session_status"] == {
        "STATUS_AUTHED": 0, "STATUS_LOGGEDIN": 1, "STATUS_TRANSFER": 2,
        "STATUS_LOGGEDIN_OR_RECENTLY_LOGGOUT": 3, "STATUS_NEVER": 4, "STATUS_UNHANDLED": 5,
    }
    assert bones["enums"]["packet_processing"] == {
        "PROCESS_INPLACE": 0, "PROCESS_THREADUNSAFE": 1, "PROCESS_THREADSAFE": 2,
    }
    assert bones["enums"]["encounter_state"] == {
        "NOT_STARTED": 0, "IN_PROGRESS": 1, "FAIL": 2, "DONE": 3, "SPECIAL": 4,
        "TO_BE_DECIDED": 5,
    }
    # the transition law lives in the .cpp, not only the header -- assert we found it
    assert bones["enums"]["_instance_cpp_present"]["yes"] == 1


def test_phase_histogram_is_the_contract_pin(bones):
    """A pin, not a derivation: if upstream re-phases a verb, this fails loudly (new contract)."""
    from collections import Counter
    hist = Counter(r["status"] for r in bones["tables"]["client_opcodes"])
    assert dict(hist) == {
        "STATUS_LOGGEDIN": 410,
        "STATUS_NEVER": 292,
        "STATUS_AUTHED": 20,
        "STATUS_LOGGEDIN_OR_RECENTLY_LOGGOUT": 2,
        "STATUS_TRANSFER": 1,
    }
    assert sum(hist.values()) == 725


def test_digest_is_stable_across_extractions(bones):
    """The digest is the contract version; two reads of the same source must agree."""
    again = wb.extract()
    assert again["bones_digest"] == bones["bones_digest"]
    assert wb.extract()["bones_digest"] == bones["bones_digest"]  # re-derivable, not cached


# --- B01/B03: the alphabet is a gated table, refusals are typed -------------------------------

def test_every_verb_is_gated_and_every_refusal_is_typed(bones):
    d = wb.Dispatch(bones)
    statuses = list(bones["enums"]["session_status"])
    dispatched = never = 0
    for name in d.verbs():
        row = d.rows[name]
        own = row["status"]
        if own in ("STATUS_NEVER", "STATUS_UNHANDLED"):
            res = d.dispatch(name, "STATUS_AUTHED")
            assert res["ok"] is False and res["reason"] == own
            never += 1
            continue
        # a legal status that is NOT this verb's phase must refuse, for all 5 other statuses
        for other in statuses:
            if other == own:
                continue
            res = d.dispatch(name, other)
            assert res["ok"] is False
            assert res["reason"] in ("STATUS_MISMATCH", "STATUS_NEVER", "STATUS_UNHANDLED")
            assert res["handler_ran"] is False
        assert d.dispatch(name, own)["ok"] is True
        dispatched += 1
    assert (dispatched, never) == (433, 292)
    assert dispatched + never == 725


def test_unknown_verb_and_unknown_status_are_typed(bones):
    d = wb.Dispatch(bones)
    assert d.dispatch("CMSG_NOT_A_REAL_VERB", "STATUS_LOGGEDIN") == {
        "ok": False, "reason": "UNKNOWN_OPCODE", "handler_ran": False}
    assert d.dispatch("CMSG_WORLD_TELEPORT", "STATUS_WOKE") == {
        "ok": False, "reason": "UNKNOWN_STATUS", "handler_ran": False}


def test_every_dispatched_verb_carries_a_processing_place(bones):
    d = wb.Dispatch(bones)
    places = set(bones["enums"]["packet_processing"])
    for name in d.verbs():
        row = d.rows[name]
        assert row["processing"] in places, name


# --- B02: the ordering law (the gate runs before the verb) ------------------------------------

def test_gate_runs_before_the_verb(bones):
    """The stolen bone: phase is checked on the TABLE, so a verb that exists still never fires."""
    d = wb.Dispatch(bones)
    name = "CMSG_WORLD_TELEPORT"          # STATUS_LOGGEDIN, PROCESS_THREADUNSAFE in the source
    assert d.rows[name]["status"] == "STATUS_LOGGEDIN"

    refused = d.dispatch(name, "STATUS_AUTHED")
    assert refused["ok"] is False and refused["reason"] == "STATUS_MISMATCH"
    assert refused["handler_ran"] is False
    assert d.calls == []                  # the handler provably never ran

    allowed = d.dispatch(name, "STATUS_LOGGEDIN")
    assert allowed["ok"] is True and allowed["handler_ran"] is True
    assert allowed["handler"] == "HandleWorldTeleportOpcode"
    assert allowed["processing"] == "PROCESS_THREADUNSAFE"
    assert d.calls == [name]


# --- B05: the encounter law -------------------------------------------------------------------

def test_encounter_law_matches_setbossstate(bones):
    inst = wb.Instance(bones, boss_ids=3)
    assert inst.name(inst.enums["TO_BE_DECIDED"]) == "TO_BE_DECIDED"

    # a load is not a transition: first write on a TO_BE_DECIDED boss returns False ...
    assert inst.set_boss_state(0, "IN_PROGRESS") is False
    assert inst.name(inst.state[0]) == "IN_PROGRESS"
    # ... and leaves no transition in the log
    assert inst.log == []

    # a repeat is not a transition
    assert inst.set_boss_state(0, "IN_PROGRESS") is False
    # a real transition is True and is logged
    assert inst.set_boss_state(0, "DONE") is True
    assert inst.log == [(0, 3)]
    assert inst.is_done(0) is True

    # DONE is guarded while a world boss lives
    inst.set_boss_state(1, "IN_PROGRESS")
    assert inst.set_boss_state(1, "DONE", world_boss_alive=True) is False
    assert inst.is_done(1) is False
    assert inst.set_boss_state(1, "DONE", world_boss_alive=False) is True
    assert inst.is_done(1) is True

    # out-of-range boss id and unknown state name are refused, not raised
    assert inst.set_boss_state(99, "DONE") is False
    assert inst.set_boss_state(0, "VICTORY") is False


# --- B06: the RNG law, and the differential ---------------------------------------------------

def test_stream_replays_or_reports_divergence():
    s = wb.Stream("seed-A", modulo=100)
    for _ in range(8):
        s.next()
    assert len(s.log) == 8 and s.index == 8
    assert s.replay(s.log) == {"ok": True, "reason": "REPLAY_MATCH", "draws": 8}

    tampered = [dict(e) for e in s.log]
    tampered[5]["value"] = (tampered[5]["value"] + 1) % 100
    bad = s.replay(tampered)
    assert bad["ok"] is False and bad["reason"] == "RNG_DIVERGE" and bad["index"] == 5


def test_stream_is_seeded_and_has_no_global_state():
    """Two instances, same seed -> identical draws. No process-global stream (unlike urand())."""
    a, b = wb.Stream("same"), wb.Stream("same")
    assert [a.next() for _ in range(6)] == [b.next() for _ in range(6)]
    c = wb.Stream("different")
    assert [c.next() for _ in range(6)] != [x["value"] for x in a.log]


# --- the receipt ------------------------------------------------------------------------------

def test_fixture_on_disk_matches_a_fresh_extraction():
    fx = wb.load_fixture()
    if fx is None:
        pytest.skip("fixture not generated yet (run: python -m mag.wow_bones extract)")
    assert fx["bones_digest"] == wb.extract()["bones_digest"]
    assert fx["counts"]["client_opcodes"] == 725
