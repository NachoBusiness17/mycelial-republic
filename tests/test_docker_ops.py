"""Tests for mag/docker_ops — the deterministic Docker containment probe + launch path.

These tests verify STRUCTURE and SAFETY (report-only cadence, never auto-ups/downs),
not that Docker is running — probe()/status() must not crash whether or not the
engine is reachable.
"""

import json
from pathlib import Path

from mag import docker_ops

ROOT = Path(docker_ops.ROOT)


def test_probe_shape():
    p = docker_ops.probe()
    assert p["schema"] == "docker_ops.probe.v1"
    for key in ("engine", "compose_file", "compose_valid", "containers",
                "container_count", "native_port_conflicts", "cutover_ready"):
        assert key in p, key
    assert isinstance(p["containers"], list)
    assert isinstance(p["native_port_conflicts"], list)


def test_status_shape_and_verdict():
    s = docker_ops.status()
    assert s["schema"] == "docker_ops.status.v1"
    assert s["verdict"] in ("ready", "running", "engine_down", "compose_invalid", "port_conflict")
    # verdict must be consistent with cutover_ready
    if s["cutover_ready"]:
        assert s["verdict"] in ("ready", "running")
    else:
        assert s["verdict"] != "ready"


def test_compose_file_is_valid_target():
    # The module must point at the real compose file in the repo.
    assert docker_ops.COMPOSE == ROOT / "docker-compose.yml"
    assert ROOT.joinpath("docker-compose.yml").is_file()


def test_cadence_is_report_only():
    # run_cadence must NOT mutate (no containers created/torn down). It only probes
    # and logs. We assert it returns a probe-shaped dict and does not change state.
    before = docker_ops.status()
    cad = docker_ops.run_cadence()
    after = docker_ops.status()
    assert cad["schema"] == "docker_ops.probe.v1"
    # engine reachability should be stable across a report-only cadence tick
    assert cad["engine"].get("reachable") == after["engine"].get("reachable")
    assert cad["container_count"] == before["container_count"]


def test_main_dispatch_returns_something_for_each_cmd():
    import io
    import sys as _sys

    for cmd in ("status", "probe"):
        buf = io.StringIO()
        old = _sys.stdout
        _sys.stdout = buf
        try:
            docker_ops.main([cmd])
        finally:
            _sys.stdout = old
        try:
            json.loads(buf.getvalue())
        except Exception as e:  # pragma: no cover - only on regressions
            raise AssertionError(f"main(['{cmd}']) did not print valid JSON: {e}")
