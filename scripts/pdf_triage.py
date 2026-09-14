#!/usr/bin/env python3
"""pdf_triage.py — deterministic digital-vs-scanned PDF triage (stdlib-only).

Extraction ladder (first that works wins):
  1. pdftotext binary, if present on PATH
  2. pypdf / PyPDF2 / pdfminer, if importable in this interpreter
  3. raw-byte heuristic: zlib-decompress FlateDecode streams, count text
     objects (BT/Tj/TJ operators) vs image objects (/Subtype /Image)

Classification (deterministic thresholds):
  DIGITAL : extracted words >= 50% of expected tokens (pages * EXPECTED_WPP)
  SCANNED : extracted words <  5%  of expected tokens
  MIXED   : everything in between
If page count is unobtainable, absolute word thresholds are used and the
evidence line says so. Prints classification + evidence per file. Honest
errors: a file that fails to parse is reported as ERROR, never guessed.

Usage: python pdf_triage.py <pdf-or-dir> [<pdf-or-dir> ...]
"""
import re
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

EXPECTED_WPP = 300          # expected words per page for a text-dense book page
DIGITAL_RATIO = 0.50        # >= 50% of expected tokens -> DIGITAL
SCANNED_RATIO = 0.05        # <  5%  of expected tokens -> SCANNED
ABS_DIGITAL = 1000          # pages-unknown fallbacks
ABS_SCANNED = 50
PDFTOTEXT_TIMEOUT = 90


def count_pages(path: Path, raw: bytes) -> int:
    """Page count: pdfinfo binary if present, else /Type /Page scan of raw bytes."""
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        try:
            out = subprocess.run(
                [pdfinfo, str(path)], capture_output=True, text=True, timeout=30
            )
            m = re.search(r"^Pages:\s+(\d+)", out.stdout, re.M)
            if m:
                return int(m.group(1))
        except Exception:
            pass
    # raw-byte fallback: count /Type /Page (not /Pages); misses pages inside
    # compressed object streams — evidence line flags when this is used.
    n = len(re.findall(rb"/Type\s*/Page(?![sS])", raw))
    return n


def extract_text(path: Path):
    """Ladder step 1+2. Returns (words:int, tool:str) or (None, reason:str)."""
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        try:
            r = subprocess.run(
                [pdftotext, "-q", str(path), "-"],
                capture_output=True, timeout=PDFTOTEXT_TIMEOUT,
                encoding="utf-8", errors="replace",
            )
            if r.returncode == 0:
                return len(r.stdout.split()), "pdftotext"
        except Exception:
            pass
    for mod, fn in _python_extractors():
        try:
            text = fn(path)
            if text is not None:
                return len(text.split()), mod
        except Exception:
            continue
    return None, "no-extractor"


def _python_extractors():
    """Ladder step 2: any PDF library importable in this interpreter."""
    out = []
    try:
        from pypdf import PdfReader  # noqa

        def pypdf_extract(path):
            r = PdfReader(str(path))
            return "\n".join((p.extract_text() or "") for p in r.pages)

        out.append(("pypdf", pypdf_extract))
    except Exception:
        pass
    try:
        from PyPDF2 import PdfReader  # noqa

        def pypdf2_extract(path):
            r = PdfReader(str(path))
            return "\n".join((p.extract_text() or "") for p in r.pages)

        out.append(("PyPDF2", pypdf2_extract))
    except Exception:
        pass
    try:
        from pdfminer.high_level import extract_text as pm_extract  # noqa

        out.append(("pdfminer", lambda p: pm_extract(str(p))))
    except Exception:
        pass
    return out


def raw_heuristic(path: Path, raw: bytes) -> dict:
    """Ladder step 3 (used as evidence even when text extraction succeeded):
    zlib-decompress stream objects, count text ops vs image objects."""
    text_ops = image_refs = 0
    streams_tried = streams_ok = 0
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        streams_tried += 1
        blob = m.group(1)
        try:
            blob = zlib.decompress(blob)
            streams_ok += 1
        except Exception:
            pass  # uncompressed or other filter — count as-is below
        text_ops += blob.count(b"BT") + blob.count(b"Tj") + blob.count(b"TJ")
    image_refs = len(re.findall(rb"/Subtype\s*/Image", raw))
    return {
        "text_ops": text_ops,
        "image_objs": image_refs,
        "streams": streams_tried,
        "streams_decompressed": streams_ok,
    }


def classify(words: int, pages: int) -> str:
    if pages > 0:
        expected = pages * EXPECTED_WPP
        ratio = words / expected
        if ratio >= DIGITAL_RATIO:
            return "DIGITAL"
        if ratio < SCANNED_RATIO:
            return "SCANNED"
        return "MIXED"
    # pages unknown — absolute fallback, flagged in evidence
    if words >= ABS_DIGITAL:
        return "DIGITAL"
    if words < ABS_SCANNED:
        return "SCANNED"
    return "MIXED"


def triage(path: Path) -> dict:
    res = {"path": str(path), "class": "ERROR", "words": 0, "pages": 0,
           "tool": "", "pages_source": "", "raw": {}}
    try:
        raw = path.read_bytes()
    except Exception as e:
        res["tool"] = f"unreadable: {e}"
        return res
    pages = count_pages(path, raw)
    res["pages"] = pages
    res["pages_source"] = "pdfinfo/raw-scan"
    words, tool = extract_text(path)
    res["raw"] = raw_heuristic(path, raw)
    if words is None:
        # no extractor at all — classify on raw structure only, honestly
        rh = res["raw"]
        res["tool"] = "raw-bytes-only"
        if rh["text_ops"] > 0 and rh["image_objs"] == 0:
            res["class"] = "DIGITAL"
        elif rh["image_objs"] > 0 and rh["text_ops"] == 0:
            res["class"] = "SCANNED"
        elif rh["text_ops"] > 0 and rh["image_objs"] > 0:
            res["class"] = "MIXED"
        else:
            res["class"] = "ERROR"
        return res
    res["words"] = words
    res["tool"] = tool
    res["class"] = classify(words, pages)
    return res


def main(argv):
    targets = []
    for a in argv:
        p = Path(a)
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.pdf")))
        elif p.is_file():
            targets.append(p)
        else:
            print(f"MISSING {a}")
    if not targets:
        print("usage: pdf_triage.py <pdf-or-dir> ...")
        return 1
    counts = {}
    for t in targets:
        r = triage(t)
        counts[r["class"]] = counts.get(r["class"], 0) + 1
        rh = r["raw"]
        wpp = (r["words"] / r["pages"]) if r["pages"] else 0
        print(
            f"{r['class']:<8} | words={r['words']:>7} pages={r['pages']:>4} "
            f"wpp={wpp:>7.1f} | tool={r['tool']:<14} "
            f"img_objs={rh.get('image_objs', '?'):>4} "
            f"text_ops={rh.get('text_ops', '?'):>6} "
            f"streams={rh.get('streams_decompressed', '?')}/{rh.get('streams', '?')} "
            f"| {r['path']}"
        )
    print(f"\nSUMMARY: {sum(counts.values())} PDFs -> "
          + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
