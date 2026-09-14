from pathlib import Path
need = ("fireball", "babel", "percolat", "howl", "calcifer", "steampunk", "steam punk", "babel fish")
roots = [
    Path("memory"), Path("mag"),
]
skip = {".venv", "node_modules", "__pycache__", ".git", "mine"}
hits = {k: [] for k in need}
for folder in roots:
    if not folder.exists():
        continue
    for p in folder.rglob("*"):
        if any(s in p.parts for s in skip):
            continue
        if not p.is_file() or p.suffix not in {".md", ".json", ".jsonl", ".txt", ".py", ".yaml"}:
            continue
        if p.stat().st_size > 900_000:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        low = t.lower()
        for k in need:
            if k in low:
                lines = []
                for i, line in enumerate(t.splitlines(), 1):
                    if k in line.lower():
                        lines.append(f"{i}:{line.strip()[:160]}")
                        if len(lines) >= 3:
                            break
                hits[k].append((str(p), lines))
for k, arr in hits.items():
    print("====", k, "n=", len(arr))
    for path, lines in arr[:8]:
        print(" ", path)
        for ln in lines:
            print("   ", ln)
