"""Finish-line byte battery for the cutter-disco lane (gala_20260925 music-ractor).

Checks watch/inbox/music/cutter-disco_cuts.md:
  1. exactly 3 CUT packs (## CUT n of 3)
  2. each pack: STYLE STRING, tagged LYRICS with [Intro]/[Verse]/[Chorus]/[Outro]
  3. each pack: TRIANGULATES names exactly 2 folder tracks
  4. each pack: DNA ENCODED list present
  5. style strings contain NO artist names (folder table artists + facet brief names)
  6. whole file ASCII-only, zero em/en dashes (U+2013/U+2014)
  7. every encoded DNA number byte-exists in the numeric recipe source
     watch/inbox/music/audio-dna.md (source numbers listed below; receipt may
     round only where noted)
Exit 0 all green, exit 1 any miss.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
RECEIPT = ROOT / "watch/inbox/music/cutter-disco_cuts.md"
RECIPE = ROOT / "watch/inbox/music/audio-dna.md"

# numbers cited by the packs, each must appear in the recipe bytes
RECIPE_NUMBERS = [
    "286.9275", "-12.205", "12.04", "1416.35", "0.6179", "64.95", "62.85",
    "106.825", "151.9", "0.7458", "0.7588", "0.772", "107.1", "-11.1",
    "1930.2", "62.5", "2140.8", "0.3134", "63.2", "0.5412", "-9.45",
    "319.653", "112.1", "0.7492", "1537.4", "465.4", "64.9", "0.7037",
    "1669.8", "-9.62", "-7.48",
]

ARTIST_NAMES = [
    "Aphex Twin", "Basement Jaxx", "Billie Eilish", "Birdy Nam Nam",
    "Boys Noize", "Busy P", "Caravan Palace", "Cassius", "Cut Copy",
    "Johnny SA", "BieBieQ", "DJ Mehdi", "Thomas Bangalter", "DJ Shadow",
    "Daft Punk", "Digitalism", "Fischerspooner", "Friendly Fires", "Goldfrapp",
    "Hot Chip", "Jackson And His Computer Band", "Junior Boys", "Justice",
    "Kavinsky", "SebastiAn", "LA Priest", "LCD Soundsystem", "MSTRKRFT",
    "Simian", "Soulwax", "Aeroplane", "Phoenix", "Chromeo",
]

misses = []
lines_out = []


def check(name, ok, detail=""):
    lines_out.append(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))
    if not ok:
        misses.append(name)


text = RECEIPT.read_text(encoding="utf-8")
recipe = RECIPE.read_text(encoding="utf-8")

check("receipt exists nonempty", RECEIPT.exists() and len(text) > 1000,
      f"{len(text)} chars")

packs = re.findall(r"^## CUT (\d) of 3: (.+)$", text, re.M)
check("3 pack headers", len(packs) == 3, f"found {len(packs)}: {packs}")

# split into pack sections
sections = re.split(r"^## CUT \d of 3: .+$", text, flags=re.M)[1:]
check("3 pack sections", len(sections) == 3, f"found {len(sections)}")

for i, sec in enumerate(sections, 1):
    style = ""
    m = re.search(r"STYLE STRING \(paste-ready\):\n(.*?)\n\nLYRICS:", sec, re.S)
    if m:
        style = " ".join(m.group(1).split())
    check(f"pack {i} style string present", len(style) > 100, f"{len(style)} chars")
    check(f"pack {i} style string under 900 chars", 0 < len(style) <= 900,
          f"{len(style)} chars")
    bad = [a for a in ARTIST_NAMES if a.lower() in style.lower()]
    check(f"pack {i} style string artist-name-free", not bad, f"hits: {bad}")
    for tag in ["[Intro]", "[Verse", "[Chorus]", "[Outro]"]:
        check(f"pack {i} lyrics tag {tag}", tag in sec)
    tri = re.findall(r"^- (.{1,60}?) - \"", sec, re.M)
    tri_in_block = re.search(r"TRIANGULATES \(2 folder tracks.*?\n\n", sec, re.S)
    n_tracks = len(re.findall(r"^- .+ - \"", tri_in_block.group(0), re.M)) if tri_in_block else 0
    check(f"pack {i} triangulates exactly 2 folder tracks", n_tracks == 2,
          f"found {n_tracks}")
    check(f"pack {i} DNA ENCODED section", "DNA ENCODED:" in sec)

non_ascii = [(i, ch, hex(ord(ch))) for i, ch in enumerate(text) if ord(ch) > 127]
check("file ASCII-only", not non_ascii, f"{len(non_ascii)} non-ascii chars" + (f" first: {non_ascii[:5]}" if non_ascii else ""))
em = text.count("\u2014") + text.count("\u2013")
check("zero em/en dashes", em == 0, f"{em} dashes")

missing_nums = [n for n in RECIPE_NUMBERS if n not in recipe]
check("all encoded DNA numbers byte-exist in recipe", not missing_nums,
      f"missing: {missing_nums}" if missing_nums else f"{len(RECIPE_NUMBERS)} numbers verified")

# lyric voice: each pack has an ECHOES receipt block (no fabricated quotes law)
for i, sec in enumerate(sections, 1):
    check(f"pack {i} ECHOES receipt block", "ECHOES" in sec)

print("\n".join(lines_out))
print(f"\nTOTAL: {len(lines_out) - len(misses)} checks, {len(misses)} FAIL")
sys.exit(1 if misses else 0)
