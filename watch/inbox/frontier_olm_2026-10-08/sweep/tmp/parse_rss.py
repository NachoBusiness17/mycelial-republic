"""Parse the four reddit top-month RSS pulls into (thread_id, date, title) lines.

Scratch instrument for sweep-open-local-models-reddit, 2026-10-08.
Raw payloads: watch/inbox/frontier_olm_2026-10-08/sweep/_raw/rss_<sub>.xml
"""
import glob
import os
import re
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
RAW_DIR = (
    r"C:/Users/foste/Documents/projects/local_sovereign_agent"
    r"/watch/inbox/frontier_olm_2026-10-08/sweep/_raw"
)

for path in sorted(glob.glob(os.path.join(RAW_DIR, "rss_*.xml"))):
    sub = os.path.basename(path)[4:-4]
    try:
        root = ET.parse(path).getroot()
    except Exception as e:  # noqa: BLE001 - scratch instrument, report and continue
        print(f"## {sub}: PARSE ERROR {e}")
        continue
    entries = root.findall("a:entry", NS)
    print(f"## {sub}: {len(entries)} entries")
    for e in entries:
        title = (e.findtext("a:title", "", NS) or "").strip().replace("\n", " ")
        updated = (e.findtext("a:updated", "", NS) or "")[:10]
        link = e.find("a:link", NS)
        href = link.get("href") if link is not None else ""
        m = re.search(r"/comments/([a-z0-9]+)/", href)
        tid = m.group(1) if m else "?"
        print(f"{tid} | {updated} | {title[:110]}")
    print()
