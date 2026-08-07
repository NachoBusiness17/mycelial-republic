"""Plugin surface contract for the dashboard prototype."""
from __future__ import annotations


def test_dashboard_plugin_manifest_and_snapshot():
    from mag.dashboard_plugin import build_dashboard_plugin

    plugin = build_dashboard_plugin()
    manifest = plugin.manifest()
    snapshot = plugin.snapshot(goal="map the dashboard prototype", write=False)

    assert manifest["schema"] == "mag_dashboard_plugin.v1"
    assert "system_map" in manifest["data_contract"]
    assert manifest["endpoints"]["system_map"] == "/api/v1/system-map"
    assert snapshot["plugin"]["name"] == "mag-dashboard"
    assert snapshot["context_pack"]["text"]
    assert snapshot["system_map"]["schema"] == "system_map.v1"
