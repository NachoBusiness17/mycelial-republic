"""f-16 INDEX truth sweep.

Reads watch/inbox/INDEX.json, and for every item answers three questions:
  1. does the file exist on disk (host root watch/inbox)?
  2. does its sha256 match the INDEX-recorded sha256?
  3. is it registered in watch/inbox/LINKS.jsonl?

LINKS.jsonl is a URL/finding ledger, so "registered" is tested by two joins
and reported separately:
  a. sha join:   item sha256 equals a LINKS row canonical_sha256 (case-insensitive)
  b. text join:  item basename appears anywhere in a LINKS row's string fields

Writes f-16_sweep.json (full per-item results) next to this script and prints
a JSON summary to stdout. Read-only over the inbox: opens files for hashing,
never writes them.
"""
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
ROOT = os.path.join(REPO, "watch", "inbox")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    idx_path = os.path.join(ROOT, "INDEX.json")
    with open(idx_path, encoding="utf-8-sig") as f:
        idx = json.load(f)
    items = idx["items"]

    links_path = os.path.join(ROOT, "LINKS.jsonl")
    with open(links_path, encoding="utf-8-sig") as f:
        links_rows = [json.loads(line) for line in f if line.strip()]

    link_shas = {}
    for i, row in enumerate(links_rows):
        s = (row.get("canonical_sha256") or "").strip().lower()
        if s:
            link_shas.setdefault(s, []).append(i)

    def row_text(row):
        return " ".join(v for v in row.values() if isinstance(v, str)).lower()

    link_texts = [row_text(r) for r in links_rows]

    results = []
    missing = []
    mismatches = []
    size_field_bad = []
    n_exist = n_match = n_sha_link = n_text_link = 0
    n_size_field = 0

    for it in items:
        rel = it["path"].replace("/", os.sep)
        full = os.path.join(ROOT, rel)
        rec = (it.get("sha256") or "").strip().lower()
        exists = os.path.isfile(full)
        actual = None
        size = None
        sha_ok = None
        if exists:
            actual = sha256_file(full)
            size = os.path.getsize(full)
            sha_ok = actual == rec
        base = os.path.basename(it["path"]).strip().lower()
        sha_rows = link_shas.get(rec, [])
        text_rows = (
            [i for i, t in enumerate(link_texts) if base and base in t]
            if base
            else []
        )
        if exists:
            n_exist += 1
            if sha_ok:
                n_match += 1
            else:
                mismatches.append(
                    {
                        "path": it["path"],
                        "class": it.get("class"),
                        "recorded": rec,
                        "actual": actual,
                        "size": size,
                    }
                )
        else:
            missing.append({"path": it["path"], "class": it.get("class")})
        if sha_rows:
            n_sha_link += 1
        if text_rows:
            n_text_link += 1
        if "size" in it:
            n_size_field += 1
            try:
                if int(it["size"]) != size:
                    size_field_bad.append(
                        {"path": it["path"], "recorded": it["size"], "actual": size}
                    )
            except (TypeError, ValueError):
                size_field_bad.append(
                    {"path": it["path"], "recorded": it["size"], "actual": size}
                )
        results.append(
            {
                "path": it["path"],
                "class": it.get("class"),
                "exists": exists,
                "sha_ok": sha_ok,
                "actual_sha256": actual,
                "size": size,
                "links_sha_rows": sha_rows,
                "links_text_rows": text_rows,
            }
        )

    # INDEX derivations cross-check
    deriv = idx.get("derivations", {})
    events_file = deriv.get("source", "")
    events_local = (
        events_file.replace("C:/Users/foste/Documents/projects/local_sovereign_agent/", "")
        if events_file
        else ""
    )
    events_path = os.path.join(REPO, events_local) if events_local else ""
    events_lines = None
    events_exists = os.path.isfile(events_path)
    if events_exists:
        with open(events_path, "rb") as f:
            events_lines = sum(1 for _ in f)

    summary = {
        "index_items": len(items),
        "exists": n_exist,
        "missing": len(missing),
        "sha_match": n_match,
        "sha_mismatch": len(mismatches),
        "links_sha_join": n_sha_link,
        "links_text_join": n_text_link,
        "links_rows": len(links_rows),
        "links_rows_with_canonical_sha256": len(link_shas),
        "size_field_present": n_size_field,
        "size_field_mismatch": len(size_field_bad),
        "derivations": deriv,
        "events_file_exists": events_exists,
        "events_file_lines": events_lines,
        "fold_warnings": len(idx.get("fold_warnings", [])),
        "missing_list": missing,
        "mismatch_list": mismatches,
        "size_field_mismatch_list": size_field_bad,
        "index_sha256": sha256_file(idx_path),
        "links_sha256": sha256_file(links_path),
    }
    out = os.path.join(HERE, "f-16_sweep.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"summary": summary, "items": results}, f, indent=1)
    print(json.dumps({k: v for k, v in summary.items() if not k.endswith("_list")}, indent=1))
    print("MISSING:", json.dumps(missing, indent=1))
    print("MISMATCHES:", json.dumps(mismatches[:60], indent=1))
    if len(mismatches) > 60:
        print("... plus", len(mismatches) - 60, "more mismatches (see f-16_sweep.json)")
    print("SIZE FIELD MISMATCHES:", json.dumps(size_field_bad, indent=1))
    # sample links text-join hits for the audit
    hits = [r["path"] for r in results if r["links_text_rows"]][:40]
    print("TEXT-JOIN HITS (first 40):", json.dumps(hits, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
