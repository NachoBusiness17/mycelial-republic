"""Parse the four top-month Atom feeds pulled this session into a compact listing.

Estate laws honored: local parse, no fetch-model conversion; counts instrument-tagged.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "raw"
NS = {"a": "http://www.w3.org/2005/Atom"}

total = 0
for f in sorted(RAW.glob("rss_*.xml")):
    tree = ET.parse(f)
    entries = tree.getroot().findall("a:entry", NS)
    print(f"== {f.stem} : {len(entries)} entries ==")
    for e in entries:
        title = (e.findtext("a:title", "", NS) or "").strip()
        eid = (e.findtext("a:id", "", NS) or "").strip()
        updated = (e.findtext("a:updated", "", NS) or "").strip()
        # reddit entry ids look like t3_<id>
        short = eid.split("_")[-1] if "_" in eid else eid
        print(f"{short}\t{updated}\t{title[:150]}")
        total += 1
print(f"TOTAL {total}")
