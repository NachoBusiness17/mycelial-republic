#!/usr/bin/env python
# F6 canon verification: PDF identity checks + abstract-claim spot-checks against full texts.
import os
import re
import sys
import xml.etree.ElementTree as ET

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "memory", "corpus", "mycology_canon")))
from pypdf import PdfReader


def pdftext(name, maxpages=6):
    try:
        r = PdfReader(name)
        out = []
        for i, p in enumerate(r.pages):
            if i >= maxpages:
                break
            out.append(p.extract_text() or "")
        return "\n".join(out)
    except Exception as e:
        return f"<<PDFFAIL {e}>>"


def pdftext_all(name, maxpages=999):
    try:
        r = PdfReader(name)
        out = []
        for i, p in enumerate(r.pages):
            if i >= maxpages:
                break
            out.append(p.extract_text() or "")
        return "\n".join(out)
    except Exception as e:
        return f"<<PDFFAIL {e}>>"


def show(label, text, pats, ctx=120):
    print(f"\n### {label}")
    flat = re.sub(r"\s+", " ", text)
    for pat in pats:
        ms = [m for m in re.finditer(pat, flat, re.I)]
        if not ms:
            print(f"  [MISS] {pat}")
        else:
            for m in ms[:3]:
                s = max(0, m.start() - ctx // 2)
                print(f"  [HIT] ...{flat[s:m.end() + ctx]}...")


# 1) Schmidt Frontiers PDF identity (S1 says Miranda quantum test; G-D says Schmidt 'From simulation to reality')
t = pdftext("schmidt2025_slime_mould_circuit_model.pdf", 2)
print("=== schmidt2025_frontsoft ID ===")
print(re.sub(r"\s+", " ", t)[:600])

# 2) Key-number spot checks
show("beasley arXiv 2002.06413", pdftext_all("arxiv_2002_06413.pdf"),
     [r"mem-?fract\w*", r"0\.5\s*V", r"1\s*V", r"iridium", r"10\s*mm", r"pinch"])
show("star array arXiv 2601.08099", pdftext_all("arxiv_2601_08099.pdf"),
     [r"star[- ]shaped", r"synchron", r"burst", r"aniso\w*", r"Pico", r"1\s*Hz"])
show("mayne arXiv 2304.10675", pdftext_all("arxiv_2304.10675.pdf"),
     [r"No signals were measured in control", r"shuffl\w*", r"half a century"])
show("mishra NSF PDF", pdftext("mishra2024_scirobotics_adk8019.pdf", 4),
     [r"blue light", r"ultraviolet|UV", r"acid|alkalin", r"cytoplasm", r"hyph"])
show("prakash bubble logic", pdftext("prakash2007_bubble_logic.pdf", 2),
     [r"bubble logic", r"AND|OR|NOT gate", r"toggle", r"counter"])
show("moratto2023 spiral AM", pdftext("moratto2023_electrotaxis.pdf", 2),
     [r"electrotaxis|electrotactic", r"0\.7|1\.0\s*V\s*cm", r"germination"])

# 3) XML spot checks
def xmlflat(name):
    return re.sub(r"\s+", " ", open(name, "rb").read().decode("utf-8", "ignore"))

show("adamatzky2026_linear pmc13212958.xml", xmlflat("pmc13212958.xml"),
     [r"0\.7\s*cm", r"median[^.]{0,80}0\.6", r"shuffl\w*", r"1\.4\s*mV", r"180\s*s"])
show("telhan pmc13500807.xml", xmlflat("pmc13500807.xml"),
     [r"0\.209", r"0\.048", r"NARMA", r"memory capacity", r"non-?living|not living|dead"])
show("larocco pmc12513579.xml", xmlflat("pmc12513579.xml"),
     [r"5\.85", r"90", r"dehydrat\w*", r"dried|sun-dried|dry", r"volatile"])
show("buffi FEMS pmc11995700.xml", xmlflat("pmc11995700.xml"),
     [r"nV", r"300\s*mV", r"door", r"Donnan", r"uncolonized|uncolonised"])
show("buffi FPC pmc12483595.xml", xmlflat("pmc12483595.xml"),
     [r"1604", r"Faraday", r"microvolt", r"cycloheximide", r"DMSO"])
show("yoneoka pmc10667701.xml", xmlflat("pmc10667701.xml"),
     [r"0\.5\s*mM", r"cut", r"rotat\w*", r"deleted|delete", r"mesh"])
show("kramar alim html", re.sub(r"<[^>]+>", " ", open("kramar2021_alim.html", "rb").read().decode("utf-8", "ignore")),
     [r"310\s*min", r"15\s*min", r"glucose", r"leucine", r"15\s*.*m/s|15\s*&\#956;m|m/s wave|µm/s"])
show("boussard html", re.sub(r"<[^>]+>", " ", open("boussard2019_memory.html", "rb").read().decode("utf-8", "ignore")),
     [r"sclerotia", r"2\s*h", r"sodium", r"1\s*month", r"circulating"])
print("\nDONE")
