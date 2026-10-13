"""Tests for the zknot self-steal meter alarm (lane d05-meter-alarm, dogfood-100m-20261006).

The disease: the meter was computed week-over-week in tools/zknot.py with no
consumer - the 2026-10-06 memory/zknot/LATEST.md line 3 read last 7d 126 vs
prior 7d 108 (a worsening toward the dive baseline ~148, target <75) and
nothing alerted. These pins hold the cure: meter_alarm_verdict fires on the
126->148-shaped drift and on the live banked worsening shape, stays quiet on
improvement, and meter_alarm_step appends one deduped alert row to
memory/attention.md (gate_age_patrol.py convention), never blocking the run.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import zknot  # noqa: E402

BANKED = {"last": 126, "prior": 108, "baseline": 148, "target": 75}  # LATEST.md line 3, 2026-10-06


def _nums(last: int, prior: int) -> dict:
    return {**BANKED, "last": last, "prior": prior}


def test_alarm_fires_on_126_to_148_drift():
    """The ask's named shape: the banked 126 reading drifts up to the dive
    baseline 148 - both the worsening leg and the baseline leg must fire."""
    m = _nums(last=148, prior=126)
    v = zknot.meter_alarm_verdict(m)
    assert v["fire"] is True
    joined = "; ".join(v["legs"])
    assert "WORSENED week-over-week" in joined, "148 > 126 must trip the worsening leg"
    assert "AT-OR-ABOVE dive baseline" in joined, "148 >= 148 must trip the baseline leg"


def test_alarm_fires_on_current_banked_numbers():
    """The live disease shape from LATEST.md line 3 (126 vs prior 108): the
    meter worsened below the baseline and still must alert (worsening leg)."""
    m = dict(BANKED)
    v = zknot.meter_alarm_verdict(m)
    assert v["fire"] is True
    joined = "; ".join(v["legs"])
    assert "WORSENED week-over-week" in joined, "126 > 108 is the worsening the alarm exists for"
    assert "AT-OR-ABOVE" not in joined, "126 is below the 148 baseline; only the worsening leg fires"


def test_alarm_quiet_on_improvement():
    v = zknot.meter_alarm_verdict(_nums(last=90, prior=126))
    assert v["fire"] is False and v["legs"] == [], "an improving meter below baseline is not an alarm"
    assert zknot.meter_alarm_verdict(_nums(last=100, prior=100))["fire"] is False, (
        "flat below baseline is quiet too")


def test_baseline_leg_fires_when_flat_above_baseline():
    v = zknot.meter_alarm_verdict(_nums(last=150, prior=150))
    assert v["fire"] is True
    joined = "; ".join(v["legs"])
    assert "AT-OR-ABOVE dive baseline" in joined, "sitting at/above ~148 alarms even without worsening"
    assert "WORSENED" not in joined, "flat week-over-week must not claim the worsening leg"


def test_meter_nums_rate_math_and_constants():
    """meter_nums keeps the meter math: per-1000 rate over non-template human
    prompts, and the line still carries the banked baseline/target literals."""
    wk = 7 * 86400 * 1000
    now_ms = 1_800_000_000_000
    prompts = {"s": [
        {"t": now_ms - 1000, "text": "self steal the rib again"},
        {"t": now_ms - 2000, "text": "i forgot where the law lived"},
        *[{"t": now_ms - 3000 - i, "text": f"plain ask {i}"} for i in range(8)],
        *[{"t": now_ms - wk - 1000 - i, "text": f"old plain ask {i}"} for i in range(5)],
    ]}
    m = zknot.meter_nums(prompts, set(), now_ms)
    assert (m["last"], m["prior"]) == (200, 0), "2 of 10 = 200 per 1000; 0 of 5 = 0"
    assert m["baseline"] == 148 and m["target"] == 75, "constants are single-source"
    line = zknot.meter_line(m)
    assert line == ("METER self-steal+forgot per 1000 human prompts: last 7d 200 "
                    "(1 self-steal + 1 forgot of 10) vs prior 7d 0 (0 + 0 of 5); "
                    "dive baseline ~148, target <75"), "meter line shape is byte-stable"
    assert zknot.meter_alarm_verdict(m)["fire"] is True


def test_alert_block_carves_verdict_and_key_without_em_dashes():
    now = dt.datetime(2026, 10, 6, 12, 0, 0, tzinfo=zknot.ET)
    v = zknot.meter_alarm_verdict(dict(BANKED))
    block, key = zknot.meter_alert_block(dict(BANKED), v, now)
    assert "### zknot self-steal meter alarm fired (2026-10-06 12:00:00 ET)" in block
    assert "METER-ALARM: WORSENED week-over-week (last 7d 126 vs prior 7d 108)" in block
    assert "target <75" in block
    assert key == "- key: meter-alarm last7d-126 prior7d-108 2026-10-06"
    assert key in block
    for ch in ("\u2014", "\u2013"):
        assert ch not in block, "no em/en-dash law holds in the alert row"


def test_meter_alarm_step_appends_dedups_and_dry_run_writes_nothing(tmp_path):
    att = tmp_path / "attention.md"
    att.write_text("seed\n", encoding="utf-8")
    fired = zknot.meter_alarm_step(dict(BANKED), attention_path=att,
                                   now=dt.datetime(2026, 10, 6, 12, 0, 0, tzinfo=zknot.ET))
    assert fired["fire"] is True and fired["appended"] is True
    body = att.read_text(encoding="utf-8")
    assert "METER-ALARM" in body and "- key: meter-alarm last7d-126 prior7d-108 2026-10-06" in body
    again = zknot.meter_alarm_step(dict(BANKED), attention_path=att,
                                   now=dt.datetime(2026, 10, 6, 13, 0, 0, tzinfo=zknot.ET))
    assert again["appended"] is False, "same numbers same day dedup on the key line"
    drifted = zknot.meter_alarm_step(_nums(last=148, prior=126), attention_path=att,
                                     now=dt.datetime(2026, 10, 6, 14, 0, 0, tzinfo=zknot.ET))
    assert drifted["appended"] is True, "a changed meter shape appends a fresh row"
    quiet = zknot.meter_alarm_step(_nums(last=90, prior=126), attention_path=att,
                                   now=dt.datetime(2026, 10, 6, 15, 0, 0, tzinfo=zknot.ET))
    assert quiet["fire"] is False and quiet["appended"] is False
    dry = zknot.meter_alarm_step(_nums(last=200, prior=100), attention_path=att, write=False,
                                 now=dt.datetime(2026, 10, 6, 16, 0, 0, tzinfo=zknot.ET))
    assert dry["fire"] is True and dry.get("dry_run") is True, "dry-run evaluates, writes nothing"
    assert att.read_text(encoding="utf-8").count("### zknot self-steal meter alarm fired") == 2
