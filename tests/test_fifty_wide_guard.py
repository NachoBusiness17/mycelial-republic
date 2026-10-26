"""Fifty-wide guard tests (GO item 8, D1 ruling, 2026-10-04).

Cause and evidence this pins (watch/inbox/burn_claims_50wide_20261003.md;
corpus/steal/MASTER_MICKEY17_V2.md section 7 D1): the 2026-10-03 fifty-wide
burn wave fired 50 lanes while the extraction artifact held 60 units, so 10
units carried no verdict and no artifact explained the drop; the em-dash
mechanism was refuted (2 measured, never 10). The guard
(tools/fifty_wide_guard.py) is the countermeasure: a dispatch may fire only
when the extraction unit count equals the lane count, a mismatch fails loud
with the dropped-unit list printed to stdout and appended to the wave receipt,
and every passing pre-flight banks a replayable dispatch-log row.

Bands: the clean fixture passes and writes the log row; a known dropped unit
fails exit 1 with the unit named on stdout and in the receipt; unknown plan
keys and duplicate plan keys fail even when lengths match; an explicit --lanes
mismatch fails; missing and unparseable inputs fail closed exit 2; and the CLI
exit codes are pinned through a subprocess against a synthetic mini-estate in
tmp_path.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tools.fifty_wide_guard as fwg

REPO = Path(__file__).resolve().parents[1]


def _write_units(tmp_path: Path, keys: list[tuple[str, int]]) -> Path:
    p = tmp_path / "units.json"
    p.write_text(
        json.dumps([{"file": f, "line": n, "claim": "c"} for f, n in keys], ensure_ascii=False),
        encoding="utf-8",
    )
    return p


def _write_plan(tmp_path: Path, entries: list, name: str = "plan.json") -> Path:
    # name is a parameter because two plans in one tmp_path must not share a
    # filename: same-path writes clobber the first plan before the subprocess
    # reads it (caught live 2026-10-04: the CLI pass case read the short plan).
    p = tmp_path / name
    p.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    return p


def _run(units: Path, plan: Path, *extra: str) -> int:
    # Fail-path calls never reach the log append (the guard logs on pass only),
    # so only the clean test needs --log to keep writes inside tmp_path.
    return fwg.run(["--units", str(units), "--plan", str(plan), *extra])


def test_clean_fixture_passes_and_banks_log_row(tmp_path, capsys):
    units = _write_units(tmp_path, [("a.md", 1), ("a.md", 2), ("b.md", 7)])
    plan = _write_plan(tmp_path, ["a.md:1", "a.md:2", "b.md:7"])
    log = tmp_path / "dispatch_log.jsonl"
    rc = _run(units, plan, "--log", str(log))
    out = capsys.readouterr().out
    assert rc == fwg.EXIT_PASS
    assert "3 units == 3 lanes" in out
    rows = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["units_count"] == 3 and rows[0]["lanes"] == 3
    assert rows[0]["units_sha256"] and rows[0]["moment"].endswith("Z")


def test_dropped_unit_fails_loud_printing_the_unit(tmp_path, capsys):
    units = _write_units(tmp_path, [("a.md", 1), ("a.md", 2), ("b.md", 7), ("b.md", 9)])
    plan = _write_plan(tmp_path, ["a.md:1", "a.md:2", "b.md:7"])
    receipt = tmp_path / "wave.md"
    receipt.write_text("# wave receipt\n", encoding="utf-8")
    rc = fwg.run(["--units", str(units), "--plan", str(plan), "--receipt", str(receipt), "--no-log"])
    out = capsys.readouterr().out
    assert rc == fwg.EXIT_FAIL
    assert "FIFTY-WIDE GUARD: FAIL" in out
    assert "4 units" in out and "3 lanes" in out
    assert "b.md:9" in out, "the dropped unit key must print on stdout"
    body = receipt.read_text(encoding="utf-8")
    assert "fifty-wide guard FAIL" in body
    assert "DROPPED UNITS (1" in body and "b.md:9" in body


def test_unknown_plan_key_fails_even_when_lengths_match(tmp_path, capsys):
    units = _write_units(tmp_path, [("a.md", 1), ("a.md", 2)])
    plan = _write_plan(tmp_path, ["a.md:1", "zzz.md:404"])
    rc = _run(units, plan)
    out = capsys.readouterr().out
    assert rc == fwg.EXIT_FAIL
    assert "zzz.md:404" in out


def test_duplicate_plan_key_fails(tmp_path, capsys):
    units = _write_units(tmp_path, [("a.md", 1), ("a.md", 2)])
    plan = _write_plan(tmp_path, ["a.md:1", "a.md:1"])
    rc = _run(units, plan)
    out = capsys.readouterr().out
    assert rc == fwg.EXIT_FAIL
    assert "duplicate plan keys" in out


def test_explicit_lanes_mismatch_fails(tmp_path, capsys):
    units = _write_units(tmp_path, [("a.md", 1), ("a.md", 2), ("b.md", 3)])
    plan = _write_plan(tmp_path, ["a.md:1", "a.md:2", "b.md:3"])
    rc = _run(units, plan, "--lanes", "50")
    out = capsys.readouterr().out
    assert rc == fwg.EXIT_FAIL
    assert "3 units" in out and "50 lanes" in out


def test_missing_units_file_fails_closed(tmp_path, capsys):
    plan = _write_plan(tmp_path, ["a.md:1"])
    rc = fwg.run(["--units", str(tmp_path / "nope.json"), "--plan", str(plan), "--no-log"])
    out = capsys.readouterr().out
    assert rc == fwg.EXIT_CANNOT_VERIFY
    assert "CANNOT-VERIFY" in out


def test_unparseable_plan_fails_closed(tmp_path, capsys):
    units = _write_units(tmp_path, [("a.md", 1)])
    bad = tmp_path / "plan.json"
    bad.write_text("{not json", encoding="utf-8")
    rc = fwg.run(["--units", str(units), "--plan", str(bad), "--no-log"])
    assert rc == fwg.EXIT_CANNOT_VERIFY


def test_non_dict_unit_without_identity_fails_closed(tmp_path, capsys):
    units = tmp_path / "units.json"
    units.write_text(json.dumps(["just a string"]), encoding="utf-8")
    plan = _write_plan(tmp_path, ["just a string"])
    rc = fwg.run(["--units", str(units), "--plan", str(plan), "--no-log"])
    assert rc == fwg.EXIT_FAIL
    assert "identity error" in capsys.readouterr().out


def test_unit_and_plan_key_shapes_agree():
    assert fwg.unit_key({"file": "a.md", "line": 3}) == "a.md:3"
    assert fwg.plan_entry_key("a.md:3") == "a.md:3"
    assert fwg.plan_entry_key(["a.md", 3]) == "a.md:3"
    assert fwg.plan_entry_key({"file": "a.md", "line": 3}) == "a.md:3"
    assert fwg.unit_key({"id": "u7"}) == "u7"


def test_cli_exit_codes_pinned_through_subprocess(tmp_path):
    units = _write_units(tmp_path, [("a.md", 1), ("a.md", 2)])
    good = _write_plan(tmp_path, ["a.md:1", "a.md:2"], name="plan_good.json")
    short = _write_plan(tmp_path, ["a.md:1"], name="plan_short.json")
    base = [str(REPO / "tools" / "fifty_wide_guard.py"), "--no-log"]
    r_pass = subprocess.run(
        [sys.executable, *base, "--units", str(units), "--plan", str(good)],
        capture_output=True, text=True, timeout=60,
    )
    r_fail = subprocess.run(
        [sys.executable, *base, "--units", str(units), "--plan", str(short)],
        capture_output=True, text=True, timeout=60,
    )
    r_cant = subprocess.run(
        [sys.executable, *base, "--units", str(tmp_path / "gone.json"), "--plan", str(good)],
        capture_output=True, text=True, timeout=60,
    )
    assert (r_pass.returncode, r_fail.returncode, r_cant.returncode) == (0, 1, 2)
