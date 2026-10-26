"""backup_chain completeness (2026-10-15): a truncated backup must be marked INCOMPLETE, raise,
and never count toward the keep-7 prune; a full copy must verify and count; the 20261004 pin
stays exempt. Hermetic: every path is redirected into tmp_path (the live-estate write fence in
conftest also refuses memory/biography writes)."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mag.verkle_knot as vk  # noqa: E402


@pytest.fixture()
def env(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("backup_chain_t", ROOT / "scripts" / "backup_chain.py")
    bc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bc)
    src = tmp_path / "biography"
    (src / "knots" / ".mimosa").mkdir(parents=True)
    (src / "verkle_chain.jsonl").write_text("".join(f'{{"i":{i}}}\n' for i in range(300)), encoding="utf-8")
    (src / "verkle_tip.json").write_text('{"tip":"abc"}', encoding="utf-8")
    for i in range(400):
        (src / "knots" / f"k{i:05d}.knot.json").write_text("x" * (100 + i % 7), encoding="utf-8")
    monkeypatch.setattr(vk, "CHAIN", src / "verkle_chain.jsonl")
    monkeypatch.setattr(vk, "KNOTS", src / "knots")
    monkeypatch.setattr(vk, "LOCK", src / ".verkle.lock")
    monkeypatch.setattr(bc, "BACKUP_ROOT", tmp_path / "biography_backup")
    monkeypatch.setattr(bc, "ATTENTION", tmp_path / "attention.md")
    monkeypatch.setattr(bc, "LOG", tmp_path / "backup_chain.log")
    for day in range(1, 9):  # 8 verified-complete history folders
        d = bc.BACKUP_ROOT / f"biography_backup_202609{day:02d}"
        (d / "knots").mkdir(parents=True)
        (d / bc.COMPLETE_MANIFEST).write_text("{}", encoding="utf-8")
    (bc.BACKUP_ROOT / "biography_backup_20261004" / "knots").mkdir(parents=True)  # the pin
    return bc, src


def _names(bc):
    return sorted(p.name for p in bc.BACKUP_ROOT.iterdir())


def test_killed_mid_copy_leaves_marker_and_is_not_counted(env, monkeypatch):
    bc, _ = env
    monkeypatch.setattr(bc, "_today", lambda: "20261020")
    real, n = bc._copy_if_needed, {"i": 0}

    def dying(s, d):
        n["i"] += 1
        if n["i"] > 221:
            raise KeyboardInterrupt("simulated kill")
        return real(s, d)

    monkeypatch.setattr(bc, "_copy_if_needed", dying)
    before = _names(bc)
    with pytest.raises(KeyboardInterrupt):
        bc.backup()
    d = bc.BACKUP_ROOT / "biography_backup_20261020"
    assert json.loads((d / bc.INCOMPLETE_MARKER).read_text())["state"] == "copy_failed"
    assert not bc.is_complete(d)
    assert set(before) <= set(_names(bc))  # nothing pruned


def test_truncated_copy_fails_loudly_and_never_prunes(env, monkeypatch):
    bc, src = env
    monkeypatch.setattr(bc, "_today", lambda: "20261021")
    short = src.parent / "short"
    short.mkdir()
    for i in range(221):
        (short / f"k{i:05d}.knot.json").write_bytes((src / "knots" / f"k{i:05d}.knot.json").read_bytes())
    real_verify = bc.verify
    monkeypatch.setattr(vk, "KNOTS", short)  # copy sees a truncated view...
    monkeypatch.setattr(bc, "verify", lambda dest, chain, knots: real_verify(dest, chain, src / "knots"))
    before = _names(bc)
    with pytest.raises(bc.BackupIncomplete) as ei:
        bc.backup()
    assert any("knots 221/400 files" in p for p in ei.value.summary["problems"])
    d = bc.BACKUP_ROOT / "biography_backup_20261021"
    assert (d / bc.INCOMPLETE_MARKER).is_file() and not bc.is_complete(d)
    assert set(before) <= set(_names(bc))


def test_tip_mismatch_is_incomplete(env, monkeypatch):
    bc, _ = env
    monkeypatch.setattr(bc, "_today", lambda: "20261022")
    real = bc._sha256
    monkeypatch.setattr(bc, "_sha256", lambda p: "0" if p.name == "verkle_tip.json" and "backup" in str(p) else real(p))
    with pytest.raises(bc.BackupIncomplete) as ei:
        bc.backup()
    assert "tip sha256 differs" in ei.value.summary["problems"]


def test_resume_full_copy_passes_counts_and_prunes_only_complete(env, monkeypatch):
    bc, _ = env
    monkeypatch.setattr(bc, "_today", lambda: "20261020")
    d = bc.BACKUP_ROOT / "biography_backup_20261020"
    (d / "knots").mkdir(parents=True)
    (d / bc.INCOMPLETE_MARKER).write_text('{"state": "copying"}', encoding="utf-8")
    inc = bc.BACKUP_ROOT / "biography_backup_20261019"  # an older incomplete folder
    (inc / "knots").mkdir(parents=True)
    (inc / bc.INCOMPLETE_MARKER).write_text('{"state": "failed_verification"}', encoding="utf-8")
    r = bc.backup()
    assert r["ok"] and r["counted"]
    assert r["verify"]["knots"]["backup_files"] == r["verify"]["knots"]["source_files"] == 400
    assert r["verify"]["chain_sha256"]["source"] == r["verify"]["chain_sha256"]["backup"]
    assert r["verify"]["tip_sha256"]["source"] == r["verify"]["tip_sha256"]["backup"]
    assert r["resumed_from"]["state"] == "copying"
    assert bc.is_complete(d) and not (d / bc.INCOMPLETE_MARKER).exists()
    assert r["removed"] == ["biography_backup_20260901", "biography_backup_20260902"]
    names = _names(bc)
    assert "biography_backup_20261004" in names  # pin exempt
    assert "biography_backup_20261019" in names  # incomplete: not counted, not pruned
    assert sum(bc.is_complete(bc.BACKUP_ROOT / n) for n in names) == bc.KEEP
    assert bc.backup()["skipped"] == "already_today"


def test_alarm_writes_attention_block(env):
    bc, _ = env
    bc.alarm("INCOMPLETE: knots 221/400 files (< 99%)", {"dest": "x"})
    t = bc.ATTENTION.read_text(encoding="utf-8")
    assert "### Chain backup patrol fired" in t and "221/400" in t
    assert "ALARM INCOMPLETE" in bc.LOG.read_text(encoding="utf-8")
