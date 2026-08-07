"""Pytest-visible routing smoke for VS Code Test Explorer."""
from __future__ import annotations


def test_routing_smoke_contract():
    from scripts.routing_smoke import main

    assert main() == 0