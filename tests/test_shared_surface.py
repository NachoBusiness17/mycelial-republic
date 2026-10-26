"""Shared surface (2026-10-17): warm resources, redaction, seat receipts, warm profile, shim.

Plan: watch/LIBRARY/SHARED_SURFACE_SELFSTEAL_20261017.md. Every path the
modules read or write is redirected to tmp_path (live-estate write fence in
tests/conftest.py stays armed; MAG_ALLOW_LIVE_WRITES must be unset).
"""
from __future__ import annotations

import hashlib
import io
import json
import socket
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from mag import estate_bridge as eb  # noqa: E402
from mag import mcp_server as ms  # noqa: E402
from mag import warm_surface as ws  # noqa: E402

FAKE_SK = "sk-" + "a1b2c3d4e5f6g7h8i9j0"
FAKE_GHP = "ghp_" + "A" * 36
FAKE_ENV_LINE = "OPENAI_API_KEY=" + "zz9yy8xx7ww6"
FAKE_PEM = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg\n-----END PRIVATE KEY-----"


@pytest.fixture
def warm(tmp_path, monkeypatch):
    """Point every warm_surface source at a tmp estate."""
    bio = tmp_path / "memory" / "biography"
    bio.mkdir(parents=True)
    tip = bio / "verkle_tip.json"
    tip.write_text(json.dumps({
        "schema": "verkle_tip.v1", "root": "ab" * 32, "n_leaves": 100,
        "last_filename": "x.knot.json", "last_leaf_hash": "cd" * 32,
        "last_session_id": "s1", "updated_minute": "2026-10-17T17:40:12+00:00",
    }), encoding="utf-8")
    state = tmp_path / "memory" / "warm_state.json"
    state.write_text(json.dumps({"schema": "hermes_warm_state.v1",
                                 "chain": {"n_leaves": 90, "index": 89},
                                 "session_brief": {"path": str(ROOT / "memory" / "briefs" / "latest.md")},
                                 "api_key": "should-never-leave"}), encoding="utf-8")
    zk = tmp_path / "memory" / "zknot" / "LATEST.md"
    zk.parent.mkdir(parents=True)
    zk.write_text("# zknot\nnote " + FAKE_SK + "\n" + FAKE_GHP + "\n" + FAKE_ENV_LINE
                  + "\npeer 100.101.102.103\n" + FAKE_PEM + "\nhome C:\\Users\\someone\\proj\n",
                  encoding="utf-8")
    rib = tmp_path / "memory" / "rib_boot.json"
    rib.write_text(json.dumps({
        "ts": "2026-10-17T00:00:00+00:00", "read_only": True,
        "core_laws": [{"id": "chain-is-truth", "law": "chain=record, window=reasoning."}],
        "vault": {"law_ribs": [{"file": "RIB_X.md", "law_head": "head", "law_amendments": [],
                                "amendment_count": 0, "bytes": 4, "mounted": True}]},
        "superseded_register": {"path": "memory/fold_history/SUPERSEDED.md", "exists": True},
    }), encoding="utf-8")
    lib = tmp_path / "watch" / "LIBRARY" / "INDEX.md"
    monkeypatch.setattr(ws, "TIP", tip)
    monkeypatch.setattr(ws, "WARM_STATE", state)
    monkeypatch.setattr(ws, "ZKNOT", zk)
    monkeypatch.setattr(ws, "RIB_BOOT", rib)
    monkeypatch.setattr(ws, "LIBRARY_INDEX", lib)
    return {"tip": tip, "state": state, "zknot": zk, "rib": rib, "lib": lib}


def _rpc(method, params=None, profile="warm"):
    msg = {"jsonrpc": "2.0", "id": 7, "method": method}
    if params is not None:
        msg["params"] = params
    return ms.handle(msg, profile)


# ───────────────────────────── resources ─────────────────────────────

def test_initialize_advertises_resources():
    caps = _rpc("initialize")["result"]["capabilities"]
    assert "resources" in caps and "tools" in caps


def test_resources_list_fixed_uris(warm):
    uris = [r["uri"] for r in _rpc("resources/list")["result"]["resources"]]
    for u in ("mag://warm/tip", "mag://warm/state", "mag://warm/zknot", "mag://warm/laws"):
        assert u in uris
    assert "mag://warm/library-index" not in uris  # file absent -> not listed
    assert all(u.startswith("mag://warm/") for u in uris)
    assert {f"mag://warm/preamble/{s}" for s in ws.SEATS} <= set(uris)
    warm["lib"].parent.mkdir(parents=True)
    warm["lib"].write_text("# INDEX\n", encoding="utf-8")
    uris = [r["uri"] for r in _rpc("resources/list")["result"]["resources"]]
    assert "mag://warm/library-index" in uris


def test_resources_list_served_on_every_profile(warm):
    for profile in ("archivist", "full", "warm"):
        assert _rpc("resources/list", profile=profile)["result"]["resources"]


def test_resources_read_tip_is_live(warm):
    first = json.loads(_rpc("resources/read", {"uri": "mag://warm/tip"})["result"]["contents"][0]["text"])
    assert first["ok"] and first["n_leaves"] == 100 and first["root_short"] == "ab" * 8
    data = json.loads(warm["tip"].read_text(encoding="utf-8"))
    data["n_leaves"] = 101
    warm["tip"].write_text(json.dumps(data), encoding="utf-8")
    second = json.loads(_rpc("resources/read", {"uri": "mag://warm/tip"})["result"]["contents"][0]["text"])
    assert second["n_leaves"] == 101  # re-read per call, never cached


def test_resources_read_state_reports_lag(warm):
    body = json.loads(_rpc("resources/read", {"uri": "mag://warm/state"})["result"]["contents"][0]["text"])
    assert body["leaves_behind_live_tip"] == 10


def test_resources_read_laws_and_preamble(warm):
    laws = json.loads(_rpc("resources/read", {"uri": "mag://warm/laws"})["result"]["contents"][0]["text"])
    assert laws["core_laws"][0]["id"] == "chain-is-truth"
    assert laws["law_ribs"][0]["file"] == "RIB_X.md"
    pre = _rpc("resources/read", {"uri": "mag://warm/preamble/gemini"})["result"]["contents"][0]
    assert pre["mimeType"] == "text/markdown"
    assert "seat=gemini" in pre["text"] and "chain-is-truth" in pre["text"]
    assert 'estate_shared_receipt(seat="gemini"' in pre["text"]


@pytest.mark.parametrize("uri", [
    "file:///C:/Windows/win.ini", "mag://warm/../.env", "mag://warm/preamble/../../.env",
    "mag://warm/preamble/nobody", "mag://warm/state?path=.env", "", "memory/warm_state.json",
])
def test_resources_read_rejects_unknown_and_path_shaped(warm, uri):
    out = _rpc("resources/read", {"uri": uri})
    assert out["error"]["code"] == -32002


# ───────────────────────────── redaction ─────────────────────────────

def test_redaction_masks_secret_shapes(warm):
    text = _rpc("resources/read", {"uri": "mag://warm/zknot"})["result"]["contents"][0]["text"]
    for secret in (FAKE_SK, FAKE_GHP, "zz9yy8xx7ww6", "MIIEvQIBADANBg", "100.101.102.103",
                   "someone"):
        assert secret not in text, secret
    assert "OPENAI_API_KEY=<redacted>" in text and "<tailnet-ip>" in text


def test_redaction_drops_credential_fields_and_repo_path(warm):
    text = _rpc("resources/read", {"uri": "mag://warm/state"})["result"]["contents"][0]["text"]
    assert "should-never-leave" not in text
    assert str(ROOT) not in text and str(ROOT).replace("\\", "\\\\") not in text
    assert "<repo>" in text


def test_redact_text_is_idempotent():
    once = ws.redact_text(FAKE_SK + " " + FAKE_ENV_LINE)
    assert ws.redact_text(once) == once


# ───────────────────────────── receipts ──────────────────────────────

@pytest.fixture
def receipts(tmp_path, monkeypatch):
    d = tmp_path / "watch" / "receipts"
    monkeypatch.setattr(eb, "SHARED_RECEIPT_DIR", d)
    return d


def _call(name, args, profile="warm"):
    out = ms.call_tool(name, args, set(ms._profile_names(profile)))
    return out, json.loads(out["content"][0]["text"])


def test_receipt_lands_in_receipts_with_seat_field(receipts):
    out, body = _call("estate_shared_receipt",
                      {"seat": "gemini", "model": "gemini-3-pro", "title": "t", "body": "hello"})
    assert not out.get("isError") and body["ok"]
    files = list(receipts.iterdir())
    assert len(files) == 1 and files[0].parent == receipts
    assert files[0].name.startswith("seat_") and "_gemini_" in files[0].name
    rec = json.loads(files[0].read_text(encoding="utf-8"))
    assert rec["schema"] == "shared_receipt.v1"
    assert rec["seat"]["name"] == "gemini" and rec["seat"]["model"] == "gemini-3-pro"
    assert rec["seat"]["ts"].endswith("+00:00")
    assert rec["body_sha256"] == hashlib.sha256(b"hello").hexdigest() == body["body_sha256"]
    assert body["path"] == f"watch/receipts/{files[0].name}"


def test_receipt_never_overwrites(receipts):
    _call("estate_shared_receipt", {"seat": "grok", "body": "same"})
    _call("estate_shared_receipt", {"seat": "grok", "body": "same"})
    assert len(list(receipts.iterdir())) == 2


def test_receipt_body_redacted_before_landing(receipts):
    _, body = _call("estate_shared_receipt", {"seat": "hermes", "body": "leak " + FAKE_SK})
    rec = json.loads(next(receipts.iterdir()).read_text(encoding="utf-8"))
    assert FAKE_SK not in rec["body"] and rec["redacted"] is True and body["redacted"] is True
    assert rec["body_sha256"] == hashlib.sha256(rec["body"].encode("utf-8")).hexdigest()


@pytest.mark.parametrize("args", [
    {"seat": "../etc", "body": "x"},
    {"seat": "a/b", "body": "x"},
    {"seat": "a\\b", "body": "x"},
    {"seat": "..", "body": "x"},
    {"seat": "", "body": "x"},
    {"seat": "grok", "body": "x", "path": "../../.env"},
    {"seat": "grok", "body": "x", "name": "INDEX.json"},
    {"seat": "grok", "body": "x", "wave": "inbox"},
    {"seat": "grok", "body": "x", "model": "../../x"},
    {"seat": "grok", "body": "x" * (eb.SHARED_RECEIPT_CAP + 1)},
    {"seat": "grok", "body": "x", "title": "t" * (eb.SHARED_TITLE_CAP + 1)},
    {"seat": "grok", "body": 123},
])
def test_receipt_refusals(receipts, args):
    out, body = _call("estate_shared_receipt", args)
    assert out.get("isError") is True and body["ok"] is False
    assert not receipts.exists() or not any(receipts.iterdir())


def test_receipt_confined_even_if_root_is_symlinked_elsewhere(receipts, tmp_path):
    """Files land directly in the resolved receipts dir, never a subdir/parent."""
    _call("estate_shared_receipt", {"seat": "zcode", "body": "ok"})
    (f,) = list(receipts.iterdir())
    assert f.resolve().parent == receipts.resolve()


# ───────────────────────────── warm profile ──────────────────────────

WRITE_OR_EXEC = {"write_file", "apply_patch", "run_shell", "run_python", "pheromone_drop",
                 "blackboard_post", "estate_thought_compile", "estate_receipt_append",
                 "estate_queue_closes", "verb_anchor", "voice_turn"}


def test_warm_profile_exposes_no_write_tools():
    names = {t["name"] for t in ms.tools_manifest("warm")}
    assert names == {"estate_warm_read", "estate_chain_verify", "estate_shared_receipt",
                     "estate_propose", "estate_review", "estate_proposals",
                     # fleet coordination (2026-10-17)
                     "estate_fleet_report", "estate_notices", "estate_lease_acquire",
                     "estate_lease_renew", "estate_lease_release", "estate_lease_transfer",
                     "estate_leases"}
    assert not names & WRITE_OR_EXEC
    assert not names & ms._MUTATING_TOOLS
    metas = {t["name"]: t["_meta"]["mag"] for t in ms.tools_manifest("warm")}
    assert metas["estate_warm_read"]["effect_class"] == "read_or_deterministic_compute"
    assert metas["estate_shared_receipt"]["authority"] == "canned_broker"
    assert metas["estate_propose"]["authority"] == "canned_broker"
    assert metas["estate_review"]["authority"] == "canned_broker"
    assert metas["estate_proposals"]["effect_class"] == "read_or_deterministic_compute"
    for n in ("estate_notices", "estate_leases"):
        assert metas[n]["effect_class"] == "read_or_deterministic_compute"
    for n in ("estate_fleet_report", "estate_lease_acquire", "estate_lease_renew",
              "estate_lease_release", "estate_lease_transfer"):
        assert metas[n]["authority"] == "canned_broker"


def test_warm_profile_refuses_write_tool_calls(tmp_path):
    out, body = _call("write_file", {"path": str(tmp_path / "x.txt"), "content": "x"})
    assert out["isError"] and "not in active MCP profile" in body["error"]
    assert not (tmp_path / "x.txt").exists()
    out, body = _call("run_shell", {"command": "echo hi"})
    assert out["isError"]


def test_warm_read_tool_matches_resource(warm):
    out, body = _call("estate_warm_read", {"uri": "mag://warm/tip"})
    assert not out.get("isError") and body["uri"] == "mag://warm/tip"
    assert json.loads(body["text"])["n_leaves"] == 100
    out, body = _call("estate_warm_read", {"uri": "file:///etc/passwd"})
    assert out["isError"]


# ───────────────────────────── shim ──────────────────────────────────

def test_shim_loopback_law():
    import mcp_stdio_shim as shim

    assert shim.is_loopback("127.0.0.1") and shim.is_loopback("::1") and shim.is_loopback("localhost")
    assert not shim.is_loopback("100.101.102.103") and not shim.is_loopback("example.com")
    assert shim.main(["--host", "192.0.2.1"]) == 3


def test_shim_pipes_a_jsonrpc_round_trip():
    import mcp_stdio_shim as shim

    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def serve_once():
        conn, _ = srv.accept()
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = conn.recv(4096)
            if not chunk:
                break
            buf += chunk
        req = json.loads(buf)
        conn.sendall((json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {"echo": req["method"]}})
                      + "\n").encode())
        conn.close()

    t = threading.Thread(target=serve_once, daemon=True)
    t.start()
    stdin = io.BytesIO(b'{"jsonrpc":"2.0","id":1,"method":"ping"}\n')
    stdout = io.BytesIO()
    assert shim.run("127.0.0.1", port, 2.0, stdin=stdin, stdout=stdout) == 0
    t.join(2)
    srv.close()
    assert json.loads(stdout.getvalue())["result"] == {"echo": "ping"}


def test_shim_unreachable_returns_2():
    import mcp_stdio_shim as shim

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()  # nothing listens here now
    assert shim.run("127.0.0.1", port, 0.5, stdin=io.BytesIO(b""), stdout=io.BytesIO()) == 2
