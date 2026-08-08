"""Tests for the memory-mapping / obfuscation layer (mag.memory_map)."""
import mag.memory_map as mm


def _isolate(tmp_path, monkeypatch):
    monkeypatch.setattr(mm, "MAPPING_DIR", tmp_path)
    monkeypatch.setattr(mm, "KEY_PATH", tmp_path / "key.json")
    monkeypatch.setattr(mm, "SALT_PATH", tmp_path / "salt")
    monkeypatch.setattr(mm, "STORE_PATH", tmp_path / "store.jsonl")


def test_register_produces_opaque_token(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    r = mm.register("foste", kind="user")
    assert r["ok"] is True
    # token is opaque: does not contain the real name
    assert "foste" not in r["token"]
    assert r["token"].startswith("u-")
    # idempotent / stable
    r2 = mm.register("foste", kind="user")
    assert r2["token"] == r["token"] and r2["existing"] is True


def test_encode_obfuscates_and_decode_recovers(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    mm.register("Alice", kind="user")
    mm.register("quantum_lab", kind="project")
    text = "Alice works in quantum_lab."
    enc = mm.encode(text)
    assert "Alice" not in enc and "quantum_lab" not in enc  # not readable at rest
    assert mm.decode(enc) == "Alice works in quantum_lab."  # operator surface recovers


def test_surface_modes(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    mm.register("Bob", kind="user")
    world = mm.surface("Bob said hi", mode="world")
    op = mm.surface(world, mode="operator")
    assert "Bob" not in world
    assert op == "Bob said hi"


def test_assert_cage_detects_leak(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    mm.register("Carol", kind="user")
    # write a raw (leaked) row with the real entity into the store
    mm.STORE_PATH.write_text('{"note": "Carol is here"}\n', encoding="utf-8")
    c = mm.assert_cage()
    assert c["ok"] is False
    assert "Carol" in c["leaked_real_entities"]
    # after encoding it, the cage is clean
    mm.STORE_PATH.write_text(mm.encode('{"note": "Carol is here"}') + "\n", encoding="utf-8")
    c2 = mm.assert_cage()
    assert c2["ok"] is True
