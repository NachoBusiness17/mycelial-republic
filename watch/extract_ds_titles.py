import re, os, tempfile

p = os.path.join(tempfile.gettempdir(), "ds_main.js")
txt = open(p, encoding="utf-8", errors="ignore").read()
pat = r'"title":"((?:[^"\\]|\\.){2,300})"'
titles = re.findall(pat, txt)
seen = []
for t in titles:
    try:
        t2 = bytes(t, "utf-8").decode("unicode_escape").encode("latin-1", "ignore").decode("utf-8", "ignore")
    except Exception:
        t2 = t
    t2 = re.sub(r"<[^>]+>", "", t2).strip()
    t2 = t2.replace("\n", " ")
    if t2 and t2 not in seen:
        seen.append(t2)
print(len(seen), "unique titles")
for i, t in enumerate(seen, 1):
    print(i, t)
