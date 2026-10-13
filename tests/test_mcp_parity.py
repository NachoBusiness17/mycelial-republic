"""Unit tests for tools/mcp_parity.py — the MCP-2 standing parity check.

Pure comparison-logic tests: fake manifests injected directly into
compare_transport() / evaluate() / format_report(). NO live transport is
contacted (no stdio spawn, no gateway POST, no docker socket) so the suite
runs green on a box where docker and the gateway are dark — the same property
the CLI itself must have via named SKIPs.

Covers the two verdict-neutral residue classes (pin-gate withholds, named
SKIPs) versus the two fail-loud classes (name/digest divergence, profile
mismatch), plus the exit contract 0/1/2 and the R2.0 defect shape (image
rebuilt, container never recreated) as data.
"""
from __future__ import annotations

from tools.mcp_parity import compare_transport, evaluate, format_report, manifest_digest


def tool(name: str, desc: str | None = None, schema: dict | None = None,
         profile: str = "full") -> dict:
    return {
        "name": name,
        "description": desc if desc is not None else f"tool {name}",
        "inputSchema": schema if schema is not None else {"type": "object"},
        "_meta": {"mag": {"profile": profile}},
    }


def row(**overrides):
    """A green stdio-shaped row; tests override the fields under test."""
    base = {
        "transport": "stdio", "status": "ok", "reasons": [],
        "expected_profile": "bridge", "served_profile": "bridge",
        "profile_match": True, "served_count": 3, "host_truth_count": 3,
        "declared_count": 3, "missing": [], "extra": [], "withheld": [],
        "digest_match": True,
    }
    base.update(overrides)
    return base


# ─────────────────────────── compare_transport ──────────────────────────────

def test_ok_when_names_and_digest_match_host_truth():
    truth = [tool("estate_a", profile="bridge"),
             tool("estate_b", profile="bridge")]
    served = [tool("estate_b", profile="bridge"),
              tool("estate_a", profile="bridge")]
    r = compare_transport("stdio", "bridge", served, truth,
                          ["estate_a", "estate_b"])
    assert r["status"] == "ok"
    assert r["missing"] == [] and r["extra"] == []
    assert r["digest_match"] is True
    assert r["served_count"] == 2 and r["host_truth_count"] == 2


def test_missing_names_diverge_and_are_listed():
    truth = [tool("a", profile="archivist"), tool("b", profile="archivist"),
             tool("c", profile="archivist")]
    served = [tool("a", profile="archivist")]
    r = compare_transport("docker", "archivist", served, truth,
                          ["a", "b", "c"])
    assert r["status"] == "diverge"
    assert r["missing"] == ["b", "c"]
    assert any("missing 2: b, c" in reason for reason in r["reasons"])


def test_extra_names_diverge_and_are_listed():
    truth = [tool("a", profile="archivist")]
    served = [tool("a", profile="archivist"),
              tool("zombie_tool", profile="archivist")]
    r = compare_transport("docker", "archivist", served, truth, ["a"])
    assert r["status"] == "diverge"
    assert r["extra"] == ["zombie_tool"]


def test_withheld_pin_gate_names_are_named_but_verdict_neutral():
    # Host truth withholds estate_compile (drift alarm standing); a transport
    # withholding the SAME name is at parity: withheld is residue, not divergence.
    truth = [tool("estate_a"), tool("estate_b")]
    served = [tool("estate_a"), tool("estate_b")]
    r = compare_transport("http", "full", served, truth,
                          ["estate_a", "estate_b", "estate_compile"])
    assert r["status"] == "ok"
    assert r["withheld"] == ["estate_compile"]
    assert r["declared_count"] == 3


def test_profile_mismatch_diverges():
    # Served manifest self-declares _meta.mag.profile=archivist while the
    # deployment promised bridge: the surface serves the wrong projection.
    truth = [tool("estate_a", profile="bridge")]
    served = [tool("list_dir", profile="archivist")]
    r = compare_transport("docker", "bridge", served, truth, ["estate_a"])
    assert r["status"] == "diverge"
    assert r["profile_match"] is False
    assert r["served_profile"] == "archivist"


def test_same_names_different_bytes_diverges_on_digest():
    truth = [tool("a", desc="current description", profile="archivist")]
    served = [tool("a", desc="STALE 2026-09-26 description", profile="archivist")]
    r = compare_transport("docker", "archivist", served, truth, ["a"])
    assert r["status"] == "diverge"
    assert r["digest_match"] is False
    assert any("digest" in reason for reason in r["reasons"])


def test_missing_host_baseline_is_a_named_skip_not_a_silent_pass():
    r = compare_transport("stdio", "bridge", [tool("a")], None, ["a"])
    assert r["status"] == "skip"
    assert "host baseline probe unavailable" in r["skip_reason"]


# ─────────────────────────────── evaluate ───────────────────────────────────

def test_evaluate_diverge_fails_loud_exit_1():
    report = evaluate([row(), row(transport="docker", status="diverge",
                                  reasons=["stale image"])], ["bridge"])
    assert report["verdict"] == "FAIL" and report["exit"] == 1
    assert report["counts"] == {"ok": 1, "diverge": 1, "skip": 0}


def test_evaluate_ok_with_named_skips_passes_exit_0():
    rows = [row(), row(transport="docker", status="skip",
                       skip_reason="127.0.0.1:8766 unreachable — docker down")]
    report = evaluate(rows, ["bridge"])
    assert report["verdict"] == "PASS" and report["exit"] == 0
    assert report["counts"]["skip"] == 1


def test_evaluate_all_skipped_cannot_verify_exit_2():
    rows = [row(transport="stdio", status="skip", skip_reason="x"),
            row(transport="docker", status="skip", skip_reason="y")]
    report = evaluate(rows, ["bridge"])
    assert report["verdict"] == "CANNOT-VERIFY" and report["exit"] == 2


def test_evaluate_withheld_only_rows_stay_pass():
    # The 2026-10-01 live shape: every transport ok, compile withheld on host
    # and transports alike — named residue, green verdict.
    rows = [row(withheld=["estate_thought_compile"], declared_count=7,
                served_count=6, host_truth_count=6),
            row(transport="http", withheld=["estate_thought_compile"],
                declared_count=7, served_count=6, host_truth_count=6)]
    report = evaluate(rows, ["bridge"])
    assert report["verdict"] == "PASS" and report["exit"] == 0


def test_evaluate_ignores_baseline_rows():
    report = evaluate([{"transport": "stdio[full]", "status": "baseline"},
                       row()], ["bridge", "full"])
    assert report["counts"] == {"ok": 1, "diverge": 0, "skip": 0}


# ─────────────────────────── digest + report shape ──────────────────────────

def test_manifest_digest_excludes_meta():
    a = [tool("x", schema={"type": "object", "properties": {}})]
    b = [tool("x", schema={"type": "object", "properties": {}},
              profile="archivist")]
    assert manifest_digest(a) == manifest_digest(b)


def test_manifest_digest_orders_tools():
    assert manifest_digest([tool("a"), tool("b")]) == \
        manifest_digest([tool("b"), tool("a")])


def test_format_report_names_skips_withholds_and_missing():
    report = evaluate(
        [row(withheld=["estate_thought_compile"]),
         row(transport="docker", status="diverge",
             reasons=["missing 1: estate_receipt_append"],
             missing=["estate_receipt_append"]),
         row(transport="http", status="skip",
             skip_reason="127.0.0.1:8001 unreachable — gateway down?")],
        ["bridge"])
    text = format_report(report)
    assert "SKIP" in text and "gateway down" in text
    assert "estate_thought_compile" in text          # withhold named, not buried
    assert "estate_receipt_append" in text           # divergence names the tool
    assert "exit=1" in text


def test_format_report_handles_image_only_row():
    # Manifest probe skipped but docker CLI alive: the standalone docker-image
    # row carries no served/declared counts (regression: KeyError, 2026-10-01).
    img = {"container_image": "sha256:" + "a" * 64,
           "tagged_image": "sha256:" + "a" * 64, "match": True,
           "container": "mag-mcp", "image_ref": "mag-sovereign:local"}
    report = evaluate([{"transport": "docker-image", "status": "ok",
                        "reasons": [], "expected_profile": "-",
                        "image": img}], [])
    text = format_report(report)
    assert "docker-image" in text and "match" in text and "exit=0" in text
