# B2-104 probe 3: scope solve. Hypothesis: the Sep-18 tag pass applied the
# Appendix B kind rules ONLY inside the local_sovereign_agent/ prefix and
# bucketed everything else as other. Compare per-kind vs TAG_REPORT v2.
import json
import re

PFX = "local_sovereign_agent/"
CODE = {".py", ".js", ".mjs", ".ts", ".ps1", ".sh", ".cmd", ".bat", ".sql"}
IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico",
         ".tif", ".tiff"}
CONFIG = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".xml",
          ".env", ".properties"}
CORPUS_DIRS = ("memory/corpus/", "memory/research_packs/",
               "memory/archaeology/", "memory/ingest/")
TEXTS = {".md", ".txt", ".rst", ".html", ".htm"}
CARD = re.compile(r"_\d{8}\.md$")


def classify(p, ext):
    """Appendix B first match, applied to the LSA-relative path."""
    base = p.rsplit("/", 1)[-1]
    parent = p.rsplit("/", 2)[-2] if "/" in p else ""
    if p.startswith("watch/") and CARD.search(base):
        return "card"
    if "receipt" in base or "receipt" in parent:
        return "receipt"
    if ext == ".jsonl":
        return "ledger"
    if ext == ".json" and "/state/" in ("/" + p):
        return "state"
    if p.startswith("memory/briefs/") and ext == ".md":
        return "brief"
    if p.startswith(CORPUS_DIRS) and ext in TEXTS:
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
sample_other_sib = []
with open(r"catalog/catalog.jsonl", encoding="utf-8") as fh:
    for line in fh:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        full = str(row.get("path", "")).replace("\\", "/").lower()
        ext = str(row.get("ext", "") or "")
        if full.startswith(PFX):
            rel = full[len(PFX):]
            k = classify(rel, ext)
        else:
            k = "other"
            if len(sample_other_sib) < 5:
                sample_other_sib.append(full)
        counts[k] = counts.get(k, 0) + 1

TARGET = {"other": 585226, "code": 63219, "prose": 52906, "image": 21363,
          "receipt": 10354, "ledger": 10155, "test": 5668, "brief": 3679,
          "config": 3198, "card": 1282, "state": 382, "corpus": 235}
total = 0
for k in sorted(TARGET, key=lambda x: -TARGET[x]):
    got = counts.get(k, 0)
    total += got
    print("%-8s got %7d want %7d %s" % (k, got, TARGET[k],
                                        "OK" if got == TARGET[k] else "DIFF"))
print("total", total, "sample other-sibling:", sample_other_sib[:3])
