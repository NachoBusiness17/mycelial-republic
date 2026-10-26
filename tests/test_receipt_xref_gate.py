"""receipt_xref_gate tests (W2, 2026-09-29, MICKEY17 wave 2 lane).

Covers the RETURN 14 contract in three bands, following the
tests/test_census_drift_patrol.py house style: the pure cores (extraction
regex self-stolen from tools/skills_lint.py plus the LINKS-N row check, and
scan_receipt naming EXACTLY the dead citations, never the live ones), the
mask law (secret-looking citation content never reaches stdout verbatim),
and the real CLI exit codes (0 clean / 0 WARN-only with dead citations /
1 strict with dead citations / 2 cannot-verify) pinned through a subprocess
against a synthetic mini-estate in tmp_path, including the --changed git
diff arm and the --summary per-receipt counts.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Module import, not from-imports: keeps every helper out of this module's
# namespace so pytest cannot mis-collect test_-prefixed objects (the
# 2026-09-26 collection-error law noted in tests/test_census_drift_patrol.py).
import tools.receipt_xref_gate as rxg

TOOL = Path(__file__).resolve().parents[1] / "tools" / "receipt_xref_gate.py"


def make_estate(tmp_path: Path) -> Path:
    """Synthetic mini-estate: one live cited file, one live receipt."""
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "real_tool.py").write_text("# live\n", encoding="utf-8")
    (tmp_path / "watch").mkdir()
    return tmp_path


def write_receipt(repo: Path, name: str, body: str) -> Path:
    md = repo / "watch" / name
    md.write_text(body, encoding="utf-8")
    return md


def cli(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=repo,
    )


# --- pure cores ---------------------------------------------------------------

def test_extract_paths_takes_only_backticked_allowlisted():
    text = (
        "cites `tools/real_tool.py` and `docs/absent.md`, "
        "ignores tools/real_tool.py without backticks, "
        "ignores `node_modules/x.js` and `C:/abs/win.md`."
    )
    assert rxg.extract_paths(text) == ["docs/absent.md", "tools/real_tool.py"]


def test_extract_links_rows_dedupes_and_sorts():
    assert rxg.extract_links_rows("LINKS-3 then LINKS-3 and LINKS-1") == [1, 3]


def test_scan_receipt_names_exactly_the_dead_citation(tmp_path: Path):
    repo = make_estate(tmp_path)
    md = write_receipt(
        repo,
        "R1.md",
        "live: `tools/real_tool.py` dead: `tools/ghost_never_landed.py`\n",
    )
    dead = rxg.scan_receipt(md, repo)
    assert len(dead) == 1
    assert "ghost_never_landed.py" in dead[0]
    assert "real_tool.py" not in dead[0]
    assert dead[0].startswith("DEAD-CITATION")


def test_scan_receipt_clean_passes(tmp_path: Path):
    repo = make_estate(tmp_path)
    md = write_receipt(repo, "R2.md", "only live: `tools/real_tool.py`\n")
    assert rxg.scan_receipt(md, repo) == []


def test_line_anchor_citation_resolves_base_file(tmp_path: Path):
    # W2 first-run defect, pinned: `path:120-125` cites the file, not a
    # literal filename ending in ":120-125" (12 of 21 raw first-run hits were
    # live files flagged dead). Live base must pass, dead base must still
    # die, and the dead row must carry the ORIGINAL citation text.
    repo = make_estate(tmp_path)
    live = write_receipt(
        repo,
        "R2a.md",
        "anchored live: `tools/real_tool.py:120-125` and `tools/real_tool.py:7`\n",
    )
    dead = write_receipt(repo, "R2b.md", "anchored dead: `tools/ghost.py:33`\n")
    assert rxg.scan_receipt(live, repo) == []
    rows = rxg.scan_receipt(dead, repo)
    assert len(rows) == 1 and "`tools/ghost.py:33`" in rows[0]


def test_links_row_citation_bounds_checked(tmp_path: Path):
    repo = make_estate(tmp_path)
    ledger = repo / "watch" / "inbox"
    ledger.mkdir()
    (ledger / "LINKS.jsonl").write_text('{"n": 1}\n{"n": 2}\n', encoding="utf-8")
    ok = write_receipt(repo, "R3.md", "row exists: LINKS-2\n")
    bad = write_receipt(repo, "R4.md", "row past the end: LINKS-3\n")
    assert rxg.scan_receipt(ok, repo) == []
    dead = rxg.scan_receipt(bad, repo)
    assert len(dead) == 1 and "LINKS-3" in dead[0] and "2 rows" in dead[0]


def test_links_row_dead_when_ledger_missing(tmp_path: Path):
    repo = make_estate(tmp_path)  # no watch/inbox/LINKS.jsonl
    md = write_receipt(repo, "R5.md", "cites LINKS-1 with no ledger on disk\n")
    dead = rxg.scan_receipt(md, repo)
    assert len(dead) == 1 and "ledger" in dead[0] and "missing" in dead[0]


# --- mask law -----------------------------------------------------------------

def test_mask_redacts_secret_looking_runs():
    out = rxg.mask("key sk-abc123def456ghi789 and hash " + "a" * 44)
    assert "sk-abc123def456ghi789" not in out
    assert "[REDACTED]" in out


def test_cli_output_masks_secret_in_dead_citation(tmp_path: Path):
    repo = make_estate(tmp_path)
    secret = "sk-abc123def456ghi789"
    write_receipt(repo, "R6.md", f"secret-named path: `tools/{secret}.py`\n")
    proc = cli(repo, "watch/R6.md", "--strict")
    assert proc.returncode == 1
    assert secret not in proc.stdout
    assert "[REDACTED]" in proc.stdout


# --- CLI exit codes (pinned through subprocess) -------------------------------

def test_cli_clean_receipt_exit_0_and_first_line_contract(tmp_path: Path):
    repo = make_estate(tmp_path)
    write_receipt(repo, "R7.md", "live only: `tools/real_tool.py`\n")
    proc = cli(repo, "watch/R7.md")
    assert proc.returncode == 0
    assert proc.stdout.splitlines()[0].startswith("RECEIPT-XREF: ok")


def test_cli_dead_citation_warn_only_exit_0(tmp_path: Path):
    repo = make_estate(tmp_path)
    write_receipt(repo, "R8.md", "dead: `tools/ghost.py`\n")
    proc = cli(repo, "watch/R8.md")
    assert proc.returncode == 0
    assert "DEAD-CITATIONS (WARN-ONLY)" in proc.stdout
    assert "ghost.py" in proc.stdout


def test_cli_dead_citation_strict_exit_1(tmp_path: Path):
    repo = make_estate(tmp_path)
    write_receipt(repo, "R9.md", "dead: `tools/ghost.py`\n")
    proc = cli(repo, "watch/R9.md", "--strict")
    assert proc.returncode == 1
    assert proc.stdout.splitlines()[0].startswith("RECEIPT-XREF: DEAD-CITATIONS (STRICT)")


def test_cli_missing_receipt_exit_2(tmp_path: Path):
    repo = make_estate(tmp_path)
    proc = cli(repo, "watch/NOPE.md")
    assert proc.returncode == 2
    assert "CANNOT-VERIFY" in proc.stdout


def test_cli_no_args_exit_2(tmp_path: Path):
    proc = cli(make_estate(tmp_path))
    assert proc.returncode == 2


def test_cli_summary_counts_per_receipt(tmp_path: Path):
    repo = make_estate(tmp_path)
    write_receipt(repo, "R10.md", "dead a: `tools/g1.py` dead b: `tools/g2.py`\n")
    write_receipt(repo, "R11.md", "live: `tools/real_tool.py`\n")
    proc = cli(repo, "watch/R10.md", "watch/R11.md", "--summary")
    assert proc.returncode == 0
    assert "dead=2" in proc.stdout and "dead=0" in proc.stdout


# --- --changed git diff arm ----------------------------------------------------

@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_cli_changed_mode_reads_git_diff(tmp_path: Path):
    repo = make_estate(tmp_path)
    (repo / "watch" / "inbox").mkdir()
    md = repo / "watch" / "inbox" / "LANE.md"
    md.write_text("clean start\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t",
         "commit", "-q", "-m", "base"],
        check=True, capture_output=True,
    )
    md.write_text("now cites `tools/ghost_changed.py`\n", encoding="utf-8")

    warn = cli(repo, "--changed")
    assert warn.returncode == 0
    assert "ghost_changed.py" in warn.stdout

    strict = cli(repo, "--changed", "--strict")
    assert strict.returncode == 1

    both = cli(repo, "--changed", "watch/inbox/LANE.md")
    assert both.returncode == 2
