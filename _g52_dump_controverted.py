"""_g52_dump_controverted.py — MICKEY G5-2 helper: run mag/invariant_surface.py's
pipeline VERBATIM (copied body of main(), logic unchanged) and dump the FULL
CONTROVERTED list — the sheet surfaces only top-15 of 30. G3-3/G4-2 covered the
first 10; this dumps all rows so G5-2 can fire on 11..30. Writes no sheet.
"""
import hashlib, json, re, sys, time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_g52_controverted_full.json"
OUT_MD = ROOT / "watch" / "INVARIANT_SHEET_V2.md"
MEMORY_DIR = ROOT / "memory"
WATCH_DIR = ROOT / "watch"
CAPS = {"memory": 400, "watch": 200}

VERDICT = re.compile(r"\b(SUPPORTED|DISPUTED|UNPROVEN|CONFIRMED|PRIMARY-READ)\b")
LAW = re.compile(r"\b(law\s?\d+|THE LAW|standing law|never\s+(start|retry|edit|paste|promise)|always\s+)\b", re.I)
FALSIF = re.compile(r"\bfalsif", re.I)
MEASURE = re.compile(r"(\d{1,3}(?:\.\d+)?%|\d+(?:\.\d+)?x\b|corr(eleration)?\s*=?\s*0?\.\d{2,})|(\b\d{2,}[,\d]*\s+(files|leaves|knots|tokens|bytes)\b)", re.I)
NEG_MARK = re.compile(
    r"\b(not|never|isn.t|don.t|doesn.t|won.t|can.t|cannot|wrong|false|"
    r"disputed|refuted|fails?|without|no)\b", re.I)

MIN_LEN, MAX_LEN = 40, 400

STOP = set("""the and for with that this from are was were has have had its their there then than
when what which will would should could into onto under over about after before between through
during also been being both each more most other some such only same just like very can may might
must shall does did doing done dont doesnt isnt wont cant cannot not never no none nor but if
while because until against above below again further once here all any out up down off own too
aint arent couldnt didnt hadnt hasnt havent mightnt mustnt neednt shant shouldnt wasnt werent
wouldnt your you our we they them their theirs she he his her him us me my mine ours yours every
another per via etc eg ie card cards line lines file files folder sheet table section note notes
draft page pages data record records report rows row column corpus corpus domain value values
claim claims state status first second third next last then thus hence also based using used use""".split())


def files_under(base, cap, exclude=()):
    if not base.exists():
        return []
    fs = [p for p in base.rglob("*.md") if p.name not in exclude]
    fs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return fs[:cap]


def bucket_of(line):
    if VERDICT.search(line):
        return "VERDICT"
    if FALSIF.search(line):
        return "FALSIFIER"
    if LAW.search(line):
        return "LAW"
    if MEASURE.search(line):
        return "MEASURED"
    return None


def clean(line):
    s = line.strip().lstrip("-*#> ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())[:160]


def subject_of(s):
    toks = {t for t in re.findall(r"[a-z][a-z0-9/+_-]{3,}", s.lower())
            if t not in STOP and not NEG_MARK.fullmatch(t)}
    return frozenset(toks)


def contradicts(subj_pos, subj_neg):
    shared = len(subj_pos & subj_neg)
    smaller = min(len(subj_pos), len(subj_neg)) or 1
    return shared >= 2 and shared / smaller >= 0.4


def main():
    t0 = time.time()
    corpus = [(p, "memory") for p in files_under(MEMORY_DIR, CAPS["memory"], exclude={"MEMORY.md"})] \
           + [(p, "watch") for p in files_under(WATCH_DIR, CAPS["watch"], exclude={OUT_MD.name})]

    seen = {}
    for p, lane in corpus:
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        mt = p.stat().st_mtime
        for raw in lines:
            s = clean(raw)
            if not (MIN_LEN <= len(s) <= MAX_LEN):
                continue
            b = bucket_of(s)
            if not b:
                continue
            k = hashlib.sha256(norm(s).encode()).hexdigest()[:12]
            rec = seen.get(k)
            if rec is None:
                seen[k] = {"text": s, "bucket": b, "count": 1,
                           "files": [str(p.relative_to(ROOT))], "mtime": mt,
                           "neg": bool(NEG_MARK.search(s)), "subj": subject_of(s)}
            else:
                rec["count"] += 1
                rel = str(p.relative_to(ROOT))
                if rel not in rec["files"]:
                    rec["files"].append(rel)

    recs = list(seen.values())
    pos = [r for r in recs if not r["neg"]]
    neg = [r for r in recs if r["neg"]]

    inv = defaultdict(list)
    by_id = {}
    for n in neg:
        by_id[id(n)] = n
        for t in n["subj"]:
            inv[t].append(n)
    for r in pos:
        hits = defaultdict(int)
        for t in r["subj"]:
            for n in inv.get(t, ()):
                hits[id(n)] += 1
        refs = 0
        for nid, shared in hits.items():
            n = by_id[nid]
            if contradicts(r["subj"], n["subj"]):
                refs += n["count"]
        r["refutations"] = refs
    for n in neg:
        n["refutations"] = 0
    for r in recs:
        r["net"] = r["count"] - r["refutations"]

    controverted = [r for r in recs if r["refutations"] >= 1 and r["count"] >= 2]
    controverted.sort(key=lambda r: (-min(r["count"], r["refutations"] + 1), -r["refutations"]))

    rows = []
    for i, r in enumerate(controverted):
        rows.append({
            "n": i + 1,
            "agree": r["count"],
            "refute": r["refutations"],
            "net": r["net"],
            "bucket": r["bucket"],
            "src": r["files"][0],
            "files": r["files"],
            "text": r["text"][:400],
        })
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "files_walked": len(corpus),
        "unique_lines": len(recs),
        "controverted_total": len(controverted),
        "rows": rows,
    }, indent=1), encoding="utf-8")
    print(f"files={len(corpus)} unique={len(recs)} controverted={len(controverted)} in {time.time()-t0:.1f}s")
    for r in rows:
        print(f'{r["n"]:2d}. [a={r["agree"]} r={r["refute"]}] {r["text"][:100]}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
