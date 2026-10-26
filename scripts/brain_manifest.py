#!/usr/bin/env python3
"""brain_manifest: the curated "brain" set, hashed and secret-screened (2026-10-17).

The brain is what a fresh machine needs to boot this estate's memory:
  - warm pack: memory/biography/verkle_tip.json, memory/warm_state.json,
    memory/zknot/LATEST.md, memory/rib_boot.json
  - library: watch/LIBRARY/INDEX.md, catalog.jsonl, every shelf */LATEST.md
  - chain v2: memory/biography_v2/ top-level *.json/*.jsonl (row log
    chain_v2.jsonl, checkpoints_v2.jsonl, tip_v2.json), seed/*, knots_v2/**
  - chain v1: memory/biography/verkle_chain.jsonl (+ tip above)
  - the latest COMPLETE memory/biography_backup/biography_backup_<date>/
    (completeness rule reused from scripts/backup_chain.py: BACKUP_COMPLETE.json
    present and no BACKUP_INCOMPLETE.json)
  - the verifier: scripts/verify_knot_v2.py (so any copy can check itself)

Every candidate passes TWO screens reused verbatim from
mag/deepseek_direct_runner.py: the path denylist (is_denied) and the
line-redaction scanner (redact_lines). A file that trips either is EXCLUDED
and listed by path only (no reason text, no content).

build() reads each file ONCE: the same bytes are hashed, screened and handed
to an optional sink(sha256, data), so a replica written from the sink can
never disagree with the manifest even while the chain is being appended.

Manifest (schema brain_manifest.v1): files [{path, sha256, size}], excluded
[path...], missing [path...], v2 {root, n, chain_id}, v1 {root, n_leaves},
totals. manifest_sha256 = sha256 of the exact canonical bytes written.

CLI: python scripts/brain_manifest.py [--out FILE]   (read-only unless --out)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCHEMA = "brain_manifest.v1"

WARM_FILES = (
    "memory/biography/verkle_tip.json",
    "memory/warm_state.json",
    "memory/zknot/LATEST.md",
    "memory/rib_boot.json",
)
LIBRARY_FILES = ("watch/LIBRARY/INDEX.md", "watch/LIBRARY/catalog.jsonl")
V1_FILES = ("memory/biography/verkle_chain.jsonl",)
VERIFIER_FILES = ("scripts/verify_knot_v2.py",)
V2_DIR = "memory/biography_v2"
BACKUP_DIR = "memory/biography_backup"


def _latest_complete_backup(root: Path) -> Path | None:
    """Newest biography_backup_<date> that backup_chain.py would call complete."""
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import backup_chain as bc  # reuse: PREFIX, markers, is_complete()
    finally:
        sys.path.pop(0)
    base = root / BACKUP_DIR
    if not base.is_dir():
        return None
    import re

    dirs = sorted(p for p in base.iterdir()
                  if p.is_dir() and re.fullmatch(re.escape(bc.PREFIX) + r"\d{8}", p.name))
    done = [d for d in dirs if bc.is_complete(d)]
    return done[-1] if done else None


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def candidates(root: Path | None = None) -> tuple[list[str], list[str]]:
    """(present repo-relative paths, missing named paths), sorted, de-duplicated."""
    root = Path(root or ROOT)
    found: set[str] = set()
    missing: list[str] = []
    for rel in WARM_FILES + LIBRARY_FILES + V1_FILES + VERIFIER_FILES:
        (found.add(rel) if (root / rel).is_file() else missing.append(rel))
    lib = root / "watch" / "LIBRARY"
    if lib.is_dir():
        for shelf in sorted(lib.iterdir()):
            if shelf.is_dir() and (shelf / "LATEST.md").is_file():
                found.add(_rel(root, shelf / "LATEST.md"))
    v2 = root / V2_DIR
    if v2.is_dir():
        for p in v2.iterdir():
            if p.is_file() and p.suffix in (".json", ".jsonl"):
                found.add(_rel(root, p))
        for sub in ("seed", "knots_v2"):
            if (v2 / sub).is_dir():
                found.update(_rel(root, p) for p in (v2 / sub).rglob("*") if p.is_file())
    else:
        missing.append(V2_DIR + "/")
    bk = _latest_complete_backup(root)
    if bk is not None:
        found.update(_rel(root, p) for p in bk.rglob("*") if p.is_file())
    else:
        missing.append(BACKUP_DIR + "/<latest complete>")
    return sorted(found), missing


def screen(rel: str, data: bytes) -> bool:
    """True when the file may enter the brain (denylist AND redaction scan clean)."""
    from mag.deepseek_direct_runner import is_denied, redact_lines

    if is_denied(rel) is not None:
        return False
    _, counts = redact_lines(data.decode("utf-8", errors="replace").splitlines())
    return not counts


def _json(root: Path, rel: str) -> dict:
    try:
        d = json.loads((root / rel).read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def canonical_bytes(manifest: dict) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")


def build(root: Path | None = None, *, sink: Callable[[str, bytes], None] | None = None,
          paths: Iterable[str] | None = None, created: str | None = None) -> tuple[dict, bytes, str]:
    """Return (manifest, canonical bytes, manifest_sha256)."""
    root = Path(root or ROOT)
    if paths is None:
        rels, missing = candidates(root)
    else:
        rels, missing = sorted(set(paths)), []
    files, excluded = [], []
    total = 0
    for rel in rels:
        try:
            data = (root / rel).read_bytes()
        except OSError:
            missing.append(rel)
            continue
        if not screen(rel, data):
            excluded.append(rel)
            continue
        sha = hashlib.sha256(data).hexdigest()
        files.append({"path": rel, "sha256": sha, "size": len(data)})
        total += len(data)
        if sink is not None:
            sink(sha, data)
    tip2, tip1 = _json(root, V2_DIR + "/tip_v2.json"), _json(root, WARM_FILES[0])
    manifest = {
        "schema": SCHEMA,
        "created": created or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "<repo>",
        "v2": {"root": tip2.get("root"), "n": tip2.get("n"), "chain_id": tip2.get("chain_id")},
        "v1": {"root": tip1.get("root"), "n_leaves": tip1.get("n_leaves")},
        "totals": {"files": len(files), "bytes": total, "excluded": len(excluded),
                   "missing": len(missing)},
        "files": files,
        "excluded": excluded,
        "missing": sorted(missing),
        "screens": "mag/deepseek_direct_runner.py is_denied + redact_lines; "
                   "excluded files are listed by path only",
    }
    raw = canonical_bytes(manifest)
    return manifest, raw, hashlib.sha256(raw).hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="brain_manifest", description=__doc__.splitlines()[0])
    ap.add_argument("--out", help="write the manifest here (otherwise summary only)")
    a = ap.parse_args(argv)
    m, raw, sha = build()
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(raw)
    print(json.dumps({"manifest_sha256": sha, "totals": m["totals"], "v2": m["v2"],
                      "v1": m["v1"], "excluded": m["excluded"], "missing": m["missing"],
                      "out": a.out}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
