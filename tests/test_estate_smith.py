"""estate_smith tests (standing-wave build lane B3, promotion 2026-10-08).

The estate chart must read the machine through psutil and bounded file tails
only (no disk walks) and write nothing but its own ledger row and attention
alert lines. These pins cover the six-block shape on faked organs, the three
alert thresholds with their quiet boundaries, resonance delta math on a
synthetic ledger, loss from disk_smith rows, the 24h flow counter, and the
history/dry/live write semantics of main.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import tools.estate_smith as es

NOW = datetime(2026, 10, 9, 3, 0, 0, tzinfo=timezone.utc)


def _usage(free=458.1, total=1862.2):
    return SimpleNamespace(free=free * 2**30, total=total * 2**30,
                           used=(total - free) * 2**30)


def _vm(avail=39.2, total=64.0):
    return SimpleNamespace(total=total * 2**30, available=avail * 2**30,
                           percent=38.6)


def _sm(total=64.0, used=0.0):
    return SimpleNamespace(total=total * 2**30, used=used * 2**30)


def _procs():
    return [
        SimpleNamespace(pid=11, info={
            "name": "python.exe", "cpu_times": (3600.0, 0.0),
            "memory_info": SimpleNamespace(rss=2 * 2**30)}),
        SimpleNamespace(pid=12, info={
            "name": "ollama.exe", "cpu_times": None,
            "memory_info": SimpleNamespace(rss=0)}),
        SimpleNamespace(pid=13, info={
            "name": "chrome", "cpu_times": (7200.0, 0.0, 0.0, 0.0),
            "memory_info": SimpleNamespace(rss=1 * 2**30)}),
    ]


def _fake_psutil(monkeypatch):
    monkeypatch.setattr(es.psutil, "disk_usage", lambda p: _usage())
    monkeypatch.setattr(es.psutil, "virtual_memory", lambda: _vm())
    monkeypatch.setattr(es.psutil, "swap_memory", lambda: _sm())
    monkeypatch.setattr(es.psutil, "process_iter", lambda fields=None: _procs())


def _smith_ledger(tmp_path):
    """Two synthetic disk_smith rows: zcode_cache shrinks 335.33 -> 100.42."""
    path = tmp_path / "disk_smith.jsonl"
    rows = [
        {"ts": "2026-10-09T00:48:57Z", "free_gb": 167.3,
         "monsters": {"pagefile": 63.95}, "seats": {"zcode_cache": 335.33}},
        {"ts": "2026-10-09T02:16:26Z", "free_gb": 458.1,
         "monsters": {"pagefile": 63.95}, "seats": {"zcode_cache": 100.42}},
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def _events_ledger(tmp_path):
    """Two fresh rows, one stale row, one ts-less row: counter must read 2."""
    path = tmp_path / "events.jsonl"
    rows = [
        {"ts": (NOW - timedelta(hours=1)).isoformat()},
        {"ts": (NOW - timedelta(hours=23)).isoformat()},
        {"ts": (NOW - timedelta(hours=30)).isoformat()},
        {"payload": "no ts field"},
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def test_sweep_six_blocks_shape(monkeypatch, tmp_path):
    _fake_psutil(monkeypatch)
    monkeypatch.setattr(es, "DISK_SMITH", _smith_ledger(tmp_path))
    monkeypatch.setattr(es, "EVENTS", _events_ledger(tmp_path))
    monkeypatch.setattr(es, "BURN_LEDGER", tmp_path / "missing_burn.jsonl")
    ledger = tmp_path / "estate_smith.jsonl"
    prior = {"ts": (NOW - timedelta(hours=2)).isoformat().replace("+00:00", "Z"),
             "storage": {"free_gb": 400.0}}
    ledger.write_text(json.dumps(prior) + "\n", encoding="utf-8")
    monkeypatch.setattr(es, "LEDGER", ledger)

    row = es.sweep(NOW)

    assert set(row) >= {"ts", "storage", "pressure", "compute", "flow",
                        "loss", "resonance", "alerts"}
    assert row["ts"].endswith("Z")
    assert row["storage"]["free_gb"] == 458.1
    assert row["storage"]["used_pct"] == 75.4
    assert row["storage"]["pagefile_file_gb"] == 63.95
    assert row["storage"]["last_smith_free"] == 458.1
    assert row["storage"]["disk_smith_rows"] == 2
    assert row["pressure"]["ram_avail_gb"] == 39.2
    assert row["pressure"]["pagefile_alloc_gb"] == 64.0
    assert row["compute"]["buckets"]["python"]["procs"] == 1
    assert row["compute"]["buckets"]["python"]["cpu_hours"] == 1.0
    assert row["compute"]["buckets"]["ollama"]["cpu_hours"] == 0.0
    assert row["compute"]["top_rss_procs"][0]["name"] == "python"
    assert row["flow"]["events_24h"] == 2
    assert row["flow"]["burn_ledger_rows_24h"] is None
    assert row["loss"]["zcode_delta_gb"] == -234.91
    assert row["loss"]["window"] == "2026-10-09T00:48:57Z -> 2026-10-09T02:16:26Z"
    assert row["resonance"]["rows_before"] == 1
    assert row["resonance"]["dt_h"] == 2.0
    assert row["resonance"]["gb_filled_per_h"] == -29.05  # disk emptied, negative fill
    # pagefile file 63.95GB > 40GB cap must trip the level sensor in-row
    assert any("PAGEFILE FILE BALLOON" in a for a in row["alerts"])


def test_alerts_ram_pressure():
    fired = es.alerts({"pressure": {"ram_avail_gb": 7.9}})
    assert any("RAM PRESSURE" in a and "7.9GB" in a for a in fired)


def test_alerts_ram_boundary_at_floor_is_quiet():
    assert es.alerts({"pressure": {"ram_avail_gb": 8.0}}) == []


def test_alerts_disk_floor_and_boundary():
    assert any("DISK FLOOR" in a for a in
               es.alerts({"storage": {"free_gb": 14.9, "total_gb": 1862.2}}))
    assert es.alerts({"storage": {"free_gb": 15.0}}) == []


def test_alerts_pagefile_file_balloon_and_boundary():
    row = {"storage": {"pagefile_file_gb": 40.1}}
    assert any("PAGEFILE FILE BALLOON" in a and "40.1GB" in a for a in es.alerts(row))
    assert es.alerts({"storage": {"pagefile_file_gb": 40.0}}) == []


def test_alerts_healthy_quiet_and_missing_organs_tolerated():
    row = {"storage": {"free_gb": 458.1, "total_gb": 1862.2, "pagefile_file_gb": None},
           "pressure": {"ram_avail_gb": 39.2}}
    assert es.alerts(row) == []


def test_resonance_delta_math_on_synthetic_two_row_ledger(tmp_path):
    ledger = tmp_path / "estate_smith.jsonl"
    first = {"ts": (NOW - timedelta(hours=8)).isoformat().replace("+00:00", "Z"),
             "storage": {"free_gb": 100.0}}
    second = {"ts": (NOW - timedelta(hours=4)).isoformat().replace("+00:00", "Z"),
              "storage": {"free_gb": 90.0}}
    ledger.write_text(json.dumps(first) + "\n" + json.dumps(second) + "\n",
                      encoding="utf-8")
    prior = es.tail_json(ledger, 1)[0]
    assert prior["ts"] == second["ts"]  # the tail reads the LATEST row
    res = es.resonance_block(NOW, {"free_gb": 80.0}, prior)
    assert res["rows_before"] == 1
    assert res["dt_h"] == 4.0
    assert res["gb_filled_per_h"] == 2.5  # 10GB filled over 4h


def test_resonance_first_row_has_no_rates():
    assert es.resonance_block(NOW, {"free_gb": 90.0}, None) == {"rows_before": 0}


def test_resonance_unparsable_prior_stays_row_count_only():
    res = es.resonance_block(NOW, {"free_gb": 90.0}, {"ts": "not-a-date"})
    assert res == {"rows_before": 1}


def test_history_flag_prints_last_rows(monkeypatch, tmp_path, capsys):
    ledger = tmp_path / "estate_smith.jsonl"
    rows = [{"ts": f"2026-10-09T0{i}:00:00Z", "storage": {"free_gb": float(i)}}
            for i in (1, 2, 3)]
    ledger.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    monkeypatch.setattr(es, "LEDGER", ledger)
    monkeypatch.setattr(sys, "argv", ["estate_smith", "--history", "2"])
    assert es.main() == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2
    assert json.loads(out[0])["ts"] == "2026-10-09T02:00:00Z"
    assert json.loads(out[1])["ts"] == "2026-10-09T03:00:00Z"


def test_history_flag_with_no_ledger(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(es, "LEDGER", tmp_path / "absent.jsonl")
    monkeypatch.setattr(sys, "argv", ["estate_smith", "--history", "5"])
    assert es.main() == 0
    assert "no ledger yet" in capsys.readouterr().out


def test_main_dry_writes_nothing(monkeypatch, tmp_path, capsys):
    _fake_psutil(monkeypatch)
    monkeypatch.setattr(es, "DISK_SMITH", tmp_path / "absent_smith.jsonl")
    monkeypatch.setattr(es, "EVENTS", tmp_path / "absent_events.jsonl")
    monkeypatch.setattr(es, "BURN_LEDGER", tmp_path / "absent_burn.jsonl")
    ledger = tmp_path / "estate_smith.jsonl"
    attention = tmp_path / "attention.md"
    monkeypatch.setattr(es, "LEDGER", ledger)
    monkeypatch.setattr(es, "ALERT", attention)
    monkeypatch.setattr(sys, "argv", ["estate_smith", "--dry"])
    assert es.main() == 0  # healthy fakes: 458.1GB free, 39.2GB avail, no smith row
    assert not ledger.exists()
    assert not attention.exists()
    assert '"storage"' in capsys.readouterr().out


def test_main_live_appends_exactly_one_row_and_exits_0(monkeypatch, tmp_path, capsys):
    _fake_psutil(monkeypatch)
    monkeypatch.setattr(es, "DISK_SMITH", tmp_path / "absent_smith.jsonl")
    monkeypatch.setattr(es, "EVENTS", tmp_path / "absent_events.jsonl")
    monkeypatch.setattr(es, "BURN_LEDGER", tmp_path / "absent_burn.jsonl")
    ledger = tmp_path / "estate_smith.jsonl"
    monkeypatch.setattr(es, "LEDGER", ledger)
    monkeypatch.setattr(es, "ALERT", tmp_path / "attention.md")
    monkeypatch.setattr(sys, "argv", ["estate_smith"])
    assert es.main() == 0
    lines = ledger.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["resonance"] == {"rows_before": 0}
    assert not (tmp_path / "attention.md").exists()
    capsys.readouterr()


def test_main_breach_appends_attention_and_exits_1(monkeypatch, tmp_path, capsys):
    _fake_psutil(monkeypatch)
    monkeypatch.setattr(es, "DISK_SMITH", _smith_ledger(tmp_path))  # pagefile 63.95
    monkeypatch.setattr(es, "EVENTS", tmp_path / "absent_events.jsonl")
    monkeypatch.setattr(es, "BURN_LEDGER", tmp_path / "absent_burn.jsonl")
    ledger = tmp_path / "estate_smith.jsonl"
    attention = tmp_path / "attention.md"
    monkeypatch.setattr(es, "LEDGER", ledger)
    monkeypatch.setattr(es, "ALERT", attention)
    monkeypatch.setattr(sys, "argv", ["estate_smith"])
    assert es.main() == 1
    text = attention.read_text(encoding="utf-8")
    assert "ESTATE_SMITH" in text
    assert "PAGEFILE FILE BALLOON" in text
    # the row still lands: one writer, one row, even on alert
    assert len(ledger.read_text(encoding="utf-8").strip().splitlines()) == 1
    capsys.readouterr()
