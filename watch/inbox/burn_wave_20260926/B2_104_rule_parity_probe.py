# B2-104: pin the ambiguous salon tag rules against the real map bytes.
# Parity targets from catalog/TAG_REPORT.md (v2, 757,667 rows, Sep-18):
# state=382 corpus=235 card=1282 image=21363 receipt=10354 brief=3679
# ledger=10155 test=5668 code=63219 config=3198 prose=52906 other=585226
import json
import re

CATALOG = r"catalog/catalog.jsonl"
TEXT_EXTS = {".md", ".txt", ".rst", ".html", ".htm"}
CORPUS_DIRS = ("memory/corpus/", "memory/research_packs/",
               "memory/archaeology/", "memory/ingest/")
IMG_BASE = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico",
            ".tif", ".tiff"}

top = seg = corpus_a = corpus_b = card_re = card_str = 0
img_set = img_union = receipt_name = receipt_either = 0
examples = {"corpus_b_only": [], "img_union_extra": []}
with open(CATALOG, encoding="utf-8") as fh:
    for line in fh:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        p = str(row.get("path", "")).replace("\\", "/").lower()
        ext = str(row.get("ext", "") or "")
        base = p.rsplit("/", 1)[-1]
        parent = p.rsplit("/", 2)[-2] if "/" in p else ""
        if ext == ".json" and (p.startswith("state/") or "/state/" in ("/" + p)):
            top += 1
        if ext == ".json" and any(s == "state" for s in p.split("/")[:-1]):
            seg += 1
        if any(p.startswith(d) for d in CORPUS_DIRS) and ext in TEXT_EXTS:
            corpus_a += 1
        elif any(d in p for d in CORPUS_DIRS) and ext in TEXT_EXTS:
            corpus_b += 1
            if len(examples["corpus_b_only"]) < 3:
                examples["corpus_b_only"].append(p)
        if p.startswith("watch/") and re.search(r"_\d{8}\.md$", p):
            card_re += 1
        if p.startswith("watch/") and base.endswith(".md") and any(
                c.isdigit() for c in base):
            card_str += 1
        if ext in IMG_BASE:
            img_set += 1
        else:
            e2 = "." + p.rsplit(".", 1)[-1] if "." in base else ""
            if e2 and e2 in ("*.x",):
                pass
        if "receipt" in base:
            receipt_name += 1
        if "receipt" in base or "receipt" in parent:
            receipt_either += 1

print("state top-level-rule:", top, "(target 382)")
print("state segment-rule:", seg, "(target 382)")
print("corpus startswith:", corpus_a, "contains-extra:", corpus_b,
      "(target 235)", examples["corpus_b_only"])
print("card regex:", card_re, "card loose:", card_str, "(target 1282)")
print("image base-set:", img_set, "(target 21363; .svg/.webp may add)")
print("receipt name:", receipt_name, "name-or-parent:", receipt_either,
      "(target 10354)")
