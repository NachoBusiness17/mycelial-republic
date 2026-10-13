"""longrunner_patrol ML advisory head tests (ml-moonshot-20261007).

The head is advisory by law: ML rows never append to memory/attention.md and
never change the exit code; the rule-based WMI scan stays the enforcement
surface. These tests pin the three advisory classes on fixtures built from
the labeled incidents in memory/attention.md (2026-10-07):

  storm - the FullScan 429 burst (2026-09-24): 18,489 failing marker-heavy
          events in one day vs a 50-431/day baseline
          (state/fuel/full_scan_ledger.jsonl).
  hung  - the 5h hung cycle: fleet --cycle twins age 295min vs a 10min design
          cadence (attention.md 2026-10-07T00:38:38Z row).
  dead  - the 11-day runaway: run_armC.py alive 11 days vs an hour-scale arm
          (attention.md 2026-10-07T00:30:15Z row).

The fixtures parameterize those recorded incidents (295min silence vs 10min
cadence; 11-day span vs a 1-day horizon); they do not replay the original
event bytes. The storm fixture additionally validates on the real labeled
ledger shape: marker-heavy failing bursts against sparse failing baseline.
"""
from __future__ import annotations

import json
import sys
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import tools.longrunner_patrol as lp  # noqa: E402


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def _write_ledger(path: Path, rows: list) -> Path:
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return path


def _storm_vs_baseline_ledger(path: Path) -> Path:
    """Fixture of the labeled storm shape: 12 sparse baseline days, then the
    2026-09-24 burst (5 dense marker-heavy failing hours)."""
    rows = []
    day = datetime(2026, 9, 8, tzinfo=timezone.utc)
    for d in range(12):
        base = day + timedelta(days=d)
        rows.append({"ts": _iso(base.replace(hour=14, minute=0, second=0)),
                     "lane": "groq-llama33", "brief": "[429] throttled", "ok": False})
        rows.append({"ts": _iso(base.replace(hour=14, minute=30, second=0)),
                     "lane": "groq-llama33", "brief": "[429] throttled", "ok": False})
    storm = datetime(2026, 9, 24, tzinfo=timezone.utc)
    for hour, n in ((3, 2000), (4, 2000), (5, 2000), (9, 2000), (13, 2000)):
        t0 = storm.replace(hour=hour)
        for i in range(n):
            rows.append({"ts": _iso(t0 + timedelta(seconds=1.8 * i)),
                         "lane": "groq-llama33", "brief": "[429] throttled", "ok": False})
    return _write_ledger(path, rows)


def _tick_rows(key: str, start: datetime, cadence_min: float, n: int, gaps=None):
    rows, t = [], start
    for i in range(n):
        rows.append({"ts": _iso(t), "lane": key, "brief": "cycle tick", "ok": True})
        step = gaps[i] if gaps else cadence_min
        t = t + timedelta(minutes=step)
    return rows


def _parse_args(tmp_path, ledger, **over):
    fields = {"ml": True, "ml_only": True, "ml_model": "gbm", "ml_ledger": Path(ledger),
              "ml_window_min": 60.0, "ml_storm_day": "2026-09-24", "ml_marker": "429",
              "ml_hung_mult": 25.0, "ml_dead_horizon_min": 1440.0,
              "ml_min_key_events": 3, "ml_out": tmp_path / "adv.jsonl", "ml_now": None,
              "dry": False}
    fields.update(over)
    return types.SimpleNamespace(**fields)


def test_gbm_flags_every_labeled_storm_window_and_zero_nominal(tmp_path):
    led = _storm_vs_baseline_ledger(tmp_path / "led.jsonl")
    out = lp.ml_head(_parse_args(tmp_path, led))
    storm = [r for r in out["rows"] if r.get("klass") == "storm"]
    assert len(storm) == 5, out["summary"]
    for r in storm:
        assert r["t0"].startswith("2026-09-24")
        assert r["score"] >= 0.5
    assert "storm_recall=1.000" in out["summary"]
    assert "nominal_flagged=0" in out["summary"]
    assert "cv_acc=" in out["summary"]  # 5 storm vs 24 nominal: CV runs
    assert "advisory only" in out["summary"]


def test_iforest_one_class_isolates_storm_without_labels(tmp_path):
    led = _storm_vs_baseline_ledger(tmp_path / "led.jsonl")
    out = lp.ml_head(_parse_args(tmp_path, led, ml_model="iforest"))
    storm = [r for r in out["rows"] if r.get("klass") == "storm"]
    assert len(storm) >= 4, out["summary"]
    for r in storm:
        assert r["t0"].startswith("2026-09-24")
    assert "iforest outliers" in out["summary"]


def test_hung_tail_fires_at_the_labeled_295min_vs_10min_ratio(tmp_path):
    start = datetime(2026, 10, 7, tzinfo=timezone.utc)
    rows = _tick_rows("fleet-cycle", start, 10.0, 30)
    led = _write_ledger(tmp_path / "led.jsonl", rows)
    last = start + timedelta(minutes=290)
    hit = lp.ml_head(_parse_args(tmp_path, led, ml_now=_iso(last + timedelta(minutes=295))))
    hung = [r for r in hit["rows"] if r.get("klass") == "hung"]
    assert len(hung) == 1 and hung[0]["detail"]["kind"] == "tail", hit["summary"]
    assert abs(hung[0]["detail"]["tail_min"] - 295.0) < 1.0
    miss = lp.ml_head(_parse_args(tmp_path, led, ml_now=_iso(last + timedelta(minutes=15))))
    assert not [r for r in miss["rows"] if r.get("klass") == "hung"], miss["summary"]


def test_hung_internal_fires_on_a_midseries_stall_only(tmp_path):
    start = datetime(2026, 10, 7, tzinfo=timezone.utc)
    gaps = [10.0] * 29 + [295.0] + [10.0] * 30
    rows = _tick_rows("fleet-cycle", start, 10.0, 60, gaps=gaps)
    led = _write_ledger(tmp_path / "led.jsonl", rows)
    last = rows[-1]["ts"]
    out = lp.ml_head(_parse_args(tmp_path, led, ml_now=last))
    hung = [r for r in out["rows"] if r.get("klass") == "hung"]
    assert len(hung) == 1 and hung[0]["detail"]["kind"] == "internal", out["summary"]
    assert hung[0]["detail"]["max_gap_min"] == 295.0
    uniform_rows = _tick_rows("fleet-cycle", start, 10.0, 60)
    uniform = _write_ledger(tmp_path / "led2.jsonl", uniform_rows)
    clean = lp.ml_head(_parse_args(tmp_path, uniform, ml_now=uniform_rows[-1]["ts"]))
    assert not [r for r in clean["rows"] if r.get("klass") == "hung"], clean["summary"]


def test_dead_fires_past_horizon_at_the_labeled_11day_span(tmp_path):
    start = datetime(2026, 9, 24, tzinfo=timezone.utc)
    rows = _tick_rows("run_armC", start, 60.0, 265)  # 264h span = the 11-day runaway
    led = _write_ledger(tmp_path / "led.jsonl", rows)
    out = lp.ml_head(_parse_args(tmp_path, led, ml_now=rows[-1]["ts"]))
    dead = [r for r in out["rows"] if r.get("klass") == "dead"]
    assert len(dead) == 1 and dead[0]["key"] == "run_armC", out["summary"]
    assert dead[0]["detail"]["span_min"] >= 15840
    short = _write_ledger(tmp_path / "led2.jsonl",
                          _tick_rows("run_armC", start, 60.0, 13))  # 12h, inside horizon
    clean = lp.ml_head(_parse_args(tmp_path, short, ml_now=rows[-1]["ts"]))
    assert not [r for r in clean["rows"] if r.get("klass") == "dead"], clean["summary"]


def test_ml_only_contract_exit0_advisory_file_no_attention_append(tmp_path, capsys):
    led = tmp_path / "led.jsonl"
    start = datetime(2026, 10, 7, tzinfo=timezone.utc)
    _write_ledger(led, _tick_rows("fleet-cycle", start, 10.0, 30))
    out_path = tmp_path / "adv.jsonl"
    alert = tmp_path / "attention.md"
    argv = ["longrunner_patrol", "--ml", "--ml-only", "--ml-ledger", str(led),
            "--ml-out", str(out_path),
            "--ml-now", _iso(start + timedelta(minutes=600))]
    saved_argv, saved_alert = sys.argv, lp.ALERT
    blocked = ("win32com", "win32com.client")
    saved_modules = {k: sys.modules.get(k) for k in blocked}
    try:
        sys.argv = argv
        lp.ALERT = alert
        for k in blocked:  # --ml-only must never touch the WMI rule scan path
            sys.modules[k] = None
        rc = lp.main()
    finally:
        sys.argv, lp.ALERT = saved_argv, saved_alert
        for k, v in saved_modules.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    assert rc == 0  # advisory law: --ml-only never fails a scheduled task
    assert not alert.exists()  # advisory law: attention.md untouched by ML rows
    assert "ML ADVISORY" in capsys.readouterr().out
    rows = [json.loads(line) for line in out_path.read_text(encoding="utf-8").splitlines()]
    assert rows and all(r["kind"] == "ml_advisory" for r in rows)
    assert any(r["klass"] == "hung" for r in rows)


def test_default_parse_is_rule_based_ml_off():
    args = lp._build_parser().parse_args([])
    assert args.ml is False and args.ml_only is False and args.dry is False
    assert args.ml_model == "gbm"
    assert args.ml_window_min == 60.0
    assert args.ml_storm_day == "2026-09-24"
    assert args.ml_hung_mult == 25.0
    assert args.ml_dead_horizon_min == 1440.0
    assert args.ml_ledger.name == "full_scan_ledger.jsonl"
