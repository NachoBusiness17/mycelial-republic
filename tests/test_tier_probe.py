"""Tier probe — deterministic tests (no API calls).

Covers the objective scoring, cost math, and report plumbing so the harness
can be trusted when it runs live against real DeepSeek tiers.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.tier_probe import cost_for, score_design, score_exec  # noqa: E402


def test_exec_score_good_implementation() -> None:
    code = (
        "```python\n"
        "from datetime import datetime\n"
        "def parse_ts(iso: str):\n"
        "    iso = iso.replace('Z', '+00:00')\n"
        "    return datetime.fromisoformat(iso)\n"
        "```"
    )
    score, note = score_exec(code)
    assert score == 1.0, note
    assert "passes hidden test" in note


def test_exec_score_bad_implementation() -> None:
    # compiles + has the function, but returns the string unchanged → fails
    code = "```python\ndef parse_ts(iso: str):\n    return iso\n```"
    score, note = score_exec(code)
    assert score == 0.5, note
    assert "fails hidden assert" in note


def test_exec_score_no_function() -> None:
    assert score_exec("```python\nx = 1\n```")[0] == 0.0
    assert score_exec("```python\ndef wrong_name(a): return a\n```")[0] == 0.0


def test_design_score_rubric() -> None:
    good = (
        "1. `python -m pytest tests/ -x` PASS if: 0 failures\n"
        "2. `pytest tests/test_router.py -k tier` PASS if: 2 passed\n"
        "3. `git diff --stat` PASS if: only expected files changed"
    )
    s, note = score_design(good)
    assert s == 1.0, note
    prose = "We should probably test the routing stuff and see if things work okay in general."
    assert score_design(prose)[0] < 0.5


def test_cost_math_real_prices() -> None:
    # flash: miss $0.14/M in, out $0.28/M  → 1000 in + 500 out = $0.00014 + $0.00014
    c = cost_for("deepseek-v4-flash", {"prompt_tokens": 1000, "completion_tokens": 500})
    assert c["cost_miss"] == round(1000 / 1e6 * 0.14 + 500 / 1e6 * 0.28, 6)
    # pro is more expensive
    p = cost_for("deepseek-v4-pro", {"prompt_tokens": 1000, "completion_tokens": 500})
    assert p["cost_miss"] > c["cost_miss"]
    # cache-hit lane is ~50-120x cheaper on input
    assert c["cost_hit"] < c["cost_miss"]


def test_cost_counts_reasoning_as_output() -> None:
    c = cost_for("deepseek-v4-flash", {"prompt_tokens": 100, "completion_tokens": 50, "reasoning_tokens": 100})
    assert c["cost_miss"] == round(100 / 1e6 * 0.14 + 150 / 1e6 * 0.28, 6)


def test_report_renders_and_ledger_appends(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    import tools.tier_probe as tp

    monkeypatch.setattr(tp, "LEDGER", tmp_path / "assumptions.md")
    cells = [
        {"task": "exec", "task_label": "exec", "tier": "flash-off", "ok": True, "score": 1.0, "note": "passes",
         "text": "x", "ms": 5, "usage": cost_for("deepseek-v4-flash", {"prompt_tokens": 100, "completion_tokens": 50})},
        {"task": "exec", "task_label": "exec", "tier": "pro-on", "ok": True, "score": 1.0, "note": "passes",
         "text": "x", "ms": 9, "usage": cost_for("deepseek-v4-pro", {"prompt_tokens": 100, "completion_tokens": 50})},
    ]
    report = tp.render_report(cells, live=False)
    assert "flash-off" in report and "pro-on" in report
    tp.append_ledger(cells, assumption="test assumption")
    assert tmp_path.joinpath("assumptions.md").is_file()
    txt = tmp_path.joinpath("assumptions.md").read_text(encoding="utf-8")
    assert "LOW fine" in txt or "tier matters" in txt
