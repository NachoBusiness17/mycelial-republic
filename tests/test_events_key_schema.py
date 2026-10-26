"""tests for the events key schema registry gate in mag/shared_surface.py (B2-342, 2026-09-26).

Spec under test (module docstring, "Events key schema"; registry spec:
configs/events_key_schema.json):
  - the registry is a CLOSED VOCABULARY of writer keys, not a required-fields
    spec: any registered key may be omitted on any line;
  - an event key NOT in the registry is an ERROR, one per distinct key,
    naming key, count, first line, seq and writer;
  - the underscore prefix is reserved for fold-internal fields (B2-329 dump
    purity) and is exempt from the scan;
  - a missing or shape-invalid registry is an ERROR;
  - malformed lines are the B2-42 gate's job and are skipped here.

All tests run against a throwaway surface; the durable watch/inbox is only
read by the two real-registry tests, which pin the shipped registry against
the real log bytes (the living falsifier).
"""
import json
from pathlib import Path

import pytest

import mag.shared_surface as ss

VALID = json.dumps({"seq": 1, "ts": "2026-09-26T00:00:00Z", "op": "note",
                    "writer": "t", "nonce": 1})


@pytest.fixture
def surface(tmp_path, monkeypatch):
    """Point every module constant at a throwaway surface (B2-42 pattern)."""
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    configs = tmp_path / "configs"
    configs.mkdir()
    monkeypatch.setattr(ss, "ROOT", tmp_path)
    monkeypatch.setattr(ss, "WATCH", tmp_path / "watch")
    monkeypatch.setattr(ss, "INBOX", inbox)
    monkeypatch.setattr(ss, "INDEX", inbox / "INDEX.json")
    monkeypatch.setattr(ss, "CONTRACT", inbox / "SHARED_SURFACE_CONTRACT.json")
    monkeypatch.setattr(ss, "WARM_PACK", tmp_path / "watch" / "WARM_PACK.json")
    monkeypatch.setattr(ss, "EVENTS_LOG", inbox / "index_events.jsonl")
    monkeypatch.setattr(ss, "MALFORMED_BASELINE", configs / "events_malformed_baseline.json")
    monkeypatch.setattr(ss, "EVENTS_KEY_SCHEMA", configs / "events_key_schema.json")
    return {"inbox": inbox, "configs": configs, "log": inbox / "index_events.jsonl",
            "schema": configs / "events_key_schema.json"}


def _write_schema(path, keys):
    path.write_text(json.dumps({"schema": "events_key_schema.v1",
                                "keys": [{"key": k} for k in keys]}), encoding="utf-8")


def _key_errors(result):
    return [e for e in result["errors"] if e.startswith("NEW event key")]


def test_new_key_is_an_error_naming_key_and_first_seen(surface):
    fresh = json.dumps({"seq": 2, "ts": "2026-09-26T00:01:00Z", "op": "note",
                        "writer": "rogue", "nonce": 1, "totally_fresh_key": "x"})
    surface["log"].write_text(VALID + "\n" + fresh + "\n" + fresh + "\n", encoding="utf-8")
    _write_schema(surface["schema"], ["seq", "ts", "op", "writer", "nonce"])
    result = ss.inspect_surface()
    bad = _key_errors(result)
    assert len(bad) == 1, result["errors"]  # one error per DISTINCT key
    assert "'totally_fresh_key'" in bad[0]
    assert "x2" in bad[0]  # occurrence count
    assert "first line 2" in bad[0]
    assert "'rogue'" in bad[0]
    assert result["events_log_keys"] == {"lines_scanned": 3, "unknown_keys": 1}
    assert result["ok"] is False


def test_registered_keys_are_clean(surface):
    _write_schema(surface["schema"], ["seq", "ts", "op", "writer", "nonce"])
    surface["log"].write_text(VALID + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert _key_errors(result) == []
    assert result["events_log_keys"] == {"lines_scanned": 1, "unknown_keys": 0}


def test_underscore_keys_are_exempt_b2_329_reserved_prefix(surface):
    underscored = json.dumps({"seq": 2, "ts": "2026-09-26T00:01:00Z", "op": "note",
                              "_outside": False, "_unresolved": False})
    _write_schema(surface["schema"], ["seq", "ts", "op"])
    surface["log"].write_text(underscored + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert _key_errors(result) == []


def test_missing_registry_is_an_error(surface):
    surface["log"].write_text(VALID + "\n", encoding="utf-8")
    result = ss.inspect_surface()  # no schema file written
    assert any("missing events key schema registry" in e for e in result["errors"])
    assert result["ok"] is False


def test_shape_invalid_registry_is_an_error(surface):
    surface["schema"].write_text(json.dumps({"schema": "events_key_schema.v1",
                                             "keys": []}), encoding="utf-8")
    surface["log"].write_text(VALID + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert any("invalid events key schema registry" in e for e in result["errors"])


def test_malformed_lines_are_skipped_by_the_key_scan(surface):
    _write_schema(surface["schema"], ["seq", "ts", "op", "writer", "nonce"])
    surface["log"].write_text("{'seq':NEXT,'op':'register'}\n", encoding="utf-8")
    (surface["configs"] / "events_malformed_baseline.json").write_text(
        json.dumps({"grandfathered": []}), encoding="utf-8")
    result = ss.inspect_surface()
    assert _key_errors(result) == []
    assert result["events_log_keys"] == {"lines_scanned": 0, "unknown_keys": 0}


def test_registry_keys_may_be_omitted_closed_not_required_fields(surface):
    # the vocabulary is closed, not required-fields: op-less beacon rows and
    # seq-less arc-burn rows are schema-clean as long as every key is known.
    row = json.dumps({"ts": "2026-09-18T11:52:00Z", "kind": "adv_arc_burn",
                      "item": "burn complete", "card": "watch/inbox/x.md"})
    _write_schema(surface["schema"], ["ts", "kind", "item", "card"])
    surface["log"].write_text(row + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert _key_errors(result) == []
    assert result["events_log_keys"]["unknown_keys"] == 0


# ---------------------------------------------------------------------------
# real-registry pins: the shipped spec against the real log bytes.
# ---------------------------------------------------------------------------

REAL_ROOT = Path(ss.__file__).resolve().parents[1]


def test_real_registry_covers_every_key_in_the_real_log():
    # the living falsifier: any key a writer ever appended must be registered.
    known = ss.load_event_key_registry(REAL_ROOT / "configs" / "events_key_schema.json")
    found = ss.scan_event_keys(REAL_ROOT / "watch" / "inbox" / "index_events.jsonl", known)
    assert found["unknown"] == [], [r["key"] for r in found["unknown"]]
    assert found["lines"] > 0


def test_real_registry_entries_carry_first_seen_evidence():
    data = json.loads((REAL_ROOT / "configs" / "events_key_schema.json").read_text(encoding="utf-8"))
    assert data["schema"] == "events_key_schema.v1"
    keys = [e["key"] for e in data["keys"]]
    assert len(keys) == len(set(keys))
    assert len(keys) >= 30  # the B2-342 census baseline; may only grow
    for e in data["keys"]:
        assert isinstance(e["key"], str) and e["key"]
        assert isinstance(e["first_line"], int) and e["first_line"] > 0
        assert "carries" in e and e["carries"]
        assert e["first_seq"] is None or isinstance(e["first_seq"], str)  # B2-40: never a float64


def test_load_event_key_registry_rejects_shape_drift(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"schema": "events_key_schema.v1"}), encoding="utf-8")
    with pytest.raises(ValueError):
        ss.load_event_key_registry(bad)
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(Exception):
        ss.load_event_key_registry(bad)
