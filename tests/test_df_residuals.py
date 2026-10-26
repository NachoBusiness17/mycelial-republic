"""Unit tests for DF fold residuals (Temptation.luau, ProceduralBody.luau, Worldgen.luau).

Verifies:
1. Zero em-dashes invariant across all three files.
2. Supernatural villain plots in Temptation.luau (deathless_cult, artifact_theft, usurp_throne, false_prophet).
3. Per-class attack triggers and anatomical/evil filtering in ProceduralBody.luau.
4. Ages of Powers branch in Worldgen.luau (Three Powers, Two Powers, Powers, Ghost and Shadows, Civilization).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "roblox" / "src" / "shared"
EM_DASH = re.compile(r"[\u2010\u2011\u2012\u2013\u2014\u2015]")


def test_no_em_dashes_in_folded_modules():
    targets = [
        SHARED / "Temptation.luau",
        SHARED / "ProceduralBody.luau",
        SHARED / "Worldgen.luau",
    ]
    for target in targets:
        assert target.exists(), f"Missing target file: {target}"
        content = target.read_text(encoding="utf-8")
        matches = EM_DASH.findall(content)
        assert len(matches) == 0, f"Found {len(matches)} em-dashes in {target.name}"


def test_temptation_supernatural_plots():
    content = (SHARED / "Temptation.luau").read_text(encoding="utf-8")
    expected_plots = [
        "grant_of_belonging",
        "deathless_cult",
        "artifact_theft",
        "usurp_throne",
        "false_prophet",
    ]
    for plot in expected_plots:
        assert f"{plot} = {{" in content, f"Missing plot definition for {plot}"

    expected_ethics = [
        "OATH_BREAKING",
        "THEFT",
        "TREASON",
        "CORRUPTION",
        "DECEIT",
    ]
    for ethic in expected_ethics:
        assert f"{ethic} = {{" in content, f"Missing ethic definition for {ethic}"

    assert "function Temptation.listPlots" in content
    assert "function Temptation.getPlot" in content


def test_procedural_body_per_class_triggers():
    content = (SHARED / "ProceduralBody.luau").read_text(encoding="utf-8")
    triggers = [
        'material == "FLAME"',
        'must_have_scorpion_tail',
        'must_have_insect_stinger',
        'must_have_webs',
        'must_have_poison_bite',
        'suck_blood_through_proboscis',
        'hasMouthOrBeak',
        'BREATHE_TRAILING_FLOW',
        'BREATHE_UNDIRECTED',
        'POISON_BLOOD',
        'SECRETION',
    ]
    for trigger in triggers:
        assert trigger in content, f"Missing trigger logic: {trigger}"


def test_worldgen_ages_of_powers_branch():
    content = (SHARED / "Worldgen.luau").read_text(encoding="utf-8")
    assert "Worldgen.INITIAL_POWERS = 30" in content
    assert "function Worldgen.setSupernaturalPowers" in content
    assert "function Worldgen.supernaturalPowers" in content
    assert "function Worldgen.remainingPowers" in content
    assert "function Worldgen.resetBossKills" in content
    assert '"The Age of Three Powers"' in content
    assert '"The Age of Two Powers"' in content
    assert '"The Age of Powers"' in content
    assert '"The Age of Ghost and Shadows"' in content
    assert '"The Age of Civilization"' in content
