"""Dead-instrument sweep for tools/ — Lane 2 Part B, run by the parent seat.

Lane 2's own harness crashed three times on `rg` PCRE look-around (its bug,
`rg: look-around ... is not supported`, needs --pcre2). This does the same
measurement in pure Python so the number exists regardless.

For each tools/*.py:
  referenced_by : how many OTHER repo files mention the module name
  has_test      : any tests/test_*.py mentioning it
  documented    : mentioned in AGENTS.md, githooks/, docs/, or main.py
  verdict       : LIVE / ORPHAN / DEAD
    LIVE   = referenced by code AND (tested or documented)
    ORPHAN = not referenced by any code
    DEAD   = not referenced anywhere at all (no code, no docs, no test)

Run: .venv/Scripts/python.exe memory/audit_20260926/dead_instrument_sweep.py
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO / "tools"

CODE_EXT = {".py", ".ps1", ".sh", ".bat", ".cmd", ".js", ".mjs"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__",
             "site-packages", ".pytest_cache", "corpus", "attic",
             "library", "mine", "raw"}

# Build one big lowercase haystack per file, and a code-only haystack.
code_hay, doc_hay, test_hay = {}, {}, {}
for p in list(REPO.glob("*.py")) + list(REPO.glob("*.md")) + \
         list((REPO / "mag").rglob("*.py")) + \
         list((REPO / "tools").glob("*.py")) + \
         list((REPO / "scripts").rglob("*")) + \
         list((REPO / "githooks").glob("*")) + \
         list((REPO / "tests").rglob("*.py")) + \
         list((REPO / "docs").rglob("*.md")) + \
         list((REPO / "memory").glob("*.md")) + \
         list((REPO / "queue").rglob("*.md")) + \
         list((REPO / "configs").rglob("*.yaml")):
    if not p.is_file():
        continue
    if any(part in SKIP_DIRS for part in p.parts):
        continue
    ext = p.suffix.lower()
    if ext not in CODE_EXT and ext not in (".md", ".txt", ".rst", ".yaml", ".yml", ".json") \
            and p.name not in ("pre-push", "pre-commit", "pre-commit.sample"):
        continue
    if ext in (".json",) and p.stat().st_size > 3_000_000:
        continue
    try:
        txt = p.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        continue
    key = str(p.relative_to(REPO)).replace("\\", "/")
    if ext in CODE_EXT or p.name in ("pre-push","pre-commit","pre-commit.sample"):
        code_hay[key] = txt
        if key.startswith("tests/"):
            test_hay[key] = txt
    else:
        doc_hay[key] = txt

# Explicit doc surfaces that count as "documented"
DOC_SURFACES = [k for k in doc_hay
                if k.startswith(("AGENTS.md", "docs/", "githooks/", "README"))
                or k == "main.py"]

rows = []
for t in sorted(TOOLS.glob("*.py")):
    mod = t.stem.lower()
    rel = str(t.relative_to(REPO)).replace("\\", "/")
    # word-ish match to avoid 'corpus' matching 'corpus_lens_run' etc.
    pat = re.compile(r"(?<![\w.])" + re.escape(mod) + r"(?![\w])")

    code_refs = [k for k, v in code_hay.items() if k != rel and pat.search(v)]
    test_refs = [k for k, v in test_hay.items() if k != rel and pat.search(v)]
    doc_refs = [k for k in DOC_SURFACES if pat.search(doc_hay[k])]

    if code_refs:
        verdict = "LIVE" if (test_refs or doc_refs) else "ORPHAN"
    elif doc_refs or test_refs:
        verdict = "ORPHAN"          # named in prose/tests but no code calls it
    else:
        verdict = "DEAD"
    rows.append({
        "tool": t.name, "module": mod,
        "referenced_by": len(code_refs),
        "code_refs": code_refs[:4],
        "has_test": bool(test_refs),
        "test_refs": test_refs[:2],
        "documented": bool(doc_refs),
        "doc_refs": doc_refs[:2],
        "verdict": verdict,
        "bytes": t.stat().st_size,
    })

tally = {}
for r in rows:
    tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1

print(f"tools/*.py examined      : {len(rows)}")
for k in ("LIVE", "ORPHAN", "DEAD"):
    print(f"  {k:8} {tally.get(k,0):4}")
print(f"  tested   {sum(1 for r in rows if r['has_test']):4}")
print(f"  docs-hit {sum(1 for r in rows if r['documented']):4}")
print()
print("THE DEAD SET (no code, no docs, no test reference anywhere):")
for r in rows:
    if r["verdict"] == "DEAD":
        print(f"   {r['tool']:38} {r['bytes']:>7} bytes")

out = Path(__file__).resolve().parent / "lane2_dead_instruments.json"
out.write_text(json.dumps({"tally": tally, "total": len(rows), "rows": rows}, indent=1),
               encoding="utf-8")
print(f"\nwrote {out}")
