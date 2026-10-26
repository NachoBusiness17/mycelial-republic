"""Marathon terminal voice metrics: the Rampancy Wire probe.

Turns the Marathon trilogy terminal corpus
(research/gaming_corpus/marathon_terminals/m1|m2|m3/*.txt, one file per
chapter, sections delimited by lines starting "### ") into measured probe
features: first-person-singular density per 1000 words, garbled burst token
density per 1000 words, word count, and terminal section count, per chapter
file, per game, and for the trilogy.

CONSUMER: the geometric probe feature rows (emitted JSON lands at
state/probe_features/marathon_rampancy.json and feeds geometric proximity
probes) and the persona palace spec
(watch/inbox/DURANDAL_PALACE_ROW_SPEC_20261019.md, the Durandal salon-lens
chair that reads inputs through the rampancy-stage lens).

VERIFIER: the emitted JSON itself (state/probe_features/marathon_rampancy.json,
reloadable and self-describing) plus tests/test_marathon_voice_metrics.py,
which pins the token heuristic, the per-1000 math on a tiny synthetic text,
the arc labels, and JSON loadability.

Heuristic: FIRST-PERSON-SINGULAR
    Regex \\b(i'm|i'll|i've|mine|i|me|my)\\b, case-insensitive (longest
    alternations first so "I'm" is counted once, not as "I" + "I'm").
    Contractions outside the listed set (e.g. "I'd") contribute through their
    "I" stem: a plain word-boundary match of "I" succeeds inside "I'd".

Heuristic: WORD COUNT
    A word is a maximal run of ASCII letters with optional internal
    apostrophes ([A-Za-z]+(?:'[A-Za-z]+)*). Timestamps, IP fragments and pure
    digit runs contribute zero words; garble that carries letters counts,
    because garble is part of the voice being measured.

Heuristic: GARBLED BURST TOKENS (the "^9320wrefkddud" class)
    Tokens are maximal [a-z0-9]+ runs of the lowercased text. A token is a
    garbled burst token when ANY of:
      A. mixed alnum: it has >=1 digit AND >=5 letters
         (catches 9320wrefkddud, 9034thssksbvs, 9066hhhthsrls, and the
         m3 burst class 99102hngbrncztscl / 19201facltebicubcc);
      B. consonant wall: no digits, >=6 letters, total vowels (aeiou)
         <=1, and the longest run of consecutive non-vowel letters >=6,
         where "y" breaks runs (treated as a vowel) so "systems" and
         "standby" stay clean (catches hhhthsrls, thssksbvs);
      C. doubled-consonant garble: no digits, >=8 letters, total vowels
         (aeiou) <=2, AND some consonant run of length >=4 that itself
         contains a doubled pair (catches wrefkddud bare: its "fkdd"
         run carries the "dd"; attempts/worthless/resupply stay clean
         because their doubles sit in separate runs of 2-3).
    Known false-positive classes, accepted and documented: archive
    fan-credit handles in thanks lines (Callie21V, sinclair123) that rule
    A cannot tell from garble, and archive hex/UI remnants (ebhilite7f
    class; the m2 ones are in-fiction Durandal screen dumps and count as
    garble honestly). Deliberately NOT flagged: hex ids with few
    letters (a94f12), pure digit runs (binary noise, timestamps), 2-letter
    callsigns (vt920), canon alien names (W'rkncacnter's letter-runs carry
    no doubled consonants and 2+ vowels), and consonant-cluster English
    (strengths, postscript, construct clear every wall).

Heuristic: TERMINAL COUNT
    A terminal is a "### " section whose title contains "(Terminal"
    (case-insensitive). Navigation stubs ("Go Back to Marathon's Story
    Home Page", "Go Next Chapter ...") and the bare "### " separator line
    are excluded.

Properties: deterministic (no clock, no randomness, no network), stdlib only.
Corpus credit law: marathon.bungie.org (fan-maintained archive; cite on any
use) - the source field of every emitted record carries it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = REPO_ROOT / "research" / "gaming_corpus" / "marathon_terminals"
DEFAULT_OUT = REPO_ROOT / "state" / "probe_features" / "marathon_rampancy.json"

SOURCE_CREDIT = (
    "marathon.bungie.org (fan-maintained Marathon terminal archive; "
    "cite on any use)"
)

# INDEX.md-anchored arc labels, one per game (applies to every chapter file
# of that game).
ARC_LABELS = {
    "m1": "Melancholy onset",
    "m2": "peak rampancy",
    "m3": "dissolution",
}

GAME_NAMES = {
    "m1": "Marathon",
    "m2": "Marathon 2: Durandal",
    "m3": "Marathon Infinity",
}

GAMES = ("m1", "m2", "m3")

FP_RE = re.compile(r"\b(?:i'm|i'll|i've|mine|i|me|my)\b", re.IGNORECASE)
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*")
TOKEN_RE = re.compile(r"[a-z0-9]+")
SECTION_TITLE_RE = re.compile(r"^###\s+(.*)$", re.MULTILINE)

VOWELS = frozenset("aeiou")
VOWELS_AND_Y = frozenset("aeiouy")


def _longest_consonant_run(letters: str) -> int:
    """Longest run of consecutive letters that are not in aeiou (y breaks
    the run: it behaves as a vowel in English clusters like "systems")."""
    best = run = 0
    for ch in letters:
        if ch not in VOWELS_AND_Y:
            run += 1
            if run > best:
                best = run
        else:
            run = 0
    return best


def _has_run_with_double(letters: str) -> bool:
    """True when some non-vowel run of length >=4 contains a doubled pair
    (the "fkdd" shape of wrefkddud; attempts' "tt" lives in a run of 2)."""
    run = 0
    prev = ""
    for ch in letters:
        if ch in VOWELS_AND_Y:
            run = 0
            prev = ""
            continue
        run += 1
        if ch == prev and run >= 4:
            return True
        prev = ch
    return False


def is_garbled_burst(token: str) -> bool:
    """Return True when a lowercased [a-z0-9]+ token matches the garbled
    burst heuristic (exact rules in the module docstring)."""
    letters = [c for c in token if c.isalpha()]
    digits = [c for c in token if c.isdigit()]
    n_letters = len(letters)
    n_digits = len(digits)
    if n_letters == 0:
        return False
    # Rule A: mixed alnum.
    if n_digits >= 1 and n_letters >= 5:
        return True
    if n_digits:
        return False
    joined = "".join(letters)
    n_vowels = sum(1 for c in letters if c in VOWELS)
    run = _longest_consonant_run(joined)
    # Rule B: consonant wall.
    if n_letters >= 6 and n_vowels <= 1 and run >= 6:
        return True
    # Rule C: doubled-consonant garble.
    if n_letters >= 8 and n_vowels <= 2 and _has_run_with_double(joined):
        return True
    return False


def first_person_count(text: str) -> int:
    return len(FP_RE.findall(text))


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def garbled_burst_count(text: str) -> int:
    return sum(1 for tok in TOKEN_RE.findall(text.lower()) if is_garbled_burst(tok))


def terminal_count(text: str) -> int:
    titles = SECTION_TITLE_RE.findall(text)
    return sum(1 for t in titles if "(terminal" in t.lower())


def _per_1000(count: int, words: int) -> float:
    if words <= 0:
        return 0.0
    return round(count / words * 1000.0, 2)


def metrics_for_text(text: str) -> dict:
    words = word_count(text)
    fp = first_person_count(text)
    garbled = garbled_burst_count(text)
    return {
        "terminal_count": terminal_count(text),
        "word_count": words,
        "first_person_singular": fp,
        "first_person_per_1000": _per_1000(fp, words),
        "garbled_burst_tokens": garbled,
        "garbled_per_1000": _per_1000(garbled, words),
    }


def metrics_for_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    return metrics_for_text(text)


def _rollup(rows: list) -> dict:
    words = sum(r["word_count"] for r in rows)
    fp = sum(r["first_person_singular"] for r in rows)
    garbled = sum(r["garbled_burst_tokens"] for r in rows)
    return {
        "terminal_count": sum(r["terminal_count"] for r in rows),
        "word_count": words,
        "first_person_singular": fp,
        "first_person_per_1000": _per_1000(fp, words),
        "garbled_burst_tokens": garbled,
        "garbled_per_1000": _per_1000(garbled, words),
    }


def compute_for_corpus(corpus_dir: Path) -> dict:
    """Measure every chapter file under corpus_dir/m1|m2|m3/*.txt (sorted),
    roll up per game and for the trilogy."""
    chapters = []
    games = {}
    for game in GAMES:
        game_dir = corpus_dir / game
        files = sorted(game_dir.glob("*.txt")) if game_dir.is_dir() else []
        rows = []
        for path in files:
            row = {"file": f"{game}/{path.name}", "game": game}
            row.update(metrics_for_file(path))
            row["arc_label"] = ARC_LABELS[game]
            rows.append(row)
        chapters.extend(rows)
        if rows:
            game_row = _rollup(rows)
            game_row.update(
                {
                    "game": game,
                    "game_name": GAME_NAMES[game],
                    "arc_label": ARC_LABELS[game],
                    "chapter_files": [r["file"] for r in rows],
                    # audit sample: first unique garbled tokens, sorted,
                    # capped so the JSON stays a feature row not a dump
                    "garbled_examples": sorted(
                        {
                            tok
                            for path in files
                            for tok in TOKEN_RE.findall(
                                path.read_text(encoding="utf-8", errors="replace").lower()
                            )
                            if is_garbled_burst(tok)
                        }
                    )[:5],
                }
            )
            games[game] = game_row
    trilogy = _rollup(chapters)
    return {
        "source": SOURCE_CREDIT,
        "instrument": "tools/marathon_voice_metrics.py",
        "arc_labels": dict(ARC_LABELS),
        "corpus_dir": str(corpus_dir),
        "chapter_file_count": len(chapters),
        "chapters": chapters,
        "games": games,
        "trilogy": trilogy,
    }


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Marathon terminal voice metrics (Rampancy Wire probe)."
    )
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="also print the trilogy and per-game summary to stdout",
    )
    args = parser.parse_args(argv)

    corpus: Path = args.corpus
    if not corpus.is_dir():
        print(f"corpus dir not found: {corpus}", file=sys.stderr)
        return 2
    result = compute_for_corpus(corpus)

    out: Path = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.stdout:
        print(f"source: {result['source']}")
        print(f"chapters measured: {result['chapter_file_count']}")
        header = f"{'game':5} {'terms':>5} {'words':>7} {'1p-sg':>6} {'1p/1k':>7} {'garble':>6} {'garb/1k':>8}"
        print(header)
        for game in GAMES:
            g = result["games"][game]
            print(
                f"{game:5} {g['terminal_count']:>5} {g['word_count']:>7} "
                f"{g['first_person_singular']:>6} {g['first_person_per_1000']:>7} "
                f"{g['garbled_burst_tokens']:>6} {g['garbled_per_1000']:>8}"
            )
        t = result["trilogy"]
        print(
            f"{'all':5} {t['terminal_count']:>5} {t['word_count']:>7} "
            f"{t['first_person_singular']:>6} {t['first_person_per_1000']:>7} "
            f"{t['garbled_burst_tokens']:>6} {t['garbled_per_1000']:>8}"
        )
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
