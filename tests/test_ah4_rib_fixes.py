"""AH4 (audit finding #15, 2026-09-30) — rib fixes.

Three laws pinned here:
  1. The rib's LANGUAGE line ("this model's native tongue is Chinese") rides only
     Chinese-native targets (z.ai GLM family / z_ai lanes); the default omits it
     for everyone else, and rib_chat picks per its own model/lane.
  2. grok_warm_rib's standing knot id + verkle root are DERIVED from
     memory/biography/verkle_tip.json at call time — never hardcoded stale ids,
     and they track a moved tip.
  3. scripts/warm_rib.py (moved from mag/_warm_rib.py) makes no metered call and
     no file write at import; its paths derive from the repo root.

Receipt: watch/inbox/last_mile_20260930/AH4_RIB_FIXES.md
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from mag import grok_warm_rib, rib_cache
from mag.rib_cache import FROZEN_RIB, _DOCTRINE_CORE, frozen_rib, is_chinese_native

REPO_ROOT = Path(__file__).resolve().parent.parent
_LINE = "native tongue is Chinese"
_RETIRED_KNOT = "710745b79a0a149d"
_RETIRED_ROOT = "caec3c98c7625bda"


# ── 1. language-line conditionality ────────────────────────────────────────────

def test_chinese_native_detection():
    assert is_chinese_native(model="glm-4.5-flash")
    assert is_chinese_native(model="GLM-5.3")
    assert is_chinese_native(model="glm-4.7-flash", lane="z_ai3")
    assert is_chinese_native(lane="z_ai3")  # a z.ai lane is the provider signal itself
    assert is_chinese_native(lane="z_ai")
    assert not is_chinese_native()  # nothing known -> the AH4 default omits the line
    assert not is_chinese_native(model="grok-4")
    assert not is_chinese_native(model="deepseek-chat", lane="deepseek")
    assert not is_chinese_native(model="llama-3.3-70b", lane="openrouter")


def test_language_line_rides_chinese_native_targets_only():
    assert _LINE in frozen_rib(model="glm-4.5-flash")
    assert frozen_rib(model="glm-4.5-flash", lane="z_ai3") == FROZEN_RIB  # bytes pinned
    assert _LINE not in frozen_rib()  # AH4 default: omit for non-Chinese-native
    assert _LINE not in frozen_rib(model="grok-4")
    assert frozen_rib(model="grok-4") == _DOCTRINE_CORE
    # explicit override both ways
    assert _LINE in frozen_rib(model="grok-4", chinese_native=True)
    assert _LINE not in frozen_rib(model="glm-4.5-flash", chinese_native=False)
    # byte-stability per target: same target -> same bytes (cache mining survives)
    assert frozen_rib(model="grok-4") == frozen_rib(model="grok-4")


class _FakeHold:
    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _capture_system(monkeypatch):
    seen = {}

    def fake_provider(lane, system, user, **k):
        seen["system"] = system
        seen["lane"] = lane
        return {"ok": True, "text": "ok", "usage": {}}

    import mag.concurrency_gate as cg
    import mag.lite_guard as lg
    import models.providers as mp
    monkeypatch.setattr(cg, "hold", lambda *a, **k: _FakeHold())
    monkeypatch.setattr(mp, "chat_provider", fake_provider)
    monkeypatch.setattr(lg, "check", lambda door: {"ok": True})
    monkeypatch.setattr(lg, "record", lambda *a, **k: None)
    return seen


def test_rib_chat_sends_language_line_per_target(monkeypatch):
    seen = _capture_system(monkeypatch)
    r = rib_cache.rib_chat("t", lane="z_ai3", model="glm-4.5-flash")
    assert r["ok"], r.get("error")
    assert seen["system"] == FROZEN_RIB  # Chinese-native: the line rides, bytes unchanged
    r = rib_cache.rib_chat("t", lane="grok", model="grok-4")
    assert r["ok"], r.get("error")
    assert seen["system"] == _DOCTRINE_CORE  # non-native: the line is omitted


# ── 2. tip-derived knot id ─────────────────────────────────────────────────────

def test_warm_rib_text_derives_knot_and_root_from_tip(monkeypatch, tmp_path):
    bio = tmp_path / "memory" / "biography"
    bio.mkdir(parents=True)
    (bio / "verkle_tip.json").write_text(json.dumps(
        {"schema": "verkle_tip.v1", "root": "c" * 64,
         "last_leaf_hash": "a" * 64, "n_leaves": 3}), encoding="utf-8")
    monkeypatch.setattr(grok_warm_rib, "ROOT", tmp_path)
    text = grok_warm_rib.warm_rib_text()
    assert "a" * 16 in text  # knot id = last_leaf_hash[:16]
    assert "c" * 16 in text  # root = root[:16]
    assert _RETIRED_KNOT not in text
    assert _RETIRED_ROOT not in text


def test_warm_rib_text_tracks_tip_moves(monkeypatch, tmp_path):
    bio = tmp_path / "memory" / "biography"
    bio.mkdir(parents=True)
    tip = bio / "verkle_tip.json"
    tip.write_text(json.dumps({"root": "1" * 64, "last_leaf_hash": "2" * 64}),
                   encoding="utf-8")
    monkeypatch.setattr(grok_warm_rib, "ROOT", tmp_path)
    assert "2" * 16 in grok_warm_rib.warm_rib_text()
    tip.write_text(json.dumps({"root": "3" * 64, "last_leaf_hash": "4" * 64}),
                   encoding="utf-8")
    text = grok_warm_rib.warm_rib_text()
    assert "4" * 16 in text and "3" * 16 in text
    assert "2" * 16 not in text  # stale ids do not survive a tip move


def test_warm_rib_text_quotes_no_stale_ids_when_tip_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(grok_warm_rib, "ROOT", tmp_path)  # no tip file at all
    text = grok_warm_rib.warm_rib_text()
    assert _RETIRED_KNOT not in text and _RETIRED_ROOT not in text
    assert "tip unavailable" in text


def test_warm_rib_text_live_tip_matches_the_file():
    p = grok_warm_rib.ROOT / "memory" / "biography" / "verkle_tip.json"
    tip = json.loads(p.read_text(encoding="utf-8"))
    text = grok_warm_rib.warm_rib_text()
    assert tip["last_leaf_hash"][:16] in text
    assert tip["root"][:16] in text


# ── 3. the moved script is import-safe ─────────────────────────────────────────

def test_warm_rib_script_moved_and_import_safe(monkeypatch):
    assert not (REPO_ROOT / "mag" / "_warm_rib.py").exists()
    src = REPO_ROOT / "scripts" / "warm_rib.py"
    assert src.is_file()
    rib_md = REPO_ROOT / "queue" / "handoff" / "zcode" / "RIB.md"

    def _no_metered_call(*a, **k):
        raise AssertionError("metered call at import time")

    monkeypatch.setattr(rib_cache, "rib_chat", _no_metered_call)
    before = (rib_md.is_file(), rib_md.stat().st_mtime_ns if rib_md.is_file() else None)
    spec = importlib.util.spec_from_file_location("warm_rib_script_ah4", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # top level must be side-effect free
    after = (rib_md.is_file(), rib_md.stat().st_mtime_ns if rib_md.is_file() else None)
    assert before == after  # nothing written on import
    assert mod.ROOT == REPO_ROOT  # paths derive from the repo root, no hardcode
    assert callable(mod.main)
