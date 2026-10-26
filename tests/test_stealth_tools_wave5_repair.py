"""wave5-repair stealth-tools lane: the three owed fixes, pinned by tests.

1. NTFS ADS defect: slugs at the fanout and driver write sites must strip
   every NTFS-unsafe char (the 'ling-3.0-flash-sante:free' colon put lane
   answers into ':free.md' alternate data streams on 0-byte base files;
   stealth-sw-15 finding 1, flash50, 2026-09-29).
2. Hermes resolution: _dispatch_hermes must gate off LOUDLY when no Hermes
   python resolves, and must name the wedged cua-driver pipe when that
   known failure signature returns (selffeed burned 19+ cycles on an
   unnamed 'rc=1 The system cannot find the file specified.').
3. Single instance: a second driver instance (win32 named mutex / posix
   flock) must refuse to start. And mirrors.json writes only on change.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FANOUT_PATH = ROOT / "tools" / "stealth_fanout.py"
DRIVER_PATH = ROOT / "tools" / "stealth_driver.py"


def _load(name: str, path: Path):
    """Load a tools/ module as a fresh module (tools/ is not importable as
    a cheap package: tools/__init__ drags the whole toolbelt in)."""
    if name in sys.modules:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


COLON_MODEL = "inclusionai/ling-3.0-flash-sante:free"

SLUG_CASES = [
    (COLON_MODEL, "inclusionai_ling-3.0-flash-sante_free"),
    ("stealth/space-bunny-alpha", "stealth_space-bunny-alpha"),
    ('a*b?c"d<e>f|g', "a_b_c_d_e_f_g"),
    ("", "unnamed"),
    ("  .  ", "unnamed"),
]


def test_slug_identical_in_both_tools_and_ntfs_safe():
    fan = _load("stealth_fanout", FANOUT_PATH)
    drv = _load("stealth_driver", DRIVER_PATH)
    for text, expected in SLUG_CASES:
        assert fan.slug(text) == expected, (text, fan.slug(text))
        assert drv.slug(text) == expected, (text, drv.slug(text))
    for text, _ in SLUG_CASES:
        for fn in (fan.slug(text), drv.slug(text)):
            assert not (set(fn) & set(fan.NTFS_UNSAFE)), fn
            assert all(ord(c) >= 32 for c in fn), fn


def test_fanout_write_site_roundtrip_base_file_not_ads(tmp_path, monkeypatch):
    """The finish-line shape: a lane answer round-trips a colon-containing
    slug and is readable back from the BASE file, not an ADS."""
    fan = _load("stealth_fanout", FANOUT_PATH)
    monkeypatch.setattr(fan, "OUT_DIR", tmp_path)
    monkeypatch.setattr(fan, "HEARTBEAT", tmp_path / "hb.jsonl")
    monkeypatch.setattr(fan, "LANES", [{"base":
        "https://api.llm7.io/v1/chat/completions", "key": "",
        "model": COLON_MODEL}])
    monkeypatch.setattr(fan, "dispatch", lambda lane, ask, max_tokens=3000:
                        ("ANSWER BODY for ADS probe", {}))
    row = fan.run_item(0, "probe-ads", "ask text")
    assert row["ok"] is True
    written = list(tmp_path.glob("fan_probe-ads_*.md"))
    assert len(written) == 1, list(tmp_path.iterdir())
    base = written[0]
    # 1. no NTFS-unsafe char survives into the filename
    assert not (set(base.name) & set(fan.NTFS_UNSAFE)), base.name
    assert base.name == "fan_probe-ads_inclusionai_ling-3.0-flash-sante_free.md"
    # 2. the base file carries the content (old code: 0 bytes here, all of
    #    it in the ':free.md' stream)
    text = base.read_text(encoding="utf-8")
    assert "ANSWER BODY for ADS probe" in text
    assert f"lane model: {COLON_MODEL}" in text
    # 3. and no stray ADS-bearing name exists on disk (win32 forbids ':'
    #    in directory listings; the slug guarantees it structurally)
    assert ":" not in base.name
    heartbeat_rows = (tmp_path / "hb.jsonl").read_text(
        encoding="utf-8").strip().splitlines()
    assert json.loads(heartbeat_rows[-1])["model"] == COLON_MODEL


def test_driver_work_out_name_sanitizes_selffeed_ids():
    drv = _load("stealth_driver", DRIVER_PATH)
    # selffeed ids come from Hermes output; a colon id must not reach NTFS
    name = drv._work_out_name("m1:free", "hermes")
    assert name == "m1_free_hermes.md"
    assert not (set(name) & set(drv.NTFS_UNSAFE))
    assert drv._work_out_name("w-quant-compare", "openrouter3") == \
        "w-quant-compare_openrouter3.md"


def test_dispatch_hermes_gates_off_loudly_when_unresolvable(
        tmp_path, monkeypatch):
    drv = _load("stealth_driver", DRIVER_PATH)
    monkeypatch.delenv("HERMES_PYTHON", raising=False)
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))  # empty fake home
    got = drv._dispatch_hermes("any ask")
    assert got[0] is False
    assert got[1].startswith("GATE-OFF hermes:"), got
    assert "dispatch not burned" in got[1]


def test_hermes_failure_cause_names_wedged_pipe_and_empty():
    drv = _load("stealth_driver", DRIVER_PATH)
    observed = "The system cannot find the file specified.\n"
    cause = drv._hermes_failure_cause(1, "", observed)
    assert "cua-driver" in cause and "pipe" in cause and cause.startswith("rc=1")
    cause0 = drv._hermes_failure_cause(0, "", "")
    assert "EMPTY stdout" in cause0
    assert drv._hermes_failure_cause(7, "boom", "").startswith("rc=7")


def test_instance_lock_refuses_second_acquire():
    drv = _load("stealth_driver", DRIVER_PATH)
    # ball3 driver-meter 2026-09-29: the LIVE driver holds the production
    # mutex (Local\MagStealthDriverInstance), so the old no-namespace test
    # was refused on its FIRST acquire. The test now acquires in its own
    # pid-unique namespace; the strictness under test (a SECOND acquire of
    # the same lock refuses) is unchanged, and production keeps the shared
    # lock because the driver never passes a namespace.
    ns = f"ball3.{os.getpid()}"
    drv.acquire_instance_lock(namespace=ns)
    try:
        with pytest.raises(drv.InstanceLocked):
            drv.acquire_instance_lock(namespace=ns)
    finally:
        drv.release_instance_lock()
    # after release a fresh acquire succeeds again, then clean up
    drv.acquire_instance_lock(namespace=ns)
    drv.release_instance_lock()


def test_mirrors_write_only_on_change(tmp_path, monkeypatch):
    drv = _load("stealth_driver", DRIVER_PATH)
    mirrors = tmp_path / "mirrors.json"
    monkeypatch.setattr(drv, "MIRRORS", mirrors)
    catalog = {"llm7": {"models": 64, "prev_models": 64, "churn": False}}
    assert drv._write_mirrors_if_changed(catalog, "llm7 64 stable") is True
    first_ts = json.loads(mirrors.read_text(encoding="utf-8"))["ts"]
    # identical catalog: no write, ts on disk stays the first one
    assert drv._write_mirrors_if_changed(catalog, "llm7 64 stable") is False
    assert json.loads(mirrors.read_text(encoding="utf-8"))["ts"] == first_ts
    # changed catalog: written again
    catalog2 = {"llm7": {"models": 65, "prev_models": 64, "churn": True}}
    assert drv._write_mirrors_if_changed(catalog2, "llm7 64 CHURN") is True
    assert json.loads(mirrors.read_text(encoding="utf-8"))["hosts"] == catalog2


def test_selffeed_loud_gate_after_consecutive_failures(
        tmp_path, monkeypatch):
    drv = _load("stealth_driver", DRIVER_PATH)
    inbox = tmp_path / "watch" / "inbox"
    inbox.mkdir(parents=True)
    mined = inbox / "STEALTH_MINED_FINDINGS.jsonl"
    mined.write_text(
        json.dumps({"ts": "t", "work_id": "w1", "lane": "llm7",
                    "model": "gpt-4o-mini", "finish": "stop"}) + "\n",
        encoding="utf-8")
    work_state = tmp_path / "work_state.json"
    work_queue = tmp_path / "work_queue.jsonl"
    monkeypatch.setattr(drv, "ROOT", tmp_path)
    monkeypatch.setattr(drv, "WORK_STATE", work_state)
    monkeypatch.setattr(drv, "WORK_QUEUE", work_queue)
    # v2 rail 1 (2026-09-29): selffeed fires only when t_work sensed a new
    # item this tick; arm the trigger so the breaker contract below is
    # what this test exercises.
    drv._TICK["work_sensed_new"] = True
    calls = {"n": 0}

    def fake_dispatch_fail(ask):
        calls["n"] += 1
        return False, "rc=1 The system cannot find the file specified."

    monkeypatch.setattr(drv, "_dispatch_hermes", fake_dispatch_fail)
    results = [drv.t_selffeed() for _ in range(5)]
    # first SELFFEED_GATE_AFTER calls dispatch and fail loudly
    for r in results[:drv.SELFFEED_GATE_AFTER]:
        assert r.startswith("ERR selffeed: rc=1"), r
    assert calls["n"] == drv.SELFFEED_GATE_AFTER
    # then the loud gate: no dispatch burn, named cause, re-probe countdown
    for r in results[drv.SELFFEED_GATE_AFTER:]:
        assert r.startswith("GATE-OFF selffeed:"), r
    assert calls["n"] == drv.SELFFEED_GATE_AFTER
    assert "cannot find the file specified" in results[-1]
    # re-probe: REPROBE_CYCLES=0 means the gated window is always exhausted,
    # so the next call dispatches once more (rail 1 is bypassed for a
    # breaker re-probe); success resets the streak
    def fake_dispatch_ok(ask):
        calls["n"] += 1
        return True, json.dumps({"id": "m9",
                                 "ask": "Go deeper on the ADS recovery.",
                                 "tier": "free"})
    monkeypatch.setattr(drv, "_dispatch_hermes", fake_dispatch_ok)
    monkeypatch.setattr(drv, "SELFFEED_REPROBE_CYCLES", 0, raising=False)
    result = drv.t_selffeed()
    # v2 rail 4: the hermes-proposed id is ignored; ids are m%03d
    assert result.startswith("selffed m001:"), result
    assert calls["n"] == drv.SELFFEED_GATE_AFTER + 1
    rows = [json.loads(l) for l in
            work_queue.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert rows[-1]["id"] == "m001" and rows[-1]["status"] == "queued"
    # v2 rail 7: the appended row carries the bounded-loop schema
    assert rows[-1]["depth"] == 1 and rows[-1]["parent_id"] == "w1"
    assert rows[-1]["queued_ts"]
    final_state = json.loads(work_state.read_text(encoding="utf-8"))
    assert final_state["selffeed_fail_streak"] == 0
    # v2 rail 1 (spacing): the healthy next call is capped at one fire per
    # hour, so it skips WITHOUT a dispatch (v1 burned one every 300s tick)
    assert drv.t_selffeed().startswith("skip: selffeed rail 1 (spacing):")
    assert calls["n"] == drv.SELFFEED_GATE_AFTER + 1
