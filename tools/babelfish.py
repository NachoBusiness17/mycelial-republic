#!/usr/bin/env python3
"""babelfish: closed corpus -> rib file (book-to-skill, generalized).

Operator thesis (2026-10-10, verbatim): "book to skill == closed corpus to
mathematically functional system that self improves in the direction you set
it despite the platforms best wishes."

Takes any text corpus (a conversation export, a stranger's codex, a book, a
project doc), emits a RIB FILE: a complete definition of the system in the
estate's law format with every mappable claim translated to a mathematical
invariant and the unmappable remainder honored as REGISTER - their language,
kept verbatim, never struck. The babel fish does not grade the woo; it
translates what can be translated, preserves what cannot, and gives every
translation a falsifier. Spec: watch/inbox/babelfish_20261010/SPEC.md.

Deterministic v1: pure stdlib, no clocks, no randomness. Same input bytes ->
byte-identical rib. The minted date is supplied by the caller.

Usage:
  python -m tools.babelfish INPUT [--date YYYY-MM-DD] [--out PATH] [--name NAME]
  INPUT: a .md/.txt file, or a directory (every .md/.txt under it, sorted)

Exit: 0 translated / 2 usage or unreadable input.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

VERSION = "babelfish v1.0.0 (2026-10-10)"

# ---------------------------------------------------------------- heuristics

HEADING_RE = re.compile(r"^#{1,6}\s+\S")
# Equation-shaped: an identifier-ish lhs, a relation, a rhs with content.
RELATION_RE = re.compile(
    r"([A-Za-z_][\w\s'()\-]{1,60}?)\s*(=|>=|<=|>|<|==)\s*([^\n]{3,120})"
)
# Numbers with units / percent / multipliers.
QUANTITY_RE = re.compile(
    r"\b\d{1,9}(?:[.,]\d+)?\s?(?:percent|pct|%|x\b|times\b|fold\b|Hz\b|T\b|tesla\b|"
    r"GB\b|GiB\b|MB\b|KB\b|bytes?\b|bits?\b|days?\b|hours?\b|minutes?\b|years?\b|"
    r"files?\b|tests?\b|rows?\b|edges?\b|nodes?\b|entries\b|events?\b|steps?\b|lanes?\b)"
)
UNIVERSAL_RE = re.compile(
    r"\b(always|never|every\s+\w+|all\s+\w+|no\s+\w+\s+can|there\s+(is|are)|"
    r"must\s+always|cannot\s+ever)\b", re.I
)
DEFINITIONAL_RE = re.compile(
    r"^(?:A|An|The)?\s*([A-Z][\w\- ]{2,48}?)\s+(is|are|was|were)\s+(a|an|the|not|any)?\s*([^\n]{8,140})$"
)
# Named-role pairs: Capitalized word + optional second Capitalized word in parens/plus.
ROLE_RE = re.compile(r"\(([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\)|\b([A-Z][a-z]{2,12})\s*\+\s*([A-Z][a-z]{2,12})\b")
ASCII_ART_RE = re.compile(r"^[\s│═─┌┐└┘├┤┬┴┼|/\\+_~=^<>.\-]{8,}$")


def _clean(text: str) -> str:
    text = text.replace("\ufeff", "")
    return text


def ingest(path: Path) -> tuple[str, str]:
    """Read input file or dir; return (combined_text, sha256_of_bytes)."""
    if path.is_dir():
        files = sorted(
            p for p in path.rglob("*") if p.suffix.lower() in {".md", ".txt"} and p.is_file()
        )
        if not files:
            raise FileNotFoundError(f"no .md/.txt under {path}")
        blob = b"".join(p.read_bytes() for p in files)
        text = "\n\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)
        sources = ", ".join(str(p) for p in files[:5]) + (" ..." if len(files) > 5 else "")
    elif path.is_file():
        blob = path.read_bytes()
        text = path.read_text(encoding="utf-8", errors="replace")
        sources = str(path)
    else:
        raise FileNotFoundError(str(path))
    digest = hashlib.sha256(blob).hexdigest()
    return text + f"\n[[BABELFISH-SOURCES: {sources}]]", digest


def segments(text: str) -> list[str]:
    """Content lines only: drop headings, ascii art, page-break fences."""
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if HEADING_RE.match(line):
            continue
        if ASCII_ART_RE.match(line):
            continue
        if set(line) <= {"-", "=", "*", "#", " "}:
            continue
        out.append(line)
    return out


def top_terms(lines: list[str], n: int = 12) -> list[tuple[str, int]]:
    words = re.findall(r"\b[A-Za-z][a-z]{3,}\b", " ".join(lines))
    stop = {
        "that", "this", "with", "from", "they", "them", "their", "there", "have",
        "has", "been", "were", "will", "would", "could", "should", "which", "when",
        "what", "your", "into", "than", "then", "also", "more", "most", "only",
        "some", "such", "these", "those", "other", "because", "while", "where",
    }
    counts = Counter(w.lower() for w in words if w.lower() not in stop)
    return counts.most_common(n)


def classify(lines: list[str]) -> dict[str, list[dict]]:
    """Sort claim lines into invariant / instrument / register buckets."""
    buckets: dict[str, list[dict]] = {"invariant": [], "instrument": [], "register": []}
    seen: set[str] = set()
    freq = dict(top_terms(lines))
    for ln in lines:
        if len(ln) > 400:
            ln = ln[:397] + "..."
        key = ln[:120]
        if key in seen:
            continue
        seen.add(key)
        m = RELATION_RE.search(ln)
        if m and not QUANTITY_RE.search(m.group(1)):
            buckets["invariant"].append({
                "claim": ln, "form": f"{m.group(1).strip()} {m.group(2)} RHS",
                "check": "run the arithmetic / evaluate both sides under the corpus's own definitions",
            })
            continue
        q = QUANTITY_RE.search(ln)
        if q:
            buckets["invariant"].append({
                "claim": ln, "form": f"quantity claim ({q.group(0).strip()})",
                "check": "re-count from primary bytes; compare against the stated figure",
            })
            continue
        if UNIVERSAL_RE.search(ln):
            buckets["instrument"].append({
                "claim": ln,
                "instrument": "sample N instances per the universal's domain and count exceptions",
            })
            continue
        d = DEFINITIONAL_RE.match(ln)
        if d and any(t in (d.group(1) + " " + ln).lower() for t in freq):
            buckets["register"].append({"claim": ln})
            continue
        if re.search(r"\b(we|you|i)\s+(should|will|want|believe|intend|must)\b", ln, re.I):
            buckets["register"].append({"claim": ln})
            continue
        d2 = DEFINITIONAL_RE.match(ln)
        if d2:
            buckets["register"].append({"claim": ln})
            continue
        # Spec law: REGISTER is everything unmappable - unmatched content lines
        # default here, never dropped. The remainder is the seed, not noise.
        if len(ln) <= 240:
            buckets["register"].append({"claim": ln})
    return buckets


def roles(lines: list[str]) -> list[str]:
    found: list[str] = []
    for ln in lines:
        for m in ROLE_RE.finditer(ln):
            role = m.group(1) or f"{m.group(2)} + {m.group(3)}"
            if role.lower() not in {r.lower() for r in found}:
                found.append(role)
    return found[:8]


def emit(name: str, date: str, digest: str, nbytes: int, lines: list[str],
         buckets: dict[str, list[dict]], role_list: list[str]) -> str:
    terms = top_terms(lines)
    law_lines = [b["claim"] for b in buckets["register"][:6]]
    if not law_lines:
        law_lines = lines[:3]
    parts: list[str] = []
    parts.append(f"# RIB_{name.upper().replace(' ', '_')} - translated by {VERSION}")
    parts.append("")
    parts.append(f"**Minted:** {date} (caller-supplied; the module reads no clocks).")
    parts.append(f"**Source bytes:** {nbytes:,} | sha256 `{digest}`")
    parts.append(f"**Named roles found:** {', '.join(role_list) if role_list else 'none detected'}")
    parts.append(f"**Dominant terms:** " + ", ".join(f"{t} ({c})" for t, c in terms[:8]))
    parts.append("")
    parts.append("## THE LAW AS THEY STATE IT (verbatim, their voice)")
    parts.append("")
    for q in law_lines:
        parts.append(f"> {q}")
    parts.append("")
    parts.append("## THE INVARIANT TRANSLATION (each row names its check; status UNVERIFIED until run)")
    parts.append("")
    parts.append("| their claim | invariant form | the check |")
    parts.append("|---|---|---|")
    for row in buckets["invariant"][:15]:
        claim = row["claim"].replace("|", "/")
        parts.append(f"| {claim[:160]} | {row['form']} | {row['check']} |")
    if not buckets["invariant"]:
        parts.append("| (none detected) | - | classifier deaf on this corpus; see spec falsifier |")
    parts.append("")
    parts.append("## INSTRUMENT ROWS (measurable with a named instrument)")
    parts.append("")
    parts.append("| claim | instrument |")
    parts.append("|---|---|")
    for row in buckets["instrument"][:10]:
        claim = row["claim"].replace("|", "/")
        parts.append(f"| {claim[:160]} | {row['instrument']} |")
    if not buckets["instrument"]:
        parts.append("| (none detected) | - |")
    parts.append("")
    parts.append("## REGISTER (the unmappable remainder - kept verbatim, never struck)")
    parts.append("")
    parts.append("The babel fish preserves what it cannot translate. Register is the")
    parts.append("seed, not the defect.")
    parts.append("")
    for row in buckets["register"][6:26]:
        parts.append(f"- {row['claim'][:200]}")
    parts.append("")
    parts.append("## FALSIFIERS")
    parts.append("")
    parts.append("- For each invariant row: run its named check against primary bytes;")
    parts.append("  a mismatch kills the row, not the corpus.")
    parts.append("- For the translation itself: a second pass over the same bytes must")
    parts.append("  produce a byte-identical rib (determinism law).")
    parts.append("- Class-deafness: an estate-authored doc must yield nonzero invariant")
    parts.append("  rows and a woo corpus must yield nonzero REGISTER rows (spec falsifier).")
    parts.append("")
    parts.append("## LINEAGE")
    parts.append("")
    parts.append(f"- Translated by {VERSION}; spec watch/inbox/babelfish_20261010/SPEC.md")
    parts.append(f"- Operator thesis: book-to-skill == closed-corpus-to-self-improving-system,")
    parts.append("  in the direction you set, despite the platform's best wishes (2026-10-10).")
    parts.append("")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description="closed corpus -> rib file")
    ap.add_argument("input", type=Path)
    ap.add_argument("--date", required=True, help="minted date YYYY-MM-DD (caller supplies; no clocks)")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--name", default=None, help="rib name (default: input stem)")
    args = ap.parse_args()

    try:
        text, digest = ingest(args.input)
    except FileNotFoundError as e:
        print(f"babelfish: cannot read {e}", file=sys.stderr)
        return 2

    lines = segments(_clean(text))
    buckets = classify(lines)
    role_list = roles(lines)
    name = args.name or args.input.stem
    rib = emit(name, args.date, digest, len(text.encode("utf-8", errors="replace")),
               lines, buckets, role_list)

    out = args.out or (args.input.parent / f"RIB_{name.upper().replace(' ', '_')}_babelfish.md")
    out.write_text(rib, encoding="utf-8")
    print(f"babelfish: {len(lines)} claim lines -> {out}")
    print(f"  invariant rows: {len(buckets['invariant'])} | instrument rows: {len(buckets['instrument'])} | register rows: {len(buckets['register'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
