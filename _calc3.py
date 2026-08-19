from pathlib import Path
files = [
    Path("memory/working.md"),
    Path("memory/runs/party_subchain/chain.jsonl"),
    Path("memory/operator_directives.md"),
    Path("memory/game/STATE.md"),
    Path("memory/knowledge_packs/dnd-classic-stub/datasheet.json"),
    Path("memory/game_modules/dnd_classic_stub.v1.json"),
    Path("memory/narrative_corpus/rashomon/tavern_bar_fight_party.v1.md"),
]
for p in files:
    if not p.exists():
        print("missing", p)
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    low = t.lower()
    if "calcifer" in low or "howl" in low:
        print("HIT", p)
        for i, line in enumerate(t.splitlines(), 1):
            if "calcifer" in line.lower() or ("howl" in line.lower() and "howl" in line.lower()):
                print(f"  {i}: {line[:180]}")
    else:
        print("no", p.name)
