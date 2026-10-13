"""fossil_check tests — the registry-driven FOSSIL-IN-FEED arm.

The arm exists because artifacts fossilized silently in live feed paths
(quantizer packs, 9 days, ~1,300 stale cycles). These pin: WARN fires on a
breached bar, tombstones never warn, missing registered artifacts are HARD,
and a stale registry path fails closed as cannot-verify.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import fossil_check as fc  # noqa: E402


def _mk_registry(tmp_path, entries):
    reg = tmp_path / "fossil_registry.json"
    reg.write_text(json.dumps({"entries": entries}), encoding="utf-8")
    return reg


def test_warn_fires_on_breached_bar(tmp_path, capsys):
    art = tmp_path / "stale.json"
    art.write_text("{}", encoding="utf-8")
    old = time.time() - 100 * 3600
    import os
    os.utime(art, (old, old))
    reg = _mk_registry(tmp_path, [{
        "artifact": str(art), "consumer": "test", "bar_hours": 24,
        "disposition": "recompile"}])
    # ROOT-relative resolution: fossil_check joins ROOT/artifact; absolute
    # paths pass through Path unchanged, so an absolute tmp artifact works.
    rc = fc.check(now=time.time(), registry_path=reg)
    out = capsys.readouterr().out
    assert rc == 1
    assert "WARN" in out and "stale.json" in out


def test_tombstone_never_warns(tmp_path, capsys):
    art = tmp_path / "dead.json"
    art.write_text("{}", encoding="utf-8")
    old = time.time() - 500 * 3600
    import os
    os.utime(art, (old, old))
    reg = _mk_registry(tmp_path, [{
        "artifact": str(art), "consumer": "none", "bar_hours": None,
        "disposition": "tombstoned"}])
    rc = fc.check(registry_path=reg)
    assert rc == 0
    assert "tombstoned" in capsys.readouterr().out


def test_missing_registered_artifact_is_hard(tmp_path, capsys):
    reg = _mk_registry(tmp_path, [{
        "artifact": str(tmp_path / "nope.json"), "consumer": "test",
        "bar_hours": 24, "disposition": "recompile"}])
    rc = fc.check(registry_path=reg)
    assert rc == 1
    assert "MISSING" in capsys.readouterr().out


def test_missing_tombstone_is_ok(tmp_path, capsys):
    reg = _mk_registry(tmp_path, [{
        "artifact": str(tmp_path / "gone.json"), "consumer": "none",
        "disposition": "tombstoned"}])
    rc = fc.check(registry_path=reg)
    assert rc == 0


def test_unreadable_registry_fails_closed(tmp_path):
    rc = fc.check(registry_path=tmp_path / "no-registry.json")
    assert rc == 2
