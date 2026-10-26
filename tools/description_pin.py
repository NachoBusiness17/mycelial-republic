#!/usr/bin/env python3
"""description_pin.py — tool-description pinning gate.

Fold receipt: MASTER_MICKEY17_V2_20260924.md, Section 3 row 15 (rug-pull
tool-definition drift, a2a-mcp-security lane) plus the this-week gate list:
"land the three cheapest gates (verbatim-quote check, freshness receipts,
tool-description pinning)". A server can change a tool description after the
client approved it; the cheapest structural defense is that every tool
description carries its version pin, or an explicit PINNED-UNVERSIONED
marker when the tool is deliberately version-free. This is the pattern,
not a product: it checks text, it does not hash schemas or chase servers.

Bar (stated before reading anything):
  a tool description is PINNED when it contains a version token
  (v1, 1.2, 1.2.3 style) or the literal marker PINNED-UNVERSIONED.
  Anything else is a finding. Unparsable manifests and manifests whose
  entries lack a description are findings too: negatives are first-class.

Input: one or more paths. A path may be a JSON manifest file or a
directory (walked recursively for *.json). Accepted manifest shapes:
  - bare list of tool objects
  - {"tools": [ ... ]}
  - name-keyed mapping of tool name -> tool object
Tool objects are read for "name" (fallback "id") and "description".

Usage: python tools/description_pin.py PATH [PATH ...]

Exit codes: 0 = all descriptions pinned or marked; 1 = usage error
(no paths, or a path that does not exist); 2 = findings, each printed
as "path: tool: reason".
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "PINNED-UNVERSIONED"
# Receipt (t11c refire, 2026-09-25): the first cut \bv?\d+\.\d+(\.\d+)?\b only
# accepted dotted versions, so "stable v2" failed the gate while this file's
# own bar (docstring: "v1, 1.2, 1.2.3 style") says a v-prefixed single number
# pins. Evidence: lanes t11c.check.txt, 1 failed / 7 passed. Bare integers
# ("uses 5 tools") still do not pin: they need the v prefix or a dot.
VERSION_RE = re.compile(r"\bv\d+(?:\.\d+)*\b|\b\d+\.\d+(?:\.\d+)*\b")
NAME_KEYS = ("name", "id")


def is_pinned(description: str) -> bool:
    """True when the description carries a version pin or the marker."""
    if MARKER.lower() in description.lower():
        return True
    return VERSION_RE.search(description) is not None


def _tool_name(entry: object, index: int) -> str:
    if isinstance(entry, dict):
        for key in NAME_KEYS:
            value = entry.get(key)
            if isinstance(value, str) and value.strip():
                return value
    return f"<unnamed tool #{index}>"


def _unpinned_tools(tools: list, source: str) -> list[tuple[str, str]]:
    out = []
    for i, entry in enumerate(tools):
        name = _tool_name(entry, i)
        if not isinstance(entry, dict):
            out.append((f"{source}: {name}", "entry is not an object"))
            continue
        description = entry.get("description")
        if not isinstance(description, str) or not description.strip():
            out.append((f"{source}: {name}", "no description field"))
        elif not is_pinned(description):
            out.append((f"{source}: {name}", "description unpinned and unmarked"))
    return out


def _tools_from_doc(doc: object) -> list | None:
    """Return the tools list for an accepted manifest shape, else None."""
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        tools = doc.get("tools")
        if isinstance(tools, list):
            return tools
        if all(isinstance(v, dict) for v in doc.values()) and doc:
            return [{"name": k, **v} for k, v in doc.items()]
    return None


def findings_for_file(path: Path) -> list[tuple[str, str]]:
    """All (who, reason) findings for one manifest file."""
    source = path.as_posix()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [(source, f"unparsable manifest: {e.msg} at line {e.lineno}")]
    except OSError as e:
        return [(source, f"unreadable manifest: {type(e).__name__}")]
    tools = _tools_from_doc(doc)
    if tools is None:
        return [(source, "manifest shape not recognized (need list, "
                         'dict with "tools", or name-keyed mapping)')]
    return _unpinned_tools(tools, source)


def manifests_from(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.rglob("*.json"))
    return [path]


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python tools/description_pin.py PATH [PATH ...]",
              file=sys.stderr)
        return 1
    paths: list[Path] = []
    for arg in argv:
        p = Path(arg)
        if not p.exists():
            print(f"no such path: {arg}", file=sys.stderr)
            return 1
        paths.extend(manifests_from(p))
    findings: list[tuple[str, str]] = []
    for manifest in paths:
        findings.extend(findings_for_file(manifest))
    for who, reason in findings:
        print(f"{who}: {reason}")
    if findings:
        print(f"\n{len(findings)} finding(s); "
              f"pin the description or add {MARKER}.")
        return 2
    print("all tool descriptions pinned or marked")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
