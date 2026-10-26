#!/usr/bin/env python3
"""prompt_compiler - deterministic reduction passes for verbose prompts.

Design (flash50 deep-prompt-compiler, 2026-09-28): a prompt is a program
whose semantics are the load-bearing constraints it carries. The compiler
applies ordered, deterministic passes and guarantees the constraint surface
survives byte-identical; everything else it deletes is logged so the compile
is falsifiable (the State XI receipt law: deletion without a falsifier is a
silent skip).

Passes:
  P0 dashnorm      em-dash -> " - " (house law: no em-dashes in compiled output)
  P1 linededupe    exact duplicate lines dropped (common subexpression elimination)
  P2 neardedupe    line token-set Jaccard >= --overlap drops the LATER line (DCE)
  P3 peephole      filler-phrase rewrites (please / in order to / note that ...)
  P4 sectmerge     overlapping markdown sections merged, unique lines folded, rest dropped
  P5 backpatch     every pinned constraint line verified verbatim; restores lost pins
  P6 evidence      (--release only) long parenthetical receipt runs on non-pin lines
                   bounded to a pointer: the debug-vs-release build distinction.
                   Lossy by design; falsifiable because the elided refs resolve
                   on disk from the compile report's sha_in source pointer.

Gates (reported, never papered over):
  factgate         every file path / hex token in the source must survive in the output
  idempotency      compile(compile(x)) byte-size vs compile(x)

Reuse: pin shaping borrows tools/thought_quantizer.py's LAW_SHAPE_RE spirit
(its signature() dedupe idea too) - the estate already built the row-level
version of this compiler; this tool is the document-level one.

Run:  .venv/Scripts/python.exe tools/prompt_compiler.py compile <input> [-o out] [--report rpt.json]
Exit: 0 ok / 1 factgate FAIL (lost path or hash tokens) / 2 input error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---- load-bearing constraint pin (echoes thought_quantizer LAW_SHAPE_RE) ----
PIN_RE = re.compile(
    r"(?i)\b(must|never|always|required|law|owed|falsifier|do not|don't|"
    r"never trust|only with|until verified|before declaring|counts as|"
    r"exit\s*[0-9]|no git|no paid|read[- ]only|verbatim)\b")

# ---- fact tokens: paths and hashes the downstream model must be able to cite ----
PATH_RE = re.compile(r"[A-Za-z0-9_\-./\\]{3,}\.(?:md|py|json|jsonl|txt|yaml|yml|ps1|ts|html|js)\b")
HEX_RE = re.compile(r"\b[a-f0-9]{8,64}\b")

# ---- peephole table: zero-instruction filler ----
PEEPHOLE = [
    (re.compile(r"(?i)\b(?:please|kindly)\s+"), ""),
    (re.compile(r"(?i)\bit (?:is|'s) important to note that\s+"), ""),
    (re.compile(r"(?i)\bas you know,\s+"), ""),
    (re.compile(r"(?i)\bmake sure to\s+"), ""),
    (re.compile(r"(?i)\bbe sure to\s+"), ""),
    (re.compile(r"(?i)\bin order to\b"), "to"),
    (re.compile(r"(?i)\bdue to the fact that\b"), "because"),
    (re.compile(r"(?i)\bin the event that\b"), "if"),
    (re.compile(r"(?i)\bat this point in time\b"), "now"),
    (re.compile(r"(?i)\butilize\b"), "use"),
    (re.compile(r"(?i)\bnote that\s+"), ""),
]

EMDASH_RE = re.compile(r"\s*[\u2014\u2013]\s*")


def signature(text: str, n: int = 60) -> str:
    t = text.strip().lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n]


def tokens(text: str) -> set:
    return set(re.findall(r"[a-z0-9_.:/\\-]{2,}", text.lower()))


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def compile_prompt(src: str, overlap: float = 0.72, sect_overlap: float = 0.55,
                   release: bool = False) -> tuple[str, dict]:
    stats = {"passes": {}, "restored_pins": [], "bytes_in": len(src.encode("utf-8"))}
    lines = src.splitlines()

    def fired(name, n):
        stats["passes"][name] = stats["passes"].get(name, 0) + n

    # pins and fact tokens are computed on P0-normalized text so restored pins
    # never carry an em-dash back into the compiled output
    ndash = sum(1 for ln in lines if "\u2014" in ln or "\u2013" in ln)
    lines = [EMDASH_RE.sub(" - ", ln) for ln in lines]
    fired("P0_dashnorm", ndash)
    norm_src = "\n".join(lines)
    pins = [ln.strip() for ln in lines if ln.strip() and PIN_RE.search(ln)]
    fact_tokens = set(PATH_RE.findall(norm_src)) | set(HEX_RE.findall(norm_src))

    # P1: exact line dedupe (keep first occurrence = definition site)
    seen, out, dup = set(), [], 0
    for ln in lines:
        sig = signature(ln)
        if sig and sig in seen and not PIN_RE.search(ln):
            dup += 1
            continue
        if sig:
            seen.add(sig)
        out.append(ln)
    fired("P1_linededupe", dup)
    lines = out

    # P2: near-duplicate line elimination (later occurrence dies)
    kept_sigs = []  # (tokenset, is_pin)
    out = []
    ndup = 0
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append(ln)
            continue
        pin = bool(PIN_RE.search(ln))
        tk = tokens(ln)
        near = any(jaccard(tk, kt) >= overlap and not pin and not kp for kt, kp in kept_sigs)
        if near:
            ndup += 1
            continue
        kept_sigs.append((tk, pin))
        out.append(ln)
    fired("P2_neardedupe", ndup)
    lines = out

    # P3: peephole rewrites
    nph = 0
    for i, ln in enumerate(lines):
        new = ln
        for rx, rep in PEEPHOLE:
            new2 = rx.sub(rep, new)
            if new2 != new:
                nph += 1
                new = new2
        lines[i] = new
    fired("P3_peephole", nph)

    # P4: merge overlapping markdown sections (same-signature headers, or same
    # header level whose content token sets overlap >= sect_overlap)
    header_idx = [i for i, ln in enumerate(lines) if re.match(r"^#{1,6}\s+\S", ln)]
    merged = 0
    if header_idx:
        sections = []
        for k, i in enumerate(header_idx):
            j = header_idx[k + 1] if k + 1 < len(header_idx) else len(lines)
            level = len(re.match(r"^#+", lines[i]).group(0))
            body_tk = tokens("\n".join(lines[i:j]))
            sections.append([i, j, signature(re.sub(r"^#+\s*", "", lines[i])), level, body_tk])
        canonical = []  # list of [first_i, first_j, sig, level, tokenset]
        alias = {}
        for sec in sections:
            i, j, sig, level, tk = sec
            target = None
            for ci, c in enumerate(canonical):
                if c[2] == sig or (c[3] == level and jaccard(tk, c[4]) >= sect_overlap):
                    target = ci
                    break
            if target is None:
                canonical.append([i, j, sig, level, tk])
            else:
                alias[i] = target
        appends, skip = {}, set()
        for i, j, sig, level, tk in sections:
            if i in alias:
                merged += 1
                c = canonical[alias[i]]
                fi, fj = c[0], c[1]
                first_sigs = {signature(x) for x in lines[fi:fj] if x.strip()}
                uniq = [ln for ln in lines[i:j]
                        if ln.strip() and signature(ln) not in first_sigs
                        and not PIN_RE.search(ln) and ln not in appends.get(fi, [])]
                appends.setdefault(fi, []).extend(uniq)
                skip.update(range(i, j))
        new_lines = []
        for idx, ln in enumerate(lines):
            if idx in skip:
                continue
            new_lines.append(ln)
            if idx in appends:
                new_lines.extend(appends[idx])
        lines = new_lines
    fired("P4_sectmerge", merged)

    # collapse blank runs
    out, blank = [], 0
    for ln in lines:
        if not ln.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(ln)

    # P6: evidence-channel extraction (release build only). Forensic provenance
    # (paths / dates / shas / counts) on NON-PIN, NON-IMPERATIVE text is
    # evidence, not instruction: bound it to a pointer. Two shapes:
    #   P6a parenthetical spans >= 120 chars with >= 2 receipt tokens
    #   P6b declarative lines with >= 4 receipt tokens: keep first sentence,
    #       elide the provenance tail
    # Pin lines and imperative (executable) lines pass through untouched.
    nev = 0
    elided = set()
    if release:
        RX_RE = re.compile(r"\([^()]{120,}\)")
        RX_TOKEN = re.compile(r"(?:[A-Za-z0-9_\-./\\]{3,}\.\w{2,4}\b|\b20\d{2}[-/]\d{2}[-/]\d{2}\b|\b[a-f0-9]{8,64}\b|\b\d[\d,]{3,}\b)")
        IMP_RE = re.compile(
            r"(?i)\b(read|run|write|check|verify|file|land|send|append|propose|"
            r"distill|probe|skip|execute|amend|list|use|ride|go|do|make|keep|"
            r"take|open|close|stop|start|summarize)\b")
        for i, ln in enumerate(out):
            if PIN_RE.search(ln) or IMP_RE.search(ln):
                continue

            def bound(m):
                nonlocal nev
                hits = RX_TOKEN.findall(m.group(0))
                if len(hits) >= 2:
                    nev += 1
                    elided.update(hits)
                    return "(receipts: %d refs elided, recoverable from compile source)" % len(hits)
                return m.group(0)

            new = RX_RE.sub(bound, ln)
            if new == ln and len(ln) >= 160:
                hits = RX_TOKEN.findall(ln)
                if len(hits) >= 4:
                    first = RX_TOKEN.search(ln)
                    head = ln[:first.start()].rstrip(" ,;:") if first else ""
                    if len(head) < 20:
                        head = ln[:60].rsplit(" ", 1)[0]
                    if head and head != ln:
                        nev += 1
                        elided.update(hits)
                        new = head + " [evidence: %d refs elided]" % len(hits)
            out[i] = new
    fired("P6_evidence", nev)
    stats["elided_refs"] = sorted(elided)

    text_out = "\n".join(out).strip() + "\n"

    # P5: backpatch pins (byte-identical restore)
    missing = [p for p in pins if p not in text_out]
    if missing:
        block = "\n".join("RESTORED-PIN: " + p for p in missing)
        text_out = text_out.rstrip("\n") + "\n\n" + block + "\n"
        stats["restored_pins"] = missing

    stats["bytes_out"] = len(text_out.encode("utf-8"))
    stats["pinned_lines"] = len(pins)
    stats["pinned_preserved"] = len(pins) - len(missing)
    lost = sorted(t for t in fact_tokens if t not in text_out)
    unaccounted = [t for t in lost if t not in elided]
    stats["fact_tokens"] = len(fact_tokens)
    stats["fact_tokens_lost"] = lost
    stats["fact_tokens_unaccounted"] = unaccounted
    stats["factgate"] = "PASS" if not unaccounted else "FAIL"
    stats["sha_in"] = hashlib.sha256(src.encode("utf-8")).hexdigest()[:16]
    stats["sha_out"] = hashlib.sha256(text_out.encode("utf-8")).hexdigest()[:16]
    return text_out, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["compile"])
    ap.add_argument("input")
    ap.add_argument("-o", "--out")
    ap.add_argument("--report")
    ap.add_argument("--release", action="store_true",
                    help="enable P6 evidence-channel extraction (lossy, falsifiable)")
    a = ap.parse_args()
    try:
        src = Path(a.input).read_text(encoding="utf-8")
    except OSError as e:
        print(json.dumps({"error": str(e)}))
        return 2
    out, stats = compile_prompt(src, release=a.release)
    # idempotency probe
    out2, st2 = compile_prompt(out, release=a.release)
    stats["idempotency_residual_bytes"] = max(0, st2["bytes_in"] - st2["bytes_out"])
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
    if a.report:
        Path(a.report).write_text(json.dumps(stats, indent=1), encoding="utf-8")
    r = stats["bytes_out"] / max(1, stats["bytes_in"])
    print(json.dumps({
        "input": a.input, "bytes_in": stats["bytes_in"], "bytes_out": stats["bytes_out"],
        "ratio": round(r, 3), "passes": stats["passes"],
        "pins": stats["pinned_lines"], "pins_preserved": stats["pinned_preserved"],
        "restored": len(stats["restored_pins"]),
        "fact_tokens": stats["fact_tokens"], "fact_tokens_lost": len(stats["fact_tokens_lost"]),
        "factgate": stats["factgate"], "idempotency_residual_bytes": stats["idempotency_residual_bytes"],
        "sha_in": stats["sha_in"], "sha_out": stats["sha_out"],
    }, indent=1))
    return 0 if stats["factgate"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
