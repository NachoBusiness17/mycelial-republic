#!/usr/bin/env python3
"""prepush_workflow_metadata.py - CR + typed-default patrol over saved
workflow metadata blocks (build-it-all wave lane B6, 2026-10-05).

Defect class (cause + evidence, struck twice): saved .dwf.ts metadata blocks
carry Windows CR bytes and string-typed defaults where a number/boolean is
declared, and both refuse runs at dispatch time. Strike 1: the
ractor-engine.dwf.ts moonshots default read as the STRING "2<CR>" (a quoted
2 with a CR inside the quotes, type: number) and the workflow refused runs
until hand-fixed. Strike 2: the .env CRLF outage (the same byte disease on a
different surface). This tool makes that class a standing pre-push WARN.

Scope: the /* zcode-workflow ... */ metadata block of every
.zcode/workflows/*.dwf.ts and .zcode/workflow-drafts/*.dwf.ts. Two finding
classes only, both named by the brief:
- CR-IN-METADATA: any CR byte inside the block (the parser-visible surface;
  script bodies are deliberately out of scope - a push hook must not force a
  whole-file line-ending migration).
- TYPE-DEFAULT: an arg declaring type number/boolean whose default fails the
  type - a quoted default of ANY content is a string default under YAML
  (strike 1 was quoted "2<CR>"), and an unquoted default must parse as the
  declared type (number: plain int/float literal; boolean: true/false).
  Quoted defaults stay legal for type json/string (the lenses JSON array in
  ractor-engine.dwf.ts is the sanctioned shape).

A .dwf.ts with no metadata block is counted and skipped, not a finding: the
drafts dir holds plain script drafts, and the brief names exactly the two
classes above (zero-baseline day one, the census-tripwire precedent:
WARN-ONLY at pre-push, flip to enforce is an operator call).

Accept-by-NAME law (citation_lint / credential_shape precedent): a finding
may be accepted by fingerprint into configs/prepush_workflow_metadata_
baseline.json after triage, never mass-imported. The baseline starts ABSENT
(zero baseline day one); the landing fixes every live finding instead.

Fix law: strip CR from the metadata block ONLY (never touch the script
body); a TYPE-DEFAULT fix rewrites the default to the declared type's
literal. Note for editors: the harness Edit tool normalizes line endings on
match/write (measured at landing: an LF-only old_string matched a CRLF
block, and the write preserved CRLF), so CR surgery goes through a
block-scoped byte edit with before/after byte verification - block CR to 0,
body byte-identical.

Output contract (B2-338 law): a green run's FIRST stdout line opens with
"WORKFLOW-METADATA: ok"; findings open "WORKFLOW-METADATA: WARN". Exit
codes: 0 = clean or all findings accepted; 1 = findings (the WARN payload);
2 = cannot verify (no scan dir resolves under --root).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
# Anchored to ESTATE_ROOT (violation_ratchet cwd-relative-path class, first
# landing law: a push hook runs from the repo root but the tool must not
# depend on that). main() re-resolves RELATIVE --baseline/--files args
# against --root so tmp-root tests keep working.
DEFAULT_BASELINE = ESTATE_ROOT / "configs/prepush_workflow_metadata_baseline.json"
SCAN_DIRS = (".zcode/workflows", ".zcode/workflow-drafts")
WORKFLOW_GLOB = "*.dwf.ts"
METADATA_RE = re.compile(rb"/\*\s*zcode-workflow(.*?)\*/", re.DOTALL)
# Plain int/float literal only (YAML scalar the harness can deliver as a
# number). No nan/inf/1e5 spellings: nobody writes those as a default, and
# the strict shape is the point.
NUMERIC_RE = re.compile(r"-?(?:\d+\.?\d*|\.\d+)")
# Indent captured (R3 move 7, ouroboros 2026-10-05): the header regex matched
# EXACTLY two spaces, so a four-space-indented args block (the strike-1 shape
# re-spelled) escaped TYPE-DEFAULT whole. The first arg header under args:
# fixes the block indent; headers must sit at exactly that indent.
ARG_HEADER_RE = re.compile(r"^([ \t]+)([A-Za-z0-9_.-]+):[ \t]*$")
PROP_RE = re.compile(r"^([ \t]+)(type|default):[ \t]*(.*?)[ \t]*$")


def extract_block(data: bytes) -> tuple[re.Match, bytes] | None:
    """The first zcode-workflow metadata block, or None when absent."""
    m = METADATA_RE.search(data)
    if m is None:
        return None
    return m, m.group(1)


def cr_findings(data: bytes, m: re.Match, rel: str) -> list[dict]:
    """One CR-IN-METADATA row per file (count + line range), not per line:
    the fix is always the same block-scoped strip, and a per-line row set
    turns one CRLF'd block into dozens of WARN lines a push hook would
    train operators to dismiss (the B2-338 channel-discipline lesson)."""
    block = m.group(1)
    line_no = data[: m.start()].count(b"\n") + 1  # 1-based file line of block start
    total = 0
    first = last = None
    for seg in block.split(b"\n"):
        cr_count = seg.count(b"\r")
        if cr_count:
            total += cr_count
            if first is None:
                first = line_no
            last = line_no
        line_no += 1
    if not total or first is None:
        return []
    return [{
        "name": "CR-IN-METADATA",
        "file": rel,
        "line": first,
        "detail": f"{total} CR byte(s) across metadata block lines {first}-{last}",
        "line_text": f"cr-bytes {total} lines {first}-{last}",
    }]


def typed_default_findings(block: bytes, block_start_line: int, rel: str) -> list[dict]:
    """TYPE-DEFAULT rows: defaults failing their declared number/boolean type.

    Parsing is deliberately shallow: an arg is a bare indented `name:` line
    under the `args:` header; its `type:`/`default:` properties sit at deeper
    indent until the next arg or block end. The first arg header fixes the
    block indent (two-space and four-space conventions both parse, R3 move 7:
    the exactly-two-space regex let a four-space args block escape whole);
    deeper bare `name:` lines are nested default content, never a new arg,
    and once an arg's first property indent is seen, type:/default: lines at
    any other indent are nested block-default content, never a re-declare.
    The raw default value keeps interior CR bytes so the struck shape (a CR
    inside the quotes) reports with the CR visible.
    """
    out: list[dict] = []
    lines = block.decode("utf-8", "replace").split("\n")
    line_no = block_start_line - 1  # 1-based file line of each block line
    in_args = False
    args_indent: str | None = None  # indent of the first arg header
    prop_indent: str | None = None  # indent of the current arg's first prop
    current: str | None = None
    declared: dict[str, tuple[str, int]] = {}  # arg -> (type, line)
    defaults: dict[str, tuple[str, int]] = {}  # arg -> (raw value, line)
    for raw_line in lines:
        line_no += 1
        eol_stripped = raw_line.rstrip("\r")
        if re.match(r"^args:[ \t]*$", eol_stripped):
            in_args = True
            continue
        if not in_args or not eol_stripped.strip():
            continue
        if not eol_stripped[:1].isspace():
            in_args = False  # a new top-level key ends the args section
            args_indent = None
            prop_indent = None
            current = None
            continue
        header = ARG_HEADER_RE.match(eol_stripped)
        if header:
            indent, name = header.group(1), header.group(2)
            if args_indent is None:
                args_indent = indent  # the first arg header fixes the indent
            if indent == args_indent:
                current = name
                prop_indent = None
            # deeper bare name lines are nested value content: current and
            # its property level stay untouched
            continue
        prop = PROP_RE.match(raw_line)
        if prop is None or current is None:
            continue
        if prop_indent is None:
            if args_indent is not None and len(prop.group(1)) <= len(args_indent):
                continue  # a prop at or above the header indent is malformed
            prop_indent = prop.group(1)  # this arg's property level
        elif prop.group(1) != prop_indent:
            continue  # nested block-default content, not this arg's property
        key, value = prop.group(2), prop.group(3)
        if key == "type":
            declared[current] = (value.strip(), line_no)
        elif key == "default":
            defaults[current] = (value, line_no)
    for arg in sorted(defaults):
        raw_value, def_line = defaults[arg]
        if arg not in declared:
            continue
        dtype, _type_line = declared[arg]
        if dtype not in ("number", "boolean"):
            continue  # json/string quoted defaults are the sanctioned shape
        raw = raw_value.strip(" \t")
        token = raw.strip()
        if not token:
            continue  # empty/continuation default: not this patrol's class
        quoted = raw[:1] in ("'", '"')
        ok = False
        if not quoted:
            if dtype == "number":
                ok = NUMERIC_RE.fullmatch(token) is not None
            else:
                ok = token in ("true", "false")
        if ok:
            continue
        shown = repr(token.replace("\r", "\\r"))[:60]
        kind = "string default" if quoted else "unparseable default"
        out.append({
            "name": "TYPE-DEFAULT",
            "file": rel,
            "line": def_line,
            "detail": f"arg '{arg}' declares type {dtype} but default is a "
                      f"{kind}: {shown}",
            "line_text": raw_value.replace("\r", "\\r"),
        })
    return out


def fingerprint(finding: dict) -> str:
    """Accept-by-NAME identity: class + file + offending line text. Line
    numbers are excluded on purpose so a one-line shift does not resurrect
    accepted debt (credential_shape precedent); editing the offending line
    changes the text and re-opens triage."""
    raw = f"{finding['name']}|{finding['file']}|{finding['line_text']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def scan_file(path: Path, rel: str) -> tuple[list[dict], str]:
    """Return (findings, status) for one .dwf.ts; status in block/noblock."""
    data = path.read_bytes()
    extracted = extract_block(data)
    if extracted is None:
        return [], "noblock"
    m, block = extracted
    block_start_line = data[: m.start()].count(b"\n") + 1
    return (cr_findings(data, m, rel)
            + typed_default_findings(block, block_start_line, rel), "block")


def load_baseline(path: Path) -> dict:
    if not path.is_file():
        return {"accepted": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"accepted": {}}
    return data if isinstance(data, dict) and "accepted" in data else {"accepted": {}}


def iter_workflow_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for rel_dir in SCAN_DIRS:
        base = root / rel_dir
        if base.is_dir():
            files.extend(sorted(p for p in base.glob(WORKFLOW_GLOB) if p.is_file()))
    return files


def run(root: Path, baseline_path: Path, extra_files: list[Path]) -> int:
    files = iter_workflow_files(root)
    scan_dirs_found = any((root / d).is_dir() for d in SCAN_DIRS)
    for extra in extra_files:
        if extra.is_file():
            files.append(extra)
    if not scan_dirs_found and not extra_files:
        print(f"WORKFLOW-METADATA: cannot verify, no scan dir under {root.as_posix()} "
              f"(looked for {' and '.join(SCAN_DIRS)})")
        return 2
    accepted = load_baseline(baseline_path).get("accepted", {})
    findings: list[dict] = []
    noblock = 0
    for path in files:
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
        rows, status = scan_file(path, rel)
        if status == "noblock":
            noblock += 1
        findings.extend(rows)
    fresh = [f for f in findings if fingerprint(f) not in accepted]
    head = (f"scanned {len(files)} workflow file(s) ({noblock} without a metadata "
            f"block, skipped), {len(findings)} finding(s) "
            f"({len(findings) - len(fresh)} accepted by name)")
    if not findings or not fresh:
        print(f"WORKFLOW-METADATA: ok - {head}")
        for f in findings:
            print(f"  accepted [{fingerprint(f)}]: {f['name']} {f['file']}:"
                  f"{f['line']} {f['detail']}")
        return 0
    print(f"WORKFLOW-METADATA: WARN - {head}")
    for f in findings:
        if fingerprint(f) in accepted:
            print(f"  accepted [{fingerprint(f)}]: {f['name']} {f['file']}:"
                  f"{f['line']} {f['detail']}")
    for f in fresh:
        print(f"  {f['name']} {f['file']}:{f['line']}: {f['detail']} "
              f"[fp {fingerprint(f)}]")
    print("  fix: strip CR from the metadata block only (never touch the script "
          "body) and rewrite the default as the declared type's literal; or "
          f"accept THIS finding by fingerprint into {baseline_path.as_posix()}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="CR + typed-default patrol over saved workflow metadata "
                    "blocks (build-it-all lane B6)")
    ap.add_argument("--root", type=Path, default=ESTATE_ROOT,
                    help="estate root (default: this repo)")
    ap.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE,
                    help="accept-by-NAME baseline (default: configs/"
                         "prepush_workflow_metadata_baseline.json; absent = zero)")
    ap.add_argument("--files", type=Path, nargs="*", default=[],
                    help="extra explicit .dwf.ts files to scan on top of the "
                         "two scan dirs")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    baseline = args.baseline
    if not baseline.is_absolute():
        baseline = root / baseline
    extra = [f if f.is_absolute() else root / f for f in args.files]
    return run(root, baseline, extra)


if __name__ == "__main__":
    sys.exit(main())
