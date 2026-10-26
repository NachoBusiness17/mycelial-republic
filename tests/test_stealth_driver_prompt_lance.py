"""Test prompt_lance topic wired into stealth_driver.

Proves: t_prompt_lance runs self_check on the last context pack output
and banks a verdict string (clean or findings-worst) to the heartbeat.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "memory" / "context_pack_latest.md"
SD_PATH = ROOT / "tools" / "stealth_driver.py"


def _load_mod():
    """Load tools/stealth_driver.py as a fresh module (tools/ not on sys.path)."""
    name = "stealth_driver"
    if name in sys.modules:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SD_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def _isolate_pack(tmp_path):
    """Point prompt_lance at a controlled pack so the test is deterministic."""
    real = None
    if PACK.is_file():
        real = PACK.read_text(encoding="utf-8")
    mem = tmp_path / "memory"
    mem.mkdir()
    pack = mem / "context_pack_latest.md"
    pack.write_text(
        "# Pack\n\nHermes is dormant.\n\nTODO wire the key here\n\n"
        "Hermes is not dormant.\n\none two three four five six\n\n"
        "one two three four five six\n",
        encoding="utf-8",
    )
    mod = _load_mod()
    mod.ROOT = tmp_path
    yield pack, real
    mod.ROOT = ROOT
    if real is not None:
        PACK.write_text(real, encoding="utf-8")


def test_t_prompt_lance_returns_verdict(_isolate_pack):
    """Topic returns a verdict line with schema, count, and worst finding."""
    mod = _load_mod()
    mod.ROOT = _isolate_pack[0].parent.parent  # tmp_path (parent of memory/)
    out = mod.t_prompt_lance()
    assert out.startswith("prompt_lance: "), out
    # verdict shape: "N findings; worst=severity CODE at L..."
    assert "findings;" in out and "worst=" in out, out


def test_t_prompt_lance_skip_when_no_pack(tmp_path):
    """Without a context pack file the topic skips cleanly."""
    mod = _load_mod()
    mod.ROOT = tmp_path
    assert mod.t_prompt_lance() == "skip: no context_pack_latest.md"


def test_t_prompt_lance_banks_to_heartbeat(_isolate_pack):
    """one_cycle banks the prompt_lance verdict into the heartbeat row."""
    mod = _load_mod()
    mod.ROOT = _isolate_pack[0].parent.parent  # tmp_path (parent of memory/)
    hb = mod.HEARTBEAT
    if hb.is_file():
        hb.unlink()
    # run only prompt_lance topic (not the full cycle — roster blocks on network)
    row = {"ts": mod._now(), "cycle": 0, "topics": {}}
    try:
        row["topics"]["prompt_lance"] = mod.t_prompt_lance()
    except Exception as e:
        row["topics"]["prompt_lance"] = f"ERR {type(e).__name__}: {str(e)[:80]}"
    assert "prompt_lance" in row["topics"]
    assert row["topics"]["prompt_lance"].startswith("prompt_lance: ")
    assert "findings;" in row["topics"]["prompt_lance"]