"""Pack Mag archaeology slice onto the host, split under 24MB for chat."""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = ROOT / "_archaeology_out"
OUT.mkdir(exist_ok=True)
STAGING = OUT / "mag-disk-20260905"
if STAGING.exists():
    import shutil
    shutil.rmtree(STAGING)
STAGING.mkdir()

INCLUDE_DIRS = [
    "mag",
    "dashboard",
    "memory/steal",
    "memory/game",
    "memory/working/game_campaigns",
    "memory/working/game_sessions",
    "memory/working/party_subchain",
    "handoff",
]
INCLUDE_GLOBS = [
    "STEAL_*.md",
    "_patch*.py",
    "_prove*.py",
    "_afk*.py",
    "afk_speak_proof*.py",
    "mag.cmd",
    "mag.ps1",
    "docker-compose.yml",
    "Dockerfile",
    "CONSTITUTION.md",
    "AGENTS.md",
    "RUNNING.md",
    "README.md",
]
SKIP_PARTS = {".venv", "node_modules", "__pycache__", ".git", "models", ".pytest_cache"}

copied = 0
bytes_in = 0

def should_skip(path: Path) -> bool:
    return any(p in SKIP_PARTS for p in path.parts)

def copy_file(src: Path, dest: Path) -> None:
    global copied, bytes_in
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    dest.write_bytes(data)
    copied += 1
    bytes_in += len(data)

for rel in INCLUDE_DIRS:
    src = ROOT / rel
    if not src.exists():
        print("MISSING", rel)
        continue
    if src.is_file():
        copy_file(src, STAGING / rel)
        continue
    for f in src.rglob("*"):
        if not f.is_file() or should_skip(f):
            continue
        # skip huge binaries
        if f.suffix.lower() in {".pt", ".bin", ".safetensors", ".gguf", ".onnx", ".mp4", ".zip"}:
            continue
        if f.stat().st_size > 8_000_000:
            print("SKIP big", f.relative_to(ROOT), f.stat().st_size)
            continue
        copy_file(f, STAGING / f.relative_to(ROOT))

for pattern in INCLUDE_GLOBS:
    for f in ROOT.glob(pattern):
        if f.is_file() and not should_skip(f):
            copy_file(f, STAGING / f.name)

# manifest
man = STAGING / "00_MANIFEST_MAG_DISK.md"
man.write_text(
    f"""# Mag disk archaeology — 2026-09-05

Host: DESKTOP-7C70KSC
Root: {ROOT}

Included: mag/, dashboard/, memory/steal|game|working (campaigns/sessions/party_subchain),
handoff/, STEAL_*.md, _patch/_prove/_afk scripts, mag.cmd/ps1, docker basics.

Excluded: .venv, models, node_modules, .git, pytest caches, files >8MB.

Files staged: {copied}
Bytes staged: {bytes_in}
""",
    encoding="utf-8",
)

# One zip then split
full = OUT / "nacho-archaeology-part8-mag-disk-FULL.zip"
with zipfile.ZipFile(full, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in STAGING.rglob("*"):
        if f.is_file():
            z.write(f, arcname=str(Path("mag-disk") / f.relative_to(STAGING)))
print("FULL", full.stat().st_size)

# Split into parts under 24MB by walking files into buckets
LIMIT = 24 * 1024 * 1024
files = [f for f in STAGING.rglob("*") if f.is_file()]
# largest first packing into bins
files.sort(key=lambda p: p.stat().st_size, reverse=True)
bins: list[list[Path]] = [[]]
sizes = [0]
for f in files:
    sz = f.stat().st_size
    # compressed estimate ~0.4 for text; be conservative use raw for limit of compressed zip
    # put large alone
    placed = False
    for i, s in enumerate(sizes):
        # rough: assume compress to 50% for estimate when adding
        if s + max(sz // 2, min(sz, 500_000)) < LIMIT or not bins[i]:
            bins[i].append(f)
            sizes[i] += max(sz // 2, min(sz, 500_000))
            placed = True
            break
    if not placed:
        bins.append([f])
        sizes.append(max(sz // 2, min(sz, 500_000)))

parts = []
for i, bucket in enumerate(bins, start=8):
    path = OUT / f"nacho-archaeology-part{i}-mag-disk.zip"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in bucket:
            z.write(f, arcname=str(Path("mag-disk") / f.relative_to(STAGING)))
    actual = path.stat().st_size
    print("PART", path.name, actual)
    # if over limit, fail loudly
    if actual > LIMIT:
        print("OVER", path.name)
    parts.append((path, actual))

print("DONE", len(parts), "parts", "files", copied)
