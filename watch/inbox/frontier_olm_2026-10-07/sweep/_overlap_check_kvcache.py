"""Overlap check for the kv-cache-context-engineering-hn sweep (2026-10-07).

No subprocess spawns; plain file reads only (win32 CREATE_NO_WINDOW law is N/A).
Mandated check: exact title / distinctive phrase vs catalog/catalog.jsonl and
every file under memory/. Courtesy extra: sibling sweep .md files in this run.
"""
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
SWEEP = ROOT / "watch" / "inbox" / "frontier_olm_2026-10-07" / "sweep"

PHRASES = {
    "agentic-kv-cache": ["agentic-kv-cache", "LRU is harder to beat"],
    "compaction-measured": ["context-compaction-measured", "FutureOS"],
    "doug.sh-vllm": ["vllm-kv-cache-agents", "Prefix Cache Warm"],
    "dsv41flash": ["dsv41flash", "DeepSeek-V4.1-Flash", "DeepSeek V4.1 Flash"],
    "mempko-keepalive": ["keeping-the-kv-cache-warm-measuring", "mempko"],
    "context-rot": ["context-rot-quantified", "boolean.ai"],
    "yandex-runtime": ["the-kv-cache-as-an-agent-runtime", "Hogwild"],
    "lensvlm": ["LensVLM"],
    "estate-anchors": ["BreadthKV", "890 bytes per token"],
}

def counts(text, phrases):
    low = text.lower()
    return {p: low.count(p.lower()) for p in phrases}

def main():
    mandated = [ROOT / "catalog" / "catalog.jsonl"]
    mandated += [p for p in (ROOT / "memory").rglob("*") if p.is_file()]
    courtesy = [p for p in SWEEP.glob("*.md") if p.is_file()]

    agg = {name: {p: 0 for p in ps} for name, ps in PHRASES.items()}
    sib_agg = {name: {p: 0 for p in ps} for name, ps in PHRASES.items()}
    files_scanned = 0
    for f in mandated:
        if not f.exists():
            print(f"MISSING: {f}")
            continue
        files_scanned += 1
        text = f.read_text(encoding="utf-8", errors="ignore")
        for name, ps in PHRASES.items():
            for p, n in counts(text, ps).items():
                agg[name][p] += n
    print(f"mandated corpus: {files_scanned} files (catalog/catalog.jsonl + memory/ tree)")
    for name, ps in PHRASES.items():
        for p in ps:
            n = agg[name][p]
            print(f"{'HIT ' if n else 'miss'} {n:>4}  [{name}]  {p!r}")

    print()
    print("courtesy: sibling sweep .md files in this frontier run")
    for f in courtesy:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for name, ps in PHRASES.items():
            for p, n in counts(text, ps).items():
                if n:
                    print(f"HIT {n:>4}  [{name}] {p!r} in {f.name}")
                    sib_agg[name][p] += n
    if not any(n for ps in sib_agg.values() for n in ps.values()):
        print("no sibling-sweep hits")

if __name__ == "__main__":
    main()
