"""tests/test_chain_contract.py -- the Mickey17 chain pin (WAVE0, 2026-09-29).

One test pins the platform's chain contract end to end: an authoritative
Mountain tick row (server/world.py, hash-chained from a 64-zero genesis)
is sealed into a signed gwap payload (mag/gwap_payload.py, ed25519 over
the canonical bytes minus the signature block) whose replay tape carries
the row's own sha, so signature + receipt jointly identify the world
bytes. Flipping ONE byte of the sealed payload fails the offline
signature check; flipping ONE byte of the world row fails
verify_log_rows. Written for watch/inbox/MICKEY17_RUN_PLAN_20260929.md
WAVE0 so the chain contract cannot rot while the default test
entrypoint is being repaired.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mag.gwap_payload as gw  # noqa: E402
from server.world import MountainWorld, verify_log_rows  # noqa: E402

UTC = "2026-09-29T12:00:00Z"

needs_crypto = pytest.mark.skipif(
    not gw.HAS_CRYPTO, reason="cryptography package not installed in this venv"
)


def flip_first_byte(text: str) -> str:
    """One byte changed, rest identical: 'mountain' -> 'xountain'."""
    return ("x" if text[0] != "x" else "y") + text[1:]


@needs_crypto
def test_world_row_seals_into_signed_gwap_payload_and_both_tampers_fail():
    # -- the world side: one session, one staged action, one authoritative tick
    world = MountainWorld()
    world.register_session("s1", "ada")
    assert world.stage("s1", "boil", "spring")["op"] == "ack"
    tick = world.tick()
    assert tick["op"] == "tick" and tick["n"] == 1
    assert verify_log_rows(world.rows) is True     # chain green before the seal
    row = world.rows[-1]                           # the tick row just appended
    assert row["kind"] == "tick" and row["winner"] is False

    # -- the gwap side: a payload whose replay tape IS the world row's sha
    robber = gw.anon_id("chain-pin-robber-20260929")
    cop = gw.anon_id("chain-pin-cop-20260929")
    payload = gw.build_payload(
        scene_id="mountain-tick-1",
        intent_struct={"author": robber, "claims": [
            {"subject": "ada", "verb": "boils", "object": "spring"},
            {"subject": "steam", "verb": "condenses", "object": "crown"},
        ]},
        report_struct={"author": cop, "claims": [
            {"subject": "ada", "verb": "boils", "object": "spring"},
        ]},
        participants=[
            {"anon_id": robber, "role": "robber"},
            {"anon_id": cop, "role": "cop"},
        ],
        consent=True,
        created_utc=UTC,
        replay_tape_ref={
            "sha256": row["sha"],
            "engine_version": "server.world.v0",
        },
    )
    assert payload["replay_tape_ref"]["sha256"] == row["sha"]  # the pin itself

    # -- fresh keypair, seal, verify offline (the unsigned original never passes)
    priv_hex, pub_hex = gw.author_keypair("chain-pin-key-20260929")
    signed = gw.sign_payload(payload, robber, priv_hex)
    assert signed["signature"]["pubkey"] == pub_hex
    assert gw.verify_signature(signed) is True
    assert gw.verify_signature(payload) is False

    # -- flip ONE byte inside the sealed core: the offline check must fail
    tampered = copy.deepcopy(signed)
    tampered["scene_id"] = flip_first_byte(tampered["scene_id"])
    assert tampered["scene_id"] != signed["scene_id"]
    assert gw.verify_signature(tampered) is False
    assert gw.verify_signature(signed) is True       # the seal itself is intact

    # -- flip ONE byte of a world row: the hash chain must fail
    victim = world.rows[0]                           # the action row (ada boils)
    victim["event"] = flip_first_byte(victim["event"])
    assert victim["event"].startswith(("x", "y"))
    assert verify_log_rows(world.rows) is False
    assert world.verify_log() is False
