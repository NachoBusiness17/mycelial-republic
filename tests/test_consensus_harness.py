"""tests for tools/consensus_harness.py (GB perimeter A2, 2026-10-10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import consensus_harness as ch  # noqa: E402


def test_norm_collapses_and_lowercases():
    assert ch.norm("  Memory. ") == "memory"
    assert ch.norm("It's  FINE!!") == "it s fine"
    assert ch.norm("") == ""


def test_modal_consensus_majority():
    assert ch.modal_consensus(["a", "a", "b"]) == ("a", 2)
    assert ch.modal_consensus(["a", "b", "c"]) == (None, 1)
    assert ch.modal_consensus(["x", "x", "x", "y"]) == ("x", 3)


def test_dead_salmon_null_computed_not_guessed():
    # K=3 models, uniform answers over 3 values, majority=2-of-3: the null is
    # 1 - P(all different) = 21/27 ~ 0.778. At small K a 2-of-3 majority is
    # cheap even for noise - the lesson this control taught (2026-10-10):
    # consensus claims need K>=5 or a rich answer space to be testable.
    matrix = [["a", "b", "c"] for _ in range(3)]
    null = ch.dead_salmon(matrix)
    assert 0.7 < null < 0.85


def test_dead_salmon_binary_space_saturates():
    # Each model 2/3 'a' + 1/3 'b', K=3: with two answer values any three
    # draws contain a 2-majority, so the null is exactly 1.0. A binary answer
    # space cannot demonstrate consensus at K=3 - distribution, not structure.
    aligned = [["a", "a", "b"], ["a", "a", "b"], ["a", "a", "b"]]
    assert ch.dead_salmon(aligned) == 1.0


def test_dead_salmon_disjoint_constants_null_zero():
    # Three constant models with disjoint answers never pair up: null 0.0.
    matrix = [["a", "a", "a"], ["b", "b", "b"], ["c", "c", "c"]]
    assert ch.dead_salmon(matrix) == 0.0


def test_dead_salmon_is_deterministic():
    m = [["a", "b"], ["a", "b"], ["b", "a"]]
    assert ch.dead_salmon(m) == ch.dead_salmon([list(r) for r in m])


def test_check_host_allows_lan_loopback_tailnet():
    assert ch.check_host("http://localhost:11434")
    assert ch.check_host("http://127.0.0.1:11434/")
    assert ch.check_host("http://192.168.1.20:11434")
    assert ch.check_host("http://100.101.5.7:11434")  # tailscale CGNAT


def test_check_host_refuses_public_and_metadata(monkeypatch):
    import socket

    ips = {"evil.example": "93.184.216.34", "meta.example": "169.254.169.254"}

    def fake_resolve(host, *a, **k):
        # build the addrinfo tuple directly; calling the real getaddrinfo here
        # would recurse into this same patched function
        return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (ips[host], 0))]

    monkeypatch.setattr(ch.socket, "getaddrinfo", fake_resolve)
    for bad in ("http://evil.example", "http://meta.example"):
        try:
            ch.check_host(bad)
        except ValueError:
            continue
        raise AssertionError("host should have been refused: " + bad)


def test_check_host_refuses_bare_and_userinfo():
    for bad in ("localhost:11434", "ftp://x", "http://u:p@10.0.0.5", "http://10.0.0.5/x"):
        try:
            ch.check_host(bad)
        except ValueError:
            continue
        raise AssertionError("should refuse: " + bad)
