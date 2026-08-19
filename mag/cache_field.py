"""cache_field — the SDF-over-the-stochastic-map adapter (deep steal, 2026-08-16).

Maps our invariants/stable-prefixes to determine WHICH parts of the stochastic (latent) map we
land in — stochastic/deterministic navigation + mining of the frontier. Grounded in the hybrid
voxel+SDF-in-octree robotics pattern (shaped-swarm, Voxblox), adapted to model latent space:

  * COORDINATE space   = theme/region index from cache_map.build_map() (by_theme buckets).
  * SIGNED DISTANCE    = cache hit/miss per region: hit = inside/known (cache-warm), miss =
                        outside/novel (frontier). The SDF over the stochastic map.
  * GRADIENT / STEER   = toward cache-warm (cheap re-entry) OR deliberately into the miss
                        (mine the frontier) — a mode flag.
  * MINING FLYWHEEL    = each frontier expedition freezes the new invariant -> cache-warm ->
                        field updates -> next navigation knows the boundary (Voxblox ESDF).

Reuses (self-steal, no new core): cache_map (hit/miss = the signed distance), flock_field
(PhiField gradient steering), invariant (stable prefix), lens_chain (lens direction).
Deterministic $0.

Schema: cache_field.v1 · CLI: python -m mag.cache_field map | distance <region> |
        steer --mode warm|frontier | status
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "cache_field.v1"


def _coord(theme: str) -> tuple[float, float, float]:
    """Deterministic coordinate for a theme (content-addressed -> point in field space)."""
    h = hashlib.sha256((theme or "?").encode("utf-8")).hexdigest()

    def u(i: int) -> float:
        return (int(h[i:i + 4], 16) % 1000) / 100.0 - 5.0  # -5..5

    return (u(0), u(4), u(8))


def _zone(hr: Any, split_rows: int) -> str:
    """Honest zone: unknown = no split recorded (unmeasured, NOT cold); warm = measured >=0.5;
    cold = measured <0.5 (the real mine). Fix (2026-08-16): split_rows==0 must be 'unknown', not
    'frontier' — a 0.0 hit_ratio with no split data means unmeasured, not cache-cold."""
    if split_rows <= 0 or hr is None:
        return "unknown"
    return "warm" if float(hr) >= 0.5 else "cold"


def map_() -> dict[str, Any]:
    """THE STOCHASTIC MAP: every theme/region, its coordinate, and its cache signed-distance."""
    try:
        from mag import cache_map
        cm = cache_map.build_map()
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:200]}
    themes = cm.get("by_theme") or []
    regions = []
    for t in themes:
        theme = t.get("theme") or "?"
        hr = t.get("split_hit_ratio")
        split_rows = int(t.get("split_rows") or 0)
        regions.append({
            "region": theme,
            "coord": _coord(theme),
            "hit_ratio": round(float(hr), 4) if hr is not None else None,
            "split_rows": split_rows,
            "zone": _zone(hr, split_rows),
            "input_tokens": int(t.get("input_tokens") or 0),
            "calls": int(t.get("calls") or 0),
        })
    # measured first (warmest -> coldest), unknown last
    regions.sort(key=lambda r: (r["zone"] == "unknown", - (r["hit_ratio"] or 0)))
    return {"ok": True, "schema": SCHEMA, "n_regions": len(regions), "regions": regions}


def signed_distance(region: str) -> dict[str, Any]:
    """Distance-to-known-boundary for one region (Voxblox ESDF analogy): warm = inside,
    cold = outside; unknown = unmeasured (no cache split), needs instrumentation, not a mine yet."""
    m = map_()
    if not m.get("ok"):
        return m
    hit = next((r for r in m["regions"] if r["region"] == region), None)
    if not hit:
        return {"ok": True, "schema": SCHEMA, "region": region, "known": False,
                "zone": "unknown", "signed_distance": None,
                "note": "region not on the cache map -> unmeasured"}
    if hit["zone"] == "unknown":
        return {"ok": True, "schema": SCHEMA, "region": region, "known": False,
                "coord": hit["coord"], "split_rows": hit["split_rows"],
                "zone": "unknown", "signed_distance": None,
                "note": "no cache split recorded -> unmeasured, NOT confirmed cold; instrument to measure"}
    sd = round(0.5 - hit["hit_ratio"], 4)  # <0 = warm/inside, >0 = cold/outside
    return {"ok": True, "schema": SCHEMA, "region": region, "known": True,
            "coord": hit["coord"], "hit_ratio": hit["hit_ratio"], "zone": hit["zone"],
            "signed_distance": sd,
            "nearest_known_boundary": round(hit["hit_ratio"], 4)}


def steer(mode: str = "warm") -> dict[str, Any]:
    """GRADIENT of the stochastic map: where the swarm should go.
    mode='warm'     -> toward the most cache-warm MEASURED region (cheap re-entry).
    mode='frontier' -> into the coldest MEASURED region (split data shows real cold = the mine).
    Unknown (unmeasured) regions are NOT targets until they record a cache split."""
    m = map_()
    if not m.get("ok"):
        return m
    if not m["regions"]:
        return {"ok": True, "schema": SCHEMA, "n_regions": 0, "target": None}
    measured = [r for r in m["regions"] if r["zone"] in ("warm", "cold")]
    if mode == "frontier":
        target = min(measured, key=lambda r: r["hit_ratio"]) if measured else None
    else:
        target = max(measured, key=lambda r: r["hit_ratio"]) if measured else None
    if not target:
        return {"ok": True, "schema": SCHEMA, "mode": mode, "target": None,
                "n_measured": 0, "note": "no MEASURED region to steer to; all unknown/unmeasured"}
    return {"ok": True, "schema": SCHEMA, "mode": mode, "target": target,
            "target_zone": target["zone"], "target_hit_ratio": target["hit_ratio"],
            "target_split_rows": target["split_rows"],
            "gradient": ("toward cache-warm (cheap re-entry)" if target["zone"] == "warm"
                          else "into measured cold frontier (the mine)")}


def status() -> dict[str, Any]:
    m = map_()
    regions = m.get("regions", []) if m.get("ok") else []
    warm = sum(1 for r in regions if r["zone"] == "warm")
    cold = sum(1 for r in regions if r["zone"] == "cold")
    unknown = sum(1 for r in regions if r["zone"] == "unknown")
    return {"ok": True, "schema": SCHEMA,
            "contract": ("map()->regions+coords+cache signed-distance; signed_distance(r)->warm/"
                         "cold/unknown; steer(warm|frontier)->where the swarm goes (SDF gradient over "
                         "the stochastic map). Reuses cache_map+flock_field+invariant+lens_chain. $0. "
                         "Zones: warm=measured>=0.5, cold=measured<0.5 (the mine), unknown=no split "
                         "recorded (unmeasured, NOT cold)."),
            "n_regions": m.get("n_regions"), "n_warm": warm, "n_cold": cold, "n_unknown": unknown}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cache_field")
    p.add_argument("cmd", choices=["map", "distance", "steer", "status"])
    p.add_argument("arg", nargs="?", default="")
    p.add_argument("--mode", default="warm", choices=["warm", "frontier"])
    a = p.parse_args(argv)
    if a.cmd == "map":
        print(json.dumps(map_(), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "distance":
        print(json.dumps(signed_distance(a.arg), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "steer":
        print(json.dumps(steer(a.mode), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
