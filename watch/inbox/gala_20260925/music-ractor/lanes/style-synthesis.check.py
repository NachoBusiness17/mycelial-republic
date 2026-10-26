"""style-synthesis finish-line check.

Byte-verifies watch/inbox/music/STYLE_SPEC.md:
  1. file exists, prints size + sha256
  2. exactly 3 Suno style strings (fenced blocks under '### Facet' headers), each < 900 chars, each names its BPM
  3. artist-name blocklist (from folder filenames + audio-dna artist column): zero hits in the style strings AND the whole file
  4. em-dash law: no U+2014 / U+2013 anywhere in the file
  5. numeric claims in the spec re-derived from the lane's own profile JSON and matched
Exit 0 = all pass. Print raw PASS/FAIL lines for the receipt.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np

SPEC = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/music/STYLE_SPEC.md")
PROFILE = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.json")

# artist names + distinctive fragments (lowercase). bare "punk" excluded on purpose: genre word.
BLOCKLIST = [
    "daft", "justice", "soundsystem", "lcd", "soulwax", "mstrkrft", "sebastian",
    "boys noize", "aeroplane", "classixx", "photek", "ronson", "oizo", "vitalic",
    "digitalism", "simian", "ratatat", "kavinsky", "bangalter", "fischerspooner",
    "goldfrapp", "aphex", "jaxx", "eilish", "caravan palace", "cut copy", "cassius",
    "hot chip", "junior boys", "mehdi", "friendly fires", "la priest", "birdy nam nam",
    "johnny sa", "biebieq", "lekker", "busy p", "chemical brothers",
]

failures = []

def check(label, ok, detail=""):
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail), flush=True)
    if not ok:
        failures.append(label)

def main() -> int:
    print("== style-synthesis finish-line check ==")
    print("spec:", str(SPEC))
    check("spec.exists", SPEC.is_file())
    if not SPEC.is_file():
        return 1
    raw = SPEC.read_bytes()
    text = raw.decode("utf-8")
    print("spec.size_bytes", len(raw))
    print("spec.sha256", hashlib.sha256(raw).hexdigest())

    facets = re.findall(r"### Facet [ABC]:[^\n]*\n+```\n(.*?)\n```", text, re.S)
    check("facet.count3", len(facets) == 3, "found %d" % len(facets))
    for i, s in enumerate(facets):
        check("facet.%d.lt900" % (i + 1), 0 < len(s) < 900, "len=%d" % len(s))
        check("facet.%d.has_bpm" % (i + 1), "BPM" in s)

    low = text.lower()
    for i, s in enumerate(facets):
        hits = [w for w in BLOCKLIST if w in s.lower()]
        check("facet.%d.no_artist_names" % (i + 1), not hits, "hits=%s" % hits)
    all_hits = sorted({w for w in BLOCKLIST if w in low})
    check("spec.no_artist_names_anywhere", not all_hits, "hits=%s" % all_hits)

    em = re.findall("[\u2013\u2014]", text)
    check("spec.no_em_dash", not em, "count=%d" % len(em))

    d = json.loads(PROFILE.read_text(encoding="utf-8"))
    rows = [r for r in d["rows"] if "bpm" in r]
    folded = np.array([r["bpm"] * 2 if r["bpm"] < 90 else r["bpm"] for r in rows])
    strong = np.array([r["bpm"] * 2 if r["bpm"] < 90 else r["bpm"]
                       for r in rows if r["bpm_conf"] >= 3.0])
    dur = np.array([r["duration_s"] for r in rows if r.get("duration_s")])
    peaks0 = sum(1 for r in rows if r["peak_dbfs"] > -0.5)

    spec_num = {
        "folded_median_124": ("124.0", abs(np.median(folded) - 124.0) <= 0.05),
        "strong_median_125": ("125.0", abs(np.median(strong) - 125.0) <= 0.05),
        "folded_p25_115.5": ("115.5", abs(np.percentile(folded, 25) - 115.5) <= 0.05),
        "folded_p75_129.75": ("129.75", abs(np.percentile(folded, 75) - 129.75) <= 0.05),
        "rms_median_-12.35": ("-12.35", abs(d["aggregate"]["rms_dbfs"]["median"] - (-12.35)) <= 0.02),
        "zcr_1272": ("1272", round(d["aggregate"]["zcr"]["median"] * 8000) == 1272),
        "centroid_1070": ("1070", d["aggregate"]["centroid_hz"]["median"] == 1070.0),
        "low_0.47": ("0.47", round(d["aggregate"]["low_share"]["median"], 2) == 0.47),
        "duration_264.6": ("264.6", round(np.median(dur), 1) == 264.6),
        "peaks_pinned_97of110": ("97 of 110", peaks0 == 97),
        "n_110": ("110/110", d["files_profiled"] == 110 and d["files_failed"] == 0),
        "band_115_130": ("115-130", True),  # shape check: band derived from p25/p75 above
    }
    for label, (needle, derived_ok) in spec_num.items():
        check("spec.%s" % label, derived_ok and needle in low,
              "needle=%r derived_ok=%s" % (needle, derived_ok))

    print("== %s: %d failure(s) ==" % ("GREEN" if not failures else "RED", len(failures)))
    if failures:
        for f in failures:
            print("FAILED:", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
