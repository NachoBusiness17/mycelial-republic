import glob, html, re, os

RAW = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928\sweep\_raw"

def strip(raw):
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<(h[1-6]|p|div|li|tr|figcaption|section)\b", r"\n<\1", raw, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    return txt.strip()

for path in sorted(glob.glob(RAW + r"\full_*.html")):
    aid = os.path.basename(path).replace("full_", "").replace(".html", "")
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    txt = strip(raw)
    out = RAW + "\\" + "full_" + aid + ".txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(txt)
    heads = re.findall(r"\n(?:\s*)?(\d(?:\.\d)?\s+[A-Z][^\n]{5,90})\n", txt)[:14]
    print(aid, "chars:", len(txt))
    for h in heads:
        print("   ", h.strip())
    print()
