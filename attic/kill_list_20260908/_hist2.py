from pathlib import Path
# targeted small files first
needles = ["fireball", "babel", "percolat", "howl", "calcifer", "steampunk"]
files = []
for folder in [Path("memory/game"), Path("memory/working"), Path("memory/steal"), Path("memory/narrative_corpus"), Path("memory/runs"), Path("memory/knowledge_packs"), Path("memory/dungeon")]:
    if not folder.exists():
        continue
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".json", ".jsonl", ".txt"} and p.stat().st_size < 400000:
            files.append(p)
print("files", len(files))
for k in needles:
    n = 0
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if k in t.lower():
            n += 1
            print("HIT", k, p)
            for i, line in enumerate(t.splitlines(), 1):
                if k in line.lower():
                    print(" ", i, line.strip()[:180])
                    break
    print("done", k, n)
