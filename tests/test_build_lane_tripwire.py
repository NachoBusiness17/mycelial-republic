"""Pins for the B2-188 across-runs transport tripwire in scripts/build_lane_game.py."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "build_lane_game", ROOT / "scripts" / "build_lane_game.py")
blg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blg)


def _rec(ok, error=None, model="stealth/union-alpha", ts="2026-09-26T11:38:06Z",
         detail=""):
    r = {"lane": "build-union", "model": model, "ts": ts, "ok": ok}
    if error:
        r["error"] = error
    if detail:
        r["detail"] = detail
    return r


def _setup(tmp_path, recs):
    blg.PROPOSALS = tmp_path / "proposals.jsonl"
    blg.TRIPWIRE = tmp_path / "transport_tripwire.jsonl"
    blg.PROPOSALS.write_text(
        "\n".join(json.dumps(r) for r in recs) + "\n", encoding="utf-8")


def test_alarm_fires_at_threshold_with_successor():
    with tempfile.TemporaryDirectory() as td:
        body = json.dumps({"error": {"message": "Thank you for participating. "
                                     "This model has been retired; migrate to unbiased/pareto"}})
        recs = ([_rec(True, model="unbiased/pareto", ts="2026-09-18T05:00:00Z")]
                + [_rec(False, error="HTTP 404", detail=body) for _ in range(8)])
        _setup(Path(td), recs)
        state: dict = {}
        alarm = blg._transport_tripwire(state)
        assert alarm is not None
        assert alarm["streak"] == 8
        assert alarm["model"] == "stealth/union-alpha"
        assert alarm["last_success"] == "2026-09-18T05:00:00Z"
        assert alarm["successor"] == "unbiased/pareto"
        assert state["transport_404_streak"] == 8
        assert blg.TRIPWIRE.is_file()


def test_below_threshold_is_silent_but_counts():
    with tempfile.TemporaryDirectory() as td:
        recs = [_rec(False, error="HTTP 404") for _ in range(4)]
        _setup(Path(td), recs)
        state: dict = {}
        assert blg._transport_tripwire(state) is None
        assert state["transport_404_streak"] == 4


def test_dedupe_no_repeat_alarm_same_streak_and_reset_on_success():
    with tempfile.TemporaryDirectory() as td:
        recs = [_rec(False, error="HTTP 404") for _ in range(9)]
        _setup(Path(td), recs)
        state: dict = {}
        assert blg._transport_tripwire(state) is not None
        # same streak again: no new alarm
        assert blg._transport_tripwire(state) is None
        # a success lands, streak resets, then a fresh streak (new deaths,
        # newer timestamps: a different signature) re-alarms
        recs2 = [_rec(False, error="HTTP 404", ts="2026-09-27T09:00:00Z")
                 for _ in range(9)]
        _setup(Path(td), recs + [_rec(True, model="unbiased/pareto")] + recs2)
        alarm2 = blg._transport_tripwire(state)
        assert alarm2 is not None and alarm2["streak"] == 9


def test_non_404_failure_breaks_the_streak():
    with tempfile.TemporaryDirectory() as td:
        # the 500 is the NEWEST record: the 404 tail behind it is not the
        # live signature, so the streak is 0 and the tripwire stays silent
        recs = [_rec(False, error="HTTP 404") for _ in range(8)] + \
               [_rec(False, error="HTTP 500")]
        _setup(Path(td), recs)
        state: dict = {}
        alarm = blg._transport_tripwire(state)
        assert alarm is None  # newest record is not a 404: not the dead-model signature
        assert state["transport_404_streak"] == 0
