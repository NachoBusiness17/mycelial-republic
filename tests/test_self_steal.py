"""Self-steal must recognize successful centralized dogfood evidence."""
from __future__ import annotations

import json


def test_dogfood_receipt_counts_as_capability_evidence(tmp_path, monkeypatch):
    from mag import self_steal

    report = tmp_path / "report.jsonl"
    report.write_text(json.dumps({
        "results": [
            {"system": "archetype_image", "ok": True},
            {"system": "ecosystem_surface", "ok": False},
        ]
    }) + "\n", encoding="utf-8")
    monkeypatch.setattr(self_steal, "DOGFOOD_REPORT", report)

    assert self_steal._dogfood_mtime("archetype_image") > 0
    assert self_steal._dogfood_mtime("ecosystem_surface") == 0
    assert self_steal._dogfood_mtime("archetype") == 0


def test_surface_steal_leaves_bounded_receipt(tmp_path, monkeypatch):
    from mag import surface_steal

    monkeypatch.setattr(surface_steal, "STEAL_DIR", tmp_path)
    monkeypatch.setattr(surface_steal, "related_nodes", lambda *_args: [{"label": "known"}])
    monkeypatch.setattr(surface_steal, "steal_docs", lambda *_args: [])
    monkeypatch.setattr(surface_steal, "lingering", lambda *_args: ["keep"])

    out = surface_steal.surface("a deliberately bounded ask", limit=2)
    assert out["ok"] is True
    row = json.loads((tmp_path / "surface_receipts.jsonl").read_text(encoding="utf-8"))
    assert row["schema"] == "surface_steal.receipt.v1"
    assert "ask" not in row
