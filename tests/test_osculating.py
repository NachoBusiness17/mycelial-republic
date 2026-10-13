"""tests for osculating — the MISSING geometry of the wave (self-steal moonshot). Deterministic + $0.

RIB (frozen spec):
  geometry() -> per-point osculating circle of the standing-wave RIB trajectory: tangent (lean),
      curvature kappa, radius R, CENTER of curvature, + the EVOLUTE (locus of centers). ok:True with
      >=3 RIB points; per-node k_norm normalized so the sharpest bend = 1.0.
  seams(top) -> the sharpest bends (highest k_norm) = the coldest seams to shade, mapped back to RIBs.
  moonshot() -> geometry + route the sharpest-seam insight to the swarm via route_novel (never fatal).
  svg()      -> bare-metal SVG string containing the curve + evolute markers.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import osculating  # noqa: E402


def test_geometry_ok_and_missing_pieces_present():
    g = osculating.geometry()
    if not g.get("ok"):
        # need >=3 RIBs to fit a curve — if the wave has fewer, honest error, not a crash
        assert "error" in g and g.get("n_points", 0) < 3
        return
    assert g["ok"] is True
    assert g["n_nodes"] >= 1
    n = g["nodes"][0]
    # the MISSING geometry is now present: curvature, radius, center of curvature, tangent
    assert "kappa" in n and "radius" in n and "center" in n and "tangent" in n
    assert "evolute" in g                          # the locus of centers
    # normalized curvature: sharpest bend -> 1.0, all others in [0,1]
    assert all(0.0 <= n["k_norm"] <= 1.0 for n in g["nodes"])
    assert any(n["k_norm"] == 1.0 for n in g["nodes"])


def test_seams_returns_sharpest_bends():
    g = osculating.geometry()
    if not g.get("ok"):
        return
    s = osculating.seams(top=3)
    assert s["ok"] is True
    assert len(s["seams"]) <= 3
    for se in s["seams"]:
        assert se["key"] and "k_norm" in se and "center" in se and "radius" in se
    # seams are sorted by sharpness descending
    ks = [se["k_norm"] for se in s["seams"]]
    assert ks == sorted(ks, reverse=True)


def test_moonshot_routes_novel_never_fatal():
    g = osculating.geometry()
    if not g.get("ok"):
        return
    mo = osculating.moonshot(route=True, top=2)
    assert mo["ok"] is True
    assert "geometry" in mo and "seams" in mo and "routed" in mo
    r = mo["routed"]
    assert r.get("ok") in (True, False)
    assert any(k in r for k in ("task_id", "deduped", "error"))


def test_svg_bare_metal():
    g = osculating.geometry()
    if not g.get("ok"):
        return
    s = osculating.svg()
    assert s.startswith("<svg") and s.endswith("</svg>")
    assert "EVOLUTE" in s or "evolute" in s.lower()


def test_status_marks_missing_now_built():
    st = osculating.status()
    assert st["ok"] is True
    assert st["schema"] == "osculating.v1"
    # the pieces that SHOULD be here but weren't are now named as built
    for piece in ("curvature", "radius", "center of curvature", "evolute"):
        assert piece in st["missing_now_built"]
