"""Icon-drop icon-thread tests (B2-414, 2026-09-26).

The old drop() ico_line ('start "" /D "%CD%" /B >nul 2>&1') was a line that
launched nothing and never referenced the icon path; a .cmd cannot carry an
icon. Spec (docstring, B2-414): the icon belongs on a .lnk via
drop_shortcut's IconLocation, so drop() with an icon now lays a companion
.lnk and the .cmd stays clean. Tests run the whole surface inside tmp_path
(desktop_folder + LEDGER patched, drop_shortcut recorded not executed).
"""
from __future__ import annotations

from pathlib import Path

import mag.icon_drop as idp


def _patch_surface(tmp_path, monkeypatch):
    folder = tmp_path / "desktop" / "Mag" / "Tools"
    folder.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(idp, "desktop_folder", lambda: folder)
    monkeypatch.setattr(idp, "LEDGER", tmp_path / "ledger.jsonl")
    calls = []
    monkeypatch.setattr(idp, "drop_shortcut",
                        lambda name, target_path, args="", *, icon=None, desc="":
                        calls.append({"name": name, "target": target_path,
                                      "args": args, "icon": icon, "desc": desc})
                        or {"path": str(folder / f"{name}.lnk"), "status": "dropped"})
    return folder, calls


def test_ico_bytes_never_appear_in_the_cmd(tmp_path, monkeypatch):
    ico = tmp_path / "mag_agent.ico"
    ico.write_bytes(b"ico")
    folder, _ = _patch_surface(tmp_path, monkeypatch)
    row = idp.drop("t", "ver", icon=str(ico))
    cmd = Path(row["path"]).read_bytes()
    assert b".ico" not in cmd                          # the brief's falsifier
    assert b'start "" /D' not in cmd                   # the dead line is gone
    assert b"@echo off" in cmd                         # still a valid launcher
    assert Path(row["path"]).suffix == ".cmd"


def test_icon_given_lays_a_companion_lnk(tmp_path, monkeypatch):
    ico = tmp_path / "mag_agent.ico"
    ico.write_bytes(b"ico")
    folder, calls = _patch_surface(tmp_path, monkeypatch)
    row = idp.drop("ver", "ver.cmd", icon=str(ico))
    assert len(calls) == 1
    call = calls[0]
    assert call["icon"] == str(ico)                    # the icon thread lands on the .lnk
    assert call["target"] == str(folder / "ver.cmd")
    assert row["companion_status"] == "dropped"
    assert row["companion_lnk"].endswith("ver.lnk")


def test_auto_secret_carries_no_dead_line_and_lays_the_lnk(tmp_path, monkeypatch):
    ico = tmp_path / "mag_agent.ico"
    ico.write_bytes(b"ico")
    monkeypatch.setattr(idp, "ROOT_CMD", ico)
    folder, calls = _patch_surface(tmp_path, monkeypatch)
    res = idp.auto("need the secret entry flow")
    assert res["matched"] == "secret"
    row = res["dropped"]
    cmd = Path(row["path"]).read_bytes()
    assert b'start "" /D' not in cmd                   # no dead line on the real drop path
    assert any(c["icon"] == str(ico) for c in calls)   # companion .lnk carries the icon


def test_no_icon_means_no_companion_and_no_ico_reference(tmp_path, monkeypatch):
    folder, calls = _patch_surface(tmp_path, monkeypatch)
    row = idp.drop("plain", "ver")
    assert calls == []
    assert "companion_lnk" not in row
    assert b".ico" not in Path(row["path"]).read_bytes()


def test_missing_icon_file_means_no_companion(tmp_path, monkeypatch):
    folder, calls = _patch_surface(tmp_path, monkeypatch)
    row = idp.drop("ghost_ico", "ver", icon=str(tmp_path / "nope.ico"))
    assert calls == []
    assert "companion_lnk" not in row
