import re, html, os, sys
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
base = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep"
ids = ["1wms904", "1wnedrc", "1wlss89", "1wyf63m", "1wl5hfk", "1whf345", "1wromzr", "1wjhk0r"]
for tid in ids:
    p = os.path.join(base, f"_kvr2_thread_{tid}.xml")
    outp = os.path.join(base, f"_kvr2_read_{tid}.txt")
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        print(f"{tid}: MISSING"); continue
    try:
        tree = ET.parse(p)
    except Exception as e:
        print(f"{tid}: PARSE FAIL {e}"); continue
    entries = tree.getroot().findall("a:entry", NS)
    lines = [f"THREAD {tid} ({len(entries)} entries incl OP)"]
    for e in entries:
        author = e.findtext("a:author/a:name", "?", NS)
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        content = e.findtext("a:content", "", NS) or ""
        text = html.unescape(re.sub(r"<br\s*/?>", "\n", content))
        text = re.sub(r"</p>|</li>", "\n", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"[ \t]+", " ", text).strip()
        lines.append(f"\n--- [{author}] {title}\n{text}")
    body = "\n".join(lines)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"{tid}: {len(entries)} entries, {len(body)} chars -> {os.path.basename(outp)}")
