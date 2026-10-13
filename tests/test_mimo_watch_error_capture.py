"""mimo_watch error-row capture tests (B2-252, 2026-09-26).

The brief's falsifier: two 403s with different bodies both recorded only
"HTTP Error 403: Forbidden" because the probe kept only str(e)[:160]. The
contract now landed on the serve transport (the gateway probe was retired
mid-lane by B2-253): every row carrying an error also carries error_type, and
HTTP error rows additionally keep the status code and a bounded error_body
snippet, so two error responses with different bodies can never collapse into
one indistinguishable row. The FreeTierError body shape is the real bytes from
the B2-236 diagnostic battery (B2_236_mimo_retest_20260926.md Evidence).

B2-308 (2026-09-26): the row also carries resp_server / resp_content_type from
the response headers, so two OPAQUE bodies (no JSON, no prose discriminator)
from different servers still differ on a structured field.
"""
from __future__ import annotations

import io
import urllib.error
import urllib.request

import pytest

import tools.mimo_watch as mw

# Exact shape captured live by the B2-236 battery against the gateway 403.
FREETIER_BODY = (
    b'{"type":"error","error":{"type":"FreeTierError","message":'
    b'"OpenCode\'s free tier can only be used from within OpenCode"}}'
)
EDGE_BODY = b"<html>\r\nerror code: 1020\r\n</html>"  # Cloudflare-style edge block, no JSON


def _http_error(body: bytes, code: int = 403, headers=None) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "http://127.0.0.1:4096/session", code, "Forbidden", headers, io.BytesIO(body)
    )


def _probe_with(monkeypatch, exc: Exception) -> dict:
    """Raise exc on the first urlopen (the /session create call)."""
    return _probe_scripted(monkeypatch, [exc])


def _probe_scripted(monkeypatch, outcomes: list) -> dict:
    """Drive both phases: outcomes[i] is raised if an Exception, else returned
    from the i-th urlopen call (create, then message)."""
    calls = []

    def fake_urlopen(req, timeout=0):
        i = min(len(calls), len(outcomes) - 1)
        calls.append(i)
        out = outcomes[i]
        if isinstance(out, Exception):
            raise out
        return io.BytesIO(out)

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    return mw._serve_probe()


def test_http_error_row_records_status_type_body(monkeypatch):
    row = _probe_with(monkeypatch, _http_error(FREETIER_BODY))
    assert row["probe"] == "error"
    assert row["serve"] == "up"
    assert row["status"] == 403
    assert row["error_type"] == "FreeTierError"
    assert "free tier" in row["error_body"]
    assert row["error"].startswith("HTTP 403: ")


def test_edge_403_body_reads_other(monkeypatch):
    row = _probe_with(monkeypatch, _http_error(EDGE_BODY))
    assert row["status"] == 403
    assert row["error_type"] == "other"
    assert "1020" in row["error_body"]


def test_two_403s_with_different_bodies_never_collapse(monkeypatch):
    """The brief's falsifier, now dead: under the old code both rows carried
    only the identical string "HTTP Error 403: Forbidden". The structured
    fields must separate them even though the status lines are identical."""
    free = _probe_with(monkeypatch, _http_error(FREETIER_BODY))
    edge = _probe_with(monkeypatch, _http_error(EDGE_BODY))
    assert free["status"] == edge["status"] == 403
    assert (free["error_type"], free["error_body"]) != (edge["error_type"], edge["error_body"])
    assert free["error_type"] == "FreeTierError"
    assert edge["error_type"] == "other"
    assert free["error_body"] != edge["error_body"]


def test_httperror_takes_the_structured_branch_not_the_generic_one(monkeypatch):
    row = _probe_with(monkeypatch, _http_error(FREETIER_BODY))
    # the generic path records error_type "other" with no status field; an
    # HTTPError falling through there would lose both
    assert "status" in row
    assert row["error_type"] == "FreeTierError"


def test_httperror_on_create_is_an_error_row_not_serve_down(monkeypatch):
    """HTTPError subclasses Exception: before the split, a daemon that answered
    and refused the session create was recorded as serve=down with no status,
    type or body. The daemon answered, so the row must classify."""
    row = _probe_with(monkeypatch, _http_error(FREETIER_BODY))
    assert row["serve"] == "up"
    assert row["probe"] == "error"
    assert row["status"] == 403
    assert row["error_type"] == "FreeTierError"


def test_httperror_on_message_takes_the_structured_branch(monkeypatch):
    row = _probe_scripted(
        monkeypatch,
        [b'{"id": "s1"}', _http_error(FREETIER_BODY)],
    )
    assert row["probe"] == "error"
    assert row["serve"] == "up"
    assert row["status"] == 403
    assert row["error_type"] == "FreeTierError"
    assert "free tier" in row["error_body"]
    assert row["error"].startswith("HTTP 403: ")


def test_message_phase_failure_records_other(monkeypatch):
    row = _probe_scripted(
        monkeypatch,
        [b'{"id": "s1"}', urllib.error.URLError("timed out")],
    )
    assert row["probe"] == "error"
    # rebased 2026-09-26 (B2-308, claim-law rebase on B2-307's landed bytes):
    # B2-307's non-http classifier parses the URLError reason, so a "timed out"
    # reason now reads error_type "timeout", not the B2-252-era "other".
    assert row["error_type"] == "timeout"
    assert "status" not in row


def test_serve_down_row_records_other(monkeypatch):
    row = _probe_with(monkeypatch, urllib.error.URLError("WinError 10061 refused"))
    assert row["serve"] == "down"
    assert row["probe"] == "skipped"
    assert row["error_type"] == "other"


@pytest.mark.parametrize(
    "raw, expected",
    [
        (FREETIER_BODY, "FreeTierError"),
        (b"", "other"),
        (b"not json at all", "other"),
        (b'{"type":"error","error":"plain string"}', "other"),
        (b'{"type":"error","error":{"message":"no type key"}}', "other"),
        (b'{"type":"error","error":{"type":123}}', "other"),
        (b'{"unrelated": true}', "other"),
        (b'{"error":{"type":"' + b"X" * 100 + b'"}}', "X" * 60),
    ],
)
def test_error_type_from_body_edges(raw: bytes, expected: str):
    assert mw._error_type_from_body(raw) == expected


def test_two_opaque_bodies_differ_by_server_header(monkeypatch):
    """The B2-308 falsifier, dead: two opaque (non-JSON) bodies with different
    Server headers used to differ only in body prose; now resp_server separates
    them as a structured field even when both error_type read "other"."""
    cloudflare = _probe_with(monkeypatch, _http_error(
        EDGE_BODY, headers={"Server": "cloudflare", "Content-Type": "text/html"}))
    nginx = _probe_with(monkeypatch, _http_error(
        b"BINARY-PAYLOAD-NOT-JSON-7f3a", headers={"Server": "nginx", "Content-Type": "application/octet-stream"}))
    assert cloudflare["error_type"] == "other"
    assert nginx["error_type"] == "other"
    assert cloudflare["resp_server"] == "cloudflare"
    assert nginx["resp_server"] == "nginx"
    assert cloudflare["resp_content_type"] == "text/html"
    assert nginx["resp_content_type"] == "application/octet-stream"
    assert cloudflare["resp_server"] != nginx["resp_server"]


def test_missing_headers_read_empty_not_crash(monkeypatch):
    row = _probe_with(monkeypatch, _http_error(FREETIER_BODY, headers=None))
    assert row["resp_server"] == ""
    assert row["resp_content_type"] == ""
    assert row["error_type"] == "FreeTierError"
