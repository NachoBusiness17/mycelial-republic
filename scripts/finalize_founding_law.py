"""PD3 finalize — extract Federalist No. 78 + sha256-complete the manifest.

Idempotent: hashes whatever is in memory/corpus/founding_law/, extracts F78 if
missing, and rewrites manifest.json with hashes + the extraction entry.
No network. Pairs with scripts/fetch_founding_law.py.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "memory" / "corpus" / "founding_law"
FED = OUT / "federalist_papers_gutenberg_1404.txt"
F78 = OUT / "federalist_no78_judicial_review.txt"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def extract_f78() -> dict:
    """Cut Federalist No. 78 out of the Gutenberg text (marker -> next No. 79)."""
    text = FED.read_text(encoding="utf-8")
    start = text.index("FEDERALIST No. 78")
    end_match = re.search(r"FEDERALIST No\. 79", text[start:])
    if end_match is None:
        raise SystemExit("F79 marker not found; refusing to guess the cut")
    end = start + end_match.start()
    body = text[start:end].strip() + "\n"
    F78.write_text(body, encoding="utf-8")
    # sanity checks on the extracted essay
    checks = {
        "chars": len(body),
        "judicial_review_phrase": "manifest tenor of the Constitution void" in body,
        "constitution_supreme": "fundamental law" in body.lower(),
        "least_dangerous": "least dangerous" in body.lower(),
    }
    return checks


def main() -> None:
    info = extract_f78()
    print(f"Federalist No. 78 extracted: {info}")

    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # add the extraction entry if absent
    have = {e["id"] for e in manifest["entries"]}
    if "federalist_no78_judicial_review" not in have:
        manifest["entries"].append(
            {
                "id": "federalist_no78_judicial_review",
                "title": "Federalist No. 78 (Hamilton) — judicial review: who interprets the ledger. Extracted from Gutenberg #1404; cut verified against the No. 79 marker.",
                "url": "https://www.gutenberg.org/cache/epub/1404/pg1404.txt#FEDERALIST-No-78",
                "status": "extracted",
                "extraction_checks": info,
                "files": {},
            }
        )

    # refresh extraction checks on the F78 entry (idempotent)
    for entry in manifest["entries"]:
        if entry["id"] == "federalist_no78_judicial_review":
            entry["extraction_checks"] = info

    # hash every file on disk and stitch into entries
    hashes = {
        p.name: sha256(p)
        for p in sorted(OUT.iterdir())
        if p.is_file() and p.name != "manifest.json"
    }
    for entry in manifest["entries"]:
        for slot, val in list(entry.get("files", {}).items()):
            fname = val["name"] if isinstance(val, dict) else val
            if fname in hashes:
                entry["files"][slot] = {"name": fname, "sha256": hashes[fname]}

    # entries that reference files via convention (extracted F78)
    for entry in manifest["entries"]:
        if entry["id"] == "federalist_no78_judicial_review" and F78.name in hashes:
            entry["files"] = {"text": {"name": F78.name, "sha256": hashes[F78.name]}}

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest hashed ({len(hashes)} files) -> {manifest_path}")


if __name__ == "__main__":
    main()
