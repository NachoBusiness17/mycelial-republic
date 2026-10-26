#!/usr/bin/env python3
"""measure_hologram.py - empirical size census for the deep-verkle-hologram item.

Asks: how big is the FULL estate (structure + state), what fraction does git
carry, what fraction is untracked state, and what does generic compression
(stand-in for Kolmogorov's K, which is uncomputable) make of it?

No subprocess; pure stdlib. Writes measure_out.json beside itself.
"""
from __future__ import annotations

import json
import lzma
import os
import re
import sys
import time
import zlib
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "flash50"

# ---- buckets -------------------------------------------------------------
DERIVED_TOPS = {".venv", "node_modules", "models", "vendor", ".tmp_dig"}
DERIVED_SUFFIX = (".pyc", ".gguf", ".apk", ".aab")
DERIVED_PARTS = ("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
                 "pytest-", ".gradle")
CACHE_TOPS = {".zcode", ".claude", ".mimosa", ".obsidian", "_archaeology_out"}
REGINDEX = "catalog/catalog_fts.sqlite"

HEX64 = re.compile(rb"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])")
TEXT_SUFFIX = (".md", ".json", ".jsonl", ".txt", ".py", ".yaml", ".yml",
               ".html", ".js", ".toml", ".cfg", ".csv", ".ps1", ".sh")

def bucket_of(rel: str, sz: int) -> str:
    top = rel.split("/")[0]
    low = rel.lower()
    if low == ".git" or low.startswith(".git/"):
        return "git"
    if any(low.startswith(d + "/") or low == d for d in DERIVED_TOPS):
        return "derived"
    if any(p in low for p in DERIVED_PARTS) or low.endswith(DERIVED_SUFFIX):
        return "derived"
    if low == REGINDEX:
        return "derived"
    if any(low.startswith(d + "/") or low == d for d in CACHE_TOPS):
        return "seat_cache"
    if low.startswith("corpus/library/") or low.startswith("corpus/oral_history/"):
        return "derived"   # media corpora, downloadable/vendor class per .gitignore
    return "state"

def main() -> int:
    t0 = time.time()
    tracked = set()
    for tok in (OUT / "lsfiles.zlist").read_bytes().split(b"\0"):
        if tok:
            tracked.add(tok.decode("utf-8", "surrogateescape").replace("\\", "/"))

    per_dir = {}
    buckets = {}
    hex_chars = 0
    hex_hits = 0
    text_scanned = 0
    scanned_files = 0
    all_files = tracked_files = 0
    all_bytes = tracked_bytes = 0
    state_files: list[tuple[int, str]] = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            p = os.path.join(dirpath, name)
            rel = Path(p).relative_to(ROOT).as_posix()
            try:
                st = os.stat(p)
            except OSError:
                continue
            sz = st.st_size
            is_trk = rel in tracked
            top = rel.split("/")[0]
            d = per_dir.setdefault(top, {"bytes": 0, "files": 0,
                                         "tbytes": 0, "tfiles": 0})
            d["bytes"] += sz; d["files"] += 1
            all_files += 1; all_bytes += sz
            if is_trk:
                d["tbytes"] += sz; d["tfiles"] += 1
                tracked_files += 1; tracked_bytes += sz
                b = "tracked"
            else:
                b = bucket_of(rel, sz)
                if b == "state":
                    state_files.append((sz, rel))
            bk = buckets.setdefault(b, {"bytes": 0, "files": 0})
            bk["bytes"] += sz; bk["files"] += 1
            # hex-seal census on modest text files
            if (not is_trk or True) and sz <= 1_000_000 and low_ok(rel):
                if text_scanned < 600_000_000:
                    try:
                        data = Path(p).read_bytes()
                    except OSError:
                        continue
                    text_scanned += sz; scanned_files += 1
                    for m in HEX64.finditer(data):
                        hex_hits += 1
                        hex_chars += len(m.group(0))

    state_files.sort(reverse=True)

    # ---- compression experiments -----------------------------------------
    comp = {}

    # (a) zlib-6 over the untracked "state proper" stream, input-capped
    cap = 2_500_000_000
    co = zlib.compressobj(6)
    cin = cout = 0
    covered = skipped = 0
    state_files_sorted = sorted(state_files)  # small first to cover breadth
    for sz, rel in state_files_sorted:
        if cin >= cap:
            skipped += 1
            continue
        try:
            data = (ROOT / rel).read_bytes()
        except OSError:
            skipped += 1
            continue
        cin += len(data)
        cout += len(co.compress(data))
        covered += 1
    cout += len(co.flush())
    comp["zlib6_state_untracked"] = {
        "in_bytes": cin, "out_bytes": cout, "files_covered": covered,
        "files_skipped_over_cap": skipped,
        "ratio": round(cin / cout, 3) if cout else None}

    # (b) lzma preset 6 over the state-core roots (state/, queue/, logs/, memory/)
    def in_core(rel: str) -> bool:
        top = rel.split("/")[0]
        return top in ("state", "queue", "logs", "memory")
    co2 = lzma.LZMACompressor(preset=6)
    cin2 = cout2 = 0
    for sz, rel in sorted(state_files):
        if cin2 >= 300_000_000:
            break
        if not in_core(rel):
            continue
        try:
            data = (ROOT / rel).read_bytes()
        except OSError:
            continue
        cin2 += len(data)
        cout2 += len(co2.compress(data))
    cout2 += len(co2.flush())
    comp["lzma6_state_core"] = {
        "in_bytes": cin2, "out_bytes": cout2,
        "ratio": round(cin2 / cout2, 3) if cout2 else None}

    # (c) lzma preset 6 over the tracked working tree (the structure layer),
    # input-capped; git pack size is the other bound for history
    co3 = lzma.LZMACompressor(preset=6)
    cin3 = cout3 = 0
    for rel in sorted(tracked):
        if cin3 >= 250_000_000:
            break
        p = ROOT / rel
        if not p.is_file():
            continue
        try:
            data = p.read_bytes()
        except OSError:
            continue
        cin3 += len(data)
        cout3 += len(co3.compress(data))
    cout3 += len(co3.flush())
    comp["lzma6_tracked_sample"] = {
        "in_bytes": cin3, "out_bytes": cout3,
        "ratio": round(cin3 / cout3, 3) if cout3 else None,
        "note": "sample: first ~250MB of tracked tree in path order"}

    out = {
        "tool": "measure_hologram.py",
        "when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_s": round(time.time() - t0, 1),
        "tracked": {"files": tracked_files, "bytes": tracked_bytes},
        "working_tree_excl_git": {"files": all_files, "bytes": all_bytes},
        "per_top_dir": per_dir,
        "buckets": buckets,
        "hex_seal_census": {
            "files_scanned": scanned_files, "text_bytes_scanned": text_scanned,
            "hex64_hits": hex_hits, "hex64_chars": hex_chars,
            "share_of_scanned_bytes": round(hex_chars / text_scanned, 6)
                if text_scanned else None},
        "top20_untracked_state_files": [
            {"bytes": s, "path": r} for s, r in state_files[:20]],
        "compression": comp,
    }
    (OUT / "measure_out.json").write_text(json.dumps(out, indent=1),
                                          encoding="utf-8")
    print(json.dumps(out, indent=1)[:6000])
    return 0

def low_ok(rel: str) -> bool:
    low = rel.lower()
    return low.endswith(TEXT_SUFFIX) or low.endswith(".jsonl")

if __name__ == "__main__":
    sys.exit(main())
