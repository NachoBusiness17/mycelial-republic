"""invariant_percolator_audit tests (WAVE invariant-percolator, 2026-10-20).

Binds tools/invariant_percolator_audit.py:
  ipa.load(root) -> (registry dict, explore rows)
  ipa.audit(registry, explore) -> (gate results, stats)
  ipa.main(["--root", tmp]) -> exit 0 green / 1 violated / 2 cannot-verify

The battery is the executable spec for the wave's thesis: a registry that compiles
first sightings is not a registry of invariants. Every case is synthetic bytes on a
tmp estate -- no dependence on the live registry, which changes by the minute.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import tools.invariant_percolator_audit as ipa

TOOL = Path(__file__).resolve().parents[1] / "tools" / "invariant_percolator_audit.py"


def _estate(tmp_path: Path, invariants: dict, explore: list[dict]) -> Path:
    d = tmp_path / "memory" / "percolator"
    d.mkdir(parents=True, exist_ok=True)
    (d / "invariants.json").write_text(
        json.dumps({"invariants": invariants, "false_positives": 0}), encoding="utf-8")
    (d / "explore.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in explore), encoding="utf-8")
    return tmp_path


def _green_registry(n: int = 20) -> dict:
    return {
        f"{i:016x}": {"text": f"operator doctrine line {i}", "count": 3, "domain": "behavioral",
                       "first_seen": "2026-10-01T00:00:00Z", "last_seen": "2026-10-19T00:00:00Z",
                       "depends_on": ["aaaa"] if i % 5 == 0 else []}
        for i in range(n)
    }


def _green_explore(n: int = 10, open_n: int = 2) -> list[dict]:
    return [{"ts": "2026-10-19T00:00:00Z", "status": "open" if i < open_n else "done"}
            for i in range(n)]


def test_green_estate_passes_all_gates(tmp_path):
    root = _estate(tmp_path, _green_registry(), _green_explore())
    results, stats = ipa.audit(*ipa.load(root))
    assert [r["id"] for r in results if not r["ok"]] == []
    assert stats["invariants"] == 20
    assert stats["repeat_share_pct"] == 100.0


def test_first_sighting_compiled_as_invariant_fails_i1(tmp_path):
    reg = _green_registry(10)
    reg["deadbeefdeadbeef"] = {"text": "pro-1a2b3c4d -> ok", "count": 1, "domain": "behavioral",
                               "first_seen": "2026-10-20T00:00:00Z",
                               "last_seen": "2026-10-20T00:00:00Z", "depends_on": []}
    results, _ = ipa.audit(*ipa.load(_estate(tmp_path, reg, _green_explore())))
    i1 = next(r for r in results if r["id"] == "I1")
    assert i1["ok"] is False
    assert "1/11" in i1["detail"]
    assert i1["offenders"][0]["canonical"] == "deadbeefdeadbeef"


def test_probe_chatter_fails_i3(tmp_path):
    reg = _green_registry(10)
    for i in range(6):
        reg[f"p{i:015x}"] = {"text": f"I never imagined {i}", "count": 2, "domain": "probe_cohere",
                             "first_seen": "2026-10-01T00:00:00Z",
                             "last_seen": "2026-10-19T00:00:00Z", "depends_on": []}
    results, _ = ipa.audit(*ipa.load(_estate(tmp_path, reg, _green_explore())))
    i3 = next(r for r in results if r["id"] == "I3")
    assert i3["ok"] is False
    assert "6/16" in i3["detail"]


def test_unclassified_stale_rows_fail_i4(tmp_path):
    # wave 6: "open share" was replaced by "open rows past the age bar that the
    # decay ledger has not classified". Old rows with no decay ledger = FAIL.
    old = _green_explore(n=10, open_n=9)
    for row in old:
        row["ts"] = "2026-09-01T00:00:00Z"   # 50 days before the fixture clock
    results, _ = ipa.audit(*ipa.load(_estate(tmp_path, _green_registry(), old)))
    i4 = next(r for r in results if r["id"] == "I4")
    assert i4["ok"] is False
    assert "unclassified" in i4["detail"]


def test_decayed_stale_rows_pass_i4(tmp_path):
    old = _green_explore(n=10, open_n=9)
    for row in old:
        row["ts"] = "2026-09-01T00:00:00Z"
        row["canonical"] = f"c{old.index(row)}"
    root = _estate(tmp_path, _green_registry(), old)
    ledger = root / "memory" / "percolator" / "explore_decay.jsonl"
    ledger.write_text("".join(
        json.dumps({"schema": "explore_decay.v1", "canonical": f"c{i}"}) + "\n"
        for i in range(9)), encoding="utf-8")
    results, stats = ipa.audit(*ipa.load(root), decayed={f"c{i}" for i in range(9)})
    i4 = next(r for r in results if r["id"] == "I4")
    assert i4["ok"] is True, i4
    assert stats["explore_stale_classified"] == 9


def test_leaf_rows_pass_i5(tmp_path):
    # wave 7: a leaf (nothing depends on it, it declares nothing) is where an
    # observation lands - that is not a defect.
    reg = {k: dict(v, depends_on=[]) for k, v in _green_registry().items()}
    results, _ = ipa.audit(*ipa.load(_estate(tmp_path, reg, _green_explore())))
    i5 = next(r for r in results if r["id"] == "I5")
    assert i5["ok"] is True, i5


def test_depended_on_but_silent_fails_i5(tmp_path):
    # the real failure class: something depends on this row, yet it declares nothing
    reg = {k: dict(v, depends_on=[]) for k, v in _green_registry().items()}
    keys = sorted(reg)
    reg[keys[0]]["depends_on"] = [keys[1]]
    results, _ = ipa.audit(*ipa.load(_estate(tmp_path, reg, _green_explore())))
    i5 = next(r for r in results if r["id"] == "I5")
    assert i5["ok"] is False
    assert "undeclared" in i5["detail"]


def test_cli_exit_0_on_green(tmp_path):
    root = _estate(tmp_path, _green_registry(), _green_explore())
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root)],
                        capture_output=True, text=True)
    assert cp.returncode == 0, cp.stdout + cp.stderr
    assert cp.stdout.startswith("PERCOLATOR-AUDIT: ok")


def test_cli_exit_1_and_names_each_failed_gate(tmp_path):
    reg = {k: dict(v, depends_on=[]) for k, v in _green_registry().items()}
    reg["0" * 16] = {"text": "one off", "count": 1, "domain": "probe_x",
                     "first_seen": "2026-10-20T00:00:00Z", "last_seen": "2026-10-20T00:00:00Z",
                     "depends_on": []}
    root = _estate(tmp_path, reg, _green_explore(n=10, open_n=9))
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root)],
                        capture_output=True, text=True)
    assert cp.returncode == 1, cp.stdout + cp.stderr
    assert cp.stdout.startswith("PERCOLATOR-AUDIT: VIOLATED")
    tail = cp.stdout.strip().splitlines()[-1]
    assert "I1" in tail


def test_cli_exit_2_when_registry_absent(tmp_path):
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(tmp_path)],
                        capture_output=True, text=True)
    assert cp.returncode == 2, cp.stdout + cp.stderr
    assert cp.stdout.startswith("PERCOLATOR-AUDIT: UNVERIFIABLE")


def test_cli_json_receipt_is_machine_readable(tmp_path):
    root = _estate(tmp_path, _green_registry(), _green_explore())
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--json"],
                        capture_output=True, text=True)
    receipt = json.loads(cp.stdout)
    assert receipt["schema"] == "percolator_audit.v1"
    assert receipt["status"] == "green"
    assert {g["id"] for g in receipt["gates"]} == {"I1", "I2", "I3", "I4", "I5"}


# --- promoted surface (wave 2): one policy, two readers -----------------------

def _promoted_estate(tmp_path: Path) -> Path:
    """Reg drops one eligible row; the promote tool writes the ledger for it."""
    import subprocess as sp

    reg = {"a" * 16: {"text": "operator doctrine line", "count": 4, "domain": "behavioral",
                      "first_seen": "2026-10-01T00:00:00Z",
                      "last_seen": "2026-10-19T00:00:00Z", "depends_on": []},
           "b" * 16: {"text": "one off", "count": 1, "domain": "behavioral",
                      "first_seen": "2026-10-20T00:00:00Z",
                      "last_seen": "2026-10-20T00:00:00Z", "depends_on": []}}
    root = _estate(tmp_path, reg, _green_explore())
    promote = Path(__file__).resolve().parents[1] / "tools" / "invariant_promote.py"
    sp.run([sys.executable, str(promote), "--root", str(root), "--apply"],
           capture_output=True, text=True, check=True)
    return root


def test_promoted_only_filters_to_ledger_rows(tmp_path):
    root = _promoted_estate(tmp_path)
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root),
                         "--promoted-only", "--json"], capture_output=True, text=True)
    receipt = json.loads(cp.stdout)
    assert receipt["surface"].startswith("promoted")
    assert receipt["stats"]["invariants"] == 1


def test_promoted_only_without_ledger_exits_2(tmp_path):
    root = _estate(tmp_path, _green_registry(), _green_explore())
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--promoted-only"],
                        capture_output=True, text=True)
    assert cp.returncode == 2, cp.stdout + cp.stderr
    assert cp.stdout.startswith("PERCOLATOR-AUDIT: UNVERIFIABLE")
