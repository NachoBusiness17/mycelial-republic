from pathlib import Path
need = "calcifer"
for folder in [Path("memory/copilot"), Path("memory/grok"), Path("memory/chatgpt"), Path("memory/press"), Path("memory/embassy"), Path("memory/working/chasm"), Path("memory/agent_sessions"), Path("memory/sessions")]:
    if not folder.exists():
        print("skip", folder)
        continue
    n = 0
    for p in folder.rglob("*"):
        if not p.is_file() or p.stat().st_size > 400000:
            continue
        if p.suffix not in {".md", ".json", ".jsonl", ".txt"}:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if need in t.lower():
            n += 1
            print("HIT", p)
            for i, line in enumerate(t.splitlines(), 1):
                if need in line.lower():
                    print(f"  {i}: {line[:200]}")
                    break
    print("done", folder, "hits", n)
