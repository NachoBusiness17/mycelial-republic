"""FW-46 silent-pass batch 2 (2026-09-28): the three sites fixed this batch name
their failure on stderr instead of swallowing it.

Sites (each formerly `except Exception: pass`):
  - mag/afk_loop.py        module-load stdout reconfigure
  - mag/act.py             _toast_optional attention flag write
  - mag/agent_cli.py       _load_mag_yaml corrupt configs/mag.yaml

Law: best-effort stands, the reason is named (batch-1 pattern,
tools/audio_channel.py:31; STEAL_WAVE_FOLD_20260911 "silent loss masquerading
as health"). These tests pin that the named-failure stays named.
"""
from __future__ import annotations

import importlib
import io
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_afk_loop_reconfigure_failure_is_named(capsys, monkeypatch):
    """A stdout whose reconfigure raises must not silently pass: the reason
    lands on stderr and the module still finishes importing."""
    class BadStdout:
        def reconfigure(self, **kwargs):
            raise OSError("fake console has no reconfigure")

    monkeypatch.setattr(sys, "stdout", BadStdout())
    import mag.afk_loop as afk_loop

    importlib.reload(afk_loop)
    err = capsys.readouterr().err
    assert "[afk_loop] stdout reconfigure skipped:" in err
    assert "fake console has no reconfigure" in err
    # the module body still loaded (socratic table present)
    assert isinstance(afk_loop._SOCRATIC, list) and afk_loop._SOCRATIC


def test_act_toast_failure_names_the_flag_write(capsys, monkeypatch, tmp_path):
    """When the attention flag write fails, _toast_optional stays best-effort
    (returns None) but the failure is named on stderr."""
    import mag.act as act

    # make ROOT/"watch"/"attention_flag.txt" unwritable: "watch" is a FILE,
    # so the path under it is not a directory -> write_text raises
    (tmp_path / "watch").write_text("not a dir", encoding="utf-8")
    monkeypatch.setattr(act, "ROOT", tmp_path)
    ret = act._toast_optional("t", "m")
    assert ret is None
    err = capsys.readouterr().err
    assert "[act] toast/attention-flag write failed:" in err


def test_act_toast_success_stays_quiet(capsys, monkeypatch, tmp_path):
    """The happy path writes the flag and prints nothing (no warning creep)."""
    import mag.act as act

    (tmp_path / "watch").mkdir()
    monkeypatch.setattr(act, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "platform", "win32")
    ret = act._toast_optional("t", "m")
    assert ret is None
    flag = tmp_path / "watch" / "attention_flag.txt"
    assert flag.read_text(encoding="utf-8") == "t\nm\n"
    assert capsys.readouterr().err == ""


def test_load_mag_yaml_corrupt_config_is_named(capsys, monkeypatch, tmp_path):
    """A corrupt configs/mag.yaml still yields {} (defaults stand) but names
    the parse failure on stderr; a good config parses silently."""
    import mag.agent_cli as agent_cli

    cfg_dir = tmp_path / "configs"
    cfg_dir.mkdir()
    (cfg_dir / "mag.yaml").write_text("]:[ not: yaml: [[{", encoding="utf-8")
    monkeypatch.setattr(agent_cli, "ROOT", tmp_path)
    assert agent_cli._load_mag_yaml() == {}
    err = capsys.readouterr().err
    assert "[agent_cli] configs/mag.yaml unreadable, using defaults:" in err

    (cfg_dir / "mag.yaml").write_text("context_repack_ratio: 0.7\n", encoding="utf-8")
    assert agent_cli._load_mag_yaml() == {"context_repack_ratio": 0.7}
    assert capsys.readouterr().err == ""
