from pathlib import Path
keys = ("calcifer", "howl", "hearth demon", "fire demon", "moving castle")
folders = [
    Path("memory/biography"), Path("memory/sessions"), Path("memory/diary"),
    Path("memory/story"), Path("memory/working/game_characters"),
    Path("memory/runs/party_subchain"), Path("memory/briefs"),
    Path("memory/operator_directives.md"),
]
for folder in folders:
    paths = [folder] if folder.is_file() else list(folder.rglob("*") if folder.exists() else [])
    for p in paths:
        if p.is_dir() or not p.is_file():
            continue
        if p.suffix not in {".md", ".json", ".jsonl", ".txt"}:
            continue
        if p.stat().st_size > 1_500_000:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue
        if any(k in t for k in keys):
            print("HIT", p)
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if any(k in line.lower() for k in keys):
                    print(f"  {i}: {line[:160]}")
