"""rib_launcher — an INVARIANT RIB LAUNCHER, for fun (and truth-as-hardy-spore).

Operator (2026-08-13): "an invariant rib launcher for fun!"

A RIB is a spore — a true invariant we seed into a domain. The launcher FIRES it: publish an invariant
into a breeding ground (rib_bus domain), and let it do what spores do — persist, and spread. Fun on the
surface, standing-wave underneath: launching a RIB is planting truth where it can germinate.

REUSE (self-steal, all real): mag.rib_bus.publish_rib (the real publish mechanism — deterministic + $0),
memory/rib_bus/*.json domains (the breeding grounds), standing_wave.wave_packets (the spores we hold).

Schema: rib_launcher.v1 · deterministic + $0 (rib_bus publish) · optional route_novel seam (propagate to swarm)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "rib_launcher.v1"

# the breeding grounds (rib_bus domains) where a spore can land
KNOWN_DOMAINS = ["general", "swarm", "research", "self-shape", "good-work", "recovery",
                 "toolkit", "mirror", "standing-wave"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def launch(invariant: str, *, domain: str = "general", target_rank: str = "T2",
           source: str = "rib-launcher", propagate: bool = False) -> dict[str, Any]:
    """FIRE a spore: publish an invariant RIB into a breeding ground via rib_bus.publish_rib.
    Deterministic + $0. Optionally propagate to the swarm (route_novel) so the spore travels.
    HONEST — only a real invariant lands; publish_rib dedupes by content hash."""
    invariant = (invariant or "").strip()
    if not invariant:
        return {"ok": False, "schema": SCHEMA, "error": "empty invariant (nothing to fire)"}
    if domain not in KNOWN_DOMAINS:
        return {"ok": False, "schema": SCHEMA, "error": f"unknown domain: {domain}",
                "known": KNOWN_DOMAINS}
    try:
        from mag import rib_bus
        r = rib_bus.publish_rib(invariant, domain=domain, source=source,
                                target_rank=target_rank, fold=False, publish=False)
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": f"publish failed: {str(e)[:120]}"}
    out: dict[str, Any] = {
        "ok": True, "schema": SCHEMA, "tool": "rib_launcher", "fired": True,
        "spore": {"invariant": invariant[:200], "domain": domain,
                  "target_rank": str(target_rank or "T2").upper()},
        "landed": r.get("n_total"), "added": r.get("added"), "key": r.get("key"),
        "flavor": _flavor(domain),
    }
    if propagate:
        try:
            from mag import swarm_surface
            routed = swarm_surface.route_novel(goal=invariant, surface="rib-launcher",
                                               lens=f"rib:{domain}")
            out["propagated"] = {"ok": routed.get("ok"),
                                 "task_id": routed.get("task_id") or routed.get("enqueued")}
        except Exception as e:
            out["propagate_error"] = str(e)[:80]
    return out


def salvo(invariants: list[str], *, domain: str = "general", target_rank: str = "T2",
          propagate: bool = False) -> dict[str, Any]:
    """FIRE A SALVO: launch several spores at once into a domain. Deterministic + $0."""
    invs = [s.strip() for s in (invariants or []) if (s or "").strip()]
    if not invs:
        return {"ok": False, "schema": SCHEMA, "error": "no spores to fire"}
    results = [launch(s, domain=domain, target_rank=target_rank, propagate=propagate)
               for s in invs]
    landed = sum(1 for r in results if r.get("ok"))
    return {"ok": True, "schema": SCHEMA, "tool": "rib_launcher", "fired": len(results),
            "landed": landed, "domain": domain, "results": results,
            "flavor": f"a salvo of {len(results)} spores, {landed} germinating in '{domain}'"}


def launchpad() -> dict[str, Any]:
    """The launchpad — the breeding grounds where a spore can land, with current RIB counts.
    Deterministic + $0."""
    from mag import rib_bus
    pad = {}
    for d in KNOWN_DOMAINS:
        try:
            m = rib_bus.mount(d)
            pad[d] = len(m.get("ribs") or [])
        except Exception:
            pad[d] = -1
    return {"ok": True, "schema": SCHEMA, "tool": "rib_launcher", "domains": pad,
            "flavor": "choose a breeding ground and FIRE a spore"}


def _flavor(domain: str) -> str:
    flavors = {
        "general": "a seed in open soil",
        "swarm": "a spore into the swarm's mycelium",
        "research": "a spore into the frontier's field",
        "self-shape": "a knot examined — fired into the mirror",
        "good-work": "a mark of work well done, launched",
        "recovery": "a lesson from a fireball, re-fired as a lens",
        "toolkit": "a tool's essence, launched to the toolbelt",
        "mirror": "a mirror persona seeded into the edge",
        "standing-wave": "a wave-packet fired into the medium",
    }
    return flavors.get(domain, "a spore into the breeding ground")


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="rib-launcher")
    ap.add_argument("cmd", nargs="?", default="launchpad",
                    choices=["launchpad", "launch", "salvo"])
    ap.add_argument("args", nargs="*", default=[])
    ap.add_argument("--domain", default="general")
    ap.add_argument("--rank", default="T2")
    ap.add_argument("--propagate", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "launchpad":
        print(json.dumps(launchpad(), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "launch":
        print(json.dumps(launch(" ".join(a.args) or "a true invariant", domain=a.domain,
                                target_rank=a.rank, propagate=a.propagate),
                         ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "salvo":
        print(json.dumps(salvo(a.args or ["a true invariant"], domain=a.domain,
                               target_rank=a.rank, propagate=a.propagate),
                         ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
