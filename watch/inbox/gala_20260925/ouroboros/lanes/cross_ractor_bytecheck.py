"""cross-ractor lane: byte-check the OLM mine's confirmed finds (both registers).

Evidentiary rule: a confirmed find's quote counts as BYTE-VERIFIED only when it
appears in an INDEPENDENT holding written by the mining run BEFORE the fold
(sweep/ write-ups, sweep/_fx raw fetch caches, steal/ cards, lens/, raw xml).
A quote that appears only in the fold's own outputs (DIGEST.md, register.jsonl,
percolator_candidates.jsonl, RECEIPT.md) is FOLD-ONLY: self-carried, not
verifiable against any pre-fold capture.

Tiers:
T0-exact     : exact byte substring.
T1-wsnorm    : whitespace-collapsed match (byte-true modulo line wraps).
T2-punctnorm : whitespace + smart-punctuation normalized (content-true,
               byte-infidel).
MISS         : no tier matched anywhere scanned (independent AND fold files).

JSON files (.json/.jsonl) are additionally searched through their DECODED
string values, so JSON escaping cannot hide or fake a match.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
D1 = ROOT / "watch/inbox/frontier_olm_2026-09-30"
D2 = ROOT / "watch/inbox/frontier_olm_2026-10-01"

FOLD_NAMES = {"DIGEST.md", "register.jsonl", "percolator_candidates.jsonl", "RECEIPT.md"}
EXTS = {".md", ".json", ".jsonl", ".xml", ".py"}

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)

_PUNCT = {
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2192": "->", "\u00a0": " ",
    "\u2026": "...",
}

def pn(s: str) -> str:
    for k, v in _PUNCT.items():
        s = s.replace(k, v)
    return re.sub(r"\s+", " ", s)

def load_rows(fp: Path):
    rows = []
    for i, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if line:
            rows.append((i, json.loads(line)))
    return rows

def decoded_strings(path: Path):
    """All JSON string values in a .json/.jsonl file (decoded, so escaping
    cannot interfere with matching)."""
    out = []
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return out
    if path.suffix == ".jsonl":
        for line in txt.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                out.extend(_walk_strings(obj))
            except Exception:
                pass
    else:
        try:
            out.extend(_walk_strings(json.loads(txt)))
        except Exception:
            pass
    return out

def _walk_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from _walk_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk_strings(v)

def find_in(text: str, quote: str):
    if quote in text:
        return "T0-exact"
    if norm(quote) in norm(text):
        return "T1-wsnorm"
    if pn(quote) in pn(text):
        return "T2-punctnorm"
    return None

def scan(files, quote):
    """Return list of (relpath, class, tier)."""
    hits = []
    for f, cls in files:
        # raw bytes
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            t = ""
        tier = find_in(t, quote)
        if tier is None and f.suffix in (".json", ".jsonl"):
            tier = find_in(" \n ".join(decoded_strings(f)), quote)
        if tier:
            hits.append((str(f).replace(str(ROOT) + "/", ""), cls, tier))
    return hits

TIER_RANK = {"T0-exact": 0, "T1-wsnorm": 1, "T2-punctnorm": 2}

def collect(folder: Path):
    indep, fold = [], []
    for p in folder.rglob("*"):
        if not p.is_file() or ".mimosa" in p.parts or p.suffix not in EXTS:
            continue
        cls = "FOLD" if p.name in FOLD_NAMES and p.parent == folder else "INDEP"
        (fold if cls == "FOLD" else indep).append((p, cls))
    return indep, fold

def main():
    out = []
    out.append("CROSS-RACTOR BYTE-CHECK of the OLM mine's confirmed finds")
    out.append("instrument: cross_ractor_bytecheck.py (this file), run " +
               datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    out.append("verdict rule: BYTE-VERIFIED = quote found in an INDEPENDENT pre-fold "
               "holding (sweep/, sweep/_fx, steal/, lens/, raw xml).")
    out.append("FOLD-ONLY = found only in the fold's own outputs. MISS = nowhere.")
    out.append("")

    grand = {"BYTE-VERIFIED": 0, "FOLD-ONLY": 0, "MISS": 0}

    for label, folder, regname in (
        ("DAY-1", D1, "register.jsonl"),
        ("DAY-2", D2, "register.jsonl"),
    ):
        indep, fold = collect(folder)
        out.append(f"== {label} register {folder.relative_to(ROOT)}/{regname} ==")
        out.append(f"independent files scanned: {len(indep)} | fold outputs scanned: {len(fold)}")
        rows = load_rows(folder / regname)
        out.append(f"rows parsed: {len(rows)}")
        for i, (lineno, r) in enumerate(rows, 1):
            quote = r.get("quote", "")
            hits = scan(indep, quote)
            if hits:
                best = min(hits, key=lambda h: TIER_RANK[h[2]])
                verdict = "BYTE-VERIFIED"
                where = f"{best[0]} [{best[2]}]"
                if len(hits) > 1:
                    where += f" (+{len(hits)-1} more indep)"
            else:
                fhits = scan(fold, quote)
                if fhits:
                    best = min(fhits, key=lambda h: TIER_RANK[h[2]])
                    verdict = "FOLD-ONLY"
                    where = f"{best[0]} [{best[2]}]"
                else:
                    verdict, where = "MISS", ""
            grand[verdict] += 1
            out.append(f"row {i:2d} (jsonl:{lineno}) [{verdict:12s}] {where} | {r.get('title','')[:55]}")
        out.append("")

    out.append(f"GRAND TOTALS (46 rows): BYTE-VERIFIED={grand['BYTE-VERIFIED']}  "
               f"FOLD-ONLY={grand['FOLD-ONLY']}  MISS={grand['MISS']}")
    print("\n".join(out))

if __name__ == "__main__":
    main()
