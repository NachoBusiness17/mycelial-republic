import re, html, json, glob, os
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
base = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep"
seen = {}
files = sorted(glob.glob(os.path.join(base, "_kvr2_*.xml")))
for p in files:
    fname = os.path.basename(p)
    if os.path.getsize(p) == 0:
        print(f"== {fname}: EMPTY"); continue
    try:
        tree = ET.parse(p)
    except Exception as e:
        print(f"== {fname}: PARSE FAIL {e}"); continue
    entries = tree.getroot().findall("a:entry", NS)
    print(f"== {fname} ({len(entries)} entries)")
    for e in entries:
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        link_el = e.find("a:link", NS)
        link = (link_el.get("href") if link_el is not None else "") or ""
        updated = e.findtext("a:updated", "", NS)[:10]
        content = e.findtext("a:content", "", NS)
        text = html.unescape(re.sub(r"<[^>]+>", " ", content or ""))[:300]
        text = re.sub(r"\s+", " ", text).strip()
        if link in seen:
            seen[link]["tags"].add(fname); continue
        seen[link] = {"title": title, "url": link, "date": updated, "blurb": text, "tags": {fname}}
out = [{**v, "tags": sorted(v["tags"])} for v in seen.values()]
out.sort(key=lambda x: x.get("date", ""), reverse=True)
with open(os.path.join(base, "_kvr2_candidates.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(f"\nTOTAL UNIQUE {len(out)}")
