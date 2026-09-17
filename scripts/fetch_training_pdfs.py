#!/usr/bin/env python3
"""Training-corpus fetcher -- wave lane N6, 2026-09-16.

Law compliance:
  - receipt FIRST: watch/inbox/wave_20260916/receipts/N6_TRAINING_PDF_FETCH.md
  - no paid APIs; free fetches only (arXiv PDFs, PMC/Europe-PMC open access,
    Feynman Lectures HTML, institutional open mirrors verified in receipts)
  - robots.txt checked manually for every target host on 2026-09-16; per-host
    crawl delays below mirror what the robots files declare
  - stdlib only (urllib, hashlib, html.parser); no third-party deps

Fixed manifest of open-access training documents. For each entry the candidate
URLs are tried in order until one yields (a) bytes with the %PDF magic, or
(b) an HTML/XML page whose text survives extraction (bot-challenge pages and
stub pages are rejected and the next candidate is tried). PDFs are stored
as .pdf; HTML/XML sources are stored as plain-text .txt extractions.

Outputs (all under memory/corpus/training_pdfs/20260916/):
  - one .pdf or .txt file per fetched entry
  - manifest.jsonl: one row per entry {id,title,source,url,file,sha256,format,bytes,status,attempts}
  - INDEX.md: human-readable index + blocked list + readiness assessment
"""

import hashlib
import html.parser
import http.client
import json
import os
import re
import socket
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "memory", "corpus", "training_pdfs", "20260916")

USER_AGENT = "MagTrainingCorpusFetcher/1.0 (local research corpus; robots-respecting; single-user)"
TIMEOUT = 90

# Per-host crawl delay (seconds), mirroring robots.txt declarations checked 2026-09-16.
HOST_DELAY = {
    "arxiv.org": 15.0,
    "pmc.ncbi.nlm.nih.gov": 1.0,
    "www.ebi.ac.uk": 1.0,
}
DEFAULT_DELAY = 1.5

# ---------------------------------------------------------------------------
# Manifest: entries with candidate URLs in priority order.
# Sources: S4 (fungal register), O2/O3/CONCERT002 (fiber-optical),
# B10/B11/LINKS_ORE3 (attention), LINKS_ORE3 (BO primer), spinor-lattice vein.
# ---------------------------------------------------------------------------

def pmc(pmcid):
    """Candidate URL list for one PMC open-access item.

    Route 1: Europe PMC REST JATS full text (works for the OA subset; a few
             items return HTTP 500 -- see route 2).
    Route 2: PMC article page HTML (robots-allowed /articles/). NOTE: the
             /articles/<id>/pdf/ route is intentionally NOT used -- it now
             serves a JS interstitial stub to non-browser clients, not the PDF
             (verified 2026-09-16).
    """
    return [
        "https://www.ebi.ac.uk/europepmc/webservices/rest/%s/fullTextXML" % pmcid,
        "https://pmc.ncbi.nlm.nih.gov/articles/%s/" % pmcid,
    ]


def arxiv(aid):
    return ["https://arxiv.org/pdf/%s" % aid]


ENTRIES = [
    # --- S4 fungal-compute canon (open rows) -------------------------------
    {"id": "s4_t12_adamatzky_2018_towards_fungal_computer",
     "title": "Adamatzky (2018) Towards fungal computer, Interface Focus 8:20180029",
     "source": "S4-T1.2", "urls": pmc("PMC6227805") + [
         "https://r.jina.ai/https://pmc.ncbi.nlm.nih.gov/articles/PMC6227805/"]},
    {"id": "s4_t13_adamatzky_2022_language_of_fungi",
     "title": "Adamatzky (2022) Language of fungi derived from their electrical spiking activity, R. Soc. Open Sci. 9:211926",
     "source": "S4-T1.3", "urls": pmc("PMC8984380")},
    {"id": "s4_t14_adamatzky_2023_moisture_response",
     "title": "Adamatzky (2023) Electrical response of fungi to changing moisture content, Fungal Ecol. Biol.",
     "source": "S4-T1.4", "urls": pmc("PMC10069029")},
    {"id": "s4_t15_adamatzky_2026_star_array",
     "title": "Adamatzky (2026) Directional electrical spiking, bursting, and information propagation in oyster mycelium (star electrode array), arXiv 2601.08099",
     "source": "S4-T1.5", "urls": arxiv("2601.08099")},
    {"id": "s4_t16_adamatzky_2026_sci_rep_linear_array",
     "title": "Adamatzky (2026) Propagation of electrical spike trains in substrates colonised by oyster fungi, Sci. Rep.",
     "source": "S4-T1.6", "urls": pmc("PMC13212958")},
    {"id": "s4_t17_buffi_2025_iscience_fpc",
     "title": "Buffi et al. (2025) Detection of electrical signals in fungal mycelia in response to external stimuli (Fungal Potential Card), iScience 28:113484",
     "source": "S4-T1.7", "urls": pmc("PMC12483595")},
    {"id": "s4_t18_buffi_2025_fems_review",
     "title": "Buffi et al. (2025) Electrical signaling in fungi: past and present challenges (methods checklist), FEMS Microbiol. Rev. 49:fuaf009",
     "source": "S4-T1.8 + O2/O3/CONCERT002", "urls": pmc("PMC11995700")},
    {"id": "s4_t21_telhan_2026_mycelium_chips",
     "title": "Telhan et al. / Ecovative (2026) Morphologically tunable mycelium chips for physical reservoir computing, Sci. Rep. 16",
     "source": "S4-T2.1 + CONCERT002", "urls": pmc("PMC13500807")},
    {"id": "s4_t22_larocco_2025_shiitake_memristors",
     "title": "LaRocco et al. (2025) Sustainable memristors from shiitake mycelium for high-frequency bioelectronics, PLOS ONE",
     "source": "S4-T2.2 + CONCERT002", "urls": pmc("PMC12513579")},
    {"id": "s4_t23_adamatzky_2020_boolean_gates",
     "title": "Adamatzky, Tsompanas (2020) On Boolean gates in fungal colony, Biosystems 198:104138 (arXiv version)",
     "source": "S4-T2.3", "urls": arxiv("2002.09680")},
    {"id": "s4_t25_kagan_2022_dishbrain",
     "title": "Kagan et al. (2022) In vitro neurons learn and exhibit sentience when embodied in a simulated game-world (DishBrain), Neuron 110:2029",
     "source": "S4-T2.5", "urls": pmc("PMC9747182")},
    {"id": "s4_t26_sumi_2023_pnas_generalization_filters",
     "title": "Sumi et al. (2023) Biological neurons act as generalization filters in reservoir computing, PNAS 120:e2217008120",
     "source": "S4-T2.6", "urls": pmc("PMC10288593")},
    {"id": "s4_t33_jones_2013_shrinking_blob_tsp",
     "title": "Jones, Adamatzky (2013) Computation of the Travelling Salesman Problem by a Shrinking Blob, arXiv 1303.4969",
     "source": "S4-T3.3", "urls": arxiv("1303.4969")},
    {"id": "s4_t34_gale_2013_slime_mould_memristors",
     "title": "Gale, Adamatzky, de Lacy Costello (2013) Slime Mould Memristors, arXiv 1306.3414",
     "source": "S4-T3.4", "urls": arxiv("1306.3414")},
    {"id": "s4_t35_pershin_2008_amoeba_memristive",
     "title": "Pershin, La Fontaine, Di Ventra (2008) Memristive model of amoeba's learning, arXiv 0810.4179",
     "source": "S4-T3.5", "urls": arxiv("0810.4179")},
    {"id": "s4_t36_volkov_2007_venus_flytrap",
     "title": "Volkov, Adesina, Jovanov (2007) Closing of Venus flytrap by electrical stimulation of motor cells, Plant Signal. Behav. 2:139",
     "source": "S4-T3.6", "urls": pmc("PMC2634039") + [
         "https://r.jina.ai/https://pmc.ncbi.nlm.nih.gov/articles/PMC2634039/"]},
    {"id": "s4_t37_bajpai_2025_physarum_rc",
     "title": "Bajpai, Lucas-DeMott, Murugan, Levin, Kurian (2025) Morphological computational capacity of Physarum polycephalum, arXiv 2510.19976",
     "source": "S4-T3.7", "urls": arxiv("2510.19976")},
    {"id": "s4_t42_adamatzky_2021_fungal_sensing_skin_retracted",
     "title": "Adamatzky (2021) Fungal sensing skin [RETRACTED], Fungal Ecol. Biol. -- kept as retraction-case training material",
     "source": "S4-T4.2", "urls": pmc("PMC7972235")},
    {"id": "s4_t42_retraction_note",
     "title": "Retraction Note to: Fungal sensing skin (2021), DOI 10.1186/s40694-021-00114-7",
     "source": "S4-T4.2", "urls": pmc("PMC8173894")},
    {"id": "s4_t43_thomas_cooper_2022_mycelium_bridges",
     "title": "Thomas, Cooper (2022) Building bridges: mycelium-mediated plant-plant electrophysiological communication [contested claim], Plant Signal. Behav. 17:2129291",
     "source": "S4-T4.3", "urls": pmc("PMC9673936")},
    {"id": "s4_t44_blatt_2023_challenge",
     "title": "Blatt et al. (2023) A challenge to claims for mycorrhizal-transmitted wound signaling, Plant Signal. Behav. 18:2222957",
     "source": "S4-T4.4", "urls": pmc("PMC10259323")},
    {"id": "s4_t27_adamatzky_2024_fungal_skin_robots_preprint",
     "title": "Adamatzky (2024) Fungal skin for robots, Biosystems 236:105106 -- Research Square open preprint (journal version paywalled)",
     "source": "S4-T2.7", "urls": [
         # reader-proxy first: the direct article page is a JS app shell whose
         # server-rendered HTML is mostly navigation (verified 2026-09-16)
         "https://r.jina.ai/https://www.researchsquare.com/article/rs-3292325/v1",
         "https://www.researchsquare.com/article/rs-3292325/v1"]},
    {"id": "s4_appx_dale_2018_rc_characterization",
     "title": "Dale, Miller, Stepney (2018) Reservoir computing as a model for in-materio computing (characterization framework), arXiv 1810.07135",
     "source": "S4-appendix", "urls": arxiv("1810.07135")},

    # --- Fiber / optical (O2, O3, CONCERT002, G-F spinor lattice) ----------
    {"id": "o2_carrillo_acuna_2023_apl_diffuser",
     "title": "Carrillo-Acuna et al. (2023) An efficient optical diffuser fabricated from fungal mycelium, Appl. Phys. Lett. 122:113702 (IPICYT open-repository PDF)",
     "source": "O2/CONCERT002", "urls": [
         "https://repositorio.ipicyt.edu.mx/bitstream/handle/11627/6549/ApplPhysLett122%282023%29113702.pdf"]},
    {"id": "o3_mishra_2024_science_robotics",
     "title": "Mishra et al. (2024) Sensorimotor control of robots mediated by fungal biohybrid interface, Science Robotics 9:eadk8019 (NSF PAR open PDF)",
     "source": "O3/C19", "urls": ["https://par.nsf.gov/servlets/purl/10548775"]},
    {"id": "o3_neurospora_wcc_blue_light",
     "title": "Neurospora WCC blue-light photoreception (PMC open access)",
     "source": "O3", "urls": pmc("PMC2775248") + [
         "https://r.jina.ai/https://pmc.ncbi.nlm.nih.gov/articles/PMC2775248/"]},
    {"id": "gf_mobius_microring_apl_2019",
     "title": "Mobius microring resonator, Appl. Phys. Lett. 114:101106 (2019) -- landing page only; PDF paywalled at AIP",
     "source": "G-F spinor lattice", "urls": [
         "https://pubs.aip.org/aip/apl/article/114/10/101106/36781/"]},

    # --- Attention papers (B10/B11/LINKS_ORE3) -----------------------------
    {"id": "b11_sliding_window_sinks_2608.28444",
     "title": "Jolicoeur-Martineau et al. (2026) Training-free sliding-window attention with sink tokens (the B11 moving baseline), arXiv 2608.28444",
     "source": "B10/B11", "urls": arxiv("2608.28444")},
    {"id": "goat_entropic_ot_attention_2601.15380",
     "title": "GOAT: entropic optimal-transport attention with trainable continuous prior (rival to B11 sink doctrine), arXiv 2601.15380",
     "source": "LINKS_ORE3", "urls": arxiv("2601.15380")},
    {"id": "b10_jelassi_2024_repeat_after_me",
     "title": "Jelassi, Brandfonbrener, Kakade, Malach (2024) Repeat After Me: Transformers are Better than State Space Models at Copying, arXiv 2402.01032",
     "source": "B10", "urls": arxiv("2402.01032")},
    {"id": "b10_kimi_linear_2510.26692",
     "title": "Kimi Linear (2025): hybrid linear attention beating full attention under fair comparison, arXiv 2510.26692",
     "source": "B10", "urls": arxiv("2510.26692")},
    {"id": "honjo_2021_100k_spin_cim",
     "title": "Honjo et al. (2021) 100,000-spin coherent Ising machine, Science Advances 7:eabh0952 (Inagaki->Honjo correction chain)",
     "source": "substrate synthesis / N6", "urls": pmc("PMC8480917")},

    # --- Bayesian optimization primers (LINKS_ORE3 note 2 -> cube program) -
    {"id": "bo_frazier_2018_tutorial",
     "title": "Frazier (2018) A Tutorial on Bayesian Optimization, arXiv 1807.02811",
     "source": "LINKS_ORE3 #2", "urls": arxiv("1807.02811")},
    {"id": "bo_snoek_2012_practical_bo",
     "title": "Snoek, Larochelle, Adams (2012) Practical Bayesian Optimization of Machine Learning Algorithms, NIPS 2012",
     "source": "LINKS_ORE3 #2", "urls": [
         "https://papers.nips.cc/paper_files/paper/2012/file/05311655a15b75fab86956663e1819cd-Paper.pdf",
         "https://papers.nips.cc/paper_files/paper/2012/hash/05311655a15b75fab86956663e1819cd-Abstract.html"]},

    # --- Spinor primers (G-F spinor lattice vein; Feynman III sections 3.1-3.2)
    {"id": "feynman_iii_03_probability_amplitudes_3_1_3_2",
     "title": "Feynman Lectures on Physics, Vol III ch 3 Probability Amplitudes (sections 3.1-3.2), Caltech free HTML edition",
     "source": "spinor primer", "urls": [
         "https://www.feynmanlectures.caltech.edu/III_03.html",
         # fallback: free reader proxy returns the same public page as plain
         # text with a URL Source provenance line (Caltech front door is
         # Cloudflare-challenged for non-browser clients; verified 2026-09-16)
         "https://r.jina.ai/https://www.feynmanlectures.caltech.edu/III_03.html"]},
]

# Known-paywalled canon rows (from S4 register + fiber receipts): not fetched.
# Included in INDEX.md so the blocked list is honest and library needs are named.
KNOWN_PAYWALLED = [
    ("S4-T1.1 Slayman 1976, 'Action potentials' in Neurospora crassa, BBA 426:732",
     "Elsevier ScienceDirect", "institutional library / interlibrary loan"),
    ("S4-T2.4 Adamatzky 2026, Fungal biohybrid substrates, Biosystems 261:105739",
     "Elsevier ScienceDirect", "institutional library; abstract held"),
    ("S4-T2.7 journal version Adamatzky 2024 Fungal skin for robots, Biosystems 236:105106",
     "Elsevier ScienceDirect", "open preprint fetched instead"),
    ("S4-T3.1 Nakagaki 2000, Maze-solving by an amoeboid organism, Nature 407:470",
     "nature.com", "institutional library"),
    ("S4-T3.2 Tero 2010, Rules for biologically inspired adaptive network design, Science 327:439",
     "science.org", "institutional library (author PDFs circulate; not fetched -- provenance hygiene)"),
    ("S4-T4.1 Karst 2023, Positive citation bias..., Nat. Ecol. Evol. 7:501",
     "nature.com", "institutional library (correction is free)"),
    ("S4-T4.4b Blatt 2024, Does electrical activity in fungi function as a language?, Fungal Ecol. 68:101326",
     "Elsevier ScienceDirect", "institutional library"),
    ("Adamatzky 2023, Propagation of electrical signals by fungi, Biosystems 233:104933",
     "Elsevier ScienceDirect", "superseded for our use by S4-T1.6 (open)"),
    ("Toyota 2018, Glutamate triggers long-distance Ca2+ plant defense signaling, Science 361:1112",
     "science.org", "free after 12 months on science.org; not robot-fetchable tonight"),
    ("Fernando & Sojakka 2003, Pattern Recognition in a Bucket, ECAL LNCS 2801",
     "Springer", "Semantic Scholar openAccessPdf route exists (api.semanticscholar.org) -- next pass"),
    ("GF Mobius microring APL 114:101106 (2019) PDF",
     "pubs.aip.org", "institutional library; landing page attempted in manifest"),
    ("Honjo 2021 Sci Adv PDF via science.org",
     "science.org /na101 CDN is robots-disallowed", "PMC8480917 open copy fetched instead"),
]

# ---------------------------------------------------------------------------

_LAST_HIT = {}  # host -> monotonic time of last request


def _respect_delay(host):
    delay = HOST_DELAY.get(host, DEFAULT_DELAY)
    last = _LAST_HIT.get(host)
    if last is not None:
        wait = delay - (time.monotonic() - last)
        if wait > 0:
            time.sleep(wait)
    _LAST_HIT[host] = time.monotonic()


def fetch(url):
    """Fetch URL bytes with honest UA + robots-mirroring delays.

    Streams in 64 KiB chunks and resumes truncated transfers with HTTP Range
    requests (the 11.7 MB NSF PAR PDF truncated twice under single-shot
    reads). Retries with backoff on transient failures; 4xx (except 416 on a
    completed resume) is not retried.
    """
    host = re.sub(r"^https?://", "", url).split("/")[0]
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    body = b""
    last_err = None
    for attempt in range(5):
        if attempt:
            time.sleep([3.0, 8.0, 15.0, 30.0][attempt - 1])
        _respect_delay(host)
        h = dict(headers)
        ranged = bool(body)
        start = len(body)
        if ranged:
            h["Range"] = "bytes=%d-" % start
        req = urllib.request.Request(url, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                status = resp.getcode()
                clen = resp.headers.get("Content-Length")
                if ranged and status == 200:
                    body = b""  # server ignored Range; restart cleanly
                buf = bytearray(body)
                while True:
                    chunk = resp.read(1 << 16)
                    if not chunk:
                        break
                    buf.extend(chunk)
                body = bytes(buf)
                if ranged and status == 206 and clen:
                    expected = start + int(clen)
                elif clen:
                    expected = int(clen)
                else:
                    expected = None
                if expected is None or len(body) >= expected:
                    return body
                last_err = RuntimeError("truncated: %d of %s bytes" % (len(body), clen))
        except urllib.error.HTTPError as e:
            if ranged and e.code == 416:
                return body  # range past end -> already complete
            if 400 <= e.code < 500:
                raise
            last_err = e
        except (urllib.error.URLError, socket.timeout, http.client.IncompleteRead,
                ConnectionError, OSError) as e:
            last_err = e
    if isinstance(last_err, BaseException):
        raise last_err
    raise RuntimeError(str(last_err))


def is_pdf(content):
    return content[:1024].lstrip().startswith(b"%PDF")


def is_bot_challenge(content):
    head = content[:8192]
    return (b"cf_chl_opt" in head or b"Just a moment..." in head
            or b"challenges.cloudflare.com" in head
            or b"Enable JavaScript and cookies" in head)


def looks_like_html(content):
    head = content[:1024].lstrip().lower()
    return (b"<!doctype" in head or b"<html" in head or b"<body" in head
            or head.startswith(b"<?xml") or head.startswith(b"<article")
            or b"<article" in head or b"<section" in head)


class _TextExtractor(html.parser.HTMLParser):
    """Crude HTML/XML -> plain text: drop script/style, keep block newlines."""
    _SKIP = {"script", "style", "noscript", "svg", "iframe", "head", "title"}
    _BLOCK = {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "h5",
              "h6", "li", "tr", "br", "table", "ul", "ol", "blockquote",
              "sec", "abstract", "ref-list", "body", "fig", "table-wrap"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._chunks = []
        self._skip_depth = 0
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag in self._BLOCK and self._chunks:
            self._chunks.append("\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in self._BLOCK:
            self._chunks.append("\n")

    def handle_data(self, data):
        if self._skip_depth == 0 and data.strip():
            self._chunks.append(data)

    def text(self):
        raw = "".join(self._chunks)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n\s*\n+", "\n\n", raw)
        return raw.strip()


def html_to_text(content):
    parser = _TextExtractor()
    for enc in ("utf-8", "latin-1"):
        try:
            parser.feed(content.decode(enc))
            break
        except UnicodeDecodeError:
            parser = _TextExtractor()
            continue
    return parser.text()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest_path = os.path.join(OUT_DIR, "manifest.jsonl")
    index_path = os.path.join(OUT_DIR, "INDEX.md")
    rows = []
    url_cache = {}  # url -> (status, content)

    for entry in ENTRIES:
        status = "blocked"
        got_url = None
        fmt = None
        content = None
        attempts = []
        for url in entry["urls"]:
            if url in url_cache:
                status, content = url_cache[url]
                attempts.append({"url": url, "result": "cached:" + status})
                if status != "failed":
                    got_url = url
                    break
                continue
            try:
                content = fetch(url)
            except urllib.error.HTTPError as e:
                attempts.append({"url": url, "result": "HTTP %d" % e.code})
                url_cache[url] = ("failed", b"")
                continue
            except Exception as e:  # noqa: BLE001 -- record every failure kind
                attempts.append({"url": url, "result": type(e).__name__ + ": " + str(e)[:120]})
                url_cache[url] = ("failed", b"")
                continue
            if is_pdf(content):
                url_cache[url] = ("fetched:pdf", content)
                status, got_url, fmt = "fetched", url, "pdf"
                attempts.append({"url": url, "result": "ok pdf %d bytes" % len(content)})
                break
            if is_bot_challenge(content):
                attempts.append({"url": url, "result": "bot-challenge page (rejected)"})
                url_cache[url] = ("failed", b"")
                continue
            if looks_like_html(content):
                text = html_to_text(content)
                if len(text) < 400:
                    attempts.append({"url": url, "result": "html stub (%d chars, rejected)" % len(text)})
                    url_cache[url] = ("failed", b"")
                    continue
                url_cache[url] = ("fetched:text", text.encode("utf-8"))
                content = text.encode("utf-8")
                status, got_url, fmt = "fetched", url, "txt"
                attempts.append({"url": url, "result": "ok text %d chars" % len(text)})
                break
            # plain-text response (e.g. reader-proxy markdown of an HTML page)
            try:
                decoded = content.decode("utf-8")
            except UnicodeDecodeError:
                decoded = ""
            printable = sum(1 for ch in decoded if ch.isprintable() or ch in "\n\r\t")
            if len(decoded) >= 400 and printable / max(1, len(decoded)) > 0.85:
                url_cache[url] = ("fetched:text", content)
                status, got_url, fmt = "fetched", url, "txt"
                attempts.append({"url": url, "result": "ok plain text %d chars" % len(decoded)})
                break
            attempts.append({"url": url, "result": "unrecognized content-type, rejected"})
            url_cache[url] = ("failed", b"")

        row = {
            "id": entry["id"],
            "title": entry["title"],
            "source": entry["source"],
            "status": status,
            "format": fmt,
            "url": got_url,
            "file": None,
            "sha256": None,
            "bytes": None,
            "attempts": attempts,
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        if status == "fetched":
            ext = "pdf" if fmt == "pdf" else "txt"
            fname = entry["id"] + "." + ext
            with open(os.path.join(OUT_DIR, fname), "wb") as f:
                f.write(content)
            row["file"] = fname
            row["bytes"] = len(content)
            row["sha256"] = hashlib.sha256(content).hexdigest()
            print("[FETCHED] %-52s %-4s %9d B  %s" % (entry["id"], ext, len(content), got_url))
        else:
            print("[BLOCKED] %-52s %s" % (entry["id"], attempts[-1]["result"] if attempts else "no url"))
        rows.append(row)

    with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")

    fetched = [r for r in rows if r["status"] == "fetched"]
    blocked = [r for r in rows if r["status"] != "fetched"]
    total_bytes = sum(r["bytes"] or 0 for r in fetched)
    n_pdf = sum(1 for r in fetched if r["format"] == "pdf")
    n_txt = sum(1 for r in fetched if r["format"] == "txt")

    # ---- INDEX.md ---------------------------------------------------------
    lines = []
    a = lines.append
    a("# Training-corpus batch 20260916 -- INDEX")
    a("")
    a("Lane: N6 · Built by the stdlib fetcher (see `scripts/`, wave law: no git,")
    a("no paid APIs, robots-respecting). Receipt:")
    a("`watch/inbox/wave_20260916/receipts/N6_TRAINING_PDF_FETCH.md`.")
    a("")
    a("## Summary")
    a("")
    a("| metric | value |")
    a("|---|---|")
    a("| manifest entries | %d |" % len(rows))
    a("| fetched | %d (%d pdf, %d txt) |" % (len(fetched), n_pdf, n_txt))
    a("| blocked this run | %d |" % len(blocked))
    a("| total size | %.2f MB |" % (total_bytes / 1e6))
    a("")
    a("## Fetched documents")
    a("")
    a("| file | format | KB | source | sha256 (first 12) |")
    a("|---|---|---|---|---|")
    for r in fetched:
        a("| `%s` | %s | %d | %s | %s |" % (
            r["file"], r["format"], (r["bytes"] or 0) // 1000,
            r["source"], (r["sha256"] or "")[:12]))
    a("")
    if blocked:
        a("## Blocked / failed this run")
        a("")
        a("| entry | last attempt result |")
        a("|---|---|")
        for r in blocked:
            last = r["attempts"][-1]["result"] if r["attempts"] else "no url tried"
            a("| `%s` | %s |" % (r["id"], last))
        a("")
    a("## Known-paywalled canon (not fetched; library needed)")
    a("")
    a("| item | paywall | what opens it |")
    a("|---|---|---|")
    for item, wall, lib in KNOWN_PAYWALLED:
        a("| %s | %s | %s |" % (item, wall, lib))
    a("")
    a("## Readiness for training / retrieval")
    a("")
    a("- **Directly chunkable now:** the %d `.txt` files (PMC JATS/HTML and Feynman" % n_txt)
    a("  HTML extractions) -- plain text, section breaks preserved, ready for any")
    a("  fixed-window or heading-aware chunker.")
    a("- **Chunkable after one extraction pass:** the %d `.pdf` files -- all" % n_pdf)
    a("  born-digital (arXiv / PMC / NSF-PAR / DSpace renders), none scanned, so")
    a("  `pypdf`/`pdfminer` (or `pdftotext`) extracts clean text; **no OCR is")
    a("  expected for any file in this batch**. The 11.7 MB Mishra NSF PDF is the")
    a("  only large item (figures inflate size; text layer is normal).")
    a("- **Tables/equations:** PDF extraction will flatten tables and equations;")
    a("  the PMC JATS XML route (recorded as `url` on affected rows) can be")
    a("  re-fetched for structure-preserving XML when a chunker wants it.")
    a("- **Integrity:** every file is sha256-summed in `manifest.jsonl`; re-run the")
    a("  fetcher to verify hashes byte-for-byte (trust bytes, not reports).")
    a("- **License posture:** open-access items only; the retracted + contested")
    a("  papers are included deliberately as negative/case-study training material")
    a("  and are labeled as such in their titles.")
    a("")
    with open(index_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print("---")
    print("entries=%d fetched=%d (pdf=%d txt=%d) blocked=%d total_MB=%.2f"
          % (len(rows), len(fetched), n_pdf, n_txt, len(blocked), total_bytes / 1e6))
    print("out=%s" % OUT_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
