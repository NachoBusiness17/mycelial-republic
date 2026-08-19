from pathlib import Path
g = Path("mag/game_campaign.py").read_text(encoding="utf-8")
i = g.find("def _look_at")
print("==== LOOK_AT ====")
print(g[i:i+1400] if i>=0 else "missing")
print("==== TALK_EVENTS ====")
i = g.find("def _talk_events")
print(g[i:i+1800] if i>=0 else "missing")
print("==== CLAW ====")
root = Path(".")
hits = []
for p in root.rglob("*"):
    if p.is_file() and p.suffix in {".json",".md",".py",".yaml",".yml"} and p.stat().st_size < 2_000_000:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "claw_hall" in t or "Claw-Marked" in t:
            hits.append(str(p))
print("files", hits[:20])
