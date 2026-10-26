"""Fifty-wide archive tests (a07 operator-owed item made mechanical, 2026-10-04).

Cause and evidence this pins (watch/inbox/go_wave_20261004/fifty_wide_guard.md
section 7): the 2026-10-03 fifty-wide burn wave lost 10 units and no per-agent
artifact existed on disk to explain the drop; per-agent retention was filed as
an operator-owed convention. The archive tool (tools/fifty_wide_archive.py)
makes it mechanical: one post-wave run writes each agent report to
memory/runs/fifty_wide/<wave>/agents/<lane>.md, banks a manifest.jsonl row
{wave, lane, file, sha256, ts}, and re-archiving identical bytes is a no-op
by sha.

Bands: labeled-block and JSONL inputs both archive with correct manifest rows
{wave, lane, file, sha256, bytes, ts}; archive-then-rearchive is a byte no-op
(zero new rows, file untouched); changed bytes for a lane rewrite the file and
append a fresh row; empty input, duplicate lanes, headerless content, and
empty bodies fail exit 1; a missing input file and a corrupt manifest fail
closed exit 2; wave slugs and lane labels sanitize to safe path components;
the CLI exit codes plus stdin feeding are pinned through a subprocess; and
verify mode re-hashes each lane against the manifest and joins the guard's
dispatch-log row: a clean pair verifies exit 0 (rows without the bytes field,
i.e. pre-2026-10-18 manifests, still verify), a tampered or missing lane file
is SHA-DRIFT exit 1, and a banked-vs-dispatched count gap is exit 1.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import tools.fifty_wide_archive as fwa
import tools.fifty_wide_guard as fwg

REPO = Path(__file__).resolve().parents[1]

BLOCKS = """=== lane-alpha ===
alpha report body

=== lane-beta ===
beta report body
"""

JSONL = (
    '{"lane": "lane-alpha", "report": "alpha report body"}\n'
    '{"lane": "lane-beta", "report": "beta report body"}\n'
)


def _write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def _manifest_rows(base: Path, wave: str) -> list[dict]:
    m = base / wave / "manifest.jsonl"
    return [json.loads(l) for l in m.read_text(encoding="utf-8").splitlines() if l.strip()]


def _agent(base: Path, wave: str, lane: str) -> Path:
    return base / wave / "agents" / f"{lane}.md"


def test_blocks_archive_writes_files_and_correct_manifest_rows(tmp_path):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    rc = fwa.run(["--wave", "demo_wave", "--input", str(src), "--dir", str(base)])
    assert rc == fwa.EXIT_PASS
    a, b = _agent(base, "demo_wave", "lane-alpha"), _agent(base, "demo_wave", "lane-beta")
    assert a.read_text(encoding="utf-8") == "alpha report body"
    assert b.read_text(encoding="utf-8") == "beta report body"
    rows = _manifest_rows(base, "demo_wave")
    assert len(rows) == 2
    for row, lane, path in zip(rows, ("lane-alpha", "lane-beta"), (a, b)):
        assert set(row) == {"wave", "lane", "file", "sha256", "bytes", "ts"}
        assert row["wave"] == "demo_wave" and row["lane"] == lane
        assert row["file"], "manifest row must name the archived file"
        assert row["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert row["bytes"] == len(path.read_bytes())
        assert row["ts"].endswith("Z")


def test_jsonl_input_archives_the_same_way(tmp_path):
    src = _write(tmp_path, "reports.jsonl", JSONL)
    base = tmp_path / "fifty_wide"
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    assert rc == fwa.EXIT_PASS
    assert _agent(base, "w", "lane-alpha").read_text(encoding="utf-8") == "alpha report body"
    rows = _manifest_rows(base, "w")
    assert [r["lane"] for r in rows] == ["lane-alpha", "lane-beta"]


def test_rearchive_same_bytes_is_a_full_noop(tmp_path, capsys):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    first = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    rows_after_first = _manifest_rows(base, "w")
    agent = _agent(base, "w", "lane-alpha")
    mtime_before = agent.stat().st_mtime_ns
    second = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    out = capsys.readouterr().out
    assert (first, second) == (fwa.EXIT_PASS, fwa.EXIT_PASS)
    assert out.splitlines()[0] == "ARCHIVED 2/2", "the first run archives both lanes"
    assert "ARCHIVED 0/2" in out, "the re-run must report zero newly written lanes"
    assert "unchanged (sha match): lane-alpha" in out
    assert agent.read_bytes() == b"alpha report body"
    assert agent.stat().st_mtime_ns == mtime_before, "a sha match must not rewrite the file"
    assert _manifest_rows(base, "w") == rows_after_first, "a sha match must not bank a row"


def test_changed_bytes_rewrite_the_file_and_append_a_fresh_row(tmp_path):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    src.write_text(BLOCKS.replace("alpha report body", "alpha REVISED"), encoding="utf-8")
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    assert rc == fwa.EXIT_PASS
    assert _agent(base, "w", "lane-alpha").read_text(encoding="utf-8") == "alpha REVISED"
    rows = _manifest_rows(base, "w")
    assert len(rows) == 3, "manifest is append-only history: 2 first-run rows + 1 revision"
    assert rows[-1]["lane"] == "lane-alpha"
    assert rows[-1]["sha256"] == hashlib.sha256(b"alpha REVISED").hexdigest()


def test_empty_input_fails_nonzero(tmp_path, capsys):
    src = _write(tmp_path, "empty.md", "   \n\t\n")
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(tmp_path / "fw")])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_FAIL
    assert "empty input" in out
    assert not (tmp_path / "fw" / "w").exists(), "nothing may be written on empty input"


def test_content_before_first_header_fails(tmp_path, capsys):
    src = _write(tmp_path, "bad.md", "stray preamble\n=== lane-a ===\nbody\n")
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(tmp_path / "fw")])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_FAIL
    assert "before any '=== lane ===' header" in out


def test_empty_report_body_fails(tmp_path, capsys):
    src = _write(tmp_path, "bad.md", "=== lane-a ===\n   \n=== lane-b ===\nbody\n")
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(tmp_path / "fw")])
    assert rc == fwa.EXIT_FAIL
    assert "empty report body" in capsys.readouterr().out


def test_duplicate_lane_labels_fail(tmp_path, capsys):
    src = _write(tmp_path, "bad.md", "=== lane-a ===\nbody one\n=== lane-a ===\nbody two\n")
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(tmp_path / "fw")])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_FAIL
    assert "duplicate lane labels" in out and "lane-a" in out


def test_missing_input_file_fails_closed(tmp_path, capsys):
    rc = fwa.run(["--wave", "w", "--input", str(tmp_path / "gone.md"),
                  "--dir", str(tmp_path / "fw")])
    assert rc == fwa.EXIT_CANNOT_VERIFY
    assert "CANNOT-VERIFY" in capsys.readouterr().out


def test_corrupt_manifest_fails_closed_and_writes_nothing(tmp_path):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    assert fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)]) == fwa.EXIT_PASS
    m = base / "w" / "manifest.jsonl"
    m.write_text(m.read_text(encoding="utf-8") + "{corrupt row\n", encoding="utf-8")
    rc = fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    assert rc == fwa.EXIT_CANNOT_VERIFY, "idempotency must never decide on an unreadable manifest"
    assert len(m.read_text(encoding="utf-8").splitlines()) == 3, "no row added past the corruption"


def test_wave_slug_and_lane_labels_sanitize_to_safe_paths(tmp_path):
    src = _write(tmp_path, "reports.md", "=== lane alpha!! ===\nbody\n")
    base = tmp_path / "fifty_wide"
    rc = fwa.run(["--wave", "burn wave!", "--input", str(src), "--dir", str(base)])
    assert rc == fwa.EXIT_PASS
    assert _agent(base, "burn_wave", "lane_alpha").is_file()


def test_cli_exit_codes_and_stdin_pinned_through_subprocess(tmp_path):
    src = _write(tmp_path, "reports.md", BLOCKS)
    empty = _write(tmp_path, "empty.md", "")
    tool = str(REPO / "tools" / "fifty_wide_archive.py")
    r_pass = subprocess.run(
        [sys.executable, tool, "--wave", "w1", "--input", str(src), "--dir", str(tmp_path / "fw")],
        capture_output=True, text=True, timeout=60,
    )
    r_stdin = subprocess.run(
        [sys.executable, tool, "--wave", "w2", "--dir", str(tmp_path / "fw")],
        input=BLOCKS, capture_output=True, text=True, timeout=60,
    )
    r_empty = subprocess.run(
        [sys.executable, tool, "--wave", "w3", "--input", str(empty), "--dir", str(tmp_path / "fw")],
        capture_output=True, text=True, timeout=60,
    )
    r_missing = subprocess.run(
        [sys.executable, tool, "--wave", "w4", "--input", str(tmp_path / "gone.md"),
         "--dir", str(tmp_path / "fw")],
        capture_output=True, text=True, timeout=60,
    )
    assert (r_pass.returncode, r_stdin.returncode, r_empty.returncode, r_missing.returncode) == (
        fwa.EXIT_PASS, fwa.EXIT_PASS, fwa.EXIT_FAIL, fwa.EXIT_CANNOT_VERIFY)
    assert r_pass.stdout.startswith("ARCHIVED 2/2")
    assert r_stdin.stdout.startswith("ARCHIVED 2/2")
    assert (tmp_path / "fw" / "w2" / "agents" / "lane-alpha.md").is_file()


def _bank_dispatch_row(tmp_path: Path, wave: str, lanes: int, log: Path) -> int:
    # Fire the REAL guard pre-flight so the log row is the production shape and
    # the --wave join key (G2) is proven end to end, not against a hand-written
    # imitation row.
    units = tmp_path / "units.json"
    units.write_text(
        json.dumps([{"file": "a.md", "line": n} for n in range(1, lanes + 1)], ensure_ascii=False),
        encoding="utf-8",
    )
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps([f"a.md:{n}" for n in range(1, lanes + 1)], ensure_ascii=False),
                    encoding="utf-8")
    return fwg.run(["--units", str(units), "--plan", str(plan),
                    "--log", str(log), "--wave", wave])


def test_verify_clean_pair_replay_verified_and_rows_without_bytes(tmp_path, capsys):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    log = tmp_path / "dispatch_log.jsonl"
    assert fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)]) == fwa.EXIT_PASS
    assert _bank_dispatch_row(tmp_path, "w", 2, log) == fwg.EXIT_PASS
    rc = fwa.run(["--verify", "--wave", "w", "--dir", str(base), "--log", str(log)])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_PASS
    assert "REPLAY w: 2/2 sha-ok; count 2/2; REPLAY VERIFIED" in out
    # Old manifests (pre-2026-10-18 rows without the bytes field) still verify.
    m = base / "w" / "manifest.jsonl"
    rows = _manifest_rows(base, "w")
    for row in rows:
        row.pop("bytes")
    m.write_text(
        "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows),
        encoding="utf-8",
    )
    rc = fwa.run(["--verify", "--wave", "w", "--dir", str(base), "--log", str(log)])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_PASS
    assert "REPLAY VERIFIED" in out


def test_verify_catches_a_tampered_lane_file(tmp_path, capsys):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    log = tmp_path / "dispatch_log.jsonl"
    fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    _bank_dispatch_row(tmp_path, "w", 2, log)
    _agent(base, "w", "lane-alpha").write_text("alpha TAMPERED", encoding="utf-8")
    rc = fwa.run(["--verify", "--wave", "w", "--dir", str(base), "--log", str(log)])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_FAIL
    assert "SHA-DRIFT (mutated): lane-alpha" in out
    assert "REPLAY FAILED" in out


def test_verify_catches_a_missing_lane_file(tmp_path, capsys):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    log = tmp_path / "dispatch_log.jsonl"
    fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    _bank_dispatch_row(tmp_path, "w", 2, log)
    _agent(base, "w", "lane-beta").unlink()
    rc = fwa.run(["--verify", "--wave", "w", "--dir", str(base), "--log", str(log)])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_FAIL
    assert "SHA-DRIFT (missing): lane-beta" in out
    assert "REPLAY FAILED" in out


def test_verify_catches_a_count_gap(tmp_path, capsys):
    src = _write(tmp_path, "reports.md", BLOCKS)
    base = tmp_path / "fifty_wide"
    log = tmp_path / "dispatch_log.jsonl"
    fwa.run(["--wave", "w", "--input", str(src), "--dir", str(base)])
    # The guard passed pre-flight for 3 lanes but only 2 reports were archived:
    # exactly the 2026-10-03 shape the replay pair exists to explain.
    assert _bank_dispatch_row(tmp_path, "w", 3, log) == fwg.EXIT_PASS
    rc = fwa.run(["--verify", "--wave", "w", "--dir", str(base), "--log", str(log)])
    out = capsys.readouterr().out
    assert rc == fwa.EXIT_FAIL
    assert "COUNT-GAP" in out
    assert "2 lanes banked vs 3 lanes dispatched" in out
    assert "lane-alpha, lane-beta" in out
    assert "REPLAY FAILED" in out
