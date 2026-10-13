#!/usr/bin/env python3
"""lattice_render.py — render the Law Lattice data from source, never a hand-copied array.

Parses .agents/skills/operator-corrections/SKILL.md numbered laws (1..N) into JSON
(number, short title, one-line summary), then regenerates:

  dashboard/static/lattice_data.json  — plain JSON record
  dashboard/static/lattice_data.js    — window.LATTICE_DATA, consumed verbatim by
                                        dashboard/static/viz_lattice_test.html

The HTML page must load lattice_data.js BEFORE its inline script and read
window.LATTICE_DATA.laws / .primaryEdges / .keywordEdges (see build lane B7 patch).
Edge tables are the measured G2-3 co-citation mining (watch/inbox/mickey/G2_3_cocitation.md);
laws 19-20 postdate that mining, so they render as isolated (dashed-border) nodes —
the page already draws zero-evidence nodes honestly.

Run:  python scripts/lattice_render.py
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".agents" / "skills" / "operator-corrections" / "SKILL.md"
OUT_JSON = ROOT / "dashboard" / "static" / "lattice_data.json"
OUT_JS = ROOT / "dashboard" / "static" / "lattice_data.js"

SMALL_WORDS = {
    "a", "an", "the", "and", "or", "of", "at", "to", "in", "on", "for",
    "with", "by", "not", "is", "are", "as", "its", "it", "vs",
}
# words a truncated label must not end on
TRAILING_STOP = SMALL_WORDS | {
    "during", "from", "into", "onto", "over", "under", "than", "then",
    "that", "this", "before", "after", "without", "between", "against",
}

# ── MEASURED EDGES — G2-3 law co-citation mining (watch/inbox/mickey/G2_3_cocitation.md;
#    raw machine copy _cocitation_raw.json; corpus watch/ + docs/ + memory/improve/,
#    4,415 files, 2026-09-11). Carried verbatim from the pre-B7 inline page arrays. ──
PRIMARY_EDGES = [
    [1, 2, 7], [1, 3, 7], [2, 3, 6], [3, 4, 6],
    [1, 4, 3], [2, 5, 3], [3, 5, 3], [3, 6, 3], [4, 10, 3],
    [1, 5, 2], [1, 10, 2], [1, 12, 2], [2, 4, 2], [2, 12, 2], [3, 7, 2], [3, 8, 2],
    [3, 9, 2], [3, 10, 2], [3, 12, 2],
    [4, 7, 2], [4, 8, 2], [4, 9, 2], [5, 12, 2], [7, 8, 2], [7, 9, 2], [7, 10, 2],
    [7, 13, 2], [8, 9, 2], [8, 10, 2], [9, 10, 2], [13, 15, 2], [13, 16, 2],
    [1, 6, 1], [1, 7, 1], [1, 8, 1], [1, 9, 1], [1, 13, 1], [1, 14, 1], [1, 15, 1], [1, 16, 1],
    [2, 6, 1], [2, 10, 1], [2, 13, 1], [2, 14, 1], [2, 15, 1], [2, 16, 1],
    [4, 13, 1], [4, 14, 1], [4, 15, 1], [4, 16, 1], [5, 6, 1], [6, 12, 1], [7, 12, 1],
    [7, 16, 1], [7, 17, 1],
    [10, 13, 1], [10, 14, 1], [10, 15, 1], [10, 16, 1], [12, 13, 1], [12, 14, 1],
    [12, 16, 1], [12, 17, 1],
    [13, 14, 1], [14, 15, 1], [14, 16, 1], [15, 16, 1],
]
KEYWORD_EDGES = [
    [2, 17, 18], [9, 17, 17], [2, 9, 10], [11, 17, 9], [10, 17, 7],
    [2, 11, 7], [10, 11, 6], [9, 11, 4], [2, 7, 3], [17, 18, 3], [12, 15, 2],
]


def roman(n: int) -> str:
    vals = [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


def parse_laws(text: str):
    """Lenient parse: every line starting '<N>. **' opens a law; the bold run is the
    title (may span lines, e.g. law 15); the body runs to the next law start."""
    starts = list(re.finditer(r"^(\d{1,2})\.\s+\*\*", text, re.M))
    laws = []
    for i, m in enumerate(starts):
        num = int(m.group(1))
        seg_end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        segment = text[m.end():seg_end]
        close = segment.find("**")
        if close == -1:
            title_raw, body = segment.strip(), segment
        else:
            title_raw = segment[:close]
            body = segment[close + 2:]
        laws.append({"number": num, "title_raw": title_raw, "body": body})
    return laws


def clean_title(raw: str) -> str:
    t = re.sub(r"\s+", " ", raw).strip()
    t = re.sub(r"\([^)]*\)", "", t)  # drop (date, context) parentheticals
    t = t.strip().rstrip(":").strip().rstrip(".").strip()
    return t


def display_title(t: str, max_words: int = 8) -> str:
    words = t.split()[:max_words]
    while len(words) > 1 and (words[-1].lower().strip(",.;:\u2014-") in TRAILING_STOP
                              or words[-1].strip(",.;:") == ""):
        words.pop()  # don't end a truncated label on a dangling small word
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        core = lw.strip(",.;:\u2014-")
        out.append(lw if (i > 0 and core in SMALL_WORDS) else lw.capitalize())
    return " ".join(out).rstrip(",;:")


def first_sentence(body: str, maxlen: int = 220) -> str:
    b = re.sub(r"\s+", " ", body).strip()
    b = b.replace("**", "").replace("`", "")
    cut = None
    for m in re.finditer(r"[.!?]", b):
        end = m.end()
        if end < len(b) and b[end] in ')"\u201d':
            end += 1
        rest = b[end:].lstrip()
        if not rest:
            cut = end
            break
        if rest[0].isupper() or rest[0] in '"(\u201c[':
            cut = end
            break
    s = b if cut is None else b[:cut]
    if len(s) > maxlen:
        s = s[:maxlen].rsplit(" ", 1)[0] + " …"
    return s


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    parsed = parse_laws(text)
    if not parsed:
        print("FATAL: no numbered laws parsed from", SKILL)
        return 1

    laws = []
    for p in parsed:
        title = clean_title(p["title_raw"])
        laws.append({
            "number": p["number"],
            "id": p["number"] - 1,  # page convention: node id = law number - 1
            "title": title,         # verbatim parsed title (e.g. "THE INFINITY RULE")
            "label": f"{roman(p['number'])}. {display_title(title)}",
            "group": (p["number"] - 1) // 3,  # page grouping: triads
            "sum": first_sentence(p["body"]),
        })

    numbers = [l["number"] for l in laws]
    expected = list(range(1, max(numbers) + 1))
    if numbers != expected:
        print(f"FATAL: law numbers not contiguous 1..{max(numbers)}: {numbers}")
        return 1

    data = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": ".agents/skills/operator-corrections/SKILL.md",
        "generator": "scripts/lattice_render.py",
        "lawCount": len(laws),
        "laws": laws,
        "primaryEdges": PRIMARY_EDGES,
        "keywordEdges": KEYWORD_EDGES,
    }

    OUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    js = (
        "// AUTO-GENERATED by scripts/lattice_render.py — DO NOT EDIT BY HAND.\n"
        f"// Source: {data['source']} · {len(laws)} laws · generated {data['generated']}\n"
        "// Consumed by viz_lattice_test.html (window.LATTICE_DATA).\n"
        "window.LATTICE_DATA = "
        + json.dumps(data, ensure_ascii=False, separators=(", ", ": "))
        + ";\n"
    )
    OUT_JS.write_text(js, encoding="utf-8")

    print(f"OK: {len(laws)} laws parsed -> {OUT_JSON.name}, {OUT_JS.name}")
    for l in laws:
        print(f"  {l['label']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
