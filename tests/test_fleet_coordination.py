"""Fleet coordination organs (2026-10-17): fleet_report.v1, leases, notices.

Doctrine: watch/LIBRARY/FLEET_COORDINATION_DOCTRINE_20261017.md. Every path
constant is redirected to tmp_path; nothing touches watch/receipts/, the chain,
docker, or the lab. Docker calls are monkeypatched and asserted NOT to run when
a gate refuses.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import estate_bridge as eb  # noqa: E402
from mag import fleet_report as fr  # noqa: E402
from mag import leases as L  # noqa: E402
from mag import mcp_server as ms  # noqa: E402
from mag import warm_surface as ws  # noqa: E402

FAKE_SK = "sk-" + "abcdefghijklmnopqrstuvwx1234"


@pytest.fixture
def receipts(tmp_path, monkeypatch):
    d = tmp_path / "watch" / "receipts"
    monkeypatch.setattr(eb, "SHARED_RECEIPT_DIR", d)
    monkeypatch.setattr(fr, "RECEIPTS_DIR", d)
    return d


@pytest.fixture
def lease_dir(tmp_path, monkeypatch):
    d = tmp_path / "watch" / "receipts" / "leases"
    monkeypatch.setattr(L, "LEASE_DIR", d)
    monkeypatch.delenv(L.ENV_SEAT, raising=False)
    monkeypatch.delenv(L.ENV_TOKEN, raising=False)
    return d


def _call(name, args, profile="warm"):
    out = ms.call_tool(name, args, set(ms._profile_names(profile)))
    return out, json.loads(out["content"][0]["text"])


SITREP = {"status": "green: 2 tasks in flight", "readiness": "ready"}
SPOT = {"size": "1 container", "activity": "restarted", "location": "mag-sovereign",
        "unit": "unknown seat", "time": "2026-10-17T18:15:44Z", "equipment": "docker compose"}
NOTICE = {"notice_id": "N-20261017-test-hazard", "category": "hazard_file",
          "subject": "test hazard", "affects": ["mag/x.py"], "action_required": "do not edit",
          "in_force_until": "until_cancelled", "names": ["SOME_KEY_NAME"]}


# ───────────────────────────── schema / validator ─────────────────────────

def test_schema_file_and_validator_agree_on_kinds():
    doc = fr.load_schema()
    assert doc["properties"]["kind"]["enum"] == list(fr.KINDS)
    assert doc["properties"]["schema"]["const"] == fr.SCHEMA
    kinds_with_rules = {b["if"]["properties"]["kind"]["const"] for b in doc["allOf"]}
    assert kinds_with_rules == set(fr.KINDS)


@pytest.mark.parametrize("kind,fields", [
    ("SITREP", SITREP), ("SPOTREP", SPOT), ("NOTICE", NOTICE),
    ("RELIEF", {"status": "handing over", "outstanding": "none", "leases": [], "stand_relieved": True}),
    ("ACK", {"ack_of": "N-20261017-test-hazard"}),
])
def test_valid_reports_pass(kind, fields):
    assert fr.validate(fr.build_report(kind, "grok", fields)) == []


@pytest.mark.parametrize("mutate,needle", [
    (lambda r: r.pop("readiness"), "SITREP requires field: readiness"),
    (lambda r: r.update(kind="GOSSIP"), "kind"),
    (lambda r: r.update(extra="x"), "unknown field"),
    (lambda r: r.update(dtg="yesterday"), "dtg"),
    (lambda r: r.update(dtg="2026-10-17T10:00:00"), "dtg"),  # no zone
    (lambda r: r.update(seat="../etc"), "seat"),
    (lambda r: r.update(status="x" * 401), "longer than"),
    (lambda r: r.update(narrative="leak " + FAKE_SK), "secret-shaped"),
    (lambda r: r.update(schema="fleet_report.v2"), "schema"),
])
def test_invalid_reports_rejected(mutate, needle):
    r = fr.build_report("SITREP", "grok", dict(SITREP))
    mutate(r)
    errs = fr.validate(r)
    assert errs and any(needle in e for e in errs), errs


def test_notice_names_only_value_refused():
    bad = dict(NOTICE, names=["OPENAI_API_KEY=" + "x" * 20])
    assert any("secret-shaped" in e for e in fr.validate(fr.build_report("NOTICE", "grok", bad)))


def test_relief_stand_relieved_must_be_true_boolean():
    r = fr.build_report("RELIEF", "grok", {"status": "s", "outstanding": "o", "leases": [],
                                           "stand_relieved": 1})
    assert fr.validate(r)


# ───────────────────────────── receipt writer gate ────────────────────────

def test_invalid_fleet_body_refused_by_receipt_writer(receipts):
    body = json.dumps({"schema": "fleet_report.v1", "kind": "SITREP", "seat": "grok",
                       "dtg": "2026-10-17T20:00:00Z"})  # missing status/readiness
    out, res = _call("estate_shared_receipt", {"seat": "grok", "body": body})
    assert out.get("isError") and "fleet_report.v1 refused" in res["error"]
    assert not receipts.exists() or not any(receipts.iterdir())


def test_fleet_body_seat_must_match_receipt_seat(receipts):
    rep = fr.build_report("SITREP", "gemini", SITREP)
    out, res = _call("estate_shared_receipt", {"seat": "grok", "body": fr.canonical_body(rep)})
    assert out.get("isError") and "seat" in res["error"]


def test_plain_and_other_json_receipts_unchanged(receipts):
    out, res = _call("estate_shared_receipt", {"seat": "grok", "body": "plain text"})
    assert not out.get("isError") and "fleet_report" not in res
    out, res = _call("estate_shared_receipt", {"seat": "grok", "body": '{"kind": "ACK", "x": 1}'})
    assert not out.get("isError") and "fleet_report" not in res


def test_valid_fleet_body_indexed(receipts):
    out, res = _call("estate_fleet_report", {"seat": "grok", "kind": "SITREP", "report": SITREP})
    assert not out.get("isError"), res
    rec = json.loads((receipts.parent.parent / res["path"]).read_text(encoding="utf-8"))
    assert rec["fleet_report"]["kind"] == "SITREP"
    body = json.loads(rec["body"])
    assert body["schema"] == "fleet_report.v1" and body["seat"] == "grok" and body["dtg"].endswith("Z")
    assert rec["title"].startswith("SITREP")


def test_fleet_report_tool_refuses_invalid_and_extra_args(receipts):
    out, res = _call("estate_fleet_report", {"seat": "grok", "kind": "SPOTREP", "report": {"size": "1"}})
    assert out.get("isError") and "SPOTREP requires" in res["error"]
    out, res = _call("estate_fleet_report", {"seat": "grok", "kind": "SITREP", "report": SITREP,
                                             "path": "../../x"})
    assert out.get("isError")
    assert not receipts.exists() or not any(receipts.iterdir())


def test_cli_validate_and_dry(tmp_path, capsys):
    import importlib.util

    spec = importlib.util.spec_from_file_location("fleet_cli", ROOT / "scripts" / "fleet_report.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    p = tmp_path / "r.json"
    p.write_text(json.dumps(fr.build_report("SITREP", "grok", SITREP)), encoding="utf-8")
    assert cli.main(["validate", str(p)]) == 0
    assert cli.main(["file", "SITREP", "--seat", "grok", "--field", "status=x", "--dry"]) == 1
    assert cli.main(["file", "SITREP", "--seat", "grok", "--field", "status=x",
                     "--field", "readiness=y", "--dry"]) == 0


# ───────────────────────────── notices ────────────────────────────────────

def test_notices_in_force_ack_and_cancel(receipts):
    fr.file_report(seat="grok", kind="NOTICE", report=NOTICE)
    fr.file_report(seat="gemini", kind="ACK", report={"ack_of": NOTICE["notice_id"], "note": "seen"})
    nb = fr.notices()
    assert nb["in_force_count"] == 1
    row = nb["in_force"][0]
    assert row["notice_id"] == NOTICE["notice_id"] and row["acks"][0]["seat"] == "gemini"
    cancel = dict(NOTICE, notice_id="N-20261017-test-hazard-cleared", subject="cleared",
                  cancels=NOTICE["notice_id"])
    fr.file_report(seat="grok", kind="NOTICE", report=cancel)
    nb = fr.notices()
    ids = [n["notice_id"] for n in nb["in_force"]]
    assert NOTICE["notice_id"] not in ids
    assert any(c["notice_id"] == NOTICE["notice_id"] and c["state"] == "cancelled"
               for c in nb["closed_recent"])


def test_notice_with_past_until_lapses(receipts):
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    fr.file_report(seat="grok", kind="NOTICE", report=dict(NOTICE, in_force_until=past))
    nb = fr.notices()
    assert nb["in_force_count"] == 0 and nb["closed_recent"][0]["state"] == "lapsed"


def test_warm_notices_and_leases_resources(receipts, lease_dir):
    fr.file_report(seat="grok", kind="NOTICE", report=NOTICE)
    uris = ws.resource_uris()
    assert "mag://warm/notices" in uris and "mag://warm/leases" in uris
    body = json.loads(ws.read_resource("mag://warm/notices")["text"])
    assert body["in_force"][0]["notice_id"] == NOTICE["notice_id"]
    a = L.acquire(resource="proc:lab", seat="grok", purpose="test restart")
    board = json.loads(ws.read_resource("mag://warm/leases")["text"])
    row = next(r for r in board["leases"] if r["resource"] == "proc:lab")
    assert row["state"] == "held" and row["holder"] == "grok"
    assert a["lease_token"] not in json.dumps(board) and "token_sha256" not in json.dumps(board)
    pre = ws.read_resource("mag://warm/preamble/grok")["text"]
    assert "LEASE proc:lab held by grok" in pre and NOTICE["notice_id"] in pre
    out, res = _call("estate_notices", {})
    assert not out.get("isError") and res["in_force_count"] == 1
    out, res = _call("estate_leases", {})
    assert not out.get("isError") and res["held"] == 1


# ───────────────────────────── leases ─────────────────────────────────────

def test_only_restricted_list_is_leasable(lease_dir):
    with pytest.raises(L.LeaseError):
        L.acquire(resource="file:mag/anything.py", seat="grok", purpose="x")
    assert set(L.restricted()) == {"chain:biography", "file:mag/verkle_knot.py", "proc:lab",
                                   "file:docker-compose.yml", "keys:names"}


def test_holder_keeps_newcomer_refused_with_who_until(lease_dir):
    a = L.acquire(resource="proc:lab", seat="grok", purpose="restart lab")
    assert a["ok"] and a["lease_token"]
    b = L.acquire(resource="proc:lab", seat="gemini", purpose="also restart")
    assert b["ok"] is False and b["refused"] and b["holder"] == "grok"
    assert b["until"] == a["until"] and b["purpose"] == "restart lab" and b["remaining_s"] > 0
    again = L.acquire(resource="proc:lab", seat="grok", purpose="dup")
    assert again["refused"] and "renew" in again["how"]
    disk = (lease_dir / "proc_lab.json").read_text(encoding="utf-8")
    assert a["lease_token"] not in disk and "token_sha256" in disk


def test_renew_release_transfer(lease_dir):
    a = L.acquire(resource="chain:biography", seat="grok", purpose="repair", ttl_s=120)
    with pytest.raises(L.LeaseError):
        L.renew(resource="chain:biography", seat="grok", lease_token="wrong")
    with pytest.raises(L.LeaseError):
        L.renew(resource="chain:biography", seat="gemini", lease_token=a["lease_token"])
    r = L.renew(resource="chain:biography", seat="grok", lease_token=a["lease_token"], ttl_s=600)
    assert r["ok"] and r["until"] >= a["until"]
    t = L.transfer(resource="chain:biography", seat="grok", lease_token=a["lease_token"],
                   to_seat="gemini")
    assert t["ok"] and t["to"] == "gemini" and t["fence"] == a["fence"] + 1
    with pytest.raises(L.LeaseError):  # old token dead
        L.release(resource="chain:biography", seat="grok", lease_token=a["lease_token"])
    assert L.check(resource="chain:biography", seat="gemini", lease_token=t["lease_token"])["holds"]
    rel = L.release(resource="chain:biography", seat="gemini", lease_token=t["lease_token"])
    assert rel["ok"] and not L.check(resource="chain:biography")["held"]
    events = [json.loads(x)["event"] for x in (lease_dir / "ledger.jsonl").read_text().splitlines()]
    assert events == ["acquired", "renewed", "transferred", "released"]


def test_ttl_bounds_and_expiry_supersede(lease_dir, monkeypatch):
    with pytest.raises(L.LeaseError):
        L.acquire(resource="proc:lab", seat="grok", purpose="x", ttl_s=5)
    with pytest.raises(L.LeaseError):
        L.acquire(resource="proc:lab", seat="grok", purpose="x", ttl_s=10 ** 6)
    with pytest.raises(L.LeaseError):
        L.acquire(resource="proc:lab", seat="grok", purpose="  ")
    L.acquire(resource="proc:lab", seat="grok", purpose="x", ttl_s=60)
    real = time.time
    monkeypatch.setattr(L, "_now", lambda: real() + 61)
    b = L.acquire(resource="proc:lab", seat="gemini", purpose="after expiry")
    assert b["ok"] and b["fence"] == 2
    events = [json.loads(x)["event"] for x in (lease_dir / "ledger.jsonl").read_text().splitlines()]
    assert "expired_superseded" in events


def test_mcp_lease_tools(lease_dir):
    out, res = _call("estate_lease_acquire", {"resource": "proc:lab", "seat": "grok", "purpose": "t"})
    assert not out.get("isError") and res["ok"]
    tok = res["lease_token"]
    out, res = _call("estate_lease_acquire", {"resource": "proc:lab", "seat": "zcode", "purpose": "t"})
    assert res["refused"] and res["holder"] == "grok"
    out, res = _call("estate_lease_renew", {"resource": "proc:lab", "seat": "grok", "token": tok})
    assert not out.get("isError") and res["ok"]  # alias token -> lease_token
    out, res = _call("estate_lease_release", {"resource": "proc:lab", "seat": "grok", "lease_token": tok})
    assert res["ok"]
    out, res = _call("estate_lease_acquire", {"resource": "../../.env", "seat": "grok", "purpose": "t"})
    assert out.get("isError")


def test_resource_for_path():
    assert L.resource_for_path("memory/biography/verkle_chain.jsonl") == ["chain:biography"]
    assert L.resource_for_path("./mag/verkle_knot.py") == ["file:mag/verkle_knot.py"]
    assert L.resource_for_path("docker-compose.yml") == ["file:docker-compose.yml"]
    assert L.resource_for_path(".env") == ["keys:names"]
    assert L.resource_for_path("mag/other.py") == []


def test_break_is_logged(lease_dir):
    L.acquire(resource="proc:lab", seat="grok", purpose="x")
    with pytest.raises(L.LeaseError):
        L.break_lease(resource="proc:lab", operator="nacho", reason="")
    out = L.break_lease(resource="proc:lab", operator="nacho", reason="seat died")
    assert out["broken_holder"] == "grok" and not L.check(resource="proc:lab")["held"]


# ───────────────────────────── guards / gated scripts ─────────────────────

def test_guard_modes(lease_dir, monkeypatch):
    assert L.guard("proc:lab", "t", enforce="warn")["allowed"]
    assert L.guard("proc:lab", "t", enforce="conflict")["allowed"]  # unleased = warn
    assert not L.guard("proc:lab", "t", enforce="require")["allowed"]
    a = L.acquire(resource="proc:lab", seat="grok", purpose="x")
    assert not L.guard("proc:lab", "t", enforce="conflict")["allowed"]  # someone else holds
    assert L.guard("proc:lab", "t", enforce="warn")["allowed"]
    monkeypatch.setenv(L.ENV_SEAT, "grok")
    monkeypatch.setenv(L.ENV_TOKEN, a["lease_token"])
    assert L.guard("proc:lab", "t", enforce="require")["allowed"]
    assert L.guard("proc:lab", "t", enforce="conflict")["allowed"]


def test_docker_ops_up_down_refused_when_other_seat_holds(lease_dir, monkeypatch):
    from mag import docker_ops

    ran = []
    monkeypatch.setattr(docker_ops, "_run", lambda *a, **k: ran.append(a) or {"ok": True, "code": 0, "out": "", "err": ""})
    monkeypatch.setattr(docker_ops, "ensure_engine", lambda *a, **k: ran.append("engine") or {"engine_reachable": True})
    monkeypatch.setattr(docker_ops, "_log", lambda *a, **k: None)
    L.acquire(resource="proc:lab", seat="gemini", purpose="mine")
    for fn in (docker_ops.up, docker_ops.down):
        out = fn()
        assert out["ok"] is False and out["refused"] and out["lease_holder"] == "gemini"
    assert ran == []


def test_lab_ctl_requires_lease_and_dry_runs_nothing(lease_dir, monkeypatch):
    import importlib.util

    from mag import docker_ops

    ran = []
    monkeypatch.setattr(docker_ops, "_run", lambda *a, **k: ran.append(a) or {"ok": True, "code": 0, "out": "", "err": ""})
    spec = importlib.util.spec_from_file_location("lab_ctl", ROOT / "scripts" / "lab_ctl.py")
    lab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lab)
    out = lab.run("restart", dry=True)
    assert out["refused"] and out["cmd"] == ["docker", "compose", "restart", "mag"]
    a = L.acquire(resource="proc:lab", seat="grok", purpose="restart test")
    out = lab.run("freeze", dry=True, seat="grok", lease_token=a["lease_token"])
    assert out["ok"] and out["dry"] and out["cmd"] == ["docker", "pause", "mag-sovereign"]
    out = lab.run("restart", dry=True, seat="gemini", lease_token=a["lease_token"])
    assert out["refused"]
    assert lab.main(["stop", "--dry"]) == 3
    assert ran == []


def test_chain_repair_tools_refuse_when_other_seat_holds(lease_dir, monkeypatch, capsys):
    import importlib.util

    L.acquire(resource="chain:biography", seat="gemini", purpose="mine")
    spec = importlib.util.spec_from_file_location("chain_repair_t", ROOT / "tools" / "chain_repair.py")
    cr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cr)
    monkeypatch.setattr(cr, "_verify_chain_consistent", lambda: (False, "test: forced"))

    def boom(*a, **k):
        raise AssertionError("verkle_lock must not be taken when the lease refuses")

    monkeypatch.setattr(cr, "verkle_lock", boom)
    assert cr.repair(dry=False) == 3
    assert "held by gemini" in capsys.readouterr().out


def test_consolidate_hook_is_warn_only(lease_dir, monkeypatch):
    from mag import verkle_knot as vk

    L.acquire(resource="chain:biography", seat="gemini", purpose="mine")
    called = []

    class _Lock:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(vk, "verkle_lock", lambda *a, **k: _Lock())
    monkeypatch.setattr(vk, "_consolidate_chain_one_leaf_per_session_unlocked",
                        lambda: called.append(1) or {"ok": True})
    assert vk.consolidate_chain_one_leaf_per_session() == {"ok": True}
    assert called == [1]  # held by another seat, still proceeds: warn-only
