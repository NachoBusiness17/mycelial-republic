from mag.openclaw_catalog import CROWN, compile_catalog


def test_compile_lists_memlance_and_scan(tmp_path, monkeypatch):
    from mag import openclaw_catalog as oc
    monkeypatch.setattr(oc, "OUT", tmp_path / "latest.json")
    out = compile_catalog()
    assert out["ok"] is True
    ids = {c["id"] for c in out["crown"]}
    assert {"memlance", "verkle-lance", "steer", "dnd", "mermaid", "lab"} <= ids
    assert out["scanned_cli_n"] > 50
    blob = (tmp_path / "latest.json").read_text(encoding="utf-8")
    assert "ghost_memlance" in blob
    assert "surface_render" in blob
    from mag.openclaw_catalog import compile_fabric
    fab = compile_fabric()
    assert fab["n_nodes"] >= 16
    ids = {n["id"] for n in fab["nodes"]}
    assert "memlance" in ids and "agent-tools" in ids
    mem = next(n for n in fab["nodes"] if n["id"] == "memlance")
    assert "select" in mem["subtools"] or "index" in mem["subtools"]
