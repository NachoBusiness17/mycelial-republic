# vonnegut lane form-law gate, gala vonnegut-final 2026-10-01
# Verifies watch/inbox/gala_20260925/vonnegut-final/vonnegut-final-cuts.md
# against the resolved form: 14-line riddle, loop lines at 2/6/10, one-word
# reversal at line 10, two-line dialogue hook repeated three times, closer
# lands last (1-4 words), line-length bands, one past-tense line max,
# system-word ban inside lyrics, ASCII only / no em or en dashes, and
# byte-identity of every style string against its source pack.
# Raw output: vonnegut.check.txt (this file's stdout). Verdict = exit code.
import re, sys

BASE = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\gala_20260925\vonnegut-final"
MD = BASE + r"\vonnegut-final-cuts.md"
DISCO = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\music\cutter-disco_cuts.md"
ELECTRO = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\music\cutter-electro_cuts.md"

fails = []
def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    if not cond:
        fails.append(label)
    print(f"[{status}] {label}" + (f" :: {detail}" if detail else ""))

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

raw = open(MD, "rb").read().decode("utf-8")
print("=== 1. file-level laws ===")
lines_all = raw.splitlines()
print(f"vonnegut-final-cuts.md: {len(raw)} bytes, {len(lines_all)} lines")
check("deliverable is non-empty", len(raw) > 10000, f"{len(raw)} bytes")
check("no em dash (U+2014) anywhere in the file", "\u2014" not in raw)
check("no en dash (U+2013) anywhere in the file", "\u2013" not in raw)
non_ascii = sorted({c for c in raw if ord(c) > 127})
check("ASCII only (no codepoints above 127)", not non_ascii, repr(non_ascii) if non_ascii else "clean")

sections = re.split(r"\n## CUT ", raw)[1:]
check("file holds 6 CUT sections", len(sections) == 6, str(len(sections)))

# per-cut expected facts: (object in line 1, clock token in beats 1-2,
# loop mutation pair, source file, style substring key)
CUTS = [
    ("SIGN FOR IT",   "bag",   "a.m.",    ("bag", "man"),     DISCO,   "filtered disco funk, chopped disco strings"),
    ("THE LEASE",     "key",   "dawn",    ("alone", "again"), DISCO,   "half-time disco strut, filtered synth-pop"),
    ("LAST HAND",     "chip",  "a.m.",    ("in", "out"),      DISCO,   "punk-funk disco, wah-wah filtered guitar loops"),
    ("SEVEN COATS",   "coats", "Tuesday", ("hallway", "cellar"), ELECTRO, "Dark electro-house, 126 BPM"),
    ("THE NIGHT WATCH", "needle", "Tuesday", ("oil", "climb"), ELECTRO, "Maximal electro-rock, 124 BPM"),
    ("NO CLOCKS IN HERE", "clocks", "nights", ("keeps", "is"), ELECTRO, "Dark electro-funk, 122 BPM"),
]

PAST = {"came","said","was","were","went","took","died","slept","wore","broke",
        "pulled","gave","got","made","had","told","kept","left","sold","bought",
        "hung","rang","sat","stood","found","lost","won"}
BANNED = ["bytes","hash","verdict","suite","commit","census","ledger","repo",
          "lane","invariant","entropy","denominator","basetemp","receipt",
          "doctrine","falsifier","rigged","smirk","casino","exit code",
          "trust bytes","green is","2,568","thirteen mirrors"]

disco_bytes = open(DISCO, "rb").read().decode("utf-8")
electro_bytes = open(ELECTRO, "rb").read().decode("utf-8")

print("\n=== 2. per-cut form law ===")
for idx, (section, (name, obj, clock, (w_from, w_to), src, style_key)) in enumerate(zip(sections, CUTS), start=1):
    print(f"\n--- CUT {idx}: {name} ---")
    fences = re.findall(r"```(.*?)```", section, re.S)
    check(f"{name}: exactly 2 fenced blocks (style, lyrics)", len(fences) == 2, f"{len(fences)} fences")
    if len(fences) != 2:
        continue
    style_block, lyrics_block = fences
    src_bytes = disco_bytes if src == DISCO else electro_bytes
    check(f"{name}: style string byte-identical (modulo wrapping) to source pack",
          norm(style_block) in norm(src_bytes),
          "found" if norm(style_block) in norm(src_bytes) else "NOT FOUND in source")
    check(f"{name}: style string opens with the source pack's facet lead",
          norm(style_block).startswith(style_key))

    # lyric content lines: drop tags and blanks
    lyric_lines = [l.strip() for l in lyrics_block.splitlines()
                   if l.strip() and not l.strip().startswith("[")]
    n = len(lyric_lines)
    check(f"{name}: exactly 14 content lines", n == 14, str(n))
    if n != 14:
        for i, l in enumerate(lyric_lines, 1):
            print(f"    {i:2d}: {l}")
        continue

    words = [l.split() for l in lyric_lines]
    wc = [len(w) for w in words]

    # line-length bands: verse/bridge lines 4-8; hook lines 2-6.
    # Fix receipt (2026-10-01): first run FAILED cut 5 here because line 14
    # (the exit line) was forced into the 4-8 band; the exit line's own law
    # is 1-4 words (enforced by the dedicated exit check below), so it is
    # exempt from this band. Evidence: vonnegut.check.txt first run, FAIL
    # row "THE NIGHT WATCH: line-length bands", (14, 3) for 'Same time
    # tonight.' which passed the 1-4 exit law.
    hook_pos = {3, 4, 7, 8, 11, 12}
    band_ok = all(
        (2 <= wc[i-1] <= 6) if i in hook_pos else (4 <= wc[i-1] <= 8)
        for i in range(1, 14)
    )
    check(f"{name}: line-length bands (hooks 2-6, others 4-8 words)", band_ok,
          str(list(zip(range(1, 15), wc))))

    # loop law: lines 2 and 6 identical; line 10 differs by exactly one word
    check(f"{name}: line 2 == line 6 (the loop)", lyric_lines[1] == lyric_lines[5],
          f"{lyric_lines[1]!r} vs {lyric_lines[5]!r}")
    l2, l10 = words[1], words[9]
    same_len = len(l2) == len(l10)
    diffs = [i for i, (a, b) in enumerate(zip(l2, l10)) if a != b] if same_len else list(range(max(len(l2), len(l10))))
    check(f"{name}: line 10 same word count as line 2", same_len, f"{len(l2)} vs {len(l10)}")
    check(f"{name}: reversal at line 10 is exactly ONE mutated word", len(diffs) == 1,
          f"{len(diffs)} diffs")
    if len(diffs) == 1:
        got_from, got_to = l2[diffs[0]].strip(".,!?\"'"), l10[diffs[0]].strip(".,!?\"'")
        check(f"{name}: mutated word is the named turn {w_from} -> {w_to}",
              got_from == w_from and got_to == w_to, f"{got_from} -> {got_to}")

    # chorus law: two-line dialogue hook, identical three times
    check(f"{name}: chorus line 1 identical at 3/7/11",
          lyric_lines[2] == lyric_lines[6] == lyric_lines[10])
    check(f"{name}: chorus line 2 identical at 4/8/12",
          lyric_lines[3] == lyric_lines[7] == lyric_lines[11])
    hook_text = lyric_lines[2] + " " + lyric_lines[3]
    check(f"{name}: hook is dialogue (ASCII straight quotes present)",
          '"' in lyric_lines[2] and '"' in lyric_lines[3], hook_text)

    # closer lands last: exit line 1-4 words; end is a beginning-adjacent short line
    check(f"{name}: exit line (14) is 1-4 words", 1 <= wc[13] <= 4, f"{wc[13]} words: {lyric_lines[13]!r}")

    # stakes object staged flat in beat 1 (line 1)
    check(f"{name}: stakes object {obj!r} staged in line 1", obj in lyric_lines[0],
          lyric_lines[0])

    # clock visible in beats 1-2 (lines 1-8)
    clock_hit = [i for i in range(1, 9) if clock in lyric_lines[i-1]]
    check(f"{name}: clock token {clock!r} visible in beats 1-2", bool(clock_hit),
          f"lines {clock_hit}" if clock_hit else "none")

    # tense: at most one past-tense line (the flashback stamp)
    past_lines = [i for i in range(1, 15)
                  for tok in re.findall(r"[A-Za-z']+", lyric_lines[i-1])
                  if tok.lower() in PAST]
    past_lines = sorted(set(past_lines))
    check(f"{name}: at most ONE past-tense line (flashback stamp)", len(past_lines) <= 1,
          f"lines {past_lines}" if past_lines else "all present")

    # system-word ban inside lyrics
    low = " ".join(lyric_lines).lower()
    hits = [b for b in BANNED if b in low]
    check(f"{name}: no system words / doctrine names / receipts in lyrics", not hits,
          f"hits {hits}" if hits else "clean")

print("\n=== 3. summary ===")
print(f"FAILURES: {len(fails)} {fails if fails else ''}")
print("VONNEGUT FORM-LAW GATE: " + ("PASS" if not fails else "FAIL"))
sys.exit(0 if not fails else 1)
