from pathlib import Path
root = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
steal = root / "memory" / "steal"
print("=== steal dir ===")
if steal.exists():
    files = sorted(steal.rglob("*"), key=lambda p: p.stat().st_mtime if p.is_file() else 0, reverse=True)
    for p in files:
        if p.is_file() and p.suffix in {".md", ".json", ".txt"}:
            print(f"{p.stat().st_size:7} {p.relative_to(root)}")
else:
    print("no steal dir")
print("=== mag game organs ===")
for p in sorted((root/"mag").glob("*.py")):
    n = p.name.lower()
    if any(k in n for k in ("game","wow","mud","chasm","quest","df_","world","campaign","wave","view","tileset","story","brawl")):
        print(p.name, p.stat().st_size)
