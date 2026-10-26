"""B2-76 junction probe: enumerate live reparse points under the catalog root.

Verifies the estate bytes behind the 189K-row junction prune claim
(watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md:23, TAG_REPORT.md:3,
SOCRATIC_GAPS_20260918.md:40). Python 3.11 has no os.path.isjunction
(3.12+), so junctions are detected via lstat st_file_attributes
FILE_ATTRIBUTE_REPARSE_POINT (0x400) + st_reparse_tag. Junction dirs are
pruned from traversal (never descended) and their reparse tag + target
recorded. Run with .venv/Scripts/python.exe.
"""
import json
import os
import stat
import sys
from datetime import datetime, timezone

ROOT = r"C:\Users\foste\Documents\projects"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "B2_76_junction_probe_results.json")

IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003  # junction / mounted folder
IO_REPARSE_TAG_SYMLINK = 0xA0000000
FLAG_REPARSE = 0x400  # FILE_ATTRIBUTE_REPARSE_POINT

TAG_NAMES = {
    0xA0000003: "mount_point",
    0xA0000000: "symlink",
    0xC0000004: "onefile_hl",
    0x80000006: "append",
    0x80000007: "ea",
    0x80000008: "ufi",
    0x80000012: "csv",
    0x8000001A: "iis_cache",
    0x8000001B: "dfs",
    0x8000001E: "dfs_filter",
    0x80000020: "hsm",
    0x80000022: "wim",
    0xA0000019: "appexeclink",
    0x80000023: "cloud",
}


def main():
    found = []
    pruned_dirs = 0
    scanned_dirs = 0
    errors = []
    for dp, dns, fns in os.walk(ROOT, onerror=lambda e: errors.append(str(e))):
        scanned_dirs += 1
        keep = []
        for d in dns:
            full = os.path.join(dp, d)
            try:
                lst = os.lstat(full)
            except OSError as e:
                errors.append(f"{full}: {e}")
                continue
            is_reparse = bool(lst.st_file_attributes & FLAG_REPARSE)
            if is_reparse:
                tag = lst.st_reparse_tag
                try:
                    target = os.readlink(full)
                except OSError as e:
                    target = f"<readlink OSError: {e}>"
                found.append({
                    "path": os.path.relpath(full, ROOT).replace("\\", "/"),
                    "kind": TAG_NAMES.get(tag, f"tag_0x{tag:08X}"),
                    "tag_hex": f"0x{tag:08X}",
                    "is_dir": stat.S_ISDIR(lst.st_mode),
                    "target": target,
                    "target_is_unc": target.startswith("\\\\"),
                })
                pruned_dirs += 1
            else:
                keep.append(d)
        dns[:] = keep

    doc = {
        "probe": "B2_76_junction_probe.py",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": ROOT,
        "python": sys.version.split()[0],
        "scanned_dirs": scanned_dirs,
        "reparse_points_found": len(found),
        "pruned_dir_entries": pruned_dirs,
        "walk_errors": errors[:20],
        "reparse_points": found,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: doc[k] for k in
                      ("ts", "scanned_dirs", "reparse_points_found",
                       "pruned_dir_entries", "walk_errors")}, indent=1))
    for r in found:
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
