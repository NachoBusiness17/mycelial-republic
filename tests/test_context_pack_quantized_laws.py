"""Context-pack delivery of the quantized laws (the v0.3 vehicle).

QUANTIZER_V03_20260927: the packs' original sin was zero consumers. These
tests pin the wiring so it cannot silently unwire: the section renders
INSIDE the default budget (a section past the clip is unconsumed), the
stale branch renders as visible debt instead of law, and the caps hold.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_quantized_laws_section_renders_in_default_budget():
    from mag.context_pack import build_context_pack, format_context_pack_text
    txt = format_context_pack_text(build_context_pack())
    i = txt.find("Compiled laws")
    assert i >= 0, "compiled-laws section missing from rendered pack"
    assert i < 4500, "section lands past the default clip — unconsumed again"
    assert "Verify with git diff" in txt or "Elevate with a deliberate ask" in txt, (
        "no known compiled law rode the pack")


def test_quantized_laws_capped_and_headered():
    from mag.context_pack import _quantized_laws
    s = _quantized_laws()
    assert s.startswith("[compile v"), "compile provenance header missing"
    assert len(s) <= 1800, "laws section exceeds its byte cap"


def test_stale_packs_render_as_visible_debt(tmp_path, monkeypatch):
    from mag import context_pack as cp
    import json

    qt = tmp_path / "memory" / "corpus" / "quantized_thought"
    qt.mkdir(parents=True)
    (qt / "instructions_flash.jsonl").write_text(
        json.dumps({"flash": "Verify everything before declaring done"}) + "\n",
        encoding="utf-8")
    (qt / "compile_report.json").write_text(json.dumps(
        {"v": "0.3", "compiled": "2026-09-01T00:00:00+00:00"}), encoding="utf-8")
    monkeypatch.setattr(cp, "ROOT", tmp_path)
    s = cp._quantized_laws()
    assert "STALE" in s and "recompile owed" in s, (
        "stale packs must render as a debt pointer, never silent law")
    assert "Verify everything" not in s, "stale law bytes must NOT ride the pack"
