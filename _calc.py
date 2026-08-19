from pathlib import Path
need = "calcifer"
roots = [
    Path("memory/steal"), Path("memory/narrative_corpus"), Path("memory/working"),
    Path("memory/runs/party_subchain"), Path("memory/game"), Path("memory/knowledge_packs"),
    Path("memory/rib"), Path("memory/runs/steer"), Path("mag"),
]
for folder in roots:
    if not folder.exists():
        continue
    for p in folder.rglob("*"):
        if p.suffix not in {".md", ".json", ".jsonl", ".txt", ".py"}:
            continue
        if not p.is_file() or p.stat().st_size > 800000:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if need in t.lower():
            print("HIT", p)
            for i, line in enumerate(t.splitlines(), 1):
                if need in line.lower():
                    print(f"  {i}: {line[:180]}")
