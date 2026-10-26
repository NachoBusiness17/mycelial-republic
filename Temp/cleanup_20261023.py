#!/usr/bin/env python3
"""CLEANUP 20261023 - manifest-first file organizer for Downloads + Desktop.
ZERO deletions: every operation is a move, logged to MANIFEST.csv
(ts, origin, dest) so any move is reversible by reading the manifest back.
Classification is by FILENAME/METADATA ONLY - no file contents are opened.
Uncertain ownership goes to neutral buckets, never guessed.
One-shot family-organizer run, not a standing tool."""
import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path

HOME = Path("C:/Users/foste")
DL = HOME / "Downloads"
DESK = HOME / "Desktop"
ROOT = HOME / "CLEANUP_20261023"
MANIFEST = ROOT / "MANIFEST.csv"

BUCKETS = {
    "installers": ROOT / "installers_quarantine",
    "takeout": ROOT / "takeout_dl_export",
    "his_mckenna": ROOT / "his_mark" / "mckenna",
    "his_kungfu": ROOT / "his_mark" / "martial_arts",
    "wife_likely_yoga": ROOT / "wife_likely" / "yoga",
    "photos_unsorted": ROOT / "photos_unsorted",
    "quarantine_ext": ROOT / "quarantine_browser_extension",
    "his_docs": ROOT / "his_mark" / "docs",
    "scratch": DESK / "vault_staging" / "scratch_scripts_20261022",
}

INSTALLER_EXT = {".exe", ".msi", ".msix"}
TAKEOUT_PREFIXES = ("dl-2026", "drive-download-2026")
CAMERA_PREFIXES = ("IMG_", "PXL_", "DSC_", "Screenshot", "VID_", "MVIMG",
                   "WhatsApp", "Snapchat", "saved", "Save")
YOGA_TOKENS = ("kundalini", "yoga", "ana brett", "ravi singh")
KUNGFU_TOKENS = ("yip man", "moy yat", "wing chun", "ving tsun", "martial art",
                 "ip chun", "wooden dummy", "kung fu", "muk yan", "chi kung")
MCKENNA_TOKENS = ("mckenna", "terence")


def classify(name: str) -> str | None:
    low = name.lower()
    p = Path(name)
    ext = p.suffix.lower()
    if any(low.startswith(c.lower()) for c in CAMERA_PREFIXES) and ext in {
            ".jpg", ".jpeg", ".png", ".mp4", ".webp", ".heic", ".mov"}:
        return "photos_unsorted"
    if ext in INSTALLER_EXT:
        return "installers"
    if name.startswith(TAKEOUT_PREFIXES) and ext == ".zip":
        return "takeout"
    if ext == ".iso":
        return "installers"
    if any(t in low for t in MCKENNA_TOKENS):
        return "his_mckenna"
    if any(t in low for t in YOGA_TOKENS):
        return "wife_likely_yoga"
    if any(t in low for t in KUNGFU_TOKENS):
        return "his_kungfu"
    return None


def move(src: Path, bucket: str, rows: list) -> None:
    dest_dir = BUCKETS[bucket]
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    i = 1
    while dest.exists():
        dest = dest_dir / (src.stem + f"_{i}" + src.suffix)
        i += 1
    shutil.move(str(src), str(dest))
    rows.append([datetime.now(timezone.utc).isoformat(), str(src), str(dest)])


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    rows: list = []

    # 1. Downloads sweep
    dl_items = [p for p in DL.iterdir() if p.is_file()]
    moved = 0
    for p in dl_items:
        b = classify(p.name)
        if b:
            move(p, b, rows)
            moved += 1

    # 2. Desktop loose python scratch scripts -> vault_staging scratch
    for p in DESK.glob("*.py"):
        move(p, "scratch", rows)
        moved += 1

    # 3. Desktop "New folder (2)" unpacked browser extension -> quarantine;
    #    the PDF inside goes to his docs
    nf2 = DESK / "New folder (2)"
    if nf2.is_dir():
        for p in list(nf2.rglob("*")):
            if p.is_file() and p.suffix.lower() == ".pdf":
                move(p, "his_docs", rows)
                moved += 1
        leftovers = [p for p in nf2.rglob("*") if p.is_file()]
        if not leftovers:
            shutil.move(str(nf2), str(BUCKETS["quarantine_ext"] / nf2.name))
            rows.append([datetime.now(timezone.utc).isoformat(),
                         str(nf2),
                         str(BUCKETS["quarantine_ext"] / nf2.name)])
            moved += 1
        else:
            print("New folder (2) NOT empty of non-pdf files; left in place")

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts_utc", "origin", "dest"])
        w.writerows(rows)

    print(f"moved {moved} items; manifest: {MANIFEST}")
    by = {}
    for r in rows:
        by[r[2].split("CLEANUP_20261023")[-1].split("\\")[1].split("/")[1]
           if "CLEANUP_20261023" in r[2] else "desktop_vault"] = \
            by.get(r[2].split("CLEANUP_20261023")[-1].split("\\")[1].split("/")[1]
                   if "CLEANUP_20261023" in r[2] else "desktop_vault", 0) + 1
    for k, v in sorted(by.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
