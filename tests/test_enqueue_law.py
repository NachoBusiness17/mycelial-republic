"""Tests for tools/enqueue_law.py (Mickey17 W3J, 2026-09-29).

Covers the spec's three contracts against a fixture ledger holding one zombie
piece (stale enqueues to a module that does not exist under the fixture root)
plus one healthy piece (its module exists there): the census names the zombie
and not the healthy piece, the epitaph row lands in the graveyard with the
frozen shape and is idempotent on re-run, and --prune removes zombie entries
from the COPY only while the original ledger bytes never change. Also pins
the cadence grace window (fresh enqueues to a missing module are not yet
zombies) and the fail-closed exit-2 paths.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tools import enqueue_law

NOW = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)
ZOMBIE_PIECE = "nomic_rules_patch"
ZOMBIE_MODULE = "mag/game_rules.py"
HEALTHY_PIECE = "dice_pool"
HEALTHY_MODULE = "mag/game_dice.py"


def _ts(delta_days: int) -> str:
    return (NOW - timedelta(days=delta_days)).isoformat()


def _row(piece: str, module: str, delta_days: int, enqueued: bool = True) -> dict:
    return {"ts": _ts(delta_days), "action": "test", "piece": piece,
            "module": module, "enqueued": enqueued,
            "queue_id": "qfixture" if enqueued else None}


def _fixture_rows() -> list[dict]:
    return [
        _row(ZOMBIE_PIECE, ZOMBIE_MODULE, 12),            # stale zombie enqueue
        _row(ZOMBIE_PIECE, ZOMBIE_MODULE, 9),             # stale zombie enqueue
        _row(ZOMBIE_PIECE, ZOMBIE_MODULE, 1),             # fresh: inside cadence
        _row(ZOMBIE_PIECE, ZOMBIE_MODULE, 12, enqueued=False),  # dequeue marker
        _row(HEALTHY_PIECE, HEALTHY_MODULE, 30),          # landed long ago
    ]


def _make_ledger(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Ledger + graveyard + pruned paths plus a fixture root whose only
    existing module is the healthy one."""
    root = tmp_path / "estate"
    (root / "mag").mkdir(parents=True)
    (root / "mag" / "game_dice.py").write_text("# healthy module\n", encoding="utf-8")
    ledger = tmp_path / "FLOW_LEDGER.jsonl"
    ledger.write_text(
        "".join(json.dumps(r) + "\n" for r in _fixture_rows()), encoding="utf-8")
    return ledger, tmp_path / "GRAVEYARD.jsonl", tmp_path / "pruned.jsonl", root


def test_census_names_zombie_not_healthy(tmp_path, capsys):
    ledger, graveyard, pruned, root = _make_ledger(tmp_path)
    code = enqueue_law.run(ledger=ledger, graveyard=graveyard, pruned=pruned,
                           root=root, days=7, now=NOW)
    assert code == 1  # zombies found
    out = capsys.readouterr().out
    assert f"ZOMBIE {ZOMBIE_PIECE} -> {ZOMBIE_MODULE}" in out
    assert "2 stale of 3 enqueues" in out
    assert "STILL PROMISING 1 fresh" in out  # the fresh enqueue is named
    assert HEALTHY_PIECE not in out          # landed pieces never appear
    census = enqueue_law.zombie_census(enqueue_law.load_ledger(ledger), root, 7, NOW)
    assert [z["piece"] for z in census["zombies"]] == [ZOMBIE_PIECE]
    z = census["zombies"][0]
    assert z["zombie_entries"] == 2 and z["total_enqueues"] == 3
    assert z["first_enqueued"] == _ts(12) and z["last_enqueued"] == _ts(1)
    assert census["grace"] == [] and census["landed_pairs"] == 1


def test_grace_inside_cadence_is_not_zombie(tmp_path, capsys):
    root = tmp_path / "estate"
    (root / "mag").mkdir(parents=True)
    ledger = tmp_path / "FLOW_LEDGER.jsonl"
    ledger.write_text(json.dumps(_row("late_clone", "mag/game_late.py", 2)) + "\n",
                      encoding="utf-8")
    code = enqueue_law.run(ledger=ledger, graveyard=tmp_path / "GRAVEYARD.jsonl",
                           pruned=tmp_path / "p.jsonl", root=root, days=7, now=NOW)
    assert code == 0  # no stale enqueue yet: the cadence is still running
    out = capsys.readouterr().out
    assert "grace late_clone -> mag/game_late.py" in out


def test_epitaph_written_and_idempotent(tmp_path):
    ledger, graveyard, pruned, root = _make_ledger(tmp_path)
    for _ in range(2):  # second run must not duplicate the epitaph
        code = enqueue_law.run(ledger=ledger, graveyard=graveyard, pruned=pruned,
                               root=root, days=7, now=NOW)
        assert code == 1
    lines = [l for l in graveyard.read_text(encoding="utf-8").splitlines() if l]
    assert len(lines) == 1  # append-only + dedupe by (piece, module)
    row = json.loads(lines[0])
    # Frozen shape and order per the W3J spec.
    assert list(row) == ["piece", "module", "times_enqueued", "first_ts", "epitaph"]
    assert row == {"piece": ZOMBIE_PIECE, "module": ZOMBIE_MODULE,
                   "times_enqueued": 3, "first_ts": _ts(12),
                   "epitaph": "module never existed"}


def test_prune_only_touches_copy(tmp_path):
    ledger, graveyard, pruned, root = _make_ledger(tmp_path)
    original = ledger.read_bytes()
    code = enqueue_law.main([
        "--ledger", str(ledger), "--graveyard", str(graveyard),
        "--pruned", str(pruned), "--root", str(root), "--days", "7", "--prune"])
    assert code == 1
    assert ledger.read_bytes() == original  # the original is never modified
    kept = [json.loads(l) for l in
            pruned.read_text(encoding="utf-8").splitlines() if l]
    assert len(kept) == 3  # 5 fixture rows minus the 2 stale zombie enqueues
    assert not any(r["piece"] == ZOMBIE_PIECE and r["enqueued"] and
                   r["ts"] in (_ts(12), _ts(9)) for r in kept)
    # The fresh zombie enqueue, the dequeue marker and the healthy row survive.
    assert any(r["piece"] == ZOMBIE_PIECE and r["ts"] == _ts(1) for r in kept)
    assert any(r["piece"] == ZOMBIE_PIECE and r["enqueued"] is False for r in kept)
    assert any(r["piece"] == HEALTHY_PIECE for r in kept)


def test_clean_ledger_exit_0_and_no_epitaph(tmp_path, capsys):
    root = tmp_path / "estate"
    (root / "mag").mkdir(parents=True)
    (root / "mag" / "game_dice.py").write_text("# landed\n", encoding="utf-8")
    ledger = tmp_path / "FLOW_LEDGER.jsonl"
    ledger.write_text(json.dumps(_row(HEALTHY_PIECE, HEALTHY_MODULE, 30)) + "\n",
                      encoding="utf-8")
    graveyard = tmp_path / "GRAVEYARD.jsonl"
    code = enqueue_law.run(ledger=ledger, graveyard=graveyard,
                           pruned=tmp_path / "p.jsonl", root=root, now=NOW)
    assert code == 0
    assert "ENQUEUE-LAW: ok" in capsys.readouterr().out
    assert not graveyard.exists()  # nothing died, nothing buried


def test_fail_closed_missing_ledger_exit_2(tmp_path, capsys):
    code = enqueue_law.run(ledger=tmp_path / "nope.jsonl",
                           graveyard=tmp_path / "G.jsonl",
                           pruned=tmp_path / "p.jsonl", root=tmp_path, now=NOW)
    assert code == 2
    assert "cannot verify" in capsys.readouterr().out


def test_fail_closed_malformed_rows_exit_2(tmp_path):
    root = tmp_path
    bad_bodies = [
        "{not json}\n",                                        # unparseable line
        json.dumps({"ts": _ts(9), "enqueued": True}) + "\n",   # missing keys
        json.dumps({"ts": "2026-09-01T00:00:00", "piece": "p",  # naive ts
                    "module": "mag/x.py", "enqueued": True}) + "\n",
        json.dumps({"ts": _ts(9), "piece": "p",                 # absolute module
                    "module": "C:/abs/x.py", "enqueued": True}) + "\n",
    ]
    for body in bad_bodies:
        ledger = tmp_path / "FLOW_LEDGER.jsonl"
        ledger.write_text(body, encoding="utf-8")
        assert enqueue_law.run(ledger=ledger, graveyard=tmp_path / "G.jsonl",
                               pruned=tmp_path / "p.jsonl", root=root,
                               now=NOW) == 2


def test_prune_refuses_same_path_as_ledger(tmp_path):
    ledger, graveyard, pruned, root = _make_ledger(tmp_path)
    code = enqueue_law.run(ledger=ledger, graveyard=graveyard, pruned=ledger,
                           root=root, prune=True, now=NOW)
    assert code == 2  # a pruned "copy" over the original would break the law
