"""tests for compute_reconcile — the AUTOMATIC compute-rightsize reconciler. Deterministic + $0.

RIB (frozen spec):
  measure()   -> REAL compute state: gpu (util/vram/free), local_gpu tier (ollama) up?, swarm queue
      undrained count, lifecycle gaps. Always ok:True; honest when a source is missing.
  reconcile() -> the automatic-fix actions + a rightsize verdict. If GPU free + local tier down ->
      "bring-up-local-gpu" (automatable). If swarm queue has undrained tasks -> "revive-swarm-drain"
      (system-imperative, automatabl=False). verdict = misallocated | rightsized.
  run_cadence() -> measure + reconcile + persist. status() -> the contract.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import compute_reconcile as cr  # noqa: E402


def test_measure_ok_and_shape():
    m = cr.measure()
    assert m["ok"] is True
    assert "gpu" in m and "local_gpu_tier" in m and "swarm" in m and "local_loop" in m
    assert "free" in m["gpu"] and "ollama_up" in m["local_gpu_tier"]
    assert "queued" in m["swarm"]


def test_reconcile_always_returns_verdict_and_split():
    r = cr.reconcile()
    assert r["ok"] is True
    assert r["verdict"] in ("misallocated", "rightsized")
    assert "split" in r and "actions" in r
    # every action has a fix + an automatable flag (honest about what the loop can do alone)
    for a in r["actions"]:
        assert a["action"] and a.get("fix") and "automatable" in a


def test_reconcile_detects_idle_gpu_and_brings_it_up():
    # when the GPU is free + the local tier is down, the reconciler must raise the bring-up
    r = cr.reconcile()
    actions = {a["action"] for a in r["actions"]}
    if bool(r["measure"]["gpu"]["free"]) and not r["measure"]["local_gpu_tier"]["ollama_up"]:
        assert "bring-up-local-gpu" in actions


def test_reconcile_surfaces_dead_swarm():
    r = cr.reconcile()
    actions = {a["action"] for a in r["actions"]}
    if int(r["measure"]["swarm"]["queued"]) > 0:
        assert "revive-swarm-drain" in actions
        # the swarm revival is system-imperative -> flagged, never silently auto-run
        for a in r["actions"]:
            if a["action"] == "revive-swarm-drain":
                assert a["automatable"] is False


def test_status_contract_and_reuses():
    st = cr.status()
    assert st["ok"] is True
    assert st["schema"] == "compute_reconcile.v1"
    for dep in ("gpu_lifecycle", "lifecycle", "swarm_worker"):
        assert dep in st["reuses"]
