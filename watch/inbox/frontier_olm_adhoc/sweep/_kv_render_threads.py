import re, html, sys, os
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
BASE = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep"
ids = sys.argv[1:]
for tid in ids:
    p = os.path.join(BASE, f"_kv_thread_{tid}.xml")
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        print(f"##### {tid}: MISSING/EMPTY")
        continue
    try:
        tree = ET.parse(p)
    except Exception as e:
        print(f"##### {tid}: PARSE FAIL {e}")
        continue
    print(f"\n##### THREAD {tid} #####")
    entries = tree.getroot().findall("a:entry", NS)
    for i, e in enumerate(entries):
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        author = e.findtext("a:author/a:name", "anon", NS)
        updated = e.findtext("a:updated", "", NS)[:16]
        content = html.unescape(e.findtext("a:content", "", NS))
        text = re.sub(r"<br\s*/?>", "\n", content)
        text = re.sub(r"</p>|</li>", "\n", text)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"&nbsp;?", " ", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        tag = "POST" if i == 0 else f"COMMENT {i}"
        print(f"\n--- {tag} | {author} | {updated}")
        print(f"TITLE: {title}" if i == 0 else f"RE: {title[:80]}")
        print(text[:4500])
        if len(text) > 4500:
            print(f"[...truncated {len(text)-4500} chars]")
