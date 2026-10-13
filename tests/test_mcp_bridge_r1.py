"""Bridge R1 tests: the estate verbs on the house MCP surface.

Owed work (2026-09-29): watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md
R1 + the mcp-composition isError contract. Covers: bridge profile projection,
per-tool effect classes, live tools/call round trips (real output, not
stubs), correct error shapes on bad input (in-band isError, never a protocol
error), determinism of the water tick, the OUT_DIR pin on compile, the
redaction scrub on driver status, and the never-exposed ruling (repair, bank,
control words).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mag.mcp_server import ROLE_TOOLSETS, call_tool, handle, tools_manifest
from tools import TOOL_MAP

BRIDGE_TOOLS = (
    "estate_water_graph_tick", "estate_dirac_scan", "estate_dirac_rank",
    "estate_chain_verify", "estate_thought_compile", "estate_driver_status",
    "estate_receipt_append",
)

TICK_SPEC = {
    "schema": "water_graph.v1",
    "tick": 0,
    "nodes": {
        "src": {"elev": 3, "kind": "plain", "volume": 5},
        "dst": {"elev": 0, "kind": "plain", "volume": 0},
    },
    "pipes": {"p1": {"src": "src", "dst": "dst", "cap": 2}},
}


def _names(profile: str = "bridge") -> set[str]:
    return {t["name"] for t in tools_manifest(profile)}


def _call(name: str, args: dict | None = None, profile: str = "bridge") -> dict:
    return call_tool(name, args, set(ROLE_TOOLSETS[profile]))


def _text(resp: dict) -> dict:
    return json.loads(resp["content"][0]["text"])


# ------------------------------------------------------- surface projection --

def test_bridge_profile_lists_exactly_the_estate_tools() -> None:
    assert _names("bridge") == set(BRIDGE_TOOLS)


def test_every_bridge_tool_registered_static_with_schema_and_meta() -> None:
    for name in BRIDGE_TOOLS:
        assert name in TOOL_MAP, name
        row = next(t for t in tools_manifest("bridge") if t["name"] == name)
        assert row["inputSchema"].get("type") == "object", name
        meta = row["_meta"]["mag"]
        assert meta["effect_class"] and meta["authority"], name


def test_effect_classes_match_the_design_table() -> None:
    meta = {t["name"]: t["_meta"]["mag"]["effect_class"]
            for t in tools_manifest("bridge")}
    assert meta["estate_thought_compile"] == "mutating_or_executing"
    assert meta["estate_receipt_append"] == "mutating_or_executing"
    for read_tool in ("estate_water_graph_tick", "estate_dirac_scan",
                      "estate_dirac_rank", "estate_chain_verify",
                      "estate_driver_status"):
        assert meta[read_tool] == "read_or_deterministic_compute", read_tool
    # R2.5 (ractor50 mcp.md 9): the canned_broker tier, not the generic
    # switchboard mutating tier - deterministic local cost, retry_or_defer.
    tiers = {t["name"]: t["_meta"]["mag"] for t in tools_manifest("bridge")}
    receipt = tiers["estate_receipt_append"]
    assert receipt["authority"] == "canned_broker"
    assert receipt["cost_kind"] == "deterministic_local"
    assert receipt["exhaustion"] == "retry_or_defer"


def test_bridge_profile_carries_no_generic_tools() -> None:
    assert not (_names("bridge") & {"run_shell", "write_file", "read_file"})


# ------------------------------------------------------------ water tick ----

def test_tick_live_call_returns_real_output() -> None:
    out = _text(_call("estate_water_graph_tick", {"spec": TICK_SPEC}))
    assert out["ok"] is True
    assert out["events"], "gravity tick must emit event lines"
    assert out["spec"]["nodes"]["src"]["volume"] == 3  # cap 2 moved
    assert out["spec"]["nodes"]["dst"]["volume"] == 2
    assert out["spec"]["tick"] == 1


def test_tick_is_deterministic_across_calls() -> None:
    a = _text(_call("estate_water_graph_tick", {"spec": TICK_SPEC, "ticks": 3}))
    b = _text(_call("estate_water_graph_tick", {"spec": TICK_SPEC, "ticks": 3}))
    assert a == b, "same spec in must give same spec out (stateless physics)"


def test_tick_bad_input_rides_iserror() -> None:
    resp = _call("estate_water_graph_tick", {"spec": {}})
    assert resp["isError"] is True
    body = _text(resp)
    assert body["ok"] is False and "spec.nodes" in body["error"]
    wrong_schema = _call("estate_water_graph_tick",
                         {"spec": {"schema": "water_graph.v2", "nodes": {"a": {}}}})
    assert wrong_schema["isError"] is True
    bad_ticks = _call("estate_water_graph_tick",
                      {"spec": TICK_SPEC, "ticks": 1001})
    assert bad_ticks["isError"] is True


# ---------------------------------------------------------- dirac scan/rank --

def test_dirac_scan_live_call_real_output() -> None:
    out = _text(_call("estate_dirac_scan", {"scope": "operational"}))
    assert out["ok"] is True
    assert isinstance(out["betti1"], int)
    assert isinstance(out["n_loops"], int)
    assert set(out) >= {"closed_solved", "open_gaps", "closed", "open"}


def test_dirac_rank_live_call_real_output() -> None:
    out = _text(_call("estate_dirac_rank", {"scope": "operational"}))
    assert out["ok"] is True
    assert out["beta1"] == out["n_edges"] - out["n_vertices"] + out["components"]


def test_dirac_bad_scope_is_iserror() -> None:
    resp = _call("estate_dirac_scan", {"scope": "internet"})
    assert resp["isError"] is True
    assert "scope must be one of" in _text(resp)["error"]


# ---------------------------------------------------------- chain verify ----

def test_chain_verify_live_call_preserves_exit_contract() -> None:
    out = _text(_call("estate_chain_verify", {}))
    assert out["dry"] is True
    assert out["exit_code"] in (0, 1, 2)
    assert out["ok"] == (out["exit_code"] == 0)
    assert out["verdict"].startswith("CHAIN-REPAIR")


def test_chain_verify_never_writes_when_chain_broken(monkeypatch, tmp_path) -> None:
    """dry=True returns before any write even on a broken chain: the dry
    return sits ahead of every write_text in tools/chain_repair.repair."""
    import tools.chain_repair as cr

    src = Path(cr.__file__).read_text(encoding="utf-8")
    assert src.index("if dry:") < src.index("tmp.write_text"), \
        "the dry return must precede any chain write"


# ------------------------------------------------------- thought compile ----

def _seed_invariants(tmp_path: Path) -> Path:
    inp = tmp_path / "invariants.json"
    inp.write_text(json.dumps({"invariants": {
        "a": {"text": "Never trust a hand-written test count; verify the bytes.",
              "count": 4, "last_seen": "2026-09-29T10:00:00Z"},
        "b": {"text": "Run the suite before claiming done.",
              "count": 2, "last_seen": "2026-09-28T10:00:00Z"},
    }}), encoding="utf-8")
    return inp


def test_thought_compile_writes_only_inside_pinned_out_dir(
        tmp_path, monkeypatch) -> None:
    from tools import thought_quantizer as tq

    monkeypatch.setattr(tq, "DEFAULT_IN", _seed_invariants(tmp_path))
    monkeypatch.setattr(tq, "OUT_DIR", tmp_path / "out")
    out = _text(_call("estate_thought_compile", {}))
    assert out["ok"] is True and out["pinned"] is True
    assert (tmp_path / "out" / "compile_report.json").is_file()
    assert (tmp_path / "out" / "instructions_frontier.jsonl").is_file()


def test_thought_compile_refuses_caller_supplied_paths(tmp_path) -> None:
    evil = tmp_path / "evil"
    resp = _call("estate_thought_compile", {"out": str(evil)})
    assert resp["isError"] is True
    assert "bridge pin" in _text(resp)["error"]
    assert not evil.exists(), "a refused path must never be written"


def test_thought_compile_converts_systemexit_to_iserror(
        tmp_path, monkeypatch) -> None:
    from tools import thought_quantizer as tq

    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"nope": 1}), encoding="utf-8")
    monkeypatch.setattr(tq, "DEFAULT_IN", bad)
    monkeypatch.setattr(tq, "OUT_DIR", tmp_path / "out")
    resp = _call("estate_thought_compile", {})
    assert resp["isError"] is True  # SystemExit must not kill the server loop
    assert "input error" in _text(resp)["error"]


# --------------------------------------------------------- driver status ----

def test_driver_status_redacts_and_reads(monkeypatch, tmp_path) -> None:
    from tools import stealth_driver as sd

    hb = tmp_path / "hb.jsonl"
    hb.write_text(
        json.dumps({"ts": "t0", "cycle": 1, "topics": {"x": "ok"},
                    "key": "nous-abcdef123456"}) + "\n"
        + json.dumps({"ts": "t1", "cycle": 2,
                      "topics": {"y": "sk-abc123456789 in prose"}}) + "\n",
        encoding="utf-8")
    ws = tmp_path / "ws.json"
    ws.write_text(json.dumps({"last_lane_ts": {"a": 1.0},
                              "api_key": "sk-ab12cd34ef56"}), encoding="utf-8")
    monkeypatch.setattr(sd, "HEARTBEAT", hb)
    monkeypatch.setattr(sd, "OFF_FLAG", tmp_path / "absent.off")
    monkeypatch.setattr(sd, "WORK_STATE", ws)
    out = _text(_call("estate_driver_status", {"tail": 2}))
    assert out["ok"] is True and out["off"] is False
    dumped = json.dumps(out)
    assert "nous-abcdef123456" not in dumped
    assert "sk-abc123456789" not in dumped
    assert "sk-ab12cd34ef56" not in dumped
    assert out["heartbeat_tail"][0]["key"] == "<redacted>"
    assert out["work_state"]["api_key"] == "<redacted>"
    assert out["work_state"]["last_lane_ts"] == {"a": 1.0}


def test_driver_status_dark_surface_is_ok_not_crash(monkeypatch, tmp_path) -> None:
    from tools import stealth_driver as sd

    monkeypatch.setattr(sd, "HEARTBEAT", tmp_path / "nope.jsonl")
    off = tmp_path / "off.flag"
    off.write_text("", encoding="utf-8")
    monkeypatch.setattr(sd, "OFF_FLAG", off)
    monkeypatch.setattr(sd, "WORK_STATE", tmp_path / "nope.json")
    out = _text(_call("estate_driver_status", {}))
    assert out["ok"] is True and out["off"] is True
    assert out["heartbeat_tail"] == [] and out["work_state"] == {}


# ------------------------------------------------------ protocol contract ----

def test_profile_rejection_is_inband_iserror() -> None:
    resp = _call("estate_water_graph_tick", {"spec": TICK_SPEC}, profile="governor")
    assert resp["isError"] is True
    assert "not in active MCP profile" in resp["content"][0]["text"]


def test_unknown_tool_is_inband_iserror() -> None:
    # allowed_tools=None (full projection) reaches the unknown-tool branch;
    # under a bounded profile the same name reads as a profile rejection.
    resp = call_tool("estate_no_such_tool", {}, None)
    assert resp["isError"] is True
    assert "unknown tool" in resp["content"][0]["text"]
    bounded = _call("estate_no_such_tool", {})
    assert bounded["isError"] is True


def test_tools_call_over_handle_round_trip() -> None:
    resp = handle({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                   "params": {"name": "estate_water_graph_tick",
                              "arguments": {"spec": TICK_SPEC}}},
                  profile="bridge", pin_ledger=None)
    assert resp["id"] == 7
    assert json.loads(resp["result"]["content"][0]["text"])["ok"] is True


def test_never_exposed_repair_bank_and_control_words() -> None:
    for forbidden in ("estate_chain_repair", "estate_dirac_bank",
                      "estate_driver_stop", "estate_driver_start",
                      "estate_driver_once"):
        assert forbidden not in TOOL_MAP, forbidden
        assert forbidden not in _names("bridge"), forbidden


def test_arg_aliases_normalize_blob_shapes() -> None:
    from tools import _normalize_args

    assert _normalize_args("estate_water_graph_tick",
                           {"graph": TICK_SPEC})["spec"] == TICK_SPEC
    assert _normalize_args("estate_dirac_scan",
                           {"graph_scope": "all"})["scope"] == "all"


# ------------------------------------------------ receipt append (R2.5) ------
# Spec: watch/inbox/ractor50/mcp.md section 9. All receipt tests pin the
# write root to tmp_path the same way the compile tests pin tq.OUT_DIR, so
# the suite never files into the real watch/inbox/.

def _pin_inbox(tmp_path: Path, monkeypatch) -> Path:
    from mag import estate_bridge as eb

    inbox = tmp_path / "inbox"
    monkeypatch.setattr(eb, "RECEIPT_INBOX_DIR", inbox)
    return inbox


def _receipt_call(wave: str, name: str, payload: str) -> dict:
    return _call("estate_receipt_append",
                 {"wave": wave, "name": name, "payload": payload})


def test_receipt_append_happy_path_hash_equality(tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    out = _text(_receipt_call("wave_r25", "receipt.md",
                              "# receipt\nR2.5 happy path\n"))
    assert out["ok"] is True
    target = tmp_path / "inbox" / "wave_r25" / "receipt.md"
    assert Path(out["path"]) == target.resolve()
    on_disk = target.read_bytes()  # falsifier arm: hash must match the bytes
    assert out["sha256"] == hashlib.sha256(on_disk).hexdigest()
    assert out["bytes"] == len(on_disk)
    assert "rotated_to" not in out  # first write rotates nothing


def test_receipt_append_overwrite_rotates_to_bak(tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    first = _text(_receipt_call("wave_r25", "receipt.md", "v1 bytes"))
    assert first["ok"] is True
    second = _text(_receipt_call("wave_r25", "receipt.md", "v2 bytes"))
    assert second["ok"] is True
    assert second["rotated_to"], "overwrite must report both paths"
    backup = Path(second["rotated_to"])
    assert backup.name.startswith("receipt.md.bak_")
    assert backup.read_text(encoding="utf-8") == "v1 bytes"  # old bytes kept
    assert Path(second["path"]).read_text(encoding="utf-8") == "v2 bytes"


def test_receipt_append_dotdot_escape_refused(tmp_path, monkeypatch) -> None:
    inbox = _pin_inbox(tmp_path, monkeypatch)
    for bad in ({"wave": "../evil", "name": "r.md", "payload": "x"},
                {"wave": "..", "name": "r.md", "payload": "x"},
                {"wave": "ok_wave", "name": "../../evil.md", "payload": "x"},
                {"wave": "wave/../..", "name": "r.md", "payload": "x"}):
        resp = _call("estate_receipt_append", bad)
        assert resp["isError"] is True, bad
    # every call refused before any mkdir: not even the inbox root exists
    assert list(tmp_path.iterdir()) == [], "nothing may land outside the inbox"


def test_receipt_append_absolute_path_refused(tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    for bad in ({"wave": "w", "name": "/etc/passwd.md", "payload": "x"},
                {"wave": "w", "name": "C:/Windows/evil.md", "payload": "x"},
                {"wave": "w", "name": "\\\\server\\share\\r.md", "payload": "x"},
                {"wave": "C:/tmp", "name": "r.md", "payload": "x"}):
        resp = _call("estate_receipt_append", bad)
        assert resp["isError"] is True, bad
    assert not (tmp_path / "inbox" / "w").exists(), "a refused call writes nothing"


def test_receipt_append_oversize_refused(tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    resp = _call("estate_receipt_append",
                 {"wave": "w", "name": "r.md", "payload": "x" * 65537})
    assert resp["isError"] is True
    assert "65536" in _text(resp)["error"], "the cap must be named"
    # the cap is UTF-8 BYTES, not characters: 33000 two-byte chars > 65536
    wide = _call("estate_receipt_append",
                 {"wave": "w", "name": "r.md", "payload": "\u00e9" * 33000})
    assert wide["isError"] is True
    # boundary: exactly the cap lands and reports its own byte length
    edge = _text(_receipt_call("w", "r.md", "y" * 65536))
    assert edge["ok"] is True and edge["bytes"] == 65536


def test_receipt_append_bad_charset_wave_refused(tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    for bad_wave in ("bad wave", "wave/x", "wave\\x", "-lead", ".dot",
                     "a" * 65, "wave..x"):
        resp = _receipt_call(bad_wave, "r.md", "x")
        assert resp["isError"] is True, bad_wave
    # name charset + suffix rule (same charset, .json/.md only)
    for bad_name in ("r.txt", "r", "a" * 62 + ".md"):  # 65 chars > 64 cap
        resp = _receipt_call("w", bad_name, "x")
        assert resp["isError"] is True, bad_name


def test_receipt_append_never_touches_index_json(tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    for bad_name in ("INDEX.json", "index.json"):
        resp = _receipt_call("w", bad_name, "x")
        assert resp["isError"] is True, bad_name
    assert not (tmp_path / "inbox" / "INDEX.json").exists()
    assert not (tmp_path / "inbox" / "w").exists(), "no dir for a refused name"


def test_receipt_append_unknown_tool_iserror_discipline_untouched(
        tmp_path, monkeypatch) -> None:
    _pin_inbox(tmp_path, monkeypatch)
    resp = call_tool("estate_receipt_no_such", {}, None)  # full projection
    assert resp["isError"] is True
    assert "unknown tool" in resp["content"][0]["text"]
    bounded = _call("estate_receipt_no_such", {})
    assert bounded["isError"] is True
    # missing required arguments still ride isError, never a crash
    missing = _call("estate_receipt_append", {"wave": "w"})
    assert missing["isError"] is True
