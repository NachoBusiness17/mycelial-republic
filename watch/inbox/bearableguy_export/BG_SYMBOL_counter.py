"""BG123 symbol census counter - THE 50 task 10 (W2).

Vocabulary-limited, negation-safe counting over structured decl lines.

Decl grammar: each line is "[negators] term [xN] : free description".
Only the head (before the first colon) is counted. A head beginning with a
negator (no, not, none, without, never, zero, absent) or declaring x0 is
cancelled and logged. Free-text scan mode cancels hits with a negator within
the 3 tokens before the hit. Text-in-image entries are exact, case-sensitive
declared strings, one occurrence per entry.

Replay: load BG_SYMBOL_CENSUS.json, import this module, run count_decl /
count_text over the artifact's readings with the artifact's vocab, and compare
with the artifact's counts.
"""
import re

NEGATORS = {"no", "not", "none", "without", "never", "zero", "absent",
            "isnt", "wasnt", "arent", "cannot"}


def build_matchers(symbols):
    """One case-insensitive word-boundary regex per (term, alias), longest first."""
    pairs = []
    for term, aliases in symbols.items():
        for a in [term] + list(aliases):
            pairs.append((term, a))
    pairs.sort(key=lambda p: -len(p[1]))
    return [(term, re.compile(r"\b" + re.escape(a).replace(r"\ ", r"\s+") + r"\b",
                              re.IGNORECASE)) for term, a in pairs]


def _prev_tokens(text, pos, n=3):
    toks = re.findall(r"[A-Za-z']+", text[:pos])
    return [t.lower().rstrip("'") for t in toks[-n:]]


def scan_text(text, matchers):
    """Free-text mode: longest-first alias scan with a 3-token negation window."""
    counts, log = {}, []
    for term, rx in matchers:
        for m in rx.finditer(text):
            prev = _prev_tokens(text, m.start())
            if any(p in NEGATORS for p in prev):
                log.append({"term": term, "alias": m.group(0), "cancelled_by": prev})
                continue
            counts[term] = counts.get(term, 0) + 1
    return counts, log


HEAD_RX = re.compile(
    r"^((?:(?:no|not|none|without|never|zero|absent)\s+)*)([a-z_]+)(?:\s*x(\d+))?$")


def count_decl(decl_lines, symbols):
    """Decl mode: returns (counts, unknown, cancelled)."""
    counts, unknown, cancelled = {}, [], []
    for line in decl_lines:
        head = line.split(":", 1)[0].strip()
        m = HEAD_RX.match(head)
        if not m:
            unknown.append({"line": line, "reason": "unparseable head"})
            continue
        negs, term, mult = m.group(1), m.group(2), int(m.group(3) or 1)
        if term not in symbols:
            unknown.append({"line": line, "reason": "term not in vocab", "term": term})
            continue
        if negs.strip() or mult == 0:
            cancelled.append({"line": line, "term": term, "negators": negs.strip()})
            continue
        counts[term] = counts.get(term, 0) + mult
    return counts, unknown, cancelled


def count_text(text_decls):
    """Text-in-image: one occurrence per non-negated declared entry."""
    counts = {}
    for e in text_decls:
        if e.get("negated"):
            continue
        s = e["string"]
        counts[s] = counts.get(s, 0) + 1
    return counts
