"""Launch-plan and room-bridge tests; no Vast/network/process calls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import blade_plan  # noqa: E402
from watch import blade_room_bridge  # noqa: E402


def test_plan_uses_registry_rate_and_covenant_ttl(monkeypatch, tmp_path):
    templates = tmp_path / "templates.json"
    covenant = tmp_path / "covenant.json"
    boot = tmp_path / "boot.log"
    templates.write_text(json.dumps({"default": "qwen", "templates": [{"name": "qwen", "dph": 0.07}]}))
    covenant.write_text(json.dumps({"blade_lifetime_h": 4, "buyer_enabled": False}))
    boot.write_text("\n".join([
        "[boot 01:00:00] watching instance 1 template=qwen",
        "[boot 01:01:00] phase: None -> pull",
        "[boot 01:03:00] phase: pull -> READY",
        "[boot 02:00:00] watching instance 2 template=qwen",
        "[boot 02:01:00] phase: None -> pull",
        "[boot 02:04:00] phase: pull -> READY",
        "[boot 03:00:00] watching instance 3 template=qwen",
        "[boot 03:01:00] phase: None -> pull",
        "[boot 03:05:00] phase: pull -> READY",
    ]))
    monkeypatch.setattr(blade_plan, "TEMPLATES", templates)
    monkeypatch.setattr(blade_plan, "COVENANT", covenant)
    monkeypatch.setattr(blade_plan, "BOOT_LOG", boot)
    plan = blade_plan.make_plan("qwen", "batch")
    assert plan["expected_boot_min"] == 3
    assert plan["dph"] == 0.07
    assert plan["est_cost"] == 0.28


def test_short_history_is_explicitly_unestimated(monkeypatch, tmp_path):
    monkeypatch.setattr(blade_plan, "TEMPLATES", tmp_path / "templates.json")
    monkeypatch.setattr(blade_plan, "COVENANT", tmp_path / "covenant.json")
    monkeypatch.setattr(blade_plan, "BOOT_LOG", tmp_path / "boot.log")
    blade_plan.TEMPLATES.write_text(json.dumps({"default": "qwen", "templates": [{"name": "qwen", "dph": 0.1}]}))
    blade_plan.COVENANT.write_text(json.dumps({"blade_lifetime_h": 4}))
    blade_plan.BOOT_LOG.write_text("[boot 01:00:00] watching instance 1\n[boot 01:01:00] phase: None -> pull\n[boot 01:02:00] phase: pull -> READY\n")
    plan = blade_plan.make_plan("qwen", "batch")
    assert plan["expected_boot_min"] is None
    assert plan["expected_boot_note"] == "no history yet"


def test_bridge_posts_only_new_lifecycle_lines(monkeypatch, tmp_path):
    buyer, boot, room, state = (tmp_path / x for x in ("buyer.log", "boot.log", "room.jsonl", "state.json"))
    buyer.write_text("[blade 01:00:00] blade contract 12\n[blade 01:01:00] proxy-dark — destroying\n")
    boot.write_text("[boot 01:00:00] phase: pull -> READY\n")
    monkeypatch.setattr(blade_room_bridge, "SOURCES", (buyer, boot))
    monkeypatch.setattr(blade_room_bridge, "ROOM", room)
    monkeypatch.setattr(blade_room_bridge, "STATE", state)
    blade_room_bridge.run()
    rows = [json.loads(line) for line in room.read_text().splitlines()]
    assert [row["event"] for row in rows] == ["contract_signed", "proxy_dark", "ready"]
    blade_room_bridge.run()
    assert len(room.read_text().splitlines()) == 3
