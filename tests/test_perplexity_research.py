"""Fixture tests for mag/perplexity_research.py REMAP_PATH.

Proves the post-2026-09-27 route (Perplexity Search API) is READY but NOT LIVE:
  - default route stays "chat" and refuses on/after the sunset without network;
  - route="search" (param, $SONAR_ROUTE, or CLI) posts the Search API request
    shape and normalizes the documented response, with zero live HTTP
    (transport is a fake opener fixture).
Grounding for the search request/response shape: docs.perplexity.ai
getting-started + docs/search/quickstart, fetched 2026-09-25.
"""
from __future__ import annotations

import io
import json
import urllib.error

from mag import perplexity_research as pr

BEFORE_SUNSET = "2026-09-26"
ON_SUNSET = "2026-09-27"
AFTER_SUNSET = "2026-09-28"

SEARCH_FIXTURE = {
    "id": "fix-1",
    "results": [
        {"title": "Stealable Mechanism One", "url": "https://a.example/1",
         "snippet": "S1 body", "date": "2026-09-01", "last_updated": "2026-09-20"},
        {"title": "Stealable Mechanism Two", "url": "https://b.example/2",
         "snippet": "S2 body", "date": None, "last_updated": "2026-09-21"},
    ],
    "server_time": None,
}

CHAT_FIXTURE = {
    "choices": [{"message": {"role": "assistant", "content": "cited answer"}}],
    "citations": ["https://x.example/1"],
    "usage": {"total_tokens": 42},
}


class FakeOpener:
    """Stands in for pr._OPENER; records every request, serves canned payloads."""

    def __init__(self, payload_by_url):
        self.payload_by_url = payload_by_url
        self.calls = []

    def open(self, req, timeout=None):
        self.calls.append({
            "url": req.full_url,
            "method": req.get_method(),
            "headers": {k.lower(): v for k, v in req.header_items()},
            "body": json.loads(req.data.decode("utf-8")),
            "timeout": timeout,
        })
        payload = self.payload_by_url.get(req.full_url)
        if isinstance(payload, Exception):
            raise payload
        return _FakeResp(payload)


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def _install(monkeypatch, tmp_path, payload_by_url):
    fake = FakeOpener(payload_by_url)
    monkeypatch.setattr(pr, "_OPENER", fake)
    monkeypatch.setattr(pr, "LEAF_DIR", tmp_path / "leaves")
    monkeypatch.setenv("PERPLEXITY_API_KEY", "pplx-fixture-key")
    monkeypatch.delenv("PPLX_API_KEY", raising=False)
    monkeypatch.delenv("SONAR_ROUTE", raising=False)
    return fake


def test_default_route_refuses_after_sunset_with_no_network(monkeypatch, tmp_path):
    """Ready, not live: post-sunset, the DEFAULT route must not fire at all."""
    fake = _install(monkeypatch, tmp_path, {pr.API_URL: CHAT_FIXTURE,
                                            pr.SEARCH_URL: SEARCH_FIXTURE})
    monkeypatch.setattr(pr, "_today", lambda: AFTER_SUNSET)

    r = pr.research("steal mechanisms")

    assert r["ok"] is False
    assert r["route"] == "chat"
    assert ON_SUNSET in r["error"] and pr.REMAP_PATH in r["error"]
    assert pr.SEARCH_URL in r["error"]  # the refusal names the remap path
    assert fake.calls == []  # nothing hit the wire


def test_sunset_boundary_is_inclusive(monkeypatch, tmp_path):
    _install(monkeypatch, tmp_path, {pr.API_URL: CHAT_FIXTURE})
    monkeypatch.setattr(pr, "_today", lambda: ON_SUNSET)
    r = pr.research("q")
    assert r["ok"] is False and "retired" in r["error"]

    monkeypatch.setattr(pr, "_today", lambda: BEFORE_SUNSET)
    r2 = pr.research("q")
    assert r2["ok"] is True  # pre-sunset the dormant default still works


def test_search_route_posts_search_shape_after_sunset(monkeypatch, tmp_path):
    """The remap: route='search' posts the Search API shape post-sunset."""
    fake = _install(monkeypatch, tmp_path, {pr.SEARCH_URL: SEARCH_FIXTURE})
    monkeypatch.setattr(pr, "_today", lambda: AFTER_SUNSET)

    r = pr.research("steal mechanisms", route="search")

    assert r["ok"] is True and r["route"] == "search"
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call["url"] == pr.SEARCH_URL
    assert call["method"] == "POST"
    assert call["headers"]["authorization"] == "Bearer pplx-fixture-key"
    assert call["headers"]["content-type"] == "application/json"
    body = call["body"]
    assert body["query"] == "steal mechanisms"
    assert body["max_results"] == 10  # documented default
    assert "max_tokens" in body  # carried from the legacy signature
    # the SHAPE is Search API, not chat completions:
    assert "model" not in body and "messages" not in body
    # response normalized into the module's content/citations contract:
    assert r["n_citations"] == 2
    assert r["citations"] == ["https://a.example/1", "https://b.example/2"]
    assert "[1] Stealable Mechanism One https://a.example/1" in r["content"]
    assert "S1 body" in r["content"] and "S2 body" in r["content"]
    # leaf still written, still schema-versioned, now route-tagged:
    leaves = list((tmp_path / "leaves").glob("leaf-*.json"))
    assert len(leaves) == 1
    leaf = json.loads(leaves[0].read_text(encoding="utf-8"))
    assert leaf["schema"] == pr.SCHEMA and leaf["route"] == "search"
    assert leaf["citations"] == ["https://a.example/1", "https://b.example/2"]


def test_search_route_flags_and_bounds(monkeypatch, tmp_path):
    fake = _install(monkeypatch, tmp_path, {pr.SEARCH_URL: SEARCH_FIXTURE})
    monkeypatch.setattr(pr, "_today", lambda: AFTER_SUNSET)

    r = pr.research("q", route="search", fast=True, max_results=99)
    assert r["ok"] is True
    body = fake.calls[0]["body"]
    assert body["search_type"] == "fast"  # $1/1k fast tier
    assert body["max_results"] == 20  # documented 1-20 clamp

    r2 = pr.research("q", route="search", max_results=0)
    assert r2["ok"] is True
    assert fake.calls[1]["body"]["max_results"] == 1


def test_env_flag_selects_search_route(monkeypatch, tmp_path):
    fake = _install(monkeypatch, tmp_path, {pr.SEARCH_URL: SEARCH_FIXTURE})
    monkeypatch.setenv("SONAR_ROUTE", "search")
    monkeypatch.setattr(pr, "_today", lambda: AFTER_SUNSET)

    r = pr.research("q")  # no explicit route: env flag drives the remap

    assert r["ok"] is True and r["route"] == "search"
    assert fake.calls[0]["url"] == pr.SEARCH_URL


def test_explicit_route_overrides_env(monkeypatch, tmp_path):
    _install(monkeypatch, tmp_path, {pr.API_URL: CHAT_FIXTURE,
                                     pr.SEARCH_URL: SEARCH_FIXTURE})
    monkeypatch.setenv("SONAR_ROUTE", "chat")
    monkeypatch.setattr(pr, "_today", lambda: BEFORE_SUNSET)

    r = pr.research("q", route="search")
    assert r["ok"] is True and r["route"] == "search"

    r2 = pr.research("q", route="chat")
    assert r2["ok"] is True and r2["route"] == "chat"


def test_chat_route_keeps_chat_shape_before_sunset(monkeypatch, tmp_path):
    """The dormant default must not drift pre-sunset: same URL, same body shape."""
    fake = _install(monkeypatch, tmp_path, {pr.API_URL: CHAT_FIXTURE})
    monkeypatch.setattr(pr, "_today", lambda: BEFORE_SUNSET)

    r = pr.research("steal mechanisms")  # default route

    assert r["ok"] is True and r["route"] == "chat" and r["model"] == "sonar"
    call = fake.calls[0]
    assert call["url"] == pr.API_URL  # the dying endpoint, untouched by default
    assert call["method"] == "POST"
    body = call["body"]
    assert body["model"] == "sonar"
    assert [m["role"] for m in body["messages"]] == ["system", "user"]
    assert "query" not in body and "max_results" not in body
    assert r["content"] == "cited answer" and r["n_citations"] == 1


def test_agent_route_is_an_honest_stub(monkeypatch, tmp_path):
    fake = _install(monkeypatch, tmp_path, {})
    monkeypatch.setattr(pr, "_today", lambda: AFTER_SUNSET)

    r = pr.research("q", route="agent")

    assert r["ok"] is False and r["route"] == "agent"
    assert "not pinned" in r["error"] and "search" in r["error"]
    assert fake.calls == []  # no invented shape ever hits the wire


def test_unknown_route_is_an_honest_error(monkeypatch, tmp_path):
    fake = _install(monkeypatch, tmp_path, {})
    r = pr.research("q", route="carrier-pigeon")
    assert r["ok"] is False and "unknown route" in r["error"]
    assert fake.calls == []


def test_search_route_requires_key(monkeypatch, tmp_path):
    fake = _install(monkeypatch, tmp_path, {pr.SEARCH_URL: SEARCH_FIXTURE})
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)

    r = pr.research("q", route="search")

    assert r["ok"] is False and "PERPLEXITY_API_KEY" in r["error"]
    assert fake.calls == []


def test_search_http_error_is_normalized(monkeypatch, tmp_path):
    fake = _install(monkeypatch, tmp_path, {
        pr.SEARCH_URL: urllib.error.HTTPError(
            pr.SEARCH_URL, 402, "Payment Required", {},
            io.BytesIO(b'{"error": "no quota"}')),
    })
    monkeypatch.setattr(pr, "_today", lambda: AFTER_SUNSET)

    r = pr.research("q", route="search")

    assert r["ok"] is False and r["route"] == "search"
    assert r["error"].startswith("HTTP 402")


def test_search_body_pure_shape_and_clamps():
    b = pr._search_body("  spaced  ", max_results=5, max_tokens=0, fast=False)
    assert b == {"query": "spaced", "max_results": 5}  # no zero-token key
    b2 = pr._search_body("q", max_results=-3, max_tokens=10, fast=False)
    assert b2["max_results"] == 1
    b3 = pr._search_body("q", max_results=10**6, max_tokens=None, fast=True)
    assert b3["max_results"] == 20 and b3["search_type"] == "fast"


def test_endpoint_guard_blocks_non_pinned_targets():
    assert pr.endpoint_blocked("http://api.perplexity.ai/search") is not None
    assert pr.endpoint_blocked("https://169.254.169.254/latest/meta-data") is not None
    assert pr.endpoint_blocked("https://internal.local/search") is not None
    assert pr.endpoint_blocked(pr.SEARCH_URL) is None
    assert pr.endpoint_blocked(pr.API_URL) is None


def test_status_reports_remap_fields():
    s = pr.status()
    assert s["default_route"] == "chat"
    assert s["remap_path"] == "search"
    assert s["sonar_chat_sunset"] == ON_SUNSET
    assert s["routes"]["search"] == pr.SEARCH_URL
    assert s["routes"]["agent"] is None


def test_main_cli_routes():
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = pr.main(["--route", "carrier-pigeon", "q"])
    assert rc == 0
    out = json.loads(buf.getvalue().split("=====")[0])
    assert out["ok"] is False and "unknown route" in out["error"]
