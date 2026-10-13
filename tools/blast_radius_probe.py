"""Blast-radius probe: ALLOW_RE x ENT counter-leak quantification.

Reads tools/secret_gate_rules.py (ALLOW_RE, ENTROPY_MIN=4.3, ENT_LEN_MIN=25)
and scans source files in sample repos. Counts tokens that match ALLOW_RE
AND have Shannon entropy >= ENTROPY_MIN — the hidden findings the scanner
silently drops on line 275-276 of secret_gate_scan.py.
"""
from __future__ import annotations

import math
import os
import re
import sys
import json
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.secret_gate_rules import ALLOW_RE, ENTROPY_MIN, ENT_LEN_MIN

ROOT = Path(__file__).resolve().parent.parent
REPO_CANDIDATES = [
    "local_sovereign_agent",
    "mycelial-republic",
    "azerothcore-wow",
    "embassy-aos",
    "embassy-sandbox",
    "livingmud",
    "laptop_bridge",
    "bond-audit",
    "audit_prep",
    "field-strike-the-chord",
    "env-secrets-checker",
    "codex_pytest_desk",
    "codex_pytest_factory",
    "laptop_seat.git",
    "Mag-backup.git",
    "mag-current-rebuild",
]

SOURCE_EXT = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".c", ".h",
    ".cpp", ".hpp", ".cs", ".rb", ".php", ".lua", ".toml", ".yaml", ".yml",
    ".json", ".md", ".txt", ".cfg", ".ini", ".sh", ".bash", ".ps1",
}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
             "target", "dist", "build", ".tox", ".mypy_cache", ".pytest_cache"}


def shannon(s: str) -> float:
    if not s:
        return 0.0
    freq = Counter(s)
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def allowlist_clause(tok: str) -> str:
    """Return which ALLOW_RE clause matched, or 'other'."""
    lower = tok.lower()
    if "your_api_key" in lower or "your-api-key" in lower:
        return "your_api_key"
    if "your_token" in lower or "your-token" in lower:
        return "your_token"
    if tok.startswith("<") and tok.endswith(">"):
        return "angle_bracket"
    if tok.startswith("${") and tok.endswith("}"):
        return "dollar_brace"
    if re.match(r"^x{4,}$", tok, re.I):
        return "x_repeat"
    if re.match(r"^\.{4,}$", tok):
        return "dot_repeat"
    if re.match(r"^\*{3,}$", tok):
        return "star_repeat"
    if tok.upper() == "REDACTED":
        return "REDACTED"
    if tok.upper() == "MASKED":
        return "MASKED"
    if tok.upper() == "PLACEHOLDER":
        return "PLACEHOLDER"
    if tok.upper().startswith("EXAMPLE"):
        return "EXAMPLE"
    if tok.upper() in ("DUMMY", "FAKE"):
        return tok.upper()
    if tok == "abcd1234":
        return "abcd1234"
    if tok == "1234567890":
        return "1234567890"
    if tok == "0123456789abcdef":
        return "0123456789abcdef"
    return "other"


def scan_repo(repo_path: Path, max_files: int = 500) -> dict:
    stats = {"repo": repo_path.name, "files_scanned": 0,
             "allow_hit_total": 0, "allow_high_entropy": 0,
             "by_clause": Counter(), "examples": []}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SOURCE_EXT:
                continue
            fpath = Path(root) / fname
            rel = str(fpath.relative_to(ROOT)) if fpath.is_relative_to(ROOT) else str(fpath)
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            stats["files_scanned"] += 1
            if stats["files_scanned"] >= max_files:
                break
            for line in content.splitlines():
                # tokens: contiguous non-whitespace, >= ENT_LEN_MIN
                for raw in line.split():
                    tok = raw.strip("'\"`[],:;(){}")
                    if len(tok) < ENT_LEN_MIN:
                        continue
                    if not ALLOW_RE.search(tok):
                        continue
                    stats["allow_hit_total"] += 1
                    h = shannon(tok)
                    clause = allowlist_clause(tok)
                    if h >= ENTROPY_MIN:
                        stats["allow_high_entropy"] += 1
                        stats["by_clause"][clause] += 1
                        if len(stats["examples"]) < 10:
                            stats["examples"].append({
                                "clause": clause, "token": mask(tok),
                                "entropy": round(h, 2), "len": len(tok),
                                "file": rel,
                            })
        if stats["files_scanned"] >= max_files:
            break
    return stats


def mask(tok: str) -> str:
    if len(tok) <= 6:
        return tok
    return tok[:3] + "..." + tok[-3:]


def main():
    print(f"ALLOW_RE pattern: {ALLOW_RE.pattern}")
    print(f"ENTROPY_MIN={ENTROPY_MIN}  ENT_LEN_MIN={ENT_LEN_MIN}")
    print(f"Root: {ROOT}")
    print()

    all_repos = []
    for name in REPO_CANDIDATES:
        p = ROOT / name
        if p.is_dir():
            all_repos.append(p)
        else:
            print(f"  SKIP {name}: not found")

    # Fallback: grab any extra git repos under projects
    if len(all_repos) < 5:
        projects = ROOT.parent
        for p in sorted(projects.iterdir()):
            if p.is_dir() and (p / ".git").is_dir() and p not in all_repos:
                all_repos.append(p)

    repos = all_repos[:10]
    print(f"Scanning {len(repos)} repos: {[r.name for r in repos]}")
    print("=" * 70)

    total_allow = 0
    total_high = 0
    total_files = 0
    all_clauses = Counter()
    all_examples = []

    for repo in repos:
        s = scan_repo(repo)
        total_files += s["files_scanned"]
        total_allow += s["allow_hit_total"]
        total_high += s["allow_high_entropy"]
        all_clauses.update(s["by_clause"])
        all_examples.extend(s["examples"])
        print(f"\n--- {s['repo']} ({s['files_scanned']} files) ---")
        print(f"  ALLOW hits: {s['allow_hit_total']}  high-entropy leaks: {s['allow_high_entropy']}")
        if s["by_clause"]:
            for clause, cnt in s["by_clause"].most_common():
                print(f"    {clause}: {cnt}")

    print("\n" + "=" * 70)
    print(f"TOTAL files scanned: {total_files}")
    print(f"TOTAL ALLOW hits (any entropy): {total_allow}")
    print(f"TOTAL HIGH-ENTROPY ALLOW hits (blast radius): {total_high}")
    if total_allow > 0:
        print(f"FRACTION of ALLOW hits that are high-entropy leaks: {total_high}/{total_allow} = {total_high/total_allow:.1%}")
    print(f"\nBy clause (high-entropy only):")
    for clause, cnt in all_clauses.most_common():
        print(f"  {clause}: {cnt}")
    if all_examples:
        print(f"\nExamples (max 10):")
        for ex in all_examples[:10]:
            print(f"  [{ex['clause']}] entropy={ex['entropy']} len={ex['len']} file={ex['file']} token={ex['token']}")

    # Check fleet scan history
    print("\n--- Fleet scan history ---")
    history_dir = ROOT / "memory" / "runs"
    if history_dir.is_dir():
        gate_dirs = sorted(history_dir.glob("20260727T203059Z-gate-test-*"))
        gate_dirs += sorted(history_dir.glob("20260727T214717Z-seat-gate-verify-*"))
        for d in gate_dirs:
            print(f"  {d.name}")
            # check for count files
            for f in d.iterdir():
                if f.is_file() and f.suffix in (".json", ".jsonl", ".txt", ".md"):
                    try:
                        txt = f.read_text(encoding="utf-8", errors="replace")[:300]
                        print(f"    {f.name}: {txt[:150]}")
                    except Exception:
                        pass
    else:
        print("  No memory/runs/ directory found")


if __name__ == "__main__":
    main()