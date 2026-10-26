"""tests for mag/wow_player.py -- player files, bound by blueprint M2's falsifiers.

M2 falsifier: state survives restart byte-identical (canonical_state equality, plus a
real cross-process resume). Ledger law: every mutation appends exactly one row; tamper
one row -> typed TAMPERED; hash chain must stay intact. Determinism law: no timestamps
anywhere in the file bytes (the ISO-year pattern is grepped as a test). Inventory is
append-only at the ledger level: spends shadow, grants survive.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

import mag.wow_player as wp
from mag.wow_player import (SCHEMA, PlayerFile, PlayerLedgerError,
                            canonical, player_id_for, verify_file)

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


@pytest.fixture()
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(wp, "STORE", tmp_path)
    return tmp_path


def read_doc(store: Path, player_id: str) -> dict:
    return json.loads((store / f"{player_id}.json").read_text(encoding="utf-8"))


def write_doc(store: Path, player_id: str, doc: dict) -> None:
    (store / f"{player_id}.json").write_text(canonical(doc), encoding="utf-8")


def played_character(store: Path) -> PlayerFile:
    """A short life: genesis, a walk, a grant, a stamina bump, a spend."""
    p = PlayerFile.create("adam", room="atrium", stamina_max=10)
    p.apply("move", to="kiln")
    p.apply("grant_item", item={"item_id": "torch-1", "kind": "light"})
    p.apply("stamina", delta=5)
    p.apply("spend_item", item_id="torch-1")
    return p


# -- shape + derived identity --------------------------------------------------------

def test_file_shape_and_derived_id(store):
    p = PlayerFile.create("adam")
    doc = read_doc(store, p.player_id)
    assert doc["schema"] == SCHEMA == "wow_player.v1"
    assert set(doc) == {"schema", "player_id", "name", "traits", "ledger"}
    assert doc["player_id"] == player_id_for("adam")
    assert doc["player_id"].startswith("ply-") and len(doc["player_id"]) == 16
    genesis = doc["ledger"][0]
    assert genesis["n"] == 1 and genesis["event"] == "create"
    assert genesis["prev"] == "0" * 64
    assert doc["traits"] == {"room": "atrium", "stamina_max": 10, "inventory": []}


def test_player_id_is_secret_free_and_deterministic(store):
    assert player_id_for("adam") == player_id_for("adam")
    assert player_id_for("adam") != player_id_for("Eve")
    # the derivation is pure sha256 of schema+name -- no env, no clock, no secret
    import hashlib
    assert player_id_for("adam") == "ply-" + hashlib.sha256(
        b"wow_player.v1:adam").hexdigest()[:12]


# -- the M2 falsifier: cold-restart resume is byte-identical -------------------------

def test_cold_restart_resume_byte_identical(store):
    p = played_character(store)
    before_state = p.canonical_state()
    before_bytes = (store / f"{p.player_id}.json").read_bytes()

    resumed = PlayerFile.load(p.player_id)   # a fresh object, as a new process would
    assert resumed is not p
    assert resumed.canonical_state() == before_state
    assert resumed.traits == {"room": "kiln", "stamina_max": 15, "inventory": []}
    # and the resumed instance keeps appending on the same chain
    resumed.apply("move", to="atrium")
    assert (store / f"{p.player_id}.json").read_bytes() != before_bytes
    assert PlayerFile.load(p.player_id).traits["room"] == "atrium"


def test_fresh_process_resume_byte_identical(store):
    """The falsifier for real: one process plays, a brand-new interpreter resumes."""
    writer = (
        "import sys, json\n"
        "sys.path.insert(0, r'%s')\n"
        "import mag.wow_player as m\n"
        "from pathlib import Path\n"
        "m.STORE = Path(r'%s')\n"
        "p = m.PlayerFile.create('adam', room='atrium', stamina_max=10)\n"
        "p.apply('move', to='kiln')\n"
        "p.apply('grant_item', item={'item_id': 'torch-1', 'kind': 'light'})\n"
        "p.apply('spend_item', item_id='torch-1')\n"
        "print(m.canonical({'player_id': p.player_id, 'state': p.canonical_state()}))\n"
    ) % (wp.ROOT, store)
    reader = (
        "import sys, json\n"
        "sys.path.insert(0, r'%s')\n"
        "import mag.wow_player as m\n"
        "from pathlib import Path\n"
        "m.STORE = Path(r'%s')\n"
        "pid = m.player_id_for('adam')\n"
        "p = m.PlayerFile.load(pid)\n"
        "assert p is not None\n"
        "print(m.canonical({'player_id': p.player_id, 'state': p.canonical_state()}))\n"
    ) % (wp.ROOT, store)

    w = subprocess.run([sys.executable, "-c", writer],
                       capture_output=True, text=True, timeout=120,
                       creationflags=HEADLESS)
    assert w.returncode == 0, w.stderr
    r = subprocess.run([sys.executable, "-c", reader],
                       capture_output=True, text=True, timeout=120,
                       creationflags=HEADLESS)
    assert r.returncode == 0, r.stderr
    assert json.loads(w.stdout) == json.loads(r.stdout)
    doc = json.loads(r.stdout)
    assert json.loads(doc["state"])["traits"]["inventory"] == []


# -- the chain: tamper is typed -------------------------------------------------------

def test_tamper_one_row_is_typed_tampered(store):
    p = played_character(store)
    doc = read_doc(store, p.player_id)
    doc["ledger"][2]["data"]["item_id"] = "torch-9"   # rewrite history, keep hashes
    bad = verify_file(doc)
    assert bad == (False, "TAMPERED")
    write_doc(store, p.player_id, doc)
    with pytest.raises(PlayerLedgerError) as err:
        PlayerFile.load(p.player_id)
    assert err.value.reason == "TAMPERED"


def test_broken_chain_and_bad_n_are_typed(store):
    p = played_character(store)
    doc = read_doc(store, p.player_id)

    # break the chain while n stays contiguous: point row 3 at the wrong parent
    relinked = json.loads(json.dumps(doc))
    relinked["ledger"][2]["prev"] = relinked["ledger"][0]["hash"]
    assert verify_file(relinked) == (False, "BROKEN_CHAIN")

    # reordering history breaks n contiguity first -- caught as BAD_N
    reordered = json.loads(json.dumps(doc))
    reordered["ledger"][1], reordered["ledger"][2] = \
        reordered["ledger"][2], reordered["ledger"][1]
    assert verify_file(reordered) == (False, "BAD_N")

    holed = json.loads(json.dumps(doc))
    del holed["ledger"][2]
    assert verify_file(holed) == (False, "BAD_N")   # n checked before the chain

    renamed = json.loads(json.dumps(doc))
    renamed["name"] = "not-adam"
    assert verify_file(renamed) == (False, "BAD_ID")


def test_edited_view_without_touching_rows_is_view_mismatch(store):
    p = played_character(store)
    doc = read_doc(store, p.player_id)
    doc["traits"]["stamina_max"] = 999            # the row says 15; the view lies
    assert verify_file(doc) == (False, "VIEW_MISMATCH")
    write_doc(store, p.player_id, doc)
    with pytest.raises(PlayerLedgerError) as err:
        PlayerFile.load(p.player_id)
    assert err.value.reason == "VIEW_MISMATCH"


def test_bad_schema_and_unknown_file(store):
    assert verify_file({"schema": "mysql_row.v1"}) == (False, "BAD_SCHEMA")
    assert PlayerFile.load(player_id_for("nobody-here")) is None
    with pytest.raises(PlayerLedgerError):
        PlayerFile.load("ply-not-a-real-id")


# -- append-only law -------------------------------------------------------------------

def test_every_mutation_appends_exactly_one_row(store):
    p = PlayerFile.create("adam")
    n0 = len(p.ledger)
    p.apply("move", to="kiln")
    assert len(p.ledger) == n0 + 1
    assert p.ledger[-1]["n"] == n0 + 1
    assert p.ledger[-1]["prev"] == p.ledger[-2]["hash"]


def test_inventory_is_append_only_ledger_view_drops_spent(store):
    p = played_character(store)
    doc = p.to_file()
    assert len(doc["ledger"]) == 5                        # create + 4 mutations
    grant_rows = [r for r in doc["ledger"] if r["event"] == "grant_item"]
    spend_rows = [r for r in doc["ledger"] if r["event"] == "spend_item"]
    assert len(grant_rows) == 1 and len(spend_rows) == 1
    assert grant_rows[0]["data"]["item"]["item_id"] == "torch-1"   # the grant survives
    assert p.traits["inventory"] == []                    # only the replayed view drops it


def test_earlier_rows_never_change_under_later_applies(store):
    p = PlayerFile.create("adam")
    p.apply("move", to="kiln")
    prefix = canonical(p.to_file()["ledger"])
    p.apply("grant_item", item={"item_id": "torch-1"})
    p.apply("stamina", delta=-3)
    longer = p.to_file()["ledger"]
    assert canonical(longer[:2]) == prefix                # history is never rewritten
    assert verify_file(p.to_file()) == (True, "OK")


def test_unknown_event_refused_and_files_untouched(store):
    p = PlayerFile.create("adam")
    before = (store / f"{p.player_id}.json").read_bytes()
    with pytest.raises(PlayerLedgerError) as err:
        p.apply("teleport_to_gold", zone="stratholme")
    assert err.value.reason == "UNKNOWN_EVENT"
    assert len(p.ledger) == 1
    assert (store / f"{p.player_id}.json").read_bytes() == before


def test_double_create_refused_resume_from_ledger(store):
    a = PlayerFile.create("adam", room="atrium")
    with pytest.raises(PlayerLedgerError) as err:
        PlayerFile.create("adam", room="elsewhere")
    assert err.value.reason == "ALREADY_EXISTS"
    b = PlayerFile.load(a.player_id)                      # login = resume-from-ledger
    assert b.canonical_state() == a.canonical_state()
    assert b.traits["room"] == "atrium"                   # the refused create changed nothing


# -- determinism: no timestamps anywhere ----------------------------------------------

def test_no_timestamps_anywhere_in_file_bytes(store):
    p = played_character(store)
    raw = (store / f"{p.player_id}.json").read_bytes()
    assert not re.search(rb"20\d{2}-\d{2}-\d{2}", raw), "ISO date leaked into the ledger"
    for word in (b"created", b"timestamp", b"datetime", b"time_", b"_ts"):
        assert word not in raw.lower(), word


def test_same_name_same_moves_same_bytes(store, tmp_path, monkeypatch):
    p1 = played_character(store)
    other = tmp_path / "mirror"
    monkeypatch.setattr(wp, "STORE", other)
    p2 = played_character(other)
    assert p1.player_id == p2.player_id
    assert p1.canonical_state() == p2.canonical_state()   # determinism falsifier


# -- the CLI is the same referee -------------------------------------------------------

def test_cli_create_and_verify_ok(store, capsys):
    assert wp.main(["create", "--name", "adam", "--room", "atrium"]) == 0
    pid = player_id_for("adam")
    out = json.loads(capsys.readouterr().out)
    assert out["player_id"] == pid
    assert wp.main(["verify", "--player", pid]) == 0
    verdict = json.loads(capsys.readouterr().out)
    assert verdict == {"ok": True, "reason": "OK"}
    assert wp.main(["apply", "--player", pid, "--event", "move",
                    "--data", '{"to": "kiln"}']) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["traits"]["room"] == "kiln"


def test_cli_verify_catches_tamper(store, capsys):
    PlayerFile.create("eve")
    pid = player_id_for("eve")
    doc = read_doc(store, pid)
    doc["ledger"][0]["data"]["room"] = "forged"
    write_doc(store, pid, doc)
    assert wp.main(["verify", "--player", pid]) == 1      # the referee refuses
    verdict = json.loads(capsys.readouterr().out)
    assert verdict == {"ok": False, "reason": "TAMPERED"}
