"""Sacred-cow sweep helper: inventory game modules (docstring + function counts)."""
import re
from pathlib import Path

mods = sorted(p for p in Path("mag").glob("*.py")
              if re.search(r"game_|dungeon|quest|roshomon|adventure|abundance|campaign|arena", p.name))
for m in mods:
    txt = m.read_text(encoding="utf-8", errors="replace")
    doc = ""
    dm = re.search(r'"""(.*?)"""', txt, re.S)
    if dm:
        doc = re.sub(r"\s+", " ", dm.group(1)).strip()[:110]
    defs = re.findall(r"^def (\w+)", txt, re.M)
    public = [d for d in defs if not d.startswith("_")]
    print(f"{m.name:38} defs={len(defs):3} pub={len(public):3} | {doc}")
