"""Tests for mag/boot_regen.py (ouroboros R4-L1, 2026-10-05).

The chain law: context-pack fires zknot + hermes_warm_boot + rib_boot as ONE
idempotent chain, stamps component ages, and the verdict turns into exit 2
on age, missing organs, step failure, or the zknot S1 gate. These pins hold
the verdict grammar and the age math without firing real subprocesses.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.boot_regen as br  # noqa: E402


def _iso(days_ago: float) -> str:
    return datetime.fromtimestamp(time.time() - days_ago * 86400,
                                  tz=timezone.utc).isoformat()


def _point_artifacts(tmp_path, monkeypatch, *, ages_d=None, omit=()):
    """Point ARTIFACTS at tmp files with controlled ages; returns the map.

    `omit` names stay in ARTIFACTS but their file is never created (the
    production missing-artifact shape: entry present, file absent).
    """
    ages_d = ages_d if ages_d is not None else {"zknot": 0.0, "warm_boot": 0.0,
                                                "rib_boot": 0.0, "lawpack": 0.0}
    now = time.time()
    paths = {}
    for name, age in ages_d.items():
        p = tmp_path / f"{name}_artifact"
        if name in omit:
            paths[name] = p
            continue
        if name == "lawpack":
            p = tmp_path / "compile_report.json"
            p.write_text(json.dumps({"compiled": _iso(age)}), encoding="utf-8")
        else:
            p.write_text("x", encoding="utf-8")
            os.utime(p, (now - age * 86400, now - age * 86400))
        paths[name] = p
    monkeypatch.setattr(br, "ARTIFACTS", paths)
    return paths


def test_component_ages_reads_lawpack_stamp_not_mtime(tmp_path, monkeypatch):
    paths = _point_artifacts(tmp_path, monkeypatch, ages_d={"lawpack": 3.0})
    ages = br.component_ages()
    assert 2.9 < ages["lawpack"]["age_d"] < 3.1, (
        "the law pack ages by its own compiled stamp, the consumer's logic")


def test_component_ages_missing_and_unreadable(tmp_path, monkeypatch):
    _point_artifacts(tmp_path, monkeypatch, omit=("rib_boot",))
    (tmp_path / "compile_report.json").write_text('{"compiled": "not-a-ts"}',
                                                  encoding="utf-8")
    ages = br.component_ages()
    assert ages["rib_boot"]["exists"] is False
    assert ages["lawpack"]["age_d"] is None, "an unreadable stamp reads as unreadable"


def test_run_boot_regen_ok_with_injected_runner(tmp_path, monkeypatch):
    _point_artifacts(tmp_path, monkeypatch)
    rep = br.run_boot_regen(runner=lambda cmd, t: (0, "fine"))
    assert [n for n, *_ in br.STEPS] == list(rep["steps"].keys()), (
        "the chain fires zknot, warm_boot, rib_boot in order")
    assert all(s["ok"] for s in rep["steps"].values())
    assert rep["verdict"] == "ok"


def test_step_failure_names_the_step(tmp_path, monkeypatch):
    _point_artifacts(tmp_path, monkeypatch)

    def runner(cmd, t):
        return (2, "S1 GATE - 15 qualifying sessions dropped") if "zknot" in cmd[0] else (0, "")

    rep = br.run_boot_regen(runner=runner)
    assert rep["verdict"] == "step-failure"
    assert "zknot" in rep["reason"] and "S1 GATE" in rep["reason"], (
        "a zknot exit 2 (the S1 gate) must surface as the chain's step failure")


def test_age_gate_fires_past_the_one_decay_bar(tmp_path, monkeypatch):
    _point_artifacts(tmp_path, monkeypatch,
                     ages_d={"zknot": 0.0, "warm_boot": 0.0,
                             "rib_boot": 0.0, "lawpack": float(br.PACK_STALE_DAYS) + 0.5})
    rep = br.run_boot_regen(runner=lambda cmd, t: (0, ""))
    assert rep["verdict"] == "age"
    assert "lawpack" in rep["reason"], (
        "a dark daily task ages the law pack and context-pack must exit 2 on it")


def test_missing_artifact_fires_missing_verdict(tmp_path, monkeypatch):
    _point_artifacts(tmp_path, monkeypatch, omit=("warm_boot",))
    rep = br.run_boot_regen(runner=lambda cmd, t: (0, ""))
    assert rep["verdict"] == "missing"
    assert "warm_boot" in rep["reason"]


def test_skip_env_skips_firing_but_not_the_age_gate(tmp_path, monkeypatch):
    _point_artifacts(tmp_path, monkeypatch,
                     ages_d={"zknot": 0.0, "warm_boot": 0.0,
                             "rib_boot": 0.0, "lawpack": 99.0})
    monkeypatch.setenv("MAG_BOOT_REGEN_SKIP", "1")
    rep = br.run_boot_regen(runner=lambda cmd, t: (0, ""))
    assert rep["steps"] == {} and rep["skipped"] is True
    assert rep["verdict"] == "age", (
        "skipping the regen is allowed; serving stale organs is not")
