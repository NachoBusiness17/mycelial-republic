"""cartographer cycle 7: inventory of the manifested public-domain founding texts.

Reads corpus/library/MANIFEST.sha256 (57 entries), verifies each file exists, recomputes
sha256, counts bytes and lines, and emits a bank plus agent-ready group assignments.
Fold basis note: this cycle reads bounded windows, never full texts; the inventory is
the frame the windows hang on.
"""
import hashlib
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MANIFEST = os.path.join(ROOT, "corpus", "library", "MANIFEST.sha256")
OUT = os.path.join(os.path.dirname(__file__), "pd_foundings_inventory.json")


def count_lines(path):
    lines = 0
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            lines += chunk.count(b"\n")
    return lines


def main():
    entries = []
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                entries.append({"parse_error": line[:80]})
                continue
            sha, rest = parts
            fields = rest.split("  ")
            entries.append({
                "sha_manifest": sha,
                "path": fields[0],
                "source": fields[1] if len(fields) > 1 else "",
                "tier": fields[2] if len(fields) > 2 else "",
            })

    rows = []
    ok = mismatch = missing = 0
    for e in entries:
        if "parse_error" in e:
            rows.append(e)
            continue
        full = os.path.join(ROOT, e["path"].replace("/", os.sep))
        if not os.path.isfile(full):
            missing += 1
            rows.append({**e, "exists": False})
            continue
        h = hashlib.sha256()
        size = 0
        with open(full, "rb") as fh:
            while True:
                chunk = fh.read(1 << 20)
                if not chunk:
                    break
                size += len(chunk)
                h.update(chunk)
        digest = h.hexdigest()
        lines = count_lines(full)
        match = digest == e["sha_manifest"]
        if match:
            ok += 1
        else:
            mismatch += 1
        rows.append({**e, "exists": True, "bytes": size, "lines": lines,
                     "sha_recomputed": digest, "sha_match": match,
                     "origin": "gutenberg" if "gutenberg.org" in e["source"] else "archive"})

    by_pod = {}
    for r in rows:
        if "parse_error" in r:
            continue
        pod = r["path"].split("/")[2] if r["path"].count("/") >= 2 else "?"
        by_pod.setdefault(pod, []).append(r)

    bank = {
        "moment": "2026-10-16 cycle 7",
        "manifest_lines_total": len(entries),
        "sha_ok": ok,
        "sha_mismatch": mismatch,
        "missing": missing,
        "total_bytes": sum(r.get("bytes", 0) for r in rows),
        "total_lines": sum(r.get("lines", 0) for r in rows),
        "pods": {p: {"count": len(v),
                     "bytes": sum(x.get("bytes", 0) for x in v),
                     "lines": sum(x.get("lines", 0) for x in v)}
                 for p, v in by_pod.items()},
        "rows": rows,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(bank, fh, indent=1)
    print(json.dumps({k: v for k, v in bank.items() if k != "rows"}, indent=1))
    for p, v in bank["pods"].items():
        print(f"{p}: {v['count']} texts, {v['bytes']} bytes, {v['lines']} lines")


if __name__ == "__main__":
    main()
