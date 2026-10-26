"""Pins the 2026-10-10 pricing_diff re-cuts (locksmith cycle receipt_20261010).

The organ went 13 days with a silently broken anthropic extractor (page moved
to a two-row header) and a brittle huggingface zero-word sentinel, both because
nothing nightly runs it. These tests hold the new shapes so the next upstream
drift is a local test failure, not silent rust.
Receipt: watch/inbox/mates_leave_protocol/receipts/receipt_20261010_locksmith.md
"""
import pytest

from tools import pricing_diff as pd

# Observed live 2026-10-10: colgroup header row + sub-header row; cached price
# lives in "Hits and refreshes" (index 5), base input in "Input" (index 1).
TWO_ROW = """<table>
<tr><th>Model</th><th colspan="2">Base tokens</th><th colspan="3">Prompt caching</th></tr>
<tr><th>Name</th><th>Input</th><th>Output</th><th>5m writes</th><th>1h writes</th><th>Hits and refreshes</th></tr>
<tr><td>Claude Fable 5.1 For demanding reasoning</td><td>$10 / MTok</td><td>$50 / MTok</td><td>$12.50 / MTok</td><td>$20 / MTok</td><td>$0.25 / MTok</td></tr>
<tr><td>Claude Old 1.0 (limited availability)</td><td>$2 / MTok</td><td>$10 / MTok</td><td>$2.50 / MTok</td><td>$4 / MTok</td><td>$0.10 / MTok</td></tr>
</table>"""

# Pre-2026-10 shape: one header row carrying "Cache hits and refreshes".
LEGACY = """<table>
<tr><th>Model</th><th>Base input tokens</th><th>5m cache write</th><th>1h cache write</th><th>Cache hits and refreshes</th><th>Output tokens</th></tr>
<tr><td>Claude Opus 4.8</td><td>$10 / MTok</td><td>$12.50 / MTok</td><td>$20 / MTok</td><td>$0.25 / MTok</td><td>$50 / MTok</td></tr>
</table>"""


def test_anthropic_two_row_header(monkeypatch):
    monkeypatch.setattr(pd, "safe_get", lambda url: TWO_ROW)
    row = pd.ex_anthropic()
    assert row["model"].startswith("Claude Fable 5.1")
    assert row["cached"] == 0.25
    assert row["compute"] == 10.0


RETIRED_FIRST = """<table>
<tr><th>Model</th><th colspan="2">Base tokens</th><th colspan="3">Prompt caching</th></tr>
<tr><th>Name</th><th>Input</th><th>Output</th><th>5m writes</th><th>1h writes</th><th>Hits and refreshes</th></tr>
<tr><td>Claude Old 1.0 (limited availability)</td><td>$2 / MTok</td><td>$10 / MTok</td><td>$2.50 / MTok</td><td>$4 / MTok</td><td>$0.10 / MTok</td></tr>
<tr><td>Claude Fable 5.1 For demanding reasoning</td><td>$10 / MTok</td><td>$50 / MTok</td><td>$12.50 / MTok</td><td>$20 / MTok</td><td>$0.25 / MTok</td></tr>
</table>"""


def test_anthropic_two_row_header_skips_retired_first(monkeypatch):
    monkeypatch.setattr(pd, "safe_get", lambda url: RETIRED_FIRST)
    row = pd.ex_anthropic()
    assert row["model"].startswith("Claude Fable 5.1")
    assert row["cached"] == 0.25


def test_anthropic_legacy_single_row_header(monkeypatch):
    monkeypatch.setattr(pd, "safe_get", lambda url: LEGACY)
    row = pd.ex_anthropic()
    assert row["model"] == "Claude Opus 4.8"
    assert row["cached"] == 0.25
    assert row["compute"] == 10.0


def test_huggingface_prose_cache_mention_is_excluded(monkeypatch):
    body = "<html><body><p>usage reports include cached input token counts.</p></body></html>"
    monkeypatch.setattr(pd, "safe_get", lambda url: body)
    out = pd.check_huggingface()
    assert "excluded" in out


def test_huggingface_cache_price_shape_raises(monkeypatch):
    body = "<html><body><p>cache read $0.10 per 1M tokens</p></body></html>"
    monkeypatch.setattr(pd, "safe_get", lambda url: body)
    with pytest.raises(ValueError):
        pd.check_huggingface()
