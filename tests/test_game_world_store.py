"""Q21-class regression for the game-world store (mag/game_world.py).

The store previously wrote non-atomically with no lock and, worse, swallowed
corrupt JSON into a silent empty world so the next set_state wiped the store.
Contracts here: concurrent set_state all land; corruption is loud.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

import mag.game_world as gw


def _point_store_at(tmp_path: Path, monkeypatch) -> Path:
    world = tmp_path / "world_state.json"
    monkeypatch.setattr(gw, "WORLD", world)
    monkeypatch.setattr(gw, "WORLD_DIR", tmp_path)
    return world


def test_concurrent_set_state_all_land(tmp_path, monkeypatch) -> None:
    world = _point_store_at(tmp_path, monkeypatch)
    gw.set_state("seed", 0)

    def writer(i: int) -> None:
        gw.set_state(f"key{i}", i)

    threads = [threading.Thread(target=writer, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    state = json.loads(world.read_text(encoding="utf-8"))
    got = sorted(k for k in state["world"] if k != "seed")
    assert got == [f"key{i}" for i in range(8)]
    assert len(state["changes"]) == 9  # seed + 8, none lost
    assert state["root"]


def test_corrupt_store_is_loud_not_a_silent_wipe(tmp_path, monkeypatch) -> None:
    world = _point_store_at(tmp_path, monkeypatch)
    world.write_text('{"schema": "game_world.v1", "world": {"a": 1}, "ch', encoding="utf-8")
    try:
        gw.set_state("b", 2)
    except ValueError as exc:
        assert "corrupt" in str(exc)
    else:
        raise AssertionError("corrupt store must raise, not reset to empty")
    # and the corrupt bytes are still on disk - nothing overwrote them
    assert world.read_text(encoding="utf-8").startswith('{"schema"')


def test_fresh_store_bootstraps(tmp_path, monkeypatch) -> None:
    _point_store_at(tmp_path, monkeypatch)
    out = gw.set_state("first", {"hp": 3})
    assert out["ok"] is True
    assert gw.get_state("first")["value"] == {"hp": 3}
