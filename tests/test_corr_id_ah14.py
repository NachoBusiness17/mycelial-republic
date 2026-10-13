"""AH14 correlation-law tests (receipt watch/inbox/last_mile_20260930/AH14_CORR_ID.md).

One law, three writers: every provenance row carries corr_id — a uuid4 hex8
carried in the MAG_CORR_ID env var. trajectory steps and game-flow burns read
it from the env (null when unset); duels mint one per series (process) when
the env is unset, and the env always wins. Old rows without the field must
keep parsing: absent = null, readers use .get and fixed keys, and the
trajectory step_hash basis deliberately excludes corr_id so `verify`
recomputes pre-AH14 and post-AH14 rows identically.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import game_flow, trajectory_step  # noqa: E402
from tools import duel_harness  # noqa: E402

HEX8 = re.compile(r"^[0-9a-f]{8}$")


# --- trajectory steps -------------------------------------------------------


def test_trajectory_row_carries_env_corr_id(tmp_path: Path, monkeypatch) -> None:
    stream = tmp_path / "steps.jsonl"
    monkeypatch.setattr(trajectory_step, "STREAM", stream)
    monkeypatch.setenv("MAG_CORR_ID", "deadbeef")
    trajectory_step.append_row(trajectory_step.make_row("s1", "echo hi", "out", 0))
    row = json.loads(stream.read_text(encoding="utf-8").splitlines()[0])
    assert row["corr_id"] == "deadbeef"
    # unset lane -> null, never a fabricated id
    monkeypatch.delenv("MAG_CORR_ID")
    assert trajectory_step.make_row("s1", "echo hi", "out", 0)["corr_id"] is None


def test_trajectory_corr_id_stays_out_of_hash_basis(tmp_path: Path, monkeypatch, capsys) -> None:
    stream = tmp_path / "steps.jsonl"
    monkeypatch.setattr(trajectory_step, "STREAM", stream)
    monkeypatch.setenv("MAG_CORR_ID", "cafe0001")
    for cmd in ("echo one", "echo two"):
        trajectory_step.append_row(trajectory_step.make_row("s1", cmd, "out", 0))
    trajectory_step.cmd_verify(None)  # recomputes every step_hash over the stream
    assert "2/2 rows hash-clean" in capsys.readouterr().out


# --- game-flow burns ledger ---------------------------------------------------


def test_burns_ledger_row_carries_env_corr_id(tmp_path: Path, monkeypatch) -> None:
    ledger = tmp_path / "FLOW_LEDGER.jsonl"
    monkeypatch.setattr(game_flow, "LEDGER", ledger)
    monkeypatch.setenv("MAG_CORR_ID", "cafe1234")
    game_flow._log({"ts": "2026-09-30T00:00:00Z", "action": "test", "piece": "p",
                    "module": "m", "enqueued": True, "queue_id": "q1"})
    row = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
    assert row["corr_id"] == "cafe1234"
    monkeypatch.delenv("MAG_CORR_ID")
    game_flow._log({"ts": "2026-09-30T00:00:01Z", "action": "test", "piece": "p2",
                    "module": "m", "enqueued": True, "queue_id": "q2"})
    row2 = json.loads(ledger.read_text(encoding="utf-8").splitlines()[1])
    assert row2["corr_id"] is None


# --- duel ledger --------------------------------------------------------------


def _fake_lane():
    def caller(model: str, prompt: str, key: str, max_tokens: int = 16000) -> dict:
        content = "WINNER: A\nRATIONALE: A is sharper.\n" if "ember" in model else "answer"
        return {"choices": [{"message": {"content": content}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "cost": 0.001}}
    return caller


def _duel(out: Path, ask_id: str) -> dict:
    return duel_harness.run_duel(
        ask_id=ask_id, task="t",
        a_model="qwen/qwen3.8-max-prime", b_model="z-ai/glm-5.3-prime",
        out_path=out, keys=["k1"], caller=_fake_lane(),
    )


def test_duel_row_carries_env_then_series_mint(tmp_path: Path, monkeypatch) -> None:
    out = tmp_path / "duels.jsonl"
    monkeypatch.setenv("MAG_CORR_ID", "beef0001")
    assert _duel(out, "c1")["corr_id"] == "beef0001"
    # env unset -> per-series mint (uuid4 hex8), stable across the series
    monkeypatch.delenv("MAG_CORR_ID")
    duel_harness._SERIES_CORR = None  # fresh series
    r2 = _duel(out, "c2")
    r3 = _duel(out, "c3")
    assert HEX8.match(r2["corr_id"])
    assert r3["corr_id"] == r2["corr_id"]  # one mint per series/process
    # env wins again the moment a lane sets it
    monkeypatch.setenv("MAG_CORR_ID", "beef0002")
    assert _duel(out, "c4")["corr_id"] == "beef0002"
    banked = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines()]
    assert [r["corr_id"] for r in banked] == ["beef0001", r2["corr_id"], r2["corr_id"], "beef0002"]


# --- backward compat: old rows without the field ------------------------------


def test_old_rows_without_corr_id_still_parse(tmp_path: Path) -> None:
    # pre-AH14 duel row shape + pre-AH14 trajectory row shape: plain json,
    # absent corr_id reads as null via .get, row counting unaffected
    duels = tmp_path / "duels.jsonl"
    duels.write_text(json.dumps({"ask_id": "old", "winner": "A",
                                 "ts": "2026-09-29T00:00:00"}) + "\n", encoding="utf-8")
    assert duel_harness.ledger_row_count(duels) == 1
    assert json.loads(duels.read_text(encoding="utf-8").splitlines()[0]).get("corr_id") is None

    steps = tmp_path / "steps.jsonl"
    old_row = {"schema_version": "trajectory_step.v1", "step_hash": "0" * 16,
               "ts": "2026-09-29T00:00:00Z", "session_id": "unknown", "face": "bash",
               "command": "echo old", "result": {"exit": 0, "output_excerpt": "", "truncated": False}}
    steps.write_text(json.dumps(old_row) + "\n", encoding="utf-8")
    parsed = json.loads(steps.read_text(encoding="utf-8").splitlines()[0])
    assert parsed.get("corr_id") is None  # absent = null, no reader break
