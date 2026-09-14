"""llm_k8s_lang — the LANGUAGE between k8s/k3s and LLMs (2026-08-15, operator).

Operator: "maybe the language between k8s and llms somehow... build it and steal do the thing."

The bridge between the DETERMINISTIC cluster and the STOCHASTIC model:
  LLM speaks COORDINATES (Mag's BPE / RIB-STEER) -> the bridge translates them into
  DETERMINISTIC k8s/k3s operations (k8s_bridge) -> the cluster responds in coordinates
  the LLM can read (the X-ray of the cluster, keyed on our atoms).

SELF-STEAL (nothing new built from scratch — the pieces exist):
  rib_bus.inject_for / steer_engine.compile_steer = Mag's BPE (the atom/steer layer, seats get
                                                     coordinates not raw text)
  k8s_bridge (cronjobs/jobs)                       = the k8s surface (windowless, system-native)
  router.classify_depth                           = the intent -> operation classifier

THE LANGUAGE (three verbs):
  speak()     — the LLM's side: compile a task's STEER COORDINATE (the atom the LLM operates under).
  translate() — map an LLM ask -> a deterministic k8s/k3s OPERATION (status/cronjobs/reconcile/
                scale/deploy), via the router.
  listen()    — the return path: read cluster state and emit COORDINATES the LLM can read (the
                cluster X-ray). HONEST: never fabricates cluster state.
  bridge()    — the full cycle: speak -> translate -> listen, as one grab-write.

Schema: llm_k8s_lang.v1 · deterministic + $0 · honest (cluster state read, never invented)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCHEMA = "llm_k8s_lang.v1"


def speak(ask: str, *, domain: str = "general") -> dict[str, Any]:
    """The LLM's side: compile the task's STEER COORDINATE (Mag's BPE atom). Seats receive
    coordinates, not raw text. Deterministic + $0."""
    try:
        from mag import rib_bus
        steer = rib_bus.inject_for(ask, domain=domain)
    except Exception as e:
        steer = f"(steer unavailable: {str(e)[:80]})"
    return {"ok": True, "schema": SCHEMA, "domain": domain,
            "steer_coordinate": steer,
            "note": "the LLM's atom layer (Mag's BPE): coordinates, not raw text"}


def translate(ask: str) -> dict[str, Any]:
    """THE TRANSLATION: map an LLM ask -> a deterministic k8s/k3s OPERATION, via the router.
    Honest: reports the operation; does NOT execute destructive ops unless the ask clearly asks."""
    try:
        from mag.router import classify_depth
        d = classify_depth(ask)
        depth = str(d.get("depth") or "scut")
    except Exception:
        depth = "scut"
    g = (ask or "").lower()
    if any(w in g for w in ("reconcil", "sync", "conform", "check", "converge")):
        op = "reconcile"
    elif any(w in g for w in ("cronjob", "job", "workload", "schedule", "swarm")):
        op = "cronjobs"
    elif any(w in g for w in ("scale", "rightsize", "size", "capacity")):
        op = "scale"
    elif any(w in g for w in ("deploy", "apply", "ship", "launch")):
        op = "deploy"
    else:
        op = "status"
    return {"ok": True, "schema": SCHEMA, "intent_depth": depth, "operation": op,
            "note": "LLM ask -> deterministic k8s operation"}


def listen() -> dict[str, Any]:
    """THE RETURN PATH: read cluster state and emit COORDINATES the LLM can read (the cluster
    X-ray). HONEST: if k8s is unreachable, report it — NEVER fabricate cluster state."""
    try:
        from mag import k8s_bridge as kb
        cj = kb.cronjobs()
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:120],
                "note": "cluster unreachable — no fabricated state"}
    return {"ok": bool(cj.get("ok")), "schema": SCHEMA, "code": cj.get("code"),
            "cronjobs": str(cj.get("stdout") or "")[:1500],
            "note": "cluster X-ray — k8s state as coordinates for the LLM to read"}


def bridge(ask: str, *, domain: str = "general") -> dict[str, Any]:
    """The full language cycle (grab-write): speak a coordinate -> translate to a k8s op -> read
    state back. One move, not three hand-steps."""
    s = speak(ask, domain=domain)
    t = translate(ask)
    l = listen()
    return {"ok": True, "schema": SCHEMA, "speak": {"coordinate": s.get("steer_coordinate", "")[:140]},
            "translate": {"operation": t.get("operation"), "depth": t.get("intent_depth")},
            "listen": {"ok": l.get("ok"), "cluster": l.get("note")},
            "note": "the language between k8s and LLMs: coordinates in, coordinates out"}


if __name__ == "__main__":
    import json as _json
    import argparse as _ap
    p = _ap.ArgumentParser(prog="llm_k8s_lang", description="the language between k8s/k3s and LLMs")
    p.add_argument("ask", nargs="*", default=["status of the swarm cronjobs"])
    a = p.parse_args()
    print(_json.dumps(bridge(" ".join(a.ask)), indent=2, ensure_ascii=False, default=str))
