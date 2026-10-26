"""Tests for tools/marathon_voice_metrics.py (the Rampancy Wire probe).

VERIFIER for the tool's CONSUMER contract: these tests pin the garbled-burst
token heuristic (including the known "^9320wrefkddud" class), the per-1000
math on a tiny synthetic text, terminal section counting, the arc labels on
an emitted feature file, and that the emitted JSON loads as a dict.

Corpus credit law: marathon.bungie.org on any use (the emitted JSON carries
it in the "source" field).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import marathon_voice_metrics as mvm  # noqa: E402


def test_garbled_heuristic_known_class_flagged():
    # The known "^9320wrefkddud" class must match rule A (mixed alnum).
    assert mvm.is_garbled_burst("9320wrefkddud")
    assert mvm.is_garbled_burst("9034thssksbvs")
    # Consonant-wall / vowel-starved forms.
    assert mvm.is_garbled_burst("9066hhhthsrls")
    assert mvm.is_garbled_burst("wrefkddud")


def test_garbled_heuristic_clean_tokens_pass():
    # Real prose, terminal ids, hex, binary noise, and canon alien names
    # must NOT count as garble.
    for tok in (
        "strengths",  # consonant wall too short (ngt-h-s runs stay under 6)
        "computer",
        "durandal",
        "rampancy",
        "systems",
        "attempts",  # doubled tt sits in a run of 2, never inside a run of 4
        "worthless",
        "resupply",
        "vt920",  # digits but only 2 letters
        "a94f12",  # hex-ish, only 2 letters
        "101111011110111100001",  # pure digits
        "rkncacnter",  # W'rkncacnter letter-run, no run-with-double
    ):
        assert not mvm.is_garbled_burst(tok), tok


def test_per_1000_math_on_synthetic_text():
    text = "I know my mind. I've seen me fall."
    got = mvm.metrics_for_text(text)
    # words: I know my mind I've seen me fall = 8; fp: I my I've me = 4
    assert got["word_count"] == 8
    assert got["first_person_singular"] == 4
    assert got["first_person_per_1000"] == 500.0
    assert got["garbled_burst_tokens"] == 0
    assert got["terminal_count"] == 0


def test_terminal_section_counting_skips_nav_stubs():
    text = (
        "### Fire! Fire! Fire! Fire! Fire! (Terminal 2)\n"
        "he is in the Jealous stage of Rampancy.\n"
        "### Go Back to Marathon's Story Home Page\n"
        "nav noise\n"
        "### Go Next Chapter... Captured\n"
        "more nav noise\n"
    )
    assert mvm.terminal_count(text) == 1


def test_arc_labels_present_and_json_loads(tmp_path):
    corpus = tmp_path / "marathon_terminals"
    for game, body in (
        ("m1", "I am awake. ### Defend THIS! (Terminal 2)\nalarm text\n"),
        ("m2", "My fleet is mine. ### Central Cicerone (Terminal 1)\nmore\n"),
        ("m3", "^9320wrefkddud overthought unravel ### Aye Mak Sicur (Terminal 0)\nGo.\n"),
    ):
        (corpus / game).mkdir(parents=True)
        (corpus / game / "chapter.txt").write_text(body, encoding="utf-8")

    out = tmp_path / "features.json"
    rc = mvm.main(["--corpus", str(corpus), "--out", str(out)])
    assert rc == 0

    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert "marathon.bungie.org" in data["source"]
    assert data["chapter_file_count"] == 3

    by_game = {ch["game"]: ch for ch in data["chapters"]}
    assert by_game["m1"]["arc_label"] == "Melancholy onset"
    assert by_game["m2"]["arc_label"] == "peak rampancy"
    assert by_game["m3"]["arc_label"] == "dissolution"

    # Rollups are internally consistent: trilogy fp equals the sum of games.
    fp_sum = sum(g["first_person_singular"] for g in data["games"].values())
    assert data["trilogy"]["first_person_singular"] == fp_sum
    # Garble from the m3 synthetic body made it into the features.
    assert data["games"]["m3"]["garbled_burst_tokens"] == 1
