"""Tests for tools/prepush_credential_shape.py (a11-commits row 4 instrument).

Contract under test: every row-named shape (sk- 16+, xai-, AIza, gsk_,
Bearer 15+, api_key/password assignment, PRIVATE KEY header, operator home
path) trips on a planted value and stays silent on the row's own literal
greps quoted as prose; values are masked, never printed in full; the CLI
exits 0 clean / 1 findings / 2 cannot-verify; a finding is accept-by-NAME via
fingerprint into the zero-day-one baseline; --changed covers dirty and
untracked content.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import tools.prepush_credential_shape as pcs

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "prepush_credential_shape.py"
PY = sys.executable

# Fixture tokens: shape-true, content-fake, and each exactly one shape.
# Discipline (cause + evidence): the PRIVATE KEY header and the operator home
# path are built by runtime concatenation because a source-byte literal makes
# this test file itself a scan finding (the first landing tripped the gate on
# its own fixture bytes; receipt
# watch/inbox/go_wave_20261004/prepush_instruments.md). Runtime values are
# byte-identical to the literals; only the source text is broken up.
_PLATED_KEY_HEADER = "-----" + "BEGIN RSA PRIVATE KEY" + "-----"
_HOME_FWD = "C:/" + "Users/" + "foste/notes/x.md"
_HOME_BACK = "C:" + chr(92) + "Users" + chr(92) + "foste" + chr(92) + "notes" + chr(92) + "x.md"
PLANTED = [
    ("OPENAI-SK", "sk-" + "a1" * 12),
    ("XAI-KEY", "xai-" + "b2" * 8),
    ("GOOGLE-AIZA", "AIza" + "c3" * 17),
    ("GROQ-GSK", "gsk_" + "d4" * 12),
    ("BEARER-TOKEN", "Authorization: Bearer " + "e5" * 10),
    ("KV-ASSIGN", "api_key = '" + "f6" * 8 + "'"),
    ("KV-ASSIGN", "password=" + "g7" * 8),
    ("PRIVATE-KEY-BLOCK", _PLATED_KEY_HEADER),
    ("OPERATOR-HOME-PATH", _HOME_FWD),
    ("OPERATOR-HOME-PATH", _HOME_BACK),
]

ROW_GREP_PROSE = (
    "the row grepped sk-[16+], xai-, AIza, gsk_, Bearer+15, api_key=val, "
    "password=, BEGIN PRIVATE KEY and got zero hits"
)


def test_all_row_shapes_flagged():
    text = "\n".join(f"line {i}: {tok}" for i, (_name, tok) in enumerate(PLANTED))
    findings = pcs.scan_text(text, "fixture.md")
    names = {f["name"] for f in findings}
    assert names == {n for n, _ in PLANTED}
    assert len(findings) == len(PLANTED)


def test_prose_grep_mentions_stay_silent():
    """The row's literal greps carry no value-sized token, so quoting them in
    a receipt must not WARN (the value-shape gate's whole point)."""
    assert pcs.scan_text(ROW_GREP_PROSE, "receipt.md") == []
    assert pcs.scan_text("clean prose, no shapes at all\n", "clean.md") == []


def test_masking_and_fingerprint():
    text = "token = " + PLANTED[0][1] + "\n"
    findings = pcs.scan_text(text, "x.md")
    assert len(findings) == 1
    masked = findings[0]["masked"]
    assert PLANTED[0][1] not in masked
    assert masked.startswith("sk-a")
    assert "(len" in masked
    assert findings[0]["fp"] == pcs.fingerprint("OPENAI-SK", "x.md", masked)
    # fp is stable and identity-sensitive
    assert pcs.fingerprint("OPENAI-SK", "x.md", masked) == findings[0]["fp"]
    assert pcs.fingerprint("OPENAI-SK", "y.md", masked) != findings[0]["fp"]


def test_cli_clean_file_exits_zero(tmp_path):
    clean = tmp_path / "clean.md"
    clean.write_text(ROW_GREP_PROSE + "\n", encoding="utf-8")
    r = subprocess.run([PY, str(TOOL), "--root", str(tmp_path), str(clean)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("CRED-SHAPE: ok")


def test_cli_planted_file_trips_then_baseline_accepts_by_name(tmp_path):
    dirty = tmp_path / "dirty.md"
    dirty.write_text("bearer: " + PLANTED[4][1] + "\n", encoding="utf-8")
    r = subprocess.run([PY, str(TOOL), "--root", str(tmp_path), str(dirty)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1, r.stdout + r.stderr
    assert r.stdout.startswith("CRED-SHAPE: WARN")
    assert "BEARER-TOKEN" in r.stdout
    fps = [ln.split("fp: ")[1].strip() for ln in r.stdout.splitlines()
           if ln.startswith("  fp: ")]
    assert len(fps) == 1
    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps(
        {"accepted": {fps[0]: {"accepted_by": "test", "reason": "fixture"}}}),
        encoding="utf-8")
    r2 = subprocess.run(
        [PY, str(TOOL), "--root", str(tmp_path), "--baseline", str(baseline), str(dirty)],
        capture_output=True, text=True, timeout=60)
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert "all accepted or none" in r2.stdout


def _git(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True, timeout=60)


@pytest.mark.skipif(shutil.which("git") is None, reason="no git")
def test_changed_scope_covers_dirty_and_untracked(tmp_path):
    """The secret_gate fast path: a secret in a DIRTY tracked file and a
    different shape in an UNTRACKED file both land in the scan."""
    repo = tmp_path / "repo"
    repo.mkdir()
    assert _git("init", "-q", cwd=repo).returncode == 0
    _git("config", "user.email", "t@t", cwd=repo)
    _git("config", "user.name", "t", cwd=repo)
    (repo / "tracked.txt").write_text("v1 clean\n", encoding="utf-8")
    _git("add", "-A", cwd=repo)
    _git("commit", "-q", "-m", "base", cwd=repo)
    dirty_secret = PLANTED[0][1]
    (repo / "tracked.txt").write_text("v1 clean\nkey=" + dirty_secret + "\n",
                                      encoding="utf-8")
    untracked_secret = PLANTED[3][1]
    (repo / "untracked.md").write_text("groq: " + untracked_secret + "\n",
                                       encoding="utf-8")
    r = subprocess.run([PY, str(TOOL), "--root", str(repo), "--changed"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "tracked.txt" in r.stdout
    assert "untracked.md" in r.stdout
    # masking law: neither planted value appears in full
    assert dirty_secret not in r.stdout
    assert untracked_secret not in r.stdout


def test_tool_source_does_not_self_trip():
    """Cause + evidence: the gate warned on its own docstring at first landing
    because it spelled the operator home path literally (receipt banked the
    self-trip); the citation now uses C:/Users/<name>, so the tool's own bytes
    must scan clean."""
    text = TOOL.read_text(encoding="utf-8", errors="replace")
    assert pcs.scan_text(text, "tools/prepush_credential_shape.py") == []


# --- ouroboros R3 move 6 (2026-10-05): three absent families, one-per-line
# cap, JSON-escaped separators. SYNTHESIS row 6 verified each shape scanned
# clean before the fix. Tokens runtime-built, content-fake, per the fixture
# discipline above.


def test_github_pat_trips():
    ghp = "ghp_" + "A1" * 18  # classic PAT shape: 36-char value
    rows = pcs.scan_text("token " + ghp + " inlined in a receipt", "x.md")
    assert [r["name"] for r in rows] == ["GITHUB-PAT"]
    assert ghp not in rows[0]["masked"]


def test_aws_key_and_bare_jwt_same_line_trip():
    akia = "AKIA" + "B2C3D4E5F6G7H8J9"  # 16 uppercase alnum key id
    jwt = "eyJ" + "c9" * 10 + "." + "d8" * 10 + "." + "e7" * 8
    line = "creds " + akia + " and " + jwt + " on one line"
    names = [r["name"] for r in pcs.scan_text(line, "x.md")]
    assert names == ["AWS-AKIA", "BARE-JWT"]


def test_two_sk_secrets_one_line_report_two():
    """rx.search reported exactly one finding for a two-secret line (verified
    pre-fix); finditer must report both, each with its own mask."""
    sk1 = "sk-" + "a1" * 12
    sk2 = "sk-" + "b2" * 12
    rows = pcs.scan_text("pair " + sk1 + " " + sk2 + " leaked", "x.md")
    assert len(rows) == 2
    assert all(r["name"] == "OPENAI-SK" for r in rows)
    assert {r["masked"] for r in rows} == {pcs.mask_value(sk1), pcs.mask_value(sk2)}


def test_json_escaped_doubled_backslash_home_path_trips():
    """The single-separator class matched exactly one separator, so a
    JSON-escaped home path (doubled backslashes) evaded the shape."""
    bb = chr(92) * 2
    line = "C:" + bb + "Users" + bb + "foste" + bb + "notes" + bb + "x.md"
    names = [r["name"] for r in pcs.scan_text(line, "x.md")]
    assert names == ["OPERATOR-HOME-PATH"]


def test_family_name_prose_mentions_stay_silent():
    """Shape-name prose with no value-sized token stays out (value-shape law)."""
    prose = ("added ghp_ (GitHub PAT), AKIA (AWS) and bare JWT rows; the "
             "families are named, no values present")
    assert pcs.scan_text(prose, "receipt.md") == []
