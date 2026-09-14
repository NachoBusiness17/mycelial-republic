#!/usr/bin/env python3
"""audit_bundle.py — build the EXTERNAL AUDIT bundle (what leaves the house).

Ships: code + architecture docs. Stays: keys, biography, journal, charged corpus,
sessions, models, logs, assets with unclear rights.

Run:  python scripts/audit_bundle.py
Out:  dist_audit/nacho_business_audit_<date>/  + a zip next to it + MANIFEST.txt
Law:  read-only on sources; every copied path is resolved and verified inside ROOT.
"""
import hashlib
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = ROOT / "dist_audit"

SHIP_DIRS = [
    "mag", "scripts", "backend", "configs", "dashboard/static",
    "site/build.py", "site/package.json", "site/wrangler.jsonc",
]
SHIP_FILES = [
    "docs/ref/STACK_V1.md",
    "docs/ref/ZAI_API_EXPERT_REFERENCE.md",
    "packs/p20_pending_20260912.json",
    "packs/p20_clarkes_end_20260912.json",
    "packs/p80_loom3_20260912.json",
]

EXCLUDE_PARTS = {
    ".env", ".mimosa", ".wrangler", "node_modules", "__pycache__",
    "memory", "journal", "handoff", "campaigns", "artifacts", "corpus",
    "logs", "models", "attic", "vault", "sessions", ".git", "suno", "dist_audit",
    "key", "secret", "credential",
}
EXCLUDE_FILES = {"agents.md", "claude.md", ".dev.vars", "readme.md"}
BIG = 3_000_000
SECRET_PATTERNS = ["sk-", "api_key=", "api_key:", "secret=", "begin rsa",
                   "begin openssh", "password="]


def excluded(rel_path: Path) -> bool:
    parts = {p.lower() for p in rel_path.parts[:-1]}
    if parts & EXCLUDE_PARTS:
        return True
    return rel_path.name.lower() in EXCLUDE_FILES


def contained(path: Path) -> bool:
    try:
        return path.resolve() == ROOT or ROOT in path.resolve().parents
    except OSError:
        return False


def secret_scan(text: str):
    low = text.lower()
    return [p for p in SECRET_PATTERNS if p in low]


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUT_ROOT / f"nacho_business_audit_{stamp}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    manifest, flagged, count = [], [], 0

    candidates = []
    for item in SHIP_DIRS:
        p = (ROOT / item)
        if p.is_dir():
            candidates.extend(q for q in p.rglob("*") if q.is_file())
        elif p.is_file():
            candidates.append(p)
    for item in SHIP_FILES:
        p = ROOT / item
        if p.is_file():
            candidates.append(p)
        else:
            manifest.append(f"MISSING\t{item}")

    for src in candidates:
        if not contained(src):
            continue
        rel = src.relative_to(ROOT)
        if excluded(rel):
            continue
        if src.stat().st_size > BIG:
            manifest.append(f"SKIPPED_LARGE\t{rel.as_posix()}")
            continue
        try:
            text = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        dest = out / rel
        if not contained(dest):
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:16]
        manifest.append(f"SHIPPED\t{rel.as_posix()}\t{src.stat().st_size}\tsha16:{digest}")
        count += 1
        hits = secret_scan(text)
        if hits:
            flagged.append(f"{rel.as_posix()}: {hits}")

    (out / "MANIFEST.txt").write_text(
        "\n".join(manifest) + f"\n\nFILES: {count}\nBUILT: {stamp}\n", encoding="utf-8"
    )
    zpath = out.with_suffix(".zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, _dirs, files in os.walk(out):
            for fn in files:
                full = Path(dirpath) / fn
                z.write(full, full.relative_to(out))
    print(f"bundle: {out}")
    print(f"zip:    {zpath} ({zpath.stat().st_size} bytes, {count} files)")
    if flagged:
        print("FLAGGED FOR REVIEW (secret-shaped strings — verify by hand):")
        for f in flagged:
            print("  " + f)
    else:
        print("secret scan: CLEAN")


if __name__ == "__main__":
    main()
