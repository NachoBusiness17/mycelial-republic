"""music_cut_gate.py: form-law gate for music-cut standing-workflow CUT packs.

The pack format is the one the Seed Saver proved 2026-10-02
(watch/inbox/music/CUT_SEED_SAVER.md: parable + alliteration + playful, Suno
paste-ready) with the DNA/TRIANGULATES section The Hum carried. A pack that
fails shape is not paste-ready; this gate is the workflow's deterministic
verdict, same exit-code-is-the-verdict discipline as the vonnegut form gate.

Per pack, checked:
  1. header       first pack line matches: # CUT: "<title>"
  2. style-block  a "## STYLE" section holds a non-empty fenced block containing BPM
  3. lyrics-block a "## LYRICS" section holds a fenced block with a [Verse] tag and
                  a hook-class tag ([Chorus]/[Hook]/[Drop]/[Pre-Chorus]; the Drop-form
                  CUT THE HUM pack is the precedent that [Chorus] is not the only hook)
  4. layers       a LAYERS section names Surface, Layer 2 and Layer 3
  5. alliteration an ALLITERATION section exists and is non-empty
  6. dna          a TRIANGULATES or DNA section exists (numbers land somewhere)
  7. ascii        pack is pure ASCII
  8. dashes       no em-dash or en-dash anywhere in the pack

Usage:
  python tools/music_cut_gate.py pack1.md [pack2.md ...] [--expect N]

Output: [PASS]/[FAIL] lines, "FAILURES: N", "MUSIC CUT FORM GATE: PASS|FAIL",
"EXIT_CODE=N". Exit 0 = all packs pass, 1 = any FAIL, 2 = usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADER_RE = re.compile(r'^# CUT:\s*"')


def split_packs(text: str) -> list:
    lines = text.splitlines()
    packs = []
    current = None
    for line in lines:
        if line.startswith("# CUT:"):
            if current is not None:
                packs.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
    if current is not None:
        packs.append(current)
    return ["\n".join(p) for p in packs]


def section(pack: str, keyword: str) -> str:
    """Return the text between the first heading containing keyword and the next ## heading."""
    lines = pack.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("##") and keyword.upper() in line.upper():
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def fenced_block(section_text: str) -> str:
    """Return the content of the first fenced ``` block in the section text."""
    lines = section_text.splitlines()
    inside = False
    buf = []
    for line in lines:
        stripped = line.strip()
        if not inside and stripped.startswith("```"):
            inside = True
            continue
        if inside and stripped.startswith("```"):
            break
        if inside:
            buf.append(line)
    return "\n".join(buf).strip()


def gate_pack(pack: str, label: str) -> list:
    results = []

    def check(name: str, ok: bool, detail: str = ""):
        results.append((name, bool(ok), detail))

    lines = [ln for ln in pack.splitlines() if ln.strip()]
    check("header", bool(lines) and bool(HEADER_RE.match(lines[0])),
          "first line: " + (lines[0][:70] if lines else "<empty pack>"))

    style_sec = section(pack, "STYLE")
    style_block = fenced_block(style_sec)
    check("style-block", bool(style_block) and "BPM" in style_block.upper(),
          "style block chars: %d, BPM named: %s" % (len(style_block), "BPM" in style_block.upper()))

    lyrics_sec = section(pack, "LYRICS")
    lyrics_block = fenced_block(lyrics_sec)
    upper = lyrics_block.upper()
    has_verse = "[VERSE" in upper
    has_hook = any(tag in upper for tag in ("[CHORUS", "[HOOK", "[DROP", "[PRE-CHORUS"))
    check("lyrics-block", len(lyrics_block) >= 200 and has_verse and has_hook,
          "lyrics chars: %d, verse tag: %s, hook-class tag: %s" % (len(lyrics_block), has_verse, has_hook))

    layers_sec = section(pack, "LAYERS")
    has_layers = ("Surface" in layers_sec and "Layer 2" in layers_sec and "Layer 3" in layers_sec)
    check("layers", bool(layers_sec.strip()) and has_layers,
          "Surface/Layer 2/Layer 3 present: %s" % has_layers)

    allit_sec = section(pack, "ALLITERATION")
    check("alliteration", len(allit_sec.strip()) >= 40,
          "alliteration section chars: %d" % len(allit_sec.strip()))

    dna_sec = section(pack, "TRIANGULATES") or section(pack, "DNA")
    check("dna", len(dna_sec.strip()) >= 30,
          "triangulates/dna section chars: %d" % len(dna_sec.strip()))

    non_ascii = [ch for ch in pack if ord(ch) > 127]
    check("ascii", not non_ascii, "non-ascii chars: %d %s" % (len(non_ascii), repr(non_ascii[:5])))

    dashes = pack.count("\u2014") + pack.count("\u2013")
    check("dashes", dashes == 0, "em/en dash count: %d" % dashes)

    return [(label + ":" + name, ok, detail) for (name, ok, detail) in results]


def main() -> int:
    ap = argparse.ArgumentParser(description="Form-law gate for music-cut CUT packs (Seed Saver format)")
    ap.add_argument("packs", nargs="+", help="pack .md files to gate")
    ap.add_argument("--expect", type=int, default=None, help="fail if pack count differs")
    args = ap.parse_args()

    all_results = []
    texts = []
    for p in args.packs:
        path = Path(p)
        if not path.is_file():
            print("[FAIL] %s:file-missing (no such file)" % str(path))
            return 2
        texts.append(path.read_text(encoding="utf-8"))

    packs = []
    for path, text in zip(args.packs, texts):
        got = split_packs(text)
        if not got:
            print("[FAIL] %s:no-packs (no '# CUT:' header found)" % path)
            return 2
        for k, pack in enumerate(got, 1):
            packs.append(pack)
            all_results.extend(gate_pack(pack, "%s#%d" % (Path(path).name, k)))

    if args.expect is not None and len(packs) != args.expect:
        print("[FAIL] pack-count: expected %d, found %d" % (args.expect, len(packs)))
        all_results.append(("pack-count", False, "%d != %d" % (len(packs), args.expect)))

    failures = 0
    for name, ok, detail in all_results:
        print(("[PASS] " if ok else "[FAIL] ") + name + (" - " + detail if detail else ""))
        if not ok:
            failures += 1

    print("PACKS: %d" % len(packs))
    print("FAILURES: %d" % failures)
    verdict = "PASS" if failures == 0 else "FAIL"
    print("MUSIC CUT FORM GATE: %s" % verdict)
    print("EXIT_CODE=%d" % (0 if failures == 0 else 1))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
