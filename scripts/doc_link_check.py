"""doc_link_check - report-only checker for repo-relative path references in docs.

Scans (default scope):
  *.md at the repo root, docs/*.md (add --docs-recursive for docs/**),
  .agents/**/*.md, state/**/*.md, memory/MEMORY.md,
  *.cmd / *.bat / *.vbs at the repo root and under scripts/.

For each doc it extracts repo-relative path references and lists the ones
that do not exist, grouped by doc. Exit code 1 if any are missing, else 0.
Never modifies any file except the optional --receipt JSON.

Self-steal: extraction and resolution wrap mag/cite_gate.py (URL_RE masking,
the repo-anchored PATH_RE anchor list, _resolve_path, _TRAIL_PUNCT). This
script extends that with: anchors from the live top-level dirs, markdown link
targets resolved relative to the doc, code-fence skipping, %~dp0-style
variable handling for .cmd/.bat/.vbs, glob and template counting, and a
cross-repo check (a missing path that exists in a sibling repo named on the
same line is not counted as dead), a prose filter (an un-backticked a/b/c with
no file extension is prose, not a path), and phantom-ledger sections (dead refs
kept on purpose under a PHANTOM/tombstone heading, or on a line that says the
path "never existed", are reported separately). Prefix fragments ending in _ or -
count as templates.

Usage:
  python scripts/doc_link_check.py [--json] [--receipt PATH] [--docs-recursive] [--top 10]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:  # self-steal: reuse cite_gate's extraction primitives
    from mag import cite_gate as _cg
    URL_RE = _cg.URL_RE
    _CG_ANCHOR = _cg._ANCHOR
    _TRAIL = _cg._TRAIL_PUNCT
    STOLE_FROM = "mag/cite_gate.py"
except Exception:  # noqa: BLE001 - standalone fallback, same patterns
    URL_RE = re.compile(r"https?://[^\s<>\"'`\]\}]+")
    _CG_ANCHOR = r"(?:state|watch|memory|mag|corpus|docs|configs|queue|handoff|docker|salon|tools|dashboard)"
    _TRAIL = ".,;:!?'\"*"
    STOLE_FROM = None

SKIP_TOP = re.compile(r"^(\.pytest|__pycache__|\.git$|\.venv$|%)")
TOP_DIRS = sorted(d.name for d in ROOT.iterdir() if d.is_dir() and not SKIP_TOP.match(d.name))
_extra = "|".join(re.escape(d) for d in TOP_DIRS)
ANCHOR = rf"(?:{_CG_ANCHOR[3:-1]}|{_extra})" if _extra else _CG_ANCHOR
SEG = r"[\w.@+\-*?{}<>$]+"
# anchored path: optional ./ or ../ or %~dp0 prefix, anchor dir, then >= 1 segment
PATH_RE = re.compile(
    rf"(?<![\w./\\%-])(?P<pre>%~dp0\\?|%~dp0/|\.\.?[/\\])?(?P<p>{ANCHOR}(?:[/\\]{SEG})+[/\\]?)"
)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\((?P<t>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
VAR_RE = re.compile(r"%[A-Za-z_][\w]*%|![A-Za-z_]\w*!|\$\{?[A-Za-z_]\w*\}?|%\d")
TEMPLATE_RE = re.compile(r"[<>{}$]|YYYY|MMDD|HHMM|XXXX|\bNNN\b|<seat>|\.\.\.|[_-]$")
# a line that itself says the path is dead documents it; not a dead link
DOCUMENTED_DEAD_RE = re.compile(r"never existed|does not exist|doesn't exist|no longer exists", re.I)
GLOB_RE = re.compile(r"[*?]")
EXT_RE = re.compile(r"\.(?!v\d+$)[A-Za-z0-9]{1,6}$")
TICK_RE = re.compile(r"`[^`]+`")
# headings under which dead refs are deliberately kept (documented phantom ledgers)
PHANTOM_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s.*\b(phantom|tombstone|graveyard|dead refs?)\b", re.I)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
SIBLINGS = sorted(d.name for d in ROOT.parent.iterdir() if d.is_dir() and d.name != ROOT.name)


def collect_docs(docs_recursive: bool) -> list[Path]:
    out: list[Path] = []
    out += sorted(ROOT.glob("*.md"))
    out += sorted((ROOT / "docs").rglob("*.md") if docs_recursive else (ROOT / "docs").glob("*.md"))
    out += sorted((ROOT / ".agents").rglob("*.md"))
    out += sorted((ROOT / "state").rglob("*.md"))
    mm = ROOT / "memory" / "MEMORY.md"
    if mm.is_file():
        out.append(mm)
    for ext in ("*.cmd", "*.bat", "*.vbs"):
        out += sorted(ROOT.glob(ext))
        out += sorted((ROOT / "scripts").rglob(ext))
    seen, uniq = set(), []
    for p in out:
        if p.is_file() and p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def _clean(p: str) -> str:
    p = p.rstrip(_TRAIL + ")]`")
    return p.replace("\\", "/")


def _exists(rel: str, base: Path) -> bool:
    rel = rel.split("#", 1)[0].split("?", 1)[0]
    if not rel:
        return True
    for cand in (ROOT / rel, base / rel):
        try:
            if cand.exists():
                return True
        except OSError:
            continue
    return False


def _cross_repo(rel: str, line: str) -> str | None:
    for s in SIBLINGS:
        if s in line and (ROOT.parent / s / rel).exists():
            return s
    return None


def scan_doc(doc: Path) -> dict[str, Any]:
    is_md = doc.suffix.lower() == ".md"
    text = doc.read_text(encoding="utf-8", errors="replace")
    base = doc.parent
    refs: dict[str, dict[str, Any]] = {}
    counts = Counter()
    in_fence = False
    in_phantom = False
    phantom: list[dict[str, Any]] = []
    for ln, line in enumerate(text.splitlines(), 1):
        if is_md and not in_fence and HEADING_RE.match(line):
            in_phantom = bool(PHANTOM_HEADING_RE.match(line))
        if is_md and FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            counts["skipped_in_fence"] += len(PATH_RE.findall(line))
            continue
        masked = URL_RE.sub(lambda m: " " * len(m.group(0)), line)
        found: list[tuple[str, bool]] = []
        link_spans: list[tuple[int, int]] = []
        if is_md:
            for m in MD_LINK_RE.finditer(masked):
                link_spans.append(m.span())
                t = m.group("t").strip("<>")
                if re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I) or t.startswith("#"):
                    continue  # mailto:, file:, anchors
                found.append((t, True))
        ticks = [m.span() for m in TICK_RE.finditer(masked)]
        for m in PATH_RE.finditer(masked):
            a0 = m.start("p")
            if any(x <= a0 < y for x, y in link_spans):
                continue  # already taken as a markdown link target
            p = _clean(m.group("p"))
            in_tick = any(x <= a0 < y for x, y in ticks)
            if not (in_tick or p.endswith("/") or EXT_RE.search(p) or not is_md):
                counts["prose_slash_skipped"] += 1  # e.g. "bridge/MCP/probe" in prose
                continue
            found.append((m.group("p"), False))
        for raw, is_link in found:
            rel = _clean(raw)
            if not rel or rel in ("./", "../"):
                continue
            if VAR_RE.search(rel):
                counts["variables"] += 1
                continue
            if GLOB_RE.search(rel):
                counts["globs"] += 1
                continue
            if TEMPLATE_RE.search(rel):
                counts["templates"] += 1
                continue
            if rel in refs:
                continue
            ok = _exists(rel, base)
            xr = None if ok else _cross_repo(rel, line)
            if not ok and not xr and DOCUMENTED_DEAD_RE.search(line):
                counts["documented_dead"] += 1
                refs[rel] = {"ref": rel, "line": ln, "exists": False, "cross_repo": None, "phantom": True}
                continue
            if not ok and not xr and in_phantom:
                phantom.append({"ref": rel, "line": ln})
                refs[rel] = {"ref": rel, "line": ln, "exists": False, "cross_repo": None, "phantom": True}
                continue
            refs[rel] = {"ref": rel, "line": ln, "exists": ok, "cross_repo": xr, "md_link": is_link}
    missing = [r for r in refs.values() if not r["exists"] and not r["cross_repo"] and not r.get("phantom")]
    return {
        "doc": doc.relative_to(ROOT).as_posix(),
        "refs": len(refs),
        "missing": missing,
        "cross_repo": [r for r in refs.values() if r["cross_repo"]],
        "counts": dict(counts),
        "phantom": phantom,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Report-only repo-relative doc link checker.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--receipt", help="write a JSON receipt to this repo-relative path")
    ap.add_argument("--docs-recursive", action="store_true", help="scan docs/**/*.md, not just docs/*.md")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args(argv)

    docs = collect_docs(a.docs_recursive)
    results = [scan_doc(d) for d in docs]
    total_refs = sum(r["refs"] for r in results)
    total_missing = sum(len(r["missing"]) for r in results)
    agg = Counter()
    for r in results:
        agg.update(r["counts"])
    with_missing = sorted((r for r in results if r["missing"]), key=lambda r: (-len(r["missing"]), r["doc"]))
    summary = {
        "schema": "doc_link_check.v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "self_steal": STOLE_FROM,
        "scope": "root *.md, docs/" + ("**" if a.docs_recursive else "") + "*.md, .agents/**/*.md, state/**/*.md, "
                 "memory/MEMORY.md, root + scripts/** *.cmd/*.bat/*.vbs",
        "docs_scanned": len(docs),
        "refs_checked": total_refs,
        "missing_total": total_missing,
        "docs_with_missing": len(with_missing),
        "cross_repo_resolved": sum(len(r["cross_repo"]) for r in results),
        "phantom_ledger_dead": sum(len(r["phantom"]) for r in results),
        "excluded": {"globs": agg.get("globs", 0), "variables": agg.get("variables", 0),
                     "templates": agg.get("templates", 0), "in_code_fence": agg.get("skipped_in_fence", 0),
                     "prose_slash": agg.get("prose_slash_skipped", 0),
                     "documented_dead_same_line": agg.get("documented_dead", 0)},
        "top_docs": [{"doc": r["doc"], "missing": len(r["missing"])} for r in with_missing[: a.top]],
        "by_doc": {r["doc"]: [{"ref": m["ref"], "line": m["line"]} for m in r["missing"]] for r in with_missing},
        "cross_repo": {r["doc"]: [{"ref": m["ref"], "line": m["line"], "repo": m["cross_repo"]} for m in r["cross_repo"]]
                       for r in results if r["cross_repo"]},
    }
    if a.receipt:
        out = (ROOT / a.receipt).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    if a.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        for r in with_missing:
            print(f"\n{r['doc']}  ({len(r['missing'])} missing of {r['refs']})")
            for m in r["missing"]:
                print(f"  L{m['line']}: {m['ref']}")
        print(f"\nDOC LINK CHECK: {total_missing} missing of {total_refs} refs across {len(docs)} docs "
              f"({len(with_missing)} docs with dead refs)")
        ex = summary["excluded"]
        print(f"  excluded: globs={ex['globs']} variables={ex['variables']} templates={ex['templates']} "
              f"in_code_fence={ex['in_code_fence']} prose_slash={ex['prose_slash']} "
              f"documented_dead_same_line={ex['documented_dead_same_line']}")
        print(f"  cross_repo_resolved={summary['cross_repo_resolved']}  "
              f"phantom_ledger_dead={summary['phantom_ledger_dead']} (deliberately kept under PHANTOM headings, not counted)")
        print(f"  top {a.top}:")
        for t in summary["top_docs"]:
            print(f"    {t['missing']:>4}  {t['doc']}")
        if a.receipt:
            print(f"  receipt: {a.receipt}")
    return 1 if total_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
