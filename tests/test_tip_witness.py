"""tests/test_tip_witness.py - W3 external tip witness (2026-09-30).

The chain is writer-only tamper-evident; the gist is the external checkpoint
that survives a writer rewrite. All API traffic is mocked through the
transport seam (tests never touch the network, never touch the real token):

  line format     build/parse roundtrip, garbage rejection
  compare law     MATCH / LAG / DIVERGENT-shrink / DIVERGENT-rewrite
  tip loading     happy path, bad hex, missing file (fail closed)
  gating          bare run and --publish-without---go never write
  single-gist law create when none, patch when state, adopt by description
  ratchet         publish REFUSES on DIVERGENT, no-ops on MATCH, advances on LAG
  verify exits    MATCH/LAG 0, DIVERGENT 1, cannot-verify 2, NONE 0
  secrecy         the token never appears in output (scope-403 path)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import tip_witness as tw  # noqa: E402

FAKE_TOKEN = "ghp_testtoken_do_not_print_123456"
R_A = "a" * 64
R_B = "b" * 64
R_C = "c" * 64


def tip_file(tmp_path: Path, root: str = R_A, n_leaves: int = 100) -> Path:
    p = tmp_path / "verkle_tip.json"
    p.write_text(json.dumps({
        "schema": "verkle_tip.v1", "root": root, "n_leaves": n_leaves,
        "note": "test"}), encoding="utf-8")
    return p


class FakeTransport:
    """Canned GitHub API. Records write calls; serves list/get/create/patch."""

    def __init__(self, gists: dict | None = None, gist_list: list | None = None,
                 fail_list: bool = False, fail_get: bool = False):
        self.gists = gists or {}          # gist_id -> {content, desc}
        self.gist_list = gist_list if gist_list is not None else []
        self.fail_list = fail_list
        self.fail_get = fail_get
        self.calls: list = []             # (method, url, body)
        self.next_id = 700

    # -- transport contract: (req, timeout) -> (status, body_bytes, headers)
    def __call__(self, req, timeout):
        method, url = req.method, req.full_url
        body = json.loads(req.data.decode()) if req.data else None
        self.calls.append((method, url, body))

        def reply(status, payload):
            return (status, json.dumps(payload).encode("utf-8"), {})

        if self.fail_list and "/gists" in url and method == "GET":
            raise OSError("network down (simulated)")
        if self.fail_get and method == "GET" and url.startswith(
                "https://api.github.com/gists/"):
            return reply(404, {"message": "Not Found"})
        if url.startswith("https://api.github.com/gists?"):
            return reply(200, self.gist_list)
        if url == "https://api.github.com/gists" and method == "POST":
            if body.get("public") is True:  # default-law probe
                pass
            gid = f"g{self.next_id}"
            self.next_id += 1
            content = body["files"][tw.GIST_FILENAME]["content"]
            self.gists[gid] = {"content": content,
                               "desc": body.get("description")}
            self.gist_list.append({
                "id": gid, "description": body.get("description")})
            return reply(201, {"id": gid, "html_url":
                               f"https://gist.github.com/x/{gid}"})
        if method == "GET" and url.startswith(
                "https://api.github.com/gists/"):
            gid = url.rsplit("/", 1)[-1].split("?")[0]
            g = self.gists.get(gid)
            if not g:
                return reply(404, {"message": "Not Found"})
            return reply(200, {
                "id": gid, "description": g["desc"],
                "html_url": f"https://gist.github.com/x/{gid}",
                "files": {tw.GIST_FILENAME: {"content": g["content"]}}})
        if method == "PATCH":
            gid = url.rsplit("/", 1)[-1]
            g = self.gists.get(gid)
            if not g:
                return reply(404, {"message": "Not Found"})
            g["content"] = body["files"][tw.GIST_FILENAME]["content"]
            return reply(200, {"id": gid, "html_url":
                               f"https://gist.github.com/x/{gid}"})
        return reply(404, {"message": f"unhandled {method} {url}"})


class ScopeDeniedTransport(FakeTransport):
    """The live 2026-09-30 probe: GET /gists 200, POST /gists 403."""

    def __call__(self, req, timeout):
        if req.method == "POST" and req.full_url.endswith("/gists"):
            self.calls.append((req.method, req.full_url,
                               json.loads(req.data.decode())))
            return (403, json.dumps({
                "message": "Resource not accessible by personal access token"
            }).encode("utf-8"), {})
        return super().__call__(req, timeout)


@pytest.fixture()
def env(tmp_path: Path, monkeypatch) -> Path:
    """Point tip/state at tmp_path; hand every run a fake token."""
    monkeypatch.setattr(tw, "TIP_FILE", tmp_path / "verkle_tip.json")
    monkeypatch.setattr(tw, "STATE_FILE", tmp_path / "tip_witness_state.json")
    monkeypatch.setenv("GITHUB_TOKEN", FAKE_TOKEN)
    return tmp_path


def state_file(tmp_path: Path, gist_id: str) -> Path:
    p = tmp_path / "tip_witness_state.json"
    p.write_text(json.dumps({"schema": tw.STATE_SCHEMA, "gist_id": gist_id}),
                 encoding="utf-8")
    return p


def with_gist(ft: FakeTransport, gid: str, line: str) -> None:
    ft.gists[gid] = {"content": line + "\n", "desc": tw.GIST_DESC}
    ft.gist_list.append({"id": gid, "description": tw.GIST_DESC})


def writes(ft: FakeTransport) -> list:
    return [c for c in ft.calls if c[0] in ("POST", "PATCH")]


# ── line format ─────────────────────────────────────────────────────

def test_line_roundtrip():
    line = tw.build_line(R_A, 8691, "2026-09-30T22:42:00Z")
    parsed = tw.parse_line(line)
    assert parsed == {"root": R_A, "n_leaves": 8691,
                      "ts": "2026-09-30T22:42:00Z"}


def test_parse_line_rejects_garbage():
    assert tw.parse_line("") is None
    assert tw.parse_line("hello world") is None
    assert tw.parse_line("MAG-TIP-WITNESS.v1 root=ZZZ n_leaves=5 ts=t") is None
    assert tw.parse_line(f"prefix MAG-TIP-WITNESS.v1 root={R_A} "
                         "n_leaves=5 ts=2026-01-01T00:00:00Z") is None


# ── compare law ─────────────────────────────────────────────────────

def _w(root, n):
    return {"root": root, "n_leaves": n, "ts": "2026-09-30T00:00:00Z"}


def test_compare_match():
    v, _ = tw.compare(_w(R_A, 100), {"root": R_A, "n_leaves": 100})
    assert v == "WITNESS-MATCH"


def test_compare_lag():
    v, _ = tw.compare(_w(R_A, 90), {"root": R_B, "n_leaves": 100})
    assert v == "WITNESS-LAG"


def test_compare_divergent_shrink():
    v, detail = tw.compare(_w(R_A, 100), {"root": R_B, "n_leaves": 90})
    assert v == "WITNESS-DIVERGENT" and "SHRANK" in detail


def test_compare_divergent_same_count_rewrite():
    v, detail = tw.compare(_w(R_A, 100), {"root": R_B, "n_leaves": 100})
    assert v == "WITNESS-DIVERGENT" and "rewrite" in detail


# ── tip loading (fail closed) ───────────────────────────────────────

def test_load_tip_ok(env):
    tip_file(env, R_A, 8691)
    assert tw.load_tip() == {"root": R_A, "n_leaves": 8691}


def test_load_tip_bad_root_fail_closed(env):
    tip_file(env, "nothex", 5)
    with pytest.raises(tw.WitnessError):
        tw.load_tip()


def test_load_tip_missing_file_fail_closed(env):
    with pytest.raises(tw.WitnessError):
        tw.load_tip()


# ── gating: default is dry-run, writes need --publish --go ──────────

def test_bare_run_never_writes(env, capsys):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    rc = tw.main([], transport=ft)
    out = capsys.readouterr().out
    assert rc == 0 and writes(ft) == []
    assert "DRY-RUN" in out and "--publish --go" in out
    assert f"root={R_A}" in out  # the plan shows the real line


def test_publish_without_go_never_writes(env, capsys):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    rc = tw.main(["--publish"], transport=ft)
    assert rc == 0 and writes(ft) == []
    assert "DRY-RUN" in capsys.readouterr().out


def test_no_token_cannot_verify(env, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    tip_file(env, R_A, 100)
    rc = tw.main(["--verify"], transport=FakeTransport())
    assert rc == 2


# ── single-gist law + publish paths ─────────────────────────────────

def test_publish_creates_single_gist_and_state(env, capsys):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    rc = tw.main(["--publish", "--go"], transport=ft)
    out = capsys.readouterr().out
    assert rc == 0 and len(writes(ft)) == 1
    assert writes(ft)[0][0] == "POST"
    content = writes(ft)[0][2]["files"][tw.GIST_FILENAME]["content"]
    assert tw.parse_line(content) == {"root": R_A, "n_leaves": 100,
                                      "ts": tw.parse_line(content)["ts"]}
    assert writes(ft)[0][2]["public"] is False  # secret by default
    assert "WITNESS-CREATED" in out
    state = json.loads((env / "tip_witness_state.json").read_text())
    assert state["gist_id"].startswith("g") and state["last_line"] in out


def test_publish_patches_existing_no_second_gist(env, capsys):
    tip_file(env, R_A, 200)
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_B, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--publish", "--go"], transport=ft)
    out = capsys.readouterr().out
    assert rc == 0 and "WITNESS-ADVANCED" in out
    ws = writes(ft)
    assert len(ws) == 1 and ws[0][0] == "PATCH" and "/gists/g1" in ws[0][1]
    state = json.loads((env / "tip_witness_state.json").read_text())
    assert state["gist_id"] == "g1"  # one gist, id preserved


def test_adopt_orphan_gist_by_description_when_state_lost(env):
    tip_file(env, R_A, 200)
    ft = FakeTransport()
    with_gist(ft, "g9", tw.build_line(R_B, 100, "2026-09-30T00:00:00Z"))
    # no state file on purpose
    rc = tw.main(["--publish", "--go"], transport=ft)
    assert rc == 0
    ws = writes(ft)
    assert len(ws) == 1 and ws[0][0] == "PATCH" and "/gists/g9" in ws[0][1]
    assert json.loads((env / "tip_witness_state.json").read_text())[
        "gist_id"] == "g9"


# ── the ratchet: publish refuses divergence ─────────────────────────

def test_publish_refuses_on_shrunk_chain(env, capsys):
    tip_file(env, R_A, 50)  # live SHRANK below the witnessed 100
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_B, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--publish", "--go"], transport=ft)
    out = capsys.readouterr().out
    assert rc == 1 and writes(ft) == []  # refusal: zero witness writes
    assert "PUBLISH REFUSED" in out and "WITNESS-DIVERGENT" in out


def test_publish_refuses_on_same_count_rewrite(env):
    tip_file(env, R_A, 100)  # same count, different root than witnessed
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_B, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--publish", "--go"], transport=ft)
    assert rc == 1 and writes(ft) == []


def test_publish_noop_on_match(env, capsys):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_A, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--publish", "--go"], transport=ft)
    assert rc == 0 and writes(ft) == []
    assert "no write" in capsys.readouterr().out


# ── verify exit codes ───────────────────────────────────────────────

def test_verify_match_exit0(env, capsys):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_A, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--verify"], transport=ft)
    assert rc == 0 and "WITNESS-MATCH" in capsys.readouterr().out


def test_verify_lag_exit0(env, capsys):
    tip_file(env, R_A, 120)
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_B, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--verify"], transport=ft)
    assert rc == 0 and "WITNESS-LAG" in capsys.readouterr().out


def test_verify_divergent_exit1_alarm(env, capsys):
    tip_file(env, R_A, 80)
    ft = FakeTransport()
    with_gist(ft, "g1", tw.build_line(R_B, 100, "2026-09-30T00:00:00Z"))
    state_file(env, "g1")
    rc = tw.main(["--verify"], transport=ft)
    out = capsys.readouterr().out
    assert rc == 1 and "WITNESS-DIVERGENT" in out and "LAUNDERING" in out


def test_verify_none_exit0_when_no_gist(env, capsys):
    tip_file(env, R_A, 100)
    rc = tw.main(["--verify"], transport=FakeTransport())
    assert rc == 0 and "WITNESS-NONE" in capsys.readouterr().out


def test_verify_network_failure_exit2(env):
    tip_file(env, R_A, 100)
    rc = tw.main(["--verify"], transport=FakeTransport(fail_list=True))
    assert rc == 2


def test_verify_gist_gone_exit2(env):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    state_file(env, "g404")
    rc = tw.main(["--verify"], transport=ft)
    assert rc == 2


def test_verify_unparseable_witness_line_exit2(env):
    tip_file(env, R_A, 100)
    ft = FakeTransport()
    with_gist(ft, "g1", "someone hand-edited this gist")
    state_file(env, "g1")
    rc = tw.main(["--verify"], transport=ft)
    assert rc == 2


# ── secrecy: the token never leaks, even on the scope-403 path ──────

def test_token_never_printed_on_scope_denial(env, capsys):
    tip_file(env, R_A, 100)
    ft = ScopeDeniedTransport()
    rc = tw.main(["--publish", "--go"], transport=ft)
    captured = capsys.readouterr()
    assert rc == 2
    assert FAKE_TOKEN not in captured.out and FAKE_TOKEN not in captured.err
    assert "SCOPE" in captured.err


def test_scope_denial_names_the_fix(env, capsys):
    tip_file(env, R_A, 100)
    rc = tw.main(["--publish", "--go"], transport=ScopeDeniedTransport())
    err = capsys.readouterr().err
    assert rc == 2 and "Gists: Read and write" in err
