"""citation_lint_numbers -- the PHANTOM-NUMBER engine (a05-r2, 2026-10-01).

The founding class: STORY.md:240 stated "191.8M tokens spent" and named
watch/inbox/frontier_olm_20260928/DIGEST.md in the same sentence; the number
appeared nowhere in the source bytes. Pairing is per SENTENCE, because a
paragraph can hold measurements of files (byte sizes live outside their own
content) and unrelated counts no source should have to contain.

Identifier shapes never pair (each cut earned by a live false-fire class):
compact dates, arXiv ids, >3-fraction-digit floats, hyphen-attached ids
(B2-125, UF-119), IP:port shapes, colon-attached ports, sed print ranges
("238,242p"), non-grouping comma lists (2,3,4,7), line/row references
sitting after a path or anchor ("DIGEST.md lines 7 to 17", "txt:1058-1071,
2118-2139", "line 131 (AGENTS.md)"), and disk/census unit nouns ("397
records in the ledger" is a re-run, not a citation; B2-216 owns counts).
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from tools.citation_lint_io import (
        ANCHOR_RE,
        PATH_RE,
        Finding,
        RECORD_SOURCE_SUFFIXES,
        file_contains,
        rel_path,
        resolve_path,
    )
except ImportError:  # script invocation (python tools/citation_lint.py)
    from citation_lint_io import (
        ANCHOR_RE,
        PATH_RE,
        Finding,
        RECORD_SOURCE_SUFFIXES,
        file_contains,
        rel_path,
        resolve_path,
    )

URL_RE = re.compile(r"https?://\S+")
IP_RE = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{2,5})?")
DOTANCHOR_RE = re.compile(r"\.[A-Za-z][\w\-]*:\d{1,5}(?:-\d{1,5})?")
NUM_RE = re.compile(r"(?<![\w.\-])(\d[\d,]*(?:\.\d+)?)( ?[KMB])?(?![\w.]*\d)")
YEAR_RE = re.compile(r"(19|20)\d{2}")
DATE8_RE = re.compile(r"(19|20)\d{6}")
ARXIV_RE = re.compile(r"\d{4}\.\d{4,5}")


def _notable(num: str, suffix: str) -> bool:
    """A number worth byte-checking: K/M suffix, comma groups, or 4+ digits.

    B-suffixed byte sizes and 1-3 digit prose numbers are census/disk facts
    (the B2-216 instrument class), not content claims; the founding phantom
    (191.8M) and comma-grouped totals are the checkable shapes.
    """
    if suffix:
        return suffix.strip().upper() != "B"
    if "," in num:
        return True
    digits = num.replace(",", "").replace(".", "")
    return len(digits) >= 4


def _expanded_forms(num: str, suffix: str) -> list[str]:
    """Search forms for a number: raw, comma-stripped, int part, expansion."""
    forms = [num, num.replace(",", "")]
    plain = num.replace(",", "")
    if "." in plain:
        forms.append(plain.split(".")[0])
    if suffix:
        s = suffix.strip().upper()
        expanded = float(plain) * {"K": 1e3, "M": 1e6, "B": 1e9}[s]
        if expanded == int(expanded):
            forms.append(str(int(expanded)))
    out = []
    for f in forms:
        if f and f not in out:
            out.append(f)
    return out


def check_phantom_numbers(
    record: Path, record_lines: list[str], result, resolve=resolve_path,
    contains=file_contains,
) -> None:
    """Sentence-level check: a notable quantity vs its sentence's named sources.

    Fires when a notable number appears in NONE of its sentence's resolvable
    record-type named sources. Sources stream or cache per run; an oversize
    source makes the number unverifiable, never phantom. A sentence whose
    named record sources ALL fail to resolve is no longer silent (ouroboros
    R3 move 5, 2026-10-05): each number on it files a warn-tier
    UNRESOLVED-SOURCE finding, because the 900M probe line passed the gate
    exit 0 and the founding 191.8M class survives one dead-path citation.
    """
    paras: list[tuple[int, int]] = []
    para_start = None
    for i, ln in enumerate(record_lines, 1):
        if ln.strip():
            if para_start is None:
                para_start = i
        elif para_start is not None:
            paras.append((para_start, i - 1))
            para_start = None
    if para_start is not None:
        paras.append((para_start, len(record_lines)))

    sent_re = re.compile(r"(?<=[.!?])\s+")
    ref_gap_re = re.compile(r"^[\s:,;~]*(?:(?:lines?|rows?|entries|at|L)\s*)*$", re.I)
    ref_before_re = re.compile(
        r"(?:lines?|rows?|entries|L|exit(ed)?|sums? to|totals?)[\s:~]*$", re.I
    )
    cont_gap_re = re.compile(r"^[\s,;]*(?:to|and|or)?[\s,;]*$", re.I)
    unit_after_re = re.compile(
        r"^\s{0,3}(?:-line|-row|bytes?|chars?|lines?\b|rows?\b|records?\b|"
        r"entries\b|tools\b|keys\b|leaves\b|files\b|tests\b|cases\b|hits\b|"
        r"pings?\b|seals?\b|pins\b|passed\b|failed\b|skipped\b|p\b)",
        re.I,
    )

    for p_start, p_end in paras:
        p_text = "\n".join(record_lines[p_start - 1 : p_end])
        cuts = [0] + [m.end() for m in sent_re.finditer(p_text)] + [len(p_text)]
        for s_a, s_b in zip(cuts, cuts[1:]):
            sent = p_text[s_a:s_b]
            if not sent.strip():
                continue
            excl = [m.span() for m in URL_RE.finditer(sent)]
            path_spans = []
            anchor_spans = []
            for m in PATH_RE.finditer(sent):
                path_spans.append(m)
                excl.append(m.span())
            for m in ANCHOR_RE.finditer(sent):
                anchor_spans.append(m)
                excl.append(m.span())
            for m in DOTANCHOR_RE.finditer(sent):
                excl.append(m.span())
            for m in IP_RE.finditer(sent):
                excl.append(m.span())
            numbers: list[tuple[str, str, int]] = []
            prev_ref_end = -1  # end offset of the last ref-classified number
            for m in NUM_RE.finditer(sent):
                if any(a <= m.start() < b for a, b in excl):
                    continue
                if m.start() > 0 and sent[m.start() - 1] == ":":
                    continue  # colon-attached: ports (:8765), times, ref tails
                num, suffix = m.group(1).rstrip(","), (m.group(2) or "")
                if not num:
                    continue
                # comma-grouped must BE grouping (46,531), not an id list
                # (2,3,4,7,8,9,11,12)
                if "," in num and not re.fullmatch(r"\d{1,3}(?:,\d{3})+", num):
                    prev_ref_end = -1
                    continue
                if YEAR_RE.fullmatch(num) and not suffix and "," not in num:
                    continue
                if DATE8_RE.fullmatch(num.replace(",", "")):
                    continue
                if ARXIV_RE.fullmatch(num):
                    continue
                plain = num.replace(",", "")
                if "." in plain and len(plain.split(".")[1]) > 3:
                    continue
                if not _notable(num, suffix):
                    prev_ref_end = -1
                    continue
                # a number directly after a path/anchor is a line/row ref
                # into that source ("DIGEST.md lines 7 to 17"), not a quantity
                is_ref = False
                for pm in list(path_spans) + list(anchor_spans):
                    if pm.end() > m.start():
                        continue  # number precedes the path: not a ref into it
                    gap = sent[pm.end() : m.start()]
                    if len(gap) <= 25 and ref_gap_re.fullmatch(gap or ""):
                        is_ref = True
                        break
                # "...lines 79, 109, 150, 170": continuations of a ref list
                if not is_ref and prev_ref_end >= 0:
                    cont = sent[prev_ref_end : m.start()]
                    if len(cont) <= 6 and cont_gap_re.fullmatch(cont or ""):
                        is_ref = True
                # "line 131 (AGENTS.md)": a ref word directly BEFORE the number
                if not is_ref:
                    before = sent[max(0, m.start() - 10) : m.start()]
                    if ref_before_re.search(before or ""):
                        is_ref = True
                # a file's own shape (bytes/chars/line count) is measured on
                # disk, not stated in its content: uncheckable by containment
                if not is_ref:
                    after = sent[m.end() : m.end() + 12]
                    if unit_after_re.match(after or ""):
                        prev_ref_end = -1
                        continue
                if is_ref:
                    prev_ref_end = m.end()
                    continue
                prev_ref_end = -1
                line = p_text[: s_a + m.start()].count("\n") + p_start
                numbers.append((num, suffix, line))
            if not numbers:
                continue
            sources: dict[str, Path] = {}
            unresolved: list[str] = []
            for pm in path_spans:
                if Path(pm.group(0)).suffix.lower() not in RECORD_SOURCE_SUFFIXES:
                    continue  # code/config paths anchor; they do not attribute
                resolved = resolve(pm.group(0), record)
                if resolved is None:
                    unresolved.append(pm.group(0))
                    continue
                if resolved.resolve() == record.resolve():
                    continue  # a self-cite resolved; it is not an unresolved name
                sources[pm.group(0)] = resolved
            if not sources:
                # R3 move 5 (ouroboros 2026-10-05, SYNTHESIS row 5): numbers on
                # a sentence whose record-type named sources ALL fail to
                # resolve were skipped whole, so a fabricated aggregate citing
                # a dead path was invisible. Warn tier: unresolved means
                # unverifiable, not proven phantom.
                if unresolved:
                    for num, suffix, line in numbers:
                        result.numbers += 1
                        result.findings.append(
                            Finding(
                                "UNRESOLVED-SOURCE", rel_path(record), line,
                                f"{num}{suffix.strip()}",
                                "number unverifiable: the sentence's named "
                                "record sources resolve nowhere ("
                                + ", ".join(sorted(unresolved)[:3]) + ")",
                            )
                        )
                continue
            readable: dict[str, Path] = {}
            for name, path in sources.items():
                try:
                    if path.is_file():
                        readable[name] = path
                except OSError:
                    continue
            if not readable:
                continue
            for num, suffix, line in numbers:
                forms = [f.lower() for f in _expanded_forms(num, suffix)]
                comma_forms = [f.replace(",", "") for f in forms if "," in f]
                found = False
                unverifiable = False
                for path in readable.values():
                    r = contains(path, forms)
                    if r is None:
                        # an oversize source cannot be contained: no verdict
                        unverifiable = True
                        break
                    if r:
                        found = True
                        break
                    if comma_forms and contains(path, comma_forms):
                        found = True
                        break
                if unverifiable:
                    continue
                result.numbers += 1
                if not found:
                    result.findings.append(
                        Finding(
                            "PHANTOM-NUMBER", rel_path(record), line,
                            f"{num}{suffix.strip()}",
                            "number appears in none of the sentence's named sources ("
                            + ", ".join(sorted(readable)[:3])
                            + ")",
                        )
                    )
