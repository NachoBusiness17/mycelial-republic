"""Tests for mag.rib_cache.freeze_rib (AH17, audit SS2.2 gap close, 2026-09-30).

AGENTS.md "Deliberate-ask" says the frozen RIB = system+bootloader+manifest+verkle
tip; the legacy FROZEN_RIB constant carried only doctrine text. freeze_rib() must
compose all four: doctrine (minus the AH4-conditionalized LANGUAGE line), manifest
sha, verkle tip root/n_leaves, timestamp, plus the AGENTS.md formula reference —
cached to memory/runs/frozen_rib_cache.json keyed by (manifest_sha, tip_root) so a
moved tip recomposes automatically and repeated calls in one process are free.

Laws pinned here: FROZEN_RIB bytes never move (sha256 pinned; the compat constant
keeps the LANGUAGE line), fail-closed when there is nothing to bind, cache layers
miss -> memory -> disk, tip change = new key = recompose.

Receipt: watch/inbox/last_mile_20260930/AH17_FROZEN_RIB.md
"""
from __future__ import annotations

import hashlib
import json
import re

import pytest

from mag import rib_cache as rc

# Byte-stability guard: the legacy constant is a cache-mined prefix; if these bytes
# move, every caller riding the cache loses the mine. Pinned at AH17 landing.
_FROZEN_RIB_SHA256 = "7ca50bdccea3731f748d95166cdd6947c2e48f53e413429dbf3d000adfec01d2"
_FROZEN_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


@pytest.fixture()
def frozen_env(tmp_path, monkeypatch):
    """Isolated binding surface: tmp anchor + tip + cache, seed manifest absent
    (forces the anchor path), in-process memo emptied per test."""
    anchor = tmp_path / "manifest_anchor.json"
    anchor.write_text(json.dumps(
        {"schema": "manifest.v1", "manifest_hash": "a" * 64}), encoding="utf-8")
    tip = tmp_path / "verkle_tip.json"
    tip.write_text(json.dumps(
        {"schema": "verkle_tip.v1", "root": "b" * 64, "n_leaves": 12}),
        encoding="utf-8")
    cache = tmp_path / "frozen_rib_cache.json"
    monkeypatch.setattr(rc, "ANCHOR_PATH", anchor)
    monkeypatch.setattr(rc, "SEED_MANIFEST_PATH", tmp_path / "no_seed_manifest")
    monkeypatch.setattr(rc, "VERKLE_TIP_PATH", tip)
    monkeypatch.setattr(rc, "RIB_FREEZE_CACHE_PATH", cache)
    monkeypatch.setattr(rc, "_FREEZE_MEMO", {})
    return {"anchor": anchor, "tip": tip, "cache": cache, "tmp": tmp_path}


# ── composition: all four formula parts present, AH4 line dropped ──────────────

def test_freeze_rib_contains_all_four_parts(frozen_env):
    r = rc.freeze_rib()
    assert r["ok"], r.get("error")
    rib = r["rib"]
    # (1) system+bootloader: the doctrine text (BRIEF + TRI-STATE + rightsized law)
    assert rib.startswith(rc._DOCTRINE_CORE)
    assert rc._BRIEF in rib
    assert "STANDING DOCTRINE" in rib and "TRI-STATE" in rib
    assert "THE RIGHTSIZE LAW" in rib
    # (2) manifest sha + its source
    assert "a" * 64 in rib
    assert "manifest_anchor.json#manifest_hash" in rib
    # (3) verkle tip root + n_leaves
    assert "b" * 64 in rib
    assert "12" in rib.split("verkle_tip_leaves:")[1].split("\n")[0]
    # (4) timestamp + the AGENTS.md formula reference
    assert _FROZEN_AT_RE.match(r["frozen_at"])
    assert "frozen_at: " + r["frozen_at"] in rib
    assert "AGENTS.md" in rib and "system+bootloader+manifest+verkle tip" in rib


def test_freeze_rib_drops_the_ah4_conditionalized_language_line(frozen_env):
    r = rc.freeze_rib()
    assert r["ok"]
    # "this model's native tongue is Chinese" is one model family's property, not
    # fleet law — the composed rib must not carry it (callers pass language in the tail).
    assert "LANGUAGE:" not in r["rib"]
    assert "native tongue" not in r["rib"]


def test_freeze_rib_doctrine_is_the_legacy_core_minus_language(frozen_env):
    r = rc.freeze_rib()
    assert r["rib"].startswith(rc._DOCTRINE_CORE)
    assert rc._DOCTRINE_CORE + "\n\nFROZEN RIB BINDING BLOCK" in r["rib"]


# ── legacy compat: FROZEN_RIB bytes never move ─────────────────────────────────

def test_frozen_rib_bytes_are_pinned():
    assert hashlib.sha256(rc.FROZEN_RIB.encode()).hexdigest() == _FROZEN_RIB_SHA256


def test_frozen_rib_is_core_plus_language_line():
    assert rc.FROZEN_RIB == rc._DOCTRINE_CORE + rc._LANGUAGE_LINE
    # the legacy constant KEEPS the language line (compat: byte-identity is the law)
    assert "LANGUAGE: answer in English" in rc.FROZEN_RIB


# ── cache: miss -> memory -> disk; key = (manifest_sha, tip_root) ──────────────

def test_cache_miss_then_memory_hit_same_process(frozen_env):
    first = rc.freeze_rib()
    second = rc.freeze_rib()
    assert first["cache"] == "miss"
    assert second["cache"] == "memory"
    assert first["rib"] == second["rib"] and first["frozen_at"] == second["frozen_at"]
    # miss wrote the disk cache entry
    disk = json.loads(frozen_env["cache"].read_text(encoding="utf-8"))
    assert first["cache_key"] in disk["entries"]


def test_disk_cache_hit_in_a_fresh_process(frozen_env, monkeypatch):
    first = rc.freeze_rib()
    monkeypatch.setattr(rc, "_FREEZE_MEMO", {})  # simulate a new process
    again = rc.freeze_rib()
    assert again["cache"] == "disk"
    assert again["rib"] == first["rib"]
    assert again["frozen_at"] == first["frozen_at"]  # the original freeze time


def test_corrupt_disk_cache_recomposes_honestly(frozen_env):
    rc.freeze_rib()
    frozen_env["cache"].write_text("{not json", encoding="utf-8")
    rc._FREEZE_MEMO.clear()
    r = rc.freeze_rib()
    assert r["cache"] == "miss" and r["ok"]
    disk = json.loads(frozen_env["cache"].read_text(encoding="utf-8"))
    assert r["cache_key"] in disk["entries"]


# ── honest invalidation: tip change = new key = recompose ──────────────────────

def test_tip_change_recomposes_and_keeps_old_entry(frozen_env):
    old = rc.freeze_rib()
    tip = {"schema": "verkle_tip.v1", "root": "c" * 64, "n_leaves": 13}
    frozen_env["tip"].write_text(json.dumps(tip), encoding="utf-8")
    new = rc.freeze_rib()
    assert new["cache"] == "miss"  # new tip_root -> new cache key -> recompose
    assert "c" * 64 in new["rib"] and "c" * 64 == new["tip_root"]
    assert new["n_leaves"] == 13
    assert new["frozen_at"] >= old["frozen_at"]
    assert old["tip_root"] != new["tip_root"]
    # the old binding survives on disk as history, not served as current
    disk = json.loads(frozen_env["cache"].read_text(encoding="utf-8"))
    assert old["cache_key"] in disk["entries"] and new["cache_key"] in disk["entries"]


# ── manifest sources: anchor wins, seed falls back, explicit path overrides ─────

def test_manifest_seed_fallback_when_anchor_absent(frozen_env, monkeypatch):
    seed = frozen_env["tmp"] / "MANIFEST.sha256"
    seed.write_text("d8049696  ACCOUNTS.md\n", encoding="utf-8")
    monkeypatch.setattr(rc, "ANCHOR_PATH", frozen_env["tmp"] / "no_anchor.json")
    monkeypatch.setattr(rc, "SEED_MANIFEST_PATH", seed)
    r = rc.freeze_rib()
    assert r["ok"]
    assert r["manifest_sha"] == hashlib.sha256(seed.read_bytes()).hexdigest()
    assert "seed/MANIFEST.sha256" in r["manifest_source"] or "MANIFEST.sha256" in r["manifest_source"]
    assert r["manifest_sha"] in r["rib"]


def test_manifest_explicit_path_overrides_defaults(frozen_env):
    m = frozen_env["tmp"] / "custom_manifest.json"
    m.write_text(json.dumps({"manifest_hash": "e" * 64}), encoding="utf-8")
    r = rc.freeze_rib(manifest_path=m)
    assert r["ok"] and r["manifest_sha"] == "e" * 64
    assert str(m) in r["manifest_source"] and "e" * 64 in r["rib"]


def test_manifest_explicit_json_without_field_hashes_bytes(frozen_env):
    m = frozen_env["tmp"] / "plain.json"
    m.write_text('{"note": "no manifest_hash here"}', encoding="utf-8")
    r = rc.freeze_rib(manifest_path=m)
    assert r["ok"]
    assert r["manifest_sha"] == hashlib.sha256(m.read_bytes()).hexdigest()


# ── fail closed: nothing to bind -> no rib, named error ────────────────────────

def test_no_manifest_fails_closed(frozen_env, monkeypatch):
    monkeypatch.setattr(rc, "ANCHOR_PATH", frozen_env["tmp"] / "nope.json")
    monkeypatch.setattr(rc, "SEED_MANIFEST_PATH", frozen_env["tmp"] / "nope2")
    r = rc.freeze_rib()
    assert not r["ok"] and "no manifest to bind" in r["error"]


def test_no_tip_fails_closed(frozen_env, monkeypatch):
    monkeypatch.setattr(rc, "VERKLE_TIP_PATH", frozen_env["tmp"] / "no_tip.json")
    r = rc.freeze_rib()
    assert not r["ok"] and "verkle tip" in r["error"]


def test_missing_manifest_path_arg_fails_closed(frozen_env):
    r = rc.freeze_rib(manifest_path=frozen_env["tmp"] / "ghost.json")
    assert not r["ok"] and "not found" in r["error"]
