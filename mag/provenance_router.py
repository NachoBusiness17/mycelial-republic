"""provenance_router — ground the routing decision in verkle/provenance truth, not labels.

The operator (2026-08-16): the early "frontier" calls were really DeepSeek (frontier-pennies,
frontier-scout, grok_hub all `provider=deepseek` under frontier tags). So we had NO grounded context
for when to route — the history was contaminated. The fix: route on verkle-anchored provenance, never
labels or memory.

This is the "deterministic lens to feed to deepseek": the deterministic (verkle/provenance) layer
shapes the routing decision BEFORE any model is called.

Reuses (self-steal, no new core):
  * model_pick.recommend_model  -> intent (flash vs pro)
  * frontier_rib.seat_status    -> is a REAL frontier seat live? (honest: says not_dispatched if not)
  * frontier_council.route_type -> is this frontier-type work (code-planning/frontier-research)?
  * trust_gate.SOURCE_TRUST     -> provenance trust scoring
  * truth_audit.provenance_audit -> grounded history of real frontier calls (verkle)

THE LAW (never fake frontier):
  route to frontier ONLY when (a) work is frontier-type AND (b) a real frontier seat is live AND
  (c) verkle-anchored frontier provenance exists (real calls landed). Otherwise flash/pro with the
  TRUE provider. Never label a DeepSeek result 'frontier'.

Schema: provenance_router.v1 · deterministic $0
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "provenance_router.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _frontier_provenance() -> dict[str, Any]:
    """Grounded history: has a REAL frontier call landed (verkle-anchored)? Reads truth_audit."""
    try:
        from mag import truth_audit
        a = truth_audit.provenance_audit()
        if isinstance(a, dict):
            real = (a.get("real_frontier") or a.get("frontier_real") or
                    a.get("n_frontier_real") or 0)
            return {"real_frontier_calls": int(real) if isinstance(real, (int, float)) else 0,
                    "audit": a}
    except Exception:
        pass
    return {"real_frontier_calls": 0, "audit": {}}


def _seat_status_fast() -> dict[str, Any]:
    """NON-BLOCKING seat check. Does NOT call browser_driver.connect() (it can hang — the blocking-
    command trap). Only fast, REAL signals count as a live seat: the grok CLI harness (the proven
    authenticated transport) availability. Honest: no browser connect, no claiming live without a real signal."""
    grok = False
    try:
        from harness.grok_cli import harness_available  # type: ignore
        grok = bool(harness_available())
    except Exception:
        pass
    return {"ok": True, "schema": SCHEMA, "ts": _now(),
            "any_seat_live": grok,
            "grok_harness": grok,
            "honest": "fast non-blocking check (no browser_driver.connect, avoids hang); a real "
                       "seat is only counted live on the grok CLI harness availability, not config"}


def route(goal: str = "", *, force_frontier: bool = False) -> dict[str, Any]:
    """THE GROUNDED ROUTING DECISION (the deterministic lens). flash/pro/frontier by truth."""
    # 1. intent -> flash vs pro (model_pick)
    intent: dict[str, Any] = {}
    try:
        from mag import model_pick
        intent = model_pick.recommend_model(goal or "")
    except Exception:
        intent = {"model": "deepseek-v4-flash", "shape": "balanced"}
    # 2. is a REAL frontier seat live? (fast, non-blocking)
    seat = _seat_status_fast()
    live = bool(seat.get("any_seat_live"))
    # 3. is this frontier-type work?
    wtype = "data"
    try:
        from mag import frontier_council
        wtype = frontier_council.route_type(goal or "").get("type", "data")
    except Exception:
        pass
    needs_frontier = (wtype == "frontier") or bool(force_frontier)
    # 4. verkle-anchored frontier provenance (real calls landed?)
    prov = _frontier_provenance()
    real_calls = int(prov.get("real_frontier_calls", 0) or 0)
    # THE LAW: frontier only if frontier-type + real seat live + real provenance
    if needs_frontier and live and real_calls > 0:
        return {"ok": True, "schema": SCHEMA, "ts": _now(), "goal": (goal or "")[:160],
                "tier": "frontier", "provider": "frontier (real seat)",
                "provenance": "frontier_model_output",
                "seat_live": live, "real_frontier_calls": real_calls,
                "intent_model": intent.get("model"),
                "rule": "frontier ONLY on a real live seat + grounded verkle provenance; never fake",
                "grounded": "real frontier seat live AND verkle frontier provenance present"}
    # else flash/pro with the TRUE provider
    model = intent.get("model", "deepseek-v4-flash")
    return {"ok": True, "schema": SCHEMA, "ts": _now(), "goal": (goal or "")[:160],
            "tier": "pro" if model == "deepseek-v4-pro" else "flash",
            "provider": "deepseek", "model": model,
            "provenance": "deepseek",
            "seat_live": live, "needs_frontier": needs_frontier,
            "real_frontier_calls": real_calls,
            "rule": "route to deepseek (flash/pro) — real frontier not grounded/live; never label "
                    "a DeepSeek result 'frontier'",
            "why": (("frontier-type work, but " if needs_frontier else "not frontier-type work; ") +
                    ("no real frontier seat live" if not live else "no verkle frontier provenance"))}


def status() -> dict[str, Any]:
    seat = _seat_status_fast()
    prov = _frontier_provenance()
    return {"ok": True, "schema": SCHEMA,
            "contract": ("route(goal)->flash/pro/frontier grounded in verkle/provenance truth, not "
                         "labels. Frontier only if frontier-type + real seat live + real provenance "
                         "(frontier_rib/truth_audit). Deterministic lens fed to deepseek. $0. "
                         "Fast non-blocking seat check (no browser hang)."),
            "seat_live": bool(seat.get("any_seat_live")),
            "real_frontier_calls": prov.get("real_frontier_calls", 0),
            "trust_sources": "operator=1.0 frontier/grok=0.8 swarm=0.6 unknown=0.3 (trust_gate)"}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="provenance_router")
    p.add_argument("cmd", choices=["route", "status"])
    p.add_argument("goal", nargs="*", default=[])
    a = p.parse_args(argv)
    if a.cmd == "route":
        print(json.dumps(route(" ".join(a.goal)), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
