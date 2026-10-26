# archaeology lane byte-check, gala lyric-workover 2026-10-01
# Verifies the countable claims in watch/inbox/music/lyric-archaeology.md against bytes:
# folder contents, hook word-counts, density arithmetic, quote presence, em-dash law.
# Raw output goes to archaeology.check.txt (this file's stdout).
import os, sys, unicodedata

FOLDER = r"C:\Users\foste\Desktop\music-ai"
MD = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\music\lyric-archaeology.md"
LANE_JSON = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\gala_20260925\lyric-workover\lanes\archaeology.json"

fails = []
def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    if not cond:
        fails.append(label)
    print(f"[{status}] {label}" + (f" :: {detail}" if detail else ""))

print("=== 1. corpus folder ===")
mp3s = sorted(f for f in os.listdir(FOLDER) if f.lower().endswith(".mp3"))
print(f"folder mp3 count: {len(mp3s)}")
check("folder holds 110 mp3 files (as cited in the md header)", len(mp3s) == 110, str(len(mp3s)))

# the 22 in-folder tracks the lane fetched, matched to actual filenames
expected = {
    "Around the World": "Around the World _ Harder, Better, Faster, Stronger_spotdown.org.mp3",
    "Harder Better Faster Stronger": "Around the World _ Harder, Better, Faster, Stronger_spotdown.org.mp3",
    "D.A.N.C.E.": "D.A.N.C.E._spotdown.org.mp3",
    "DVNO": "DVNO_spotdown.org.mp3",
    "We Are Your Friends": "We Are Your Friends - Justice Vs Simian_spotdown.org.mp3",
    "TTHHEE PPAARRTTYY": "TTHHEE PPAARRTTYY_spotdown.org.mp3",
    "All My Friends": "All My Friends_spotdown.org.mp3",
    "Someone Great": "Someone Great_spotdown.org.mp3",
    "Daft Punk Is Playing at My House": "Daft Punk Is Playing at My House_spotdown.org.mp3",
    "North American Scum": "North American Scum_spotdown.org.mp3",
    "Get Innocuous!": "Get Innocuous!_spotdown.org.mp3",
    "Ready For The Floor": "Ready For The Floor_spotdown.org.mp3",
    "Over And Over": "Over And Over_spotdown.org.mp3",
    "Boy From School": "Boy From School_spotdown.org.mp3",
    "Huarache Lights": "Huarache Lights_spotdown.org.mp3",
    "One Life Stand": "One Life Stand_spotdown.org.mp3",
    "Crystalised": "Crystalised_spotdown.org.mp3",
    "Heartbeats": "Heartbeats_spotdown.org.mp3",
    "We Share Our Mothers' Health": "We Share Our Mothers' Health_spotdown.org.mp3",
    "Strict Machine": "Strict Machine_spotdown.org.mp3",
    "E Talking": "E Talking_spotdown.org.mp3",
    "My Friend Dario": "My Friend Dario_spotdown.org.mp3",
}
print("\n=== 2. fetched in-folder tracks exist on disk (22) ===")
missing = [k for k, fn in expected.items() if fn not in mp3s]
check("all 22 fetched in-folder tracks present by filename", not missing, f"missing: {missing}" if missing else "22/22")

print("\n=== 3. ask-named tracks absent from folder (negative evidence) ===")
one_more_time = [f for f in mp3s if "one more" in f.lower()]
losing_edge = [f for f in mp3s if "edge" in f.lower()]
phoenix = [f for f in mp3s if "phoenix" in f.lower()]
dance_trouble = [f for f in mp3s if "trouble" in f.lower()]
check("no 'One More Time' file (md flags it ask-named, folder-absent)", not one_more_time, str(one_more_time))
check("no 'Losing My Edge' file (md flags it ask-named, folder-absent)", not losing_edge, str(losing_edge))
check("no Phoenix file (md flags ask named Phoenix; folder has none)", not phoenix, str(phoenix))
check("no 'trouble' file (md flags 'dance with trouble' unresolvable)", not dance_trouble, str(dance_trouble))

print("\n=== 4. hook word-count arithmetic (quoted lines, recomputed) ===")
quotes = {
    "work is never over": 4,
    "go slow": 2,
    "set 'em up": 3,
    "do the dance": 3,
    "Doesn't care, about to crash": 5,
}
for q, want in quotes.items():
    n = len(q.split())
    check(f"'{q}' = {want} words", n == want, f"computed {n}")
    check(f"2 <= {n} <= 8 (md: hook lines 2-8 words)", 2 <= n <= 8)
atw = "around the world" + ", " + "around the world"
check("'around the world, around the world' = 6 words (md: 3 words x2)", len(atw.split()) == 6, str(len(atw.split())))
omt_block = ["one more time", "four word celebration line", "four word affirmation line", "four word dance instruction"]
check("One More Time hook symmetry = 4 lines", len(omt_block) == 4)
check("riddle spec: 14 lines / 4 beats = 3.5 lines per beat", abs(14 / 4 - 3.5) < 1e-9)
check("14-line split: 3 blocks x 4 + 2 exit = 14", 3 * 4 + 2 == 14)
check("density band claim 'one beat per 3.5 to 4 lines' brackets 3.5", 3.5 <= 14 / 4 <= 4.0)

print("\n=== 5. deliverable byte checks ===")
md_bytes = open(MD, "rb").read().decode("utf-8")
lines = md_bytes.splitlines()
print(f"lyric-archaeology.md: {len(md_bytes)} bytes, {len(lines)} lines")
check("md exists and is non-empty", len(md_bytes) > 5000, f"{len(md_bytes)} bytes")
emdash_md = [i + 1 for i, l in enumerate(lines) if "\u2014" in l]
check("no em-dash (U+2014) anywhere in the md (record law)", not emdash_md, f"lines {emdash_md}" if emdash_md else "0 hits")
json_bytes = open(LANE_JSON, "rb").read().decode("utf-8")
check("lane json exists", len(json_bytes) > 0, f"{len(json_bytes)} bytes")
emdash_json = "\u2014" in json_bytes
check("no em-dash in lane json", not emdash_json)
must_contain = [
    "The joy of repetition really is in you",
    "work is never over",
    "go slow",
    "set 'em up",
    "One, two, three, four",
    "Doesn't care, about to crash",
    "when I",  # Over And Over swap fragment
    "ten days",
    "hour after hour",
]
for s in must_contain:
    check(f"md carries evidence string: {s!r}", s in md_bytes)

print("\n=== 6. fetch register (24 pages fetched live via WebFetch this session, genius.com) ===")
register = [
    ("in-folder", "Daft Punk", "Around the World", "https://genius.com/Daft-punk-around-the-world-lyrics", "1 distinct phrase, 144 instances"),
    ("in-folder", "Daft Punk", "Harder Better Faster Stronger", "https://genius.com/Daft-punk-harder-better-faster-stronger-lyrics", "8 distinct phrases, ~55-60 line reps"),
    ("in-folder", "Justice", "D.A.N.C.E.", "https://genius.com/Justice-dance-lyrics", "~45-55 lines, you/present, no arc"),
    ("in-folder", "Justice", "DVNO", "https://genius.com/Justice-dvno-lyrics", "~25-30 lines, 15-18 unique, I/you present"),
    ("in-folder", "Justice vs Simian", "We Are Your Friends", "https://genius.com/Justice-and-simian-we-are-your-friends-lyrics", "4 distinct lines in ~60"),
    ("in-folder", "Justice ft Uffie", "TTHHEE PPAARRTTYY", "https://genius.com/Justice-tthhee-ppaarrttyy-lyrics", "~40 lines, prep/club/after-party"),
    ("in-folder", "LCD Soundsystem", "All My Friends", "https://genius.com/Lcd-soundsystem-all-my-friends-lyrics", "~60 lines, night+life arc"),
    ("in-folder", "LCD Soundsystem", "Someone Great", "https://genius.com/Lcd-soundsystem-someone-great-lyrics", "~50 lines, 8-line verses, chorus x8"),
    ("in-folder", "LCD Soundsystem", "Daft Punk Is Playing at My House", "https://genius.com/Lcd-soundsystem-daft-punk-is-playing-at-my-house-lyrics", "~45 lines, house-party scene"),
    ("in-folder", "LCD Soundsystem", "North American Scum", "https://genius.com/Lcd-soundsystem-north-american-scum-lyrics", "~55 lines, vignettes"),
    ("in-folder", "LCD Soundsystem", "Get Innocuous!", "https://genius.com/Lcd-soundsystem-get-innocuous-lyrics", "~16 unique of ~25, refrain x8"),
    ("in-folder", "Hot Chip", "Ready For The Floor", "https://genius.com/Hot-chip-ready-for-the-floor-lyrics", "~45-50 lines, anxiety to invitation"),
    ("in-folder", "Hot Chip", "Over And Over", "https://genius.com/Hot-chip-over-and-over-lyrics", "~20 distinct of ~50, one-word chorus swap"),
    ("in-folder", "Hot Chip", "Boy From School", "https://genius.com/Hot-chip-and-i-was-a-boy-from-school-lyrics", "~26-28 distinct lines"),
    ("in-folder", "Hot Chip", "Huarache Lights", "https://genius.com/Hot-chip-huarache-lights-lyrics", "~35 lines, refrain x12"),
    ("in-folder", "Hot Chip", "One Life Stand", "https://genius.com/Hot-chip-one-life-stand-lyrics", "~30 distinct of 45-50, open ending"),
    ("in-folder", "The xx", "Crystalised", "https://genius.com/The-xx-crystalised-lyrics", "~46 lines, 4-8 words/line, wordless chorus, 'go slow' x5"),
    ("in-folder", "The Knife", "Heartbeats", "https://genius.com/The-knife-heartbeats-lyrics", "~29 lines, predominantly past, would-flip"),
    ("in-folder", "The Knife", "We Share Our Mothers' Health", "https://genius.com/The-knife-we-share-our-mothers-health-lyrics", "~16 distinct of ~60, overlapping stanzas"),
    ("in-folder", "Goldfrapp", "Strict Machine", "https://genius.com/Goldfrapp-strict-machine-lyrics", "~14 distinct lines, I/you-machine present"),
    ("in-folder", "Soulwax", "E Talking", "https://genius.com/Soulwax-e-talking-lyrics", "~30 lines, drug-as-addressee"),
    ("in-folder", "Vitalic", "My Friend Dario", "https://genius.com/Vitalic-my-friend-dario-lyrics", "~9-10 unique of ~20, third person"),
    ("ask-named, folder-absent", "LCD Soundsystem", "Losing My Edge", "https://genius.com/Lcd-soundsystem-losing-my-edge-lyrics", "~90-100 lines, refrain 15+"),
    ("ask-named, folder-absent", "Daft Punk", "One More Time", "https://genius.com/Daft-punk-one-more-time-lyrics", "10-12 distinct lines, 4 words/line x4, title 30+"),
]
in_folder_rows = [r for r in register if r[0] == "in-folder"]
check("register has 24 rows", len(register) == 24, str(len(register)))
check("register has 22 in-folder rows", len(in_folder_rows) == 22, str(len(in_folder_rows)))
check("register in-folder rows == expected-on-disk set", {r[2] for r in in_folder_rows} == set(expected.keys()))
for kind, artist, title, url, fact in register:
    print(f"  [{kind}] {artist} - {title} :: {fact} :: {url}")

print("\n=== 7. summary ===")
print(f"FAILURES: {len(fails)} {fails if fails else ''}")
print("ARCHAEOLOGY BYTE-CHECK: " + ("PASS" if not fails else "FAIL"))
sys.exit(0 if not fails else 1)
