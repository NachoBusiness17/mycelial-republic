"""tests for tools/battery_rerun.py - frozen battery regression harness.

Offline, stdlib only, fixture seals. Covers the t71 lane contract:
seal mismatch refuses with exit 2 and writes no score-out; happy path
scaffolds the score outline without ever opening ground-truth content
unless --score is passed; heldout pin drift and shape drift refuse.
Spec: watch/inbox/method_card_exp/RERUN_PREREG_20260926.md Sections 0 to 5.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import battery_rerun as br  # noqa: E402

INDEX_BODY = b'{"row": 1}\n{"row": 2}\n{"row": 3}\n'
LAST_RUN_BODY = b'{"run": "fixture"}\n'
ROLLUP_BODY = b'{"rollup": true}\n'

BATTERY_BODY = (
    "# Battery heldout fixture\n\n"
    "- Q1. fixture heldout question one?\n"
    "- Q2. fixture heldout question two?\n"
)

GROUND_TRUTH_BODY = (
    "# Ground truth fixture\n\n"
    "## Q1\nfixture truth one SENTINEL_GT_1\n\n"
    "## Q2\nfixture truth two\n\n"
    "## Q3\norphan truth row\n"
)

ANSWERS_BODY = (
    "# RERUN ANSWERS fixture\n\n"
    "- Q1. fixture answer one, path dashboard/data/ESTATE_INDEX.jsonl\n"
    "- Q2. fixture answer two, value 3\n"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_fixture(tmp_path: Path) -> dict:
    """Lay down a tiny sealed estate + heldouts + pins. Returns path dict."""
    index = tmp_path / "dashboard" / "data" / "ESTATE_INDEX.jsonl"
    index.parent.mkdir(parents=True)
    index.write_bytes(INDEX_BODY)
    last_run = tmp_path / "dashboard" / "static" / "index_data" / "last_run.json"
    last_run.parent.mkdir(parents=True)
    last_run.write_bytes(LAST_RUN_BODY)
    rollup = last_run.parent / "rollup.json"
    rollup.write_bytes(ROLLUP_BODY)

    battery = tmp_path / "BATTERY_HELDOUT.md"
    battery.write_bytes(BATTERY_BODY.encode("utf-8"))
    truth = tmp_path / "GROUND_TRUTH_HELDOUT.md"
    truth.write_bytes(GROUND_TRUTH_BODY.encode("utf-8"))
    answers = tmp_path / "RERUN_ANSWERS_fixture.md"
    answers.write_bytes(ANSWERS_BODY.encode("utf-8"))

    seal = {
        "experiment": "fixture",
        "index_sha256": sha(INDEX_BODY),
        "index_bytes": len(INDEX_BODY),
        "index_rows": INDEX_BODY.count(b"\n"),
        "last_run_sha256": sha(LAST_RUN_BODY),
        "rollup_sha256": sha(ROLLUP_BODY),
    }
    seal_path = tmp_path / "FREEZE_SEAL.json"
    seal_path.write_text(json.dumps(seal), encoding="utf-8")

    pins = {
        "battery_sha256": sha(BATTERY_BODY.encode("utf-8")),
        "ground_truth_sha256": sha(GROUND_TRUTH_BODY.encode("utf-8")),
    }
    pins_path = tmp_path / "fixture_pins.json"
    pins_path.write_text(json.dumps(pins), encoding="utf-8")

    return {
        "estate_root": tmp_path,
        "seal": seal_path,
        "battery": battery,
        "ground_truth": truth,
        "answers": answers,
        "pins": pins_path,
    }


def run_tool(fx: dict, tmp_path: Path, score: bool) -> tuple[int, Path]:
    score_out = tmp_path / "RERUN_SCORE_scaffold.md"
    argv = [
        "--answers", str(fx["answers"]),
        "--score-out", str(score_out),
        "--seal", str(fx["seal"]),
        "--estate-root", str(fx["estate_root"]),
        "--battery", str(fx["battery"]),
        "--ground-truth", str(fx["ground_truth"]),
        "--pins", str(fx["pins"]),
    ]
    if score:
        argv.append("--score")
    code = br.main(argv)
    return code, score_out


def test_seal_mismatch_refuses(tmp_path, capsys):
    fx = build_fixture(tmp_path)
    index = fx["estate_root"] / "dashboard" / "data" / "ESTATE_INDEX.jsonl"
    index.write_bytes(INDEX_BODY + b'{"row": 4}\n')  # post-seal spine change
    code, score_out = run_tool(fx, tmp_path, score=False)
    err = capsys.readouterr().err
    assert code == br.EXIT_REFUSED == 2
    assert "SEAL MISMATCH" in err
    assert not score_out.exists(), "refused run must write no score-out"


def test_heldout_drift_refuses(tmp_path, capsys):
    fx = build_fixture(tmp_path)
    fx["battery"].write_text(BATTERY_BODY + "tampered\n", encoding="utf-8")
    code, score_out = run_tool(fx, tmp_path, score=False)
    err = capsys.readouterr().err
    assert code == br.EXIT_REFUSED == 2
    assert "HELDOUT DRIFT" in err
    assert not score_out.exists()


def test_shape_drift_refuses(tmp_path, capsys):
    fx = build_fixture(tmp_path)
    seal = json.loads(fx["seal"].read_text(encoding="utf-8"))
    seal["index_rows"] = 99  # abort condition 3: row count no longer matches
    fx["seal"].write_text(json.dumps(seal), encoding="utf-8")
    code, score_out = run_tool(fx, tmp_path, score=False)
    err = capsys.readouterr().err
    assert code == br.EXIT_REFUSED == 2
    assert "SHAPE DRIFT" in err
    assert not score_out.exists()


def test_happy_path_default_never_opens_ground_truth(tmp_path, capsys):
    fx = build_fixture(tmp_path)
    code, score_out = run_tool(fx, tmp_path, score=False)
    out = capsys.readouterr().out
    assert code == br.EXIT_OK == 0
    assert "SEAL OK" in out
    assert score_out.exists()
    text = score_out.read_text(encoding="utf-8")
    assert "NOT OPENED" in text
    assert "SENTINEL_GT_1" not in text, "default mode must not leak ground-truth content"
    assert "fixture answer one" in text
    assert "### Q1" in text and "### Q2" in text
    assert "VERDICT (MATCH/PARTIAL/MISS):" in text
    assert "MATCH= PARTIAL= MISS= of 2 rows" in text


def test_score_mode_pairs_ground_truth(tmp_path, capsys):
    fx = build_fixture(tmp_path)
    code, score_out = run_tool(fx, tmp_path, score=True)
    out = capsys.readouterr().out
    assert code == br.EXIT_OK == 0
    assert "SEAL OK" in out
    text = score_out.read_text(encoding="utf-8")
    assert "SENTINEL_GT_1" in text, "score phase pairs ground truth into the scaffold"
    assert "Q3" in text, "orphan truth section must be flagged"
    assert "unpaired ground-truth sections" in text


def test_gate_refuses_missing_seal_file(tmp_path, capsys):
    fx = build_fixture(tmp_path)
    fx["seal"].unlink()
    code, score_out = run_tool(fx, tmp_path, score=False)
    err = capsys.readouterr().err
    assert code == br.EXIT_REFUSED == 2
    assert "SEAL MISMATCH" in err
    assert not score_out.exists()
