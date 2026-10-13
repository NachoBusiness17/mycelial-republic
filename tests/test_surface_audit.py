"""Tests for mag.surface_audit — deterministic surface inventory (Surface Hub)."""
from __future__ import annotations

from mag.surface_audit import audit, collect_surfaces


def test_audit_shape():
    a = audit()
    assert a["ok"] is True
    assert a["schema"] == "surface_audit.v1"
    assert a["version"]
    assert a["entries"] > 0
    assert a["verdict"] in ("ready", "attention", "n/a")
    assert isinstance(a["checks"], list)


def test_surfaces_present():
    ids = {s["id"] for s in collect_surfaces()}
    assert {
        "cli", "route_dashboard", "route_cast", "launcher",
        "provider", "loop", "ext_command", "tab",
    } <= ids


def test_surfaces_positive_counts():
    for s in collect_surfaces():
        assert s["count"] >= 0
        assert s["label"]


def test_groups_have_counts():
    a = audit()
    for g in a["groups"]:
        assert "id" in g and "label" in g and "count" in g


def test_surface_total_matches_entries():
    a = audit()
    # cli + dashboard routes + cast routes + providers come from the same render
    surf = {s["id"]: s["count"] for s in a["surfaces"]}
    # entries should at least include cli + route_dashboard + provider kinds
    assert a["entries"] >= surf["cli"] + surf["route_dashboard"] + surf["provider"]
