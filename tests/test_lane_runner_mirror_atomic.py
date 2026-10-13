"""Regression: _mirror must never O_TRUNC the live mirrored file.

Cause: 2026-10-05T03:59:15Z "mirror fail research: [Errno 22] Invalid
argument: /app/dashboard/static/trails/research.jsonl" - _mirror's plain
write_text was the uncured twin of the state-path O_TRUNC burst class
_save_state cured 2026-10-04 (commit 9c52757f9 half). Fix: _atomic_copy
ports the same unique-tmp + os.replace rename-CAS idiom to the mirror
site. The tripwire: mirror writes go through tmp+replace, a failing
replace leaves the live file intact, and no tmp crumbs survive.
"""
import os
from pathlib import Path

from mag.lane_runner import _atomic_copy, _mirror


def test_atomic_copy_swaps_bytes_and_cleans_tmp(tmp_path):
    src = tmp_path / "src.jsonl"
    dst = tmp_path / "dst.jsonl"
    src.write_text("old-line\n", encoding="utf-8")
    dst.write_text("stale\n", encoding="utf-8")
    src.write_text("new-line\n", encoding="utf-8")
    _atomic_copy(src, dst)
    assert dst.read_text(encoding="utf-8") == "new-line\n"
    assert [p.name for p in tmp_path.iterdir() if ".tmp-" in p.name] == []


def test_atomic_copy_failed_replace_leaves_live_file_intact(tmp_path, monkeypatch):
    src = tmp_path / "src.md"
    dst = tmp_path / "dst.md"
    src.write_text("fresh\n", encoding="utf-8")
    dst.write_text("live-bytes\n", encoding="utf-8")
    real_replace = os.replace

    def boom(a, b, *a_, **k_):
        raise OSError(22, "Invalid argument")

    monkeypatch.setattr("mag.lane_runner.os.replace", boom)
    try:
        _atomic_copy(src, dst)
        raised = False
    except OSError:
        raised = True
    assert raised
    assert dst.read_text(encoding="utf-8") == "live-bytes\n"
    assert [p.name for p in tmp_path.iterdir() if ".tmp-" in p.name] == []
    _ = real_replace  # keep the real binding referenced for clarity


def test_mirror_routes_both_surfaces_through_atomic_copy(tmp_path, monkeypatch):
    lane_dir = tmp_path / "lanes" / "research"
    static = tmp_path / "static"
    lane_dir.mkdir(parents=True)
    (static / "trails").mkdir(parents=True)
    (static / "lanes").mkdir(parents=True)
    (lane_dir / "trail.jsonl").write_text('{"e":1}\n', encoding="utf-8")
    (lane_dir / "surface.md").write_text("# surface\n", encoding="utf-8")
    seen = []
    monkeypatch.setattr("mag.lane_runner.LANES", tmp_path / "lanes")
    monkeypatch.setattr("mag.lane_runner.STATIC", static)
    monkeypatch.setattr(
        "mag.lane_runner._atomic_copy",
        lambda s, d: seen.append(d.name) or _atomic_copy(s, d),
    )
    _mirror("research")
    # both surfaces mirrored, both through the atomic path, live bytes landed
    assert sorted(seen) == ["research.jsonl", "research.md"]
    assert (static / "trails" / "research.jsonl").read_text(encoding="utf-8") == '{"e":1}\n'
    assert (static / "lanes" / "research.md").read_text(encoding="utf-8") == "# surface\n"
