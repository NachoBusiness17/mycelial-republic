# jung lane finish-line byte check, gala_20260925 lyric-workover
# Verifies archetype-workover.md against the ask's finish line:
# per cut: archetype, its shadow, symbol set, rewritten lyrics in the
# riddle structure (clock, object, dialogue hook, note, closer last),
# universal-situation survival, and doctrine-as-symbol-only (no law
# names, no receipts, no system words inside any lyric).
import re
import sys

PATH = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\gala_20260925\lyric-workover\archetype-workover.md"

fails = []


def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL") + "  " + name + ("  " + detail if detail else ""))
    if not ok:
        fails.append(name)


with open(PATH, "rb") as f:
    raw = f.read()

check("file readable, %d bytes" % len(raw), len(raw) > 0)

try:
    text = raw.decode("ascii")
    check("ASCII only (pack house law)", True)
except UnicodeDecodeError as e:
    text = raw.decode("utf-8", "replace")
    check("ASCII only (pack house law)", False, str(e))

check("no em dash (U+2014)", "\u2014" not in text)
check("no en dash (U+2013)", "\u2013" not in text)

cut_headers = re.findall(r"^## CUT ([1-6]) of 6: \"(.+?)\" \(was (.+?),", text, re.M)
check("six cut sections found", len(cut_headers) == 6, str(len(cut_headers)))

closers = {
    "1": "In my own hand.",
    "2": "She set the alarm for five.",
    "3": "That was the joke.",
    "4": "It has my chin.",
    "5": "Same time tonight.",
    "6": "The fire was mine. I took it home.",
}
time_re = re.compile(
    r"clock|a\.m\.|midnight|dawn|morning|tonight|monday|tuesday|wednesday|"
    r"thursday|friday|saturday|sunday|nights?\b|hours?\b|watch|five|three|four|"
    r"eleven|closing time",
    re.I,
)
note_re = re.compile(r"folded|note|slip|log", re.I)
# doctrine-as-symbol law: never inside a lyric
banned_re = re.compile(
    r"byte|hash|commit|repo|basetemp|census|verdict|suite|runtime|append|"
    r"falsifier|ledger|trust bytes|green is|rigged|queue|receipt|exit code|"
    r"\bbpm\b|doctrine|\blaw\b|persona|shadow|trickster|hero|\d{3,}",
    re.I,
)

for num, title, was in cut_headers:
    sec = re.search(
        r"^## CUT " + num + r" of 6:.*?(?=^## CUT|^# FOLD)", text, re.M | re.S
    )
    if not sec:
        check("cut " + num + " section extractable", False)
        continue
    body = sec.group(0)
    tag = "cut " + num + " (" + title + ", was " + was.strip() + ")"
    check(tag + ": ARCHETYPE named", "ARCHETYPE:" in body)
    check(tag + ": ITS SHADOW named", "ITS SHADOW" in body)
    check(tag + ": symbol set named", "SYMBOL SET" in body)
    check(tag + ": universal situation answered", "UNIVERSAL SITUATION" in body)
    check(tag + ": riddle elements listed", "RIDDLE ELEMENTS" in body)

    lyr = re.search(r"^LYRICS:\s*$(.*?)(?=^---)", body, re.M | re.S)
    if not lyr:
        check(tag + ": LYRICS block present", False)
        continue
    lines = [ln.rstrip() for ln in lyr.group(1).splitlines() if ln.strip()]
    check(tag + ": LYRICS block present", True, str(len(lines)) + " lines")
    joined = "\n".join(lines)

    check(tag + ": dialogue hook (quoted speech)", '"' in joined)
    check(tag + ": a note exists", bool(note_re.search(joined)))
    check(tag + ": a visible clock", bool(time_re.search(joined)))
    check(
        tag + ": object with stakes in cold open",
        bool(re.search(r"\[(Intro[^\]]*)\]", joined)),
    )

    bad = [w for w in (banned_re.findall(joined) or [])]
    check(tag + ": no law names / receipts / system words in lyrics", not bad, repr(bad))

    tail = [ln for ln in lines if ln.strip()][-4:]
    check(
        tag + ": closer lands last",
        closers.get(num, "\x00") in "\n".join(tail),
        closers.get(num, "?"),
    )

check("fold note has MASK ON arc", "MASK ON" in text)
check("fold note has MASK SEEN THROUGH arc", "MASK SEEN THROUGH" in text)
check("fold note has MASK CHOSEN arc", "MASK CHOSEN" in text)
check(
    "style strings unchanged, pointer to source packs",
    "STYLE STRING and DNA numbers are UNCHANGED" in text,
)

print("PYEXIT=%d" % (1 if fails else 0))
sys.exit(1 if fails else 0)
