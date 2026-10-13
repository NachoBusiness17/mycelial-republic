"""B2-327: the research-lane transport precheck (wall classifier + journal)."""
import json

import tools.transport_precheck as tp


def _stub(status, body="", err=None):
    def fetch(url, timeout):
        if err:
            raise err
        return "GET", status, body
    return fetch


def test_403_classifies_bot_wall(tmp_path):
    row = tp.precheck("https://x.example/a", journal=tmp_path / "j.jsonl",
                      fetch=_stub(403))
    assert row["class"] == "bot-wall"
    assert row["status"] == 403


def test_404_classifies_dead(tmp_path):
    row = tp.precheck("https://x.example/b", journal=tmp_path / "j.jsonl",
                      fetch=_stub(404))
    assert row["class"] == "dead"


def test_200_with_interstitial_marker_classifies_interstitial(tmp_path):
    row = tp.precheck("https://x.example/c", journal=tmp_path / "j.jsonl",
                      fetch=_stub(200, "<html>Just a moment...</html>"))
    assert row["class"] == "interstitial"


def test_200_clean_classifies_ok(tmp_path):
    row = tp.precheck("https://x.example/d", journal=tmp_path / "j.jsonl",
                      fetch=_stub(200, "<html>recipe body</html>"))
    assert row["class"] == "ok"


def test_transport_failure_classifies_unreachable(tmp_path):
    import urllib.error
    row = tp.precheck("https://x.example/e", journal=tmp_path / "j.jsonl",
                      fetch=_stub(0, err=urllib.error.URLError("getaddrinfo failed")))
    assert row["class"] == "unreachable"
    assert "getaddrinfo" in row["error"]


def test_journal_row_is_appended(tmp_path):
    j = tmp_path / "j.jsonl"
    tp.precheck("https://x.example/f", journal=j, fetch=_stub(403))
    rows = [json.loads(l) for l in j.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["url"] == "https://x.example/f"
    assert rows[0]["class"] == "bot-wall"
    assert {"ts", "url", "method", "status", "class", "latency_ms", "error"} <= set(rows[0])
