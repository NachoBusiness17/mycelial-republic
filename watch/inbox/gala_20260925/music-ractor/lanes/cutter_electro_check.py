"""Finish-line byte battery for lane cutter-electro (division B, music-ractor).

Checks the 3 CUT packs in watch/inbox/music/cutter-electro_cuts.md against landed bytes:
  1. 3 CUT pack headers present
  2. style strings under 900 chars, ASCII-only, and the char counts claimed in the file
     match the measured counts
  3. zero em (U+2014) / en (U+2013) dashes in the whole file (seat law gate rule 2)
  4. no artist names inside the style strings (descriptors only)
  5. every triangulated folder-track filename exists in C:/Users/foste/Desktop/music-ai
  6. per-track DNA numbers cited in the cuts file match landed sources:
     watch/inbox/music/audio_dna.json (audio-dna lane, 30-track sample, first-90s window)
     and watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.json
     (style-synthesis lane, all 110 files)
  7. the electro-punch subset medians claimed in the cuts file recompute exactly from
     audio_dna.json rows
  8. the prior-cuts claim (dashboard/static/suno/ canon renders) is true on disk

Exit 0 = all checks pass. Any FAIL line = exit 1.
"""
import json
import os
import re
import statistics
import sys

ESTATE = "C:/Users/foste/Documents/projects/local_sovereign_agent"
CUTS = ESTATE + "/watch/inbox/music/cutter-electro_cuts.md"
FOLDER = "C:/Users/foste/Desktop/music-ai"
ADNA = ESTATE + "/watch/inbox/music/audio_dna.json"
SPROF = ESTATE + "/watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.json"
SUNO = ESTATE + "/dashboard/static/suno"

fails = []


def check(name, ok, detail):
    print(("PASS" if ok else "FAIL") + " | " + name + " | " + detail)
    if not ok:
        fails.append(name)


text = open(CUTS, encoding="utf-8").read()

# 1. three CUT headers
cuts = re.findall(r"^## CUT (\d): \"(.+?)\"$", text, re.M)
check("1 three-cut-headers", len(cuts) == 3,
      "found %d: %s" % (len(cuts), ", ".join(n + "=" + t for n, t in cuts)))

# 2. style blocks: under 900 chars, ASCII, claimed counts match
blocks = re.findall(r"```(.*?)```", text, re.S)
styles = [b for b in blocks if "BPM" in b and "LYRICS" not in b]
check("2a three-style-blocks", len(styles) == 3, "found %d" % len(styles))
claimed = [int(m) for m in re.findall(r"style field, (\d+) chars incl line breaks\)", text)]
measured = [len(s) for s in styles]
check("2b style-under-900", all(m < 900 for m in measured), "measured %s" % measured)
check("2c claimed-counts-match", claimed == measured,
      "claimed %s vs measured %s" % (claimed, measured))
check("2d style-ascii", all(all(ord(c) < 128 for c in s) for s in styles), "all ascii")

# 3. dash law
check("3 no-em-en-dashes", chr(0x2014) not in text and chr(0x2013) not in text,
      "em=%d en=%d" % (text.count(chr(0x2014)), text.count(chr(0x2013))))

# 4. no artist names in style strings
ARTISTS = ["justice", "mstrkrft", "soulwax", "daft punk", "boys noize", "sebastian",
           "digitalism", "phoenix", "chromeo", "kavinsky", "oizo", "gesaffelstein",
           "lcd soundsystem", "hot chip", "aeroplane", "photek", "classixx",
           "simian", "bernays", "jung", "ellul"]
leaks = []
for i, s in enumerate(styles, 1):
    low = s.lower()
    for a in ARTISTS:
        if a in low:
            leaks.append("cut%d:%s" % (i, a))
check("4 no-artist-names-in-styles", not leaks, "leaks=%s (genre terms only allowed)" % (leaks or "none"))

# 5. triangulated tracks exist in the folder
tracks = re.findall(r"- `(.+?\.mp3)` \(", text)
folder_files = set(os.listdir(FOLDER))
missing = [t for t in tracks if t not in folder_files]
check("5a six-tracks-named", len(tracks) == 6, "named %d: %s" % (len(tracks), tracks))
check("5b tracks-exist-in-folder", not missing, "missing=%s" % (missing or "none"))

# 6. cited per-track numbers match landed sources
adna = json.load(open(ADNA, encoding="utf-8"))["tracks"]
sprof = json.load(open(SPROF, encoding="utf-8"))["rows"]
def near(v, target, tol=0.011):
    return any(abs(r[k] - v) <= tol for r in rows for k in [kname])

cited = {
    "D.A.N.C.E. - MSTRKRFT Remix_spotdown.org.mp3": [(-10.67, "rms_dbfs"), (1906.3, "zcr_hz"), (126.0, "bpm_folded_or_raw"), (0.825, "bpm_conf")],
    "Phantom Pt II - Soulwax Remix_spotdown.org.mp3": [(-11.32, "rms_dbfs"), (127.0, "bpm_folded_or_raw"), (0.779, "bpm_conf")],
    "Blitz_spotdown.org.mp3": [(-9.62, "rms_dbfs"), (9.62, "crest_db"), (128.0, "bpm_folded_or_raw"), (0.782, "bpm_conf")],
    "We Are Your Friends - Justice Vs Simian_spotdown.org.mp3": [(-7.48, "rms_dbfs"), (7.48, "crest_db")],
    "& Down_spotdown.org.mp3": [(-9.87, "rms_dbfs"), (0.3837, "low_ratio")],
    "Time To Dance - SebastiAn Remix_spotdown.org.mp3": [(-11.21, "rms_dbfs"), (0.6208, "low_share"), (0.1620, "zcr_norm")],
}
adna_by_file = {r["file"]: r for r in adna}
sprof_by_file = {r["file"]: r for r in sprof}
num_report = []
num_bad = []
for f, vals in cited.items():
    a = adna_by_file.get(f)
    s = sprof_by_file.get(f)
    if a is None and s is None:
        num_bad.append(f + ": not in any landed source")
        continue
    for v, kind in vals:
        ok = False
        src = ""
        if a is not None:
            if kind == "rms_dbfs":
                ok, src = abs(a["rms_dbfs"] - v) <= 0.011, "audio_dna.json"
            elif kind == "crest_db":
                ok, src = abs(a["crest_db"] - v) <= 0.011, "audio_dna.json"
            elif kind == "zcr_hz":
                ok, src = abs(a["zcr_hz"] - v) <= 0.11, "audio_dna.json"
            elif kind == "low_ratio":
                ok, src = abs(a["low_ratio"] - v) <= 0.0011, "audio_dna.json"
            elif kind == "bpm_conf":
                ok, src = abs(a["bpm_conf"] - v) <= 0.0011, "audio_dna.json"
            elif kind == "bpm_folded_or_raw":
                b = a["bpm"]
                ok, src = abs(b - v) <= 0.11 or abs(b * 2 - v) <= 0.11, "audio_dna.json"
        if not ok and s is not None:
            if kind == "rms_dbfs":
                ok, src = abs(s["rms_dbfs"] - v) <= 0.011, "style-synthesis.profile.json"
            elif kind == "bpm_folded_or_raw":
                ok, src = abs(s["bpm"] - v) <= 0.11, "style-synthesis.profile.json"
            elif kind == "low_share":
                ok, src = abs(s["low_share"] - v) <= 0.0011, "style-synthesis.profile.json"
            elif kind == "zcr_norm":
                ok, src = abs(s["zcr"] - v) <= 0.0011, "style-synthesis.profile.json"
        tag = "PASS" if ok else "FAIL"
        num_report.append("%s %s %s=%s src=%s" % (tag, f[:44], kind, v, src))
        if not ok:
            num_bad.append("%s %s=%s" % (f[:44], kind, v))
for line in num_report:
    print("  " + line)
check("6 cited-numbers-match-sources", not num_bad, "bad=%s" % (num_bad or "none"))

# 7. subset medians recompute
pat = ["mstrkrft", "soulwax", "boys noize", "sebastian", "digitalism", "justice"]
sub = [r for r in adna if any(p in r["artist"].lower() for p in pat)]
def med(key, xform=lambda v: v):
    return round(statistics.median(xform(r[key]) for r in sub), 2)
got = {
    "rms -11.32 dBFS": med("rms_dbfs") == -11.32,
    "crest 11.32 dB": med("crest_db") == 11.32,
    "zcr 1693.1": round(statistics.median(r["zcr_hz"] for r in sub), 1) == 1693.1,
    "low 0.5941": round(statistics.median(r["low_ratio"] for r in sub), 4) == 0.5941,
    "bpm_folded 127.0": med("bpm", lambda v: v * 2 if v < 90 else v) == 127.0,
    "n=9": len(sub) == 9,
}
check("7 subset-medians-recompute", all(got.values()),
      "n=%d %s" % (len(sub), {k: v for k, v in got.items()}))

# 8. prior cuts claim
suno_files = set(os.listdir(SUNO))
need = {"aerodynamic.mp3", "dance.mp3", "flat_beat.mp3", "genesis.mp3"}
check("8 prior-suno-cuts-exist", need <= suno_files,
      "found=%s" % sorted(need & suno_files))

print("")
print("TOTAL: %d checks, %d failed" % (10 + len(num_report), len(fails)))
sys.exit(1 if fails else 0)
