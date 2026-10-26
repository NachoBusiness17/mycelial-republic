"""Ledger registry tests (Mickey17 wave 3 re-fire, 2026-09-29).

Covers the tools/ledger_registry.py contract in the test_gap_sentinel house
style: fixture chains for every mounted family (wow_player, gwap, server
world) verify OK through the registry, corruption in each family is caught by
that chain's OWN verify (never a registry reimplementation), the nightly
canary files its attention alert exactly once per failure-origin key
(idempotent across repeated runs), the exit-code ladder holds (0 healthy,
1 failing, 2 cannot-verify via ImportError), the verkle family is wired
through mag/chain_guard.check (the ask's "verkle via its guard" law), and the
query-by-hash stub finds known row hashes and rejects non-hex prefixes.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ledger_registry as lr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

NOW = datetime(2026, 9, 29, 21, 0, tzinfo=timezone.utc)
HEX64 = "0" * 64


# ── fixture chains: one valid chain per family, built by the owning module ──


def build_wow_fixture(store: Path) -> Path:
    from mag import wow_player as wp
    create_data = {"room": "atrium", "stamina_max": 10}
    row1 = wp._new_row(1, "create", create_data, HEX64)
    traits = wp._reduce("create", create_data, None)
    move_data = {"to": "garden"}
    row2 = wp._new_row(2, "move", move_data, row1["hash"])
    traits = wp._reduce("move", move_data, traits)
    doc = {
        "schema": wp.SCHEMA,
        "player_id": wp.player_id_for("Registry Test"),
        "name": "Registry Test",
        "traits": traits,
        "ledger": [row1, row2],
    }
    path = store / f"{doc['player_id']}.json"
    path.write_text(wp.canonical(doc), encoding="utf-8")
    return path


def build_gwap_fixture(store: Path) -> Path:
    from mag import gwap_payload as gw
    robber = gw.anon_id("reg-test-robber")
    cop = gw.anon_id("reg-test-cop")
    payload = gw.build_payload(
        scene_id="scene-registry-test",
        intent_struct={"author": robber, "claims": [
            {"subject": "intruder", "verb": "cut", "object": "junction power"}]},
        report_struct={"author": cop, "claims": [
            {"subject": "intruder", "verb": "cut", "object": "junction power"}]},
        participants=[{"anon_id": robber, "role": "robber"},
                      {"anon_id": cop, "role": "cop"}],
        consent=True,
        created_utc="2026-09-29T00:00:00Z",
        replay_tape_ref={"sha256": HEX64, "engine_version": "test"},
    )
    ledger = gw.SessionLedger("reg-test-20260929", store=store)
    ledger.append(payload, ts_utc="2026-09-29T00:00:01Z")
    ledger.append(payload, ts_utc="2026-09-29T00:00:02Z")
    return ledger.path


def build_world_fixture(store: Path) -> Path:
    from server.world import MountainWorld
    path = store / "world_log.jsonl"
    world = MountainWorld(log_path=path)
    world.register_session("sid-1", "tester")
    world.stage("sid-1", "join", "spring")
    world.tick()
    world.close()
    return path


def mounted(paths_by_family: dict[str, list[Path]]) -> list[dict]:
    """Registry entries built from the real family adapters, pointed at fixtures."""
    entries = []
    for fam, paths in paths_by_family.items():
        entry = dict(lr.FAMILY_BUILDERS[fam]())
        entry["paths"] = [str(p) for p in paths]
        entries.append(entry)
    return entries


def tamper_wow(path: Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["ledger"][1]["data"]["to"] = "vault"  # bytes moved, stored hash untouched
    path.write_text(json.dumps(doc), encoding="utf-8")


def tamper_gwap(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[0])
    row["payload"]["scene_id"] = "scene-forged"
    lines[0] = json.dumps(row)  # row_sha256 left stale on purpose
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def tamper_world(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[-1])
    row["nodes"]["crown"] = 99  # volume forged, stored sha untouched
    lines[-1] = json.dumps(row)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


TAMPERERS = {"wow_player": tamper_wow, "gwap": tamper_gwap, "server_world": tamper_world}


# ── the contract ──


def test_default_families_mount_the_asked_set():
    names = [e["name"] for e in lr.default_families()]
    assert names == ["wow_player", "gwap", "server_world", "verkle"]


def test_fixture_chains_verify_ok_through_the_registry(tmp_path):
    paths = {
        "wow_player": [build_wow_fixture(tmp_path)],
        "gwap": [build_gwap_fixture(tmp_path)],
        "server_world": [build_world_fixture(tmp_path)],
    }
    result = lr.verify_all(mounted(paths))
    assert result["chains"] == 3 and not result["failing"]
    assert not result["cannot_verify"]
    by_family = {r["family"]: r for r in result["rows"]}
    assert by_family["wow_player"]["rows"] == 2
    assert by_family["gwap"]["rows"] == 2
    assert by_family["server_world"]["rows"] == 2  # action row + tick row
    for row in result["rows"]:
        assert row["ok"] and row["detail"] in ("OK", "True")
        assert isinstance(row["tip"], str) and len(row["tip"]) == 64


def test_corruption_caught_by_each_chains_own_verify(tmp_path):
    for fam, tamper in TAMPERERS.items():
        store = tmp_path / fam
        store.mkdir()
        paths = {
            "wow_player": [build_wow_fixture(store)],
            "gwap": [build_gwap_fixture(store)],
            "server_world": [build_world_fixture(store)],
        }
        tamper(paths[fam][0])
        result = lr.verify_all(mounted(paths))
        bad = [r for r in result["rows"] if r["family"] == fam]
        assert len(bad) == 1 and not bad[0]["ok"], fam
        assert bad[0]["detail"], fam
        # the two untouched families still pass: one bad chain never poisons the table
        assert all(r["ok"] for r in result["rows"] if r["family"] != fam), fam


def test_canary_files_once_and_never_duplicates(tmp_path):
    path = build_wow_fixture(tmp_path)
    tamper_wow(path)
    entries = mounted({"wow_player": [path]})

    first = lr.canary(root=tmp_path, entries=entries, now=NOW)
    assert first == 1
    attention = tmp_path / "memory" / "attention.md"
    text = attention.read_text(encoding="utf-8")
    assert text.count("### Ledger registry canary fired") == 1
    assert text.count("- key: ledger-registry wow_player") == 1
    alerted = (tmp_path / "logs" / "ledger_registry" / "alerted.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(alerted) == 1

    second = lr.canary(root=tmp_path, entries=entries, now=NOW)
    assert second == 1  # persistent failure stays exit 1
    assert attention.read_text(encoding="utf-8") == text  # byte-identical: no re-file
    runs = (tmp_path / "logs" / "ledger_registry" / "runs.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(runs) == 2 and json.loads(runs[-1])["exit"] == 1


def test_canary_exit_0_when_healthy_and_records_the_run(tmp_path):
    path = build_gwap_fixture(tmp_path)
    entries = mounted({"gwap": [path]})
    assert lr.canary(root=tmp_path, entries=entries, now=NOW) == 0
    assert not (tmp_path / "memory" / "attention.md").exists()
    run = json.loads((tmp_path / "logs" / "ledger_registry" / "runs.jsonl")
                     .read_text(encoding="utf-8").splitlines()[0])
    assert run["exit"] == 0 and run["chains"] == 1 and run["failing"] == 0


def test_cannot_verify_is_exit_2_and_files_no_alert(tmp_path):
    def verify_raises_import(_path):
        raise ImportError("No module named 'nonexistent_family'")

    entry = dict(lr.FAMILY_BUILDERS["wow_player"]())
    entry["verify"] = verify_raises_import
    entry["paths"] = [str(build_wow_fixture(tmp_path))]
    assert lr.canary(root=tmp_path, entries=[entry], now=NOW) == 2
    assert not (tmp_path / "memory" / "attention.md").exists()
    assert not (tmp_path / "logs" / "ledger_registry" / "alerted.jsonl").exists()


def test_verkle_family_is_wired_through_its_guard(monkeypatch, tmp_path):
    import mag.chain_guard as cg
    chain_file = tmp_path / "verkle_chain.jsonl"
    chain_file.write_text('{"leaf_hash": "%s"}\n' % ("a" * 64), encoding="utf-8")
    entries = mounted({"verkle": [chain_file]})

    # one verify_all consumes check() twice (verify word + tip reader), so each
    # wiring state is patched as a constant dict, not an iterator
    monkeypatch.setattr(cg, "check", lambda: {
        "ok": False, "state": "regression", "rows": 5, "chain_root": "b" * 64})
    bad = lr.verify_all(entries)
    row = bad["rows"][0]
    assert not row["ok"] and row["detail"] == "regression"
    assert row["rows"] == 5 and row["tip"] == "b" * 64

    monkeypatch.setattr(cg, "check", lambda: {
        "ok": True, "state": "healthy", "rows": 5, "chain_root": "b" * 64})
    good = lr.verify_all(entries)
    assert good["rows"][0]["ok"] and good["rows"][0]["detail"] == "healthy"


def test_query_by_hash_finds_row_hashes_across_families(tmp_path):
    (tmp_path / "wow").mkdir()
    wow_path = build_wow_fixture(tmp_path / "wow")
    gwap_path = build_gwap_fixture(tmp_path / "gwap")
    entries = mounted({"wow_player": [wow_path], "gwap": [gwap_path]})

    gwap_tip = json.loads(gwap_path.read_text(encoding="utf-8").splitlines()[-1])
    hits = lr.query_by_hash(gwap_tip["row_sha256"][:12], entries)
    assert len(hits) == 1
    assert hits[0]["family"] == "gwap" and hits[0]["field"] == "row_sha256"
    assert hits[0]["hash"] == gwap_tip["row_sha256"]

    wow_doc = json.loads(wow_path.read_text(encoding="utf-8"))
    hits = lr.query_by_hash(wow_doc["ledger"][0]["hash"][:16], entries)
    assert hits and hits[0]["family"] == "wow_player" and hits[0]["field"] == "hash"

    assert lr.query_by_hash("zz-not-hex", entries) == []
    assert lr.query_by_hash("f" * 16, entries) == []
