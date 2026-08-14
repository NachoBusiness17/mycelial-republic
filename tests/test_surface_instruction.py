"""Stateless tests for surface_instruction — one shape, rendered rightsized to the surface.
RIB: surface_instruction.v1 — onboarding(module) canonical start; render(module, surface) same shape
rightsized (vscode=tools, generic_ai=plaintext prompt); ingest(artifact) reversible; trigger(chat)
content-gated 'dnd' -> loads the DND module; route() via swarm_surface. Stateless: no disk, no
framework dependency (only pure string building)."""
from __future__ import annotations


def test_onboarding_canonical():
    import mag.surface_instruction as m
    o = m.onboarding("dnd")
    assert o["ok"] and o["module"] == "dungeon_dev"
    assert o["name"] == "the Dungeon"
    assert len(o["shape_laws"]) == 8


def test_render_generic_ai_is_self_contained_prompt():
    import mag.surface_instruction as m
    r = m.render("dnd", "generic_ai")
    assert r["ok"] and r["surface"] == "generic_ai"
    assert r["surface_kind"] == "self-contained-prompt"
    a = r["artifact"]
    assert "you are the engine" in a.lower()
    assert "begin. show the party" in a.lower()  # actionable start
    # self-contained: no framework import assumed, shape laws present
    assert "evidence over self-report" in a.lower()
    assert "never capture" in a.lower()


def test_render_vscode_uses_tools():
    import mag.surface_instruction as m
    r = m.render("dnd", "vscode")
    assert r["ok"] and r["surface"] == "vscode"
    assert r["surface_kind"] == "framework-native"
    a = r["artifact"]
    assert "dungeon_dev" in a  # hands the module name
    assert "use them" in a.lower()  # uses the surface's tools, does not simulate


def test_ingest_is_reversible():
    import mag.surface_instruction as m
    generic = m.render("dnd", "generic_ai")["artifact"]
    g = m.ingest(generic)
    assert g["ok"] and g["module"] == "dnd" and g["surface"] == "generic_ai"
    vscode = m.render("dnd", "vscode")["artifact"]
    v = m.ingest(vscode)
    assert v["ok"] and v["module"] == "dnd" and v["surface"] == "vscode"


def test_trigger_content_gated_dnd():
    import mag.surface_instruction as m
    t = m.trigger("can we play dnd")
    assert t["ok"] and t["module"] == "dungeon_dev"
    # no signal -> does not fire
    t2 = m.trigger("hello world")
    assert t2["ok"] is False and t2.get("fired") is False


def test_route_uses_swarm_surface(monkeypatch):
    import mag.surface_instruction as m
    import mag.swarm_surface as ss
    called = {}

    def fake_route(goal, *, surface=None, lens=None, domain=None, provider=None, model=None):
        called["goal"] = goal
        called["surface"] = surface
        return {"ok": True, "surface": surface, "anchor": "z" * 16, "task_id": "t"}

    monkeypatch.setattr(ss, "route_novel", fake_route)
    r = m.route()
    assert r["ok"] is True
    assert called["surface"] == "surface-instruction"
    assert "rightsized" in called["goal"].lower()
