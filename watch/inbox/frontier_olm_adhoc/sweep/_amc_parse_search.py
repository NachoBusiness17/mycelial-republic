import re, html, json, sys, glob, os
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
BASE = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep"
out = []
for path in sorted(glob.glob(BASE + r"\_amc_s*_*.xml")):
    name = os.path.basename(path)
    try:
        tree = ET.parse(path)
    except Exception as e:
        print(f"## {name}: PARSE FAIL {e}", file=sys.stderr)
        continue
    entries = tree.getroot().findall("a:entry", NS)
    print(f"## {name} - {len(entries)} entries")
    for e in entries:
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        link = e.findtext("a:link", "", NS).strip()
        updated = e.findtext("a:updated", "", NS)[:10]
        content = e.findtext("a:content", "", NS)
        text = html.unescape(re.sub(r"<[^>]+>", " ", content or ""))[:180]
        text = re.sub(r"\s+", " ", text).strip()
        print(f"- [{updated}] {title} || {link}")
        out.append({"feed": name, "title": title, "url": link, "date": updated, "blurb": text})
with open(BASE + r"\_amc_search_candidates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(f"\nTOTAL {len(out)}")
