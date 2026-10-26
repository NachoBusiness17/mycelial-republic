"""tests/test_cost_rollup.py — cost_rollup.py unit + CLI cover.

Owns the contract landed in IMP5 (watch/inbox/last_mile_20260930/IMP5_COST.md):
  - all four scattered surfaces feed one rollup (day, model, calls, total_usd, surfaces)
  - grand total + trailing trend window with zero-filled days
  - unparseable surfaces are NAMED (path + line + error) and never dropped
  - --json emits a dashboard-parsable payload
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import cost_rollup  # noqa: E402


@pytest.fixture()
def tree(tmp_path: Path) -> Path:
    """A miniature replica of all four cost surfaces."""
    (tmp_path / "logs" / "duel").mkdir(parents=True)
    (tmp_path / "logs" / "mates").mkdir(parents=True)
    (tmp_path / "logs" / "hermes_gopher_burn_20260928").mkdir(parents=True)
    (tmp_path / "training").mkdir(parents=True)

    (tmp_path / "logs" / "duel" / "duels.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "ask_id": "duel-1",
                        "a_model": "model-a",
                        "b_model": "model-b",
                        "judge": "the-judge",
                        "a_cost": 0.10,
                        "b_cost": 0.02,
                        "judge_cost": 0.03,
                        "ts": "2026-09-28T10:00:00+00:00",
                    }
                ),
                # malformed line: must be named, never dropped
                "{not json",
                json.dumps(
                    {
                        "ask_id": "duel-2",
                        "a_model": "model-a",
                        "b_model": "model-b",
                        "judge": "the-judge",
                        "a_cost": 0.05,
                        "b_cost": 0.01,
                        "judge_cost": 0.02,
                        "ts": "2026-09-29T10:00:00+00:00",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (tmp_path / "logs" / "mates" / "alpha_burn_20260929.jsonl").write_text(
        json.dumps({"id": "m1", "model": "glm", "cost_usd": 0.05}) + "\n",
        encoding="utf-8",
    )

    (tmp_path / "logs" / "hermes_gopher_burn_20260928" / "output.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"id": "g1", "model": "glm", "cost_usd": 0.0712, "cost": 0.0457}),
                # no cost_usd, only the raw cost field: the fallback must catch it
                json.dumps({"id": "g2", "model": "glm", "cost": 0.02}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (tmp_path / "training" / "cost_ledger.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "schema": "cost_ledger.v1",
                        "ts": "2026-09-28T12:00:00+00:00",
                        "actual": {"usd_est": 0.0167, "usd_fixed": 0.0003, "calls": 7},
                        "platform": {"model": "deepseek-v4-flash", "seat": "deepseek"},
                    }
                ),
                # route-only no-op: zero calls, zero usd -> no bucket
                json.dumps(
                    {
                        "schema": "cost_ledger.v1",
                        "ts": "2026-09-28T13:00:00+00:00",
                        "actual": {"usd_est": 0.0, "usd_fixed": 0.0, "calls": 0},
                        "platform": {"model": "", "seat": "ollama"},
                    }
                ),
                # empty platform.model: falls back to estimate.model
                json.dumps(
                    {
                        "schema": "cost_ledger.v1",
                        "ts": "2026-09-29T09:00:00+00:00",
                        "actual": {"usd_est": 0.0045, "usd_fixed": 0.0, "calls": 10},
                        "estimate": {"model": "fallback-model"},
                        "platform": {"model": "", "seat": "deepseek"},
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return tmp_path


def _cell(report: dict, day: str, model: str) -> dict | None:
    for c in report["rollup"]:
        if c["day"] == day and c["model"] == model:
            return c
    return None


def test_rollup_aggregates_all_four_surfaces(tree: Path) -> None:
    report = cost_rollup.build_report(tree)

    duel = _cell(report, "2026-09-28", "model-a")
    assert duel == {
        "day": "2026-09-28",
        "model": "model-a",
        "calls": 1,
        "total_usd": 0.10,
        "surfaces": ["logs/duel/duels.jsonl"],
    }

    judge = _cell(report, "2026-09-28", "the-judge")
    assert judge is not None and judge["total_usd"] == pytest.approx(0.03)
    assert judge["calls"] == 1

    mates = _cell(report, "2026-09-29", "glm")
    assert mates is not None
    assert mates["total_usd"] == pytest.approx(0.05)
    assert "logs/mates/alpha_burn_20260929.jsonl" in mates["surfaces"]

    gopher = _cell(report, "2026-09-28", "glm")
    assert gopher is not None
    assert gopher["total_usd"] == pytest.approx(0.0712 + 0.02)
    assert gopher["calls"] == 2

    ledger = _cell(report, "2026-09-28", "deepseek-v4-flash")
    assert ledger is not None
    assert ledger["total_usd"] == pytest.approx(0.017)
    assert ledger["calls"] == 7

    fb = _cell(report, "2026-09-29", "fallback-model")
    assert fb is not None and fb["calls"] == 10

    assert _cell(report, "2026-09-28", "ollama") is None  # zero-cost no-op makes no bucket


def test_grand_total_sums_cells(tree: Path) -> None:
    report = cost_rollup.build_report(tree)
    assert report["grand_total_usd"] == pytest.approx(round(sum(c["total_usd"] for c in report["rollup"]), 4))
    assert report["grand_total_calls"] == sum(c["calls"] for c in report["rollup"])


def test_trend_window_is_trailing_and_zero_filled(tree: Path) -> None:
    report = cost_rollup.build_report(tree, days=7)
    days = [t["day"] for t in report["trend"]]
    assert len(days) == 7
    assert days[-1] == "2026-09-29"  # ends at the latest day with data
    assert days[0] == "2026-09-23"
    # duel trio (0.10 + 0.02 + 0.03) + gopher (0.0712 + 0.02) + ledger (0.017)
    assert report["trend"][-2]["total_usd"] == pytest.approx(0.2582)
    assert report["trend"][0]["total_usd"] == 0.0  # gap days stay visible


def test_unparseable_rows_are_named_never_dropped(tree: Path) -> None:
    report = cost_rollup.build_report(tree)
    bad = [u for u in report["unparseable"] if u["surface"] == "logs/duel/duels.jsonl"]
    assert len(bad) == 1
    assert bad[0]["line"] == 2
    assert "bad JSON" in bad[0]["error"]
    # the good rows around the bad line still counted
    assert _cell(report, "2026-09-29", "model-a")["total_usd"] == pytest.approx(0.05)


def test_missing_required_surface_is_named(tmp_path: Path) -> None:
    report = cost_rollup.build_report(tmp_path)
    surfaces = {u["surface"] for u in report["unparseable"]}
    assert "logs/duel/duels.jsonl" in surfaces
    assert "training/cost_ledger.jsonl" in surfaces
    assert report["rollup"] == []
    assert report["grand_total_usd"] == 0.0


def test_json_cli_payload(tree: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "cost_rollup.py"), "--json", "--root", str(tree)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    for key in ("generated_utc", "surfaces", "rollup", "grand_total_usd", "grand_total_calls", "trend", "unparseable"):
        assert key in payload
    assert payload["grand_total_usd"] > 0


def test_text_cli_names_unparseable(tree: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "cost_rollup.py"), "--root", str(tree)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert "GRAND TOTAL" in proc.stdout
    assert "UNPARSEABLE (named, never dropped)" in proc.stdout
    assert "logs/duel/duels.jsonl line 2" in proc.stdout
