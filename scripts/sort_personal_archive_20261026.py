#!/usr/bin/env python3
"""sort_personal_archive_20261026 -- execute DEVICE_DOWNLOADS_PLAN_20261025.csv.

consumer: this window's operator order ("sort them into their appropriate areas
so we can start sorting through the chaff"); verifier: the move ledger
(PersonalArchiveSort20261026/move_ledger.jsonl, one row per move) + the dry-run
count pass which must match the executed counts.

Laws obeyed: zero deletions (remove_candidates and dedupes move to a chaff/
review tree for the operator's weekly triage, never removed); manifest-first
(the CSV + per-device sha256 manifests are the record); moves are same-volume
renames (reversible by ledger replay in reverse).

Device files live in PERSONAL_ARCHIVE_20261025/<Device>/<source-path-minus-
/sdcard/>; PC rows resolve against the live home (they never left). Bob rows
strip C:\\Users\\etfag\\ . Bob+Moto pulls were rc=1 truncated tars: missing
files are counted, never invented.

Usage:
  python sort_personal_archive_20261026.py            # dry run (counts only)
  python sort_personal_archive_20261026.py --execute  # perform moves
"""
from __future__ import annotations
import csv, json, os, sys
from pathlib import Path

HOME = Path(r"C:\Users\foste")
ARCHIVE = HOME / "PERSONAL_ARCHIVE_20261025"
DEST = HOME / "PERSONAL_SORTED_20261026"
PLAN = HOME / "Documents/projects/local_sovereign_agent/watch/inbox/DEVICE_DOWNLOADS_PLAN_20261025.csv"
LEDGER = DEST / "move_ledger.jsonl"

DEVICE_DIR = {"Moto": "Moto", "T90": "T90", "Pixel": "Pixel", "Bob": "Bob"}


def resolve_src(device: str, src: str) -> Path | None:
    src = src.strip().strip('"')
    if device == "PC":
        p = Path(src)
        return p if p.is_absolute() and p.exists() else None
    base = DEVICE_DIR.get(device)
    if not base:
        return None
    rel = src.replace("\\", "/")
    for prefix in ("/sdcard/", "/storage/emulated/0/", "/"):
        if rel.startswith(prefix):
            rel = rel[len(prefix):]
            break
    cand = ARCHIVE / base / rel
    if cand.exists():
        return cand
    # Bob sources are user-dir paths (C:\Users\etfag\Downloads\x -> Bob/Downloads/x)
    if "\\" in src or ":" in src:
        parts = src.replace("\\", "/").split("/")
        if len(parts) >= 3:
            cand2 = ARCHIVE / base / "/".join(parts[3 if parts[1] == "Users" else 2:])
            if cand2.exists():
                return cand2
    return None


def dest_for(action: str, device: str, suggested: str, src: Path) -> Path:
    rel = suggested.strip().strip('"').replace("\\", "/")
    dev = device.lower()
    if action == "move_to_photos":
        parts = rel.split("/")
        if len(parts) > 1 and parts[1] != dev:
            rel = f"photos/{dev}/" + "/".join(parts[1:])
        return DEST / rel
    if action == "move_to_memes":
        parts = rel.split("/")
        if len(parts) > 1 and parts[1] != dev:
            rel = f"memes/{dev}/" + "/".join(parts[1:])
        return DEST / rel
    if action == "uncertain_image":
        return DEST / "uncertain" / dev / Path(rel).name
    if action == "personal_archive":
        return DEST / "personal_archive" / dev / Path(rel).name
    if action in ("remove_candidate", "dedupe"):
        keep = src.relative_to(ARCHIVE) if str(src).startswith(str(ARCHIVE)) else Path(dev) / src.name
        return DEST / ("chaff" if action == "remove_candidate" else "chaff/dedupe") / keep
    return DEST / "unrouted" / dev / Path(rel).name


def unique_dst(dst: Path) -> Path:
    if not dst.exists():
        return dst
    stem, suf = dst.stem, dst.suffix
    for i in range(2, 1000):
        cand = dst.with_name(f"{stem}_{i}{suf}")
        if not cand.exists():
            return cand
    raise RuntimeError(f"no unique name for {dst}")


def main() -> int:
    execute = "--execute" in sys.argv
    counts: dict[str, dict[str, int]] = {}
    if execute:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
    ledger = open(LEDGER, "a", encoding="utf-8") if execute else None
    with open(PLAN, newline="", encoding="utf-8", errors="replace") as f:
        rows = csv.DictReader(f)
        for row in rows:
            action = (row.get("action") or "").strip()
            if action not in ("move_to_photos", "move_to_memes", "uncertain_image",
                              "personal_archive", "keep", "remove_candidate",
                              "dedupe", "SKIP_GT2GB"):
                counts.setdefault("malformed_rows", {"n": 0})["n"] += 1
                continue
            device = (row.get("source_device") or "").strip()
            src = resolve_src(device, row.get("source path") or "")
            bucket = counts.setdefault(action, {"found": 0, "missing": 0, "moved": 0, "bytes": 0})
            if action in ("keep", "SKIP_GT2GB"):
                bucket["found"] += 1  # stays put by design
                continue
            if src is None:
                # idempotent re-run: a prior crashed pass may have moved this
                # row before its ledger line; if the destination exists, count
                # it already-moved and complete the ledger.
                probe = dest_for(action, device, row.get("suggested new name") or "",
                                 ARCHIVE / DEVICE_DIR.get(device, device) / "x")
                probe2 = dest_for(action, device, row.get("suggested new name") or "",
                                  ARCHIVE / DEVICE_DIR.get(device, device) / (row.get("source path") or "x").replace("\\", "/").split("/")[-1])
                found_dst = probe if probe.exists() else (probe2 if probe2.exists() else None)
                if found_dst is not None:
                    bucket.setdefault("already_moved", 0)
                    bucket["already_moved"] += 1
                    if ledger:
                        ledger.write(json.dumps({"action": action, "device": device,
                                                 "src": row.get("source path"),
                                                 "dst": str(found_dst),
                                                 "note": "preflight-pass"}) + "\n")
                else:
                    bucket["missing"] += 1
                continue
            bucket["found"] += 1
            dst = dest_for(action, device, row.get("suggested new name") or "", src)
            if execute:
                dst.parent.mkdir(parents=True, exist_ok=True)
                final = unique_dst(dst)
                os.replace(src, final)
                bucket["moved"] += 1
                bucket["bytes"] += final.stat().st_size
                if ledger:
                    ledger.write(json.dumps({"action": action, "device": device,
                                             "src": str(src), "dst": str(final)}) + "\n")
    if ledger:
        ledger.close()
    for action in sorted(counts):
        print(action, json.dumps(counts[action], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
