"""Hollow-200 regression (a08-rails-laws r6) plus the exception-path bank
(a08-rails-laws r10).

The founding evidence pattern is memory/runs/hermes_burn/usage.jsonl line
1151: a 2026-10-03T19:25:23Z prime-judgment row banked ok:true at
content_chars:1 for $0.25 with finish_reason "length" - a hollow 200 that
read as green. Here route_chat is fed the same shape (mocked, fully
offline) and must bank an ok:false row.

Fully offline: fence, key lookup, DNS and urlopen are all patched; the bank
lands in tmp_path so the production usage.jsonl stays test-clean.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

import pytest

import mag.route_chat as rc


class _FakeResp:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture(autouse=True)
def _offline(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "USAGE", tmp_path / "usage.jsonl")
    monkeypatch.setattr(rc, "_fence",
                        lambda base_url, host: {"93.184.216.34"})
    monkeypatch.setattr(rc, "_keys_for",
                        lambda lane_cfg: [("FAKE_KEY_ENV", "sk-fake")])
    # the DNS pin reads getaddrinfo through the socket module; feed it the
    # fence-validated address so the pin cannot disagree
    monkeypatch.setattr(
        rc.socket, "getaddrinfo",
        lambda *a, **k: [(2, 1, 6, "", ("93.184.216.34", 443))])
    captured = {}

    def fake_urlopen(req, timeout=0):
        captured["url"] = req.full_url
        captured["body"] = json.loads(req.data.decode())
        payload = captured.get("raise")
        if payload is not None:
            raise payload
        return _FakeResp(json.dumps({
            "choices": [{"message": {"content": "x"},
                         "finish_reason": "length"}],
            "usage": {"prompt_tokens": 12, "completion_tokens": 16000},
        }).encode())

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    return captured


def _rows(tmp_path):
    lines = (tmp_path / "usage.jsonl").read_text(
        encoding="utf-8").splitlines()
    return [json.loads(l) for l in lines]


def test_hollow_200_banks_ok_false(tmp_path, _offline):
    # the founding pattern: content_chars 1 + finish_reason length must
    # bank ok:false, never read as green
    out = rc.route_chat("summarize the receipt", lane="deepseek",
                        model="deepseek-v4-flash",
                        goal="hollow-200 regression")
    assert out == "x"  # the stub still returns; the ledger is the point
    rows = _rows(tmp_path)
    assert len(rows) == 1
    row = rows[0]
    assert row["ok"] is False
    assert row["content_chars"] == 1
    assert row["finish_reason"] == "length"
    assert row["lane"] == "deepseek"
    assert row["model"] == "deepseek-v4-flash"
    assert row["prompt_tokens"] == 12
    assert row["completion_tokens"] == 16000


def test_exception_path_banks_error_row(tmp_path, _offline):
    # r10: a call that never parses a response (here: URLError on every
    # attempt) must still land an ok:false error row in usage
    _offline["raise"] = urllib.error.URLError("connection refused")
    with pytest.raises(RuntimeError, match="failed on all 1 key"):
        rc.route_chat("any real ask", lane="deepseek", retries=0,
                      model="deepseek-v4-flash",
                      goal="exception-bank regression")
    rows = _rows(tmp_path)
    assert len(rows) == 1
    row = rows[0]
    assert row["ok"] is False
    assert row["error"] == "RuntimeError"
    assert "failed on all 1 key" in row["detail"]
    assert row["prompt_tokens"] == 0
    assert row["completion_tokens"] == 0
