"""Blade template registry — files+code only, no instance calls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "state" / "vast"))

import blade_buyer as bb  # noqa: E402


def test_registry_has_required_fields() -> None:
    d = json.loads((ROOT / "state" / "vast" / "blade_templates.json").read_text(encoding="utf-8"))
    assert len(d["templates"]) >= 3
    for t in d["templates"]:
        for k in ("name", "image", "onstart_cmd", "env", "port", "vram_gb"):
            assert k in t, t.get("name")


def test_default_is_ollama_qwen3() -> None:
    t = bb.pick_template(None)
    assert t["name"] == "qwen3-8b-ollama"
    assert t["image"] == "ollama/ollama:latest"
    assert t["port"] == 11434
    assert "status.json" in t["onstart_cmd"]


def test_pick_fits_vram() -> None:
    small = bb.pick_template({"gpu_ram": 12000})
    assert small["name"] == "qwen3-8b-ollama"
    big = bb.pick_template({"gpu_ram": 48000})
    assert big["name"] == "qwen25-32b-ollama"
    assert big["vram_gb"] <= 48


def test_library_templates_not_auto_selected() -> None:
    t = bb.pick_template({"gpu_ram": 200000})
    assert t.get("blade_eligible") is True
    assert t.get("image")
    names = {x["name"] for x in bb.load_templates()["templates"]}
    assert "vast-lib-glm-5.2" in names
    assert "vast-lib-qwen38-27b" in names
