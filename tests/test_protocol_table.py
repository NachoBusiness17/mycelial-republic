"""protocol_table tests: the verbs-as-data layer behind server/protocol.

Every test is a law from the W1 lane brief (Mickey17 return 17):
  - the table is FROZEN (mutation refused or isolated)
  - the digest is STABLE (pure compile) and SENSITIVE (any edit moves it)
  - every verb ROUTES to a named handler
  - an unknown verb gets a TYPED reject and the handler provably never ran
  - state GATING works, including the NOT_YOUR_TURN machinery (a state
    column) that the v0 table reserves but never emits
  - server/protocol's surface (VERBS, REJECT_CODES) is table-backed with
    byte-identical values, so in-flight tests cannot break
  - our dispatch keeps the wow_bones.Dispatch call contract (the shape is
    the steal, not the import)
"""
from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import server.protocol as protocol  # noqa: E402
from server.protocol_table import (  # noqa: E402
    DEFAULT_DISPATCH,
    DEFAULT_SPEC,
    DEFAULT_TABLE,
    PROTOCOL_DIGEST,
    ProtocolDispatch,
    ProtocolSpecError,
    compile_table,
    state_for_sid,
    validate,
)


# ------------------------------------------------------------ immutability ----

def test_frozen_rows_refuse_mutation():
    row = DEFAULT_TABLE.rows[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        row.verb = "dance"
    with pytest.raises(AttributeError):
        DEFAULT_TABLE.rows.append(object())  # type: ignore[attr-defined]
    with pytest.raises(TypeError):
        DEFAULT_TABLE.session_states["TURN_HELD"] = 99  # type: ignore[index]


def test_document_copy_is_isolated():
    doc = DEFAULT_TABLE.to_document()
    doc["rows"][0]["verb"] = "sabotage"
    doc["session_states"].append("GHOST")
    assert DEFAULT_TABLE.verbs == ("boil", "valve", "join", "tag")
    assert "GHOST" not in DEFAULT_TABLE.session_states
    assert compile_table().digest == PROTOCOL_DIGEST  # the table never moved


def test_rows_are_json_serializable():
    doc = DEFAULT_TABLE.to_document()
    text = json.dumps(doc, sort_keys=True)
    assert json.loads(text) == doc
    assert [r.verb for r in DEFAULT_TABLE.rows] == ["boil", "valve", "join", "tag"]
    assert set(doc["rows"][0]) == {"verb", "required_state", "handler_name", "reject_code"}


# ----------------------------------------------------------------- digest ----

def test_digest_is_stable():
    assert compile_table().digest == PROTOCOL_DIGEST
    assert compile_table(DEFAULT_SPEC).digest == PROTOCOL_DIGEST
    assert DEFAULT_TABLE.digest == PROTOCOL_DIGEST
    assert len(PROTOCOL_DIGEST) == 64
    int(PROTOCOL_DIGEST, 16)  # pure hex


def test_digest_is_sensitive_to_every_part():
    def variant(**change):
        import copy
        spec = copy.deepcopy(DEFAULT_SPEC)
        for key, value in change.items():
            spec[key] = value
        return compile_table(spec).digest

    rows = [dict(r) for r in DEFAULT_SPEC["rows"]]
    tampered = [dict(r) for r in DEFAULT_SPEC["rows"]]
    tampered[0]["required_state"] = "TURN_HELD"
    reordered = list(reversed([dict(r) for r in DEFAULT_SPEC["rows"]]))
    assert variant(rows=tampered) != PROTOCOL_DIGEST   # a row edit moves it
    assert variant(rows=reordered) != PROTOCOL_DIGEST  # row order is semantic
    assert variant(session_states=["CONNECTED", "AUTHED"]) != PROTOCOL_DIGEST
    assert variant(reject_codes=list(DEFAULT_SPEC["reject_codes"]) + ["NEW_CODE"]) != PROTOCOL_DIGEST
    assert variant(transport_reject_codes=["BAD_AUTH", "BAD_JSON"]) != PROTOCOL_DIGEST


def test_document_roundtrip_recompiles_identical():
    doc = DEFAULT_TABLE.to_document()
    shipped = json.loads(json.dumps(doc))  # what a peer would receive
    assert compile_table(shipped).digest == PROTOCOL_DIGEST


# --------------------------------------------------------------- routing ----

def test_every_verb_routes():
    d = ProtocolDispatch()
    handlers = set()
    for verb in protocol.VERBS:
        out = d.dispatch(verb, "AUTHED")
        row = DEFAULT_TABLE.row(verb)
        assert out == {
            "ok": True,
            "reason": "DISPATCHED",
            "handler": row.handler_name,
            "required_state": "AUTHED",
            "handler_ran": True,
        }
        handlers.add(row.handler_name)
        assert verb in d.calls  # the handler firing is recorded
    assert len(handlers) == len(protocol.VERBS)  # one verb, one owner
    assert all(h.startswith("world_") for h in handlers)


def test_unknown_verb_typed_reject():
    d = ProtocolDispatch()
    for bogus in ("dance", "", "BOIL", "boil "):
        out = d.dispatch(bogus, "AUTHED")
        assert out == {"ok": False, "reason": "UNKNOWN_VERB", "handler_ran": False}
    assert d.calls == []  # nothing fired


# ------------------------------------------------------------ state gating ----

def test_unauthed_state_gates_every_verb():
    d = ProtocolDispatch()
    for verb in protocol.VERBS:
        out = d.dispatch(verb, "CONNECTED")
        assert out == {"ok": False, "reason": "UNKNOWN_SID", "handler_ran": False}
    assert d.calls == []


def test_unknown_state_is_an_internal_typed_refusal():
    out = DEFAULT_DISPATCH.dispatch("boil", "FLYING")
    assert out == {"ok": False, "reason": "UNKNOWN_STATE", "handler_ran": False}


def test_not_your_turn_machinery_exists_but_v0_never_emits_it():
    # machinery: compile a turn-gated verb and the state column fires
    import copy
    spec = copy.deepcopy(DEFAULT_SPEC)
    spec["rows"].append({"verb": "chant", "required_state": "TURN_HELD",
                         "handler_name": "world_chant", "reject_code": "NOT_YOUR_TURN"})
    turn_table = compile_table(spec)
    assert turn_table.digest != PROTOCOL_DIGEST  # the contract version moved
    d = ProtocolDispatch(turn_table)
    assert d.dispatch("chant", "AUTHED") == {
        "ok": False, "reason": "NOT_YOUR_TURN", "handler_ran": False}
    assert d.dispatch("chant", "TURN_HELD")["ok"] is True
    # reservation: the DEFAULT table never emits it, on any verb, any state
    for verb in protocol.VERBS:
        for state in DEFAULT_TABLE.session_states:
            out = DEFAULT_DISPATCH.dispatch(verb, state)
            assert out["reason"] != "NOT_YOUR_TURN"


# --------------------------------------------------- surface + fail-closed ----

def test_protocol_surface_is_table_backed():
    assert protocol.VERBS == DEFAULT_TABLE.verbs
    assert protocol.VERBS == ("boil", "valve", "join", "tag")  # byte-identical v0
    assert protocol.REJECT_CODES == DEFAULT_TABLE.reject_codes
    assert protocol.REJECT_CODES == (
        "UNKNOWN_SID", "NOT_YOUR_TURN", "UNKNOWN_VERB", "UNKNOWN_TARGET", "DRY_POOL")
    assert protocol.TRANSPORT_REJECT_CODES == ("BAD_AUTH", "BAD_JSON", "UNKNOWN_OP")
    assert protocol.PROTOCOL_DIGEST == PROTOCOL_DIGEST
    assert protocol.DEFAULT_TABLE is DEFAULT_TABLE
    assert isinstance(protocol.VERBS, tuple)  # world.py membership use keeps working


@pytest.mark.parametrize("mutation", [
    lambda s: s["rows"].append(dict(s["rows"][0])),                 # duplicate verb
    lambda s: s["rows"][0].update(required_state="FLYING"),         # bad state
    lambda s: s["rows"][0].update(reject_code="NOPE"),              # bad reject code
    lambda s: s["rows"][0].update(handler_name=""),                 # empty handler
    lambda s: s["rows"][1].update(handler_name="world_boil"),       # duplicate handler
    lambda s: s["rows"][0].update(extra=1),                         # extra key
    lambda s: s["rows"][0].pop("reject_code"),                      # missing key
    lambda s: s.update(rows=[]),                                    # no verbs at all
    lambda s: s.update(schema="protocol_table.v0"),                 # wrong schema
    lambda s: s.update(session_states=["CONNECTED", "CONNECTED"]),  # dup states
    lambda s: s.update(transport_reject_codes=["UNKNOWN_VERB"]),    # vocab overlap
])
def test_compile_fails_closed(mutation):
    import copy
    spec = copy.deepcopy(DEFAULT_SPEC)
    mutation(spec)
    with pytest.raises(ProtocolSpecError):
        compile_table(spec)


def test_validate_keeps_the_world_shape_contract():
    assert validate("AUTHED", "boil") == (True, None)
    assert validate("AUTHED", "dance") == (False, "UNKNOWN_VERB")
    assert validate("CONNECTED", "boil") == (False, "UNKNOWN_SID")
    roster = {"s1"}
    assert state_for_sid("s1", roster) == "AUTHED"
    assert state_for_sid("nope", roster) == "CONNECTED"


# ------------------------------------------------- the Dispatch shape steal ----

def test_dispatch_shape_matches_wow_bones():
    from mag.wow_bones import Dispatch as WowDispatch
    fixture = {
        "tables": {"client_opcodes": [
            {"opcode": "0x1", "name": "CMSG_TEST", "status": "STATUS_LOGGEDIN",
             "processing": "PROCESS_INPLACE", "handler": "HandleTest"},
        ]},
        "enums": {"session_status": {"STATUS_AUTHED": 0, "STATUS_LOGGEDIN": 1},
                  "packet_processing": {"PROCESS_INPLACE": 0},
                  "encounter_state": {}},
    }
    wow = WowDispatch(fixture)
    ours = ProtocolDispatch()
    wow_refusal = wow.dispatch("CMSG_TEST", "STATUS_AUTHED")   # wrong phase
    our_refusal = ours.dispatch("boil", "CONNECTED")           # wrong phase
    assert wow_refusal["ok"] is False and our_refusal["ok"] is False
    assert set(wow_refusal) == set(our_refusal) == {"ok", "reason", "handler_ran"}
    assert wow_refusal["handler_ran"] is our_refusal["handler_ran"] is False
    wow_ok = wow.dispatch("CMSG_TEST", "STATUS_LOGGEDIN")
    our_ok = ours.dispatch("boil", "AUTHED")
    assert {"ok", "reason", "handler", "handler_ran"} <= set(our_ok)
    assert {"ok", "reason", "handler", "handler_ran"} <= set(wow_ok)
    assert our_ok["handler_ran"] is wow_ok["handler_ran"] is True
    # ordering law both ways: the gate runs before the verb runs, and a
    # refusal never records a call
    assert ours.calls == ["boil"] and wow.calls == ["CMSG_TEST"]
