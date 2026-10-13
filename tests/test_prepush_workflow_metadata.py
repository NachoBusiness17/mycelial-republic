"""Tests for tools/prepush_workflow_metadata.py (build-it-all lane B6).

Contract under test: the two struck defect classes surface as WARN findings -
CR bytes inside a /* zcode-workflow ... */ metadata block, and a default that
fails its declared type (the ractor-engine moonshots regression: the default
read as the STRING "2<CR>", a quoted 2 with a CR inside the quotes, where
type: number was declared, and the workflow refused runs). Clean files pass;
script-body CR is never flagged (block-only scope law); quoted defaults stay
legal for json/string types; the CLI exits 0 clean / 1 findings / 2
cannot-verify; a finding is accept-by-NAME via fingerprint into the
zero-day-one baseline; line numbers are file-absolute.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import tools.prepush_workflow_metadata as pwm

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "prepush_workflow_metadata.py"
PY = sys.executable
CR = "\r"


def make_root(tmp_path: Path) -> Path:
    root = tmp_path / "estate"
    (root / ".zcode" / "workflows").mkdir(parents=True)
    return root


# The struck ractor-engine shape, byte-faithful: quoted 2 with a CR inside
# the quotes, declared type: number, sitting in a CRLF'd metadata block.
POISONED_BLOCK = (
    "/* zcode-workflow\n".replace("\n", CR + "\n")
    + 'description: "poisoned fixture"\n'.replace("\n", CR + "\n")
    + "args:\n".replace("\n", CR + "\n")
    + "  moonshots:\n".replace("\n", CR + "\n")
    + "    type: number\n".replace("\n", CR + "\n")
    + "    description: count of wild-eye lanes\n".replace("\n", CR + "\n")
    + "    required: false\n".replace("\n", CR + "\n")
    + '    default: "2' + CR + '"\n'.replace("\n", CR + "\n")
    + "  loud:\n".replace("\n", CR + "\n")
    + "    type: boolean\n".replace("\n", CR + "\n")
    + "    description: noise gate\n".replace("\n", CR + "\n")
    + "    required: false\n".replace("\n", CR + "\n")
    + "    default: 'true'\n".replace("\n", CR + "\n")
    + "*/\n"
)

CLEAN_BLOCK = """/* zcode-workflow
description: "clean fixture"
args:
  moonshots:
    type: number
    description: count of wild-eye lanes
    required: false
    default: 2
  width:
    type: number
    required: false
    default: 3.5
  loud:
    type: boolean
    required: false
    default: false
  lenses:
    type: json
    description: sanctioned quoted json default
    required: false
    default: '["accuracy", "operations"]'
  slug:
    type: string
    required: true
    description: "quoted string defaults stay legal"
*/
"""

BODY = "// script body with windows endings stays out of scope\r\nconst x = 1;\r\n"


def write(root: Path, name: str, text: str) -> Path:
    path = root / ".zcode" / "workflows" / name
    path.write_bytes(text.encode("utf-8"))
    return path


def run_cli(root: Path, *extra: str):
    return subprocess.run(
        [PY, str(TOOL), "--root", str(root), *extra],
        capture_output=True, text=True, timeout=120,
    )


def test_poisoned_default_trips_warn(tmp_path):
    root = make_root(tmp_path)
    write(root, "poisoned.dwf.ts", POISONED_BLOCK + BODY)
    r = run_cli(root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert r.stdout.splitlines()[0].startswith("WORKFLOW-METADATA: WARN")
    # the struck ractor-engine shape: quoted "2<CR>" where type: number
    assert re.search(r"TYPE-DEFAULT .*moonshots.*number.*string default.*\\\\r", r.stdout), r.stdout
    # quoted 'true' where type: boolean is the same disease
    assert "arg 'loud' declares type boolean" in r.stdout
    # CR bytes inside the block are their own finding class
    assert "CR-IN-METADATA .zcode/workflows/poisoned.dwf.ts:1" in r.stdout
    # fingerprints ride the WARN rows: accept-by-NAME needs them visible
    assert "[fp " in r.stdout


def test_clean_files_pass(tmp_path):
    root = make_root(tmp_path)
    write(root, "clean.dwf.ts", CLEAN_BLOCK + BODY)
    r = run_cli(root)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.splitlines()[0].startswith("WORKFLOW-METADATA: ok")
    assert "0 finding(s)" in r.stdout


def test_cr_in_script_body_not_flagged(tmp_path):
    """Block-only scope law: CR bytes in the script body never WARN (the gate
    must not force a whole-file line-ending migration)."""
    root = make_root(tmp_path)
    write(root, "body-crlf.dwf.ts", CLEAN_BLOCK + BODY)
    findings, status = pwm.scan_file(
        root / ".zcode" / "workflows" / "body-crlf.dwf.ts",
        ".zcode/workflows/body-crlf.dwf.ts")
    assert status == "block"
    assert findings == []


def test_number_default_shapes(tmp_path):
    root = make_root(tmp_path)
    write(root, "numbers.dwf.ts", CLEAN_BLOCK + (
        "/*\n"
        "second block ignored: only the first metadata block is scanned\n"
        "*/\n"))
    cases = [
        ("2", False), ("3.5", False), ("-1", False), (".5", False),
        ("'3'", True), ('"2"', True), ("two", True), ("2e5", True), ("true", True),
    ]
    for value, expect_finding in cases:
        block = ("/* zcode-workflow\nargs:\n  n:\n    type: number\n"
                 f"    required: false\n    default: {value}\n*/\n")
        rows = pwm.typed_default_findings(block.encode("utf-8"), 1, "f.dwf.ts")
        assert bool(rows) == expect_finding, (value, rows)


def test_boolean_default_shapes():
    cases = [
        ("true", False), ("false", False),
        ("'true'", True), ('"false"', True), ("maybe", True), ("1", True),
    ]
    for value, expect_finding in cases:
        block = ("/* zcode-workflow\nargs:\n  b:\n    type: boolean\n"
                 f"    required: false\n    default: {value}\n*/\n")
        rows = pwm.typed_default_findings(block.encode("utf-8"), 1, "f.dwf.ts")
        assert bool(rows) == expect_finding, (value, rows)


def test_cr_finding_line_is_file_absolute():
    """A block not starting at line 1 reports absolute line numbers (the CR
    row and the TYPE-DEFAULT row both)."""
    pre = "// leading comment\n// another\n"
    data = (pre.encode("utf-8") + POISONED_BLOCK.encode("utf-8") + BODY.encode("utf-8"))
    path = Path("f.dwf.ts")
    m = pwm.METADATA_RE.search(data)
    assert m is not None
    cr_rows = pwm.cr_findings(data, m, str(path))
    assert cr_rows and cr_rows[0]["line"] == 3  # line 1 + 2 comments
    type_rows = pwm.typed_default_findings(m.group(1), 3, str(path))
    # file lines: block starts at line 3; the moonshots default is block
    # line 8, the loud default block line 13 -> absolute 10 and 15
    assert {r["line"] for r in type_rows} == {10, 15}


def test_baseline_accept_by_name(tmp_path, capsys):
    root = make_root(tmp_path)
    write(root, "poisoned.dwf.ts", POISONED_BLOCK + BODY)
    rc = pwm.main(["--root", str(root)])
    out = capsys.readouterr().out
    assert rc == 1
    fp = re.search(r"\[fp ([0-9a-f]{16})\]", out).group(1)
    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({"accepted": {fp: "lane B6 fixture triage"}}),
                        encoding="utf-8")
    rc = pwm.main(["--root", str(root), "--baseline", str(baseline)])
    out = capsys.readouterr().out
    # accepting ONE fingerprint leaves the other findings fresh
    assert rc == 1
    assert f"accepted [{fp}]" in out
    assert "1 accepted by name" in out


def test_no_scan_dirs_exit_2(tmp_path):
    r = run_cli(tmp_path / "empty")
    assert r.returncode == 2
    assert r.stdout.splitlines()[0].startswith("WORKFLOW-METADATA: cannot verify")


def test_no_metadata_block_counted_not_flagged(tmp_path):
    root = make_root(tmp_path)
    write(root, "plain.dwf.ts", "// plain draft script, no metadata block\n")
    r = run_cli(root)
    assert r.returncode == 0, r.stdout
    assert "1 without a metadata block" in r.stdout


def test_extra_files_flag_scanned(tmp_path):
    root = make_root(tmp_path)
    write(root, "clean.dwf.ts", CLEAN_BLOCK + BODY)
    poisoned_copy = tmp_path / "stray.dwf.ts"
    poisoned_copy.write_bytes(POISONED_BLOCK.encode("utf-8"))
    r = run_cli(root, "--files", str(poisoned_copy))
    assert r.returncode == 1
    assert "stray.dwf.ts" in r.stdout
    assert "scanned 2 workflow file(s)" in r.stdout


# --- R3 move 7 (ouroboros 2026-10-05, SYNTHESIS row 7): the arg-header regex
# matched EXACTLY two spaces, so a four-space-indented args block (the
# strike-1 shape re-spelled) escaped TYPE-DEFAULT whole.

FOUR_SPACE_BLOCK = """/* zcode-workflow
description: "four-space indent fixture"
args:
    moonshots:
      type: number
      description: count of wild-eye lanes
      required: false
      default: '2'
    loud:
      type: boolean
      required: false
      default: false
*/
"""


def test_four_space_args_block_no_longer_escapes(tmp_path):
    root = make_root(tmp_path)
    write(root, "four-space.dwf.ts", FOUR_SPACE_BLOCK + BODY)
    findings, status = pwm.scan_file(
        root / ".zcode" / "workflows" / "four-space.dwf.ts",
        ".zcode/workflows/four-space.dwf.ts")
    assert status == "block"
    td = [f for f in findings if f["name"] == "TYPE-DEFAULT"]
    assert len(td) == 1, findings
    assert "moonshots" in td[0]["detail"]
    assert "string default" in td[0]["detail"]
    assert "loud" not in td[0]["detail"], "the clean boolean default stays silent"


def test_nested_default_content_never_redeclares():
    """A nested block default's inner type:/default: lines are value content:
    they must not overwrite the outer arg's declared type or default (if they
    did, n would re-declare boolean with a quoted 'true' scalar and fire)."""
    block = ("/* zcode-workflow\nargs:\n  n:\n    type: number\n    default:\n"
             "      alpha:\n        type: boolean\n        default: 'true'\n"
             "  m:\n    type: boolean\n    required: false\n    default: true\n"
             "*/\n")
    rows = pwm.typed_default_findings(block.encode("utf-8"), 1, "f.dwf.ts")
    assert rows == [], rows


def test_two_space_blocks_still_parse_after_indent_fix(tmp_path):
    """The legacy two-space convention parses identically (regression guard
    for the ARG_HEADER_RE widening)."""
    root = make_root(tmp_path)
    write(root, "poisoned.dwf.ts", POISONED_BLOCK + BODY)
    r = run_cli(root)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "moonshots" in r.stdout and "loud" in r.stdout
