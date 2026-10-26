"""tests/test_root_temp_sweep_patrol.py - Unit tests for root temp sweep patrol."""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from tools import root_temp_sweep_patrol as rtsp


def test_is_root_fossil():
    assert rtsp.is_root_fossil("%TEMP%arctic_123.json")
    assert rtsp.is_root_fossil("%TEMP%")
    assert rtsp.is_root_fossil("C?UsersfosteAppDataLocalTempkvsweep")
    assert rtsp.is_root_fossil("UsersfosteAppDataLocalTempllm7.json")
    assert rtsp.is_root_fossil("Temp")
    assert not rtsp.is_root_fossil("README.md")
    assert not rtsp.is_root_fossil("ag_test.py")


def test_scan_and_sweep(tmp_path: Path, capsys):
    # Setup clean root
    (tmp_path / "valid_file.txt").write_text("clean", encoding="utf-8")
    fossils = scan_and_report = rtsp.scan_root_fossils(tmp_path)
    assert len(fossils) == 0

    # Add fossils
    (tmp_path / "%TEMP%leak1.json").write_text("{}", encoding="utf-8")
    (tmp_path / "UsersfosteAppDataLocalTempbad.txt").write_text("dump", encoding="utf-8")
    (tmp_path / "Temp").mkdir()

    fossils = rtsp.scan_root_fossils(tmp_path)
    assert len(fossils) == 3

    # Test CLI check
    code = rtsp.main(["--root", str(tmp_path)])
    assert code == 0
    out = capsys.readouterr().out
    assert "ROOT-TEMP-PATROL: WARN (3 root temp fossils found)" in out

    # Test CLI strict
    code = rtsp.main(["--root", str(tmp_path), "--strict"])
    assert code == 1
    capsys.readouterr()

    # Test CLI JSON
    code = rtsp.main(["--root", str(tmp_path), "--json"])
    assert code == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["total_fossils"] == 3
    assert data["ok"] is False

    # Test sweep / quarantine
    quarantine_dir = tmp_path / "quarantine"
    code = rtsp.main(["--root", str(tmp_path), "--sweep", "--quarantine-dir", str(quarantine_dir)])
    assert code == 0

    # Verify root is clean
    remaining = rtsp.scan_root_fossils(tmp_path)
    assert len(remaining) == 0

    # Verify quarantined files exist
    assert (quarantine_dir / "%TEMP%leak1.json").is_file()
    assert (quarantine_dir / "UsersfosteAppDataLocalTempbad.txt").is_file()
    assert (quarantine_dir / "Temp").is_dir()
