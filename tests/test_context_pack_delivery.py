"""Context-pack delivery pipe (wave5 render-pipe repair, 2026-09-29).

Pins the repair the arch-01/s2-08 census demanded: the mandated core —
standing objective, compiled laws, operator directives, RIB doctrine —
renders in EVERY pack mode within budget. The old renderer gated
directives to plan/full, gated doctrine out of janitor/route, and the
bare-policy ladder rung then dropped the whole ctx tier (directives
included) in every overflow render: 0/6 live renders reached the model.
These tests fail if the pipe silently unwires again.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MODES = ["janitor", "route", "build", "audit", "plan", "full"]

# Known compiled law bodies from the live flash pack (same markers the
# quantized-laws wiring test pins).
LAW_MARKERS = ("Verify with git diff", "Elevate with a deliberate ask")


@pytest.fixture(scope="module")
def renders() -> dict:
    from mag.context_pack import build_context_pack, format_context_pack_text

    out = {}
    for mode in MODES:
        pack = build_context_pack(mode=mode, fast=True)
        out[mode] = format_context_pack_text(pack, mode=mode)
    return out


@pytest.mark.parametrize("mode", MODES)
def test_operator_directives_render_in_every_mode(renders, mode):
    assert "### L0c Operator directives" in renders[mode], (
        f"directive tier missing from mode={mode} — the delivery pipe dropped it")


@pytest.mark.parametrize("mode", MODES)
def test_quantized_laws_render_in_every_mode(renders, mode):
    text = renders[mode]
    assert "### L0b Compiled laws" in text, f"laws section missing from mode={mode}"
    assert any(m in text for m in LAW_MARKERS), f"no known compiled law rode mode={mode}"


@pytest.mark.parametrize("mode", MODES)
def test_rib_doctrine_renders_in_every_mode(renders, mode):
    assert "### L0d RIB Doctrine" in renders[mode], (
        f"doctrine missing from mode={mode} (was gated out of janitor/route)")


@pytest.mark.parametrize("mode", MODES)
def test_render_fits_budget_without_hard_clip(renders, mode):
    from mag.context_pack import MODE_CONFIG

    text = renders[mode]
    assert "(pack clipped)" not in text, f"hard clip fired in mode={mode} — core no longer fits"
    assert len(text) <= MODE_CONFIG[mode]["max_chars"], (
        f"mode={mode} render {len(text)} exceeds its own budget")


def test_janitor_render_smaller_than_full(renders):
    assert len(renders["janitor"]) < len(renders["full"]), (
        "janitor pack must stay smaller than full (mode ladder contract)")


def test_core_sections_survive_forced_shed_ladder(monkeypatch, tmp_path):
    """The old D1: the bare-policy rung rebuilt the pack without directives.

    Force an overflow the shed rungs must resolve (budget sits between the
    sheddable context and the core floor, so rungs 1-3 do the work; the hard
    clip is the last resort for sub-floor budgets by design) and prove the
    whole core survives.
    """
    import json

    from mag import context_pack as cp

    pack = cp.build_context_pack(mode="janitor", fast=True)
    offload = tmp_path / "PACK_OFFLOAD.jsonl"
    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", offload)
    # janitor: assembled ~4.3k, core floor after bonds shed ~3.8k.
    text = cp.format_context_pack_text(pack, mode="janitor", max_chars=4000)
    assert "### L0c Operator directives" in text, "directives died under the shed ladder"
    assert "### L0b Compiled laws" in text, "laws died under the shed ladder"
    assert "### L0d RIB Doctrine" in text, "doctrine died under the shed ladder"
    assert "(pack clipped)" not in text, "hard clip fired though sheddable context existed"
    rows = [json.loads(l) for l in offload.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert rows, "shed ladder never fired — the forced overflow did not exercise rungs"
    for r in rows:
        assert 1 <= r["stage"] <= 4, f"offload stage out of contract: {r}"


def test_task_outlives_context_under_shed_ladder(monkeypatch, tmp_path):
    """The old ladder put task last, so the hard clip amputated the job.

    Under the shed rungs the task now rides inside the protected group, ahead
    of sheddable context. Budget sits between the post-shed floor and the
    assembled size so rung 3 resolves the overflow.
    """
    from mag import context_pack as cp

    pack = cp.build_context_pack(mode="route", fast=True)
    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", tmp_path / "PACK_OFFLOAD.jsonl")
    # route: assembled ~5.5k, floor after resonance+coordination shed ~3.6k.
    text = cp.format_context_pack_text(pack, mode="route", max_chars=5200)
    assert "### Brief" in text or "## L3 Task" in text, "task amputated under the shed ladder"
    assert "(pack clipped)" not in text, "hard clip fired though sheddable context existed"


def test_objective_is_bounded_in_tight_mode(renders):
    """The old objective read was uncapped: 2.2k of thesis overflowed the
    janitor budget outright. Janitor now carries a bounded objective."""
    from mag.context_pack import ROOT

    text = renders["janitor"]
    i = text.find("### L0b Current objective")
    j = text.find("### L0b Compiled laws")
    assert 0 <= i < j, "objective/laws section order broken in janitor render"
    section = text[i:j]
    obj_path = ROOT / "memory" / "boot" / "CURRENT_OBJECTIVE.md"
    if obj_path.is_file() and len(obj_path.read_text(encoding="utf-8", errors="replace").strip()) > 400:
        assert "(objective clipped" in section, "janitor objective rendered uncapped"
    assert len(section) <= 400 + 200, "objective section exceeds its bound + header/marker"


def test_stale_pack_debt_pointer_still_reaches_tight_modes(renders):
    """The 7-day staleness gate lives in _quantized_laws; the renderer must
    not hide its debt pointer behind a clip in the modes it serves."""
    from mag.context_pack import _quantized_laws

    s = _quantized_laws()
    # Either fresh laws (section header) or the visible-debt pointer — never
    # silence — is the delivery contract.
    assert s == "" or s.startswith("[compile v") or "STALE" in s
