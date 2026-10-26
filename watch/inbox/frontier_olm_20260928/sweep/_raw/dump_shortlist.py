import re
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
RAW = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928\sweep\_raw"

DEEP = ["2609.07370", "2609.23742", "2609.25373", "2609.32042",
        "2609.33467", "2608.30005", "2609.21341", "2609.05881"]
OTHERS = ["2609.28003", "2609.33141", "2609.27669", "2609.24985",
          "2609.30258", "2609.10962", "2609.23959", "2609.26550",
          "2609.33955", "2609.29333", "2609.33812", "2609.32021",
          "2609.33917", "2609.32638", "2609.13559", "2609.13470",
          "2609.05736", "2609.07280", "2609.09476", "2609.05395"]
WANT = set(DEEP + OTHERS)

entries = {}
for q in ["q_a_toolcall", "q_b_small", "q_c_json", "q_d_openweight",
          "q_e_verify", "q_f_bfcl", "q_g_quant", "q_h_smallslm"]:
    try:
        tree = ET.parse(RAW + "\\" + q + ".xml")
    except ET.ParseError:
        continue
    for ent in tree.getroot().findall("a:entry", NS):
        eid = ent.findtext("a:id", "", NS).strip()
        m = re.search(r"abs/([^v]+)(v\d+)?$", eid)
        if not m:
            continue
        aid = m.group(1)
        if aid not in WANT or aid in entries:
            continue
        entries[aid] = {
            "id": aid,
            "pub": (ent.findtext("a:published", "", NS) or "")[:10],
            "title": re.sub(r"\s+", " ", ent.findtext("a:title", "", NS) or "").strip(),
            "summ": re.sub(r"\s+", " ", ent.findtext("a:summary", "", NS) or "").strip(),
        }

missing = WANT - set(entries)
print("FOUND", len(entries), "MISSING", sorted(missing))
print()
for aid in DEEP:
    e = entries.get(aid)
    if e:
        print(f"[DEEP] {e['id']} | {e['pub']} | {e['title']}")
        print(f"  ABS: {e['summ']}")
        print()
for aid in OTHERS:
    e = entries.get(aid)
    if e:
        print(f"[PASS1] {e['id']} | {e['pub']} | {e['title']}")
        print(f"  ABS: {e['summ'][:400]}")
        print()
