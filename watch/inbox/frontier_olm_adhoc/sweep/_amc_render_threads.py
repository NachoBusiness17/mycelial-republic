import re, html, sys
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
BASE = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep"
ids = sys.argv[1:]

def clean(c):
    c = c.replace("</p>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    c = re.sub(r"<[^>]+>", " ", c)
    c = html.unescape(c)
    c = re.sub(r"[ \t]+", " ", c)
    return "\n".join(line.strip() for line in c.split("\n")).strip()

for tid in ids:
    path = BASE + rf"\_amc_thread_{tid}.xml"
    try:
        tree = ET.parse(path)
    except Exception as e:
        print(f"===== {tid}: PARSE FAIL {e}")
        continue
    root = tree.getroot()
    feed_title = html.unescape(root.findtext("a:title", "", NS))
    feed_sub = html.unescape(root.findtext("a:subtitle", "", NS))
    entries = root.findall("a:entry", NS)
    lines = [f"THREAD {tid}", f"FEED TITLE: {feed_title}", f"SUBTITLE: {feed_sub[:300]}", f"ENTRIES: {len(entries)}"]
    for e in entries:
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        author = e.findtext("a:author/a:name", "", NS).strip()
        pub = e.findtext("a:published", "", NS)[:16]
        content = clean(e.findtext("a:content", "", NS) or "")
        lines.append(f"\n--- [{pub}] {author} | {title}")
        lines.append(content)
    text = "\n".join(lines)
    with open(BASE + rf"\_amc_read_{tid}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"===== {tid}: {len(entries)} entries, {len(text)} chars, feed title: {feed_title[:90]}")
