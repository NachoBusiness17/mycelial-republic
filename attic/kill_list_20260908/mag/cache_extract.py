"""cache_extract — THE ONE JOINT: cache-priming miss -> escalate + extract.

Couples the existing pieces (self-steal, no new architecture):
  * invariant.check()          -> cache priming (prefix stable = cache-warm)
  * cache_field                -> the stochastic map zone (warm / unknown / cold)
  * provenance_router.route()  -> escalation (flash/pro/frontier, grounded in verkle truth)
  * swarm_surface.route_novel  -> THE ONE primitive for extraction (dedupe + enqueue to swarm)

THE LAW (active-learning / uncertainty sampling, the external steal): a cache MISS = high-novelty
= spend (escalate) AND mine (extract). A cache HIT = known = stay cheap, no extraction. So
extraction fires on EVERY novel cache miss automatically — the extraction architecture is
guaranteed everywhere, not incidental.

Non-blocking (never calls browser_driver.connect — avoids the hang). Deterministic $0.

Schema: cache_extract.v1
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "cache_extract.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _toks(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", (text or "").lower()))


def _region(goal: str) -> tuple[str, str, int]:
    """Best-effort: which cache_field region does this goal land in, and its zone?"""
    g = _toks(goal)
    try:
        from mag import cache_field
        m = cache_field.map_()
        best, best_zone, best_ov = "", "unknown", 0
        for r in m.get("regions", []):
            ov = len(g & _toks(r["region"]))
            if ov > best_ov:
                best, best_zone, best_ov = r["region"], r["zone"], ov
        if best_ov >= 2:
            return best, best_zone, best_ov
    except Exception:
        pass
    return "", "unknown", 0


def prime(goal: str = "") -> dict[str, Any]:
    """Cache priming: is this work cache-warm (stable prefix) or novel (a miss)?"""
    stable: bool | None = None
    try:
        from mag import invariant
        c = invariant.check()
        stable = bool(c.get("stable"))
    except Exception:
        pass
    region, zone, overlap = _region(goal)
    # a MISS = prefix not cache-stable OR the region is unmeasured/cold (novel)
    miss = (stable is not True) or (zone in ("unknown", "cold"))
    return {"ok": True, "schema": SCHEMA, "ts": _now(), "goal": (goal or "")[:160],
            "prefix_stable": stable, "region": region or "(none)", "zone": zone,
            "region_overlap": overlap, "miss": miss,
            "prime": "cache-warm (known)" if not miss else "cache-miss (novel)"}


def run(goal: str = "") -> dict[str, Any]:
    """THE JOINT: prime -> on miss, ESCALATE + EXTRACT; on hit, cheap + no extraction."""
    p = prime(goal)
    # escalation (grounded in verkle truth)
    route: dict[str, Any] = {}
    try:
        from mag import provenance_router
        route = provenance_router.route(goal)
    except Exception:
        route = {"tier": "flash", "provider": "deepseek"}
    extraction = False
    extract_ref = ""
    if p["miss"]:
        # extract: route the novel region through THE ONE primitive (dedupe + swarm)
        try:
            from mag import swarm_surface
            q = swarm_surface.route_novel(goal or "mine the novel cache-miss region",
                                          surface="cache-extract")
            extraction = bool(q.get("ok"))
            extract_ref = str(q.get("ref") or q.get("anchor") or "")
        except Exception:
            pass
    return {"ok": True, "schema": SCHEMA, "ts": _now(), "goal": (goal or "")[:160],
            "miss": p["miss"], "zone": p["zone"], "prefix_stable": p["prefix_stable"],
            "escalation_tier": route.get("tier", "flash"),
            "escalation_provider": route.get("provider", "deepseek"),
            "extraction_triggered": extraction,
            "extract_ref": extract_ref,
            "law": ("cache miss = novel = escalate + extract; cache hit = known = cheap, "
                    "no extraction")}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": ("prime(goal)->cache-warm or cache-miss (invariant prefix + cache_field zone); "
                         "run(goal)->on miss escalate (provenance_router) + extract (route_novel); "
                         "on hit stay cheap. Extraction architecture fires on every novel miss. "
                         "Non-blocking $0.")}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cache_extract")
    p.add_argument("cmd", choices=["prime", "run", "status"])
    p.add_argument("goal", nargs="*", default=[])
    a = p.parse_args(argv)
    g = " ".join(a.goal)
    if a.cmd == "prime":
        print(json.dumps(prime(g), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "run":
        print(json.dumps(run(g), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
