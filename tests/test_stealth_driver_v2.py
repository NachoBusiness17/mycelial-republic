"""stealth_driver v2 lane tests (ball 2026-09-29): the owed remainder.

Covers the four arch-03 design items this lane landed in
tools/stealth_driver.py:
1. verify topic: funded DONE gate writes done_ts (the queue could never
   drain before: lib-belady-1966 was re-sensed 154x in 24h, res-02).
2. impfeed: mined STEALABLE ideas feed the drained selfimp queue.
3. t_stealth_driver duplicate topic removed; dead groq roster host removed.
4. selffeed rails 1-7: trigger gate, hourly spacing, open cap 20, depth
   cap 2, dedupe + m%03d ids, 24h ttl sweep, append contract kept.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER_PATH = ROOT / "tools" / "stealth_driver.py"


def _load():
    """Fresh module per test (tools/ is not importable as a cheap package)."""
    name = "stealth_driver_v2_under_test"
    if name in sys.modules:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, DRIVER_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _iso(dt: datetime) -> str:
    return dt.isoformat()


# ------------------------------------------------ 3. dup + groq removal ----

def test_groq_host_and_dup_topic_removed():
    drv = _load()
    # arch-03 D4: groq /models 403'd every cycle with the key attached
    assert "groq" not in drv.ROSTER_URLS
    assert drv.ALLOWED_URLS == {drv.LLAMA_HEALTH, *drv.ROSTER_URLS.values()}
    assert len(drv.ALLOWED_URLS) == 3
    # arch-03 D3: t_stealth_driver duplicated t_roster's same-cycle diff
    names = [n for n, _ in drv.TOPICS]
    assert "stealth_driver" not in names, names
    assert not hasattr(drv, "t_stealth_driver")
    # v2 topics present, and work runs BEFORE selffeed (rail 1 needs the
    # same-tick flag)
    assert "verify" in names and "impfeed" in names
    assert names.index("work") < names.index("selffeed")


def test_reset_tick():
    drv = _load()
    drv._TICK["work_sensed_new"] = True
    drv._reset_tick()
    assert drv._TICK["work_sensed_new"] is False


def test_work_sets_tick_flag(tmp_path, monkeypatch):
    drv = _load()
    q = tmp_path / "q.jsonl"
    q.write_text(
        json.dumps({"id": "w1", "ask": "an ask", "status": "queued"}) + "\n",
        encoding="utf-8")
    monkeypatch.setattr(drv, "WORK_QUEUE", q)
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws.json")
    monkeypatch.setattr(drv, "WORK_OUT", tmp_path / "out")
    monkeypatch.setattr(drv, "MINED_FILE", tmp_path / "mined.jsonl")
    monkeypatch.setattr(drv, "_dispatch_hermes",
                        lambda ask: (True, "ANSWER BODY"))
    drv._reset_tick()
    result = drv.t_work()
    assert result.startswith("sensed w1 via hermes"), result
    assert drv._TICK["work_sensed_new"] is True


# --------------------------------------------- 1. verify / DONE gate -------

def _seed_sensed(tmp_path, monkeypatch, drv, sensed_ts=None, verdict_ts=None,
                 answer="w1_openrouter3.md"):
    outdir = tmp_path / "out"
    outdir.mkdir(parents=True, exist_ok=True)
    if answer:
        (outdir / answer).write_text(
            "# WORK w1\nanswer body\n", encoding="utf-8")
    row = {"id": "w1", "ask": "original ask", "status": "sensed",
           "sensed_ts": sensed_ts or _iso(datetime.now(timezone.utc)),
           "answer": answer}
    if verdict_ts:
        row["verdict_ts"] = verdict_ts
    q = tmp_path / "q.jsonl"
    q.write_text(json.dumps(row) + "\n", encoding="utf-8")
    monkeypatch.setattr(drv, "WORK_QUEUE", q)
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws.json")
    monkeypatch.setattr(drv, "WORK_OUT", outdir)
    return q


def test_verify_done_flip_writes_done_ts(tmp_path, monkeypatch):
    """The finish-line shape, unit level: funded verify flips done_ts."""
    drv = _load()
    q = _seed_sensed(tmp_path, monkeypatch, drv)
    monkeypatch.setattr(
        drv, "_dispatch_hermes",
        lambda ask: (True, "checked the claims against the repo receipts\n"
                           "VERDICT: DONE"))
    result = drv.t_verify()
    assert result.startswith("verify w1: done_ts written via hermes"), result
    row = json.loads(q.read_text(encoding="utf-8").splitlines()[0])
    assert row["done_ts"], row
    assert row["verdict"] == "DONE"
    assert row["verifier_lane"] == "hermes"
    receipt = drv.WORK_OUT / row["verify_receipt"]
    assert receipt.is_file()
    assert "VERDICT: DONE" in receipt.read_text(encoding="utf-8")
    # hourly spacing: the next verify inside the hour skips without a
    # second funded dispatch
    assert drv.t_verify().startswith("skip: verify hourly spacing")


def test_verify_owed_leaves_row_open_then_rearms(tmp_path, monkeypatch):
    drv = _load()
    q = _seed_sensed(tmp_path, monkeypatch, drv)
    monkeypatch.setattr(
        drv, "_dispatch_hermes",
        lambda ask: (True, "venue could not be verified\nVERDICT: OWED"))
    result = drv.t_verify()
    assert "verdict OWED" in result and "stays open" in result, result
    row = json.loads(q.read_text(encoding="utf-8").splitlines()[0])
    assert not row.get("done_ts") and row["verdict"] == "OWED"
    # same sensing round already verified: nothing to verify
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws2.json")
    assert drv.t_verify().startswith(
        "skip: verify no unverified sensed answers")
    # a fresh sensing round re-arms the row
    rows = [json.loads(l) for l in
            q.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["sensed_ts"] = _iso(datetime.now(timezone.utc) + timedelta(hours=1))
    q.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws3.json")
    assert drv.t_verify().startswith("verify w1:")


def test_verify_skips_when_answer_file_missing(tmp_path, monkeypatch):
    drv = _load()
    _seed_sensed(tmp_path, monkeypatch, drv, answer=None)
    result = drv.t_verify()
    assert result.startswith("skip: verify answer file missing for w1"), result


def test_verify_no_verdict_line_is_an_err_not_a_flip(tmp_path, monkeypatch):
    drv = _load()
    q = _seed_sensed(tmp_path, monkeypatch, drv)
    monkeypatch.setattr(
        drv, "_dispatch_hermes", lambda ask: (True, "prose without verdict"))
    result = drv.t_verify()
    assert result.startswith("ERR verify w1: no VERDICT line"), result
    row = json.loads(q.read_text(encoding="utf-8").splitlines()[0])
    assert not row.get("done_ts") and not row.get("verdict")


# ----------------------------------------------------- 4b. ttl sweep -------

def test_ttl_sweep_expires_stale_selffed_only(tmp_path, monkeypatch):
    drv = _load()
    old = _iso(datetime.now(timezone.utc) - timedelta(hours=25))
    fresh = _iso(datetime.now(timezone.utc))
    rows = [
        {"id": "m001", "ask": "old selffed", "status": "queued",
         "selffed_ts": old},
        {"id": "m002", "ask": "fresh selffed", "status": "queued",
         "selffed_ts": fresh},
        {"id": "w-old", "ask": "manual row, no stamp", "status": "queued",
         "created": "2026-09-28"},
        {"id": "w-sensed", "ask": "sensed old", "status": "sensed",
         "sensed_ts": old},
        {"id": "m003", "ask": "already expired", "status": "expired",
         "selffed_ts": old},
        {"id": "m004", "ask": "old but done", "status": "queued",
         "selffed_ts": old, "done_ts": old},
    ]
    q = tmp_path / "q.jsonl"
    q.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    monkeypatch.setattr(drv, "WORK_QUEUE", q)
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws.json")
    assert drv._work_ttl_sweep() == 1
    out = {}
    for l in q.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            out[r["id"]] = r
    assert out["m001"]["status"] == "expired" and out["m001"]["expired_ts"]
    assert out["m002"]["status"] == "queued"
    assert out["w-old"]["status"] == "queued"      # manual: never reaped
    assert out["w-sensed"]["status"] == "sensed"   # sensed: verify's job
    assert out["m003"]["status"] == "expired"      # idempotent, not recounted
    assert not out["m004"].get("expired_ts")       # done rows untouched


# --------------------------------------------------- 4. selffeed rails -----

def _selffeed_env(tmp_path, monkeypatch, drv, queue_rows=None, work_id="w1"):
    monkeypatch.setattr(drv, "ROOT", tmp_path)
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws.json")
    q = tmp_path / "q.jsonl"
    if queue_rows:
        q.write_text(
            "\n".join(json.dumps(r) for r in queue_rows) + "\n",
            encoding="utf-8")
    monkeypatch.setattr(drv, "WORK_QUEUE", q)
    inbox = tmp_path / "watch" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / "STEALTH_MINED_FINDINGS.jsonl").write_text(
        json.dumps({"ts": _iso(datetime.now(timezone.utc)),
                    "work_id": work_id, "lane": "llm7", "model": "m",
                    "finish": "stop"}) + "\n",
        encoding="utf-8")
    drv._reset_tick()
    return q


def test_selffeed_rail1_trigger_gate(tmp_path, monkeypatch):
    drv = _load()
    _selffeed_env(tmp_path, monkeypatch, drv)
    monkeypatch.setattr(
        drv, "_dispatch_hermes",
        lambda ask: (True, json.dumps({"ask": "brand new ask", "tier": "free"})))
    # work sensed nothing this tick: no dispatch, no append
    assert drv.t_selffeed().startswith(
        "skip: selffeed rail 1 (trigger)")
    assert not (tmp_path / "q.jsonl").exists()


def test_selffeed_rail1_hourly_spacing(tmp_path, monkeypatch):
    drv = _load()
    _selffeed_env(tmp_path, monkeypatch, drv)
    drv._TICK["work_sensed_new"] = True
    (tmp_path / "ws.json").write_text(
        json.dumps({"selffeed_last_fire_ts": time.time()}), encoding="utf-8")
    assert drv.t_selffeed().startswith("skip: selffeed rail 1 (spacing):")


def test_selffeed_rail2_open_cap(tmp_path, monkeypatch):
    drv = _load()
    rows = [{"id": f"w{i}", "ask": f"ask {i}", "status": "queued"}
            for i in range(drv.SELFFEED_OPEN_CAP)]
    _selffeed_env(tmp_path, monkeypatch, drv, queue_rows=rows)
    drv._TICK["work_sensed_new"] = True
    assert drv.t_selffeed().startswith("skip: selffeed rail 2 (cap):")


def test_selffeed_rail3_depth_cap(tmp_path, monkeypatch):
    drv = _load()
    rows = [{"id": "m005", "ask": "deep branch", "status": "queued",
             "depth": 2}]
    _selffeed_env(tmp_path, monkeypatch, drv, queue_rows=rows,
                  work_id="m005")
    drv._TICK["work_sensed_new"] = True
    assert drv.t_selffeed().startswith("skip: selffeed rail 3 (depth):")


def test_selffeed_depth2_ask_demands_testable(tmp_path, monkeypatch):
    drv = _load()
    rows = [{"id": "m003", "ask": "parent", "status": "queued", "depth": 1}]
    captured = {}

    def fake(ask):
        captured["ask"] = ask
        return True, json.dumps({"ask": "a depth-2 investigation",
                                 "tier": "free"})

    _selffeed_env(tmp_path, monkeypatch, drv, queue_rows=rows,
                  work_id="m003")
    monkeypatch.setattr(drv, "_dispatch_hermes", fake)
    drv._TICK["work_sensed_new"] = True
    assert drv.t_selffeed().startswith("selffed m004:")
    assert "depth 2 of max 2" in captured["ask"]
    assert "TESTABLE" in captured["ask"]


def test_selffeed_rail4_dedupe_drops_near_duplicate(tmp_path, monkeypatch):
    drv = _load()
    dup = ("Investigate the Belady anomaly downstream chain integrity bug "
           "in the estate hooks")
    rows = [{"id": "m001", "ask": dup, "status": "queued", "depth": 1}]
    q = _selffeed_env(tmp_path, monkeypatch, drv, queue_rows=rows)
    monkeypatch.setattr(
        drv, "_dispatch_hermes",
        lambda ask: (True, json.dumps({"ask": dup, "tier": "free"})))
    drv._TICK["work_sensed_new"] = True
    assert drv.t_selffeed().startswith("skip: selffeed rail 4 (dedupe):")
    assert len([l for l in q.read_text(encoding="utf-8").splitlines()
                if l.strip()]) == 1


def test_selffeed_rail4_ids_m03d_hermes_id_ignored(tmp_path, monkeypatch):
    drv = _load()
    rows = [{"id": "m1", "ask": "old drift 1", "status": "queued",
             "depth": 0},
            {"id": "m002", "ask": "old drift 2", "status": "queued",
             "depth": 0}]
    q = _selffeed_env(tmp_path, monkeypatch, drv, queue_rows=rows)
    monkeypatch.setattr(
        drv, "_dispatch_hermes",
        lambda ask: (True, json.dumps(
            {"id": "m999", "ask": "a genuinely new investigation thread",
             "tier": "free"})))
    drv._TICK["work_sensed_new"] = True
    assert drv.t_selffeed().startswith("selffed m003:")
    row = json.loads(q.read_text(encoding="utf-8").splitlines()[-1])
    assert row["id"] == "m003" and row["status"] == "queued"
    assert row["depth"] == 1 and row["parent_id"] == "w1"
    assert row["queued_ts"] and row["selffed_ts"]
    assert row["tier"] == "free"


def test_selffeed_rail7_malformed_json_dropped(tmp_path, monkeypatch):
    drv = _load()
    _selffeed_env(tmp_path, monkeypatch, drv)
    drv._TICK["work_sensed_new"] = True
    monkeypatch.setattr(drv, "_dispatch_hermes",
                        lambda ask: (True, "no json here at all"))
    assert drv.t_selffeed() == "ERR selffeed: no JSON in hermes reply"
    assert not (tmp_path / "q.jsonl").exists()
    # reset the rail-1 fire stamp before the second attempt
    (tmp_path / "ws.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(drv, "_dispatch_hermes",
                        lambda ask: (True, json.dumps({"tier": "free"})))
    assert "malformed" in drv.t_selffeed()
    assert not (tmp_path / "q.jsonl").exists()


# ---------------------------------------------------------- 2. impfeed -----

def test_impfeed_appends_build_item(tmp_path, monkeypatch):
    drv = _load()
    mined_dir = tmp_path / "watch" / "inbox"
    mined_dir.mkdir(parents=True)
    out = tmp_path / "work" / "out"
    out.mkdir(parents=True)
    (out / "w1_llm70.md").write_text(
        "STEALABLE: build a capacity-monotonicity harness for caches",
        encoding="utf-8")
    (mined_dir / "STEALTH_MINED_FINDINGS.jsonl").write_text(
        json.dumps({"ts": _iso(datetime.now(timezone.utc)),
                    "work_id": "w1", "lane": "llm7", "model": "m",
                    "finish": "stop",
                    "answer_file": "work/out/w1_llm70.md"}) + "\n",
        encoding="utf-8")
    monkeypatch.setattr(drv, "ROOT", tmp_path)
    monkeypatch.setattr(drv, "MINED_FILE",
                        mined_dir / "STEALTH_MINED_FINDINGS.jsonl")
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws.json")
    si = tmp_path / "selfimp.jsonl"
    monkeypatch.setattr(drv, "SELFIMP_QUEUE", si)
    monkeypatch.setattr(
        drv, "_dispatch_hermes",
        lambda ask: (True, 'ranked: {"task": "Build a capacity-'
                           'monotonicity harness for the context pack '
                           'cache ladder"}'))
    result = drv.t_impfeed()
    assert result.startswith("impfed imp001:"), result
    row = json.loads(si.read_text(encoding="utf-8").splitlines()[0])
    assert row["id"] == "imp001" and row["source"] == "impfeed"
    assert row["status"] == "queued" and row["depth"] == 0
    assert row["queued_ts"]
    # weekly spacing: the next call inside the week skips without a dispatch
    assert drv.t_impfeed() == "skip: impfeed weekly spacing"


def test_impfeed_skips_without_mined_or_answers(tmp_path, monkeypatch):
    drv = _load()
    monkeypatch.setattr(drv, "WORK_STATE", tmp_path / "ws.json")
    monkeypatch.setattr(drv, "MINED_FILE", tmp_path / "nope.jsonl")
    assert drv.t_impfeed() == "skip: impfeed no mined findings"
    mined = tmp_path / "mined.jsonl"
    mined.write_text(
        json.dumps({"ts": _iso(datetime.now(timezone.utc)),
                    "work_id": "w1", "answer_file": "work/gone.md"})
        + "\n", encoding="utf-8")
    monkeypatch.setattr(drv, "MINED_FILE", mined)
    assert drv.t_impfeed() == (
        "skip: impfeed no answer files inside the week window")
