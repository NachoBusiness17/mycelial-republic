#!/usr/bin/env python
# F6 mycology canon fetcher — free fetches only (Europe PMC fullTextXML, NCBI E-utilities,
# arXiv PDF, verified open publisher PDFs). No git, no paid APIs.
# Run with repo venv: .\.venv\Scripts\python.exe watch\inbox\physical_computing\receipts\f6_fetch.py
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

CANON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "memory", "corpus", "mycology_canon"))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) F6-canon-lane/1.0 (contact: fleet receipt F6)"}
LOG = []

# kind: pmc (Europe PMC fullTextXML + eutils fallback) | arxiv (pdf) | direct (url)
# tier: T1 core measurement/protocol canon · T2 substrate+mechanism canon · T3 adjacent/context/critique
JOBS = [
    # ---- PRIORITY: mission-named ----
    dict(key="adamatzky2026_star",   kind="arxiv", id="2601.08099", tier="T1",
         title="Directional Electrical Spiking, Bursting, and Information Propagation in Oyster Mycelium Recorded with a Star-Shaped Electrode Array"),
    dict(key="adamatzky2026_linear", kind="pmc", id="PMC13212958", tier="T1",
         title="Propagation of electrical spike trains in substrates colonised by oyster fungi"),
    dict(key="telhan2026_chips",     kind="pmc", id="PMC13500807", tier="T1",
         title="Morphologically tunable mycelium chips for physical reservoir computing"),
    dict(key="larocco2025_memristor",kind="pmc", id="PMC12513579", tier="T1",
         title="Sustainable memristors from shiitake mycelium for high-frequency bioelectronics"),
    dict(key="buffi2025_fems",       kind="pmc", id="PMC11995700", tier="T1",
         title="Electrical signaling in fungi: past and present challenges"),
    dict(key="buffi2025_fpc",        kind="pmc", id="PMC12483595", tier="T1",
         title="Detection of electrical signals in fungal mycelia in response to external stimuli"),
    dict(key="kramar2021_alim",      kind="pmc", id="PMC7958412", tier="T2",
         title="Morphology of the fungus-like organism Physarum polycephalum as externalized spatial memory"),
    dict(key="yoneoka2023_habituation", kind="pmc", id="PMC10667701", tier="T2",
         title="Habituation in Physarum polycephalum from network morphology (Front Cell Dev Biol 11:1249165)"),
    dict(key="beasley2022_memfractive", kind="arxiv", id="2002.06413", tier="T1",
         title="Mem-fractive properties of mushrooms"),
    dict(key="schmidt2025_frontsoft", kind="direct", tier="T2",
         url="https://www.frontiersin.org/journals/soft-matter/articles/10.3389/frsfm.2025.1588404/pdf",
         file="schmidt2025_slime_mould_circuit_model.pdf",
         title="Frontiers in Soft Matter 5:1588404 (slime mould circuit model / alleged bio-memristor line)"),
    dict(key="mishra2024_robot",     kind="direct", tier="T1",
         url="https://par.nsf.gov/servlets/purl/10548775",
         file="mishra2024_scirobotics_adk8019.pdf",
         title="Sensorimotor control of robots mediated by propulsive fungal hyphae (Science Robotics 9:eadk8019, NSF open PDF)"),
    dict(key="yamamoto2024_chemotropism", kind="pmc", id="PMC11288418", tier="T2",
         title="Hyphae of the fungus Aspergillus nidulans demonstrate chemotropism to nutrients and pH"),
    dict(key="brand2009_gow",        kind="pmc", id="PMC2728830", tier="T2",
         title="Mechanisms of hypha orientation of fungi"),
    # ---- SECONDARY: lane-cited open papers (S4 register + G-D chain + GA rig table) ----
    dict(key="adamatzky2018_towards", kind="pmc", id="PMC6227805", tier="T1",
         title="Towards fungal computer"),
    dict(key="adamatzky2018_pdjamor", kind="pmc", id="PMC5959856", tier="T1",
         title="On spiking behaviour of oyster fungi Pleurotus djamor"),
    dict(key="adamatzky2022_language", kind="pmc", id="PMC8984380", tier="T1",
         title="Language of fungi derived from their electrical spiking activity"),
    dict(key="adamatzky2023_moisture", kind="pmc", id="PMC10069029", tier="T1",
         title="Electrical response of fungi to changing moisture content"),
    dict(key="adamatzky2023_commune", kind="pmc", id="PMC10406843", tier="T1",
         title="Multiscalar electrical spiking in Schizophyllum commune"),
    dict(key="adamatzky2023_insoles", kind="pmc", id="PMC10030783", tier="T1",
         title="Responsive fungal insoles for pressure detection"),
    dict(key="adamatzky2022_psilo",  kind="pmc", id="PMC9601536", tier="T3",
         title="Electrical spiking of psilocybin fungi"),
    dict(key="adamatzky2021_skin_retracted", kind="pmc", id="PMC7972235", tier="T3",
         title="Fungal sensing skin (RETRACTED — keep as artifact case study)"),
    dict(key="adamatzky2021_retraction_note", kind="pmc", id="PMC8173894", tier="T3",
         title="Retraction Note to: Fungal sensing skin"),
    dict(key="adamatzky2021_towards_skin", kind="pmc", id="PMC8117569", tier="T3",
         title="Towards fungal sensing skin (NOT retracted companion)"),
    dict(key="adamatzky2020_boolean", kind="arxiv", id="2002.09680", tier="T2",
         title="On Boolean gates in fungal colony (arXiv version of Biosystems 198:104138)"),
    dict(key="mayne2023_propagation", kind="arxiv", id="2304.10675", tier="T1",
         title="Propagation of electrical signals by fungi for half a century (Mayne et al., arXiv of BioSystems 233:104933)"),
    dict(key="boisseau2016_habituation", kind="pmc", id="PMC4855389", tier="T2",
         title="Habituation in an amoeba: memory of the Cafeteria (Proc R Soc B 283:20160446)"),
    dict(key="nishi2026_habituation_model", kind="pmc", id="PMC13481565", tier="T2",
         title="Minimal dynamical model of habituation (J Math Biol 93:36)"),
    dict(key="kagan2022_dishbrain",  kind="pmc", id="PMC9747182", tier="T3",
         title="In vitro neurons learn and exhibit sentience when embodied in a simulated game-world"),
    dict(key="sumi2023_generalization", kind="pmc", id="PMC10288593", tier="T3",
         title="Biological neurons act as generalization filters in reservoir computing"),
    dict(key="volkov2007_flytrap",   kind="pmc", id="PMC2634039", tier="T3",
         title="Closing of Venus flytrap by electrical stimulation of motor cells"),
    dict(key="thomas2022_cooper",    kind="pmc", id="PMC9673936", tier="T3",
         title="Building bridges: mycelium-mediated plant-plant electrophysiological communication (contested claim)"),
    dict(key="blatt2023_challenge",  kind="pmc", id="PMC10259323", tier="T3",
         title="A challenge to claims for mycorrhizal-transmitted wound signaling"),
    dict(key="finalspark2024",       kind="pmc", id="PMC11097343", tier="T3",
         title="Neuroplatform: an open platform for researching electrostimulation and recording of human brain organoids (FinalSpark)"),
    dict(key="gale2013_slime_memristor", kind="arxiv", id="1306.3414", tier="T3",
         title="Slime Mould Memristors"),
    dict(key="jones2013_shrinking",  kind="arxiv", id="1303.4969", tier="T3",
         title="Computation of the Travelling Salesman Problem by a Shrinking Blob"),
    dict(key="pershin2008_amoeba",   kind="arxiv", id="0810.4179", tier="T3",
         title="Memristive model of amoeba's learning"),
    dict(key="bajpai2025_physarum_rc", kind="arxiv", id="2510.19976", tier="T3",
         title="Morphological computational Capacity of Physarum polycephalum"),
    dict(key="schick2026_light",     kind="arxiv", id="2506.12803", tier="T2",
         title="Light-trapped decision-making in Physarum (arXiv version of PRX Life 4:023026)"),
    dict(key="whittle2013_tactile",  kind="arxiv", id="1306.0258", tier="T3",
         title="Slime mould tactile sensor (arXiv 1306.0258)"),
    dict(key="arxiv2505_modeling",   kind="arxiv", id="2505.02114", tier="T3",
         title="2025 Physarum/reservoir modeling paper (simulation-only; cited C17)"),
    dict(key="arxiv2508_fading",     kind="arxiv", id="2508.19145", tier="T3",
         title="Unified fading-memory/echo-state view of physical reservoir computing (2025)"),
]

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def fetch(url, timeout=90, binary=True):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data


def looks_like_pdf(data):
    return data[:5] in (b"%PDF-", b"%PDF\n") or (len(data) > 1024 and data[:1024].find(b"%PDF-") >= 0)


def looks_like_xml(data):
    head = data[:256].lstrip()
    return head.startswith(b"<?xml") or head.startswith(b"<")


def xml_title(data):
    try:
        root = ET.fromstring(data)
    except Exception:
        return None
    for path in (".//front//article-title", ".//title-group//article-title"):
        el = root.find(path)
        if el is not None:
            txt = "".join(el.itertext())
            return re.sub(r"\s+", " ", txt).strip()
    return None


def slug(s, n=60):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s[:n]


def save(key, data, ext, tier, url, title, results):
    fname = f"{key}.{ext}"
    path = os.path.join(CANON, fname)
    with open(path, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    results.append(dict(url=url, file=fname, sha256=sha, title=title, tier=tier))
    print(f"  OK {fname} {len(data)} bytes sha256={sha[:12]}...", flush=True)
    return True


def fetch_pmc(pmcid, tier, title, results):
    xml = None
    try:
        xml = fetch(f"{EPMC}/{pmcid}/fullTextXML")
        if not looks_like_xml(xml):
            xml = None
    except Exception as e:
        LOG.append(f"epmc fullTextXML fail {pmcid}: {e}")
    if xml is None:
        try:
            xml = fetch(f"{EUTILS}/efetch.fcgi?db=pmc&id={pmcid[3:]}&retmode=xml")
            if not looks_like_xml(xml):
                xml = None
        except Exception as e:
            LOG.append(f"eutils fail {pmcid}: {e}")
    if xml is None:
        print(f"  MISS {pmcid}: no full XML", flush=True)
        return False
    t = xml_title(xml)
    if t:
        title = t
    return save(pmcid.lower(), xml, "xml", tier, f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/", title, results)


def fetch_arxiv(arxid, tier, title, results):
    try:
        pdf = fetch(f"https://arxiv.org/pdf/{arxid}")
    except Exception as e:
        LOG.append(f"arxiv fail {arxid}: {e}")
        print(f"  MISS arxiv {arxid}", flush=True)
        return False
    if not looks_like_pdf(pdf):
        print(f"  MISS arxiv {arxid}: not a PDF", flush=True)
        return False
    return save(f"arxiv_{arxid.replace('.', '_').replace('v', '')}", pdf, "pdf", tier,
                f"https://arxiv.org/abs/{arxid}", title, results)


def main():
    os.makedirs(CANON, exist_ok=True)
    results = []
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for job in JOBS:
        if only and only not in job["key"]:
            continue
        kind = job["kind"]
        print(f"[{kind}] {job['key']}", flush=True)
        ok = False
        if kind == "pmc":
            ok = fetch_pmc(job["id"], job["tier"], job["title"], results)
        elif kind == "arxiv":
            ok = fetch_arxiv(job["id"], job["tier"], job["title"], results)
        elif kind == "direct":
            try:
                data = fetch(job["url"])
                ext = "pdf" if looks_like_pdf(data) else ("xml" if looks_like_xml(data) else None)
                if ext:
                    ok = save(job["file"].rsplit(".", 1)[0], data, ext, job["tier"], job["url"], job["title"], results)
                else:
                    print(f"  MISS {job['key']}: unknown content-type head={data[:64]!r}", flush=True)
                    LOG.append(f"direct fail {job['key']}: head={data[:64]!r}")
            except Exception as e:
                print(f"  MISS {job['key']}: {e}", flush=True)
                LOG.append(f"direct fail {job['key']}: {e}")
        time.sleep(0.6)
    # incremental manifest merge
    mpath = os.path.join(CANON, "manifest.jsonl")
    have = {}
    if os.path.exists(mpath):
        with open(mpath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        r = json.loads(line)
                        have[r["file"]] = r
                    except Exception:
                        pass
    for r in results:
        have[r["file"]] = r
    with open(mpath, "w", encoding="utf-8", newline="\n") as f:
        for r in sorted(have.values(), key=lambda x: (x["tier"], x["file"])):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nmanifest rows total: {len(have)}", flush=True)
    if LOG:
        print("LOG:", flush=True)
        for l in LOG:
            print(" ", l, flush=True)


if __name__ == "__main__":
    main()
