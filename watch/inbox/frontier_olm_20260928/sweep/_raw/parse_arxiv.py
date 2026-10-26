import glob, re, sys
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
RAW = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928\sweep\_raw"
W0, W1 = "2026-08-29", "2026-09-28"

seen = {}
for path in sorted(glob.glob(RAW + r"\q_*.xml")):
    qname = path.split("\\")[-1].replace(".xml", "")
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print("PARSE-FAIL", qname, e)
        continue
    root = tree.getroot()
    for ent in root.findall("a:entry", NS):
        eid = ent.findtext("a:id", "", NS).strip()
        m = re.search(r"abs/([^v]+)(v\d+)?$", eid)
        aid = m.group(1) if m else eid
        pub = (ent.findtext("a:published", "", NS) or "")[:10]
        title = re.sub(r"\s+", " ", (ent.findtext("a:title", "", NS) or "")).strip()
        summ = re.sub(r"\s+", " ", (ent.findtext("a:summary", "", NS) or "")).strip()
        if aid not in seen:
            seen[aid] = {"id": aid, "pub": pub, "title": title, "summ": summ, "qs": []}
        seen[aid]["qs"].append(qname)

inwin = [e for e in seen.values() if W0 <= e["pub"] <= W1]
outwin = [e for e in seen.values() if e["pub"] and not (W0 <= e["pub"] <= W1)]
inwin.sort(key=lambda e: e["pub"], reverse=True)

print("UNIQUE-ENTRIES", len(seen), "IN-WINDOW", len(inwin), "OUT-OF-WINDOW", len(outwin))
print()
for i, e in enumerate(inwin, 1):
    print(f"{i:02d}|{e['id']}|{e['pub']}|{e['title']}")
print()
print("=== OUT OF WINDOW ===")
for e in outwin[:15]:
    print(f"OO|{e['id']}|{e['pub']}|{e['title'][:80]}")
