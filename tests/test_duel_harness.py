"""Tests for tools/duel_harness.py (Mickey17 W3, 2026-09-29).

Covers: a full fixture duel with fake API responses injected (row written
with the exact ledger shape and real metered costs), the judge output
parser on strict / TIE / malformed text, judge-prompt construction (rubric
and both answers embedded), retroactive pair loading from a burn jsonl,
and cost metering preferring usage.cost over the price table. v1.1 (S5
Arena audit): blind judging pinned (no contender name ever reaches the
judge ask), presentation-order swap remapping the slot verdict back to
logical contenders, per-ledger parity alternation, and markdown-header
style counts. No network, no spend: the caller is injected.

Wave ledger return 8 (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md): the
duel was fired but never judged; these tests pin the harness that fixes it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import duel_harness

JUDGE_STRICT_A = (
    "WINNER: A\n"
    "CRIT | section coverage | A=5 | B=4 | A covers all sections, B skips two\n"
    "CRIT | defect severity | A=5 | B=3 | A finds the Wilson bound flaw\n"
    "CRIT | evidence citations | A=4 | B=4 | both cite section names\n"
    "CRIT | actionability | A=4 | B=3 | A names replacement measurements\n"
    "RATIONALE: A finds deeper numeric defects with concrete fixes.\n"
)

JUDGE_STRICT_B = (
    "WINNER: B\n"
    "CRIT | coverage | A=2 | B=5 | B sweeps every table\n"
    "RATIONALE: B is denser and cites row ids.\n"
)

JUDGE_TIE = (
    "winner: TIE\n"
    "RATIONALE: Same verdicts, same depth, different prose.\n"
)

JUDGE_GARBAGE = "I think both did fine, hard to say, maybe A edges it."


def _resp(content: str, cost: float | None = None,
          pt: int = 1000, ct: int = 500) -> dict:
    usage = {"prompt_tokens": pt, "completion_tokens": ct, "total_tokens": pt + ct}
    if cost is not None:
        usage["cost"] = cost
    return {
        "choices": [{"message": {"content": content, "reasoning": ""}, "finish_reason": "stop"}],
        "usage": usage,
    }


class _FakeLane:
    """Returns canned responses per model and records every call."""

    def __init__(self, a_text: str, b_text: str, judge_text: str) -> None:
        self.canned = {
            "qwen/qwen3.8-max-prime": _resp(a_text, cost=0.0123),
            "z-ai/glm-5.3-prime": _resp(b_text, cost=0.0456),
            "fireworks/ember-1": _resp(judge_text, cost=0.0071),
        }
        self.calls: list[tuple[str, str]] = []

    def __call__(self, model: str, prompt: str, key: str, max_tokens: int = 16000) -> dict:
        self.calls.append((model, prompt))
        return self.canned[model]


def test_fixture_duel_writes_row(tmp_path: Path) -> None:
    out = tmp_path / "duels.jsonl"
    a_text = "# Review A\n## Verdicts\nA: kill section 2."
    lane = _FakeLane(a_text, "B: keep everything.", JUDGE_STRICT_A)
    row = duel_harness.run_duel(
        ask_id="fx-1",
        task="adversarially review the spec",
        a_model="qwen/qwen3.8-max-prime",
        b_model="z-ai/glm-5.3-prime",
        judge_model="fireworks/ember-1",
        rubric=["section coverage", "defect severity", "evidence citations", "actionability"],
        out_path=out,
        keys=["k1", "k2"],
        caller=lane,
        mode="live",
    )
    # ledger contract: exactly the promised keys present, correct values
    assert out.is_file()
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    banked = json.loads(lines[0])
    for key in ("ask_id", "a_model", "b_model", "a_cost", "b_cost", "judge",
                "winner", "rubric", "ts"):
        assert key in banked
    assert banked["ask_id"] == "fx-1"
    assert banked["a_model"] == "qwen/qwen3.8-max-prime"
    assert banked["b_model"] == "z-ai/glm-5.3-prime"
    assert banked["a_cost"] == 0.0123  # metered from usage.cost, not the price table
    assert banked["b_cost"] == 0.0456
    assert banked["judge_cost"] == 0.0071
    assert banked["judge"] == "fireworks/ember-1"
    assert banked["winner"] == "A"
    assert banked["rubric"] == ["section coverage", "defect severity",
                                "evidence citations", "actionability"]
    assert banked["mode"] == "live"
    assert banked["rationale"].startswith("A finds deeper")
    assert len(banked["criteria"]) == 4
    assert banked["criteria"][1] == {"criterion": "defect severity", "a": 5, "b": 3,
                                     "note": "A finds the Wilson bound flaw"}
    # style-control signals (S5 v1.1): length + markdown headers per contender
    assert banked["a_chars"] == len(a_text) and banked["b_chars"] == len("B: keep everything.")
    assert banked["a_headers"] == 2 and banked["b_headers"] == 0
    # empty ledger -> first duel presented unswapped
    assert banked["swap"] is False
    assert row == banked  # returned row is the banked row


def test_duel_fires_two_contenders_then_judge(tmp_path: Path) -> None:
    out = tmp_path / "duels.jsonl"
    lane = _FakeLane("A answer", "B answer", JUDGE_STRICT_B)
    duel_harness.run_duel(
        ask_id="fx-order",
        task="review the thing",
        a_model="qwen/qwen3.8-max-prime",
        b_model="z-ai/glm-5.3-prime",
        out_path=out, keys=["k1"], caller=lane,
    )
    models = [m for m, _ in lane.calls]
    assert models == ["qwen/qwen3.8-max-prime", "z-ai/glm-5.3-prime", "fireworks/ember-1"]
    # both contenders get the same ask verbatim (the duel invariant)
    assert lane.calls[0][1] == lane.calls[1][1] == "review the thing"
    # the judge ask embeds the rubric and both answers
    jp = lane.calls[2][1]
    assert "A answer" in jp and "B answer" in jp
    for crit in duel_harness.DEFAULT_RUBRIC.split(","):
        assert crit.strip() in jp
    # BLIND JUDGING PIN (S5 v1.1): contender identities never reach the judge
    for name in ("qwen", "glm", "z-ai", "fireworks"):
        assert name not in jp.lower()


def test_judge_prompt_shape() -> None:
    jp = duel_harness.judge_prompt(
        "review the spec", "alpha text", "beta text",
        ["coverage", "severity"], context="SPEC BODY",
    )
    assert jp.count("ANSWER_A") == 2 and jp.count("ANSWER_B") == 2
    assert "1. coverage" in jp and "2. severity" in jp
    assert "alpha text" in jp and "beta text" in jp and "SPEC BODY" in jp
    assert "no em-dashes" in jp
    assert "anonymous models" in jp
    assert "WINNER: A" in jp and "RATIONALE:" in jp


def test_swap_maps_verdict_back_to_logical_contenders(tmp_path: Path) -> None:
    out = tmp_path / "duels.jsonl"
    lane = _FakeLane("logical A text", "logical B text", JUDGE_STRICT_A)
    row = duel_harness.run_duel(
        ask_id="fx-swap", task="review",
        a_model="qwen/qwen3.8-max-prime", b_model="z-ai/glm-5.3-prime",
        out_path=out, keys=["k1"], caller=lane, swap=True,
    )
    # judge voted for slot A, but slot A held logical B's text
    assert row["swap"] is True and row["winner"] == "B"
    assert row["criteria"][1]["a"] == 3 and row["criteria"][1]["b"] == 5  # flipped
    jp = lane.calls[2][1]  # call 3 is the judge ask (1 and 2 fired the contenders)
    assert "logical B text" in jp.split("ANSWER_A")[1].split("ANSWER_B")[0]
    assert duel_harness.map_winner("TIE", True) == "TIE"
    assert duel_harness.map_winner("UNPARSED", True) == "UNPARSED"
    assert duel_harness.map_winner("A", False) == "A"
    assert duel_harness.remap_criteria([{"a": 1, "b": 2}], True) == [{"a": 2, "b": 1}]


def test_swap_alternates_by_ledger_parity(tmp_path: Path) -> None:
    out = tmp_path / "duels.jsonl"
    # empty ledger: auto picks no swap
    r0 = duel_harness.run_duel(ask_id="d0", task="t", a_model="qwen/qwen3.8-max-prime",
                               b_model="z-ai/glm-5.3-prime", out_path=out,
                               keys=["k1"], caller=_FakeLane("a", "b", JUDGE_STRICT_A))
    assert r0["swap"] is False
    # one row banked: auto flips presentation order
    r1 = duel_harness.run_duel(ask_id="d1", task="t", a_model="qwen/qwen3.8-max-prime",
                               b_model="z-ai/glm-5.3-prime", out_path=out,
                               keys=["k1"], caller=_FakeLane("a", "b", JUDGE_STRICT_A))
    assert r1["swap"] is True
    assert duel_harness.ledger_row_count(out) == 2


def test_count_headers_styles() -> None:
    assert duel_harness.count_headers("# one\nbody\n## two\n###three\n # four\nnot a # header\n") == 3
    assert duel_harness.count_headers("") == 0


def test_parse_judge_strict_and_tie() -> None:
    v = duel_harness.parse_judge(JUDGE_STRICT_A)
    assert v["parsed"] and v["winner"] == "A"
    assert len(v["criteria"]) == 4
    assert v["criteria"][0]["a"] == 5 and v["criteria"][0]["b"] == 4
    t = duel_harness.parse_judge(JUDGE_TIE)
    assert t["parsed"] and t["winner"] == "TIE" and t["criteria"] == []
    b = duel_harness.parse_judge(JUDGE_STRICT_B)
    assert b["parsed"] and b["winner"] == "B"
    assert b["criteria"][0]["note"] == "B sweeps every table"


def test_parse_judge_refuses_garbage() -> None:
    v = duel_harness.parse_judge(JUDGE_GARBAGE)
    assert not v["parsed"] and v["winner"] == "UNPARSED" and v["rationale"] == ""
    assert duel_harness.parse_judge("")["winner"] == "UNPARSED"
    # trailing model name on the winner line still parses
    w = duel_harness.parse_judge("WINNER: B (glm-prime)\nRATIONALE: sharper.\n")
    assert w["winner"] == "B" and w["rationale"] == "sharper."


def test_retro_load_pair(tmp_path: Path) -> None:
    burn = tmp_path / "burn.jsonl"
    rows = [
        {"id": "G1", "model": "qwen/qwen3.8-max-prime", "cost_usd": 0.0674, "content": "qwen review"},
        {"id": "G2", "model": "qwen/qwen3.8-max-prime", "cost_usd": 0.08, "content": "other"},
        {"id": "G3", "model": "z-ai/glm-5.3-prime", "cost_usd": 0.0264, "content": "glm review"},
    ]
    burn.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    a, b = duel_harness.load_pair(burn, "G1", "G3")
    assert a["content"] == "qwen review" and b["cost_usd"] == 0.0264
    with pytest.raises(KeyError):
        duel_harness.load_pair(burn, "G1", "G9")
    empty = tmp_path / "empty.jsonl"
    empty.write_text(json.dumps({"id": "X", "model": "m", "cost_usd": 0.0, "content": ""}) + "\n",
                     encoding="utf-8")
    with pytest.raises(ValueError):
        duel_harness.load_pair(empty, "X", "X")


def test_retro_duel_only_fires_the_judge(tmp_path: Path) -> None:
    burn = tmp_path / "burn.jsonl"
    burn.write_text(
        json.dumps({"id": "G1", "model": "qwen/qwen3.8-max-prime",
                    "cost_usd": 0.0674, "content": "qwen review"}) + "\n" +
        json.dumps({"id": "G3", "model": "z-ai/glm-5.3-prime",
                    "cost_usd": 0.0264, "content": "glm review"}) + "\n",
        encoding="utf-8",
    )
    a, b = duel_harness.load_pair(burn, "G1", "G3")
    out = tmp_path / "duels.jsonl"
    lane = _FakeLane("", "", JUDGE_STRICT_A)
    duel_harness.run_duel(
        ask_id="retro-fx", task="same adversarial ask",
        a_model=a["model"], b_model=b["model"],
        a_text=a["content"], b_text=b["content"],
        a_cost=a["cost_usd"], b_cost=b["cost_usd"],
        out_path=out, keys=["k1"], caller=lane, mode="retro",
    )
    assert [m for m, _ in lane.calls] == ["fireworks/ember-1"]  # contenders never re-paid
    banked = json.loads(out.read_text(encoding="utf-8").splitlines()[0])
    assert banked["mode"] == "retro"
    assert banked["a_cost"] == 0.0674 and banked["b_cost"] == 0.0264
    assert banked["judge_cost"] == 0.0071


def test_cost_metering_prefers_usage_cost() -> None:
    assert duel_harness.cost_of("fireworks/ember-1",
                                {"prompt_tokens": 999, "completion_tokens": 999,
                                 "cost": 0.0019}) == 0.0019
    # fallback: published price math on the qwen rate card
    assert duel_harness.cost_of("qwen/qwen3.8-max-prime",
                                {"prompt_tokens": 1_000_000,
                                 "completion_tokens": 1_000_000}) == pytest.approx(18.0)


def _banked_row(out: Path, **over: dict) -> dict:
    """One ember-judged W8-shaped ledger row banked via run_duel, then tweaked."""
    lane = _FakeLane("", "", JUDGE_STRICT_A)
    row = duel_harness.run_duel(
        ask_id="w8-fx", task="review", a_model="z-ai/glm-5.3-prime",
        b_model="x-ai/grok-4.3", a_text="logical A text", b_text="logical B text",
        a_cost=0.0, b_cost=0.029, out_path=out, keys=["k1"], caller=lane,
        mode="multifamily", swap=False,
    )
    row.update(over)
    return row


def test_run_rejudge_replays_identical_prompt_with_alternate_judge(tmp_path: Path) -> None:
    out = tmp_path / "duels.jsonl"
    orig = _banked_row(out)
    # fake alternate judge lane that ONLY knows the glm judge model
    glm_judge = _FakeLane("", "", JUDGE_STRICT_B)
    glm_judge.canned = {"z-ai/glm-5.3-prime": _resp(JUDGE_STRICT_B, cost=0.0310)}
    row = duel_harness.run_rejudge(orig, "review", "logical A text",
                                   "logical B text", "z-ai/glm-5.3-prime",
                                   out_path=out, keys=["k1"], caller=glm_judge)
    # exactly one call fired: the alternate judge; contenders never re-paid
    assert [m for m, _ in glm_judge.calls] == ["z-ai/glm-5.3-prime"]
    # altjudge row contract: pairs back to the original, keeps its costs
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert row["mode"] == "altjudge" and row["rejudge_of"] == "w8-fx"
    assert row["ask_id"] == "w8-fx|rejudge-glm-5.3-prime"
    assert row["a_cost"] == orig["a_cost"] and row["b_cost"] == orig["b_cost"]
    assert row["judge_cost"] == 0.0310
    assert row["a_model"] == orig["a_model"] and row["b_model"] == orig["b_model"]
    # same slot layout: original ran unswapped, judge saw A then B in order
    jp = glm_judge.calls[0][1]
    assert "logical A text" in jp.split("ANSWER_A")[1].split("ANSWER_B")[0]
    # swapped original: slot A must hold logical B's text, verdict remapped
    orig_swapped = _banked_row(out, swap=True)
    lane2 = _FakeLane("", "", JUDGE_STRICT_A)
    lane2.canned = {"z-ai/glm-5.3-prime": _resp(JUDGE_STRICT_A, cost=0.01)}
    row2 = duel_harness.run_rejudge(orig_swapped, "review", "logical A text",
                                    "logical B text", "z-ai/glm-5.3-prime",
                                    out_path=out, keys=["k1"], caller=lane2)
    jp2 = lane2.calls[0][1]
    assert "logical B text" in jp2.split("ANSWER_A")[1].split("ANSWER_B")[0]
    assert row2["swap"] is True and row2["winner"] == "B"  # slot A vote -> logical B


def test_run_rejudge_refuses_answer_drift_and_missing_rubric(tmp_path: Path) -> None:
    out = tmp_path / "duels.jsonl"
    orig = _banked_row(out)
    lane = _FakeLane("", "", JUDGE_STRICT_A)
    with pytest.raises(ValueError, match="answer drift"):
        duel_harness.run_rejudge(orig, "review", "tampered A text",
                                 "logical B text", "z-ai/glm-5.3-prime",
                                 out_path=out, keys=["k1"], caller=lane)
    with pytest.raises(ValueError, match="no rubric"):
        duel_harness.run_rejudge(dict(orig, rubric=[]), "review",
                                 "logical A text", "logical B text",
                                 "z-ai/glm-5.3-prime",
                                 out_path=out, keys=["k1"], caller=lane)
    # nothing banked by the refused replays
    assert len(out.read_text(encoding="utf-8").splitlines()) == 1
    assert lane.calls == []
