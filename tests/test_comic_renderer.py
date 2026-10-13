"""tests for the comics L2 lane: comic_spec (frozen schema, budget by
construction) + comic_renderer (SVG canonical + PIL PNG twin).

Fold: watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/ (SYNTHESIS
moves 2+3). The contract under test: a valid spec renders parseable SVG,
an invalid spec refuses loudly naming every violation, and the worst-case
valid spec serializes under the 1200-char fleet truncation wall and the
300-token ollama output cap. Deterministic + stateless + $0.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import comic_renderer, comic_spec  # noqa: E402

NS = "{http://www.w3.org/2000/svg}"


def good_spec() -> dict:
    return {
        "title": "the night shift",
        "panels": [
            {"who": ["operator"], "pose": "pointy",
             "action": "operator points at the queue",
             "caption": "run five rounds while I sleep"},
            {"who": ["mag", "gemma-janitor"], "pose": "strut",
             "action": "the lanes execute",
             "caption": "12 of 12 lanes done, byte-proven"},
            {"who": ["hermes"], "pose": "think",
             "action": "the paid seat waits",
             "caption": "reserve wall at 0.17 dollars, 402 again"},
            {"who": ["operator", "mag"], "pose": "slump",
             "action": "dawn reading",
             "caption": "verdict on itself: GROWS, not fixpoint"},
        ],
    }


def test_valid_spec_renders_parseable_svg():
    svg = comic_renderer.render_svg(good_spec())
    root = ET.fromstring(svg)                       # XML-parsable or nothing
    assert root.tag == NS + "svg"
    panels = [e for e in root if e.tag == NS + "rect"][1:]
    assert len(panels) == 4                         # one frame per panel
    texts = [t.text or "" for t in root.iter(NS + "text")]
    assert any("run five rounds" in t for t in texts)   # caption landed
    assert any("the night shift" in t for t in texts)   # title landed


def test_three_panel_strip_also_renders():
    spec = good_spec()
    spec["panels"] = spec["panels"][:3]
    svg = comic_renderer.render_svg(spec)
    root = ET.fromstring(svg)
    n = len([e for e in root if e.tag == NS + "rect"]) - 1
    assert n == 3


def test_png_twin_renders_raster():
    img = comic_renderer.render_png(good_spec())
    assert img.size[0] > 0 and img.size[1] > 0
    figcols = {comic_renderer._rgb(c) for c in comic_renderer.CAST_COLOR.values()}
    found = {img.getpixel((x, y)) for y in range(0, img.height, 5)
             for x in range(0, img.width, 5)} & figcols
    assert found                                  # figure ink actually drawn


def test_render_deterministic():
    spec = good_spec()
    assert comic_renderer.render_svg(spec) == comic_renderer.render_svg(spec)
    p1 = comic_renderer.render_png(spec)
    p2 = comic_renderer.render_png(spec)
    assert p1.size == p2.size and p1.tobytes() == p2.tobytes()  # pixel-identical


def test_invalid_spec_refuses_loudly():
    import pytest

    cases = {
        "unknown character": ("who", ["grok"]),
        "unknown pose": ("pose", "moonwalk"),
        "empty caption": ("caption", "   "),
        "over-long caption": ("caption", "c" * (comic_spec.CAPTION_MAX + 1)),
        "over-long action": ("action", "a" * (comic_spec.ACTION_MAX + 1)),
        "over-long title": ("title", "t" * (comic_spec.TITLE_MAX + 1)),
        "too many cast in panel": ("who", ["operator", "mag", "hermes", "lilith-figure"]),
        "duplicate cast member": ("who", ["mag", "mag"]),
    }
    for name, (field, value) in cases.items():
        spec = good_spec()
        if field == "title":
            spec["title"] = value        # title lives at top level, not panel
        else:
            spec["panels"][0][field] = value
        with pytest.raises(comic_spec.SpecError) as ei:
            comic_renderer.render_svg(spec)
        assert "panel 0" in str(ei.value) or "title" in str(ei.value)
    for n_panels, label in ((2, "too few"), (5, "too many")):
        spec = good_spec()
        spec["panels"] = spec["panels"][:1] * n_panels
        with pytest.raises(comic_spec.SpecError):
            comic_spec.check(spec)
    with pytest.raises(comic_spec.SpecError):
        comic_spec.loads("{not json at all")


def test_every_violation_named_at_once():
    spec = {"title": "", "panels": [{"who": ["grok"], "pose": "moonwalk",
                                     "action": "", "caption": ""}]}
    bad = comic_spec.errors(spec)
    assert len(bad) >= 5                              # loud, not first-error
    assert any("grok" in b for b in bad)
    assert any("moonwalk" in b for b in bad)


def test_budget_by_construction_exhaustive():
    proof = comic_spec.BUDGET_PROOF
    assert set(proof["worst_case"]) == set(comic_spec.POSES)   # every pose
    for pose, row in proof["worst_case"].items():
        assert row["chars"] < comic_spec.CHAR_BUDGET, (pose, row)
        assert row["tokens"] < comic_spec.TOKEN_BUDGET, (pose, row)
    worst_chars = max(r["chars"] for r in proof["worst_case"].values())
    worst_tokens = max(r["tokens"] for r in proof["worst_case"].values())
    assert worst_chars < 1200 and worst_tokens < 300   # the two walls


def test_serialize_canonical_roundtrip():
    spec = good_spec()
    text = comic_spec.serialize(spec)
    assert len(text) < comic_spec.CHAR_BUDGET         # real session fits too
    assert comic_spec.loads(text) == spec
    assert text == comic_spec.serialize(comic_spec.loads(text))


def test_json_schema_matches_frozen_vocab():
    schema = comic_spec.json_schema()
    item = schema["properties"]["panels"]["items"]["properties"]
    assert item["who"]["items"]["enum"] == list(comic_spec.CAST)
    assert set(item["pose"]["enum"]) == set(comic_spec.POSES)
    assert schema["properties"]["panels"]["minItems"] == 3
    assert schema["properties"]["panels"]["maxItems"] == 4


def test_pose_bbox_keeps_figures_inside_panels():
    ground = comic_renderer.PANEL_H - comic_renderer.CAPTION_H - 20
    for pose in comic_spec.POSES:                      # every pose, worst slot
        slot_w = comic_renderer.PANEL_W / comic_spec.WHO_MAX
        bb = comic_renderer.pose_bbox(pose)
        scale = min(0.95, (slot_w - 26.0) / (bb[2] - bb[0]),
                    (ground - comic_renderer.ACTION_H - 22.0) / (bb[3] - bb[1]))
        assert bb[3] * scale <= ground + 0.01          # feet on the ground
        # head top stays below the action band (panel-local, same law the
        # renderer's fit enforces: ground - height*scale >= ACTION_H + 22)
        assert ground - (bb[3] - bb[1]) * scale >= comic_renderer.ACTION_H + 22 - 1e-9
