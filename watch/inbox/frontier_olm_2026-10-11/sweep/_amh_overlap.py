"""amh overlap: per-item overlap greps for the 2026-10-11 agent-memory-continuity HN sweep.

Scans catalog/catalog.jsonl (line-by-line, count + sample paths) and a scoped
memory/ tree (rib, steal, improve, frontier, press, research_polished, zknot,
plus top-level md/json) for each candidate's distinctive phrases.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # repo root
CATALOG = ROOT / "catalog" / "catalog.jsonl"

PHRASES = {
    "harbor_agentsmd": ["gethrbr", "is-agents-md-useful", "2602.11988", "2605.10039",
                        "2606.12231", "2602.20478", "Codified Context"],
    "swarmagent": ["swarmagent", "Final Handoff", "Century Run"],
    "ihmt": ["IHMT", "Hierarchical Memory Tree"],
    "rutter": ["ruttermemory", "robin-cannon", "librarian-session"],
    "miniagi": ["volotat", "Mini-AGI", "learn less forget less", "Biderman"],
    "agentsmd_thread": ["2.1.277", "mpoteat"],
    "telemetry_thread": ["szypowi"],
    "jotbus": ["jotbus"],
    "kage_recall_neighbors": ["Kage memory", "ruttermemory"],
}

MEMORY_DIRS = ["rib", "steal", "improve", "frontier", "press", "research_polished",
               "zknot", "biography"]
MEMORY_FILES = list((ROOT / "memory").glob("*.md")) + list((ROOT / "memory").glob("*.json"))


def scan_catalog() -> dict:
    out: dict[str, list] = {k: [] for k in PHRASES}
    flat = [(k, p) for k, ps in PHRASES.items() for p in ps]
    with CATALOG.open(encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            for k, p in flat:
                if p.lower() in line.lower():
                    # pull path/title fields if present
                    m = re.search(r'"path":\s*"([^"]{0,160})"', line)
                    t = re.search(r'"title":\s*"([^"]{0,120})"', line)
                    out[k].append((i + 1, p, (t.group(1) if t else "") or (m.group(1) if m else "")))
    return out


def scan_memory() -> dict:
    out: dict[str, list] = {k: [] for k in PHRASES}
    targets: list[Path] = []
    for d in MEMORY_DIRS:
        p = ROOT / "memory" / d
        if p.is_dir():
            targets.extend(q for q in p.rglob("*") if q.is_file() and q.suffix in
                           (".md", ".json", ".jsonl", ".txt") and q.stat().st_size < 3_000_000)
    targets.extend(f for f in MEMORY_FILES if f.is_file())
    for f in targets:
        try:
            text = f.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue
        for k, ps in PHRASES.items():
            for phrase in ps:
                if phrase.lower() in text:
                    out[k].append((str(f.relative_to(ROOT)), phrase))
    return out


def main() -> None:
    cat = scan_catalog()
    mem = scan_memory()
    print("== catalog/catalog.jsonl ==")
    for k, hits in cat.items():
        print(f"{k:24s} {len(hits)} hits")
        for h in hits[:3]:
            print(f"    line {h[0]} [{h[1]}] {h[2][:110]}")
    print("== memory/ (scoped) ==")
    for k, hits in mem.items():
        uniq = sorted(set(hits))
        print(f"{k:24s} {len(uniq)} files")
        for h in uniq[:6]:
            print(f"    {h[0]} [{h[1]}]")


if __name__ == "__main__":
    main()
