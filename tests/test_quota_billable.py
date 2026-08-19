"""Mag period cap stays; the check must count billable tokens, not cache hits."""
from __future__ import annotations

import json
from datetime import datetime, timezone


def test_row_billable_ignores_cache_hits():
    from models.quota import _row_billable_tokens

    assert _row_billable_tokens({
        "prompt_tokens": 10000,
        "completion_tokens": 100,
        "cache_hit_tokens": 9000,
        "cache_miss_tokens": 1000,
        "tokens": 1100,
    }) == 1100
    assert _row_billable_tokens({
        "prompt_tokens": 400,
        "completion_tokens": 50,
        "tokens": 450,
    }) == 450


def test_provider_budget_uses_billable_not_inflated_ledger(tmp_path, monkeypatch):
    from models import quota

    usage = tmp_path / "provider_usage.jsonl"
    rows = [
        {
            "ts": "2026-08-16T10:00:00+00:00",
            "provider": "deepseek",
            "prompt_tokens": 10000,
            "completion_tokens": 100,
            "cache_hit_tokens": 9000,
            "cache_miss_tokens": 1000,
            "tokens": 1100,
            "calls": 1,
            "ok": True,
        },
        {
            "ts": "2026-08-16T11:00:00+00:00",
            "provider": "deepseek",
            "prompt_tokens": 5000,
            "completion_tokens": 50,
            "cache_hit_tokens": 4800,
            "cache_miss_tokens": 200,
            "tokens": 250,
            "calls": 1,
            "ok": True,
        },
    ]
    usage.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    state = tmp_path / "quota_state.json"
    state.write_text(json.dumps({
        "providers": {
            "deepseek": {
                "calls": 2,
                "tokens": 1_001_857,
                "period_start": "2026-08-16T00:00:00+00:00",
            }
        }
    }), encoding="utf-8")
    monkeypatch.setattr(quota, "USAGE_DETAIL", usage)
    monkeypatch.setattr(quota, "STATE_PATH", state)
    quota._BILLABLE_CACHE.clear()
    monkeypatch.setattr(
        quota, "_now",
        lambda: datetime(2026, 8, 16, 22, 0, tzinfo=timezone.utc),
    )

    b = quota.provider_budget("deepseek")
    assert b["usage_source"] == "usage_billable"
    assert b["used_tokens"] == 1350
    assert b["ledger_tokens"] == 1_001_857
    assert b["max_tokens"] == 1_000_000
    assert b["budget_ok"] is True


def test_provider_budget_trips_when_billable_hits_cap(tmp_path, monkeypatch):
    from models import quota

    usage = tmp_path / "provider_usage.jsonl"
    usage.write_text(json.dumps({
        "ts": "2026-08-16T10:00:00+00:00",
        "provider": "deepseek",
        "cache_hit_tokens": 0,
        "cache_miss_tokens": 1_000_001,
        "completion_tokens": 0,
        "tokens": 1_000_001,
        "calls": 1,
        "ok": True,
    }) + "\n", encoding="utf-8")
    state = tmp_path / "quota_state.json"
    state.write_text(json.dumps({
        "providers": {"deepseek": {"calls": 1, "tokens": 1_000_001}}
    }), encoding="utf-8")
    monkeypatch.setattr(quota, "USAGE_DETAIL", usage)
    monkeypatch.setattr(quota, "STATE_PATH", state)
    quota._BILLABLE_CACHE.clear()
    monkeypatch.setattr(
        quota, "_now",
        lambda: datetime(2026, 8, 16, 22, 0, tzinfo=timezone.utc),
    )

    b = quota.provider_budget("deepseek")
    assert b["used_tokens"] == 1_000_001
    assert b["budget_ok"] is False
    assert b["remaining_tokens"] == 0
