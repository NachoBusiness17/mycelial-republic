import re, html, json, glob, os
from xml.etree import ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
seen = {}
labels = {
    "_kv_s1.xml": "LocalLLaMA kv cache", "_kv_s2.xml": "LocalLLaMA prefix caching",
    "_kv_s4.xml": "LocalLLaMA cache hit prompt", "_kv_s6.xml": "LocalLLaMA context compaction agent",
    "_kv_s7.xml": "LocalLLaMA context engineering", "_kv_s8.xml": "LocalLLM kv cache",
    "_kv_s10.xml": "LocalLLaMA tool calls context", "_kv_s12.xml": "LocalLLaMA summarize long context session",
    "_kv_s14.xml": "MachineLearning kv cache", "_kv_s16.xml": "LocalLLaMA session memory agent",
    "_kv_s21.xml": "LocalLLaMA mcp token", "_kv_s22.xml": "ollama context memory",
    "_kv_s23.xml": "MachineLearning kv cache eviction", "_kv_s24.xml": "LocalLLaMA RAG retrieval instead",
}
base = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep"
for fname, label in labels.items():
    p = os.path.join(base, fname)
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        print(f"== {label}: EMPTY/MISSING")
        continue
    try:
        tree = ET.parse(p)
    except Exception as e:
        print(f"== {label}: PARSE FAIL {e}")
        continue
    entries = tree.getroot().findall("a:entry", NS)
    print(f"== {label} ({len(entries)} entries)")
    for e in entries:
        title = html.unescape(e.findtext("a:title", "", NS).strip())
        link_el = e.find("a:link", NS)
        link = (link_el.get("href") if link_el is not None else "") or e.findtext("a:link", "", NS).strip()
        updated = e.findtext("a:updated", "", NS)[:10]
        content = e.findtext("a:content", "", NS)
        text = html.unescape(re.sub(r"<[^>]+>", " ", content or ""))[:260]
        text = re.sub(r"\s+", " ", text).strip()
        if link in seen:
            seen[link]["tags"].add(label)
            continue
        seen[link] = {"title": title, "url": link, "date": updated, "blurb": text, "tags": {label}}
        print(f"- [{updated}] {title}")
        print(f"    {text[:200]}")
        print(f"    {link}")
out = [{**v, "tags": sorted(v["tags"])} for v in seen.values()]
out.sort(key=lambda x: x.get("date", ""), reverse=True)
with open(os.path.join(base, "_kv_search_candidates.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(f"\nTOTAL UNIQUE {len(out)}")
