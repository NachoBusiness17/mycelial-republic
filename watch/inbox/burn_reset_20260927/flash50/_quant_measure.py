#!/usr/bin/env python3
"""Measurement instrument for deep-quantizer-theory (flash50).

Reads the live quantizer outputs + source stream, measures the actual
distortion of the frontier->flash->local tier chain with the tool's own
regex classes. Prints one JSON blob. No fabrication: every number below
is computed from bytes on disk this run.
"""
from __future__ import annotations
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import thought_quantizer as tq  # noqa: E402  (reuse the shipped regexes verbatim)

QT = ROOT / "memory" / "corpus" / "quantized_thought"
out: dict = {}

# ---- A. packs + sizes ----
packs = {}
for tier in ("frontier", "flash", "local"):
    p = QT / f"instructions_{tier}.jsonl"
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    packs[tier] = rows
    out[f"pack_{tier}"] = {"rows": len(rows), "bytes": p.stat().st_size}
rep = json.loads((QT / "compile_report.json").read_text(encoding="utf-8"))
out["compile_report_stats"] = rep["stats"]
src_bytes = (ROOT / "memory" / "percolator" / "invariants.json").stat().st_size
src = json.loads((ROOT / "memory" / "percolator" / "invariants.json").read_text(encoding="utf-8"))
inv = src.get("invariants", src)
out["source_now"] = {"rows": len(inv), "bytes": src_bytes}

# ---- B. char-mass retention + decomposition (truncation vs selection loss) ----
frontier_field = [r["frontier"] for r in packs["frontier"]]
f24 = sum(len(t) for t in frontier_field)
flash_rows = packs["flash"][:12]
local_by_id = {r["id"]: r["local"] for r in packs["local"]}
l24 = sum(len(packs["flash"][i]["frontier"]) for i in range(len(flash_rows)))  # frontier text of the same 12 rows
f12 = sum(len(r["flash"]) for r in flash_rows)
loc = sum(len(local_by_id[r["id"]]) for r in flash_rows if r["id"] in local_by_id)
sel_loss = sum(len(t) for t in frontier_field[12:])  # rows 13..24 absent from flash/local packs
out["char_mass"] = {
    "frontier_24_chars": f24,
    "frontier_first12_chars": l24,
    "flash_12_chars": f12,
    "local_12_chars": loc,
    "flash_truncation_retention_vs_same12": round(f12 / l24, 4) if l24 else None,
    "local_truncation_retention_vs_flash": round(loc / f12, 4) if f12 else None,
    "flash_selection_loss_chars_rows13_24": sel_loss,
    "flash_total_retention_vs_frontier24": round(f12 / f24, 4) if f24 else None,
    "local_total_retention_vs_frontier24": round(loc / f24, 4) if f24 else None,
}

# ---- C. nesting / prefix property (successive refinement check) ----
reflash_ok = sum(1 for r in flash_rows if r["flash"] == tq.to_flash(r["frontier"]))
loc_prefix = sum(1 for r in flash_rows
                 if r["id"] in local_by_id and r["flash"].startswith(local_by_id[r["id"]]))
loc_prefix_ws = sum(1 for r in flash_rows
                    if r["id"] in local_by_id
                    and " ".join(r["flash"].split()).startswith(" ".join(local_by_id[r["id"]].split())))
sent_clip = 0
for r in flash_rows:
    t = tq.to_flash(r["frontier"])
    if len(t) >= 220:
        sent_clip += 1
overload_src = 0
for key, row in inv.items():
    t = str(row.get("text", "")).strip()
    first = t if t else ""
    import re as _re
    m = _re.split(r"(?<=[.!?])\s", t)
    if m and len(m[0]) > 220:
        overload_src += 1
out["nesting"] = {
    "flash_equals_to_flash_of_frontier": f"{reflash_ok}/{len(flash_rows)}",
    "local_byte_prefix_of_flash": f"{loc_prefix}/{len(flash_rows)}",
    "local_ws_normalized_prefix_of_flash": f"{loc_prefix_ws}/{len(flash_rows)}",
    "flash_rows_at_220_clip": sent_clip,
    "source_rows_whose_first_sentence_exceeds_220": overload_src,
}

# ---- D. behavioral-loss probes (verb survival down the tiers) ----
def verbs(s): return set(tq.IMPERATIVE_RE.findall(s or ""))
verb_frontier = sum(1 for r in flash_rows if verbs(r["frontier"]))
verb_flash = sum(1 for r in flash_rows if verbs(r["flash"]))
verb_local = sum(1 for r in flash_rows
                 if r["id"] in local_by_id and verbs(local_by_id[r["id"]]))
# laws where the verb survives frontier but dies in flash, or flash but not local
die_flash = [r["id"] for r in flash_rows if verbs(r["frontier"]) and not verbs(r["flash"])]
die_local = [r["id"] for r in flash_rows if r["id"] in local_by_id
             and verbs(r["flash"]) and not verbs(local_by_id[r["id"]])]
# upstream pre-truncation census: source texts not ending in sentence-final punct
import re as re2
noend = sum(1 for _, row in inv.items()
            if str(row.get("text", "")).strip()
            and not re2.search(r"[.!?\)\]\"]\s*$", str(row.get("text", "")).strip()))
srclens = sorted(len(str(row.get("text", ""))) for row in inv.values())
out["verb_survival_flashpack"] = {
    "frontier_rows_with_verb": f"{verb_frontier}/{len(flash_rows)}",
    "flash_rows_with_verb": f"{verb_flash}/{len(flash_rows)}",
    "local_rows_with_verb": f"{verb_local}/{len(flash_rows)}",
    "ids_verb_dies_at_flash": die_flash,
    "ids_verb_dies_at_local": die_local,
    "source_texts_missing_terminal_punct": f"{noend}/{len(inv)}",
    "source_text_len_min_median_max": [srclens[0], srclens[len(srclens)//2], srclens[-1]],
}

# ---- E. deadband + dedupe collision census on the live source ----
merged: dict[str, set] = {}
kept = 0
for key, row in inv.items():
    text = str(row.get("text", "")).strip()
    if not text:
        continue
    verdict, _shape = tq.classify(text)
    if verdict != "keep":
        continue
    kept += 1
    merged.setdefault(tq.signature(text), set()).add(" ".join(text.split()).lower())
false_merges = {s: len(v) for s, v in merged.items() if len(v) > 1}
out["deadband_dedupe"] = {
    "kept_now": kept,
    "distinct_signatures": len(merged),
    "signatures_merging_distinct_texts": len(false_merges),
    "max_fanin_distinct_texts_one_signature": max(false_merges.values()) if false_merges else 1,
}

# ---- F. entropy estimates over the frontier pack corpus ----
corpus = " ".join(frontier_field)
counts = Counter(corpus.lower())
n = sum(counts.values())
h0 = -sum((c / n) * math.log2(c / n) for c in counts.values())
words = [w for w in re2.findall(r"[a-z0-9']+", corpus.lower()) if w]
wc = Counter(words)
nw = sum(wc.values())
hw1 = -sum((c / nw) * math.log2(c / nw) for c in wc.values())
top10 = wc.most_common(10)
out["entropy"] = {
    "frontier_chars": n,
    "h0_char_bits": round(h0, 3),
    "frontier_words": nw,
    "word_unigram_bits_per_word": round(hw1, 3),
    "top10_words_share_pct": round(100 * sum(c for _, c in top10) / nw, 1),
    "top10_words": [w for w, _ in top10],
}

# ---- G. behavioral class census (verb, polarity) ----
def bclass(text):
    v = sorted(verbs(text))
    pol = "neg" if re2.search(r"(?i)\bnever|don'?t|do not\b", text) else (
        "univ" if re2.search(r"(?i)\balways\b", text) else "pos")
    return (v[0] if v else None, pol)
cls24 = Counter(bclass(t) for t in frontier_field)
kept_texts = []
for key, row in inv.items():
    text = str(row.get("text", "")).strip()
    if text and tq.classify(text)[0] == "keep":
        kept_texts.append(text)
cls307 = Counter(bclass(t) for t in kept_texts)
out["behavioral_classes"] = {
    "distinct_classes_frontier24": len(cls24),
    "log2_classes_frontier24_bits": round(math.log2(len(cls24)), 3),
    "distinct_classes_kept307": len(cls307),
    "log2_classes_kept307_bits": round(math.log2(len(cls307)), 3),
    "class_hist_frontier24": {f"{k[0]}/{k[1]}": v for k, v in cls24.most_common()},
}

# ---- H. rates table ----
out["rate_table"] = {
    "bits_per_row_ascii8": {
        "frontier": round(8 * f24 / 24, 1),
        "flash": round(8 * f12 / 12, 1),
        "local": round(8 * loc / 12, 1),
    },
    "frontier_vs_flash_bytes_per_row_ratio": round((f24 / 24) / (f12 / 12), 3) if f12 else None,
    "frontier_vs_local_bytes_per_row_ratio": round((f24 / 24) / (loc / 12), 3) if loc else None,
    "source_vs_frontier_pack_bytes": round(src_bytes / (QT / "instructions_frontier.jsonl").stat().st_size, 2),
}

print(json.dumps(out, indent=1, ensure_ascii=False))
