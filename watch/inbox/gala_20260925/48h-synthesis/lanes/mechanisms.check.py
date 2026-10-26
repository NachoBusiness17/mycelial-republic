"""Finish-line byte checks for the mechanisms lane (THE GALA 48h synthesis).

Checks:
 1. Receipt exists at the absolute path.
 2. At least 8 mechanisms in the register.
 3. Every mechanism carries organ + port_move + probe + cost_class (non-empty).
 4. Each of the five mine steal cards covers >= 2 mechanisms.
 5. Every row quote substring-verifies against its cited source file
    (whitespace-collapsed; en-dash/em-dash -> hyphen and U+2019 -> apostrophe
    normalization applied to BOTH sides, disclosed per row in the receipt).
 6. Every cited source file exists on disk (absolute path).
 7. Receipt is ascii-only (no em or en dashes in what the lane wrote).

Exit 0 = all pass. Exit 1 = any failure. Raw output: mechanisms.check.txt
"""
import json
import os
import sys

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
LANE = os.path.join(ROOT, "watch/inbox/gala_20260925/48h-synthesis/lanes")
RECEIPT = os.path.join(ROOT, "watch/inbox/48h_synth/steals.md")
LANEJSON = os.path.join(LANE, "mechanisms.json")

failures = []
passed = []


def check(name, cond, detail=""):
    if cond:
        passed.append(name)
        print(f"PASS {name}" + (f" :: {detail}" if detail else ""))
    else:
        failures.append(name)
        print(f"FAIL {name}" + (f" :: {detail}" if detail else ""))


def normalize(text):
    return (
        text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    )


def squash(text):
    return " ".join(normalize(text).split())


check(
    "receipt exists",
    os.path.isfile(RECEIPT),
    RECEIPT,
)

with open(LANEJSON, encoding="utf-8") as fh:
    lane = json.load(fh)

mechs = lane.get("mechanisms", [])
check("mechanism count >= 8", len(mechs) >= 8, f"count={len(mechs)}")

bad_fields = [
    m["id"]
    for m in mechs
    if not (
        m.get("organ", "").strip()
        and m.get("port_move", "").strip()
        and m.get("probe", "").strip()
        and m.get("cost_class", "").strip()
    )
]
check(
    "every mechanism has organ+port_move+probe+cost_class",
    not bad_fields,
    f"missing on: {bad_fields or 'none'}",
)

five = {
    "S1": ["evals-self-improvement via arxiv"],
    "S2": ["open-and-local-language-models-arxiv"],
    "S3": ["quantization-compression via arxiv"],
    "S4": ["quantization-compression via hn"],
    "S5": ["open-and-local-language-models via x"],
}
for sid, needles in five.items():
    hits = [
        m["id"]
        for m in mechs
        if any(needle in m.get("card", "") for needle in needles)
    ]
    check(f"{sid} covers >= 2 mechanisms", len(hits) >= 2, f"{sid}: {hits}")

quote_results = []
for row in lane.get("rows", []):
    src = row.get("source", "")
    quote = row.get("quote", "")
    tag = row.get("law", "?")
    if not (os.path.isfile(src) and quote):
        quote_results.append(f"{tag}: SOURCE-MISSING-OR-EMPTY-QUOTE")
        continue
    with open(src, encoding="utf-8") as fh:
        body = fh.read()
    ok = squash(quote) in squash(body)
    quote_results.append(f"{tag}: {'BYTE-VERIFIED' if ok else 'MISMATCH'}")

check(
    "all row quotes substring-verify against source bytes",
    all(r.endswith("BYTE-VERIFIED") for r in quote_results),
    "; ".join(quote_results),
)

src_paths = sorted({m["source"] for m in mechs})
missing = []
for entry in src_paths:
    # source field is "path (URL)" or "pathA + pathB" or "path:line (URL)"
    for token in entry.split("+"):
        token = token.strip()
        if token.startswith("http"):
            continue
        path = token
        for cut in (" (", " (http", ": (http"):
            idx = path.find(cut)
            if idx != -1:
                path = path[:idx]
        path = path.strip()
        if ":" in path:
            head, _, tail = path.rpartition(":")
            if tail.strip().isdigit() or tail.strip().split("-")[0].strip().isdigit():
                path = head
        # card-local anchors like " find 2" name a section inside the file
        while " find " in path:
            path = path[: path.rfind(" find ")].strip()
        path = path.strip()
        if not path:
            continue
        if not os.path.isfile(os.path.join(ROOT, path)):
            missing.append(path)
check(
    "all mechanism source paths exist on disk",
    not missing,
    f"missing: {missing or 'none'}",
)

with open(RECEIPT, encoding="utf-8") as fh:
    receipt_text = fh.read()
nonascii = sorted({hex(ord(c)) for c in receipt_text if ord(c) > 127})
check("receipt ascii-only (no em/en dashes)", not nonascii, f"codepoints: {nonascii or 'none'}")

lane_text = open(LANEJSON, encoding="utf-8").read()
lane_nonascii = sorted({hex(ord(c)) for c in lane_text if ord(c) > 127})
check("lane json ascii-only", not lane_nonascii, f"codepoints: {lane_nonascii or 'none'}")

print()
print(f"TOTAL: {len(passed)} passed, {len(failures)} failed")
if failures:
    print("FAILED: " + ", ".join(failures))
sys.exit(1 if failures else 0)
