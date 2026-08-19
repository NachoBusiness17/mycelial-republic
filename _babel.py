from pathlib import Path
needles = ("babel", "babelfish", "babel fish", "familiar", "liquid familiar", "fireball")
roots = [Path("memory/game"), Path("memory/working"), Path("memory/steal"), Path("memory/narrative_corpus"), Path("memory/knowledge_packs"), Path("memory/dungeon"), Path("memory/runs/party_subchain")]
for k in needles:
    print("====", k)
    n = 0
    for folder in roots:
        if not folder.exists():
            continue
        for p in folder.rglob("*"):
            if not p.is_file() or p.suffix not in {".md", ".json", ".jsonl", ".txt", ".py"}:
                continue
            if p.stat().st_size > 500000:
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if k not in t.lower():
                continue
            n += 1
            print("HIT", p)
            for i, line in enumerate(t.splitlines(), 1):
                if k in line.lower():
                    print(" ", i, line.strip()[:200])
                    if n > 0 and i > 0:
                        pass
                    if sum(1 for _ in [1]) and line:
                        break
            if n >= 12:
                break
        if n >= 12:
            break
    print("n", n)
