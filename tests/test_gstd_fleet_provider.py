"""tests for the gstd fleet lane skeleton (run gstd-mycelial-kickoff-20261007,
lane g3-fleet-lane-spec): the wallet-present gate (fail-closed), the SSRF
allowlist shape, and the gps_mesh_row.v1 contract keyed
(node_device, task_shape, evidence_hash). Spec:
docs/ref/GSTD_FLEET_LANE_SPEC.md; plan: docs/ref/GSTD_DOGFOOD_PLAN.md P3.

No test touches the network: a closed gate blocks before any call, and the
tests past the gate stub at the urllib layer or gate the URL before join.
"""
from __future__ import annotations

import json

import pytest

from tools import gstd_fleet_provider as gfp


@pytest.fixture(autouse=True)
def _no_wallets(monkeypatch):
    # P0 wallets are owed: the default world for these tests is a closed gate.
    monkeypatch.setattr(gfp, "_env", lambda name: "")


def test_wallet_gate_blocks_closed():
    ok, why = gfp.wallet_gate("submit probe-x")
    assert not ok
    assert "WALLET GATE BLOCKED" in why
    assert "P0 INPUTS OWED" in why


def test_wallet_gate_opens_with_one_wallet(monkeypatch):
    monkeypatch.setattr(
        gfp, "_env",
        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    ok, why = gfp.wallet_gate("cycle")
    assert ok
    assert "desktop" in why


def test_submit_refuses_without_wallet_and_never_touches_network(monkeypatch):
    calls = {"n": 0}

    def boom(*a, **k):
        calls["n"] += 1
        raise AssertionError("network touched behind a closed gate")

    monkeypatch.setattr(gfp, "_post_json", boom)
    out = gfp.submit_task(work_id="probe-x", prompt="p", task_shape="probe",
                          device="desktop")
    assert out.get("blocked") is True and not out.get("ok")
    assert calls["n"] == 0


def test_submit_refuses_unknown_task_shape(monkeypatch):
    monkeypatch.setattr(
        gfp, "_env",
        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    out = gfp.submit_task(work_id="q1", prompt="p", task_shape="yolo",
                          device="desktop")
    assert not out.get("ok") and "task_shape" in out["why"]


def test_poll_refuses_bad_task_id_before_url_join(monkeypatch):
    monkeypatch.setattr(
        gfp, "_env",
        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    for bad in ("../etc", "a b", "x/y", "", "id?next=http://evil", "a" * 81):
        out = gfp.poll_task(bad)
        assert not out.get("ok")
        assert "allowlist regex" in out["why"]


def test_get_url_gate_refuses_foreign_urls(monkeypatch):
    monkeypatch.setattr(
        gfp, "_env",
        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    code, body = gfp._get_json("https://evil.example.com/api/v1/tasks/abc", "tok")
    assert code == 0 and "allowlist" in str(body.get("error"))


def test_gps_row_requires_full_key():
    with pytest.raises(ValueError):
        gfp.gps_mesh_row(node_device="", task_shape="probe", evidence_hash="h")
    with pytest.raises(ValueError):
        gfp.gps_mesh_row(node_device="desktop", task_shape="", evidence_hash="h")
    with pytest.raises(ValueError):
        gfp.gps_mesh_row(node_device="desktop", task_shape="probe", evidence_hash="")


def test_gps_row_shape_keyed_triple_and_scrub():
    row = gfp.gps_mesh_row(node_device="desktop", task_shape="probe",
                           evidence_hash="a" * 64, work_id="probe-x",
                           task_id="t1", ok=True, chars=10,
                           detail="key sk-ABCDEFGHIJKLMNOPQRSTUVWX leaked")
    assert row["schema"] == "gps_mesh_row.v1"
    assert row["key"] == ["desktop", "probe", "a" * 64]
    assert (row["node_device"], row["task_shape"], row["evidence_hash"]) == tuple(row["key"])
    assert "[REDACTED]" in row["detail"]
    assert "ABCDEFGHIJKLMNOPQRSTUVWX" not in row["detail"]


def test_verdict_log_adapter_preserves_gps_key():
    # The row key is the raw (node_device, task_shape, evidence_hash) triple;
    # the adapter maps it into verdict-log space: node_device -> gstd-mesh:<device>.
    row = gfp.gps_mesh_row(node_device="bob", task_shape="corridor",
                           evidence_hash="b" * 64, ok=True, task_id="t9")
    args = gfp.to_verdict_log_args(row)
    assert args["model_id"] == "gstd-mesh:bob"
    assert row["key"] == ["bob", "corridor", "b" * 64]
    assert (args["model_id"], args["task_shape"], args["evidence_hash"]) == \
        ("gstd-mesh:" + row["node_device"], row["task_shape"], row["evidence_hash"])
    assert args["verdict"] is True
    assert "t9" in args["evidence_source"]


def test_allowlist_is_fixed_https_literals():
    assert gfp.SUBMIT_URL in gfp._ALLOWED_URLS
    assert gfp.STATS_URL in gfp._ALLOWED_URLS
    assert gfp.SUBMIT_URL.startswith("https://")
    assert gfp.PLATFORM == "https://platform.gstdtoken.com"


def test_bank_mesh_appends_and_scrubs(tmp_path, monkeypatch):
    monkeypatch.setattr(gfp, "MESH_RUNS", tmp_path)
    monkeypatch.setattr(gfp, "MESH_LEDGER", tmp_path / "mesh_ledger.jsonl")
    gfp.bank_mesh({"schema": "gps_mesh_row.v1", "node_device": "desktop",
                   "task_shape": "probe", "evidence_hash": "c" * 64,
                   "detail": "xai-" + "A" * 20})
    lines = (tmp_path / "mesh_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[-1])
    assert row["evidence_hash"] == "c" * 64
    assert "REDACTED" in row["detail"]


def test_cycle_gated_returns_blocked_without_wallets():
    out = gfp.cycle_gstd()
    assert out.startswith("WALLET GATE BLOCKED")


def test_task_id_parse_is_defensive():
    assert gfp._task_id_from({"task_id": " t7 "}) == "t7"
    assert gfp._task_id_from({"task": {"id": 42}}) == "42"
    assert gfp._task_id_from({"nope": 1}) == ""
