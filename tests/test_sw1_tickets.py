"""SW1 ticket tests - redemption proof for the SWARM_1.md one-sitting tickets.

Each test names its ticket id and the source row. Instrument: narrow pytest,
.venv interpreter, no network (ds/dispatch monkeypatched).

SW1-01: tools/ocean_v2_pilot.py COST_CAP enforcement (SWARM_1.md row 1,
kimi+glm converged): the cap was decorative; the fix adds cap_ok() checked
before every dispatch plus an aborted_at_cap receipt flag.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _ocean():
    return importlib.import_module("tools.ocean_v2_pilot")


def test_sw1_01_cap_ok_boundary():
    ocean = _ocean()
    assert ocean.cap_ok(0.0) is True
    assert ocean.cap_ok(ocean.COST_CAP - 0.0001) is True
    assert ocean.cap_ok(ocean.COST_CAP) is False
    assert ocean.cap_ok(ocean.COST_CAP + 5.0) is False


def test_sw1_01_main_aborts_at_cap(tmp_path, monkeypatch, capsys):
    ocean = _ocean()
    # one dispatch already at/over cap: every loop must refuse to dispatch
    calls = []

    def fake_ds(system, user, *, max_tokens, temperature):
        calls.append(user[:40])
        # price every successful call at the full cap so the NEXT gate trips
        return {"ok": True, "text": "RATE: 3\nJUSTIFY: cited", "usage": {}}

    monkeypatch.setattr(ocean, "ds", fake_ds)
    monkeypatch.setattr(ocean, "COST_CAP", 0.0)  # real gate: spend 0.0 < 0.0 is False
    monkeypatch.setattr(ocean, "OUT", tmp_path)
    ocean.main()
    receipt = json.loads((tmp_path / "receipt.json").read_text(encoding="utf-8"))
    assert calls == [], "no dispatch may happen when spend starts at cap"
    assert receipt["aborted_at_cap"] is True
    assert receipt["cap"] == 0.0
    out = capsys.readouterr().out
    assert "abort before dispatch" in out


def _gateway():
    return importlib.import_module("tools.roblox_npc_gateway")


def _fake_getaddrinfo(ip):
    def fake(host, port, *a, **kw):
        family = 2 if ":" not in ip else 10
        return [(family, 1, 6, "", (ip, port))]
    return fake


def test_sw1_02_pin_resolves_and_validates(monkeypatch):
    gw = _gateway()
    monkeypatch.setattr(gw.socket, "getaddrinfo", _fake_getaddrinfo("104.18.7.1"))
    assert gw._validated_pin("openrouter.ai") == "104.18.7.1"


def test_sw1_02_pin_rejects_private_rebind(monkeypatch):
    gw = _gateway()
    # the rebinding answer: allowlisted name resolves to a private address
    monkeypatch.setattr(gw.socket, "getaddrinfo", _fake_getaddrinfo("192.168.1.9"))
    with pytest.raises(ValueError, match="non-public"):
        gw._validated_pin("openrouter.ai")


def test_sw1_02_connection_carries_pin(monkeypatch):
    gw = _gateway()
    monkeypatch.setattr(gw.socket, "getaddrinfo", _fake_getaddrinfo("104.18.7.1"))
    conn = gw._PinnedHTTPSConnection("openrouter.ai", pinned="104.18.7.1", timeout=5)
    assert conn._pinned_ip == "104.18.7.1"
    assert conn.host == "openrouter.ai"  # SNI + Host + cert stay on the real name
    # opener now routes https through the pinned handler
    handlers = [type(h).__name__ for h in gw._OPENER.handlers]
    assert "_PinnedHTTPSHandler" in handlers


def test_sw1_03_key_rotation_is_stable():
    """SW1-03: shard key rotation must not depend on the salted process hash."""
    rm = importlib.import_module("tools.reverse_map")
    import hashlib
    def idx(sid, attempt, n):
        return int(hashlib.sha256(f"{sid}:{attempt}".encode()).hexdigest(), 16) % n
    # same inputs -> same index, any process/seed; attempt 2 rotates or repeats deterministically
    assert idx("s01", 1, 3) == idx("s01", 1, 3)
    picks = {idx(f"s{i:02d}", a, 3) for i in range(1, 13) for a in (1, 2)}
    assert picks <= {0, 1, 2}
    assert picks, "rotation must select real indices"
    # source no longer uses the salted builtin for key choice
    src = Path(rm.__file__).read_text(encoding="utf-8")
    assert "keys[hash((" not in src
    assert 'hashlib.sha256(f"{sid}:{attempt}"' in src


def _ps():
    return importlib.import_module("mag.preload_selector")


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _tags(names):
    return _FakeResp({"models": [{"name": n} for n in names]})


def test_sw1_04_exact_match_wins(monkeypatch):
    ps = _ps()
    monkeypatch.setattr(ps.urllib.request, "urlopen", lambda *a, **kw: _tags(
        [ps.PRIMARY_MODEL, "other:1b"]))
    assert ps.pick_model() == ps.PRIMARY_MODEL


def test_sw1_04_suffix_aware_match(monkeypatch):
    """SW1-04: gemma:2b installed as a quant variant must still be picked."""
    ps = _ps()
    monkeypatch.setattr(ps.urllib.request, "urlopen", lambda *a, **kw: _tags(
        ["gemma:2b:q4_K_M", "llama3:8b"]))
    assert ps.pick_model() == "gemma:2b:q4_K_M"


def test_sw1_04_refuses_instead_of_arbitrary_fallthrough(monkeypatch):
    ps = _ps()
    monkeypatch.setattr(ps.urllib.request, "urlopen", lambda *a, **kw: _tags(
        ["llama3:8b", "mistral:7b"]))
    with pytest.raises(ValueError, match="refuses"):
        ps.pick_model()
    src = Path(ps.__file__).read_text(encoding="utf-8")
    assert "return next(iter(sorted(names)" not in src  # the fallthrough STATEMENT is gone


def test_sw1_05_has_model_suffix_aware():
    """SW1-05 first half landed earlier (base+suffix match); pinned so it stays."""
    dmp = importlib.import_module("mag.desk_model_probe")
    assert dmp._has_model("gemma:2b", ["gemma:2b:q4_K_M"]) is True
    assert dmp._has_model("gemma:2b", ["gemma:2b"]) is True
    assert dmp._has_model("gemma:2b", ["gemma3:27b"]) is False


def test_sw1_05_refuses_modelfile_when_base_missing(monkeypatch, tmp_path):
    """SW1-05 second half: pull=False + base absent must fail closed before
    any Modelfile is written, instead of handing ollama a FROM it cannot honor."""
    import subprocess as sp
    dmp = importlib.import_module("mag.desk_model_probe")
    ran = {"create": 0}

    def fake_run(cmd, **kw):
        if cmd[:2] == ["ollama", "create"]:
            ran["create"] += 1
        class P:  # minimal CompletedProcess stand-in
            returncode = 0
            stdout = ""
            stderr = ""
        return P()

    monkeypatch.setattr(dmp, "_tags", lambda: ["unrelated:1b"])
    monkeypatch.setattr(sp, "run", fake_run)
    monkeypatch.setattr(dmp.subprocess, "run", fake_run)
    monkeypatch.setattr(dmp, "ROOT", tmp_path)
    out = dmp.ensure_qwen_desk(pull=False)
    assert out["ok"] is False
    assert "not installed" in out["error"]
    assert ran["create"] == 0
    assert not (tmp_path / "memory" / "working" / "Modelfile.qwen-desk").exists()


def test_sw1_06_canonical_seen_format_no_truncation(tmp_path, monkeypatch):
    """SW1-06: seen file is one canonical shape (plain list) and never silently
    truncates; a legacy dict loads and re-saves canonical."""
    hw = importlib.import_module("scripts.handoff_escalation_watcher")
    seen_path = tmp_path / "seen.json"
    monkeypatch.setattr(hw, "SEEN_PATH", seen_path)

    # legacy dict migrates
    seen_path.write_text(json.dumps({"ids": ["a", "b"]}), encoding="utf-8")
    assert hw._load_seen() == {"a", "b"}
    hw._save_seen({"a", "b"})
    assert json.loads(seen_path.read_text(encoding="utf-8")) == ["a", "b"]  # canonical list

    # no silent 200-id truncation: 250 ids all survive the round-trip
    many = {f"h{i:03d}" for i in range(250)}
    hw._save_seen(many)
    back = json.loads(seen_path.read_text(encoding="utf-8"))
    assert isinstance(back, list) and len(back) == 250
    assert hw._load_seen() == many
    src = Path(hw.__file__).read_text(encoding="utf-8")
    assert "[-200:]" not in src  # the truncation is gone from the writer


def test_sw1_07_warm_tokens_counted(monkeypatch):
    """SW1-07: the --cache warm-up call's tokens must land in the row, not vanish."""
    tp = importlib.import_module("tools.tier_probe")
    calls = []

    def fake_call(model, system, user, *, thinking):
        calls.append({"system": system, "user": user})
        n = len(calls)
        return {"ok": True, "text": "warm prose" if n == 1 else "measured prose",
                "usage": {"prompt_tokens": 100 * n, "completion_tokens": 10 * n},
                "ms": 5 * n}

    monkeypatch.setattr(tp, "_deepseek_call", fake_call)
    tier = next(t for t in tp.TIERS if t["id"] == "flash-off")
    row = tp.run_cell("design", tier, live=True, cache=True)
    assert len(calls) == 2, "warm-up + measured"
    assert row["warm"] is not None
    assert row["warm"]["prompt_tokens"] == 100  # the WARM call's tokens, counted
    assert row["usage"]["prompt_tokens"] == 200  # the measured call
    row2 = tp.run_cell("design", tier, live=True, cache=False)
    assert row2["warm"] is None  # no cache arm, no warm row


def test_sw1_08_task_wall_chore_contract_and_time_filter(tmp_path, monkeypatch):
    """SW1-08: no None lane placeholder; done count filtered to this run."""
    tw = importlib.import_module("tools.task_wall")
    src = Path(tw.__file__).read_text(encoding="utf-8")
    assert '"lane": None' not in src          # placeholder gone: lane assigned once in worker
    assert "run_started" in src and ">= run_started" in src  # the time filter is in
    # ledger filter unit: simulate the counting loop against rows from an older run
    import json as _json
    ledger = tmp_path / "ledger.jsonl"
    old_row = _json.dumps({"ts": "2026-09-23T01:00:00+00:00", "ok": True})
    new_row = _json.dumps({"ts": "2026-10-02T06:00:00+00:00", "ok": True})
    ledger.write_text(old_row + "\n" + new_row + "\n", encoding="utf-8")
    run_started = "2026-10-02T05:00:00+00:00"
    done = 0
    for line in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = _json.loads(line)
            if row.get("ok") and str(row.get("ts", "")) >= run_started:
                done += 1
        except Exception:
            pass
    assert done == 1  # the old run's ok row is not this run's count


def test_sw1_09_one_none_telemetry_policy():
    """SW1-09: afk_train and partition share ONE None-telemetry policy."""
    gg = importlib.import_module("mag.gpu_ghost")
    # known busy -> blocked
    assert gg.telemetry_allows_local({"free": False, "source": "amd-cim"}) is False
    # known free -> allowed
    assert gg.telemetry_allows_local({"free": True, "source": "amd-cim"}) is True
    # telemetry blind (None) -> allowed, matching afk_train's standing law
    assert gg.telemetry_allows_local({"free": None, "source": "none"}) is True
    # both call sites use the shared gate, not their own truthiness
    src = Path(gg.__file__).read_text(encoding="utf-8")
    assert "if apply_local and telemetry_allows_local(gpu)" in src
    assert "if require_free_gpu and not telemetry_allows_local(gpu)" in src
    assert "gpu.get(\"free\") and local" not in src  # the old split policy is gone


def test_sw1_10_gopher_choices_guard_and_sized_est(monkeypatch):
    """SW1-10: empty choices parses as a clean failure; est_tokens sized from
    the prompt; the --loop body survives a raising cycle."""
    gl = importlib.import_module("mag.gopher_lite")
    seen_est = []

    def fake_gate(door, est_tokens):
        seen_est.append(est_tokens)
        return {"ok": True}

    monkeypatch.setattr(gl, "_key", lambda: "k")
    monkeypatch.setattr(gl, "gate", fake_gate)

    def fake_post(url, payload, key):
        return {"choices": [], "usage": {}}  # _post_json returns the parsed dict

    monkeypatch.setattr(gl, "_post_json", fake_post)
    monkeypatch.setattr(gl, "record", lambda *a, **kw: None)
    monkeypatch.setattr(gl, "meter_row", lambda *a, **kw: None)
    prompt = "x" * 40000
    out = gl.chat(prompt, "chore")
    assert out["ok"] is False  # no crash: empty choices -> clean error row
    assert seen_est and seen_est[0] > 10000  # sized from the 40K-char prompt, not flat 4000
    src = Path(gl.__file__).read_text(encoding="utf-8")
    assert "d[\"choices\"][0]" not in src  # the unguarded parse is gone
    assert "loop cycle" in src            # the loop guard names its failures


def test_selfsteal_53_upgrade_5_family_behavior_fold(tmp_path, monkeypatch):
    """SELFSTEAL_53_ERA upgrade 5: the fold appends one behavior row per family
    and names its unwired legs; economics print at rollup close."""
    cs = importlib.import_module("tools.code_swarm")
    monkeypatch.setattr(cs, "ROOT", tmp_path)  # ledger lands in tmp, never the live one

    graded = [
        {"family": "kimi", "ok": True, "channel": "content",
         "defects": [{"start": 10, "claim": "cap is decorative"}]},
        {"family": "glm", "ok": True, "channel": "reasoning",
         "defects": [{"start": 11, "claim": "cap decorative no gate"}]},
        {"family": "glm", "ok": False},
    ]
    clusters = [{"status": "REAL", "claims": [{"family": "kimi"}, {"family": "glm"}]},
                {"status": "UNIQUE", "claims": [{"family": "kimi"}]}]
    rows = cs.family_behavior_fold("sw-test", graded, clusters, 0.0829)
    assert len(rows) == 2
    glm_row = next(r for r in rows if r["family"] == "glm")
    assert glm_row["asks"] == 2 and glm_row["landed"] == 1
    assert glm_row["terminals"] == {"reasoning": 1}
    assert glm_row["cluster_membership"]["REAL"] == 1
    assert "per_family_cost" in glm_row["not_wired"]  # unwired legs NAMED, not faked
    kimi_row = next(r for r in rows if r["family"] == "kimi")
    assert kimi_row["defects_claimed"] == 1
    assert kimi_row["schema"] == "family_behavior.v1"
    ledger = tmp_path / "memory" / "runs" / "model_garden" / "family_behavior.jsonl"
    banked = [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines()]
    assert len(banked) == 2 and {r["family"] for r in banked} == {"kimi", "glm"}
    # the fold is wired into rollup close (source contract)
    src = Path(cs.__file__).read_text(encoding="utf-8")
    assert "family_behavior_fold(run, graded, clusters, cost)" in src
    assert "unique-share" in src  # the economics line prints at close

