"""L8 dot-dir first-class lock (disk_audit_20261009, LAW_PACK.md law L8).

The founding incident: the largest estate item (.zcode, 335.3GB in the first
live smith row, cd118ed70) was invisible to the first disk inventory because
that instrument walked non-dot globs, and glob's "*" wildcard never matches a
name that begins with a dot (watch/inbox/disk_audit_20261009/internal/
TIMELINE_AND_ESTATE_LAW.md root cause 2; watch/inbox/DISK_INVENTORY_20261008.md).

These pins lock the law against the module's own constants and pure
functions (no live disk walks): the dot-dir seats (.zcode class, .ollama,
HF cache) stay permanent first-class smith rows, the monsters keep
pagefile/vhdx, and the non-dot-glob blind spot is demonstrated permanently
on a synthetic tmp home.
"""
from __future__ import annotations

import glob
import os
import datetime as dt
from pathlib import Path

import tools.disk_smith as ds
from tools.disk_smith import AGENT_HOMES, GB, SYSTEM_MONSTERS, _size_gb, delta


def _dot_components(raw: str) -> list[str]:
    return [part for part in Path(raw).parts if part.startswith(".")]


def test_agent_homes_carry_the_founding_dot_seats():
    # The measured seats include the dot-dir classes the incident missed.
    assert AGENT_HOMES["zcode_cache"].endswith(".zcode")
    assert ".ollama" in _dot_components(AGENT_HOMES["ollama_garden"])
    hf = _dot_components(AGENT_HOMES["hf_cache"])
    assert ".cache" in hf
    assert "huggingface" in Path(AGENT_HOMES["hf_cache"]).parts


def test_dot_seats_are_permanent_majority_rows():
    # 7 of 8 named seats live inside dot dirs today (.zcode/.codex/.grok/
    # .openclaw/.cache/opencode/.ollama/.cache/huggingface); dropping any
    # dot seat below this floor is the L8 regression.
    dot_seats = [label for label, raw in AGENT_HOMES.items() if _dot_components(raw)]
    assert len(dot_seats) >= 7
    assert "zcode_cache" in dot_seats


def test_seats_are_explicit_paths_never_globs():
    # L8: no inventory walks non-dot globs; the smith's rows are named
    # paths, so no seat or monster definition may carry a wildcard.
    for table in (AGENT_HOMES, SYSTEM_MONSTERS):
        for raw in table.values():
            assert not any(ch in raw for ch in "*?["), raw


def test_nondot_glob_blind_spot_founding_incident(tmp_path):
    # The founding incident as a permanent test: in a synthetic home the
    # biggest seat is a dot-dir; the non-dot-glob inventory the first audit
    # used never sees it. The disk was never hiding anything (os.listdir
    # and a full walk both see it); the instrument was blind.
    home = tmp_path / "home"
    home.mkdir()
    dot_seat_name = Path(AGENT_HOMES["zcode_cache"]).name  # ".zcode"
    zcode = home / dot_seat_name / "sessions"
    zcode.mkdir(parents=True)
    blob_bytes = 2 * 2**20  # 2MiB of transcript exhaust
    (zcode / "transcripts.bin").write_bytes(b"\0" * blob_bytes)
    docs = home / "Documents"
    docs.mkdir()
    note_bytes = 1024
    (docs / "note.txt").write_bytes(b"x" * note_bytes)

    seen = [Path(p).name for p in glob.glob(str(home / "*"))]
    assert dot_seat_name not in seen  # the blind spot
    assert "Documents" in seen
    assert dot_seat_name in os.listdir(home)  # visible to a complete listing

    # The non-dot inventory under-reports: it sums only the roots it saw.
    glob_bytes = sum(
        f.stat().st_size
        for root in glob.glob(str(home / "*"))
        for f in Path(root).rglob("*")
        if f.is_file()
    )
    truth_bytes = sum(
        f.stat().st_size for f in home.rglob("*") if f.is_file()
    )
    assert glob_bytes == note_bytes
    assert truth_bytes == note_bytes + blob_bytes
    assert glob_bytes < truth_bytes

    # The smith's way: the dot seat is an explicit named row, and the
    # smith's own measurer sees the full bytes the glob missed.
    seat_gb = _size_gb(home / dot_seat_name)
    assert seat_gb is not None
    assert abs(seat_gb - blob_bytes / GB) < 1e-9


def test_dot_seat_flows_through_delta_as_first_class_row():
    # The seat row is first-class in the delta math: pure functions, no
    # disk. If dot seats stop carrying deltas, GB/day alerts go blind.
    prev = {"seats": {"zcode_cache": 335.3}}
    curr = {"seats": {"zcode_cache": 340.0}}
    assert delta(curr, prev) == {"seats": {"zcode_cache": 4.7}}


def test_monsters_rows_include_pagefile_and_vhdx():
    # The founding monsters stay named rows: pagefile.sys ballooned to
    # 132.9GB and docker_data.vhdx to 132GB in the 1.3TB incident.
    assert SYSTEM_MONSTERS["pagefile"].endswith("pagefile.sys")
    assert SYSTEM_MONSTERS["docker_data_vhdx"].endswith(".vhdx")


def test_snap_records_none_row_for_unmeasurable_path(tmp_path, monkeypatch):
    # The 2026-10-09 cure locked: a seat that exists but cannot be measured
    # (stat/rglob raises OSError - locked system paths) is a None row, never
    # a crashed sweep. Pre-fix snap computed round(None, 2) and died
    # mid-loop, blinding the daily smith on every dot seat at once (the L8
    # falsifier). Monkeypatched tables: no live disk walk, just the volume
    # stat every snap does.
    locked = tmp_path / "locked_seat"
    locked.write_bytes(b"\0" * 1024)  # exists...
    monkeypatch.setattr(ds, "SYSTEM_MONSTERS", {"locked": str(locked)})
    monkeypatch.setattr(ds, "AGENT_HOMES", {})
    monkeypatch.setattr(ds, "ESTATE_BUCKETS", {})
    monkeypatch.setattr(ds, "_size_gb", lambda p: None)  # ...but unmeasurable
    row = ds.snap(dt.datetime.now(dt.timezone.utc))
    assert row["monsters"]["locked"] is None
    assert row["seats"] == {}
    assert row["estate"] == {}
