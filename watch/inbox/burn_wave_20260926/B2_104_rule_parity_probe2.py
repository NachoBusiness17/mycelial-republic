# B2-104 probe 2: first-match kind rules over the real map vs TAG_REPORT v2.
# Targets: other 585226 code 63219 prose 52906 image 21363 receipt 10354
#          ledger 10155 test 5668 brief 3679 config 3198 card 1282
#          state 382 corpus 235  (sum 757667)
import json
import re

PFX = "local_sovereign_agent/"
CODE = {".py", ".js", ".mjs", ".ts", ".ps1", ".sh", ".cmd", ".bat", ".sql"}
IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico",
         ".tif", ".tiff"}
CONFIG = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".xml",
          ".env", ".properties"}
CORPUS_SUFFIX = ("memory/corpus/", "memory/research_packs/",
                 "memory/archaeology/", "memory/ingest/")
TEXTS = {".md", ".txt", ".rst", ".html", ".htm"}
CARD = re.compile(r"_\d{8}\.md$")

variants = {"card_a_contains": 0, "card_b_prefixed": 0, "card_c_watch_in": 0,
            "corpus_a_prefixed": 0, "corpus_c_lsa_only_contains": 0}


def classify_first_match(p, ext, card_mode, corpus_mode):
    base = p.rsplit("/", 1)[-1]
    parent = p.rsplit("/", 2)[-2] if "/" in p else ""
    if card_mode == "a":
        is_card = "/watch/" in ("/" + p) and CARD.search(base)
    elif card_mode == "b":
        is_card = p.startswith(PFX + "watch/") and CARD.search(base)
    else:
        is_card = "watch/" in p and CARD.search(base)
    if is_card:
        return "card"
    if "receipt" in base or "receipt" in parent:
        return "receipt"
    if ext == ".jsonl":
        return "ledger"
    if ext == ".json" and "/state/" in ("/" + p):
        return "state"
    if corpus_mode == "a":
        is_corpus = p.startswith(PFX) and p[len(PFX):].startswith(CORPUS_SUFFIX)
    else:
        is_corpus = (p.startswith(PFX) and any(
            d in p for d in CORPUS_SUFFIX) and ext in TEXTS)
    if is_corpus and ext in TEXTS:
        return "corpus"
    if base.startswith("test_"):
        return "test"
    if ext in CODE:
        return "code"
    if ext in IMAGE:
        return "image"
    if ext in CONFIG:
        return "config"
    if ext == ".md":
        return "prose"
    return "other"


counts = {}
with open(r"catalog/catalog.jsonl", encoding="utf-8") as fh:
    for line in fh:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        p = str(row.get("path", "")).replace("\\", "/").lower()
        ext = str(row.get("ext", "") or "")
        for cm in ("a", "b", "c"):
            k = classify_first_match(p, ext, cm, "a")
            variants["card_%s_%s" % (
                {"a": "contains", "b": "prefixed", "c": "watch_in"}[cm],
                "x")] = 0
        # count each card variant on its own
        base = p.rsplit("/", 1)[-1]
        if "/watch/" in ("/" + p) and CARD.search(base):
            variants["card_a_contains"] += 1
        if p.startswith(PFX + "watch/") and CARD.search(base):
            variants["card_b_prefixed"] += 1
        if "watch/" in p and CARD.search(base):
            variants["card_c_watch_in"] += 1
        for km in ("a", "c"):
            k = classify_first_match(p, ext, "b", km)
            key = "kind_card_b_corpus_%s" % km
            counts.setdefault(key, {})
            counts[key][k] = counts[key].get(k, 0) + 1

TARGET = {"other": 585226, "code": 63219, "prose": 52906, "image": 21363,
          "receipt": 10354, "ledger": 10155, "test": 5668, "brief": 3679,
          "config": 3198, "card": 1282, "state": 382, "corpus": 235}
print("card variants (target 1282):", {k: v for k, v in variants.items()})
for key in sorted(counts):
    c = counts[key]
    diffs = {k: (c.get(k, 0), TARGET[k]) for k in TARGET
             if c.get(k, 0) != TARGET[k]}
    print(key, "MATCHES ALL" if not diffs else "diffs: %s" % diffs)
