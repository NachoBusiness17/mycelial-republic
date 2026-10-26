#!/usr/bin/env python
# F6 canon manifest builder: walk canon dir, verify magic bytes, compute sha256,
# write manifest.jsonl {url,file,sha256,title,tier} exactly per mission spec.
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET

CANON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "memory", "corpus", "mycology_canon"))
os.chdir(CANON)

# curated metadata for non-self-describing files: file -> (url, title, tier)
CURATED = {
    "adamatzky2018_towards.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC6227805/", "Towards fungal computer", "T1"),
    "boisseau2016_habituation.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC4855389/", "Habituation in an amoeba: memory of the Cafeteria (Proc R Soc B 283:20160446)", "T2"),
    "boussard2019_memory.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC6553583/", "Memory inception and preservation in slime moulds: the quest for a common mechanism", "T2"),
    "kramar2021_alim.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC7958412/", "Morphology of the fungus-like organism Physarum polycephalum as externalized spatial memory", "T2"),
    "kramar2021_reply.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC8040657/", "Reply to 'Missing evidence for memory in the monocellular slime mold' (authors' response)", "T3"),
    "krasowska2021_critique.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC8433532/", "Missing evidence for memory in the monocellular slime mold (PNAS critique)", "T3"),
    "volkov2007_flytrap.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC2634039/", "Closing of Venus flytrap by electrical stimulation of motor cells", "T3"),
    "arxiv_0810_4179.pdf": ("https://arxiv.org/abs/0810.4179", "Memristive model of amoeba's learning", "T3"),
    "arxiv_1303_4969.pdf": ("https://arxiv.org/abs/1303.4969", "Computation of the Travelling Salesman Problem by a Shrinking Blob", "T3"),
    "arxiv_1306_0258.pdf": ("https://arxiv.org/abs/1306.0258", "A slime mould tactile sensor (arXiv 1306.0258)", "T3"),
    "arxiv_1306_3414.pdf": ("https://arxiv.org/abs/1306.3414", "Slime Mould Memristors", "T3"),
    "arxiv_2002_06413.pdf": ("https://arxiv.org/abs/2002.06413", "Mem-fractive properties of mushrooms", "T1"),
    "arxiv_2002_09680.pdf": ("https://arxiv.org/abs/2002.09680", "On Boolean gates in fungal colony", "T2"),
    "arxiv_2304_10675.pdf": ("https://arxiv.org/abs/2304.10675", "Propagation of electrical signals by fungi (Mayne et al., arXiv of BioSystems 233:104933)", "T1"),
    "arxiv_2505_02114.pdf": ("https://arxiv.org/abs/2505.02114", "Physarum/reservoir modeling paper (simulation-only; cited C17)", "T3"),
    "arxiv_2506_12803.pdf": ("https://arxiv.org/abs/2506.12803", "Light-trapped decision-making in Physarum polycephalum (arXiv of PRX Life 4:023026)", "T2"),
    "arxiv_2508_19145.pdf": ("https://arxiv.org/abs/2508.19145", "Unified fading-memory/echo-state view of physical reservoir computing (2025)", "T3"),
    "arxiv_2510_19976.pdf": ("https://arxiv.org/abs/2510.19976", "Morphological computational Capacity of Physarum polycephalum", "T3"),
    "arxiv_2601_08099.pdf": ("https://arxiv.org/abs/2601.08099", "Directional Electrical Spiking, Bursting, and Information Propagation in Oyster Mycelium Recorded with a Star-Shaped Electrode Array", "T1"),
    "schmidt2025_slime_mould_circuit_model.pdf": ("https://www.frontiersin.org/journals/soft-matter/articles/10.3389/frsfm.2025.1588404/pdf", "From simulation to reality: experimental analysis of a quantum entanglement simulation with slime molds (Physarum polycephalum) as bioelectronic components", "T2"),
    "mishra2024_scirobotics_adk8019.pdf": ("https://par.nsf.gov/servlets/purl/10548775", "Sensorimotor control of robots mediated by propulsive fungal hyphae (Science Robotics 9:eadk8019, NSF open PDF)", "T1"),
    "prakash2007_bubble_logic.pdf": ("https://stanford.edu/~manup/docs/Prakash_Science_2007.pdf", "Microfluidic Bubble Logic (Science 315:832-835, author-hosted copy)", "T2"),
    "moratto2023_electrotaxis.pdf": ("https://spiral.imperial.ac.uk/server/api/core/bitstreams/6bb40397-676d-48c5-a102-749ca47b5be0/content", "Enhanced germination and electrotactic behaviour of Phytophthora palmivora zoospores in weak electric fields (Phys Biol 20:056005, open access)", "T2"),
}

# titles for pmc*.xml resolved from the XML itself; pmcid from filename
def xml_title(path):
    try:
        root = ET.parse(path).getroot()
        for p in (".//front//article-title", ".//title-group//article-title"):
            el = root.find(p)
            if el is not None:
                return re.sub(r"\s+", " ", "".join(el.itertext())).strip()
    except Exception:
        return None
    return None

rows = []
for fname in sorted(os.listdir(".")):
    if fname in ("manifest.jsonl", "blocked.jsonl") or fname.startswith("."):
        continue
    data = open(fname, "rb").read()
    head = data[:256].lstrip()
    if fname.endswith(".xml"):
        ok = head.startswith(b"<?xml") or head.startswith(b"<")
        m = re.match(r"pmc(\d+)\.xml", fname)
        if m:
            pmcid = "PMC" + m.group(1)
        else:
            named = {
                "montielrubies2025_navigation.xml": "PMC12109565",
                "moratto2024_fields.xml": "PMC11358279",
                "pieters2022_plant_rc.xml": "PMC9307625",
                "nikolic2023_organoid.xml": "PMC10079015",
            }
            pmcid = named[fname]
        url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
        title = xml_title(fname) or fname
        tier = None  # filled below
        tiers = {
            "PMC13500807": "T1", "PMC12513579": "T1", "PMC11995700": "T1", "PMC12483595": "T1",
            "PMC13212958": "T1", "PMC5959856": "T1", "PMC8984380": "T1", "PMC10069029": "T1",
            "PMC10406843": "T1", "PMC10030783": "T1",
            "PMC10667701": "T2", "PMC11288418": "T2", "PMC2728830": "T2", "PMC12109565": "T2",
            "PMC11358279": "T2", "PMC13481565": "T2",
            "PMC9601536": "T3", "PMC7972235": "T3", "PMC8173894": "T3", "PMC8117569": "T3",
            "PMC9747182": "T3", "PMC10288593": "T3", "PMC9673936": "T3", "PMC10259323": "T3",
            "PMC11097343": "T3", "PMC10079015": "T3", "PMC9307625": "T3",
        }
        tier = tiers.get(pmcid, "T3")
    elif fname.endswith(".pdf"):
        ok = data[:5] == b"%PDF-" or (len(data) > 1024 and b"%PDF-" in data[:1024])
        url, title, tier = CURATED[fname]
    elif fname.endswith(".html"):
        ok = b"<html" in data[:2048].lower() or b"<!doctype" in data[:256].lower()
        url, title, tier = CURATED[fname]
    else:
        ok = False
    if not ok:
        print("BAD MAGIC:", fname, head[:40])
        continue
    rows.append(dict(url=url, file=fname, sha256=hashlib.sha256(data).hexdigest(),
                     title=re.sub(r"\s+", " ", title).strip(), tier=tier))

with open("manifest.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in sorted(rows, key=lambda x: (x["tier"], x["file"])):
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"manifest rows: {len(rows)}")
from collections import Counter
print(Counter(r["tier"] for r in rows))
total = sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f) and f != "manifest.jsonl" and f != "blocked.jsonl")
print(f"total bytes: {total} ({total/1048576:.1f} MiB)")
