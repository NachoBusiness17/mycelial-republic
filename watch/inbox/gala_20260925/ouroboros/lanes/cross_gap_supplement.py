# cross-gap supplemental byte-reads (evidence for the ranked register).
# Appends to cross-gap.check.txt. Same laws: ascii only, no em/en dashes.
import json
import os
import re

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
GALA = os.path.join(ROOT, "watch", "inbox", "gala_20260925")

def head(label):
    print("")
    print("=" * 78)
    print(label)
    print("=" * 78)

# S1: resolve CHECK 1's defect class: are accuracy.md's per-dir figures a
# recursive-all-json census while its headline 213 was top-level?
head("SUPPLEMENTAL S1: recursive vs top-level lane-json census per dir")
for d in sorted(os.listdir(GALA)):
    lanes_dir = os.path.join(GALA, d, "lanes")
    if not os.path.isdir(lanes_dir):
        continue
    top = 0
    rec = 0
    for dirpath, dirnames, filenames in os.walk(lanes_dir):
        dirnames[:] = [x for x in dirnames if x not in ("__pycache__", ".mimosa")]
        for fn in filenames:
            if fn.endswith(".json"):
                rec += 1
                if os.path.dirname(os.path.join(dirpath, fn)) == lanes_dir:
                    top += 1
    print("%-24s top-level=%3d recursive=%3d" % (d, top, rec))
print("accuracy.md 09-30 parenthesized: afterparty 197, w3 65, wave5 50, ball 26,")
print("  48h 16, w1 22, w2 26, ball3 8, ball4 24, rung0 4 (sum 438); header total 213.")
print("communication.md CHECK 1b 09-30 (lane JSONs only): afterparty 95, w3 22,")
print("  wave5 12, ball 9, 48h 6, w1 6, w2 10.")

# S2: attribute the mcp_pins growth 397 -> 6229
head("SUPPLEMENTAL S2: state/mcp_pins.jsonl tail attribution")
pins = os.path.join(ROOT, "state", "mcp_pins.jsonl")
lines = [l for l in open(pins, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
print("total records: %d" % len(lines))
print("last 3 records (truncated to 300 chars each):")
for l in lines[-3:]:
    print("  %s" % l[:300])
# per-day histogram from any timestamp-looking field
import collections
day_hist = collections.Counter()
for l in lines:
    m = re.search(r"(2026-\d\d-\d\d)", l)
    if m:
        day_hist[m.group(1)] += 1
print("records per day (top 8): %s" % json.dumps(dict(day_hist.most_common(8)), sort_keys=True))

# S3: accuracy.md's own owed repair: f-25 playbook fixes at HEAD?
head("SUPPLEMENTAL S3: corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:29 (f-25 defect)")
pb = os.path.join(ROOT, "corpus", "steal", "ZCODE_OPERATING_PLAYBOOK_20260925.md")
plines = open(pb, encoding="utf-8", errors="replace").read().splitlines()
print("line 29: %s" % plines[28])
wrong = "core/src/runtime/compact/policy.ts" in plines[28]
print("wrong-path still live at :29: %s" % wrong)
t = "\n".join(plines)
print("law-8 '30KB' citation present (bash.ts): %s" % ("handlers/bash.ts" in t))
print("'30000' or '30,000' bytes figure present: %s" % bool(re.search(r"30,?000", t)))

# S4: was the saved Ractor-50 driver amended with selfsteal's four template fixes?
head("SUPPLEMENTAL S4: .zcode/workflow-drafts/Ractor-50-wave-retro.dwf.ts amendment state")
dr = os.path.join(ROOT, ".zcode", "workflow-drafts", "Ractor-50-wave-retro.dwf.ts")
if os.path.exists(dr):
    st = os.stat(dr)
    import datetime
    print("mtime: %s" % datetime.datetime.utcfromtimestamp(st.st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ"))
    dt = open(dr, encoding="utf-8", errors="replace").read()
    print("contains 'rows may be empty' (D3 defect marker): %s" % ("rows may be empty" in dt))
    print("contains 'division === \"A\"' tier gate (D4 defect marker): %s" % ('division === "A"' in dt))
    print("contains 'Do not fetch' reader cap (D5 defect marker): %s" % ("Do not fetch" in dt))
    print("contains cap-12 slice '12' high-leverage (D2 marker) : %s" % bool(re.search(r"slice\(0?,?\s*12\)", dt)))
    print("contains 'verified N of M' cap-honesty fix (D2 fix): %s" % ("verified N of M" in dt or "N of M" in dt))
else:
    print("draft file MISSING")

# S5: meta-gap 2 check: ractor corpus folded to research_polished / corpus/steal?
head("SUPPLEMENTAL S5: ractor50/vonnegut/lyric fold surfaces")
rp = os.path.join(ROOT, "memory", "research_polished")
hits = []
for fn in os.listdir(rp):
    p = os.path.join(rp, fn)
    if os.path.isfile(p):
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for term in ("ractor50", "vonnegut", "lyric-workover"):
            if term in t:
                hits.append("%s <- %s" % (fn, term))
print("memory/research_polished hits: %s" % (hits if hits else "NONE"))
cs = os.path.join(ROOT, "corpus", "steal")
cshits = []
for fn in os.listdir(cs):
    if os.path.isfile(os.path.join(cs, fn)):
        t = open(os.path.join(cs, fn), encoding="utf-8", errors="replace").read()
        for term in ("ractor50", "vonnegut-final", "lyric-workover"):
            if term in t:
                cshits.append("%s <- %s" % (fn, term))
print("corpus/steal hits: %s" % (cshits if cshits else "NONE"))

# S6: elder inbox content = the salvage lens?
head("SUPPLEMENTAL S6: queue/lanes/elder/inbox.jsonl content")
ei = os.path.join(ROOT, "queue", "lanes", "elder", "inbox.jsonl")
for i, l in enumerate(open(ei, encoding="utf-8", errors="replace").read().splitlines()):
    if l.strip():
        print("row %d: %s" % (i + 1, l[:400]))

# S7: lyric-archaeology.md:216 title count done right (comma-separated list)
head("SUPPLEMENTAL S7: lyric-archaeology.md In-folder tracks list, actual title count")
la = os.path.join(ROOT, "watch", "inbox", "music", "lyric-archaeology.md")
la_lines = open(la, encoding="utf-8", errors="replace").read().splitlines()
start = None
for i, l in enumerate(la_lines):
    if "In-folder tracks" in l:
        start = i
        break
if start is not None:
    blob = []
    for l in la_lines[start:start + 12]:
        blob.append(l)
        if re.search(r"\)\s*$", l) and len(blob) > 1 and "tracks" not in l:
            pass
    text = " ".join(x.strip() for x in la_lines[start:start + 10])
    text = re.sub(r"^.*In-folder tracks \(\d+\):\s*", "", text)
    text = text.split("Ask-named")[0]
    titles = [x for x in text.split(",") if x.strip()]
    print("declared: 20; comma-separated titles found: %d" % len(titles))
    for i, t in enumerate(titles):
        print("  %2d. %s" % (i + 1, t.strip()[:80]))
else:
    print("header line not found")

# S8: vonnegut.checks.json adverse verdicts: regraded anywhere?
head("SUPPLEMENTAL S8: vonnegut.checks.json adverse tier-1 verdicts (1 yes / 4 no)")
vj = os.path.join(GALA, "vonnegut-final", "vonnegut.checks.json")
if os.path.exists(vj):
    j = json.loads(open(vj, encoding="utf-8", errors="replace").read())
    print(json.dumps(j, indent=1)[:2500])
regrade_hits = []
for base in (os.path.join(GALA, "vonnegut-final"), os.path.join(ROOT, "watch", "inbox", "ouroboros")):
    for dirpath, dirnames, filenames in os.walk(base):
        for fn in filenames:
            if "regrade" in fn.lower():
                regrade_hits.append(os.path.join(dirpath, fn))
print("regrade artifacts found: %s" % (regrade_hits if regrade_hits else "NONE"))
print("(GAP_REGISTER Vonnegut wave owed: tier-2 entailment regrade on rows 2-5)")
