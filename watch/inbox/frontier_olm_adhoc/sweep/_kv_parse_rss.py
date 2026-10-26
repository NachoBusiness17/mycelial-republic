import re, html, json, sys
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
out = []
for sub in ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]:
    path = rf"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep\_kv_top_{sub}.xml"
    try:
        tree = ET.parse(path)
    except Exception as e:
        print(f"## {sub}: PARSE FAIL {e}", file=sys.stderr)
        continue
    entries = tree.getroot().findall("a:entry", NS)
    print(f"## r/{sub} - {len(entries)} entries")
    for e in entries:
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        link = e.findtext("a:link", "", NS).strip()
        updated = e.findtext("a:updated", "", NS)[:10]
        content = e.findtext("a:content", "", NS)
        text = html.unescape(re.sub(r"<[^>]+>", " ", content or ""))[:220]
        text = re.sub(r"\s+", " ", text).strip()
        print(f"- [{updated}] {title} || {link}")
        print(f"    {text}")
        out.append({"sub": sub, "title": title, "url": link, "date": updated, "blurb": text})
with open(r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep\_kv_candidates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(f"\nTOTAL {len(out)}")
