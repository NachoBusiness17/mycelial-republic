"""Tests for tools/prepush_seal_patrol.py (a12-ractor-legs row 3 instrument).

Contract under test (the row's CHECK3 laws, tmp_a12_verify.py): latest
sha-bearing seal row per file vs actual bytes is the verdict; sealed-but-
deleted files are NOT a defect (42 sealed vs 21 on disk was ruled expected);
malformed ledger rows are counted, never fatal; the window bounds cost
(full ledger is 5,404 distinct files / 1.81 GB); a missing ledger is exit 2.

Fixture law: every board file is written with write_bytes and sealed with the
sha of those exact bytes. The first draft used write_text and its Windows
newline translation (\n -> \r\n) silently diverged sealed sha from disk bytes,
which tripped the clean fixture into a DRIFT - the patrol catching real
byte-drift inside its own test (receipt
watch/inbox/go_wave_20261004/prepush_instruments.md).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import tools.prepush_seal_patrol as psp

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "prepush_seal_patrol.py"
PY = sys.executable


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_board(root: Path, rel: str, data: bytes) -> Path:
    path = root / "watch/inbox" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _ledger(root: Path, rows: list[dict], extra: str = "") -> Path:
    led = root / "watch/inbox/index_events.jsonl"
    led.parent.mkdir(parents=True, exist_ok=True)
    led.write_text("".join(json.dumps(r) + "\n" for r in rows) + extra,
                   encoding="utf-8")
    return led


def _cli(root: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(TOOL), "--root", str(root),
         "--ledger", "watch/inbox/index_events.jsonl", *extra],
        capture_output=True, text=True, timeout=60)


def test_resolve_sealed_path_shapes(tmp_path):
    assert psp.resolve_sealed_path(tmp_path, "board/a.md") == tmp_path / "watch/inbox/board/a.md"
    assert psp.resolve_sealed_path(tmp_path, "watch/inbox/board/a.md") == tmp_path / "watch/inbox/board/a.md"
    inside = tmp_path / "watch/inbox/board/a.md"
    assert psp.resolve_sealed_path(tmp_path, str(inside).replace("\\", "/")) == inside
    # Docker surface: outside this estate, never a finding surface
    assert psp.resolve_sealed_path(tmp_path, "/board/inbox/x.md") is None
    assert psp.resolve_sealed_path(tmp_path, "D:/somewhere/x.md") is None


def test_clean_board_ok_with_malformed_and_missing(tmp_path):
    """Known-clean fixture: latest seal wins (a.md sealed twice), 2 malformed
    rows counted, sealed-then-deleted c.md skipped, /board surface skipped."""
    a_bytes = b"v2\n"
    a = _write_board(tmp_path, "board/a.md", a_bytes)
    _write_board(tmp_path, "board/b.md", b"v1\n")
    rows = [
        {"ts": "t", "op": "register", "file": "board/a.md", "sha256": _sha(b"v1\n")},
        {"ts": "t", "op": "autoseal", "file": "board/a.md", "sha256": _sha(a_bytes)},
        {"ts": "t", "op": "register", "file": "board/b.md", "sha256": _sha(b"v1\n")},
        {"ts": "t", "op": "autoseal", "file": "board/c.md", "sha256": _sha(b"gone\n")},
        {"ts": "t", "op": "autoseal", "file": "/board/inbox/x.md", "sha256": _sha(b"x")},
    ]
    _ledger(tmp_path, rows, extra="{BROKEN\n{ALSO BROKEN\n")
    r = _cli(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("SEAL-PATROL: ok")
    assert "2 malformed" in r.stdout
    assert "1 missing-on-disk" in r.stdout
    assert "c.md" not in r.stdout  # deleted sealed file: never a finding
    assert a.name in ("a.md",)


def test_drift_trips_and_names_file_and_fix(tmp_path):
    """Known-bad fixture: b.md edited after its last seal must WARN exit 1
    with the rel path, both sha heads, and the fix line."""
    _write_board(tmp_path, "board/a.md", b"ok\n")
    b = _write_board(tmp_path, "board/b.md", b"v1\n")
    sealed = _sha(b.read_bytes())
    rows = [
        {"ts": "t", "op": "register", "file": "board/a.md", "sha256": _sha(b"ok\n")},
        {"ts": "t", "op": "autoseal", "file": "board/b.md", "sha256": sealed},
    ]
    _ledger(tmp_path, rows)
    b.write_bytes(b"v2 edited after the seal\n")
    r = _cli(tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert r.stdout.startswith("SEAL-PATROL: DRIFT")
    assert "board/b.md" in r.stdout
    assert sealed[:12] in r.stdout
    assert "re-seal through the owning writer" in r.stdout


def test_uppercase_seal_matches_but_real_drift_still_trips(tmp_path):
    """B7 fix (r2 gap closure row 8, SYNTHESIS.md): some seal writers store
    the sha UPPERCASE while file_sha256 returns lowercase hexdigest, and the
    raw compare flagged byte-identical files as drift (21 case-only false
    drifts burying 17 real ones at --rows 1000). An uppercase-sealed file
    whose bytes match must pass clean; a genuinely byte-drifted file must
    still trip, and its printed sealed head must be lowercase."""
    ok = _write_board(tmp_path, "board/ok.md", b"sealed uppercase, bytes match\n")
    bad = _write_board(tmp_path, "board/bad.md", b"v1\n")
    rows = [
        {"ts": "t", "op": "autoseal", "file": "board/ok.md",
         "sha256": _sha(ok.read_bytes()).upper()},
        {"ts": "t", "op": "autoseal", "file": "board/bad.md",
         "sha256": _sha(bad.read_bytes())},
    ]
    _ledger(tmp_path, rows)
    bad.write_bytes(b"v2 genuinely edited after its seal\n")
    r = _cli(tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert r.stdout.startswith("SEAL-PATROL: DRIFT")
    # the case-only non-drift is a match, never named as drifted
    assert "board/ok.md" not in r.stdout
    assert "1 match" in r.stdout
    # the real byte change still trips, sealed head printed lowercase
    assert "board/bad.md" in r.stdout
    assert _sha(b"v1\n").lower()[:12] in r.stdout


def test_window_bounds_the_check(tmp_path):
    """The cost law: a drift whose seal row slid out of the trailing window is
    out of scope at the default window and back in at --rows big enough."""
    old = _write_board(tmp_path, "board/old.md", b"sealed\n")
    rows = [{"ts": "t", "op": "register", "file": "board/old.md",
             "sha256": _sha(b"sealed\n")}]
    for i in range(160):
        fresh = _write_board(tmp_path, f"board/fresh{i}.md", f"f{i}\n".encode())
        rows.append({"ts": "t", "op": "autoseal", "file": f"board/fresh{i}.md",
                     "sha256": _sha(fresh.read_bytes())})
    _ledger(tmp_path, rows)
    old.write_bytes(b"edited long after its seal\n")
    r_default = _cli(tmp_path)
    assert r_default.returncode == 0, r_default.stdout + r_default.stderr
    assert "old.md" not in r_default.stdout
    r_wide = _cli(tmp_path, "--rows", "200")
    assert r_wide.returncode == 1
    assert "board/old.md" in r_wide.stdout


def test_missing_ledger_exit_two(tmp_path):
    r = _cli(tmp_path)
    assert r.returncode == 2
    assert "cannot verify" in r.stdout


def test_patrol_core_latest_seal_wins(tmp_path):
    """Unit pass over the pure core: same file sealed twice, the LAST
    sha-bearing row is the verdict (the CHECK3 query's with_sha[-1] law).
    The core resolves bare paths under watch/inbox, so the fixture lives
    there."""
    f = _write_board(tmp_path, "f.md", b"bytes matching the second seal\n")
    rows = [
        {"file": "f.md", "sha256": _sha(b"first\n"), "op": "register"},
        {"file": "f.md", "sha256": _sha(f.read_bytes()), "op": "autoseal"},
    ]
    result = psp.patrol(tmp_path, rows, 150)
    assert len(result["matched"]) == 1
    assert result["drifted"] == []
    assert result["missing"] == 0
    assert result["distinct"] == 1
