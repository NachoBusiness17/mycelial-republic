#!/usr/bin/env python3
"""luau_lint — headless structural checks for the mountain's Luau tree.

Playtest pass zero: catches unbalanced blocks/brackets and missing requires
before a human ever opens Studio. Lua block heuristic (after stripping
comments/strings): opens = function|if|repeat|do-standalone; closes = end|until.
(`for`/`while` each own exactly one `do`, so they cancel out of the do count.)

Disease tripwire (spec: roblox/docs/PLAYTEST.md "Headless tripwire",
2026-09-26 B2-31, filed before this code): two advisory checks so the two
cured diseases surface at mountain_check step 1 if they ever return.
- poll disease (t56/t63): GetAttribute read riding a task.wait(n<=10) loop
  timer at the same closure depth; cure is change-signal bindings
  (init.server.luau t56, MudBasecamp.luau t63).
- RMW disease (t74): GetAsync+SetAsync read-modify-write in one function
  body; cure is one UpdateAsync per durable append (ShadowLedger.luau t74).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def strip_comments_strings(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("--", i):
            if src.startswith("--[[", i) or src.startswith("--[=[", i):
                close = "]]" if src.startswith("--[[", i) else "]]="
                j = src.find(close, i + 4)
                i = (j + len(close)) if j != -1 else n
            else:
                j = src.find("\n", i)
                i = j if j != -1 else n
        elif c in "\"'":
            q, i = c, i + 1
            while i < n and src[i] != q:
                i += 2 if src[i] == "\\" else 1
            i += 1
        elif src.startswith("[[", i) or src.startswith("[=[", i):
            close = "]]" if src.startswith("[[", i) else "]]="
            j = src.find(close, i + 2)
            i = (j + len(close)) if j != -1 else n
        else:
            out.append(c)
            i += 1
    return "".join(out)


def count_word(src: str, word: str) -> int:
    return len(re.findall(rf"\b{word}\b", src))


# B2-119 (2026-09-26): Luau if-EXPRESSIONS (`local x = if c then a else b`,
# single-line chains including elseif arms) are counted by the \bif\b opener
# scan but carry no `end`, so each one faked delta +1: FrontierSoulsZone
# 39 vs 36, HardwarePrimerZone 25 vs 24, IncidentDungeonZone 26 vs 25 were
# all if-expression lines with zero real imbalance (luau-lsp parse_fails=0
# on the same tree the same day). This is the keyword-in-string class's
# successor: strings were already stripped, the residual noise is grammar,
# not text. Discount single-line if-expression chains (lazy spans so two
# chains on one line count twice; the token required after `else` rejects a
# trailing bare `else`, the statement form whose else-BLOCK opens on the
# following lines, RiddleMazeZone:71). A line carrying an
# `end` cannot be a pure one-liner chain (statement-if closes with end), so
# those stay counted. Known blind spot, documented here: multiline
# if-expressions still read as statement-ifs and keep faking +1.
IFEXPR_LINE_RE = re.compile(r"\bif\b[^;\n]*?\bthen\b[^;\n]*?\belse\b\s*\S")


def ifexpr_discount(src: str) -> int:
    d = 0
    for ln in src.splitlines():
        if IFEXPR_LINE_RE.search(ln) and not re.search(r"\bend\b", ln):
            d += len(IFEXPR_LINE_RE.findall(ln))
    return d


# ------------------------------------------------------------ disease tripwire
# Spec: roblox/docs/PLAYTEST.md "Headless tripwire" (2026-09-26, B2-31).
# Receipts: watch/inbox/gala_20260925/afterparty/lanes/t56.check.txt,
# t63.check.txt, t74.check.txt. Advisory output only; luau-lsp in
# tools/mountain_check stays the authoritative parser.

# t56's poll fired every 1s, t63's every 10s; anything at or under 10s inside
# a loop is treated as a standing poll interval.
POLL_WAIT_MAX = 10.0

BLOCK_RE = re.compile(r"\b(while|for|function|if|repeat|do|end|until)\b")
GETATTR_RE = re.compile(r"\bGetAttribute\b")
WAIT_RE = re.compile(r"\btask\.wait\s*\(\s*([0-9]*\.?[0-9]+)\s*\)")
GETASYNC_RE = re.compile(r"\bGetAsync\s*\(")
SETASYNC_RE = re.compile(r"\bSetAsync\s*\(")


def blank_comments_strings(src: str) -> str:
    """Length-preserving strip for the tripwire: comment/string bytes become
    spaces, newlines survive, so char offsets and line numbers map 1:1 to the
    file on disk (strip_comments_strings above deletes and shifts offsets).
    Same block semantics: content inside comments/strings cannot match."""
    out = list(src)
    i, n, spans = 0, len(src), []
    while i < n:
        if src.startswith("--", i):
            if src.startswith("--[[", i) or src.startswith("--[=[", i):
                close = "]]" if src.startswith("--[[", i) else "]]="
                j = src.find(close, i + 4)
                stop = (j + len(close)) if j != -1 else n
            else:
                j = src.find("\n", i)
                stop = j if j != -1 else n
            spans.append((i, stop))
            i = stop
        elif src[i] in "\"'":
            q, k = src[i], i + 1
            while k < n and src[k] != q:
                k += 2 if src[k] == "\\" else 1
            stop = min(k + 1, n)
            spans.append((i, stop))
            i = stop
        elif src.startswith("[[", i) or src.startswith("[=[", i):
            close = "]]" if src.startswith("[[", i) else "]]="
            j = src.find(close, i + 2)
            stop = (j + len(close)) if j != -1 else n
            spans.append((i, stop))
            i = stop
        else:
            i += 1
    for a, b in spans:
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "
    return "".join(out)


def _block_tokens(src: str) -> list[tuple[str, int]]:
    return [(m.group(1), m.start()) for m in BLOCK_RE.finditer(src)]


def _matching_closer(tokens: list[tuple[str, int]], j: int) -> int:
    """Index of the end/until token closing the block opened at tokens[j].
    while/for own their header `do`, so that do does not deepen the block
    (same opens/closes algebra as the file docstring)."""
    depth = 0
    header_do_pending = False
    while j < len(tokens):
        kw = tokens[j][0]
        if kw in ("while", "for"):
            depth += 1
            header_do_pending = True
        elif kw == "do":
            if header_do_pending:
                header_do_pending = False
            else:
                depth += 1
        elif kw in ("function", "if", "repeat"):
            depth += 1
        elif kw in ("end", "until"):
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return len(tokens) - 1


def _line_of(src: str, pos: int) -> int:
    return src.count("\n", 0, pos) + 1


def poll_disease_findings(src: str) -> list[str]:
    """t56/t63 disease: GetAttribute read inside a loop that also has a
    task.wait(n<=10), both at the same closure depth (a read nested in an
    inner function, e.g. a Touched handler, is event-driven, not a poll)."""
    findings = []
    tokens = _block_tokens(src)
    gets = [m.start() for m in GETATTR_RE.finditer(src)]
    waits = [
        (m.start(), float(m.group(1)))
        for m in WAIT_RE.finditer(src)
        if float(m.group(1)) <= POLL_WAIT_MAX
    ]
    if not gets or not waits:
        return findings
    reported_spans: list[tuple[int, int]] = []
    for idx, (kw, pos) in enumerate(tokens):
        if kw not in ("while", "for"):
            continue
        closer = _matching_closer(tokens, idx)
        loop_start, loop_end = pos, tokens[closer][1]
        # a loop inside an already-reported loop is the same disease instance
        if any(a <= loop_start and loop_end <= b for a, b in reported_spans):
            continue
        loop_gets = [p for p in gets if loop_start < p < loop_end]
        loop_waits = [(p, n) for p, n in waits if loop_start < p < loop_end]
        if not loop_gets or not loop_waits:
            continue

        def closure_depth(p: int) -> int:
            return sum(
                1 for k2, p2 in tokens[idx + 1:closer] if p2 < p and k2 == "function"
            )

        waits_by_depth: dict[int, tuple[int, float]] = {}
        for p, n in loop_waits:
            waits_by_depth.setdefault(closure_depth(p), (p, n))
        for p in loop_gets:
            hit = waits_by_depth.get(closure_depth(p))
            if hit:
                wp, n = hit
                reported_spans.append((loop_start, loop_end))
                findings.append(
                    f"poll disease (t56/t63): GetAttribute line {_line_of(src, p)} "
                    f"rides a task.wait({n:g}s) loop timer at line {_line_of(src, wp)}; "
                    f"bind GetAttributeChangedSignal/AttributeChanged instead "
                    f"(cure: init.server.luau t56, MudBasecamp.luau t63)"
                )
                break  # one finding per offending loop
    return findings


def rmw_disease_findings(src: str) -> list[str]:
    """t74 disease: GetAsync and SetAsync called in one function body, the
    lost-update read-modify-write shape. Separate write-only/read-only
    functions (HeadMuseum flushSoul/restoreSoul) do not trip."""
    findings = []
    tokens = _block_tokens(src)
    gets = [m.start() for m in GETASYNC_RE.finditer(src)]
    sets = [m.start() for m in SETASYNC_RE.finditer(src)]
    if not gets or not sets:
        return findings
    reported_spans: list[tuple[int, int]] = []
    for idx, (kw, pos) in enumerate(tokens):
        if kw != "function":
            continue
        closer = _matching_closer(tokens, idx)
        body_start, body_end = pos, tokens[closer][1]
        # a body inside an already-reported body (e.g. task.spawn's closure
        # wrapping the real offender) is the same disease instance
        if any(a <= body_start and body_end <= b for a, b in reported_spans):
            continue
        g = [p for p in gets if body_start < p < body_end]
        s = [p for p in sets if body_start < p < body_end]
        if g and s:
            reported_spans.append((body_start, body_end))
            findings.append(
                f"RMW disease (t74): GetAsync line {_line_of(src, g[0])} + SetAsync "
                f"line {_line_of(src, s[0])} in one function body; concurrent "
                f"appends lose rows, use one UpdateAsync (cure: ShadowLedger.luau t74)"
            )
    return findings


def check(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    src = strip_comments_strings(raw)
    issues = []
    opens = sum(count_word(src, w) for w in ("function", "if", "repeat", "do"))
    closes = sum(count_word(src, w) for w in ("end", "until"))
    opens -= ifexpr_discount(src)  # B2-119: if-expressions carry no `end`
    if opens != closes:
        issues.append(f"block balance: {opens} openers vs {closes} closers (delta {opens - closes})")
    for a, b in (("(", ")"), ("{", "}"), ("[", "]")):
        if src.count(a) != src.count(b):
            issues.append(f"bracket balance: {src.count(a)} '{a}' vs {src.count(b)} '{b}'")
    # local functions that are defined but never referenced (dead weight signal)
    for m in re.finditer(r"local function (\w+)", src):
        name = m.group(1)
        if len(re.findall(rf"\b{name}\b", src)) == 1:
            issues.append(f"dead local function: {name} (defined, never called)")
    # disease tripwire (spec: roblox/docs/PLAYTEST.md "Headless tripwire"):
    # runs on the offset-true blanked copy so reported lines match the file
    issues.extend(poll_disease_findings(blank_comments_strings(raw)))
    issues.extend(rmw_disease_findings(blank_comments_strings(raw)))
    return issues


def main() -> int:
    root = Path(__file__).resolve().parent.parent / "roblox" / "src"
    bad = 0
    for f in sorted(root.rglob("*.luau")):
        issues = check(f)
        if issues:
            bad += 1
            print(f"{f.relative_to(root.parent.parent)}")
            for i in issues:
                print(f"  - {i}")
    print(f"checked {len(list(root.rglob('*.luau')))} files, {bad} with findings")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
