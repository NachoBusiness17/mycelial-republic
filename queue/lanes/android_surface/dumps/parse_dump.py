"""Parse uiautomator XML dumps: print full text of nodes matching keywords, or AX bounds of a target text."""
import re, html, sys

path = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "text"
x = open(path, encoding="utf-8").read()

if mode == "bounds":
    # usage: parse_dump.py <xml> bounds <exact-or-substring text>
    target = sys.argv[3]
    for m in re.finditer(r"<node[^>]*>", x):
        n = m.group(0)
        tm = re.search(r'text="([^"]*)"', n)
        if tm and target in tm.group(1):
            b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', n)
            if b:
                cx = (int(b.group(1)) + int(b.group(3))) // 2
                cy = (int(b.group(2)) + int(b.group(4))) // 2
                print(f"{tm.group(1)[:60]!r} center=({cx},{cy}) bounds={b.group(0)}")
else:
    # print full unescaped text of every non-empty text attr containing any keyword arg
    kws = sys.argv[3:] or [""]
    for m in re.finditer(r'<node[^>]*?text="([^"]*)"', x):
        raw = m.group(1)
        t = html.unescape(raw)
        if t.strip() and any(k in t for k in kws):
            print(t)
            print("---NODE-END---")
