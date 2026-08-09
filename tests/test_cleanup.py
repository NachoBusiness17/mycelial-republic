"""Test the passive cleanup module (audit + move-to-trash + cadence)."""
from __future__ import annotations

from pathlib import Path

import pytest

from mag.cleanup import audit, cleanup


def test_audit_finds_transient_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("mag.cleanup.ROOT", tmp_path)
    d = tmp_path / "codex_nested_temp"
    d.mkdir()
    (d / "a.txt").write_text("x" * 10, encoding="utf-8")
    rep = audit()
    assert rep["n"] >= 1
    assert any("codex_nested_temp" in i["path"] for i in rep["items"])


def test_audit_finds_transient_file(tmp_path, monkeypatch):
    monkeypatch.setattr("mag.cleanup.ROOT", tmp_path)
    (tmp_path / "_tmp_probe.py").write_text("print(1)", encoding="utf-8")
    rep = audit()
    assert any("_tmp_probe.py" in i["path"] for i in rep["items"])


def test_cleanup_dry_does_not_move(tmp_path, monkeypatch):
    monkeypatch.setattr("mag.cleanup.ROOT", tmp_path)
    d = tmp_path / "codex_tmp"
    d.mkdir()
    res = cleanup(dry=True)
    assert res["dry"] is True
    assert d.exists()  # nothing moved


def test_cleanup_live_moves_to_trash(tmp_path, monkeypatch):
    monkeypatch.setattr("mag.cleanup.ROOT", tmp_path)
    monkeypatch.setattr("mag.cleanup.TRASH", tmp_path / "memory" / "trash")
    d = tmp_path / "codex_tmp"
    d.mkdir()
    (d / "f.txt").write_text("data", encoding="utf-8")
    res = cleanup(dry=False)
    assert res["moved"] >= 1
    assert not d.exists()  # removed from project
    assert (tmp_path / "memory" / "trash").exists()  # recoverable in trash
