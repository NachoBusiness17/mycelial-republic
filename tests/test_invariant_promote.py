"""invariant_promote tests (WAVE invariant-percolator, 2026-10-20, wave 2).

Binds tools/invariant_promote.py:
  promoter.assess(canonical, row) -> {promoted, reasons, blockers, count, span_days}
  promoter.plan(invariants, latest, now) -> ledger rows to append
  promoter.load_ledger(path) -> latest verdict per canonical
  promoter.main(["--root", tmp, "--apply"]) -> 0 ok / 2 cannot-verify

The battery pins the two laws the fold rests on:
  1. admission is append-only - invariants.json is never edited by promotion;
  2. promotion is idempotent - re-running on unchanged bytes appends nothing.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import tools.invariant_promote as promoter

TOOL = Path(__file__).resolve().parents[1] / "tools" / "invariant_promote.py"


def _row(**kw) -> dict:
    base = {"text": "operator doctrine line", "count": 3,
            "first_seen": "2026-10-01T00:00:00Z", "last_seen": "2026-10-19T00:00:00Z",
            "domain": "behavioral", "depends_on": []}
    base.update(kw)
    return base


def _estate(tmp_path: Path, invariants: dict) -> Path:
    d = tmp_path / "memory" / "percolator"
    d.mkdir(parents=True, exist_ok=True)
    (d / "invariants.json").write_text(
        json.dumps({"invariants": invariants, "false_positives": 0}), encoding="utf-8")
    return tmp_path


def _ledger(tmp_path: Path) -> Path:
    return tmp_path / "memory" / "percolator" / "promotion_ledger.jsonl"


def test_recurring_doctrine_promotes():
    verdict = promoter.assess("a" * 16, _row())
    assert verdict["promoted"] is True
    assert "count=3" in verdict["reasons"]


def test_single_sighting_never_promotes():
    verdict = promoter.assess("a" * 16, _row(count=1, first_seen="2026-10-19T00:00:00Z",
                                             last_seen="2026-10-19T00:00:00Z"))
    assert verdict["promoted"] is False
    assert "count<2" in verdict["blockers"]
    assert "no-recurrence" in verdict["blockers"]


def test_probe_domain_never_promotes():
    verdict = promoter.assess("a" * 16, _row(domain="probe_cohere", count=9))
    assert verdict["promoted"] is False
    assert "probe-domain" in verdict["blockers"]


def test_instrumentation_vocabulary_never_promotes():
    verdict = promoter.assess("a" * 16, _row(text="backend reported failure", count=21))
    assert verdict["promoted"] is False
    assert "instrumentation-vocabulary" in verdict["blockers"]


def test_two_sources_in_one_cycle_promotes():
    verdict = promoter.assess("a" * 16, _row(
        first_seen="2026-10-19T00:00:00Z", last_seen="2026-10-19T00:10:00Z",
        cycle_hits={"a": "2026-10-19", "b": "2026-10-19"}))
    assert verdict["promoted"] is True
    assert any(r.startswith("recurred(") for r in verdict["reasons"])


def test_plan_is_idempotent(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row()})
    inv = promoter.load_registry(root)
    rows = promoter.plan(inv, {}, "2026-10-20T00:00:00Z")
    assert len(rows) == 1
    ledger = _ledger(tmp_path)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(rows[0]) + "\n", encoding="utf-8")
    latest = promoter.load_ledger(ledger)
    assert promoter.plan(inv, latest, "2026-10-20T01:00:00Z") == []


def test_changed_row_reemits_exactly_one(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row(), "b" * 16: _row()})
    promoter.main(["--root", str(root), "--apply"])
    inv = promoter.load_registry(root)
    inv["a" * 16]["count"] = 4
    rows = promoter.plan(inv, promoter.load_ledger(_ledger(tmp_path)), "2026-10-20T02:00:00Z")
    assert [r["canonical"] for r in rows] == ["a" * 16]


def test_apply_never_edits_the_registry(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row(), "b" * 16: _row(count=1)})
    reg = root / "memory" / "percolator" / "invariants.json"
    before = hashlib.sha256(reg.read_bytes()).hexdigest()
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply"],
                        capture_output=True, text=True)
    assert cp.returncode == 0, cp.stdout + cp.stderr
    assert hashlib.sha256(reg.read_bytes()).hexdigest() == before


def test_apply_appends_and_second_run_writes_zero(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row(), "b" * 16: _row(count=1)})
    subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply"],
                   capture_output=True, text=True, check=True)
    lines_first = _ledger(tmp_path).read_text(encoding="utf-8").splitlines()
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply", "--json"],
                        capture_output=True, text=True, check=True)
    receipt = json.loads(cp.stdout)
    lines_second = _ledger(tmp_path).read_text(encoding="utf-8").splitlines()
    assert len(lines_first) == 2
    assert receipt["written"] == 0
    assert len(lines_second) == 2


def test_dry_run_writes_nothing(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row()})
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--json"],
                        capture_output=True, text=True)
    receipt = json.loads(cp.stdout)
    assert cp.returncode == 0
    assert receipt["applied"] is False
    assert receipt["pending"] == 1
    assert not _ledger(tmp_path).exists()


def test_missing_registry_exits_2(tmp_path):
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(tmp_path)],
                        capture_output=True, text=True)
    assert cp.returncode == 2, cp.stdout + cp.stderr
    assert cp.stdout.startswith("PERCOLATOR-PROMOTE: UNVERIFIABLE")


def test_ledger_survives_a_malformed_line(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row()})
    ledger = _ledger(tmp_path)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text("{not json}\n", encoding="utf-8")
    assert promoter.load_ledger(ledger) == {}
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply"],
                        capture_output=True, text=True)
    assert cp.returncode == 0
    assert len(ledger.read_text(encoding="utf-8").splitlines()) == 2


# --- policy v2: tool-guard vocabulary and compact re-emission -----------------

def test_tool_guard_strings_are_blocked_in_v2():
    verdict = promoter.assess("a" * 16, _row(
        text="write_file missing path= - emit flat JSON (sibling keys, not nested arguments)"))
    assert verdict["promoted"] is False
    assert "instrumentation-vocabulary" in verdict["blockers"]


def test_policy_change_does_not_respam_blocked_rows(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row(count=1), "b" * 16: _row()})
    stale = {"a" * 16: {"promoted": False, "policy_sha": "old", "row_hash": "x"},
             "b" * 16: {"promoted": True, "policy_sha": "old", "row_hash": "y"}}
    inv = promoter.load_registry(root)
    # row hashes in the stale ledger do not match, so both re-emit - the test that
    # matters is with MATCHING row hashes:
    stale["a" * 16]["row_hash"] = promoter.row_hash("a" * 16, inv["a" * 16])
    stale["b" * 16]["row_hash"] = promoter.row_hash("b" * 16, inv["b" * 16])
    rows = promoter.plan(inv, stale, "2026-10-20T03:00:00Z")
    assert [r["canonical"] for r in rows] == ["b" * 16]


def test_export_lists_promoted_rows_only(tmp_path):
    root = _estate(tmp_path, {"a" * 16: _row(), "b" * 16: _row(count=1)})
    promoter.main(["--root", str(root), "--apply"])
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--export"],
                        capture_output=True, text=True)
    assert cp.returncode == 0, cp.stdout + cp.stderr
    body = (root / "memory" / "percolator" / "PROMOTED_INVARIANTS.md").read_text(encoding="utf-8")
    assert "surface: 1 of 2 registry rows promoted" in body
    assert "operator doctrine line" in body
    assert "one off" not in body
    assert "| 3 | behavioral | operator doctrine line | MISSING |" in body
    assert "Kill conditions: 0 checkable, 0 manual debts, 1 missing." in body
