"""X9 motion-row tests: the idle/flee/pursue/carry/dance dialect through
the protocol table, and the fish_brain.gd decide() determinism contract.

Laws under test (receipt watch/inbox/hydrology/X9_MOTION.md):
  - the motion contract is a STRICT SUPERSET: DEFAULT (the bound v0 wire)
    stays byte-identical and MOTION_DIGEST is a new contract version
  - every motion verb routes to one rig_* owner and declares the payload
    law {intensity_q8: u8, dir: target}
  - ask() keeps the ordering law end to end: verb -> state gate -> payload
    -> handler; every refusal is TYPED (UNKNOWN_VERB / UNKNOWN_SID /
    BAD_ARGS / BAD_INTENSITY / UNKNOWN_TARGET) and handler_ran is False
  - u8 is ints 0..255 only: bools subclass int and True is rejected (a
    bool is a verdict, not an intensity)
  - fish_brain.decide() is deterministic BY CONSTRUCTION (pure function:
    no RNG, no wall clock, no state, no snapshot mutation). The estate box
    has no Godot binary (watch/inbox/GODOT_SLICE_20260929.md:37), so
    same-tick+snapshot-same-row is enforced structurally here; the first
    executed determinism run lands when a binary does
  - the .gd emitter speaks exactly the .py table's dialect
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.protocol_table import (  # noqa: E402
    DEFAULT_TABLE,
    MOTION_DIGEST,
    MOTION_DISPATCH,
    MOTION_SPEC,
    MOTION_TABLE,
    MOTION_VERBS,
    PROTOCOL_DIGEST,
    ProtocolDispatch,
    ProtocolSpecError,
    compile_table,
)

TARGETS = frozenset({"spring", "terrace", "gate1", "hollow", "waste", "crown"})
GOOD = {"intensity_q8": 128, "dir": "crown"}
FISH_BRAIN = ROOT / "roblox_to_godot" / "systems" / "fish_brain.gd"


# ------------------------------------------------------------- superset ----

def test_motion_contract_is_a_strict_superset():
    assert MOTION_TABLE.verbs == DEFAULT_TABLE.verbs + MOTION_VERBS
    assert MOTION_DIGEST != PROTOCOL_DIGEST  # a NEW contract version
    for ours, theirs in zip(MOTION_TABLE.rows, DEFAULT_TABLE.rows):
        assert ours.to_dict() == theirs.to_dict()  # base rows ride unchanged
    assert "flee" not in DEFAULT_TABLE.verbs  # the v0 wire never grew


def test_default_wire_is_byte_identical():
    # the regression the superset design exists to protect: digest of the
    # untouched v0 spec, computed fresh, still matches the pinned digest
    from server import protocol
    assert compile_table().digest == PROTOCOL_DIGEST
    assert protocol.VERBS == DEFAULT_TABLE.verbs == ("boil", "valve", "join", "tag")
    assert protocol.PROTOCOL_DIGEST == PROTOCOL_DIGEST


def test_motion_rows_declare_the_payload_law():
    for verb in MOTION_VERBS:
        row = MOTION_TABLE.row(verb)
        assert row.args == (("dir", "target"), ("intensity_q8", "u8"))
        assert row.required_state == "AUTHED"
        assert row.handler_name == f"rig_{verb}"
    assert MOTION_TABLE.row("boil").args == ()  # base verbs stay payload-less
    doc = MOTION_TABLE.to_document()
    by_verb = {r["verb"]: r for r in doc["rows"]}
    assert by_verb["dance"]["args"] == {"intensity_q8": "u8", "dir": "target"}
    assert "args" not in by_verb["boil"]  # document stays byte-shaped per row


def test_motion_digest_roundtrips_and_is_stable():
    assert compile_table(MOTION_SPEC).digest == MOTION_DIGEST
    assert compile_table(MOTION_TABLE.to_document()).digest == MOTION_DIGEST


# ----------------------------------------------------------- validate ----

@pytest.mark.parametrize("verb", MOTION_VERBS)
def test_every_motion_row_validates_through_the_table(verb):
    out = MOTION_DISPATCH.ask(verb, "AUTHED", GOOD, TARGETS)
    assert out == {"ok": True, "reason": "DISPATCHED", "handler": f"rig_{verb}",
                   "required_state": "AUTHED", "args": GOOD, "handler_ran": True}
    assert MOTION_DISPATCH.calls[-1] == verb  # the handler firing is recorded


@pytest.mark.parametrize("intensity", [0, 1, 127, 254, 255])
def test_u8_full_range_is_legal(intensity):
    # boundaries included: 0 = still, 255 = maximum urgency
    for verb in MOTION_VERBS:
        out = MOTION_DISPATCH.ask(verb, "AUTHED",
                                  {"intensity_q8": intensity, "dir": "spring"}, TARGETS)
        assert out["ok"] is True and out["handler_ran"] is True


@pytest.mark.parametrize("intensity", [256, -1, 255 + 1, 1.5, 0.0, "200", None, True, [1]])
def test_bad_intensity_is_a_typed_reject(intensity):
    out = MOTION_DISPATCH.ask("flee", "AUTHED",
                              {"intensity_q8": intensity, "dir": "crown"}, TARGETS)
    assert out == {"ok": False, "reason": "BAD_INTENSITY", "handler_ran": False}


@pytest.mark.parametrize("dir_value", ["atlantis", "", " ", 7, None, True])
def test_unknown_dir_is_a_typed_reject(dir_value):
    out = MOTION_DISPATCH.ask("pursue", "AUTHED",
                              {"intensity_q8": 10, "dir": dir_value}, TARGETS)
    assert out == {"ok": False, "reason": "UNKNOWN_TARGET", "handler_ran": False}


@pytest.mark.parametrize("args", [
    {"intensity_q8": 128},                       # missing dir
    {"dir": "crown"},                            # missing intensity_q8
    {"intensity_q8": 128, "dir": "crown", "x": 1},  # extra key
    None,                                        # no payload at all
    "flee",                                      # not a dict
    [],                                          # not a dict either
])
def test_bad_shape_is_a_typed_reject(args):
    out = MOTION_DISPATCH.ask("carry", "AUTHED", args, TARGETS)
    assert out == {"ok": False, "reason": "BAD_ARGS", "handler_ran": False}


def test_payload_on_a_schema_less_verb_is_bad_args():
    out = MOTION_DISPATCH.ask("boil", "AUTHED", GOOD, TARGETS)
    assert out == {"ok": False, "reason": "BAD_ARGS", "handler_ran": False}
    assert MOTION_DISPATCH.ask("boil", "AUTHED", None, TARGETS)["ok"] is True


# ------------------------------------------------- the ordering law ----

def test_gate_before_verb_and_payload():
    assert MOTION_DISPATCH.ask("wiggle", "AUTHED", GOOD, TARGETS) == {
        "ok": False, "reason": "UNKNOWN_VERB", "handler_ran": False}
    # CONNECTED is refused on STATE before the (garbage) payload is read
    out = MOTION_DISPATCH.ask("flee", "CONNECTED",
                              {"intensity_q8": 99999, "dir": "nope"}, TARGETS)
    assert out == {"ok": False, "reason": "UNKNOWN_SID", "handler_ran": False}
    assert MOTION_DISPATCH.ask("flee", "FLYING", GOOD, TARGETS)["reason"] == "UNKNOWN_STATE"


def test_refusals_never_fire_the_handler():
    d = ProtocolDispatch(MOTION_TABLE)
    for verb, args in [("flee", {"intensity_q8": 999, "dir": "crown"}),
                       ("pursue", {"intensity_q8": 5, "dir": "nowhere"}),
                       ("dance", {"dir": "crown"}),
                       ("idle", None)]:
        d.ask(verb, "AUTHED", args, TARGETS)
    assert d.calls == []  # nothing ran across four kinds of refusal


def test_ask_is_deterministic():
    a = MOTION_DISPATCH.ask("flee", "AUTHED", GOOD, TARGETS)
    b = MOTION_DISPATCH.ask("flee", "AUTHED", GOOD, TARGETS)
    assert a == b


# ----------------------------------------------------- fail-closed ----

@pytest.mark.parametrize("mutation", [
    lambda s: s["rows"][-1].update(args="u8"),                       # args not a dict
    lambda s: s["rows"][-1].update(args={}),                         # empty args
    lambda s: s["rows"][-1].update(args={"intensity_q8": "float"}),  # unknown spec
    lambda s: s["rows"][-1].pop("reject_code"),                      # missing core key
    lambda s: s["reject_codes"].remove("BAD_INTENSITY"),             # u8 code unowned
    lambda s: s["reject_codes"].remove("BAD_ARGS"),                  # shape code unowned
    lambda s: s["rows"][-1].update(junk=1),                          # unknown row key
    lambda s: s["rows"].append(dict(s["rows"][-1])),                 # duplicate verb
])
def test_compile_fails_closed_on_motion_specs(mutation):
    spec = copy.deepcopy(MOTION_SPEC)
    mutation(spec)
    with pytest.raises(ProtocolSpecError):
        compile_table(spec)


# --------------------------------------- fish_brain.gd (the emitter) ----

def _brain_source() -> str:
    assert FISH_BRAIN.is_file(), f"missing {FISH_BRAIN}"
    return FISH_BRAIN.read_text(encoding="utf-8")


def test_fish_brain_signature_is_pure_shape():
    src = _brain_source()
    assert src.splitlines()[0].strip() == "extends RefCounted"  # no Node: no tree, no _process
    assert ("static func decide(fish_id: int, tick: int, snapshot: Dictionary)"
            " -> Dictionary:") in src  # the mandated pure entry point
    # stateless: no class-scope vars, no signals
    assert not re.search(r"^var\s", src, re.M)
    assert not re.search(r"^signal\s", src, re.M)


def test_fish_brain_has_no_nondeterminism_sources():
    src = _brain_source()
    for token in ("randf", "randi", "rand_range", "RandomNumberGenerator",
                  "get_ticks_msec", "get_unix_time", "get_system_time",
                  "Time.", "OS."):
        assert token not in src, f"nondeterminism source in fish_brain.gd: {token}"
    # the W1 leak law: the clock never enters, not even via helpers
    assert "sim_time" not in src


def test_fish_brain_never_mutates_the_snapshot():
    src = _brain_source()
    # no writes into the snapshot or the arrays/dicts it lends by reference
    assert not re.search(r"snapshot\[[^\]]*\]\s*=[^=]", src)
    assert not re.search(
        r"\b(snapshot|fish|pools)\.(append|erase|sort|assign|clear|"
        r"push_back|insert|remove_at|fill|resize)\(", src)


def test_fish_brain_emits_exactly_the_table_dialect():
    src = _brain_source()
    verbs = set(re.findall(r'"verb":\s*"([a-z]+)"', src))
    assert verbs == set(MOTION_VERBS)  # all five, nothing invented
    assert verbs <= set(MOTION_TABLE.verbs)
    # every row literal carries the payload law's exact keys
    for row_literal in re.findall(r"\{(?:[^{}]|\{[^{}]*\})*\}", src):
        if '"verb"' in row_literal and "intensity_q8" in row_literal:
            assert '"dir"' in row_literal
    assert src.count('"intensity_q8"') >= 6  # five verbs + the _q8 helper doc shape
