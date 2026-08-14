"""Stateless tests for frontier_council — spend the ENTIRE weekly frontier allowance on the
strongest advice, coordinated with deepseek + vram. RIB: frontier_council.v1 — allowance() used/cap/
remaining per surface; rightsize() frontier vs cheap (elevate signal); spend() records a scarce
spend with a rightsize guard; delegate() routes + shapes the ask; council() the coordinated team;
route() via swarm_surface. Stateless: tmp_path, no framework dependency."""
from __future__ import annotations


def test_allowance_reports_used_cap(tmp_path, monkeypatch):
    import mag.frontier_council as m
    monkeypatch.setattr(m, "ALLOWANCE", tmp_path / "allowance.jsonl")
    monkeypatch.setattr(m, "CAPS", tmp_path / "caps.json")
    a = m.allowance()
    assert a["ok"]
    surfaces = {r["surface"]: r for r in a["surfaces"]}
    assert "chatgpt" in surfaces and surfaces["chatgpt"]["scarce"] is True
    assert surfaces["chatgpt"]["used"] == 0
    assert surfaces["chatgpt"]["cap"] > 0  # scarce -> finite cap
    # CORRECTION (2026-08-12): supergrok (both grok surfaces) is a LIMITED scarce resource,
    # NOT our local; deepseek is FREE (not scarce).
    assert surfaces["grok_web"]["scarce"] is True and surfaces["grok_x"]["scarce"] is True
    assert surfaces["grok_web"]["cap"] > 0
    assert surfaces["deepseek"]["scarce"] is False  # chat.deepseek is free
    assert "grok-4.5" in m.SURFACES["grok_web"]["models"]
    assert m.SURFACES["grok_web"]["accounts"] == ["nacho", "sd"]  # 2 accounts share supergrok


def test_rightsize_routes_by_work_type():
    import mag.frontier_council as m
    # code planning / frontier research -> scarce frontier (grok/gpt)
    f = m.rightsize("plan the architecture for the new emulator")
    assert f["tier"] == "frontier" and "code-planning" in f["work_type"]
    fr = m.rightsize("frontier research on capture-resistant nets")
    assert fr["tier"] == "frontier"
    # data / maintenance -> free deepseek (high quality, not scarce)
    c = m.rightsize("process this batch of logs")
    assert c["tier"] == "deepseek" and c["surface"] == "deepseek"
    m2 = m.rightsize("maintenance on the corpus and dedupe")
    assert m2["tier"] == "deepseek"


def test_route_type_classifies():
    import mag.frontier_council as m
    assert m.route_type("build a new code blueprint")["type"] == "frontier"
    assert m.route_type("backfill and monitor the data logs")["type"] == "deepseek"


def test_spend_records_and_rightsize_guard(tmp_path, monkeypatch):
    import mag.frontier_council as m
    monkeypatch.setattr(m, "FRONTIER_DIR", tmp_path)
    monkeypatch.setattr(m, "ALLOWANCE", tmp_path / "allowance.jsonl")
    monkeypatch.setattr(m, "CAPS", tmp_path / "caps.json")
    # elevate-worthy spend on scarce surface is allowed
    ok = m.spend("advice: plan the code for the new emulator", "chatgpt")
    assert ok["ok"] and ok["used"] == 1
    # data/maintenance spend on scarce surface is refused (routing guard)
    bad = m.spend("process this log batch", "chatgpt")
    assert bad["ok"] is False and "routing guard" in bad["error"]
    # unknown surface
    assert m.spend("x", "nope")["ok"] is False


def test_delegate_routes_and_shapes():
    import mag.frontier_council as m
    d = m.delegate("synthesize our strategic direction for the week")
    assert d["ok"] and d["tier"] == "frontier"
    assert d["surface"] in ("chatgpt", "grok_web")
    assert d["shaped_ask"]  # shaped via elevate
    cheap = m.delegate("process this log batch")
    assert cheap["tier"] == "deepseek" and cheap["surface"] == "deepseek"


def test_council_has_all_members():
    import mag.frontier_council as m
    c = m.council()
    assert c["ok"]
    names = {x["surface"] for x in c["council"]}
    assert {"chatgpt", "grok_web", "grok_x", "deepseek", "vram"} <= names


def test_recommend_self_stolen_chain():
    import mag.frontier_council as m
    # frontier (code planning) -> reasoning shape on a scarce surface
    f = m.recommend("plan the code for the new emulator")
    assert f["ok"] and f["tier"] == "frontier"
    assert f["model_shape"] == "reasoning"
    assert f["surface"] in ("chatgpt", "grok_web")
    # data/maintenance -> cheap shape on deepseek
    d = m.recommend("process this batch of logs")
    assert d["tier"] == "deepseek" and d["surface"] == "deepseek"
    assert d["model_shape"] == "cheap"


def test_route_uses_swarm_surface(monkeypatch):
    import mag.frontier_council as m
    import mag.swarm_surface as ss
    called = {}

    def fake_route(goal, *, surface=None, lens=None, domain=None, provider=None, model=None):
        called["goal"] = goal
        called["surface"] = surface
        return {"ok": True, "surface": surface, "anchor": "q" * 16, "task_id": "t"}

    monkeypatch.setattr(ss, "route_novel", fake_route)
    r = m.route()
    assert r["ok"] is True
    assert called["surface"] == "frontier-council"
    assert "allowance" in called["goal"].lower()
