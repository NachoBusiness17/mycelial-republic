"""Overlap grep for the finetuning-adaptation arxiv sweep (2026-10-05).

Searches catalog/catalog.jsonl and memory/ (plus corpus/ for steal notes) for
exact arXiv IDs and distinctive title phrases of the pass-2 deep-read items.
Run: .venv\\Scripts\\python.exe .tmp_sweep_ftarxiv_overlap.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

PHRASES = [
    "2609.17848", "SFT or RL for Tool-Calling Agents",
    "2609.24115", "EDGEGEN",
    "2609.10750", "When Synthetic Data Hurts",
    "2610.02142", "Keyword Harnesses Fail Open",
    "2609.25373", "FunctionGemma",
    "2609.35259", "Systematic Study of Distillation Dynamics",
    "2502.06659", "Who Taught You That",
    "2609.23916", "Time-Incremental Continued Pretraining",
    "2609.19513", "QVAC Genesis",
    # near-bank / considered items
    "2610.00890", "Cross-Benchmark Transfer from RL on Agentic Coding",
    "2609.06124", "State-Guided Data Synthesis with Argument Provenance",
    "2609.28395", "General Forgetting Mitigation Does Not Preserve",
    "2610.02710", "Self-Supervised Scaling of Terminal Environments",
    # estate context sanity probes
    "Gero-4B",
]

TARGETS = [
    os.path.join(ROOT, "catalog", "catalog.jsonl"),
    os.path.join(ROOT, "memory"),
]

EXTS = {".jsonl", ".md", ".txt", ".json", ".py", ".yaml", ".yml"}


def iter_files():
    for tgt in TARGETS:
        if os.path.isfile(tgt):
            yield tgt
        elif os.path.isdir(tgt):
            for dirpath, _dirnames, filenames in os.walk(tgt):
                for fn in filenames:
                    if os.path.splitext(fn)[1].lower() in EXTS:
                        yield os.path.join(dirpath, fn)


def main():
    hits = {}
    for path in iter_files():
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh, 1):
                    for ph in PHRASES:
                        if ph.lower() in line.lower():
                            snippet = line.strip()
                            if len(snippet) > 160:
                                pos = snippet.lower().find(ph.lower())
                                start = max(0, pos - 60)
                                snippet = "..." + snippet[start:start + 160] + "..."
                            key = ph
                            hits.setdefault(key, []).append(
                                (os.path.relpath(path, ROOT), lineno, snippet)
                            )
        except OSError as exc:
            print(f"WARN unreadable {path}: {exc}", file=sys.stderr)
    for ph in PHRASES:
        rows = hits.get(ph, [])
        print(f"== '{ph}': {len(rows)} hit(s)")
        for rel, lineno, snippet in rows[:4]:
            print(f"   {rel}:{lineno} :: {snippet}")


if __name__ == "__main__":
    main()
