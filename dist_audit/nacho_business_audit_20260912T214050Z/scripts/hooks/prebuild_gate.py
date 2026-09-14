#!/usr/bin/env python3
"""prebuild_gate — the self-steal law as a PreToolUse hook (2026-08-28).

Law: "every build must either reference the shelf or justify why the shelf is
insufficient" (elder ruling, enforced form). Fires on Write/Edit of NEW .py
files. Layer A (exact docstring/signature dupe) blocks with exit 2 and names
the prior art. The creativity guard: a `# why-new:` line in the first 10 lines
acknowledges the prior art and allows the build. Layer C resemblance is
advisory only (injected as context, never blocks).

A broken gate must never block the fleet: any internal error exits 0 with a
note on stderr (fail-open for availability, logged for honesty).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHELF_DIRS = [ROOT / "mag", ROOT / "state" / "vast", ROOT / "scripts"]
WHY_NEW = "why-new:"


def signatures(text: str) -> set[str]:
    sigs = set()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("def ", "class ")):
            sigs.add(re.sub(r"\s+", " ", s.split(":")[0])[:120])
    return sigs


def docline(text: str) -> str:
    m = re.search(r'"""(.{0,160})', text, re.DOTALL)
    return re.sub(r"\s+", " ", m.group(1)).strip()[:140] if m else ""


def shelf_check(content: str, target: Path) -> tuple[str | None, str | None]:
    sigs = signatures(content)
    doc = docline(content)
    if not doc or len(sigs) < 2:
        return None, None  # too small to judge
    for d in SHELF_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("*.py"):
            try:
                if f.resolve() == target.resolve():
                    continue  # editing existing shelf file = extending, fine
                t = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            ddoc = docline(t)
            if doc and ddoc and (doc[:80].lower() in ddoc.lower() or ddoc[:80].lower() in doc.lower()):
                return "docline", f"{f.relative_to(ROOT)}"
            their = signatures(t)
            overlap = len(sigs & their)
            if overlap >= 3:
                return "signatures", f"{f.relative_to(ROOT)} ({overlap} shared signatures)"
    return None, None


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    if tool not in ("Write", "Edit"):
        sys.exit(0)
    fp = ti.get("file_path") or ""
    content = ti.get("content") or ti.get("new_string") or ""
    if not fp.endswith(".py") or len(content) < 400:
        sys.exit(0)
    target = Path(fp)
    if not target.is_absolute():
        target = ROOT / target
    # creativity guard: acknowledge the prior art and proceed
    head = content[:800]
    if WHY_NEW in head:
        print(json.dumps({"decision": "allow",
                          "reason": "why-new acknowledgment present"}))
        sys.exit(0)
    try:
        layer, prior = shelf_check(content, target)
    except Exception as e:  # noqa: BLE001 — fail-open, logged
        print(f"prebuild_gate internal error: {e}", file=sys.stderr)
        sys.exit(0)
    if layer == "docline":
        print(json.dumps({
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"SELF-STEAL GATE (layer A/{layer}): docstring resembles {prior}. "
                f"Options: (1) MERGE into/extend that module instead; "
                f"(2) acknowledge with '# {WHY_NEW} <what prior art cannot do>' "
                f"in the first 10 lines and rewrite.")}), file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
