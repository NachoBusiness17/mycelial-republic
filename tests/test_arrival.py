"""tests for arrival — deterministic + stateless, no monkeypatch of internals.

RIB (frozen spec):
  _packs()        -> read the swarm's authored research packs (.answer.*.md) from PACKS_DIR,
                     newest first; grounded from disk (never invented).
  _distill(text)  -> deterministic $0 distillation: longest dense paragraph, collapsed whitespace,
                     trimmed; honest lossy extraction (not a frontier summary).
  fold_authored() -> read authored packs, distill each to invariant, publish as self-authored RIB
                     (source='swarm') via rib_bus.publish_rib -> fold to verkle. Idempotent via
                     content-hash dedup (re-folding the same pack folds once, not repeatedly).
  status()        -> read back self-authored RIBs riding the wave from the rib_bus store.
  arrival()       -> fold + status, honest (folds measured from store, packs from disk).

Stateless-correct: we exercise the pure logic (_distill, pack discovery) against a tmp dir and the
real rib_bus store is only touched through publish_rib (whose own dedup makes it safe/idempotent).
No monkeypatch of internals.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import arrival  # noqa: E402


def _write_pack(packs_dir: Path, name: str, body: str) -> Path:
    p = packs_dir / name
    p.write_text(body, encoding="utf-8")
    return p


def test_distill_takes_longest_dense_paragraph():
    text = ("Short.\n\n"
            "This is the meat of the authored pack: the dense paragraph carrying the real "
            "invariant that a cold worker can re-derive and fold. It is substantially longer than "
            "the surrounding fragments and represents the standing-wave structure to extract.")
    out = arrival._distill(text, limit=400)
    assert "dense paragraph" in out
    assert len(out) <= 400
    # whitespace collapsed
    assert "\n" not in out


def test_distill_empty_falls_back():
    assert arrival._distill("", limit=100) == ""


def test_packs_reads_from_dir(tmp_path):
    d = tmp_path / "research_packs"
    d.mkdir(parents=True)
    _write_pack(d, "p1.answer.swarm.md", "alpha " * 50)
    _write_pack(d, "p2.answer.swarm.md", "beta " * 50)
    arrival.PACKS_DIR = d
    packs = arrival._packs()
    assert len(packs) == 2
    names = [p["name"] for p in packs]
    assert "p1.answer.swarm.md" in names and "p2.answer.swarm.md" in names
    # each pack carries its text + length (grounded from disk)
    assert all(p["chars"] > 0 for p in packs)


def test_fold_authored_idempotent_and_ok(tmp_path):
    d = tmp_path / "research_packs"
    d.mkdir(parents=True)
    _write_pack(d, "pack.answer.swarm.md", ("Invariant body: " * 30) + " authoring logic core.")
    arrival.PACKS_DIR = d
    r1 = arrival.fold_authored(limit=8, min_chars=10)
    assert r1["ok"] is True
    assert r1["n_folded"] >= 1
    assert all(f["ok"] for f in r1["folded"])
    # second run is idempotent: no NEW keys added (content-hash dedup in rib_bus.publish_rib)
    r2 = arrival.fold_authored(limit=8, min_chars=10)
    keys1 = {f["key"] for f in r1["folded"] if f.get("key")}
    keys2 = {f["key"] for f in r2["folded"] if f.get("key")}
    assert keys1 == keys2  # re-folding folds the SAME key, never a duplicate


def test_arrival_report_honest(tmp_path):
    d = tmp_path / "research_packs"
    d.mkdir(parents=True)
    _write_pack(d, "pack.answer.swarm.md", ("Meat of the pack: " * 40))
    arrival.PACKS_DIR = d
    r = arrival.arrival(limit=8, min_chars=10)
    assert r["ok"] is True
    assert "fold" in r and "now_riding" in r and "honesty" in r
    assert r["honesty"]  # non-empty honesty field
    assert r["n_packs"] >= 1


def test_recreate_honest_verdict():
    # recreate is deterministic + $0: it mounts the self-authored RIBs and reports whether a cold
    # worker can use them. The verdict must be HONEST (arrived only when RIBs ride + steer usable).
    r = arrival.recreate()
    assert r["ok"] is True
    assert "arrived" in r
    assert "n_self_authored_riding" in r and "steer_block_usable" in r
    assert r["honesty"]  # honesty field present
    # consistency: arrived requires both a mounted self-authored RIB AND a usable steer block
    assert r["arrived"] == (r["n_self_authored_riding"] >= 1 and r["steer_block_usable"])
