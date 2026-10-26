"""Third-stage overlap inspection: context windows around the hits that decide
bank-vs-skip for the 2026-10-11 inference-efficiency sweep.
"""
import os
import re

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")


def windows(path, pattern, before=0, after=2, limit=8, width=240):
    """Print up to `limit` context windows around regex hits in a text file."""
    try:
        text = open(path, "r", encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print(f"  !! {path}: {exc}")
        return
    lines = text.splitlines()
    rx = re.compile(pattern, re.IGNORECASE)
    shown = 0
    hit_lines = set()
    for i, line in enumerate(lines):
        if rx.search(line):
            for j in range(max(0, i - before), min(len(lines), i + after + 1)):
                hit_lines.add(j)
    # collapse consecutive groups
    group, prev = [], None
    for j in sorted(hit_lines):
        if prev is not None and j != prev + 1:
            shown += 1
            if shown >= limit:
                break
        group.append(j)
        prev = j
    for j in group[:40]:
        print(f"  L{j+1}: {lines[j][:width]}")


def catalog_like(substr):
    n = 0
    with open(CATALOG, "r", encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            if substr in line.lower():
                n += 1
                if n <= 8:
                    print(f"  line {i+1}: {line.strip()[:320]}")
    print(f"  -> total rows: {n}")


if __name__ == "__main__":
    print("=== catalog rows containing 'leviathan'")
    catalog_like("leviathan")

    print("\n=== gapwave skill_quantization.md :: cactus/needle context")
    windows(
        os.path.join(ROOT, "memory", "runs", "gapwave", "hn_x_fanout", "skill_quantization.md"),
        r"cactus|needle",
    )

    print("\n=== gapwave context_economics_1m.md :: zartbot context")
    windows(
        os.path.join(ROOT, "memory", "runs", "gapwave", "context_economics_1m.md"),
        r"zartbot",
    )

    print("\n=== research_polished/kv_cache_compaction.md :: prompt caching / GPT-6 context")
    windows(
        os.path.join(ROOT, "memory", "research_polished", "kv_cache_compaction.md"),
        r"better prompt caching|gpt-6|openai",
    )

    print("\n=== quote_audit_wide inbox_concat.txt :: planetscale context")
    windows(
        os.path.join(ROOT, "memory", "runs", "quote_audit_wide_20260925", "inbox_concat.txt"),
        r"planetscale|\btin\b",
        limit=6,
    )

    print("\n=== mickey17_v2 lanes/small-model-agents.json :: cactus context")
    windows(
        os.path.join(ROOT, "memory", "runs", "mickey17_v2", "lanes", "small-model-agents.json"),
        r"cactus",
        limit=6,
    )
