from __future__ import annotations

from datetime import datetime, timezone

from mag.cost_truth import aggregate_rows, price_tokens


def test_price_uses_cache_miss_plus_output_at_joined_rate():
    # Sunday is unambiguously off-peak in the current DeepSeek schedule.
    priced = price_tokens(
        "deepseek",
        "deepseek-v4-flash",
        cache_hit_tokens=1_000,
        cache_miss_tokens=2_000,
        completion_tokens=500,
        at=datetime(2026, 8, 30, 12, tzinfo=timezone.utc),
    )
    assert priced["state"] == "exact_rate"
    assert priced["billable_tokens"] == 2_500
    assert priced["calculated_usd"] == 0.000777


def test_missing_split_falls_back_to_prompt_as_cold_input():
    result = aggregate_rows([
        {
            "ts": "2026-08-30T12:00:00+00:00",
            "provider": "deepseek",
            "model": "deepseek-chat",
            "prompt_tokens": 1_000,
            "completion_tokens": 500,
        }
    ])
    assert result["cache_hit_tokens"] == 0
    assert result["cache_miss_tokens"] == 1_000
    assert result["billable_tokens"] == 1_500
    assert result["split_coverage"] == 0.0
    assert result["calculated_api_cost_usd"] == 0.00055


def test_unknown_provider_stays_visible_as_unpriced():
    result = aggregate_rows([
        {
            "ts": "2026-08-30T12:00:00+00:00",
            "provider": "openrouter",
            "model": "openrouter/auto",
            "prompt_tokens": 1_000,
            "completion_tokens": 100,
        }
    ])
    assert result["unpriced_calls"] == 1
    assert result["unpriced_billable_tokens"] == 1_100
    assert result["calculated_api_cost_usd"] == 0.0

