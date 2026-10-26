"""cartographer cycle 11: corpus/apk byte census.

Consumer: receipt_20261020_cartographer.md (FINDINGS/COUNTS rows) and the
cartographer receipt chain (cycle 12 resumes from its banked numbers).
Verifier: re-run this script; every printed number must reproduce from
corpus/apk bytes alone; cross-checks R6_swarm_apk.md claims (1,079 entries,
2 dex, 4 native .so) against the zip central directory.

Recomputes every count from disk. No fabrication: anything not derivable
from the bytes is emitted as UNVERIFIED or omitted.
"""
import json
import os
import re
import struct
import sys
import zipfile
from collections import Counter
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
SHELF = os.path.join(REPO, "corpus", "apk")
APK = os.path.join(SHELF, "aurora_store_76.apk")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apk_census.json")


def shelf_census():
    rows = []
    for root, dirs, files in os.walk(SHELF):
        for f in files:
            p = os.path.join(root, f)
            rows.append((os.path.relpath(p, SHELF), os.path.getsize(p)))
    return rows


def utf16le_strings(blob, min_len=3, max_len=200):
    """Extract printable UTF-16LE strings from a binary blob."""
    out = []
    # walk aligned 2-byte units
    cur = []
    for i in range(0, len(blob) - 1, 2):
        ch = blob[i] | (blob[i + 1] << 8)
        if 0x20 <= ch < 0x7F:
            cur.append(chr(ch))
        else:
            if min_len <= len(cur) <= max_len:
                out.append("".join(cur))
            cur = []
    if min_len <= len(cur) <= max_len:
        out.append("".join(cur))
    return out


def utf8_strings(blob, min_len=3, max_len=200):
    out = []
    cur = []
    for b in blob:
        if 0x20 <= b < 0x7F:
            cur.append(chr(b))
        else:
            if min_len <= len(cur) <= max_len:
                out.append("".join(cur))
            cur = []
    if min_len <= len(cur) <= max_len:
        out.append("".join(cur))
    return out


def manifest_strings(manifest_bytes):
    """Read the AXML string pool without full parsing: harvest UTF-16LE and
    UTF-8 candidate strings, then attribute the package name by pattern.
    Android AXML string pools are UTF-8 or UTF-16; both harvested here."""
    cands = set(utf16le_strings(manifest_bytes)) | set(utf8_strings(manifest_bytes))
    pkg_like = sorted(
        s for s in cands
        if re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]+){1,6}", s or "")
    )
    return {
        "string_pool_candidates": len(cands),
        "package_shaped": pkg_like,
        "has_aurora_store": any("com.aurora.store" == s for s in cands),
        "version_strings": sorted(s for s in cands if re.search(r"(?i)version|aurora", s))[:20],
    }


def main():
    rows = shelf_census()
    total_bytes = sum(n for _, n in rows)
    result = {
        "script": os.path.relpath(__file__, REPO).replace("\\", "/"),
        "moment": datetime.now().astimezone().isoformat(timespec="seconds"),
        "shelf_rows": [{"path": p.replace("\\", "/"), "bytes": n} for p, n in sorted(rows)],
        "shelf_file_count": len(rows),
        "shelf_total_bytes": total_bytes,
    }
    with zipfile.ZipFile(APK) as z:
        infos = z.infolist()
        ext = Counter()
        uncompressed = 0
        libs = []
        dex = []
        meta_inf = []
        top_dirs = Counter()
        for i in infos:
            name = i.filename
            uncompressed += i.file_size
            e = name.rsplit(".", 1)[-1].lower() if "." in name.rsplit("/", 1)[-1] else "(none)"
            ext[e] += 1
            top = name.split("/", 1)[0]
            top_dirs[top] += 1
            if name.startswith("lib/") and name.endswith(".so"):
                libs.append({"name": name, "size": i.file_size})
            if name.endswith(".dex"):
                dex.append({"name": name, "size": i.file_size})
            if name.startswith("META-INF/"):
                meta_inf.append(name)
        result["zip"] = {
            "entry_count": len(infos),
            "uncompressed_total_bytes": uncompressed,
            "compression_ratio": round(uncompressed / max(total_bytes - 218 - 2, 1), 4),
            "extension_census": dict(ext.most_common()),
            "top_level_dirs": dict(top_dirs.most_common()),
            "native_libs": sorted(libs, key=lambda d: d["name"]),
            "abi_sets": sorted({d["name"].split("/")[1] for d in libs}),
            "dex_files": dex,
            "meta_inf_count": len(meta_inf),
            "meta_inf_signing": [n for n in meta_inf if re.search(r"\.(RSA|DSA|EC|SF|MF)$", n)],
            "has_resources_arsc": any(i.filename == "resources.arsc" for i in infos),
        }
        result["r6_report_claims_check"] = {
            "r6_claimed_entries": 1079,
            "central_directory_entries": len(infos),
            "entries_match": len(infos) == 1079,
            "r6_claimed_dex": 2,
            "actual_dex": len(dex),
            "r6_claimed_native_so": 4,
            "actual_native_so": len(libs),
        }
        manifest = z.read("AndroidManifest.xml")
        result["android_manifest"] = {
            "bytes": len(manifest),
            **manifest_strings(manifest),
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    # console summary
    print("shelf rows:", result["shelf_file_count"], "bytes:", result["shelf_total_bytes"])
    print("zip entries:", result["zip"]["entry_count"], "uncompressed:", result["zip"]["uncompressed_total_bytes"])
    print("abis:", result["zip"]["abi_sets"])
    print("r6 check:", json.dumps(result["r6_report_claims_check"]))
    print("manifest:", json.dumps(result["android_manifest"], indent=1)[:1200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
