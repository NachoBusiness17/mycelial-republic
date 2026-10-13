"""Corpus map rescan pins (B2-104, 2026-09-26): mag/catalog_rescan.py.

Covers the upsert core over a synthetic mini-map in tmp_path, never the real
489k-row estate: load_index last-row-wins on a duplicated base path, and the
incremental decide rule (same signature unchanged, new path added, changed
path refreshed, missing path vanished, no tombstone rows invented).
Rule pins live in tests/test_catalog_tags.py, freshness pins in
tests/test_catalog_freshness.py.
"""
from __future__ import annotations

import datetime
import json
import os

import mag.catalog_rescan as cr


def _mk(root, rel, body=b"x", days_ago=0):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body)
    stamp = (datetime.datetime.now()
             - datetime.timedelta(days=days_ago)).timestamp()
    os.utime(p, (stamp, stamp))
    st = p.stat()
    mt = datetime.datetime.fromtimestamp(
        st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"id": "x" * 12, "path": rel.replace("\\", "/"),
            "bytes": st.st_size, "mtime": mt, "zone": "vault",
            "ext": p.suffix.lower(), "title": rel, "age_days": days_ago}


def _write_map(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


def test_load_index_last_row_wins_and_counts_dups(tmp_path):
    cat = tmp_path / "catalog.jsonl"
    old = _mk(tmp_path, "keep/a.txt", days_ago=40)
    new = _mk(tmp_path, "keep/a.txt", days_ago=0)
    _write_map(cat, [old, new])
    index, base_rows, base_dups = cr.load_index(str(cat))
    assert base_rows == 2
    assert base_dups == 1
    assert index["keep/a.txt"] == cr._sig(new["bytes"], new["mtime"])


def test_incremental_upsert_counts(tmp_path):
    estate = tmp_path / "estate"
    estate.mkdir()
    cat = tmp_path / "catalog.jsonl"      # outside the walked root
    jun = tmp_path / "junctions.jsonl"

    def mk(rel, body=b"x", days_ago=0):
        return _mk(estate, rel, body, days_ago)

    same = mk("same.txt")          # unchanged on disk
    chg = mk("changed.txt")        # will change on disk
    gone = mk("vanished.txt")      # will be deleted
    _write_map(cat, [same, chg, gone])
    (estate / "changed.txt").write_bytes(b"changed body")
    (estate / "vanished.txt").unlink()
    mk("added.txt")                # new on disk

    summary = cr.incremental(str(cat), str(jun), root=str(estate))
    assert summary["added"] == 1
    assert summary["refreshed"] == 1
    assert summary["unchanged"] == 1
    assert summary["vanished"] == 1
    # appended rows: added.txt + changed.txt (fresh row after the stale one)
    lines = [json.loads(l) for l in
             open(str(cat), encoding="utf-8").read().splitlines()]
    paths = [r["path"] for r in lines]
    assert paths.count("added.txt") == 1
    assert paths.count("changed.txt") == 2  # stale base row + refreshed row
    assert "vanished.txt" not in paths[3:]  # no tombstone rows invented
