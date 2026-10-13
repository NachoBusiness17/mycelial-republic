"""termlink2 harvest: Marathon Infinity (m3) chapters from marathon.bungie.org/story.
Adapted from harvest_marathon.py (same parser, same domain lock, same politeness).
One .txt per INFINITY CHAPTER (Despair/Rage/Envy), each containing its level pages.
Infinity Prologue "Ne Cede Malis" = the M2 level page already held at m2/necedemalis.txt
(no re-fetch). Domain-locked to marathon.bungie.org (NETWORK LAW 09-06), ~1 req/sec."""
import sys, time, os
from harvest_marathon import fetch, parse_chapter, OUT

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(_HERE))  # local_sovereign_agent/ (OUT is ROOT-relative)
CACHE = os.path.join(_HERE, "_m3_page_cache")
os.makedirs(CACHE, exist_ok=True)
os.makedirs(os.path.join(ROOT, OUT, "m3"), exist_ok=True)

def fetch_cached(slug_html):
    """fetch() + on-disk cache so a mid-run failure never wastes politeness pages.
    Retries with backoff on transient resets."""
    cache_path = os.path.join(CACHE, slug_html.replace("/", "_"))
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            return f.read()
    last = None
    for attempt, delay in enumerate((1, 10, 30), 1):
        try:
            _, doc = fetch(slug_html)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(doc)
            return doc
        except Exception as e:  # noqa: BLE001 — log, back off, retry
            last = e
            print(f"  ! fetch {slug_html} attempt {attempt} failed: {e}; backing off {delay}s")
            time.sleep(delay)
    raise last

# (chapter_file, chapter_label, [(slug, level_label), ...])  -- order = archive order
M3 = [
    ("despair", "Despair", [
        ("riserobotrise", "Rise Robot Rise"),
        ("robotworldarena", "Robot World Arena"),
        ("pooryorick", "Poor Yorick"),
        ("twofortheprice", "Two for the Price of One"),
        ("confounddelivery", "Confound Delivery"),
        ("electricsheep1", "Electric Sheep One"),
        ("wherearemonsters", "Where are monsters in dreams"),
        ("aiemaksicur", "Aie Mak Sicur"),
    ]),
    ("rage", "Rage", [
        ("acmestation", "Acme Station"),
        ("postnavaltrauma", "Post Naval Trauma"),
        ("thingwhatkicks", "Thing What Kicks. . ."),
        ("wheresome", "Where Some Rarely Go"),
        ("electricsheep2", "Electric Sheep Two"),
        ("whateveryouplease", "Whatever You Please"),
        ("carrollstreetstation", "Carroll Street Station"),
        ("nawmanhesclose", "Naw Man He's Close"),
        ("foehammer", "Foe Hammer"),
        ("hangbrain", "Hang Brain"),
        ("electricsheep3", "Electric Sheep Three"),
        ("eatthepath", "Eat the Path"),
        ("wormfooddude", "You're Wormfood, Dude"),
    ]),
    ("envy", "Envy", [
        ("bycommittee", "By Committee"),
        ("slimythings", "One thousand thousand slimy things"),
        ("convertedchurch", "A Converted Church in Venice, Italy"),
        ("sonofgrendel", "Son of Grendel"),
        ("strangeaeons", "Strange Aeons"),
        ("baggedagain", "Bagged Again"),
        ("bigtime", "You Think You're Big Time? You're Gonna Die Big Time!"),
        ("ayemaksicur", "Aye Mak Sicur"),
    ]),
]

def main():
    fetched = 0
    receipt = []
    for chapter_file, label, levels in M3:
        parts = [f"ARCHIVE: marathon.bungie.org (fan-maintained; cite on any use)\n"
                 f"CHAPTER: Infinity / {label} (levels listed in archive order)"]
        nterm = 0
        chars_before = 0
        for slug, level_label in levels:
            doc = fetch_cached(slug + ".html")
            url = "https://marathon.bungie.org/story/" + slug + ".html"
            fetched += 1
            parts.append(f"\n\n{'#'*70}\n## LEVEL: {level_label}  [{url}]\n{'#'*70}")
            for title, body in parse_chapter(doc):
                if "(Terminal" in title:
                    nterm += 1
                parts.append(f"\n\n{'='*70}\n### {title}\n{'='*70}\n\n{body}")
            print(f"  {label}/{slug}: {level_label}")
        text = "\n".join(parts)
        path = os.path.join(ROOT, OUT, "m3", chapter_file + ".txt")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        nlevels = len(levels)
        receipt.append(f"m3/{chapter_file}\t{label}\tlevels={nlevels}\tterminals={nterm}\tchars={len(text)}")
        print(f"{chapter_file}: {label:9s} levels={nlevels} terminals={nterm:3d} chars={len(text)}")
    print("TOTAL_PAGES_FETCHED", fetched)
    with open(os.path.join(ROOT, OUT, "_harvest_log.txt"), "a", encoding="utf-8") as f:
        f.write("# m3 (termlink2, Infinity run 2026-09-06)\n")
        for row in receipt:
            f.write(row + "\n")

if __name__ == "__main__":
    sys.exit(main())
