#!/usr/bin/env python3
"""comic_renderer: the deterministic drawing hand for the comics lane.

Composes, does not invent: the pose vocabulary and the stick-figure
geometry are ported from the estate's existing drawing engine
(dashboard/static/mag_dance.html:52 POSES, :81 drawSkeleton), the bare-metal
SVG pattern from mag/game_entry.py:154 (zero-dep, deterministic, string
built), and the PNG twin uses PIL ImageDraw because the venv has no SVG
rasterizer (cairosvg/svglib/resvg absent, synthesis fold check) while
Discord's upload whitelist is raster-only. ONE geometry pass emits neutral
drawing primitives; two backends consume them: SVG canonical (dashboard +
archive deliverable) and PIL PNG (raster surfaces). Same spec, same
numbers, same layout in both.

The model never touches pixels: it emits pose names + captions through
tools/comic_spec.py (the frozen schema), this module draws what the
enum promises. Deterministic: same spec bytes -> identical SVG string and
identical PNG pixels. $0, stateless, no env reads.

CLI: .venv/Scripts/python.exe -m tools.comic_renderer --spec s.json \
        --svg out.svg --png out.png
No em-dashes in this file (citation-lint law).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from tools import comic_spec
from tools.comic_spec import CAST, POSES, SCHEMA_NAME, SpecError, check

# LAYOUT (px): one row of N panels, action band top, caption band bottom.
MARGIN, GAP = 14, 16
PANEL_W, PANEL_H = 320, 300
TITLE_H, FOOT_H = 34, 22
ACTION_H, CAPTION_H = 30, 62
ACTION_WRAP, CAPTION_WRAP = 44, 34

# PALETTE: dark register to match the dashboard surfaces (mag_dance bg).
BG, PANEL_BG, BORDER = "#0b0b10", "#12121c", "#2a2a40"
TEXT, SUBTLE = "#d8d8e8", "#7a7a99"
CAST_COLOR = {
    "operator": "#dfe6ff",
    "mag": "#b8a8ff",
    "hermes": "#ffd49a",
    "lilith-figure": "#ff9ad4",
    "gemma-janitor": "#9affc0",
    "generic-agent": "#9ad4ff",
}
if set(CAST_COLOR) != set(CAST):  # the twin engines share the frozen cast
    raise RuntimeError("CAST_COLOR out of sync with comic_spec.CAST")

# drawSkeleton port constants (mag_dance.html): segment lengths + hips.
HIP_Y, TORSO_L, HEAD_R, NECK_L = -70.0, 70.0, 14.0, 26.0
SH_DY, UPPER_ARM, FOREARM, THIGH, SHIN = 6.0, 38.0, 34.0, 44.0, 42.0


def wrap_text(s: str, limit: int) -> list[str]:
    """Greedy word wrap, shared by both backends so the twins agree."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > limit:
            lines.append(cur)
            cur = w
        else:
            cur = w if not cur else cur + " " + w
    if cur:
        lines.append(cur)
    return lines or [""]


def _joints(pose: str) -> list[tuple[float, float]]:
    """All skeleton joint points in native hip-origin coords (for bbox fit)."""
    r = [math.radians(v) for v in POSES[pose]]
    pts = [(0.0, HIP_Y)]
    neck_x = math.sin(r[0]) * TORSO_L
    neck_y = HIP_Y - math.cos(r[0]) * TORSO_L
    pts.append((neck_x, neck_y))
    hx = neck_x + math.sin(r[1]) * NECK_L
    hy = neck_y - math.cos(r[1]) * NECK_L
    pts.append((hx, hy))
    sh_x, sh_y = neck_x, neck_y + SH_DY
    for side in (-1, 1):
        sh = r[2] if side < 0 else r[4]
        el = r[3] if side < 0 else r[5]
        f = -side
        ex = sh_x + math.sin(sh) * UPPER_ARM * f
        ey = sh_y + math.cos(sh) * UPPER_ARM
        wx = ex + math.sin(sh + el) * FOREARM * f
        wy = ey + math.cos(sh + el) * FOREARM
        pts.extend([(ex, ey), (wx, wy)])
    for side in (-1, 1):
        hip = r[6] if side < 0 else r[8]
        knee = r[7] if side < 0 else r[9]
        f = side
        kx = math.sin(hip) * THIGH * f
        ky = HIP_Y + math.cos(hip) * THIGH
        fx = kx + math.sin(hip + knee) * SHIN * f
        fy = ky + math.cos(hip + knee) * SHIN
        pts.extend([(kx, ky), (fx, fy)])
    return pts


_BBOX: dict[str, tuple[float, float, float, float]] = {}


def pose_bbox(pose: str) -> tuple[float, float, float, float]:
    """Native (minx, miny, maxx, maxy) of a posed figure, head radius and
    stroke margin included, cached. The fit law: every figure lands inside
    its slot with feet on the ground line, whatever the pose does."""
    if pose not in _BBOX:
        pts = _joints(pose)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        pad = HEAD_R + 4.0
        _BBOX[pose] = (min(xs) - pad, min(ys) - pad,
                       max(xs) + pad, max(ys) + pad)
    return _BBOX[pose]


def figure_prims(pose: str, ox: float, oy: float, scale: float,
                 color: str) -> list[tuple]:
    """One stick figure as primitives. Local origin (ox, oy) is the hip;
    geometry ported 1:1 from mag_dance.html drawSkeleton (static, no
    jitter/lerp: a comic panel is a held pose, not a dance frame)."""
    r = [math.radians(v) for v in POSES[pose]]
    prims: list[tuple] = []

    def line(x1, y1, x2, y2, w):
        prims.append(("line", ox + x1 * scale, oy + y1 * scale,
                      ox + x2 * scale, oy + y2 * scale, color, w))

    neck_x = math.sin(r[0]) * TORSO_L
    neck_y = HIP_Y - math.cos(r[0]) * TORSO_L
    line(0, HIP_Y, neck_x, neck_y, 7)                       # torso
    hx = neck_x + math.sin(r[1]) * NECK_L
    hy = neck_y - math.cos(r[1]) * NECK_L
    line(neck_x, neck_y, neck_x + (hx - neck_x) * 0.4,
         neck_y + (hy - neck_y) * 0.4, 5)                   # neck stub
    sh_x, sh_y = neck_x, neck_y + SH_DY
    for side in (-1, 1):                                    # arms (JS: f=-side)
        sh = r[2] if side < 0 else r[4]
        el = r[3] if side < 0 else r[5]
        f = -side
        ex = sh_x + math.sin(sh) * UPPER_ARM * f
        ey = sh_y + math.cos(sh) * UPPER_ARM
        wx = ex + math.sin(sh + el) * FOREARM * f
        wy = ey + math.cos(sh + el) * FOREARM
        line(sh_x, sh_y, ex, ey, 5)
        line(ex, ey, wx, wy, 5)
    for side in (-1, 1):                                    # legs (JS: f=side)
        hip = r[6] if side < 0 else r[8]
        knee = r[7] if side < 0 else r[9]
        f = side
        kx = math.sin(hip) * THIGH * f
        ky = HIP_Y + math.cos(hip) * THIGH
        fx = kx + math.sin(hip + knee) * SHIN * f
        fy = ky + math.cos(hip + knee) * SHIN
        line(0, HIP_Y, kx, ky, 5)
        line(kx, ky, fx, fy, 5)
    # head LAST: poses like spirit swing upper arms across the head zone,
    # and the head must stay legible when the arms cross it (draw order).
    prims.append(("circle", ox + hx * scale, oy + hy * scale,
                  HEAD_R * scale, color))
    return prims


def build_strip(spec: dict) -> tuple[int, int, list[tuple]]:
    """Validate loudly, then compose the whole strip as primitives."""
    check(spec)
    panels = spec["panels"]
    n = len(panels)
    w = MARGIN * 2 + n * PANEL_W + (n - 1) * GAP
    h = MARGIN + TITLE_H + PANEL_H + FOOT_H + MARGIN
    prims: list[tuple] = [("rect", 0, 0, w, h, BG, BG, 0)]
    prims.append(("text", w / 2, MARGIN + 18, spec["title"], TEXT, 16, "middle"))
    top = MARGIN + TITLE_H
    ground = PANEL_H - CAPTION_H - 20
    for i, p in enumerate(panels):
        px = MARGIN + i * (PANEL_W + GAP)
        prims.append(("rect", px, top, PANEL_W, PANEL_H, PANEL_BG, BORDER, 6))
        for j, ln in enumerate(wrap_text(p["action"], ACTION_WRAP)[:2]):
            prims.append(("text", px + 10, top + 16 + j * 13, ln, SUBTLE, 10,
                          "start"))
        prims.append(("line", px + 14, top + ground + 2, px + PANEL_W - 14,
                      top + ground + 2, BORDER, 2))          # the ground line
        who = p["who"]
        slot_w = PANEL_W / len(who)
        bb = pose_bbox(p["pose"])                 # one pose per panel by schema
        scale = min(0.95, (slot_w - 26.0) / (bb[2] - bb[0]),
                    (ground - ACTION_H - 22.0) / (bb[3] - bb[1]))
        for k, name in enumerate(who):
            cx = px + slot_w * (k + 0.5)
            ox = cx - (bb[0] + bb[2]) / 2 * scale             # centered
            oy = top + ground - bb[3] * scale                 # feet grounded
            prims.extend(figure_prims(p["pose"], ox, oy, scale,
                                      CAST_COLOR[name]))
            half = len(name) * 3.0                            # label clamp
            lx = min(max(cx, px + half + 8), px + PANEL_W - half - 8)
            prims.append(("text", lx, top + ground + 14, name,
                          CAST_COLOR[name], 9, "middle"))
        for j, ln in enumerate(wrap_text(p["caption"], CAPTION_WRAP)[:4]):
            prims.append(("text", px + PANEL_W / 2,
                          top + PANEL_H - CAPTION_H + 16 + j * 13, ln, TEXT, 12,
                          "middle"))
    prims.append(("text", MARGIN, h - 8,
                  f"{SCHEMA_NAME} · {n} panels · deterministic render", SUBTLE,
                  9, "start"))
    return w, h, prims


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def render_svg(spec: dict) -> str:
    """SVG canonical (the deliverable format): zero-dep string building."""
    w, h, prims = build_strip(spec)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">']
    for pr in prims:
        if pr[0] == "rect":
            _, x, y, rw, rh, fill, stroke, rx = pr
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{rw}" '
                       f'height="{rh}" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="1" rx="{rx}"/>')
        elif pr[0] == "line":
            _, x1, y1, x2, y2, color, lw = pr
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
                       f'y2="{y2:.1f}" stroke="{color}" stroke-width="{lw}" '
                       f'stroke-linecap="round"/>')
        elif pr[0] == "circle":
            _, cx, cy, r, color = pr
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                       f'fill="{color}"/>')
        elif pr[0] == "text":
            _, x, y, s, color, size, anchor = pr
            a = "middle" if anchor == "middle" else "start"
            out.append(f'<text x="{x:.1f}" y="{y:.1f}" '
                       f'font-family="monospace" font-size="{size}" '
                       f'fill="{color}" text-anchor="{a}">{_esc(s)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def _rgb(hexcolor: str) -> tuple[int, int, int]:
    return (int(hexcolor[1:3], 16), int(hexcolor[3:5], 16), int(hexcolor[5:7], 16))


def _font(size: int):
    from PIL import ImageFont
    try:
        return ImageFont.load_default(size=size)
    except TypeError:                       # old Pillow: unsized bitmap font
        return ImageFont.load_default()


def render_png(spec: dict):
    """PIL ImageDraw twin for raster-only surfaces (Discord whitelist)."""
    from PIL import Image, ImageDraw
    w, h, prims = build_strip(spec)
    img = Image.new("RGB", (w, h), _rgb(BG))
    d = ImageDraw.Draw(img)
    fonts = {}
    for pr in prims:
        if pr[0] == "rect":
            _, x, y, rw, rh, fill, stroke, rx = pr
            d.rectangle([x, y, x + rw, y + rh], fill=_rgb(fill),
                        outline=_rgb(stroke), width=1)
        elif pr[0] == "line":
            _, x1, y1, x2, y2, color, lw = pr
            d.line([x1, y1, x2, y2], fill=_rgb(color), width=int(lw))
        elif pr[0] == "circle":
            _, cx, cy, r, color = pr
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_rgb(color))
        elif pr[0] == "text":
            _, x, y, s, color, size, anchor = pr
            f = fonts.setdefault(size, _font(size))
            if anchor == "middle":
                d.text((x - d.textlength(s, font=f) / 2, y - size), s,
                       font=f, fill=_rgb(color))
            else:
                d.text((x, y - size), s, font=f, fill=_rgb(color))
    return img


def save(spec: dict, svg_path: Path, png_path: Path) -> dict:
    """Bank both twins. One call, one receipt dict."""
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg = render_svg(spec)
    svg_path.write_text(svg, encoding="utf-8")
    img = render_png(spec)
    img.save(png_path, format="PNG")
    return {"svg": str(svg_path), "svg_bytes": len(svg.encode("utf-8")),
            "png": str(png_path), "png_size": img.size,
            "spec_chars": len(comic_spec.serialize(spec)),
            "spec_tokens": comic_spec.estimate_tokens(
                comic_spec.serialize(spec))}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="render a comic_spec.v2 panel spec to SVG + PNG twins")
    ap.add_argument("--spec", required=True, help="path to the spec JSON")
    ap.add_argument("--svg", help="output SVG (default: beside the spec)")
    ap.add_argument("--png", help="output PNG (default: beside the spec)")
    ap.add_argument("--budget", action="store_true",
                    help="print the schema budget proof and exit")
    args = ap.parse_args(argv)
    if args.budget:
        print(json.dumps(comic_spec.BUDGET_PROOF, indent=1))
        return 0
    spec_path = Path(args.spec)
    try:
        spec = comic_spec.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, SpecError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2
    svg_path = Path(args.svg) if args.svg else spec_path.with_suffix(".svg")
    png_path = Path(args.png) if args.png else spec_path.with_suffix(".png")
    receipt = save(spec, svg_path, png_path)
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
